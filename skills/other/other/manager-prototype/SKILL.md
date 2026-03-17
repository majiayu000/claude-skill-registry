---
name: manager-prototype
description: "Demonstrates the Manager Pattern: Task does work, Forked Skill audits, Manager retries if needed. Use when iterative quality control is needed and audit must be isolated from implementation history."
context: fork
agent: general-purpose
skills:
  - context-topology
---

# Manager Pattern: Build → Audit → Retry

This skill demonstrates a **Manager** that orchestrates **Worker Tasks** and **Forked Auditors** with retry logic.

## Pattern Architecture

```
┌─────────────────────────────────────────────────────┐
│ Main: Skill(manager-prototype)                      │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Manager (this skill, shared context)                │
│ - Tracks: attempt_count, errors[], current_draft    │
│ - Orchestrates: Task(builder) + Skill(auditor)      │
└─────────────────────────────────────────────────────┘
              │                    │
              ▼                    ▼
┌─────────────────────┐   ┌─────────────────────────┐
│ Task(builder)       │   │ Skill(auditor)          │
│ - Fresh context     │   │ - context: fork         │
│ - Does the work     │   │ - agent: Explore        │
│ - Returns draft     │   │ - Pure audit (no bias)  │
└─────────────────────┘   └─────────────────────────┘
```

## Why This Pattern?

| Without Manager | With Manager + Forked Auditor |
| :--- | :--- |
| Main sees: "try 1 fail", "try 2 fail", "try 3 pass" | Main sees: only final "Done" |
| Auditor sees: 20 messages of struggling | Auditor sees: only the draft |
| Retry logic pollutes main context | Retry logic isolated in Manager |

## Implementation

### Step 1: Manager Invokes Builder Task

```markdown
# Invoke Task to do the work
Task(builder-unit, agent="general-purpose")

# Task runs in forked context, returns draft to Manager
```

### Step 2: Manager Invokes Forked Auditor

```markdown
# Invoke auditor with context: fork (ISOLATED)
Skill(quality-auditor)

# Auditor sees ONLY:
# - CLAUDE.md
# - The draft (passed as argument)
# - Its own SKILL.md
#
# Auditor does NOT see:
# - Previous 5 failed attempts
# - Manager's retry logic
# - Any implementation history
```

### Step 3: Auditor Returns Pass/Fail

```markdown
# quality-auditor.skILL.md:
---
context: fork
agent: Explore
---

## Audit Result

### Draft: {passed content}
### Status: PASS | FAIL

### Issues Found:
- {issue 1}
- {issue 2}

### Recommendation:
{fix guidance}
```

### Step 4: Manager Retries or Returns

```markdown
# In Manager:
If audit.status == "FAIL":
    Spawn Task(builder-unit) again  # Fresh context
    Increment attempt_count
Else:
    Return "Done" to Main
```

## Complete Workflow Example

```markdown
# MAIN CONTEXT:
Skill(manager-prototype)

# MANAGER (this skill):
1. Invoke: Task(builder-unit) with "Create a skill for X"
2. Receive: draft_skill.md content
3. Invoke: Skill(quality-auditor) with draft_skill.md
4. Receive: {status: "FAIL", issues: ["missing frontmatter"]}
5. If attempt_count < 3:
   - Invoke: Task(builder-unit) with "Fix missing frontmatter"
   - Receive: revised_draft
   - Invoke: Skill(quality-auditor) with revised_draft
   - Receive: {status: "PASS"}
6. Return: "Skill created in 2 attempts. All quality gates passed."

# MAIN CONTEXT SEES ONLY:
"Skill created in 2 attempts. All quality gates passed."
```

## Alternative: Inline Iteration (Simpler)

```markdown
❌ MORE COMPLEX: Manager Pattern
Task(builder-unit)  # Fork 1
→ Skill(auditor)    # Fork 2
→ Task(builder-unit) # Fork 3 (retry)
→ Skill(auditor)    # Fork 4 (re-audit)

✅ SIMPLER: Inline iteration
Task(builder-unit)  # Single fork
# Builder handles its own iteration internally
# Returns final result
```

## When Manager Pattern IS Worth It

| Scenario | Why Use |
| :--- | :--- |
| **Auditor must be unbiased** | Forked auditor never sees implementation history |
| **Complex multi-phase work** | Task handles phases, Auditor validates result |
| **External quality standards** | Auditor enforces rules, Task focuses on content |
| **Audit is expensive** | Don't repeat audit if Task can self-correct |

## When to Avoid

