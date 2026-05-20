---
name: ralph
description: "Specification-first AI development powered by Ouroboros. Socratic questioning exposes hidden assumptions before writing code. Evolutionary loop (Interview → Seed → Execute → Evaluate → Evolve) runs until ontology converges. Ralph mode persists until verification passes — the boulder never stops. Use when user says \"ralph\", \"ooo\", \"don't stop\", \"must complete\", \"until it works\", \"keep going\", \"interview me\", or \"stop prompting\"."
allowed-tools: Read Write Bash Grep Glob WebFetch
metadata:
  tags: ralph, ouroboros, specification-first, socratic, interview, seed, evaluate, evolve, loop, completion, self-referential, multi-platform, claude, codex, gemini, boulder, ooo
  platforms: Claude Code, Codex, Gemini-CLI, OpenCode
  keyword: ralph
  version: 3.0.0
  source: Q00/ouroboros
---


# ralph (Ouroboros) — Specification-First AI Development

> **Stop prompting. Start specifying.**
>
> *"The beginning is the end, and the end is the beginning."*
> The serpent doesn't repeat — it evolves.

---

## When to use this skill

- **Before writing any code** — expose hidden assumptions with Socratic interviewing
- **Long-running tasks** that need autonomous iteration until verified
- **Vague requirements** — crystallize them into an immutable spec (Ambiguity ≤ 0.2)
- **Tasks requiring guaranteed completion** — loop until verification passes
- **When stuck** — 5 lateral thinking personas break through stagnation
- **Drift detection** — measure how far execution has deviated from original spec

---

## Core Architecture: The Loop

```
    Interview → Seed → Execute → Evaluate
        ↑                           ↓
        └──── Evolutionary Loop ────┘
```

Each cycle **evolves**, not repeats. Evaluation output feeds back as input for the next generation until the system converges.

### Double Diamond

```
    ◇ Wonder          ◇ Design
   ╱  (diverge)      ╱  (diverge)
  ╱    explore      ╱    create
 ╱                 ╱
◆ ──────────── ◆ ──────────── ◆
 ╲                 ╲
  ╲    define       ╲    deliver
   ╲  (converge)     ╲  (converge)
    ◇ Ontology        ◇ Evaluation
```

The first diamond is **Socratic**: diverge into questions, converge into ontological clarity.
The second diamond is **pragmatic**: diverge into design options, converge into verified delivery.

---

## 1. Commands (Full Reference)

| Command | Trigger Keywords | What It Does |
|---------|-----------------|--------------|
| `ooo interview` | `ooo interview`, `interview me`, `clarify requirements`, `socratic questioning` | Socratic questioning → expose hidden assumptions |
| `ooo seed` | `ooo seed`, `crystallize`, `generate seed`, `freeze requirements` | Crystallize interview into immutable spec (Ambiguity ≤ 0.2) |
| `ooo run` | `ooo run`, `execute seed`, `ouroboros run` | Execute via Double Diamond decomposition |
| `ooo evaluate` | `ooo evaluate`, `3-stage check`, `evaluate this`, `verify execution` | 3-stage gate: Mechanical → Semantic → Multi-Model Consensus |
| `ooo evolve` | `ooo evolve`, `evolutionary loop`, `iterate until converged` | Evolutionary loop until ontology converges (similarity ≥ 0.95) |
| `ooo unstuck` | `ooo unstuck`, `I'm stuck`, `think sideways`, `lateral thinking` | 5 lateral thinking personas when stuck |
| `ooo status` | `ooo status`, `am I drifting?`, `drift check`, `session status` | Drift detection + session tracking |
| `ooo ralph` | `ooo ralph`, `ralph`, `don't stop`, `must complete`, `keep going` | Persistent loop until verified — The boulder never stops |
| `ooo setup` | `ooo setup` | Register MCP server (one-time) |
| `ooo help` | `ooo help` | Full reference |

---

## 2. Interview → Specification Flow

### Philosophy: From Wonder to Ontology

> *Wonder → "How should I live?" → "What IS 'live'?" → Ontology* — Socrates

```
   Wonder                          Ontology
     💡                               🔬
"What do I want?"    →    "What IS the thing I want?"
"Build a task CLI"   →    "What IS a task? What IS priority?"
"Fix the auth bug"   →    "Is this the root cause, or a symptom?"
```

### Step 1: Interview (expose hidden assumptions)

```
ooo interview "I want to build a task management CLI"
```

