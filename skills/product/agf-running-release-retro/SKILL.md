---
name: agf-running-release-retro
description: Use when product-lead is about to run a release retrospective after a successful MAJOR or MINOR release push (PATCH skipped). Provides applicability gate, pre-conditions, 7-step execution sequence, anti-patterns, and the verification gate before commit. Pairs with template docs/reviews/retro-_TEMPLATE.md and slash /agf-release-retro.
---

# Running Release Retrospective

Use this skill when:

- product-lead has just pushed a MAJOR (`vX.0.0`) or MINOR (`vX.Y.0`) release tag and created the GitHub release
- The user typed `/agf-release-retro vX.Y.Z` and the slash dispatched here

## Applicability — PATCH is excluded

**Parse `vX.Y.Z`** to gate execution:

> retro 是 release 后的**建议复盘（非强制 gate，见 versioning.md step 7）**；本 skill 在用户主动触发 `/agf-release-retro` 时运行。

- `Y=0 ∧ Z=0` → **MAJOR**, retro applies — proceed
- `Y>0 ∧ Z=0` → **MINOR**, retro applies — proceed
- `Z>0` → **PATCH**, abort with message: "PATCH release — retro not applicable per versioning.md, exiting."

If the version is PATCH, do not proceed.

## Pre-conditions

All **must pass** before the execution sequence. On any failure, SendMessage product-lead the specific failure and do not proceed:

- [ ] CHANGELOG.md contains section `## [vX.Y.Z]`（不再要求"pushed to origin"——下条 `gh release view` 已隐含 release 必须可见于 GitHub）
- [ ] `git tag -l vX.Y.Z` returns the tag
- [ ] `gh release view vX.Y.Z` returns the release

## Execution sequence

### 1. Copy template and pre-fill header

