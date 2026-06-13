---
name: systematic-code-review
description: "4-phase code review: UNDERSTAND, VERIFY, ASSESS risks, DOCUMENT findings."
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
routing:
  triggers:
    - "review code"
    - "code review methodology"
    - "structured review"
    - "code audit"
    - "review methodology"
    - "comprehensive review"
  not_for: "vague no-target requests like 'make this better' — those are interview-mode, where the agent asks what to improve. Only for reviewing a named file, diff, or PR."
  category: code-review
  pairs_with:
    - forensics
    - verification-before-completion
    - parallel-code-review
---

# Systematic Code Review Skill

Systematic 4-phase code review: UNDERSTAND changes, VERIFY claims against actual behavior, ASSESS security/performance/architecture risks, DOCUMENT findings with severity classification. Each phase has an explicit gate that must pass before proceeding because skipping phases causes missed context, incorrect conclusions, and incomplete risk assessment.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| reviewing Go code: type exports, concurrency, resource management, observability, test patterns | `go-review-patterns.md` | Loads detailed guidance from `go-review-patterns.md`. |
| responding to review feedback on your own code | `receiving-feedback.md` | Loads detailed guidance from `receiving-feedback.md`. |
| labeling findings: BLOCKING vs SHOULD FIX vs SUGGESTION | `severity-classification.md` | Loads detailed guidance from `severity-classification.md`. |

## Instructions

### Phase 1: UNDERSTAND

**Goal**: Map all changes and their relationships before forming any opinions.

**Step 1: Read CLAUDE.md**
- Read and follow repository CLAUDE.md files first because project conventions override default review criteria and may define custom severity rules, approved patterns, or scope constraints.

**Step 2: Read every changed file**
- Use Read tool on EVERY changed file completely because reviewing summaries or reading partial files misses dependencies between changes and leads to incorrect conclusions.
- Map what each file does and how changes affect it.
- Check affected dependencies and identify ripple effects because changes in one file can break consumers that aren't in the diff.

**Step 3: Identify dependencies**
- Use Grep to find all callers/consumers of changed code.
- Note any comments that make claims about behavior (these are claims to verify in Phase 2, not facts to trust).

**Step 3a: Caller Tracing** (mandatory when diff modifies function signatures, parameter semantics, or introduces sentinel/special values)

When the change modifies how a function/method is called or what parameters mean:

1. **Find ALL callers** — Grep for the function name with receiver syntax (e.g., `.GetEvents(` not just `GetEvents`) across the entire repo. For Go repos, prefer gopls `go_symbol_references` via ToolSearch("gopls") — it's type-aware and catches interface implementations.
2. **Trace the VALUE SPACE** — For each parameter source, classify what values can flow through:
   - Query parameters (`r.FormValue`, `r.URL.Query`): user-controlled — ANY string including sentinel values like `"*"`
   - Auth token fields: server-controlled (UUIDs, structured IDs)
   - Constants/enums: fixed set
   - Classify sentinel strings by their true source. If a value can originate from user input, treat it as reachable and verify the input path.
3. **Verify each caller** — For each call site, check that parameters are validated before being passed. Pay special attention to sentinel values (e.g., `"*"` meaning "all/unfiltered") that bypass security filtering.
4. **Report unvalidated paths** — Any caller that passes user input to a security-sensitive parameter without validation is a BLOCKING finding.
5. **Verify callers independently** — Treat the PR description as a lead, then confirm the caller set directly in the codebase. The PR author may have forgotten about callers, or new callers may have been added in other branches.

This step catches:
- Unchecked paths where user input reaches a security-sensitive parameter
- Callers the PR author forgot about or didn't mention
- Interface implementations that don't enforce the same preconditions

**Step 4: Document scope**

```
PHASE 1: UNDERSTAND

Changed Files:
  - [file1.ext]: [+N/-M lines] [brief description of change]
  - [file2.ext]: [+N/-M lines] [brief description of change]

Change Type: [feature | bugfix | refactor | config | docs]

Scope Assessment:
  - Primary: [what's directly changed]
  - Secondary: [what's affected by the change]
  - Dependencies: [external systems/files impacted]

Caller Tracing (if signature/parameter semantics changed):
  - [function/method]: [N] callers found
    - [caller1:line] — parameter validated: [yes/no]
    - [caller2:line] — parameter validated: [yes/no]
  - Unvalidated paths: [list or "none"]

Questions for Author:
  - [Any unclear aspects that need clarification]
```

