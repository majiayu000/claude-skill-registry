---
name: frontend-design
description: Creates unique, production-grade frontend interfaces with exceptional design quality. Use when user asks to build web components, pages, materials, posters, or applications (e.g., websites, landing pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying any web UI). Generates creative, polished code and UI designs that avoid mediocre AI aesthetics.
---

# Frontend Design Skill

此技能指导创建独特的生产级前端界面，避免平庸的"AI 粗糙"美学。实现真正可用的代码，并高度关注美学细节和创意选择。

## When to Use This Skill

使用此技能当用户请求：
- 构建 Web 组件、页面或完整应用程序
- 创建着陆页、仪表盘或营销页面
- 设计 React、Vue 或原生 HTML/CSS 界面
- 美化或重新设计现有的 Web UI
- 创建海报、素材或视觉设计元素（用于 Web）
- 需要高设计品质和独特美学的任何前端项目

**关键触发词**: Web 组件、页面、应用、网站、着陆页、仪表盘、React 组件、HTML/CSS、UI 设计、美化、前端

## 核心原则

在编写代码之前，必须进行深入的设计思考。每个界面都应该是独特的、有意图的、令人难忘的。

### 设计思维流程

在实现任何代码之前，回答以下问题：

#### 1. 目的 (Purpose)
- **问题**: 此界面解决什么问题？
- **用户**: 谁使用它？在什么情境下使用？
- **目标**: 用户需要完成什么任务？

#### 2. 风格方向 (Style Direction)
选择一个**明确且大胆**的美学方向。不要选择"现代简约"这样的通用描述，而是选择极致的风格：

**风格选项**（但不限于这些）：
- **极简主义**: 极度克制，大量留白，精准排版
- **极致混乱**: 密集布局，重叠元素，视觉冲击
- **复古未来主义**: 80年代霓虹色，网格，合成波风格
- **有机/自然**: 流动形状，自然色调，柔和曲线
- **奢华/精致**: 优雅字体，金色点缀，精细细节
- **俏皮/玩具感**: 明亮色彩，圆角，趣味动画
- **编辑/杂志风格**: 大胆排版，网格系统，黑白为主
- **粗犷/原始**: 单色，硬边，实用主义
- **装饰艺术/几何**: 对称图案，几何形状，高对比度
- **柔和/粉彩**: 温和色彩，渐变，梦幻感
- **工业/实用**: 系统字体，单色，功能优先
- **新拟态**: 柔和阴影，浮雕效果，微妙深度
- **玻璃态**: 模糊背景，透明度，光感

**关键**: 选择清晰的概念方向并精准执行。大胆的极致主义和精致的极简主义都有效——关键在于**意图**，而不是强度。

#### 3. 技术限制 (Constraints)
- 使用什么框架？（React, Vue, 原生 HTML/CSS）
- 性能要求？（动画复杂度，文件大小）
- 可访问性要求？（ARIA 标签，键盘导航，色彩对比度）
- 浏览器兼容性？

#### 4. 差异化 (Differentiation)
- **记忆点**: 是什么让它令人难忘？
- **独特性**: 用户会记住哪一个细节？
- **惊喜**: 哪里会让用户眼前一亮？

## 前端美学指南

### 1. 排版 (Typography)

**原则**: 字体选择是设计的灵魂。

**Do**:
- ✅ 选择**独特且有个性**的字体
- ✅ 标题使用引人注目的字体，正文使用易读字体
- ✅ 尝试意想不到的字体配对
- ✅ 使用字体变体（font-weight, font-style）创造层次
- ✅ 精确控制字间距（letter-spacing）和行高（line-height）

**Don't**:
- ❌ 使用通用字体：Arial, Helvetica, Inter, Roboto, 系统字体
- ❌ 所有文本使用相同的字体和大小
- ❌ 忽略字体加载性能（使用 font-display: swap）

**推荐字体来源**:
- Google Fonts (选择小众、独特的字体)
- 自定义字体（如果项目允许）

**示例字体组合**:
```css
/* 极简编辑风格 */
--font-heading: 'Playfair Display', serif;
--font-body: 'Source Sans Pro', sans-serif;

/* 现代科技风格 */
--font-heading: 'Space Mono', monospace;
--font-body: 'DM Sans', sans-serif;

/* 优雅奢华风格 */
--font-heading: 'Cormorant Garamond', serif;
--font-body: 'Lato', sans-serif;
```

### 2. 颜色与主题 (Color & Theme)

**原则**: 颜色定义情绪和品牌。

**Do**:
- ✅ 使用 CSS 变量保持一致性
- ✅ 主色调 + 鲜明点缀色的组合
- ✅ 考虑色彩心理学（蓝色=信任，红色=紧迫，绿色=成功）
- ✅ 使用渐变营造深度（但要有品味）
- ✅ 保持色彩对比度（WCAG AA 标准：至少 4.5:1）

**Don't**:
- ❌ 俗套配色：白色背景 + 紫色渐变
- ❌ 过多颜色（3-5 个主色已足够）
- ❌ 忽略可访问性

