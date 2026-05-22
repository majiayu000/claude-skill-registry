---
name: nestjs-dependency-injection
description: Use when nestJS dependency injection with providers, modules, and decorators. Use when building modular NestJS applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# NestJS Dependency Injection

Master NestJS dependency injection for building modular, testable
Node.js applications with proper service architecture, provider
patterns, and module organization.

## Table of Contents

- [Provider Patterns](#provider-patterns)
- [Module System](#module-system)
- [Injection Scopes](#injection-scopes)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [Resources](#resources)

## Provider Patterns

### Class Providers (Standard Pattern)

```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  private users: User[] = [];

  findAll(): User[] {
    return this.users;
  }

  findById(id: string): User | undefined {
    return this.users.find(user => user.id === id);
  }

  create(user: User): User {
    this.users.push(user);
    return user;
  }
}

// Module registration
@Module({
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}
```

### Value Providers

```typescript
import { Module } from '@nestjs/common';

// Simple value provider
const DATABASE_CONNECTION = {
  provide: 'DATABASE_CONNECTION',
  useValue: {
    host: 'localhost',
    port: 5432,
    database: 'mydb',
  },
};

// Configuration value provider
const APP_CONFIG = {
  provide: 'APP_CONFIG',
  useValue: {
    apiUrl: process.env.API_URL,
    timeout: 5000,
    retries: 3,
  },
};

@Module({
  providers: [DATABASE_CONNECTION, APP_CONFIG],
  exports: [DATABASE_CONNECTION, APP_CONFIG],
})
export class ConfigModule {}

// Usage in service
@Injectable()
export class ApiService {
  constructor(
    @Inject('APP_CONFIG') private config: AppConfig,
  ) {}

  async fetchData(): Promise<any> {
    const response = await fetch(this.config.apiUrl, {
      timeout: this.config.timeout,
    });
    return response.json();
  }
}
```

### Factory Providers

```typescript
import { Injectable, Module } from '@nestjs/common';

// Simple factory provider
const CONNECTION_FACTORY = {
  provide: 'DATABASE_CONNECTION',
  useFactory: () => {
    return createConnection({
      type: 'postgres',
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT),
      database: process.env.DB_NAME,
    });
  },
};

// Factory with dependencies
const CACHE_MANAGER = {
  provide: 'CACHE_MANAGER',
  useFactory: (config: ConfigService) => {
    return createCacheManager({
      store: config.get('CACHE_STORE'),
      ttl: config.get('CACHE_TTL'),
      max: config.get('CACHE_MAX_ITEMS'),
    });
  },
  inject: [ConfigService],
};

@Module({
  providers: [
    ConfigService,
    CONNECTION_FACTORY,
    CACHE_MANAGER,
  ],
  exports: ['DATABASE_CONNECTION', 'CACHE_MANAGER'],
})
export class DatabaseModule {}
```

### Async Providers with useFactory

```typescript
import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

const DATABASE_PROVIDER = {
  provide: 'DATABASE_CONNECTION',
  useFactory: async (config: ConfigService) => {
    const connection = await createConnection({
      type: 'postgres',
      host: config.get('DB_HOST'),
      port: config.get('DB_PORT'),
      username: config.get('DB_USER'),
      password: config.get('DB_PASSWORD'),
      database: config.get('DB_NAME'),
    });

    await connection.runMigrations();
    return connection;
  },
  inject: [ConfigService],
};

const REDIS_PROVIDER = {
  provide: 'REDIS_CLIENT',
  useFactory: async (config: ConfigService) => {
    const client = createClient({
      url: config.get('REDIS_URL'),
    });

    await client.connect();

    client.on('error', (err) => {
      console.error('Redis error:', err);
    });

    return client;
  },
  inject: [ConfigService],
};

@Module({
  providers: [DATABASE_PROVIDER, REDIS_PROVIDER],
  exports: ['DATABASE_CONNECTION', 'REDIS_CLIENT'],
})
export class DataModule {}
```

### Token-Based Injection with String Tokens

```typescript
import { Inject, Injectable, Module } from '@nestjs/common';

// Define string tokens as constants
export const LOGGER_TOKEN = 'LOGGER';
export const METRICS_TOKEN = 'METRICS';
export const API_CLIENT_TOKEN = 'API_CLIENT';

// Provider definitions
const LOGGER_PROVIDER = {
  provide: LOGGER_TOKEN,
  useFactory: () => {
    return createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: 'json',
    });
  },
};

const METRICS_PROVIDER = {
  provide: METRICS_TOKEN,
  useValue: createMetricsClient(),
};

@Module({
  providers: [LOGGER_PROVIDER, METRICS_PROVIDER],
  exports: [LOGGER_TOKEN, METRICS_TOKEN],
})
export class ObservabilityModule {}

// Usage in service
@Injectable()
export class UserService {
  constructor(
    @Inject(LOGGER_TOKEN) private logger: Logger,
    @Inject(METRICS_TOKEN) private metrics: MetricsClient,
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    this.logger.info('Creating user', { email: data.email });
    this.metrics.increment('user.created');

    const user = await this.repository.create(data);
    return user;
  }
}
```

### Token-Based Injection with Symbol Tokens

```typescript
import { Inject, Injectable, Module } from '@nestjs/common';

// Define symbol tokens for better type safety
export const DATABASE_CONNECTION = Symbol('DATABASE_CONNECTION');
export const CACHE_MANAGER = Symbol('CACHE_MANAGER');
export const EVENT_BUS = Symbol('EVENT_BUS');

// Provider with symbol token
const DB_PROVIDER = {
  provide: DATABASE_CONNECTION,
  useFactory: async () => {
    return await createDatabaseConnection();
  },
};

const CACHE_PROVIDER = {
  provide: CACHE_MANAGER,
  useClass: RedisCacheManager,
};

@Module({
  providers: [DB_PROVIDER, CACHE_PROVIDER],
  exports: [DATABASE_CONNECTION, CACHE_MANAGER],
})
export class InfrastructureModule {}

// Usage with symbol tokens
@Injectable()
export class ProductService {
  constructor(
    @Inject(DATABASE_CONNECTION) private db: Connection,
    @Inject(CACHE_MANAGER) private cache: CacheManager,
  ) {}

  async findById(id: string): Promise<Product> {
    const cached = await this.cache.get(`product:${id}`);
    if (cached) return cached;

    const product = await this.db
      .getRepository(Product)
      .findOne({ where: { id } });

    await this.cache.set(`product:${id}`, product, 3600);
    return product;
  }
}
```

### Optional Dependencies with @Optional()

```typescript
import { Injectable, Optional, Inject } from '@nestjs/common';

@Injectable()
export class NotificationService {
  constructor(
    @Optional()
    @Inject('EMAIL_SERVICE')
    private emailService?: EmailService,
    @Optional()
    @Inject('SMS_SERVICE')
    private smsService?: SmsService,
  ) {}

  async notify(user: User, message: string): Promise<void> {
    // Gracefully handle missing optional dependencies
    if (this.emailService) {
      await this.emailService.send(user.email, message);
    }

    if (this.smsService && user.phone) {
      await this.smsService.send(user.phone, message);
    }

    // Always have a fallback notification method
    await this.logNotification(user, message);
  }

  private async logNotification(
    user: User,
    message: string,
  ): Promise<void> {
    console.log(`Notification for ${user.id}: ${message}`);
  }
}

// Module with optional providers
@Module({
  providers: [
    NotificationService,
    // EMAIL_SERVICE might not be registered
    // SMS_SERVICE might not be registered
  ],
  exports: [NotificationService],
})
export class NotificationModule {}
```

### Property-Based Injection

```typescript
import { Injectable, Inject } from '@nestjs/common';

// Property-based injection (less preferred)
@Injectable()
export class PaymentService {
  @Inject('PAYMENT_GATEWAY')
  private paymentGateway: PaymentGateway;

  @Inject('FRAUD_DETECTOR')
  private fraudDetector: FraudDetector;

  async processPayment(
    amount: number,
    card: CardDetails,
  ): Promise<PaymentResult> {
    const isFraudulent = await this.fraudDetector.check(card);
    if (isFraudulent) {
      throw new FraudDetectedException();
    }

    return await this.paymentGateway.charge(amount, card);
  }
}

// Constructor-based injection (preferred)
@Injectable()
export class OrderService {
  constructor(
    @Inject('PAYMENT_SERVICE')
    private readonly paymentService: PaymentService,
    @Inject('INVENTORY_SERVICE')
    private readonly inventoryService: InventoryService,
  ) {}

  async createOrder(data: CreateOrderDto): Promise<Order> {
    await this.inventoryService.reserve(data.items);
    await this.paymentService.processPayment(
      data.total,
      data.card,
    );

    return await this.repository.create(data);
  }
}
```

### Class Provider with useClass

```typescript
import { Injectable, Module } from '@nestjs/common';

// Abstract interface
export abstract class LoggerService {
  abstract log(message: string): void;
  abstract error(message: string, trace: string): void;
}

// Concrete implementations
@Injectable()
export class ConsoleLoggerService extends LoggerService {
  log(message: string): void {
    console.log(message);
  }

  error(message: string, trace: string): void {
    console.error(message, trace);
  }
}

@Injectable()
export class FileLoggerService extends LoggerService {
  log(message: string): void {
    fs.appendFileSync('app.log', `${message}\n`);
  }

  error(message: string, trace: string): void {
    fs.appendFileSync('error.log', `${message}\n${trace}\n`);
  }
}

// Use different implementations based on environment
@Module({
  providers: [
    {
      provide: LoggerService,
      useClass:
        process.env.NODE_ENV === 'production'
          ? FileLoggerService
          : ConsoleLoggerService,
    },
  ],
  exports: [LoggerService],
})
export class LoggerModule {}

// Usage
@Injectable()
export class AppService {
  constructor(private readonly logger: LoggerService) {}

  doSomething(): void {
    this.logger.log('Operation completed');
  }
}
```

### Alias Providers (useExisting)

```typescript
import { Injectable, Module } from '@nestjs/common';

@Injectable()
export class UserService {
  findAll(): User[] {
    return [];
  }
}

// Create an alias for the service
@Module({
  providers: [
    UserService,
    {
      provide: 'IUserService',
      useExisting: UserService,
    },
    {
      provide: 'UserRepository',
      useExisting: UserService,
    },
  ],
  exports: [
    UserService,
    'IUserService',
    'UserRepository',
  ],
})
export class UserModule {}

// Can inject using any of the tokens
@Injectable()
export class ReportService {
  constructor(
    @Inject('IUserService') private userService: UserService,
  ) {}

  async generateReport(): Promise<Report> {
    const users = this.userService.findAll();
    return this.buildReport(users);
  }
}
```

## Module System

### Module Organization and Encapsulation

```typescript
import { Module } from '@nestjs/common';

// Feature module with proper encapsulation
@Module({
  imports: [DatabaseModule, CacheModule],
  providers: [
    UserService,
    UserRepository,
    UserValidator,
  ],
  controllers: [UserController],
  exports: [UserService], // Only export what's needed
})
export class UserModule {}

// Domain module grouping related features
@Module({
  imports: [
    UserModule,
    AuthModule,
    ProfileModule,
  ],
})
export class IdentityModule {}

// Application module
@Module({
  imports: [
    ConfigModule.forRoot(),
    IdentityModule,
    ProductModule,
    OrderModule,
  ],
})
export class AppModule {}
```

### Global Modules with @Global()

```typescript
import { Module, Global } from '@nestjs/common';

// Global module available everywhere
@Global()
@Module({
  providers: [
    {
      provide: 'LOGGER',
      useFactory: () => createLogger(),
    },
    {
      provide: 'CONFIG',
      useValue: loadConfiguration(),
    },
  ],
  exports: ['LOGGER', 'CONFIG'],
})
export class CoreModule {}

// Usage in any module without importing
@Injectable()
export class AnyService {
  constructor(
    @Inject('LOGGER') private logger: Logger,
    @Inject('CONFIG') private config: Config,
  ) {}
}

// Register global module once in AppModule
@Module({
  imports: [
    CoreModule, // Only import once
    FeatureModule1,
    FeatureModule2,
  ],
})
export class AppModule {}
```

### Dynamic Modules with forRoot

```typescript
import { Module, DynamicModule, Provider } from '@nestjs/common';

export interface DatabaseModuleOptions {
  host: string;
  port: number;
  username: string;
  password: string;
  database: string;
}

@Module({})
export class DatabaseModule {
  static forRoot(
    options: DatabaseModuleOptions,
  ): DynamicModule {
    const connectionProvider: Provider = {
      provide: 'DATABASE_CONNECTION',
      useFactory: async () => {
        return await createConnection(options);
      },
    };

    return {
      module: DatabaseModule,
      providers: [
        connectionProvider,
        DatabaseService,
      ],
      exports: [
        'DATABASE_CONNECTION',
        DatabaseService,
      ],
      global: true,
    };
  }
}

// Usage in AppModule
@Module({
  imports: [
    DatabaseModule.forRoot({
      host: 'localhost',
      port: 5432,
      username: 'admin',
      password: 'secret',
      database: 'myapp',
    }),
  ],
})
export class AppModule {}
```

### Dynamic Modules with forRootAsync

```typescript
import {
  Module,
  DynamicModule,
  Provider,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

export interface CacheModuleAsyncOptions {
  useFactory: (...args: any[]) => Promise<CacheOptions>;
  inject?: any[];
}

@Module({})
export class CacheModule {
  static forRootAsync(
    options: CacheModuleAsyncOptions,
  ): DynamicModule {
    const cacheOptionsProvider: Provider = {
      provide: 'CACHE_OPTIONS',
      useFactory: options.useFactory,
      inject: options.inject || [],
    };

    const cacheProvider: Provider = {
      provide: 'CACHE_MANAGER',
      useFactory: async (cacheOptions: CacheOptions) => {
        return await createCacheManager(cacheOptions);
      },
      inject: ['CACHE_OPTIONS'],
    };

    return {
      module: CacheModule,
      providers: [
        cacheOptionsProvider,
        cacheProvider,
        CacheService,
      ],
      exports: ['CACHE_MANAGER', CacheService],
      global: true,
    };
  }
}

// Usage with ConfigService
@Module({
  imports: [
    ConfigModule.forRoot(),
    CacheModule.forRootAsync({
      useFactory: async (config: ConfigService) => ({
        store: config.get('CACHE_STORE'),
        ttl: config.get('CACHE_TTL'),
        max: config.get('CACHE_MAX_ITEMS'),
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

### Module Re-exporting

```typescript
import { Module } from '@nestjs/common';

// Low-level infrastructure modules
@Module({
  providers: [DatabaseService],
  exports: [DatabaseService],
})
export class DatabaseModule {}

@Module({
  providers: [CacheService],
  exports: [CacheService],
})
export class CacheModule {}

@Module({
  providers: [QueueService],
  exports: [QueueService],
})
export class QueueModule {}

// Shared module that re-exports common services
@Module({
  imports: [
    DatabaseModule,
    CacheModule,
    QueueModule,
  ],
  exports: [
    DatabaseModule,
    CacheModule,
    QueueModule,
  ],
})
export class SharedModule {}

// Feature modules import SharedModule instead of individual modules
@Module({
  imports: [SharedModule],
  providers: [UserService],
  controllers: [UserController],
})
export class UserModule {}

@Module({
  imports: [SharedModule],
  providers: [ProductService],
  controllers: [ProductController],
})
export class ProductModule {}
```

### Circular Dependencies Handling

```typescript
import { Module, forwardRef } from '@nestjs/common';

// UserModule depends on AuthModule
@Module({
  imports: [forwardRef(() => AuthModule)],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}

// AuthModule depends on UserModule
@Module({
  imports: [forwardRef(() => UserModule)],
  providers: [AuthService],
  exports: [AuthService],
})
export class AuthModule {}

// Service-level circular dependency
@Injectable()
export class UserService {
  constructor(
    @Inject(forwardRef(() => AuthService))
    private authService: AuthService,
  ) {}
}

@Injectable()
export class AuthService {
  constructor(
    @Inject(forwardRef(() => UserService))
    private userService: UserService,
  ) {}
}
```

### Feature Modules with Lazy Loading

```typescript
import { Module } from '@nestjs/common';

// Admin feature module
@Module({
  imports: [SharedModule],
  providers: [
    AdminService,
    AdminGuard,
  ],
  controllers: [AdminController],
})
export class AdminModule {}

// Lazy load admin module only when needed
@Module({
  imports: [
    // Other modules loaded eagerly
    CoreModule,
    UserModule,
  ],
})
export class AppModule {}

// In a controller or service, load AdminModule dynamically
@Injectable()
export class AppService {
  constructor(private readonly lazyModuleLoader: LazyModuleLoader) {}

  async performAdminTask(): Promise<void> {
    const moduleRef = await this.lazyModuleLoader.load(
      () => AdminModule,
    );
    const adminService = moduleRef.get(AdminService);
    await adminService.doAdminWork();
  }
}
```

### Module Configuration Pattern

```typescript
import { Module, DynamicModule } from '@nestjs/common';

export interface EmailModuleOptions {
  from: string;
  host: string;
  port: number;
  secure: boolean;
}

@Module({})
export class EmailModule {
  static forRoot(
    options: EmailModuleOptions,
  ): DynamicModule {
    return {
      module: EmailModule,
      providers: [
        {
          provide: 'EMAIL_OPTIONS',
          useValue: options,
        },
        EmailService,
      ],
      exports: [EmailService],
    };
  }

  static forFeature(): DynamicModule {
    return {
      module: EmailModule,
      providers: [EmailTemplateService],
      exports: [EmailTemplateService],
    };
  }
}

// Root module configuration
@Module({
  imports: [
    EmailModule.forRoot({
      from: 'noreply@example.com',
      host: 'smtp.example.com',
      port: 587,
      secure: true,
    }),
  ],
})
export class AppModule {}

// Feature module usage
@Module({
  imports: [EmailModule.forFeature()],
  providers: [NotificationService],
})
export class NotificationModule {}
```

### Shared Module Pattern

```typescript
import { Module, Global } from '@nestjs/common';

// Shared utilities module
@Global()
@Module({
  providers: [
    DateService,
    StringService,
    ValidationService,
  ],
  exports: [
    DateService,
    StringService,
    ValidationService,
  ],
})
export class UtilsModule {}

// Shared data access module
@Module({
  providers: [
    DataSource,
    TransactionManager,
    UnitOfWork,
  ],
  exports: [
    DataSource,
    TransactionManager,
    UnitOfWork,
  ],
})
export class DataAccessModule {}

// Combine into SharedModule
@Module({
  imports: [
    UtilsModule,
    DataAccessModule,
  ],
  exports: [
    UtilsModule,
    DataAccessModule,
  ],
})
export class SharedModule {}
```

## Injection Scopes

### DEFAULT Scope (Singleton)

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Default scope - single instance shared across the app
@Injectable()
export class ConfigService {
  private config: Record<string, any>;

  constructor() {
    this.config = this.loadConfiguration();
  }

  get(key: string): any {
    return this.config[key];
  }

  private loadConfiguration(): Record<string, any> {
    // Loaded once when application starts
    return {
      apiUrl: process.env.API_URL,
      dbHost: process.env.DB_HOST,
    };
  }
}

// Singleton service with state
@Injectable()
export class CacheService {
  private cache = new Map<string, any>();

  set(key: string, value: any): void {
    this.cache.set(key, value);
  }

  get(key: string): any {
    return this.cache.get(key);
  }

  // State is shared across all requests
  clear(): void {
    this.cache.clear();
  }
}
```

### REQUEST Scope with Performance Implications

```typescript
import { Injectable, Scope, Inject } from '@nestjs/common';
import { REQUEST } from '@nestjs/core';
import { Request } from 'express';

// Request-scoped provider - new instance per request
@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {
  constructor(@Inject(REQUEST) private request: Request) {}

  getUserId(): string {
    return this.request.user?.id;
  }

  getTenantId(): string {
    return this.request.headers['x-tenant-id'] as string;
  }

  getTraceId(): string {
    return this.request.headers['x-trace-id'] as string;
  }
}

// Service that depends on request-scoped provider
@Injectable({ scope: Scope.REQUEST })
export class AuditService {
  constructor(
    private readonly context: RequestContextService,
  ) {}

  async logAction(action: string): Promise<void> {
    await this.repository.create({
      userId: this.context.getUserId(),
      tenantId: this.context.getTenantId(),
      action,
      timestamp: new Date(),
    });
  }
}

// Performance consideration - all consumers become request-scoped
@Injectable({ scope: Scope.REQUEST })
export class UserService {
  // This service is now created per request
  // because it depends on a request-scoped service
  constructor(
    private readonly audit: AuditService,
  ) {
    console.log('New UserService instance created');
  }

  async createUser(data: CreateUserDto): Promise<User> {
    const user = await this.repository.create(data);
    await this.audit.logAction('user.created');
    return user;
  }
}
```

### TRANSIENT Scope

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Transient scope - new instance every time it's injected
@Injectable({ scope: Scope.TRANSIENT })
export class UniqueIdGenerator {
  private readonly id: string;

  constructor() {
    this.id = Math.random().toString(36).substring(7);
    console.log(`New generator created with id: ${this.id}`);
  }

  generate(): string {
    return `${this.id}-${Date.now()}`;
  }
}

// Each injection point gets its own instance
@Injectable()
export class OrderService {
  constructor(
    private readonly idGen1: UniqueIdGenerator, // Instance 1
  ) {}
}

@Injectable()
export class InvoiceService {
  constructor(
    private readonly idGen2: UniqueIdGenerator, // Instance 2
  ) {}
}

// Transient for stateful operations
@Injectable({ scope: Scope.TRANSIENT })
export class QueryBuilder {
  private conditions: string[] = [];
  private params: any[] = [];

  where(condition: string, ...params: any[]): this {
    this.conditions.push(condition);
    this.params.push(...params);
    return this;
  }

  build(): { query: string; params: any[] } {
    return {
      query: `SELECT * FROM table WHERE ${this.conditions.join(' AND ')}`,
      params: this.params,
    };
  }
}
```

### Durable Providers

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Durable provider - survives across requests
@Injectable({ scope: Scope.DEFAULT, durable: true })
export class ConnectionPoolService {
  private pool: Pool;

  constructor() {
    this.pool = createPool({
      host: 'localhost',
      port: 5432,
      max: 20,
    });
  }

  getConnection(): Promise<Connection> {
    return this.pool.connect();
  }

  async onModuleDestroy(): Promise<void> {
    await this.pool.end();
  }
}

// Durable request-scoped provider
@Injectable({
  scope: Scope.REQUEST,
  durable: true,
})
export class RequestLoggerService {
  private logs: string[] = [];

  log(message: string): void {
    this.logs.push(message);
  }

  getLogs(): string[] {
    return this.logs;
  }
}
```

### Scope Inheritance

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Parent service with DEFAULT scope
@Injectable()
export class DatabaseService {
  query(sql: string): Promise<any> {
    return this.pool.query(sql);
  }
}

// Child service inherits scope from parent
@Injectable()
export class UserRepository {
  constructor(private readonly db: DatabaseService) {}

  findAll(): Promise<User[]> {
    return this.db.query('SELECT * FROM users');
  }
}

// Request-scoped parent
@Injectable({ scope: Scope.REQUEST })
export class RequestContext {
  constructor(@Inject(REQUEST) private request: Request) {}

  getTenantId(): string {
    return this.request.headers['x-tenant-id'] as string;
  }
}

// Child inherits REQUEST scope
@Injectable({ scope: Scope.REQUEST })
export class TenantService {
  constructor(
    private readonly context: RequestContext,
    private readonly db: DatabaseService, // Still singleton
  ) {}

  async getData(): Promise<any[]> {
    const tenantId = this.context.getTenantId();
    return this.db.query(
      `SELECT * FROM data WHERE tenant_id = '${tenantId}'`,
    );
  }
}
```

### Scope Configuration in Modules

```typescript
import { Module } from '@nestjs/common';

@Module({
  providers: [
    // Default scope (singleton)
    ConfigService,

    // Request scope
    {
      provide: 'REQUEST_LOGGER',
      scope: Scope.REQUEST,
      useClass: RequestLoggerService,
    },

    // Transient scope
    {
      provide: 'ID_GENERATOR',
      scope: Scope.TRANSIENT,
      useClass: IdGeneratorService,
    },
  ],
})
export class AppModule {}
```

## Advanced Patterns

### Custom Decorators for Injection

```typescript
import { Inject } from '@nestjs/common';

// Custom decorator for logger injection
export const InjectLogger = () => Inject('LOGGER');

// Custom decorator for repository injection
export function InjectRepository(
  entity: Function,
): ParameterDecorator {
  return Inject(`${entity.name}Repository`);
}

// Custom decorator with options
export function InjectCache(
  namespace?: string,
): ParameterDecorator {
  const token = namespace ? `CACHE:${namespace}` : 'CACHE';
  return Inject(token);
}

// Usage in services
@Injectable()
export class UserService {
  constructor(
    @InjectLogger() private logger: Logger,
    @InjectRepository(User) private repo: Repository<User>,
    @InjectCache('users') private cache: CacheManager,
  ) {}

  async findAll(): Promise<User[]> {
    this.logger.log('Finding all users');

    const cached = await this.cache.get('all');
    if (cached) return cached;

    const users = await this.repo.find();
    await this.cache.set('all', users, 300);
    return users;
  }
}

// Register providers with custom tokens
@Module({
  providers: [
    {
      provide: 'LOGGER',
      useFactory: () => createLogger(),
    },
    {
      provide: 'UserRepository',
      useClass: UserRepository,
    },
    {
      provide: 'CACHE:users',
      useFactory: () => createCacheManager('users'),
    },
  ],
})
export class UserModule {}
```

### Provider Arrays and Multi-Providers

```typescript
import { Module, Inject } from '@nestjs/common';

// Define token for array of providers
export const EVENT_HANDLERS = 'EVENT_HANDLERS';

// Multiple implementations of event handler
@Injectable()
export class UserEventHandler implements EventHandler {
  handle(event: Event): void {
    console.log('User event:', event);
  }
}

@Injectable()
export class AuditEventHandler implements EventHandler {
  handle(event: Event): void {
    console.log('Audit event:', event);
  }
}

@Injectable()
export class NotificationEventHandler implements EventHandler {
  handle(event: Event): void {
    console.log('Notification event:', event);
  }
}

// Module registering multiple providers
@Module({
  providers: [
    UserEventHandler,
    AuditEventHandler,
    NotificationEventHandler,
    {
      provide: EVENT_HANDLERS,
      useFactory: (
        userHandler: UserEventHandler,
        auditHandler: AuditEventHandler,
        notificationHandler: NotificationEventHandler,
      ) => [userHandler, auditHandler, notificationHandler],
      inject: [
        UserEventHandler,
        AuditEventHandler,
        NotificationEventHandler,
      ],
    },
  ],
  exports: [EVENT_HANDLERS],
})
export class EventModule {}

// Service using array of providers
@Injectable()
export class EventBus {
  constructor(
    @Inject(EVENT_HANDLERS)
    private handlers: EventHandler[],
  ) {}

  emit(event: Event): void {
    this.handlers.forEach((handler) => {
      handler.handle(event);
    });
  }
}
```

### Lazy Module Loading

```typescript
import {
  Injectable,
  LazyModuleLoader,
} from '@nestjs/common';

@Injectable()
export class ReportService {
  constructor(
    private readonly lazyModuleLoader: LazyModuleLoader,
  ) {}

  async generateComplexReport(): Promise<Report> {
    // Load heavy module only when needed
    const moduleRef = await this.lazyModuleLoader.load(
      () => import('./analytics/analytics.module')
        .then((m) => m.AnalyticsModule),
    );

    const analyticsService = moduleRef.get(AnalyticsService);
    const data = await analyticsService.analyze();

    return this.buildReport(data);
  }

  async exportToPdf(report: Report): Promise<Buffer> {
    // Load PDF module lazily
    const moduleRef = await this.lazyModuleLoader.load(
      () => import('./pdf/pdf.module')
        .then((m) => m.PdfModule),
    );

    const pdfService = moduleRef.get(PdfService);
    return await pdfService.generate(report);
  }
}
```

### Testing with Dependency Injection

```typescript
import { Test, TestingModule } from '@nestjs/testing';

describe('UserService', () => {
  let service: UserService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: 'UserRepository',
          useValue: {
            find: jest.fn(),
            findOne: jest.fn(),
            create: jest.fn(),
            save: jest.fn(),
          },
        },
        {
          provide: 'LOGGER',
          useValue: {
            log: jest.fn(),
            error: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repository = module.get('UserRepository');
  });

  it('should find all users', async () => {
    const users = [{ id: '1', name: 'John' }];
    jest.spyOn(repository, 'find').mockResolvedValue(users);

    const result = await service.findAll();

    expect(result).toEqual(users);
    expect(repository.find).toHaveBeenCalledTimes(1);
  });

  it('should create a user', async () => {
    const createDto = { name: 'Jane', email: 'jane@example.com' };
    const user = { id: '2', ...createDto };

    jest.spyOn(repository, 'create').mockReturnValue(user);
    jest.spyOn(repository, 'save').mockResolvedValue(user);

    const result = await service.create(createDto);

    expect(result).toEqual(user);
    expect(repository.create).toHaveBeenCalledWith(createDto);
    expect(repository.save).toHaveBeenCalledWith(user);
  });
});

// Integration testing with test database
describe('UserService (integration)', () => {
  let app: INestApplication;
  let service: UserService;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [
        DatabaseModule.forRoot({
          type: 'postgres',
          host: 'localhost',
          port: 5433,
          database: 'test',
        }),
        UserModule,
      ],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();

    service = moduleRef.get<UserService>(UserService);
  });

  afterAll(async () => {
    await app.close();
  });

  it('should persist user to database', async () => {
    const createDto = { name: 'Integration', email: 'test@test.com' };
    const user = await service.create(createDto);

    expect(user.id).toBeDefined();
    expect(user.name).toBe(createDto.name);

    const found = await service.findById(user.id);
    expect(found).toEqual(user);
  });
});
```

### ModuleRef for Dynamic Provider Resolution

```typescript
import { Injectable, ModuleRef } from '@nestjs/core';

@Injectable()
export class DynamicService {
  constructor(private readonly moduleRef: ModuleRef) {}

  async processWithStrategy(
    strategyName: string,
    data: any,
  ): Promise<any> {
    // Dynamically resolve provider at runtime
    const strategy = this.moduleRef.get(
      `${strategyName}Strategy`,
      { strict: false },
    );

    return await strategy.process(data);
  }

  async getServiceByTenant(tenantId: string): Promise<any> {
    // Get service instance dynamically
    const token = `TenantService:${tenantId}`;
    try {
      return this.moduleRef.get(token, { strict: false });
    } catch {
      // Fallback to default service
      return this.moduleRef.get('DefaultTenantService');
    }
  }
}

// Using ModuleRef with request-scoped providers
@Injectable({ scope: Scope.REQUEST })
export class ContextAwareService {
  constructor(private readonly moduleRef: ModuleRef) {}

  async getCurrentUser(): Promise<User> {
    // Get request-scoped context
    const context = await this.moduleRef.resolve(
      RequestContextService,
    );
    const userId = context.getUserId();

    const userService = this.moduleRef.get(UserService);
    return await userService.findById(userId);
  }
}
```

### Plugin Pattern with Dependency Injection

```typescript
import { Module, DynamicModule, Type } from '@nestjs/common';

export interface Plugin {
  name: string;
  initialize(): Promise<void>;
  execute(data: any): Promise<any>;
}

export interface PluginModuleOptions {
  plugins: Type<Plugin>[];
}

@Module({})
export class PluginModule {
  static forRoot(
    options: PluginModuleOptions,
  ): DynamicModule {
    const pluginProviders = options.plugins.map((plugin) => ({
      provide: plugin,
      useClass: plugin,
    }));

    const pluginRegistryProvider = {
      provide: 'PLUGIN_REGISTRY',
      useFactory: (...plugins: Plugin[]) => plugins,
      inject: options.plugins,
    };

    return {
      module: PluginModule,
      providers: [
        ...pluginProviders,
        pluginRegistryProvider,
        PluginExecutor,
      ],
      exports: [PluginExecutor],
    };
  }
}

// Plugin implementations
@Injectable()
export class ValidationPlugin implements Plugin {
  name = 'validation';

  async initialize(): Promise<void> {
    console.log('Validation plugin initialized');
  }

  async execute(data: any): Promise<any> {
    // Validate data
    return data;
  }
}

@Injectable()
export class TransformPlugin implements Plugin {
  name = 'transform';

  async initialize(): Promise<void> {
    console.log('Transform plugin initialized');
  }

  async execute(data: any): Promise<any> {
    // Transform data
    return data;
  }
}

// Plugin executor
@Injectable()
export class PluginExecutor {
  constructor(
    @Inject('PLUGIN_REGISTRY')
    private plugins: Plugin[],
  ) {}

  async executeAll(data: any): Promise<any> {
    let result = data;
    for (const plugin of this.plugins) {
      result = await plugin.execute(result);
    }
    return result;
  }
}

// Usage
@Module({
  imports: [
    PluginModule.forRoot({
      plugins: [ValidationPlugin, TransformPlugin],
    }),
  ],
})
export class AppModule {}
```

### Conditional Provider Registration

```typescript
import { Module, DynamicModule } from '@nestjs/common';

@Module({})
export class StorageModule {
  static forRoot(): DynamicModule {
    const providers = [];

    // Conditional provider based on environment
    if (process.env.STORAGE_TYPE === 's3') {
      providers.push({
        provide: 'STORAGE_SERVICE',
        useClass: S3StorageService,
      });
    } else if (process.env.STORAGE_TYPE === 'gcs') {
      providers.push({
        provide: 'STORAGE_SERVICE',
        useClass: GcsStorageService,
      });
    } else {
      providers.push({
        provide: 'STORAGE_SERVICE',
        useClass: LocalStorageService,
      });
    }

    // Conditional feature providers
    if (process.env.ENABLE_COMPRESSION === 'true') {
      providers.push(CompressionService);
    }

    if (process.env.ENABLE_ENCRYPTION === 'true') {
      providers.push(EncryptionService);
    }

    return {
      module: StorageModule,
      providers,
      exports: ['STORAGE_SERVICE'],
    };
  }
}
```

## Best Practices

1. **Use constructor injection over property injection**: Constructor
   injection makes dependencies explicit, ensures they're available
   when the class is instantiated, and works better with TypeScript's
   type system.

2. **Prefer class-based providers for services**: Class providers are
   more idiomatic in NestJS, provide better type safety, and integrate
   seamlessly with decorators like @Injectable().

3. **Use factory providers for complex initialization**: When providers
   need async initialization, depend on other services, or require
   conditional logic, factory providers offer the flexibility needed.

4. **Avoid circular dependencies with forwardRef**: While forwardRef()
   solves circular dependencies, it's better to restructure your
   modules to eliminate the circular reference entirely.

5. **Keep modules focused and cohesive**: Each module should represent
   a single feature or domain. This improves maintainability, makes
   testing easier, and enables better code organization.

6. **Use dynamic modules for configurable features**: When building
   reusable modules that need configuration, implement forRoot() and
   forRootAsync() methods to provide flexible initialization.

7. **Leverage REQUEST scope only when needed**: Request-scoped
   providers have performance overhead. Use them only when you truly
   need per-request state, like request context or tenant isolation.

8. **Use symbol tokens for better type safety**: Symbol tokens prevent
   naming conflicts and provide better IntelliSense support compared
   to string tokens.

9. **Export only what's needed from modules**: Keep module interfaces
   minimal by exporting only the providers that other modules need to
   use. This maintains encapsulation and reduces coupling.

10. **Test providers in isolation**: Write unit tests that mock
    dependencies to test providers in isolation. Use integration tests
    to verify the full dependency graph works correctly.

## Common Pitfalls

1. **Circular dependency errors**: Occurs when Module A imports Module
   B, and Module B imports Module A. Restructure your modules or use
   forwardRef() as a last resort.

2. **REQUEST scope performance overhead**: Request-scoped providers are
   created for every request, which adds memory and CPU overhead. All
   dependent providers also become request-scoped.

3. **Not handling async provider initialization**: Forgetting to use
   async/await in factory providers can lead to providers being
   injected before they're fully initialized.

4. **Overusing global modules**: Global modules are convenient but can
   lead to tight coupling. Use them sparingly for truly global
   services like logging and configuration.

5. **Missing provider exports in modules**: If a provider is not
   listed in the module's exports array, it won't be available to
   other modules that import it.

6. **Token name conflicts**: Using generic string tokens like 'config'
   or 'service' across multiple modules can cause conflicts. Use
   descriptive, namespaced tokens.

7. **Memory leaks with REQUEST scope**: Request-scoped providers that
   hold references to large objects or don't clean up resources can
   cause memory leaks over time.

8. **Not cleaning up resources in onModuleDestroy**: Providers that
   create connections, timers, or other resources should implement
   onModuleDestroy to clean up properly.

9. **Tight coupling between modules**: Importing too many modules or
   depending on internal implementation details creates tight coupling
   that makes refactoring difficult.

10. **Missing @Injectable() decorator**: Forgetting to add
    @Injectable() to a class that should be a provider results in
    runtime errors when NestJS tries to inject it.

## Resources

- [NestJS Dependency Injection](https://docs.nestjs.com/fundamentals/custom-providers)
- [NestJS Modules](https://docs.nestjs.com/modules)
- [NestJS Injection Scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- [NestJS Dynamic Modules](https://docs.nestjs.com/fundamentals/dynamic-modules)
- [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)
- [NestJS Circular Dependency](https://docs.nestjs.com/fundamentals/circular-dependency)
- [NestJS Module Reference](https://docs.nestjs.com/fundamentals/module-ref)
- [NestJS Lifecycle Events](https://docs.nestjs.com/fundamentals/lifecycle-events)
