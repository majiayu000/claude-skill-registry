---
name: audit-fix-loop
description: "This skill should be used when the user asks to 'iteratively improve', 'audit and fix', 'hill-climb quality', 'grade and improve', 'score and fix', 'audit loop', 'quality loop', or needs structured iterative improvement of an artifact using scored independent audits. Also use when the user invokes a ralph loop for quality improvement rather than task completion."
user-invocable: false
---

**Announce:** "Using audit-fix-loop to plan a scored iterative improvement loop."

<EXTREMELY-IMPORTANT>
## The Iron Law of Independent Audit

**THE AUDITOR MUST NOT BE THE FIXER. This is not negotiable.**

If the same agent that wrote the fix also scores it, you get rubber-stamping. The audit must be structurally independent: a fresh subagent, a different model (Gemini), or a mechanical checker. The fixer's opinion of its own work is worthless.

**Skipping the independent re-audit is NOT HELPFUL — the user gets an artifact with unverified fixes that may have introduced new problems.**
</EXTREMELY-IMPORTANT>

## The Pattern

```
PLAN (this skill)
  ↓
  AskUserQuestion → identify artifact, scorers, termination
  ↓
LOOP (ralph-loop infrastructure)
  ↓
  ┌─────────────────────────────────────────────┐
  │ AUDIT: Fresh subagent scores artifact            │
  │   → Produces scored findings in .planning/AUDIT.md     │
  │   → Records score (0-10) in .planning/SCORES.md       │
  │                                              │
  │ DECIDE: Check score against threshold        │
  │   → Score >= 9.5? → DONE (output promise)   │
  │   → Score < 9.5?  → continue to FIX         │
  │                                              │
  │ FIX: Apply targeted improvements             │
  │   → Address highest-severity findings first  │
  │   → Minimal changes (don't rewrite)          │
  │                                              │
  │ → next iteration (re-audit)                  │
  └─────────────────────────────────────────────┘
```

**This is hill-climbing.** Each iteration audits, scores out of 10, fixes the worst findings, and re-audits. The loop terminates when the score crosses the threshold (default: >= 9.5/10).

<EXTREMELY-IMPORTANT>
## The Iron Law of Planning

**NO RALPH LOOP WITHOUT A PLAN. This is not negotiable.**

Before starting any audit-fix loop, you MUST identify:
1. What artifact you are improving
2. Which scoring surfaces apply
3. How the audit will be independent
4. What the score threshold is (default: 9.5/10)

A ralph loop with `--completion-promise FIXED` and no audit structure is a naive loop. It provides zero enforcement because the agent decides when it's "fixed." The score decides — not the fixer.
</EXTREMELY-IMPORTANT>

## Step 1: Plan the Loop

### Identify Artifact and Scorers

```
AskUserQuestion(questions=[
  {
    "question": "What artifact are you improving?",
    "header": "Artifact",
    "options": [
      {"label": "Writing draft", "description": "Document, essay, paper, or prose in drafts/ or a specific file"},
      {"label": "Skill or workflow", "description": "SKILL.md or workflow definition being hardened"},
      {"label": "Visual output", "description": "Slides, charts, rendered documents — use visual-verify instead"},
      {"label": "Citations", "description": "Bluebook footnotes in a DOCX manuscript"}
    ],
    "multiSelect": false
  },
  {
    "question": "Which scoring surfaces should the audit use?",
    "header": "Scorers",
    "options": [
      {"label": "AI anti-patterns", "description": "12-category checklist for AI writing indicators (puffery, structure, artifacts)"},
      {"label": "Style guide", "description": "Domain rules: legal writing, econ writing, or Strunk & White (general)"},
      {"label": "Bluebook rules", "description": "Citation compliance against Bluebook 21st edition mechanical rules"},
      {"label": "Enforcement patterns", "description": "Score skill/workflow against 12 superpowers enforcement patterns"},
      {"label": "Source verification", "description": "Check citations against paperpile.bib, verify quotes against source PDFs (use source-verify skill)"}
    ],
    "multiSelect": true
  }
])
```

If user selects "Visual output," redirect to visual-verify — it already implements this pattern with Gemini vision.

If user selects "Citations," redirect to bluebook-audit — it already implements the audit+correct+verify cycle.

### Derive Loop Parameters

Based on selections, determine:

| Parameter | How to Derive |
|-----------|--------------|
| **Audit method** | See scorer table below |
| **Fix method** | Self-edit for small artifacts, parallel subagents for large ones |
| **Max iterations** | 10 (default), adjustable |
| **Score threshold** | 9.5/10 (default), adjustable |
| **Completion promise** | `[ARTIFACT_NAME]_9_5` — descriptive, includes threshold |

**Promise naming convention:** Use a descriptive name that encodes what must be true. Examples:
- `ALL_FAMILIES_9_5` — all workflow families score >= 9.5
- `DRAFT_AI_CHECK_9_5` — draft passes AI anti-patterns at >= 9.5
- `SKILL_ENFORCEMENT_9_5` — skill scores >= 9.5 on enforcement audit

