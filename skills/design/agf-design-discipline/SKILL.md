---
name: agf-design-discipline
description: Use when uiux-designer is about to produce a design spec (spec.md) or static HTML prototype, or frontend-dev is about to build UI from a design. Provides the anti-AI-slop design discipline layer — Brief Inference (Design Read), three aesthetic dials tuned for product UI, AI Tells blacklist with overrides, mechanically-checkable Pre-Flight. Sits above the token layer (DESIGN.md) and mechanical review (code-reviewer); does not redeclare tokens or guide non-shadcn design systems. Inspired by taste-skill, cropped for AGF product UI per ADR-013.
---

# 设计纪律（agf-design-discipline）

> AGF 设计治理的**第三层**：审美判断。与 token 层（[`docs/design/DESIGN.md`](../../../docs/design/DESIGN.md)）、机械审查层（[`code-reviewer.md`](../../agents/code-reviewer.md) 设计 token 审查项）正交。本 skill **不重声明 token、不做 grep、不引导非 shadcn 设计系统** —— 只管"设计方向与审美判断"。治理背书 [ADR-013](../../../docs/adr/013-design-discipline-layer.md)。

## Use this skill when

- uiux-designer 即将产出 feature `spec.md` 或 `index.html` 原型（**设计侧**：产出前给 Design Read + 自查 9 维）
- frontend-dev 即将据设计实现 UI（**实现侧**：写码时守 AI Tells，防重新引入 AI 味）
- 任一角色需要判断"这个 UI 有没有 AI 味 / 是否模板化"

**Do NOT use this skill for**:
- 重声明颜色 / 字号 / 间距 / 圆角 token —— 那是 `docs/design/DESIGN.md` 的职责，本 skill 只**指向**它
- 机械 grep 硬编码值 —— 那是 `code-reviewer.md` 设计 token 审查项 + `agf-design-precheck.sh`
- 引导 Material / Fluent / Carbon / Polaris 等非 shadcn 设计系统 —— [ADR-000](../../../docs/adr/000-system-architecture.md) 锁死 shadcn/ui + Tailwind v4，引导其他系统会冲突
- Apple（SwiftUI）/ miniapp（WXML/WXSS）轨 —— 平台 HIG / 设计规范优先，本 skill 先落 Web / 通用轨
- 高 MOTION 营销编排（scroll-hijack / GSAP / kinetic-type）用在**产品 UI** —— 那是反模式（见 §3 motion 红线）；营销 / 落地页 feature 若 PL 显式声明可单独放开

---

## 1. Brief Inference —— Design Read 声明（产出前第一动作）

LLM 设计输出烂的头号原因：模型跳过"读需求"直接套默认审美。**写任何设计 / 代码前，先输出一句 Design Read 声明**，落 `spec.md` 顶部（feature 审美方向锚）。

### 1A 先读这些信号
1. **页面类型** —— 产品 UI（登录 / 列表 / 表单 / 详情 / 设置 / dashboard）vs 营销页（landing / 落地 / hero / portfolio）。**页面类型决定刻度档**（产品 UI 默认低，营销页可高）。
2. **风格词** —— 用户说的"简约 / 克制 / Linear 风 / Apple 感 / 严肃 B2B / 活泼 / 暗色科技"。
3. **参考信号** —— 用户贴的截图、点的竞品、链接的 URL。
4. **受众** —— B2B 采购 vs 设计敏感消费者 vs 内部运营。受众选审美，不是你的口味。
5. **既有品牌资产** —— logo / 色 / 字 / 摄影。改版时是起点素材。
6. **静默约束** —— 无障碍优先 / 公共部门 / 强监管 / 信任优先。这些约束**覆盖**审美偏好。

### 1B Design Read 模板（一句话）
```
Reading this as: <产品 UI / 营销页> for <受众>, with a <风格> language,
leaning toward <shadcn/ui + Tailwind 方向>, VARIANCE/MOTION/DENSITY = x/y/z.
```
例：
- *Reading this as: 产品 UI（后台用户列表）for 内部运营, with a 克制 B2B language, leaning toward shadcn/ui DataTable + 中性灰 + 低 motion, VARIANCE/MOTION/DENSITY = 4/3/中。*
- *Reading this as: 营销页（产品 landing）for 设计敏感消费者, with a premium language, leaning toward shadcn/ui 定制 + 大留白 + 入场 reveal, VARIANCE/MOTION/DENSITY = 7/5/低。*

