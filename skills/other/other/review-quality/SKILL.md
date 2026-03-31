---
name: review-quality
description: "Analyze code for cross-file quality issues: duplicated logic, architectural inconsistencies, and abstraction opportunities. Returns structured findings without applying fixes. Use when the user asks to \"review quality\", \"check for duplication across files\", \"find architectural inconsistencies\", \"cross-file quality review\", or \"review code quality\"."
---

# Review Quality

Analyze code for cross-file quality issues. Return structured findings.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`, `git diff main...HEAD`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Review

1. For diff scope: run the diff command to obtain the changes. For file scope: read the specified files.
2. For each file, read the surrounding context. Then identify related files in the project (shared interfaces, similar modules, files importing the same utilities) and read those to detect cross-file patterns
3. Look across all files in the review scope for the patterns below. Cross-file issues are the primary focus — single-file quality issues are out of scope (those belong in `/simplify-code`).
4. Apply the determination criteria and return findings in the output format below

### What to Look For

1. **Cross-file duplication** — Nearly identical logic in multiple files, copy-pasted functions with slight variation across components, repeated boilerplate (setup sequences, validation logic, UI blocks) that could be extracted into a shared utility, component, or module
2. **Architectural inconsistency** — Mixed error handling patterns across modules (some throw, others return error codes), inconsistent naming conventions, different approaches to the same concern in different components (e.g., some modules use dependency injection while others use global singletons)
3. **Abstraction opportunities** — Repeated structural patterns across files that suggest a missing shared abstraction, multiple components manually implementing the same protocol or interface pattern, recurring configuration or setup boilerplate
4. **Convention drift** — Divergent logging patterns across modules, inconsistent use of project-defined constants, types, or enums, different approaches to validation, serialization, or resource management across the codebase

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It spans multiple files or represents an inconsistency across components
2. The issue is discrete and actionable
3. In diff mode: the issue was introduced or worsened by the changeset. In file scope mode: this criterion does not apply
4. Fixing the inconsistency or extracting the duplication would provide clear maintenance or readability benefit
5. The pattern has at least 2 concrete instances

## Comment Standards

1. Name all files involved in the cross-file issue (use "(and others)" for findings spanning more than 3 files)
2. Be specific about what is duplicated or inconsistent
3. Keep the body to one paragraph maximum
4. No code chunks longer than 3 lines
5. Use a matter-of-fact tone

## Priority Levels

- **P0** — Harmful inconsistency actively causing bugs or maintenance traps (e.g., error handling inconsistency where some paths swallow errors)
- **P1** — Significant duplication or architectural drift that makes changes error-prone
- **P2** — Moderate duplication or convention drift with clear extraction opportunity
- **P3** — Minor inconsistency or duplication with low maintenance impact

## What to Ignore

- Single-file code quality issues (those belong in `/simplify-code`)
- Style-only differences unless they indicate a genuine pattern inconsistency
- In diff mode: pre-existing cross-file issues not introduced or worsened by this changeset
- Intentional variation documented in project guidelines

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**File:** `<file path 1>`, `<file path 2>` (and others)
**Category:** <duplication | inconsistency | abstraction | convention-drift>

<one paragraph explaining the cross-file issue and what should change>
```

After all findings, add:

```
## Overall Verdict

**Code Quality:** <clean | issues found>

<1-3 sentence summary>
```

If there are no qualifying findings, state that the code is clean and explain briefly.
