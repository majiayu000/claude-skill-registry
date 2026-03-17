---
name: parallel-vibe
description: 当用户明确要求"并行执行同一条 Vibe Coding 指令 / 多线程并行尝试多种方案 / 在多个独立工作区里同时推进"时使用。在用户当前工作目录创建 `.parallel_vibe/`，复制出多个独立工作区并按计划运行每个 thread 的 runner（默认串行、可选并行），最后在 `@main/summary.md` 汇总结果。⚠️ 不适用：用户只是想并行跑 shell 命令/单元测试/下载任务（应直接用并发工具或 CI）、没有明确"多工作区并行尝试/多方案对比"意图、要求强安全隔离或处理高度敏感数据（应使用容器/沙箱方案）。
metadata:
  author: Bensz Conan
  keywords:
    - parallel-vibe
    - parallel workspace
    - vibe coding
    - codex exec
    - claude -p
---

# parallel-vibe

## 你要做什么

把用户的一条指令，拆成多个 **thread（任务视角）**，并在多个**独立工作区（workspace）**与多个**独立进程（runner 子进程）**中执行：

- 每个 thread 只运行**一条终端命令**（例如 `codex ... exec "..."` 或 `claude ... -p "..."`），确保进程级独立
- 默认**串行**跑 threads（省资源、减少 API 限流/轮询风险）；用户明确要求时再并行
- 最终把每个 thread 的产物与日志落盘，并在 `@main/` 生成可追溯的计划与汇总

- `.parallel_vibe/{project_id}/{thread_id}/...`
- `.parallel_vibe/{project_id}/@main/summary.md`（综合汇总）

## 输入

- 必需：`prompt`（用户原始指令）
- 可选：`n`（线程数，默认 5，范围 1-9；用户明确要求则以用户为准）
- 可选：每个 thread 的 `runner/model/prompt`（通过 `@main/plan.json` 或 `--plan-file` 自定义）
- 可选：`--project-id/--resume`（复用已有 project 目录）
- 可选：`--parallel/--max-parallel`（用户明确要求并行时使用）

## 输出

你必须向用户返回：

- 本次运行的结果目录：`.parallel_vibe/{project_id}/`
- 如何查看汇总：`.parallel_vibe/{project_id}/@main/summary.md`

## 软护栏（必须遵守的操作规范；不是安全隔离）

当你在某个 thread 的 `workspace/` 内工作时：

- 只允许读写当前 `workspace/` 及其子目录
- 禁止访问父目录（`..`）与任何绝对路径写入
- 禁止读取/写入 `.parallel_vibe/{project_id}` 下的其他 thread 目录
- 产物必须落盘到当前 `workspace/`（便于追溯与汇总）

说明：`parallel-vibe` 提供的是“工程隔离”（减少相对路径污染与文件互相覆盖），不是容器/沙箱级的强安全隔离。默认拒绝 `--src-dir` 中的 symlink（可用 `--symlink-policy` 覆盖，但存在越界风险）；不要把包含敏感文件（如 `.env`、SSH key）的目录作为 `--src-dir`。

## 工作流

1. 从用户消息提取：
   - 用户指令原文 `prompt`
   - 线程数 `n`：用户明确要求则照做，否则默认 5
   - 是否要求并行：若未明确要求，默认串行
2. 规划 thread（启发式，必须落到“可执行命令”）：
   - 每个 thread 明确：`thread_id/title/runner/model/prompt`
   - **推荐路由**（默认策略）：
     - `claude`：规划/审查/风险与边界（强推理、强约束）
     - `codex`：实现/修改/测试与验证（代码落地）
   - **模型选择**：
     - 用 `profile=fast|deep|default` 表达“任务强度”，再由 `parallel-vibe/config.yaml:models` 映射到你本机可用的 `model_id`
     - 如你已经确定具体模型，也可在计划里直接写 `model=<model_id>` 覆盖 profile
3. 在用户当前目录运行脚本（不要手写编排逻辑）：

```bash
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
```

如果该 skill 已做系统级安装（推荐），脚本通常位于以下路径之一（按你当前平台选择）：

```bash
python3 ~/.codex/skills/parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
# 或
python3 ~/.claude/skills/parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
```

常见参数（按需添加）：

```bash
# 指定线程数（默认 5）
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --n 5

# 复用已有 project（便于重跑/续跑；每次运行仍会重建各 thread/workspace）
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --project-id <32位md5> --resume

# 只生成计划与工作区（不运行 threads），便于你先改 plan
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --plan-only

# 使用自定义 plan（JSON）
python3 parallel-vibe/scripts/parallel_vibe.py --plan-file /path/to/plan.json --src-dir . --out-dir .

# src_dir 存在 symlink 时的处理策略（默认 error 拒绝；skip 剔除；keep 保留为 symlink）
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --symlink-policy skip

# 用户明确要求并行时才开启（默认串行）
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --parallel --max-parallel 3
```

4. 打开并阅读汇总：
   - `.parallel_vibe/{project_id}/@main/summary.md`
5. 向用户交付：
   - 汇总结论（以 `@main/summary.md` 为准）
   - 指向每个 thread 工作区的路径（用户需要时可直接查看/对比）

## 自定义 thread（可选）

如需精确控制每个 thread 的 `runner/profile/model/prompt`，可直接编辑运行产物：

- `.parallel_vibe/{project_id}/@main/plan.json`

然后用同一个 `--project-id` + `--resume` 续跑。
注意：`--resume` 会复用 project 目录与 `@main/plan.json`，但每次运行仍会重建各 thread 的 `workspace/`（避免复用旧缓存导致不可追溯/不一致）。

⚠️ 安全提示：如计划中使用 `runner.type=shell`，它会执行你提供的任意命令模板（仅对受信任的 plan 使用）；并且 shell/工具本身可能读写用户全局缓存目录或访问绝对路径，因此不应将其理解为“安全沙箱”。

## Runner 命令形态（给规划用）

本 skill 的关键是假设 runner 支持“一条命令 = 一次独立执行”。

常见形态（以官方文档为准；具体参数以你本机 CLI 为准）：

```bash
# OpenAI Codex CLI（非交互执行）
codex -m <model_id> exec "你的指令内容"

# Claude CLI / Claude Code（打印模式）
claude --model <model_id> -p "你的指令内容"
```

## 清理方式

在触发目录执行：

```bash
rm -rf .parallel_vibe
```
