---
name: agentic-patterns
description: Design and operate multi-agent orchestration patterns (ReAct loops, evaluator-optimizer, orchestrator-workers, tool routing) for LLM systems. Use when building or debugging agent workflows, tool-use loops, or multi-step task delegation; triggers: agentic, multi-agent, orchestration, ReAct, evaluator-optimizer, tool-use, handoff.
---

# Agentic Patterns

## Overview
Use simple, composable patterns to decide when to keep a deterministic workflow versus letting an LLM drive its own control flow with tools, retrieval, and memory. Prefer minimal patterns and add agentic loops only when they unlock necessary flexibility.

## When to Use
- Use this skill when the request matches the frontmatter description and triggers; otherwise start with a deterministic workflow or a single prompt.

## Decision Tree
1. Determine whether the task can be mapped to a fixed sequence.
   - Yes: implement a workflow chain.
   - No: continue.
2. Determine whether the output can be evaluated with explicit criteria.
   - Yes: use an evaluator-optimizer loop.
   - No: continue.
3. Determine whether the task decomposes into independent subtasks.
   - Yes: use orchestrator-workers.
   - No: add a routing step to clarify intent before tool calls.

## Workflows

### 1. Evaluator-Optimizer Loop
1. Define an evaluator rubric with pass/fail criteria and required evidence.
2. Generate an initial draft with the generator.
3. Evaluate the draft with the rubric and capture structured feedback.
4. Feed feedback into the generator and iterate until pass or max iterations.

### 2. Orchestrator-Worker Task Delegation
1. Decompose the request into explicit subtasks with clear outputs.
2. Assign each subtask to a specialized worker prompt or tool.
3. Collect worker outputs and synthesize into a single answer.
4. Run a final verification pass (self-check or evaluator) before returning.

### 3. Tool Poka-Yoke Audit
1. List all tools with names, parameters, and docstrings.
2. Normalize parameter names and enforce concrete types (ids, paths, enums).
3. Add minimal examples and edge cases to each docstring.
4. Re-run a small task to confirm tool selection improves.

## Non-Obvious Insights
- Composability beats complexity: small patterns are more reliable and easier to debug than full frameworks.
- Tool metadata is part of the control surface; sloppy names or parameters cause misrouted tool selection.
- Agentic systems rely on augmentations (retrieval, tools, memory), so design those explicitly, not as afterthoughts.
- Poka-yoke tool design reduces execution errors without changing the model.

## Evidence
- "the most successful implementations use simple, composable patterns rather than complex frameworks." - [Anthropic](https://www.anthropic.com/research/building-effective-agents)
- "Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." - [Anthropic](https://www.anthropic.com/research/building-effective-agents)
- "Evaluator-optimizer: one LLM call generates a response while another provides evaluation and feedback in a loop." - [Anthropic](https://www.anthropic.com/research/building-effective-agents)
- "Poka-yoke your tools. Change the arguments so that it is harder to make mistakes." - [Anthropic](https://www.anthropic.com/research/building-effective-agents)
- "When deciding what tool to use, your agent will use the tool's name, parameters, and docstring... So it's important to make sure the docstrings are descriptive and helpful." - [LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/agent/)

## Scripts
- `scripts/agentic-patterns_tool.py`: CLI scaffolds for evaluator-optimizer, orchestrator-worker, and tool audit patterns.
- `scripts/agentic-patterns_tool.js`: Node.js CLI with the same patterns.

## Dependencies
- Python 3.11+ or Node 18+.
- Optional: your LLM SDK (OpenAI/Anthropic/Gemini) for real generation/evaluation.

## References
- [references/README.md](references/README.md)
