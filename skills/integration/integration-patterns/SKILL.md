---
name: Integration Patterns
description: Expertise in API design, database integration, and service connectivity. Activates when working with "API", "database", "webhook", "service", "integrate", "connect", or system architecture.
version: 1.0.0
---

# Integration Patterns Skill

## Overview

Design and implement robust integration patterns for connecting services, databases, and external systems. This skill encompasses RESTful and GraphQL API design, database connection management, event-driven architecture, webhook processing, retry strategies, and resilient service communication patterns.

## Core Competencies

### REST API Design

**Design Resource-Oriented APIs:**

Structure REST APIs following best practices with proper HTTP semantics:

```typescript
// src/api/users/users.controller.ts
import { Router, Request, Response, NextFunction } from 'express';
import { UserService } from './user.service';
import { validateRequest } from '../../middleware/validation';
import { authenticate } from '../../middleware/auth';
import { rateLimit } from '../../middleware/rate-limit';
import { CreateUserDto, UpdateUserDto, UserQueryDto } from './user.dto';

export class UsersController {
  public router = Router();

  constructor(private userService: UserService) {
    this.setupRoutes();
  }

  private setupRoutes(): void {
    // List users with pagination and filtering
    this.router.get(
      '/',
      authenticate,
      rateLimit({ windowMs: 60000, max: 100 }),
      validateRequest(UserQueryDto, 'query'),
      this.listUsers.bind(this)
    );

    // Get single user
    this.router.get(
      '/:id',
      authenticate,
      this.getUser.bind(this)
    );

    // Create user
    this.router.post(
      '/',
      rateLimit({ windowMs: 60000, max: 10 }),
      validateRequest(CreateUserDto, 'body'),
      this.createUser.bind(this)
    );

    // Update user (full update)
    this.router.put(
      '/:id',
      authenticate,
      validateRequest(UpdateUserDto, 'body'),
      this.updateUser.bind(this)
    );

    // Partial update
    this.router.patch(
      '/:id',
      authenticate,
      validateRequest(UpdateUserDto, 'body', { partial: true }),
      this.patchUser.bind(this)
    );

    // Delete user
    this.router.delete(
      '/:id',
      authenticate,
      this.deleteUser.bind(this)
    );
  }

  private async listUsers(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { page = 1, limit = 20, sort = 'createdAt', order = 'desc', search } = req.query;

      const result = await this.userService.findAll({
        page: Number(page),
        limit: Number(limit),
        sort: sort as string,
        order: order as 'asc' | 'desc',
        search: search as string,
      });

      res.status(200).json({
        data: result.users,
        pagination: {
          page: result.page,
          limit: result.limit,
          total: result.total,
          pages: Math.ceil(result.total / result.limit),
        },
        links: {
          self: `/api/users?page=${result.page}&limit=${result.limit}`,
          next: result.page < Math.ceil(result.total / result.limit)
            ? `/api/users?page=${result.page + 1}&limit=${result.limit}`
            : null,
          prev: result.page > 1
            ? `/api/users?page=${result.page - 1}&limit=${result.limit}`
            : null,
        },
      });
    } catch (error) {
      next(error);
    }
  }

  private async getUser(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const user = await this.userService.findById(req.params.id);

      if (!user) {
        res.status(404).json({
          error: 'Not Found',
          message: 'User not found',
          statusCode: 404,
        });
        return;
      }

      res.status(200).json({
        data: user,
        links: {
          self: `/api/users/${user.id}`,
          posts: `/api/users/${user.id}/posts`,
          comments: `/api/users/${user.id}/comments`,
        },
      });
    } catch (error) {
      next(error);
    }
  }

  private async createUser(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const user = await this.userService.create(req.body);

      res.status(201)
        .location(`/api/users/${user.id}`)
        .json({
          data: user,
          links: {
            self: `/api/users/${user.id}`,
          },
        });
    } catch (error) {
      next(error);
    }
  }

  private async updateUser(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const user = await this.userService.update(req.params.id, req.body);

      if (!user) {
        res.status(404).json({
          error: 'Not Found',
          message: 'User not found',
          statusCode: 404,
        });
        return;
      }

      res.status(200).json({
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }

  private async patchUser(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const user = await this.userService.patch(req.params.id, req.body);

      if (!user) {
        res.status(404).json({
          error: 'Not Found',
          message: 'User not found',
          statusCode: 404,
        });
        return;
      }

      res.status(200).json({
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }

  private async deleteUser(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const deleted = await this.userService.delete(req.params.id);

      if (!deleted) {
        res.status(404).json({
          error: 'Not Found',
          message: 'User not found',
          statusCode: 404,
        });
        return;
      }

      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}
```

**Implement Consistent Error Handling:**

Create standardized error responses across all endpoints:

