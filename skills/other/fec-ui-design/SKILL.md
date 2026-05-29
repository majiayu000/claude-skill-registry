---
name: fec-ui-design
description: Use when building, reviewing, or improving frontend UI that needs product-specific design direction, design-system generation, Master/Page overrides, distinctive visual identity, anti-generic interface choices, first-screen hierarchy, UI polish, chart UX, interaction states, responsive behavior, or visual QA. When an external design file is authoritative, implement from that source instead of inventing direction; Chinese triggers include UI 设计, 设计系统, 视觉风格, 不要模板化, 高级感, 界面打磨, 交互状态.
---

# UI 设计

适用于需要把前端界面推进到“符合产品语境、可扫描、可信赖、有辨识度，并且细节稳定”的 UI 任务。需要系统化设计建议时，加载 [design-intelligence.md](references/design-intelligence.md)；需要长期沉淀设计系统时，加载 [master-page-overrides.md](references/master-page-overrides.md)；上线前做 UI/UX QA 时，加载 [pre-delivery-checklist.md](references/pre-delivery-checklist.md)。

可执行设计系统生成器位于 [design-system.mjs](scripts/design-system.mjs)，其原创知识包包括 [product-rules.json](data/product-rules.json)、[style-archetypes.json](data/style-archetypes.json)、[ux-quality-rules.json](data/ux-quality-rules.json) 和 [stack-ui-rules.json](data/stack-ui-rules.json)。

## Purpose

为页面、组件、仪表盘和工具界面建立设计方向，并完成可落地的视觉与交互 polish。

## Procedure

1. 明确界面的工作
   - 先说清它帮助用户完成什么任务，而不是先选颜色或布局。
   - 判断这是日常高频工具、营销展示、内容阅读、可视化探索、游戏，还是配置/管理后台。
   - 如果已有 Figma、Sketch、MasterGo、Pixso、墨刀、摹客或截图是事实来源，优先还原设计上下文，不自行发明方向。

2. 定义审美主张
   - 写出目标用户、使用场景、可信赖感来源和一个可被记住的视觉锚点。
   - 视觉锚点可以来自信息结构、真实媒体、数据形态、行业材质、字体性格、交互节奏或空间组织，而不是空泛装饰。
   - 表现力必须服务业务语境：工具型界面重效率和稳定，展示型页面重主体识别和记忆点。

3. 生成或读取设计系统
   - 若项目还没有设计系统，可运行 `node skills/fec-ui-design/scripts/design-system.mjs "<product audience tone>" --project "<name>"` 生成建议。
   - 若需要跨会话复用，使用 `--persist` 生成 `design-system/<project>/MASTER.md`；页面差异用 `--page <page>` 写入 `pages/<page>.md`。
   - 构建具体页面时先读页面 override，再读 Master；页面规则只覆盖差异，不复制全量设计系统。

4. 建立首屏与视觉层级
   - 工具型界面：首屏直接呈现核心工作区、列表、表格、画布或编辑器。
   - 落地页：H1 使用品牌、产品、地点、人名或明确品类，价值说明放在辅助文案。
   - 产品/对象页：首屏必须可见真实产品、对象、状态或可检查媒体。
   - 首屏应留下一个明确记忆点，但不能遮挡核心任务、导航和状态反馈。

5. 组织视觉语言
   - 字体：优先沿用项目字体体系；若任务允许建立新方向，选择能表达产品性格的标题/正文字体组合，并保证可读性。
   - 色彩：明确主色、功能色、中性色和强调色的角色，避免所有元素平均用力。
   - 空间：根据任务选择高密度、留白、非对称、分栏、画布式或编辑器式布局，不套用固定卡片模板。
   - 动效：只为页面入场、层级展开、状态确认、错误反馈和重点引导建立节奏，并尊重 `prefers-reduced-motion`。
   - 图表：先判断数据任务是趋势、比较、构成、分布还是流程，再选择图表，不把所有数据都做成卡片或饼图。

6. 对齐组件与 token
   - 先复用项目已有组件、token、图标库、路由和布局约定。
   - 缺少 token 时集中补齐或明确记录，不要在多个组件里散落硬编码。
   - 复杂 UI 在实现前写出复用组件、新建组件、响应式策略和状态覆盖。

7. 打磨几何、文本和状态
   - 嵌套圆角遵循“外层圆角约等于内层圆角 + 间距”的光学关系。
   - 非对称图标、播放三角、箭头、星标等需要按视觉中心微调。
   - 标题和短文本可使用 `text-wrap: balance` 或 `text-wrap: pretty`。
   - 表格、价格、计数器、计时器使用 `font-variant-numeric: tabular-nums`。
   - 小控件点击区域至少 40x40px，空间允许时优先 44x44px。
   - focus ring 用于键盘定位，hover/active 用于鼠标反馈，disabled 不只靠透明度表达。

8. 验证设计结果
   - 检查 loading、empty、error、disabled、hover、focus、selected 状态。
   - 在 mobile(375px)、tablet(768px)、desktop(1440px) 检查文案是否溢出或遮挡。
   - 对依赖图片、图表、画布或 3D 的界面，确认资源真实渲染且承担主体信息。
   - 复核是否存在默认紫色渐变、空泛 hero、卡片堆叠、单一色相或无语境字体等模板化痕迹。

## Constraints

- 不把工具型应用做成营销落地页；首屏应是可用工作区。
- 不用通用紫色渐变、装饰光斑、堆叠卡片或空泛 hero 作为默认方案。
- 不使用无语境默认字体、均匀无重点配色、重复圆角卡片和模板化双栏 hero 来替代真实设计判断。
- 不在卡片里再套大卡片；页面分区优先用全宽区域或无框布局。
- 不用可见文案解释控件本该表达的功能，常见动作优先用图标和 tooltip。
- 不为了质感添加大面积装饰、模糊光斑、无语义渐变或无关重写。
- 不为了统一风格让整个界面落入单一色相；颜色应有层次和语义区分。
- 不把生成器输出当成不可修改的设计稿；它是决策起点，必须结合项目已有组件、token、用户任务和真实数据校正。

## Expected Output

输出应包含明确的设计方向、首屏记忆点、视觉语言策略、组件/布局边界、状态覆盖、响应式策略和验证结果。复核时界面应符合业务语境、视觉层级支持快速扫描、交互状态完整，并避免泛化模板感。
