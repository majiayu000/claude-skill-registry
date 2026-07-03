---
name: agf-writing-adr
description: Use when tech-lead is about to record an architecture decision (new tech stack member, deviation from baseline, deployment / observability / auth scheme choice). Provides ADR structure, version-audit appendix format, and "what NOT to ADR" guidance. Replaces ad-hoc copy from ADR-000.
---

# Writing an ADR (Architecture Decision Record)

Use this skill when:

- A new technology / framework / vendor is being added to the stack (not already covered by ADR-000)
- An existing baseline is being **deviated from** (e.g. swapping Postgres → SQLite for a specific service)
- A cross-cutting decision needs explicit record (auth scheme, deployment shape, observability stack, LLM caching policy)
- code-reviewer escalates a "this needs ADR" finding

**Do NOT write an ADR for**:
- Routine library version bumps (lockfile is enough)
- Internal refactors that don't change external contract or stack
- Bug fixes
- Anything one team would forget within a month

If unsure → write it. ADR cost is low; the "why" memory is what disappears.

## File path & numbering

`docs/adr/NNN-[slug-kebab-case].md` — sequential, zero-padded 3 digits. Examples:
- `001-jwt-vs-session-auth.md`
- `002-llm-caching-policy.md`
- `003-deploy-target-fly-io.md`

ADR-000 is reserved for the system architecture baseline. Never reuse a number; if abandoned, mark `Status: Superseded by ADR-NNN`.

## Status lifecycle

`Proposed` → `Accepted` → (later) `Superseded by ADR-NNN` / `Deprecated`. Once `Accepted`, **do not edit decisions**; supersede with a new ADR.

Allowed in-place edits on Accepted ADRs:
- Backfill `## 版本与查证` rows when a deferred row resolves
- Typos and broken links

Anything else → new ADR.

## Required sections

```markdown
# ADR-NNN: [Title]

- 状态：Proposed / Accepted / Superseded by ADR-NNN / Deprecated
- 日期：YYYY-MM-DD
- 决策者：tech-lead [+ co-decider role if any]
- 影响范围：[模块/全栈/单服务]

## 上下文

为什么现在需要这个决策？1–3 段：业务驱动、技术约束、当前痛点、不做这个决策会出什么问题。

## 决策

| 维度 | 选型 | 理由 |
|---|---|---|
| ... | ... | 为什么是它，而不是 [备选] |

或者用文字描述（如果不是结构化对比）。**关键：必须列出至少一个备选方案 + 为什么否决它。**

## 备选方案

- **A. [备选 1]** — pros / cons / 否决理由
- **B. [备选 2]** — pros / cons / 否决理由

如果没列备选 = 你没真正决策，只是默认接受。回去补。

## 影响

- 对现有代码：哪些模块会变 / 不变
- 对团队：谁需要学新东西
- 对成本：每月预估增量（CNY 或 token）
- 对运维：新增监控点 / 告警 / 备份策略

## 本 ADR 不覆盖的决策

明确列出"相关但留给未来 ADR"的内容，避免读者期待落空。

## 后续工作

- [ ] 谁 / 什么时间 / 做什么（具体到角色 + 触发条件）

## 版本与查证

> tech-lead 行事原则 #3「先查最新版再决策」的回填段。新增技术或大版本升级时必填。

**查证基线日期**：YYYY-MM-DD

| 选型 | 选定版本 | 最新稳定版 | 与最新版差距 | 维护状态 | 信息来源（含原文摘录） |
|---|---|---|---|---|---|
| ... | x.y.z | a.b.c | 1 个 minor 落后 | Active | [官方 changelog URL] — "原文..." |

**回填规则**：执行层在落地时（write lockfile / pyproject.toml）回填本表对应行，commit message 加 `docs(adr): backfill ADR-NNN verification for [pkg]`。
```

## "查证 → 决策 → 写 ADR" 三步骤

ADR 不是事后总结，是决策**前**的工具：

1. **查证**：每个候选选型先用 Context7（`resolve-library-id` → `get-library-docs`）拉当前版本官方文档；未收录或版本信息不足再 WebFetch 官方 changelog / release notes。记录"今天最新稳定版 + 维护状态 + 已知 breaking change"
2. **决策**：在多个候选间挑选，列至少 1 个备选 + 否决理由
3. **写 ADR**：把上述过程落地，commit + announce

做完 1 + 2 但跳过 3，未来一定会被问"当时为啥选这个"——答不了就是组织记忆缺失。

## 完成前的验证

- [ ] 至少 1 个备选方案被列出并解释为何否决？
- [ ] 「影响」节包含成本估算？
- [ ] 「版本与查证」表至少 1 行（如果是新技术决策）？
- [ ] 引用的官方 URL 都能打开？
- [ ] CLAUDE.md 的 Tech Stack 表已同步更新（如果决策影响该表）？
- [ ] 已通过 `TaskCreate` 跟踪「后续工作」中的事项（如有）？

## 反模式

- ❌ 「因为大家都用」/「业界标准」 — 不是理由，写出**你具体的约束**
- ❌ 没有备选 — 表示你只是默认采纳，不是决策
- ❌ ADR 改 Accepted 状态后的「决策」段 — 必须 supersede
- ❌ 写完 ADR 不更新 CLAUDE.md Tech Stack 表 — 单一来源原则破裂
- ❌ ADR 标题用「升级 X 到 Y 版本」 — 那不是决策，是事实记录；除非升级跨大版本且有 breaking change，否则进 commit message 即可

## Hand-off

ADR 落盘后：

1. **同步 CLAUDE.md** Tech Stack 表（如果选型清单变了）
2. **同步 ADR-000** 的「本 ADR 不覆盖的决策」节（如果新 ADR 覆盖了某项）
3. SendMessage product-lead："ADR-NNN 已 accepted, 后续工作清单 [link]"
4. 如果 ADR 引入新依赖 → SendMessage 对应执行层落地（且引用 cost-budget.md 评估增量）
