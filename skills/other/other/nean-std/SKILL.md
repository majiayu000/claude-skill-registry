---
name: nean-std
description: Coding standards for NEAN apps in an Nx monorepo.
---

## Purpose

Ensure consistent, maintainable code. Complements stack, security, and NFR skills.

## Monorepo structure

```
apps/
├── api/                          # NestJS backend
│   └── src/
│       ├── app/                  # Root module, bootstrap
│       ├── modules/              # Feature modules
│       └── main.ts               # Entry point
└── web/                          # Angular frontend
    └── src/
        ├── app/                  # Root component, routing
        ├── environments/         # Environment configs
        └── main.ts               # Bootstrap

libs/
├── shared/
│   ├── types/                    # DTOs, interfaces, enums
│   ├── constants/                # Shared constants
│   └── utils/                    # Shared utilities
├── api/
│   ├── auth/                     # Auth module (guards, strategies)
│   ├── database/                 # TypeORM config, entities, migrations
│   └── common/                   # Interceptors, filters, pipes, decorators
└── web/
    ├── auth/                     # Auth components, guards, interceptors
    ├── ui/                       # Shared UI components
    └── data-access/              # API services, NgRx state
```

- Apps import from libs via `@myapp/` path aliases
- Libs can depend on other libs; enforce dependency constraints in `nx.json`
- Feature-specific components live under the feature folder in apps

## Key conventions

### Environment

- Never access `process.env` directly in app code; use ConfigService (NestJS) or environment files (Angular)
- Validate env variables at startup using class-validator

### DTOs and types

- Define DTOs in `libs/shared/types` for request/response contracts
- Use class-validator decorators for validation
- Use class-transformer for serialization
- Keep entities separate from DTOs; map between them

```typescript
// libs/shared/types/src/user.dto.ts
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}

export class UserResponseDto {
  id: string;
  email: string;
  createdAt: Date;
  // Never expose passwordHash
}
```

### NestJS modules

- One module per feature domain
- Keep modules focused; split if > 10 services
- Use barrel exports (`index.ts`) for public API
- Prefer constructor injection over property injection

```typescript
// Feature module structure
modules/users/
├── users.module.ts
├── users.controller.ts
├── users.service.ts
├── dto/
│   ├── create-user.dto.ts
│   └── update-user.dto.ts
└── __tests__/
    ├── users.controller.spec.ts
    └── users.service.spec.ts
```

### Angular components

- Use standalone components (Angular 18+)
- Prefer OnPush change detection
- Use signals where appropriate
- Keep components focused; extract logic into services

```typescript
// Component structure
@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule, PrimeNgModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `...`,
})
export class UserCardComponent {
  @Input({ required: true }) user!: User;
  @Output() edit = new EventEmitter<User>();
}
```

### API endpoints

- Follow REST conventions
- Consistent response envelope
- Pagination for list endpoints
- Rate limiting on auth/expensive endpoints
- OpenAPI decorators for documentation

```typescript
@Controller('users')
@ApiTags('users')
export class UsersController {
  @Get()
  @ApiOperation({ summary: 'List users' })
  @ApiPaginatedResponse(UserResponseDto)
  findAll(@Query() query: PaginationDto) {
    return this.usersService.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.usersService.findOne(id);
  }
}
```

### TypeORM

- Explicit entity definitions with decorators
- Indexes defined with comments explaining why
- Use migrations for schema changes; never `synchronize: true` in production
- Repository pattern via NestJS's `@InjectRepository`

```typescript
@Entity('users')
export class UserEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  @Index() // Used for login lookup
  email: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

### Naming

- Folders: `kebab-case`
- Angular components: `PascalCase` with `.component.ts` suffix
- NestJS classes: `PascalCase` with appropriate suffix (`.service.ts`, `.controller.ts`)
- DTOs: `PascalCase` with `Dto` suffix
- Entities: `PascalCase` with `Entity` suffix
- Interfaces: `PascalCase`, no `I` prefix
- Named exports for all; default exports discouraged

## Testing requirements

TDD is mandatory — see `/shared-tdd` for the red-green-refactor workflow and evidence requirements.

**Test command:** `npm run test`

### What to test

- Unit tests for: services, validation, business logic, utilities
- Integration tests for: controllers with mocked services, repository queries
- E2E tests (Playwright) for: critical user journeys only
- Aim for >80% coverage on libs, >60% on apps

### Test file conventions

| Source | Test |
|--------|------|
| `apps/api/src/modules/foo/foo.service.ts` | `apps/api/src/modules/foo/foo.service.spec.ts` |
| `apps/api/src/modules/foo/foo.controller.ts` | `apps/api/src/modules/foo/foo.controller.spec.ts` |
| `apps/web/src/app/features/bar/bar.component.ts` | `apps/web/src/app/features/bar/bar.component.spec.ts` |
| `libs/shared/types/src/lib/baz.dto.ts` | `libs/shared/types/src/lib/baz.dto.spec.ts` |

## Output

For significant code changes, briefly note:

- Any deviation from these standards and why

## Reference

For detailed patterns and examples, see `reference/nean-std-reference.md`
