---
document_name: "backend-patterns.skill.md"
location: ".claude/skills/backend-patterns.skill.md"
codebook_id: "CB-SKILL-BACKPAT-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for backend architecture patterns"
skill_metadata:
  category: "development"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Backend framework knowledge"
    - "Design patterns"
category: "skills"
status: "active"
tags:
  - "skill"
  - "backend"
  - "architecture"
  - "patterns"
ai_parser_instructions: |
  This skill defines backend architectural patterns.
  Used by Backend Engineer agent.
---

# Backend Patterns Skill

=== PURPOSE ===

Procedures for implementing backend architectural patterns.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(backend-engineer) @ref(CB-AGENT-BACKEND-001) | Primary skill for architecture |

=== PATTERN: Layered Architecture ===

**Layers (top to bottom):**
```
┌─────────────────────────┐
│    Controllers/Routes   │  ← HTTP handling
├─────────────────────────┤
│       Services          │  ← Business logic
├─────────────────────────┤
│     Repositories        │  ← Data access
├─────────────────────────┤
│       Database          │  ← Persistence
└─────────────────────────┘
```

**Rules:**
- Each layer only calls the layer below
- Controllers handle HTTP, call services
- Services contain business logic, call repositories
- Repositories handle data access only

=== PATTERN: Service Layer ===

**Structure:**
```typescript
// services/user.service.ts
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    // Business logic here
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }

    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcome(user.email);

    return user;
  }
}
```

**Guidelines:**
- One service per domain entity/concept
- Services can call other services
- All business rules live in services
- Services are testable in isolation

=== PATTERN: Repository Pattern ===

**Interface:**
```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(options?: QueryOptions): Promise<T[]>;
  create(data: Partial<T>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}
```

**Implementation:**
```typescript
export class UserRepository implements Repository<User> {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    return this.db.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.db.user.findUnique({ where: { email } });
  }

  // ... other methods
}
```

=== PATTERN: Dependency Injection ===

**Manual DI:**
```typescript
// Bootstrap
const db = new Database();
const userRepository = new UserRepository(db);
const emailService = new EmailService();
const userService = new UserService(userRepository, emailService);
const userController = new UserController(userService);
```

**Container-based DI (example with tsyringe):**
```typescript
@injectable()
export class UserService {
  constructor(
    @inject('UserRepository') private userRepository: UserRepository,
    @inject('EmailService') private emailService: EmailService
  ) {}
}
```

=== PATTERN: Error Handling ===

**Custom Error Classes:**
```typescript
export class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public details?: unknown) {
    super('VALIDATION_ERROR', message, 400);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super('CONFLICT', message, 409);
  }
}
```

=== PATTERN: Middleware Chain ===

**Order (typical):**
```typescript
app.use(cors());              // 1. CORS
app.use(helmet());            // 2. Security headers
app.use(morgan('combined'));  // 3. Logging
app.use(express.json());      // 4. Body parsing
app.use(rateLimit());         // 5. Rate limiting
app.use(authenticate);        // 6. Authentication (where needed)
app.use('/api', routes);      // 7. Routes
app.use(errorHandler);        // 8. Error handling (last)
```

=== PATTERN: Background Jobs ===

**Job Queue Pattern:**
```typescript
// Define job
interface EmailJob {
  type: 'SEND_EMAIL';
  payload: {
    to: string;
    template: string;
    data: Record<string, unknown>;
  };
}

// Enqueue
await jobQueue.add({
  type: 'SEND_EMAIL',
  payload: { to: user.email, template: 'welcome', data: { name: user.name } }
});

// Process
jobQueue.process('SEND_EMAIL', async (job) => {
  await emailService.send(job.payload);
});
```

=== PATTERN: Caching ===

**Cache-Aside Pattern:**
```typescript
async function getUser(id: string): Promise<User> {
  const cacheKey = `user:${id}`;

  // Try cache first
  const cached = await cache.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Miss - fetch from DB
  const user = await userRepository.findById(id);
  if (!user) throw new NotFoundError('User');

  // Store in cache
  await cache.set(cacheKey, JSON.stringify(user), 'EX', 3600);

  return user;
}
```

**Cache Invalidation:**
```typescript
async function updateUser(id: string, data: UpdateUserDto): Promise<User> {
  const user = await userRepository.update(id, data);

  // Invalidate cache
  await cache.del(`user:${id}`);

  return user;
}
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(api-development) | API implementation |
| @skill(schema-design) | Data model alignment |
