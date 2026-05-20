---
name: install-bensz-skills
category: normal
description: "当需要把本仓库 pipelines/skills 下的所有 skills 安装到系统级（默认同时安装到 Codex: ~/.codex/skills 和 Claude Code: ~/.claude/skills），以便在任意项目/对话中可被发现与调用时使用。使用 MD5 哈希进行版本控制，仅安装有更新的 skills；支持强制覆盖安装、指定单一目标安装和远程安装模式（--remote --check/--auto）。"
metadata:
  author: Bensz Conan
  keywords:
    - install-bensz-skills
---

# Install Bensz Skills（系统级安装器）

目的：把当前仓库 `pipelines/skills/` 中的所有 skills（**包括 install-bensz-skills 自身**）**复制安装**到：

- Codex：`~/.codex/skills/`
- Claude Code：`~/.claude/skills/`

从而让这些 skills 在**任意项目**里都能被发现与触发（不依赖当前 workdir，也不使用软链接）。

## 安装模式

### 本地安装模式（默认）

直接从本地仓库安装 skills。

### 远程安装模式

从远程 GitHub 仓库下载并安装 skills，支持交互式确认和自动强制安装。

#### 远程安装前置条件

- 本地已安装 Git（`git --version` 可用）
- 具备 PyYAML 依赖（`python3 -m pip install pyyaml`）

## 你要做的事（触发后必须执行）

执行时不要先做 `test -f ./install-bensz-skills/...` 之类的“脚本存在性检测”。直接运行安装脚本即可；若当前项目目录没有 `install-bensz-skills/`，就改用系统级已安装位置（`~/.codex/skills/` 或 `~/.claude/skills/`）的脚本运行，并在需要时用 `--source` 显式指定源目录。

### 本地安装

1) 运行安装脚本：

```bash
# 默认：同时安装到 Codex 和 Claude Code（仅安装有更新的）
# 说明：脚本会优先从当前目录自动识别 skills 源目录（支持 ./pipelines/skills、./skills、或当前目录本身）
python3 install-bensz-skills/scripts/install.py

# 仅安装到 Claude Code
python3 install-bensz-skills/scripts/install.py --claude

# 仅安装到 Codex
python3 install-bensz-skills/scripts/install.py --codex

# 强制重新安装所有 skills（忽略版本检查）
python3 install-bensz-skills/scripts/install.py --force

# 预览模式（不实际安装）
python3 install-bensz-skills/scripts/install.py --dry-run

# 指定额外 skills 源目录
python3 install-bensz-skills/scripts/install.py --source /path/to/skills

# 多个源目录（逗号分隔）
python3 install-bensz-skills/scripts/install.py --source /path/skills-a,/path/skills-b
```

如果你在某个项目目录里只有 `skills/`（没有 `install-bensz-skills/`），但安装器已被系统级安装（通常在 `~/.codex/skills/` 或 `~/.claude/skills/`），可直接运行系统级脚本：

```bash
# Codex 安装位置（优先）
python3 ~/.codex/skills/install-bensz-skills/scripts/install.py

# 或 Claude Code 安装位置
python3 ~/.claude/skills/install-bensz-skills/scripts/install.py

# 若无法自动识别源目录，则显式指定
python3 ~/.codex/skills/install-bensz-skills/scripts/install.py --source ./skills
```

### 远程安装

**交互式检查模式**（`--remote --check`）：

```bash
# 检查并交互式安装远程技能
python3 install-bensz-skills/scripts/install.py --remote --check

# 仅对 Claude Code 执行远程检查
python3 install-bensz-skills/scripts/install.py --remote --check --claude

# 仅对 Codex 执行远程检查
python3 install-bensz-skills/scripts/install.py --remote --check --codex
```

流程：
1. 创建临时目录 `~/.install-bensz-skills/tmp-remote-install`
2. 询问是否安装每个远程源（根据配置文件）
3. 下载远程技能到临时目录
4. 与本地已安装技能对比，生成更新报告
5. 询问是否确认安装/更新
6. 执行安装/更新
7. 清理临时目录

**自动强制模式**（`--remote --auto`）：

```bash
# 自动下载并强制安装所有远程技能（无确认）
python3 install-bensz-skills/scripts/install.py --remote --auto

# 仅对 Claude Code 执行自动安装
python3 install-bensz-skills/scripts/install.py --remote --auto --claude
```

流程：
1. 创建临时目录
2. 直接下载所有远程技能（无确认）
3. 强制安装/更新（无对比，无确认）
4. 清理临时目录

### 验证

建议在任意其它目录执行：

```bash
codex exec "列出所有可用的技能"
```

## MD5 版本控制机制

脚本使用 **MD5 哈希值**进行智能版本控制：

- **版本计算**：对 skill 目录内的可安装文件进行 MD5 计算（排除 `tests/`、`plans/`、缓存与临时文件）
- **版本存储**：安装后在目标目录生成平台特定 manifest（`.skill-manifest.{codex,claude}.json`）记录版本信息
- **智能安装**：
  - ✅ **已安装且版本未变**：跳过，不重复安装
  - ✅ **版本已变化**：强制覆盖安装
  - ✅ **新 skill**：直接安装

