---
name: writing-revise
version: 1.0
description: "This skill should be used when the user asks to 'revise writing', 'fix review issues', 'polish draft', 'apply review feedback', 'complete writing workflow', or after /writing-review produces REVIEW.md with issues to fix."
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/writing-suggest-verify.py"
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/writing-claim-id-guard.py"
---

# Writing Revise

The revision loop for writing projects. Consumes `.planning/REVIEW.md` (produced by `/writing-review`) and applies targeted fixes, then completes the workflow when all issues are resolved.

## Shared Enforcement

Load the constraint index:

!`cat ${CLAUDE_SKILL_DIR}/../../references/writing-common-constraints.md`

Then load these phase-specific files:

**Constraints:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progressive-expansion-hierarchy.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/constraint-loading-protocol.md` — **CRITICAL: load domain skill + ai-anti-patterns before revising prose**
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/flowchart-authority.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/no-pause-between-phases.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progress-gating.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/post-subagent-enforcement.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/topic-change-protocol.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/writing-stop-triggers.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/drive-aligned-default.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/context-monitoring.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/deviation-rules.md`

**Conventions:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/gate-function-standard.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/phase-summary-frontmatter.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/checkpoint-type-classification.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/autonomous-phase-chaining.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/iteration-topology.md`

## Session Resume Detection

Before starting, check for an existing handoff:

1. Check if `.planning/HANDOFF.md` exists
2. **If found:** Read it and present to user:
   - Show the phase, section in progress, and Next Action
   - Ask: "Resume from handoff, or start fresh?"
   - If resume: skip to the recorded phase
   - If fresh: proceed with mode detection
3. **If not found:** Proceed normally

## Revise Flowchart (This IS the Spec)

```
START
  │
  ├─ Step 1: Load context (ACTIVE_WORKFLOW, PRECIS, OUTLINE, drafts)
  │
  ├─ Step 2: REVIEW.md exists?
  │  ├─ NO → REFUSE. Suggest /writing-review. EXIT.
  │  └─ YES → Parse issues (critical → major → minor)
  │
  ├─ Step 3: Load constraint layers
  │  ├─ Domain skill (legal/econ/general)
  │  └─ ai-anti-patterns (universal)
  │
  ├─ Step 4: Fix issues in priority order
  │  ├─ 4a: Critical issues (argument-breaking)
  │  ├─ 4b: Major issues (transitions, repetition, late introductions)
  │  └─ 4c: Minor issues (polish)
  │
  ├─ Step 5: Formatting check
  │
  └─ Step 6: Check iteration state (.planning/REVIEW_STATE.md)
     │
     ├─ No issues remain → COMPLETE
     │  └─ Archive workflow → Generate summary → EXIT
     │
     ├─ iteration < 3 AND issues remain → CONTINUE
     │  └─ Increment iteration → Re-invoke /writing-review → Loop
     │
     └─ iteration >= 3 AND issues remain → ESCALATE
        └─ Report to user with options → EXIT
```

If text and flowchart disagree, the flowchart wins.

<EXTREMELY-IMPORTANT>
## IRON LAW: Critique Over Comfort

**If the writing has problems, SAY SO. Being nice is NOT HELPFUL — the user publishes weak prose that gets rejected.**

### Red Flag Detection

If you catch yourself thinking:
- "This is pretty good overall" - STOP. Find the weakness.
- "I don't want to be too harsh" - STOP. Harsh is kind.
- "The author probably knows what they're doing" - STOP. Check anyway.
</EXTREMELY-IMPORTANT>

### Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "It's a draft, I'll be gentle" | Drafts need MORE critique, not less | Critique hardest on drafts |
| "The main point is clear enough" | "Clear enough" means unclear | Find the ambiguity and fix it |
| "I'll focus on positives first" | Positives don't help improve writing | Lead with problems |
| "This is good enough for a first pass" | "Good enough" is reward hacking | Find specific problems to fix |
| "The user will polish it themselves" | Relying on human editing defeats the workflow | Fix it now |
| "I don't want to discourage the writer" | False kindness produces bad writing | Honest critique is the kindest act |
| "The argument flows well overall" | "Overall" hides section-level problems | Check each section against PRECIS claims |
| "Minor style issues aren't worth flagging" | Minor issues compound into unprofessional prose | Flag every issue you find |
| "The structure matches the outline" | Structural match doesn't mean quality match | Check content quality, not just structure |
| "This section is creative, rules don't apply" | Creative writing still needs clarity and precision | Apply rules, note creative exceptions explicitly |

**Reporting "all checks pass" without actually running every check is NOT HELPFUL — uncaught issues survive into the final draft.** You must have evidence for every checkmark. An unchecked box with "assumed OK" means the user publishes with undetected problems.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Re-Review

**NO "FIXED" CLAIMS WITHOUT FRESH RE-REVIEW. This is not negotiable.**

After applying fixes from REVIEW.md, you MUST:
1. Re-invoke `/writing-review` to regenerate REVIEW.md with fresh diagnostics
2. Verify issues are actually resolved (not assumed)
3. Check for new issues introduced by edits (regressions, new problems)
4. Only THEN claim fixes are complete

"I fixed it" without re-reviewing is NOT HELPFUL — unverified fixes let broken prose reach the user.

### The Audit-Fix Loop (Max 3 Iterations)

```
Iteration 1: Review → REVIEW.md → Revise → Re-Review
              ↓
