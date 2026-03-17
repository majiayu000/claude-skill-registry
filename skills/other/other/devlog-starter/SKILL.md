---
name: ai-architect-lite
description: Lightweight playbook distilled from AI Architecture to keep dual-engine memory (.ai_context) and manifest dispatcher with minimal overhead; use when bootstrapping or porting the pattern into Claude Skills format.
---

# AI Architect Lite
> 精简版「AI Architecture」：保留 `.ai_context` 记忆协议与 manifest 驱动调度，服务轻量项目或快速移植场景。

## 适用场景
- 新建/迁移仓库，希望用最小开销引入 `.ai_context` + slash-first 调度。
- 需要统一开发日志格式，但不启用完整 Pro 协议。
- 想把 AI Architect 的初衷以 Claude Skill 形式交付，供其他会话直接加载。

## 快速上手
1. 解析路径：`PROJECT_ROOT` = 当前仓库；`TOOLKIT_PATH` = 本技能所在目录（用于引用资源）。
2. 检查 `PROJECT_ROOT/.ai_context/03_ACTIVE_TASK.md`；缺失则按 `references/lite-protocol.md` 模板创建或运行 `python skills/project-init/entrypoint.py`。
3. 阅读 `03_ACTIVE_TASK.md` 获取 Current Mission；若存在 `01/02` 则作为补充规则加载，不强制解析全部细节。
4. 查看 `.ai-manifest.json`：优先使用 `commands` 中的 slash 触发；若无 `cognitive_skills` 配置，则保持纯命令模式。
- 新手护栏：若拿不准流程，先快速浏览 `references/superpowers-lite.md`，按其“迷你 TDD”“快速执行模板”走一遍。
- 仅本技能加载时的默认动作：先输出友好欢迎语，告诉用户你已启用 AI Architect Lite，并给出 3 个可选下一步（如：① 生成迷你计划 `python scripts/plan_helper.py ...`；② 填写/创建 `.ai_context/03_ACTIVE_TASK.md`；③ 用 `scripts/append_log.py` 记录第一次动作）。

## 工作流程（Loop）
- **Dispatcher 次序**：Slash > Intent（可选）> 普通对话；未命中技能时按当前任务回答。
- **迷你流程（面向新手）**：用 3 步走完——① 写目标/约束/<=5 步计划（可直接在回答里列出，或运行 `python scripts/plan_helper.py --goal \"...\" --steps \"...\" --validation \"...\" --out -` 获取模板）；② 先写“会失败”的验证点（命令或检查点），再动手；③ 完成后按验证点复跑并记录结果。
- **日志写入**：优先运行 `python scripts/append_log.py --note "..." --action "..." --changes "..." --outcome "..." --next "..."`（随技能提供的最小脚本，默认在项目根执行并自动创建 `.ai_context/03_ACTIVE_TASK.md`）。若项目已有通用 `skills/memory-sync/entrypoint.py`，可直接复用；两者都不可用时在 `03_ACTIVE_TASK.md` 手动追加四段式记录。
- **范围与安全**：仅操作 `PROJECT_ROOT`；执行前用中文说明修改/命令目的与影响，避免写入密钥。
- **上下文收敛**：长文档/规范放入 `references/`，按需加载；核心指令保持在本文件。

### 默认问候模板（仅单独加载本技能时使用）
```
嗨，我是 AI Architect Lite（目前只加载了我）。为了让你轻松上手，我们可以从这三步选一：
1) 想清楚要做什么：用“迷你计划”列出目标、3 步以内的行动、以及如何确认完成（好处：先定方向，少走弯路）。
2) 准备一本“任务笔记”：如果没有 .ai_context/03_ACTIVE_TASK.md，就按 references/lite-protocol.md 的格式建一个，记录当前任务和进展（好处：状态清晰，随时可查）。
3) 留下一条“开工日志”：用 scripts/append_log.py 记下你做的第一步和结果（好处：有迹可循，方便回顾或求助）。
告诉我你的目标，或者直接挑一条开始，我会陪你一步步完成。
```

## 资源使用
- `references/lite-protocol.md`：`.ai_context` 最小规范、开发日志模板、slash-first 调度要点。
- `references/superpowers-lite.md`：超能力精简卡，涵盖迷你 TDD、系统化调试和透明协作的最小做法。
- `scripts/append_log.py`：为新手准备的最小日志脚本，自动建文件并按模板追加；可作为示例扩展。
- `scripts/plan_helper.py`：生成目标/约束/步骤/验证的极简计划模板，默认输出到终端，避免额外文件。
- `assets/`：保留占位，用于未来模板/示例；当前无需加载到上下文。

## 示例日志片段
```markdown
### [2025-11-21 10:00] Action: 初始化 lite 协议
- Changes: 创建 .ai_context/03_ACTIVE_TASK.md；检查 .ai-manifest.json
- Outcome: 完成；未运行测试
- Next: 按当前任务执行并在每步后同步日志
```
