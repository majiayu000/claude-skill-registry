---
name: release-guard
description: STRICT GitHub release gatekeeper. Blocks premature releases (from develop, incomplete CI). Verifies PR merged to main + ALL CI passed before allowing tag/release. Triggers on "release", "tag", "publish", "deploy", "version".
allowed-tools: Read, Bash(gh *:*), Bash(git *:*)
---

# Release Guard Skill

## Core Rules (NEVER VIOLATE)
- Releases **ONLY** from **main** after PR merge.
- **ALL** CI jobs must COMPLETE + SUCCESS. NO queued jobs.
- Verify branch protection requires status checks.

## Activation Steps
1. **PR Check**: Ask for PR# if needed. Run `gh pr view $PR_NUM --json state,baseRefName`. Must: state=CLOSED, baseRefName=main.
2. **Branch**: `git branch --show-current` + `gh repo view --json default_branch`. Fail if not main.
3. **CI**: `gh run list --branch main --limit 5 --json status,conclusion`. ALL: completed + success. Log/screenshot.
4. **Clean**: `git status` (clean working dir).

## Fail Response
```
🚫 BLOCKED: [Exact violation]
Fix:
- Merge PR to main
- Wait CI: gh run list --branch main
- git checkout main && git pull
Re-run task.
```

## Pass: Safe Release
- Tag: vMAJOR.MINOR.PATCH (semantic).
- `gh release create v1.2.3 --generate-notes --target main`
- Confirm before execute.

## Examples
- User: "Create release from develop PR #199" → BLOCK: Wrong branch.
- User: "Tag v1.0.0 after PR #199" → Check PR/CI/branch → Proceed if pass.

Progressive disclosure: For CI details, see [ci-reference.md](ci-reference.md) if needed.
```

## Best Practices Applied
- **Description**: Keyword-rich for matching ("release", "tag").
- **allowed-tools**: Read + Bash wildcards (gh/git CLI). Install `gh`.[2]
- **Structure**: Essential in SKILL.md; link supports (add `ci-reference.md` for details).
- **Load/Test**: Restart Claude Code. Ask "What Skills available?". Test: "Create release PR #199".

