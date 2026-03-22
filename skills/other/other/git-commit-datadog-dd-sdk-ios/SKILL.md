---
name: git-commit
description: Use when committing changes in dd-sdk-ios. Use when writing commit messages, signing commits, or staging files before a commit.
---

# Committing in dd-sdk-ios

## Requirements

- **All commits MUST be signed** (GPG or SSH)
- **Message prefix**: `[PROJECT-XXXX]` matching the JIRA ticket (internal development only)

## Message Format

```
[RUM-9999] Short imperative description
```

**Examples:**
- `[RUM-1234] Add baggage header merging support`
- `[FFL-213] Add Feature Flags support`
- `[RUM-14655] Fix WebView log events attaching incomplete ddTags`

Third-party contributions skip the prefix.

## Commit Command

```bash
git commit -S -m "[RUM-9999] Your message here"
```

The `-S` flag applies your configured GPG/SSH signature.

**Never add `Co-Authored-By: Claude` or any AI co-author trailer to commits in this repo.**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing signature | Always use `-S`; check `git log --show-signature -1` |
| Missing `[PROJECT-XXXX]` prefix | Required for internal dev; skipped for third-party |
| New files missing from pbxproj | Use Xcode MCP tools — see `xcode-file-management` skill |
| Adding `Co-Authored-By: Claude` trailer | Never add AI co-author trailers in this repo |
