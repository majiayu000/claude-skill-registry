---
name: NestJS Framework
version: 1.0.0
framework_versions:
  min: 8.0.0
  max: 11.x
  recommended: 10.4.0
compatible_agents:
  backend-developer: ">=3.0.0"
  tech-lead-orchestrator: ">=2.5.0"
description: Node.js/TypeScript backend framework with dependency injection and modular architecture
frameworks:
  - nestjs
languages:
  - typescript
  - javascript
category: backend
updated: 2025-10-22
---

# NestJS Framework Skill

## Quick Reference

**When to Use**: Building scalable Node.js/TypeScript backend applications with modular architecture

**Core Strengths**: Dependency injection, modular design, enterprise patterns, comprehensive testing

**Target Coverage**: Services ≥80%, Controllers ≥70%, E2E ≥60%, Overall ≥75%

## Essential Patterns

### Module Architecture

```typescript
// users/users.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([User]), AuthModule],
  controllers: [UserController],
  providers: [
    UserService,
    UserRepository,
    { provide: 'USER_REPOSITORY', useClass: UserRepository },
  ],
  exports: [UserService],
})
export class UsersModule {}
```

**Key Principles**:
- Clear module boundaries and responsibilities
- Export only what other modules need
- Import shared modules (AuthModule, DatabaseModule)
- Use token-based providers for abstraction

### Dependency Injection

```typescript
// users/services/user.service.ts
@Injectable()
export class UserService {
  constructor(
    @Inject('USER_REPOSITORY') private readonly userRepository: UserRepository,
    private readonly hashingService: HashingService,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async createUser(dto: CreateUserDto): Promise<User> {
    const hashedPassword = await this.hashingService.hash(dto.password);
    const user = await this.userRepository.create({
      ...dto,
      password: hashedPassword,
    });
    this.eventEmitter.emit('user.created', user);
    return user;
  }
}
```

**Best Practices**:
- Use constructor injection for all dependencies
- Inject interfaces/tokens, not concrete implementations
- Keep services focused on single responsibility
- Emit events for cross-cutting concerns

### DTO Validation

```typescript
// users/dto/create-user.dto.ts
export class CreateUserDto {
  @ApiProperty({ example: 'john@example.com' })
  @IsEmail({}, { message: 'Invalid email format' })
  email: string;

  @ApiProperty({ example: 'StrongP@ss123', minLength: 8 })
  @IsString()
  @MinLength(8)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/, {
    message: 'Password must contain uppercase, lowercase, number, symbol'
  })
  password: string;

  @ApiProperty({ example: 'John Doe', required: false })
  @IsOptional()
  @MaxLength(100)
  name?: string;
}
```

**Validation Rules**:
- All inputs validated with class-validator decorators
- API documentation via @ApiProperty
- Custom error messages for user clarity
- Optional fields with @IsOptional()

### Repository Pattern

```typescript
// users/repositories/user.repository.ts
@Injectable()
export class UserRepository {
  constructor(
    @InjectRepository(User) private readonly repository: Repository<User>
  ) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.repository.findOne({ where: { email } });
  }

  async findById(id: number): Promise<User> {
    const user = await this.repository.findOne({ where: { id } });
    if (!user) throw new NotFoundException('User not found');
    return user;
  }

  async create(data: Partial<User>): Promise<User> {
    const user = this.repository.create(data);
    return this.repository.save(user);
  }
}
```

**Repository Guidelines**:
- Encapsulate all database operations
- Throw domain-specific exceptions
- Use TypeORM query builder for complex queries
- Keep repositories focused on data access only

### Controller Best Practices

```typescript
// users/controllers/user.controller.ts
@ApiTags('users')
@Controller('users')
@UseInterceptors(ClassSerializerInterceptor)
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create new user' })
  @ApiResponse({ status: 201, type: UserResponseDto })
  @ApiResponse({ status: 400, description: 'Validation failed' })
  async create(
    @Body(ValidationPipe) dto: CreateUserDto
  ): Promise<UserResponseDto> {
    const user = await this.userService.create(dto);
    return plainToInstance(UserResponseDto, user);
  }

  @Get(':id')
  @UseGuards(JwtAuthGuard)
  @ApiParam({ name: 'id', type: 'number' })
  async findOne(
    @Param('id', ParseIntPipe) id: number
  ): Promise<UserResponseDto> {
    const user = await this.userService.findById(id);
    return plainToInstance(UserResponseDto, user);
  }
}
```

**Controller Checklist**:
- [ ] @ApiTags for logical grouping
- [ ] @ApiOperation for endpoint description
- [ ] @ApiResponse for status codes + types
- [ ] ValidationPipe for DTO validation
- [ ] Guards for authentication/authorization
- [ ] Transform responses with DTOs

### Authentication & Authorization

```typescript
// auth/guards/jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  handleRequest(err, user, info) {
    if (err || !user) {
      throw new UnauthorizedException('Invalid or expired token');
    }
    return user;
  }
}

// auth/guards/roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<Role[]>('roles', context.getHandler());
    if (!requiredRoles) return true;

    const request = context.switchToHttp().getRequest();
    const user = request.user;
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}

// Usage in controller
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
@Delete(':id')
async delete(@Param('id') id: number): Promise<void> {
  await this.userService.delete(id);
}
```

**Auth Patterns**:
- JWT strategy with Passport.js
- Role-based access control with custom decorators
- Guard composition for complex rules
- Secure password hashing (bcrypt, argon2)

### Exception Handling

```typescript
// common/filters/http-exception.filter.ts
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: ctx.getRequest().url,
      message: typeof exceptionResponse === 'string'
        ? exceptionResponse
        : (exceptionResponse as any).message,
    });
  }
}

// Usage in main.ts
app.useGlobalFilters(new HttpExceptionFilter());
```

