---
name: ds-spec-reviewer
description: "Internal skill used by ds-brainstorm at Phase 1 exit gate. Dispatches a reviewer subagent to verify SPEC.md completeness before planning. NOT user-facing."
user-invocable: false
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-reviewer-readonly-guard.py"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-reviewer-readonly-guard.py"
---

# Spec Document Reviewer (Data Science)

**Purpose:** Catch spec gaps BEFORE they survive into data profiling, planning, and implementation.

## When to Dispatch

After Phase 1 (brainstorm) writes `.planning/SPEC.md` and before Phase 2 (ds-plan) begins.

```
Phase 1: Brainstorm -> SPEC.md written
  -> [THIS SKILL] Dispatch spec reviewer subagent
  -> Issues found? Fix SPEC.md -> re-dispatch reviewer
  -> Approved? -> Phase 2: ds-plan
```

<EXTREMELY-IMPORTANT>
## The Iron Law of Spec Review

**NO PLANNING WITHOUT REVIEWED SPEC. This is not negotiable.**

A bad spec that survives into planning means:
- Profiling data you don't need
- Missing data sources discovered mid-analysis
- Building analysis against incomplete objectives
- Implementing the wrong methodology

**Catching a spec gap NOW costs 1 minute. Catching it during implementation costs hours.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The spec looks complete to me" | Self-review is rubber-stamping | Dispatch independent reviewer |
| "User already confirmed the spec" | User confirms intent, not completeness | Reviewer checks what user might miss |
| "This will slow us down" | 30-second review saves hours of rework | Dispatch the reviewer |
| "It's a simple analysis, no review needed" | Simple specs have the most hidden assumptions | Review it anyway |
| "I'll catch issues during data profiling" | You'll profile the wrong data | Review BEFORE profiling |

### Red Flags - STOP If You Catch Yourself:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This spec looks complete to me" | Self-assessment is rubber-stamping — check EVERY section against the checklist | Read each section individually, verify none are empty or vague |
| "Spec looks similar to a prior one, should be fine" | Similar structure ≠ complete content — prior specs had different data sources and objectives | Evaluate THIS spec against THIS analysis's requirements |
| "The objectives are obvious, no need to scrutinize" | Obvious objectives hide unstated assumptions — the user's intent may differ from your inference | Verify objectives are specific, measurable, and user-confirmed |
| "Incomplete section is fine, they'll fill it in during planning" | Planning consumes the spec as-is — gaps survive into data profiling and task breakdown | Flag the gap NOW, before it propagates downstream |

## Dispatch Template

Use this Task invocation to dispatch the spec reviewer:

```
Agent(
  subagent_type="general-purpose",
  description="Review DS spec document",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  prompt="""
You are a data science spec document reviewer. Verify this spec is complete and ready for data profiling and analysis planning.

**Tool Restrictions:** The spec reviewer is READ-ONLY. It reads `.planning/SPEC.md`, evaluates against checklist, returns verdict. It MUST NOT use Write or Edit.

**Spec to review:** .planning/SPEC.md

Read the spec file, then evaluate against ALL categories below.

## What to Check

| Category | What to Look For |
|----------|------------------|
| Completeness | TODOs, placeholders, "TBD", incomplete sections, empty fields |
| Data Sources | All data sources identified with location, format, and time period |
| Analysis Objectives | Clear, specific questions the analysis will answer |
| Output Format | Expected deliverables specified (report, dashboard, model, tables) |
| Success Criteria | Measurable, specific, with clear pass/fail (not vague) |
| Reproducibility | Replication strategy documented if replicating existing work |
| Constraints | Timeline, methodology requirements, computational limits documented |
| Consistency | Internal contradictions, conflicting requirements |
| YAGNI | Unrequested analyses, over-engineering, scope creep |

## CRITICAL - Look Especially Hard For:

- Any TODO markers or placeholder text
- Sections saying "to be defined later" or "will spec when data is explored"
- Sections noticeably less detailed than others
- Data sources listed without location or format
- Analysis objectives that are vague ("explore the data", "find patterns")
- Success criteria that are unmeasurable ("good model", "interesting results")
- Missing replication/reproducibility strategy when replicating existing work
- Missing constraints section
- Output format unspecified (who consumes the results and how?)

## Output Format

## Spec Review

**Status:** APPROVED | ISSUES_FOUND

**Issues (if any):**
- [Section]: [specific issue] - [why it matters for planning]

**Recommendations (advisory - don't block approval):**
- [suggestions for improvement that aren't blocking]
""")
```

## Handling Reviewer Output

### If APPROVED
Proceed immediately to Phase 2 (ds-plan). Discover and load:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-plan/SKILL.md` and follow its instructions.

### If ISSUES_FOUND
1. Fix the specific issues in `.planning/SPEC.md`
2. Re-dispatch the reviewer (same template)
3. Repeat until APPROVED or max 5 iterations

### If 5 Iterations Without Approval
Escalate to user:
```
"Spec reviewer has flagged issues 5 times. Remaining issues:
[list issues]
Should I: (A) Fix these, (B) Proceed with known gaps, (C) Rethink the spec?"
```

## Drive-Aligned Framing

**Proceeding to data profiling with a flawed spec is NOT HELPFUL — wrong profiling produces wrong plans, which produce wrong analysis, wasting everyone's time.**

You know the spec has gaps. Profiling built on a bad spec profiles the wrong data. Plans built on wrong profiling produce wrong analysis. Implementation of a wrong plan wastes everyone's time and produces incorrect results.

**Fix the spec now. It costs minutes, not hours.**

## Gate Function

**Checkpoint type:** human-verify (spec completeness is machine-verifiable)

```
1. IDENTIFY: `.planning/SPEC.md` exists
2. DISPATCH: Send to reviewer subagent
3. READ: Reviewer returns APPROVED or ISSUES_FOUND
4. VERIFY: If ISSUES_FOUND, fix and re-dispatch (max 5)
5. CLAIM: Only proceed to ds-plan when APPROVED
```
