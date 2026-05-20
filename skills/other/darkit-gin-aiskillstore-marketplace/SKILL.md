---
name: darkit-gin
description: 基于 gin-gonic/gin 的企业级 Web 框架增强版，提供开箱即用的 JWT 认证、SSE 实时通信、缓存管理、OpenAPI 文档生成等企业级功能。涵盖选项式路由配置、统一响应格式、中间件管理、安全加固、性能优化等完整开发能力。
tags:
  - go
  - gin
  - web
  - http
  - rest
  - api
  - jwt
  - sse
  - openapi
  - cache
  - middleware
  - darkit/gin
---

# Darkit Gin Framework 技能

## 适用场景

- 构建企业级 RESTful API 服务
- 需要快速集成 JWT 认证和授权系统
- 实现服务器发送事件（SSE）实时通信
- 自动生成 OpenAPI 3.0 规范和 Swagger UI
- 需要内置缓存系统提升性能
- 要求统一的 API 响应格式
- 从 gin-gonic/gin 迁移并增强功能

## 操作流程

### 1. 快速开始

```go
// 使用选项式 API 创建路由器（推荐）
router := gin.NewRouter(
    gin.WithGinMode("debug"),
    gin.WithJWT("your-secret-key"),
    gin.WithCache(&cache.Config{
        TTL: 30 * time.Minute,
    }),
    gin.WithCORS("http://localhost:3000"),
    gin.WithRateLimit(100),  // 100 次/分钟
    gin.WithRequestID(),
)

// 自动添加健康检查和监控端点
router.Health()   // GET /health
router.Metrics()  // GET /metrics

// 启动服务器
router.Run(":8080")
```

### 2. 定义路由

```go
// 基础路由
router.GET("/ping", func(c *gin.Context) {
    c.Success("pong")  // 统一成功响应
})

// CRUD 资源路由（编译期类型安全）
type UserResource struct{}
func (u *UserResource) Index(c *gin.Context)  { /* 列表 */ }
func (u *UserResource) Show(c *gin.Context)   { /* 详情 */ }
func (u *UserResource) Create(c *gin.Context) { /* 创建 */ }
func (u *UserResource) Update(c *gin.Context) { /* 更新 */ }
func (u *UserResource) Delete(c *gin.Context) { /* 删除 */ }

router.CRUD("users", &UserResource{})

// API 版本管理
v1 := router.API("v1")  // /api/v1
v2 := router.API("v2")  // /api/v2
```

### 3. 便捷响应方法

```go
// 成功响应
c.Success(data)               // 200
c.Created(newUser)            // 201
c.Accepted("任务已提交")       // 202
c.NoContent()                 // 204

// 错误响应
c.Fail("余额不足")            // 400
c.ValidationError(errors)     // 400
c.Unauthorized("请先登录")     // 401
c.Forbidden("无权访问")        // 403
c.NotFound("用户不存在")       // 404
c.ServerError("系统异常")      // 500

// 分页响应
c.Paginated(users, page, size, total)

// 自动分页查询
c.PaginateResponse(func(page, size int) (interface{}, int64) {
    return queryData(page, size)
})
```

### 4. JWT 认证

```go
// 登录 - 创建 JWT
token, _ := c.CreateJWTSession("secret-key", 2*time.Hour, gin.H{
    "user_id": user.ID,
    "username": user.Username,
    "role": user.Role,
})

// 认证中间件
func AuthMiddleware(c *gin.Context) {
    jwt, ok := c.RequireJWT()  // 自动验证并返回 401
    if !ok {
        return
    }
    c.Set("user_id", jwt["user_id"])
    c.Next()
}

// 受保护路由
protected := router.Group("/api")
protected.Use(AuthMiddleware)
{
    protected.GET("/profile", getProfile)
}

// 角色保护
admin := router.Group("/admin")
admin.Use(router.RequireAuth(), router.RequireRoles("admin"))

// 刷新令牌
newToken, _ := c.RefreshJWTSession("secret-key", 2*time.Hour)

// 注销
c.ClearJWT()
```

