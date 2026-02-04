---
name: memory-updater
description: Update and maintain Memory Bank files (activeContext, progress, decisionLog). Triggers: MB, memory, 記憶, 進度, 更新記憶, update memory, 記錄進度, 更新上下文, sync, 同步, 記下來, note, 筆記, context, 脈絡, 追蹤, track, 狀態, status.
version: 2.2.0
category: memory
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
  - memory
---

# Memory Bank 更新技能

## 描述

維護和更新專案的 Memory Bank 記憶系統，確保專案狀態在對話間持久化。

## 觸發條件

- 「更新 memory bank」「MB」「記錄進度」
- 「更新上下文」「sync」「同步」
- 工作階段結束時
- 完成重要任務後

---

## 📁 Memory Bank 檔案結構

```
memory-bank/
├── activeContext.md   # 當前工作焦點（最常更新）
├── progress.md        # 進度追蹤 Done/Doing/Next
├── decisionLog.md     # 重要決策記錄
├── architect.md       # 架構文檔
├── productContext.md  # 專案上下文
├── projectBrief.md    # 專案簡介
└── systemPatterns.md  # 系統模式
```

---

## 🔧 操作步驟

### Step 1: 讀取現有內容

使用 `read_file` 工具讀取要更新的檔案：

```
read_file("memory-bank/activeContext.md")
read_file("memory-bank/progress.md")
```

### Step 2: 判斷更新類型

| 情況 | 更新檔案 | 更新方式 |
|------|----------|----------|
| 開始新任務 | activeContext.md, progress.md | 新增 Doing |
| 完成任務 | progress.md | Doing → Done |
| 做出決策 | decisionLog.md | 新增條目 |
| 架構變更 | architect.md | 更新相關區塊 |

### Step 3: 執行更新

使用 `replace_string_in_file` 進行精確更新（推薦）：

```
replace_string_in_file(
  filePath="memory-bank/progress.md",
  oldString="## Doing\n\n- [ ] 任務 A",
  newString="## Doing\n\n- [ ] 任務 A\n- [ ] 新任務 B"
)
```

或使用 `write_file` 完整覆寫（適合大幅修改）。

---

## 📝 檔案格式規範

### activeContext.md

```markdown
# Active Context

> Last updated: 2026-01-15

## 🎯 當前焦點

[一句話描述正在處理的主要任務]

## 📁 相關檔案

- `path/to/file1.py` - [用途說明]
- `path/to/file2.ts` - [用途說明]

## ⚠️ 待解決問題

- [ ] 問題 1
- [ ] 問題 2

## 💡 備註

[其他需要記住的事項]
```

### progress.md

```markdown
# Progress

## Done ✅

- [x] 已完成任務 1 (2026-01-15)
- [x] 已完成任務 2 (2026-01-14)

## Doing 🚧

- [ ] 進行中任務 1
- [ ] 進行中任務 2

## Next 📋

- [ ] 計劃任務 1
- [ ] 計劃任務 2
```

### decisionLog.md

```markdown
# Decision Log

## 2026-01-15

### 決策：選擇 React 作為前端框架

- **背景**：需要選擇前端框架
- **選項**：React, Vue, Svelte
- **決定**：React
- **原因**：團隊熟悉度高，生態系完整

---

## 2026-01-14

### 決策：...
```

---

## ⚡ 更新原則

### 1. 增量更新

```
✅ 正確：只修改相關區塊
❌ 錯誤：每次都覆寫整個檔案
```

### 2. 保持簡潔

```
✅ 正確：「完成用戶認證模組」
❌ 錯誤：「今天我們完成了用戶認證模組的開發工作，包括...」
```

### 3. 時間標記

```
✅ 正確：- [x] 完成功能 A (2026-01-15)
❌ 錯誤：- [x] 完成功能 A
```

### 4. 檔案路徑完整

```
✅ 正確：`src/domain/entities/User.py`
❌ 錯誤：`User.py`
```

---

## 🔄 與其他 Skills 整合

| Skill | 整合方式 |
|-------|----------|
| `memory-checkpoint` | checkpoint 後呼叫 updater 寫入 |
| `git-precommit` | commit 前強制更新 progress.md |
| `feature-development` | 功能完成後更新 Done |

---

## 📊 輸出格式

執行完成後回報：

```
📝 Memory Bank 已更新

更新內容：
- ✅ activeContext.md - 更新當前焦點
- ✅ progress.md - 新增 1 個 Done 項目
- ⏭️ decisionLog.md - 無變更

下次記得：完成重要任務後執行「更新 memory bank」
```