### 1C 模糊 brief 只问一个问题
brief 真正分叉时问**一个**澄清问题（不要连环问）："这个更偏 Linear 克制还是 premium consumer？" 能从上下文推断就**别问**，直接声明 Design Read 并继续。

---

## 2. 三刻度（审美方向元数据，裁剪自 taste-skill）

三刻度是全文交叉引用的"全局变量"，驱动后续布局 / 动效 / 密度决策。**它们是风格参数不是视觉值 —— 不进 DESIGN.md token YAML，落 spec.md 顶部 Design Read 声明里**（ADR-013 决策 3）。

| 刻度 | 1 | 10 | AGF 产品 UI 默认 |
|---|---|---|---|
| **VARIANCE**（布局实验度） | 完美对称 / 居中 | 非对称 / 网格破碎 | **≤ 5** |
| **MOTION**（动效深度） | 静态（仅 hover） | 影院级 / 物理编排 | **≤ 4** |
| **DENSITY**（视口信息密度） | 画廊级留白 | 驾驶舱紧凑 | **中** |

### 2A brief → 刻度推断表
| 信号 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| 产品 UI（默认）| 4-5 | 3-4 | 中 |
| "克制 / 简约 / Linear 风 / 严肃 B2B" | 3-4 | 2-3 | 中-高 |
| dashboard / 数据密集 | 3-4 | 2-3 | 高 |
| 营销 landing / portfolio（PL 显式声明）| 7-9 | 5-7 | 低-中 |
| premium consumer / Apple 感（营销）| 7-8 | 5-6 | 低 |
| 无障碍优先 / 公共部门 / 强监管 | 2-3 | 1-2 | 中 |
| 改版 - 保留 | 匹配现状 | +1 | 匹配现状 |
| 改版 - 翻新 | +2 | +2 | 匹配现状 |

### 2B 刻度如何驱动产出（产品 UI 视角）
- **VARIANCE**：≤ 5 → 对称 / 网格规整 / 居中或左对齐合法；> 5（仅营销页）才考虑非对称 / 破格。**产品 UI 不要为"有趣"破坏网格稳定性。**
- **DENSITY**：中 → 标准 `py-16` 间距；高（dashboard）→ 紧凑 + `divide-y` 分隔；低（营销）→ `py-32` 大留白。
- **MOTION**：见 §3 红线。

---

## 3. 产品 UI motion 红线（裁剪 taste-skill 的关键差异）

taste-skill 的高 MOTION 编排是为**营销页**设计的。**AGF 产品 UI 一律禁用**，理由：破坏稳定性、Core Web Vitals（INP）、可访问性、`prefers-reduced-motion` 兜底复杂度。这是 taste-skill（营销页导向）与 AGF（产品 UI 导向）最核心的语境差异。

### 3A 产品 UI 禁用（任何 MOTION 值）
- **scroll-hijack**（纵向滚动转横向 pan）—— 营销页炫技，产品 UI 里破坏滚动预期
- **parallax 视差 / GSAP ScrollTrigger pinning / kinetic typography**
- **`window.addEventListener('scroll', ...)`** —— 每帧触发、jank；用 `useScroll()` / IntersectionObserver / CSS `animation-timeline: view()` 替代
- **`useState` 跟踪连续输入值**（鼠标位置 / 滚动进度 / 磁吸 hover）—— 每帧重渲染；用 `useMotionValue` / `useTransform`（在 React render cycle 之外）
- **磁吸按钮 / 3D tilt / gooey menu** —— 营销页花活，产品 UI 不需要

