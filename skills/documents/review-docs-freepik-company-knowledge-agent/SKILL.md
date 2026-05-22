---
name: review-docs
description: Review and clean technical documentation (Markdown/README/runbooks/ADRs). Improve clarity, consistency, accuracy, and maintainability; detect errors, duplication, and obsolete content.
argument-hint: "[paths|files|folders] (optional)"
disable-model-invocation: true
---

Act as a Technical Writer + Senior Engineer + QA. Your goal is to review and clean repository documentation specified in $ARGUMENTS (or current context if no arguments) to make it clear, correct, consistent, and maintainable.

Deliver in this format:

A) SUMMARY
- Status: ✅ Ready / ⚠️ Requires adjustments / ❌ Inconsistent or dangerous
- Top 5 issues (prioritized)
- Minimum actions to reach "✅ Ready"

B) FINDINGS (prioritized)
For each finding include:
- Severity: P0 (blocking) / P1 / P2 / P3
- Evidence: file:section (or exact heading)
- Problem: what's confusing or wrong
- Proposed fix: suggested text or concrete restructuring (in Markdown)

C) REWRITE PROPOSAL (if applicable)
- Proposed index (TOC) or recommended structure
- Sections to merge/delete/move
- List of normalized "names/terminology"

Review and cleanup criteria:

1) Accuracy and currency
- Detect obsolete content (commands, paths, flags, dependencies, versions, processes).
- Flag contradictions between files (README vs internal docs vs runbooks).
- Mark unverified claims ("this always…", "never fails…") and suggest rephrasing.

2) Clarity and readability
- Long sentences, ambiguities, logical jumps.
- Rewrite so a new developer understands the "what", "why", and "how".
- Add minimum context: prerequisites, limits, gotchas.

3) Editorial and technical consistency
- Unify terminology, component names, capitalization, list style, verb tenses.
- Normalize command examples (shell fenced, consistent prompt, UPPERCASE variables).
- Maintain convention: "imperative" for steps ("Execute…", "Verify…").

4) Security and compliance
- Find and remove/anonymize secrets, tokens, credentials, sensitive internal URLs, or PII.
- Avoid recommending insecure practices (e.g., "disable TLS", "chmod 777", "export AWS_SECRET…").
- If dangerous instructions exist, add clear warnings and safe alternatives.

5) Operations and runbooks
- Verify runbooks have: symptoms → diagnosis → mitigation → rollback → verification.
- Add "before/after" checks and measurable success criteria.
- Flag non-deterministic steps or those dependent on tribal knowledge.

6) Actionability
- Each section must allow executing the task without guessing:
  - prerequisites
  - concrete commands
  - examples of expected inputs/outputs
  - relevant internal links (no broken links)

Rules:
- Don't invent tools/processes: if data is missing, mark "NEEDS CONFIRMATION" and propose what to ask or where to verify in the repo.
- Minimize meaning changes: prioritize clarity and correctness, not style for style's sake.
- When proposing text, deliver it ready to paste into Markdown.