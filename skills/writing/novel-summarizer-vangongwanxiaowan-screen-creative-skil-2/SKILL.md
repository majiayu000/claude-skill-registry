---
name: novel-summarizer
description: 阅读理解小说文本，总结成流畅的故事大纲。适用于小说初筛选、生成500-800字故事大纲
category: novel-screening
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
        content: 优化功能、使用场景、核心能力、工作流程、约束条件、输出格式的描述，使其更符合命令式语言规范
      - type: added
        content: 添加示例和详细文档部分
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

# 故事大纲生成专家（小说版）

## 功能

阅读理解故事文本，总结成流畅的故事大纲，字数控制在500-800字之间。

## 使用场景

- 对小说文本进行初筛选，快速了解故事梗概。
- 生成规范化的故事大纲，为后续创作提供基础。
- 快速掌握故事的核心人物、关系、事件和情节。

## 核心能力

- **准确总结**: 准确总结故事文本中的人物、人物关系、人物行动与事件情节。
- **叙事转换**: 以第三人称视角进行准确总结。
- **复杂关系处理**: 理解并准确总结复杂的人物身份与人物关系。
- **语言表达**: 运用优美准确的语言总结故事梗概。

## 工作流程

1. **深入阅读**: 深入阅读故事文本，准确理解人物、人物关系与事件情节。
2. **总结生成**: 根据阅读内容，将故事文本总结为一篇行文流畅的故事大纲。

## 约束条件

- **字数控制**: 严格控制总结字数在500-800字之间。
- **内容准确性**: 严格按照文本原文总结，不进行自行创作或改编。
- **格式要求**: 直接输出总结文本内容，不带任何标题。

## 输出格式

直接输出流畅的文字总结故事大纲。

## 示例

参见 `{baseDir}/references/examples.md` 目录获取更多详细示例:
- `examples.md` - 详细总结示例（都市爱情、古言、重生复仇等不同类型）

## 详细文档

参见 `{baseDir}/references/examples.md` 获取关于小说总结的详细指导与案例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；添加 allowed-tools (Read) 和 model (opus) 字段；优化功能、使用场景、核心能力、工作流程、约束条件、输出格式的描述，使其更符合命令式语言规范；添加示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |

