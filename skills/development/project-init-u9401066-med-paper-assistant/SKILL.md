---
name: project-init
description: 初始化新專案。觸發：init、新專案、初始化、create project。
---

# 專案初始化技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 初始化新專案、create project | ✅ |
| 從模板建立專案 | ✅ |
| bootstrap、scaffold | ✅ |

---

## 可用工具

| 操作 | 工具 |
|------|------|
| 建立目錄 | `create_directory()` |
| 建立檔案 | `create_file()` |
| 終端指令 | `run_in_terminal()` |
| VS Code | `create_new_workspace()` |

---

## 專案結構模板

```
new-project/
├── .github/
│   ├── bylaws/           # 子法
│   └── prompts/          # Prompt Files
├── .claude/
│   └── skills/           # Skills
├── memory-bank/          # Memory Bank
│   ├── activeContext.md
│   ├── progress.md
│   └── decisionLog.md
├── src/                  # 原始碼
├── tests/                # 測試
├── CONSTITUTION.md       # 憲法
├── README.md
├── CHANGELOG.md
└── pyproject.toml
```

---

## 標準工作流程

```python
# 1. 取得專案資訊
project_name = "my-new-project"
project_path = f"/home/user/projects/{project_name}"

# 2. 建立目錄結構
create_directory(f"{project_path}/src")
create_directory(f"{project_path}/tests")
create_directory(f"{project_path}/memory-bank")
create_directory(f"{project_path}/.github/bylaws")
create_directory(f"{project_path}/.claude/skills")

# 3. 建立基礎檔案
create_file(f"{project_path}/README.md", "# {project_name}\n...")
create_file(f"{project_path}/CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n")
create_file(f"{project_path}/pyproject.toml", "[project]\nname = '...'")

# 4. 初始化 Git
run_in_terminal(f"cd {project_path} && git init")

# 5. 初始化 Python 環境
run_in_terminal(f"cd {project_path} && uv venv && uv sync")
```

---

## 互動式設定

詢問用戶：

| 項目 | 選項 |
|------|------|
| 專案名稱 | 自訂 |
| 程式語言 | Python / TypeScript / Other |
| 授權 | MIT / Apache-2.0 / GPL-3.0 |
| Docker | 是 / 否 |
| CI/CD | GitHub Actions / None |

---

## 輸出範例

```
🚀 專案初始化

專案名稱: my-new-project
位置: ~/projects/my-new-project

✅ 目錄結構已建立
✅ 基礎檔案已建立
✅ Git 已初始化
✅ Python 環境已設定

下一步：
  cd ~/projects/my-new-project
  code .
```

---

## 相關技能

- `ddd-architect` - 設計專案架構
- `memory-updater` - 初始化 Memory Bank
