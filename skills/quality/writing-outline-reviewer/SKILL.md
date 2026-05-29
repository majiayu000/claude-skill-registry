---
name: writing-outline-reviewer
description: "Internal skill used by writing-outline at exit gate. Dispatches a reviewer subagent to verify OUTLINE.md quality before drafting. NOT user-facing."
user-invocable: false
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Agent
---

# Outline Document Reviewer

**Purpose:** Catch outline gaps BEFORE they survive into drafting. A thin outline that survives into drafting means every section is improvised, every transition is missing, and every draft rewrites from scratch.

## Shared Enforcement

Read the constraint index: `${CLAUDE_PLUGIN_ROOT}/references/writing-common-constraints.md`

Then load these reviewer-specific files:

**Constraints:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progressive-expansion-hierarchy.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/flowchart-authority.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progress-gating.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/drive-aligned-default.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/claim-id-traceability.md`

**Conventions:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/gate-function-standard.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/artifact-review-gates.md`

## When to Dispatch

After writing-outline completes `.planning/OUTLINE.md` (master outline) and all section outlines in `outlines/`, before writing-draft begins.

```
Outline phase complete → all outlines/ files written
  → [THIS SKILL] Dispatch outline reviewer subagent
  → For outlines with 10+ sections: review in groups of 3-4
  → Issues found? Fix outlines → re-dispatch reviewer
  → Approved? → Draft phase: writing-draft
```

<EXTREMELY-IMPORTANT>
## The Iron Law of Outline Review

**NO DRAFTING WITHOUT REVIEWED OUTLINE. This is not negotiable.**

A bad outline that survives into drafting means:
- Sections that don't map to any PRECIS claim
- Subsections with topics but no POINT, EVIDENCE, or LOGIC
- Missing transitions that fragment the argument
- Scope violations that bloat the document
- Filler sections that exist because "papers usually have this" not because the argument needs it

**Catching an outline gap NOW costs 1 minute. Catching it during drafting costs a full rewrite.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The outline looks fine to me" | Self-review is rubber-stamping | Dispatch independent reviewer |
| "User already approved the structure" | User approves the approach, not subsection depth | Reviewer checks what user might miss |
| "This will slow us down" | 30-second review saves hours of drafting rework | Dispatch the reviewer |
| "It's a simple structure, no review needed" | Simple structures hide the most missing transitions | Review it anyway |
| "I'll figure out the details during drafting" | Drafting without structure is improvising, not writing | Review BEFORE drafting |

## Chunking Rule

**If the outline has 10+ sections (across OUTLINE.md and outlines/ files):** Review in groups of 3-4 sections. Each group should be logically related (e.g., "introduction + background", "core argument sections", "counterarguments + conclusion").

**If the outline has <10 sections:** Review the entire outline in one pass.

**Why chunk:** Monolithic review of large outlines produces shallow feedback. Focused review per group catches more issues.

## Dispatch Template (Single Pass or Per-Chunk)

Use this Task invocation to dispatch the outline reviewer:

```
Agent(
  subagent_type="general-purpose",
  description="Review outline documents",
  prompt="""
You are an outline document reviewer. Verify this outline is complete, maps to the PRECIS, and is ready for prose drafting.

**Tool restrictions:** You may ONLY use Read, Grep, and Glob tools. Do NOT use Write, Edit, or Bash. Your job is to evaluate, not fix.

**Master outline:** .planning/OUTLINE.md [— Chunk: sections N-M only, if chunked]
**Section outlines:** outlines/ directory
**Precis for reference:** .planning/PRECIS.md

Read ALL files, then evaluate the outline against ALL categories below.

## What to Check

| Category | What to Look For |
|----------|------------------|
| PRECIS Mapping | Every claim in PRECIS.md has at least one section advancing it. No orphan claims. No orphan sections (sections that don't serve any claim). |
| Transitions | Every section has a planned transition to the next. Missing transitions = fragmented argument. |
| Scope Honored | No sections that fall outside PRECIS scope IN. No sections covering PRECIS scope OUT items. |
| Section Purpose | Every section has a clear purpose (not filler like "background" without specific goals). Each section earns its place. |
| Subsection Depth | Each section outline in outlines/ has POINT + EVIDENCE + LOGIC for every subsection. Topic lists without these are NOT outlines. |
| Evidence Mapping | Sources are mapped to specific points, not vaguely listed at the end. |
| Completeness | Every section in OUTLINE.md has a corresponding file in outlines/. No TODOs, TBDs, or placeholders. |
| Internal Consistency | Sections don't contradict each other. Claims don't repeat across sections. |

## CRITICAL — Look Especially Hard For:

- Sections in OUTLINE.md with NO corresponding outlines/ file
- Subsections that list topics but lack POINT, EVIDENCE, or LOGIC
- Transitions that are missing or say "TBD"
- Sections that exist "because papers usually have this" not because the argument needs them
- PRECIS claims not covered by ANY section
- Sections that drift outside PRECIS scope
- Evidence listed without connection to a specific point
- Counterargument sections that address strawmen instead of the objections in PRECIS

## Output Format

## Outline Review

**Status:** APPROVED | ISSUES_FOUND

**Issues (if any):**
- [Section/File]: [specific issue] - [why it matters for drafting]

**PRECIS Coverage Check:**
- [Claim 1]: Covered by Section N ✅ | NOT COVERED ❌
- [Claim 2]: Covered by Section N ✅ | NOT COVERED ❌

**Recommendations (advisory — don't block approval):**
- [suggestions for improvement that aren't blocking]
""")
```

## Handling Reviewer Output

### If APPROVED
Proceed immediately to draft phase. Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-draft/SKILL.md` and follow its instructions.

### If ISSUES_FOUND
1. Fix the specific issues in the relevant outline files
2. Re-dispatch the reviewer (same template)
3. Repeat until APPROVED or max 5 iterations

### If 5 Iterations Without Approval
Escalate to user:
```
"Outline reviewer has flagged issues 5 times. Remaining issues:
[list issues]
Should I: (A) Fix these, (B) Proceed with known gaps, (C) Rethink the outline?"
```

## Drive-Aligned Framing

**Proceeding to draft with a thin outline is NOT HELPFUL — every section will be improvised, transitions will fragment, and the user rewrites from scratch.**

You know the subsections lack evidence mapping. You know the transitions are missing. You know some sections don't advance any claim. Drafting built on a thin outline produces improvised prose that wanders, asserts without evidence, and fragments between sections.

**Fix the outline now. It costs minutes, not hours.**

## Gate Function

```
1. IDENTIFY: `.planning/OUTLINE.md` and all `outlines/*.md` files exist
2. DISPATCH: Send to reviewer subagent (per-chunk if 10+ sections)
3. READ: Reviewer returns APPROVED or ISSUES_FOUND
4. VERIFY: If ISSUES_FOUND, fix and re-dispatch (max 5)
5. CLAIM: Only proceed to drafting when ALL chunks APPROVED
```