```typescript
// src/middleware/error-handler.ts
import { Request, Response, NextFunction } from 'express';

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true,
    public errors?: Record<string, string[]>
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export function errorHandler(
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: err.message,
      statusCode: err.statusCode,
      errors: err.errors,
      path: req.path,
      method: req.method,
      timestamp: new Date().toISOString(),
    });
    return;
  }

  // Unhandled errors
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    statusCode: 500,
    message: process.env.NODE_ENV === 'development' ? err.message : 'An unexpected error occurred',
    path: req.path,
    method: req.method,
    timestamp: new Date().toISOString(),
  });
}
```

### GraphQL API Design

**Design Type-Safe GraphQL Schema:**

Implement GraphQL APIs with proper type definitions and resolvers:

```typescript
// src/graphql/schema.ts
import { gql } from 'apollo-server-express';

export const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    comments: [Comment!]!
    published: Boolean!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Comment {
    id: ID!
    content: String!
    author: User!
    post: Post!
    createdAt: DateTime!
  }

  type Query {
    user(id: ID!): User
    users(
      page: Int = 1
      limit: Int = 20
      search: String
    ): UserConnection!

    post(id: ID!): Post
    posts(
      page: Int = 1
      limit: Int = 20
      published: Boolean
    ): PostConnection!
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): Boolean!

    createPost(input: CreatePostInput!): Post!
    publishPost(id: ID!): Post!

    createComment(input: CreateCommentInput!): Comment!
  }

  type Subscription {
    postCreated: Post!
    commentAdded(postId: ID!): Comment!
  }

  input CreateUserInput {
    name: String!
    email: String!
    password: String!
  }

  input UpdateUserInput {
    name: String
    email: String
  }

  input CreatePostInput {
    title: String!
    content: String!
    published: Boolean = false
  }

  input CreateCommentInput {
    postId: ID!
    content: String!
  }

  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type UserEdge {
    node: User!
    cursor: String!
  }

  type PostConnection {
    edges: [PostEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type PostEdge {
    node: Post!
    cursor: String!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }

  scalar DateTime
`;

// src/graphql/resolvers.ts
import { UserService } from '../services/user.service';
import { PostService } from '../services/post.service';
import { CommentService } from '../services/comment.service';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

export const resolvers = {
  Query: {
    user: async (_parent: any, { id }: { id: string }, { services }: any) => {
      return services.user.findById(id);
    },

    users: async (_parent: any, args: any, { services }: any) => {
      const result = await services.user.findAll(args);
      return {
        edges: result.users.map((user: any) => ({
          node: user,
          cursor: Buffer.from(user.id).toString('base64'),
        })),
        pageInfo: {
          hasNextPage: result.page * result.limit < result.total,
          hasPreviousPage: result.page > 1,
          startCursor: result.users.length > 0
            ? Buffer.from(result.users[0].id).toString('base64')
            : null,
          endCursor: result.users.length > 0
            ? Buffer.from(result.users[result.users.length - 1].id).toString('base64')
            : null,
        },
        totalCount: result.total,
      };
    },

    post: async (_parent: any, { id }: { id: string }, { services }: any) => {
      return services.post.findById(id);
    },
  },

  Mutation: {
    createUser: async (_parent: any, { input }: any, { services }: any) => {
      return services.user.create(input);
    },

    createPost: async (_parent: any, { input }: any, { services, user }: any) => {
      if (!user) {
        throw new Error('Authentication required');
      }

      const post = await services.post.create({
        ...input,
        authorId: user.id,
      });

      pubsub.publish('POST_CREATED', { postCreated: post });

      return post;
    },

    createComment: async (_parent: any, { input }: any, { services, user }: any) => {
      if (!user) {
        throw new Error('Authentication required');
      }

      const comment = await services.comment.create({
        ...input,
        authorId: user.id,
      });

      pubsub.publish(`COMMENT_ADDED_${input.postId}`, { commentAdded: comment });

      return comment;
    },
  },

  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator(['POST_CREATED']),
    },

    commentAdded: {
      subscribe: (_parent: any, { postId }: { postId: string }) =>
        pubsub.asyncIterator([`COMMENT_ADDED_${postId}`]),
    },
  },

  User: {
    posts: async (user: any, _args: any, { services }: any) => {
      return services.post.findByAuthorId(user.id);
    },
  },

  Post: {
    author: async (post: any, _args: any, { services }: any) => {
      return services.user.findById(post.authorId);
    },

    comments: async (post: any, _args: any, { services }: any) => {
      return services.comment.findByPostId(post.id);
    },
  },

  Comment: {
    author: async (comment: any, _args: any, { services }: any) => {
      return services.user.findById(comment.authorId);
    },

    post: async (comment: any, _args: any, { services }: any) => {
      return services.post.findById(comment.postId);
    },
  },
};
```

### Database Integration

**Implement Connection Pooling:**

Configure efficient database connection management:

```typescript
// src/database/connection.ts
import { Pool, PoolConfig } from 'pg';
import { createPool as createMySQLPool, PoolOptions } from 'mysql2/promise';

