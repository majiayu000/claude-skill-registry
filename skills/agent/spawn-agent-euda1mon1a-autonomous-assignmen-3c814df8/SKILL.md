---
name: spawn-agent
description: Spawn PAI agents via MCP factory tool. Loads identity, injects RAG context, validates spawn chain, and executes via Task(). The bridge between MCP tools and Claude Code's agent spawning.
model_tier: sonnet
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [spawn-agent]
  preferred_batch_size: 1
context_hints:
  max_file_context: 50
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "spawn chain violation"
    reason: "Parent agent lacks authority to spawn requested child"
  - pattern: "identity.*not found"
    reason: "Agent identity card missing - needs creation"
  - keyword: ["Deputy", "opus"]
    reason: "Deputy spawns require ORCHESTRATOR approval"
---

# Spawn Agent Skill

> **Purpose:** Spawn PAI agents using MCP factory pattern
> **Created:** 2026-01-16
> **Trigger:** `/spawn-agent <agent_name> <mission>`
> **Model Tier:** Sonnet (Execution)

---

## Overview

This skill bridges MCP tools with Claude Code's Task() function for agent spawning.

**The Pattern:**
1. MCP `spawn_agent_tool` prepares context (identity, RAG, skills)
2. Claude Code executes via `Task(prompt=spec.full_prompt, ...)`
3. Spawned agent runs with full Claude Code capabilities

**Why This Exists:**
- No API keys needed in MCP server
- Spawned agents have Edit/Write/Bash/MCP tool access
- Governance (spawn chain, audit trail) enforced centrally

---

## When to Use

### Use This Skill When:
- Need to spawn a PAI agent for a specific mission
- Orchestrating multi-agent workflows
- Delegating domain-specific work to specialists
- Need RAG context injected into agent prompt

### Do NOT Use When:
- Simple single-shot tasks (just do it directly)
- Research/exploration (use `/search-party` instead)
- Need to create a new agent (use `/agent-factory` instead)

---

## Usage

### Basic Syntax

```
/spawn-agent AGENT_NAME mission description here
```

### Examples

```
/spawn-agent SCHEDULER Generate Block 10 schedule with ACGME compliance
/spawn-agent COMPLIANCE_AUDITOR Audit Block 10 for work hour violations
/spawn-agent G2_RECON Find all constraint implementations in the codebase
/spawn-agent COORD_ENGINE Optimize solver performance for schedule generation
```

### With Parent Context (for spawn chain validation)

```
/spawn-agent SCHEDULER Generate Block 10 --parent COORD_ENGINE
```

---

## Execution Protocol

When `/spawn-agent` is invoked, follow these steps:

### Step 1: Load MCP Tool

```python
# First, load the spawn_agent_tool
MCPSearch(query="select:mcp__residency-scheduler__spawn_agent_tool")
```

### Step 2: Call spawn_agent_tool

```python
spec = mcp__residency-scheduler__spawn_agent_tool(
    agent_name="AGENT_NAME",
    mission="The mission description",
    context={"relevant": "context"},  # Optional
    inject_rag=True,                   # Default: True
    inject_skills=None,                # Auto-match if None
    parent_agent="PARENT_NAME"         # Optional, for spawn chain
)
```

### Step 3: Validate Response

Check the returned spec for:
- `spawn_chain_valid`: Must be True (or no parent specified)
- `identity_found`: Must be True
- `tier` and `model`: Determine execution parameters

If validation fails:
```python
if not spec["spawn_chain_valid"]:
    # Escalate: parent cannot spawn this child
    raise SpawnChainViolation(spec["spawn_chain_error"])

if not spec["identity_found"]:
    # Escalate: need to create identity card first
    raise IdentityNotFound(f"Create identity: .claude/Identities/{agent_name}.identity.md")
```

### Step 4: Execute via Task()

```python
result = Task(
    prompt=spec["full_prompt"],
    subagent_type=spec["subagent_type"],  # "general-purpose"
    model=spec["model"],                   # haiku/sonnet/opus
    max_turns=spec["max_turns"],           # 5/20/50 based on tier
    description=f"{spec['agent_name']}: {mission[:30]}..."
)
```

