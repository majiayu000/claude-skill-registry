---
name: frontend
description: "Frontend patterns: component design, state management, performance, accessibility. Use when building web frontends, components, or client-side apps."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 前端开发模式

本技能提供前端开发的最佳实践和模式，支持多框架按需加载。

## 触发条件

- 创建或修改前端组件
- 设计 UI/UX 交互
- 实现状态管理
- 性能优化
- 无障碍开发

## 框架专属模式

根据项目技术栈，加载对应的框架专属文件：

| 技术栈  | 加载文件     | 框架              |
| ------- | ------------ | ----------------- |
| Vue     | `vue.md`     | Vue 3, Nuxt 3     |
| React   | `react.md`   | React 18, Next.js |
| Svelte  | `svelte.md`  | Svelte, SvelteKit |
| Angular | `angular.md` | Angular 17+       |

**加载方式**: 检测项目中的 `package.json` 依赖确定技术栈。

---

## 通用组件模式

### 组件分类

```
┌─────────────────────────────────────────────────────┐
│                    组件金字塔                         │
├─────────────────────────────────────────────────────┤
│  页面组件 (Pages/Views)                              │
│  ├─ 负责路由和布局                                   │
│  ├─ 组合多个功能组件                                 │
│  └─ 管理页面级状态                                   │
├─────────────────────────────────────────────────────┤
│  功能组件 (Features/Containers)                      │
│  ├─ 包含业务逻辑                                     │
│  ├─ 连接状态管理                                     │
│  └─ 调用 API                                        │
├─────────────────────────────────────────────────────┤
│  UI 组件 (UI/Presentational)                        │
│  ├─ 纯展示，无业务逻辑                               │
│  ├─ 通过 props 接收数据                              │
│  └─ 通过 events 通知父组件                           │
├─────────────────────────────────────────────────────┤
│  基础组件 (Base/Primitives)                         │
│  ├─ Button, Input, Card 等                          │
│  ├─ 高度可复用                                       │
│  └─ 设计系统基础                                     │
└─────────────────────────────────────────────────────┘
```

### 组件设计原则

| 原则             | 说明                        |
| ---------------- | --------------------------- |
| **单一职责**     | 一个组件只做一件事          |
| **Props 向下**   | 数据从父组件流向子组件      |
| **Events 向上**  | 事件从子组件通知父组件      |
| **组合优于继承** | 使用 slot/children 组合组件 |
| **可预测**       | 相同 props 产生相同输出     |

### 命名规范

```
components/
├── ui/                    # 基础组件（PascalCase）
│   ├── Button.vue/tsx
│   ├── Input.vue/tsx
│   └── Card.vue/tsx
├── feature/               # 功能组件（PascalCase）
│   ├── UserCard.vue/tsx
│   └── OrderList.vue/tsx
└── layout/                # 布局组件（PascalCase）
    ├── Header.vue/tsx
    └── Sidebar.vue/tsx
```

---

## 状态管理模式

### 状态分层

| 层级           | 范围     | 存储方式      | 示例              |
| -------------- | -------- | ------------- | ----------------- |
| **组件状态**   | 单个组件 | useState/ref  | 表单输入、UI 状态 |
| **共享状态**   | 多个组件 | Context/Store | 用户信息、主题    |
| **服务器状态** | 来自 API | Query Cache   | 列表数据、详情    |
| **URL 状态**   | 路由参数 | Router        | 页码、筛选条件    |
| **持久状态**   | 跨会话   | localStorage  | 用户偏好          |

### 状态管理选择

```
简单共享状态 → Context/Provide
  ↓ 复杂度增加
中等应用 → Pinia/Zustand
  ↓ 复杂度增加
大型应用 → Redux/Vuex + 规范化
```

### 服务器状态管理

```
API 请求 → Query Library（TanStack Query）
  ├─ 自动缓存
  ├─ 重新验证
  ├─ 乐观更新
  └─ 错误重试
```

---

## 性能优化模式

### 渲染优化

| 技术               | 用途         | 框架实现                          |
| ------------------ | ------------ | --------------------------------- |
| **Memoization**    | 避免重复计算 | useMemo/computed                  |
| **Lazy Loading**   | 延迟加载组件 | lazy/defineAsyncComponent         |
| **Virtual List**   | 大列表渲染   | react-window/vue-virtual-scroller |
| **Code Splitting** | 按需加载代码 | 动态 import                       |

### 资源优化

```
图片优化:
├─ 响应式图片（srcset）
├─ 懒加载（loading="lazy"）
├─ 现代格式（WebP/AVIF）
└─ 图片 CDN

脚本优化:
├─ Tree Shaking
├─ Bundle 分析
├─ 预加载关键资源
└─ 延迟非关键脚本
```

### 性能指标

