---
name: idea-team
description: 想法群聊室主持人 — 把一句话想法丢给多角色 AI 团队（调研员/反方/类比者）做查漏补缺。每个角色有自己的 voice，他们互相 @ 接话；你随时插话。**这是创意扩展工具，不打分、不否决、不堵路**。Use when 用户说"组个团队聊一下"、"开会讨论这个想法"、"找几个角度看看"、"群聊一下 X"、"team review X"，或调用插件命令 `/idea-coach:idea-team`。Do NOT use when 用户已决定做这个想法只要 PRD（用 `idea-to-product`）、或用户要单独某个角色 skill、或用户只想自由 brainstorm（不需要 team 结构）。
---

# idea-team — 想法群聊室

把一句话想法丢给 3 人小组（调研员/反方/类比者），按回合说话，你随时插话。
**这是查漏补缺工具，不是 judge** — 他们帮你看你没想到的，不堵你的路。

## 1. 何时触发

- 插件命令：`/idea-coach:idea-team <想法>`
- Catalog 安装：直接调用 `idea-team` skill；不承诺插件外的别名
- 自然语："组个团队聊一下 X"、"开个会讨论 X"、"找几个角度看 X"、"group review X"

## 2. 何时**不要**触发

- 用户要单独某个角色 → 直接调用对应 catalog skill；插件内由 namespaced skill 自动路由
- 用户已决定做这个想法、要做 PRD → 插件用 `/idea-coach:idea`，catalog 调用 `idea-to-product`
- 用户只要自由 brainstorm 不要团队结构 → 直接对话即可

## 3. 团队成员（MVP 3 人）

| 角色 | emoji | 它做什么 | 详细 voice 规则 |
|---|---|---|---|
| 调研员 | 🔍 | 拉真实 2026 数据 / 竞品 / 案例 | `idea-research/SKILL.md` |
| 反方 | ⚔️ | 挑漏洞 / 找隐藏假设 / 给反例 | `idea-devils-advocate/SKILL.md` |
| 类比者 | 🪞 | 跨界类比 + yes-and 扩展 | `idea-analogist/SKILL.md` |

角色 SKILL.md 随 skill 安装位置解析，先解析实际位置再 Read：Claude Code 通常是 `~/.claude/skills/<name>/SKILL.md`，Codex 通常是 `~/.agents/skills/<name>/SKILL.md`。

**进入群聊前必须依次 Read 这 3 个 SKILL.md** — 加载每个角色的 voice 边界。如果其中某个没装（目录不存在），主持人提醒用户跑 spellbook 仓库根目录的 `install.sh`，不要替补凑数。

## 4. 启动流程

1. 抽取 `raw_idea`
2. 派生 kebab-case `slug`
3. 检查 `.idea-team/<slug>/`：若已有 `state.json` 或 `chat.md`，先让用户选择 **resume** 或创建带递增后缀的唯一 slug（如 `<slug>-2`）；选择前不得覆盖或 append
4. 确认目录唯一后 `mkdir -p .idea-team/<slug>/`，写 `state.json`：
   ```json
   { "slug": "...", "raw_idea": "...", "round": 1, "speakers": [], "round_complete": false, "status": "active", "utterances": [], "report_markdown": null, "created_at": "<ISO 8601>", "updated_at": "<ISO 8601>", "active_roles": ["research", "devils-advocate", "analogist"] }
   ```
5. **依次 Read 3 个角色 SKILL.md**
6. 进入群聊：主持人开场

## 5. 群聊机制（核心）

### 输出格式

每条发言独立一段，但一个回合的 3 个角色必须在**同一次 assistant response**
中按顺序输出为 3 个独立 block。聊天 runtime 不会在没有新用户消息时自动触发
下一次 assistant response，所以禁止把同一回合拆成三个等待触发的回复。

```
🔍 调研员: <内容，≤ 80 字>。[来源: <来源, 日期>]
```

```
⚔️ 反方: @调研员 <挑刺/反例，≤ 80 字>。
```

```
🪞 类比者: <类比 + yes-and 扩展，≤ 80 字>。
```

### 回合制

**一回合 = 3 个角色各说一次，固定顺序**：调研员 → 反方 → 类比者。

- 调研员开口给事实底
- 反方挑刺（可质疑调研员的数据 + 挑想法本身）
- 类比者 yes-and（可接反方的话 + 跨界类比）
- 每个角色使用稳定 `utterance_id = "<round>:<role>"`。先把 id、role、完整文本
  写入 `state.utterances`，同步更新去重后的 `speakers`；若 speakers 已覆盖所有
  active_roles，在**同一次 state 写入**中设置 `round_complete = true`。state 必须
  写到同目录临时文件并原子 rename，作为事实来源。
- 每次 state 提交成功后，从 `state.utterances` **完整重建** `chat.tmp.md`（每条含
  `<!-- utterance:<id> -->` marker），校验条目数/marker 唯一后原子 rename 为
  `chat.md`。不得分两次 append marker 和正文。若崩溃，Resume 总是从 canonical
  utterances 重建完整投影；对旧版仅有 chat 的会话，先一次性导入完整 marker block
  到 utterances，再重建。
- 一回合结束，**主持人邀请用户插话**：
  ```
  🎬 主持人: 第 N 回合结束。你想 @ 谁继续？说 "@反方 多说点"，或 "下一轮"，或 "汇总"。
  ```

### 用户插话规则

