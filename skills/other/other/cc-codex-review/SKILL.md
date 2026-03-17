---
name: cc-codex-review
description: "CC-Codex 协作讨论。自由话题驱动的 CC-Codex 协作工具，Battle Loop 辩论机制。关键词: 审查, review, 让codex看看, codex审查, 帮我审查, 讨论, discuss, battle, 让codex检查, 发给codex, 话题, topic, 代码审查, 架构讨论, 技术决策"
---

# CC-Codex 协作讨论 Skill

通过 CodexMCP 实现 Claude Code 与 Codex 的话题驱动协作讨论工具。支持自由话题、Battle Loop 辩论机制和跨会话连续性。

本 Skill 为薄触发层，负责命令路由、初始化和上下文收集。Battle Loop 执行逻辑委托给 `codex-battle-agent`。

## 触发条件

### 命令触发
- `/cc-codex-review <topic>` - 启动新话题讨论
- `/cc-codex-review 继续` - 继续当前话题
- `/cc-codex-review 结束` - 结束话题并输出制品
- `/cc-codex-review 状态` - 查看状态
- `/cc-codex-review 重置` - 重置 session_id（保留 summary，需用户确认）

### 自然语言触发
- "让 codex 看看这个方案" / "跟 codex 讨论一下" -> 启动新话题
- "继续刚才的讨论" / "接着聊" -> 继续当前话题
- "讨论结束了" / "可以了" -> 结束话题
- "审查状态" / "当前讨论进度" -> 查看状态
- "重置会话" / "重新开始" -> 重置

## 前置依赖

- CodexMCP 已安装为 MCP Server（名称: `codex`）
- 提供 `codex` 工具，支持 `prompt`、`SESSION_ID`、`sandbox`、`return_all_messages` 参数
- 约定：topic 元数据使用 `session_id` 字段存储；调用 Codex MCP 续接时由 Agent 映射为 `SESSION_ID`
- Python 3.8+（运行 topic-manager.py）

## 通用配置

```
TOPIC_MANAGER=~/.claude/skills/cc-codex-review/scripts/topic-manager.py
DATA_DIR=.cc-codex
MAX_ROUNDS_LIGHT=1
MAX_ROUNDS_DEEP=5
```

## 审查模式

| 模式 | MAX_ROUNDS | 触发条件 |
|------|-----------|---------|
| 轻量审查（默认） | 1 | 默认模式，或用户说"审查/review/看看/检查" |
| 深度讨论 | 5 | 用户明确表达深度意图（见下方关键词） |

### 深度讨论触发关键词

用户消息中包含以下任一关键词/模式时，使用深度讨论模式：
- 明确要求多轮："深度讨论"、"深入讨论"、"仔细讨论"、"详细讨论"、"多轮"、"battle"、"deep review"
- 强烈程度词："反复推敲"、"好好讨论"、"认真审查"、"彻底审查"
- 用户通过参数指定：`--deep` 或 `--rounds N`

### `--rounds N` 参数

用户可通过 `--rounds N` 手动指定轮次（1-10），覆盖默认值。例如：
- `/cc-codex-review 审查这个方案 --rounds 3` -> max_rounds=3

**不匹配以上任何条件时，一律使用轻量审查（max_rounds=1）。**

## 话题类型与制品映射

| 话题类型 | 说明 | 制品文件名 |
|----------|------|-----------|
| code-implementation | 代码实现方案讨论 | changes.md |
| architecture-design | 架构设计讨论 | plan.md |
| bug-analysis | Bug 分析讨论 | analysis.md |
| technical-decision | 技术决策讨论 | decision.md |
| open-discussion | 开放讨论 | memo.md |

## 话题分类规则

Claude Code 根据用户话题内容自动分类：
- 涉及具体代码修改、实现步骤 -> `code-implementation`
- 涉及系统设计、模块划分、技术选型 -> `architecture-design`
- 涉及 bug 排查、错误分析 -> `bug-analysis`
- 涉及技术方案选择、权衡 -> `technical-decision`
- 其他 / 不确定 -> `open-discussion`

**不确定时询问用户确认。** 用户可通过参数手动指定类型：`/cc-codex-review <topic> --type architecture-design`

## 命令路由

1. **`/cc-codex-review <topic>`** -> 执行「讨论启动流程」
2. **`/cc-codex-review 继续`** -> 执行「继续讨论流程」
3. **`/cc-codex-review 结束`** -> 执行「结束讨论流程」
4. **`/cc-codex-review 状态`** -> 执行 `python3 "$TOPIC_MANAGER" status "$PWD"` 并格式化展示
5. **`/cc-codex-review 重置`** -> 需用户确认后，将 session_id 设为 null（保留 summary.md）

