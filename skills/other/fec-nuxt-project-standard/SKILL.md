---
name: fec-nuxt-project-standard
description: Use when creating or reviewing Nuxt 3 projects, file routes, pages, layouts, SSR/SSG/SPA behavior, Nuxt data fetching, route middleware, plugins, modules, server routes, or Nuxt-specific Vue 3 conventions. Use fec-vue3-project-standard for generic Vue component architecture; Chinese triggers include Nuxt, Nuxt 3.
---

# Nuxt 3 项目规范

适用于使用 Nuxt 3 + Vue 3 + TypeScript 的仓库。

## Purpose

规范 Nuxt 3 项目中 SSR/SSG 渲染模式、组合式 API、自动导入、数据获取、路由中间件和模块插件的工程实践，确保约定式开发和类型安全。

## Procedure

1. 先识别目标属于 Nuxt pages/layouts、渲染模式、数据获取、route middleware、plugin/module 还是 server route。
2. 明确 SSR / SSG / SPA 选择，避免服务端可执行代码依赖 `window` 或 `document`。
3. 数据获取优先使用 Nuxt 的 `useFetch` / `useAsyncData`，并检查水合一致性。
4. 路由鉴权、redirect 和权限问题与 `fec-route-protection` 对齐。
5. 通用 Vue 组件架构问题分流到 `fec-vue3-project-standard`。

## 项目结构

```
├── app.vue                    # 根组件
├── nuxt.config.ts              # Nuxt 配置
│
├── pages/                     # 基于文件的路由
│   ├── index.vue               # /
│   ├── login.vue               # /login
│   ├── dashboard/
│   │   ├── index.vue           # /dashboard
│   │   └── users/
│   │       ├── index.vue       # /dashboard/users
│   │       └── [id].vue       # /dashboard/users/:id
│   └── [...slug].vue          # 捕获所有
│
├── layouts/                   # 布局
│   ├── default.vue
│   └── auth.vue
│
├── components/                # 自动导入组件
│   ├── Button/
│   │   └── Button.vue
│   └── AppHeader.vue
│
├── composables/               # 组合式函数（自动导入）
│   ├── useAuth.ts
│   └── useFetch.ts
│
├── server/                    # 服务端 API
│   ├── api/                   # API 路由
│   │   └── users/
│   │       └── index.get.ts
│   ├── middleware/            # 服务端中间件
│   └── utils/                 # 服务端工具
│
├── plugins/                   # 插件
│   └── i18n.client.ts
│
├── middleware/                # 路由中间件
│   └── auth.ts
│
├── public/                    # 静态资源
├── assets/                    # 需构建的资源
└── types/                     # 类型定义
```

## 渲染模式

| 模式    | 配置            | 说明           |
| ------- | --------------- | -------------- |
| **SSR** | 默认            | `ssr: true`    |
| **SSG** | `nuxt generate` | 预渲染所有页面 |
| **SPA** | `ssr: false`    | 纯客户端渲染   |

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true, // 或 false
});
```

## 数据获取

- `useFetch` / `useAsyncData`：服务端 + 客户端，自动去重
- `$fetch`：直接请求，适合服务端或一次性调用
- `useLazyAsyncData`：不阻塞导航，适合非首屏
- 避免在 `setup` 顶层混用同步/异步逻辑导致水合不匹配

## 路由与布局

- `pages/` 下文件自动生成路由
- 动态路由：`[id].vue`、`[...slug].vue`
- 布局：`layout` 选项或 `layouts/default.vue` 默认
- 嵌套路由：`pages/parent/child.vue` 需配合 `NuxtPage`

## 中间件

- `middleware/` 下文件自动注册
- 页面级：`definePageMeta({ middleware: ['auth'] })`
- 全局：`nuxt.config.ts` 的 `router.middleware`
- 服务端中间件：`server/middleware/`

## 插件与模块

- 插件：`plugins/*.ts`，支持 `.client`、`.server` 后缀
- 模块：`modules/` 或 `node_modules`，在 `nuxt.config` 中 `modules: []`

## Constraints

- 服务端可访问的代码不要依赖 `window`、`document`
- 使用 `useState` 共享状态时注意 SSR 序列化
- 图片使用 `NuxtImg`，链接使用 `NuxtLink`
- 避免在 `setup` 顶层使用 `await` 导致阻塞，优先用 `useAsyncData` / `useFetch`

## Related Skills / Boundary

- `fec-vue3-project-standard` — 通用 Vue 3 组件、Composables 与 Pinia 边界。
- `fec-route-protection` — 登录态、权限路由、redirect 和 middleware 风险。
- `fec-data-fetching` — 客户端 server state 或缓存模式；Nuxt `useFetch`/`useAsyncData` 仍以本 skill 为准。

## Expected Output

- 页面按 `pages/` 约定式路由组织，动态路由正确配置
- 渲染模式（SSR/SSG/SPA）选择正确，`nuxt.config.ts` 配置清晰
- 数据获取使用 `useFetch` / `useAsyncData`，自动去重和水合
- Composables 和组件自动导入正确，服务端/客户端边界清晰
