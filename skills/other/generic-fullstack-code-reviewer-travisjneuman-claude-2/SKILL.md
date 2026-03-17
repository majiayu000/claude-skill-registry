---
name: generic-fullstack-code-reviewer
description: Review full-stack code for bugs, security vulnerabilities, performance issues, accessibility gaps, and CLAUDE.md compliance. Enforces TypeScript strict mode, input validation, GPU-accelerated animations, and design system consistency. Use when completing features, before commits, or reviewing pull requests.
---

# Fullstack Code Reviewer

Review Next.js/NestJS code against production quality standards.

**Extends:** [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Read base skill for full code review methodology, P0/P1/P2 priority system, and judgment calls.

## Pre-Commit Commands

```bash
# Frontend
npm run build        # Next.js build
npm run lint         # ESLint

# Backend
npm run test         # NestJS tests
npm run type-check   # TypeScript
```

## Fullstack-Specific Checks

### Backend (NestJS)

**Authentication & Authorization:**

```typescript
// Protected routes MUST have auth guard
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@CurrentUser() user: User) {
  return this.userService.findById(user.id);
}
```

**Input Validation (DTOs):**

```typescript
// All inputs validated via class-validator
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

**Database Safety:**

```typescript
// Use Prisma, never raw SQL
// ✓ Good
await this.prisma.user.findUnique({ where: { id } });

// ✗ Bad
await this.prisma.$queryRaw`SELECT * FROM users WHERE id = ${id}`;
```

### Frontend (Next.js)

**Server vs Client Components:**

```typescript
// Default: Server Component (can fetch data, no hooks)
export default async function Page() {
  const data = await getData();
  return <div>{data}</div>;
}

// Client: Interactive (hooks, event handlers)
'use client';
export default function Interactive() {
  const [state, setState] = useState();
  return <button onClick={() => setState(...)}>Click</button>;
}
```

**API Route Patterns:**

```typescript
// app/api/[route]/route.ts
export async function POST(request: Request) {
  const body = await request.json();
  // Validate body before processing
  return NextResponse.json({ success: true });
}
```

### Cross-Stack Consistency

**Shared Types:**

```typescript
// types/api.ts - Shared between frontend/backend
interface UserResponse {
  id: string;
  email: string;
  createdAt: string;
}
```

**API Contract:**

- Request DTOs match frontend payloads
- Response types match frontend expectations
- Error format consistent (status, message, errors[])

### Environment & Secrets

```bash
# .env (never committed)
DATABASE_URL=postgres://...
JWT_SECRET=...

# Check .env.example exists with placeholder values
# Verify .gitignore includes .env
```

## Prisma Checks

```bash
# After schema changes
npx prisma migrate dev --name description
npx prisma generate
```

- Migrations are reversible
- Types regenerated after schema changes
- Relations properly defined

## Testing Requirements

**Backend:**

- Unit tests for services
- E2E tests for API endpoints
- Mocked database for tests

**Frontend:**

- Component tests for interactivity
- API mocking for integration tests

## Quick Fullstack Checklist

- [ ] Auth guards on protected routes
- [ ] DTOs validate all inputs
- [ ] No raw SQL queries
- [ ] Shared types match
- [ ] .env not committed
- [ ] Prisma types current

## See Also

- [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Base methodology
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Full requirements
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI consistency
