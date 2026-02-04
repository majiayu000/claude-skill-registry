---
name: memory-checkpoint
description: Externalize detailed memory to Memory Bank before conversation summarization to prevent context loss. Triggers: CP, checkpoint, save, 存檔, 記一下, 保存, sync memory, dump, 先記著, 備份, backup, snapshot, 快照, 記錄, 等等, 先停, pause, 離開前, before leaving, 收工.
version: 2.1.0
category: memory
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - memory-updater
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - memory
  - get_changed_files
---

# Memory Checkpoint 技能 (記憶檢查點)

## 描述
在對話被 Summarize 壓縮前，主動將詳細記憶外部化到 Memory Bank，避免重要上下文遺失。

## 觸發條件
- 「記憶檢查點」、「checkpoint」、「存檔」
- 「保存記憶」、「外部化記憶」
- 「sync memory」、「dump context」
- 對話較長時主動觸發（建議每 10-15 輪對話或重大進展後）

---

## ⚠️ 為什麼需要這個 Skill？

當對話過長時，系統會自動 Summarize（摘要）對話歷史，可能導致：
- 詳細的程式碼變更記錄被省略
- 決策背後的討論脈絡遺失
- 檔案路徑和具體實作細節模糊化
- 需要花時間重建上下文

**解決方案**：在被 Summarize 前，主動將關鍵記憶寫入 `memory-bank/` 目錄。

---

## 📋 Checkpoint 內容

### 1️⃣ activeContext.md - 當前工作焦點
```markdown
## 當前工作焦點
<!-- 當前正在做什麼 -->

## 進行中的變更
<!-- 具體的檔案和修改 -->

## 待處理事項
<!-- 下一步要做什麼 -->

## 關鍵決策
<!-- 本次對話做的重要決定 -->

## 相關檔案
<!-- 涉及的檔案路徑列表 -->
```

### 2️⃣ progress.md - 進度追蹤
```markdown
## Done (已完成)
- [x] 具體完成的事項（含檔案路徑）

## Doing (進行中)
- [ ] 正在進行的工作

## Next (下一步)
- [ ] 計劃要做的事項
```

### 3️⃣ decisionLog.md - 決策日誌
```markdown
## YYYY-MM-DD

### 決策：[決策標題]
- **背景**：為什麼需要這個決定
- **選項**：考慮過的方案
- **決定**：最終選擇
- **原因**：選擇的理由
```

### 4️⃣ architect.md - 架構記錄（如有變更）
```markdown
## 架構變更記錄

### YYYY-MM-DD: [變更標題]
- **變更內容**：
- **影響範圍**：
- **相關檔案**：
```

---

## 🚀 Checkpoint 執行步驟

### 自動執行（推薦）

當偵測到以下情況，AI 應主動執行 Checkpoint：

1. **對話長度指標**
   - 對話超過 10 輪
   - 累積修改超過 5 個檔案
   - 完成一個重要功能/修復

2. **工作階段轉換**
   - 從設計階段轉到實作
   - 完成一個 PR 或 Commit
   - 切換到不同的功能區塊

3. **明確指標**
   - 使用者說「先記一下」、「checkpoint」
   - 使用者說「等等繼續」、「我先去忙」

### 手動執行

使用者可隨時說：
- 「記憶檢查點」
- 「同步 memory bank」
- 「存檔目前進度」

---

## 📝 Checkpoint 範本

### Quick Checkpoint（快速檢查點）

更新 `activeContext.md`：
```markdown
# Active Context

> Last checkpoint: 2024-XX-XX HH:MM

## 🎯 當前焦點
[一句話描述當前在做什麼]

## 📝 本次對話摘要
1. [做了什麼 1]
2. [做了什麼 2]
3. [做了什麼 3]

## 📁 變更的檔案
- `path/to/file1.py` - [變更摘要]
- `path/to/file2.ts` - [變更摘要]

## ⚠️ 待解決
- [ ] 問題 1
- [ ] 問題 2

## 💡 重要決定
- 決定 A：[原因]
- 決定 B：[原因]

## 🔜 下一步
1. [下一步 1]
2. [下一步 2]
```

### Full Checkpoint（完整檢查點）

更新所有相關 Memory Bank 檔案：

```
memory-bank/
├── activeContext.md  ← 當前焦點 + 變更檔案
├── progress.md       ← Done/Doing/Next
├── decisionLog.md    ← 新決策（如有）
├── architect.md      ← 架構變更（如有）
├── productContext.md ← 技術棧變更（如有）
└── systemPatterns.md ← 新模式/慣例（如有）
```

---

## 🔄 與其他 Skills 整合

### 搭配 git-precommit
```
git commit 前 → 觸發 memory-checkpoint → 同步 Memory Bank → commit
```

### 搭配 memory-updater
```
memory-checkpoint = 批次更新
memory-updater = 增量更新
```

---

## 💬 對話範例

### 使用者觸發
```
User: checkpoint

AI: 📸 執行記憶檢查點...

已更新 Memory Bank：
- ✅ activeContext.md - 記錄當前焦點與 5 個變更檔案
- ✅ progress.md - 新增 3 個已完成項目
- ✅ decisionLog.md - 記錄 2 個決策

下次對話可從此處繼續，即使被 Summarize 也不會遺失關鍵資訊。
```

### AI 主動觸發
```
AI: 💡 偵測到對話較長且有多項進展，建議執行記憶檢查點。
    是否要我同步 Memory Bank？

User: 好

AI: 📸 執行記憶檢查點...
    [更新 Memory Bank]
```

---

## ⚙️ 配置選項

在 `.vscode/settings.json` 中可配置：

```json
{
  "claude.skills.memoryCheckpoint": {
    "autoTrigger": true,
    "triggerThreshold": {
      "conversationTurns": 10,
      "filesModified": 5
    },
    "includeFiles": [
      "activeContext.md",
      "progress.md",
      "decisionLog.md"
    ]
  }
}
```

---

## 📊 Checkpoint 品質檢查

好的 Checkpoint 應包含：

| 項目 | 必須 | 說明 |
|------|:----:|------|
| 當前焦點 | ✅ | 一句話描述正在做什麼 |
| 變更檔案列表 | ✅ | 完整路徑 + 簡述 |
| 待解決事項 | ✅ | 還沒完成的工作 |
| 重要決策 | ⚪ | 如有新決策 |
| 下一步 | ✅ | 接下來要做什麼 |
| 時間戳記 | ✅ | 知道這是什麼時候的狀態 |

---

## 🛠️ 實作提示

### 對 AI 的指示

在 `CLAUDE.md` 或 `AGENTS.md` 中加入：

```markdown
## Memory Checkpoint 規則

1. **主動觸發時機**
   - 對話超過 10 輪時，主動建議 checkpoint
   - 完成重大功能後，主動執行 checkpoint
   - 使用者說要離開時，主動執行 checkpoint

2. **Checkpoint 內容**
   - 必須包含：具體檔案路徑、變更摘要、下一步
   - 避免：過於籠統的描述、遺漏重要細節

3. **格式要求**
   - 使用時間戳記
   - 檔案路徑使用相對路徑
   - 保持簡潔但完整
```