**Gate**: All changed files read (not just some — reading 2 of 5 files and saying "I get the gist" fails this gate), scope fully mapped, callers traced (if applicable). Proceed only when gate passes.

### Phase 2: VERIFY

**Verification means execution, not reasoning.** Run the command. Do not reason about whether the command would pass. Do not summarize the expected output. Execute the check, paste the exit code, paste the relevant output. A verification phase that produces a verdict without an observed tool result is not a verification — it is a guess with a rigor aesthetic.

**Goal**: Validate all assertions in code, comments, and PR description against actual behavior.

**Step 1: Run tests**
- Execute existing tests for changed files because review cannot approve without test execution — visual inspection misses runtime issues that tests catch.
- Capture complete test output. Show the output rather than describing it because facts outweigh narrative.
- Verify test coverage: confirm tests exist for the changed code paths because untested code paths are a SHOULD FIX finding.

**Step 2: Verify claims**
- Check every comment claim against code behavior because comments frequently become outdated and developers may not understand what "thread-safe" actually means — never accept a comment as truth without inspecting the code that backs it.
- Verify edge cases mentioned are actually handled.
- Trace through critical code paths manually.

**Step 3: Document verification**

```
PHASE 2: VERIFY

Claims Verification:
  Claim: "[Quote from comment or PR description]"
  Verification: [How verified - test run, code trace, etc.]
  Result: VALID | INVALID | NEEDS-DISCUSSION

Test Execution:
  $ [test command]
  Result: [PASS/FAIL with summary]

Behavior Verification:
  - Expected: [what change claims to do]
  - Actual: [what code actually does]
  - Match: YES | NO | PARTIAL
```

**Gate**: All assertions in code/comments verified against actual behavior. Tests executed with output captured. Proceed only when gate passes.

### Phase 3: ASSESS

**Goal**: Evaluate security, performance, and architectural risks specific to these changes.

**Step 1: Security assessment**
- Never skip this step because security implications must be explicitly evaluated for every review, even when changes appear benign.
- Evaluate OWASP top 10 against changes.
- Explain HOW each vulnerability was ruled out (not just checkboxes) because a checkbox approach misses context-specific vulnerabilities and gives false confidence.
- If optionally enabled: perform extended deep security analysis beyond standard checks.

**Step 2: Performance assessment**
- Identify performance-critical paths and evaluate impact.
- Check for N+1 queries, unbounded loops, unnecessary allocations.
- If optionally enabled: benchmark affected code paths with profiling.

**Step 3: Architectural assessment**
- Compare patterns to existing codebase conventions.
- Assess breaking change potential.
- If optionally enabled: check for similar past issues via historical analysis.

**Step 4: Extraction severity escalation**
- If the diff extracts inline code into named helper functions, re-evaluate all defensive guards.
- A missing check rated LOW as inline code (1 caller, "upstream validates") becomes MEDIUM as a reusable function (N potential callers).

**Step 5: Document assessment**

```
PHASE 3: ASSESS

Security Assessment:
  SQL Injection: [N/A | CHECKED - how verified | ISSUE - details]
  XSS: [N/A | CHECKED - how verified | ISSUE - details]
  Input Validation: [N/A | CHECKED - how verified | ISSUE - details]
  Auth: [N/A | CHECKED - how verified | ISSUE - details]
  Secrets: [N/A | CHECKED - how verified | ISSUE - details]
  Findings: [specific issues or "No security issues found"]

Performance Assessment:
  Findings: [specific issues or "No performance issues found"]

Architectural Assessment:
  Findings: [specific issues or "Architecturally sound"]

Risk Level: LOW | MEDIUM | HIGH | CRITICAL
```

**Gate**: Security, performance, and architectural risks explicitly evaluated (not skipped or hand-waved). Proceed only when gate passes.

### Phase 3.5: VERIFY FINDINGS (GATED)

**Goal**: Refute each candidate finding before it reaches the DOCUMENT report, so speculative or already-handled findings are filtered out instead of written up. This mirrors the per-finding adversarial verify that cut a parallel review from 10 findings to 3 and targets the false-positive class that drives over-grading.

**Run this phase ONLY when the gate condition is true. Otherwise skip to Phase 4 — small, clean reviews pay nothing.**

**Gate condition (run the verify pass when EITHER is true):**

```
candidate_findings_count >= 4   OR   any finding is BLOCKING
```

