---
name: codex-plugin-dev-structure
description: Use when the user asks how to structure Codex skills (folders, SKILL.md, supporting files), wants plugin-dev-like organization, or needs conventions for templates/scripts bundled with a skill.
---

# Codex Plugin-Dev：Skill 結構慣例

## 建議目錄結構
每個 skill 一個資料夾（與現有 `.codex/skills/*` 一致）：

```
<CODEX_HOME>/skills/
  my-skill/
    SKILL.md
    scripts/                # 可選：可重用腳本
    templates/              # 可選：檔案模板
    reference/              # 可選：重型參考文件（100+ 行）
```

## SKILL.md 必要元素（最低限度）
- YAML frontmatter
  - `name`: 僅允許 `a-z0-9-`（全小寫 + hyphen）
  - `description`: **以 "Use when..." 開頭**，只寫「什麼情況要用」，不要寫流程
- 內容要包含：
  - Overview（這個 skill 的核心價值）
  - When to use（用症狀/關鍵字讓搜尋命中）
  - Quick start（最短可跑的指令或步驟）

## 觸發（Discovery）設計要點
`description` 盡量包含：
- 使用者會打的詞：`skill`, `SKILL.md`, `frontmatter`, `trigger`, `description`, `YAML`
- 症狀：`skill 沒觸發`, `找不到 skill`, `不會自動選用`
- 同義詞：`template`, `skeleton`, `boilerplate`, `scaffold`

## Supporting files 原則
- 「可複用工具」放 supporting file（script/template），避免把整段工具塞進 SKILL.md。
- 需要跑 Python 時：必須遵守專案 `uv + .venv`，且指令要用 `.venv\\Scripts\\python.exe`。

