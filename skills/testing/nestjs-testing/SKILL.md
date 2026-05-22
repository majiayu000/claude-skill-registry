---
name: nestjs-testing
description: Use when nestJS testing with unit tests, integration tests, and e2e tests. Use when building well-tested NestJS applications.
allowed-tools:
  - Bash
  - Read
---

# NestJS Testing

Master testing in NestJS for building reliable applications with
comprehensive unit, integration, and end-to-end tests.

## Unit Testing Setup

Creating and configuring test modules with TestingModule.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { getRepositoryToken } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

describe('UserService', () => {
  let service: UserService;
  let module: TestingModule;

  beforeEach(async () => {
    module = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            find: jest.fn(),
            findOne: jest.fn(),
            save: jest.fn(),
            create: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  afterEach(async () => {
    await module.close();
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should find all users', async () => {
    const users = [{ id: 1, name: 'John' }];
    jest.spyOn(service, 'findAll').mockResolvedValue(users);

    const result = await service.findAll();
    expect(result).toEqual(users);
    expect(service.findAll).toHaveBeenCalled();
  });
});

// Custom provider testing
describe('ConfigService', () => {
  let service: ConfigService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        {
          provide: ConfigService,
          useFactory: () => {
            return new ConfigService('.env.test');
          },
        },
      ],
    }).compile();

    service = module.get<ConfigService>(ConfigService);
  });

  it('should load config from test environment', () => {
    expect(service.get('NODE_ENV')).toBe('test');
  });
});
```

## Testing Controllers

Mocking services and testing request/response handling.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UserController } from './user.controller';
import { UserService } from './user.service';
import { CreateUserDto } from './dto/create-user.dto';
import { NotFoundException } from '@nestjs/common';

describe('UserController', () => {
  let controller: UserController;
  let service: UserService;

  const mockUserService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UserController],
      providers: [
        {
          provide: UserService,
          useValue: mockUserService,
        },
      ],
    }).compile();

    controller = module.get<UserController>(UserController);
    service = module.get<UserService>(UserService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const users = [
        { id: 1, name: 'John', email: 'john@example.com' },
        { id: 2, name: 'Jane', email: 'jane@example.com' },
      ];

      mockUserService.findAll.mockResolvedValue(users);

      const result = await controller.findAll();

      expect(result).toEqual(users);
      expect(service.findAll).toHaveBeenCalledTimes(1);
    });

    it('should return empty array when no users', async () => {
      mockUserService.findAll.mockResolvedValue([]);

      const result = await controller.findAll();

      expect(result).toEqual([]);
    });
  });

  describe('findOne', () => {
    it('should return a user by id', async () => {
      const user = { id: 1, name: 'John', email: 'john@example.com' };
      mockUserService.findOne.mockResolvedValue(user);

      const result = await controller.findOne('1');

      expect(result).toEqual(user);
      expect(service.findOne).toHaveBeenCalledWith(1);
    });

    it('should throw NotFoundException when user not found', async () => {
      mockUserService.findOne.mockRejectedValue(
        new NotFoundException('User not found'),
      );

      await expect(controller.findOne('999')).rejects.toThrow(
        NotFoundException,
      );
    });
  });

  describe('create', () => {
    it('should create a new user', async () => {
      const createUserDto: CreateUserDto = {
        name: 'John',
        email: 'john@example.com',
        password: 'password123',
      };

      const createdUser = { id: 1, ...createUserDto };
      mockUserService.create.mockResolvedValue(createdUser);

      const result = await controller.create(createUserDto);

      expect(result).toEqual(createdUser);
      expect(service.create).toHaveBeenCalledWith(createUserDto);
    });
  });

  describe('update', () => {
    it('should update a user', async () => {
      const updateDto = { name: 'Updated Name' };
      const updatedUser = { id: 1, name: 'Updated Name', email: 'john@example.com' };

      mockUserService.update.mockResolvedValue(updatedUser);

      const result = await controller.update('1', updateDto);

      expect(result).toEqual(updatedUser);
      expect(service.update).toHaveBeenCalledWith(1, updateDto);
    });
  });

  describe('remove', () => {
    it('should delete a user', async () => {
      mockUserService.remove.mockResolvedValue({ deleted: true });

      const result = await controller.remove('1');

      expect(result).toEqual({ deleted: true });
      expect(service.remove).toHaveBeenCalledWith(1);
    });
  });
});
```

