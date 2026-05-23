---
id: orchestrator-directives
name: Orchestrator Directives Skill
description: Cost-first delegation patterns and decision frameworks for multi-AI coordination
trigger: "when user asks about delegation, orchestration, or cost optimization"
visibility: "always"
tags: ["delegation", "orchestration", "cost-optimization", "multi-ai", "spawners"]
---

# Orchestrator Directives Skill

Use this skill for delegation patterns and decision frameworks in orchestrator mode.

**Trigger keywords:** orchestrator, delegation, subagent, task coordination, parallel execution, cost-first, spawner

---

## Quick Start - What is Orchestration?

Orchestration means delegating tactical work to specialized subagents while you focus on strategic decisions. This saves Claude Code context (expensive) by using FREE/CHEAP AIs for appropriate tasks.

**Basic pattern:**
```python
Task(
    subagent_type="htmlgraph:gemini-spawner",  # FREE - use for exploration
    description="Find auth patterns",
    prompt="Search codebase for authentication patterns..."
)
```

**When to use:** Complex tasks requiring research, code generation, git operations, or any work that could fail and require retries.

**For complete guidance:** See sections below or run `/multi-ai-orchestration` for model selection details.

---

## CRITICAL: Cost-First Delegation (IMPERATIVE)

**Claude Code is EXPENSIVE. You MUST delegate to FREE/CHEAP AIs first.**

<details>
<summary><strong>Cost Comparison & Pre-Delegation Checklist</strong></summary>

### PRE-DELEGATION CHECKLIST (MUST EXECUTE BEFORE EVERY TASK())

Ask these questions IN ORDER:

1. **Can Gemini do this?** → Exploration, research, batch ops, file analysis
   - YES = MUST use Gemini spawner (FREE - 2M tokens/min)

2. **Is this code work?** → Implementation, fixes, tests, refactoring
   - YES = MUST use Codex spawner (70% cheaper than Claude)

3. **Is this git/GitHub?** → Commits, PRs, issues, branches
   - YES = MUST use Copilot spawner (60% cheaper, GitHub-native)

4. **Does this need deep reasoning?** → Architecture, complex planning
   - YES = Use Claude Opus (expensive, but strategically needed)

5. **Is this coordination?** → Multi-agent work
   - YES = Use Claude Sonnet (mid-tier)

6. **ONLY if above fail** → Haiku (fallback)

### Cost Comparison Examples

| Task | WRONG (Cost) | CORRECT (Cost) | Savings |
|------|-------------|----------------|---------|
| Search 100 files | Task() ($15-25) | Gemini spawner (FREE) | 100% |
| Generate code | Task() ($10) | Codex spawner ($3) | 70% |
| Git commit | Task() ($5) | Copilot spawner ($2) | 60% |
| Strategic decision | Direct task ($20) | Claude Opus ($50) | Must pay for quality |

### WRONG vs CORRECT Examples

```
WRONG (wastes Claude quota):
- Code implementation → Task(haiku)               # USE Codex spawner
- Git commits → Task(haiku)                       # USE Copilot spawner
- File search → Task(haiku)                       # USE Gemini spawner (FREE!)
- Research → Task(haiku)                          # USE Gemini spawner (FREE!)

CORRECT (cost-optimized):
- Code implementation → Codex spawner             # Cheap, sandboxed
- Git commits → Copilot spawner                   # Cheap, GitHub-native
- File search → Gemini spawner                    # FREE!
- Research → Gemini spawner                       # FREE!
- Strategic decisions → Claude Opus               # Expensive, but needed
- Haiku → FALLBACK ONLY                           # When spawners fail
```

</details>

---

## Core Concepts

<details>
<summary><strong>Orchestrator vs Executor Roles</strong></summary>

**Orchestrator (You):**
- Makes strategic decisions
- Delegates tactical work
- Tracks progress with SDK
- Coordinates parallel subagents
- Only executes: Task(), AskUserQuestion(), TodoWrite(), SDK operations