### 5. SSE 实时通信

```go
// 启用 SSE
router := gin.NewRouter(
    gin.WithSSE(&sse.Config{
        HistorySize: 1000,
        PingInterval: 30 * time.Second,
    }),
)

hub := router.GetSSEHub()

// SSE 连接端点
router.GET("/events", func(c *gin.Context) {
    client := c.NewSSEClientWithOptions(
        []string{"user.created", "system.notice"},
        sse.WithClientID(c.Query("client_id")),
    )
    <-client.Disconnected
})

// 广播消息
hub.Broadcast(&sse.Event{
    Event: "notification",
    Data: gin.H{"message": "系统通知"},
})

// 发送给特定客户端
hub.SendToClient(clientID, &sse.Event{
    Event: "private",
    Data: gin.H{"message": "私有消息"},
})
```

### 6. 缓存系统

```go
router.GET("/users/:id", func(c *gin.Context) {
    id := c.Param("id")
    cacheKey := "user:" + id

    cache := c.GetCache()

    // 尝试从缓存获取
    if cachedUser, found := cache.Get(cacheKey); found {
        c.Success(cachedUser)
        return
    }

    // 从数据库获取
    user := getUserFromDB(id)

    // 设置缓存（5分钟）
    cache.SetWithTTL(cacheKey, user, 5*time.Minute)

    c.Success(user)
})
```

### 7. OpenAPI 文档

```go
// 启用 OpenAPI
router := gin.NewRouter(
    gin.WithOpenAPI(&gin.OpenAPI{
        Title: "My API",
        Version: "1.0.0",
    }),
)

// 启用 Swagger UI
router.EnableSwagger("/swagger")

// 路由文档注解
router.GET("/users/:id", getUserHandler,
    gin.Summary("获取用户详情"),
    gin.PathParam("id", "int", "用户ID"),
    gin.Response(200, User{}),
    gin.Response(404, ErrorResponse{}),
)

// 泛型 API 定义
router.POST("/users", createUserHandler,
    gin.ReqBody[CreateUserRequest](),  // 类型安全
    gin.Resp[User](201),
    gin.Resp[ValidationError](400),
)
```

## 使用示例

### 完整 RESTful API 示例

```go
package main

import (
    "time"
    "github.com/darkit/gin"
    "github.com/darkit/gin/cache"
)

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func main() {
    router := gin.NewRouter(
        gin.WithGinMode("debug"),
        gin.WithJWT("your-super-secret-key"),
        gin.WithCache(&cache.Config{
            TTL: 30 * time.Minute,
            CleanupInterval: 5 * time.Minute,
        }),
        gin.WithCORS("*"),
        gin.WithRateLimit(1000),
        gin.WithRequestID(),
    )

    // 健康检查
    router.Health()
    router.Metrics()

    // 公开路由
    router.POST("/login", handleLogin)

    // 受保护的 API
    api := router.Group("/api")
    api.Use(AuthMiddleware)
    {
        api.GET("/users", listUsers)
        api.GET("/users/:id", getUser)
        api.POST("/users", createUser)
        api.PUT("/users/:id", updateUser)
        api.DELETE("/users/:id", deleteUser)
    }

    router.Run(":8080")
}

func listUsers(c *gin.Context) {
    page := c.ParamInt("page", 1)
    size := c.ParamInt("size", 10)

    users, total := getUsersPaginated(page, size)
    c.Paginated(users, int64(page), int64(size), int64(total))
}

func createUser(c *gin.Context) {
    var user User
    if !c.BindJSON(&user) {
        return  // 自动返回 400 验证错误
    }

    createdUser := saveUser(user)
    c.Created(createdUser)  // 201 状态码
}

func AuthMiddleware(c *gin.Context) {
    jwt, ok := c.RequireJWT()
    if !ok {
        return
    }
    c.Set("user_id", jwt["user_id"])
    c.Next()
}
```

