---
name: evaluate-findings
description: "Critically assess external feedback (code reviews, AI reviewers, PR comments) and decide which suggestions to apply using adversarial verification. Use when the user asks to \"evaluate findings\", \"assess review comments\", \"triage review feedback\", \"evaluate review output\", or \"filter false positives\"."
---

# Evaluate Findings

Assess external feedback (code reviews, AI suggestions, PR comments) with adversarial verification. Triage findings into binary verdicts. Do not apply fixes.

## Step 1: Assess Each Finding

For each finding:

1. **Read the referenced code** at the mentioned location — include the full function or logical block, not just the flagged line
2. **Check for early exits:**
   - If the finding references code that no longer exists or has since changed, skip it and note that the code has diverged.
   - If two findings conflict with each other, skip both and document the conflict.
3. **Determine scope** — clarify whether the issue was introduced by the PR/changeset or is pre-existing. Present this distinction explicitly so the user can decide whether it belongs in this PR's scope.
   - Pre-existing issues in earlier commits on the same feature branch are in-scope by default — the entire branch is one coherent unit of work.
   - Out-of-scope findings that are genuinely useful and have low blast radius should be accepted. Only skip out-of-scope findings when the change is disproportionate to the current work.
4. **Verify the claim** against the actual code — does the issue genuinely exist?
5. **Assign a verdict and confidence:**

| Verdict | Criteria |
|---------|----------|
| **Apply** | The finding is real: clear bug, missing check, genuine improvement, style violation matching project conventions |
| **Skip** | False positive, subjective preference, reviewer is wrong, or change would be disproportionate |
| **Escalate** | Genuinely ambiguous: behavior might be intentional, involves product intent, or requires domain knowledge the agent lacks |

Also assign an internal confidence level — **High**, **Medium**, or **Low** — reflecting how certain you are about the verdict. Confidence is used solely to route findings to the Devil's Advocate in Step 2. It does not appear in the output.

**Escalate guidance:** When a finding questions whether behavior is intentional and neither docs, specs, nor code comments clarify the intent, assign Escalate. Do not autonomously accept or reject findings that hinge on product intent. If a counterpart implementation exists elsewhere, suggest checking it for consistency.

**Verdict guidance:**

- Never auto-dismiss findings about security defaults, permission escalation, or fail-open vs fail-closed behavior. Always surface these even if the behavior appears intentional.
- Readability and clarity improvements that genuinely make code cleaner are valid. Do not auto-classify cosmetic changes as subjective.
- Be skeptical of "defensive coding" suggestions that wrap natural code in verbose guards without evidence of real-world failures.
- Weight reviewer authority. Feedback from trusted reviewers (repository maintainers or admins) should be treated with higher credibility even when phrased softly.

## Step 2: Devil's Advocate

After the initial assessment, challenge uncertain findings from a different angle.

Spawn when any finding has **Medium** or **Low** confidence. Send only those findings to the subagent. High-confidence findings pass through unchallenged. Skip this step entirely if all findings are High confidence.

Launch a single subagent (`model: "opus"`, do not set `run_in_background`). Provide the Medium/Low-confidence findings with their file locations, claims, and initial verdicts. Instruct the subagent to challenge each finding: try to prove it wrong, or confirm it with evidence.

The subagent picks research tools based on claim type:

| Claim Type | Tool |
|------------|------|
| API deprecated/removed/changed | Documentation MCP tools or WebSearch |
| Method doesn't exist / wrong signature | Documentation MCP tools, WebSearch fallback |
| Code causes specific bug or behavior | Bash (isolated read-only test snippet) |
| Best practice or ecosystem claim | WebSearch |
| Migration or changelog lookup | WebSearch → WebFetch |

Use whatever documentation tools are available. The specific tools vary by project setup.

**Budget:** max 2 research actions per finding. If the first action is conclusive, skip the second.

### Subagent Verdicts

The subagent returns per finding:

- **Confirmed** — found evidence supporting the claim (with source)
- **Disputed** — found counter-evidence (with source and explanation)
- **Inconclusive** — no definitive evidence either way

## Step 3: Reconciliation

Merge subagent results with the initial assessment:

- **Confirmed**: verdict stands. Note the evidence source.
- **Disputed**: if originally Apply, downgrade to Skip or Escalate. Show both perspectives.
- **Inconclusive**: verdict stands, note the uncertainty.

Findings not investigated by the subagent keep their original verdict.

For Apply findings, document the issue and location. For Escalate findings, note what information would resolve the ambiguity. For Skip findings, document why.

## Step 4: Format Output

Summarize the evaluated findings in a table:

| File | Issue | Verdict | Investigated |
|------|-------|---------|--------------|

Where Investigated shows:
- *(empty)* — not investigated by subagent
- **Confirmed** (source) — subagent found supporting evidence
- **Disputed: [reason]** — subagent found counter-evidence

For disputed findings, add a callout below the table showing both perspectives. For each finding, indicate scope in the Issue column (e.g., "Pre-existing:" prefix).

The caller determines what to do with the evaluated findings.
