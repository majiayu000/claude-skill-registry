---
name: code-review
description: >
  Multi-agent code review using the Pragmatic Quality framework. Orchestrates
  parallel review agents (CLAUDE.md compliance, bug scanning, git history,
  security) with independent confidence scoring to produce high-signal findings.
  Use when user runs /code-review, /review:code-review, requests a "code review",
  "review my changes", "PR review", or mentions "review diff", "review branch".
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr comment:*), Bash(gh pr list:*)
argument-hint: "[output-directory] [--post-to-pr]"
---

# Multi-Agent Code Review

Pragmatic Quality framework — orchestrate parallel review agents for high-signal findings.

## Parse Arguments

- If `$ARGUMENTS` contains `--post-to-pr`: enable GitHub PR posting (Phase 5)
- Remaining non-flag arguments: use as output directory (default: `./reviews/code/`)

Example usage:
- `/review:code-review` — local report to `./reviews/code/`
- `/review:code-review custom/dir` — local report to `custom/dir/`
- `/review:code-review --post-to-pr` — local report + post to GitHub PR
- `/review:code-review custom/dir --post-to-pr` — both

## Git Analysis

Analyze these outputs to understand the scope and content of the changes.

GIT STATUS:
```
!`git status`
```

FILES MODIFIED:
```
!`git diff --name-only origin/HEAD...`
```

COMMITS:
```
!`git log --no-decorate origin/HEAD...`
```

DIFF CONTENT:
```
!`git diff --merge-base origin/HEAD`
```

## Phase 1 — Context Gathering

Launch **2 parallel Haiku agents**:

**Agent A — CLAUDE.md Discovery**: Find all CLAUDE.md files in the repo (root + directories modified by the changes). Return file paths and brief content summaries of each.

**Agent B — Change Summary**: Analyze the diff above. Return: files changed count, primary areas affected, change type (feature/bugfix/refactor/config/test/docs), estimated risk level (Low/Medium/High/Critical).

## Phase 2 — Parallel Review

Launch **4-5 Sonnet agents simultaneously**. Provide each with: the full diff content, the CLAUDE.md summaries from Phase 1, and the change summary. Each agent returns findings in this format:

```
Finding: {description}
File: {path}:{line}
Category: {CLAUDE.md | Bug | History | Security | Comments}
Reason: {why this was flagged}
Suggested fix: {code snippet, if applicable}
```

### Reviewer 1 — CLAUDE.md Compliance
Audit changes against all discovered CLAUDE.md rules. Only flag items **specifically** called out in a CLAUDE.md. Double-check that the CLAUDE.md actually requires what is being flagged. Ignore silenced rules (lint-ignore comments).

### Reviewer 2 — Bug Scanner
Shallow scan for **obvious bugs** in the diff only. Focus on large bugs — avoid nitpicks. Do NOT read extra context beyond the changes. Ignore issues linters/typecheckers would catch.

### Reviewer 3 — Git Blame/History Analyzer
Read git blame and history of modified files. Identify issues in light of historical context: reverted changes being re-modified, recently-fixed areas, breaking established conventions, patterns from previous PR comments.

### Reviewer 4 — Security Reviewer
Security-focused scan: injection (SQLi, XSS, command), auth/access control, secrets/credentials, data exposure in logs/responses, crypto misuse. Only report HIGH confidence exploitable findings.

### Reviewer 5 — Code Comments Compliance (conditional)
**Only launch** if modified files contain substantive code comments (`// NOTE:`, `// IMPORTANT:`, `// INVARIANT:`, `// SAFETY:`, `// TODO:`). Ensure changes comply with guidance in those comments.

### False Positive Awareness

All reviewers must skip these false positive categories:
- Pre-existing issues not introduced in the changes
- Issues that linters, typecheckers, or compilers would catch
- Pedantic nitpicks a senior engineer wouldn't flag
- Framework-handled concerns (e.g., XSS in React unless using unsafe HTML injection APIs)
- General quality issues unless explicitly required in CLAUDE.md
- Style preferences matching existing codebase conventions
- Real issues on lines the author did not modify

See [WORKFLOW.md](WORKFLOW.md) for detailed false positive filtering rules.

## Phase 3 — Confidence Scoring

For **each finding** from Phase 2, launch a **parallel Haiku agent** that:

1. Receives: the finding description, the relevant diff section, and the CLAUDE.md files list
2. Scores 0-100 using this rubric:
   - **0**: False positive — doesn't hold up to scrutiny, or pre-existing issue
   - **25**: Might be real, but may also be false positive. Unable to verify.
   - **50**: Verified issue, but minor or nitpick. Not very important relative to the rest.
   - **75**: Very likely real. Existing approach is insufficient. Important and impactful.
   - **100**: Confirmed. Will happen in practice. Evidence directly confirms this.
3. For CLAUDE.md findings: double-check the CLAUDE.md actually calls out the issue
4. Returns: score + brief justification

**Filter**: Remove all findings scoring below **80**. If no findings survive, generate a clean report.

## Phase 4 — Report Generation

Generate the report using the template in [WORKFLOW.md](WORKFLOW.md).

Map confidence scores to triage levels:
- 90-100 → **Blocker** (if severity warrants) or **Improvement**
- 80-89 → **Improvement** or **Question**

Include for each finding: the `Source` category (CLAUDE.md, Bug Scan, Git History, Security, Comments).

1. Create output directory: `mkdir -p {output-directory}`
2. Save report to: `{output-directory}/{YYYY-MM-DD}_{HH-MM-SS}_code-review.md`
3. Display the full report to the user
4. Confirm the save path

## Phase 5 — Optional GitHub PR Posting

**Only execute if** `--post-to-pr` flag was passed.

1. Check if an open PR exists for the current branch via `gh pr view`
2. If no PR exists, inform the user: "No open PR found for this branch. Skipping GitHub posting."
3. If a PR exists, check eligibility via a **Haiku agent**:
   - Is the PR closed? → skip
   - Is the PR a draft? → skip
   - Has Claude already commented on this PR? → skip
4. If eligible, format findings as a concise PR comment and post via `gh pr comment`
5. Use the GitHub comment format from [WORKFLOW.md](WORKFLOW.md)

## Phase 6 — Automatic Verification

After saving the report, invoke the false-positive verifier:

1. Use the Skill tool to invoke `review:verify-findings` with the saved report path
2. The verifier runs in an isolated forked context and produces a `.verified.md` report
3. After verification completes, inform the user of both report locations

If the Skill tool is not available (e.g., running inside a subagent):
> Run verification manually: `/review:verify-findings {report-path}`

## Resources

- [WORKFLOW.md](WORKFLOW.md) — Detailed review checklists, agent prompt templates, scoring rubric, report template, GitHub comment format
- [EXAMPLES.md](EXAMPLES.md) — Sample reports and orchestration flow examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues with pipeline, scoring, and output
