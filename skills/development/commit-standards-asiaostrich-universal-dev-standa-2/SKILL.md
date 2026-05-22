---
name: commit
scope: universal
description: |
  Format commit messages following conventional commits standard.
  Use when: writing commit messages, git commit, reviewing commit history.
  Keywords: commit, git, message, conventional, feat, fix, refactor.
---

# Commit Message Standards

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/commit-standards/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-24
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Commit Message Guide](../../core/commit-message-guide.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill ensures consistent, meaningful commit messages following conventional commits.

## Quick Reference

### Basic Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| English | When to Use |
|---------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring (no functional change) |
| `docs` | Documentation only |
| `style` | Formatting (no code logic change) |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |
| `build` | Build system or dependencies |
| `ci` | CI/CD pipeline changes |
| `chore` | Maintenance tasks |
| `revert` | Revert previous commit |
| `security` | Security vulnerability fix |

### Subject Line Rules

1. **Length**: ≤72 characters (50 ideal)
2. **Tense**: Imperative mood ("Add feature" not "Added feature")
3. **Capitalization**: First letter capitalized
4. **No period**: Don't end with a period

## Detailed Guidelines

For complete standards, see:
- [Conventional Commits Guide](./conventional-commits.md)
- [Language Options](./language-options.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/commit-message.ai.yaml`
- Language options:
  - English: `ai/options/commit-message/english.ai.yaml`
  - Traditional Chinese: `ai/options/commit-message/traditional-chinese.ai.yaml`
  - Bilingual: `ai/options/commit-message/bilingual.ai.yaml`

## Examples

### ✅ Good Examples

```
feat(auth): Add OAuth2 Google login support
fix(api): Resolve memory leak in user session cache
refactor(database): Extract query builder to separate class
docs(readme): Update installation instructions for Node 20
```

### ❌ Bad Examples

```
fixed bug                    # Too vague, no scope
feat(auth): added google login  # Past tense
Update stuff.                # Period, vague
WIP                          # Not descriptive
```

## Body Guidelines

Use the body to explain **WHY** the change was made:

```
fix(api): Resolve race condition in concurrent user updates

Why this occurred:
- Two simultaneous PUT requests could overwrite each other
- No optimistic locking implemented

What this fix does:
- Add version field to User model
- Return 409 Conflict if version mismatch

Fixes #789
```

## Breaking Changes

Always document breaking changes in footer:

```
feat(api): Change user endpoint response format

BREAKING CHANGE: User API response format changed

Migration guide:
1. Update API clients to remove .data wrapper
2. Use created_at instead of createdAt
```

## Issue References

```
Closes #123    # Automatically closes issue
Fixes #456     # Automatically closes issue
Refs #789      # Links without closing
```

---

## Language Selection Decision (YAML Compressed)

```yaml
# === LANGUAGE DECISION MATRIX ===
decision_tree:
  - q: "Open source project?"
    y: "→ English (international contributors)"
    n: next
  - q: "International/distributed team?"
    y: "→ English (common language)"
    n: next
  - q: "Single-language team?"
    y: "→ Team's primary language OR English"
    n: "→ Bilingual (subject:EN, body:local)"

recommendation_matrix:
  open_source: {lang: English, reason: "international contributors"}
  international_team: {lang: English, reason: "common language"}
  local_team_EN: {lang: English, reason: "tool compatibility, career mobility"}
  local_team_ZH: {lang: "繁體中文", reason: "clarity, team preference"}
  mixed: {lang: Bilingual, reason: "best of both worlds"}

# === TOOL COMPATIBILITY ===
tool_support:
  full_unicode:
    - GitHub/GitLab/Bitbucket
    - VS Code/JetBrains
    - SourceTree/GitKraken
  potential_issues:
    - "Some CI/CD log viewers"
    - "Legacy terminal encodings"
    - "Email notifications (rare)"

# === FORMAT BY LANGUAGE ===
english:
  types: [feat, fix, refactor, docs, style, test, perf, build, ci, chore, revert, security]
  example: "feat(auth): add OAuth2 Google login support"

traditional_chinese:
  types: [功能, 修復, 重構, 文件, 樣式, 測試, 效能, 建置, CI, 雜項, 回退, 安全]
  example: "功能(認證): 新增 OAuth2 Google 登入支援"

bilingual:
  format: "type(scope): English subject\n\n中文詳細說明"
  example: |
    feat(auth): add OAuth2 Google login

    新增 Google OAuth2 登入功能
    - 實作授權流程
    - 處理 token 交換
```

---

## Configuration Detection

This skill supports project-specific language configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Commit Message Language" section
2. If found, use the specified option (English / Traditional Chinese / Bilingual)
3. If not found, **default to English** for maximum tool compatibility

### First-Time Setup

If no configuration found and context is unclear:

1. Ask the user: "This project hasn't configured commit message language preference. Which option would you like to use? (English / 中文 / Bilingual)"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Commit Message Language

This project uses **[chosen option]** commit types.
<!-- Options: English | Traditional Chinese | Bilingual -->
```

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Commit Message Language

This project uses **English** commit types.

### Allowed Types
feat, fix, refactor, docs, style, test, perf, build, ci, chore, revert, security
```

---

## Related Standards

- [Commit Message Guide](../../core/commit-message-guide.md)
- [Git Workflow](../../core/git-workflow.md)
- [Changelog Standards](../../core/changelog-standards.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