| Scenario | Why Avoid |
| :--- | :--- |
| Simple retry logic | Inline Task iteration is simpler |
| Single-pass quality check | Task + final audit is enough |
| Low iteration count | Overhead not justified |
| Auditor is cheap | Can audit after each attempt inline |

## Key Insight: Context Accumulation

The Manager **accumulates history** (each retry adds messages). The Auditor is **isolated** (never sees retries).

```
Manager Context:
[Attempt 1: draft v1]
[Audit: FAIL - missing X]
[Attempt 2: draft v2]
[Audit: FAIL - missing Y]
[Attempt 3: draft v3]
[Audit: PASS]
→ Manager is "heavy" but that's OK

Auditor Context (each time):
[Only: draft v1] → FAIL
[Only: draft v2] → FAIL
[Only: draft v3] → PASS
→ Auditor is always "light" and unbiased
```

## Cost/Benefit Summary

| Aspect | Cost | Benefit |
| :--- | :--- | :--- |
| **Complexity** | High (3 components, retry logic) | Clean separation of concerns |
| **Token usage** | Multiple forks (4+ invocations) | Isolation reduces audit overhead |
| **Context** | Manager accumulates retry history | Auditor stays pure (no history) |
| **Reliability** | More chances for failure | Each attempt is fresh |

## Recommendation

**Use this pattern when:**
- Quality audit is complex and must be unbiased
- Implementation requires multiple iterations
- The work product is high-stakes

**Use simpler alternatives when:**
- Single-pass is sufficient
- Retry logic is simple (inline is fine)
- Auditor can be invoked once at the end

---

## P1 Use Case: Skill Creation Pipeline

This is the **highest-value use case** for thecattolkit: creating skills with automatic quality validation.

### Architecture

```
Main → Skill(skill-manager)
       → Task(create-skill)
       → Skill(quality-standards, context: fork)
         → Returns: Pass/Fail + issues
       → If Fail: Retry Task(create-skill)
       → If Pass: Return "Skill created"

quality-standards skill has:
- context: fork (isolated auditor)
- agent: Explore (read-only)
```

### Why This Works for Skill Creation

| Requirement | How Manager Pattern Addresses It |
| :--- | :--- |
| **Frontmatter validation** | quality-standards checks What-When-Not format |
| **Navigation table** | Validates "If you need X → Read Y" structure |
| **critical_constraint footer** | Ensures non-negotiable rules present |
| **References structure** | Verifies references/ is justified or empty |
| **Unbiased audit** | Auditor never sees "I tried 5 times" |

### Example Flow

```markdown
# User requests:
"Create a skill for processing images"

# Main invokes:
Skill(skill-manager)

# Manager executes:
1. Task(create-skill) with:
   - name: image-processor
   - description: "Process images..."
   - template: skill-development

2. Receives: draft_SKILL.md (missing frontmatter!)

3. Invokes: Skill(quality-standards)
   - Passes: draft_SKILL.md
   - Auditor reads draft (sees ONLY the draft)
   - Returns: {status: "FAIL", issues: ["Missing frontmatter"]}

4. Manager retries:
   - Task(create-skill) with: "Fix: add frontmatter with What-When-Not"

5. Receives: revised_draft (has frontmatter now)

6. Invokes: Skill(quality-standards)
   - Returns: {status: "FAIL", issues: ["Missing navigation table"]}

7. Manager retries:
   - Task(create-skill) with: "Fix: add navigation table"

8. Receives: final_draft (all gates pass)

9. Returns: "Skill 'image-processor' created. 2 attempts. All quality gates passed."
```

### quality-standards as Forked Auditor

```yaml
# .claude/skills/quality-standards/SKILL.md
---
name: quality-standards
description: "Verify completion with evidence..."
context: fork    # Critical: isolates from retry history
agent: Explore   # Critical: read-only, cannot modify files
auto_load_triggers:
  - pattern: "\\.claude/skills/"
    skill: "skill-development
---
```

**Key configuration:**
- `context: fork` → Auditor never sees implementation attempts
- `agent: Explore` → Cannot accidentally modify files during audit
- `auto_load_triggers` → Auto-invoked when skills are modified

### When P1 This Pattern is Worth It

| Skill Creation Scenario | Use Manager Pattern |
| :--- | :--- |
| Complex multi-section skill | ✅ Yes (multiple quality gates) |
| Teaching new developers | ✅ Yes (enforces standards) |
| Batch skill creation | ✅ Yes (consistent quality) |
| Simple one-line skill | ❌ No (overkill) |
| Quick prototype | ❌ No (inline is fine)
