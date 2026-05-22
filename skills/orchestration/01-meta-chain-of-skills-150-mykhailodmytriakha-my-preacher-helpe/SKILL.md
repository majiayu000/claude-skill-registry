---
name: 01-meta-chain-of-skills-150
description: "[01] META. Сканирует доступные skills, создает план выполнения и идет шаг за шагом с подтверждением каждого этапа. Triggers on complex tasks, multi-step work, or when structured execution is needed."
---

# Meta-Chain-of-Skills 150 Protocol

**Core Principle:** Найди skills → создай план → выполняй по шагам → подтверждай каждый шаг.

## What This Skill Does

1. **SCAN:** Сканирует систему на доступные skills
2. **BUILD:** Создает план из подходящих skills
3. **EXECUTE:** Выполняет по одному этапу с подтверждением
4. **REROUTE:** Может перестроить план если нужно

## Three Steps

### Step 1: SCAN (Find Available Skills)

```
🔍 SCANNING SYSTEM...

Looking for skills in:
- ./.codex/skills/ (project skills, canonical)
- ./skills/ (legacy project skills)
- ./.claude/skills/ (legacy project-specific)
- ~/.claude/skills/ (personal skills)

Found skills: N total

Available for chaining:
- [skill-1] — [purpose]
- [skill-2] — [purpose]
- [skill-3] — [purpose]
...
```

### Step 2: BUILD (Create Chain)

```
📋 BUILDING PLAN...

Query: [user query]
Goal: [identified goal]

Plan created:
  1. [skill-name] — [purpose]
  2. [skill-name] — [purpose]
  3. [skill-name] — [purpose]
  ...

Total steps: N

✅ Start execution? (Yes / Modify / Cancel)
```

### Step 3: EXECUTE (Run Stages)

Each stage follows this format:

```
⚡ EXECUTING — Step N of X

Current skill: [skill-name]
Purpose: [what this stage achieves]

[... skill execution output ...]

───────────────────────────────────────────────────────────────
📊 EXECUTION STATUS

✅ Completed: Step 1, Step 2, ...
⚡ Current:   Step N — [skill-name]
⏳ Remaining: Step N+1, Step N+2, ...

📍 Progress: ████████░░░░░░░░ N/X steps (XX%)

🎯 Next: Step N+1 — [next-skill-name]
   Purpose: [what next stage will do]

Continue to next step? (Yes / Pause / Reroute / Stop)
───────────────────────────────────────────────────────────────
```

## Execution Protocol

### Step 1: SCAN SYSTEM
Find all available skills:
```bash
# Check standard locations
ls -la ./.codex/skills/ 2>/dev/null || echo "No project skills"
ls -la ./skills/ 2>/dev/null || echo "No legacy project skills"
ls -la ./.claude/skills/ 2>/dev/null || echo "No legacy project-specific skills"
ls -la ~/.claude/skills/ 2>/dev/null || echo "No personal skills"
```

### Step 2: ANALYZE QUERY
Understand the task:
- What is the real goal?
- What type of task is this?
- What skills are needed?
- What is the logical order?

### Step 3: BUILD PLAN
Create execution plan:
- Select skills from scanned list
- Maximum 8 steps (prefer fewer)
- Each step = 1 skill (max 2 if tightly coupled)
- Order by dependencies

### Step 4: SHOW PLAN
Present the plan to user:
- All steps with purposes
- Total count
- Ask for confirmation

### Step 5: EXECUTE STEPS
For each step:
1. Show step number and skill
2. Execute the skill
3. Show results
4. Present execution status
5. Ask to continue

### Step 6: COMPLETE OR REBUILD
When all steps done:
- Show completion summary
- Or if user requests rebuild: create new plan

## User Commands

| Command | Action |
|---------|--------|
| **Yes / Continue / Next** | Proceed to next step |
| **Pause** | Stop here, save progress |
| **Reroute** | Rebuild plan from current position |
| **Skip** | Skip current step, go to next |
| **Back** | Return to previous step |
| **Stop** | End execution, show summary |

## Available Skills for Routing

The chain can include any of these skills:

| Skill | Use When |
|-------|----------|
| `goal-clarity-150` | Need to clarify requirements |
| `research-150` | Need internal investigation |
| `research-deep-150` | Need internal + external research |
| `impact-map-150` | Need to map dependencies |
| `deep-think-150` | Need quality reasoning |
| `proof-grade-150` | Need to verify critical claims |
| `action-plan-150` | Need to create detailed plan |
| `gated-exec-150` | Need controlled execution |
| `max-quality-150` | Need high-quality output |
| `refactor-150` | Need code restructuring |
| `coverage-70-tests` | Need test coverage |
| `integrity-check-150` | Need final quality check |
| `tidy-up-150` | Need quick cleanup |
| `task-track-150` | Need status management |
| `lessons-learn` | Need to capture learnings |
| `74-mid-session-save-150` | Need a mid-session checkpoint |
| `ask-ai-150` | Need external AI consultation |

## Common Route Templates

### 🔧 Code Change Route
```
1. goal-clarity-150     → Clarify what to change
2. research-150         → Understand existing code
3. impact-map-150       → Map what's affected
4. action-plan-150      → Create implementation plan
5. gated-exec-150       → Implement with gates
6. coverage-70-tests    → Add/verify tests
7. integrity-check-150  → Final quality check
```