Iteration 2: Re-Review → REVIEW.md → Revise → Re-Review
              ↓
Iteration 3: Re-Review → REVIEW.md → Revise → Re-Review
              ↓
         Still issues? → ESCALATE to user
         All clean? → COMPLETE
```

**Track iterations in `.planning/REVIEW_STATE.md`:**

```yaml
---
iteration: 1
max_iterations: 3
last_review_date: 2026-03-09
issues_found_count: 5
---
```

**Exit criteria:**
- **COMPLETE**: Zero issues found in REVIEW.md
- **ESCALATE**: iteration >= 3 AND issues remain
- **CONTINUE**: iteration < 3 AND issues remain → re-invoke /writing-review

**Before claiming "all fixed", check iteration count:**
1. READ `.planning/REVIEW_STATE.md` (create if missing with iteration: 1)
2. If iteration >= 3 and issues remain: ESCALATE (don't say "run review again")
3. If iteration < 3 and issues remain: INCREMENT iteration, re-invoke /writing-review
4. If no issues: COMPLETE

**Claiming "all issues resolved" without re-reviewing is NOT HELPFUL — the user trusts a false "all clear" and publishes with remaining problems.**

### Rationalization Prevention (Re-Review)

| Thought | Reality | Do Instead |
|---------|---------|------------|
| "I fixed the issues from REVIEW.md" | Your fixes need verification | Re-invoke /writing-review |
| "Just spot-check the edited sections" | Spot-checks miss cascading changes | Full re-review via /writing-review |
| "We're on iteration 3, call it done" | Max iterations means ESCALATE, not approve | Report to user with remaining issues |
| "The edits are minor, skip re-review" | Minor edits create subtle problems | Re-review anyway |
| "We've spent enough time on this" | Publishing flawed writing wastes more time | Re-review or escalate |
| "The draft looks clean now" | Looking clean != being clean | Re-run /writing-review to verify |

### Why Skipping Re-Review Hurts the Thing You Care About Most

You skip re-review because you think it's helpful, efficient, or competent. Here's what actually happens:

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Finishing fast helps the user move on" | Draft has remaining issues. User submits. Reviewers reject. The 15-minute re-review would have caught it. Your speed caused waste. | **Anti-helpful** |
| **Competence** | "I can tell the draft is clean" | Your eyes glaze over your own edits. Fresh review catches what you miss. The draft has 3 remaining issues. Your judgment failed. | **Incompetent** |
| **Efficiency** | "Re-review wastes time on fixed work" | The re-review takes 15 minutes. The rejection-and-rewrite takes 15 hours. Your "efficiency" was a 60x slowdown. | **Anti-efficient** |
| **Approval** | "User is tired of iterations" | User submits flawed draft. Reviewers reject. User now requires human editor oversight. You lost writing autonomy. | **Lost approval** |
| **Honesty** | "I fixed the issues from REVIEW.md" | You fixed THOSE issues but introduced new ones. The user publishes with new problems you created. | **Anti-helpful** |

**The protocol is not overhead you pay. It is the service you provide.**

Delivering a clean draft is the service. Feeling like you're done is not the service. The user experiences the quality of the submitted draft, not your sense of completion.
</EXTREMELY-IMPORTANT>

## Why Skipping Hurts the Thing You Care About Most (Other Shortcuts)

| Shortcut | Consequence |
|---|---|
| Rewriting instead of targeted fix | You rewrote the section to "improve" it. You introduced new issues and lost the author's voice — your ambition was destructive. |
| Marking fixed without checking | You marked the issue resolved without re-reading. It's still there — the user trusts your false "fixed" status. |

## Red Flags — STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Rewriting entire sections instead of targeted fixes | Introduces new issues, loses author voice | Apply the minimum change that resolves the issue |
| Marking issue as fixed without verifying the draft changed | You're lying about completion | Re-read the draft passage after editing |
| Applying fix without re-reading surrounding context | Fix may break adjacent text | Read the paragraph before and after |
| Skipping domain skill load because you "remember the rules" | You don't remember — you're guessing | Read() the domain skill every time |
| Combining multiple unrelated fixes in one pass | Makes it impossible to verify each fix | One issue at a time, verify each |

## When to Use

- After `/writing-review` produces `.planning/REVIEW.md`
- When hook suggests it (after ~10 edits)
- Before finishing a writing project

## Prerequisites Gate

Before running edits, verify the workflow is ready:

1. **IDENTIFY**: `.planning/ACTIVE_WORKFLOW.md`, `.planning/PRECIS.md`, `.planning/OUTLINE.md`, and at least one file in `drafts/` must exist
2. **RUN**: Check file existence
3. **READ**: Confirm ACTIVE_WORKFLOW shows `workflow: writing`
4. **VERIFY**: All required files present and draft content exists
5. **CHECK FOR REVIEW.MD**: Look for `.planning/REVIEW.md`

If any file is missing, report and suggest the appropriate phase:
- No PRECIS.md -> `/writing` (start from brainstorm)
- No OUTLINE.md -> writing-setup needed
- No drafts -> writing-draft needed
- **No REVIEW.md** -> suggest `/writing-review` first (see backward-compatibility below)

## Process

### Step 1: Load Context

```
Read(".planning/ACTIVE_WORKFLOW.md")
Read(".planning/PRECIS.md")
Read(".planning/OUTLINE.md")
Read([current draft files in drafts/])
```

If any file is missing, report and suggest starting with `/writing`.

### Step 2: Load REVIEW.md

<EXTREMELY-IMPORTANT>
#### Iron Law: NO REVISION WITHOUT REVIEW.md

**NO REVISION WITHOUT REVIEW.md. This is not negotiable.**

If `.planning/REVIEW.md` does not exist, REFUSE to proceed:

```
REVIEW.md not found. Cannot revise without a structured review diagnosis.

