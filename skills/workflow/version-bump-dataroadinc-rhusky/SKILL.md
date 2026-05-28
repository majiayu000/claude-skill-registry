---
name: version-bump
description:
  Bump version in Cargo.toml
---

# Version Bump Skill

Use this skill when bumping the version of rhusky.

## How to Bump Version

1. Edit `Cargo.toml` and update the `version` field
2. Run `cargo update --workspace` to update `Cargo.lock`
3. Commit with message: `chore(version): bump X.Y.Z -> A.B.C`

## Version Types

- **patch**: Bug fixes, minor improvements (0.0.1 -> 0.0.2)
- **minor**: New features, backward compatible (0.1.0 -> 0.2.0)
- **major**: Breaking changes (1.0.0 -> 2.0.0)

## What NOT to Do

- Do NOT use `cog bump` - it creates local tags which conflict with
  the CI workflow that creates tags after tests pass
- Do NOT create git tags manually - CI creates tags after merge
- Do NOT push to remote - the user must push manually

## Workflow

1. Edit `Cargo.toml` version field
2. Run `cargo update --workspace`
3. Stage changes: `git add Cargo.toml Cargo.lock`
4. Commit: `git commit -m "chore(version): bump X.Y.Z -> A.B.C"`
5. Push the branch or create a PR
6. Merge to main
7. CI detects version change, creates tag, publishes release

## Checking Current Version

```bash
# Get version from Cargo.toml
grep '^version' Cargo.toml
```

## After Bumping

After committing the bump, verify:

```bash
git log -1 --oneline
git diff HEAD~1 --stat
```

Then push when ready:

```bash
git push origin <branch>
```
