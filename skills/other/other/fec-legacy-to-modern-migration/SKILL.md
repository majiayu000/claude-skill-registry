---
name: fec-legacy-to-modern-migration
description: Use when planning or implementing an intentional migration from JavaScript, jQuery, HTML/CSS, server-rendered templates, or MPA legacy frontend code to React + TypeScript or Vue 3 + TypeScript while preserving behavior. Do not use for routine legacy bug fixes that stay in the old stack; Chinese triggers include 遗留项目, 技术栈升级, jQuery 迁移.
---

# 传统前端到现代框架迁移

适用于将 JavaScript + jQuery + HTML/CSS 多页面应用（MPA）或服务端模板渲染项目，迁移至 React + TypeScript 或 Vue 3 + TypeScript 单页面应用（SPA）的场景。

## Purpose

指导将 jQuery/MPA 传统前端项目渐进迁移至 React + TypeScript 或 Vue 3 + TypeScript，提供迁移策略、概念映射、分阶段步骤和实施约束，确保功能等价和风险可控。

## 迁移策略选择

| 策略                        | 适用情况                             | 优点                         | 风险                         |
| --------------------------- | ------------------------------------ | ---------------------------- | ---------------------------- |
| **渐进式（Strangler Fig）** | 大型项目、需持续交付、团队熟悉度不足 | 风险可控、可分批上线、可回滚 | 新旧并存期长、需维护两套代码 |
| **一次性重写**              | 中小型项目、业务稳定、有充足时间窗口 | 目标架构清晰、无历史包袱     | 周期长、上线压力大、回滚困难 |

**推荐**：优先考虑渐进式，除非项目规模小且业务简单。

## 概念映射

### jQuery → React

| 遗留模式                                   | React 对应                             |
| ------------------------------------------ | -------------------------------------- |
| `$(selector).html(content)`                | 声明式 JSX + state 驱动渲染            |
| `$(document).on('click', '.btn', handler)` | `onClick` + 事件委托由 React 处理      |
| `$.ajax()` / `$.get()`                     | `fetch` / `axios` + React Query 或 SWR |
| 全局变量 / 命名空间存储状态                | `useState` / `useContext` / Zustand    |
| `$(el).show()` / `$(el).hide()`            | 条件渲染 `{visible && <Component />}`  |
| 手动 DOM 操作 `append` / `remove`          | 数据驱动，通过 setState 触发重渲染     |
| 模板字符串拼接 HTML                        | JSX 组件 + props                       |
| 多页面 + 服务端路由                        | React Router 客户端路由                |

### jQuery → Vue 3

| 遗留模式                                   | Vue 3 对应                                         |
| ------------------------------------------ | -------------------------------------------------- |
| `$(selector).html(content)`                | 模板 + `ref` / `reactive` 驱动渲染                 |
| `$(document).on('click', '.btn', handler)` | `@click` + 事件修饰符                              |
| `$.ajax()` / `$.get()`                     | `fetch` / `axios` + VueUse `useFetch` 或 Vue Query |
| 全局变量 / 命名空间存储状态                | `ref` / `reactive` / Pinia                         |
| `$(el).show()` / `$(el).hide()`            | `v-show` / `v-if`                                  |
| 手动 DOM 操作                              | 数据驱动，通过响应式更新视图                       |
| 模板字符串拼接 HTML                        | 单文件组件 `<template>` + props                    |
| 多页面 + 服务端路由                        | Vue Router 客户端路由                              |

### 通用映射

| 遗留概念                          | 现代对应                                   |
| --------------------------------- | ------------------------------------------ |
| 页面级 JS 入口（每页一个 script） | 路由 + 懒加载页面组件                      |
| 公共 JS 模块（utils、ajax 封装）  | `services/`、`utils/`、类型化 API 层       |
| 内联样式 / 页面级 CSS             | CSS Modules / Tailwind / styled-components |
| 服务端模板变量                    | 通过 API 获取 + 前端状态管理               |
| 表单提交 + 整页刷新               | 表单库 + 客户端校验 + API 调用             |

## 迁移前分析

在动手迁移前，必须完成以下分析并输出**迁移分析报告**：

1. **存量盘点**
   - 页面数量、功能模块数量
   - 依赖的 jQuery 插件及替代方案（如 DataTables → TanStack Table）
   - 现有 API 调用方式、是否有统一封装
   - 是否有服务端模板（JSP/Thymeleaf/EJS 等）需改为纯前端渲染

2. **依赖关系**
   - 页面间共享的 JS/CSS 模块
   - 跨页面复用的业务逻辑
   - 与后端的接口契约（是否需调整）

3. **迁移优先级**
   - 按业务价值、复杂度、耦合度排序
   - 优先迁移独立模块、低耦合页面
   - 识别可复用的工具函数、常量、类型定义

## 分阶段迁移流程

### 阶段 0：准备

- 搭建新项目脚手架（Vite + React/Vue + TypeScript）
- 配置 ESLint、Prettier、测试框架
- 建立 `services/request.ts` 统一请求层，与现有 API 兼容
- 将遗留项目中的 `utils`、`constants` 逐步迁移并补充类型

### 阶段 1：基础层

- 迁移并类型化 API 调用（`$.ajax` → `axios`/`fetch`）
- 迁移工具函数（日期、格式化、校验等）
- 迁移常量、枚举、类型定义
- 建立路由骨架，占位未迁移页面（重定向或 iframe 嵌入旧页面）

### 阶段 2：按模块/页面迁移

