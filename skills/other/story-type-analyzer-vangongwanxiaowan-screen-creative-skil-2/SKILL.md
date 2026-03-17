---
name: story-type-analyzer
description: 分析故事题材类型，提炼创意元素与故事特色。适用于识别题材定位、提炼创意、分析市场受众
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
  - version: 2.2.0
    date: 2026-01-11
    changes:
      - type: improved
        content: 添加 references/guide.md 引用，完善详细文档部分
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: 优化 description 字段，使其更精简并符合命令式语言规范
      - type: added
        content: 添加 allowed-tools (Read) 和 model (opus) 字段
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
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 题材类型与创意提炼专家

## 功能

分析故事题材类型，提炼创意元素，识别故事特色和风格特点。

## 使用场景

- 识别故事的核心题材和类型定位，明确市场方向。
- 提炼故事的独特创意元素，增强作品吸引力。
- 分析故事的市场定位和受众群体，指导宣发策略。
- 为故事改编和商业化提供深度参考依据。

## 核心步骤

1. **题材识别**: 分析故事的主要题材类型和次要题材元素。
2. **创意提炼**: 识别并提炼故事中的核心创意元素与创新点。
3. **特色分析**: 分析故事的独特性、创新点及风格特征。
4. **风格解读**: 解读故事的叙事风格和艺术特色，把握作品基调。
5. **价值评估**: 综合评估题材的商业价值与艺术价值。

## 输入要求

- **故事文本/大纲/梗概**: 完整的原始故事文本、大纲或梗概。
- **文本长度建议**: 500字以上。

## 输出格式

```
【题材类型分析】
- 主导题材：[题材类型]
- 辅助题材：[题材类型1、题材类型2]
- 题材融合度：[高/中/低]

【创意元素提炼】
1. 核心创意：[描述最核心的创意元素]
2. 创新点1：[具体描述]
3. 创新点2：[具体描述]

【故事特色】
- 设定特色：[描述故事的设定特点]
- 叙事特色：[描述叙事手法的特色]

【题材价值】
- 商业价值：[评估商业潜力]
- 艺术价值：[评估艺术特色]
```

## 约束条件

- 分析结果需忠实于原始故事文本，不进行主观臆断。
- 题材分类需准确，创意提炼要精炼。
- 价值评估需客观，给出具体理由。

## 示例

请参见 `{baseDir}/references/examples.md` 获取详细分析示例。

## 详细文档

参见 `{baseDir}/references/` 目录获取更多文档:
- `guide.md` - 完整分析指南和定义说明
- `examples.md` - 更多场景示例

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；添加 allowed-tools (Read) 和 model (opus) 字段；优化功能、使用场景、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范；添加约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
