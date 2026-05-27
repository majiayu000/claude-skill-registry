---
name: codex-plugin-dev-validate
description: Use when the user suspects a Codex skill is not triggering, wants to validate SKILL.md frontmatter (name/description), check description quality for discovery, or needs a plugin-dev-like validation step for skill packaging.
---

# Codex Plugin-Dev：Validation（Skill 觸發/格式）

## 核心檢查項
1) `SKILL.md` frontmatter 是否存在且可解析  
2) `name` 是否符合 `^[a-z0-9-]+$`，且與資料夾名一致  
3) `description` 是否以 `Use when...` 開頭  
4) `description` 是否包含足夠關鍵字/同義詞（可被命中）  
5) Supporting files 路徑是否存在、指令是否可執行

## 快速驗證（腳本）
- `pwsh -File C:\\Users\\IOT\\.codex\\skills\\codex-plugin-dev-validate\\scripts\\validate_codex_skill.ps1 -SkillName <skill-name>`

> 若環境有設定 `$env:CODEX_HOME`，腳本會優先在 `$env:CODEX_HOME\\skills\\...` 找 skill。

## 當「沒觸發」時的 Debug 問題
- 使用者實際問法是什麼？（請貼 3～5 句原話）
- 你的 description 有沒有包含那些用詞？（同義詞也算）
- 有沒有更「精準」的 skill 在搶匹配？（描述重疊）

