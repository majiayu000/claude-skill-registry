---
name: logging-best-practices
description: 日志最佳实践，强调宽事件（canonical log lines），便于调试与分析。
license: MIT
---

# Logging Best Practices Skill

## 目的

本技能提供应用内日志的实践指南，聚焦 **宽事件**（canonical log lines）：每个请求、每个服务只发出**一条**富含上下文的日志事件，便于调试与分析。

## 适用场景

在以下情况参考本指南：
- 编写或审查日志代码
- 使用 `console.log`、`logger.info` 等
- 为新服务设计日志策略
- 搭建日志基础设施

## 核心原则

### 1. 宽事件（关键）

每个请求、每个服务**只发一条**富含上下文的日志事件。不要在 handler 里到处打 log，而是在请求结束时汇总为一条结构化事件再输出。

```typescript
const wideEvent: Record = {
 method: 'POST',
 path: '/checkout',
 requestId: c.get('requestId'),
 timestamp: new Date().toISOString(),
};

try {
 const user = await getUser(c.get('userId'));
 wideEvent.user = { id: user.id, subscription: user.subscription };

 const cart = await getCart(user.id);
 wideEvent.cart = { total_cents: cart.total, item_count: cart.items.length };

 wideEvent.status_code = 200;
 wideEvent.outcome = 'success';
 return c.json({ success: true });
} catch (error) {
 wideEvent.status_code = 500;
 wideEvent.outcome = 'error';
 wideEvent.error = { message: error.message, type: error.name };
 throw error;
} finally {
 wideEvent.duration_ms = Date.now() - startTime;
 logger.info(wideEvent);
}
```

### 2. 高基数与高维度（关键）

包含高基数字段（如 user ID、request ID，百万级唯一值）和高维度（每条事件多字段）。便于按用户查询、回答未事先想到的问题。

### 3. 业务上下文（关键）

始终包含业务上下文：用户订阅档位、购物车金额、功能开关、账号龄等。目标是能知道「一名高级用户未能完成 2499 美元购买」，而不只是「结账失败」。

### 4. 环境特征（关键）

每条事件包含环境与部署信息：commit hash、服务版本、region、实例 ID。便于把问题与部署关联、定位区域性问题。

### 5. 单一 Logger（高）

启动时配置一个 logger 实例，全局复用。保证格式一致、自动带上环境上下文。

### 6. 中间件模式（高）

用中间件处理宽事件基础设施（计时、状态、环境、写出）。Handler 只负责补充业务上下文。

### 7. 结构与一致性（高）

- 统一使用 JSON 格式
- 跨服务保持字段命名一致
- 简化为两种级别：`info`、`error`
- 不记录非结构化字符串

## 反模式

1. **分散日志**：一个请求内多次 `console.log`
2. **多个 logger**：不同文件用不同实例
3. **缺环境上下文**：无 commit hash、部署信息
4. **缺业务上下文**：只有技术细节、无用户/业务数据
5. **非结构化字符串**：`console.log('something happened')` 而非结构化数据
6. **schema 不一致**：跨服务字段名不统一

## 指南摘要

### 宽事件

- 每个服务跳转发一条宽事件
- 包含所有相关上下文
- 用 request ID 串联事件
- 在 `finally` 中、请求结束时发出

### 上下文

- 支持高基数（user_id、request_id）
- 高维度（多字段）
- 始终含业务上下文
- 始终含环境特征（commit_hash、version、region）

### 结构

- 全代码库使用单一 logger
- 用中间件保证宽事件一致
- 使用 JSON 格式
- 保持 schema 一致
- 仅 info / error 两级
- 不记录非结构化字符串

### 常见坑

- 避免一个请求多行 log
- 为「未知的未知」设计
- 跨服务传递 request ID

## 参考

- [Logging Sucks](https://loggingsucks.com)
- [Observability Wide Events 101](https://boristane.com/blog/observability-wide-events-101/)
- [Stripe - Canonical Log Lines](https://stripe.com/blog/canonical-log-lines)
