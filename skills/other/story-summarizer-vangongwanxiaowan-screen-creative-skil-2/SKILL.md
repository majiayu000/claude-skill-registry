---
name: story-summarizer
description: 基于故事文本提炼主要情节与要点，生成完整故事梗概。适用于快速了解故事内容、剧本改编、项目推介
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

# 故事梗概生成专家

## 功能

基于故事文本内容提炼主要情节与要点，生成完整的故事梗概。

## 使用场景

- 快速了解故事主要内容和情节发展。
- 为剧本改编或影视开发提供故事梗概。
- 制作项目推介材料的故事简介。
- 为后续深入分析提供故事概览。

## 核心步骤

1. **仔细阅读**: 仔细阅读故事文本，理解整体内容。
2. **主要情节识别**: 识别故事的主要情节线。
3. **要点提炼**: 提炼故事的关键要点。
4. **发展梳理**: 梳理故事的发展过程。
5. **梗概生成**: 生成完整的故事梗概。

## 输入要求

- **故事文本**: 完整的原始故事文本（小说、剧本、故事大纲等）。
- **文本长度建议**: 300字以上。

## 输出格式

```
【故事梗概】

【故事背景】
[描述故事发生的背景、环境设定等]

【主要情节】
[描述故事的主要情节发展]

【故事发展】
[按时间顺序描述故事的发展过程]

【关键转折点】
[描述故事中的关键转折点和重要变化]

【故事结局】
[描述故事的结局和最终状态]
```

## 约束条件

- 梗概要简洁完整，通常200-500字。
- 严格按照故事原文内容总结，不自行创作。
- 保持情节的准确性和完整性。
- 包含故事的核心要素：人物、事件、冲突、结局。

## 示例

参见 `{baseDir}/references/examples.md` 目录获取更多详细示例:
- `examples.md` - 包含不同类型故事（如爱情、职场、悬疑）的详细梗概示例。

## 详细文档

参见 `{baseDir}/references/examples.md` 获取关于故事梗概生成的详细指导与案例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；添加 allowed-tools (Read) 和 model (opus) 字段；优化功能、使用场景、核心步骤、输入要求、输出格式、要求等描述，使其更符合命令式语言规范；添加约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