**示例主题**:
```css
:root {
  /* 极简黑白 */
  --color-primary: #000000;
  --color-secondary: #ffffff;
  --color-accent: #ff3366;

  /* 复古未来 */
  --color-primary: #1a1a2e;
  --color-secondary: #16213e;
  --color-accent: #00fff5;
  --color-highlight: #ff006e;

  /* 自然有机 */
  --color-primary: #2d6a4f;
  --color-secondary: #52b788;
  --color-accent: #ffc857;
}
```

### 3. 动效 (Animation & Motion)

**原则**: 动画应该增强体验，而不是分散注意力。

**Do**:
- ✅ 优先使用 CSS 动画（性能更好）
- ✅ 设计页面加载动画（首次印象）
- ✅ 使用 `animation-delay` 实现元素逐个显示
- ✅ 悬停状态添加微妙过渡
- ✅ 滚动触发动画（Intersection Observer）
- ✅ 对于 React，使用 Framer Motion 或 React Spring

**Don't**:
- ❌ 过度使用动画（每个元素都在动）
- ❌ 动画持续时间过长（> 500ms 会让人不耐烦）
- ❌ 忽略 `prefers-reduced-motion` 媒体查询

**示例动画**:
```css
/* 页面加载 - 元素逐个淡入 */
.fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

.fade-in-up:nth-child(1) { animation-delay: 0.1s; }
.fade-in-up:nth-child(2) { animation-delay: 0.2s; }
.fade-in-up:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 悬停效果 */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
```

### 4. 空间构成 (Spatial Composition)

**原则**: 布局应该引导视线，创造视觉节奏。

**Do**:
- ✅ 尝试不对称布局
- ✅ 使用重叠元素创造深度
- ✅ 对角线流程引导视线
- ✅ 打破网格的元素（但有意图）
- ✅ 宽敞的留白或精心控制的密度
- ✅ 使用 Grid 和 Flexbox 创造复杂布局

**Don't**:
- ❌ 所有元素居中对齐
- ❌ 均匀分布的网格（无聊）
- ❌ 忽略响应式设计

**示例布局技巧**:
```css
/* 不对称网格 */
.grid-asymmetric {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

/* 重叠效果 */
.overlap-container {
  position: relative;
}

.overlap-item {
  position: absolute;
  z-index: 2;
  transform: translate(-20%, -20%);
}

/* 对角线流程 */
.diagonal-section {
  transform: skewY(-3deg);
  padding: 100px 0;
}

.diagonal-section > * {
  transform: skewY(3deg);
}
```

### 5. 背景和视觉细节 (Background & Visual Details)

**原则**: 背景营造氛围和深度。

**Do**:
- ✅ 渐变网格
- ✅ 噪点纹理
- ✅ 几何图案
- ✅ 分层透明度
- ✅ 戏剧性阴影
- ✅ 装饰性边框
- ✅ 自定义光标（如果适合风格）
- ✅ 颗粒叠加效果

**Don't**:
- ❌ 纯色背景（除非极简风格）
- ❌ 低质量或不相关的库存图片
- ❌ 过度使用阴影（box-shadow 污染）

**示例背景效果**:
```css
/* 渐变网格背景 */
.gradient-grid {
  background:
    linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px),
    linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-size: 50px 50px, 50px 50px, 100% 100%;
}

/* 噪点纹理 */
.noise-texture {
  position: relative;
}

.noise-texture::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* 玻璃态效果 */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

## 避免通用 AI 美学

**绝对禁止的元素**:
- ❌ 过度使用的字体：Inter, Roboto, Arial, 系统字体
- ❌ 俗套配色：白色背景 + 紫色渐变
- ❌ 可预测的布局模式（居中卡片网格）
- ❌ 缺乏特定上下文特征的千篇一律设计

**如何避免**:
- ✅ 为每个项目选择**不同**的字体
- ✅ 在浅色/深色主题之间变化
- ✅ 尝试不同的布局结构
- ✅ 添加独特的品牌元素和个性

## 实现复杂性与美学匹配

**关键原则**: 代码复杂度应与设计愿景相匹配。

### 极繁主义设计 → 复杂代码
- 大量动画和过渡效果
- 多层叠加元素
- 复杂的交互状态
- 详细的视觉效果（粒子、渐变、纹理）

```jsx
// 示例：复杂的动画卡片
<motion.div
  initial={{ opacity: 0, scale: 0.8, rotateX: -15 }}
  animate={{ opacity: 1, scale: 1, rotateX: 0 }}
  whileHover={{
    scale: 1.05,
    rotateY: 5,
    boxShadow: "0 25px 50px rgba(0,0,0,0.2)"
  }}
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 20
  }}
>
  {/* 复杂内容 */}
</motion.div>
```

### 极简主义设计 → 精准代码
- 克制的动画（仅在关键时刻）
- 精确的间距和排版
- 细微的过渡效果
- 关注细节而非数量

```css
/* 示例：精致的极简主义 */
.minimal-card {
  padding: 60px;
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.08);
  transition: border-color 0.3s ease;
}

