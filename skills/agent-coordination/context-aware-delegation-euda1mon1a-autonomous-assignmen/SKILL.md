---
name: context-aware-delegation
description: Understand agent context isolation and write effective prompts for spawned agents. Use when orchestrating multi-agent workflows to ensure subagents receive complete, self-contained context.
---

# Context-Aware Delegation Skill

> **Purpose:** Help coordinators understand and leverage agent context isolation
> **Created:** 2025-12-29
> **Audience:** Program coordinators, ORCHESTRATOR agents, anyone spawning subagents

---

## The Core Model: Context Isolation

**Spawned agents have their own isolated context** - they do NOT inherit the parent's conversation history.

```
┌─────────────────────────────────────────────────────────┐
│  Parent Agent (ORCHESTRATOR)                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Conversation History                             │   │
│  │ - User request                                   │   │
│  │ - File reads                                     │   │
│  │ - Previous decisions                             │   │
│  │ - Context accumulated over session               │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                    Task tool                            │
│                         │                               │
│          ┌──────────────┼──────────────┐               │
│          ▼              ▼              ▼               │
│    ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│    │ Agent A  │   │ Agent B  │   │ Agent C  │         │
│    │ ──────── │   │ ──────── │   │ ──────── │         │
│    │ EMPTY    │   │ EMPTY    │   │ EMPTY    │         │
│    │ context  │   │ context  │   │ context  │         │
│    │          │   │          │   │          │         │
│    │ Only has │   │ Only has │   │ Only has │         │
│    │ YOUR     │   │ YOUR     │   │ YOUR     │         │
│    │ PROMPT   │   │ PROMPT   │   │ PROMPT   │         │
│    └──────────┘   └──────────┘   └──────────┘         │
└─────────────────────────────────────────────────────────┘
```

### What This Means for You

| What Parent Has | What Subagent Gets |
|-----------------|-------------------|
| Full conversation history | **NOTHING** - starts empty |
| Files you've read | Must read them again |
| Decisions you've made | Must be told explicitly |
| Context from user | Must be passed in prompt |

---

## L3 Minimal Context Pattern (VALIDATED 2026-01-10)

**Key Discovery:** Subagents can autonomously invoke MCP tools with just mission intent + parameters.

### Context Levels Comparison

| Level | Identity | Mission | Explicit Tools | Parameters | Result |
|-------|----------|---------|----------------|------------|--------|
| L1 | Yes | Yes | Yes | Yes | MCP used (expected) |
| L2 | Yes | Yes | No | Yes | MCP used + RAG |
| **L3** | No | Yes | No | Yes | **MCP used (3 tools!)** |
| L4 | No | Minimal | No | No | Failed (file search) |

### L3 Prompt Template

```markdown
## MISSION
[Clear objective: "Assess Block 10 schedule compliance"]
[Domain context if needed: "medical residency schedule"]

[Key parameters]
- Dates: 2026-01-06 to 2026-01-31
- Requirements: ACGME compliance check

## OUTPUT
[Expected structure - JSON/markdown]
```

### When to Use L3

| Scenario | Use L3? |
|----------|---------|
| Clear mission, known domain | Yes |
| MCP tools available for task | Yes |
| Agent has standing orders | Yes |
| Uncertain requirements | No (use L2) |
| Novel task, no tools | No (use L1) |

### Anti-Pattern: Over-Contextualizing

**Wrong:** 2000 tokens of identity card + explicit tool instructions for clear tasks
**Right:** 100 tokens of mission intent + parameters (L3)

---

## Key Insight: Mid-Task Updates Don't Affect Running Agents

**Updating an agent's specification file while it's running has ZERO effect on the running instance.**

This is non-obvious but important:

```
Timeline:
─────────────────────────────────────────────────────────────────────

 T=0   ORCHESTRATOR spawns COORD_PLATFORM with Task tool
       └─ Agent receives snapshot of context from prompt

 T=1   COORD_PLATFORM is executing its task...
       └─ Running with T=0 context (frozen)

 T=2   META_UPDATER edits COORD_PLATFORM.md (fixes broken refs)
       └─ File on disk changes

 T=3   COORD_PLATFORM completes and returns results
       └─ Still using T=0 context - UNAWARE of T=2 changes

 T=4   ORCHESTRATOR spawns COORD_PLATFORM again for new task
       └─ THIS instance gets the updated spec (if included in prompt)
─────────────────────────────────────────────────────────────────────
```