- 每次迁移一个完整功能或页面
- 从简单到复杂：静态页 → 列表页 → 表单页 → 复杂交互页
- 迁移时提取可复用组件，遵循 `fec-react-project-standard` 或 `fec-vue3-project-standard` 的目录结构
- 每完成一个模块，补充单元测试和 E2E 关键路径

### 阶段 3：收尾

- 移除旧代码入口，全面切换至 SPA
- 配置 404、错误边界、全局错误处理
- 性能优化（懒加载、代码分割、缓存策略）
- 文档更新、部署流程调整

## 重构实施要求

迁移时需遵循以下实施约束，确保视觉与交互一致、代码更简洁易维护。

### 图片与图标

- 直接使用原项目的图片资源路径，不重新托管或替换
- 可使用 SVG 图片（`<img src="*.svg" />` 或 CSS `background-image`），**禁止使用内联 SVG**（`<svg>...</svg>` 直接写在组件中）
- **若原项目使用了 iconfont 或 IcoMoon 图标，重构时继续使用**，保持图标体系一致；不替换为其他图标方案（如独立 SVG、其他图标库）
- 图标优先使用原项目已有的图标文件（iconfont / IcoMoon / 已有 SVG），必要时可引入 SVG 文件作为独立资源

### 国际化（i18n）

- 新栈代码（React / Vue 等）中的用户可见文案须走项目 i18n，不在新代码里硬编码中/英文案
- 遗留 HTML/JS 中**不要新增**用户可见硬编码文案，除非纯静态且仓库尚无可用 i18n 接入点；改动文案前先查 locales 是否已有条目，并同步主要语言文件
- key 按页面/模块/语义组织，复用既有 key；仅当旧 key 为对外契约时才做映射过渡，详见项目规则中的 **国际化 (i18n)**（`templates/rules/i18n.md` 内「遗留代码与迁移场景」）

### 样式

- 布局样式对齐原项目视觉效果，但**只参考原项目效果，不照搬其 CSS**
- 优先使用 **flex 弹性布局**，避免 `float`、复杂 `position`、冗余嵌套
- 避免不合理写法：如 `!important` 滥用、过深选择器、重复定义
- **组件中禁止使用内联样式**（`style={{ ... }}` / `style="..."`），样式统一放在 CSS Modules、Tailwind 类或样式文件中，便于维护

### 目标

- **视觉和交互**：与原项目一致，用户无感知差异
- **代码质量**：更简洁、易维护，符合目标框架规范
- **业务功能**：与原项目保持一致，**不得缺失功能**；迁移前后行为等价

## 迁移检查清单

每个迁移单元完成后，确认：

- [ ] 业务逻辑与旧实现一致，无功能遗漏，功能完整等价
- [ ] 类型定义完整，无 `any` 滥用
- [ ] API 调用使用统一 request 层，错误处理完整
- [ ] 表单校验、loading、空状态、错误状态已实现
- [ ] 可访问性：表单有 label、交互可键盘操作
- [ ] 无 XSS 风险（用户输入已转义或使用安全 API）
- [ ] 关键路径有测试覆盖
- [ ] 符合目标框架的项目规范（参考 `fec-react-project-standard` / `fec-vue3-project-standard`）
- [ ] 图片使用原项目资源，无内联 SVG；若原项目用 iconfont/IcoMoon 则继续使用
- [ ] 样式参考原项目效果但不照搬 CSS，优先 flex 布局，无内联样式
- [ ] 视觉与交互与原项目一致，代码更简洁易维护
- [ ] 新代码路径文案已 i18n；遗留层未扩大硬编码；locales 检索与多语言同步已完成（参见 i18n 规则迁移补充清单）

## Constraints

- 迁移前必须先输出迁移分析报告，明确策略、优先级和风险
- 不要在一次迁移中同时改架构、改 UI、改接口
- 优先保证功能等价，再考虑优化和现代化
- 迁移过程中保持旧系统可运行，避免大爆炸式上线
- 遇到 jQuery 插件无现成替代时，可暂时用 iframe 或微前端方式嵌入，待后续替换
- **图片与图标**：使用原项目图片资源，可用 SVG 文件，禁止内联 SVG；若原项目用 iconfont/IcoMoon 则继续使用
- **样式**：参考原项目效果不照搬 CSS，优先 flex 布局，组件禁止内联样式
- **目标**：视觉与交互一致、代码更简洁易维护，业务功能不得缺失

## Detailed References

Load [references/migration-report-template.md](references/migration-report-template.md) when writing a migration analysis or migration plan report.

## Expected Output

- 迁移分析报告保存为 `reports/migration-plan-YYYY-MM-DD-HHmmss.md`，包含策略选择、存量盘点、依赖关系、分阶段步骤、风险与回滚方案
- 迁移后的业务功能与原项目完全等价，无功能缺失
- 视觉与交互与原项目一致，用户无感知差异
- 类型定义完整，无 `any` 滥用，API 调用统一且类型安全
- 图片使用原项目资源，样式使用 flex 布局，无内联样式
- 新代码文案已 i18n，关键路径有测试覆盖

## 相关技能

- `fec-legacy-web-standard` — 理解源项目（jQuery、MPA）的代码模式
- `fec-react-project-standard` — 迁移至 React 时的目标结构规范
- `fec-vue3-project-standard` — 迁移至 Vue 3 时的目标结构规范
- `fec-frontend-architect` — 大型迁移的架构设计与风险评估
