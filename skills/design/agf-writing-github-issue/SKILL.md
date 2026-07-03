---
name: agf-writing-github-issue
description: Use whenever a user, product-lead, or qa-engineer wants to create a GitHub issue in the project repo — including phrases like "提一个 issue / 写一个 issue / 报 bug / 把这个开成 issue / gh issue / 上 GitHub / track 一下 / 立个 ticket". Provides the required-field skeleton, locked label set (type / area / epic / priority / severity / phase), gh CLI heredoc template, and the QA-auto-issue exception path. Replaces ad-hoc `gh issue create` calls with inconsistent titles / missing labels / freestyle bodies.
---

# Writing a GitHub Issue

Use this skill when any of the following:

- 用户说 "写 issue / 提一个 issue / 报 bug / 上 GitHub / track 一下 / 立个 ticket"
- product-lead 把 PRD 里的 AC 拆成可分派的 issue
- dev 在 SIT 自跑中发现 P0 / P1 缺陷（**特殊路径，见下**）
- qa-engineer 在 E2E / UAT 中发现 P0 / P1 问题（**特殊路径，见下**）
- 主 Claude / 任意 agent 准备调用 `gh issue create`

> **拼 body / 写命令前必读** [`references/templates-and-examples.md`](./references/templates-and-examples.md)：Body 模板（feature + bug 增补段）、gh CLI HEREDOC 正确写法、3 个完整例子（feature / bug / dev SIT 自动路径，含 RolexOps 实例需替换为本项目实际值）。

## 最小输入模式（用户授权 / 2026-05-13）

> **默认行为**：用户只给"关键信息"，agent 智能补全其他字段，直接 `gh issue create`，不走草稿 gate。

### 用户必须给的最少信息

| 信息 | 说明 |
|---|---|
| **要解决什么 / 想做什么** | 一两句话描述问题或功能想法，bug / feature / chore 可推断 |

**就这一条**——其他字段都由 agent 推断 + 补全。

### Agent 必须自动补全的字段

| 字段 | 推断规则 |
|---|---|
| **Title** | 按用户描述拟动宾结构 + type prefix `feat(...)` / `fix(...)` / `chore(...)` / `docs(...)`，≤70 char |
| **Why / 背景** | 从用户原话扩写 1-2 段；若有相关 PRD / ADR / 历史 issue，主动 grep `docs/prd/` `docs/adr/` 并 cite |
| **AC** | 按 feature/bug 套模板生成 2-4 条可验证条件；bug 必含 "修复后用什么验证" |
| **type label** | 按关键词判 feat（新功能）/ bug（修缺陷）/ chore（重构/构建/文档）/ adr（架构决策） |
| **area label** | grep 用户描述关键词：`frontend`/`React`/`UI`/`组件` → area:frontend；`API`/`endpoint`/`后端`/`数据库`/`migration` → area:backend；`LLM`/`prompt`/`豆包`/`Qwen`/`embedding` → area:ai；`docker`/`compose`/`caddy`/`redis` → area:infra |
| **priority** | bug 默认 P1（核心流程影响）；feature 默认 P2（用户说"急/紧急/blocking"→ P1）；data loss / 安全 / 线上挂 → P0 |
| **severity**（bug 专用） | 与 priority 同步：P0/P1 |
| **epic 关联** | grep 当前 branch 名（`release/v1.6.0` etc.）+ 最近 commit + `docs/prd/`，能锁定 Epic N 才加；不确定**不加**，宁缺勿乱 |
| **phase** | 默认不加；除非用户在 SIT/E2E/UAT 上下文中报问题 |
| **复现步骤**（bug 专用） | 用户没给则合理推测填，末尾标 `<!-- TODO 用户补充实际复现 step -->` |
| **环境**（bug 专用） | grep `docker compose ps` 拿当前 image / commit hash，前端 bug 默认填 "Chrome 最新版（用户未指定）" |
| **关联 (Refs)** | 主动 grep 关联 PRD / ADR / 现有 issue（gh issue list -L 10 关键词）；找到的填，找不到填 N/A |

### 兜底问号（只在以下情况问用户）

1. **priority 真拿不准 P0/P1/P2** — 如用户说"挺重要"，bug 但没说阻塞与否
2. **area 完全猜不出** — 描述太抽象（"那个东西坏了"）
3. **是 bug 还是 feature 真分不清** — 如"X 行为不太对，是不是应该 Y"

非这三种 → **不要问，直接补全 + 创建**（事后用户在 GitHub 上 edit 比中途问还快）。

## 自动 issue 路径（已授权，跳过用户确认）

