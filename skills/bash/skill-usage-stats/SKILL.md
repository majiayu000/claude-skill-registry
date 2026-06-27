---
name: skill-usage-stats
description: >-
  扫描本机 Claude Code 和 Codex 的会话日志，统计哪些 skill 有本地调用证据、哪些在本机无证据（已安装但日志无痕迹，不等于从未使用）、调用排行、月度趋势、项目分布，输出终端表格和 Markdown 报告，可导出 CSV/JSON。Use when the user asks to 统计 skill 使用, 看 skill usage, find zombie skills, 僵尸 skill, which skills are installed but never used, skill 调用排行, skill usage report, skill 使用健康度, audit personal skill arsenal, or manage which skills to keep or remove.
---

# Skill 使用统计

## 概览

扫描本机 Claude Code（`~/.claude/projects`）和 Codex（`~/.codex/sessions`）的会话日志，回答"我的 skill 哪些在用、哪些是僵尸、用量怎么变化"，输出终端表格 + Markdown 报告，可附 CSV / JSON。

- **Claude**：结构化 `Skill` 工具调用，100% 精确。
- **Codex**：skill 不是原生工具，"调用" = 一条 `exec_command` 用 sed/cat 读 `skills/<名>/SKILL.md`，靠路径正则识别，约 95% 精度。

性能：ripgrep（`rg --json`）预过滤十几 GB 的 Codex 日志，只解析命中行；无 rg 时自动回退到 Python 扫描（`--no-rg` 强制）。

## 语言选择（重要）

报告语言用 `--lang` 控制。**请根据用户当前提问使用的语言选择**：

- 用户用**中文**提问（如"统计 skill 使用"、"僵尸 skill"、"看看哪些没用"）→ `--lang zh`（默认）
- 用户用**英文**提问（如 "skill usage"、"zombie skills"）→ `--lang en`

默认 `--lang zh`。不确定时，与用户本轮对话的语言保持一致。

## 何时使用

用户说以下任一时触发本 skill：

- 统计 skill 使用 / 看 skill 使用情况 / skill 用得多不多
- skill usage / skill usage report / skill usage stats
- 僵尸 skill / zombie skill / 哪些 skill 从没用过 / never used
- skill 调用排行 / 最常用的 skill / Top skill
- skill 使用健康度 / 个人 skill 武库 / audit my skills

## 如何运行

脚本随 skill 安装位置运行。优先使用当前 runtime 的安装路径：Codex 通常是 `~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py`，Claude Code 通常是 `~/.claude/skills/skill-usage-stats/scripts/skill_usage_report.py`，仓库开发时也可用 `skills/skill-usage-stats/scripts/skill_usage_report.py`。按用户语言带上 `--lang`：

```bash
# 默认：扫 Claude + Codex，top 20，Codex 按会话去重，中文报告
python3 ~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py --lang zh

# 近几个月（同时收窄 Codex 的 sessions/YYYY/MM 扫描范围，提速）
python3 ~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py --lang zh --since 2026-06 --top 30

# Codex 每次 sed 读取都算（默认按会话去重）
python3 ~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py --codex-mode call

# 导出 CSV / JSON
python3 ~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py --csv ~/skill-usage.csv --json ~/skill-usage.json

# 英文报告
python3 ~/.agents/skills/skill-usage-stats/scripts/skill_usage_report.py --lang en
```

参数：`--lang {zh,en}`（默认 zh）、`--top N`、`--since YYYY-MM`、`--out PATH`（`-` 为 stdout）、`--csv PATH`、`--json PATH`、`--codex-mode {call,session}`（默认 session）、`--no-claude`、`--no-codex`、`--installed-dirs`、`--no-rg`、`--quiet`。

## 默认流程

1. 按用户语言选 `--lang`（中文用户用 `zh`，默认）。
2. 跑脚本，读终端表格给出 Top-N 和僵尸数。
3. 指向写出的 Markdown 报告（默认 `~/skill-usage-report-YYYYMMDD.md`）看完整僵尸清单、月度趋势、项目分布。
4. 用户问"哪些能删"时，"无本地证据"清单是候选——但注意它不等于"没用过"，删除前要逐个确认，本 skill 不会自动删。

## 输出解读

终端表格列（表头保留英文以保证等宽对齐）：

| 列 | 含义 |
|---|---|
| SKILL | skill 名 |
| CLAUDE / CODEX | 各 runtime 调用数 |
| TOTAL | CLAUDE + CODEX |
| LAST | 最近调用日期 |
| PROJECTS | 涉及的不同项目数 |
| RUNTIME | claude / codex / both |

**无本地证据的 skill** = 已安装（在 `~/.claude/skills`、`~/.agents/skills` 或旧 Codex 路径 `~/.codex/skills`）但本机日志无任何调用痕迹。注意：这只是"本机无证据"，**不等于从未使用**——Codex 的权威调用记录（`skill_invocation` analytics）POST 到后端、不存本机。

Codex 口径（两个模式数字可能差很多）：

- `session`（默认）：每个 (skill, 会话) 计一次，同一会话内反复读取不重复计数——更接近"多少会话用过"。
- `call`：每次读取都算，反映原始读取频率，单次会话可能很高。

## 注意事项

- Codex 是路径正则启发式（约 95%）：非 skill 的 sed/cat 读到 `SKILL.md` 会被计入；Codex 原生 skill 调用（若存在）不可见。Claude 精确。
- **证据局限**：Codex 数字只是 implicit 证据（sed/cat 读 SKILL.md）。本机上 `$skill` mention 和 skill 脚本运行约为 0。这不是权威调用计数——Codex 的 `skill_invocation` analytics 直接 POST 后端、不存本机。所以"无本地证据"只表示本机没痕迹，**不等于"从未使用"**。
- 首次全量扫 Codex（十几 GB）可能要几十秒；`--since` 按每条日志时间过滤计数。
- 已装集合默认跟随启用的 runtime：Claude 用 `~/.claude/skills`，Codex 用 `~/.agents/skills`（当前 Codex）+ `~/.codex/skills`（旧 Codex）；`--installed-dirs` 可改。
- 本工具只读，绝不修改日志、skill 或配置。僵尸清单不等于删除指令，删前请逐个确认。