Copy `docs/reviews/retro-_TEMPLATE.md` to `docs/reviews/retro-vX.Y.Z-YYYY-MM-DD.md` (use today's date). Pre-fill:

- Title with version and one-sentence release summary
- Release date (from git tag annotated date or `gh release view --json createdAt`)
- Link to CHANGELOG `[vX.Y.Z](../../CHANGELOG.md)`

### 2. Draft §1 (Progress)

Read CHANGELOG `## [vX.Y.Z]` section and any linked PRD / ADR. Write §1 with:

- 起点（**前一版 release 日期，或本版本 PRD 立项日期，取较晚者**）→ tag 日期：N 天
- 范围调整 / 关键卡点（major diffs from original scope，blockers，why they happened）

### 3. Dispatch self-report tasks

Use `Agent({subagent_type: ..., prompt: ...})` to send parallel self-report prompts to roles that contributed to this release:

- `code-reviewer` — code review severity distribution, rejection rates, **SIT Audit verdicts** (Pass / Pass with concerns / Redo SIT counts)
- `qa-engineer` — E2E / UAT failure counts, AC gaps missed until production (SIT is dev-owned; not in qa scope)
- Contributing execution-layer roles (`backend-dev` / `frontend-dev` / `ai-agent-dev` / `ml-engineer` / any `miniapp-*`) — implementation blockers, rework root causes
- `tech-lead` — **only if this release contains an ADR change**

Each role returns **≤3 highlights / ≤3 pains / ≤3 Action item candidates**.

### 4. Integrate role inputs into §1–§4

Read each returned self-report and integrate into:

- §1: update with timeline/blocker insights
- §2: add quality metrics (code-review severity, test failure counts, production gaps)
- §3: 摘 `/usage` 的 4 类 token 字段（`input_tokens` / `output_tokens` / `cache_creation_input_tokens` / `cache_read_input_tokens`）+ 总 cost + cache hit ratio，按 [`cost-budget.md`](../../standards/cost-budget.md) 分档明确写"本 release 落 Small / Medium / Large 哪档"（或"不涉 cost"）。这是跨 release 对比与 sweet-spot 判定的唯一数据来源。
  **`/usage` 实数强制**：4 类实数由**用户**在会话里跑 `/usage` 贴给 product-lead（`/usage` 是 Claude Code 交互命令，agent 无法自跑）；§3 缺任一实数则本 retro **不得标记完成、不得进 Step 7**——SendMessage 用户索要后等待。
- §4: note workflow frictions and template improvements

Deduplicate Action item candidates and draft §5 (Action Items table)。§5 表**必须带「继承次数」列**：新项 = 0；承自上一轮 §5 的项 = 上一轮该项值 +1。

### 4.1 Feature cycle time trend (≥3 retros 后强制评估)

> 项目声明不统计 Velocity / Burndown（见 `product-workflow.md §4.4`），但跨 retro 的"起点 → tag 日期"数据天然存在。**累计 ≥3 个 retro 后**强制做趋势评估，作为 Velocity 的隐式形式。

执行：

1. `ls docs/reviews/retro-v*.md | sort` 列出全部历史 retro
2. 从每份 retro §1 抽取 "起点 → tag 日期：N 天" + actual work 时长
3. 跨 retro 比对趋势：稳定 / 下降（团队效率提升）/ 上升（出现系统性阻塞）
4. 若 ≥3 retro 显示上升趋势 → 必须列为 §5 Action Item 候选，分析是流程问题 / 工具问题 / 范围问题
5. 若 <3 retro：本节写 "数据点不足（当前 N 个 retro），不下结论"

写入 §1 末尾或 §4 流程协作节，**不另起独立小节**，避免文档膨胀。

### 4.2 Action 继承 Gate（硬规则：禁止第三次继承）

任一 action **继承次数已 ≥2**（上一轮 §5 该项「继承次数」列 ≥2）时，本轮**必须二选一**，不得再入 §5：

- **(a) 落地为硬手段**：hook / lint 断言 / 模板必填字段 / 带死线的 gh issue —— §0 标 `done` 并附证据链接
- **(b) 显式 `dropped`**：§0 标 `dropped` + 一句话放弃理由

本轮 §5 出现「继承次数」≥3 的行即非法（= 第三次继承），verification gate 直接 fail。

### 5. Decide §6 (Public version)

Decide: **是 (public)** or **否 (not public)**.

- If **是**: dispatch `content-writer` to produce `docs/content/internal/[YYYY-MM-DD]-[slug].md` from this retro as source material
- If **否**: mark "否" in §6

### 6. Verification gate

All **must pass** before commit:

- [ ] §0 is written (首个 retro: explicit "首个 retro，无前置项"; subsequent: table filled from prior release §5)
- [ ] **Action 继承 Gate** 已应用（§4.2）：§5 带「继承次数」列且所有行 ≤2；上一轮 §5 中继承次数 ≥2 的项本轮已 (a) 落地为硬手段（§0 `done` + 证据）或 (b) `dropped` + 理由，**禁止第三次继承**
- [ ] §3 含 `/usage` 4 类 token 实数（input / output / cache_read / cache_create，用户贴入）；缺任一实数 retro 不得标记完成
- [ ] §5 has ≥1 Action item **OR** explicit "本轮无显著改进项" + one-line reason
- [ ] Every §5 row has non-empty **Owner** column, non-empty **Due** column, and a numeric **继承次数** column

If any check fails, do not proceed to Step 7.

### 7. Commit

```bash
git add docs/reviews/retro-vX.Y.Z-YYYY-MM-DD.md
git commit -m "docs(retro): vX.Y.Z release retrospective"
```

Do **not** push.

## Anti-patterns

- ❌ Action item without owner or without due date
- ❌ 同一 action 第三次继承（继承次数 ≥3 必须已落地为硬手段或 `dropped`，见 §4.2）
- ❌ §3 无 `/usage` 4 类 token 实数仍把 retro 标记完成（实数由用户贴入，缺则等待）
- ❌ §0 missing (首个 retro must explicitly state "首个 retro，无前置项")
- ❌ PATCH release forced into the template (should have aborted at Applicability gate)
- ❌ Retro content duplicates CHANGELOG (changelog = "what was built"; retro = "why and how to improve next time")

## Outputs

- Final file: `docs/reviews/retro-vX.Y.Z-YYYY-MM-DD.md`
- Optional: `docs/content/internal/[YYYY-MM-DD]-[slug].md` (if §6 = 是)
- Action items from §5 become §0 inputs for the next release retro