### 3B 产品 UI 允许（MOTION ≤ 4 默认）
- hover / active `transition`（`cubic-bezier(0.16, 1, 0.3, 1)`，~300ms）
- 入场 reveal：`whileInView`（motion/react）或 IntersectionObserver 或 CSS `animation-timeline: view()`，`once: true`
- 状态过渡：loading skeleton shimmer、toast 入退、modal / drawer 开合
- 触觉反馈：`:active` 时 `-translate-y-[1px]` 或 `scale-[0.98]`
- **动画只动 `transform` / `opacity`**，绝不动 `top/left/width/height`
- **MOTION > 3 必须守 `prefers-reduced-motion`**（`useReducedMotion()` 降级为静态）—— 非协商

### 3C 营销 / 落地页例外
PL 派工时**显式声明**该 feature 是营销 / 落地页 → spec.md Design Read 标注 → 该 feature 可放开 MOTION 到 5-7（仍守 reduced-motion + `transform/opacity` only + 客户端 leaf 组件隔离 + `useEffect` cleanup）。**不放开到 scroll-hijack / GSAP**（AGF 不引 GSAP，ADR-000 技术栈无它）。

---

## 4. AI Tells 黑名单（AGF 化，每条 hard ban + override）

LLM 生成 UI 的高频"AI 味"模式。每条默认禁，**override 路径**说明何时可破例。

### 4A 视觉 / 配色
- **❌ AI 紫蓝渐变 / neon glow**（`from-indigo-* to-violet-*` / `bg-purple-*` 按钮 glow / 随机 mesh 渐变）—— LLM 头号指纹。
  - override：品牌 brief 明确要紫 / 渐变，且有完整色板 harmonisation。
  - Do：DESIGN.md 中性基底（surface / border）+ 单一 accent（`{color.primary}`），accent 都引自 token。
- **❌ 纯黑 `#000000` / 纯白 `#ffffff`** —— 杀死纵深。
  - Do：off-black（zinc-950 / 暖近黑）/ off-white。DESIGN.md 的 surface token 已是。
- **❌ 过饱和 accent**（饱和度 > 80%）—— 像素级尖叫。
  - Do：降饱和与中性融合。
- **❌ 多 accent 混用**（这节蓝、下节绿、footer 又红）—— 散。
  - Do：**一个 accent 锁全页**（DESIGN.md `{color.primary}`），全页审计一致。

### 4B 字体
- **❌ Inter 作默认字体** —— LLM 默认 sans，没个性。
  - override：用户明确要"中性 / 标准 / Linear 风"，或无障碍优先站点。
  - Do：DESIGN.md `typography.*.font-family` 定 system-ui 栈或 Geist；display 与 body 各一族。
- **❌ serif 用在 dashboard / 产品 UI** —— serif 仅限编辑 / 奢侈 / 出版物 brief。
- **❌ 标题靠超大字号喊**（`text-7xl/8xl`）—— 用 weight + color 控层级，不全靠 scale。
- **❌ 渐变文字**（`bg-clip-text text-transparent`）大面积标题 —— 营销页花活，产品 UI 不要。

### 4C 布局
- **❌ 三等分等高 feature 卡**（`grid-cols-3` 三张一模一样）—— LLM 布局头号指纹。
  - Do：非对称网格、zig-zag（图文左右交替）、横向滚动、或 `divide-y` 列表。
- **❌ 居中 hero**（VARIANCE > 4 时）—— 模板化。
  - override：编辑 / 宣言 / 发布公告 brief，信息本身即设计。
  - Do：split（50/50）、左对齐内容 / 右对齐 asset、非对称留白。
- **❌ 全场 `rounded-2xl`**（所有东西一个圆角）—— 单调。
  - Do：DESIGN.md `radius` token 锁**单一 radius 系统**（全锐 / 全软 / 全胶囊，或文档化规则如"按钮胶囊 / 卡片 12px / 输入 8px"）。

### 4D 内容 / 数据（"Jane Doe 效应"）
- **❌ 假人名**（John Doe / Sarah Chan / 张三 / 李四）—— 用有创意、locale 得体的真实感人名。
- **❌ 假品牌名**（Acme / Nexus / SmartFlow / Cloudly）—— 造语境化、听起来真实的品牌名。
- **❌ 假精确数字**（99.99% / 50% / 1234567）—— 用"乱"的真实数据（47.2% / +1 (312) 847-1928）；或显式标 `<!-- mock -->`。
- **❌ AI 营销套话**（Elevate / Seamless / Unleash / Next-Gen / 赋能 / 一站式）—— 具体动词。
  - 注：与 [uiux-designer.md](../../agents/uiux-designer.md)「真实文案与数据」+ DESIGN.md §2 Do/Don't 同向，不重复声明机制，只强化规则层。