**Error Strategy**:
- Global exception filter for consistency
- Domain-specific exceptions (UserNotFoundException)
- Include correlation IDs for debugging
- Log errors with appropriate severity

### Testing

```typescript
// users/services/user.service.spec.ts
describe('UserService', () => {
  let service: UserService;
  let repository: MockType<UserRepository>;
  let hashingService: MockType<HashingService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: 'USER_REPOSITORY',
          useFactory: mockRepository,
        },
        {
          provide: HashingService,
          useFactory: mockHashingService,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repository = module.get('USER_REPOSITORY');
    hashingService = module.get(HashingService);
  });

  describe('createUser', () => {
    it('should hash password and create user', async () => {
      const dto = { email: 'test@test.com', password: 'Pass123!' };
      const hashedPassword = 'hashed_password';

      hashingService.hash.mockResolvedValue(hashedPassword);
      repository.findByEmail.mockResolvedValue(null);
      repository.create.mockResolvedValue({ id: 1, ...dto, password: hashedPassword });

      const result = await service.createUser(dto);

      expect(hashingService.hash).toHaveBeenCalledWith(dto.password);
      expect(repository.create).toHaveBeenCalledWith({
        ...dto,
        password: hashedPassword,
      });
      expect(result.id).toBe(1);
    });

    it('should throw ConflictException if user exists', async () => {
      const dto = { email: 'test@test.com', password: 'Pass123!' };
      repository.findByEmail.mockResolvedValue({ id: 1 });

      await expect(service.createUser(dto)).rejects.toThrow(ConflictException);
    });
  });
});
```

**Test Strategy**:
- Unit tests for services (≥80% coverage)
- Integration tests for repositories
- E2E tests for critical workflows (≥60% coverage)
- Mock external dependencies
- Test error paths and edge cases

## Common Anti-Patterns

### ❌ Don't: Tight Coupling

```typescript
// Bad: Direct dependency on implementation
@Injectable()
export class UserService {
  async createUser(email: string, password: string) {
    const hashed = await bcrypt.hash(password, 10); // Tight coupling!
    // ...
  }
}
```

### ✅ Do: Abstraction

```typescript
// Good: Depend on abstraction
@Injectable()
export class UserService {
  constructor(private readonly hashingService: HashingService) {}

  async createUser(dto: CreateUserDto) {
    const hashed = await this.hashingService.hash(dto.password);
    // ...
  }
}
```

### ❌ Don't: No Input Validation

```typescript
// Bad: No validation, any type
@Post()
async create(@Body() body: any) {
  return this.service.create(body);
}
```

### ✅ Do: DTO Validation

```typescript
// Good: Strong typing + validation
@Post()
async create(@Body(ValidationPipe) dto: CreateUserDto): Promise<UserResponseDto> {
  return this.service.create(dto);
}
```

### ❌ Don't: Expose Sensitive Data

```typescript
// Bad: Returns password field!
@Get(':id')
async findOne(@Param('id') id: string) {
  return this.userService.findOne(id); // Contains password
}
```

### ✅ Do: Transform Responses

```typescript
// Good: Use response DTO with @Exclude()
@Get(':id')
@UseInterceptors(ClassSerializerInterceptor)
async findOne(@Param('id', ParseIntPipe) id: number): Promise<UserResponseDto> {
  const user = await this.userService.findById(id);
  return plainToInstance(UserResponseDto, user); // Excludes password
}
```

## Performance Patterns

### Caching

```typescript
@Injectable()
export class UserService {
  constructor(
    @Inject(CACHE_MANAGER) private cacheManager: Cache,
    private userRepository: UserRepository,
  ) {}

  async findById(id: number): Promise<User> {
    const cacheKey = `user:${id}`;
    const cached = await this.cacheManager.get<User>(cacheKey);
    if (cached) return cached;

    const user = await this.userRepository.findById(id);
    await this.cacheManager.set(cacheKey, user, 3600); // 1 hour TTL
    return user;
  }
}
```

### Background Jobs

```typescript
// users/processors/email.processor.ts
@Processor('email')
export class EmailProcessor {
  @Process('welcome')
  async sendWelcomeEmail(job: Job<{ email: string; name: string }>) {
    const { email, name } = job.data;
    await this.emailService.sendWelcome(email, name);
  }
}

// In service
await this.emailQueue.add('welcome', { email: user.email, name: user.name });
```

### Query Optimization

```typescript
// Bad: N+1 query problem
const users = await this.repository.find();
for (const user of users) {
  user.orders = await this.orderRepository.findByUserId(user.id);
}

// Good: Use relations
const users = await this.repository.find({
  relations: ['orders'],
});
```

## Integration Checklist

- [ ] Module properly structured with clear boundaries
- [ ] All dependencies injected via constructor
- [ ] DTOs with class-validator decorators
- [ ] Repository pattern for data access
- [ ] Guards for authentication/authorization
- [ ] Exception filters for consistent errors
- [ ] OpenAPI/Swagger documentation
- [ ] Unit tests ≥80% coverage
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical paths
- [ ] Caching for frequently accessed data
- [ ] Background jobs for async operations
- [ ] Health check endpoint

## Quick Commands

```bash
# Generate resources
nest g module users
nest g controller users
nest g service users

# Generate complete CRUD
nest g resource users

# Run tests
npm run test           # Unit tests
npm run test:e2e       # E2E tests
npm run test:cov       # Coverage report

# Build and run
npm run build
npm run start:dev      # Watch mode
npm run start:prod     # Production
```

## See Also

- [REFERENCE.md](./REFERENCE.md) - Comprehensive guide with microservices, GraphQL, advanced patterns
- [templates/](./templates/) - Code generation templates
- [examples/](./examples/) - Real-world implementation examples
