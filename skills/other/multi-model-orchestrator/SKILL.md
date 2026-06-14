---
name: multi-model-orchestrator
description: Use when coordinating complex tasks across multiple AI agents with a centralized handoff document for planning, execution tracking, and feedback fusion.
---

# multi-model-orchestrator

**Decompose. Execute. Synthesize.**

A lightweight skill for coordinating work across multiple AI agents (Claude, Opus, Haiku, Codex, or any agent) using a single **handoff document** as the source of truth.

## Why This Skill

Complex work often requires:
1. **High-level planning** — breaking down a big goal into concrete subtasks
2. **Parallel execution** — different agents handling different task types simultaneously
3. **Feedback synthesis** — collecting results and iterating intelligently
4. **Full traceability** — understanding who did what, why, and what changed

This skill provides the **structure and templates** to do this cleanly.

## Operating Contract

Direct actions: create or update one handoff document as the source of truth, decompose the goal into executor-ready subtasks, assign explicit dependencies, record execution results, and synthesize feedback into next steps.

Escalate before: starting execution when the goal, constraints, executor choice, writable scope, or done criteria are ambiguous.

Evidence-backed pushback: reject unverified completion claims, vague agent outputs, missing acceptance criteria, or parallel assignments that touch shared writable files without explicit ordering.

Feedback loop: after each execution round, update the handoff with result, evidence, blockers, and next action before assigning follow-up work.

## When to Use

✅ **Use when:**
- A single-agent conversation would be too long or unfocused
- You want to parallelize work across multiple specialized agents
- You need to decompose a vague goal into specific, executor-ready tasks
- You want to track decisions, changes, and feedback in one place
- You're exploring multiple approaches simultaneously (A/B/C branches)

❌ **Don't use when:**
- The task is simple and one agent can handle it end-to-end
- You don't need to track who did what
- Execution is strictly sequential with no parallelization
- The task is exploratory with no clear structure

## Core Concepts

### Handoff Document (Handoff)

A **YAML file** that serves as the single source of truth. It contains:

- **Goal** — what are we trying to accomplish?
- **Subtasks** — who does what, and what does success look like?
- **Context** — code references, prior decisions, constraints
- **Execution Tracking** — who executed, what was the result, what blockers?
- **Feedback** — iterations, changes, and learnings

### Agent Roles

You choose which agents execute which subtasks. Examples:

| Agent | Best For |
|-------|----------|
| **Claude (or Fable)** | Planning, decomposition, architecture review, high-level strategy |
| **Opus** | Complex reasoning, deep analysis, novel problem-solving |
| **Haiku** | Fast iteration, simple fixes, quick validation |
| **Codex** | Code generation, refactoring, technical implementation |
| **Claude Code** | Interactive development, running code, verification |

### The Loop

```
1. Define Goal
    ↓
2. Fable/Claude decomposes into Handoff subtasks
    ↓
3. You assign subtasks to agents
    ↓
4. Agents execute in parallel or sequence
    ↓
5. You record results in Handoff
    ↓
6. Review, iterate, or complete
```

## Quick Start (10 minutes)

### Step 1: Create Handoff Template

Copy the template below and save as `.claude/handoffs/my-task.yaml`:

```yaml
metadata:
  name: "descriptive name of task"
  created: "2026-06-12"
  goal: "What are we trying to accomplish?"
  status: "planning"  # planning → executing → review → complete

goal:
  summary: |
    Clear, specific goal statement.
  acceptance_criteria:
    - "Testable criterion 1"
    - "Testable criterion 2"
  context: |
    Any background, constraints, or prior decisions.

subtasks:
  - id: "task-1"
    title: "Clear description"
    type: "code | analysis | design | research | validation"
    executor: "Opus | Haiku | Codex | Claude | Claude Code"
    input: |
      What does the executor need to know?
      Include code refs, examples, constraints.
    acceptance: |
      How do we know this is done?
    depends_on: []  # other task IDs this depends on
    status: "pending"  # pending → in-progress → done → blocked

  - id: "task-2"
    title: "Another task"
    type: "code"
    executor: "Codex"
    input: |
      [...]
    depends_on: ["task-1"]
    status: "pending"

execution:
  rounds: []

feedback:
  synthesis: |
    Overall: what worked? what didn't? what changed?
  improvements:
    - "Improvement 1"
    - "Improvement 2"
  decision_log: |
    Why did we make X choice? What was the tradeoff?
```

### Step 2: Decompose with Fable/Claude

**Prompt for Fable/Claude:**

```
I have a complex goal that needs to be decomposed into subtasks for different agents.

Goal: [copy your goal from handoff]

Here's my context: [copy goal.context from handoff]

Please decompose this into 3-5 concrete subtasks that can be executed in parallel or sequence.
For each subtask:
1. Give it a clear title and type (code | analysis | design | research | validation)
2. Write the detailed input/requirements the executor needs
3. Define specific acceptance criteria
4. Suggest which agent type would be best (Opus for deep reasoning, Haiku for quick iteration, Codex for code, Claude for planning, Claude Code for interactive dev)
5. List any dependencies on other subtasks

Format as YAML subtasks I can copy into my handoff.yaml.
```