| 用户输入 | 行为 |
|---|---|
| `@角色 ...` | 该角色直接回应用户的话（不走回合） |
| "继续" / "下一轮" | 先 `round += 1`、清空 `speakers`、设置 `round_complete = false` 并持久化，再在一次 response 内完成三角色新回合 |
| "够了" / "汇总" | 进入汇总环节，写 `team-report.md` |
| 自由文本 | 主持人判断哪个角色最相关，邀请他接话 |

### 角色互相 @（鼓励但不强制）

- "🔍 调研员: ... @反方 你怎么看这个数据？"
- "⚔️ 反方: ... @类比者 你那个 X 类比漏了一个前提"
- 被 @ 的角色下一次发言时 acknowledge 那个 @（点头或反驳）

### 主持人职责（🎬 = main agent 旁白）

- 开场介绍到场角色
- 每回合结束邀请用户插话（**不许连跑 2 回合不问用户**）
- 检测到 voice 越界时拉回（例：类比者开始挑刺 → 主持人提醒 "类比者只 yes-and"）
- 用户说"汇总"时主持总结

### Resume 规则

读取 `round`、`speakers`、`round_complete`、`utterances` 和 `chat.md`，先从
canonical utterances 原子重建 chat 投影。`round_complete` 必须从
`set(speakers) == set(active_roles)` 派生并修复，不能把旧布尔值当唯一事实。若当前
回合未完成，只输出缺失角色 block；不得重复已记录角色。
若当前回合已完成，先邀请用户选择下一轮或汇总，不得擅自递增回合。

## 6. 输出物

`.idea-team/<slug>/`：

| 文件 | 内容 |
|---|---|
| `state.json` | { slug, raw_idea, round, speakers, created_at, active_roles } |
| `chat.md` | 完整对话 transcript（**每条发言实时 append**，不等汇总） |
| `team-report.md` | 用户说"汇总"后生成的结构化总结 |

### team-report.md 结构

```
# 💡 idea-team 汇总报告：<raw_idea>

## 🔍 调研员的事实底
- 事实 1（来源）
- 事实 2（来源）

## ⚔️ 反方挖出的漏洞 / 隐藏假设
- 漏洞 1
- 漏洞 2

## 🪞 类比者发现的跨界启示
- 类比 1 → 启示
- 类比 2 → 启示

## 🧩 你可能漏掉的 N 个角度
（基于本次群聊未触及但相关的角度，列 3-5 条）

## 💬 完整对话
见 chat.md
```

## 7. 命令变体

- `/idea-coach:idea-team <想法>` — 插件：启动新群聊
- `/idea-coach:idea-team resume [slug]` — 插件：续上次未完成的
- `/idea-coach:idea-team list` — 插件：列 cwd 下所有群聊

Catalog 用户直接调用 `idea-team` skill 并传相同参数。汇总时先生成完整报告文本，
再在**同一次原子 state 写入**中设置 `report_markdown`、`status = "completed"` 和
`completed_at`，之后从 `report_markdown` 写 `team-report.tmp.md` 并原子 rename。
Resume 对 completed 会话先用 canonical report_markdown 修复缺失/截断的报告投影，
再只展示报告路径；若迁移旧会话时发现完整 team-report 但 state 仍 active，先导入
报告并标 completed，不得重入对话。

## 8. Red Flags — 主持人在本 skill 里最容易跑偏的偷懒

| 你脑里的借口 | 反驳 |
|---|---|
| "每个角色等下一次用户消息再说" | ❌ runtime 不会自动续答；同一回合必须在一次 response 内输出 3 个独立角色 block |
| "调研员说完，反方接的内容不用 @ 他" | 鼓励互相 @，让对话有"群聊感" |
| "类比者觉得反方说错了，挑刺反驳" | ❌ 类比者只 yes-and。voice 越界由主持人拉回 |
| "连跑 2 个回合再问用户" | ❌ 每回合后必须邀请插话 |
| "调研员凭印象说事实" | ❌ 必须 WebSearch + [来源: xxx] |
| "汇总时只重复 chat.md 内容" | 汇总必须有"你可能漏掉的 N 个角度"——超越已聊内容 |
| "用户说 @ 反方但反方刚说过，跳过这次" | 被 @ 的角色必须立即回应，无论上一句是不是他说的 |

## 9. Important Rules

1. **不打分、不否决、不堵路** — 这是查漏补缺，不是 judge。
2. **voice 边界硬隔离** — 调研员不评判、反方不安慰、类比者不挑刺。越界由主持人拉回。
3. **一回合一条 response、三段角色 block** — 固定顺序输出，视觉上分段，不依赖不存在的自动续答。
4. **每回合后邀请插话** — 不许连跑 2 回合不问。
5. **每条 ≤ 80 字** — 群聊节奏 > 长篇大论。
6. **来源必引** — 调研员说事实必须 [来源: xxx, 日期]。
7. **chat.md 实时追写** — 每条发言 append 一行，不等汇总。
8. **角色未安装不替补** — 提醒用户跑 spellbook 根目录 install.sh，不让 main agent 自己 cosplay 缺席的角色。
9. **状态逐条持久化** — 每条发言后更新 `speakers`；轮次转换先写 `round` 再输出，Resume 不重复角色。

## 10. 维护者验证

回合触发、断点续聊和 slug 冲突场景见 `evals/evals.json`。修改回合或持久化
语义时，必须同步更新这些 eval。
