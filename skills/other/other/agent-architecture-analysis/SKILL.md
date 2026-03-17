---
name: agent-architecture-analysis
description: Perform 12-Factor Agents compliance analysis on any codebase. Use when evaluating agent architecture, reviewing LLM-powered systems, or auditing agentic applications against the 12-Factor methodology.
---

# 12-Factor Agents Compliance Analysis

> Reference: [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

## Input Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `docs_path` | Path to documentation directory (for existing analyses) | Optional |
| `codebase_path` | Root path of the codebase to analyze | Required |

## Analysis Framework

### Factor 1: Natural Language to Tool Calls

**Principle:** Convert natural language inputs into structured, deterministic tool calls using schema-validated outputs.

**Search Patterns:**
```bash
# Look for Pydantic schemas
grep -r "class.*BaseModel" --include="*.py"
grep -r "TaskDAG\|TaskResponse\|ToolCall" --include="*.py"

# Look for JSON schema generation
grep -r "model_json_schema\|json_schema" --include="*.py"

# Look for structured output generation
grep -r "output_type\|response_model" --include="*.py"
```

**File Patterns:** `**/agents/*.py`, `**/schemas/*.py`, `**/models/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | All LLM outputs use Pydantic/dataclass schemas with validators |
| **Partial** | Some outputs typed, but dict returns or unvalidated strings exist |
| **Weak** | LLM returns raw strings parsed manually or with regex |

**Anti-patterns:**
- `json.loads(llm_response)` without schema validation
- `output.split()` or regex parsing of LLM responses
- `dict[str, Any]` return types from agents
- No validation between LLM output and handler execution

---

### Factor 2: Own Your Prompts

**Principle:** Treat prompts as first-class code you control, version, and iterate on.

**Search Patterns:**
```bash
# Look for embedded prompts
grep -r "SYSTEM_PROMPT\|system_prompt" --include="*.py"
grep -r '""".*You are' --include="*.py"

# Look for template systems
grep -r "jinja\|Jinja\|render_template" --include="*.py"
find . -name "*.jinja2" -o -name "*.j2"

# Look for prompt directories
find . -type d -name "prompts"
```

**File Patterns:** `**/prompts/**`, `**/templates/**`, `**/agents/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Prompts in separate files, templated (Jinja2), versioned |
| **Partial** | Prompts as module constants, some parameterization |
| **Weak** | Prompts hardcoded inline in functions, f-strings only |

**Anti-patterns:**
- `f"You are a {role}..."` inline in agent methods
- Prompts mixed with business logic
- No way to iterate on prompts without code changes
- No prompt versioning or A/B testing capability

---

### Factor 3: Own Your Context Window

**Principle:** Control how history, state, and tool results are formatted for the LLM.

**Search Patterns:**
```bash
# Look for context/message management
grep -r "AgentMessage\|ChatMessage\|messages" --include="*.py"
grep -r "context_window\|context_compiler" --include="*.py"

# Look for custom serialization
grep -r "to_xml\|to_context\|serialize" --include="*.py"

# Look for token management
grep -r "token_count\|max_tokens\|truncate" --include="*.py"
```

**File Patterns:** `**/context/*.py`, `**/state/*.py`, `**/core/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Custom context format, token optimization, typed events, compaction |
| **Partial** | Basic message history with some structure |
| **Weak** | Raw message accumulation, standard OpenAI format only |

**Anti-patterns:**
- Unbounded message accumulation
- Large artifacts embedded inline (diffs, files)
- No agent-specific context filtering
- Same context for all agent types

---

### Factor 4: Tools Are Structured Outputs

**Principle:** Tools produce schema-validated JSON that triggers deterministic code, not magic function calls.

**Search Patterns:**
```bash
# Look for tool/response schemas
grep -r "class.*Response.*BaseModel" --include="*.py"
grep -r "ToolResult\|ToolOutput" --include="*.py"

# Look for deterministic handlers
grep -r "def handle_\|def execute_" --include="*.py"

# Look for validation layer
grep -r "model_validate\|parse_obj" --include="*.py"
```

**File Patterns:** `**/tools/*.py`, `**/handlers/*.py`, `**/agents/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | All tool outputs schema-validated, handlers type-safe |
| **Partial** | Most tools typed, some loose dict returns |
| **Weak** | Tools return arbitrary dicts, no validation layer |

**Anti-patterns:**
- Tool handlers that directly execute LLM output
- `eval()` or `exec()` on LLM-generated code
- No separation between decision (LLM) and execution (code)
- Magic method dispatch based on string matching

---

### Factor 5: Unify Execution State

**Principle:** Merge execution state (step, retries) with business state (messages, results).

**Search Patterns:**
```bash
# Look for state models
grep -r "ExecutionState\|WorkflowState\|Thread" --include="*.py"

# Look for dual state systems
grep -r "checkpoint\|MemorySaver" --include="*.py"
grep -r "sqlite\|database\|repository" --include="*.py"

# Look for state reconstruction
grep -r "load_state\|restore\|reconstruct" --include="*.py"
```

**File Patterns:** `**/state/*.py`, `**/models/*.py`, `**/database/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Single serializable state object with all execution metadata |
| **Partial** | State exists but split across systems (memory + DB) |
| **Weak** | Execution state scattered, requires multiple queries to reconstruct |

**Anti-patterns:**
- Retry count stored separately from task state
- Error history in logs but not in state
- LangGraph checkpoints + separate database storage
- No unified event thread

---

### Factor 6: Launch/Pause/Resume

**Principle:** Agents support simple APIs for launching, pausing at any point, and resuming.

**Search Patterns:**
```bash
# Look for REST endpoints
grep -r "@router.post\|@app.post" --include="*.py"
grep -r "start_workflow\|pause\|resume" --include="*.py"

# Look for interrupt mechanisms
grep -r "interrupt_before\|interrupt_after" --include="*.py"

# Look for webhook handlers
grep -r "webhook\|callback" --include="*.py"
```

**File Patterns:** `**/routes/*.py`, `**/api/*.py`, `**/orchestrator/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | REST API + webhook resume, pause at any point including mid-tool |
| **Partial** | Launch/pause/resume exists but only at coarse-grained points |
| **Weak** | CLI-only launch, no pause/resume capability |

**Anti-patterns:**
- Blocking `input()` or `confirm()` calls
- No way to resume after process restart
- Approval only at plan level, not per-tool
- No webhook-based resume from external systems

---

### Factor 7: Contact Humans with Tools

**Principle:** Human contact is a tool call with question, options, and urgency.

**Search Patterns:**
```bash
# Look for human input mechanisms
grep -r "typer.confirm\|input(\|prompt(" --include="*.py"
grep -r "request_human_input\|human_contact" --include="*.py"

# Look for approval patterns
grep -r "approval\|approve\|reject" --include="*.py"

# Look for structured question formats
grep -r "question.*options\|HumanInputRequest" --include="*.py"
```

**File Patterns:** `**/agents/*.py`, `**/tools/*.py`, `**/orchestrator/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | `request_human_input` tool with question/options/urgency/format |
| **Partial** | Approval gates exist but hardcoded in graph structure |
| **Weak** | Blocking CLI prompts, no tool-based human contact |

**Anti-patterns:**
- `typer.confirm()` in agent code
- Human contact hardcoded at specific graph nodes
- No way for agents to ask clarifying questions
- Single response format (yes/no only)

---

### Factor 8: Own Your Control Flow

**Principle:** Custom control flow, not framework defaults. Full control over routing, retries, compaction.

**Search Patterns:**
```bash
# Look for routing logic
grep -r "add_conditional_edges\|route_\|should_continue" --include="*.py"

# Look for custom loops
grep -r "while True\|for.*in.*range" --include="*.py" | grep -v test

# Look for execution mode control
grep -r "execution_mode\|agentic\|structured" --include="*.py"
```

**File Patterns:** `**/orchestrator/*.py`, `**/graph/*.py`, `**/core/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Custom routing functions, conditional edges, execution mode control |
| **Partial** | Framework control flow with some customization |
| **Weak** | Default framework loop with no custom routing |

**Anti-patterns:**
- Single path through graph with no branching
- No distinction between tool types (all treated same)
- Framework-default error handling only
- No rate limiting or resource management

---

### Factor 9: Compact Errors into Context

**Principle:** Errors in context enable self-healing. Track consecutive errors, escalate after threshold.

**Search Patterns:**
```bash
# Look for error handling
grep -r "except.*Exception\|error_history\|consecutive_errors" --include="*.py"

# Look for retry logic
grep -r "retry\|backoff\|max_attempts" --include="*.py"

# Look for escalation
grep -r "escalate\|human_escalation" --include="*.py"
```

**File Patterns:** `**/agents/*.py`, `**/orchestrator/*.py`, `**/core/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Errors in context, retry with threshold, automatic escalation |
| **Partial** | Errors logged and returned, no automatic retry loop |
| **Weak** | Errors logged only, not fed back to LLM, task fails immediately |

**Anti-patterns:**
- `logger.error()` without adding to context
- No retry mechanism (fail immediately)
- No consecutive error tracking
- No escalation to humans after repeated failures

---

### Factor 10: Small, Focused Agents

**Principle:** Each agent has narrow responsibility, 3-10 steps max.

**Search Patterns:**
```bash
# Look for agent classes
grep -r "class.*Agent\|class.*Architect\|class.*Developer" --include="*.py"

# Look for step definitions
grep -r "steps\|tasks" --include="*.py" | head -20

# Count methods per agent
grep -r "async def\|def " agents/*.py 2>/dev/null | wc -l
```

**File Patterns:** `**/agents/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | 3+ specialized agents, each with single responsibility, step limits |
| **Partial** | Multiple agents but some have broad scope |
| **Weak** | Single "god" agent that handles everything |

**Anti-patterns:**
- Single agent with 20+ tools
- Agent with unbounded step count
- Mixed responsibilities (planning + execution + review)
- No step or time limits on agent execution

---

### Factor 11: Trigger from Anywhere

**Principle:** Workflows triggerable from CLI, REST, WebSocket, Slack, webhooks, etc.

**Search Patterns:**
```bash
# Look for entry points
grep -r "@cli.command\|@router.post\|@app.post" --include="*.py"

# Look for WebSocket support
grep -r "WebSocket\|websocket" --include="*.py"

# Look for external integrations
grep -r "slack\|discord\|webhook" --include="*.py" -i
```

**File Patterns:** `**/routes/*.py`, `**/cli/*.py`, `**/main.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | CLI + REST + WebSocket + webhooks + chat integrations |
| **Partial** | CLI + REST API available |
| **Weak** | CLI only, no programmatic access |

**Anti-patterns:**
- Only `if __name__ == "__main__"` entry point
- No REST API for external systems
- No event streaming for real-time updates
- Trigger logic tightly coupled to execution

---

### Factor 12: Stateless Reducer

**Principle:** Agents as pure functions: (state, input) -> (state, output). No side effects in agent logic.

**Search Patterns:**
```bash
# Look for state mutation patterns
grep -r "\.status = \|\.field = " --include="*.py"

# Look for immutable updates
grep -r "model_copy\|\.copy(\|with_" --include="*.py"

# Look for side effects in agents
grep -r "write_file\|subprocess\|requests\." agents/*.py 2>/dev/null
```

**File Patterns:** `**/agents/*.py`, `**/nodes/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Immutable state updates, side effects isolated to tools/handlers |
| **Partial** | Mostly immutable, some in-place mutations |
| **Weak** | State mutated in place, side effects mixed with agent logic |

**Anti-patterns:**
- `state.field = new_value` (mutation)
- File writes inside agent methods
- HTTP calls inside agent decision logic
- Shared mutable state between agents

---

### Factor 13: Pre-fetch Context

**Principle:** Fetch likely-needed data upfront rather than mid-workflow.

**Search Patterns:**
```bash
# Look for context pre-fetching
grep -r "pre_fetch\|prefetch\|fetch_context" --include="*.py"

# Look for RAG/embedding systems
grep -r "embedding\|vector\|semantic_search" --include="*.py"

# Look for related file discovery
grep -r "related_tests\|similar_\|find_relevant" --include="*.py"
```

**File Patterns:** `**/context/*.py`, `**/retrieval/*.py`, `**/rag/*.py`

**Compliance Criteria:**

| Level | Criteria |
|-------|----------|
| **Strong** | Automatic pre-fetch of related tests, files, docs before planning |
| **Partial** | Manual context passing, design doc support |
| **Weak** | No pre-fetching, LLM must request all context via tools |

**Anti-patterns:**
- Architect starts with issue only, no codebase context
- No semantic search for similar past work
- Related tests/files discovered only during execution
- No RAG or document retrieval system

---

## Output Format

### Executive Summary Table

```markdown
| Factor | Status | Notes |
|--------|--------|-------|
| 1. Natural Language -> Tool Calls | **Strong/Partial/Weak** | [Key finding] |
| 2. Own Your Prompts | **Strong/Partial/Weak** | [Key finding] |
| ... | ... | ... |
| 13. Pre-fetch Context | **Strong/Partial/Weak** | [Key finding] |

**Overall**: X Strong, Y Partial, Z Weak
```

### Per-Factor Analysis

For each factor, provide:

1. **Current Implementation**
   - Evidence with file:line references
   - Code snippets showing patterns

2. **Compliance Level**
   - Strong/Partial/Weak with justification

3. **Gaps**
   - What's missing vs. 12-Factor ideal

4. **Recommendations**
   - Actionable improvements with code examples

---

## Analysis Workflow

1. **Initial Scan**
   - Run search patterns for all factors
   - Identify key files for each factor
   - Note any existing compliance documentation

2. **Deep Dive** (per factor)
   - Read identified files
   - Evaluate against compliance criteria
   - Document evidence with file paths

3. **Gap Analysis**
   - Compare current vs. 12-Factor ideal
   - Identify anti-patterns present
   - Prioritize by impact

4. **Recommendations**
   - Provide actionable improvements
   - Include before/after code examples
   - Reference roadmap if exists

5. **Summary**
   - Compile executive summary table
   - Highlight strengths and critical gaps
   - Suggest priority order for improvements

---

## Quick Reference: Compliance Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| **Strong** | Fully implements principle | Maintain, minor optimizations |
| **Partial** | Some implementation, significant gaps | Planned improvements |
| **Weak** | Minimal or no implementation | High priority for roadmap |

## When to Use This Skill

- Evaluating new LLM-powered systems
- Reviewing agent architecture decisions
- Auditing production agentic applications
- Planning improvements to existing agents
- Comparing frameworks or implementations
