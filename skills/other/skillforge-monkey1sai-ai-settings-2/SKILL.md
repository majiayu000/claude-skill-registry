---
name: skillforge
description: Use when the user asks which skill to use, wants to route a request to an existing skill, or wants to create/improve skills.
---

# SkillForge (Codex CLI Port)

這是將 SkillForge 4.0 的概念移植為 Codex CLI skill 的版本。目標是把「輸入 → 分流 → 建議」的思路保留，同時符合 Codex CLI 的 skill frontmatter 規格。

## Triggers

- `skillforge: {goal}` - 啟動完整流程，協助建立新技能或改進既有技能
- `do I have a skill for {topic}` - 幫你搜尋/建議現有 skill
- `which skill should I use for {task}` - 根據任務推薦適合的 skill
- `help me route this request: {input}` - 對任意輸入做 triage 與路由
- `improve {skill-name} skill` - 針對現有 skill 進行改進建議

## Quick Reference

| Input | Output | Duration |
|-------|--------|----------|
| 使用者詢問「該用哪個 skill」或「要建立/改進 skill」 | 路由建議（USE / IMPROVE / CREATE / COMPOSE / CLARIFY） | 1-3 分鐘 |

## Process

### Phase 0: Skill Triage

將輸入分類（需求/錯誤/代碼/URL），並以已知 skill 的領域與關鍵字做比對，產出建議路由。

**Verification:** 清楚給出建議 action 與至少一個理由。

### Phase 1: Deep Analysis（必要時）

在確定要「建立/改進」skill 時，補齊需求、隱含條件與長期可維護性。

**Verification:** 產出清楚的需求與風險列表。

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| 只憑直覺決定 action | 容易錯過現有 skill 或產生重複 | 先做簡短 triage |
| 一開始就產生完整內容 | 需求未釐清易走偏 | 先做分析與規格 |

## Verification

- [ ] 已明確標示建議 action 與理由
- [ ] 若需建立/改進 skill，已補齊需求與風險

## Extension Points

1. **Index 來源擴充：** 可接入更多 skill 來源（市場、私有 repo）
2. **分數校正：** 依實際命中率調整門檻

## References

- `SKILL.md`（repo 根目錄）- 原始 SkillForge 方法論與 4-phase 詳細內容
- `scripts/triage_skill_request.py` - Triage 邏輯參考
- `scripts/discover_skills.py` - 索引建立流程
