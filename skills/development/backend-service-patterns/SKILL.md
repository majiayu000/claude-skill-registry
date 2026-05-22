---
name: backend-service-patterns
description: Architect scalable backend services using layered architecture, dependency injection, middleware patterns, service classes, and separation of concerns. Use when building API services, implementing business logic layers, creating service classes, setting up middleware chains, implementing dependency injection, designing controller-service-repository patterns, handling cross-cutting concerns, creating domain models, implementing CQRS patterns, or establishing backend architecture standards.
---

# Backend Service Patterns - Building Scalable Server Applications

## When to use this skill

- Building API services and backend applications
- Implementing business logic in service layers
- Creating controller-service-repository architectures
- Setting up Express/Fastify middleware chains
- Implementing dependency injection containers
- Designing domain models and business entities
- Handling cross-cutting concerns (logging, auth, validation)
- Implementing CQRS (Command Query Responsibility Segregation)
- Creating background job processing services
- Designing event-driven service architectures
- Implementing API gateway patterns
- Building microservices with clear boundaries

## When to use this skill

- Designing backend architecture, implementing APIs, handling business logic, managing microservices, or building serverless functions.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Designing backend architecture, implementing APIs, handling business logic, managing microservices, or building serverless functions.

## Core Principles

1. **Separation of Concerns** - Clear boundaries between layers
2. **Single Responsibility** - Each service does one thing well
3. **Stateless Design** - Easy to scale horizontally
4. **Idempotency** - Safe to retry operations
5. **Fail Fast, Recover Gracefully** - Handle errors explicitly

## Layered Architecture

### 1. **Three-Tier Architecture**

```typescript
// ✅ Routes Layer - HTTP endpoints
// routes/users.ts
import express from 'express';
import { UserController } from '../controllers/UserController';

const router = express.Router();
const userController = new UserController();

router.get('/users', userController.list);
router.post('/users', userController.create);
router.get('/users/:id', userController.get);

export default router;

// ✅ Controller Layer - Request/response handling
// controllers/UserController.ts
import { Request, Response } from 'express';
import { UserService } from '../services/UserService';
import { CreateUserSchema } from '../schemas/user';

export class UserController {
  private userService = new UserService();

  list = async (req: Request, res: Response) => {
    try {
      const users = await this.userService.listUsers({
        page: parseInt(req.query.page as string) || 1,
        limit: parseInt(req.query.limit as string) || 20
      });
      res.json(users);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch users' });
    }
  };

  create = async (req: Request, res: Response) => {
    try {
      const validated = CreateUserSchema.parse(req.body);
      const user = await this.userService.createUser(validated);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };
}

// ✅ Service Layer - Business logic
// services/UserService.ts
import { UserRepository } from '../repositories/UserRepository';
import { EmailService } from './EmailService';

export class UserService {
  private userRepo = new UserRepository();
  private emailService = new EmailService();

  async createUser(data: CreateUserInput) {
    // Business logic here
    const existingUser = await this.userRepo.findByEmail(data.email);
    if (existingUser) {
      throw new Error('Email already exists');
    }

    const hashedPassword = await bcrypt.hash(data.password, 10);
    const user = await this.userRepo.create({
      ...data,
      passwordHash: hashedPassword
    });

    // Send welcome email asynchronously
    await this.emailService.sendWelcome(user.email);

    return user;
  }

  async listUsers(params: { page: number; limit: number }) {
    return await this.userRepo.findMany({
      skip: (params.page - 1) * params.limit,
      take: params.limit
    });
  }
}

// ✅ Repository Layer - Data access
// repositories/UserRepository.ts
import { prisma } from '../db';

export class UserRepository {
  async create(data: CreateUserData) {
    return await prisma.user.create({ data });
  }

  async findByEmail(email: string) {
    return await prisma.user.findUnique({ where: { email } });
  }

  async findMany(params: { skip: number; take: number }) {
    return await prisma.user.findMany(params);
  }
}
```

### 2. **Dependency Injection**

