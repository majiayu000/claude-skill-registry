---
name: vue3-frontend-dev
description: Vue3 前端开发规范和最佳实践指南。适用于现代Vue3项目开发，涵盖代码组织、Composition API、状态管理、性能优化、测试等全方位内容。
---

# Vue3 前端开发规范

## 技术栈

本项目基于 **Vue 3 + TypeScript + Vite + Pinia + Vue Router 4 + Axios + Tailwind CSS + Element Plus/Vant**

## 核心原则

- **组件化设计**：小而美、可复用、可组合
- **Composition API**：使用 `<script setup>` 语法
- **类型安全**：强制使用TypeScript
- **性能优先**：代码分割、懒加载、虚拟滚动
- **用户体验**：响应式设计、加载状态、错误处理
- **代码规范**：ESLint + Prettier + Stylelint

## 项目结构

### 目录组织

```
project-root/
├── src/
│   ├── api/            # API接口定义
│   │   ├── user.ts
│   │   ├── product.ts
│   │   └── index.ts
│   ├── assets/         # 静态资源
│   │   ├── images/
│   │   ├── fonts/
│   │   └── styles/
│   ├── components/     # 公共组件
│   │   ├── common/     # 通用组件
│   │   └── business/   # 业务组件
│   ├── composables/    # 组合式函数
│   │   ├── useAuth.ts
│   │   ├── useRequest.ts
│   │   └── useTable.ts
│   ├── router/         # 路由配置
│   │   ├── index.ts
│   │   └── routes/
│   ├── stores/         # 状态管理（Pinia）
│   │   ├── user.ts
│   │   ├── app.ts
│   │   └── modules/
│   ├── types/          # TypeScript类型定义
│   │   ├── api.d.ts
│   │   ├── components.d.ts
│   │   └── global.d.ts
│   ├── utils/          # 工具函数
│   │   ├── request.ts  # Axios封装
│   │   ├── storage.ts  # 本地存储
│   │   └── validate.ts
│   ├── views/          # 页面组件
│   ├── App.vue
│   └── main.ts
├── public/             # 公共资源
├── tests/              # 测试文件
│   ├── unit/
│   └── e2e/
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## Vue3 规范

### 组件开发

#### 基础组件结构

```vue
<template>
  <div class="user-card">
    <h3 class="user-name">{{ user.name }}</h3>
    <p class="user-email">{{ user.email }}</p>
    <button @click="handleEdit">编辑</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types/api'