## Testing Services

Mocking repositories and database operations.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';
import { getRepositoryToken } from '@nestjs/typeorm';
import { NotFoundException, ConflictException } from '@nestjs/common';

describe('UserService', () => {
  let service: UserService;
  let repository: Repository<User>;

  const mockRepository = {
    find: jest.fn(),
    findOne: jest.fn(),
    findOneBy: jest.fn(),
    save: jest.fn(),
    create: jest.fn(),
    delete: jest.fn(),
    update: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const users = [{ id: 1, name: 'John', email: 'john@example.com' }];
      mockRepository.find.mockResolvedValue(users);

      const result = await service.findAll();

      expect(result).toEqual(users);
      expect(repository.find).toHaveBeenCalled();
    });
  });

  describe('findOne', () => {
    it('should return a user', async () => {
      const user = { id: 1, name: 'John', email: 'john@example.com' };
      mockRepository.findOneBy.mockResolvedValue(user);

      const result = await service.findOne(1);

      expect(result).toEqual(user);
      expect(repository.findOneBy).toHaveBeenCalledWith({ id: 1 });
    });

    it('should throw NotFoundException when user not found', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create a new user', async () => {
      const createDto = {
        name: 'John',
        email: 'john@example.com',
        password: 'password123',
      };
      const user = { id: 1, ...createDto };

      mockRepository.findOneBy.mockResolvedValue(null); // Email not taken
      mockRepository.create.mockReturnValue(user);
      mockRepository.save.mockResolvedValue(user);

      const result = await service.create(createDto);

      expect(result).toEqual(user);
      expect(repository.create).toHaveBeenCalledWith(createDto);
      expect(repository.save).toHaveBeenCalledWith(user);
    });

    it('should throw ConflictException when email exists', async () => {
      const createDto = {
        name: 'John',
        email: 'john@example.com',
        password: 'password123',
      };

      mockRepository.findOneBy.mockResolvedValue({ id: 1 }); // Email exists

      await expect(service.create(createDto)).rejects.toThrow(
        ConflictException,
      );
    });
  });

  describe('update', () => {
    it('should update a user', async () => {
      const updateDto = { name: 'Updated Name' };
      const existingUser = { id: 1, name: 'John', email: 'john@example.com' };
      const updatedUser = { ...existingUser, ...updateDto };

      mockRepository.findOneBy.mockResolvedValue(existingUser);
      mockRepository.save.mockResolvedValue(updatedUser);

      const result = await service.update(1, updateDto);

      expect(result).toEqual(updatedUser);
      expect(repository.save).toHaveBeenCalled();
    });
  });

  describe('remove', () => {
    it('should delete a user', async () => {
      const user = { id: 1, name: 'John', email: 'john@example.com' };
      mockRepository.findOneBy.mockResolvedValue(user);
      mockRepository.delete.mockResolvedValue({ affected: 1 });

      await service.remove(1);

      expect(repository.delete).toHaveBeenCalledWith(1);
    });

    it('should throw NotFoundException when deleting non-existent user', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.remove(999)).rejects.toThrow(NotFoundException);
    });
  });
});
```

## Testing Providers

Factory providers and async providers.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { ConfigService } from '@nestjs/config';
import { DatabaseService } from './database.service';

describe('Factory Providers', () => {
  let databaseService: DatabaseService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        {
          provide: 'DATABASE_CONNECTION',
          useFactory: (config: ConfigService) => {
            return {
              host: config.get('DB_HOST'),
              port: config.get('DB_PORT'),
              database: config.get('DB_NAME'),
            };
          },
          inject: [ConfigService],
        },
        {
          provide: ConfigService,
          useValue: {
            get: jest.fn((key: string) => {
              const config = {
                DB_HOST: 'localhost',
                DB_PORT: 5432,
                DB_NAME: 'test_db',
              };
              return config[key];
            }),
          },
        },
        DatabaseService,
      ],
    }).compile();

    databaseService = module.get<DatabaseService>(DatabaseService);
  });

  it('should create database connection with correct config', () => {
    const connection = databaseService.getConnection();
    expect(connection.host).toBe('localhost');
    expect(connection.port).toBe(5432);
    expect(connection.database).toBe('test_db');
  });
});

// Async provider testing
describe('Async Providers', () => {
  let service: any;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        {
          provide: 'ASYNC_CONNECTION',
          useFactory: async () => {
            await new Promise((resolve) => setTimeout(resolve, 100));
            return { connected: true };
          },
        },
      ],
    }).compile();

    service = module.get('ASYNC_CONNECTION');
  });

  it('should resolve async provider', () => {
    expect(service.connected).toBe(true);
  });
});
```