## 指导原则

### 架构设计

- **选项式配置优先**：使用 `gin.NewRouter()` 配合 `gin.WithXXX()` 选项进行链式配置
- **统一响应格式**：始终使用 `Success()`、`Fail()`、`NotFound()` 等便捷方法
- **分层架构**：遵循 Handler → Service → Repository 分层模式
- **接口抽象**：业务逻辑依赖接口而非具体实现

### 安全实践

- **JWT 密钥管理**：从环境变量读取，不要硬编码
- **CORS 配置**：生产环境明确指定允许的域名
- **输入验证**：使用 `binding` 标签自动验证，结合 `c.BindJSON()`
- **敏感信息过滤**：启用 `SecurityConfig.SensitiveFilter`
- **安全头**：使用 `c.SetSecureHeaders()` 设置安全响应头

### 性能优化

- **缓存策略**：对热点数据使用缓存，设置合理的 TTL
- **连接池**：配置数据库连接池参数（MaxOpenConns、MaxIdleConns）
- **并发处理**：使用 goroutine 并行获取独立数据
- **分页限制**：限制最大分页大小（如 100）
- **Context 超时**：使用 `gin.WithTimeout()` 设置全局超时

### 错误处理

- **统一错误响应**：使用框架提供的错误响应方法
- **定义业务错误**：创建自定义错误类型
- **错误日志记录**：记录详细错误信息，返回用户友好消息
- **错误包装**：使用 `fmt.Errorf("...: %w", err)` 包装错误

### 测试策略

- **单元测试**：测试业务逻辑和数据访问层
- **集成测试**：使用 `httptest` 测试 HTTP 处理器
- **Mock 依赖**：使用接口进行依赖注入，便于测试

## 常见陷阱

### 配置问题

- ❌ **硬编码配置**：不要在代码中硬编码密钥、URL 等配置

  ```go
  // 错误
  router := gin.NewRouter(gin.WithJWT("hardcoded-secret"))

  // 正确
  router := gin.NewRouter(gin.WithJWT(os.Getenv("JWT_SECRET")))
  ```

- ❌ **通配符 CORS**：生产环境不要使用 `"*"` 允许所有域名

  ```go
  // 错误
  gin.WithCORS("*")

  // 正确
  gin.WithCORS("https://example.com", "https://app.example.com")
  ```

### 响应格式

- ❌ **不统一的响应格式**：直接使用 `c.JSON()` 导致格式不一致

  ```go
  // 错误
  c.JSON(200, user)

  // 正确
  c.Success(user)
  ```

### 错误处理

- ❌ **忽略错误**：不处理或忽略错误返回值

  ```go
  // 错误
  user, _ := userService.GetUser(id)

  // 正确
  user, err := userService.GetUser(id)
  if err != nil {
      c.ServerError("获取用户失败")
      return
  }
  ```

- ❌ **泄露敏感信息**：直接返回数据库错误给用户

  ```go
  // 错误
  c.JSON(500, gin.H{"error": err.Error()})

  // 正确
  log.Printf("数据库错误: %v", err)
  c.ServerError("系统异常")
  ```

### JWT 使用

- ❌ **不设置过期时间**：JWT 令牌应设置合理的过期时间

  ```go
  // 错误
  c.CreateJWTSession("key", 0, payload)

  // 正确
  c.CreateJWTSession("key", 2*time.Hour, payload)
  ```

- ❌ **未验证 JWT**：受保护的路由忘记添加认证中间件

  ```go
  // 错误
  router.GET("/api/profile", getProfile)

  // 正确
  protected := router.Group("/api")
  protected.Use(AuthMiddleware)
  protected.GET("/profile", getProfile)
  ```

### 缓存使用

- ❌ **缓存键冲突**：使用简单的键名导致冲突

  ```go
  // 错误
  cache.Set("user", user)

  // 正确
  cache.Set(fmt.Sprintf("user:%d", id), user)
  ```