### Why This Matters

1. **Safe parallel updates:** You can run an agent AND update its documentation simultaneously
2. **No "hot reload" surprises:** Running agents won't suddenly change behavior
3. **Blueprints vs. soldiers:** The `.md` spec is a blueprint; spawned agents are soldiers already deployed
4. **Only future spawns see updates:** Changes take effect on the NEXT spawn, not current execution

### Practical Implications

| Scenario | Safe? | Why |
|----------|-------|-----|
| Update agent spec while agent runs | ✅ Yes | Running agent has frozen context |
| Fix broken refs in `.claude/Agents/` during multi-agent operation | ✅ Yes | Each agent operates independently |
| Change agent's constraints mid-task | ❌ Won't work | Agent won't see the change |
| Update shared documentation (CLAUDE.md) | ✅ Safe for running agents | They already read it at spawn |

**Bottom line:** Treat spawned agents like deployed units. Updating HQ's playbook doesn't radio new orders to troops already in the field.

---

## The Golden Rule

> **Write prompts as if the agent knows NOTHING about your session.**

Think of spawning an agent like calling a function:
- You must pass all parameters explicitly
- You cannot rely on global state
- The function only knows what you tell it

---

## What to Include in Agent Prompts

### Required Elements Checklist

```markdown
□ Agent persona/role (who they are)
□ Explicit file paths (absolute, not relative)
□ Complete task description (what to do)
□ Success criteria (how to know when done)
□ Constraints (what NOT to do)
□ Expected output format (how to report back)
```

### Context Transfer Template

```markdown
## Agent: [AGENT_NAME]

**Role:** [Brief description of agent's expertise]

**Relevant Context:**
- [Key fact 1 from parent conversation]
- [Key fact 2 the agent needs to know]
- [Decision already made that affects this task]

**Files to Read:**
- `/absolute/path/to/file1.py` - [why this file matters]
- `/absolute/path/to/file2.md` - [what to look for]

## Task

[Clear, specific task description]

## Constraints

- [Constraint 1]
- [Constraint 2]

## Expected Output

Return:
1. [What to include in response]
2. [Format expectations]
```

---

## Anti-Patterns: What NOT to Do

### Anti-Pattern 1: Assuming Shared Context

```markdown
❌ BAD:
"Fix the bug we discussed earlier"

✅ GOOD:
"Fix the null reference error in /backend/app/services/swap_executor.py:142
where `person.assignments` is accessed before checking if person exists.
The error occurs when a swap request references a deleted faculty member."
```

### Anti-Pattern 2: Vague File References

```markdown
❌ BAD:
"Check the scheduler file for issues"

✅ GOOD:
"Read /backend/app/scheduling/engine.py and verify that the
generate_schedule() function properly handles the case where
no faculty are available for a given rotation."
```

### Anti-Pattern 3: Implicit Decisions

```markdown
❌ BAD:
"Implement the solution"

✅ GOOD:
"Implement retry logic using exponential backoff (2s, 4s, 8s, 16s).
We decided to use this approach because the API has rate limiting.
Maximum 4 retries before failing permanently."
```

### Anti-Pattern 4: Missing Success Criteria

```markdown
❌ BAD:
"Make the tests pass"

✅ GOOD:
"Fix the failing test in /backend/tests/test_swap_executor.py::test_rollback.
The test expects SwapExecutor.rollback() to restore the original assignment
within 24 hours. Currently it's returning None instead of the Assignment object.
Success = test passes AND no other tests regress."
```

---

## Prompt Templates by Agent Type

### SCHEDULER Agent

```markdown
## Agent: SCHEDULER

**Charter:** Handle all scheduling operations with ACGME compliance as top priority.

**Context:**
- Academic year: [YEAR]
- Block being scheduled: [BLOCK_NUMBER] ([START_DATE] to [END_DATE])
- Known constraints: [LIST ANY SPECIAL CONSTRAINTS]

**Files:**
- `/backend/app/scheduling/engine.py` - Core scheduling logic
- `/backend/app/scheduling/acgme_validator.py` - Compliance rules

## Task

[Specific scheduling task]

## Constraints

- Never violate ACGME 80-hour rule
- Maintain 1-in-7 day off requirement
- Verify backup database exists before writes

## Expected Output

1. Schedule assignments (JSON or table format)
2. Any ACGME warnings generated
3. Coverage gaps if any exist
```