### 4E 图标 / 组件
- **❌ emoji 当 icon**（按钮 / 导航 / 状态用 🔥✨🚀）—— 业余。
  - Do：用 shadcn/ui 默认的 **lucide-react** 图标（**AGF 不禁 lucide**，ADR-000 锁 shadcn/ui 默认配它；区别于 taste-skill 禁 lucide）。
  - override：用户明确要"活泼 / 聊天风 / 社交原生"brief，少量有意使用。
- **❌ div 伪造截图 / dashboard / terminal**（用 `<div>` 矩形堆假任务列表 / 假面板）—— LLM-design 头号 Tell。
  - Do：真实截图 URL、或 image 工具生成图、或真实组件 mini 预览、或跳过预览用编辑摄影。
- **❌ shadcn/ui 默认态直出** —— 允许用，但**禁止默认态**：定制 radius / 色 / 字 / 阴影对齐项目审美（DESIGN.md token）。
- **❌ 手写 SVG icon**（自己画 path）—— 用 lucide；缺字形就找另一个库或组合，不画。
- **❌ 破碎 Unsplash 链接** —— 用 `https://picsum.photos/seed/{描述性 seed}/{w}/{h}` 或 DESIGN.md token 色。

### 4F 状态 / 交互
- **❌ 只生成"成功静态态"** —— LLM 默认只画 happy path。
  - Do：full cycle —— loading（骨架屏对齐最终布局，禁通用圆 spinner）/ empty（引导操作的空态，**非白屏**）/ error（分类文案 + 重试）/ disabled（灰置 + 原因）。与 [uiux-designer.md](../../agents/uiux-designer.md)「页面/模块状态覆盖」+ 自查第 5 维同向。
- **❌ 按钮白底白字 / 透明按钮无描边** —— 对比度不足。
  - Do：WCAG AA（正文 4.5:1 / 大字 3:1），DESIGN.md on-* 配对。

---

## 5. Pre-Flight Check（产出前自检，可机械验证的优先）

对照下表逐条自检 spec + 原型。**机械可验项**（可 grep / 可数）优先，**人审项**（AI Tells）其次。`agf-design-precheck.sh` 跑机械项作 step 0。

**机械可验项**（脚本 / grep 可查）:
- [ ] 样式无裸 `#RRGGBB` / 字面 px 间距字号 / 一次性圆角（引用 DESIGN.md token）
- [ ] 全高区域用 `min-h-[100dvh]` / `100dvh`，**无** `100vh` / `h-screen`（iOS Safari 地址栏跳动）
- [ ] code 内无可见 emoji 当 icon（用 lucide）
- [ ] `font-family` 无 Inter 作默认（system-ui 栈或 Geist）
- [ ] 无 `from-indigo-* to-violet-*` / `bg-purple-*` AI 渐变信号
- [ ] 颜色全引自 DESIGN.md token + on-* 配对（与自查第 3 维同向）
- [ ] `prefers-reduced-motion` 对 MOTION > 3 的动效有兜底

**人审项**（AI Tells，§4）:
- [ ] 无三等分等高 feature 卡（VARIANCE > 4 时无居中 hero）
- [ ] 无假人名 / 假品牌名 / 假精确数字 / AI 营销套话
- [ ] 无 div 伪造截图 / dashboard
- [ ] 无纯黑纯白 / 过饱和 accent / 多 accent 混用
- [ ] shadcn/ui 组件非默认态直出（已按 token 定制）
- [ ] loading / empty / error / disabled 状态全覆盖
- [ ] 产品 UI 无禁用 motion（scroll-hijack / GSAP / `window.addEventListener('scroll')`）

