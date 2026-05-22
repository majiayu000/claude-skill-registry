---
name: backend-patterns
description: Apply backend architecture patterns to the user's project. Covers repository pattern, service layer, middleware, error handling, validation, and database patterns. Adapts to the detected stack.
allowed-tools: Read, Write, Grep, Glob
---

# Backend Patterns

Apply production-ready backend architecture patterns.

## Stack Detection

Check for: `package.json` (Node/Express/Fastify/Hono), `pom.xml` (Spring Boot), `pyproject.toml` (FastAPI/Django), `go.mod` (Go/Gin/Fiber)

## Universal Patterns (all stacks)

### Repository Pattern
Separate data access from business logic:

```typescript
// TypeScript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findAll(options: PaginationOptions): Promise<Page<User>>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User>;
  delete(id: string): Promise<void>;
}
```

```python
# Python
class UserRepository:
    async def find_by_id(self, id: str) -> User | None: ...
    async def find_all(self, options: PaginationOptions) -> Page[User]: ...
    async def create(self, data: CreateUserDto) -> User: ...
```

### Service Layer
Business logic lives in services, not controllers:

```typescript
// TypeScript
class UserService {
  constructor(private readonly userRepo: UserRepository) {}

  async createUser(dto: CreateUserDto): Promise<User> {
    // Business logic: validation, hashing, etc.
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) throw new ConflictError("Email already exists");

    const hashed = await bcrypt.hash(dto.password, 12);
    return this.userRepo.create({ ...dto, password: hashed });
  }
}
```

### Error Handling Middleware

```typescript
// TypeScript / Express
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof ValidationError) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: err.message } });
  }
  if (err instanceof NotFoundError) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: err.message } });
  }
  logger.error("Unhandled error", { error: err.message, stack: err.stack });
  res.status(500).json({ error: { code: "INTERNAL_ERROR", message: "Internal server error" } });
});
```

### Input Validation

```typescript
// TypeScript with Zod
const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(72),
  name: z.string().min(1).max(100),
});

// Python with Pydantic
class CreateUserDto(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str = Field(min_length=1, max_length=100)
```

## N+1 Query Prevention

```typescript
// ❌ N+1 problem
const users = await userRepo.findAll();
for (const user of users) {
  user.posts = await postRepo.findByUserId(user.id); // N queries!
}

// ✅ Join or batch
const users = await userRepo.findAllWithPosts(); // 1 query with JOIN
// or use DataLoader pattern for GraphQL
```

## Pagination Pattern

```typescript
interface PaginationOptions {
  page: number;   // 1-based
  limit: number;  // max 100
}

interface Page<T> {
  data: T[];
  meta: { total: number; page: number; limit: number; totalPages: number };
}
```

## Usage

```
/backend-patterns              # review and improve current backend
/backend-patterns repository   # add repository pattern
/backend-patterns service      # add service layer
/backend-patterns error        # add error handling
/backend-patterns validation   # add input validation
```