### Step 5: Handle Checkpoint (Optional)

If the agent needs to persist state:
```python
# Agent writes checkpoint to spec["checkpoint_path"]
# Example: .claude/Scratchpad/AGENT_SCHEDULER_20260116_143022.md

# To resume later:
# Read checkpoint, include in next spawn's context
```

---

## Tier-Based Execution

| Tier | Model | Max Turns | Use Case |
|------|-------|-----------|----------|
| **Specialist** | haiku | 5 | Single-shot focused tasks |
| **Coordinator** | sonnet | 20 | Multi-step domain work |
| **Deputy** | opus | 50 | Strategic cross-domain work |
| **G-Staff** | sonnet | 15 | Advisory/research roles |

**Rule:** Match task complexity to tier. Don't spawn opus for simple validation.

---

## Spawn Chain Validation

The MCP tool validates that parent agents can spawn children:

```yaml
# From agents.yaml
COORD_ENGINE:
  can_spawn: [SCHEDULER, SWAP_MANAGER, OPTIMIZATION_SPECIALIST]

ARCHITECT:
  can_spawn: [COORD_PLATFORM, COORD_QUALITY, COORD_ENGINE, ...]
```

**If spawn chain fails:**
- Error message tells you who CAN spawn this agent
- Escalate to the correct parent or ORCHESTRATOR

---

## Spawning Constraints (Session 138 Discovery)

### Task() Availability by Spawner

| Spawner | Has Task()? | Spawn Method |
|---------|-------------|--------------|
| ORCHESTRATOR (main session) | Yes | Use `Task()` directly |
| Deputy/Coordinator/Specialist (via Task) | No | Use CLI spawning |
| Agent spawned via CLI | Yes | Use `Task()` directly |

### Why This Matters

Subagents spawned via `Task()` do NOT have `Task()` available. They have all other tools (Bash, Edit, MCP, etc.) but cannot spawn further agents via Task().

**Two working patterns:**

**Pattern A: Flat Parallelism (ORCHESTRATOR spawns all)**
```
ORCHESTRATOR ──┬── Agent 1 (no Task(), works directly)
               ├── Agent 2 (no Task(), works directly)
               └── Agent N (no Task(), works directly)
```

**Pattern B: CLI Spawning (for hierarchical)**
```
ORCHESTRATOR ── Coordinator (via Task, no Task())
                     │
                     └── Bash: claude -p → Specialist (HAS Task())
                                               │
                                               └── Can spawn further agents
```

### CLI Spawning Syntax

When a subagent needs to spawn another agent:

```bash
claude -p "
You are SPECIALIST.

## Identity
[Include identity card content or key details]

## Mission
[Mission description with full context]

## Constraints
- Budget: Do not exceed this mission scope
- Report: Write findings to [path]
" --model haiku --max-budget-usd 1.00
```

**Key points:**
- CLI agents have full capabilities including Task()
- Context must be passed in prompt (same as Task() spawning)
- Use `--max-budget-usd` to prevent runaway costs
- Spawn chain validation is NOT enforced via CLI (governance by convention)

---

## RAG Injection

By default, `inject_rag=True` queries relevant context:

```python
# spawn_agent_tool internally does:
rag_results = rag_search(
    query=mission,
    doc_types=agent.relevant_doc_types,  # From agents.yaml
    top_k=5
)
```

**To disable (faster, less context):**
```
spec = spawn_agent_tool(..., inject_rag=False)
```

---

## Checkpoint Protocol

Agents can persist state for resumption:

### Writing Checkpoint (in spawned agent)

```markdown
# .claude/Scratchpad/AGENT_SCHEDULER_20260116_143022.md

## Agent Checkpoint

**Agent:** SCHEDULER
**Mission:** Generate Block 10 schedule
**Status:** In Progress
**Timestamp:** 2026-01-16T14:30:22

### Progress
- [x] Loaded constraints
- [x] Ran solver (15 solutions found)
- [ ] Validation pending

### State
```json
{
  "block_number": 10,
  "solutions_found": 15,
  "best_objective": 0.87
}
```

### Next Steps
1. Validate ACGME compliance on top 3 solutions
2. Select best based on fairness metric
3. Write to database
```

