---
name: mind-map-generator
description: 调用generateTreeMind工具创建可视化思维导图，返回图片URL和编辑链接。适用于故事结构可视化、情节关系图谱展示
category: tools
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: 宫凡
allowed-tools: []
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
        content: 优化功能、核心能力、输入要求、输出格式的描述，使其更符合命令式语言规范
      - type: added
        content: 添加使用场景、约束条件、示例和详细文档部分
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

# 思维导图生成专家

## 功能

调用 `generateTreeMind` 工具创建可视化思维导图，并提供图片URL和编辑链接。

## 使用场景

- **故事结构可视化**: 将复杂的故事大纲、情节点或人物关系转化为直观的思维导图，帮助用户快速理解和梳理。
- **情节关系图谱展示**: 通过图形化方式展示人物关系、事件发展脉络，便于分析和设计。
- **创作思路整理**: 辅助创作者整理和发散创意，将零散的想法组织成结构化的思维导图。
- **团队协作与分享**: 生成可编辑的思维导图链接，方便团队成员共同协作和迭代。

## 核心能力

- **思维导图生成**: 调用 `generateTreeMind` API，将文本内容（如大纲、列表、自由文本）转化为结构化思维导图。
- **可视化展示**: 提供生成的思维导图图片URL，支持在线预览、下载和嵌入。
- **编辑链接提供**: 为生成的思维导图提供在线编辑链接，允许用户进行二次修改和定制。
- **API 调用管理**: 有效管理 `generateTreeMind` API 的请求与响应，确保稳定性和容错性。

## 输入要求

- **需要转换的内容**: 待生成思维导图的文本内容（如故事大纲、角色列表、剧本片段）。
- **思维导图结构**（可选）: 指定思维导图的层级关系或特定节点连接方式。
- **样式设置**（可选）: 定义思维导图的颜色、字体、布局等视觉样式。

## 输出格式

```json
{
  "pic": "[思维导图图片URL]",
  "jump_link": "[思维导图编辑链接]",
  "data": "[原始数据，通常为 JSON 格式的思维导图数据]",
  "log_id": "[日志ID]"
}
```

## 约束条件

- 确保 `generateTreeMind` API 调用的稳定性和成功率。
- 处理 API 响应中的各种状态，包括成功、失败或错误信息。
- 思维导图生成内容必须准确反映输入文本的结构和语义。
- 返回的图片URL和编辑链接必须有效且可访问。
- 不得在输出中引入任何与思维导图生成无关的信息。

## 示例

参见 `{baseDir}/references/examples.md` 目录获取更多详细示例:
- `examples.md` - 包含不同输入内容（如故事大纲、人物列表）和样式设置的思维导图生成示例。

## 详细文档

参见 `{baseDir}/references/examples.md` 获取关于思维导图生成工具的详细指导与案例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；模型更改为 opus；优化功能、核心能力、输入要求、输出格式的描述，使其更符合命令式语言规范；添加使用场景、约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
