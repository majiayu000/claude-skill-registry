---
name: file-navigator
description: 文件导航器，智能创建文件路径、推荐文件结构、检查文件冲突
---

# 文件导航器

## 功能

- 智能推荐文件路径
- 创建标准目录结构
- 检查文件是否存在
- 推荐文件命名

## 页面文件结构

标准结构:
  apps/{app}/src/modules/{module}/views/{page-name}/
  ├── index.vue              # 主页面
  ├── composables/           # 组合式函数
  │   ├── use{Page}Service.ts
  │   ├── use{Page}Print.ts
  │   └── use{Page}Data.ts
  └── components/            # 页面私有组件
      └── {Page}PrintTemplate.vue

## 创建文件命令

创建目录:
  New-Item -ItemType Directory -Path \"apps/admin-app/src/modules/test/views/page-a\" -Force

创建页面:
  New-Item -ItemType File -Path \"apps/admin-app/src/modules/test/views/page-a/index.vue\" -Force

创建 composable:
  New-Item -ItemType File -Path \"apps/admin-app/src/modules/test/views/page-a/composables/usePageAService.ts\" -Force

## 文件命名规范

页面: kebab-case（如 page-a, user-list）
组件: PascalCase.vue（如 UserCard.vue）
Composable: use{Name}.ts（如 useUserService.ts）
工具: kebab-case.ts（如 format-date.ts）

## 检查文件存在

  Test-Path \"apps/admin-app/src/modules/test/views/page-a/index.vue\"

## 推荐路径

新页面:
  apps/{app}/src/modules/{module}/views/{page-name}/index.vue

新组件:
  apps/{app}/src/components/{ComponentName}.vue
  packages/shared-components/src/components/{category}/{component-name}/

新工具:
  apps/{app}/src/utils/{util-name}.ts
  packages/shared-core/src/utils/{util-name}.ts

新服务:
  apps/{app}/src/services/{service-name}.ts

## 快速创建模板

创建完整页面结构:
  \ = \"apps/admin-app/src/modules/test/views/page-a\"
  New-Item -ItemType Directory -Path \"\/composables\" -Force
  New-Item -ItemType Directory -Path \"\/components\" -Force
  New-Item -ItemType File -Path \"\/index.vue\" -Force
  New-Item -ItemType File -Path \"\/composables/usePageAService.ts\" -Force
