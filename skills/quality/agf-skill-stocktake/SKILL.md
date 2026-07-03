---
name: agf-skill-stocktake
description: Use when PL / tech-lead audits the content quality of AGF's own skills (`.claude/skills/agf-*/SKILL.md`). Provides the 5-dimension checklist (Actionability / Scope fit / Uniqueness vs CLAUDE.md+standards / Currency of pointers / Gate-binding validity), 5-verdict rubric (Keep/Improve/Update/Retire/Merge), reason-quality bar (反敷衍), and output skeleton. Triggered each MINOR release retro or manually.
---

# Skill Stocktake（AGF 自有 skill 内容质量审计）

Use this skill when:

- MINOR release retro 时审 AGF 自有 skill 是否腐化
- 手动盘点 skill 质量（感觉 skill 集膨胀 / 指针过期 / 内容重叠）
- 新增 / 删除 skill 后回归一次确保无重叠

## What it is — and is not

**Skill Stocktake** 审计 AGF 自有治理型 skill 的**内容质量**——不是语法（`lint-all.sh` 管）、不是 SSOT drift（`gen-roles.py --check` 管）。它审 skill 是否仍 actionable / scope-fit / unique / 指针新鲜 / 绑定有效 gate。

**不审**：第三方 skill（`docx` / `pptx`，Anthropic 提供，非 AGF 治理资产）。

## Scope

`.claude/skills/agf-*/SKILL.md`。**以 `ls .claude/skills/agf-*/SKILL.md` 实际为准，不在文档硬编码计数**（守 `verified-facts.md` 纪律）。

## 5 维 checklist（每 skill 逐条核）

AGF 在 ECC 4 维上加 1 维 **Gate 绑定**（AGF 治理型 skill 的核心——每个 `agf-*` 都该绑一个受治理流程 + gate）：

1. **Actionability**：有可立即执行的步骤 / 命令 / 代码示例（不是空泛原则）
2. **Scope fit**：name / trigger（description）/ 内容对齐，不过宽不过窄
3. **Uniqueness**：内容不被 `CLAUDE.md` / `standards/` / 另一 skill 替代（守 SSOT，不重复）
4. **Currency（指针新鲜度）**：引用的 `CLAUDE.md` / `standards/*.md` / `docs/adr/*.md` 路径仍存在 + 内容同步（用 `rg` / `[ -f ]` 验路径，抽查引用内容是否漂移）
5. **Gate 绑定有效性**（AGF 特有）：skill 是否仍绑一个有效 gate / SSOT 命令（如 `agf-deploying-uat` 绑部署门 + `/agf-deploy-uat`；`agf-writing-change` 绑变更文件夹 + `agf-spec-validate`）。无 gate 的 skill 要么是知识型（说明）要么是孤儿（候选 Retire）

## 5 档 verdict

| Verdict | 含义 |
|---|---|
| **Keep** | 5 维全过，仍有效 |
| **Improve** | 值得保留但需具体改进（指明哪段 / 什么改 / 目标规模） |
| **Update** | 引用的技术 / 路径过期（`rg` / WebSearch 验证后更新） |
| **Retire** | 低质量 / 过时 / cost-asymmetric（说明什么覆盖了它） |
| **Merge into [X]** | 与另一 skill 重叠（指明目标 + 整合什么内容） |

## Reason 质量要求（反敷衍）

评估是整体 AI 判断（非数值 rubric）。但 `reason` 字段必须自包含、可决策：

- ❌ 不写 "unchanged" / "overlaps with X" 这种空话
- ✅ **Retire**：(1) 发现什么具体缺陷 (2) 什么覆盖了同一需求
  - Bad: `"Superseded"`
  - Good: `"agf-writing-prd 已 v6.9.0 弃用，agf-writing-change 覆盖全部场景 + delta + archive；无独有内容残留"`
- ✅ **Merge**：目标 skill + 整合什么内容
- ✅ **Improve**：哪段、什么改、目标规模
- ✅ **Keep**（仅 mtime 改）：重述原 verdict 依据，不写 "unchanged"

## 流程

### 1. Inventory

```bash
ls .claude/skills/agf-*/SKILL.md
```

### 2. 逐 skill 评估

对每个 skill：Read `SKILL.md` → 5 维核对 → 填 verdict + reason。

**Currency 维必须验路径**（静默腐化高发点）：
```bash
# 验 skill 引用的路径存在
rg -oE '\[.*?\]\(([^)]+)\)' .claude/skills/agf-<name>/SKILL.md | ...   # 抽链接
[ -f <引用路径> ] && echo OK || echo STALE
```

skill 数少（~15），**一批跑完**，不需要 chunk / resume（ECC 的 chunk 是为 261 skill 设计，AGF 裁剪掉）。

### 3. 输出

写 `docs/reviews/skill-stocktake-<YYYY-MM-DD>.md`：

- frontmatter（`reviewer` / `date` / `scope: agf-*` / `skill_count`）
- 汇总表（Skill | Verdict | Reason 一行）
- 按 verdict 分组详情
- 改进项（Improve / Update / Retire / Merge 的具体 action 清单）

### 4. PL 决策

**Retire / Merge** 涉及删 / 合 skill，PL 确认后才动（不自动删——守 `agf-writing-change` 变更门，删 skill 是 REMOVED Requirement 级变更）。Improve / Update 由 PL 派 maintainer 或 tech-lead 执行。

## 触发节奏

- **每 MINOR release retro**：作为 retro 的可选步骤（见 `agf-running-release-retro`）
- **手动**：PL / tech-lead 觉得 skill 集膨胀 / 指针过期时随时跑
- **PATCH 不跑**：skill 腐化慢，MINOR 周期够
- **MAJOR release 前**：强烈建议跑一次（大版本是清理窗口）

## Anti-patterns

- ❌ 把 stocktake 当 lint 跑（语法 / drift 是 `lint-all.sh` + `gen-roles.py --check` 的事）
- ❌ 审第三方 skill（`docx` / `pptx` 非 AGF 治理资产）
- ❌ Retire / Merge 不经 PL 确认直接删 / 合（违反变更门）
- ❌ reason 写 "unchanged" / "overlaps"（反敷衍要求）
- ❌ 跳过 Currency 维的 `rg` 验证（指针过期是静默腐化，不验 = 没审）
- ❌ 硬编码 skill 计数（以 `ls` 实际为准，守 `verified-facts.md`）
