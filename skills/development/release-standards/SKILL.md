---
source: skills/claude-code/release-standards/SKILL.md
source_version: 1.1.0
translation_version: 1.1.0
last_synced: 2026-01-02
status: current
name: release-standards
description: |
  語意化版本控制和變更日誌格式化的軟體發布標準。
  使用時機：準備發布、更新版本號、撰寫變更日誌。
  關鍵字：version, release, changelog, semver, major, minor, patch, 版本, 發布, 變更日誌。
---

# 發布標準

> **語言**: [English](../../../../../skills/claude-code/release-standards/SKILL.md) | 繁體中文

**版本**: 1.1.0
**最後更新**: 2026-01-02
**適用範圍**: Claude Code Skills

---

## 目的

本技能提供語意化版本控制和變更日誌格式化標準。

## 快速參考

### 語意化版本格式

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
2.3.1
1.0.0-alpha.1
3.2.0-beta.2+20250112
```

### 版本遞增規則

| 組成部分 | 何時遞增 | 範例 |
|-----------|-------------------|----------|
| **MAJOR** | 重大變更 | 1.9.5 → 2.0.0 |
| **MINOR** | 新功能（向後相容） | 2.3.5 → 2.4.0 |
| **PATCH** | 錯誤修復（向後相容） | 3.1.2 → 3.1.3 |

### 預發布識別符

| 識別符 | 穩定性 | 目標受眾 |
|------------|-----------|----------|
| `alpha` | 不穩定 | 內部團隊 |
| `beta` | 大致穩定 | 早期採用者 |
| `rc` | 穩定 | Beta 測試者 |

### CHANGELOG 分類

| 分類 | 用途 |
|----------|-------|
| **Added** | 新功能 |
| **Changed** | 現有功能的變更 |
| **Deprecated** | 即將移除的功能 |
| **Removed** | 已移除的功能 |
| **Fixed** | 錯誤修復 |
| **Security** | 安全性漏洞修復 |

## 詳細指南

完整標準請參閱：
- [語意化版本控制指南](./semantic-versioning.md)
- [變更日誌格式](./changelog-format.md)
- [發布流程指南](./release-workflow.md) - 本專案完整發布流程

## CHANGELOG 條目格式

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- Add user dashboard with customizable widgets (#123)

### Changed
- **BREAKING**: Change API response format from XML to JSON

### Fixed
- Fix memory leak when processing large files (#456)

### Security
- Fix SQL injection vulnerability (CVE-2025-12345)
```

## 重大變更

使用 **BREAKING** 前綴標記重大變更：

```markdown
### Changed
- **BREAKING**: Remove deprecated `getUserById()`, use `getUser()` instead
```

## Git 標籤

```bash
# Create annotated tag (recommended)
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag to remote
git push origin v1.2.0
```

## 版本排序

```
1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0
```

---

## 配置檢測

本技能支援專案特定配置。

### 檢測順序

1. 檢查 `CONTRIBUTING.md` 中的「Disabled Skills」段落
   - 如果列出此技能，則該專案停用此技能
2. 檢查 `CONTRIBUTING.md` 中的「Release Standards」段落
3. 如果未找到，**預設使用語意化版本控制和 Keep a Changelog 格式**

### 首次設定

如果未找到配置且上下文不明確：

1. 詢問使用者：「此專案尚未配置發布標準。您想使用語意化版本控制嗎？」
2. 使用者選擇後，建議在 `CONTRIBUTING.md` 中記錄：

```markdown
## Release Standards

### Versioning
This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH).

### Changelog
This project follows **Keep a Changelog** format.
```

### 配置範例

在專案的 `CONTRIBUTING.md` 中：

```markdown
## Release Standards

### Versioning
This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH).

### Changelog
This project follows **Keep a Changelog** format.

### Release Process
1. Update version in package.json
2. Update CHANGELOG.md
3. Create git tag with `v` prefix (e.g., v1.2.0)
4. Push tag to trigger release workflow
```

---

## 相關標準

- [版本控制](../../core/versioning.md)
- [變更日誌標準](../../core/changelog-standards.md)
- [Git 工作流程](../../core/git-workflow.md)

---

## 版本歷史

| 版本 | 日期 | 變更內容 |
|---------|------|---------|
| 1.1.0 | 2026-01-02 | 新增：發布流程指南，包含完整發布流程 |
| 1.0.0 | 2025-12-24 | 新增：標準段落（目的、相關標準、版本歷史、授權條款） |

---

## 授權條款

本技能依據 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權發布。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
