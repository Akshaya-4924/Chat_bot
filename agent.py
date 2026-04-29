"""
agent.py - Core LangGraph agent with Planner, Search, Code Writer, Executor, Response Generator
Uses Groq (free) instead of Google Gemini
"""

import os
import subprocess
import tempfile
import json
from typing import TypedDict, Literal
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END

load_dotenv()

# ──────────────────────────────────────────────
# LLM Setup (Groq - FREE)
# ──────────────────────────────────────────────
llm = ChatGroq(
    model="llama3-70b-8192",   # Free, fast, capable model on Groq
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

# ──────────────────────────────────────────────
# Tavily Search Tool
# ──────────────────────────────────────────────
search_tool = TavilySearchResults(
    max_results=3,
    api_key=os.getenv("TAVILY_API_KEY"),
)

# ──────────────────────────────────────────────
# Agent State
# ──────────────────────────────────────────────
class AgentState(TypedDict):
    question: str
    action: str          # "search" | "code"
    search_results: list
    code: str
    execution_output: str
    execution_error: str
    answer: str
    sources: list

# ──────────────────────────────────────────────
# Node 1: Planner
# ──────────────────────────────────────────────
def planner_node(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""You are a decision-making agent. Given a user question, decide which tool to use.

Rules:
- If the question asks for current events, news, facts about the real world, prices, recent info → respond with: search
- If the question asks to calculate, compute, generate code, solve math, or run a program → respond with: code
- For general/simple questions you can answer from knowledge → respond with: search

User question: {question}

Respond with ONLY one word: either "search" or "code". Nothing else."""

    response = llm.invoke(prompt)
    action = response.content.strip().lower()

    if action not in ["search", "code"]:
        action = "search"  # safe default

    return {**state, "action": action}

# ──────────────────────────────────────────────
# Node 2: Search Tool
# ──────────────────────────────────────────────
def search_node(state: AgentState) -> AgentState:
    question = state["question"]

    try:
        results = search_tool.invoke(question)
        sources = [r.get("url", "") for r in results if isinstance(r, dict)]
        return {**state, "search_results": results, "sources": sources}
    except Exception as e:
        return {**state, "search_results": [], "sources": [], "execution_error": str(e)}

# ──────────────────────────────────────────────
# Node 3: Code Writer
# ──────────────────────────────────────────────
def code_writer_node(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""You are a Python code generator. Write clean, executable Python code to answer the user's request.

Rules:
- Output ONLY valid Python code. No markdown. No explanation. No backticks.
- Use print() to display the final result.
- Keep the code simple and correct.
- Do not import external libraries that are not part of Python's standard library (no pandas, numpy, etc.)

User request: {question}

Python code:"""

    response = llm.invoke(prompt)
    code = response.content.strip()

    # Strip accidental markdown fences if model includes them
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    return {**state, "code": code}

# ──────────────────────────────────────────────
# Node 4: Code Executor
# ──────────────────────────────────────────────
def code_executor_node(state: AgentState) -> AgentState:
    code = state.get("code", "")

    if not code:
        return {**state, "execution_output": "", "execution_error": "No code to execute."}

    try:
        # Write code to a temp file and run safely via subprocess
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=15,   # 15-second safety timeout
        )

        os.unlink(tmp_path)  # clean up temp file

        return {
            **state,
            "execution_output": result.stdout.strip(),
            "execution_error": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {**state, "execution_output": "", "execution_error": "Code execution timed out (15s limit)."}
    except Exception as e:
        return {**state, "execution_output": "", "execution_error": str(e)}

# ──────────────────────────────────────────────
# Node 5: Response Generator
# ──────────────────────────────────────────────
def response_generator_node(state: AgentState) -> AgentState:
    question = state["question"]
    action = state.get("action", "search")

    if action == "search":
        results = state.get("search_results", [])
        context = "\n\n".join(
            [f"Source: {r.get('url','')}\n{r.get('content','')}" for r in results if isinstance(r, dict)]
        )
        prompt = f"""You are a helpful assistant. Answer the user's question based on these search results.

Question: {question}

Search Results:
{context}

Give a clear, concise answer in 2-4 sentences."""

    else:
        exec_output = state.get("execution_output", "")
        exec_error = state.get("execution_error", "")
        code = state.get("code", "")

        prompt = f"""You are a helpful assistant. Explain the result of running this Python code.

Question: {question}
Code:
{code}

Output: {exec_output}
Error: {exec_error}

Write a clear, friendly explanation of the result for the user. If there was an error, explain what went wrong."""

    response = llm.invoke(prompt)
    return {**state, "answer": response.content.strip()}

# ──────────────────────────────────────────────
# Routing Logic
# ──────────────────────────────────────────────
def route_action(state: AgentState) -> Literal["search", "code_writer"]:
    return "search" if state["action"] == "search" else "code_writer"

# ──────────────────────────────────────────────
# Build LangGraph
# ──────────────────────────────────────────────
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("code_writer", code_writer_node)
    graph.add_node("code_executor", code_executor_node)
    graph.add_node("response_generator", response_generator_node)

    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", route_action, {
        "search": "search",
        "code_writer": "code_writer",
    })
    graph.add_edge("search", "response_generator")
    graph.add_edge("code_writer", "code_executor")
    graph.add_edge("code_executor", "response_generator")
    graph.add_edge("response_generator", END)

    return graph.compile()


agent_graph = build_graph()


def run_agent(question: str) -> dict:
    """Run the agent and return a structured result."""
    initial_state: AgentState = {
        "question": question,
        "action": "",
        "search_results": [],
        "code": "",
        "execution_output": "",
        "execution_error": "",
        "answer": "",
        "sources": [],
    }

    final_state = agent_graph.invoke(initial_state)

    return {
        "answer": final_state.get("answer", ""),
        "code": final_state.get("code", ""),
        "execution_output": final_state.get("execution_output", ""),
        "execution_error": final_state.get("execution_error", ""),
        "sources": final_state.get("sources", []),
        "action": final_state.get("action", ""),
    }
