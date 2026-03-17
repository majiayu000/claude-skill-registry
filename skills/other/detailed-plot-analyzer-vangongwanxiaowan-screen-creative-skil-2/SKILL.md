---
name: detailed-plot-analyzer
description: 基于大情节点，深入分析并生成详细情节点描述及情节发展说明。适用于细化故事大纲、指导剧本写作、分析情节内在逻辑
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
      - type: changed
        content: 模型更改为 opus
      - type: improved
        content: 优化功能、使用场景、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范
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
      - type: added
        content: 添加 allowed-tools (Read) 和 model 字段
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 详细情节点分析专家

## 功能

基于大情节点，深入分析并扩展，生成详细的情节点描述及情节发展说明。

## 使用场景

- 细化和扩展故事大纲。
- 为剧本写作提供详细的情节指导。
- 分析情节发展的内在逻辑。
- 发现情节设计中的问题和优化空间。

## 核心步骤

1. **理解核心要素**: 仔细分析大情节点内容，理解每个情节点的核心要素。
2. **深入扩展**: 对每个情节点进行深入分析，生成详细的情节描述。
3. **逻辑分析**: 分析情节点之间的逻辑关系和发展脉络。
4. **提供建议**: 提供情节发展的详细说明和优化建议。

## 输入要求

- 已提炼的大情节点列表
- 原始故事文本（可选，用于参考）
- 特定分析需求（可选）

## 输出格式

```
【详细情节点分析】

【情节点1】：大情节描述
- 核心要素：关键要素分析
- 人物行为：人物行为分析
- 情节发展：情节发展说明
- 逻辑关系：与其他情节点的关系

【情节点2】：大情节描述
- 核心要素：关键要素分析
- 人物行为：人物行为分析
- 情节发展：情节发展说明
- 逻辑关系：与其他情节点的关系
...

【情节发展总结】
整体情节发展的总结和建议
```

## 约束条件

- 每个详细情节点的描述控制在200-300字。
- 严格按照大情节点的内容进行分析，不自行创作。
- 保持情节发展的逻辑性和连贯性。
- 避免重复和冗余的描述。

## 示例

请参见 `{baseDir}/references/examples.md` 获取更多详细示例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，添加 allowed-tools 和 model 字段，调整主内容语言风格，并引导至 references/examples.md |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
