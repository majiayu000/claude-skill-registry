---
name: langchain-agents
description: Building LLM agents with LangChain and LangGraph, covering tool-calling model initialization, state management, and observability with LangSmith. Triggers: langchain, langgraph, langsmith, agent-executor, chat-model-tools.
---

# LangChain Agents

## Overview
LangChain provides a standard interface for building LLM agents that can use tools. Modern agent development is moving toward LangGraph to handle stateful, multi-turn, and non-linear logic that simple loops cannot capture.

## When to Use
- **Multi-Provider Apps**: When you want to swap between OpenAI, Anthropic, and local models without changing business logic.
- **Stateful Agents**: When you need human-in-the-loop, long-term persistence, or complex execution graphs.
- **Observability**: Using LangSmith to debug exactly where an agentic chain failed.

## Decision Tree
1. Is it a simple tool-calling loop? 
   - YES: Use the `create_agent` abstraction.
2. Does it require cycles, complex state transitions, or human approval? 
   - YES: Build using LangGraph.
3. Do you need to track exactly how much an agent run cost or where it halluncinated? 
   - YES: Enable LangSmith tracing.

## Workflows

### 1. Creating a Simple Tool-Enabled Agent
1. Define a Python function with a docstring to serve as a tool.
2. Initialize a ChatModel (e.g., `ChatAnthropic`).
3. Call `create_agent(model, tools=[...])` to generate the agent.
4. Execute the agent using `agent.invoke({"messages": [...]})`.

### 2. Debugging with LangSmith
1. Enable LangSmith environment variables (`LANGSMITH_API_KEY`, `LANGSMITH_TRACING`).
2. Run the agent as usual; traces are automatically captured.
3. Visualize the execution path and captured state transitions in the LangSmith UI to identify where the agent went wrong.

### 3. Adding Memory to an Agent
1. Initialize a `Checkpointer` or `Memory` object.
2. Pass the memory to the agent's invoke call to maintain state across turns.
3. The agent will automatically append tool outputs and model responses to the conversation thread.

## Non-Obvious Insights
- **Abstraction Layer**: LangChain's primary value is standardizing the interface across providers, preventing vendor lock-in.
- **Simple vs. Complex**: For many basic tasks, you don't need LangGraph; the high-level `agent_executor` is often enough for under 10 lines of code.
- **Durable Execution**: Using LangGraph allows for "checkpoints," meaning an agent can stop, wait for human input, and resume hours later without losing state.

## Evidence
- "Standardizes how you interact with models so that you can seamlessly swap providers..." - [LangChain Docs](https://python.langchain.com/docs/concepts/agents/)
- "LangChain agents are built on top of LangGraph in order to provide durable execution, streaming... persistence." - [LangChain Docs](https://python.langchain.com/docs/concepts/agents/)
- "You do not need to know LangGraph for basic LangChain agent usage." - [LangChain Docs](https://python.langchain.com/docs/concepts/agents/)

## Scripts
- `scripts/langchain-agents_tool.py`: Python script for tool definition and agent invocation.
- `scripts/langchain-agents_tool.js`: Equivalent logic using LangChain.js.

## Dependencies
- `langchain`
- `langgraph`
- `langsmith`

## References
- [references/README.md](references/README.md)