---
name: 50-execute-gated-150
description: "[50] EXECUTE. Execute plans step-by-step with confirmation gates. Each step requires user approval before proceeding. Includes change management lifecycle (Pre-Change → During → Post-Change → Rollback). Use when implementing approved plans, deploying changes, or any multi-step execution requiring control and reversibility."
---

# Execute-Gated 150 Protocol

**Core Principle:** Execute with control. Every step gets a gate — confirm before proceeding. Build in rollback points. Maintain audit trail.

## What This Skill Does

When you invoke this skill, you're asking AI to:
- **Execute step-by-step** — One atomic action at a time
- **Gate every step** — Get confirmation before next step
- **Manage change lifecycle** — Pre/During/Post/Rollback phases
- **Stay reversible** — Every step can be undone
- **Adapt dynamically** — Pause, research, or replan when needed

## The 150% Execution Rule

| Dimension | 100% Core | +50% Enhancement |
|-----------|-----------|------------------|
| **Steps** | Execute sequence | + Atomic, reversible actions |
| **Gates** | Get confirmation | + Offer Continue/Pause/Research/Replan |
| **Documentation** | Log actions | + Full audit trail |
| **Rollback** | Have revert plan | + Pre-identified safe points |

## When to Use This Skill

- **Implementing approved plans** — After action-plan-150
- **Deploying changes** — Code, config, infrastructure
- **Multi-step operations** — Migrations, refactoring
- **High-risk executions** — Where mistakes are costly
- **When user needs control** — They decide pace and direction

## Execution Protocol

### Step 1: ACTIVATE
Declare execution mode and current state:
```
⚙️ **Gated-Exec 150 Activated**

**Plan:** [What we're executing]
**Total Steps:** [N]
**Current Phase:** [1 of N]
**Rollback Points:** [Where we can safely stop]
```

### Step 2: PRE-CHANGE
Before each step:
- Verify prerequisites met
- Backup current state if needed
- Validate change safety
- Confirm readiness

### Step 3: EXECUTE
Single atomic step:
- Execute one reversible action
- Monitor for immediate issues
- Document what was done

### Step 4: VALIDATE
After each step:
- Check completion
- Verify expected outcomes
- Flag any anomalies

### Step 5: GATE
Present decision point:
```
✅ **Step [X/N] Complete**

**Action:** [What was done]
**Result:** [Outcome]
**Next:** [What's coming]

**Options:**
- **Continue** → Proceed to next step
- **Pause** → Stop for clarification
- **Research** → Need more investigation
- **Replan** → Strategy needs modification
- **Rollback** → Revert to safe point
```

## Change Management Lifecycle

```
🔄 CHANGE LIFECYCLE

PRE-CHANGE (Before each step)
├── Impact analysis complete
├── Risk assessment done
├── Backup strategy ready
└── Rollback plan documented

DURING CHANGE (Execution)
├── Atomic step execution
├── Real-time monitoring
├── Immediate issue detection
└── Progress tracking

POST-CHANGE (After each step)
├── Outcome verification
├── Integration testing
├── Performance validation
└── Documentation update

ROLLBACK READY (Always)
├── Safe reversal path
├── State restoration
├── Impact minimization
└── Lesson documentation
```

## Decision Gates

| Situation | Action | Reason |
|-----------|--------|--------|
| **Step Success** | Get confirmation, proceed | Maintain control |
| **Minor Issue** | Document, continue with caution | Don't stop for small problems |
| **Major Problem** | Pause, investigate, possibly rollback | Prevent cascading failures |
| **Plan Deviation** | Replan with user approval | Maintain strategic alignment |
| **New Information** | Research, update plan | Adapt to new insights |

## Output Format

During execution:

```
⚙️ **Gated-Exec: Step [X/N]**

**Phase:** [Current phase name]
**Action:** [What we're doing]

[Execution details...]

**Result:** ✅ Success | ⚠️ Issues | ❌ Failed

**Status:**
├── ✅ Completed: [Steps done]
├── 🔄 Current: [This step]
└── ⏳ Pending: [Steps remaining]

**Rollback Point:** [Last safe state]

**Continue?** (Yes / Pause / Research / Replan / Rollback)
```

## Operational Rules

1. **ATOMIC STEPS:** Each step must be reversible and testable
2. **GATE REQUIRED:** No proceeding without user confirmation
3. **DOCUMENT EVERYTHING:** Full audit trail of all actions
4. **FLEXIBLE ADAPTATION:** Can return to research/planning anytime
5. **CHANGE LIFECYCLE:** Always use Pre/During/Post/Rollback phases
6. **USER CONTROL:** User decides pace and direction

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Phase Skipping** | No confirmation obtained | Return to skipped gate |
| **Poor Documentation** | Missing audit trail | Document current state, continue with logging |
| **Change Cascades** | Unexpected side effects | Rollback to safe point, investigate |
| **Loss of Control** | Process confusion | Emergency pause, status assessment |

## Examples

### ❌ Without Gated-Exec
```
User: "Deploy the new feature"
AI: [Deploys all 5 steps without confirmation]
Result: Breaking change deployed, emergency rollback needed
```

### ✅ With Gated-Exec 150
```
User: "Deploy the new feature"

⚙️ Gated-Exec 150 Activated

Plan: Feature deployment
Total Steps: 5
Rollback Points: After step 2, After step 4

---

⚙️ Gated-Exec: Step 1/5

Phase: Database Migration
Action: Run migration script

[Migration executed successfully]

Result: ✅ Success
- 3 tables updated
- No data loss
- Backup created

Continue? (Yes/Pause/Research/Replan/Rollback)

User: "Yes"

⚙️ Gated-Exec: Step 2/5
...
```

## Relationship to Other Skills

- **action-plan-150** → Creates the plan
- **gated-exec-150** → Executes the plan with control
- **integrity-check-150** → Validates after completion

---

**Remember:** Gated execution isn't slow — it's safe. The gates prevent costly mistakes and keep you in control. Every "Yes" is a conscious decision, every step is reversible.

