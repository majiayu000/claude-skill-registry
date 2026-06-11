---
name: parallel-code-review
description: "Parallel 3-reviewer code review: Security, Business-Logic, Architecture."
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Task
routing:
  triggers:
    - "parallel review"
    - "3-reviewer review"
    - "security review"
    - "multi-reviewer"
    - "concurrent review"
  category: code-review
  pairs_with:
    - systematic-code-review
    - verification-before-completion
---

# Parallel Code Review Skill

Orchestrate three specialized code reviewers (Security, Business Logic, Architecture) in true parallel using the Fan-Out/Fan-In pattern. Each reviewer runs independently with domain-specific focus, then findings are aggregated by severity into a unified BLOCK/FIX/APPROVE verdict.

---

## Instructions

### Phase 1: IDENTIFY SCOPE

**Goal**: Determine changed files and select appropriate agents before dispatching.

**Step 1: Read repository CLAUDE.md** to load project-specific conventions that reviewers must respect.

**Step 2: List changed files**

```bash
# For recent commits:
git diff --name-only HEAD~1
# For PRs:
gh pr view --json files -q '.files[].path'
```

**Step 3: Select architecture reviewer agent** based on the dominant language. This ensures the architecture reviewer applies idiomatic standards rather than generic advice, because different languages have fundamentally different design patterns and conventions.

| File Types | Agent |
|-----------|-------|
| `.go` files | `golang-general-engineer` |
| `.py` files | `python-general-engineer` |
| `.ts`/`.tsx` files | `typescript-frontend-engineer` |
| Mixed or other | `Explore` |

**Optional enrichments** (only when user explicitly requests):
- "include threat model" -- adds threat modeling to Security reviewer scope
- "find breaking commit" -- adds git bisect regression tracking
- "benchmark" -- adds performance profiling to Architecture reviewer scope

**Gate**: Changed files listed, architecture reviewer agent selected. Proceed only when gate passes.

### Phase 2: DISPATCH PARALLEL REVIEWERS

**Goal**: Launch all 3 reviewers in a single message for true concurrent execution.

**Critical constraint**: All three Task calls MUST appear in ONE response. Sending them sequentially triples wall-clock time and defeats the purpose of parallel review. This is not optional—parallelism is the entire value proposition of this skill.

Dispatch exactly these 3 agents. This is a read-only review—reviewers observe and report but never modify code.

**Reviewer 1 -- Security**
- Focus: OWASP Top 10, authentication, authorization, input validation, secrets exposure
- Output: Severity-classified findings with `file:line` references

**Reviewer 2 -- Business Logic**
- Focus: Requirements coverage, edge cases, state transitions, data validation, failure modes
- Output: Severity-classified findings with `file:line` references

**Reviewer 3 -- Architecture** (using agent selected in Phase 1)
- Focus: Design patterns, naming, structure, performance, maintainability
- Output: Severity-classified findings with `file:line` references

**Dimension lenses (all 3 reviewers apply, in addition to their role focus).** Roles cover *who* reviews; lenses cover *what classes of issue* every review must touch. Folding these into the existing briefs catches doc-accuracy and scope creep without paying for extra agents:

| Lens | What it catches | Owner reviewer (primary) |
|------|-----------------|--------------------------|
| Doc-accuracy | Comments, docstrings, READMEs, or PR description that no longer match the code's actual behavior | Business Logic |
| Scope / simplicity | Changes beyond the stated task, speculative abstraction, dead options, YAGNI violations | Architecture |

Each reviewer reports lens findings inline with its role findings, tagged with the same `[Reviewer]` and `file:line` format so they flow through the schema gate unchanged.

**Critical constraint**: Always run all 3 reviewers regardless of perceived change simplicity. Config changes can expose secrets, "trivial" fixes can break authorization, and each reviewer's specialization catches issues the others miss. Let a reviewer report "no findings" rather than skip it—because silence is information too.

**Gate**: All 3 Task calls dispatched in a single message. Proceed only when ALL 3 return results—never issue a verdict from partial results, because the missing reviewer may hold the only CRITICAL finding. Partial results are worse than no review.

### Phase 3: AGGREGATE

**Goal**: Merge all findings into a unified severity-classified report.

**Critical constraint**: Never dump raw reviewer outputs as three separate sections—the reader should not have to mentally merge findings across reviewers. Your job is to synthesize, not summarize.

**Step 1: Classify each finding by severity**

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Security vulnerability, data loss risk | BLOCK merge |
| HIGH | Significant bug, logic error | Fix before merge |
| MEDIUM | Code quality issue, potential problem | Should fix |
| LOW | Minor issue, style preference | Nice to have |

**Step 2: Deduplicate overlapping findings**

Multiple reviewers may flag the same issue. Merge duplicates, keeping the highest severity. Overlap between reviewers is a feature (independent confirmation), but the report should consolidate it so readers see a unified issue once, not three times.

**Step 3: Build reviewer summary matrix**

Include this matrix in every report so stakeholders see the severity distribution at a glance:

