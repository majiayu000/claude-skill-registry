---
name: logging-system
description: 日志系统完整指南，包括应用日志、脚本日志、错误监控上报、请求日志等
---

# 日志系统

## 何时使用

当你需要：
- 记录应用日志
- 监控和上报错误
- 查看请求日志
- 调试问题
- 分析用户行为

## 项目日志架构

### 1. 脚本日志（@build-utils/logger）

用途：构建脚本、部署脚本的日志输出
位置：packages/@build-utils/logger/

使用：
  import { logger } from '@build-utils/logger'
  
  logger.info('构建开始')
  logger.warn('警告信息')
  logger.error('错误信息')
  logger.success('操作成功')

特点：
  - 带时间戳
  - 彩色输出
  - 支持子logger

### 2. 应用日志（shared-core/logger）

用途：前端应用的日志记录
位置：packages/shared-core/src/logger/

使用：
  import { logger } from '@btc/shared-core'
  
  logger.info('用户登录', { username: 'admin' })
  logger.warn('Token即将过期')
  logger.error('API调用失败', error)

日志级别：
  - debug：调试信息（开发环境）
  - info：一般信息
  - warn：警告
  - error：错误

### 3. 错误监控系统

用途：捕获、上报、分析前端错误
位置：packages/shared-core/src/utils/error-monitor/

功能：
  ✅ 自动捕获 JS 错误
  ✅ 捕获 Promise 未处理的 rejection
  ✅ 捕获 Vue 组件错误
  ✅ 存储到 localStorage
  ✅ 导出错误报告

使用：
  import { captureError, getErrorList } from '@btc/shared-core'
  
  // 手动上报错误
  captureError(new Error('自定义错误'), {
    type: 'business',
    context: { userId: 123 }
  })
  
  // 获取错误列表
  const errors = getErrorList()

### 4. 请求日志（request-logger）

用途：记录所有 HTTP 请求
位置：apps/{app}/src/utils/request-logger.ts

功能：
  ✅ 记录请求 URL、方法、参数
  ✅ 记录响应状态、耗时
  ✅ 自动过滤敏感信息
  ✅ 支持查询和导出

使用（自动集成）：
  HTTP 拦截器自动记录所有请求
  无需手动调用

查看日志：
  import { getRequestLogs } from '@/utils/request-logger'
  const logs = getRequestLogs()

## 错误监控使用

### 自动错误捕获

在应用入口（main.ts）中已自动启用：
  import { initErrorMonitor } from '@btc/shared-core'
  
  initErrorMonitor({
    appName: 'admin-app',
    version: '1.0.0',
    onError: (error) => {
      // 可选：上报到服务器
      console.error('Error captured:', error)
    }
  })

### 手动上报

业务错误：
  try {
    await saveData(data)
  } catch (error) {
    captureError(error, {
      type: 'business',
      context: { operation: 'save', data }
    })
    BtcMessage.error('保存失败')
  }

网络错误：
  fetch('/api/data')
    .catch(error => {
      captureError(error, { type: 'network' })
    })

组件错误：
  onErrorCaptured((error, instance, info) => {
    captureError(error, {
      type: 'component',
      context: { component: instance?.\$.type.name, info }
    })
  })

### 错误查看和导出

查看错误列表：
  访问：operations-app 的错误监控页面
  路径：/operations/error-monitor

导出错误：
  使用 BtcErrorMonitorExport 组件
  支持按日期、来源、类型筛选导出

## 日志级别配置

### 开发环境

  // vite.config.ts
  define: {
    __LOG_LEVEL__: JSON.stringify('debug')
  }

  所有级别日志都输出

### 生产环境

  define: {
    __LOG_LEVEL__: JSON.stringify('warn')
  }

  只输出 warn 和 error

## 日志最佳实践

### 1. 使用正确的日志级别

  logger.debug('变量值', { value })     // 调试信息
  logger.info('用户登录成功')           // 操作记录
  logger.warn('Token即将过期')          // 警告
  logger.error('保存失败', error)       // 错误

### 2. 包含上下文信息

  logger.info('订单创建', {
    orderId: order.id,
    userId: user.id,
    amount: order.amount
  })

### 3. 避免敏感信息

  ❌ logger.info('用户密码', { password: '123456' })
  ✅ logger.info('用户登录', { username: 'admin' })

### 4. 使用错误监控

  try {
    await riskyOperation()
  } catch (error) {
    captureError(error, { type: 'business', context: {...} })
    // 然后处理错误
  }

## 错误分类

项目支持的错误类型：
  - network：网络错误
  - api：API调用错误
  - business：业务逻辑错误
  - component：组件错误
  - runtime：运行时错误
  - resource：资源加载错误

## 查看日志的位置

### 浏览器控制台

开发环境所有日志都在控制台

### 错误监控页面

  访问：http://localhost:5109/operations/error-monitor
  
  功能：
  - 查看所有捕获的错误
  - 按来源、类型、时间筛选
  - 导出错误报告 Excel
  - 清除错误记录

### localStorage

错误存储：
  Key: btc_error
  格式：{ errors: { [date]: FormattedError[] } }

查看：
  浏览器 DevTools > Application > Local Storage

## 请求日志

### 查看请求日志

  import { getRequestLogs } from '@/utils/request-logger'
  
  const logs = getRequestLogs()
  console.table(logs)

### 日志内容

每条日志包含：
  - url: 请求URL
  - method: 请求方法
  - status: 响应状态
  - duration: 耗时（ms）
  - timestamp: 时间戳
  - params: 请求参数（脱敏）
  - response: 响应数据（部分）

### 日志导出

  import { exportRequestLogs } from '@/utils/request-logger'
  exportRequestLogs()  // 导出为 Excel

## 性能监控

### 关键指标日志

  logger.info('页面加载耗时', {
    loadTime: performance.now()
  })
  
  logger.info('API调用耗时', {
    api: '/api/data',
    duration: 350
  })

### 用户行为日志

  logger.info('用户操作', {
    action: 'click',
    target: 'save-button',
    module: 'warehouse'
  })

## 日志存储策略

### 前端

- Console：开发环境所有日志
- localStorage：错误日志（最近7天）
- IndexedDB：请求日志（可选，未启用）

### 后端（建议）

- 创建日志上报 API
- 批量上报错误日志
- 存储到数据库或日志服务

## 集成第三方日志服务（可选）

### Sentry

  pnpm add @sentry/vue
  
  import * as Sentry from '@sentry/vue'
  
  Sentry.init({
    app,
    dsn: 'your-sentry-dsn',
    integrations: [
      new Sentry.BrowserTracing(),
    ],
    tracesSampleRate: 1.0,
  })

### 其他选项

- 阿里云日志服务（SLS）
- 腾讯云日志服务（CLS）
- ELK Stack
- Grafana Loki

## 常见问题

Q: 如何查看某个应用的所有错误？
A: 访问 operations-app 错误监控页面，按来源筛选

Q: 日志太多影响性能？
A: 生产环境设置 LOG_LEVEL=warn，减少日志输出

Q: 如何上报到服务器？
A: 在 initErrorMonitor 的 onError 回调中发送API请求

Q: 请求日志存哪里？
A: 内存中（可配置存储到 localStorage）

## 相关工具

查看错误统计：
  访问 operations-app 错误监控页面

导出错误报告：
  使用 BtcErrorMonitorExport 组件

清理旧日志：
  localStorage.removeItem('btc_error')

## 下一步

需要排查错误？→ 使用 troubleshooting 技能
需要导出日志？→ 使用 excel-toolkit 技能
