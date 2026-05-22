---
name: readme-updater
description: 更新 README.md。觸發：readme、說明、文檔、怎麼用、安裝說明。
---

# README 更新技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 更新 README、文檔 | ✅ |
| 怎麼用、安裝說明 | ✅ |
| 被 git-precommit 調用 | ✅ 自動觸發 |

---

## 可用工具

此技能使用標準檔案操作：

| 操作 | 工具 |
|------|------|
| 讀取 | `read_file("README.md")` |
| 更新 | `replace_string_in_file()` |
| 目錄列表 | `list_dir()` |
| Git diff | `get_changed_files()` |

---

## 更新區塊對應

| 變更類型 | 更新區塊 |
|----------|----------|
| 新功能 | 功能列表 |
| 新依賴 | 安裝說明 |
| API 變更 | 使用範例 |
| 目錄變更 | 專案結構 |
| 新設定 | 配置說明 |

---

## 保護區塊（不自動修改）

- 授權資訊
- 貢獻指南
- 致謝

---

## 標準工作流程

```python
# 1. 讀取 README
read_file("README.md")

# 2. 分析變更
get_changed_files()

# 3. 更新對應區塊
replace_string_in_file(
    filePath="README.md",
    oldString="## Features\n\n- Feature A",
    newString="## Features\n\n- Feature A\n- Feature B (新增)"
)
```

---

## 輸出範例

```
📝 README 更新分析

變更偵測：
  ✅ 新增功能：用戶認證模組
  ✅ 新增依賴：bcrypt

建議更新：
  [功能列表] 新增「🔐 用戶認證」
  [安裝說明] 新增 bcrypt 安裝指令
```

---

## 相關技能

- `readme-i18n` - 多語言 README 同步
- `git-precommit` - 提交前自動調用
