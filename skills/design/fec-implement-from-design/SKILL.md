---
name: fec-implement-from-design
description: Use when implementing UI from Figma, Sketch, MasterGo, Pixso, Modao, MockingBot, screenshots, design selections, design tokens, or design-to-code tasks for production frontend components/pages; Chinese triggers include 设计稿, 按设计实现.
---

# 按设计稿实现

## Purpose

基于设计工具（Figma、Sketch、MasterGo、Pixso、墨刀、摹客）的设计上下文，高保真实现页面或组件，强调组件复用、设计 Token 映射、可访问性和面向生产的前端实现。

## 支持的设计工具

| 工具     | MCP 集成                  | 获取设计数据方式                          |
| -------- | ------------------------- | ----------------------------------------- |
| Figma    | `figma` / `figma-desktop` | API 获取设计结构、变量定义                |
| Sketch   | `sketch`                  | MCP 获取设计选区截图                      |
| MasterGo | `mastergo`                | API 获取 DSL 结构数据                     |
| Pixso    | `pixso`                   | 本地 MCP 获取帧数据和代码                 |
| 墨刀     | `modao`                   | MCP 获取原型数据、生成设计描述            |
| 摹客     | 无 MCP                    | 通过用户提供的截图、标注或导出的 CSS 获取 |

## 目标

- 尽量高还原地实现设计稿
- 在创建新组件前优先复用现有项目组件
- 尽可能把设计变量映射到现有 Token
- 保持实现结果可维护、类型明确、可测试且具备可访问性
- 避免引入重复的基础组件或并行设计系统

## 必需工作流

### 1. 识别设计来源

按优先级选择设计数据获取方式：

- `figma` — Figma API 集成
- `figma-desktop` — Figma 桌面端集成
- `mastergo` — MasterGo DSL 数据
- `pixso` — Pixso 本地 MCP
- `modao` — 墨刀原型数据
- `sketch` — Sketch 选区截图
- 如以上 MCP 均不可用，请求用户提供设计截图或标注（适用于摹客等无 MCP 工具）

### 2. 读取设计上下文

通过 MCP 或用户提供的设计数据读取设计上下文：

- 检查布局结构
- 检查间距、字体、颜色、变量、状态、图标和组件层级
- 如果 MCP 提供了资源文件或 SVG / 图片源，直接使用
- 如果 MCP 已提供真实资源，不要自行造占位资源
- 如果用户提供截图而非 MCP 数据，从截图中推断布局、颜色、字体等视觉信息

### 3. 搜索可复用组件

在创建新组件前先搜索代码库中的可复用组件，重点检查：

- Button
- Input / Select / Checkbox / Radio / Switch
- Modal / Drawer / Dialog
- Table / List / Card
- Tabs / Breadcrumb / Pagination
- 页面容器 / 区块容器 / 空状态 / Loading 状态

### 4. 产出实现计划

在改文件前先产出一份简短实现计划，计划必须包含：

- 需要改动的文件列表
- 组件拆分方案
- 状态 / 数据流
- 响应式行为
- 复用还是新建的决策
- 设计缺口或歧义点

### 5. 按框架实现

按仓库当前使用的前端框架进行实现：

- 严格遵循仓库现有约定
- 优先使用明确类型的 props 和 interfaces/types
- 保持组件小而可组合
- 将重复逻辑提取为 hooks / composables / utilities

### 6. 设计 Token 映射

- 优先使用现有 design token、CSS 变量、主题变量或工具类
- 除非确实没有对应 Token，否则不要硬编码颜色、圆角和间距
- 如果设计使用了新 Token，要明确指出，不要悄悄到处硬编码

### 7. 可访问性保障

- 优先使用语义化 HTML
- 确保交互控件具有可访问名称
- 保留可见的焦点样式
- 检查对话框、菜单、标签页、表单控件的键盘可操作性

### 8. 编码后验证

- 如有 lint，执行 lint
- 如有测试，执行测试
- 如果缺少测试，说明建议补充的最小测试范围

## Detailed References

撰写实现计划报告时，加载 [references/design-plan-template.md](references/design-plan-template.md)。

## Constraints

- 如果已有设计上下文（MCP 或截图），不要靠猜来实现 UI
- 如果项目已有 UI 体系，不要再引入一套新的 UI Kit
- 除非有合理理由，不要用硬编码替代已 Token 化的样式
- 不要忽略 hover、active、disabled、loading、empty、error 等状态
- 摹客等无 MCP 工具场景下，主动向用户索要关键截图和标注信息，不要凭空编造视觉数据

## Expected Output

- 设计实现计划报告保存为 `reports/design-plan-YYYY-MM-DD-HHmmss.md`，包含实现概要、组件拆分方案、状态/数据流、变更文件清单
- 代码实现高保真还原设计稿，组件复用率最大化
- 设计变量映射到现有 Token，无硬编码颜色/间距/圆角
- 交互元素具备可访问名称和键盘支持，焦点样式可见
