---
name: agf-writing-prd
description: "[DEPRECATED since v6.9.0 → removed in v7.0.0; use agf-writing-change instead] Legacy PRD intake. Use when product-lead is about to draft a PRD for a new feature. Provides the 10-section PRD structure, AC quality bar, must-have fields, and the verification gate before sign-off."
---

# Writing a PRD (Product Requirements Document)

> ⚠️ **Deprecated since v6.9.0, will be removed in v7.0.0. Migrate to: `docs/changes/` + skill `agf-writing-change`**（变更文件夹入口，决策见 [ADR-012](../../../docs/adr/012-spec-driven-change-folders.md)）。
> PRD 仍可用作 fallback，但**新需求一律走变更文件夹**——它把需求表达成对活规格的 delta，交付后 merge 进 `docs/specs/`，让「系统当前有哪些行为」永远有 SSOT；PRD 是一次性快照、交付后沉底。

Use this skill when:

- product-lead finished `superpowers:brainstorming` and the user approved the rough direction
- Formalizing a feature into `docs/prd/[feature]-[YYYY-MM-DD].md` before dispatching execution layer
- Updating an existing PRD after an open question is resolved

## Pre-conditions

- [ ] Feature direction approved (don't write a PRD for something still being explored — use `superpowers:brainstorming` first)
- [ ] You know who the user is and what business outcome you're optimizing
- [ ] At least 1 measurable success metric is identifiable (else: brainstorm more, the requirement is too vague)

If any precondition fails: **stop, do not write a PRD**. Route back to brainstorming or SendMessage user for clarification.

## File path & naming

`docs/prd/[feature-kebab-case]-[YYYY-MM-DD].md` — e.g. `docs/prd/oauth-login-2026-05-12.md`.

One PRD per feature. Updates go to the same file with a `## Changelog` entry at the bottom; do NOT create a new dated file unless scope materially changes (then archive old, link to new).

## Required sections (in order)

```markdown
# PRD — [Feature Name]

- **Date**: YYYY-MM-DD
- **Owner**: product-lead
- **Status**: Draft / Review / Approved / In Progress / Done / Archived
- **Estimated effort tier**: Small / Medium / Large（依据 `.claude/standards/cost-budget.md`）

## 1. Background

为什么做？解决的用户痛点 / 业务驱动；引用 Linear ticket / Slack 讨论 / 用户访谈。1–3 段。

## 2. Goal & Non-Goals

**目标**:
- 一句话目标声明
- KPI（上线后用什么数据判定成功）

**Non-Goals**: 明确不做什么，避免 scope creep。

## 3. User Stories

| ID | As a | I want to | So that |
|---|---|---|---|
| US-1 | ... | ... | ... |

## 4. Acceptance Criteria

每条 AC 必须**独立可验证**——code-reviewer / qa-engineer 会逐条核对。

| ID | Priority | AC | Verification method |
|---|---|---|---|
| AC-1 | P0 | 用户提交邮箱+密码 → POST /api/auth/login 返回 200 + JWT | curl + 验响应体 |
| AC-2 | P0 | 错误密码返回 401，不区分"邮箱不存在"vs"密码错"以防枚举 | 手动 / SIT |

**AC 质量条**：
- ❌ "登录功能正常工作" → 不可验证
- ✅ "POST /api/auth/login with valid creds → 200 + body 含 `{"token": "..."}` 字段" → 可验证

## 5. Design

- UI: 链接 `docs/design/[feature]/spec.md` + `index.html` 原型
- API 契约：列新增/变更接口签名（path, request, response, error code）
- 数据模型：列新增/变更表结构（字段、类型、索引）

## 6. Technical Constraints

- 必须遵守 `.claude/standards/coding.md`、`security.md`、`observability.md`
- LLM 集成：参考 skill `agf-wiring-multi-llm-sdk`
- 性能预算：API P95 ≤ 500ms / LLM P95 ≤ 5s（项目可调）
- 不引入新依赖（除非 tech-lead 已起 ADR）

## 7. Cost Estimate

- 预估 LLM token / 月：
- 预估 Agent Team 开发 token：
- 触发 cost-budget.md 哪一档？（Small / Medium / Large）

## 8. Out of Scope / Future Work

明确不在本次范围、留给后续迭代的工作项。

## 9. Open Questions

未确定的问题，**每条必须标 Owner + Due**，否则不允许进入 Step 2 任务分配（见 `docs/product-workflow.md §4` 与本 skill"完成前的验证"checklist）。

| ID | 问题 | Owner | Due | 备注 |
|---|---|---|---|---|
| Q-1 | <一句话问题> | <role / 具名> | YYYY-MM-DD | <附加上下文> |
| Q-2 | … | … | … | … |

## 10. Sign-offs

- [ ] product-lead: 初稿
- [ ] tech-lead: 技术可行性 review（仅在涉及架构变更时）
- [ ] frontend-dev / backend-dev / ai-agent-dev / ml-engineer / miniapp-dev: 实现可行性确认（按 PRD 涉及的执行层角色勾选；feature 不涉及的 dev 可跳过）
- [ ] uiux-designer: 设计契合 PRD（仅在有 UI 时；含 miniapp UI 时由 uiux-designer 在 MiniApp Mode 下确认）
- [ ] qa-engineer / miniapp-qa-engineer: AC 可测性确认（按 feature 涉及的 QA 角色勾选）

## Changelog

- YYYY-MM-DD: 初稿
```

## AC 写作 6 条铁律

1. **每条 AC 独立可验证** — qa-engineer 不该需要"先看其他 AC"才能测这一条
2. **优先级强制标注**（P0/P1/P2） — SIT/E2E 阶段据此决定 Block vs Conditional Pass
3. **用动词起头**（"用户点击 X 后...返回 Y"），不用"应该" / "需要" 这种弱断言
4. **错误路径单独成条**，别把"valid 时 200 / invalid 时 401"塞同一条
5. **不写实现细节** — AC 是"行为契约"，不是"代码方案"
6. **交互类 AC 写成可点击因果链** — "点击 X 控件 → 发出 `<method path>` → 成功后 UI 显示 Z"，把控件 + API 调用 + 可观测后果串进一条（防"按钮没事件 / 前后端接不上"在验收时无据可依；见 `ac-lifecycle.md` AC 可测试性标准）

## 反模式

- ❌ PRD 里写 SQL schema 字段长度（除非真是业务约束，如发票号 32 位）— 那是 design / dev 的细节
- ❌ AC = "性能良好" / "用户体验好" — 不可验证
- ❌ 不列 Non-Goals — scope 一定蔓延
- ❌ 不写 Cost Estimate — 进 cost-budget 哪一档都不知道
- ❌ Open Questions 留空 + 无 owner — 等于没问

## 完成前的验证

PRD 落盘前**自检**：

- [ ] 每条 AC 都能被 qa-engineer 用一段话描述测试步骤吗？
- [ ] Non-Goals 列了至少 1 项？
- [ ] 至少 1 个 KPI 可从现有 metrics 系统拿到？
- [ ] Open Questions 每条都填了 **Owner + Due**（缺任一项 → hook 会在 dispatch 阶段拦下，回头补更慢）？
- [ ] Cost Estimate 落到 cost-budget.md 的某一档了？

任何一条不行 → 不要发布，回去补。

## Hand-off

PRD 落盘后：

1. `TaskCreate` 建对应任务（按 product-lead Step 2 的 6 段 schema）
2. SendMessage 给相关执行层（**按 PRD 涉及的角色：frontend-dev / backend-dev / ai-agent-dev / ml-engineer / miniapp-dev** 中需要的若干个）："PRD 已就绪 [path]，请阅读 + 在初次 Plan Mode 报告里 cite AC 编号"
3. 如有 UI → SendMessage uiux-designer 起稿设计（含 miniapp UI 时由 uiux-designer 在 MiniApp Mode 下覆盖）