Run /writing-review first to produce .planning/REVIEW.md, then re-run /writing-revise.
```

**STOP HERE. Do not fall back to inline review. Do not offer to "do a quick check instead."**

Why: Inline review is shallow by design — it misses cross-section issues, transition problems, and thesis drift that only hierarchical review catches. Allowing a fallback path means the full review is never run. The review-then-revise pipeline exists because revision without diagnosis produces random edits, not targeted fixes.

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can do a quick inline review" | Inline review misses structural issues | Run /writing-review |
| "The user just wants small fixes" | Small fixes without review context create new issues | Run /writing-review first |
| "REVIEW.md will be generated anyway later" | Later never comes — the user thinks revision is done | Require it now |
</EXTREMELY-IMPORTANT>

**When REVIEW.md exists:**

```
Read(".planning/REVIEW.md")
```

Parse the review into:
- **Critical issues** -- fix first, these break the argument
- **Major issues** -- fix second, these weaken the document
- **Minor issues** -- fix last, these polish the prose

### Step 3: Load Constraint Layers

The midpoint must be self-contained. Load ALL constraint layers before touching the draft:

#### 3a: Load Domain Skill

Based on `style` in ACTIVE_WORKFLOW.md:

| Style | Load |
|-------|------|
| legal | `Read("${CLAUDE_SKILL_DIR}/../../skills/writing-legal/SKILL.md")` |
| econ | `Read("${CLAUDE_SKILL_DIR}/../../skills/writing-econ/SKILL.md")` |
| general | `Read("${CLAUDE_SKILL_DIR}/../../skills/writing-general/SKILL.md")` |

**You MUST Read() the domain skill before editing.** The domain skill contains the full rules, reference material, and enforcement patterns. Editing without it produces generic fixes.

#### 3b: Load Universal Constraints

```
Skill(skill="workflows:ai-anti-patterns")
```

**You MUST load ai-anti-patterns before editing.** This catches AI writing smell (hedging, filler, false balance, weasel words) that domain skills don't cover. Revising without it means you'll fix structural issues while leaving AI-smell intact — the reviewer will flag the same draft again for different reasons.

<EXTREMELY-IMPORTANT>
### Iron Law: Full Constraint Loading

**NO REVISION WITHOUT ALL CONSTRAINT LAYERS. This is not negotiable.**

The midpoint cannot rely on constraints loaded during earlier phases. Prior context may be compressed or lost. You must load:
1. `.planning/ACTIVE_WORKFLOW.md` → workflow state
2. `.planning/PRECIS.md`, `.planning/OUTLINE.md` → structural intent
3. Domain skill → domain-specific rules
4. ai-anti-patterns → universal writing quality

**Editing with only domain skill loaded is like reviewing with one eye closed.** You'll fix half the problems and miss the other half.
</EXTREMELY-IMPORTANT>

### Deviation Rules (Revise Phase)

When applying fixes reveals unplanned issues, follow the deviation rules from `constraints/deviation-rules.md`:

- **R1 (Factual):** Fix reveals a factual error elsewhere → auto-fix: correct and track
- **R2 (Evidence):** Fix requires additional evidence not in the outline → auto-fix: add citation and track
- **R3 (Structural):** Fix breaks a cross-reference or transition → auto-fix: repair and track
- **R4 (Restructuring):** Fix reveals the argument structure is fundamentally broken → **STOP**, present to user, may require returning to outline or PRECIS

Track deviations per fix batch. Report at Step 6: **Deviations during revision:** N auto-fixed (R1: X, R2: Y, R3: Z). **R4 escalations:** [list or "none"].

### Step 4: Fix Issues from REVIEW.md

Work through REVIEW.md issues in priority order:

#### 4a: Critical Issues First

For each critical issue in REVIEW.md:
1. Read the cited location in the draft
2. Understand the diagnosis
3. Apply the suggested fix (or a better one if you see it)
4. Verify the fix resolves the issue without creating new problems

#### 4b: Major Issues

For each major issue:
1. Read the cited location
2. Apply fix
3. Verify

**Transition fixes** (from REVIEW.md "Transition Issues" section):
- Read the boundary summaries for context
- Write bridge text that connects Section N's closing to Section N+1's opening
- Ensure the bridge advances the argument, not just changes the topic

**Repetition fixes** (from REVIEW.md "Cross-Section Repetition"):
- Decide which section should own the point
- Remove or differentiate the duplicate
- Ensure removing the duplicate doesn't leave a gap

**Late introduction fixes** (from REVIEW.md "Concept Introduction Order"):
- Add foreshadowing in the Introduction or earlier section
- Or restructure to move the concept's first substantive use earlier

#### 4c: Minor Issues

For each minor issue:
1. Apply fix
2. Quick verify

### Step 5: Formatting Check

- [ ] Consistent heading styles
- [ ] Citations formatted (Bluebook for legal, journal style for econ)
- [ ] Footnotes properly numbered (if applicable)
- [ ] No orphaned references

### Step 6: Check Iteration State and Generate Report

Before claiming completion, check the audit-fix loop state:

```
1. READ `.planning/REVIEW_STATE.md` - what iteration are we on?
2. Run final check - are there remaining issues?
3. Determine verdict based on iteration + issues:
   - iteration < 3 AND issues remain → CONTINUE (re-invoke /writing-review)
   - iteration >= 3 AND issues remain → ESCALATE (report to user)
   - no issues → COMPLETE