The Socratic Interviewer asks questions until **Ambiguity ≤ 0.2**.

**Ambiguity formula:**
```
Ambiguity = 1 − Σ(clarityᵢ × weightᵢ)

Greenfield: Goal(40%) + Constraint(30%) + Success(30%)
Brownfield: Goal(35%) + Constraint(25%) + Success(25%) + Context(15%)

Threshold: Ambiguity ≤ 0.2 → ready for Seed
```

Example scoring:
```
Goal:       0.9 × 0.4 = 0.36
Constraint: 0.8 × 0.3 = 0.24
Success:    0.7 × 0.3 = 0.21
                        ──────
Clarity             = 0.81
Ambiguity = 1 − 0.81 = 0.19 ≤ 0.2 → ✓ Ready for Seed
```

### Step 2: Seed (crystallize into immutable spec)

```
ooo seed
```

Generates YAML specification:
```yaml
goal: Build a CLI task management tool
constraints:
  - Python 3.14+
  - No external database
  - SQLite for persistence
acceptance_criteria:
  - Tasks can be created
  - Tasks can be listed
  - Tasks can be marked complete
ontology_schema:
  name: TaskManager
  fields:
    - name: tasks
      type: array
    - name: title
      type: string
```

### Step 3: Run (execute via Double Diamond)

```
ooo run seed.yaml
ooo run  # uses seed from conversation context
```

### Step 4: Evaluate (3-stage verification)

```
ooo evaluate <session_id>
```

| Stage | Cost | What It Checks |
|-------|------|----------------|
| **Mechanical** | $0 | Lint, build, tests, coverage |
| **Semantic** | Standard | AC compliance, goal alignment, drift score |
| **Consensus** | Frontier (optional) | Multi-model vote, majority ratio |

Drift thresholds:
- `0.0 – 0.15` — Excellent: on track
- `0.15 – 0.30` — Acceptable: monitor closely
- `0.30+` — Exceeded: course correction needed

---

## 3. Ralph — Persistent Loop Until Verified

```
ooo ralph "fix all failing tests"
/ouroboros:ralph "fix all failing tests"
```

**"The boulder never stops."**
Each failure is data for the next attempt. Only complete success or max iterations stops it.

### How Ralph Works

```
┌─────────────────────────────────┐
│  1. EXECUTE (parallel)          │
│     Independent tasks           │
│     concurrent scheduling       │
├─────────────────────────────────┤
│  2. VERIFY                      │
│     Check completion            │
│     Validate tests pass         │
│     Measure drift vs seed       │
├─────────────────────────────────┤
│  3. LOOP (if failed)            │
│     Analyze failure             │
│     Fix identified issues       │
│     Repeat from step 1          │
├─────────────────────────────────┤
│  4. PERSIST (checkpoint)        │
│     .omc/state/ralph-state.json │
│     Resume after interruption   │
└─────────────────────────────────┘
```

### State File

Create `.omc/state/ralph-state.json` on start:
```json
{
  "mode": "ralph",
  "session_id": "<uuid>",
  "request": "<user request>",
  "status": "running",
  "iteration": 0,
  "max_iterations": 10,
  "last_checkpoint": null,
  "verification_history": []
}
```

### Loop Logic

```
while iteration < max_iterations:
    result = execute_parallel(request, context)
    verification = verify_result(result, acceptance_criteria)
    state.verification_history.append({
        "iteration": iteration,
        "passed": verification.passed,
        "score": verification.score,
        "timestamp": <now>
    })
    if verification.passed:
        save_checkpoint("complete")
        break
    iteration += 1
    save_checkpoint("iteration_{iteration}")
```

### Progress Report Format

```
[Ralph Iteration 1/10]
Executing in parallel...

Verification: FAILED
Score: 0.65
Issues:
- 3 tests still failing
- Type errors in src/api.py

The boulder never stops. Continuing...

[Ralph Iteration 3/10]
Executing in parallel...

Verification: PASSED
Score: 1.0

Ralph COMPLETE
==============
Request: Fix all failing tests
Duration: 8m 32s
Iterations: 3

Verification History:
- Iteration 1: FAILED (0.65)
- Iteration 2: FAILED (0.85)
- Iteration 3: PASSED (1.0)
```

### Cancellation

| Action | Command |
|--------|---------|
| Save checkpoint & exit | `/ouroboros:cancel` |
| Force clear all state | `/ouroboros:cancel --force` |
| Resume after interruption | `ooo ralph continue` or `ralph continue` |

