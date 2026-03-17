---
id: skill-factory
name: 技能工厂
version: 1.0.0
author: Yunshu
description: 元技能：用于快速生成新的标准技能模组。
icon: 🏭
color: "#607D8B"
tags: [system, meta, generator]
entry_point: tools.SkillFactory
workspace_root: ../
input:
  - name: skill_id
    type: text
    label: 技能ID (英文)
    placeholder: "例如: character_generator (使用下划线命名)"
    required: true
    default: ""
  
  - name: display_name
    type: text
    label: 显示名称
    placeholder: "例如: 角色生成器"
    required: true
    default: ""

  - name: description
    type: textarea
    label: 技能描述
    placeholder: "简要描述这个技能的功能..."
    required: true
    default: ""

  - name: template_type
    type: select
    label: 模板类型
    options:
      - label: 基础模板 (Basic)
        value: basic
      - label: 内容生成器 (Generator)
        value: generator
      - label: 数据处理器 (Data Process)
        value: data_process
    required: true
    default: "basic"
---

# 技能工厂说明

这是一个特殊的“元技能”，用于生产其他技能。

## 功能
- **自动创建目录**：在 `skills/` 目录下创建新的技能文件夹。
- **多模板支持**：支持生成基础、生成器、数据处理等不同类型的技能结构。
- **即时生效**：创建后刷新页面即可看到新技能。

## 使用方法
1. 输入 **技能ID**（如 `my_new_tool`）。
2. 输入 **显示名称**（如 `我的新工具`）。
3. 选择 **模板类型**。
4. 点击 **执行**。