```
| Reviewer       | CRITICAL | HIGH | MEDIUM | LOW |
|----------------|----------|------|--------|-----|
| Security       | N        | N    | N      | N   |
| Business Logic | N        | N    | N      | N   |
| Architecture   | N        | N    | N      | N   |
| **Total**      | **N**    | **N**| **N**  | **N**|
```

**Gate**: All findings classified, deduplicated, and summarized. Proceed only when gate passes.

### Phase 3.5: ADVERSARIAL VERIFY (GATED)

**Goal**: Refute each surviving finding independently before it reaches the report, so speculative or already-handled findings are dropped instead of shipped. This is the behavior that cut a native review from 10 findings to 3 (~70% noise removed) and directly targets the false-positive class that produced a 25% false-positive rate earlier.

**Run this phase ONLY when the gate condition below is true. Otherwise skip straight to Phase 4 — small, clean reviews pay nothing.**

**Gate condition (run the verify pass when EITHER is true):**

```
findings_count >= 4   OR   any finding is severity CRITICAL or HIGH
```

Otherwise (≤3 findings, all MEDIUM/LOW): skip this phase. State in the report: `Adversarial verify: SKIPPED (N findings, max severity MEDIUM — below gate).`

**Step 1: Dispatch one verification check per finding.** Each finding gets an independent check (a Task call) prompted to REFUTE the finding, not confirm it. Dispatch the checks for a single review in one message so they run concurrently, matching the parallel pattern of Phase 2. The verifier's default stance is **not-real**; the finding survives only if the verifier cannot refute it.

Verifier prompt contract (per finding):
- Input: the finding text, its `file:line`, its claimed severity, and read access to the cited code.
- Task: attempt to refute. Mark the finding **REFUTED** if any of these hold:
  - **Speculative** — the failure path is hypothetical; no concrete input or call sequence reaches it.
  - **Already-handled** — a guard, validation, type constraint, or upstream caller already prevents it (cite the line that handles it).
  - **Not actionable** — no specific code change would resolve it, or it restates a style preference already covered by lint/format.
- Output: `CONFIRMED` or `REFUTED`, a one-line justification with a `file:line` citation, and (for confirmed findings) a verified severity per Step 2.

**Step 2: Verify-and-downgrade severity.** Reviewers over-grade. The verifier may re-grade a confirmed finding's severity, recording original→final with a written justification. Severity changes only on evidence (e.g., "downgraded CRITICAL→MEDIUM: the unsanitized value is server-issued UUID, not user input — `auth/token.go:88`"). Record every re-grade; never silently alter a severity.

**Step 3: Keep only CONFIRMED findings.** REFUTED findings are removed from the aggregate and listed separately as refuted (with the refutation reason) so the reader sees what was filtered and why — transparency, not a silent drop.

**Honest framing**: per-finding verify catches false positives at the structure-and-plausibility level — it refutes findings whose failure path is hypothetical or already-guarded. It is not a correctness oracle: it cannot prove a confirmed finding is a real exploitable bug, only that a refutation attempt failed. Treat CONFIRMED as "survived refutation," not "proven."

**Cost guardrail**: the verify pass scales linearly with finding count (one check per finding) and is bounded two ways — (1) the gate above skips it entirely for small/clean reviews, and (2) it runs at most once per finding (no verify-the-verifier recursion). For larger diffs, cap the number of verify checks to the right-sizing tier for the review (the tier rules and `scripts/right-size-review.py` live outside this skill; reference the tier the review was sized to). When the cap is hit, verify the highest-severity findings first and note the uncapped remainder in the report.

**Gate**: Verify pass was either skipped (gate condition false, stated in report) or completed (every finding marked CONFIRMED/REFUTED, severity re-grades recorded). Proceed only when gate passes.

### Phase 4: VERDICT

**Goal**: Produce final report with clear recommendation.

**Critical constraint**: Every review must end with an explicit verdict. Ambiguity is a decision to merge untested code. Choose: BLOCK, FIX, or APPROVE.

The verdict is computed from **confirmed findings only** (after Phase 3.5). When the verify pass was skipped, all aggregated findings count as confirmed. Use each finding's **final** severity (post-downgrade), not its original.

**Step 1: Determine verdict**

| Condition | Verdict |
|-----------|---------|
| Any CRITICAL findings | **BLOCK** |
| HIGH findings, no CRITICAL | **FIX** (fix before merge) |
| Only MEDIUM/LOW findings | **APPROVE** (with suggestions) |

**Step 2: Output structured report**

