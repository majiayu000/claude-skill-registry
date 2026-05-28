---
name: fec-ui-design-direction
description: Use when building or improving frontend UI that needs product-specific design direction, visual hierarchy, layout tone, first-screen composition, or domain-appropriate interaction design. When an external design file is authoritative, implement from that source instead of inventing direction; Chinese triggers include UI 设计方向, 视觉风格, 界面质感, 产品化界面.
---

# UI 设计方向

适用于需要从“能用”推进到“符合产品语境、可扫描、可信赖”的前端 UI 任务。

## Purpose

为页面、组件、仪表盘和工具界面建立清晰的产品化设计方向。

## Procedure

1. 明确界面的工作
   - 先说清它帮助用户完成什么任务，而不是先选颜色或布局。
   - 判断这是日常高频工具、营销展示、内容阅读、可视化探索、游戏，还是配置/管理后台。

2. 选择设计语气
   - SaaS、CRM、后台、运营工具默认安静、密集、可扫描。
   - 品牌页、作品集、发布页可更具表现力，但首屏仍要让主体明确出现。
   - 游戏、可视化和创作工具可以更有动效和沉浸感，但不能牺牲交互可控性。

3. 建立首屏优先级
   - 工具型界面：首屏直接呈现核心工作区、列表、表格、画布或编辑器。
   - 落地页：H1 使用品牌、产品、地点、人名或明确品类，价值说明放在辅助文案。
   - 产品/对象页：首屏必须可见真实产品、对象、状态或可检查媒体。

4. 对齐现有系统
   - 先复用项目已有组件、token、图标库、路由和布局约定。
   - 缺少 token 时集中补齐或明确记录，不要在多个组件里散落硬编码。
   - 复杂 UI 在实现前写出复用组件、新建组件、响应式策略和状态覆盖。

5. 验证设计结果
   - 检查 loading、empty、error、disabled、hover、focus、selected 状态。
   - 在 mobile(375px)、tablet(768px)、desktop(1440px) 检查文案是否溢出或遮挡。
   - 对依赖图片、图表、画布或 3D 的界面，确认资源真实渲染且承担主体信息。

## Constraints

- 不把工具型应用做成营销落地页；首屏应是可用工作区。
- 不用通用紫色渐变、装饰光斑、堆叠卡片或空泛 hero 作为默认方案。
- 不在卡片里再套大卡片；页面分区优先用全宽区域或无框布局。
- 不用可见文案解释控件本该表达的功能，常见动作优先用图标和 tooltip。
- 不引入只服务视觉噱头的新依赖，除非它显著提升核心体验。
- 不为了统一风格让整个界面落入单一色相；颜色应有层次和语义区分。

## Expected Output

输出应包含明确的设计方向、组件/布局边界、状态覆盖、响应式策略和验证结果。实现后的 UI 应符合业务语境，首屏主体明确，视觉层级支持快速扫描。
