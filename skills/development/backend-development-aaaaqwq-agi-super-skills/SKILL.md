---
name: backend-development
description: 后端服务开发。当用户需要开发 API、数据库设计、微服务架构或后端业务逻辑时使用此技能。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 后端服务开发

## 功能说明
此技能专门用于后端服务开发,包括:
- RESTful API 设计和实现
- 数据库设计和优化
- 微服务架构
- 认证和授权
- 消息队列和缓存
- 性能优化和监控

## 使用场景
- "设计一个用户认证 API"
- "创建 RESTful API 接口"
- "设计数据库表结构"
- "实现微服务架构"
- "优化数据库查询性能"
- "集成第三方支付接口"

## 技术栈

### 编程语言
- **Node.js**:Express、Koa、NestJS
- **Python**:Django、Flask、FastAPI
- **Java**:Spring Boot、Spring Cloud
- **Go**:Gin、Echo、Fiber
- **Rust**:Actix、Rocket

### 数据库
- **关系型**:MySQL、PostgreSQL、SQL Server
- **NoSQL**:MongoDB、Redis、Cassandra
- **时序数据库**:InfluxDB、TimescaleDB
- **图数据库**:Neo4j、ArangoDB

### 消息队列
- **RabbitMQ**:AMQP 协议消息队列
- **Kafka**:分布式流处理平台
- **Redis Pub/Sub**:轻量级消息发布订阅
- **NATS**:云原生消息系统

### 缓存
- **Redis**:内存数据库和缓存
- **Memcached**:分布式内存缓存
- **CDN**:静态资源缓存

## API 设计最佳实践

### RESTful API 规范
```
GET    /api/users          # 获取用户列表
GET    /api/users/:id      # 获取单个用户
POST   /api/users          # 创建用户
PUT    /api/users/:id      # 更新用户
PATCH  /api/users/:id      # 部分更新用户
DELETE /api/users/:id      # 删除用户
```

### 响应格式
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com"
  },
  "message": "操作成功",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

### 错误处理
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在",
    "details": {
      "userId": 123
    }
  },
  "timestamp": "2025-01-01T00:00:00Z"
}
```

## 代码示例

### Express API 示例
```typescript
import express from 'express';
import { body, validationResult } from 'express-validator';

const app = express();
app.use(express.json());

// 中间件:认证
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: '未授权' });
  }
  // 验证 token
  next();
};

// 中间件:错误处理
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: err.message
    }
  });
};

// 路由:获取用户列表
app.get('/api/users', authenticate, async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const users = await User.find()
      .skip((page - 1) * limit)
      .limit(limit);

    res.json({
      success: true,
      data: users,
      pagination: {
        page,
        limit,
        total: await User.countDocuments()
      }
    });
  } catch (error) {
    next(error);
  }
});

// 路由:创建用户
app.post('/api/users',
  authenticate,
  [
    body('email').isEmail(),
    body('password').isLength({ min: 6 })
  ],
  async (req, res, next) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array()
        });
      }

      const user = await User.create(req.body);
      res.status(201).json({
        success: true,
        data: user
      });
    } catch (error) {
      next(error);
    }
  }
);

app.use(errorHandler);
app.listen(3000);
```

### FastAPI 示例
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True

# 依赖注入:数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 依赖注入:当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="未授权")
    return user

@app.get("/api/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.post("/api/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")

    # 创建用户
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## 数据库设计

### 表结构设计
```sql
-- 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status (status)
);

-- 文章表
CREATE TABLE posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    FULLTEXT INDEX idx_title_content (title, content)
);
```

### 查询优化
```sql
-- 使用索引
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- 避免 SELECT *
SELECT id, name, email FROM users WHERE status = 'active';

-- 使用 JOIN 代替子查询
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

-- 分页查询
SELECT * FROM posts
WHERE status = 'published'
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;
```

## 认证和授权

### JWT 认证
```typescript
import jwt from 'jsonwebtoken';

// 生成 token
function generateToken(user: User): string {
  return jwt.sign(
    {
      userId: user.id,
      email: user.email
    },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
}

// 验证 token
function verifyToken(token: string): any {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// 认证中间件
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: '未授权' });
  }

  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: '无效的 token' });
  }
}
```

### RBAC 权限控制
```typescript
enum Role {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

enum Permission {
  READ = 'read',
  WRITE = 'write',
  DELETE = 'delete'
}

const rolePermissions = {
  [Role.ADMIN]: [Permission.READ, Permission.WRITE, Permission.DELETE],
  [Role.USER]: [Permission.READ, Permission.WRITE],
  [Role.GUEST]: [Permission.READ]
};

function authorize(requiredPermission: Permission) {
  return (req, res, next) => {
    const userRole = req.user.role;
    const permissions = rolePermissions[userRole];

    if (!permissions.includes(requiredPermission)) {
      return res.status(403).json({ error: '权限不足' });
    }

    next();
  };
}

// 使用
app.delete('/api/users/:id',
  authenticate,
  authorize(Permission.DELETE),
  deleteUser
);
```

## 缓存策略

### Redis 缓存
```typescript
import Redis from 'ioredis';

const redis = new Redis({
  host: 'localhost',
  port: 6379
});

// 缓存装饰器
function cache(ttl: number = 3600) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const cacheKey = `${propertyKey}:${JSON.stringify(args)}`;

      // 尝试从缓存获取
      const cached = await redis.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }

      // 执行原方法
      const result = await originalMethod.apply(this, args);

      // 存入缓存
      await redis.setex(cacheKey, ttl, JSON.stringify(result));

      return result;
    };

    return descriptor;
  };
}

class UserService {
  @cache(3600)
  async getUserById(id: number) {
    return await User.findById(id);
  }
}
```

## 消息队列

### RabbitMQ 示例
```typescript
import amqp from 'amqplib';

class MessageQueue {
  private connection: amqp.Connection;
  private channel: amqp.Channel;

  async connect() {
    this.connection = await amqp.connect('amqp://localhost');
    this.channel = await this.connection.createChannel();
  }

  async publish(queue: string, message: any) {
    await this.channel.assertQueue(queue, { durable: true });
    this.channel.sendToQueue(
      queue,
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    );
  }

  async consume(queue: string, handler: (msg: any) => Promise<void>) {
    await this.channel.assertQueue(queue, { durable: true });
    this.channel.prefetch(1);

    this.channel.consume(queue, async (msg) => {
      if (msg) {
        try {
          const content = JSON.parse(msg.content.toString());
          await handler(content);
          this.channel.ack(msg);
        } catch (error) {
          console.error('处理消息失败:', error);
          this.channel.nack(msg, false, true);
        }
      }
    });
  }
}

// 使用
const mq = new MessageQueue();
await mq.connect();

// 发布消息
await mq.publish('email-queue', {
  to: 'user@example.com',
  subject: '欢迎注册',
  body: '感谢您的注册'
});

// 消费消息
await mq.consume('email-queue', async (message) => {
  await sendEmail(message);
});
```

## 微服务架构

### 服务间通信
```typescript
// API Gateway
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

// 用户服务
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  changeOrigin: true
}));

// 订单服务
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  changeOrigin: true
}));

app.listen(3000);
```

## 监控和日志

### 日志记录
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 使用
logger.info('用户登录', { userId: 123, ip: '192.168.1.1' });
logger.error('数据库连接失败', { error: err.message });
```

## 注意事项
- 实现完善的错误处理
- 使用环境变量管理配置
- 实施 API 限流和防护
- 定期备份数据库
- 监控系统性能和日志
- 编写单元测试和集成测试
- 使用 Docker 容器化部署
