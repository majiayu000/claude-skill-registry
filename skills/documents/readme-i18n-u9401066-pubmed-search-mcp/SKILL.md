---
name: readme-i18n
description: Maintain multilingual README versions (English primary, Chinese translation). Triggers: i18n, 翻譯, translate, 多語言, sync readme, 中英文, bilingual.
---

# Skill: README 國際化 (i18n)

## 描述
維護 README 的多語言版本，確保中文與英文內容對照同步。

## 觸發條件
- 使用者說「更新 README」「sync readme」「翻譯 README」
- README.md 有變更時
- 新增功能需要更新文檔時

## 檔案結構
```
README.md          # 主 README（英文，Primary）
README.zh-TW.md    # 繁體中文版本（對照翻譯）
```

## 執行流程

### 1. 確認變更來源
```
如果使用者提供中文內容 → 同步到英文版
如果使用者提供英文內容 → 同步到中文版
如果主 README 變更 → 同步兩個版本
```

### 2. 主 README 格式
主 README.md 採用雙語並列格式：
- 使用語言切換連結在頂部
- 每個章節先中文後英文
- 或使用摺疊區塊分隔

### 3. 翻譯原則
- 技術術語保持一致（建立術語表）
- 程式碼範例不翻譯，只翻譯註解
- 保持 Markdown 結構完全對應
- 連結指向對應語言版本

### 4. 同步檢查
```markdown
## 同步檢查清單
- [ ] 章節數量一致
- [ ] 程式碼區塊一致
- [ ] 連結有效性
- [ ] 術語一致性
```

## 術語對照表

| 中文 | English |
|------|---------|
| 憲法 | Constitution |
| 子法 | Bylaws |
| 技能 | Skills |
| 記憶庫 | Memory Bank |
| 領域驅動設計 | Domain-Driven Design (DDD) |
| 資料存取層 | Data Access Layer (DAL) |
| 提交 | Commit |
| 工作流 | Workflow |
| 架構 | Architecture |
| 模組化 | Modular |
| 跨對話 | Cross-conversation |

## 輸出範本

### 主 README.md 頂部
```markdown
# Project Name / 專案名稱

[English](#english) | [繁體中文](#繁體中文)

---

## English

(English content here)

---

## 繁體中文

(中文內容在此)
```

### 或使用獨立檔案連結
```markdown
# Project Name

🌐 [English](README.en.md) | [繁體中文](README.zh-TW.md)

(預設語言內容)
```

## 相依 Skills
- `readme-updater` - 基礎 README 更新邏輯

## 注意事項
- 翻譯時保持語氣一致（專業但親切）
- 不要過度意譯，保持技術準確性
- Emoji 兩個版本保持一致
- 更新日期同步標記
