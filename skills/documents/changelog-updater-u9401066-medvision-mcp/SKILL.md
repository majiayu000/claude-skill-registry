---
name: changelog-updater
description: Auto-update CHANGELOG.md following Keep a Changelog format. Triggers: CL, changelog, 變更, 版本, version, 更新日誌, whatsnew, release notes, 發布說明, 變更紀錄, history, 歷史, 更新紀錄, 新功能, new features, breaking changes.
version: 2.2.0
category: documentation
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies: []
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - get_changed_files
---

# CHANGELOG 更新技能

## 描述

根據變更內容自動更新 CHANGELOG.md，遵循 [Keep a Changelog](https://keepachangelog.com/) 格式。

## 觸發條件

- 「更新 changelog」「CL」「變更紀錄」
- 被 `git-precommit` 編排器調用
- 功能完成後需要記錄時

## 法規依據

- 憲法：CONSTITUTION.md 第 7 條
- 格式：Keep a Changelog 1.1.0

---

## 📁 CHANGELOG.md 標準格式

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- 待發布的新功能

## [1.2.0] - 2026-01-15

### Added
- 新增用戶認證模組 (#123)
- 新增密碼重設功能

### Changed
- 改進登入頁面 UI

### Fixed
- 修復登出後 session 未清除問題 (#456)

## [1.1.0] - 2026-01-01

### Added
- 初始版本功能
```

---

## 🔧 操作步驟

### Step 1: 讀取現有 CHANGELOG

```
read_file("CHANGELOG.md")
```

### Step 2: 取得變更資訊

從 `git-precommit` 調用時，分析變更內容：

```
get_changed_files()
```

或從使用者提供的變更描述判斷。

### Step 3: 分類變更

| 類型 | 使用時機 | 關鍵字偵測 |
| ---- | -------- | ---------- |
| Added | 新功能 | 新增, add, feat, create |
| Changed | 修改現有功能 | 變更, 修改, update, change, refactor |
| Deprecated | 即將移除的功能 | 棄用, deprecate |
| Removed | 已移除的功能 | 移除, 刪除, remove, delete |
| Fixed | Bug 修復 | 修復, fix, bug, resolve |
| Security | 安全性修復 | 安全, security, 漏洞, CVE |

### Step 4: 判斷版本號

依據 [Semantic Versioning](https://semver.org/)：

```
MAJOR.MINOR.PATCH

├── MAJOR: 不相容的 API 變更（Breaking Changes）
│   - 移除功能
│   - API 簽名變更
│   - 資料格式變更
│
├── MINOR: 新增功能（向下相容）
│   - 新增 API
│   - 新增功能模組
│   - 新增設定選項
│
└── PATCH: Bug 修復（向下相容）
    - 修復錯誤
    - 安全性修補
    - 文檔修正
```

### Step 5: 更新 CHANGELOG

**方式 A：新增到 Unreleased**（推薦用於開發中）

```
oldString: "## [Unreleased]\n\n### Added"
newString: "## [Unreleased]\n\n### Added\n- 新增功能描述"
```

**方式 B：發布新版本**（用於 release）

```
oldString: "## [Unreleased]\n\n### Added\n- 新功能"
newString: "## [Unreleased]\n\n## [1.2.0] - 2026-01-15\n\n### Added\n- 新功能"
```

---

## 📝 條目撰寫規範

### 好的寫法

```markdown
### Added
- 新增使用者認證模組，支援 OAuth2.0 (#123)
- 實作密碼強度檢查功能

### Fixed
- 修復登出後 session 未正確清除的問題 (#456)
```

### 不好的寫法

```markdown
### Added
- 做了一些事情
- fix bug
- update code
```

### 撰寫原則

1. **以使用者角度描述**：說明「做了什麼」而非「改了什麼程式碼」
2. **關聯 Issue/PR**：如有對應的 Issue，加上連結 `(#123)`
3. **一行一項**：每個變更獨立一行
4. **使用動詞開頭**：新增、修復、改進、移除

---

## 🔄 與其他 Skills 整合

| Skill | 整合方式 |
| ----- | -------- |
| `git-precommit` | 自動調用，分析 commit 內容 |
| `roadmap-updater` | 完成的功能可交叉參考 |
| `release` | 發布時從 Unreleased 建立新版本 |

---

## 📊 輸出格式

執行完成後回報：

```
📋 CHANGELOG 更新報告

偵測到的變更：
- [Added] 新增用戶認證模組
- [Fixed] 修復登入 session 問題

建議版本：1.2.0 (MINOR - 新增功能)

更新位置：
- ✅ CHANGELOG.md - 新增 2 個條目到 [Unreleased]

預覽：
## [Unreleased]

### Added
+ - 新增用戶認證模組 (#123)

### Fixed
+ - 修復登入 session 問題 (#456)
```

---

## ⚠️ 注意事項

1. **保持時序**：新版本在上，舊版本在下
2. **Unreleased 區塊**：總是保留，作為開發中變更的暫存區
3. **不要修改歷史版本**：已發布的版本內容不應修改（除非修正錯誤）
4. **Breaking Changes 要明確標示**：在 Changed 或獨立的 Breaking 區塊說明