Otherwise (≤3 findings, none BLOCKING): skip this phase and note in DOCUMENT: `Finding verify: SKIPPED (N findings, none blocking — below gate).`

**Step 1: Refute each finding.** For every candidate finding from Phases 2–3, attempt to refute it against the actual code. The default stance is **not-real**; a finding survives only if refutation fails. Mark **REFUTED** when:
- **Speculative** — the failure path is hypothetical; no concrete input or call sequence reaches it (Phase 1 caller tracing is the evidence here).
- **Already-handled** — a guard, validation, type constraint, or upstream caller already prevents it; cite the line.
- **Not actionable** — no specific code change resolves it, or it restates a lint/format-covered style preference.

**Step 2: Verify-and-downgrade severity.** Reviewers over-grade; the verify step may re-grade a confirmed finding's tier (BLOCKING / SHOULD FIX / SUGGESTIONS) with a written justification, recording original→final. Change severity only on evidence (e.g., "BLOCKING→SHOULD FIX: the value is a server-issued UUID, not user input — `auth/token.go:88`"). Never silently alter a tier.

**Step 3: Keep only confirmed findings** for DOCUMENT. List refuted findings separately with their refutation reason so the reader sees what was filtered and why.

**Honest framing**: this verify is structure-and-plausibility level — it refutes findings whose path is hypothetical or already-guarded. It is not a correctness oracle: a CONFIRMED finding survived a refutation attempt, it is not thereby proven a real exploitable bug.

**Cost guardrail**: the pass scales with finding count (one refutation per finding) and is bounded — the gate skips it for small/clean reviews, and each finding is verified at most once. For large reviews, cap verification to the right-sizing tier the review was sized to (tier rules and `scripts/right-size-review.py` live outside this skill); verify highest-severity findings first and note any uncapped remainder.

**Gate**: Verify pass was skipped (gate false, noted in DOCUMENT) or completed (each candidate finding CONFIRMED/REFUTED, severity re-grades recorded). Proceed only when gate passes.

### Phase 4: DOCUMENT

**Goal**: Produce structured review output with clear verdict and rationale.

Report facts without self-congratulation. Show command output rather than describing it. Be concise but informative because the review consumer needs actionable findings, not commentary.

Only flag issues within the scope of the changed code because suggesting features outside PR scope is over-engineering — but DO flag all issues IN the changed code even if fixing them requires touching other files. No speculative improvements.

When classifying severity, use the Severity Classification Rules below and classify UP when in doubt because it is better to require a fix and have the author push back than to let a real issue slip through as "optional."

Document **confirmed findings only** (after Phase 3.5). When the verify pass was skipped, all candidate findings count as confirmed. Use each finding's **final** tier (post-downgrade).

```
PHASE 4: DOCUMENT

Review Summary:
  Files Reviewed: [N]
  Lines Changed: [+X/-Y]
  Test Status: [PASS/FAIL/SKIPPED]
  Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]

Finding Verify: [RAN — confirmed N / refuted N; re-grades: original→final or "none"] | [SKIPPED — N findings, none blocking]

Refuted (filtered, not in verdict):
  1. [Original finding with file:line] — Refuted: [speculative | already-handled | not-actionable] ([citing file:line])

Findings (use Severity Classification Rules - when in doubt, classify UP):

BLOCKING (cannot merge - security/correctness/reliability):
  1. [Issue with file:line reference and category from rules]

SHOULD FIX (fix unless urgent - patterns/tests/debugging):
  1. [Issue with file:line reference and category from rules]

SUGGESTIONS (author's choice - purely stylistic):
  1. [Suggestion with benefit - only if genuinely optional]

POSITIVE NOTES:
  1. [Good practice observed]

Verdict: APPROVE | REQUEST-CHANGES | NEEDS-DISCUSSION

Rationale: [1-2 sentences explaining verdict]
```

**Validate the structured output (schema gate)**

Before accepting this review as complete, run the DOCUMENT output through the deterministic schema validator so a malformed review is caught mechanically rather than trusted on sight:

```bash
# Write the review markdown to a temp file, then validate.
python3 scripts/validate-review-output.py --type systematic /tmp/review-output.md
# Or pipe directly:
echo "$review_markdown" | python3 scripts/validate-review-output.py --type systematic -
```

