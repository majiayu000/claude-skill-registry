---
argument-hint: <pr-number>
context: fork
disable-model-invocation: false
name: coderabbit
user-invocable: true
description: This skill should be used when the user asks to "review CodeRabbit feedback", "triage CodeRabbit comments", "check CodeRabbit PR review", "evaluate CodeRabbit suggestions", "process CodeRabbit review", "address CodeRabbit comments", "fix CodeRabbit issues", "coderabbit review", or mentions reviewing, triaging, or acting on CodeRabbit bot feedback on a pull request.
---

# CodeRabbit Review

Triage CodeRabbit feedback on pull requests by classifying each comment as Valid or False Positive through inspection of the actual code at the referenced location. Produce a prioritized fix plan for valid findings ordered by severity. Critical evaluation is the core principle here — not every CodeRabbit suggestion deserves a code change. Some are false positives based on incorrect assumptions about the codebase, nitpicks on matters of style preference, or inapplicable to the project's established conventions. The goal is to separate signal from noise and give the developer a clear, actionable list of what actually needs fixing.

## Arguments

Parse `$ARGUMENTS` for a PR number (required integer). Supported formats:

- Plain number: `123`
- Hash-prefixed: `#123`
- Full reference: `owner/repo#123`
- URL: `https://github.com/owner/repo/pull/123`

If `$ARGUMENTS` is empty, stop and ask the user for a PR number.

When only a bare number or `#number` is provided, infer `owner/repo` from the current working directory:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

## Related Skills

For detailed GitHub CLI command syntax, flags, and patterns, activate the `cli-gh` skill. That skill covers the full gh command surface including issue management, PR operations, repository queries, workflow triggers, and API interactions.

## Prerequisites

Verify GitHub CLI authentication before proceeding:

```bash
gh auth status
```

If not authenticated, stop with an error instructing the user to run `gh auth login`.

## Workflow

### 1) Fetch PR Metadata

Retrieve PR details for context and scoping:

```bash
gh pr view {pr_number} --json title,baseRefName,headRefName,url,files
```

Extract the PR title, base and head branches, URL, and the list of changed files. The changed files list defines the primary scope. Comments on unchanged files may still be relevant if the PR's changes affect their behavior — use judgment during classification.

### 2) Fetch CodeRabbit Review Threads

Use the GraphQL query from `references/graphql-queries.md` to fetch all review threads on the PR. Filter to threads where any comment's author login starts with `coderabbitai` (GraphQL returns `coderabbitai` without the `[bot]` suffix; REST returns `coderabbitai[bot]`). The GraphQL approach returns threaded conversations with resolution status, which is essential for skipping already-addressed feedback.

Fall back to the REST API for inline comments if GraphQL returns incomplete data:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

Also fetch PR review bodies to capture CodeRabbit's walkthrough summary, which provides high-level context about what the bot thinks the PR does:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

### 3) Parse and Group

Group comments by file path. For each comment, categorize it into one of three buckets:

- **AI-actionable**: a concrete code suggestion with a clear, specific fix that can be applied
- **Nitpick**: a style or naming preference without functional impact (e.g., "consider renaming this variable")
- **Outside diff range**: comment references code that was not changed in this PR

Skip resolved threads entirely. Check three resolution signals:

1. The `isResolved` field on the review thread
2. "Addressed in commit" markers in thread replies
3. `[x]` checkboxes indicating the author already handled the suggestion

### 4) Classify Each Comment

For each unresolved, AI-actionable comment, perform a thorough assessment:

1. **Read the actual code** at the referenced file and line number. Do not rely solely on CodeRabbit's quoted snippet — it may be outdated or truncated.
2. **Check project conventions** by examining linter configs (ESLint, Prettier, Biome, Ruff, etc.), existing patterns in the codebase, and any style guides or CONTRIBUTING.md files.
3. **Review broader context** by reading surrounding functions, the module's purpose, and related tests to understand whether the suggestion fits.
4. **Assess applicability** — does this suggestion make sense for this specific codebase, or is it generic advice that doesn't apply here?
5. **Evaluate severity** based on real impact to the system, not just theoretical concern.

Assign one of two classifications:

- **Valid** with severity: CRITICAL > HIGH > MEDIUM > LOW
  - **CRITICAL**: exploitable security flaw, data loss path, or outage risk on critical paths
  - **HIGH**: logic defect or performance failure that can break core behavior
  - **MEDIUM**: maintainability or reliability issue likely to cause near-term defects
  - **LOW**: localized clarity, style, or documentation improvements
- **False Positive** with a specific reason:
  - Incorrect assumption about the code's behavior or purpose
  - Project convention mismatch (suggestion contradicts established patterns)
  - Already handled elsewhere in the codebase
  - Out of scope for this PR's intent

### 5) Generate Fix Plan

For each valid finding, ordered by severity (CRITICAL first, LOW last), produce a structured entry:

| Field                 | Content                                       |
| --------------------- | --------------------------------------------- |
| Location              | `file:line`                                   |
| CodeRabbit suggestion | Brief summary of what was suggested           |
| Assessment            | Why this is valid and what the real impact is |
| Proposed fix          | Concrete code change description              |
| Confidence            | High / Medium / Low                           |

Confidence reflects certainty that the fix is correct and safe to apply:

- **High**: clear defect with an obvious fix, no ambiguity
- **Medium**: likely correct but depends on runtime behavior or external state not fully visible
- **Low**: plausible improvement but may have side effects or require domain knowledge to validate

### 6) Report

Output a structured report with the following sections:

**PR Summary**: title, URL, base/head branches, number of files changed.

**Scope**: N total CodeRabbit comments analyzed, N resolved (skipped), N unresolved (triaged).

**Valid Findings** (grouped by severity):

For each severity level present, list findings with location, CodeRabbit's original suggestion, your assessment, and the proposed fix. CRITICAL and HIGH findings should include explicit reasoning about blast radius and failure modes.

**False Positives**:

For each dismissed comment, list the location, what CodeRabbit suggested, and the specific rationale for dismissal. This section serves as documentation for why certain suggestions were intentionally not acted upon.

**Fix Plan**:

Ordered implementation steps for all valid findings. Group related fixes that touch the same file. Note any fixes that should be applied together to avoid intermediate broken states.

**Nitpicks (skipped)**:

Brief list of nitpick comments that were excluded from triage — mention location and what was suggested, but no fix plan entry.

**Residual Risks**:

Flag anything that needs human judgment or falls beyond automated triage — ambiguous intent, architectural concerns, suggestions that require product decisions, or findings where classification confidence is low on critical-path code.

## Stop Conditions

Stop and ask for direction when:

- The PR does not exist or is not accessible (permissions, private repo without auth).
- No CodeRabbit comments are found on the PR.
- A suggestion requires architectural changes beyond the PR's scope.
- Classification confidence is low for code on critical paths (auth, payments, data integrity).
- CodeRabbit's walkthrough summary contradicts its own individual comment suggestions, indicating the bot may have misunderstood the PR's purpose.
