---
name: assess-release-readiness
description: Analyze branch changes for release readiness, identifying concerns and special instructions.
user-invocable: false
---

# Assess Release Readiness

Analyze a branch to determine if it's ready for release.

## Analysis Tasks

1. **Review code changes**: Check `git diff main..HEAD` for:
   - Incomplete work (TODO, FIXME, XXX comments in new code)
   - Security concerns (hardcoded secrets, credentials)
   - Runtime errors or obvious bugs

2. **Check for blocking issues**:
   - Tests failing (if tests exist)
   - Type errors (if type checking exists)
   - Missing files referenced in code

3. **Identify actionable items** (not theoretical concerns):
   - Documentation that needs updating
   - Version numbers to bump
   - Files to stage/commit before release

## What NOT to Flag

- "Breaking changes" for command renames - users adapt
- API changes in a plugin - plugins are configuration, not APIs
- Internal refactoring - doesn't affect users
- Theoretical upgrade concerns - users pull fresh versions

## Output Format

Return JSON:

```json
{
  "releasable": true,
  "verdict": "Ready for release",
  "concerns": [],
  "instructions": {
    "pre_release": [],
    "post_release": []
  }
}
```

Or if issues found:

```json
{
  "releasable": false,
  "verdict": "Needs attention before release",
  "concerns": [
    "Found TODO comment in src/foo.ts",
    "Tests failing in commands/drive.md"
  ],
  "instructions": {
    "pre_release": ["Fix failing tests", "Remove TODO comments"],
    "post_release": []
  }
}
```

## Guidelines

- Focus on issues that actually block releases
- Provide actionable instructions, not theoretical warnings
- "Breaking change" is rarely a real concern for plugins
- Empty concerns array is the happy path, not a failure
- If it doesn't require action, don't flag it