## 新会话初始化流程

每次 Claude Code 新会话启动、用户触发 `/cc-codex-review` 相关命令时，先执行初始化：

```
1. auto-cleanup: python3 "$TOPIC_MANAGER" auto-cleanup "$PWD" 120
2. 检测活跃话题: python3 "$TOPIC_MANAGER" topic-read "$PWD"
3. 如果有活跃话题:
   - 告知用户："检测到未完成的话题: [标题]（第 N/5 轮）"
   - 提示用户选择：继续讨论 / 结束话题 / 放弃并开始新话题
4. 如果无活跃话题: 正常进入命令处理
```

## 讨论启动流程（`/cc-codex-review <topic>`）

### Step 1: 创建话题

```bash
# Claude Code 自动分类话题类型（或用户指定）
python3 "$TOPIC_MANAGER" topic-create "$PWD" "<话题标题>" "<类型>"
```

从返回的 JSON 中提取 `topic_id`。

### Step 2: 收集上下文

- 读取项目背景：先查 `$PWD/CLAUDE.md`，再查 `$PWD/.claude/CLAUDE.md`
- 根据话题类型收集相关素材：
  - `code-implementation`: git diff、相关源码
  - `architecture-design`: 现有架构描述、相关文档
  - `bug-analysis`: 错误日志、相关代码
  - `technical-decision`: 备选方案描述
  - `open-discussion`: 用户提供的素材

### Step 3: 写入 context-bundle.md

将收集到的所有上下文写入一个文件，供 Agent 读取：

路径：`$PWD/.cc-codex/topics/<topic_id>/context-bundle.md`

```markdown
# Context Bundle

## 话题
<话题标题和描述>

## 项目背景
<从 CLAUDE.md 提取的信息摘要>

## 讨论素材
<收集到的上下文内容>
```

### Step 4: 构造参数并 spawn Agent

根据审查模式确定 `max_rounds`：
- 轻量审查: `max_rounds` = `MAX_ROUNDS_LIGHT` (1)
- 深度讨论: `max_rounds` = `MAX_ROUNDS_DEEP` (5)，或用户通过 `--rounds N` 指定的值

```
调用 Task tool:
  subagent_type: codex-battle-agent
  description: "CC-Codex Battle Loop"
  mode: bypassPermissions
  prompt: |
    执行 CC-Codex Battle Loop。配置如下：

    ```json
    {
      "mode": "NEW",
      "topic_id": "<topic_id>",
      "topic_title": "<话题标题>",
      "topic_type": "<话题类型>",
      "session_id": null,
      "workdir": "<$PWD>",
      "max_rounds": <根据审查模式确定: 1 或 5 或用户指定值>,
      "current_round": 1,
      "context_bundle_path": ".cc-codex/topics/<topic_id>/context-bundle.md",
      "artifact_type": "<根据话题类型映射的制品文件名>",
      "debug": false
    }
    ```

    context-bundle 路径: .cc-codex/topics/<topic_id>/context-bundle.md
```

### Step 5: 接收结果并完成

1. 解析 Agent 返回的 JSON 结果
2. 完成话题：`python3 "$TOPIC_MANAGER" topic-complete "$PWD"`
3. 如果话题有 output_dir，将制品从 artifacts/ 复制到用户指定目录
4. 向用户展示结论（见下方展示格式）

## 跨会话恢复策略

- **主路径**：使用保存的 session_id 恢复 Codex 会话（CONTINUE 模式）
- **备路径**：session_id 失效时，基于 summary.md 重建上下文（REBUILD 模式）
- 模式判断由 Skill 层完成，执行由 Agent 层负责
- 续接参数规范：Skill 仅传递 `session_id` 给 Agent；Agent 调用 MCP 时必须使用 `SESSION_ID`

## 继续讨论流程（`/cc-codex-review 继续`）

### Step 1: 读取活跃话题

```bash
python3 "$TOPIC_MANAGER" topic-read "$PWD"
```

如果无活跃话题，提示用户先创建。

### Step 2: 判断恢复模式

- 如果有 `session_id` -> 模式为 `CONTINUE`
- 如果无 `session_id`（或之前标记为失效） -> 模式为 `REBUILD`

### Step 3: 准备 context-bundle.md

- **CONTINUE 模式**：将已有的 summary.md 内容写入 context-bundle.md 作为上下文提示（Codex 仍通过 session_id 保有完整历史，此文件仅供 Agent 参考）
- **REBUILD 模式**：将 summary.md 完整内容写入 context-bundle.md 作为从零重建讨论上下文的唯一信息源（旧 session 已失效）

### Step 4: spawn Agent