Fable generates the subtasks → you copy them into your handoff.

### Step 3: Execute One Subtask

Pick the first subtask. Copy its `input` section and give it to the assigned executor:

**For Opus/Haiku/Codex:**

```
[Copy the subtask.input here]

Success criteria:
[Copy the subtask.acceptance here]

Please execute and provide:
1. What you delivered
2. Any issues or blockers
3. What should happen next
```

**For Claude Code or interactive dev:**

```
I'm using the multi-model-orchestrator skill.

Subtask: [title]
Input: [input]
Acceptance: [acceptance]

Please execute this subtask. When done, I'll record the result in my handoff.yaml.
```

The executor completes the work.

### Step 4: Record Execution

Copy the result into your `execution.rounds` array:

```yaml
execution:
  rounds:
    - round: 1
      task_id: "task-1"
      executor: "Opus"
      status: "done"  # or "blocked" if it failed
      result: "[what was delivered]"
      issues: "[any blockers]"
      next_step: "[what's next]"
      timestamp: "2026-06-12T11:00:00Z"
```

### Step 5: Iterate or Complete

- **If blocked**: analyze the issue with the same executor or escalate to a different agent
- **If done**: move to the next subtask
- **If complete**: update `metadata.status` to "review" and optionally run a final review pass

---

## Complete Example: Add Authentication to API

See `references/add-auth-to-api.yaml` for a real-world multi-agent execution walkthrough.

---

## Using with Claude Code

If you're running Claude Code:

1. Save your handoff to `.claude/handoffs/task.yaml`
2. Run: `cat .claude/handoffs/task.yaml` to load it in conversation
3. Ask Claude to execute a subtask
4. When done, update the handoff manually or using a script

If you want automation, see "Advanced: Handoff Sync" below.

---

## Using with Codex

Codex does not have handoff-specific subcommands. Use `codex exec` with a focused prompt that names the handoff file and the exact subtask:

```bash
codex exec "Read .claude/handoffs/task.yaml. Execute subtask task-1 only. Return the result, blockers, files changed, and verification evidence."
```

For decomposition:

```bash
codex exec "Read .claude/handoffs/task.yaml. Propose 3-5 YAML subtasks using goal.summary, goal.context, and goal.acceptance_criteria. Do not edit files."
```

(Optional CLI workflow — the core skill works without it.)

---

## Handoff Structure Reference

### `metadata`

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | yes | Human-readable task name |
| `created` | date | yes | When the handoff was created |
| `goal` | string | yes | Summary of what we're doing |
| `status` | enum | yes | planning \| executing \| review \| complete |

### `goal`

| Field | Type | Purpose |
|-------|------|---------|
| `summary` | string | Detailed description of the goal |
| `acceptance_criteria` | array | Testable completion conditions |
| `context` | string | Background, constraints, prior decisions |

### `subtasks`

| Field | Type | Purpose |
|-------|------|---------|
| `id` | string | Unique identifier (e.g., task-1, task-auth-setup) |
| `title` | string | Short, clear description |
| `type` | enum | code \| analysis \| design \| research \| validation |
| `executor` | string | Which agent: Opus, Haiku, Codex, Claude, Claude Code |
| `input` | string | Everything the executor needs to know |
| `acceptance` | string | How to verify completion |
| `depends_on` | array | List of task IDs this depends on |
| `status` | enum | pending \| in-progress \| done \| blocked |

### `execution.rounds`

| Field | Type | Purpose |
|-------|------|---------|
| `round` | number | Iteration number |
| `task_id` | string | Which subtask was executed |
| `executor` | string | Which agent did it |
| `status` | enum | done \| blocked \| partial |
| `result` | string | What was delivered |
| `issues` | string | Blockers or concerns |
| `next_step` | string | Recommendation for next action |
| `timestamp` | ISO 8601 | When it was executed |

### `feedback`

| Field | Type | Purpose |
|-------|------|---------|
| `synthesis` | string | Overall assessment: what worked, what didn't, what changed |
| `improvements` | array | List of ideas for next iteration |
| `decision_log` | string | Why we made certain choices and tradeoffs |

---

## Workflow Patterns

### Pattern 1: Parallel Execution

All subtasks with no dependencies run simultaneously:

```yaml
subtasks:
  - id: task-1
    title: "Analyze requirements"
    executor: "Claude"
    depends_on: []

  - id: task-2
    title: "Design architecture"
    executor: "Opus"
    depends_on: []  # No dependency on task-1

  - id: task-3
    title: "Set up project"
    executor: "Claude Code"
    depends_on: []  # Independent
```

→ Run all three agents at the same time, then sync results.

### Pattern 2: Sequential with Dependency Chain

Each task waits for the previous one:

```yaml
subtasks:
  - id: task-1
    title: "Understand the problem"
    executor: "Fable"
    depends_on: []

  - id: task-2
    title: "Write the code"
    executor: "Codex"
    depends_on: ["task-1"]  # Waits for task-1

  - id: task-3
    title: "Test and validate"
    executor: "Claude Code"
    depends_on: ["task-2"]  # Waits for task-2
```