export class DatabaseConnection {
  private static pgPool: Pool;
  private static mysqlPool: any;

  static initializePostgres(config: PoolConfig): Pool {
    this.pgPool = new Pool({
      host: config.host || process.env.DB_HOST,
      port: config.port || Number(process.env.DB_PORT) || 5432,
      database: config.database || process.env.DB_NAME,
      user: config.user || process.env.DB_USER,
      password: config.password || process.env.DB_PASSWORD,
      max: 20, // Maximum pool size
      min: 5, // Minimum pool size
      idleTimeoutMillis: 30000, // Close idle clients after 30s
      connectionTimeoutMillis: 2000, // Timeout connection attempts after 2s
      maxUses: 7500, // Close connections after 7500 uses
    });

    // Handle pool errors
    this.pgPool.on('error', (err) => {
      console.error('Unexpected database error:', err);
    });

    return this.pgPool;
  }

  static initializeMySQL(config: PoolOptions): any {
    this.mysqlPool = createMySQLPool({
      host: config.host || process.env.DB_HOST,
      port: config.port || Number(process.env.DB_PORT) || 3306,
      database: config.database || process.env.DB_NAME,
      user: config.user || process.env.DB_USER,
      password: config.password || process.env.DB_PASSWORD,
      connectionLimit: 20,
      queueLimit: 0,
      waitForConnections: true,
      enableKeepAlive: true,
      keepAliveInitialDelay: 0,
    });

    return this.mysqlPool;
  }

  static getPostgresPool(): Pool {
    if (!this.pgPool) {
      throw new Error('PostgreSQL pool not initialized');
    }
    return this.pgPool;
  }

  static async closeAll(): Promise<void> {
    if (this.pgPool) {
      await this.pgPool.end();
    }
    if (this.mysqlPool) {
      await this.mysqlPool.end();
    }
  }
}

// src/repositories/user.repository.ts
import { Pool } from 'pg';
import { DatabaseConnection } from '../database/connection';

export class UserRepository {
  private pool: Pool;

  constructor() {
    this.pool = DatabaseConnection.getPostgresPool();
  }