```markdown
## Parallel Review Complete

### Severity Matrix

| Severity | Count | Summary |
|----------|-------|---------|
| Critical | N | One-line aggregated summary |
| High     | N | One-line aggregated summary |
| Medium   | N | One-line aggregated summary |
| Low      | N | One-line aggregated summary |

Counts above are CONFIRMED findings (post-verify). Details by reviewer below.

### Adversarial Verify
- Status: RAN (gate: N findings / max severity X) | SKIPPED (gate condition false)
- Confirmed: N | Refuted: N
- Severity re-grades: [original→final with justification, or "none"]

### Refuted Findings (filtered, not in verdict)
1. [Reviewer] Original finding - file:line — Refuted: [speculative | already-handled | not-actionable] ([citing file:line])

### Combined Findings

#### CRITICAL (Block Merge)
1. [Reviewer] Issue description - file:line

#### HIGH (Fix Before Merge)
1. [Reviewer] Issue description - file:line

#### MEDIUM (Should Fix)
1. [Reviewer] Issue description - file:line

#### LOW (Nice to Have)
1. [Reviewer] Issue description - file:line

### Summary by Reviewer
[Matrix from Phase 3]

### Recommendation
**VERDICT** - [1-2 sentence rationale]
```

**Step 3: Validate the structured output (schema gate)**

Each reviewer returns markdown. Before accepting a reviewer's output into the aggregate, run it through the deterministic schema validator so a malformed review is caught mechanically rather than trusted on sight:

```bash
# Pipe each reviewer's markdown directly (preferred — no shared temp file, so
# 3 parallel reviewers never overwrite each other):
echo "$reviewer_markdown" | python3 scripts/validate-review-output.py --type parallel -
# Or, if writing to disk, use a per-reviewer path (NOT a shared /tmp file):
python3 scripts/validate-review-output.py --type parallel /tmp/reviewer-<name>.md
```

Exit codes: `0` = structurally valid (verdict present, severity_matrix complete, every finding carries `[Reviewer]` and a `file:line` location); `1` = schema errors; `2` = unparseable; `3` = `jsonschema` not installed (`pip install jsonschema`).

This gate verifies the review is **structurally well-formed** (verdict, severity buckets, and locations present) — it does NOT verify findings completeness (no minimum count; a parser-dropped malformed finding leaves no trace) NOR that the severity_matrix counts agree with the findings array (no matrix↔findings cross-check).

**On validation failure:** retry that ONE reviewer exactly once, then stop.
- **Exit 1 (schema errors):** re-invoke the reviewer passing the validator's specific numbered error lines (e.g. `MISSING: reviewer`, `MISSING: location`) so it knows precisely what to repair.
- **Exit 2 (unparseable):** there are no per-error lines to feed back — the output couldn't be structured at all. Regenerate the reviewer's markdown from scratch in the required format.

Validate the retried result. If it still fails, STOP and report the malformed output — proceed only on review data that passes the schema, because a verdict synthesized from broken findings is worse than no verdict.

**Step 4: If BLOCK verdict, initiate re-review protocol**

After user addresses CRITICAL issues, re-run ALL 3 reviewers (not just the one that found the issue) to verify:
1. Original CRITICAL issues resolved
2. No regressions introduced
3. No new CRITICAL/HIGH issues from fixes

Re-run all three because fixes often introduce new issues in adjacent code, and you need confirmation across all three domains that the solution is safe.

**Gate**: Each reviewer's output passed `validate-review-output.py --type parallel` (exit 0), structured report delivered with verdict. Review is complete.

---

## Error Handling

### Error: "Reviewer Times Out"

**Cause**: One or more Task agents exceed execution time.

**Solution**:
1. Report findings from completed reviewers immediately—a partial review is better than no review, because you'll know at least some classes of issues are present.
2. Note which reviewer(s) timed out and on which files, so the user understands the blind spots.
3. Offer to re-run failed reviewer separately or proceed with partial results (but disclose the incompleteness in the verdict).

### Error: "All Reviewers Fail"

**Cause**: Systemic issue (bad file paths, permission errors, context overflow).

**Solution**:
1. Verify changed file list is correct and files are readable—start with the basics.
2. Reduce scope if file count is very large (split into batches), because each reviewer needs enough context tokens to reason properly.
3. Fall back to systematic-code-review (sequential) as last resort, because at least one reviewer completing sequentially is better than zero reviewers failing.

### Error: "Conflicting Findings Across Reviewers"

**Cause**: Two reviewers disagree on severity or interpretation of same code.

**Solution**:
1. Keep the higher severity classification (classify UP), because you want to err on the side of caution—false positives are correctable, false negatives ship bugs.
2. Include both perspectives in the finding description, so the code author understands the disagreement and can make an informed decision.
3. Flag as "needs author input" if genuinely ambiguous, and include both interpretations verbatim so they can choose.

---

## References

- Severity classification: CRITICAL (blocks merge), HIGH (fix before), MEDIUM (should fix), LOW (nice to have)
- Verdict decision tree: Any CRITICAL → BLOCK; HIGH without CRITICAL → FIX; MEDIUM/LOW only → APPROVE (computed from confirmed findings, final severity)
- Adversarial verify gate: run per-finding refutation when `findings_count >= 4` OR any finding is CRITICAL/HIGH; else skip. One check per finding, capped to the right-sizing tier; refuted findings filtered, severity re-grades recorded
- Re-review trigger: Always re-run all 3 reviewers after BLOCK fixes to catch regressions
