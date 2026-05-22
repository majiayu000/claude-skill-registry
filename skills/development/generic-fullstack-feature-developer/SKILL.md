---
name: generic-fullstack-feature-developer
description: Guide feature development for full-stack applications with architecture focus. Covers Next.js App Router patterns, NestJS backend services, database models, data workflows, and seamless integration. Use when adding new features, refactoring existing code, or planning major changes.
---

# Fullstack Feature Developer

Guide feature development for Next.js/NestJS full-stack applications.

**Extends:** [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Read base skill for development workflow, decision frameworks, data flow patterns, and error handling.

## Full-Stack Data Flow

```
User Action → Event Handler → API Call → NestJS Controller
                                              ↓
UI Update ← Response ← Service ← Prisma ← Database
```

### Request/Response Cycle

```typescript
// Frontend: Call API
const response = await fetch('/api/users', {
  method: 'POST',
  body: JSON.stringify(userData),
});

// Backend: Handle request
@Post()
@UseGuards(JwtAuthGuard)
async createUser(@Body() dto: CreateUserDto) {
  return this.userService.create(dto);
}
```

## Next.js App Router Patterns

### File Conventions

| File          | Purpose                                |
| ------------- | -------------------------------------- |
| `page.tsx`    | Route UI (server component by default) |
| `layout.tsx`  | Shared UI wrapper                      |
| `loading.tsx` | Suspense loading UI                    |
| `error.tsx`   | Error boundary                         |
| `route.ts`    | API endpoint                           |

### Server vs Client Components

```typescript
// Server Component (default) - can fetch data
export default async function Page() {
  const data = await getData(); // Direct DB/API call
  return <div>{data.title}</div>;
}

// Client Component - needs 'use client'
'use client';
export default function Interactive() {
  const [state, setState] = useState();
  return <button onClick={() => setState(...)}>Click</button>;
}
```

## NestJS Module Pattern

```
Module → Controller → Service → Prisma
```

### Adding a Feature Module

```typescript
// 1. Module definition
@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}

// 2. Controller with guards
@Controller("users")
@UseGuards(JwtAuthGuard)
export class UsersController {
  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}

// 3. Service with Prisma
@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  create(dto: CreateUserDto) {
    return this.prisma.user.create({ data: dto });
  }
}
```

## Prisma Workflow

### Schema Changes

```bash
# 1. Edit schema.prisma
# 2. Create migration
npx prisma migrate dev --name add_user_role

# 3. Regenerate client
npx prisma generate

# 4. Update services to use new fields
```

### Type-Safe Queries

```typescript
// ✓ Type-safe with generated types
const user = await this.prisma.user.findUnique({
  where: { id },
  include: { posts: true },
});

// ✗ Avoid raw SQL
await this.prisma.$queryRaw`SELECT * FROM users`; // No type safety
```

## Authentication Flow

```
Login Request → Validate Credentials → Generate JWT → Set Cookie
      ↓
Protected Route → JwtAuthGuard → Extract User → Inject to Controller
```

### Auth Integration Points

```typescript
// Frontend: Include credentials
fetch('/api/protected', { credentials: 'include' });

// Backend: Guard + decorator
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@CurrentUser() user: User) {
  return user;
}
```

## Feature Checklist (Fullstack)

### Before Starting

- [ ] Plan data model (Prisma schema)
- [ ] Define API contract (DTOs)
- [ ] Identify auth requirements

### During Development

- [ ] Create/update Prisma schema
- [ ] Run migrations
- [ ] Implement NestJS module (controller + service)
- [ ] Create frontend components
- [ ] Add loading/error states

### Before Completion

- [ ] Add DTO validation decorators
- [ ] Write backend unit tests
- [ ] Write E2E tests for API
- [ ] Verify TypeScript types match

## See Also

- [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Base methodology
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Quality requirements
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI patterns