  async findById(id: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE id = $1',
        [id]
      );
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  async findAll(options: any): Promise<any> {
    const client = await this.pool.connect();
    try {
      const offset = (options.page - 1) * options.limit;

      let query = 'SELECT * FROM users';
      let countQuery = 'SELECT COUNT(*) FROM users';
      const params: any[] = [];

      if (options.search) {
        const searchCondition = ' WHERE name ILIKE $1 OR email ILIKE $1';
        query += searchCondition;
        countQuery += searchCondition;
        params.push(`%${options.search}%`);
      }

      query += ` ORDER BY ${options.sort} ${options.order}`;
      query += ` LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
      params.push(options.limit, offset);

      const [users, count] = await Promise.all([
        client.query(query, params),
        client.query(countQuery, params.length > 0 ? [params[0]] : []),
      ]);

      return {
        users: users.rows,
        total: Number(count.rows[0].count),
        page: options.page,
        limit: options.limit,
      };
    } finally {
      client.release();
    }
  }

  async create(user: any): Promise<any> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');

      const result = await client.query(
        'INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING *',
        [user.name, user.email, user.passwordHash]
      );

      await client.query('COMMIT');
      return result.rows[0];
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

**Implement Query Optimization:**

Use prepared statements and indexes for performance:

```typescript
// src/repositories/optimized-queries.ts
export class OptimizedQueryRepository {
  async batchFindByIds(ids: string[]): Promise<any[]> {
    // Use IN clause for batch retrieval
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE id = ANY($1::uuid[])',
        [ids]
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  async findWithJoins(userId: string): Promise<any> {
    // Optimize joins with indexes
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT
          u.*,
          json_agg(
            json_build_object(
              'id', p.id,
              'title', p.title,
              'createdAt', p.created_at
            )
          ) FILTER (WHERE p.id IS NOT NULL) as posts
        FROM users u
        LEFT JOIN posts p ON p.author_id = u.id
        WHERE u.id = $1
        GROUP BY u.id
      `, [userId]);

      return result.rows[0];
    } finally {
      client.release();
    }
  }
}

// Create indexes for performance
// migrations/001_add_indexes.sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_comments_post_id ON comments(post_id);
```

### Event-Driven Architecture

**Implement Message Queue Integration:**

Use message queues for asynchronous processing:

```typescript
// src/queues/job.queue.ts
import Bull, { Queue, Job } from 'bull';
import Redis from 'ioredis';

export interface JobData {
  type: string;
  payload: any;
}

export class JobQueue {
  private queue: Queue<JobData>;
  private redis: Redis;

  constructor(queueName: string) {
    this.redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: Number(process.env.REDIS_PORT) || 6379,
      maxRetriesPerRequest: null,
      enableReadyCheck: false,
    });

    this.queue = new Bull<JobData>(queueName, {
      redis: this.redis,
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000,
        },
        removeOnComplete: 100,
        removeOnFail: 500,
      },
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.queue.on('error', (error) => {
      console.error('Queue error:', error);
    });

    this.queue.on('failed', (job, error) => {
      console.error(`Job ${job.id} failed:`, error);
    });

    this.queue.on('completed', (job) => {
      console.log(`Job ${job.id} completed`);
    });
  }

  async addJob(data: JobData, options?: Bull.JobOptions): Promise<Job<JobData>> {
    return this.queue.add(data, options);
  }

  async process(concurrency: number, processor: (job: Job<JobData>) => Promise<any>): Promise<void> {
    this.queue.process(concurrency, processor);
  }

  async close(): Promise<void> {
    await this.queue.close();
    this.redis.disconnect();
  }
}

// src/workers/email.worker.ts
import { JobQueue } from '../queues/job.queue';
import { EmailService } from '../services/email.service';

export class EmailWorker {
  private queue: JobQueue;
  private emailService: EmailService;

  constructor() {
    this.queue = new JobQueue('email');
    this.emailService = new EmailService();
    this.start();
  }

  private start(): void {
    this.queue.process(5, async (job) => {
      const { type, payload } = job.data;

      switch (type) {
        case 'welcome':
          await this.emailService.sendWelcomeEmail(payload);
          break;
        case 'password-reset':
          await this.emailService.sendPasswordResetEmail(payload);
          break;
        case 'notification':
          await this.emailService.sendNotification(payload);
          break;
        default:
          throw new Error(`Unknown email type: ${type}`);
      }
    });
  }
}
```

**Implement Webhook Processing:**

Handle incoming webhooks with retry logic:

```typescript
// src/webhooks/webhook.handler.ts
import { Request, Response } from 'express';
import crypto from 'crypto';

export class WebhookHandler {
  async handleStripeWebhook(req: Request, res: Response): Promise<void> {
    const signature = req.headers['stripe-signature'] as string;

    try {
      // Verify webhook signature
      this.verifyStripeSignature(req.rawBody, signature);

      const event = req.body;

      // Process event asynchronously
      await this.processStripeEvent(event);

      res.status(200).json({ received: true });
    } catch (error) {
      console.error('Webhook error:', error);
      res.status(400).json({ error: 'Webhook validation failed' });
    }
  }

  private verifyStripeSignature(payload: string, signature: string): void {
    const secret = process.env.STRIPE_WEBHOOK_SECRET!;
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');

    if (signature !== expectedSignature) {
      throw new Error('Invalid signature');
    }
  }

  private async processStripeEvent(event: any): Promise<void> {
    switch (event.type) {
      case 'payment_intent.succeeded':
        await this.handlePaymentSuccess(event.data.object);
        break;
      case 'payment_intent.failed':
        await this.handlePaymentFailure(event.data.object);
        break;
      case 'customer.subscription.updated':
        await this.handleSubscriptionUpdate(event.data.object);
        break;
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
  }
}
```

### Retry Strategies

**Implement Exponential Backoff:**

Handle transient failures with intelligent retry logic:

```typescript
// src/utils/retry.ts
export interface RetryOptions {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
  retryableErrors?: string[];
}

export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  let lastError: Error;
  let delay = options.initialDelay;

  for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error: any) {
      lastError = error;

      // Check if error is retryable
      if (options.retryableErrors &&
          !options.retryableErrors.includes(error.code)) {
        throw error;
      }

      // Don't retry on last attempt
      if (attempt === options.maxAttempts) {
        break;
      }

      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);

      await new Promise(resolve => setTimeout(resolve, delay));

      // Calculate next delay with exponential backoff
      delay = Math.min(
        delay * options.backoffMultiplier,
        options.maxDelay
      );
    }
  }

  throw lastError!;
}

// Usage example
async function fetchUserWithRetry(userId: string): Promise<User> {
  return retryWithBackoff(
    () => userService.findById(userId),
    {
      maxAttempts: 3,
      initialDelay: 1000,
      maxDelay: 10000,
      backoffMultiplier: 2,
      retryableErrors: ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND'],
    }
  );
}
```

## Related Resources

- **DevOps Practices Skill** - For deploying and managing integrated services
- **Performance Optimization Skill** - For monitoring API and database performance
- **Documentation Patterns Skill** - For API documentation with OpenAPI/Swagger
- **REST API Best Practices** - https://restfulapi.net
- **GraphQL Documentation** - https://graphql.org
- **Database Design Patterns** - https://www.postgresql.org/docs/