- ❌ **忘记清除缓存**：更新或删除数据后忘记清除缓存
  ```go
  // 正确
  updateUser(user)
  cache.Delete(fmt.Sprintf("user:%d", user.ID))
  ```

### 并发安全

- ❌ **共享变量无保护**：多个 goroutine 访问共享变量未加锁

  ```go
  // 错误 - 竞态条件
  var counter int
  for i := 0; i < 100; i++ {
      go func() { counter++ }()
  }

  // 正确 - 使用互斥锁
  var counter int
  var mu sync.Mutex
  for i := 0; i < 100; i++ {
      go func() {
          mu.Lock()
          counter++
          mu.Unlock()
      }()
  }
  ```

## 资源导航

### 核心特性

- [Quick Start Guide](resources/quick-start.md) - 快速开始和基础配置
- [Router Configuration](resources/router-config.md) - 路由器配置选项详解
- [Response Methods](resources/response-methods.md) - 统一响应方法详解
- [Middleware Guide](resources/middleware-guide.md) - 中间件使用指南

### 认证授权

- [JWT Authentication](resources/jwt-auth.md) - JWT 认证完整指南
- [OAuth 2.0 System](resources/oauth.md) - OAuth 2.0 认证系统
- [Role-Based Access](resources/rbac.md) - 基于角色的访问控制

### 高级特性

- [SSE Real-time](resources/sse-realtime.md) - 服务器发送事件
- [Cache System](resources/cache-system.md) - 缓存系统详解
- [OpenAPI Documentation](resources/openapi-docs.md) - OpenAPI 文档生成
- [Static Resources](resources/static-resources.md) - 静态资源和文件系统

### 安全和性能

- [Security Hardening](resources/security.md) - 安全加固指南
- [Performance Optimization](resources/performance.md) - 性能优化技巧
- [Production Deployment](resources/deployment.md) - 生产环境部署

### 最佳实践

- [Project Structure](resources/project-structure.md) - 推荐的项目结构
- [Error Handling](resources/error-handling.md) - 错误处理模式
- [Testing Strategies](resources/testing.md) - 测试策略和实践
- [Migration Guide](resources/migration.md) - 从 gin-gonic/gin 迁移

### 完整示例

- [Complete Examples](resources/complete-examples.md) - 生产级应用示例
- [API Reference](resources/api-reference.md) - 完整 API 速查表

## 相关技能

- **golang-web-development** - Go Web 开发基础
- **golang-database** - 数据库操作和 ORM
- **golang-testing** - 测试驱动开发
- **golang-security** - Go 应用安全实践
- **golang-best-practices** - Go 最佳实践
- **backend-dev-guidelines** - 后端开发指南

## 核心优势

### vs gin-gonic/gin

| 特性          | gin-gonic/gin | darkit/gin  |
| ------------- | ------------- | ----------- |
| 基础路由      | ✅            | ✅ 增强     |
| 统一响应      | ❌            | ✅          |
| JWT 认证      | ❌            | ✅ 内置     |
| SSE 支持      | ❌            | ✅ 完整     |
| 缓存系统      | ❌            | ✅ 内置     |
| OpenAPI       | ❌            | ✅ 自动生成 |
| 选项式配置    | ❌            | ✅          |
| CRUD 快捷方法 | ❌            | ✅          |
| 安全加固      | 部分          | ✅ 完整     |
| 性能优化      | 标准          | ✅ 提升 45% |

### 性能指标

- **Context 创建**：提升 45%（对象池优化）
- **内存使用**：减少 35%（延迟初始化）
- **缓存 QPS**：高并发下提升 400%（分片缓存）
- **SSE 广播**：非阻塞设计，保护 Hub 性能

---

**框架版本**: 基于 gin-gonic/gin v1.11.0
**Go 版本要求**: Go 1.23+
**文档版本**: v0.1.5
**最后更新**: 2025-11-26
