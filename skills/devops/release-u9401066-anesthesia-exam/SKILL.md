---
name: release
description: 完整的版本發布準備流程，包含版本號更新、CHANGELOG 生成、文檔同步和部署檢查。
---

---
name: release
description: Version release preparation workflow including changelog, version bump, and deployment checks. Triggers: REL, release, 發布, 版本發布, deploy, 部署, publish, 上線, ship, tag, 打標籤, 版本, version bump, 升版.
version: 1.0.0
category: workflow
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
orchestrates:
  - changelog-updater
  - readme-updater
  - roadmap-updater
  - test-generator
  - security-reviewer
  - memory-updater
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - grep_search
  - run_in_terminal
  - get_changed_files
---

# 版本發布工作流

## 描述

完整的版本發布準備流程，包含版本號更新、CHANGELOG 生成、文檔同步和部署檢查。

## 觸發條件

- 「準備發布」「release」「發布版本」
- 「REL: v1.2.0」

---

## 📦 發布流程

```
┌─────────────────────────────────────────────────────────────┐
│                   Release Workflow                           │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: 🔍 發布檢查 (Pre-release Check)                    │
│  ├─ 確認所有測試通過                                         │
│  ├─ 執行安全掃描                                             │
│  ├─ 檢查待處理問題                                           │
│  └─ 確認 main/master 分支狀態                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 🔢 版本決定 (Version Decision)                     │
│  ├─ 分析變更類型 (MAJOR/MINOR/PATCH)                        │
│  ├─ 確認版本號                                               │
│  └─ 更新版本檔案                                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 📝 文檔更新 (Documentation)                        │
│  ├─ [changelog-updater] 更新 CHANGELOG                      │
│  ├─ [readme-updater] 更新 README                            │
│  ├─ [roadmap-updater] 標記完成項目                          │
│  └─ 更新 API 文檔（如有）                                    │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 🏷️ 標籤準備 (Tagging)                             │
│  ├─ 建立 Git tag                                            │
│  ├─ 準備 release notes                                      │
│  └─ 確認變更摘要                                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: 🚀 發布 (Publish)                                  │
│  ├─ 推送 tag                                                │
│  ├─ 建立 GitHub Release                                     │
│  └─ 觸發 CI/CD pipeline                                     │
├─────────────────────────────────────────────────────────────┤
│  Phase 6: 📢 發布後 (Post-release)                           │
│  ├─ 更新 Memory Bank                                        │
│  ├─ 通知相關人員                                             │
│  └─ 準備下一版本                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔢 版本號規則 (SemVer)

```
MAJOR.MINOR.PATCH

MAJOR: 不相容的 API 變更 (Breaking Changes)
MINOR: 向下相容的新功能 (New Features)
PATCH: 向下相容的 Bug 修復 (Bug Fixes)
```

### 版本號決定指南

| 變更類型 | 版本 | 範例 |
|----------|------|------|
| Breaking API 變更 | MAJOR | 1.0.0 → 2.0.0 |
| 新功能（不破壞現有） | MINOR | 1.0.0 → 1.1.0 |
| Bug 修復 | PATCH | 1.0.0 → 1.0.1 |
| 安全修復 | PATCH | 1.0.0 → 1.0.1 |
| 文檔更新 | PATCH | 1.0.0 → 1.0.1 |
| 效能改善 | MINOR/PATCH | 視影響範圍 |

---

## 🚀 使用範例

### 基本用法

```
「準備發布」

AI 執行：
1. 🔍 執行發布前檢查
2. 🔢 分析變更，建議版本號
3. 📝 更新 CHANGELOG、README、ROADMAP
4. 🏷️ 準備 Git tag
5. 📊 生成發布清單
```

### 指定版本

```
「REL: v2.0.0」

AI 執行：
1. 確認這是 MAJOR 版本（Breaking Changes）
2. 要求確認 breaking changes 清單
3. 執行完整發布流程
```

---

## 📊 輸出格式

```markdown
## 📦 發布準備報告

### 版本資訊

- **當前版本**: 1.1.0
- **建議版本**: 1.2.0 (MINOR)
- **原因**: 新增 3 個功能，無 breaking changes

### 🔍 發布檢查

| 檢查項目 | 狀態 |
|----------|------|
| 測試通過 | ✅ 42/42 |
| 安全掃描 | ✅ 無風險 |
| Lint | ✅ 0 errors |
| 文檔同步 | ✅ 已更新 |

### 📝 變更摘要

#### Added
- 用戶認證模組
- API 限流功能
- 匯出功能

#### Fixed
- 登入超時問題
- 資料同步錯誤

#### Changed
- 改進錯誤訊息

### 📁 更新的文件

- ✅ CHANGELOG.md - 新增 v1.2.0 區塊
- ✅ README.md - 更新功能列表
- ✅ ROADMAP.md - 標記 3 個完成項目
- ✅ pyproject.toml - 版本號更新

### 🏷️ Git 指令

```bash
git add -A
git commit -m "chore: release v1.2.0"
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags
```

### 📋 Release Notes

```markdown
## v1.2.0 (2026-01-15)

### ✨ New Features
- 用戶認證模組
- API 限流功能
- 匯出功能

### 🐛 Bug Fixes
- 修復登入超時問題
- 修復資料同步錯誤

### 📖 Documentation
- 更新 API 文檔
- 新增使用範例
```

### 下一步

1. 確認變更摘要無誤
2. 執行上述 Git 指令
3. 在 GitHub 建立 Release
```

---

## ⚙️ 配置選項

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--dry-run` | 只預覽不執行 | false |
| `--skip-tests` | 跳過測試 | false |
| `--prerelease` | 預發布 (alpha/beta/rc) | false |
| `--force` | 強制指定版本 | false |
