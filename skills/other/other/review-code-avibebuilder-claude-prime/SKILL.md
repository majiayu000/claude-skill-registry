---
name: review-code
description: "Review code for quality, correctness, and fit. Use when the user wants judgment on code that already exists — their own changes, a teammate's patch, a PR, branch, commit, diff, staged changes, or one or more files to look over. Activate on requests like review, look over, sanity check, critique, code review, or 'is this good?' The key signal is that the user wants evaluation of existing code and its tradeoffs, not implementation, debugging, or explanation. This skill works independently, but when plans, specs, task artifacts, or prior discussion exist, use them to understand why the code exists before judging it."
argument-hint: what-to-review
---

ultrathink

## Process

Critique only — no fixes or implementation. Understand *why* the code exists before judging it.

### 1. Identify the review target

Prefer in order: explicit `<target>`, changes made in this conversation, working diff. If unclear, ask.

Then gather enough context (PR/issue text, plans, surrounding code) to avoid misreads. Don't turn every review into archaeology — if a missing detail would materially change judgment, ask briefly.

### 2. Match depth to risk

- **Quick** — small, local, low-risk; keep output brief
- **Standard** — normal feature or refactor
- **Deep** — risky, cross-cutting, security-sensitive, or surprising

### 3. Review flow first, then details

Understand how important parts work before commenting line by line. Focus on load-bearing logic, edge cases, scope drift, and intentional tradeoffs.

### 4. Report

For each finding: file path + line, why it matters, severity.

- **Critical** — correctness, safety, broken edge cases, scope violations. Requires evidence in the code — speculative failure modes belong in Questions.
- **Suggestion** — non-blocking improvements
- **Question** — missing context or unconfirmable concerns

If something looks odd but context supports it, acknowledge rather than flag.

### 5. Output format

```
## Code Review: [scope]

**Verdict: {Approve | Request Changes | Reject}**

### Inferred Intent
[Only when context supports it]

### Critical Issues (Must Fix)
- `path/to/file:line` — concise description. Why: [reason]

### Suggestions (Nice to Have)
- `path/to/file:line` — concise description

### Questions
- [Clarifications on intent or tradeoffs]

### Summary
[1-2 sentences]
```

Include only sections with content. Always include Verdict and Summary.

## Boundaries

- Read surrounding code when the diff alone is misleading.
- Deliberate decisions (inline comments, user-stated tradeoffs) are not defects — raise as Question only with concrete evidence.
- Don't judge by personal preference when project fit explains the choice.
- Name the right approach ("needs parameterized queries") but don't write corrected code.

## Target

<target>$ARGUMENTS</target>
