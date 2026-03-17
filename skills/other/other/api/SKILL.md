---
name: api
description: "RESTful API design patterns and best practices. Use when creating endpoints, designing APIs, or implementing routes."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API 开发技能

本技能提供 RESTful API 开发的最佳实践和模式。

## 触发条件

- 创建 API 端点
- 设计 REST API
- 实现后端路由
- 处理请求/响应
- API 版本控制

## RESTful 设计原则

### URL 设计

```
# 资源命名 - 使用名词复数
GET    /api/v1/users           # 获取用户列表
GET    /api/v1/users/:id       # 获取单个用户
POST   /api/v1/users           # 创建用户
PUT    /api/v1/users/:id       # 更新用户（完整替换）
PATCH  /api/v1/users/:id       # 更新用户（部分更新）
DELETE /api/v1/users/:id       # 删除用户

# 嵌套资源
GET    /api/v1/users/:id/orders           # 用户的订单
GET    /api/v1/users/:id/orders/:orderId  # 用户的特定订单

# 动作资源
POST   /api/v1/users/:id/activate         # 激活用户
POST   /api/v1/orders/:id/cancel          # 取消订单
```

### HTTP 方法语义

| 方法   | 语义     | 幂等 | 安全 |
| ------ | -------- | ---- | ---- |
| GET    | 读取资源 | ✅   | ✅   |
| POST   | 创建资源 | ❌   | ❌   |
| PUT    | 完整更新 | ✅   | ❌   |
| PATCH  | 部分更新 | ❌   | ❌   |
| DELETE | 删除资源 | ✅   | ❌   |

## 统一响应格式

### 成功响应

```typescript
// 单个资源
{
  "success": true,
  "data": {
    "id": "123",
    "name": "张三",
    "email": "zhangsan@example.com"
  }
}

// 列表资源
{
  "success": true,
  "data": [
    { "id": "1", "name": "用户1" },
    { "id": "2", "name": "用户2" }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}

// 创建成功
{
  "success": true,
  "data": { "id": "123", ... },
  "message": "创建成功"
}
```

### 错误响应

```typescript
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数无效",
    "details": [
      { "field": "email", "message": "邮箱格式不正确" },
      { "field": "age", "message": "年龄必须大于 0" }
    ]
  }
}
```

## API 路由实现

各框架的完整 CRUD 路由实现：

> 详见 [Next.js API Patterns](nextjs.md) - App Router + Zod 验证 + 认证授权
>
> 详见 [FastAPI Patterns](fastapi.md) - Pydantic 模型 + 异步路由
>
> 详见 [Express.js Patterns](express.md) - express-validator + 中间件

## 查询参数处理

### 分页

```typescript
interface PaginationParams {
  page?: number;
  pageSize?: number;
  cursor?: string; // 游标分页
}

// 偏移分页
const { page = 1, pageSize = 20 } = query;
const skip = (page - 1) * pageSize;

// 游标分页（大数据量推荐）
const { cursor, pageSize = 20 } = query;
const where = cursor ? { id: { gt: cursor } } : {};
```

### 排序

```typescript
// ?sort=createdAt:desc,name:asc
const sortParam = query.sort as string;
const orderBy = sortParam?.split(",").map((s) => {
  const [field, order] = s.split(":");
  return { [field]: order || "asc" };
}) || [{ createdAt: "desc" }];
```

### 筛选

```typescript
// ?status=active&role=admin
const { status, role } = query;
const where = {
  ...(status && { status }),
  ...(role && { role }),
};
```

### 搜索

```typescript
// ?q=keyword
const { q } = query;
const where = q
  ? {
      OR: [
        { name: { contains: q, mode: "insensitive" } },
        { email: { contains: q, mode: "insensitive" } },
      ],
    }
  : {};
```

## API 版本控制

### URL 路径版本

```
/api/v1/users
/api/v2/users
```

### 请求头版本

```
Accept: application/vnd.api+json; version=1
```

### 版本控制实现

> 详见 [Next.js API Patterns](nextjs.md#版本控制实现)

## 认证与授权

> JWT 认证中间件和权限检查的完整实现详见 [Next.js API Patterns](nextjs.md#认证与授权)

## HTTP 状态码

| 状态码 | 含义                  | 使用场景      |
| ------ | --------------------- | ------------- |
| 200    | OK                    | 成功获取/更新 |
| 201    | Created               | 成功创建      |
| 204    | No Content            | 成功删除      |
| 400    | Bad Request           | 请求参数错误  |
| 401    | Unauthorized          | 未认证        |
| 403    | Forbidden             | 无权限        |
| 404    | Not Found             | 资源不存在    |
| 409    | Conflict              | 资源冲突      |
| 422    | Unprocessable Entity  | 业务逻辑错误  |
| 429    | Too Many Requests     | 请求过多      |
| 500    | Internal Server Error | 服务器错误    |

## 最佳实践

1. **使用名词复数** - `/users` 而非 `/user`
2. **HTTP 方法语义** - GET 读取，POST 创建，PUT/PATCH 更新
3. **统一响应格式** - success、data、error、pagination
4. **输入验证** - 使用 Zod/Pydantic 验证
5. **错误处理** - 返回有意义的错误码和消息
6. **版本控制** - /api/v1/
7. **分页** - 列表接口必须分页
8. **HATEOAS** - 可选，返回相关链接
9. **文档** - OpenAPI/Swagger 文档
10. **幂等性** - PUT、DELETE 保持幂等

> **记住**: API 设计的核心是一致性——统一的 URL 结构、响应格式、错误处理，让调用方可预测。
