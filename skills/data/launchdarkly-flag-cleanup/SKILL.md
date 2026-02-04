---
name: launchdarkly-flag-cleanup
description: "Safely automate feature flag cleanup workflows using the LaunchDarkly MCP server. Use when removing flags from code, cleaning up stale flags, assessing removal readiness, or creating PRs that preserve production behavior."
license: Apache-2.0
compatibility: Requires LaunchDarkly MCP server (@launchdarkly/mcp-server)
metadata:
  author: launchdarkly
  version: "1.0.0-alpha"
---

# LaunchDarkly Flag Cleanup

A workflow for safely removing feature flags from codebases while preserving production behavior. This skill uses LaunchDarkly as the source of truth to determine removal readiness and the correct forward value.

## Prerequisites

This skill requires the LaunchDarkly MCP server to be configured in your environment.

**Required MCP tools:**
- `get-environments`
- `get-feature-flag`
- `get-flag-status-across-environments`
- `get-code-references`

## Core Principles

1. **Safety First**: Always preserve current production behavior.
2. **LaunchDarkly as Source of Truth**: Never guess. Query the actual configuration.
3. **Clear Communication**: Explain reasoning in PR descriptions.
4. **Follow Conventions**: Respect existing code style and structure.

## Flag Removal Workflow

### Step 1: Identify Critical Environments

Use `get-environments` with the project key to find environments marked as critical (typically `production`, `staging`, or user-specified).

### Step 2: Fetch Flag Configuration

Use `get-feature-flag` to retrieve the full configuration. Extract:
- `variations`: Possible values
- Per critical environment:
  - `on`: Whether enabled
  - `fallthrough.variation`: Variation index when no rules match
  - `offVariation`: Variation index when flag is off
  - `rules`: Targeting rules (complexity indicator)
  - `targets`: Individual context targets

### Step 3: Determine Forward Value

The **forward value** replaces the flag in code.

| Scenario | Forward Value |
|----------|---------------|
| All critical envs ON, same fallthrough, no rules/targets | Use `fallthrough.variation` |
| All critical envs OFF, same offVariation | Use `offVariation` |
| Critical envs differ in ON/OFF state | **NOT SAFE** - stop |
| Critical envs serve different variations | **NOT SAFE** - stop |

### Step 4: Assess Removal Readiness

Use `get-flag-status-across-environments` to check lifecycle status.

**READY** if ALL true:
- Status is `launched` or `active` in all critical environments
- Same variation served across all critical environments
- No targeting rules or individual targets in critical environments
- Flag is not already archived/deprecated

**PROCEED WITH CAUTION** if:
- Status is `inactive` (no recent traffic)
- Zero evaluations in last 7 days (confirm with user)

**NOT READY** if:
- Status is `new` (still rolling out)
- Different variations across critical environments
- Complex targeting rules exist
- Critical environments differ in ON/OFF state

### Step 5: Check Code References

Use `get-code-references` to identify repositories. If the current repo isn't listed, inform the user. Note the count of other repositories for awareness.

### Step 6: Remove Flag from Code

Search for all references and replace with the forward value:

1. **Find evaluation patterns:**
   - `variation('flag-key', ...)`
   - `boolVariation('flag-key', ...)`
   - `featureFlags['flag-key']`
   - SDK-specific and wrapper patterns

2. **Replace with forward value:**
   - Preserve the branch matching the forward value
   - Remove the dead branch and related code
   - If assigned to a variable, replace with the value directly

3. **Clean up:**
   - Remove unused imports/constants
   - Avoid unrelated refactors
   - Double-check for orphaned exports or files created solely for the flag
     (unused components, hooks, helpers, styles, and test files)
   - If the repo uses an unused-export tool (e.g., lint rules, Knip, ts-prune),
     run it and remove any flag-related orphans it reports

**Example transformation (forward value = true):**
```typescript
// Before
const showNewCheckout = await ldClient.variation('new-checkout-flow', user, false);
if (showNewCheckout) {
  return renderNewCheckout();
} else {
  return renderOldCheckout();
}

// After
return renderNewCheckout();
```

### Step 7: Create Pull Request

Use the template in `references/pr-template.md` for a structured PR description including removal summary, readiness assessment, and risk analysis.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Flag not found | Inform user, check for typos |
| Already archived | Ask if code cleanup still needed |
| Multiple SDK patterns | Search all: `variation()`, `boolVariation()`, `variationDetail()`, `allFlags()` |
| Dynamic flag keys (`flag-${id}`) | Warn that automated removal may be incomplete |
| Different default values in code | Flag as inconsistency in PR |
| Orphaned exports/files remain | Run unused-export checks and remove dead files |

## What NOT to Do

- Don't change code unrelated to flag cleanup.
- Don't refactor or optimize beyond flag removal.
- Don't remove flags still being rolled out.
- Don't guess the forward value.

## Related Resources

- [PR Template](references/pr-template.md)
- [SDK Patterns](references/sdk-patterns.md)