| 指标    | 目标    | 说明         |
| ------- | ------- | ------------ |
| **LCP** | < 2.5s  | 最大内容绘制 |
| **FID** | < 100ms | 首次输入延迟 |
| **CLS** | < 0.1   | 累积布局偏移 |
| **TTI** | < 3.8s  | 可交互时间   |

---

## 无障碍模式 (a11y)

### 基础清单

- [ ] **语义化 HTML** - 使用正确的元素（button, nav, main...）
- [ ] **键盘可访问** - 所有交互可用键盘完成
- [ ] **焦点管理** - 焦点顺序合理，焦点可见
- [ ] **ARIA 标签** - 为动态内容添加适当标签
- [ ] **颜色对比** - 符合 WCAG 2.1 AA 标准（4.5:1）
- [ ] **替代文本** - 图片有 alt，图标有 aria-label

### 常见 ARIA 模式

```html
<!-- 按钮 -->
<button aria-label="关闭菜单" aria-expanded="false">
  <Icon name="close" aria-hidden="true" />
</button>

<!-- 表单 -->
<input
  aria-labelledby="label-id"
  aria-describedby="hint-id error-id"
  aria-invalid="true"
/>

<!-- 动态内容 -->
<div aria-live="polite" aria-busy="false">加载完成</div>

<!-- 对话框 -->
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">对话框标题</h2>
</div>
```

### 键盘交互

| 元素    | 按键        | 行为     |
| ------- | ----------- | -------- |
| 按钮    | Enter/Space | 激活     |
| 链接    | Enter       | 导航     |
| 菜单    | ↑↓          | 移动焦点 |
| 对话框  | Esc         | 关闭     |
| Tab列表 | ←→          | 切换标签 |

---

## 表单模式

### 表单验证

```
客户端验证:
├─ 实时验证（onChange）
├─ 提交验证（onSubmit）
├─ 字段级错误
└─ 表单级错误

验证库:
├─ React: react-hook-form + zod
├─ Vue: vee-validate + zod
└─ 通用: yup/zod
```

### 表单状态

```
{
  values: {},        // 字段值
  errors: {},        // 验证错误
  touched: {},       // 字段已交互
  isSubmitting: false,
  isValid: true
}
```

### 错误处理

```html
<!-- 字段错误 -->
<div class="field">
  <label for="email">邮箱</label>
  <input id="email" aria-invalid="true" aria-describedby="email-error" />
  <span id="email-error" role="alert" class="error">
    请输入有效的邮箱地址
  </span>
</div>

<!-- 表单级错误 -->
<div role="alert" class="form-error">提交失败：网络错误，请重试</div>
```

---

## 动画模式

### 动画类型

| 类型          | 用途           | 实现               |
| ------------- | -------------- | ------------------ |
| **进入/退出** | 元素出现/消失  | CSS Transition     |
| **状态变化**  | hover/active   | CSS Transition     |
| **列表动画**  | 添加/删除/排序 | FLIP 动画          |
| **页面切换**  | 路由过渡       | 路由动画           |
| **复杂动画**  | 多阶段动画     | Framer Motion/GSAP |

### 动画原则

1. **有意义** - 动画应该传达信息
2. **快速** - 持续时间 150-300ms
3. **可禁用** - 尊重 `prefers-reduced-motion`
4. **不阻塞** - 不影响用户操作

### 减少动画

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 设计美学（避免 AI Slop）

> 详见 [design-guide.md](./design-guide.md) — AI 通用审美定义、设计思维方向矩阵、反模式清单与审查清单。

---

## 测试模式

> 前端测试策略详见 `rules/frontend/frontend-testing.md` 和 `rules/frontend/frontend-e2e.md`（按文件类型自动加载）。

---

## 框架专属内容

详细的框架专属实现请参考：

- **Vue**: [vue.md](./vue.md) - Vue 3 + Composition API
- **React**: [react.md](./react.md) - React 18 + Hooks
- **Svelte**: [svelte.md](./svelte.md) - Svelte/SvelteKit
- **Angular**: [angular.md](./angular.md) - Angular 17+

## 专项优化

- **性能优化**: [performance.md](./performance.md) - Core Web Vitals (LCP/INP/CLS)
- **Tailwind CSS**: [tailwind.md](./tailwind.md) - Tailwind 最佳实践 + v4 迁移指南
- **设计指南**: [design-guide.md](./design-guide.md) - Designer 角色设计方法论与审查清单

---

## Maintenance

- Sources: MDN, WCAG 2.1, web.dev, 各框架官方文档
- Last updated: 2025-01-22
- Pattern: 通用清单 + 按需加载框架专属

> **记住**: 前端开发的核心是用户体验——性能、无障碍、交互细节缺一不可，独特的设计比通用模板更有价值。
