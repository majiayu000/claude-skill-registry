---
name: changelog
scope: partial
description: "[UDS] Generate and maintain CHANGELOG.md entries"
allowed-tools: Read, Write, Grep, Bash(git log:*)
disable-model-invocation: true
---

# Changelog Assistant | 變更日誌助手

Generate and maintain CHANGELOG.md entries following the Keep a Changelog format.

根據 Keep a Changelog 格式產生和維護 CHANGELOG.md 條目。

## Workflow | 工作流程

1. **Analyze git log** - Read commit history since last release using `git log`
2. **Categorize changes** - Map commits to changelog categories
3. **Generate entries** - Write user-friendly descriptions for each change
4. **Update CHANGELOG.md** - Insert entries into the [Unreleased] or versioned section

## Change Categories | 變更分類

| Category | When to Use | 使用時機 | Commit Types |
|----------|-------------|---------|-------------|
| **Added** | New features | 新功能 | `feat` |
| **Changed** | Modifications to existing features | 修改既有功能 | `perf`, `BREAKING CHANGE` |
| **Deprecated** | Features to be removed | 即將移除的功能 | -- |
| **Removed** | Removed features | 已移除的功能 | `BREAKING CHANGE` |
| **Fixed** | Bug fixes | 錯誤修復 | `fix` |
| **Security** | Security patches | 安全性修補 | `security` |

## Entry Format | 條目格式

```markdown
## [Unreleased]

### Added
- Add user dashboard with customizable widgets (#123)

### Changed
- **BREAKING**: Change API response format from XML to JSON (#789)

### Fixed
- Fix memory leak when processing large files (#456)

### Security
- Fix SQL injection vulnerability in search endpoint (CVE-2025-12345)
```

### Writing Guidelines | 撰寫指南

- Write for **users**, not developers | 為使用者而非開發者撰寫
- Focus on **impact**, not implementation | 聚焦影響而非實作
- Include issue/PR references | 附上 issue/PR 編號
- Mark breaking changes with **BREAKING** prefix | 用 **BREAKING** 標記破壞性變更

## Usage | 使用方式

- `/changelog` - Analyze recent commits and generate changelog entries
- Also available via `/release changelog [version]`

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [changelog-standards.md](../../core/changelog-standards.md)