**路径 A — dev 在 SIT 中发现 P0 / P1**（SIT 由 dev 自跑）：

1. 直接 `gh issue create`（不需问用户、不需 product-lead 同意）
2. `--label "type:bug,priority:P0,severity:P0,phase:sit"`（或对应 P1）
3. 创建后通过 SendMessage 向 product-lead 报告 issue 号
4. **P2 问题不开 issue**，只在 `progress/<role>.md` 的 `**SIT 证据**` 段记 fail/blocked

**路径 B — qa-engineer 在 E2E / UAT 中发现 P0 / P1**：

1. 直接 `gh issue create`
2. `--label "type:bug,priority:P0,severity:P0,phase:e2e"`（或 `phase:uat`）
3. 创建后通过 SendMessage 向 product-lead 报告 issue 号
4. **P2 问题不开 issue**，只记录在 E2E / UAT 报告里

来源：用户 2026-05-13 授权；SIT 归 dev，QA 仅覆盖 E2E / UAT。

## 优先级判定

| 级别 | 适用场景 |
|---|---|
| **P0** | 线上阻塞 / 数据损坏 / 安全漏洞 / UAT-block regression |
| **P1** | 核心流程影响 / UX regression / 性能 SLA 超标但非阻塞 |
| **P2** | 次要 / 体验优化 / nice-to-have |

判不准时 → 偏保守降一级（P0→P1），勿默认拔高。

## 本仓锁定 label 集合（不要自创）

`gh label list` 已固化的 label，**只能从下面选**（新需求要新 label → **先停下问用户**，不要直接 `gh label create`）：

```
type:feat | type:bug | type:chore | type:adr
area:frontend | area:backend | area:ai | area:infra
epic:1 | epic:2 | epic:3 | epic:4 | epic:5 | epic:6
epic:7 | epic:8 | epic:9 | epic:10 | epic:11 | epic:12
phase:design | phase:dev | phase:review | phase:sit | phase:e2e | phase:uat
priority:P0 | priority:P1 | priority:P2
severity:P0 | severity:P1
status:blocked | status:needs-info | status:wontfix
release:vX.Y   # release 关联标签，按项目实际 milestone 替换（模板无固定值）
```

## gh CLI 写法红线

正确写法 = HEREDOC `--body "$(cat <<'EOF' ... EOF)"`（完整模板见 [`references/templates-and-examples.md`](./references/templates-and-examples.md)）。**错误做法**（禁止）：

- ❌ `gh issue create --body "..."` 含换行 / 反引号 / 中文引号 —— shell 转义噩梦
- ❌ `--label "P0"` —— 不带 `priority:` 前缀
- ❌ `gh label create` 自创新 label —— 必须先问用户

## 执行流程（最小输入模式）

1. 接收「关键信息」→ 按上文"Agent 必须自动补全的字段"表推断 title / type / area / priority / severity + grep epic / refs，按 type 套 body 模板（见 references）。
2. 命中"兜底问号"三类才简短问一句（且只问那一个不确定字段），否则跳过。
3. HEREDOC 拼 body + 锁定 label → `gh issue create`（直接执行）→ 报告 URL + label 清单 →（QA 路径）SendMessage product-lead 报 issue #。

## 验证 gate（issue 创建后）

每次 `gh issue create` 成功后，最后一条 user-facing 消息**必须包含**：

- ✅ Issue URL（gh 命令的 stdout 第一行）
- ✅ 已贴的 label 清单
- ✅（若 QA 路径）已发给 product-lead 的 SendMessage 确认

让用户能立刻点链接 + 确认分类对不对。

## Anti-patterns

| 反模式 | 为什么不行 |
|---|---|
| Title 用句号结尾 / 含特殊字符 | gh search / 看板列表不易扫读 |
| AC 写 "正常工作" / "符合预期" | 不可验证 → code-reviewer / qa-engineer 没法逐条核 |
| Body 大段无结构 | 后续被分派的 dev 找不到关键信息 |
| 不标 priority | 看板按 priority 排序 / 触发不了 P0 通知机制 |
| 既不标 type 也不标 area | 责任田不清 → 没人接 |
| Mock / fake 描述 | 禁 mock 描述，issue 必须真实场景 |

## Related skills

- `agf-writing-prd` — issue 通常源于 PRD AC，反向链回 PRD 路径
- `agf-writing-adr` — 涉及架构变更时先开 ADR，再开 issue 引用
- `agf-running-sit-tests`（dev-owned SIT）/ `agf-writing-qa-report`（E2E/UAT 报告，SIT 不在范围内） — QA 与 dev SIT 路径上下文