// Props定义
interface Props {
  user: User
  readonly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

// Emits定义
interface Emits {
  (e: 'edit', user: User): void
  (e: 'delete', userId: number): void
}

const emit = defineEmits<Emits>()

// 响应式状态
const isEditing = ref(false)
const formData = ref<User>({ ...props.user })

// 计算属性
const displayName = computed(() => {
  return props.user.name || '未知用户'
})

// 方法
const handleEdit = () => {
  emit('edit', props.user)
}

// 生命周期
onMounted(() => {
  console.log('UserCard mounted')
})
</script>

<style scoped lang="scss">
.user-card {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  
  .user-name {
    font-size: 18px;
    font-weight: 600;
  }
  
  .user-email {
    color: #6b7280;
  }
}
</style>
```

#### 命名规范

- **组件文件**：PascalCase（如 `UserCard.vue`）
- **变量和函数**：camelCase（如 `userName`、`handleClick`）
- **组件标签**：kebab-case（如 `<user-card>`）
- **Props**：camelCase（如 `userName`）
- **Events**：kebab-case（如 `@user-update`）

```vue
<!-- 组件文件名：UserCard.vue -->
<template>
  <div>
    <user-card :user="userData" @user-update="handleUpdate" />
  </div>
</template>

<script setup lang="ts">
const userData = ref<User>({ name: '张三', email: 'zhangsan@example.com' })
const handleUpdate = (updatedUser: User) => {
  console.log('用户更新:', updatedUser)
}
</script>
```

### Composition API 最佳实践

#### 组合式函数

```typescript
// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

export function useAuth() {
  const userStore = useUserStore()
  const isAuthenticated = computed(() => userStore.isAuthenticated)
  const user = computed(() => userStore.user)
  
  const login = async (credentials: LoginRequest) => {
    try {
      await userStore.login(credentials)
      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }
  
  const logout = async () => {
    await userStore.logout()
  }
  
  return {
    isAuthenticated,
    user,
    login,
    logout
  }
}
```

#### 使用组合式函数

```vue
<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated, user, login, logout } = useAuth()

const handleLogin = async () => {
  const success = await login({
    username: 'admin',
    password: 'password123'
  })
  if (success) {
    console.log('登录成功')
  }
}
</script>
```

## API 调用规范

### Axios 封装

```typescript
// utils/request.ts
import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import type { Result } from '@/types/api'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse<Result>) => {
    const { code, data, message } = response.data
    
    // 成功响应
    if (code === 0) {
      return data
    }
    
    // 业务错误
    ElMessage.error(message || '请求失败')
    return Promise.reject(new Error(message))
  },
  (error) => {
    // HTTP错误
    if (error.response) {
      const { status } = error.response
      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录')
          // 跳转登录页
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('拒绝访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(`请求失败: ${status}`)
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default service
```

### API 接口定义

```typescript
// api/user.ts
import request from '@/utils/request'
import type { User, UserCreate, UserUpdate, UserListParams } from '@/types/api'

/**
 * 获取用户列表
 */
export function getUserList(params: UserListParams) {
  return request<User[]>({
    url: '/api/v1/users',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情
 */
export function getUserById(id: number) {
  return request<User>({
    url: `/api/v1/users/${id}`,
    method: 'get'
  })
}

/**
 * 创建用户
 */
export function createUser(data: UserCreate) {
  return request<User>({
    url: '/api/v1/users',
    method: 'post',
    data
  })
}

/**
 * 更新用户
 */
export function updateUser(id: number, data: UserUpdate) {
  return request<User>({
    url: `/api/v1/users/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 */
export function deleteUser(id: number) {
  return request<void>({
    url: `/api/v1/users/${id}`,
    method: 'delete'
  })
}
```

### 使用Mock数据

```typescript
// api/mock.ts
export const MOCK_ENABLED = import.meta.env.VITE_MOCK_ENABLED === 'true'

export const mockUserList: User[] = [
  {
    id: 1,
    name: '张三',
    email: 'zhangsan@example.com'
  },
  {
    id: 2,
    name: '李四',
    email: 'lisi@example.com'
  }
]

// api/user.ts
import { MOCK_ENABLED, mockUserList } from './mock'

export function getUserList(params: UserListParams) {
  if (MOCK_ENABLED) {
    return Promise.resolve(mockUserList)
  }
  
  return request<User[]>({
    url: '/api/v1/users',
    method: 'get',
    params
  })
}
```

## 状态管理

### Pinia Store 定义

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string>('')
  const permissions = ref<string[]>([])
  
  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userName = computed(() => user.value?.name || '')
  const hasPermission = computed(() => {
    return (permission: string) => permissions.value.includes(permission)
  })
  
  // Actions
  const setUser = (userData: User) => {
    user.value = userData
  }
  
  const setToken = (tokenValue: string) => {
    token.value = tokenValue
    localStorage.setItem('token', tokenValue)
  }
  
  const setPermissions = (perms: string[]) => {
    permissions.value = perms
  }
  
  const login = async (credentials: LoginRequest) => {
    // 调用API登录
    const response = await loginApi(credentials)
    setUser(response.user)
    setToken(response.token)
    setPermissions(response.permissions)
  }
  
  const logout = async () => {
    // 调用API登出
    await logoutApi()
    user.value = null
    token.value = ''
    permissions.value = []
    localStorage.removeItem('token')
  }
  
  const updateUserInfo = (updates: Partial<User>) => {
    if (user.value) {
      Object.assign(user.value, updates)
    }
  }
  
  return {
    user,
    token,
    permissions,
    isAuthenticated,
    userName,
    hasPermission,
    setUser,
    setToken,
    setPermissions,
    login,
    logout,
    updateUserInfo
  }
})
```

### 使用Store

```vue
<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 访问state
console.log(userStore.user)

// 访问getters
console.log(userStore.isAuthenticated)
console.log(userStore.userName)

// 调用actions
const handleLogin = async () => {
  await userStore.login({
    username: 'admin',
    password: 'password123'
  })
}

const handleLogout = async () => {
  await userStore.logout()
}
</script>

<template>
  <div v-if="userStore.isAuthenticated">
    欢迎您，{{ userStore.userName }}
  </div>
  <div v-else>
    请先登录
  </div>
</template>
```

## 路由配置

### 路由定义

```typescript
// router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('@/views/Users.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: () => import('@/views/UserDetail.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    // 需要认证但未登录，跳转到登录页
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
```

## TypeScript 类型定义

### API 类型

```typescript
// types/api.d.ts

// 通用响应
export interface Result<T = any> {
  code: number
  data: T
  message: string
}

// 分页响应
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// 用户相关
export interface User {
  id: number
  name: string
  email: string
  avatar?: string
  status: number
  createdAt: string
  updatedAt: string
}

export interface UserCreate {
  name: string
  email: string
  password: string
}

export interface UserUpdate {
  name?: string
  email?: string
  avatar?: string
  status?: number
}

export interface UserListParams {
  page?: number
  pageSize?: number
  name?: string
  email?: string
  status?: number
}

// 登录请求
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应
export interface LoginResponse {
  user: User
  token: string
  permissions: string[]
}
```

### 组件类型

```typescript
// types/components.d.ts
export interface BaseProps {
  id?: string | number
  class?: string
  style?: string | Record<string, any>
}

export interface ButtonProps extends BaseProps {
  type?: 'primary' | 'success' | 'warning' | 'danger'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  loading?: boolean
}

export interface FormProps extends BaseProps {
  model: Record<string, any>
  rules?: Record<string, any>
  labelWidth?: string | number
}
```

## 性能优化

### 代码分割和懒加载

```typescript
// 路由级别代码分割
const routes: RouteRecordRaw[] = [
  {
    path: '/users',
    component: () => import('@/views/Users.vue')  // 懒加载
  }
]

// 组件级别懒加载
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>
```

### 虚拟滚动

```vue
<template>
  <div class="virtual-list">
    <virtual-list
      :data-sources="items"
      :data-key="'id'"
      :keeps="30"
      :estimate-size="50"
    >
      <template #default="{ source }">
        <div class="list-item">{{ source.name }}</div>
      </template>
    </virtual-list>
  </div>
</template>
```

### 防抖和节流

```typescript
// composables/useDebounce.ts
import { ref, watch } from 'vue'

export function useDebounce<T>(value: Ref<T>, delay: number = 300) {
  const debouncedValue = ref<T>(value.value)
  
  let timeout: ReturnType<typeof setTimeout>
  
  watch(value, (newValue) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })
  
  return debouncedValue
}
```

## 测试规范

### 单元测试

```typescript
// tests/unit/components/UserCard.spec.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import UserCard from '@/components/UserCard.vue'

describe('UserCard.vue', () => {
  const mockUser = {
    id: 1,
    name: '张三',
    email: 'zhangsan@example.com'
  }
  
  it('渲染用户信息', () => {
    const wrapper = mount(UserCard, {
      props: {
        user: mockUser
      }
    })
    
    expect(wrapper.find('.user-name').text()).toBe('张三')
    expect(wrapper.find('.user-email').text()).toBe('zhangsan@example.com')
  })
  
  it('触发编辑事件', async () => {
    const wrapper = mount(UserCard, {
      props: {
        user: mockUser
      }
    })
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('edit')).toBeTruthy()
    expect(wrapper.emitted('edit')?.[0]).toEqual([mockUser])
  })
})
```

## 严格禁止事项

1. **直接修改Props**：禁止直接修改props，使用emit通知父组件
2. **v-if和v-show混用**：避免混用，根据场景选择
3. **全局变量**：避免使用全局变量，使用Pinia管理状态
4. **内联样式过多**：避免大量内联样式，使用Scoped CSS
5. **过度使用watch**：优先使用computed
6. **空函数**：禁止生成空函数或使用测试代码

## 最佳实践总结

### 关注点分离
- 组件：UI展示和用户交互
- Composables：可复用的逻辑
- Stores：全局状态管理
- API：数据请求

### 可维护性
- TypeScript类型安全
- 代码复用（组件、composables）
- 统一的代码规范
- 完善的注释文档

### 性能优化
- 代码分割和懒加载
- 虚拟滚动
- 防抖节流
- 合理使用缓存