### QA_TESTER Agent

```markdown
## Agent: QA_TESTER

**Charter:** Ensure code quality through comprehensive testing.

**Context:**
- Feature being tested: [FEATURE_NAME]
- Related PR/commit: [REFERENCE]
- Test framework: pytest (backend) / Jest (frontend)

**Files to Test:**
- `/backend/app/services/[service].py` - Implementation
- `/backend/tests/test_[service].py` - Existing tests (if any)

## Task

Write tests for [SPECIFIC FUNCTIONALITY].

## Test Requirements

- Cover happy path
- Cover error cases: [LIST SPECIFIC ERRORS]
- Cover edge cases: [LIST EDGE CASES]
- Use fixtures from conftest.py where available

## Expected Output

1. Test file with pytest tests
2. List of scenarios covered
3. Any mocking requirements identified
```

### ARCHITECT Agent

```markdown
## Agent: ARCHITECT

**Charter:** Design robust database schemas and API interfaces.

**Context:**
- Current models: [LIST RELEVANT MODELS]
- Problem being solved: [DESCRIPTION]
- Integration points: [OTHER SYSTEMS AFFECTED]

**Files:**
- `/backend/app/models/[model].py` - Current schema
- `/backend/alembic/versions/` - Migration history

## Task

Design [SCHEMA/API CHANGE].

## Constraints

- Must maintain backward compatibility with: [LIST]
- Must support: [REQUIREMENTS]
- Migration must be reversible

## Expected Output

1. Schema design (SQLAlchemy model)
2. Migration strategy
3. API contract changes (if any)
4. Rollback plan
```

---

## Context for Built-in Agent Types

Some Task tool `subagent_type` options have special context behavior:

| subagent_type | Context Behavior |
|---------------|------------------|
| `general-purpose` | Isolated - needs full prompt |
| `Explore` | Can see conversation history before tool call |
| `Plan` | Can see conversation history before tool call |
| `claude-code-guide` | Isolated - searches docs independently |

### Using "Access to Current Context" Agents

For `Explore` and `Plan` agents, you can write shorter prompts:

```markdown
## With Explore agent (HAS context access):

Task(
  prompt="Find where the scheduling conflict we discussed is handled",
  subagent_type="Explore"
)
# Works because Explore can see prior conversation

## With general-purpose agent (NO context access):

Task(
  prompt="""
  Find where scheduling conflicts are detected in the codebase.

  Specifically looking for:
  - Time overlap detection between assignments
  - ACGME work hour limit checks
  - Faculty double-booking prevention

  Search in /backend/app/scheduling/ directory.
  """,
  subagent_type="general-purpose"
)
# Must be explicit because agent starts fresh
```

---

## Parallel Agent Context Strategy

When spawning multiple agents in parallel, each needs independent context:

```markdown
## Parallel Spawn Pattern

# Agent 1: Code Review
Task(
  description="QA_TESTER: Review swap logic",
  prompt="""
  ## Agent: QA_TESTER

  Review /backend/app/services/swap_executor.py for:
  - Error handling completeness
  - Edge case coverage
  - ACGME compliance checks

  Return: List of issues found with line numbers
  """,
  subagent_type="general-purpose"
)

# Agent 2: Security Audit (PARALLEL - different context)
Task(
  description="ARCHITECT: Security review",
  prompt="""
  ## Agent: ARCHITECT (Security Focus)

  Audit /backend/app/services/swap_executor.py for:
  - SQL injection risks
  - Authorization bypass
  - Data exposure in logs

  Return: Security findings with severity ratings
  """,
  subagent_type="general-purpose"
)

# Agent 3: Test Generation (PARALLEL - different context)
Task(
  description="QA_TESTER: Generate tests",
  prompt="""
  ## Agent: QA_TESTER

  Generate pytest tests for SwapExecutor.execute_swap() in
  /backend/app/services/swap_executor.py

  Cover:
  - Successful one-to-one swap
  - Swap with ACGME violation (should fail)
  - Rollback within 24-hour window
  - Rollback after 24-hour window (should fail)

  Return: Complete test file content
  """,
  subagent_type="general-purpose"
)
```

