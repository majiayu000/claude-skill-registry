---
name: monorepo-quick-start
description: BTC ShopFlow Monorepo 快速上手指南，项目结构、应用列表、包依赖、快速定位文件和模块
---

# Monorepo 快速上手

## 何时使用此技能

当你需要：
- 了解项目整体结构
- 查找特定应用或包的位置
- 理解应用和包的依赖关系
- 快速定位功能模块

## 项目结构概览

BTC ShopFlow 是一个基于 pnpm + Turbo 的 Monorepo 项目，采用微前端架构。

项目根目录: btc-shopflow-monorepo/
├── apps/              # 15 个应用
│   ├── main-app       # 主应用（核心）
│   ├── layout-app     # 布局应用（核心）
│   ├── system-app     # 系统配置
│   ├── admin-app      # 管理后台
│   ├── logistics-app  # 物流管理
│   ├── quality-app    # 品质管理
│   ├── production-app # 生产管理
│   ├── engineering-app # 工程管理
│   ├── finance-app    # 财务管理
│   ├── operations-app # 运维管理
│   ├── personnel-app  # 人事管理
│   ├── dashboard-app  # 仪表盘
│   ├── mobile-app     # 移动端
│   ├── docs-app       # 文档站点
│   └── home-app       # 公司首页
├── packages/          # 7 个共享包
│   ├── shared-core         # 核心工具和类型
│   ├── shared-components   # BTC 组件库
│   ├── shared-router       # 路由工具
│   ├── design-tokens       # 设计令牌
│   ├── vite-plugin         # Vite 插件
│   ├── @build-utils/logger # 日志工具
│   └── subapp-manifests    # 子应用清单
└── scripts/           # 构建和部署脚本

## 应用分类

核心应用（必需）:
- main-app: 主应用，负责微前端容器、路由、认证
- layout-app: 布局应用，提供统一布局模板

业务应用（按需加载）:
- system-app: 系统配置、基础数据、仓库管理
- admin-app: 权限管理、菜单管理、策略引擎
- logistics-app: 物流、仓库、盘点
- quality-app, production-app, engineering-app, finance-app
- operations-app, personnel-app, dashboard-app

工具应用:
- docs-app: VitePress 文档站点
- home-app: 公司首页
- mobile-app: 移动端盘点

## 常用命令速查

查看应用配置:
  cat apps.config.json

列出所有应用:
  node scripts/commands/tools/turbo.js ls

在特定应用中运行命令:
  pnpm --filter=@btc/admin-app <command>
  pnpm build:app --app=admin-app

查看应用依赖:
  cat apps/admin-app/package.json
  pnpm --filter=@btc/admin-app list --depth=1

## 快速启动和构建

### 启动应用
启动单个应用:
  ```bash
  pnpm dev:app --app=admin-app
  pnpm dev:app --app=system-app
  pnpm dev:app --app=logistics-app
  ```

启动多个应用（推荐）:
  ```bash
  pnpm dev:all              # 后台运行
  pnpm dev:all:window       # 新窗口（推荐）
  ```

**详细说明**: 使用 `dev-workflow` 技能查看完整的启动指南和所有应用端口配置

### 构建应用
构建单个应用:
  ```bash
  pnpm build:app --app=admin-app
  pnpm build:app --app=system-app
  ```

构建所有应用:
  ```bash
  pnpm build:all            # 基础构建
  pnpm build-cdn:all        # CDN构建
  pnpm build-dist:all       # 集中构建
  pnpm build-dist-cdn:all   # 完整构建（生产）
  ```

**详细说明**: 使用 `build-guide` 技能查看完整的构建指南和4种构建模式

## 快速定位

应用入口: apps/{app-name}/src/main.ts
应用路由: apps/{app-name}/src/router/
应用模块: apps/{app-name}/src/modules/{module-name}/
私有组件: apps/{app-name}/src/components/
共享组件: packages/shared-components/src/components/
国际化: apps/{app-name}/src/locales/{lang}.json

## 应用端口和快速访问

| 应用 | 端口 | 启动命令 | 访问地址 |
|------|------|----------|----------|
| main-app | 5100 | `pnpm dev:app --app=main-app` | http://localhost:5100 |
| layout-app | 5101 | `pnpm dev:app --app=layout-app` | http://localhost:5101 |
| system-app | 5102 | `pnpm dev:app --app=system-app` | http://localhost:5100/system |
| admin-app | 5103 | `pnpm dev:app --app=admin-app` | http://localhost:5100/admin |
| logistics-app | 5104 | `pnpm dev:app --app=logistics-app` | http://localhost:5100/logistics |
| quality-app | 5105 | `pnpm dev:app --app=quality-app` | http://localhost:5100/quality |
| production-app | 5106 | `pnpm dev:app --app=production-app` | http://localhost:5100/production |
| engineering-app | 5107 | `pnpm dev:app --app=engineering-app` | http://localhost:5100/engineering |
| finance-app | 5108 | `pnpm dev:app --app=finance-app` | http://localhost:5100/finance |
| operations-app | 5109 | `pnpm dev:app --app=operations-app` | http://localhost:5100/operations |
| dashboard-app | 5110 | `pnpm dev:app --app=dashboard-app` | http://localhost:5100/dashboard |
| personnel-app | 5111 | `pnpm dev:app --app=personnel-app` | http://localhost:5100/personnel |
| mobile-app | 5112 | `pnpm dev:app --app=mobile-app` | http://localhost:5112 |
| docs-app | 5113 | `pnpm dev:app --app=docs-app` | http://localhost:5113 |
| home-app | 5114 | `pnpm dev:app --app=home-app` | http://localhost:5114 |

**提示**: 
- 主应用入口: http://localhost:5100（通过主应用访问所有子应用）
- 子应用也可直接通过端口访问: http://localhost:{port}
- 使用 `dev-workflow` 技能查看详细的启动指南

## 技术栈

包管理器: pnpm 8.15.0
构建工具: Vite + Turbo
框架: Vue 3 + TypeScript
微前端: qiankun
UI 库: Element Plus + UnoCSS
