---
name: release-harness
description: "Automate Harness release. CHANGELOG, version, tag in one click. Use when user mentions harness release, harness version bump. Do NOT load for: general release discussions, other project releases."
description-en: "Automate Harness release. CHANGELOG, version, tag in one click. Use when user mentions harness release, harness version bump. Do NOT load for: general release discussions, other project releases."
description-ja: "Harness リリース作業を自動化。CHANGELOG、バージョン、タグをポチッと一発。Use when user mentions harness release, harness version bump. Do NOT load for: general release discussions, other project releases."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
argument-hint: "[patch|minor|major]"
user-invocable: false
context: fork
---

# Release Harness Skill

Automates the claude-code-harness release process.

## Quick Reference

- "**Release a new harness version**" -> `/release-harness`
- "**Bump patch version**" -> `/release-harness patch`
- "**Create a minor release**" -> `/release-harness minor`

---

## Execution Flow

### Step 1: Change Verification

Run in parallel:
1. `git status` - Check uncommitted changes
2. `git diff --stat` - List changed files
3. `git log --format="%h|%s|%an|%ad" --date=short -10` - Recent commit history (structured)

### Git Log Flags (CC 2.1.30+)

Use structured log output for release note generation.

#### Commit List for Release Notes

```bash
# Structured format commit list
git log --format="%s" vPREV..HEAD

# Exclude merge commits (actual changes only)
git log --cherry-pick --no-merges --format="%s" vPREV..HEAD

# Detailed info (with author and date)
git log --format="%h|%s|%an|%ad" --date=short vPREV..HEAD
```

#### Key Use Cases

| Use Case | Flags | Effect |
|----------|-------|--------|
| **Release note generation** | `--format="%s"` | Extract commit messages only |
| **Exclude merges** | `--cherry-pick --no-merges` | Actual commits only |
| **Detailed list** | `--format="%h\|%s\|%an\|%ad"` | Structured detailed info |
| **Changed files** | `--raw` | Impact analysis |

### Step 2: Version Determination

Check current version:
```bash
cat VERSION
```

Determine version based on changes ([Semantic Versioning](https://semver.org/)):
- **patch** (x.y.Z): Bug fixes, minor improvements
- **minor** (x.Y.0): New features (backward compatible)
- **major** (X.0.0): Breaking changes

Ask user: "What should the next version be? (e.g., 2.5.23)"

### Step 3: CHANGELOG Update (JP + EN)

> **Important**: Focus on user-facing changes. Keep internal fixes brief.

Update both `CHANGELOG_ja.md` and `CHANGELOG.md`.

#### CHANGELOG Rules

| Change Type | How to Document |
|-------------|-----------------|
| **User-facing impact** | `What's Changed` + Before/After table |
| **New feature** | `Added` section, concise |
| **Internal (CI/test/docs)** | `Internal` section, one line |
| **Bug fix (user-facing)** | `Fixed` section |
| **Bug fix (internal only)** | Omit or merge into `Internal` |

#### Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### What's Changed

**One-line description of user experience change**

| Before | After |
|--------|-------|
| Previous state | New state |

### Added

- Concise feature description

### Internal

- One-line summary of internal changes
```

#### Before/After Table Rules

- Only for **user-facing changes**
- Not needed for internal fixes (CI, tests, refactoring)
- Write from **user perspective**, not technical details

### Step 3.5: README Update Check

> Check if README needs update (JP/EN both)

### Step 4: Version File Update

```bash
echo "X.Y.Z" > VERSION
```

Also update `.claude-plugin/plugin.json`:
```json
"version": "X.Y.Z"
```

### Step 5: Commit and Tag

```bash
git add -A
git commit -m "chore: release vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### Step 6: Push

```bash
git push origin main
git push origin vX.Y.Z
```

### Step 7: GitHub Release (Optional)

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - Title" \
  --notes "$(cat <<'EOF'
## What's Changed

**One-line user experience change**

| Before | After |
|--------|-------|
| Previous state | New state |

### Added / Changed / Fixed

- Concise description

---

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## GitHub Release Format

Follow `.claude/rules/github-release.md`:

```markdown
## What's Changed

**One-line value description**

| Before | After |
|--------|-------|
| Previous state | New state |

### Added / Changed / Fixed

- Brief description

---

Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Related Skills

- `verify` - Pre-release verification
