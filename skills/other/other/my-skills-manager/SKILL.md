---
name: my-skills-manager
description: 管理本地 skills 仓库（添加 / 删除 / 修改 / 同步 skills）；触发条件：需要在 `~/.my-skills-collection` 中管理技能、同步远端或安装到 AI agent 的 skills 目录时使用。
---

## 概要（精简）

本技能用于在本地 skills 仓库 `~/.my-skills-collection` 中：
- 添加或移除 skill（支持作为 submodule 或直接复制）
- 同步仓库并更新 submodule
- 安装/准备 skills 供 AI agent 使用（提示安装步骤）

## 何时使用

- 需要将第三方或自制 skill 加入到本地 skills 仓库
- 需要从远端拉取最新的 skills 或更新子模块
- 需要删除不再使用的 skill

## 快速命令（推荐使用 scripts 下的工具）

创建并添加 skill（作为子模块）：

```bash
python skills/my-skills-manager/scripts/add_skill.py --submodule <git-url> --name <skill-name>
```

复制本地 skill 目录到仓库：

```bash
python skills/my-skills-manager/scripts/add_skill.py --copy /path/to/skill --name <skill-name>
```

删除 skill：

```bash
python skills/my-skills-manager/scripts/remove_skill.py --name <skill-name>
```

同步仓库并更新所有子模块：

```bash
python skills/my-skills-manager/scripts/sync_repo.py
```

## 参考文件

- `reference/add-skills.md` — 添加 skill 的详细步骤
- `reference/remove-skills.md` — 删除 skill 的详细步骤
- `reference/sync-skills.md` — 同步仓库的详细步骤

## 脚本（已包含）

- `scripts/add_skill.py` — 添加 skill（支持 submodule 或复制）
- `scripts/remove_skill.py` — 删除 skill（处理 submodule 与普通目录）
- `scripts/sync_repo.py` — 安全地同步仓库并更新子模块

在执行脚本前，脚本会提示确认操作以避免误删或未保存的改动。
