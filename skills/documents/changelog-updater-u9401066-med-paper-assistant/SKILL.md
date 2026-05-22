---
name: changelog-updater
description: 更新 CHANGELOG.md。觸發：changelog、變更、版本、發布、改了什麼。
---

# CHANGELOG 更新技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 更新 changelog、紀錄變更 | ✅ |
| 發布、新版本 | ✅ |
| 被 git-precommit 調用 | ✅ 自動觸發 |

---

## 可用工具

此技能使用標準檔案操作：

| 操作 | 工具 |
|------|------|
| 讀取 | `read_file("CHANGELOG.md")` |
| 更新 | `replace_string_in_file()` |
| Git diff | `get_changed_files()` |

---

## 格式規範

遵循 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
# Changelog

## [Unreleased]

### Added
- 新增功能

### Changed
- 變更功能

### Fixed
- 修復問題

## [1.0.0] - 2025-12-22

### Added
- 初始版本
```

---

## 分類規則

| 類型 | 關鍵字 | 說明 |
|------|--------|------|
| Added | feat, 新增, add | 新功能 |
| Changed | change, update, 變更 | 修改現有功能 |
| Deprecated | deprecate, 棄用 | 即將移除的功能 |
| Removed | remove, delete, 移除 | 已移除的功能 |
| Fixed | fix, bug, 修復 | Bug 修復 |
| Security | security, 安全 | 安全性更新 |

---

## 版本號規則 (SemVer)

```
MAJOR.MINOR.PATCH

MAJOR: Breaking Changes（不向下相容）
MINOR: 新功能（向下相容）
PATCH: Bug 修復
```

---

## 標準工作流程

```python
# 1. 讀取現有 CHANGELOG
read_file("CHANGELOG.md")

# 2. 分析 Git diff
get_changed_files()

# 3. 分類變更
# - 新檔案 → Added
# - 修改檔案 → Changed/Fixed
# - 刪除檔案 → Removed

# 4. 更新 [Unreleased] 區塊
replace_string_in_file(
    filePath="CHANGELOG.md",
    oldString="## [Unreleased]\n",
    newString="## [Unreleased]\n\n### Added\n- 新增用戶認證模組\n"
)
```

---

## 輸出範例

```
📋 CHANGELOG 更新

偵測到的變更：
  - [Added] 新增用戶認證模組
  - [Fixed] 修復登入問題

建議版本：0.2.0 (MINOR - 新功能)
```

---

## 相關技能

- `git-precommit` - 提交前自動調用
- `roadmap-updater` - 同步里程碑狀態
