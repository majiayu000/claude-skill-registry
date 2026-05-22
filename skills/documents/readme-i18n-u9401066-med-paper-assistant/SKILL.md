---
name: readme-i18n
description: README 多語言同步。觸發：i18n、翻譯、多語言、sync readme。
---

# README 國際化 (i18n) 技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 翻譯 README、sync readme | ✅ |
| 多語言、i18n | ✅ |
| README 有變更時 | ✅ 自動觸發 |

---

## 可用工具

| 操作 | 工具 |
|------|------|
| 讀取 README | `read_file()` |
| 更新 README | `replace_string_in_file()` |
| 比對差異 | `get_changed_files()` |

---

## 檔案結構

```
README.md          # 主 README（英文，Primary）
README.zh-TW.md    # 繁體中文版本
```

---

## 同步方向

| 情況 | 動作 |
|------|------|
| 用戶提供中文 | 同步到英文版 |
| 用戶提供英文 | 同步到中文版 |
| README.md 變更 | 同步到 README.zh-TW.md |

---

## 標準工作流程

```python
# 1. 讀取兩個版本
en_content = read_file("README.md")
zh_content = read_file("README.zh-TW.md")

# 2. 比對章節差異
# - 檢查 ## 標題數量是否一致
# - 檢查程式碼區塊數量是否一致

# 3. 翻譯新增/變更的段落
# - 技術術語保持一致（見術語表）
# - 程式碼只翻譯註解

# 4. 更新對應版本
replace_string_in_file("README.zh-TW.md", old, new)
```

---

## 術語對照表

| English | 中文 |
|---------|------|
| Constitution | 憲法 |
| Bylaws | 子法 |
| Skills | 技能 |
| Memory Bank | 記憶庫 |
| Domain-Driven Design | 領域驅動設計 |
| Data Access Layer | 資料存取層 |
| Workflow | 工作流 |
| Architecture | 架構 |

---

## 翻譯原則

1. **技術術語一致** - 使用術語對照表
2. **程式碼不翻譯** - 只翻譯註解
3. **結構對應** - Markdown 結構完全對應
4. **Emoji 一致** - 兩個版本保持相同

---

## 同步檢查清單

```markdown
- [ ] 章節數量一致
- [ ] 程式碼區塊一致
- [ ] 連結有效性
- [ ] 術語一致性
```

---

## 輸出範例

```
🌐 README 國際化同步

變更來源: README.md
同步目標: README.zh-TW.md

變更內容:
  + ## New Feature → ## 新功能
  + Installation → 安裝

✅ 同步完成
```

---

## 相關技能

- `readme-updater` - 基礎 README 更新
