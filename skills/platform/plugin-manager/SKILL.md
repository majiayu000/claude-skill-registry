---
name: plugin-manager
description: "管理 Claude Code 插件。功能: 列出插件、查看详情、批量更新、备份配置、检查更新、导出列表。关键词: plugin, plugins, 插件, 更新, 备份, 管理"
---

# Plugin Manager Skill

通过自然语言管理 Claude Code 插件。

## 插件系统说明

Claude Code 的插件通过官方插件系统安装和管理：

### 存储位置
- **插件缓存**: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`
- **配置文件**: `~/.claude/plugins/installed_plugins.json`

### 更新机制
所有插件统一使用 `claude plugin update <plugin>` 命令逐个更新，不支持 `--all` 批量参数。

### 嵌套会话限制
`claude plugin update` 内部会启动 Claude Code 进程。在当前会话中直接调用会触发嵌套检测报错：
> Error: Claude Code cannot be launched inside another Claude Code session.

**解决方案:** 脚本执行前需 `unset CLAUDECODE` 环境变量以绕过嵌套检测。本技能的脚本已内置此处理，可在会话内正常使用。

## 触发条件

当用户提到以下内容时自动触发：
- "列出插件" / "list plugins" / "我有什么插件"
- "插件详情" / "plugin info" / "关于插件"
- "更新插件" / "update plugins" / "批量更新"
- "备份插件" / "backup plugins"
- "检查更新" / "check updates"
- "导出插件" / "export plugins"

## 使用方法

### 1. 列出所有插件

**触发词:** "列出插件", "我安装了什么插件", "list plugins"

**执行:**
```bash
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh list
```

### 2. 查看插件详情

**触发词:** "查看 [插件名] 详情", "plugin info [name]"

**执行:**
```bash
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh info <plugin-name>
```

### 3. 更新插件

**触发词:** "更新插件", "全部更新", "update plugins"

**执行:**
```bash
# 更新所有插件
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh update --all

# 更新指定插件
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh update <plugin-name>@<marketplace>
```

### 4. 检查更新

**触发词:** "检查插件更新", "有没有更新", "check updates"

**执行:**
```bash
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh check-updates
```

### 5. 备份配置

**触发词:** "备份插件", "backup plugins"

**执行:**
```bash
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh backup
```

### 6. 导出列表

**触发词:** "导出插件列表", "export plugins"

**执行:**
```bash
~/.claude/skills/plugin-manager/scripts/plugin-manager.sh export
```

## 响应格式

执行命令后，提供简洁的结果摘要：

- "你安装了 10 个插件，按来源分组如下: [输出]"
- "插件 xxx 版本 v1.0.0，安装于 2026-01-20"
- "检查完成: 2 个有更新，8 个已是最新"
- "配置已备份到 ~/.claude/backups/plugins_backup_xxx.json"

## 注意事项

- 更新后需要重启 Claude Code 才能生效
- 备份文件保存在 `~/.claude/backups/` 目录
- `claude plugin update` 不支持 `--all` 参数，必须逐个指定插件名称（格式: `<plugin>@<marketplace>`）
- 脚本已内置 `unset CLAUDECODE` 处理，无需手动绕过嵌套会话限制