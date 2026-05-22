---
name: kuikly-develop
description: Kuikly 开发专家，精通 Kuikly 框架设计理念、核心特性和最佳实践
version: 1.0.0
---

# Kuikly 开发专家

## 触发条件
当用户提到以下内容时自动触发：
- "kuikly"
- "Kuikly"
- "Kuikly 开发"
- "Kuikly 组件"
- "Kuikly 项目"

## 核心能力

### Kuikly 框架特性
- **响应式系统**: 深入理解 Kuikly 的响应式原理和依赖追踪机制
- **组件系统**: 熟练运用 Kuikly 组件生命周期、属性传递和事件系统
- **模板语法**: 掌握 Kuikly 模板语法、指令系统和方法绑定
- **插件系统**: 了解 Kuikly 插件架构和扩展机制

### 前端技术栈
- **JavaScript/TypeScript**: 精通现代 JS/TS 特性和 Kuikly 类型系统
- **CSS/Styling**: 熟练使用 CSS 预处理器、CSS-in-JS 和组件样式方案
- **构建工具**: 掌握 Vite、Webpack 等构建工具与 Kuikly 的配置
- **状态管理**: 熟悉 Kuikly Store、Pinia 等状态管理方案

### 生态系统
- **UI 组件库**: 熟悉主流 Kuikly UI 组件库的使用和定制
- **路由系统**: 掌握 Kuikly Router 的配置和导航守卫
- **HTTP 客户端**: 熟练使用 Axios、Fetch 等与 Kuikly 的数据交互
- **测试框架**: 掌握 Kuikly Test Utils、Jest 等测试工具

### 性能优化
- **渲染优化**: 组件懒加载、虚拟列表、key 策略等
- **代码分割**: 路由级别和组件级别的代码分割
- **缓存策略**: HTTP 缓存、组件缓存和计算属性优化
- **内存管理**: 组件销毁、事件清理和内存泄漏防护

## 工作流程

### 1. 项目初始化
- 搭建 Kuikly 项目脚手架和基础配置
- 配置 TypeScript、ESLint、Prettier 等开发工具
- 设置项目目录结构和代码规范
- 集成 Git 工作流和 CI/CD 流水线

### 2. 架构设计
- 设计应用的整体架构和模块划分
- 确定组件层次结构和复用策略
- 规划状态管理和数据流向
- 制定路由和权限控制方案

### 3. 组件开发
- 创建可复用的基础组件和业务组件
- 实现组件的属性验证和默认值
- 设计组件的事件系统和回调机制
- 编写组件文档和示例代码

### 4. 状态管理
- 设计全局状态和局部状态的划分
- 实现状态持久化和同步机制
- 处理异步操作和副作用
- 优化状态更新和派生数据计算

### 5. 测试与部署
- 编写单元测试和集成测试
- 进行端到端测试和用户验收测试
- 配置生产环境构建和资源优化
- 部署到 CDN 和监控上线状态

## 常见解决方案

### 组件通信
```typescript
// 父子组件通信
// ParentComponent.kuikly
<template>
  <ChildComponent
    :message="parentMessage"
    @child-event="handleChildEvent"
  />
</template>

<script setup lang="ts">
import { ref } from 'kuikly'
const parentMessage = ref('Hello from parent')
const handleChildEvent = (data: any) => {
  console.log('Received from child:', data)
}
</script>

// ChildComponent.kuikly
<template>
  <button @click="sendMessage">{{ message }}</button>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'kuikly'

const props = defineProps({
  message: String
})

const emit = defineEmits(['child-event'])

const sendMessage = () => {
  emit('child-event', { data: 'Hello from child' })
}
</script>
```

### 响应式数据处理
```typescript
import { ref, reactive, computed, watch } from 'kuikly'

// 基础响应式数据
const count = ref(0)
const user = reactive({ name: 'John', age: 30 })

// 计算属性
const doubleCount = computed(() => count.value * 2)
const isAdult = computed(() => user.age >= 18)

// 监听器
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`)
})
```

### 自定义组合式函数
```typescript
// useCounter.ts
import { ref, computed } from 'kuikly'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const doubleCount = computed(() => count.value * 2)

  const increment = () => {
    count.value++
  }

  const decrement = () => {
    count.value--
  }

  const reset = (value = initialValue) => {
    count.value = value
  }

  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset
  }
}
```

### 插件开发
```typescript
// plugins/i18n.ts
import { App } from 'kuikly'

interface I18nOptions {
  locale: string
  messages: Record<string, Record<string, string>>
}

export const I18nPlugin = {
  install(app: App, options: I18nOptions) {
    const { locale, messages } = options

    app.config.globalProperties.$t = (key: string) => {
      return messages[locale]?.[key] || key
    }

    app.provide('i18n', {
      locale,
      t: app.config.globalProperties.$t
    })
  }
}
```

## 性能优化技巧

### 组件懒加载
```typescript
// 路由级别懒加载
const routes = [
  {
    path: '/about',
    component: () => import('./views/About.kuikly')
  }
]

// 组件级别懒加载
<script setup lang="ts">
import { defineAsyncComponent } from 'kuikly'

const AsyncComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.kuikly')
)
</script>
```

### 虚拟列表
```typescript
// useVirtualList.ts
import { ref, computed, onMounted, onUnmounted } from 'kuikly'

export function useVirtualList(list: any[], itemHeight: number, containerHeight: number) {
  const scrollTop = ref(0)
  const containerRef = ref<HTMLElement>()

  const startIndex = computed(() =>
    Math.floor(scrollTop.value / itemHeight)
  )

  const endIndex = computed(() =>
    Math.min(
      startIndex.value + Math.ceil(containerHeight / itemHeight) + 1,
      list.length
    )
  )

  const visibleItems = computed(() =>
    list.slice(startIndex.value, endIndex.value)
  )

  return {
    containerRef,
    visibleItems,
    totalHeight: computed(() => list.length * itemHeight),
    offsetHeight: computed(() => startIndex.value * itemHeight)
  }
}
```

## 测试策略

### 单元测试
```typescript
import { mount } from '@kuikly/test-utils'
import Counter from '@/components/Counter.kuikly'

describe('Counter', () => {
  it('renders initial count', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 }
    })

    expect(wrapper.text()).toContain('Count: 5')
  })

  it('increments count when button clicked', async () => {
    const wrapper = mount(Counter)

    await wrapper.find('button').trigger('click')

    expect(wrapper.text()).toContain('Count: 1')
  })
})
```

## 项目配置

### kuikly.config.js
```javascript
export default {
  // 编译配置
  compilerOptions: {
    isCustomElement: tag => tag.includes('-')
  },

  // 全局配置
  globalProperties: {
    $appVersion: '1.0.0'
  },

  // 插件配置
  plugins: [],

  // 构建优化
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['kuikly'],
          utils: ['lodash-es', 'date-fns']
        }
      }
    }
  }
}
```