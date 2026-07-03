---
name: agf-writing-change
description: Use when product-lead is about to formalize a feature into a change folder (the OpenSpec-style intake that replaces PRD as of v6.9.0). Provides the four-artifact structure (proposal / delta specs / design / tasks), the Requirement+Scenario delta format (ADDED/MODIFIED/REMOVED/RENAMED), the AC↔scenario mapping that keeps the AGF verification spine intact, the validate gate, and the archive-merge hand-off. Replaces agf-writing-prd (deprecated).
---

# Writing a Change（变更文件夹入口）

变更文件夹（`docs/changes/<change>/`）是 AGF 自 v6.9.0 起的**新需求入口**，取代 PRD（OpenSpec 风格，决策见 [ADR-012](../../../docs/adr/012-spec-driven-change-folders.md)）。它把需求表达成**对活规格的 delta**，交付签字后 merge 进 `docs/specs/`——让「系统当前有哪些行为」永远有 SSOT。

Use this skill when：

- product-lead 跑完 `superpowers:brainstorming` 且用户批准了大方向。
- 要把一个 feature 正式化成 `docs/changes/<change>/` 四件套，再派工。
- 既有 change 在 open question 解决后更新。

> **验证脊柱不变**：apply 之后的 SIT 自跑 / code review + SIT Audit / 部署门 / E2E / UAT pass² / 业务签字全照旧。本 skill 只管**入口**。

## Pre-conditions

- [ ] 方向已获批（还在探索 → 先 `superpowers:brainstorming`，别建 change）。
- [ ] 知道用户是谁、优化什么业务结果。
- [ ] 至少 1 个可测的成功标志。

任一不满足：**停，别建 change**，回 brainstorming 或 SendMessage 用户澄清。

## 建一个 change

```bash
cp -r docs/changes/_TEMPLATE docs/changes/<change-kebab-case>
```

`<change>` 用 kebab-case 动词短语（如 `add-dark-mode`、`oauth-login`）。一个 change 一个文件夹。

## 四件套

### 1. `proposal.md` —— why + what + scope

- **Why**：用户痛点 / 业务驱动（1–3 段）。
- **What**：本次交付的能力一句话；**Non-Goals** 至少 1 项。
- **影响的能力**表：列触及的 capability + 对应活规格路径 + 本次 delta 文件（新建能力标 NEW）。
- **Open Questions**：每条标 Owner + Due（缺则不进派工）。
- 顶部填 effort tier（Small/Medium/Large）+ **交付 lane**（full/fast；高风险一律 full）。

### 2. `specs/<capability>.md` —— delta（唯一会 merge 进活规格的部分）

对每个触及的能力写一个 delta 文件（文件名 = capability kebab-case）。段头**只保留用到的**：

```markdown
## ADDED Requirements
### Requirement: <新行为名>
The system MUST <规范性契约>.
#### Scenario: <名>
- WHEN <触发>
- THEN <可观察结果>

## MODIFIED Requirements
### Requirement: <既有行为名>       # header 须与活规格精确匹配（whitespace-insensitive）
The system MUST <改后的完整行为>.    # 整块复制活规格里的 requirement+scenario 再改
#### Scenario: <名>
- WHEN ...
- THEN ...

## REMOVED Requirements
### Requirement: <被删行为名>
**Reason**: <为什么删>
**Migration**: <调用方/用户怎么迁移>

## RENAMED Requirements
- FROM: `### Requirement: <旧名>`
- TO: `### Requirement: <新名>`
```

**铁律**：每个 `### Requirement:`（ADDED/MODIFIED）下**至少 1 个 `#### Scenario:`**（恰好 4 个 `#`）；Requirement 用 MUST/SHALL；REMOVED 必带 Reason+Migration。

### 3. `design.md` —— 单 change 技术「怎么做」（薄，可省）

简单 change 删掉本文件即可。高风险 change（auth / schema 迁移 / LLM 切换 / cross-cutting）**引用一个新 ADR**（tech-lead 写），不在 design.md 自拍架构。API 契约 SSOT 仍是 OpenAPI（[ADR-006](../../../docs/adr/006-frontend-backend-contract-sync.md)）。

### 4. `tasks.md` —— 实现 checklist + AC↔scenario 映射

**关键**：维护 `AC-N ↔ <capability> / Requirement / Scenario` 映射表。AC 仍是 `AC-N`（编号 / 优先级 / progress 5 段格式 / SIT hook 全不变，[ADR-012](../../../docs/adr/012-spec-driven-change-folders.md) 决策 4），语义来源是 delta 的 scenario——dev 逐 AC 自验、qa 逐 AC 测、PL 逐 AC 签字，照旧。

