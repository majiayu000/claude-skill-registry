---
name: verify-findings
description: >
  Verify code-review or security-review findings for false positives using
  deep codebase tracing, framework-aware analysis, and web research.
  Produces a .verified.md report alongside the original.
  Use when a review report has been generated and needs independent verification,
  or when user runs /verify-findings, mentions "verify review", "check false positives",
  or "validate findings".
context: fork
argument-hint: "<report-path>"
---

# Verify Review Findings

Independent false-positive verification. Assume every finding is false until proven by evidence.

## Parse Arguments

- `$ARGUMENTS` (required): Path to the review report file to verify

If no argument is provided, ask the user for the report path.

## Step 1 — Read and Parse Report

1. Read the report file at the provided path
2. Detect review type from the header:
   - "Pragmatic Code Review Report" → code review
   - "Security Review Report" → security review
3. Extract each finding into a structured list:
   - Triage level (Blocker, Improvement, Question)
   - File path and line number
   - Description and confidence/severity scores
   - For security: CWE, category, exploit scenario
4. **Skip** Praise and Nit findings — only verify Blocker, Improvement, and Question

## Step 2 — Verify Each Finding

For each extracted finding, perform independent verification. See [WORKFLOW.md](WORKFLOW.md) for detailed procedures.

### Code Review Findings

1. **Read the flagged code** at the specified line with ~50 lines of surrounding context
2. **Grep the codebase** for the same pattern to check if it's an established convention
3. **Verify the cited principle** — does SOLID/DRY/KISS/YAGNI actually apply here?
4. **Check framework handling** — does the framework or library address this concern automatically?
5. **Assess concrete impact** — is the problem demonstrable or theoretical?

### Security Review Findings

1. **Read the flagged code** and trace data flow from source to sink
2. **Grep for sanitizers/validators** in the code path between source and sink
3. **Detect framework protections** — React auto-escaping, Spring Security, Django ORM parameterization, etc.
4. **WebSearch the CWE/CVE** for known false positive patterns and framework-specific mitigations
5. **Verify exploit feasibility** — is the exploit scenario actually possible in this application context?
6. **Check code context** — is this test-only code, behind authentication, or behind a feature flag?

## Step 3 — Render Verdict

For each finding, assign one of:

| Verdict | Criteria | Action |
|---------|----------|--------|
| **CONFIRMED** | Evidence supports the finding | Keep in report, add verification note |
| **DISMISSED** | Finding is a false positive | Move to Dismissed section with explanation |
| **DOWNGRADED** | Valid but lower severity/confidence | Adjust scores, add explanation |

**Decision rules**: See [WORKFLOW.md](WORKFLOW.md) for the complete verdict decision matrix.

**Default to CONFIRMED** if uncertain after thorough investigation (conservative approach).

## Step 4 — Generate Verified Report

1. **Create the verified report** at: `{original-path-without-extension}.verified.md`
   - Example: `reviews/code/2026-03-01_14-30-00_code-review.md` → `reviews/code/2026-03-01_14-30-00_code-review.verified.md`
2. **Preserve original structure** — keep the same header, PR assessment, and format
3. **Add verification header**:

```markdown
**Verified by**: Claude Code (false-positive-verifier)
**Verification Date**: {ISO 8601 date}

## Verification Summary
| Metric | Count |
|--------|-------|
| **Findings Reviewed** | {N} |
| **Confirmed** | {N} |
| **Downgraded** | {N} |
| **Dismissed** | {N} |
| **Signal Ratio** | {confirmed / total reviewed}% |
```

4. **Annotate confirmed findings** with verification notes:

```markdown
> **Verification**: CONFIRMED — {evidence summary}
```

5. **Append Dismissed Findings section**:

```markdown
## Dismissed Findings

### Dismissed 1: `{file}:{line}` — {Original description}
- **Original Triage**: {Blocker/Improvement/Question}
- **Original Confidence**: {score}
- **Reason**: {Why this is a false positive}
- **Evidence**: {What was checked — grep results, framework docs, web research}
```

6. **Update Verdict** with revised counts and recommendation

See [WORKFLOW.md](WORKFLOW.md) for the complete report template.
See [EXAMPLES.md](EXAMPLES.md) for sample verified reports.

## Output Instructions

1. Save the verified report alongside the original
2. Display the full verified report to the user
3. Confirm: "Verified report saved to: {path}"

## Resources

- [WORKFLOW.md](WORKFLOW.md) — Detailed verification procedures, verdict decision matrix, web research protocol, report template
- [EXAMPLES.md](EXAMPLES.md) — Sample verified reports for code and security reviews
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues with input parsing, verification quality, and output
