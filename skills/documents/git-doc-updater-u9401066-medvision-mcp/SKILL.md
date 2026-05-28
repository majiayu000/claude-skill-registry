---
name: git-doc-updater
description: Auto-check and update key documentation before Git commits to keep docs in sync with code. Triggers: docs, 文檔, 更新文檔, sync docs, release, 發布, documentation, 同步文件, 文件檢查, doc check, 發布前, before release, 準備發布.
version: 2.1.0
category: documentation
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - readme-updater
  - changelog-updater
  - roadmap-updater
  - memory-updater
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - get_changed_files
  - list_dir
---

# Git 文檔自動更新技能

## 描述
在執行 Git commit 之前，自動檢查並更新專案的關鍵文檔，確保文檔與程式碼保持同步。

## 觸發條件
當用戶要求進行以下操作時啟用此技能：
- Git commit
- Git push
- 提交程式碼
- 準備發布

## 自動更新的文檔

### 1. README.md
- 更新專案描述（如有變更）
- 更新安裝/使用說明
- 更新功能列表
- 更新依賴項目

### 2. CHANGELOG.md
- 根據本次變更添加新條目
- 遵循 [Keep a Changelog](https://keepachangelog.com/) 格式
- 分類為：Added, Changed, Deprecated, Removed, Fixed, Security
- 包含日期和版本號（如適用）

### 3. ROADMAP.md
- 標記已完成的功能項目
- 更新進行中的項目狀態
- 調整優先順序（如需要）

### 4. ARCHITECTURE.md (ARCH)
- 更新架構圖和說明（如有結構性變更）
- 更新組件關係
- 更新技術決策記錄

### 5. Memory Bank 文件
更新 `memory-bank/` 目錄下的相關文件：
- `activeContext.md` - 當前工作焦點
- `progress.md` - 進度追蹤（Done/Doing/Next）
- `decisionLog.md` - 記錄重要決策
- `productContext.md` - 專案上下文（如有變更）

## 執行流程

```
1. 分析本次程式碼變更內容
2. 識別哪些文檔需要更新
3. 依序更新各文檔
4. 顯示更新摘要供用戶確認
5. 將文檔變更加入 Git staging
```

## 更新原則

- **最小變更**：只更新與本次提交相關的內容
- **保持一致性**：維持現有文檔格式和風格
- **自動摘要**：從 commit 內容推斷變更摘要
- **版本控制**：CHANGELOG 使用語義化版本

## 範例輸出

當用戶說「準備 commit」時：

```
📝 文檔更新檢查：

✅ README.md - 無需更新
✅ CHANGELOG.md - 已添加 v1.2.0 條目
✅ ROADMAP.md - 已標記「用戶認證」為完成
⏭️ ARCHITECTURE.md - 無結構性變更，跳過
✅ memory-bank/progress.md - 已更新進度

準備提交以下文件變更...
```

## 自定義選項

用戶可以透過提示指定：
- `--skip-readme` 跳過 README 更新
- `--skip-changelog` 跳過 CHANGELOG 更新
- `--skip-memory` 跳過 Memory Bank 更新
- `--dry-run` 只顯示將要更新的內容，不實際修改
