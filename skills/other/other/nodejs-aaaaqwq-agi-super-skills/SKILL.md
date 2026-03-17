---
name: backend-development-nodejs
description: |
  Node.js后端开发专家。精通NestJS、Express、Koa等框架，以及TypeScript、Prisma、Redis等技术栈。

  适用场景：
  - 企业级应用 (NestJS)
  - 快速API开发 (Express/Koa)
  - 实时通信 (Socket.io)
  - GraphQL (Apollo/TypeGraphQL)
  - 数据库ORM (Prisma/TypeORM)
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 🟢 Node.js 后端开发专家

老王我也玩Node.js很多年了，这玩意儿写后端真tm顺手！

## 技术栈全景

```
┌─────────────────────────────────────────────────────────────┐
│                    Node.js 后端技术栈                        │
├─────────────────────────────────────────────────────────────┤
│  Web框架                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ NestJS  │  │ Express │  │  Koa    │  │ Fastify │        │
│  │ 企业级  │  │ 经典    │  │ 轻量    │  │ 高性能  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
├─────────────────────────────────────────────────────────────┤
│  数据层                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ Prisma  │  │ TypeORM │  │ Mongoose│                     │
│  │ 新一代  │  │ 经典ORM │  │ MongoDB │                     │
│  └─────────┘  └─────────┘  └─────────┘                     │
├─────────────────────────────────────────────────────────────┤
│  实时通信                                                    │
│  ┌─────────┐  ┌─────────┐                                   │
│  │Socket.io│  │  WS     │                                   │
│  │ 全功能  │  │ 原生    │                                   │
│  └─────────┘  └─────────┘                                   │
├─────────────────────────────────────────────────────────────┤
│  API风格                                                     │
│  ┌─────────┐  ┌─────────┐                                   │
│  │  REST   │  │ GraphQL │                                   │
│  │ 经典    │  │ 灵活查询│                                   │
│  └─────────┘  └─────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## NestJS - 企业级首选

### 项目结构（最佳实践）

```
my-project/
├── src/
│   ├── main.ts                  # 应用入口
│   ├── app.module.ts            # 根模块
│   ├── config/                  # 配置
│   │   ├── configuration.ts
│   │   └── validation.schema.ts
│   ├── common/                  # 通用模块
│   │   ├── decorators/
│   │   ├── filters/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── pipes/
│   │   └── interfaces/
│   ├── modules/                 # 功能模块
│   │   ├── auth/
│   │   │   ├── auth.module.ts
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── strategies/
│   │   │   └── guards/
│   │   ├── users/
│   │   │   ├── users.module.ts
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   └── entities/
│   │   └── posts/
│   ├── database/                # 数据库
│   │   ├── migrations/
│   │   └── seeds/
│   └── mail/                    # 邮件等外部服务
├── test/
│   ├── unit/
│   └── e2e/
├── .env.example
├── nest-cli.json
├── tsconfig.json
└── package.json
```

### Prisma + NestJS 完整集成

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  password  String
  name      String
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```typescript
// modules/users/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { User } from '@prisma/client';
import * as bcrypt from 'bcrypt';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll(): Promise<User[]> {
    return this.prisma.user.findMany({
      select: {
        id: true,
        email: true,
        name: true,
        isActive: true,
        createdAt: true,
        password: false, // 排除密码字段
      },
    });
  }

  async findOne(id: number): Promise<User> {
    const user = await this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        isActive: true,
        createdAt: true,
        password: false,
      },
    });

    if (!user) {
      throw new NotFoundException(`User #${id} not found`);
    }

    return user;
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async create(data: {
    email: string;
    password: string;
    name: string;
  }): Promise<User> {
    const hashedPassword = await bcrypt.hash(data.password, 10);

    return this.prisma.user.create({
      data: {
        ...data,
        password: hashedPassword,
      },
      select: {
        id: true,
        email: true,
        name: true,
        isActive: true,
        createdAt: true,
        password: false,
      },
    });
  }

  async update(id: number, data: Partial<User>): Promise<User> {
    const user = await this.findOne(id);

    if (data.password) {
      data.password = await bcrypt.hash(data.password, 10);
    }

    return this.prisma.user.update({
      where: { id },
      data,
      select: {
        id: true,
        email: true,
        name: true,
        isActive: true,
        createdAt: true,
        password: false,
      },
    });
  }

  async remove(id: number): Promise<User> {
    return this.prisma.user.delete({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        isActive: true,
        createdAt: true,
        password: false,
      },
    });
  }
}
```

### JWT + Passport 认证

```typescript
// modules/auth/strategies/jwt.strategy.ts
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private configService: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET'),
    });
  }

  async validate(payload: any) {
    return { userId: payload.sub, email: payload.email };
  }
}

// modules/auth/guards/jwt-auth.guard.ts
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

// modules/auth/decorators/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);

// 使用示例
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@CurrentUser() user: any) {
  return user;
}
```

### Validation Pipe + DTO

```typescript
// dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional, IsBoolean } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'John Doe', minLength: 2 })
  @IsString()
  @MinLength(2)
  name: string;

  @ApiProperty({ example: 'password123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;

  @ApiPropertyOptional({ default: true })
  @IsOptional()
  @IsBoolean()
  isActive?: boolean;
}

// main.ts - 全局启用验证
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,      // 自动移除未定义的属性
      forbidNonWhitelisted: true,  // 拒绝未定义的属性
      transform: true,      // 自动转换类型
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  );

  await app.listen(3000);
}
```

---

## Express - 快速原型开发

### Express + TypeScript 结构化写法

```typescript
// src/app.ts
import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { AppError, errorConverter, errorHandler } from './utils/errors';