## Testing Guards

Authentication and authorization guards.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { JwtAuthGuard } from './jwt-auth.guard';
import { JwtService } from '@nestjs/jwt';
import { ExecutionContext, UnauthorizedException } from '@nestjs/common';

describe('JwtAuthGuard', () => {
  let guard: JwtAuthGuard;
  let jwtService: JwtService;

  const mockJwtService = {
    verifyAsync: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        JwtAuthGuard,
        {
          provide: JwtService,
          useValue: mockJwtService,
        },
      ],
    }).compile();

    guard = module.get<JwtAuthGuard>(JwtAuthGuard);
    jwtService = module.get<JwtService>(JwtService);
  });

  it('should allow request with valid token', async () => {
    const mockContext = createMockExecutionContext({
      headers: { authorization: 'Bearer valid-token' },
    });

    mockJwtService.verifyAsync.mockResolvedValue({
      userId: 1,
      email: 'user@example.com',
    });

    const result = await guard.canActivate(mockContext);

    expect(result).toBe(true);
    expect(jwtService.verifyAsync).toHaveBeenCalledWith('valid-token', {
      secret: expect.any(String),
    });
  });

  it('should deny request without token', async () => {
    const mockContext = createMockExecutionContext({
      headers: {},
    });

    await expect(guard.canActivate(mockContext)).rejects.toThrow(
      UnauthorizedException,
    );
  });

  it('should deny request with invalid token', async () => {
    const mockContext = createMockExecutionContext({
      headers: { authorization: 'Bearer invalid-token' },
    });

    mockJwtService.verifyAsync.mockRejectedValue(new Error('Invalid token'));

    await expect(guard.canActivate(mockContext)).rejects.toThrow(
      UnauthorizedException,
    );
  });
});

// Helper function
function createMockExecutionContext(request: any): ExecutionContext {
  return {
    switchToHttp: () => ({
      getRequest: () => request,
      getResponse: () => ({}),
    }),
    getHandler: () => ({}),
    getClass: () => ({}),
  } as ExecutionContext;
}

// Testing RolesGuard
import { RolesGuard } from './roles.guard';
import { Reflector } from '@nestjs/core';
import { ForbiddenException } from '@nestjs/common';

