---
name: google-adk
description: |
  Guide for building AI agents with Google ADK (Agent Development Kit). Use when creating multi-agent pipelines, implementing conditional agent branching, designing agent tools with FunctionTool, or debugging agent data flow issues. Covers SequentialAgent, LoopAgent, ParallelAgent patterns, session.state management, output_key chaining, and transfer_to_agent for control flow. Essential for understanding non-obvious ADK behaviors like why SequentialAgent runs ALL agents even after rejection.
---

# Google ADK Agent Development

## Critical Architecture Insight

**SequentialAgent runs ALL sub-agents unconditionally.** There is NO native conditional branching. The pipeline does not stop if an agent outputs "REJECT" or any other signal.

```python
# THIS RUNS ALL 4 AGENTS regardless of gatekeeper output
research_cycle = SequentialAgent(
    sub_agents=[theorist, critic, gatekeeper, architect]
)
```

To skip agents, use `transfer_to_agent` tool.

## Data Flow: output_key -> session.state -> {placeholder}

```python
# Agent A stores output
agent_a = Agent(
    instruction="Generate hypothesis",
    output_key="hypothesis"  # Stored in session.state["hypothesis"]
)

# Agent B reads via placeholder
agent_b = Agent(
    instruction="""
    Critique this hypothesis:
    {hypothesis}
    """,  # Resolved from session.state at runtime
    output_key="critique"
)
```

Placeholders support optional syntax: `{variable?}` (no error if missing).

## Conditional Branching with transfer_to_agent

```python
from google.adk.tools import transfer_to_agent

gatekeeper = Agent(
    name="gatekeeper",
    instruction="""
    Decide: PROCEED, REVISE, or REJECT

    - PROCEED: Continue normally (don't call transfer_to_agent)
    - REVISE: Call transfer_to_agent("theorist")
    - REJECT: Call transfer_to_agent("reporter") to skip experiment
    """,
    tools=[transfer_to_agent],
    output_key="gate_decision"
)
```

The runner sees `event.actions.transfer_to_agent` and jumps to that agent.

## FunctionTool Design

### Automatic tool_context injection

```python
def my_tool(
    query: str,                    # From LLM function call
    limit: int = 10,               # Optional parameter
    tool_context: ToolContext      # Auto-injected, never passed by LLM
) -> str:
    # Access session state
    session = tool_context.invocation_context.session
    previous = session.state.get("previous_result")
    return f"Result for {query}"

my_tool_wrapped = FunctionTool(func=my_tool)
```

### Docstring becomes tool description

```python
def search_papers(query: str, tool_context: ToolContext) -> str:
    """
    Search academic papers on arXiv.

    Args:
        query: Search terms for paper lookup

    Returns:
        Formatted list of matching papers
    """
```

The docstring is sent to the LLM as the tool description.

## Agent Types

| Type | Behavior |
|------|----------|
| `Agent` (LlmAgent) | Single LLM agent with tools |
| `SequentialAgent` | Runs sub_agents in order, ALL of them |
| `LoopAgent` | Repeats until `escalate=True` or max_iterations |
| `ParallelAgent` | Runs sub_agents concurrently with branch isolation |

## Common Pitfalls

### 1. Expecting SequentialAgent to stop on rejection
```python
# WRONG: Architect runs even if gatekeeper rejects
SequentialAgent(sub_agents=[theorist, gatekeeper, architect])

# RIGHT: Gatekeeper uses transfer_to_agent to skip
gatekeeper = Agent(
    tools=[transfer_to_agent],
    instruction="If REJECT, call transfer_to_agent('reporter')"
)
```

### 2. Missing output_key breaks data flow
```python
# WRONG: No output_key, next agent can't access result
theorist = Agent(instruction="Generate hypothesis")

# RIGHT: Output stored in session.state
theorist = Agent(instruction="...", output_key="hypothesis")
```

### 3. Placeholder without matching output_key
```python
# WRONG: {analysis} referenced but no agent sets output_key="analysis"
editor = Agent(instruction="Review: {analysis}")

# Debug: Check which agents set output_key
```

### 4. tool_context as required parameter
```python
# WRONG: tool_context has no default, LLM can't call it
def bad_tool(query: str, tool_context: ToolContext) -> str: ...

# RIGHT: Default allows LLM to omit it (auto-injected anyway)
def good_tool(query: str, tool_context: ToolContext = None) -> str: ...
```

### 5. launch_persistent_context returns BrowserContext
```python
# Type hint should be BrowserContext, not Browser
self._browser: Optional[BrowserContext] = None
self._browser = playwright.chromium.launch_persistent_context(...)
```

### 6. Context overflow from session history (token limit exceeded)
ADK stores all conversation history in session.db which gets sent to the LLM. This causes "input token count exceeds maximum" errors.

```python
# WRONG: Agent loads full conversation history (can exceed 128K+ tokens)
root_agent = Agent(name="my_agent", model=MODEL)

# RIGHT: Prevent loading conversation history
root_agent = Agent(
    name="my_agent",
    model=MODEL,
    include_contents='none',  # Stateless - no prior context
)
```

Also clear `.adk/session.db` files when they grow too large:
```bash
rm -rf ika_agent/.adk/session.db
```

## Control Flow Actions

```python
# From tool or callback
tool_context.actions.transfer_to_agent = "agent_name"  # Jump to agent
tool_context.actions.escalate = True                    # Exit loop
tool_context.actions.skip_summarization = True          # Skip post-tool summary

# State updates
event.actions.state_delta = {"key": "value"}            # Update session.state
```

## Thread Safety for Shared State

When tools share global state:

```python
import threading

memory_lock = threading.Lock()

def save_result(data: str, tool_context: ToolContext) -> str:
    global shared_state
    with memory_lock:
        shared_state = reload_from_disk()  # Get fresh state
        shared_state.append(data)
        save_to_disk(shared_state)
    return "Saved"
```

## Sub-Agent Hierarchy

```python
root_agent = Agent(
    name="orchestrator",
    sub_agents=[
        SequentialAgent(
            name="pipeline",
            sub_agents=[agent_a, agent_b, agent_c]
        ),
        standalone_agent,
    ],
    instruction="""
    Commands:
    - "run pipeline" -> Transfer to pipeline
    - "analyze" -> Transfer to standalone_agent
    """,
    tools=[transfer_to_agent]
)
```

All agents in SequentialAgent share the same `session.state`.

## Computer Use Model

Computer use requires dedicated model - **no Gemini 3 version exists yet**:
```python
COMPUTER_USE_MODEL = "gemini-2.5-computer-use-preview-10-2025"
```

Standard agents can use `gemini-3-flash-preview`, but browser automation agents must use the 2.5 computer use model.

## Skill Maintenance

When discovering new ADK patterns through actual code execution, add them to this skill file at `C:\Users\cuba6\.claude\skills\google-adk\SKILL.md`. Only add 100% verified behaviors - no assumptions.

## Resources

- **GitHub**: https://github.com/google/adk-python
- **Docs**: https://google.github.io/adk-docs/
- **Source**: Explore installed package at `google/adk/agents/` and `google/adk/tools/`