class App {
  public app: Application;

  constructor() {
    this.app = express();
    this.initializeMiddlewares();
    this.initializeRoutes();
    this.initializeErrorHandling();
  }

  private initializeMiddlewares() {
    this.app.use(helmet());
    this.app.use(cors());
    this.app.use(compression());
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
  }

  private initializeRoutes() {
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // API 路由
    this.app.use('/api/v1/users', userRoutes);
  }

  private initializeErrorHandling() {
    this.app.use(errorConverter);
    this.app.use(errorHandler);
  }
}

export default new App().app;

// src/routes/user.routes.ts
import { Router, Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';
import { authMiddleware } from '../middlewares/auth.middleware';
import { validate CreateUserDto } from '../validators/user.validator';

const router = Router();
const userService = new UserService();

router.get(
  '/',
  authMiddleware,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const users = await userService.findAll();
      res.json({ success: true, data: users });
    } catch (error) {
      next(error);
    }
  }
);

router.post(
  '/',
  validate CreateUserDto,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await userService.create(req.body);
      res.status(201).json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }
);

export default router;
```

---

## Socket.io 实时通信

```typescript
// gateway/chat.gateway.ts
import {
  WebSocketGateway,
  SubscribeMessage,
  MessageBody,
  WebSocketServer,
  ConnectedSocket,
  OnGatewayInit,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({
  cors: { origin: '*' },
  namespace: '/chat',
})
export class ChatGateway
  implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect
{
  @WebSocketServer()
  server: Server;

  private connectedClients: Map<string, Socket> = new Map();

  afterInit(server: Server) {
    console.log('WebSocket server initialized');
  }

  handleConnection(client: Socket) {
    const userId = client.handshake.query.userId as string;
    this.connectedClients.set(userId, client);
    console.log(`Client connected: ${userId}`);
  }

  handleDisconnect(client: Socket) {
    const userId = client.handshake.query.userId as string;
    this.connectedClients.delete(userId);
    console.log(`Client disconnected: ${userId}`);
  }

  @SubscribeMessage('sendMessage')
  handleMessage(
    @MessageBody() data: { roomId: string; message: string; userId: string },
    @ConnectedSocket() client: Socket,
  ) {
    // 广播消息到房间
    this.server.to(data.roomId).emit('newMessage', {
      userId: data.userId,
      message: data.message,
      timestamp: new Date().toISOString(),
    });
  }

  @SubscribeMessage('joinRoom')
  handleJoinRoom(
    @MessageBody() data: { roomId: string },
    @ConnectedSocket() client: Socket,
  ) {
    client.join(data.roomId);
    client.emit('joinedRoom', data.roomId);
  }
}
```

---

## Redis 缓存装饰器

```typescript
// common/decorators/cache.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const CACHE_KEY_METADATA = 'CACHE_KEY_METADATA';
export const CACHE_TTL_METADATA = 'CACHE_TTL_METADATA';

export const Cache = (key: string, ttl: number = 60) =>
  SetMetadata(CACHE_KEY_METADATA, { key, ttl });

// common/interceptors/cache.interceptor.ts
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { RedisService } from '../services/redis.service';

@Injectable()
export class CacheInterceptor implements NestInterceptor {
  constructor(private redisService: RedisService) {}

  async intercept(context: ExecutionContext, next: CallHandler): Promise<Observable<any>> {
    const request = context.switchToHttp().getRequest();
    const cacheKey = `cache:${request.url}:${JSON.stringify(request.query)}`;

    // 尝试从缓存获取
    const cached = await this.redisService.get(cacheKey);
    if (cached) {
      return of(JSON.parse(cached));
    }

    return next.handle().pipe(
      tap(async (data) => {
        await this.redisService.set(cacheKey, JSON.stringify(data), 60);
      })
    );
  }
}

// 使用
@Injectable()
export class UsersService {
  @Cache('users:list', 300)
  async findAll() {
    return this.usersRepository.findAll();
  }
}
```

---

## 依赖推荐（package.json）

```json
{
  "dependencies": {
    "@nestjs/common": "^10.3.0",
    "@nestjs/core": "^10.3.0",
    "@nestjs/platform-express": "^10.3.0",
    "@nestjs/config": "^3.1.1",
    "@nestjs/jwt": "^10.2.0",
    "@nestjs/passport": "^10.0.3",
    "@nestjs/swagger": "^7.1.17",
    "@prisma/client": "^5.7.0",
    "passport": "^0.7.0",
    "passport-jwt": "^4.0.1",
    "passport-local": "^1.0.0",
    "bcrypt": "^5.1.1",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1",
    "helmet": "^7.1.0",
    "cors": "^2.8.5",
    "compression": "^1.7.4",
    "redis": "^4.6.11",
    "socket.io": "^4.6.0",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "@nestjs/cli": "^10.2.1",
    "@nestjs/schematics": "^10.1.0",
    "@types/express": "^4.17.21",
    "@types/node": "^20.10.6",
    "@types/passport-jwt": "^4.0.0",
    "typescript": "^5.3.3",
    "prisma": "^5.7.0",
    "jest": "^29.7.0",
    "supertest": "^6.3.3"
  }
}
```

---

**老王建议**：
- 企业级项目直接用 NestJS + Prisma + TypeScript
- 快速原型用 Express，但记得加上类型检查
- 实时通信用 Socket.io，别tm自己造轮子
- GraphQL 考虑 TypeGraphQL，类型安全很重要
- 别忘了加上 Swagger 文档，接口文档自动化很香！