```
调用 Task tool:
  subagent_type: codex-battle-agent
  description: "CC-Codex Battle Loop"
  mode: bypassPermissions
  prompt: |
    执行 CC-Codex Battle Loop。配置如下：

    ```json
    {
      "mode": "CONTINUE 或 REBUILD",
      "topic_id": "<topic_id>",
      "topic_title": "<话题标题>",
      "topic_type": "<话题类型>",
      "session_id": "<session_id 或 null>",
      "workdir": "<$PWD>",
      "max_rounds": <根据审查模式确定: 沿用原话题的模式>,
      "current_round": <当前轮次>,
      "context_bundle_path": ".cc-codex/topics/<topic_id>/context-bundle.md",
      "artifact_type": "<制品文件名>",
      "debug": false
    }
    ```

    context-bundle 路径: .cc-codex/topics/<topic_id>/context-bundle.md
```

### Step 5: 接收结果并完成

同「讨论启动流程 Step 5」。

## 结束讨论流程（`/cc-codex-review 结束`）

1. 读取活跃话题元数据和 summary.md
2. 如果 Battle Loop 尚未自然结束（仍有未决项）：
   - 基于 summary.md 中记录的共识清单，直接生成制品文件
   - 写入 `$PWD/.cc-codex/topics/<topic_id>/artifacts/<制品文件>`
3. 如果有 output_dir，复制到用户指定目录
4. 完成话题：`python3 "$TOPIC_MANAGER" topic-complete "$PWD"`
5. 向用户报告结论

## 结果展示格式

Agent 返回结果后，向用户展示：

```
## CC-Codex 讨论结论

**话题**: <话题标题>
**类型**: <话题类型>
**轮次**: <final_round>/<max_rounds>
**结论**: <conclusion>

### 达成共识
- <consensus_items 列表>

### 待处理项（如有）
- <pending_items 列表>

### 制品
- 路径: <artifact_path>
```

如果 status 为 error，展示错误信息并提示用户可选操作。

Battle 过程的中间产物（summary.md 更新等）不主动展示给用户，除非用户主动查询。

## Debug 模式

用户说 "debug 模式" / "查看交互过程" / "显示完整对话" 时，在 spawn Agent 的 JSON 参数中将 `debug` 设为 `true`。Agent 会将 Codex 调用的 `return_all_messages` 设为 `true`，返回完整对话历史。

## 用户交互说明

- Battle Loop 由 Agent 执行，执行期间用户无法中途干预
- 用户可通过 MAX_ROUNDS（默认 5）控制最大轮次
- 如需提前终止正在进行的讨论，等 Agent 返回后使用 `/cc-codex-review 结束` 基于已有 summary 生成制品
- Agent 执行完毕后，Skill 层统一向用户展示结论摘要

## 制品输出规则

**两步发布策略：**

1. **先写入内部目录**（单一真源）：
   `$PWD/.cc-codex/topics/<topic_id>/artifacts/<制品文件>`
   （topic_id 从 topic-read 返回值获取，制品文件名由话题类型决定，见映射表）

2. **用户指定目录时，成功后发布到外部**：
   - 话题创建时或结束时，用户可指定 `output_dir`
   - 指定后通过 `topic-update` 保存: `python3 "$TOPIC_MANAGER" topic-update "$PWD" output_dir "<路径>"`
   - 结束时将制品从 artifacts/ 复制到用户指定目录

## 异常处理

### CodexMCP 不可用
如果 codex 工具不可用，所有命令将报错并提示安装：
```
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

### Agent 返回 error
- 展示 error 信息给用户
- 提示可选操作：重试 / 手动处理 / 放弃话题

### topic-manager.py 调用失败
- 检查 Python 3 是否可用
- 检查脚本路径是否正确
- 展示 stderr 错误信息

### 话题目录损坏
- meta.json 损坏：读取 summary.md 解析基本信息（标题、类型、轮次），调用 topic-create 重建话题
- summary.md 丢失：从 meta.json 读取元数据，用 Write 工具重建空的 summary.md 模板
- 这些恢复逻辑由 Skill 层（Claude Code）执行，topic-manager.py 本身不提供自动修复

### 预算耗尽
- 当 Agent 返回 `error: "budget_exhausted"` 时
- 保存当前进展（Agent 已在退出前更新 summary.md）
- 完成话题：`python3 "$TOPIC_MANAGER" topic-complete "$PWD"`
- 告知用户讨论因预算耗尽而终止，可用 `/cc-codex-review 继续` 恢复

## .gitignore 提示

首次运行时，检查项目 `.gitignore` 是否包含 `.cc-codex/`，如果没有则提示用户添加：
```
# CC-Codex 协作讨论运行时数据
.cc-codex/
```
