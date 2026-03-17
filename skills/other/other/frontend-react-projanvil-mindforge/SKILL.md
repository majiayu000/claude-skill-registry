---
name: frontend-react
description: 专业的 React 开发技能，涵盖 Next.js、React Server Components、Tailwind CSS 和 React 生态系统。使用此技能构建现代 React 应用程序、实现 Next.js 功能、使用 shadcn/ui 创建 UI 组件，或处理复杂状态管理。
---

# React 开发技能

现代 React 开发的综合技能，专注于 Next.js、TypeScript、Tailwind CSS 和广泛的 React 生态系统。

## 技术栈

### 核心框架：React + Next.js

#### React 基础
- **基于组件**：声明式 UI 构建块
- **Hooks**：函数式状态和副作用管理 (`useState`, `useEffect`, `useContext`)
- **虚拟 DOM**：高效的协调和渲染
- **React Server Components (RSC)**：静态内容的服务器端渲染，零客户端包大小

#### Next.js 特性 (App Router)
- **App Router**：`app/` 目录下基于文件系统的路由
- **Server Actions**：直接从客户端组件进行服务器端数据变更
- **流式 SSR**：使用 Suspense 进行渐进式渲染
- **Metadata API**：SEO 和社交分享优化
- **Route Handlers**：`route.ts` 文件中的 API 端点 (GET, POST 等)
- **Middleware**：请求拦截和处理

### UI 框架：Tailwind CSS + shadcn/ui

#### Tailwind CSS
- 实用优先 CSS 框架
- 带有前缀的响应式设计 (`md:`, `lg:`)
- 通过 `tailwind.config.ts` 进行自定义配置
- 深色模式支持

#### shadcn/ui
- 基于 Radix UI 和 Tailwind CSS 构建的可重用组件
- 可访问且可定制
- "拥有你的代码" 理念 (将组件代码复制到你的项目中)
- **关键组件**：Button, Dialog, Form, Dropdown, Card, Sheet

### 状态管理
- **本地状态**：`useState`, `useReducer`
- **全局状态**：React Context, Zustand (用于轻量级全局状态)
- **服务器状态**：TanStack Query (React Query) 用于异步数据获取和缓存

## 项目架构

### 推荐目录结构 (Next.js App Router)
```
src/
├── app/
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   ├── globals.css        # 全局样式
│   ├── (auth)/            # 路由组 (不影响 URL 路径)
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   └── api/               # API 路由
├── components/
│   ├── ui/                # shadcn/ui 组件
│   │   ├── button.tsx
│   │   └── ...
│   ├── Navbar.tsx
│   └── Footer.tsx
├── lib/
│   ├── utils.ts           # 工具函数 (cn 等)
│   └── db.ts              # 数据库连接
└── hooks/                 # 自定义 React hooks
    └── use-toast.ts
```

## 最佳实践

### 组件设计
- **默认服务端**：对不需要交互的所有内容使用 Server Components。
- **客户端边界**：仅在使用 hooks 或事件监听器时添加 `'use client'` 指令。
- **组合**：使用 `children` 属性以避免属性钻取 (prop drilling)。
- **微组件**：将复杂的 UI 分解为更小的、单一职责的组件。

### 性能
- **图片优化**：使用 `next/image` 进行自动优化。
- **字体优化**：使用 `next/font` 以防止布局偏移。
- **懒加载**：对重型组件使用 `next/dynamic` 或 `React.lazy`。
- **代码分割**：Next.js 中自动进行，但要注意大型依赖项。

### 可访问性 (a11y)
- 使用语义化 HTML 标签 (`<main>`, `<article>`, `<nav>`)。
- 确保所有交互元素都支持键盘操作。
- 当语义化 HTML 不够时使用有效的 ARIA 属性。
- Radix UI 原语 (用于 shadcn/ui) 自动处理许多无障碍问题。

## 常见代码模式

### Next.js 页面 (Server Component)
```tsx
import { db } from "@/lib/db"

export default async function DashboardPage() {
  const data = await db.user.findMany()

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">仪表板</h1>
      <ul>
        {data.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </main>
  )
}
```

### 带状态的客户端组件
```tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div className="flex gap-4 items-center">
      <span>计数: {count}</span>
      <Button onClick={() => setCount(c => c + 1)}>增加</Button>
    </div>
  )
}
```
