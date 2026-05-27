---
name: codex-plugin-dev-publish
description: Use when the user wants to share, install, or migrate Codex skills across machines or teammates (copying ~/.codex/skills, packaging a skill folder, or standardizing a plugin-dev-like toolkit for a team).
---

# Codex Plugin-Dev：Publish / Install（分享 skills）

## 常見場景
- 把個人 skills 複製到另一台機器
- 團隊想共用一套 skills（repo 內版控 + 個人安裝）

## 推薦策略（兩種）
A) **個人化安裝（最簡）**  
- 直接複製 `<HOME>\\.codex\\skills\\<skill-name>` 到目標機器同一路徑

B) **Repo 版控 + 安裝腳本（給團隊）**  
- 在 repo 放 `tools/codex-skills/`（或類似路徑）
- 提供 `scripts/install_codex_skills.ps1`，把目錄同步到 `<HOME>\\.codex\\skills\\`
- 在腳本內加 `validate_codex_skill.ps1` 先驗證再安裝

## 安裝驗收
- 列出目標資料夾下確實存在 `SKILL.md`
- 用 `codex-plugin-dev-validate` 驗證 frontmatter/description