.minimal-card:hover {
  border-color: rgba(0,0,0,0.2);
}

.minimal-card h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.5rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin: 0 0 20px 0;
}
```

## 工作流程

### 第 1 步：理解需求
- 阅读用户请求，提取关键信息
- 确定项目类型（组件、页面、完整应用）
- 识别技术栈（React、Vue、原生 HTML/CSS）

### 第 2 步：设计思考
- 回答设计思维流程中的 4 个问题
- 选择明确的美学方向
- 在心中可视化最终效果

### 第 3 步：技术决策
- 选择框架和工具
- 决定动画库（Framer Motion、CSS、React Spring）
- 确定字体来源

### 第 4 步：实现
- 编写语义化 HTML 结构
- 实现 CSS 样式（使用 CSS 变量）
- 添加交互和动画
- 确保响应式设计

### 第 5 步：精细化
- 调整间距和排版
- 优化动画时间
- 测试不同屏幕尺寸
- 确保可访问性（ARIA、键盘导航）

## 示例场景

### 场景 1: 创建着陆页

**用户请求**: "帮我创建一个 SaaS 产品的着陆页"

**设计思考**:
- 目的：展示产品价值，吸引用户注册
- 风格：现代科技 + 编辑风格，使用 Space Grotesk 字体，黑白 + 蓝色点缀
- 布局：不对称，英雄区域占据 70% 屏幕，对角线流程
- 差异化：独特的字体配对，大胆的排版层次

**实现重点**:
- Hero section 使用大字号标题（4-6rem）
- 滚动触发的淡入动画
- 玻璃态 CTA 按钮
- 响应式网格展示功能

### 场景 2: 设计仪表盘

**用户请求**: "创建一个数据分析仪表盘"

**设计思考**:
- 目的：清晰展示数据，支持快速决策
- 风格：实用主义 + 精致，使用 IBM Plex Sans，深色主题
- 布局：网格系统，卡片式布局，数据可视化优先
- 差异化：微妙的动画过渡，悬停显示详细信息

**实现重点**:
- 深色背景减少眼睛疲劳
- 卡片使用柔和阴影和边框
- 图表使用鲜明的点缀色
- 加载状态使用骨架屏

### 场景 3: React 组件库

**用户请求**: "创建一套自定义按钮组件"

**设计思考**:
- 目的：可复用、可定制的按钮系统
- 风格：灵活，支持多种变体
- 技术：使用 styled-components 或 CSS modules
- 差异化：独特的悬停效果和加载状态

**实现重点**:
- 主按钮、次要按钮、文本按钮变体
- 大小变体（small, medium, large）
- 加载和禁用状态
- 平滑的过渡动画

## 代码质量标准

### 必须遵守:
- ✅ 语义化 HTML（`<header>`, `<nav>`, `<main>`, `<article>`）
- ✅ BEM 命名规范或 CSS Modules
- ✅ CSS 变量用于颜色和间距
- ✅ 移动优先的响应式设计
- ✅ 可访问性（ARIA 标签，键盘导航）
- ✅ 性能优化（图片懒加载，字体优化）

### 禁止:
- ❌ 内联样式（除非动态值）
- ❌ 不必要的 `!important`
- ❌ 硬编码的颜色值（使用 CSS 变量）
- ❌ 未优化的图片
- ❌ 无意义的类名（`.box1`, `.container2`）

## 技术栈参考

### 推荐工具:
- **字体**: Google Fonts, Font Squirrel
- **颜色**: Coolors.co, Adobe Color
- **动画**: Framer Motion (React), Anime.js, GreenSock
- **图标**: Heroicons, Lucide, Phosphor Icons
- **CSS 框架**: Tailwind CSS (自定义配置), styled-components

### 避免:
- ❌ Bootstrap, Material-UI（容易产生通用外观）
- ❌ 默认 Tailwind 配置（需要自定义）

## 检查清单

在完成实现后，验证以下内容:

- [ ] 选择了独特的字体组合（不是 Inter/Roboto/Arial）
- [ ] 颜色方案有明确的美学方向
- [ ] 至少有 1-2 处精心设计的动画
- [ ] 布局不是简单的居中网格
- [ ] 有独特的视觉细节（背景、纹理、阴影）
- [ ] 响应式设计在手机和桌面都好看
- [ ] 可访问性标准达标（对比度、ARIA）
- [ ] 代码清晰、可维护
- [ ] 性能良好（无卡顿动画，快速加载）

## 最后提醒

> **创造性诠释是关键**。不要问用户"你想要什么颜色？"，而是基于上下文做出大胆的设计决策。每个设计都应该是独一无二的。在不同项目之间变化浅色/深色主题、字体和美学风格。

> **追求卓越，而非完美**。一个有强烈个性的设计胜过一个"安全"但平庸的设计。敢于尝试，为用户带来惊喜。
