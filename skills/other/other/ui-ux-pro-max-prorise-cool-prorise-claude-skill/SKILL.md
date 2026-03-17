---
name: ui-ux-pro-max
description: "UI/UX 设计智能，在设计页面时必须使用"
---

# UI/UX Pro Max - 设计智能

一个可搜索的数据库，包含 UI 风格、配色方案、字体搭配、图表类型、产品推荐、UX 准则以及特定技术栈的最佳实践。

## 前置条件

检查是否已安装 Python：

```bash
python3 --version || python --version

```

如果未安装 Python，请根据用户的操作系统进行安装：

**macOS:**

```bash
brew install python3

```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3

```

**Windows:**

```powershell
winget install Python.Python.3.12

```

---

## 如何使用此技能

当用户请求进行 UI/UX 工作（设计、构建、创建、实现、审查、修复、改进）时，请遵循以下工作流程：

### 步骤 1：分析用户需求

从用户请求中提取关键信息：

* **产品类型**：SaaS、电商、作品集、仪表盘、落地页等。
* **风格关键词**：极简、俏皮、专业、优雅、暗黑模式等。
* **行业**：医疗、金融科技、游戏、教育等。
* **技术栈**：React, Vue, Next.js, 或默认为 `html-tailwind`。

### 步骤 2：搜索相关领域

多次使用 `search.py` 以收集全面的信息。持续搜索直到获得足够的上下文。

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <领域> [-n <最大结果数>]

```

**推荐搜索顺序：**

1. **Product (产品)** - 获取针对该产品类型的风格建议
2. **Style (风格)** - 获取详细的风格指南（颜色、特效、框架）
3. **Typography (排版)** - 获取带有 Google Fonts 引入代码的字体搭配
4. **Color (颜色)** - 获取配色方案（主色、辅助色、CTA、背景、文本、边框）
5. **Landing (落地页)** - 获取页面结构（如果是落地页）
6. **Chart (图表)** - 获取图表推荐（如果是仪表盘/分析类）
7. **UX (用户体验)** - 获取最佳实践和反模式（即应避免的设计）
8. **Stack (技术栈)** - 获取特定技术栈的指南（默认：html-tailwind）

### 步骤 3：技术栈指南 (默认: html-tailwind)

如果用户未指定技术栈，**默认为 `html-tailwind**`。

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack html-tailwind

```

可用技术栈：`html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## 搜索参考

### 可用领域 (Domains)

| 领域 (`domain`) | 用途 | 关键词示例 |
| --- | --- | --- |
| `product` | 产品类型推荐 | SaaS, e-commerce (电商), portfolio (作品集), healthcare (医疗), beauty (美业), service (服务) |
| `style` | UI 风格、颜色、特效 | glassmorphism (玻璃拟态), minimalism (极简), dark mode (暗黑), brutalism (粗野主义) |
| `typography` | 字体搭配, Google Fonts | elegant (优雅), playful (俏皮), professional (专业), modern (现代) |
| `color` | 按产品类型的配色方案 | saas, ecommerce, healthcare, beauty, fintech (金融), service |
| `landing` | 页面结构, CTA 策略 | hero (首屏), hero-centric, testimonial (评价), pricing (定价), social-proof (社会证明) |
| `chart` | 图表类型, 库推荐 | trend (趋势), comparison (对比), timeline (时间轴), funnel (漏斗), pie (饼图) |
| `ux` | 最佳实践, 反模式 | animation (动画), accessibility (无障碍), z-index, loading (加载) |
| `prompt` | AI 提示词, CSS 关键词 | (风格名称) |

### 可用技术栈 (Stacks)

| 技术栈 (`stack`) | 侧重点 |
| --- | --- |
| `html-tailwind` | Tailwind 工具类, 响应式, 无障碍性 (默认) |
| `react` | 状态管理, hooks, 性能, 模式 |
| `nextjs` | SSR (服务端渲染), 路由, 图片优化, API 路由 |
| `vue` | 组合式 API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | 视图, 状态, 导航, 动画 |
| `react-native` | 组件, 导航, 列表 |
| `flutter` | Widgets, 状态, 布局, 主题 |
| `shadcn` | shadcn/ui 组件, 主题定制, 表单, 模式 |

---

## 示例工作流

**用户请求：** "为专业护肤服务制作一个落地页 (Landing page)"

**AI 应当执行：**

```bash
# 1. 搜索产品类型
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product

# 2. 搜索风格 (基于行业: 美业, 优雅)
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style

# 3. 搜索排版/字体
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography

# 4. 搜索配色方案
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color

# 5. 搜索落地页结构
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing

# 6. 搜索 UX 准则
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 7. 搜索技术栈指南 (默认: html-tailwind)
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind

```

