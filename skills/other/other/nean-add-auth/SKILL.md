---
name: nean-add-auth
description: Add authentication to a NEAN project using Passport.js with JWT and optional OAuth.
argument-hint: "[--providers local,google,github] [--with-refresh-tokens]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add secure authentication to an existing NEAN project using Passport.js and JWT.

## Arguments
- `--providers <list>` — Comma-separated providers (default: `local`)
  - Options: `local`, `google`, `github`, `discord`
- `--with-refresh-tokens` — Enable refresh token rotation (recommended for production)

## What gets created

```
libs/api/auth/
├── src/
│   ├── auth.module.ts                # Auth module with guards
│   ├── auth.controller.ts            # Login, register, refresh endpoints
│   ├── auth.service.ts               # Auth logic
│   ├── strategies/
│   │   ├── jwt.strategy.ts           # JWT validation
│   │   ├── jwt-refresh.strategy.ts   # Refresh token (if enabled)
│   │   ├── local.strategy.ts         # Username/password
│   │   ├── google.strategy.ts        # (if selected)
│   │   └── github.strategy.ts        # (if selected)
│   ├── guards/
│   │   ├── jwt-auth.guard.ts         # Route protection
│   │   ├── local-auth.guard.ts       # Login guard
│   │   └── roles.guard.ts            # RBAC guard
│   ├── decorators/
│   │   ├── current-user.decorator.ts # Extract user from request
│   │   ├── public.decorator.ts       # Mark route as public
│   │   └── roles.decorator.ts        # Role requirements
│   └── index.ts

libs/api/database/src/entities/
├── user.entity.ts                    # User entity
└── refresh-token.entity.ts           # (if --with-refresh-tokens)

libs/shared/types/src/
├── auth.dto.ts                       # Login, register, token DTOs
└── user.dto.ts                       # User response DTO

apps/web/src/app/auth/
├── auth.routes.ts                    # Auth routing
├── login/                            # Login page
├── register/                         # Registration page
├── callback/                         # OAuth callback (if OAuth)
└── guards/
    └── auth.guard.ts                 # Angular route guard

libs/web/auth/
├── src/
│   ├── auth.service.ts               # Auth API calls
│   ├── auth.interceptor.ts           # Attach JWT to requests
│   ├── auth.store.ts                 # NgRx auth state
│   └── index.ts

.env.example                          # Updated with auth vars
```

## Environment variables required

```bash
# JWT
JWT_SECRET=                           # Generate with: openssl rand -base64 64
JWT_EXPIRES_IN=15m
JWT_REFRESH_SECRET=                   # If using refresh tokens
JWT_REFRESH_EXPIRES_IN=7d

# OAuth (per provider)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_CALLBACK_URL=http://localhost:3000/api/auth/google/callback

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_CALLBACK_URL=http://localhost:3000/api/auth/github/callback
```

## Workflow
1. Install dependencies: `@nestjs/passport`, `passport`, `passport-jwt`, `passport-local`, `bcrypt`
2. Create User entity with password hash
3. Create auth module with strategies
4. Create guards and decorators
5. Create auth controller with endpoints
6. Create Angular auth components
7. Create Angular auth interceptor and guard
8. Update env validation schema
9. Run tests to verify

## API Endpoints

| Method | Endpoint             | Description           | Auth |
|--------|----------------------|-----------------------|------|
| POST   | /api/auth/register   | Create new account    | No   |
| POST   | /api/auth/login      | Login with credentials| No   |
| POST   | /api/auth/refresh    | Refresh access token  | No*  |
| POST   | /api/auth/logout     | Invalidate tokens     | Yes  |
| GET    | /api/auth/me         | Get current user      | Yes  |
| GET    | /api/auth/google     | Start Google OAuth    | No   |
| GET    | /api/auth/google/callback | Google callback  | No   |

*Refresh endpoint uses refresh token in httpOnly cookie

## Protected routes
Apply `JwtAuthGuard` globally in `main.ts` or per-controller:

```typescript
// Global (with @Public() decorator for exceptions)
app.useGlobalGuards(new JwtAuthGuard());

// Per-controller
@UseGuards(JwtAuthGuard)
@Controller('users')
export class UsersController {}

// Per-route
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
@Delete(':id')
delete() {}
```

## Usage patterns

### NestJS Controller
```typescript
@Controller('protected')
@UseGuards(JwtAuthGuard)
export class ProtectedController {
  @Get('profile')
  getProfile(@CurrentUser() user: User) {
    return user;
  }
}
```

### Angular Component
```typescript
@Component({...})
export class ProfileComponent {
  private authStore = inject(AuthStore);
  
  user = this.authStore.user;
  isAuthenticated = this.authStore.isAuthenticated;
}
```

### Angular Route Guard
```typescript
export const authGuard: CanActivateFn = () => {
  const authStore = inject(AuthStore);
  const router = inject(Router);
  
  if (authStore.isAuthenticated()) {
    return true;
  }
  
  return router.createUrlTree(['/auth/login']);
};
```

## Output
Summarize: providers configured, environment variables needed, protected routes, components available.

## Reference
For templates and OAuth setup guides, see `reference/nean-add-auth-reference.md`