→ Run sequentially, using output of each as input to the next.

### Pattern 3: Parallel with Sync Point

Some tasks run in parallel; others converge:

```yaml
subtasks:
  - id: task-1a
    executor: "Opus"
    depends_on: []

  - id: task-1b
    executor: "Haiku"
    depends_on: []

  - id: task-2
    title: "Synthesize results"
    executor: "Claude"
    depends_on: ["task-1a", "task-1b"]  # Waits for both
```

→ 1a and 1b run in parallel; 2 waits for both to finish.

---

## Best Practices

### 1. **Clear Subtask Descriptions**

Bad:
```yaml
- id: task-1
  input: "fix the code"
```

Good:
```yaml
- id: task-1
  input: |
    The authentication middleware in src/auth.ts has a race condition
    when multiple requests arrive simultaneously.

    Current behavior: requests can bypass the token refresh check
    Expected behavior: all requests wait for token refresh to complete

    Code reference: src/auth.ts:45-62
    Test: tests/auth.race-condition.test.ts
```

### 2. **Specific Acceptance Criteria**

Bad:
```yaml
acceptance: "it should work"
```

Good:
```yaml
acceptance: |
  - Token refresh completes within 100ms
  - No requests can bypass the mutex
  - All 100 concurrent requests pass the test suite
  - Performance regression < 5% vs baseline
```

### 3. **Declare Dependencies Explicitly**

```yaml
depends_on: ["task-1", "task-2"]  # Clear ordering
```

Not:
```yaml
# Implicitly assumes task-1 was done first (bad)
```

### 4. **Record Everything**

Even if a task fails, record it:

```yaml
- round: 2
  task_id: "task-2"
  status: "blocked"
  result: "Attempt failed due to missing dependency"
  issues: |
    Task-1 output was incomplete.
    Need to ask Opus to redo task-1.
  next_step: "Re-execute task-1 with clearer requirements"
```

### 5. **Keep Handoffs in Git**

```bash
# Commit your handoff
git add .claude/handoffs/my-task.yaml
git commit -m "WIP: multi-agent task execution for feature X"

# Later you can see the full evolution:
git log -p .claude/handoffs/my-task.yaml
```

---

## Advanced: Handoff Sync (Optional)

If you want to automate handoff updates (instead of manual YAML editing):

1. **Python script** (if you need it):
   ```python
   import yaml

   with open('.claude/handoffs/task.yaml') as f:
       handoff = yaml.safe_load(f)

   handoff['execution']['rounds'].append({
       'round': 2,
       'task_id': 'task-1',
       'executor': 'Opus',
       'status': 'done',
       'result': '...',
       'timestamp': '2026-06-12T12:00:00Z'
   })

   with open('.claude/handoffs/task.yaml', 'w') as f:
       yaml.dump(handoff, f)
   ```

2. **CLI wrapper** (if you have one):
   ```bash
   handoff-update task-1 --executor opus --status done \
     --result "What was delivered" \
     --next-step "What's next"
   ```

3. **No automation**: just edit the YAML manually (perfectly fine).

---

## FAQ

**Q: Can I use this with Claude, Opus, Haiku, Grok, Mistral, etc.?**

A: Yes. The skill is agent-agnostic. Use any LLM model. The `executor` field is just a label.

**Q: Should I commit handoffs to git?**

A: Commit handoffs only when the repository is private or the file has been
reviewed for secrets, customer data, internal plans, and copied prompts/logs.
For sensitive work, keep handoffs outside git or commit a redacted summary.

**Q: Can I parallelize execution?**

A: Yes. If subtasks have no dependencies, execute them simultaneously. Record results when they finish.

**Q: What if a subtask blocks?**

A: Record it in `execution.rounds` with `status: blocked`. Decide whether to:
1. Fix the blocker and retry
2. Reassign to a different agent
3. Escalate to human review

**Q: How long should a subtask be?**

A: Aim for 15-60 minute chunks. If a subtask would take 4+ hours, break it down further.

**Q: Can I have multiple handoffs active?**

A: Yes. Use separate files: `task-1.yaml`, `task-2.yaml`. Each one is independent.

**Q: How is this different from running agents sequentially?**

A: This skill structures the work so:
- Multiple agents can work in parallel
- Results are centralized in one document
- Changes and decisions are all traceable
- You can review and optimize the overall plan, not just individual agent outputs

---

## Resources

- **Template**: `templates/handoff-template.yaml`
- **Real Example**: `references/add-auth-to-api.yaml`
- **Companion Tools**:
  - Codex (code-focused multi-agent router)
  - Claude Code (interactive execution)
- **Patterns**: See the usage patterns in this skill.

---

## Support & Feedback

This skill is designed to be simple, flexible, and composable. If you find edge cases or want to suggest improvements, share your handoff example (anonymized) and let us know what worked and what didn't.

---

**Updated**: 2026-06-12
**Status**: Production ready
**License**: MIT