```typescript
// ✅ Constructor injection for testability
export class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentService: PaymentService,
    private emailService: EmailService
  ) {}

  async processOrder(orderId: string) {
    const order = await this.orderRepo.findById(orderId);
    const payment = await this.paymentService.charge(order);
    await this.emailService.sendReceipt(order, payment);
    return payment;
  }
}

// Easy to mock in tests
const mockOrderRepo = {
  findById: jest.fn().mockResolvedValue({ id: '1', total: 100 })
};
const mockPaymentService = {
  charge: jest.fn().mockResolvedValue({ id: 'pay_123' })
};
const service = new OrderService(mockOrderRepo, mockPaymentService, mockEmailService);
```

## Design Patterns

### 1. **Repository Pattern**

```typescript
// ✅ Abstract data access behind interface
interface IUserRepository {
  create(data: CreateUserData): Promise<User>;
  findById(id: string): Promise<User | null>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

// PostgreSQL implementation
export class PostgresUserRepository implements IUserRepository {
  async create(data: CreateUserData) {
    return await prisma.user.create({ data });
  }
  
  async findById(id: string) {
    return await prisma.user.findUnique({ where: { id } });
  }
  
  // ... other methods
}

// MongoDB implementation (easy to swap)
export class MongoUserRepository implements IUserRepository {
  async create(data: CreateUserData) {
    return await User.create(data);
  }
  
  // ... other methods
}
```

### 2. **Service Layer Pattern**

```typescript
// ✅ Encapsulate business logic
export class OrderService {
  async placeOrder(userId: string, items: OrderItem[]) {
    // Validate inventory
    for (const item of items) {
      const product = await this.productRepo.findById(item.productId);
      if (product.stock < item.quantity) {
        throw new InsufficientStockError(item.productId);
      }
    }

    // Calculate total
    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    // Apply discount
    const discount = await this.discountService.calculateDiscount(userId, total);

    // Create order
    const order = await this.orderRepo.create({
      userId,
      items,
      subtotal: total,
      discount,
      total: total - discount,
      status: 'pending'
    });

    // Reserve inventory
    for (const item of items) {
      await this.inventoryService.reserve(item.productId, item.quantity);
    }

    // Queue payment processing
    await this.paymentQueue.add({ orderId: order.id });

    return order;
  }
}
```

### 3. **Factory Pattern**

```typescript
// ✅ Create objects based on conditions
interface PaymentProvider {
  charge(amount: number, currency: string): Promise<PaymentResult>;
}

class StripeProvider implements PaymentProvider {
  async charge(amount: number, currency: string) {
    return await stripe.charges.create({ amount, currency });
  }
}

class PayPalProvider implements PaymentProvider {
  async charge(amount: number, currency: string) {
    return await paypal.payment.create({ amount, currency });
  }
}

class PaymentProviderFactory {
  static create(provider: string): PaymentProvider {
    switch (provider) {
      case 'stripe':
        return new StripeProvider();
      case 'paypal':
        return new PayPalProvider();
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }
}

// Usage
const provider = PaymentProviderFactory.create(user.preferredPaymentMethod);
await provider.charge(100, 'USD');
```

### 4. **Strategy Pattern**

```typescript
// ✅ Swap algorithms at runtime
interface ShippingStrategy {
  calculateCost(weight: number, distance: number): number;
}

class StandardShipping implements ShippingStrategy {
  calculateCost(weight: number, distance: number) {
    return weight * 0.5 + distance * 0.1;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculateCost(weight: number, distance: number) {
    return weight * 1.0 + distance * 0.3;
  }
}

class OvernightShipping implements ShippingStrategy {
  calculateCost(weight: number, distance: number) {
    return weight * 2.0 + distance * 0.5;
  }
}

class ShippingCalculator {
  constructor(private strategy: ShippingStrategy) {}

  calculate(weight: number, distance: number) {
    return this.strategy.calculateCost(weight, distance);
  }
}

// Usage
const calculator = new ShippingCalculator(new ExpressShipping());
const cost = calculator.calculate(10, 500);
```

### 5. **Observer Pattern (Event-Driven)**