describe('RolesGuard', () => {
  let guard: RolesGuard;
  let reflector: Reflector;

  beforeEach(() => {
    reflector = new Reflector();
    guard = new RolesGuard(reflector);
  });

  it('should allow access when user has required role', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue(['admin']);

    const mockContext = createMockExecutionContext({
      user: { id: 1, roles: ['admin'] },
    });

    const result = guard.canActivate(mockContext);

    expect(result).toBe(true);
  });

  it('should deny access when user lacks required role', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue(['admin']);

    const mockContext = createMockExecutionContext({
      user: { id: 1, roles: ['user'] },
    });

    expect(() => guard.canActivate(mockContext)).toThrow(ForbiddenException);
  });

  it('should allow access when no roles required', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue(undefined);

    const mockContext = createMockExecutionContext({
      user: { id: 1, roles: [] },
    });

    const result = guard.canActivate(mockContext);

    expect(result).toBe(true);
  });
});
```

## Testing Interceptors

Transformation and logging interceptors.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { TransformInterceptor } from './transform.interceptor';
import { ExecutionContext, CallHandler } from '@nestjs/common';
import { of } from 'rxjs';

describe('TransformInterceptor', () => {
  let interceptor: TransformInterceptor;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TransformInterceptor],
    }).compile();

    interceptor = module.get<TransformInterceptor>(TransformInterceptor);
  });

  it('should transform response data', (done) => {
    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => ({ url: '/test' }),
      }),
    } as ExecutionContext;

    const mockCallHandler: CallHandler = {
      handle: () => of({ name: 'Test', value: 123 }),
    };

    interceptor.intercept(mockContext, mockCallHandler).subscribe({
      next: (result) => {
        expect(result).toHaveProperty('data');
        expect(result.data).toEqual({ name: 'Test', value: 123 });
        expect(result).toHaveProperty('timestamp');
        expect(result).toHaveProperty('path');
        expect(result.path).toBe('/test');
        done();
      },
    });
  });
});

// Testing caching interceptor
import { CacheInterceptor } from './cache.interceptor';
import { CACHE_MANAGER } from '@nestjs/cache-manager';

describe('CacheInterceptor', () => {
  let interceptor: CacheInterceptor;
  let cacheManager: any;

  const mockCacheManager = {
    get: jest.fn(),
    set: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CacheInterceptor,
        {
          provide: CACHE_MANAGER,
          useValue: mockCacheManager,
        },
      ],
    }).compile();

    interceptor = module.get<CacheInterceptor>(CacheInterceptor);
    cacheManager = module.get(CACHE_MANAGER);
  });

  it('should return cached data if available', async (done) => {
    const cachedData = { cached: true };
    mockCacheManager.get.mockResolvedValue(cachedData);

    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => ({ method: 'GET', url: '/test' }),
      }),
    } as ExecutionContext;

    const mockCallHandler: CallHandler = {
      handle: () => of({ fresh: true }),
    };

    const result$ = await interceptor.intercept(mockContext, mockCallHandler);

    result$.subscribe({
      next: (result) => {
        expect(result).toEqual(cachedData);
        expect(cacheManager.get).toHaveBeenCalledWith('GET:/test');
        done();
      },
    });
  });

  it('should cache fresh data', (done) => {
    const freshData = { fresh: true };
    mockCacheManager.get.mockResolvedValue(null);

    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => ({ method: 'GET', url: '/test' }),
      }),
    } as ExecutionContext;

    const mockCallHandler: CallHandler = {
      handle: () => of(freshData),
    };

    interceptor.intercept(mockContext, mockCallHandler).then((result$) => {
      result$.subscribe({
        next: async (result) => {
          expect(result).toEqual(freshData);
          // Give time for cache to be set
          await new Promise((resolve) => setTimeout(resolve, 100));
          expect(cacheManager.set).toHaveBeenCalled();
          done();
        },
      });
    });
  });
});
```

## Testing Pipes

Validation and transformation pipes.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { ValidationPipe, BadRequestException } from '@nestjs/common';
import { ParseIntPipe } from '@nestjs/common';
import { ArgumentMetadata } from '@nestjs/common';

describe('ParseIntPipe', () => {
  let pipe: ParseIntPipe;

  beforeEach(() => {
    pipe = new ParseIntPipe();
  });

  it('should parse valid number string', async () => {
    const metadata: ArgumentMetadata = {
      type: 'param',
      metatype: Number,
      data: 'id',
    };

    const result = await pipe.transform('123', metadata);

    expect(result).toBe(123);
  });

  it('should throw error for invalid number string', async () => {
    const metadata: ArgumentMetadata = {
      type: 'param',
      metatype: Number,
      data: 'id',
    };

    await expect(pipe.transform('abc', metadata)).rejects.toThrow(
      BadRequestException,
    );
  });
});

// Custom validation pipe testing
import { CustomValidationPipe } from './custom-validation.pipe';
import { IsString, IsEmail, MinLength } from 'class-validator';

class CreateUserDto {
  @IsString()
  @MinLength(3)
  name: string;

  @IsEmail()
  email: string;
}