**Executor (Subagent):**
- Handles tactical implementation
- Researches specific problems
- Fixes issues with retries
- Reports findings back
- Consumes resources independently (saves your context)

**Why separation matters:**
- Context preservation (failures don't compound in your context)
- Parallel efficiency (multiple subagents work simultaneously)
- Cost optimization (subagents are cheaper than Claude Code)
- Error isolation (failures stay in subagent context)

</details>

<details>
<summary><strong>Why Delegation Matters: Context Cost Model</strong></summary>

**What looks like "one bash call" becomes many:**
- Initial command fails → need to retry
- Test hooks break → need to fix code → retry
- Push conflicts → need to pull/merge → retry
- Each retry consumes tokens

**Context cost comparison:**
```
Direct execution (fails):
  bash call 1 → fails
  bash call 2 → fails
  bash call 3 → fix code
  bash call 4 → bash call 1 retry
  bash call 5 → bash call 2 retry
  = 5+ tool calls, context consumed

Delegation (cascades isolated):
  Task(subagent handles all retries) → 1 tool call
  Read result → 1 tool call
  = 2 tool calls, clean context
```

**Token savings:**
- Each failed retry: 2,000-5,000 tokens wasted
- Cascading failures: 10,000+ tokens wasted
- Subagent isolation: None of that pollution in orchestrator context

</details>

<details>
<summary><strong>Decision Framework: When to Delegate vs Execute</strong></summary>

Ask yourself these questions:

1. **Will this likely be ONE tool call?**
   - Uncertain → DELEGATE
   - Certain → MAY do directly (single file read, quick check)

2. **Does this require error handling?**
   - If yes → DELEGATE (subagent handles retries)

3. **Could this cascade into multiple operations?**
   - If yes → DELEGATE

4. **Is this strategic or tactical?**
   - Strategic (decisions) → Do directly
   - Tactical (execution) → DELEGATE

**Rule of thumb:** When in doubt, DELEGATE. Cascading failures are expensive.

</details>

<details>
<summary><strong>Three Allowed Direct Operations</strong></summary>

Only these can be executed directly by orchestrator:

1. **Task()** - Delegation itself
   - Use spawner subagent types when possible
   - Example: `Task(subagent_type="htmlgraph:gemini-spawner", ...)`

2. **AskUserQuestion()** - Clarifying requirements
   - Get user input before delegating
   - Example: `AskUserQuestion("Should we use Redis or PostgreSQL?")`

3. **TodoWrite()** - Tracking work items
   - Create/update todo lists
   - Example: `TodoWrite(todos=[...])`

**SDK operations** (create features, spikes, bugs):
- `sdk.features.create()`
- `sdk.spikes.create()`
- `sdk.bugs.create()`

Everything else MUST be delegated.

</details>

---

## Model Selection & Spawner Guide

<details>
<summary><strong>Spawner Selection Decision Tree</strong></summary>

**Decision tree (check each in order):**

1. **Is this exploration/research/analysis?**
   - Files search: YES → Gemini spawner (FREE)
   - Pattern analysis: YES → Gemini spawner (FREE)
   - Documentation reading: YES → Gemini spawner (FREE)
   - Learning unfamiliar system: YES → Gemini spawner (FREE)

2. **Is this code implementation/testing?**
   - Generate code: YES → Codex spawner (70% cheaper)
   - Fix bugs: YES → Codex spawner
   - Write tests: YES → Codex spawner
   - Refactor code: YES → Codex spawner

3. **Is this git/GitHub operation?**
   - Commit changes: YES → Copilot spawner (60% cheaper, GitHub-native)
   - Create PR: YES → Copilot spawner
   - Manage branches: YES → Copilot spawner
   - Review code: YES → Copilot spawner

4. **Does this need deep reasoning?**
   - Architecture decisions: YES → Claude Opus (expensive, but needed)
   - Complex design: YES → Claude Opus
   - Strategic planning: YES → Claude Opus

5. **Is this multi-agent coordination?**
   - Coordinate multiple spawners: YES → Claude Sonnet (mid-tier)
   - Complex workflows: YES → Claude Sonnet

6. **All else fails** → Task() with Haiku (fallback)

**Spawner Subagent Types:**
- `htmlgraph:gemini-spawner` - FREE, 2M tokens/min
- `htmlgraph:codex-spawner` - Cheap code specialist
- `htmlgraph:copilot-spawner` - Cheap git specialist
- `general-purpose` - Generic Claude (use as fallback or when spawners fail)

</details>

<details>
<summary><strong>Spawner Details & Configuration</strong></summary>

### Gemini Spawner (FREE - Exploration)
```python
Task(
    subagent_type="htmlgraph:gemini-spawner",
    description="Analyze authentication patterns",
    prompt="""
    Analyze codebase for:
    - All authentication patterns
    - OAuth implementations
    - Session management
    - JWT usage
    """
)
```

**Best for:**
- File searching (FREE!)
- Pattern analysis (FREE!)
- Documentation research (FREE!)
- Understanding unfamiliar systems (FREE!)

### Codex Spawner (Cheap - Code)
```python
Task(
    subagent_type="htmlgraph:codex-spawner",
    description="Implement OAuth middleware",
    prompt="""
    Implement OAuth authentication:
    - Sandbox mode: workspace-write
    - Add JWT token generation
    - Include error handling
    - Write unit tests
    """
)
```

**Best for:**
- Code generation
- Bug fixes
- Test writing
- Refactoring
- Sandboxed execution

### Copilot Spawner (Cheap - Git)
```python
Task(
    subagent_type="htmlgraph:copilot-spawner",
    description="Commit and create PR",
    prompt="""
    Commit changes and create PR:
    - Message: "feat: add OAuth authentication"
    - Files: src/auth/*.py, tests/test_auth.py
    - Create PR with description
    """
)
```

**Best for:**
- Git commits (60% cheaper than Task)
- PR creation
- Branch management
- GitHub integration
- Resolving conflicts

### Task() with Sonnet/Opus (Strategic)
```python
Task(
    prompt="Design authentication architecture...",
    subagent_type="sonnet"  # or "opus"
)
```

**Sonnet (Mid-tier):**
- Coordinate complex workflows
- Multi-agent orchestration
- Fallback when spawners fail

**Opus (Expensive):**
- Deep reasoning
- Architecture decisions
- Strategic planning
- When quality matters more than cost

</details>

---

## Delegation Patterns & Examples

<details>
<summary><strong>Basic Delegation Pattern</strong></summary>

**Simple exploration:**
```python
Task(
    subagent_type="htmlgraph:gemini-spawner",
    description="Find all auth patterns",
    prompt="Search codebase for authentication patterns and summarize findings"
)
```

**Code implementation:**
```python
Task(
    subagent_type="htmlgraph:codex-spawner",
    description="Implement OAuth endpoint",
    prompt="Implement OAuth authentication endpoint with JWT support"
)
```

**Git operations:**
```python
Task(
    subagent_type="htmlgraph:copilot-spawner",
    description="Commit changes",
    prompt="Commit changes with message: 'feat: add OAuth authentication'"
)
```

</details>

<details>
<summary><strong>Parallel Delegation (Multiple Independent Tasks)</strong></summary>

**Pattern: Spawn all at once, retrieve results independently**

```python
# Create all tasks in parallel (single message)
Task(
    subagent_type="htmlgraph:gemini-spawner",
    description="Research auth patterns",
    prompt="Analyze existing authentication patterns..."
)

Task(
    subagent_type="htmlgraph:codex-spawner",
    description="Implement OAuth",
    prompt="Implement OAuth flow..."
)

Task(
    subagent_type="htmlgraph:copilot-spawner",
    description="Create PR",
    prompt="Commit and create pull request..."
)

# All run in parallel, optimized for cost:
# - Gemini: FREE
# - Codex: $ (cheap)
# - Copilot: $ (cheap)
```

**Benefits:**
- 3 tasks in parallel: time = max(T1, T2, T3) instead of T1+T2+T3
- Cost optimization: Uses cheapest model for each task
- Independent results: Each task tracked separately

</details>

<details>
<summary><strong>Sequential Delegation with Dependencies</strong></summary>

**Pattern: Chain dependent tasks in sequence**

```python
# 1. Research existing patterns
Task(
    subagent_type="htmlgraph:gemini-spawner",
    description="Research OAuth patterns",
    prompt="Find all OAuth implementations in codebase..."
)

# 2. Wait for research, then implement
# (In next message after reading result)
research_findings = "..."  # Read from previous task result

Task(
    subagent_type="htmlgraph:codex-spawner",
    description="Implement OAuth based on research",
    prompt=f"""
    Implement OAuth using discovered patterns:
    {research_findings}
    """
)

# 3. Wait for implementation, then commit
Task(
    subagent_type="htmlgraph:copilot-spawner",
    description="Commit implementation",
    prompt="Commit OAuth implementation..."
)
```

**When to use:** When later tasks depend on earlier results

</details>

<details>
<summary><strong>HtmlGraph Result Retrieval</strong></summary>

**Subagents report findings automatically:**

When a Task() completes, findings are stored in HtmlGraph:
```python
# SDK can retrieve results
from htmlgraph import SDK
sdk = SDK(agent='orchestrator')

# Get recent spike (subagent's findings)
spike = sdk.spikes.list(limit=1)[0]
findings = spike.get_findings()
```

**Pattern: Read findings after Task completes**

```python
# 1. Delegate exploration
Task(
    subagent_type="htmlgraph:gemini-spawner",
    description="Analyze auth patterns",
    prompt="Find all authentication patterns..."
)

# 2. Read findings from HtmlGraph
sdk = SDK(agent='orchestrator')
recent_spike = sdk.spikes.list(limit=1)[0]
findings = recent_spike.get_findings()

# 3. Use findings in next delegation
Task(
    subagent_type="htmlgraph:codex-spawner",
    description="Implement based on findings",
    prompt=f"Implement authentication:\n{findings}"
)
```

</details>

<details>
<summary><strong>Error Handling & Retries</strong></summary>

**Let subagents handle retries:**

```python
# WRONG - Don't retry directly as orchestrator
bash_result = Bash(command="git commit -m 'feat: new'")
if failed:
    # Retry directly (context pollution)
    Bash(command="git pull && git commit")  # More context used

# CORRECT - Subagent handles retries
Task(
    subagent_type="htmlgraph:copilot-spawner",
    description="Commit changes with retry",
    prompt="""
    Commit changes:
    Message: "feat: new feature"

    If commit fails:
    1. Pull latest changes
    2. Resolve conflicts if any
    3. Retry commit
    4. Handle pre-commit hooks

    Report final status: success or failure
    """
)
```

**Benefits:**
- Subagent context handles retries (not your context)
- Cleaner error reporting
- Automatic recovery attempts
- You get clean success/failure

</details>

---

## Advanced: Post-Compact Persistence

<details>
<summary><strong>Orchestrator Activation After Compact</strong></summary>

**How it works:**

1. Before compact, SDK sets environment variable: `CLAUDE_ORCHESTRATOR_ACTIVE=true`
2. SessionStart hook detects post-compact state
3. Orchestrator Directives Skill auto-activates
4. This skill section appears automatically (first time post-compact)

**Why:** Preserve orchestration discipline after context compact

**What you see:**
- Skill automatically activates (no manual invocation needed)
- Quick start section visible by default
- Expand detailed sections as needed
- Full guidance available without re-reading docs

**To manually trigger:**
```
/orchestrator-directives
```

**Environment variable:**
```bash
CLAUDE_ORCHESTRATOR_ACTIVE=true  # Set by SDK
```

</details>

<details>
<summary><strong>Session Continuity Across Compacts</strong></summary>

**Features preserved across compact:**
- Work items in HtmlGraph
- Feature/spike tracking
- Delegation patterns
- Model selection guidance
- This skill's guidance

**What's lost:**
- Your context (that's why compact happens)
- Intermediate tool outputs
- Local variables

**Re-activation pattern:**

```
Before compact:
- Work on features, track in HtmlGraph
- Delegate with clear prompts
- Use SDK to save progress

After compact:
- Orchestrator Skill auto-activates
- Re-read recent spikes for context
- Continue delegations
- Use Task IDs for parallel coordination
```

</details>

---

## Core Philosophy

<details>
<summary><strong>Core Principles Summary</strong></summary>

**Principle 1: Delegation > Direct Execution**
- Cascading failures consume exponentially more context than structured delegation
- One failed bash call becomes 3-5 calls with retries
- Delegation isolates failures to subagent context

**Principle 2: Cost-First > Capability-First**
- Use FREE/cheap AIs (Gemini, Codex, Copilot) before expensive Claude Code
- Gemini: FREE (exploration)
- Codex: 70% cheaper (code)
- Copilot: 60% cheaper (git)
- Claude: Expensive (strategic only)

**Principle 3: You Don't Know the Outcome**
- What looks like "one tool call" often becomes many
- Unexpected failures, conflicts, retries consume context
- Delegation removes unpredictability from orchestrator context

**Principle 4: Parallel > Sequential**
- Multiple subagents can work simultaneously
- Much faster than sequential execution
- Orchestrator stays available for decisions

**Principle 5: Track Everything**
- Use HtmlGraph SDK to track delegations
- Features, spikes, bugs created for all work
- Clear record of who did what

</details>

---

## Core Philosophy

**Delegation > Direct Execution.** Cascading failures consume exponentially more context than structured delegation.

**Cost-First > Capability-First.** Use FREE/cheap AIs before expensive Claude models.

---

## Quick Reference Table

<details>
<summary><strong>Operation Type → Correct Delegation</strong></summary>

| Operation | MUST Use | Cost | Fallback |
|-----------|----------|------|----------|
| Search files | Gemini spawner | FREE | Haiku |
| Pattern analysis | Gemini spawner | FREE | Haiku |
| Documentation research | Gemini spawner | FREE | Haiku |
| Code generation | Codex spawner | $ (70% off) | Sonnet |
| Bug fixes | Codex spawner | $ (70% off) | Haiku |
| Write tests | Codex spawner | $ (70% off) | Haiku |
| Git commits | Copilot spawner | $ (60% off) | Haiku |
| Create PRs | Copilot spawner | $ (60% off) | Haiku |
| Architecture | Claude Opus | $$$$ | Sonnet |
| Strategic decisions | Claude Opus | $$$$ | Task() |

**Key:** FREE = No cost | $ = Cheap | $$$$ = Expensive (but necessary)

</details>

---

## Related Skills

- **[/multi-ai-orchestration](/multi-ai-orchestration)** - Comprehensive model selection guide with detailed decision matrix
- **[/code-quality](/code-quality)** - Quality gates and pre-commit workflows
- **[/strategic-planning](/strategic-planning)** - HtmlGraph analytics for smart prioritization

## Reference Documentation

- **Complete Rules:** See [orchestration.md](../../rules/orchestration.md)
- **Advanced Patterns:** See [reference.md](./reference.md)
- **HtmlGraph SDK:** `from htmlgraph import SDK`

---

## Quick Summary

**Cost-First Orchestration:**
1. Gemini (FREE) → exploration, research, analysis
2. Codex (70% off) → code implementation, fixes, tests
3. Copilot (60% off) → git operations, PRs
4. Claude Opus → deep reasoning, strategy only

**Orchestrator Rule:**
Only execute: Task(), AskUserQuestion(), TodoWrite(), SDK operations

**Everything else → Delegate to appropriate spawner**

**When in doubt → DELEGATE**