```typescript
// ✅ Decouple components with events
import { EventEmitter } from 'events';

class OrderEvents extends EventEmitter {
  static CREATED = 'order.created';
  static PAID = 'order.paid';
  static SHIPPED = 'order.shipped';
  static CANCELLED = 'order.cancelled';
}

const orderEvents = new OrderEvents();

// Listeners
orderEvents.on(OrderEvents.CREATED, async (order) => {
  await emailService.sendOrderConfirmation(order);
  await analyticsService.trackOrderCreated(order);
});

orderEvents.on(OrderEvents.PAID, async (order) => {
  await inventoryService.deductStock(order.items);
  await shippingService.createShipment(order);
});

// Emit events
export class OrderService {
  async createOrder(data: CreateOrderData) {
    const order = await this.orderRepo.create(data);
    orderEvents.emit(OrderEvents.CREATED, order);
    return order;
  }

  async markAsPaid(orderId: string) {
    const order = await this.orderRepo.update(orderId, { status: 'paid' });
    orderEvents.emit(OrderEvents.PAID, order);
    return order;
  }
}
```

## Microservices Patterns

### 1. **API Gateway**

```typescript
// ✅ Single entry point for multiple services
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

// Route to different services
app.use('/api/users', createProxyMiddleware({ 
  target: 'http://user-service:3001',
  changeOrigin: true 
}));

app.use('/api/orders', createProxyMiddleware({ 
  target: 'http://order-service:3002',
  changeOrigin: true 
}));

app.use('/api/payments', createProxyMiddleware({ 
  target: 'http://payment-service:3003',
  changeOrigin: true 
}));

// Add authentication, rate limiting, logging here
app.use(authMiddleware);
app.use(rateLimiter);
app.use(logger);
```

### 2. **Service-to-Service Communication**

```typescript
// ✅ HTTP/REST communication
export class UserService {
  private orderServiceUrl = process.env.ORDER_SERVICE_URL;

  async getUserWithOrders(userId: string) {
    const user = await this.userRepo.findById(userId);
    
    // Call order service
    const response = await fetch(`${this.orderServiceUrl}/orders?userId=${userId}`);
    const orders = await response.json();

    return { ...user, orders };
  }
}

// ✅ Message queue communication (async)
import { Queue } from 'bullmq';

const emailQueue = new Queue('emails', {
  connection: { host: 'redis', port: 6379 }
});

// Producer (User Service)
export class UserService {
  async createUser(data: CreateUserData) {
    const user = await this.userRepo.create(data);
    
    // Async notification
    await emailQueue.add('welcome', {
      userId: user.id,
      email: user.email
    });

    return user;
  }
}

// Consumer (Email Service)
import { Worker } from 'bullmq';

const worker = new Worker('emails', async (job) => {
  if (job.name === 'welcome') {
    await sendWelcomeEmail(job.data.email);
  }
});
```

### 3. **Circuit Breaker Pattern**

```typescript
// ✅ Prevent cascading failures
import CircuitBreaker from 'opossum';

const options = {
  timeout: 3000,        // If function takes > 3s, trigger failure
  errorThresholdPercentage: 50,  // When 50% of requests fail...
  resetTimeout: 30000   // ...open circuit for 30s
};

const breaker = new CircuitBreaker(callExternalAPI, options);

breaker.fallback(() => {
  return { data: null, fromCache: true }; // Fallback response
});

breaker.on('open', () => {
  console.log('Circuit breaker opened - too many failures');
});

async function callExternalAPI() {
  const response = await fetch('https://external-api.com/data');
  return response.json();
}

// Usage
try {
  const data = await breaker.fire();
} catch (error) {
  // Circuit is open or request failed
}
```

## Serverless Patterns

### 1. **Function-as-a-Service**

```typescript
// ✅ AWS Lambda handler
import { APIGatewayProxyHandler } from 'aws-lambda';

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    const body = JSON.parse(event.body || '{}');
    
    // Business logic
    const result = await processOrder(body);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};

// ✅ Vercel Edge Function
export const config = {
  runtime: 'edge'
};

export default async function handler(request: Request) {
  const data = await processData();
  
  return new Response(JSON.stringify(data), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### 2. **Cold Start Optimization**

```typescript
// ✅ Initialize outside handler (persists across invocations)
import { PrismaClient } from '@prisma/client';

// Created once, reused across warm invocations
const prisma = new PrismaClient();

export const handler = async (event) => {
  // This runs on every invocation
  const users = await prisma.user.findMany();
  return { statusCode: 200, body: JSON.stringify(users) };
};