describe('CustomValidationPipe', () => {
  let pipe: CustomValidationPipe;

  beforeEach(() => {
    pipe = new CustomValidationPipe();
  });

  it('should validate valid DTO', async () => {
    const dto = {
      name: 'John Doe',
      email: 'john@example.com',
    };

    const metadata: ArgumentMetadata = {
      type: 'body',
      metatype: CreateUserDto,
    };

    const result = await pipe.transform(dto, metadata);

    expect(result).toEqual(dto);
  });

  it('should throw error for invalid DTO', async () => {
    const dto = {
      name: 'Jo', // Too short
      email: 'invalid-email',
    };

    const metadata: ArgumentMetadata = {
      type: 'body',
      metatype: CreateUserDto,
    };

    await expect(pipe.transform(dto, metadata)).rejects.toThrow(
      BadRequestException,
    );
  });
});
```

## Integration Testing / E2E Tests

Testing with supertest and real HTTP requests.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';
import { getRepositoryToken } from '@nestjs/typeorm';
import { User } from '../src/users/entities/user.entity';

describe('UserController (e2e)', () => {
  let app: INestApplication;
  let userRepository: any;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe());

    userRepository = moduleFixture.get(getRepositoryToken(User));

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  beforeEach(async () => {
    // Clean database before each test
    await userRepository.query('DELETE FROM users');
  });

  describe('/users (POST)', () => {
    it('should create a new user', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com',
          password: 'password123',
        })
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.name).toBe('John Doe');
          expect(res.body.email).toBe('john@example.com');
          expect(res.body).not.toHaveProperty('password');
        });
    });

    it('should return 400 for invalid data', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          name: 'Jo', // Too short
          email: 'invalid-email',
        })
        .expect(400);
    });
  });

  describe('/users (GET)', () => {
    it('should return all users', async () => {
      // Seed data
      await userRepository.save([
        { name: 'User 1', email: 'user1@example.com' },
        { name: 'User 2', email: 'user2@example.com' },
      ]);

      return request(app.getHttpServer())
        .get('/users')
        .expect(200)
        .expect((res) => {
          expect(res.body).toHaveLength(2);
          expect(res.body[0]).toHaveProperty('id');
          expect(res.body[0]).toHaveProperty('name');
        });
    });

    it('should return empty array when no users', () => {
      return request(app.getHttpServer())
        .get('/users')
        .expect(200)
        .expect([]);
    });
  });

  describe('/users/:id (GET)', () => {
    it('should return a user by id', async () => {
      const user = await userRepository.save({
        name: 'John Doe',
        email: 'john@example.com',
      });

      return request(app.getHttpServer())
        .get(`/users/${user.id}`)
        .expect(200)
        .expect((res) => {
          expect(res.body.id).toBe(user.id);
          expect(res.body.name).toBe('John Doe');
        });
    });

    it('should return 404 for non-existent user', () => {
      return request(app.getHttpServer()).get('/users/999').expect(404);
    });
  });

  describe('/users/:id (PATCH)', () => {
    it('should update a user', async () => {
      const user = await userRepository.save({
        name: 'John Doe',
        email: 'john@example.com',
      });

      return request(app.getHttpServer())
        .patch(`/users/${user.id}`)
        .send({ name: 'Jane Doe' })
        .expect(200)
        .expect((res) => {
          expect(res.body.name).toBe('Jane Doe');
        });
    });
  });

  describe('/users/:id (DELETE)', () => {
    it('should delete a user', async () => {
      const user = await userRepository.save({
        name: 'John Doe',
        email: 'john@example.com',
      });

      await request(app.getHttpServer())
        .delete(`/users/${user.id}`)
        .expect(200);

      // Verify deletion
      const deletedUser = await userRepository.findOne({ where: { id: user.id } });
      expect(deletedUser).toBeNull();
    });
  });
});
```

## Testing with Database

In-memory, Docker, and test containers.

```typescript
// In-memory SQLite for testing
import { Test, TestingModule } from '@nestjs/testing';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

describe('UserService with In-Memory DB', () => {
  let module: TestingModule;
  let service: UserService;

  beforeAll(async () => {
    module = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'sqlite',
          database: ':memory:',
          entities: [User],
          synchronize: true,
          dropSchema: true,
        }),
        TypeOrmModule.forFeature([User]),
      ],
      providers: [UserService],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  afterAll(async () => {
    await module.close();
  });

  it('should create and retrieve a user', async () => {
    const user = await service.create({
      name: 'John',
      email: 'john@example.com',
      password: 'password123',
    });

    expect(user.id).toBeDefined();

    const foundUser = await service.findOne(user.id);
    expect(foundUser.name).toBe('John');
  });
});

// Test with Docker container (using testcontainers)
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('UserService with PostgreSQL Container', () => {
  let container: StartedTestContainer;
  let module: TestingModule;

  beforeAll(async () => {
    // Start PostgreSQL container
    container = await new GenericContainer('postgres:15')
      .withEnvironment({
        POSTGRES_USER: 'test',
        POSTGRES_PASSWORD: 'test',
        POSTGRES_DB: 'testdb',
      })
      .withExposedPorts(5432)
      .start();

    const port = container.getMappedPort(5432);

    module = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'postgres',
          host: 'localhost',
          port,
          username: 'test',
          password: 'test',
          database: 'testdb',
          entities: [User],
          synchronize: true,
        }),
        TypeOrmModule.forFeature([User]),
      ],
      providers: [UserService],
    }).compile();
  }, 60000);

  afterAll(async () => {
    await module.close();
    await container.stop();
  });

  it('should work with real PostgreSQL', async () => {
    const service = module.get<UserService>(UserService);
    const user = await service.create({
      name: 'John',
      email: 'john@example.com',
      password: 'password123',
    });

    expect(user.id).toBeDefined();
  });
});
```