### 安装报告示例

```
============================================================
📦 正在安装到 CLAUUDE: /Users/xxx/.claude/skills
============================================================

【安装过程】
────────────────────────────────────────────────────────────
installed: /Users/xxx/.claude/skills/nsfc-bib-manager

【安装摘要】
────────────────────────────────────────────────────────────
┌────────────────────────┬──────────────┬─────────────────┐
│ Skill 名称              │ 状态         │ 原因            │
├────────────────────────┼──────────────┼─────────────────┤
│ nsfc-bib-manager        │ ✅ 已安装    │ 版本已更新...  │
│ git-commit              │ ⏭️  跳过     │ 版本未变化     │
└────────────────────────┴──────────────┴─────────────────┘

【辅助技能（已忽略，仅用于开发）】(1 个)
   • install-bensz-skills ⏭️ 跳过

────────────────────────────────────────────────────────────
📊 统计
────────────────────────────────────────────────────────────
普通技能: 1 个已安装, 1 个跳过

============================================================
🎯 总体安装摘要
============================================================

总计数:
  • 已安装/更新: 1 个
  • 跳过: 1 个
```

**注**：完整报告格式规范见 [references/install-report-template.md](references/install-report-template.md)。

## 安装策略（脚本保证）

- 仅安装"包含 `SKILL.md` 的目录"（即每个 skill 的根目录）。
- **技能类型控制**：通过 SKILL.md 中的 `category` 字段控制（`normal` 可安装，`auxiliary` 和 `test` 不安装）。
- **MD5 版本检查**：优先检查 `.skill-manifest.{codex,claude}.json`，回退到重新计算
- **直接替换**：发现到目标路径已存在同名目录且版本变化时，直接删除旧版本并安装新版本（不备份）
  - 理由：Git 已提供版本控制，可随时回退；新版本通常比旧版本更好
- 若存在旧的 `pipeline-skills` 软链接：会移除该软链接（不删除真实目录）。

## 命令行参数

### 本地安装参数

| 参数 | 说明 |
|------|------|
| `--dry-run` | 预览模式，不实际写入文件 |
| `--codex` | 仅安装到 Codex |
| `--claude` | 仅安装到 Claude Code |
| `--force` | 强制重新安装所有 skills（忽略 MD5 检查） |
| `--source` | 指定额外的 skills 源目录路径 |

### 远程安装参数

| 参数 | 说明 |
|------|------|
| `--remote` | 启用远程安装模式（必须与 `--check` 或 `--auto` 一起使用） |
| `--check` | 检查模式（交互式确认后再安装） |
| `--auto` | 自动模式（强制安装，无需确认） |
| `--{id}` | 仅安装指定远程源（如 `--general`、`--research`） |

**参数组合**：
- `--remote --check`：交互式远程安装
- `--remote --auto`：自动强制远程安装
- `--remote --check --codex`：仅对 Codex 执行远程检查
- `--remote --check --claude`：仅对 Claude Code 执行远程检查
- `--remote --check --general`：仅检查并安装 general 源

### 远程源配置

远程技能源通过 `config.yaml` 配置文件定义：

```yaml
# install-bensz-skills/config.yaml
remote_sources:
  - id: "general"
    name: "通用技能"
    url: "https://github.com/huangwb8/skills"
    branch: "main"
    skills_path: "skills"
    description: "通用技能，建议所有用户安装"
    recommended: true

  - id: "research"
    name: "科研技能"
    url: "https://github.com/huangwb8/ChineseResearchLaTeX"
    branch: "main"
    skills_path: "skills"
    description: "科研相关技能，建议有科研需要的用户安装"
    recommended: false
```

配置字段说明：
- `id`：源 ID（用于 `--{id}` 过滤）
- `name`：源名称（用于显示和提示）
- `url`：Git 仓库 URL
- `branch`：分支名称（默认 `main`）
- `skills_path`：技能目录相对于仓库根目录的路径
- `description`：源描述（用于提示用户）
- `recommended`：是否推荐安装（影响默认提示行为）

## 常见问题

### 本地安装

- **如果你刚更新了本仓库的技能**：再次触发本 skill 运行脚本即可完成系统级更新（仅安装有变化的）。
- **需要强制重装**：使用 `--force` 参数。
- **Claude Code / Codex 都需要新会话**才会重新加载更新后的技能；安装后建议新建会话验证。
- **如何回退到旧版本**：使用 Git 回退源代码后，重新运行安装脚本即可（不备份旧版本）。

### 远程安装

- **如何添加新的远程源**：编辑 `config.yaml`，在 `remote_sources` 数组中添加新的源配置。
- **远程安装失败**：检查网络连接和 Git 是否安装。某些网络环境可能需要配置代理。
- **临时目录未清理**：手动删除 `~/.install-bensz-skills/tmp-remote-install` 目录。
- **远程技能与本地冲突**：远程安装会覆盖本地同名技能，建议先备份或使用 `--check` 模式预览变更。