**然后：** 综合所有搜索结果并实现设计。

---

## 获取更好结果的技巧

1. **关键词要具体** - 使用 "healthcare SaaS dashboard" (医疗 SaaS 仪表盘) 优于 "app"。
2. **多次搜索** - 不同的关键词会揭示不同的见解。
3. **组合领域** - 风格 (Style) + 排版 (Typography) + 颜色 (Color) = 完整的设计系统。
4. **务必检查 UX** - 搜索 "animation" (动画), "z-index", "accessibility" (无障碍) 以避免常见问题。
5. **使用 Stack 标志** - 获取特定实现的最佳实践。
6. **迭代** - 如果第一次搜索不匹配，尝试不同的关键词。

---

## 专业 UI 的通用规则

这些是经常被忽视的问题，它们会让 UI 看起来不专业：

### 图标与视觉元素

| 规则 | 应做 (Do) | 不应做 (Don't) |
| --- | --- | --- |
| **不要使用 Emoji 图标** | 使用 SVG 图标 (Heroicons, Lucide, Simple Icons) | 使用 🎨 🚀 ⚙️ 等 Emoji 作为 UI 图标 |
| **稳定的悬停状态** | 悬停时使用颜色/透明度过渡 | 使用会导致布局偏移的缩放变换 |
| **正确的品牌 Logo** | 从 Simple Icons 查找官方 SVG | 猜测或使用错误的 Logo 路径 |
| **一致的图标尺寸** | 使用固定的 viewBox (24x24) 和 w-6 h-6 | 随意混合不同尺寸的图标 |

### 交互与光标

| 规则 | 应做 (Do) | 不应做 (Don't) |
| --- | --- | --- |
| **指针光标 (Cursor pointer)** | 给所有可点击/可悬停的卡片添加 `cursor-pointer` | 在交互元素上保留默认光标 |
| **悬停反馈** | 提供视觉反馈（颜色、阴影、边框） | 没有任何指示表明元素可交互 |
| **平滑过渡** | 使用 `transition-colors duration-200` | 状态瞬间切换或过慢 (>500ms) |

### 亮/暗模式对比度

| 规则 | 应做 (Do) | 不应做 (Don't) |
| --- | --- | --- |
| **亮色模式下的玻璃卡片** | 使用 `bg-white/80` 或更高不透明度 | 使用 `bg-white/10` (太透明) |
| **亮色文本对比度** | 文本使用 `#0F172A` (slate-900) | 正文使用 `#94A3B8` (slate-400) |
| **柔和/次级文本 (亮色)** | 最低使用 `#475569` (slate-600) | 使用 gray-400 或更浅的颜色 |
| **边框可见性** | 亮色模式使用 `border-gray-200` | 使用 `border-white/10` (不可见) |

### 布局与间距

| 规则 | 应做 (Do) | 不应做 (Don't) |
| --- | --- | --- |
| **悬浮导航栏** | 添加 `top-4 left-4 right-4` 间距 | 将导航栏紧贴 `top-0 left-0 right-0` |
| **内容内边距 (Padding)** | 考虑到固定导航栏的高度 | 让内容隐藏在固定元素后面 |
| **一致的最大宽度** | 使用统一的 `max-w-6xl` 或 `max-w-7xl` | 混合使用不同的容器宽度 |

---

## 交付前检查清单

在交付 UI 代码之前，请验证这些项目：

### 视觉质量

* [ ] 没有将 Emoji 用作图标（应使用 SVG）
* [ ] 所有图标来自一致的图标集 (Heroicons/Lucide)
* [ ] 品牌 Logo 正确（已通过 Simple Icons 验证）
* [ ] 悬停状态不会导致布局偏移
* [ ] 直接使用主题颜色 (bg-primary) 而不是 var() 包装器

### 交互体验

* [ ] 所有可点击元素都有 `cursor-pointer`
* [ ] 悬停状态提供清晰的视觉反馈
* [ ] 过渡效果平滑 (150-300ms)
* [ ] 键盘导航时焦点状态可见

### 亮/暗模式

* [ ] 亮色模式文本有足够的对比度（最低 4.5:1）
* [ ] 玻璃/透明元素在亮色模式下可见
* [ ] 边框在两种模式下均可见
* [ ] 交付前在两种模式下都进行了测试

### 布局

* [ ] 悬浮元素与边缘有适当的间距
* [ ] 没有内容隐藏在固定导航栏后面
* [ ] 在 320px, 768px, 1024px, 1440px 下均响应良好
* [ ] 移动端没有水平滚动条

### 无障碍性

* [ ] 所有图片都有 alt 文本
* [ ] 表单输入框有标签 (label)
* [ ] 颜色不是唯一的指示器
* [ ] 尊重 `prefers-reduced-motion`（减少动态效果）设置