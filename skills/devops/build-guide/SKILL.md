---
name: build-guide  
description: BTC ShopFlow 构建指南，包括4种构建模式、单应用/全量构建、预览构建等
---

# 构建指南

## 何时使用

当你需要：构建应用、了解构建模式、预览构建结果、排查构建错误

## 4种构建模式

模式1 - build（基础构建）:
  用途: 本地开发、CI测试、快速构建
  命令: pnpm build:all / pnpm build:app --app=admin-app
  产物: apps/{app}/dist/
  特点: 快速，无CDN

模式2 - build-cdn（CDN构建）:
  用途: CDN部署，静态资源加速
  命令: pnpm build-cdn:all / pnpm build-cdn:system
  产物: apps/{app}/dist-cdn/
  特点: 资源上传OSS，CDN加速
  需要: 配置OSS环境变量

模式3 - build-dist（集中构建）:
  用途: 服务器部署
  命令: pnpm build-dist:all / pnpm build-dist:system  
  产物: dist/{app}/ (根目录)
  特点: 产物集中，方便部署

模式4 - build-dist-cdn（完整构建）:
  用途: 生产环境（服务器+CDN）
  命令: pnpm build-dist-cdn:all / pnpm build-dist-cdn:admin
  产物: dist-cdn/{app}/
  特点: 生产最佳，CDN加速

## 应用构建命令快速参考

### 核心应用
- **main-app** - 主应用
  ```bash
  pnpm build:app --app=main-app
  pnpm build-cdn:main
  pnpm build-dist:main
  pnpm build-dist-cdn:main
  ```

- **layout-app** - 布局应用
  ```bash
  pnpm build:app --app=layout-app
  pnpm build-cdn:layout
  pnpm build-dist:layout
  pnpm build-dist-cdn:layout
  ```

### 业务应用
- **system-app** - 系统应用
  ```bash
  pnpm build:app --app=system-app
  pnpm build-cdn:system
  pnpm build-dist:system
  pnpm build-dist-cdn:system
  ```

- **admin-app** - 管理应用
  ```bash
  pnpm build:app --app=admin-app
  pnpm build-cdn:admin
  pnpm build-dist:admin
  pnpm build-dist-cdn:admin
  ```

- **logistics-app** - 物流应用
  ```bash
  pnpm build:app --app=logistics-app
  pnpm build-cdn:logistics
  pnpm build-dist:logistics
  pnpm build-dist-cdn:logistics
  ```

- **quality-app** - 品质应用
  ```bash
  pnpm build:app --app=quality-app
  pnpm build-cdn:quality
  pnpm build-dist:quality
  pnpm build-dist-cdn:quality
  ```

- **production-app** - 生产应用
  ```bash
  pnpm build:app --app=production-app
  pnpm build-cdn:production
  pnpm build-dist:production
  pnpm build-dist-cdn:production
  ```

- **engineering-app** - 工程应用
  ```bash
  pnpm build:app --app=engineering-app
  pnpm build-cdn:engineering
  pnpm build-dist:engineering
  pnpm build-dist-cdn:engineering
  ```

- **finance-app** - 财务应用
  ```bash
  pnpm build:app --app=finance-app
  pnpm build-cdn:finance
  pnpm build-dist:finance
  pnpm build-dist-cdn:finance
  ```

- **operations-app** - 运维应用
  ```bash
  pnpm build:app --app=operations-app
  pnpm build-cdn:operations
  pnpm build-dist:operations
  pnpm build-dist-cdn:operations
  ```

- **personnel-app** - 人事应用
  ```bash
  pnpm build:app --app=personnel-app
  pnpm build-dist:personnel
  pnpm build-dist-cdn:personnel
  ```

- **dashboard-app** - 仪表盘应用
  ```bash
  pnpm build:app --app=dashboard-app
  pnpm build-dist:dashboard
  pnpm build-dist-cdn:dashboard
  ```

### 工具应用
- **docs-app** - 文档站点
  ```bash
  pnpm build:app --app=docs-app
  pnpm build-cdn:docs
  pnpm build-dist:docs
  pnpm build-dist-cdn:docs
  ```

- **home-app** - 公司首页
  ```bash
  pnpm build:app --app=home-app
  pnpm build-dist:home
  pnpm build-dist-cdn:home
  ```

- **mobile-app** - 移动端应用
  ```bash
  pnpm build:app --app=mobile-app
  # 注意: mobile-app 默认不包含在 build:all 中
  ```

## 预览构建

本地预览:
  pnpm preview:all
  pnpm preview:app --app=admin-app

构建并预览:
  pnpm build-preview:all
  pnpm build-preview:layout

## 构建前检查

自动检查（prebuild）:
  pnpm check:circular  # 循环依赖
  pnpm run prebuild:all  # 清理缓存

手动检查:
  pnpm type-check:all
  pnpm lint:all
  pnpm check:i18n

## 构建优化

并发构建: Turbo 自动并发（concurrency=20）
增量构建: Turbo 自动检测变更
清理缓存: pnpm clean:vite / pnpm clean

## 常见构建错误

Cannot find module:
  → 运行 pnpm build:share

Type errors:
  → pnpm type-check:app --app=admin-app
  → pnpm ts-error-reports

Out of memory:
  → export NODE_OPTIONS=\"--max-old-space-size=8192\"
  → 重新构建

Circular dependency:
  → pnpm check:circular
  → 根据报告修复

Build hangs:
  → pnpm clean:vite
  → rm -rf node_modules pnpm-lock.yaml && pnpm install

## 构建脚本位置

scripts/commands/build/:
  - cdn-build.mjs
  - dist-build.mjs  
  - dist-cdn-build.mjs
  - preview-build.mjs

统一入口:
  node scripts/bin/build.js cdn system-app
