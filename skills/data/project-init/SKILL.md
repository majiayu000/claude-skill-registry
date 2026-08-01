---
name: project-init
description: 將此專案作為模板，快速初始化新專案，完整繼承法規系統和 Skills 架構。
---

---
name: project-init
description: Initialize new projects using this template. Triggers: init, new, 新專案, 初始化, create project, 建立專案, bootstrap, scaffold project, setup, 設定, 起始, start, 從頭, from scratch, template, 模板, 範本, clone, fork.
version: 2.2.0
category: scaffold
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies: []
allowed-tools:
  - read_file
  - write_file
  - create_file
  - create_directory
  - list_dir
  - run_in_terminal
---

# 專案初始化技能

## 描述

將此專案作為模板，快速初始化新專案，完整繼承法規系統和 Skills 架構。

## 觸發條件

- 「初始化新專案」「init」「新專案」
- 「從模板建立專案」「template」
- 「create new project」「bootstrap」

---

## 🔧 操作步驟

### Step 1: 收集專案資訊

詢問使用者：

```markdown
請提供新專案資訊：

1. **專案名稱**：my-awesome-project
2. **專案描述**：一句話描述
3. **專案類型**：
   - [ ] Python 後端
   - [ ] Node.js 後端
   - [ ] React 前端
   - [ ] Vue 前端
   - [ ] 全端 (Monorepo)
4. **授權類型**：MIT / Apache-2.0 / GPL-3.0
5. **目標路徑**：~/projects/my-awesome-project
```

### Step 2: 建立目錄結構

```powershell
# 建立專案目錄
New-Item -ItemType Directory -Path "C:\projects\my-awesome-project" -Force

# 建立核心目錄
$dirs = @(
    ".github\bylaws",
    ".github\workflows",
    ".github\ISSUE_TEMPLATE",
    ".claude\skills",
    "memory-bank",
    "docs",
    "tests"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path "C:\projects\my-awesome-project\$dir" -Force
}
```

### Step 3: 複製法規系統

| 檔案/目錄 | 動作 | 說明 |
| --------- | ---- | ---- |
| CONSTITUTION.md | 複製 | 憲法 |
| .github/bylaws/*.md | 複製 | 所有子法 |
| .github/copilot-instructions.md | 複製並修改 | 更新專案名稱 |

### Step 4: 複製 Skills

```powershell
# 複製整個 skills 目錄
Copy-Item -Path "D:\template\.claude\skills\*" -Destination "C:\projects\my-awesome-project\.claude\skills" -Recurse
```

### Step 5: 初始化 Memory Bank

建立空的 Memory Bank 檔案：

```powershell
$memoryFiles = @(
    "activeContext.md",
    "progress.md",
    "decisionLog.md",
    "architect.md",
    "productContext.md",
    "projectBrief.md",
    "systemPatterns.md"
)

foreach ($file in $memoryFiles) {
    New-Item -ItemType File -Path "C:\projects\my-awesome-project\memory-bank\$file" -Force
}
```

**初始內容範例（activeContext.md）**：

```markdown
# Active Context

> Last updated: 2026-01-15

## 🎯 當前焦點

專案剛初始化，尚未開始開發。

## 📁 相關檔案

- 待新增

## ⚠️ 待解決問題

- [ ] 設定開發環境
- [ ] 定義領域模型
```

### Step 6: 初始化專案檔案

**README.md**：

```markdown
# {專案名稱}

> {專案描述}

## ✨ 功能特色

- 待新增

## 📦 安裝

\`\`\`bash
# 待補充
\`\`\`

## 🚀 快速開始

\`\`\`bash
# 待補充
\`\`\`

## 📄 授權

{授權類型} License
```

**CHANGELOG.md**：

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- 專案初始化
```

### Step 7: 初始化 Git

```powershell
cd "C:\projects\my-awesome-project"
git init
git add .
git commit -m "chore: 初始化專案 (使用 template-is-all-you-need)"
```

### Step 8: 依專案類型設定

#### Python 專案

```powershell
# 建立 pyproject.toml
Copy-Item "D:\template\pyproject.toml.template" "pyproject.toml"

# 建立虛擬環境
uv venv
uv sync --all-extras
```

#### Node.js 專案

```powershell
npm init -y
npm install --save-dev typescript @types/node
```

---

## 📁 複製內容對照表

| 來源 | 目標 | 動作 |
| ---- | ---- | ---- |
| CONSTITUTION.md | CONSTITUTION.md | 複製 |
| .github/bylaws/*.md | .github/bylaws/*.md | 複製 |
| .github/copilot-instructions.md | .github/copilot-instructions.md | 複製並編輯 |
| .claude/skills/* | .claude/skills/* | 複製 |
| memory-bank/*.md | memory-bank/*.md | 建立空檔 |
| README.md | README.md | 重新生成 |
| CHANGELOG.md | CHANGELOG.md | 重新生成 |
| .gitignore | .gitignore | 複製 |
| .git/ | .git/ | 重新初始化 |

---

## 📊 輸出格式

```
🚀 專案初始化完成

專案資訊：
- 名稱：my-awesome-project
- 類型：Python 後端
- 位置：C:\projects\my-awesome-project

已建立：
- ✅ 目錄結構
- ✅ 憲法與子法 (CONSTITUTION.md + 4 bylaws)
- ✅ Claude Skills (19 個)
- ✅ Memory Bank (7 個空檔案)
- ✅ README.md / CHANGELOG.md
- ✅ Git 初始化

下一步：
1. cd C:\projects\my-awesome-project
2. code .
3. 執行「更新 memory bank」記錄專案目標
```

---

## ⚠️ 注意事項

1. **不要複製 data/ 目錄**：這是模板專案的暫存資料
2. **重設所有版本號**：CHANGELOG 從 Unreleased 開始
3. **清空 Memory Bank**：不要複製模板的記憶內容
4. **更新專案名稱**：搜尋並替換所有 "template-is-all-you-need"