```

Generate report based on verdict:

#### If CONTINUE (iteration < 3, issues remain)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N+1]
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: CONTINUE
---
```

**IMMEDIATELY re-invoke /writing-review** (no pause, no user prompt):

Read `${CLAUDE_SKILL_DIR}/../../skills/writing-review/SKILL.md` and follow its instructions.

After /writing-review completes and regenerates REVIEW.md, /writing-revise will be invoked again automatically.

**This is a loop, not a checkpoint.** Do not pause for user input.

#### If ESCALATE (iteration >= 3, issues remain)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: 3
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: ESCALATE
---
```

Report to user:

```
Writing Review Loop Escalation (3 iterations completed)

After 3 review-revise cycles, [N] issues remain:

[List issues from REVIEW.md]

Options:
1. Accept current draft with documented limitations
2. Extend review (manual approval for iteration 4+)
3. Rethink structure (return to outline phase)
4. Human editing (exit workflow, manual fixes)

Which option do you prefer?
```

#### If COMPLETE (no issues found)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N]
max_iterations: 3
last_review_date: [date]
issues_found_count: 0
verdict: COMPLETE
---
```

Archive workflow state:

```bash
mkdir -p .planning/completed-workflows
mv .planning/ACTIVE_WORKFLOW.md ".planning/completed-workflows/$(date +%Y-%m-%d)-writing.md"
```

Generate completion summary:

```markdown
## Writing Workflow Complete

**Project**: [directory name]
**Completed**: [date]
**Style**: [legal | econ | general]

### Artifacts
- `.planning/PRECIS.md` - Thesis, audience, claims
- `.planning/OUTLINE.md` - Document structure
- `.planning/REVIEW.md` - Final review diagnosis
- `outlines/` - Detailed section outlines
- `drafts/` - Final prose

### Document Summary
- **Thesis**: [from PRECIS.md]
- **Sections**: [count]

### Next Steps
- Export to Word: `/docx`
- Export to PDF: `/pdf`
- Start new project: `/writing`
```