### Scorer Reference

Each scorer has a specific audit method that ensures independence:

| Scorer | Audit Method | Independence Mechanism | Score Metric |
|--------|-------------|----------------------|-------------|
| **AI anti-patterns** | Fresh subagent reads `../ai-anti-patterns/SKILL.md` (relative to this skill's base directory) + all references, then audits the artifact | Fresh subagent (no fixer context) | Count by severity (CRITICAL/HIGH/MEDIUM) |
| **Style guide** | Fresh subagent reads domain skill (writing-legal, writing-econ, or writing-general), then audits | Fresh subagent | Rule violations by severity |
| **Bluebook rules** | Fresh subagent reads `../bluebook/SKILL.md` + references, then audits citations | Fresh subagent | Violations by rule category |
| **Enforcement patterns** | Fresh subagent reads `references/enforcement-checklist.md`, scores all 12 patterns | Fresh subagent | Count of Absent + Weak scores |
| **Source verification** | Invoke `Skill(skill="workflows:source-verify")` — checks citations against paperpile.bib, verifies quotes against source PDFs | Mechanical (bibtex grep) + NLM (quote search) | Verified / checkable citations |

**Composing scorers:** When multiple scorers are selected, each audit iteration runs ALL of them. The total score is the sum of all findings across all scorers. This means the audit catches different failure modes simultaneously — AI-smell AND style violations AND unsupported claims.

## Step 2: Initialize State Files

Create the `.planning/` directory and two state files before starting the loop:

```bash
mkdir -p .planning
```

**`.planning/AUDIT.md`** — current audit findings (overwritten each iteration):
```markdown
# Audit Findings

## Iteration: 1
## Scorers: [list]
## Total Score: [N]

### [Scorer Name]
| # | Severity | Finding | Location | Suggestion |
|---|----------|---------|----------|------------|
| 1 | HIGH | ... | ... | ... |
```

**`.planning/SCORES.md`** — score history across iterations (append-only):
```markdown
# Score History

| Iteration | Score | Threshold | Delta | Key Findings |
|-----------|-------|-----------|-------|-------------|
| 1 | 6.5 | 9.5 | — | 3 CRITICAL, 2 HIGH |
| 2 | 8.0 | 9.5 | +1.5 | 0 CRITICAL, 1 HIGH, 3 MEDIUM |
```

## Step 3: Start the Loop

Generate the structured ralph-loop prompt and invoke:

```
Skill(skill="ralph-loop:ralph-loop", args="Audit-fix loop: [ARTIFACT DESCRIPTION]. Audit then fix in parallel. --max-iterations [N] --completion-promise [PROMISE_NAME]")
```

Example:
```
Skill(skill="ralph-loop:ralph-loop", args="Bring all three workflow families to 9.5 enforcement score. Audit then fix in parallel. --max-iterations 10 --completion-promise ALL_FAMILIES_9_5")
```

The prompt fed to each ralph iteration must enforce this exact sequence:

### Iteration Protocol

**Phase A: Audit (MUST be first)**

For each selected scorer, spawn a fresh audit subagent:

```
Agent(prompt="""
You are an independent auditor. You have NO knowledge of any prior fixes.

Read the scoring rules:
[SCORER-SPECIFIC SKILL PATH]

Then audit this artifact:
[ARTIFACT PATH]

Produce findings in this EXACT format:

| # | Severity | Finding | Location | Suggestion |
|---|----------|---------|----------|------------|

Severity levels: CRITICAL, HIGH, MEDIUM, LOW

Be thorough. A clean audit with missed issues is worse than a harsh audit.
Do NOT soften findings. Do NOT say "overall good."
""", subagent_type="general-purpose")
```

After all audit subagents return, compile findings into `.planning/AUDIT.md` and compute the score:

**Scoring:** The auditor scores the artifact 0-10 across the selected scoring surfaces.

The score reflects compliance rate: 9.5/10 = 95% of checkable items pass. For checklist-based scorers (ai-anti-patterns, style guide, enforcement patterns), this is concrete — count violations, divide by total checkpoints, invert. For judgment-based scorers, the auditor must justify the score with specific findings.

| Score | Meaning |
|-------|---------|
| 10.0 | 100% — zero findings |
| 9.5 | 95% — 1-2 minor items remain (default threshold) |
| 8.0 | 80% — several items need fixing |
| < 7.0 | Major gaps — significant work needed |

Record in `.planning/SCORES.md`.

**Phase B: Decide**

Read `.planning/SCORES.md`. Check against threshold:

| Condition | Action |
|-----------|--------|
| Score >= threshold (default 9.5) | Output `<promise>[PROMISE_NAME]</promise>` — artifact meets quality bar |
| Score < threshold | Continue to Phase C |
| Max iterations reached | Escalate to user with current score and remaining findings |

**Phase C: Fix**

Address findings from `.planning/AUDIT.md`, prioritized by severity:
1. Fix all CRITICAL findings first
2. Then HIGH
3. Then MEDIUM (if iteration budget allows)
4. Skip LOW unless everything else is clean

**Fix rules:**
- Targeted changes only — do NOT rewrite the entire artifact
- Each fix should address ONE finding
- After fixing, do NOT self-assess — the next iteration's audit will judge

**Then end your turn** (the ralph loop will feed you back for re-audit).

**After fixing, do NOT pause to summarize or ask "should I continue?" — end your turn immediately so the loop feeds you back for re-audit. The score decides when to stop, not you.**

<EXTREMELY-IMPORTANT>
## The Iron Law of Score Threshold

**You may ONLY output the completion promise when the independent audit scores >= the threshold.**

Not when you "feel" the artifact is good enough. Not when you're tired of iterating. Not when the remaining findings seem minor. The auditor's score decides — you don't.

Read `.planning/SCORES.md`, check the number against the threshold, output promise only if the score meets or exceeds it.

**Outputting the completion promise when the score is below threshold is NOT HELPFUL — the user receives a substandard artifact that fails its quality bar.**
</EXTREMELY-IMPORTANT>

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The remaining findings are minor" | Minor findings keep the score below 9.5. The threshold exists for a reason. | Fix them or document why they're false positives |
| "I can audit my own fixes" | Self-audit is rubber-stamping. You'll approve your own work. | Spawn a fresh subagent for every audit |
| "One more iteration won't help" | You don't know that. The score decides. | Run the audit, check the score, then decide |
| "The audit is too harsh" | Harsh audits produce quality. Soft audits produce complacency. | Keep the standard. Lower scores, not standards |
| "I'll batch all the fixes" | Batching makes it impossible to trace which fix helped | Fix by severity priority, let re-audit measure impact |
| "Bluebook checking is overkill for this draft" | If the document has footnotes, they must be correct. Wrong citations undermine credibility. | Run the Bluebook check |
| "FIXED is basically the same as meeting the threshold" | FIXED is honor system. Threshold requires an independent auditor score >= 9.5. | Use descriptive promise names that encode the threshold |
| "I'll skip the AskUserQuestion planning" | Unplanned loops are naive loops. | Plan first, loop second |

## Delete & Restart

**If you started a ralph loop without planning (no AskUserQuestion, no scorer selection), CANCEL the loop and START OVER with Step 1.** No patching a naive loop mid-flight — cancel it (`/cancel-ralph`), plan properly, then restart.

**If you ran an audit with the fixer agent instead of a fresh subagent, DELETE the audit findings and RE-RUN with a fresh subagent.** Tainted audit results are worse than no audit — they give false confidence.

## Red Flags — STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|--------|-----------|------------|
| Starting a ralph loop without running Step 1 | Naive loop — no audit structure | Plan the loop first |
| Using `--completion-promise FIXED` | Honor system — agent decides when done | Use descriptive promise with threshold (e.g., `DRAFT_9_5`) |
| Auditing your own fixes in the same context | Rubber-stamping — no independence | Spawn fresh audit subagent |
| Outputting promise when score < threshold | Lying about quality | Read `.planning/SCORES.md`, check score >= threshold |
| Rewriting the entire artifact instead of targeted fixes | Introduces new issues, loses original voice | Fix one finding at a time |
| Skipping a selected scorer "to save time" | Partial audit misses entire failure categories | Run all selected scorers every iteration |

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "I'll save time by self-auditing" | You approved your own sloppy work | **Anti-helpful** — the artifact still has issues |
| **Competence** | "I know the quality is good enough" | A fresh auditor found 8 more issues | **Incompetent** — you missed what a checklist caught |
| **Efficiency** | "Planning the loop is overhead" | Unplanned loop ran 10 iterations with no progress | **Inefficient** — planning takes 30 seconds, unplanned loops waste minutes |
| **Honesty** | "Close enough to 9.5" | Score is 8.7 — you claimed threshold met without checking | **Dishonest** — you lied about quality |

## Integration

This skill **does not replace** existing audit workflows. It plans and structures loops that use them:

| Existing Skill | Relationship |
|---------------|-------------|
| **visual-verify** | Already implements audit-fix-loop for visual output. Redirect there. |
| **bluebook-audit** | Already implements audit+correct+verify for citations. Redirect there. |
| **writing-review + writing-revise** | Can be wrapped in audit-fix-loop for iterative improvement |
| **skill-creator** | Enforcement audit step IS an audit-fix pattern |
| **ai-anti-patterns** | Used AS a scorer within audit-fix-loop |
| **source-verify** | Domain-specific audit-fix-loop for citation/quote verification |

## Source Verification

For citation and quote verification, use the dedicated skill:

```
Skill(skill="workflows:source-verify")
```

Source-verify checks citations against `paperpile.bib` (existence + field accuracy), verifies quotes against source PDFs (via `rga` or NLM), and optionally checks claim grounding via NLM. It implements its own audit-fix-loop with scored threshold termination.

Use source-verify directly — do NOT try to reinvent citation checking inside a generic audit-fix-loop.