---

## 4. Evolutionary Loop (Evolve)

```
ooo evolve "build a task management CLI"
ooo evolve "build a task management CLI" --no-execute  # ontology-only, fast mode
```

### Flow

```
Gen 1: Interview → Seed(O₁) → Execute → Evaluate
Gen 2: Wonder → Reflect → Seed(O₂) → Execute → Evaluate
Gen 3: Wonder → Reflect → Seed(O₃) → Execute → Evaluate
...until ontology converges (similarity ≥ 0.95) or max 30 generations
```

### Convergence Formula

```
Similarity = 0.5 × name_overlap + 0.3 × type_match + 0.2 × exact_match
Threshold: Similarity ≥ 0.95 → CONVERGED

Gen 1: {Task, Priority, Status}
Gen 2: {Task, Priority, Status, DueDate}  → similarity 0.78 → CONTINUE
Gen 3: {Task, Priority, Status, DueDate}  → similarity 1.00 → CONVERGED ✓
```

### Stagnation Detection

| Signal | Condition | Meaning |
|--------|-----------|---------|
| **Stagnation** | Similarity ≥ 0.95 for 3 consecutive gens | Ontology has stabilized |
| **Oscillation** | Gen N ≈ Gen N-2 (period-2 cycle) | Stuck bouncing between two designs |
| **Repetitive feedback** | ≥ 70% question overlap across 3 gens | Wonder asking the same things |
| **Hard cap** | 30 generations reached | Safety valve |

### Ralph in Evolve Mode

```
Ralph Cycle 1: evolve_step(lineage, seed) → Gen 1 → action=CONTINUE
Ralph Cycle 2: evolve_step(lineage)       → Gen 2 → action=CONTINUE
Ralph Cycle 3: evolve_step(lineage)       → Gen 3 → action=CONVERGED ✓
                                                └── Ralph stops.
                                                    The ontology has stabilized.
```

### Rewind

```
ooo evolve --status <lineage_id>          # check lineage status
ooo evolve --rewind <lineage_id> <gen_N>  # roll back to generation N
```

---

## 5. The Nine Minds (Agents)

Loaded on-demand — never preloaded:

| Agent | Role | Core Question |
|-------|------|--------------|
| **Socratic Interviewer** | Questions-only. Never builds. | *"What are you assuming?"* |
| **Ontologist** | Finds essence, not symptoms | *"What IS this, really?"* |
| **Seed Architect** | Crystallizes specs from dialogue | *"Is this complete and unambiguous?"* |
| **Evaluator** | 3-stage verification | *"Did we build the right thing?"* |
| **Contrarian** | Challenges every assumption | *"What if the opposite were true?"* |
| **Hacker** | Finds unconventional paths | *"What constraints are actually real?"* |
| **Simplifier** | Removes complexity | *"What's the simplest thing that could work?"* |
| **Researcher** | Stops coding, starts investigating | *"What evidence do we actually have?"* |
| **Architect** | Identifies structural causes | *"If we started over, would we build it this way?"* |

---

## 6. Unstuck — Lateral Thinking

When blocked after repeated failures, choose a persona:

```
ooo unstuck                 # auto-select based on situation
ooo unstuck simplifier      # cut scope to MVP — "Start with exactly 2 tables"
ooo unstuck hacker          # make it work first, elegance later
ooo unstuck contrarian      # challenge all assumptions
ooo unstuck researcher      # stop coding, find missing information
ooo unstuck architect       # restructure the approach entirely
```

**When to use each:**
- Repeated similar failures → `contrarian` (challenge assumptions)
- Too many options → `simplifier` (reduce scope)
- Missing information → `researcher` (seek data)
- Analysis paralysis → `hacker` (just make it work)
- Structural issues → `architect` (redesign)

---

## 7. Platform Installation & Usage

### Claude Code (Native Plugin — Full Mode)

```bash
# Install
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros

# One-time setup
ooo setup

# Use
ooo interview "I want to build a task CLI"
ooo seed
ooo run
ooo evaluate <session_id>
ooo ralph "fix all failing tests"
```

All `ooo` commands work natively. Hooks auto-activate:
- `UserPromptSubmit` → keyword-detector.mjs detects triggers
- `PostToolUse(Write|Edit)` → drift-monitor.mjs tracks deviation
- `SessionStart` → session initialization

