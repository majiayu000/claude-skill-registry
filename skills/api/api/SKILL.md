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

### Next.js App Router

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).optional(),
});

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get("page") || "1");
    const pageSize = parseInt(searchParams.get("pageSize") || "20");

    const [users, total] = await Promise.all([
      db.users.findMany({
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      db.users.count(),
    ]);

    return NextResponse.json({
      success: true,
      data: users,
      pagination: {
        page,
        pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      },
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: { message: "获取用户失败" } },
      { status: 500 },
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = CreateUserSchema.parse(body);

    const user = await db.users.create({ data: validated });

    return NextResponse.json(
      { success: true, data: user, message: "创建成功" },
      { status: 201 },
    );
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: "VALIDATION_ERROR",
            message: "请求参数无效",
            details: error.errors,
          },
        },
        { status: 400 },
      );
    }
    throw error;
  }
}
```

### FastAPI

```python
# routers/users.py
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

@router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    skip = (page - 1) * page_size
    users = await db.users.find().skip(skip).limit(page_size).to_list()
    total = await db.users.count_documents({})

    return {
        "success": True,
        "data": users,
        "pagination": {
            "page": page,
            "pageSize": page_size,
            "total": total,
            "totalPages": (total + page_size - 1) // page_size
        }
    }

@router.post("", status_code=201)
async def create_user(user: UserCreate):
    result = await db.users.insert_one(user.dict())
    created = await db.users.find_one({"_id": result.inserted_id})

    return {
        "success": True,
        "data": created,
        "message": "创建成功"
    }

@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    return {"success": True, "data": user}
```

### Express.js

```typescript
// routes/users.ts
import { Router } from "express";
import { body, query, validationResult } from "express-validator";

const router = Router();

router.get(
  "/",
  [
    query("page").optional().isInt({ min: 1 }),
    query("pageSize").optional().isInt({ min: 1, max: 100 }),
  ],
  async (req, res, next) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: "VALIDATION_ERROR", details: errors.array() },
        });
      }

      const page = parseInt(req.query.page as string) || 1;
      const pageSize = parseInt(req.query.pageSize as string) || 20;

      const [users, total] = await Promise.all([
        User.find()
          .skip((page - 1) * pageSize)
          .limit(pageSize),
        User.countDocuments(),
      ]);

      res.json({
        success: true,
        data: users,
        pagination: {
          page,
          pageSize,
          total,
          totalPages: Math.ceil(total / pageSize),
        },
      });
    } catch (error) {
      next(error);
    }
  },
);

router.post(
  "/",
  [body("name").notEmpty().isLength({ max: 100 }), body("email").isEmail()],
  async (req, res, next) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: "VALIDATION_ERROR", details: errors.array() },
        });
      }

      const user = await User.create(req.body);
      res.status(201).json({ success: true, data: user, message: "创建成功" });
    } catch (error) {
      next(error);
    }
  },
);

export default router;
```

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

```typescript
// app/api/v1/users/route.ts
export async function GET() { ... }

// app/api/v2/users/route.ts
export async function GET() { ... }
```

## 认证与授权

### JWT 认证中间件

```typescript
// middlewares/auth.ts
import jwt from "jsonwebtoken";

export async function authMiddleware(request: NextRequest) {
  const token = request.headers.get("Authorization")?.replace("Bearer ", "");

  if (!token) {
    return NextResponse.json(
      {
        success: false,
        error: { code: "UNAUTHORIZED", message: "未提供认证信息" },
      },
      { status: 401 },
    );
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    request.user = decoded;
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        error: { code: "UNAUTHORIZED", message: "Token 无效" },
      },
      { status: 401 },
    );
  }
}
```

### 权限检查

```typescript
export function requireRole(...roles: string[]) {
  return (request: NextRequest) => {
    if (!roles.includes(request.user.role)) {
      return NextResponse.json(
        { success: false, error: { code: "FORBIDDEN", message: "权限不足" } },
        { status: 403 },
      );
    }
  };
}

// 使用
export async function DELETE(request: NextRequest) {
  const authError = await authMiddleware(request);
  if (authError) return authError;

  const roleError = requireRole("admin")(request);
  if (roleError) return roleError;

  // 执行删除
}
```

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
