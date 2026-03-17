---
name: clawdbot-backup
description: "Backup and restore ClawdBot configuration, skills, commands, and settings. Sync across devices, version control with git, automate backups, and migrate to new machines."
license: MIT
metadata:
  version: 1.0.0
  domains: [backup, sync, migration, version-control]
  type: utility
---

# ClawdBot 备份与恢复

## 当使用此技能

- 备份配置和技能
- 跨设备同步
- 迁移到新机器
- 版本控制管理

## 备份内容

- 配置文件 (openclaw.json, agents config)
- Skills 目录
- 自定义命令
- 记忆文件 (MEMORY.md, daily logs)

## 同步方式

1. **Git 仓库**: 推送到 GitHub/GitLab
2. **自动化**: 定时自动备份
3. **手动**: 按需备份

## 迁移流程

1. 导出备份
2. 传输到新设备
3. 导入配置
4. 验证功能

## 触发词

- "备份配置"
- "同步 skills"
- "迁移到新机器"
- "导出配置"