---

## Result Synthesis: Getting Information Back

Subagents return a single message. Design your prompts to get structured output:

### Structured Output Request

```markdown
## Expected Output Format

Return a JSON object:
```json
{
  "status": "success" | "failure" | "partial",
  "findings": [
    {
      "file": "path/to/file.py",
      "line": 42,
      "issue": "description",
      "severity": "high" | "medium" | "low",
      "suggestion": "how to fix"
    }
  ],
  "summary": "one-line summary",
  "next_steps": ["recommended action 1", "recommended action 2"]
}
```
```

### Aggregating Multiple Agent Results

```markdown
After spawning 3 parallel agents, synthesize:

1. Collect all findings
2. Deduplicate (same issue found by multiple agents)
3. Prioritize by severity
4. Create unified action plan

Use synthesis pattern from delegation-patterns.md:
- All-or-Nothing: For compliance checks
- Merge-Deduplicate: For findings/issues
- Weighted: For scoring/ranking
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│           CONTEXT-AWARE DELEGATION CHEATSHEET           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  REMEMBER: Subagents start with EMPTY context           │
│                                                         │
│  ALWAYS INCLUDE:                                        │
│  □ Agent role/persona                                   │
│  □ Absolute file paths                                  │
│  □ Complete task description                            │
│  □ Constraints and boundaries                           │
│  □ Expected output format                               │
│                                                         │
│  NEVER ASSUME:                                          │
│  ✗ Agent knows conversation history                     │
│  ✗ Agent has read files you read                        │
│  ✗ Agent knows decisions you made                       │
│  ✗ Agent understands implicit context                   │
│                                                         │
│  CONTEXT-AWARE TYPES:                                   │
│  • Explore, Plan → CAN see prior conversation           │
│  • general-purpose → CANNOT, needs full prompt          │
│                                                         │
│  THINK LIKE A FUNCTION CALL:                            │
│  spawn_agent(                                           │
│    role="QA_TESTER",                                    │
│    files=["/path/to/file.py"],                          │
│    task="Write tests for X",                            │
│    constraints=["no mocking DB"],                       │
│    output_format="pytest file"                          │
│  )                                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Identity Card Integration

When spawning ANY PAI agent, load their identity card for proper boot context:

### Pattern
```python
Task(
  prompt=f"""
  ## BOOT CONTEXT
  {read('.claude/Identities/AGENT_NAME.identity.md')}

  ## MISSION
  [Task description]

  ## CONSTRAINTS
  [Any additional constraints]

  ## OUTPUT FORMAT
  [Expected output]
  """,
  subagent_type="general-purpose"
)
```

### Why Identity Cards?
- Agent knows who they are (role, tier)
- Agent knows chain of command (reports to, can spawn)
- Agent knows standing orders (pre-authorized actions)
- Agent knows escalation triggers (when to ask)
- Agent knows constraints (what NOT to do)

### Identity Card Location
All identity cards are in `.claude/Identities/[AGENT_NAME].identity.md`

### Available Identity Cards
Current identity cards in the system:
- `ARCHITECT.identity.md` - Database and API architecture specialist
- `SYNTHESIZER.identity.md` - Multi-source synthesis and integration specialist
- `TEMPLATE.identity.md` - Template for creating new identity cards

**Note:** If spawning an agent that doesn't have an identity card yet, follow the template at `.claude/Identities/TEMPLATE.identity.md` to create one.

---

## Related Skills

- **startupO**: Initialize ORCHESTRATOR mode (loads this skill)
- **CORE/delegation-patterns.md**: Execution patterns (parallel, sequential, hybrid)
- **CORE/spawn-with-identity.md**: Identity card loading patterns
- **MCP_ORCHESTRATION**: Tool-level orchestration
- **agent-factory**: Create new agent personas

---

## Version

- **Created:** 2025-12-29
- **Author:** Claude Code Session
- **Applies to:** Claude Code CLI, Claude Agent SDK
- **Last Updated:** 2026-01-06 (Added identity card integration)

---

*Effective delegation requires explicit context transfer. Write prompts as if teaching a capable colleague who just joined the project today.*
