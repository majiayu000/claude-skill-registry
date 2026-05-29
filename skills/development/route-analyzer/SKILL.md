---
name: route-analyzer
description: 路由分析器，分析应用路由结构、获取路由列表、智能推荐路由配置
---

# 路由分析器

## 功能

- 列出应用所有路由
- 分析路由层级结构
- 查找可用的路由名称
- 推荐新路由配置

## 使用方式

列出应用路由:
  cat apps/admin-app/src/modules/*/config.ts | grep -E 'path:|name:'

分析模块路由:
  cat apps/admin-app/src/modules/test/config.ts

## 路由配置规范

格式:
  path: '/{module}/{page-name}'
  name: '{module}-{page-name}'
  
示例:
  path: '/test/page-a'
  name: 'test-page-a'

## 主要应用路由前缀

- admin-app: /access, /org, /ops, /platform, /strategy, /test
- system-app: /warehouse, /procurement, /customs, /data
- logistics-app: /warehouse, /inventory, /procurement, /customs

## 路由配置位置

apps/{app-name}/src/modules/{module}/config.ts

配置示例:
  export default {
    views: [
      {
        path: '/test/new-page',
        name: 'test-new-page',
        component: () => import('./views/new-page/index.vue'),
        meta: { labelKey: 'test.newPage.title' }
      }
    ]
  }

## 检查路由冲突

  # 在应用目录搜索路由名称
  grep -r \"test-page-a\" apps/admin-app/src/modules/*/config.ts

## 自动路由发现

项目使用模块自动扫描，路由会自动注册。
只需在模块 config.ts 中配置即可。