### 🐛 Bug Fix Route
```
1. goal-clarity-150     → Clarify symptoms
2. research-150         → Investigate code/logs
3. deep-think-150       → Identify root cause
4. action-plan-150      → Plan the fix
5. gated-exec-150       → Apply fix
6. lessons-learn        → Capture learnings
```

### 📝 Document Creation Route
```
1. goal-clarity-150     → Clarify document purpose
2. research-150         → Gather information
3. action-plan-150      → Create outline
4. max-quality-150      → Write document
5. integrity-check-150  → Review quality
```

### 🔍 Research Route
```
1. goal-clarity-150     → Clarify what to find
2. research-deep-150    → Internal + external research
3. proof-grade-150      → Verify findings
4. deep-think-150       → Synthesize conclusions
```

## Output Format

### End of Each Message (MANDATORY)

Every message during execution MUST end with this summary block:

```
───────────────────────────────────────────────────────────────
📊 EXECUTION STATUS

✅ Completed: [list of completed steps]
⚡ Current:   Step N — [skill-name] — [status]
⏳ Remaining: [list of remaining steps]

📍 Progress: [progress bar] N/X steps (XX%)

🎯 Next: [next step description]

Continue? (Yes / Pause / Reroute / Stop)
───────────────────────────────────────────────────────────────
```

### Plan Presentation Format

```
📋 **PLAN CREATED**

**Query:** [original user query]
**Goal:** [identified goal]

**Plan:**
| Step | Skill | Purpose |
|------|-------|---------|
| 1 | [skill] | [purpose] |
| 2 | [skill] | [purpose] |
| ... | ... | ... |

**Total:** N steps

Start execution? (Yes / Modify / Cancel)
```

### Step Completion Format

```
✅ **Step N Complete**

**Skill:** [skill-name]
**Result:** [brief summary of what was accomplished]
**Artifacts:** [any outputs produced]

───────────────────────────────────────────────────────────────
📊 EXECUTION STATUS
[... standard status block ...]
───────────────────────────────────────────────────────────────
```

### Execution Complete Format

```
🏁 **EXECUTION COMPLETE**

**Query:** [original query]
**Goal:** [goal] — ✅ ACHIEVED

**Summary:**
| Step | Skill | Status | Notes |
|------|-------|--------|-------|
| 1 | [skill] | ✅ | [note] |
| 2 | [skill] | ✅ | [note] |
| ... | ... | ... | ... |

**Total steps:** N
**Artifacts produced:** [list]

**What's next?** New task / Save session / End
```

## Operational Rules

1. **ALWAYS SHOW STATUS:** Every message ends with execution status block
2. **ONE STEP AT A TIME:** Execute only the current step, then wait
3. **CONFIRMATION REQUIRED:** Always ask before proceeding to next step
4. **REBUILD ON REQUEST:** Create new plan when user asks
5. **CLEAR PROGRESS:** Step counter visible at all times (Step N of X)
6. **SIMPLE LANGUAGE:** Use clear, direct language

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Wrong plan** | User says "this isn't right" | Rebuild: create new plan |
| **Step failed** | Skill didn't produce expected output | Option to retry or skip |
| **Lost context** | User confusion | Show full status + plan |
| **Too many steps** | >8 steps | Simplify plan |

## Examples

### ❌ Without Chain-of-Skills
```
User: "Add dark mode to the app"
AI: [Writes code immediately without planning]
Result: Incomplete, breaks other features, no tests
```

### ✅ With Chain-of-Skills
```
User: "Add dark mode to the app"

📋 PLAN CREATED

Query: Add dark mode to the app
Goal: Working dark mode toggle with proper styling

Plan:
| Step | Skill | Purpose |
|------|-------|---------|
| 1 | goal-clarity-150 | Clarify dark mode requirements |
| 2 | research-150 | Understand current styling system |
| 3 | impact-map-150 | Map all affected components |
| 4 | action-plan-150 | Create implementation plan |
| 5 | gated-exec-150 | Implement dark mode |
| 6 | coverage-70-tests | Add tests |
| 7 | integrity-check-150 | Final quality check |

Total: 7 steps

Start execution? (Yes / Modify / Cancel)

User: "Yes"

⚡ EXECUTING — Step 1 of 7

Current skill: goal-clarity-150
Purpose: Clarify dark mode requirements

[... skill execution ...]

───────────────────────────────────────────────────────────────
📊 EXECUTION STATUS

✅ Completed: (none yet)
⚡ Current:   Step 1 — goal-clarity-150 — ✅ Complete
⏳ Remaining: Step 2-7

📍 Progress: ██░░░░░░░░░░░░░░ 1/7 steps (14%)

🎯 Next: Step 2 — research-150
   Purpose: Understand current styling system

Continue? (Yes / Pause / Reroute / Stop)
───────────────────────────────────────────────────────────────
```

## Relationship to Other Skills

- **chain-flow-150** → More complex, full orchestration logic
- **chain-of-skills** → Simpler, user-friendly, step-by-step experience
- **action-plan-150** → Creates plans within steps
- **gated-exec-150** → Executes code within steps

**Key difference:** `chain-of-skills` is the user-facing execution experience, while other skills are the individual actions in each step.

## Session Log Entry (MANDATORY)

After completing the chain, write to `.sessions/SESSION_[date]-[name].md`:

```
### [date - HH"MM] Chain-of-Skills 150 Complete
**Goal:** <original goal>
**Result:** <Success/Partial>
**Steps Executed:** <N>
**Artifacts:** <key outputs>
```

---

**Remember:** Scan skills → build plan → execute step by step → confirm each step. Simple, controlled, user in charge.
