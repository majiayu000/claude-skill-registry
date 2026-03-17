---
name: frontend-vue
description: 专业的 Vue.js 开发技能，涵盖 Nuxt 3、Vue 3 Composition API、Tailwind CSS 和 Vue 生态系统。使用此技能构建 Vue 应用程序、实现 Nuxt 功能、使用 Pinia 进行状态管理，或使用 shadcn-vue 等组件库。
---

# Vue 开发技能

现代 Vue.js 开发的综合技能，专注于 Nuxt 3、Vue 3 Composition API、Tailwind CSS 和 Vue 生态系统。

## 技术栈

### 核心框架：Vue 3 + Nuxt 3

#### Vue 3 特性
- **组合式 API (Composition API)**：使用 `<script setup>` 复用逻辑
- **响应式系统**：`ref`, `reactive`, `computed`, `watch`
- **Teleport**：将内容渲染到组件 DOM 层次结构之外
- **Fragments**：支持多个根节点
- **Suspense**：处理异步依赖

#### Nuxt 3 特性
- **自动导入**：自动导入 Vue API 和组件
- **基于文件的路由**：`pages/` 目录中的文件创建路由
- **服务器引擎 (Nitro)**：通用部署
- **数据获取**：`useFetch`, `useAsyncData`
- **服务器路由**：`server/api/` 中的 API 端点
- **SEO/Meta**：`useHead`, `useSeoMeta`

### UI 框架：Tailwind CSS + shadcn-vue

#### Tailwind CSS
- 实用优先架构
- 通过 `tailwind.config.ts` 配置
- 使用 PostCSS 优化

#### shadcn-vue (或类似库)
- shadcn/ui 的 Vue 移植版
- 基于 Radix Vue 的可访问组件
- **关键组件**：Button, Input, Select, Dialog, Toast

### 状态管理
- **Pinia**：Vue 官方状态管理库
  - 模块化 Store
  - TypeScript 支持
  - DevTools 集成
  - 无 Mutation (只有 Actions)

## 项目架构

### 推荐目录结构 (Nuxt 3)
```
project-root/
├── app.vue            # 根组件
├── nuxt.config.ts     # 配置
├── components/        # 自动导入组件
│   ├── ui/            # UI 库组件
│   │   ├── button/
│   │   └── ...
│   └── Header.vue
├── pages/             # 路由
│   ├── index.vue
│   └── about.vue
├── layouts/           # 布局包装器
│   └── default.vue
├── composables/       # 自动导入逻辑
│   └── useUser.ts
├── server/            # 服务器 API
│   └── api/
│       └── hello.ts
├── stores/            # Pinia stores
│   └── counter.ts
└── assets/            # CSS, 图片
    └── main.css
```

## 最佳实践

### 使用 `<script setup>` 的组合式 API
- 对响应式变量使用 `const`。
- 按功能组织逻辑。
- 将复杂逻辑提取到组合式函数中 (`composables/`)。

### 性能
- **异步组件**：使用 `defineAsyncComponent` 进行懒加载。
- **懒获取**：对非关键数据在 `useFetch` 中使用 `lazy: true` 选项。
- **资源优化**：使用 Nuxt Image 进行图片优化。

### Nuxt 特定注意事项
- **水合不匹配 (Hydration Mismatch)**：确保服务器渲染的 HTML 与客户端匹配。避免在初始渲染时使用随机 ID 或日期。
- **中间件**：使用路由中间件进行权限守卫 (`middleware/auth.ts`)。

## 常见代码模式

### 带数据获取的 Nuxt 页面
```vue
<script setup lang="ts">
const { data: user, error } = await useFetch('/api/user/1')

if (error.value) {
  console.error(error.value)
}
</script>

<template>
  <div v-if="user" class="p-4">
    <h1 class="text-2xl font-bold">{{ user.name }}</h1>
    <p>{{ user.email }}</p>
  </div>
  <div v-else>加载中...</div>
</template>
```

### Pinia Store
```ts
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})
```

### 组合式函数 (Composable)
```ts
// composables/useMouse.ts
export function useMouse() {
  const x = ref(0)
  const y = ref(0)

  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  return { x, y }
}
```