**Claude Code hooks.json** (installed at `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`):
```json
{
  "hooks": {
    "SessionStart": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/session-start.mjs\"", "timeout": 5 }] }],
    "UserPromptSubmit": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/keyword-detector.mjs\"", "timeout": 5 }] }],
    "PostToolUse": [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/drift-monitor.mjs\"", "timeout": 3 }] }]
  }
}
```

### Codex CLI (Adapted Mode — bash loop)

Codex CLI has no native AfterAgent hooks. Use the setup script to configure:

```bash
# Setup
bash <your-agent-skills>/ralph/scripts/setup-codex-hook.sh

# Restart Codex, then use:
/prompts:ralph              # load ralph loop context
/prompts:ouroboros          # load full ouroboros context

# Use ooo commands in conversation:
ooo interview "build a REST API"
ooo ralph "fix all TypeScript errors"
```

**Codex ralph loop contract:**
1. Treat `/ralph "<task>" [--completion-promise=TEXT] [--max-iterations=N]` as a contract command
2. Parse completion signal inside XML: `<promise>VALUE</promise>`
3. If promise missing and iteration < max-iterations → continue immediately with same original command
4. If promise found or max-iterations reached → finish with status report

**Completion promise syntax:**
```xml
<promise>DONE</promise>
```

Manual state management for Codex:
- Create `.omc/state/ralph-state.json` at loop start
- Update `iteration` counter each cycle
- Set `status: "complete"` when promise found
- Default completion promise: `DONE` | Default max iterations: `10`

### Gemini CLI (AfterAgent Hook Mode)

```bash
# Install via extensions
gemini extensions install https://github.com/Q00/ouroboros
# OR install skills-template
gemini extensions install https://github.com/supercent-io/skills-template
```

Required in `~/.gemini/settings.json`:
```json
{
  "hooksConfig": { "enabled": true },
  "context": {
    "includeDirectories": ["~/.gemini/extensions/ralph"]
  }
}
```

AfterAgent hook for loop continuation (add to `~/.gemini/settings.json`):
```json
{
  "hooks": {
    "AfterAgent": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.gemini/hooks/ralph-check.sh",
        "timeout": 10
      }]
    }]
  }
}
```

Run in sandbox + YOLO mode to prevent constant confirmation prompts:
```bash
gemini -s -y
```

Then use `ooo` commands directly:
```
ooo interview "build a task CLI"
ooo ralph "fix all tests"
```

⚠️ **Gemini v0.30.0 bug**: `stop_hook_active` always `false` in hook JSON.
Workaround: check `.omc/state/ralph-state.json` directly instead of relying on the hook field.

---

## 8. Platform Support Matrix

| Platform | Native Support | Mechanism | ooo Commands | Loop |
|----------|---------------|-----------|-------------|------|
| **Claude Code** | ✅ Full | Plugin + hooks | All `ooo` commands | Auto via hooks |
| **Codex CLI** | 🔧 Adapted | bash + `/prompts:ralph` | Via conversation | Manual state file |
| **Gemini CLI** | ✅ Native | AfterAgent hook | All `ooo` commands | Auto via hook |
| **OpenCode** | ✅ Native | Skills system | All `ooo` commands | Auto via loop |

---

## 9. Quick Reference

| Action | Command |
|--------|---------|
| Socratic interview | `ooo interview "topic"` |
| Generate spec | `ooo seed` |
| Execute spec | `ooo run [seed.yaml]` |
| 3-stage evaluate | `ooo evaluate <session_id>` |
| Evolve until converged | `ooo evolve "topic"` |
| Persistent loop | `ooo ralph "task"` |
| Break stagnation | `ooo unstuck [persona]` |
| Check drift | `ooo status [session_id]` |
| First-time setup | `ooo setup` |
| Cancel | `/ouroboros:cancel` |
| Force cancel + clear | `/ouroboros:cancel --force` |
| Resume | `ooo ralph continue` |
| Cancel (Gemini/Codex) | `/ralph:cancel` |

---

## 10. Installation

```bash
# Claude Code
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
ooo setup

# Codex CLI
bash <skills>/ralph/scripts/setup-codex-hook.sh

# Gemini CLI (extensions)
gemini extensions install https://github.com/Q00/ouroboros

# All platforms via skills-template
npx skills add https://github.com/supercent-io/skills-template --skill ralph
```

Source: [Q00/ouroboros](https://github.com/Q00/ouroboros) — MIT License