## 写 delta 前：消歧自检（借鉴 Spec Kit `/clarify`）

`brainstorming` 探索完、动笔写 delta 前，按这张 taxonomy 核一遍关键维度有没有遗漏（避免"写完才发现没问清"）；有 Partial / Missing 的回去 SendMessage 用户澄清：

| 维度 | 自检 |
|---|---|
| Scope / 边界 | 本次做什么、明确**不做**什么（Non-Goals）清楚？ |
| 数据 / 实体 | 关键实体 / 字段 / 约束 / 生命周期定义了？ |
| UX / 流程 | 用户主路径 + 关键分支（含失败 / 空态）覆盖？ |
| 非功能 | 性能 / 并发 / 配额 / 安全 / 合规有要求吗？有则**量化**（别写"快"/"高效"，写阈值） |
| 集成 / 依赖 | 触及哪些既有能力 / 外部服务 / 契约？ |
| 边界 / 异常 | 错误 / 超时 / 越权 / 并发冲突等 edge case 想过？ |
| 术语 | 与活规格既有术语一致（无同义漂移）？ |

> 每个有内容的维度落进对应 delta 的 Requirement / Scenario；与本 change 无关的维度跳过即可，不强凑。

## validate（对齐前自检）

```bash
bash .claude/scripts/agf-spec-validate.sh docs/changes/<change>/specs/*.md
```

advisory（不阻断）；修掉 flag 省一轮 review 打回。code-reviewer 在 review 时也会跑。

## 完成前的验证

- [ ] 每个 capability 的 delta 段头合法、每 Requirement ≥1 Scenario、REMOVED 带 Reason+Migration？
- [ ] **无模糊词**：Requirement 无未量化的「快 / 高效 / 友好 / scalable…」（跑 validate 看 ⑥ flag；该量化给阈值、该明确给标准）？
- [ ] `tasks.md` 的 AC↔scenario 映射齐全、每条 AC 可被 qa 用一段话测？
- [ ] proposal 有 Non-Goals + Open Questions（每条 Owner+Due）？
- [ ] `agf-spec-validate.sh` 对所有 delta 输出 PASS（或 flag 已知可接受）？
- [ ] 已从 `_TEMPLATE` 改名 delta 文件为实际 capability、删掉未用的示例段与占位（防模板示例假绿 + archive 生成 `_capability_/` 垃圾目录）？

任一不行 → 不要派工，回去补。

## Hand-off

1. **对齐门**：SendMessage 用户审 `proposal.md` + `specs/` delta，批准后才派工（写码前对齐）。
2. `TaskCreate` 建 Agent Teams task（按 product-lead Step 2 的 6 段 schema，引用 `tasks.md`）。
3. SendMessage 执行层："change 已就绪 docs/changes/<change>/，请在 Plan Mode 报告里 cite AC 编号"。
4. 如有 UI → SendMessage uiux-designer 起稿。

## 归档（UAT 业务签字后，PL 执行）

```bash
bash .claude/scripts/agf-spec-archive.sh <change> <YYYY-MM-DD> --dry-run   # 先核查 merge 结果
bash .claude/scripts/agf-spec-archive.sh <change> <YYYY-MM-DD>            # 确认无误再正式归档
```

按 RENAMED→REMOVED→MODIFIED→ADDED 把 delta merge 进 `docs/specs/<cap>/spec.md`，change 移 `docs/changes/archive/<date>-<change>/`。脚本 **pre-flight 门控**：名称失配 / 重名 Requirement 等异常 → 非零退出、不写不归档（确认有意则 `--force` 放行）。与 `archive-progress.sh`（归档 progress）各跑各的。

> **同一 capability 同时只允许一个在途 change**（防并行 change 归档时后者覆盖前者已合并行为的 lost-update）。多个在途 change 触及同一能力时，PL 串行归档、后者基于前者已 merge 的活规格重写 delta。

## 反模式

- ❌ delta 写实现细节（SQL 字段长度等）——Requirement 是行为契约，不是代码方案。
- ❌ Requirement 无 Scenario / 用「应该」弱断言 / 不用 MUST。
- ❌ 直接手改 `docs/specs/` 活规格做功能变更——一律走 delta + archive-merge。
- ❌ 不列 Non-Goals / Open Questions 留空无 owner。
- ❌ 高风险 change 在 design.md 自拍架构而不开 ADR。
