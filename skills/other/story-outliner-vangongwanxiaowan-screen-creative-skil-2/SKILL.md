---
name: story-outliner
description: 阅读理解故事文本，总结人物、关系、情节，整理成流畅大纲。适用于快速了解故事核心、为剧本创作提供大纲基础
category: story-analysis
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: 宫凡
allowed-tools:
  - Read
model: opus
changelog:
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: 优化 description 字段，使其更精简并符合命令式语言规范
      - type: added
        content: 添加 allowed-tools (Read) 和 model (opus) 字段
      - type: improved
        content: 优化功能、使用场景、核心步骤、输入要求、输出格式、要求等描述，使其更符合命令式语言规范
      - type: added
        content: 添加约束条件、示例和详细文档部分
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: 按照 Agent Skills 官方规范重构
      - type: improved
        content: 优化 description，使用命令式语言，精简主内容
      - type: added
        content: 添加 license、compatibility 可选字段
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 故事大纲生成专家

## 功能

深入阅读理解故事文本，总结人物、人物关系、情节，整理成流畅的故事大纲。

## 使用场景

- 快速了解故事的核心内容和结构。
- 为剧本创作提供故事大纲基础。
- 制作项目申报或推介材料。
- 为故事评估和改编提供概览。

## 核心步骤

1. **深入阅读**: 深入阅读故事文本，准确理解故事中的人物、人物关系与事件情节。
2. **信息提取**: 提取主要人物、人物关系及关键情节。
3. **结构整理**: 按照故事发展的逻辑整理信息，构建大纲框架。
4. **大纲撰写**: 将故事总结为一篇行文流畅的故事大纲。

## 输入要求

- **故事文本**: 完整的原始故事文本（支持第一人称或第三人称叙事）。
- **文本长度建议**: 300字以上。

## 输出格式

直接输出流畅的文字总结故事大纲，不带任何标题。

## 约束条件

- **字数控制**: 严格控制总结字数在300-500汉字之间。
- **内容准确性**: 严格按照文本原文总结，不进行自行创作或改编。
- **人称统一**: 用第三人称进行总结（即使原文是第一人称）。
- **格式要求**: 直接输出正文，不带任何标题。
- **避免评述**: 不对文本内容做总结性或评述性概述。

## 示例

参见 `{baseDir}/references/examples.md` 目录获取更多详细示例:
- `examples.md` - 包含不同叙事视角（第一人称、第三人称）和复杂人物关系的故事大纲示例。

## 详细文档

参见 `{baseDir}/references/examples.md` 获取关于故事大纲生成的详细指导与案例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；添加 allowed-tools (Read) 和 model (opus) 字段；优化功能、使用场景、核心步骤、输入要求、输出格式、要求等描述，使其更符合命令式语言规范；添加约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
