---
name: eps-analyzer
description: EPS服务分析器，分析EPS服务树、推荐服务路径、生成服务代码
---

# EPS 服务分析器

## 功能

- 分析 EPS 服务树结构
- 查找可用的 EPS 服务
- 推荐服务路径
- 生成服务调用代码

## EPS 文件位置

系统 EPS:
  apps/system-app/src/build/eps/eps.json
  apps/system-app/src/build/eps/eps.d.ts

其他应用会从 system-app 复制 EPS:
  apps/{app}/src/build/eps/

## 查看 EPS 结构

  cat apps/admin-app/src/build/eps/eps.json | grep -E '\"(query|save|update|delete)\"'

## EPS 路径规范

格式: eps.{module}.{entity}.{method}

示例:
  - eps.warehouse.location.query
  - eps.inventory.result.export
  - eps.test.pageA.save

## 使用 EPS 服务

方式1 - getEpsService（推荐）:
  import { getEpsService } from '@btc/shared-core'
  const epsNode = getEpsService('eps.test.pageA')
  const data = await epsNode?.query({ page: 1 })

方式2 - 直接导入:
  import { eps } from '@/build/eps/eps'
  const data = await eps.test?.pageA?.query({ page: 1 })

## CRUD 方法

标准方法（EPS 自动生成）:
  - query: 查询列表
  - save: 新增
  - update: 更新
  - delete: 删除
  - get: 获取单条

自定义方法（后端定义）:
  - export: 导出
  - import: 导入
  - batchDelete: 批量删除
  - approve: 审批

## 生成服务代码

  export const use{Page}Service = () => {
    const epsNode = getEpsService('eps.test.pageA')
    
    return {
      query: epsNode?.query,
      save: epsNode?.save,
      update: epsNode?.update,
      delete: epsNode?.delete,
    }
  }

## 检查 EPS 是否存在

  cat apps/admin-app/src/build/eps/eps.json | grep \"eps.test.pageA\"

## 服务测试

  # 在浏览器控制台
  const eps = await import('@/build/eps/eps')
  console.log(eps.eps.test.pageA)
