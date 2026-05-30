---
name: backend
description: "Backend development patterns for services, error handling, logging, caching. Use when building backend services, APIs, or microservices."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 后端开发模式

本技能提供后端服务开发的最佳实践和模式，支持多语言按需加载。

## 触发条件

- 构建后端服务
- 设计服务架构
- 实现业务逻辑层
- 配置中间件
- 处理错误和日志
- 性能优化（数据库、缓存、并发）

## 语言专属模式

根据项目技术栈，加载对应的语言专属文件：

| 技术栈             | 加载文件        | 框架                     |
| ------------------ | --------------- | ------------------------ |
| Python             | `python.md`     | FastAPI, Django, Flask   |
| TypeScript/Node.js | `typescript.md` | Express, NestJS, Fastify |
| Java               | `java.md`       | Spring Boot, Quarkus     |
| Go                 | `go.md`         | Gin, Echo, Fiber         |
| C#                 | `csharp.md`     | ASP.NET Core             |
| Rust               | `rust.md`       | Axum, Actix-web, Rocket  |

**加载方式**: 检测项目中的 `pyproject.toml`/`package.json`/`pom.xml`/`go.mod`/`Cargo.toml` 等文件确定技术栈。

---

## 通用架构模式

### 分层架构

```
┌─────────────────────────────────────┐
│           Controller 层              │  处理 HTTP 请求/响应
├─────────────────────────────────────┤
│            Service 层                │  业务逻辑
├─────────────────────────────────────┤
│          Repository 层               │  数据访问
├─────────────────────────────────────┤
│             Model 层                 │  数据模型
└─────────────────────────────────────┘
```

### 通用目录结构

```
src/
├── controllers/          # 控制器（或 routes/handlers）
├── services/             # 业务逻辑
├── repositories/         # 数据访问（或 dal/）
├── models/               # 数据模型（或 entities/）
├── middlewares/          # 中间件
├── utils/                # 工具函数
├── config/               # 配置
└── types/                # 类型定义（如适用）
```

---

## 通用最佳实践

### 1. 错误处理原则

```
┌─────────────────────────────────────────────────────┐
│                    错误处理金字塔                     │
├─────────────────────────────────────────────────────┤
│  业务错误 (400-499)                                  │
│  ├─ ValidationError (400)   输入验证失败             │
│  ├─ UnauthorizedError (401) 未认证                  │
│  ├─ ForbiddenError (403)    无权限                  │
│  └─ NotFoundError (404)     资源不存在              │
├─────────────────────────────────────────────────────┤
│  系统错误 (500-599)                                  │
│  ├─ InternalError (500)     服务器内部错误           │
│  ├─ ServiceUnavailable (503) 服务不可用             │
│  └─ GatewayTimeout (504)    网关超时                │
└─────────────────────────────────────────────────────┘
```

**原则**:

- 自定义错误类继承基础错误
- 统一错误响应格式
- 区分可操作错误和程序错误
- 记录足够的上下文用于调试

### 2. 日志规范

**日志级别**:
| 级别 | 用途 | 示例 |
|------|------|------|
| ERROR | 需要立即关注的错误 | 数据库连接失败 |
| WARN | 潜在问题 | 重试成功、降级处理 |
| INFO | 重要业务事件 | 用户登录、订单创建 |
| DEBUG | 开发调试信息 | 变量值、执行路径 |

**结构化日志字段**:

```json
{
  "timestamp": "2025-01-22T10:00:00Z",
  "level": "info",
  "message": "用户登录成功",
  "requestId": "uuid",
  "userId": "123",
  "duration": 45
}
```

### 3. 缓存策略

| 策略          | 适用场景     | TTL 建议  |
| ------------- | ------------ | --------- |
| Cache-Aside   | 读多写少     | 5-60 分钟 |
| Write-Through | 强一致性要求 | 短 TTL    |
| Write-Behind  | 写多读少     | 根据业务  |

**缓存键命名**:

```
{service}:{entity}:{id}
{service}:{entity}:list:{hash}
```

### 4. API 设计原则

- **RESTful** 资源导向
- **版本控制** `/api/v1/...`
- **统一响应格式**
- **幂等性** PUT/DELETE 操作
- **分页** 大列表查询

### 5. 安全检查清单

- [ ] 输入验证（白名单优先）
- [ ] SQL/NoSQL 注入防护
- [ ] 认证令牌安全存储
- [ ] 敏感数据加密
- [ ] 速率限制
- [ ] CORS 配置

---

## 通用代码模式

### 统一响应格式

```
成功响应:
{
  "success": true,
  "data": { ... },
  "meta": { "total": 100, "page": 1 }
}

错误响应:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "邮箱格式不正确"
  }
}
```

### 健康检查端点

```
GET /health

{
  "status": "ok",
  "timestamp": "2025-01-22T10:00:00Z",
  "services": {
    "database": { "status": "ok" },
    "redis": { "status": "ok" }
  }
}
```

### 优雅关闭

```
1. 收到 SIGTERM 信号
2. 停止接受新请求
3. 等待进行中的请求完成（超时时间内）
4. 关闭数据库连接
5. 关闭其他资源
6. 退出进程
```

---

## 语言专属内容

详细的语言专属实现请参考：

- **Python**: [python.md](./python.md) - FastAPI/Django/Flask
- **TypeScript**: [typescript.md](./typescript.md) - Express/NestJS
- **Java**: [java.md](./java.md) - Spring Boot
- **Go**: [go.md](./go.md) - Gin/Echo
- **C#**: [csharp.md](./csharp.md) - ASP.NET Core
- **Rust**: [rust.md](./rust.md) - Axum/Actix-web/Rocket

## 专项优化

- **性能优化**: [performance.md](./performance.md) - 数据库、缓存、并发优化

## Python 进阶

- **设计模式**: [python-patterns.md](./python-patterns.md) - KISS、组合、策略模式
- **类型提示**: [python-types.md](./python-types.md) - Protocol、泛型、TypeGuard
- **可观测性**: [python-observability.md](./python-observability.md) - 日志、指标、追踪

---

## Maintenance

- Sources: 各语言官方文档, 12-Factor App
- Last updated: 2025-01-22
- Pattern: 通用清单 + 按需加载语言专属

> **记住**: 后端代码的质量标准是可维护性——类型安全、错误处理、日志追踪缺一不可。
