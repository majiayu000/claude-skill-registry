---
name: readme-updater
description: Intelligently update README.md to sync with code changes. Triggers: readme, 說明, 更新說明, update readme, 文檔同步, documentation, doc, 文件, 說明文件, 更新文檔, sync readme, 同步說明, 專案說明.
version: 2.2.0
category: documentation
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - readme-i18n
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - list_dir
  - get_changed_files
  - run_in_terminal
---

# README 更新技能

## 描述

智能更新 README.md，保持與程式碼變更同步。

## 觸發條件

- 「更新 README」「readme」「文檔同步」
- 被 `git-precommit` 編排器調用
- 新增重要功能後

## 法規依據

- 憲法：CONSTITUTION.md 第 6 條

---

## 📁 README.md 建議結構

```markdown
# 專案名稱

> 一句話描述

## ✨ 功能特色

- 🔥 功能 1
- 🚀 功能 2

## 📦 安裝

### 前置需求
- Node.js >= 18
- Python >= 3.11

### 安裝步驟
\`\`\`bash
npm install
\`\`\`

## 🚀 快速開始

\`\`\`bash
npm run dev
\`\`\`

## 📖 使用說明

### 基本用法
...

### 進階用法
...

## 📁 專案結構

\`\`\`
src/
├── domain/
├── application/
├── infrastructure/
└── presentation/
\`\`\`

## ⚙️ 設定

| 變數 | 說明 | 預設值 |
| ---- | ---- | ------ |
| PORT | 服務埠號 | 3000 |

## 🤝 貢獻

請參閱 CONTRIBUTING.md

## 📄 授權

MIT License
```

---

## 🔧 操作步驟

### Step 1: 讀取現有 README

```
read_file("README.md")
```

### Step 2: 分析變更內容

從 `git-precommit` 調用時：

```
get_changed_files()
```

或分析專案結構：

```
list_dir("src/")
```

### Step 3: 判斷需要更新的區塊

| 變更類型 | 更新區塊 | 偵測方式 |
| -------- | -------- | -------- |
| 新功能 | ✨ 功能特色 | 新增 feature 資料夾 |
| 新依賴 | 📦 安裝 | pyproject.toml/package.json 變更 |
| API 變更 | 📖 使用說明 | 公開 API 檔案變更 |
| 目錄變更 | 📁 專案結構 | 新增/移除主要資料夾 |
| 新設定 | ⚙️ 設定 | config 檔案變更 |

### Step 4: 執行更新

使用 `replace_string_in_file` 精確更新：

**新增功能到功能列表**：

```
oldString: "## ✨ 功能特色\n\n- 🔥 功能 1\n- 🚀 功能 2"
newString: "## ✨ 功能特色\n\n- 🔥 功能 1\n- 🚀 功能 2\n- 🔐 用戶認證（新）"
```

**更新專案結構**：

```
oldString: "## 📁 專案結構\n\n```\nsrc/\n├── domain/"
newString: "## 📁 專案結構\n\n```\nsrc/\n├── domain/\n│   └── entities/"
```

---

## 🛡️ 保護區塊

以下區塊**不應自動修改**（需人工確認）：

- 📄 授權資訊（License）
- 🤝 貢獻指南（Contributing）
- 🙏 致謝（Acknowledgments）
- 📜 免責聲明（Disclaimer）

---

## 🔄 與其他 Skills 整合

| Skill | 整合方式 |
| ----- | -------- |
| `git-precommit` | 自動調用，傳入變更資訊 |
| `readme-i18n` | 更新後同步多語言版本 |
| `changelog-updater` | 參考 CHANGELOG 新功能 |

---

## 📊 輸出格式

```
📝 README 更新報告

變更偵測：
- ✅ 新增功能：用戶認證模組
- ✅ 新增依賴：bcrypt

建議更新：
- [功能列表] 新增「🔐 用戶認證」
- [安裝說明] 新增 bcrypt 安裝指令

執行結果：
- ✅ README.md 已更新 (2 處變更)

📌 提醒：請檢查 readme-i18n 是否需要同步
```

---

## ⚠️ 注意事項

1. **保持格式一致**：使用 emoji 時要與現有風格一致
2. **不要移除內容**：只新增或更新，不主動刪除區塊
3. **程式碼範例驗證**：更新範例時確保語法正確
4. **多語言同步**：有 README.zh-TW.md 時需通知 readme-i18n