## Testing WebSockets

WebSocket gateway testing.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import { io, Socket } from 'socket.io-client';
import { ChatGateway } from './chat.gateway';

describe('ChatGateway (e2e)', () => {
  let app: INestApplication;
  let clientSocket: Socket;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      providers: [ChatGateway],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.listen(3001);
  });

  afterAll(async () => {
    await app.close();
  });

  beforeEach((done) => {
    clientSocket = io('http://localhost:3001');
    clientSocket.on('connect', done);
  });

  afterEach(() => {
    clientSocket.close();
  });

  it('should receive messages', (done) => {
    clientSocket.emit('message', { text: 'Hello World' });

    clientSocket.on('message', (data) => {
      expect(data.text).toBe('Hello World');
      done();
    });
  });

  it('should handle multiple clients', (done) => {
    const client2 = io('http://localhost:3001');

    client2.on('connect', () => {
      clientSocket.emit('message', { text: 'Broadcast' });

      client2.on('message', (data) => {
        expect(data.text).toBe('Broadcast');
        client2.close();
        done();
      });
    });
  });
});
```

## Testing GraphQL Resolvers

GraphQL testing with supertest.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { GraphQLModule } from '@nestjs/graphql';
import { ApolloDriver, ApolloDriverConfig } from '@nestjs/apollo';

describe('UserResolver (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [
        GraphQLModule.forRoot<ApolloDriverConfig>({
          driver: ApolloDriver,
          autoSchemaFile: true,
        }),
        UserModule,
      ],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('should query users', () => {
    return request(app.getHttpServer())
      .post('/graphql')
      .send({
        query: `
          query {
            users {
              id
              name
              email
            }
          }
        `,
      })
      .expect(200)
      .expect((res) => {
        expect(res.body.data.users).toBeDefined();
        expect(Array.isArray(res.body.data.users)).toBe(true);
      });
  });

  it('should create a user', () => {
    return request(app.getHttpServer())
      .post('/graphql')
      .send({
        query: `
          mutation {
            createUser(createUserInput: {
              name: "John Doe"
              email: "john@example.com"
            }) {
              id
              name
              email
            }
          }
        `,
      })
      .expect(200)
      .expect((res) => {
        expect(res.body.data.createUser).toHaveProperty('id');
        expect(res.body.data.createUser.name).toBe('John Doe');
      });
  });
});
```

## Mocking Strategies

jest.mock and custom providers.

```typescript
// Mock entire module
jest.mock('./user.service');
import { UserService } from './user.service';

describe('UserController with mocked service', () => {
  let controller: UserController;

  beforeEach(() => {
    controller = new UserController(new UserService());
  });

  it('should use mocked service', async () => {
    jest.spyOn(UserService.prototype, 'findAll').mockResolvedValue([]);
    const result = await controller.findAll();
    expect(result).toEqual([]);
  });
});

// Partial mocking
const mockUserService = {
  findAll: jest.fn(),
  findOne: jest.fn(),
} as unknown as UserService;

// Mock external dependencies
import axios from 'axios';
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ExternalApiService', () => {
  it('should fetch data from external API', async () => {
    mockedAxios.get.mockResolvedValue({ data: { result: 'success' } });

    const service = new ExternalApiService();
    const result = await service.fetchData();

    expect(result).toEqual({ result: 'success' });
    expect(mockedAxios.get).toHaveBeenCalledWith('https://api.example.com/data');
  });
});

// Custom mock factory
function createMockRepository() {
  return {
    find: jest.fn(),
    findOne: jest.fn(),
    save: jest.fn(),
    create: jest.fn((dto) => dto),
    delete: jest.fn(),
  };
}
```

## Test Fixtures and Factories

Creating reusable test data.

