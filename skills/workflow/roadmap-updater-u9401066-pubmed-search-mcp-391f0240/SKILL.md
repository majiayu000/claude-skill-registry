---
name: roadmap-updater
description: Auto-update ROADMAP.md status based on completed features. Triggers: RM, roadmap, 路線, 規劃, 完成功能, milestone, 里程碑.
---

# ROADMAP 更新技能

## 描述
根據完成的功能自動更新 ROADMAP.md。

## 觸發條件
- 「更新 roadmap」
- 被 git-precommit 編排器調用
- 完成規劃中的功能後

## 功能

### 1. 狀態標記
```
📋 計劃中 → 🚧 進行中 → ✅ 已完成
```

### 2. 自動偵測
分析 commit 內容，匹配 ROADMAP 中的項目

### 3. 建議新增
如果完成了 ROADMAP 未列出的功能，建議添加

## 輸出格式

```
🗺️ ROADMAP 更新

匹配到的項目：
  ✅ 用戶認證 → 標記為已完成
  🚧 API 文檔 → 保持進行中

建議新增：
  - 新增「密碼重設」到已完成

預覽：
## 已完成 ✅
+ - [x] 用戶認證 (2025-12-15)
```
