---
name: readme-updater
description: Intelligently update README.md to sync with code changes. Triggers: readme, 說明, 更新說明, update readme, 文檔同步.
---

# README 更新技能

## 描述
智能更新 README.md，保持與程式碼同步。

## 觸發條件
- 「更新 README」
- 被 git-precommit 編排器調用
- 新增重要功能後

## 法規依據
- 憲法：CONSTITUTION.md 第 6 條

## 更新策略

### 1. 偵測變更類型
- 新功能 → 更新功能列表
- 新依賴 → 更新安裝說明
- API 變更 → 更新使用範例
- 結構變更 → 更新專案結構

### 2. 更新區塊

| 區塊 | 條件 |
|------|------|
| 功能列表 | 新增/移除功能 |
| 安裝說明 | 依賴變更 |
| 使用範例 | API 變更 |
| 專案結構 | 目錄結構變更 |
| 配置說明 | 新增設定選項 |

### 3. 保持區塊
以下區塊不自動修改：
- 授權資訊
- 貢獻指南
- 致謝

## 輸出格式

```
📝 README 更新分析

變更偵測：
  ✅ 新增功能：用戶認證模組
  ✅ 新增依賴：bcrypt

建議更新：
  [功能列表] 新增「🔐 用戶認證」
  [安裝說明] 新增 bcrypt 安裝指令

預覽：
  ## 功能
  - 🤖 Claude Skills
  - 📝 Memory Bank
+ - 🔐 用戶認證（新增）
```