### Resuming from Checkpoint

```python
# Read checkpoint
checkpoint = Read(".claude/Scratchpad/AGENT_SCHEDULER_20260116_143022.md")

# Include in new spawn context
spec = spawn_agent_tool(
    agent_name="SCHEDULER",
    mission="RESUME: Complete Block 10 schedule generation",
    context={"checkpoint": checkpoint}
)
```

---

## Audit Trail

Every spawn is logged to `.claude/History/agent_invocations/`:

```json
{
  "invocation_id": "20260116_143022_SCHEDULER",
  "timestamp": "2026-01-16T14:30:22",
  "agent_name": "SCHEDULER",
  "tier": "Specialist",
  "model": "haiku",
  "mission": "Generate Block 10 schedule",
  "parent_agent": "COORD_ENGINE",
  "spawn_chain_valid": true,
  "rag_injected": true,
  "checkpoint_path": ".claude/Scratchpad/AGENT_SCHEDULER_20260116_143022.md"
}
```

---

## Error Handling

### Identity Not Found

```
Error: Identity card not found for agent: NEW_AGENT

Resolution:
1. Check if agent exists in .claude/agents.yaml
2. If not, use /agent-factory to create the agent
3. Create identity card at .claude/Identities/NEW_AGENT.identity.md
```

### Spawn Chain Violation

```
Error: Spawn chain violation: SCHEDULER cannot spawn ARCHITECT

Resolution:
1. SCHEDULER can only spawn: [] (no children)
2. ARCHITECT should be spawned by: ORCHESTRATOR
3. Escalate to correct parent or invoke as ORCHESTRATOR
```

### Registry Not Found

```
Error: Agent registry not found at .claude/agents.yaml

Resolution:
1. Verify .claude/agents.yaml exists
2. Check for YAML syntax errors
3. Regenerate from identity cards if needed
```

---

## Integration Points

### With ORCHESTRATOR Startup

`/startupO` and `/startupO-lite` can use this skill:

```python
# In ORCHESTRATOR session
spec = spawn_agent_tool("G2_RECON", "Explore codebase for...")
Task(prompt=spec["full_prompt"], ...)
```

### With Coordinator Skills

`/coord-engine`, `/coord-platform`, etc. spawn specialists:

```python
# COORD_ENGINE spawning SCHEDULER
spec = spawn_agent_tool(
    "SCHEDULER",
    "Generate Block 10",
    parent_agent="COORD_ENGINE"  # Validates spawn chain
)
```

### With Party Protocols

`/search-party`, `/qa-party` can spawn multiple agents in parallel:

```python
# Spawn 10 G2_RECON probes
for i in range(10):
    specs.append(spawn_agent_tool("G2_RECON", f"Probe {i}: {target}"))

# Execute in parallel
for spec in specs:
    Task(prompt=spec["full_prompt"], ..., run_in_background=True)
```

---

## Quick Reference

### Agent Tiers

| Tier | Agents (Examples) |
|------|-------------------|
| Deputy | ARCHITECT, SYNTHESIZER |
| Coordinator | COORD_ENGINE, COORD_PLATFORM, COORD_FRONTEND |
| Specialist | SCHEDULER, COMPLIANCE_AUDITOR, TEST_WRITER |
| G-Staff | G1_PERSONNEL, G2_RECON, G3_OPERATIONS |
| SOF | SF_MEDIC, SF_ENGINEER, SF_WEAPONS |

### Common Spawns

```bash
# Scheduling
/spawn-agent SCHEDULER Generate Block X schedule

# Validation
/spawn-agent COMPLIANCE_AUDITOR Audit Block X for ACGME

# Research
/spawn-agent G2_RECON Find implementations of X

# Testing
/spawn-agent QA_TESTER Run test suite for X

# Documentation
/spawn-agent META_UPDATER Update docs for feature X
```

---

## Aliases

- `/spawn-agent` (primary)
- `/spawn` (short form)
- `/agent` (alternative)

---

*spawn-agent: The bridge between MCP governance and Claude Code execution.*
