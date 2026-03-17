---
name: scaffold-skill
description: 系统初始化脚手架。用于在新项目中克隆和初始化 sop-engine 内核。
trigger: initialize system, scaffold project, clone engine
---

# Scaffold Skill (脚手架)

负责将 sop-engine 的核心组件（Runtime, Core Skills）克隆到新的项目目录中，使其成为一个独立的自包含系统。

## 输入
- `target_path`: 目标项目路径（相对或绝对）
- `system_name`: 系统名称

## 输出
- `result`: 包含初始化状态和克隆的文件列表

## 流程
1. 检查目标目录是否存在，不存在则创建
2. 复制 `.sop-engine/runtime`
3. 复制 `.claude/skills` (Core Skills)
4. 初始化 `.claude/agents`
5. 创建基础配置文件 (`CLAUDE.md`, `config.sh`)
