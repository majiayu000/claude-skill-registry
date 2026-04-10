---
name: frontend
description: "Frontend patterns: component design, state management, performance, accessibility. Use when building web frontends, components, or client-side apps."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 前端开发模式

本技能提供前端开发的最佳实践和模式，支持多框架按需加载。

## 快速参考

- **核心职责**: 提供前端开发最佳实践——组件设计、状态管理、性能优化、无障碍开发
- **框架支持**: Vue 3 / React 18 / Svelte / Angular 17+（根据 `package.json` 按需加载）
- **性能目标**: LCP < 2.5s, FID < 100ms, CLS < 0.1, TTI < 3.8s
- **设计原则**: 单一职责、Props 向下、Events 向上、组合优于继承

## 触发条件

- 创建或修改前端组件
- 设计 UI/UX 交互
- 实现状态管理
- 性能优化
- 无障碍开发

## 框架专属模式

根据项目 `package.json` 依赖加载对应文件：

| 技术栈  | 加载文件     | 框架              |
| ------- | ------------ | ----------------- |
| Vue     | `vue.md`     | Vue 3, Nuxt 3     |
| React   | `react.md`   | React 18, Next.js |
| Svelte  | `svelte.md`  | Svelte, SvelteKit |
| Angular | `angular.md` | Angular 17+       |

## 子文件索引

| 文件                                 | 内容                                  |
| ------------------------------------ | ------------------------------------- |
| [vue.md](./vue.md)                   | Vue 3 + Composition API 模式          |
| [react.md](./react.md)               | React 18 + Hooks 模式                 |
| [svelte.md](./svelte.md)             | Svelte/SvelteKit 模式                 |
| [angular.md](./angular.md)           | Angular 17+ 模式                      |
| [performance.md](./performance.md)   | Core Web Vitals 优化                  |
| [tailwind.md](./tailwind.md)         | Tailwind 最佳实践 + v4 迁移           |
| [design-guide.md](./design-guide.md) | 设计方法论与审查清单                  |
| [patterns.md](./patterns.md)         | 通用组件/状态管理/表单/动画/a11y 模式 |

## 性能指标

| 指标    | 目标    | 说明         |
| ------- | ------- | ------------ |
| **LCP** | < 2.5s  | 最大内容绘制 |
| **FID** | < 100ms | 首次输入延迟 |
| **CLS** | < 0.1   | 累积布局偏移 |
| **TTI** | < 3.8s  | 可交互时间   |

## 设计美学（避免 AI Slop）

> 详见 [design-guide.md](./design-guide.md) — AI 通用审美定义、设计思维方向矩阵、反模式清单与审查清单。

## 测试模式

> 详见 `rules/frontend/frontend-testing.md` 和 `rules/frontend/frontend-e2e.md`（按文件类型自动加载）。

---

> **记住**: 前端开发的核心是用户体验——性能、无障碍、交互细节缺一不可，独特的设计比通用模板更有价值。