Exit codes: `0` = structurally valid (verdict in {APPROVE, REQUEST-CHANGES, NEEDS-DISCUSSION}, `risk_level` present, every finding carries a `file:line` location); `1` = schema errors; `2` = unparseable; `3` = `jsonschema` not installed (`pip install jsonschema`).

This gate verifies the review is **structurally well-formed** (verdict, risk level, and finding locations present) — it does NOT verify findings completeness; a finding the parser couldn't structure is silently dropped rather than flagged.

**On validation failure:** retry exactly once, then stop.
- **Exit 1 (schema errors):** regenerate the DOCUMENT output using the validator's specific numbered error lines (e.g. `MISSING: risk_level`, `MISSING: location`) to repair the precise defect.
- **Exit 2 (unparseable):** there are no per-error lines to feed back — the output couldn't be structured at all. Regenerate the DOCUMENT output from scratch in the required format.

Validate the regenerated output. If it still fails, STOP and report the malformed output — deliver only a review that passes the schema, because a verdict built on findings without locations or a missing risk level is unactionable.

After producing the review, remove any temporary analysis files, notes, or debug outputs created during review because only the final review document should persist.

**Gate**: Output passed `validate-review-output.py --type systematic` (exit 0). Structured review output with clear verdict. Review is complete.

---

## Reference Material

### Trust Hierarchy

When conflicting information exists, trust in this order:

1. **Running code** (highest) - What tests show
2. **HTTP/API requests** - Verified external behavior
3. **Grep results** - What exists in codebase
4. **Reading source** - Direct file inspection
5. **Comments/docs** - Claims that need verification
6. **PR description** (lowest) - May be outdated or incomplete

### Severity Classification Rules

Three tiers: BLOCKING (cannot merge — security, correctness, reliability), SHOULD FIX (fix unless urgent — patterns, tests, debugging), SUGGESTIONS (genuinely optional — style, naming, micro-optimizations). When in doubt, classify UP.

See `references/severity-classification.md` for full classification tables, the decision tree, and common misclassification examples.

### Go-Specific Review Patterns

Watch for patterns that linters miss: type export design, concurrency patterns (batch+callback, loop variable capture, commit callbacks), resource management (defer placement, connection pool reuse), metrics pre-initialization, testing deduplication, and unnecessary function extraction.

For projects using shared organization libraries: check for manual SQL row iteration instead of helpers, incorrect assertion depth, raw `sql.Open()` in tests, dead migration files, and database-specific naming violations.

See `references/go-review-patterns.md` for full checklists and red flags.

### Receiving Review Feedback

When receiving feedback: read completely, restate requirement to confirm understanding, verify against codebase, evaluate technical soundness, respond with reasoning or just fix it. Never performative agreement. Apply YAGNI check before implementing "proper" features. Stop and clarify before implementing anything unclear — items may be related.

See `references/receiving-feedback.md` for the full reception pattern, pushback examples, implementation order, and external vs internal reviewer handling.

---

## Error Handling

### Error: "Incomplete Information"
Cause: Missing context about the change or its purpose
Solution:
1. Ask for clarification in Phase 1
2. Do not proceed past UNDERSTAND with unanswered questions
3. Document gaps in scope assessment

### Error: "Test Failures"
Cause: Tests fail during Phase 2 verification
Solution:
1. Document in Phase 2
2. Automatic BLOCKING finding in Phase 4
3. Cannot APPROVE with failing tests

### Error: "Unclear Risk"
Cause: Cannot determine severity of an issue
Solution:
1. Default to higher risk level (classify UP)
2. Document uncertainty in assessment
3. REQUEST-CHANGES if critical uncertainty exists

---

## References

### Examples

#### Example 1: Pull Request Review
User says: "Review this PR"
Actions:
1. Read CLAUDE.md, then read all changed files, map scope and dependencies (UNDERSTAND)
2. Run tests, verify claims in comments and PR description (VERIFY)
3. Evaluate security/performance/architecture risks (ASSESS)
4. Produce structured findings with severity and verdict (DOCUMENT)
Result: Structured review with clear verdict and rationale

#### Example 2: Pre-Merge Verification
User says: "Check this before we merge"
Actions:
1. Read CLAUDE.md, then read all changes, identify breaking change potential (UNDERSTAND)
2. Run full test suite, verify backward compatibility claims (VERIFY)
3. Assess risk level for production deployment (ASSESS)
4. Document findings with APPROVE/REQUEST-CHANGES verdict (DOCUMENT)
Result: Go/no-go decision with evidence
