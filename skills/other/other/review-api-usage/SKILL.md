---
name: review-api-usage
description: "Check API, library, and framework usage in code against official documentation and installed skill knowledge. Flags deprecated APIs, incorrect method signatures, wrong parameter types, version-incompatible patterns, and best-practice violations. Use when the user asks to \"review API usage\", \"check API usage\", \"verify against docs\", \"check library usage\", \"validate API calls\", \"check against documentation\", or \"check for deprecated APIs\"."
---

# Review API Usage

Check API, library, and framework usage in code against official documentation and installed skill knowledge. Return structured findings.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`, `git diff main...HEAD`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Extract Library Usage

1. For diff scope: run the diff command to obtain the changes and identify external library/framework APIs in changed lines. For file scope: read the specified files and identify all external library/framework API usage.
2. Cross-reference with project dependency files to determine library versions in use
3. Filter out standard library and language built-ins. Focus on third-party dependencies.

If no external library usage is found, report that and stop.

## Step 3: Look Up Documentation

For each identified library with non-trivial usage in the diff:

1. Resolve the library using documentation MCP tools or WebSearch
2. Query for the specific APIs, methods, or configuration patterns being used
3. Note the documented signatures, parameter types, return types, deprecation status, and version requirements

Prioritize libraries where the diff introduces new usage or changes existing call patterns. Skip libraries where the diff only adds/removes an import with no API calls.

## Step 4: Load Relevant Skills

Check available skills for any relevant to the libraries or frameworks identified in Step 2. Run matching skills to load their domain-specific best practices and conventions as additional review context.

If no relevant skills are found, proceed without them.

## Step 5: Review Against Documentation and Best Practices

For each API usage site in the diff, compare actual usage against the retrieved documentation:

- **Wrong signatures** — incorrect parameter count, order, or types
- **Deprecated APIs** — using methods/classes/functions marked as deprecated
- **Version mismatches** — using APIs not available in the project's pinned version
- **Missing required parameters** — omitting parameters that have no default value
- **Incorrect return type assumptions** — treating the return value as a different type than documented
- **Configuration errors** — invalid option names, wrong value types, removed configuration keys
- **Breaking change patterns** — usage patterns that match known breaking changes between versions
- **Best-practice violations** — patterns that contradict guidance from loaded skills

## Issue Determination Criteria

Flag an issue only when ALL of these hold:

1. The documentation or loaded skill clearly contradicts the usage (not ambiguous or underdocumented)
2. The issue is discrete and actionable
3. In diff mode: the issue was introduced in the changeset (do not flag pre-existing usage). In file scope mode: this criterion does not apply
4. The documented behavior applies to the library version in the project's dependency file
5. The issue would cause incorrect behavior, a runtime error, or a deprecation warning

## Comment Standards

1. Name the specific API and what the documentation says
2. Quote or paraphrase the relevant documentation
3. Keep the body to one paragraph maximum
4. No code chunks longer than 3 lines
5. Include the library version context when relevant
6. Use a matter-of-fact tone

## Priority Levels

- **P0** — Will cause a runtime error or crash (wrong signature, removed API)
- **P1** — Will cause incorrect behavior silently (wrong parameter type coerced, deprecated API with changed semantics)
- **P2** — Deprecated API that still works but will be removed in a future version
- **P3** — Suboptimal usage where documentation recommends a better alternative

## What to Ignore

- Standard library and language built-in usage
- APIs where documentation is ambiguous or unavailable
- In diff mode: pre-existing usage not changed by this diff
- Internal project APIs (only check third-party dependencies)
- Style preferences not grounded in documentation

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**File:** `<file path>` (lines <start>-<end>)
**Library:** <library name> <version>
**Docs:** <brief quote or paraphrase of what the documentation says>

<one paragraph explaining the mismatch between usage and documentation, and the impact>
```

After all findings, add:

```
## Overall Verdict

**API Usage:** <correct | issues found>

<1-3 sentence summary of libraries checked and whether usage aligns with documentation>
```

If there are no qualifying findings, state that API usage looks correct, list the libraries checked, and explain briefly.
