---
name: ui-ux-pro-max
description: "UI/UX 设计情报库：50 种风格、21 套配色、50 组字体搭配、20 类图表、8 个技术栈（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind）。动作：plan、build、create、design、implement、review、fix、improve、optimize、enhance、refactor、check UI/UX code。项目：website、landing page、dashboard、admin panel、e-commerce、SaaS、portfolio、blog、mobile app、.html、.tsx、.vue、.svelte。元素：button、modal、navbar、sidebar、card、table、form、chart。风格：glassmorphism、claymorphism、minimalism、brutalism、neumorphism、bento grid、dark mode、responsive、skeuomorphism、flat design。主题：color palette、accessibility、animation、layout、typography、font pairing、spacing、hover、shadow、gradient。"
---

# UI/UX Pro Max - 设计情报库

可搜索的 UI 风格、配色方案、字体搭配、图表类型、产品推荐、UX 指南与技术栈最佳实践数据库。

## 使用方法

当用户提出 UI/UX 相关需求（design、build、create、implement、review、fix、improve）时，遵循以下流程：

### Step 1：分析用户需求

从用户请求中提取关键信息：
- **产品类型**：SaaS、电商、作品集、仪表盘、落地页等。
- **风格关键词**：极简、活泼、专业、优雅、暗黑模式等。
- **行业领域**：医疗、金融科技、游戏、教育等。
- **技术栈**：React、Vue、Next.js，默认 `html-tailwind`。

### Step 2：检索相关领域

多次使用 `search.py` 获取完整信息，直到具备足够上下文。

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**推荐检索顺序：**

1. **Product** - 获取产品类型的风格建议
2. **Style** - 获取详细风格指南（颜色、效果、框架）
3. **Typography** - 获取字体搭配与 Google Fonts 导入
4. **Color** - 获取配色方案（主色、辅色、CTA、背景、正文、边框）
5. **Landing** - 获取页面结构（如为落地页）
6. **Chart** - 获取图表推荐（如为数据看板/分析）
7. **UX** - 获取最佳实践与反模式
8. **Stack** - 获取技术栈最佳实践（默认 html-tailwind）

### Step 3：技术栈指南（默认：html-tailwind）

如果用户未指定技术栈，**默认使用 `html-tailwind`**。

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈：`html-tailwind`、`react`、`nextjs`、`vue`、`svelte`、`swiftui`、`react-native`、`flutter`

---

## 检索参考

### 可用 Domain

| Domain | 用途 | 示例关键词 |
|--------|------|-----------|
| `product` | 产品类型推荐 | SaaS、e-commerce、portfolio、healthcare、beauty、service |
| `style` | UI 风格、颜色、效果 | glassmorphism、minimalism、dark mode、brutalism |
| `typography` | 字体搭配、Google Fonts | elegant、playful、professional、modern |
| `color` | 按产品类型的配色 | saas、ecommerce、healthcare、beauty、fintech、service |
| `landing` | 页面结构、CTA 策略 | hero、hero-centric、testimonial、pricing、social-proof |
| `chart` | 图表类型、库推荐 | trend、comparison、timeline、funnel、pie |
| `ux` | 最佳实践、反模式 | animation、accessibility、z-index、loading |
| `prompt` | AI 提示词、CSS 关键词 | (style name) |

### 可用技术栈

| Stack | 关注点 |
|-------|--------|
| `html-tailwind` | Tailwind 工具类、响应式、无障碍（默认） |
| `react` | 状态、Hooks、性能、模式 |
| `nextjs` | SSR、路由、图片、API routes |
| `vue` | Composition API、Pinia、Vue Router |
| `svelte` | Runes、stores、SvelteKit |
| `swiftui` | Views、State、Navigation、Animation |
| `react-native` | Components、Navigation、Lists |
| `flutter` | Widgets、State、Layout、Theming |

---

## 示例流程

**用户请求：** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

**AI 应该：**

```bash
# 1. 检索产品类型
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product

# 2. 检索风格（基于行业：beauty、elegant）
python3 skills/ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style

# 3. 检索字体搭配
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography

# 4. 检索配色
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color

# 5. 检索落地页结构
python3 skills/ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing

# 6. 检索 UX 指南
python3 skills/ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 skills/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 7. 检索技术栈指南（默认：html-tailwind）
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind
```