// ✅ Lazy initialization
let connection: Connection | null = null;

async function getConnection() {
  if (!connection) {
    connection = await createConnection();
  }
  return connection;
}

export const handler = async (event) => {
  const conn = await getConnection();
  // Use connection
};
```

## Background Jobs

### 1. **Job Queue Pattern**

```typescript
// ✅ BullMQ job processing
import { Queue, Worker } from 'bullmq';

const videoQueue = new Queue('video-processing', {
  connection: { host: 'redis', port: 6379 }
});

// Add jobs
export class VideoService {
  async uploadVideo(file: File) {
    const video = await this.videoRepo.create({ 
      filename: file.name,
      status: 'pending'
    });

    // Queue processing job
    await videoQueue.add('transcode', {
      videoId: video.id,
      inputPath: file.path
    }, {
      attempts: 3,           // Retry up to 3 times
      backoff: {
        type: 'exponential',
        delay: 5000          // 5s, 10s, 20s
      }
    });

    return video;
  }
}

// Worker process
const worker = new Worker('video-processing', async (job) => {
  if (job.name === 'transcode') {
    await transcodeVideo(job.data.videoId, job.data.inputPath);
    
    // Update progress
    job.updateProgress(50);
    
    await generateThumbnail(job.data.videoId);
    
    job.updateProgress(100);
  }
}, {
  connection: { host: 'redis', port: 6379 },
  concurrency: 5  // Process 5 jobs concurrently
});

worker.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});

worker.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed:`, err);
});
```

### 2. **Scheduled Tasks**

```typescript
// ✅ Cron jobs with node-cron
import cron from 'node-cron';

// Run every day at midnight
cron.schedule('0 0 * * *', async () => {
  await cleanupExpiredSessions();
  await generateDailyReport();
});

// Run every 5 minutes
cron.schedule('*/5 * * * *', async () => {
  await checkPaymentStatus();
});

// ✅ Or use BullMQ repeat
await queue.add('daily-report', {}, {
  repeat: {
    pattern: '0 0 * * *'  // Cron expression
  }
});
```

## Backend Best Practices

### 1. **Configuration Management**

```typescript
// ✅ Environment-based config
export const config = {
  port: parseInt(process.env.PORT || '3000'),
  database: {
    url: process.env.DATABASE_URL,
    poolSize: parseInt(process.env.DB_POOL_SIZE || '10')
  },
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379')
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '1h'
  }
};

// Validate required vars on startup
const required = ['DATABASE_URL', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}
```

### 2. **Health Checks**

```typescript
// ✅ Health check endpoint
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'ok',
    checks: {
      database: 'ok',
      redis: 'ok'
    }
  };

  try {
    await prisma.$queryRaw`SELECT 1`;
  } catch (error) {
    health.status = 'degraded';
    health.checks.database = 'error';
  }

  try {
    await redis.ping();
  } catch (error) {
    health.status = 'degraded';
    health.checks.redis = 'error';
  }

  const statusCode = health.status === 'ok' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

## Backend Service Checklist

```
Architecture:
□ Clear separation of concerns (routes/controllers/services/repos)
□ Dependency injection for testability
□ Business logic in service layer (not controllers)
□ Data access abstracted in repositories
□ No database queries in controllers

API Design:
□ RESTful endpoints
□ Proper HTTP methods and status codes
□ Input validation on all endpoints
□ Pagination for lists
□ API versioning strategy

Error Handling:
□ Try/catch in all async functions
□ Meaningful error messages
□ Proper error status codes
□ Error logging with context
□ No sensitive data in error responses

Performance:
□ Database queries optimized
□ Connection pooling configured
□ Caching strategy implemented
□ Background jobs for heavy operations
□ Rate limiting on public endpoints

Security:
□ Authentication required
□ Authorization checks
□ Input sanitization
□ SQL injection prevention
□ CORS configured properly

Monitoring:
□ Health check endpoint
□ Logging configured
□ Metrics collected
□ Error tracking (Sentry, etc.)
□ Performance monitoring
```

## Resources

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Microservices Patterns](https://microservices.io/patterns/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Remember**: Great backend services are maintainable, testable, scalable, and resilient. Design for failure, optimize for readability.
