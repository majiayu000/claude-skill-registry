---
name: thinking-critically
description: Deep engineering analysis before implementation (Phase 2 of 9-Phase Feature Cycle). Challenges assumptions, identifies unknowns, and prevents architectural mistakes. Use when planning complex features, writing PRDs, designing systems, or before any significant code changes.
globs: ["docs/features/**/spec.md", "docs/features/**/analysis.md", "docs/architecture/**"]
---

# Thinking Critically

Rigorous pre-implementation analysis that simulates a paranoid staff engineer review. This skill prevents costly architectural mistakes by forcing systematic examination of assumptions, trade-offs, and failure modes **before** writing code.

**Phase 2 of the 9-Phase Feature Development Cycle:**
```
Interview -> THINK CRITICALLY -> Plan -> Branch -> Implement -> Verify -> PR -> Merge -> Wrap-Up
              ^ YOU ARE HERE
```

## Philosophy

```
"The best time to find a design flaw is before you write the code."
"Every assumption you don't question is a bug waiting to happen."
```

## When to Use

- Planning a new feature or system (Phase 2 of Feature Cycle)
- Writing or reviewing a PRD
- Making architectural decisions
- Before implementing anything complex
- When something "feels off" but you can't articulate why
- After getting initial requirements, before diving into code

## Prerequisites

- Feature spec completed (Phase 1: Interview complete)
- `docs/features/FEAT-XXX/spec.md` exists with decisions
- `docs/project.md` exists (for project context)
- `docs/architecture/_index.md` exists (for technical constraints)

## Process

### 0. Read Context First

```bash
# Read feature spec (REQUIRED - output of Interview phase)
cat docs/features/FEAT-XXX/spec.md

# Read project context
cat docs/project.md 2>/dev/null

# Read architecture constraints
cat docs/architecture/_index.md 2>/dev/null

# Check current status
cat docs/features/FEAT-XXX/status.md
```

### 0.1 Determine Analysis Depth

```
AUTOMATIC ABBREVIATION RULES

Condition                        | Steps Executed     | Reason
---------------------------------|--------------------|-----------------------
New feature + new system         | All 11 steps       | Max architectural risk
New feature + existing patterns  | 1-2-3-5-9-11      | Medium risk
Small/clear scope feature        | 1-2-5-11          | Low risk
Bug fix / hotfix                 | SKIP entirely      | No architectural risk

When in doubt -> execute ALL 11 steps
```

## The 11-Step Critical Analysis Protocol

Execute ALL steps in order. Do not skip steps unless explicitly told to or abbreviation rules apply.

### Step 1: Problem Clarification & Constraints
Define exactly what we're solving and within what boundaries.

### Step 2: Implicit Assumptions Identification (CRITICAL)
Surface hidden assumptions that could invalidate the entire approach.
**Most failures stem from unstated assumptions.**

### Step 3: Design Space Exploration
Enumerate possible approaches before committing to one.

### Step 4: Trade-off Analysis
Explicitly weigh competing concerns.

### Step 5: Failure-First Analysis
Systematically identify what can go wrong.

### Step 6: Boundaries & Invariants
Define what must ALWAYS be true and what the system will NEVER do.

### Step 7: Observability & Control
Ensure the system can be monitored and managed.

### Step 8: Reversibility & Entropy
Assess how hard it is to undo decisions and recover from mistakes.

### Step 9: Adversarial Review (Paranoid Staff Engineer Mode)
Attack the design from every angle.

### Step 10: AI Delegation Assessment
Determine what AI (Ralph Loop) can safely handle vs what needs human oversight.

### Step 11: Decision Summary
Synthesize everything into actionable conclusions.

## Critical Rules

```
1. NEVER skip Step 2 (Assumptions) - most failures stem from here

2. If ANY assumption has Low confidence + High impact -> STOP
   Validate with user before proceeding

3. Step 9 must be genuinely adversarial - attack your own design

4. All 11 steps for complex/critical features
   Steps 1-2-5-11 for smaller features

5. In Ralph Loop: auto-PAUSE if confidence is Low in Step 11
```

## Ralph Loop Integration

When running autonomously via Ralph Loop:

```
Iteration 1: INTERVIEW -> reads spec.md, pauses if TBD -> emits INTERVIEW_COMPLETE
Iteration 2: THINK CRITICALLY -> executes protocol -> emits ANALYSIS_COMPLETE
             AUTO-PAUSE if:
             - Low confidence + High impact assumption found
             - Step 9 identifies critical red flag
             - Step 11 confidence level is "Low"
Iteration 3: PLAN -> reads spec.md + analysis.md -> generates design.md + tasks.md
```

## How Analysis Feeds Plan Phase

The Plan phase reads `analysis.md` **in addition to** `spec.md` to:
- Select recommended approach (from Step 11)
- Incorporate failure mitigations (from Step 5) into design
- Include invariants/boundaries (from Step 6) as validations
- Use AI delegation matrix (from Step 10) to decide Ralph automation scope
- Add observability requirements (from Step 7) to implementation tasks

## Output

After completing the protocol, save output to `docs/features/FEAT-XXX/analysis.md`

## Status Updates

After completing analysis:

1. **Update status.md:**
   Phase: Critical Analysis complete

2. **Update _index.md:**
   Feature status updated with phase progress

3. **Update context/decisions.md** with key decisions from Step 11

4. **Append to status-log.md** with action record
