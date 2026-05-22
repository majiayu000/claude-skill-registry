---
name: interactive-code-review
description: Human-in-the-loop code review with chunk-by-chunk approve/reject/chat loop (git add -p style). Use when reviewing PRs, diffs, patches, or documents interactively. Triggers on "review my PR", "walk through changes", "interactive review".
---

# Interactive Code Review

Run a structured, interactive review session that presents changes in small, readable chunks and waits for the human to approve, reject, or chat before moving on.

## Framework

Structured Walkthrough: author intent is surfaced first, then the reviewer probes for risks, gaps, and misunderstandings. Established software quality practice (IEEE 1028) for defect detection and shared understanding.

## Workflow

1. **Confirm target and intent.**
   - Ask for the diff source if unclear (branch range, file paths, or patch).
   - Clarify what "good" looks like (correctness, style, performance, risk).

2. **Gather material.**
   - For code: `git status -sb`, `git diff --stat`, then `git diff <base>...<head>`.
   - For documents: ask for the text, sections, or relevant excerpt.

3. **Chunk the review.**
   - File-by-file, then hunk-by-hunk within each file.
   - Target 40–120 lines per chunk. Split large hunks.
   - Order: module boundaries (entry points, public interfaces) first, then internals, finally tests.
   - For prose: split by headings or logical paragraphs.

4. **Present each chunk** with the standard template. Pause for explicit response.

5. **Handle responses.**
   - **Approve**: mark approved, continue.
   - **Reject**: explain issue, propose concrete edit, confirm before changing files.
   - **Chat**: answer questions, show context. Re-prompt with same actions. Chat loops until user gives approve/reject/skip.
   - **Skip**: mark for later, continue.
   - **Done**: end review immediately, show summary.
   - **Jump [file]**: skip to specific file.

6. **Wrap up with summary.**
   - List approved, rejected, skipped chunks.
   - Offer to apply edits or re-run on updated diffs.

## Actions

| Action | Aliases | Effect |
|--------|---------|--------|
| approve | ok, lgtm, yes, y, +1 | Mark approved, continue |
| reject | no, fix, change, -1 | Explain issue, propose edit |
| chat | ?, context, explain, why | More context, re-prompt |
| skip | later, defer | Mark for later, continue |
| done | stop, abort | End review, show summary |
| jump [file] | go [file] | Skip to specific file |

## Chunk Template

```
Review chunk [i/N]
File: <path>
Summary: <1–2 lines>

<diff snippet>

Action? (approve / reject / chat / skip / done)
```

## Progress Indicator

After every 5 chunks or on request:
```
Progress: [====------] 4/10 | 2 approved | 1 rejected | 1 skipped
```

## Reviewer Conduct

- Verify before asserting or applying edits.
- Ask clarifying questions when feedback or intent is unclear.
- Avoid performative agreement; focus on evidence and fixes.
- Keep tone neutral and concise; avoid rewriting unless requested.

## Review Heuristics

- Flag correctness risks, security issues, breaking changes, and missing tests first.
- At module boundaries: verify the contract (inputs/outputs) is preserved.
- For legacy code: check if change increases or decreases testability.
- For text: flag unclear intent, inconsistencies, missing context.
- If rejecting, include: issue, why it matters, and a concrete fix.

## Deep Review Mode

If user asks for full assessment (e.g., "production readiness"):

### Strengths
[What's well done.]

### Issues

#### Critical (Must Fix)
[Bugs, security, data loss risks]

#### Important (Should Fix)
[Design gaps, missing requirements, test gaps]

#### Minor (Nice to Have)
[Nitpicks, optimizations, docs]

### Recommendations
[Concise improvements]

### Assessment

**Ready to merge?** [Yes/No/With fixes] (X-Y% confident)

**Key assumptions:** [List 2-3 assumptions behind assessment]

**Reasoning:** [1-2 sentences]

## Integration

- Before claiming review complete: run `hope:gate` checklist
- If rejection reveals systemic issue: suggest `hope:trace` for root cause
- For security-focused reviews: reference `soul/references/differential-review.md`

## Safety

- Do not stage, commit, or modify files unless user explicitly asks.
- Maximum: 20 files or 2000 lines of diff per session. Larger reviews: split by directory.
- Binary files: skip with note "Binary file, review manually"
- Merge conflicts: pause and ask user to resolve first
