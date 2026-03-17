---
name: memory-updater
description: Update and maintain Memory Bank files (activeContext, progress, decisionLog). Triggers: MB, memory, 記憶, 進度, 更新記憶, update memory, 記錄進度, 更新上下文.
---

# Memory Bank 更新技能

## 描述
維護和更新專案的 Memory Bank 記憶系統。

## 觸發條件
- 「更新 memory bank」
- 「記錄進度」
- 「更新上下文」
- 工作階段結束時

## 更新的檔案

### activeContext.md
當前工作焦點，包含：
- 正在處理的任務
- 相關檔案
- 待解決問題

### progress.md
進度追蹤：
- Done: 已完成項目
- Doing: 進行中
- Next: 下一步

### decisionLog.md
重要決策記錄：
- 決策內容
- 原因/理由
- 日期

## 更新原則

1. **增量更新**：只新增/修改相關內容
2. **保持簡潔**：避免冗餘描述
3. **時間標記**：重要項目加上日期
4. **關聯性**：標記相關檔案和決策
