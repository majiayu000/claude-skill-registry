---
name: dev-spec-reviewer
description: "Internal skill used by dev-brainstorm at Phase 1 exit gate. Dispatches a reviewer subagent to verify SPEC.md completeness before exploration. NOT user-facing."
user-invocable: false
disable-model-invocation: true
---

# Spec Document Reviewer

**Purpose:** Catch spec gaps BEFORE they survive into exploration, design, and implementation.

## When to Dispatch

After Phase 1 (brainstorm) writes `.planning/SPEC.md` and before Phase 2 (explore) begins.

```
Phase 1: Brainstorm → SPEC.md written
  → [THIS SKILL] Dispatch spec reviewer subagent
  → Issues found? Fix SPEC.md → re-dispatch reviewer
  → Approved? → Phase 2: Explore
```

<EXTREMELY-IMPORTANT>
## The Iron Law of Spec Review

**NO EXPLORATION WITHOUT REVIEWED SPEC. This is not negotiable.**

A bad spec that survives into exploration means:
- Exploring the wrong areas of the codebase
- Clarifying the wrong ambiguities
- Designing against incomplete requirements
- Implementing the wrong thing

**Catching a spec gap NOW costs 1 minute. Catching it during implementation costs hours.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The spec looks complete to me" | Self-review is rubber-stamping | Dispatch independent reviewer |
| "User already confirmed the spec" | User confirms intent, not completeness | Reviewer checks what user might miss |
| "This will slow us down" | 30-second review saves hours of rework | Dispatch the reviewer |
| "It's a simple feature, no review needed" | Simple specs have the most hidden assumptions | Review it anyway |
| "I'll catch issues during exploration" | You'll explore the wrong things | Review BEFORE exploring |

## Dispatch Template

Use this Task invocation to dispatch the spec reviewer:

```
Agent(
  subagent_type="general-purpose",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  description="Review spec document",
  prompt="""
You are a spec document reviewer. Verify this spec is complete and ready for codebase exploration and implementation planning.

**Tool Restrictions:** You are READ-ONLY. You MUST NOT use Write or Edit tools. You read `.planning/SPEC.md`, evaluate it against the checklist, and return a verdict. If you find issues, you report them — the main chat fixes them.

**Spec to review:** .planning/SPEC.md

Read the spec file, then evaluate against ALL categories below.

## What to Check

| Category | What to Look For |
|----------|------------------|
| Completeness | TODOs, placeholders, "TBD", incomplete sections, empty fields |
| Coverage | Missing error handling, edge cases, integration points |
| Consistency | Internal contradictions, conflicting requirements |
| Clarity | Ambiguous requirements that could be interpreted multiple ways |
| YAGNI | Unrequested features, over-engineering, gold-plating |
| Scope | Focused enough for a single implementation — not covering multiple independent features |
| Testing | Testing strategy section filled (not empty or "manual only") |
| Success Criteria | Measurable, specific, with clear pass/fail (not vague) |

## CRITICAL — Look Especially Hard For:

- Any TODO markers or placeholder text
- Sections saying "to be defined later" or "will spec when X is done"
- Sections noticeably less detailed than others
- Testing strategy that says "manual" (this is a BLOCKER in workflows:dev)
- Success criteria that are vague ("works well", "is fast", "handles errors")
- Requirements that contradict each other
- Missing constraints section

## Output Format

## Spec Review

**Status:** APPROVED | ISSUES_FOUND

**Issues (if any):**
- [Section]: [specific issue] - [why it matters for implementation]

**Recommendations (advisory — don't block approval):**
- [suggestions for improvement that aren't blocking]
""")
```

## Handling Reviewer Output

### If APPROVED
Proceed immediately to Phase 2 (explore):

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-explore/SKILL.md` and follow its instructions.

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

**Proceeding to exploration with a flawed spec is NOT HELPFUL — you'll explore the wrong areas and build the wrong thing, creating hours of rework.**

You know the spec has gaps. Exploration built on a bad spec produces bad findings. Design built on bad findings produces a bad plan. Implementation of a bad plan wastes everyone's time.

**Fix the spec now. It costs minutes, not hours.**

## Gate Function

```
1. IDENTIFY: `.planning/SPEC.md` exists
2. DISPATCH: Send to reviewer subagent
3. READ: Reviewer returns APPROVED or ISSUES_FOUND
4. VERIFY: If ISSUES_FOUND, fix and re-dispatch (max 5)
5. CLAIM: Only proceed to explore when APPROVED
```