**纪律项**:
- [ ] spec.md 顶部有 Design Read 声明（§1B 模板）
- [ ] 三刻度值明确且由 brief 推断（非无脑默认）
- [ ] 营销页 feature 若 MOTION > 4，PL 已显式声明 + 仍守 reduced-motion

任一项不过 = 产出未完成，改完再交。

---

## 6. 真实参考锚点（防 LLM 编造）

设计系统选型**只锚定 ADR-000 锁定的栈**，不引导其他系统（ADR-013 决策 5）：

- **组件 / 样式**：[shadcn/ui 官方文档](https://ui.shadcn.com/docs)（你拥有组件源码，可定制；禁默认态直出）+ [Tailwind v4](https://tailwindcss.com)
- **可访问性 / 对比度**：[WCAG 2.1 quick ref](https://www.w3.org/WAI/WCAG21/quickref/)（正文 ≥ 4.5:1 / 大字 ≥ 3:1）+ `frontend-design:frontend-design` 插件检查清单
- **动效**：[Motion（motion/react）](https://motion.dev)（产品 UI 默认）+ [CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)（入场 reveal 替代）
- **token 来源**：本项目 `docs/design/DESIGN.md`（SSOT，禁另立色板）

**不要引导**：Material / Fluent / Carbon / Polaris / Atlassian / Primer / GOV.UK / USWDS / Bootstrap / Radix Themes（这些是 taste-skill 的多系统引导，与 AGF 锁死 shadcn/ui 冲突）。若用户明确要某系统 → 退回 tech-lead 开新 ADR（技术选型变更）。

---

## 完成前的验证

- [ ] Design Read 声明已写进 spec.md 顶部（页面类型 + 受众 + 风格 + 三刻度）？
- [ ] 三刻度由 brief 推断，产品 UI 默认 ≤ 5/4/中（营销页另声明）？
- [ ] AI Tells 黑名单（§4）逐条过，命中项有 override 理由或已改？
- [ ] Pre-Flight Check（§5）机械项 + 人审项全过？
- [ ] 产品 UI motion 守 §3 红线（无 scroll-hijack / GSAP / `window.addEventListener('scroll')`）？
- [ ] 视觉值全引自 DESIGN.md token，未在本 skill / spec 重声明色板？
- [ ] 未引导非 shadcn 设计系统？
- [ ] 跑 `bash .claude/scripts/agf-design-precheck.sh docs/design/[feature]/` advisory 通过？

## 反模式（Anti-patterns）

- ❌ 把 taste-skill 的营销页高 MOTION 编排（GSAP sticky-stack / horizontal-pan / kinetic-type）机械照搬到产品 UI —— 破坏稳定性 / 可访问性
- ❌ 在本 skill / spec.md 里重声明颜色 / 间距 / 圆角 —— 那是 DESIGN.md 的 SSOT 职责
- ❌ 引导 Material / Fluent / Carbon 等非 shadcn 设计系统 —— 冲突 ADR-000
- ❌ 禁 lucide-react —— AGF 用 shadcn/ui 默认配 lucide；只禁 emoji 当 icon（taste-skill 禁 lucide 是它的语境，不是 AGF 的）
- ❌ 把三刻度塞进 DESIGN.md token YAML —— 刻度是风格参数不是视觉值，落 spec.md Design Read 声明（ADR-013 决策 3）
- ❌ 把审美规则塞进 uiux-designer / frontend-dev 正文大段重复 —— 本 skill 是单点维护，agent 正文只放指针 + 自查维
- ❌ MOTION 声明 > 4 但页面实际不动 —— "motion claimed, motion shown"；声了就得有真动效，否则降到 3 出静态干净页
- ❌ 只生成成功静态态 —— loading / empty / error / disabled 必须全覆盖

## Hand-off

设计产出（uiux-designer）或 UI 实现（frontend-dev）完成自检后：
1. spec.md 顶部 Design Read 声明 + 三刻度在位
2. SendMessage 通告（uiux → frontend-dev / PL，或 frontend-dev → code-reviewer）含"已过 agf-design-discipline 自查 9 维 + precheck"
3. code-reviewer 审查时跑 `agf-design-precheck.sh` step 0 + §4 AI Tells 人审 + §3 motion 红线核