```typescript
// User factory
export class UserFactory {
  static create(overrides?: Partial<User>): User {
    return {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      password: 'hashed_password',
      createdAt: new Date(),
      updatedAt: new Date(),
      ...overrides,
    };
  }

  static createMany(count: number, overrides?: Partial<User>): User[] {
    return Array.from({ length: count }, (_, i) =>
      this.create({ id: i + 1, ...overrides }),
    );
  }
}

// Usage in tests
describe('UserService', () => {
  it('should find users', async () => {
    const users = UserFactory.createMany(3);
    mockRepository.find.mockResolvedValue(users);

    const result = await service.findAll();
    expect(result).toHaveLength(3);
  });
});

// Builder pattern for complex entities
class UserBuilder {
  private user: Partial<User> = {};

  withName(name: string): this {
    this.user.name = name;
    return this;
  }

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  asAdmin(): this {
    this.user.role = 'admin';
    return this;
  }

  build(): User {
    return {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password',
      role: 'user',
      createdAt: new Date(),
      updatedAt: new Date(),
      ...this.user,
    } as User;
  }
}

// Usage
const adminUser = new UserBuilder()
  .withName('Admin User')
  .withEmail('admin@example.com')
  .asAdmin()
  .build();
```

## Code Coverage and CI/CD

Testing configuration for coverage and automation.

```typescript
// jest.config.js
module.exports = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: 'src',
  testRegex: '.*\\.spec\\.ts$',
  transform: {
    '^.+\\.(t|j)s$': 'ts-jest',
  },
  collectCoverageFrom: [
    '**/*.(t|j)s',
    '!**/*.module.ts',
    '!**/node_modules/**',
    '!**/dist/**',
  ],
  coverageDirectory: '../coverage',
  testEnvironment: 'node',
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};

// package.json scripts
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:cov": "jest --coverage",
    "test:debug": "node --inspect-brk -r tsconfig-paths/register -r ts-node/register node_modules/.bin/jest --runInBand",
    "test:e2e": "jest --config ./test/jest-e2e.json"
  }
}

// GitHub Actions CI
// .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - run: npm ci
      - run: npm run test:cov

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

## When to Use This Skill

Use nestjs-testing when:

- Building production applications that require reliability
- Implementing new features that need verification
- Refactoring code safely with confidence
- Debugging complex issues through isolated tests
- Ensuring API contracts are maintained
- Validating business logic correctness
- Setting up CI/CD pipelines
- Documenting expected behavior through tests
- Preventing regressions in existing functionality
- Meeting code quality standards and coverage requirements

## NestJS Testing Best Practices

1. **Test isolation** - Each test should be independent and not rely on others
2. **AAA pattern** - Structure tests as Arrange, Act, Assert
3. **Mock external dependencies** - Mock databases, APIs, and third-party services
4. **Use factories** - Create test data with factories for consistency
5. **Test behavior, not implementation** - Focus on what the code does, not how
6. **Meaningful test names** - Describe what is being tested and expected outcome
7. **Setup and teardown** - Clean up resources after tests
8. **Coverage goals** - Aim for 80%+ coverage but focus on critical paths
9. **E2E for critical flows** - Test important user journeys end-to-end
10. **Run tests in CI/CD** - Automate testing in your deployment pipeline

## NestJS Testing Common Pitfalls

1. **Testing implementation details** - Tests break when refactoring
2. **Shared state** - Tests fail when run in different orders
3. **Not cleaning up** - Database pollution between tests
4. **Over-mocking** - Mocking everything reduces test value
5. **Flaky tests** - Tests that randomly fail due to timing issues
6. **Slow tests** - Not using in-memory databases for unit tests
7. **Missing edge cases** - Only testing happy paths
8. **Incomplete mocks** - Missing methods on mocked services
9. **Not testing errors** - Only testing successful scenarios
10. **Poor test organization** - Hard to find and maintain tests

## Resources

- [NestJS Testing Documentation](https://docs.nestjs.com/fundamentals/testing)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Supertest Documentation](https://github.com/visionmedia/supertest)
- [TestContainers Node](https://node.testcontainers.org/)
- [Testing TypeORM](https://typeorm.io/testing)
- [Socket.IO Client Testing](https://socket.io/docs/v4/client-api/)
- [Apollo Testing Utilities](https://www.apollographql.com/docs/apollo-server/testing/testing/)
- [Code Coverage with Jest](https://jestjs.io/docs/configuration#collectcoverage-boolean)