**然后：** 综合所有检索结果并实现设计。

---

## 提升结果质量的提示

1. **关键词尽量具体** - "healthcare SaaS dashboard" > "app"
2. **多次检索** - 不同关键词会揭示不同信息
3. **组合多个领域** - Style + Typography + Color = 完整设计系统
4. **始终检查 UX** - 检索 "animation"、"z-index"、"accessibility" 规避常见问题
5. **使用 stack 参数** - 获取实现层面的最佳实践
6. **迭代搜索** - 首次结果不匹配就换关键词重试

---

## 专业 UI 的常见规则

这些问题经常被忽视，会让 UI 看起来不专业：

### 图标与视觉元素

| 规则 | 建议 | 避免 |
|------|------|------|
| **不要用 emoji 图标** | 使用 SVG 图标（Heroicons、Lucide、Simple Icons） | 用 🎨 🚀 ⚙️ 等 emoji 充当 UI 图标 |
| **悬停状态稳定** | 悬停使用颜色/透明度过渡 | 使用缩放导致布局抖动 |
| **品牌 Logo 正确** | 从 Simple Icons 获取官方 SVG | 猜测或使用错误 Logo |
| **图标尺寸一致** | 固定 viewBox（24x24）并使用 w-6 h-6 | 混用不同尺寸 |

### 交互与指针

| 规则 | 建议 | 避免 |
|------|------|------|
| **鼠标指针提示** | 所有可点击卡片加 `cursor-pointer` | 交互元素仍是默认指针 |
| **悬停反馈** | 提供颜色/阴影/边框反馈 | 交互无可见提示 |
| **过渡要顺滑** | `transition-colors duration-200` | 突变或过慢（>500ms） |

### 明暗对比

| 规则 | 建议 | 避免 |
|------|------|------|
| **浅色玻璃卡片** | 使用 `bg-white/80` 或更高不透明度 | `bg-white/10`（太透明） |
| **浅色文字对比** | 正文用 `#0F172A`（slate-900） | 用 `#94A3B8`（slate-400） |
| **浅色次级文字** | 最低 `#475569`（slate-600） | 用 gray-400 或更浅 |
| **边框可见性** | 浅色用 `border-gray-200` | 用 `border-white/10`（看不见） |

### 布局与间距

| 规则 | 建议 | 避免 |
|------|------|------|
| **悬浮导航栏** | 增加 `top-4 left-4 right-4` 间距 | 直接贴 `top-0 left-0 right-0` |
| **内容内边距** | 预留固定导航的高度 | 内容被固定元素遮挡 |
| **一致的最大宽度** | 统一使用 `max-w-6xl` 或 `max-w-7xl` | 混用不同容器宽度 |

---

## 交付前检查清单

在交付 UI 代码前，确认以下事项：

### 视觉质量
- [ ] 不使用 emoji 作为图标（改用 SVG）
- [ ] 图标来自一致的图标集（Heroicons/Lucide）
- [ ] 品牌 Logo 正确（从 Simple Icons 验证）
- [ ] 悬停状态不引发布局抖动
- [ ] 直接使用主题色（如 bg-primary），不包一层 var()

### 交互
- [ ] 所有可点击元素有 `cursor-pointer`
- [ ] 悬停反馈清晰可见
- [ ] 过渡动画顺滑（150-300ms）
- [ ] 键盘导航有可见的 focus 状态

### 明暗模式
- [ ] 浅色模式文本对比度满足 4.5:1 最低要求
- [ ] 浅色模式玻璃/透明元素可见
- [ ] 明暗模式下边框都可见
- [ ] 交付前测试明暗两套主题

### 布局
- [ ] 悬浮元素与边缘有足够间距
- [ ] 内容不会被固定导航遮挡
- [ ] 在 320px、768px、1024px、1440px 下响应正常
- [ ] 移动端不出现横向滚动

### 无障碍
- [ ] 所有图片有 alt 文本
- [ ] 表单输入有 label
- [ ] 颜色不是唯一信息传达方式
- [ ] 尊重 `prefers-reduced-motion`
