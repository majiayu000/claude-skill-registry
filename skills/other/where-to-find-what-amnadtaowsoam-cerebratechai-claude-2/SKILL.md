---
name: Where to Find What
description: A quick lookup guide for navigating a repository: where to find endpoints, business logic, models, tests, configs, docs, scripts, plus search patterns and commands
---

# Where to Find What

## Overview

Reference guide that tells you "where to find X" for common patterns in a codebase, such as API endpoints, database models, tests, configs. Helps AI and humans search quickly.

## Why This Matters

- **Fast lookup**: Know immediately which file to go to
- **No guessing**: Don't need to grep multiple times
- **Pattern recognition**: Understand the conventions of the repo
- **Consistent navigation**: Everyone finds things the same way

---

## Core Concepts

### 1. Code Categories

- HTTP layer: routes/controllers/middleware
- Domain layer: use-cases/services/entities/policies
- Infrastructure: DB clients/repos, queues, external API adapters
- Shared: types, utils, constants, logging/errors

### 2. Search Patterns

- Find by "entry points": `routes`, `controllers`, `handlers`, `index`, `main`
- Find by "contracts": `OpenAPI`, `schema`, `dto`, `types`, `events`
- Find by "dependencies": import paths, client constructors, env var names

### 3. Naming Conventions

- Follow suffixes (`*.service.ts`, `*.repository.ts`, `*.controller.ts`)
- Tests mirror source path
- Configs are at root/config following the same standard

### 4. Common Lookups

- "where are endpoints" → `src/api/routes` / `src/routes`
- "where are business rules" → `src/domain/*` (or `src/modules/*/domain` in monorepo)
- "where is DB schema" → `prisma/schema.prisma` / `migrations/` / `src/db/models`

### 5. Cross-References

- endpoint ↔ request/response types ↔ domain service ↔ repository ↔ migration
- event producer ↔ schema registry ↔ consumer handler ↔ DLQ runbook
- feature flag ↔ rollout plan ↔ dashboards/alerts

### 6. Test Locations

- Unit tests are near domain or mirror path in `tests/`
- Integration/e2e are separate folders to avoid mixing with unit
- Fixtures/mocks have clear positions (e.g., `tests/__fixtures__`, `tests/__mocks__`)

### 7. Config Locations

- Runtime env vars: `.env.example`
- App config: `config/` or `src/config/`
- Infra deploy: `Dockerfile`, `k8s/`, `.github/workflows/`, `terraform/`

### 8. Documentation Locations

- API: `docs/api/` or `docs/api.yaml`
- Architecture: `docs/architecture/`
- Runbooks: `docs/runbooks/`
- ADRs: `docs/adr/`

## Quick Start

```markdown
# Add a `WHERE.md` at repo root or `docs/`:
# - "Finding Code / Tests / Config / Docs" sections
# - Concrete path patterns + examples (not theory)
# - 5–10 copy/paste search commands for the repo
```

## Production Checklist

- [ ] Common lookups documented
- [ ] Naming conventions explained
- [ ] Search patterns provided
- [ ] Updated when structure changes
- [ ] Easy to scan/search

## Where to Find What Template

````markdown
# WHERE.md - Quick Lookup Guide

## 🔍 Finding Code

### API Endpoints
```
Want: REST endpoint for /users
Look: src/api/routes/users.ts
Pattern: src/api/routes/{resource}.ts
```

### Business Logic
```
Want: User creation logic
Look: src/domain/users/services/createUser.ts
Pattern: src/domain/{entity}/services/{action}.ts
```

### Database Models
```
Want: User schema
Look: src/infrastructure/db/models/user.ts
Pattern: src/infrastructure/db/models/{entity}.ts
```

### Database Migrations
```
Want: Migration files
Look: prisma/migrations/
Pattern: prisma/migrations/{timestamp}_{name}/
```

### Type Definitions
```
Want: API request/response types
Look: src/api/types/{resource}.ts

Want: Domain types
Look: src/domain/{entity}/types.ts
```

### External API Integrations
```
Want: Stripe integration
Look: src/infrastructure/stripe/

Want: Email service
Look: src/infrastructure/email/
```

## 🧪 Finding Tests

### Unit Tests
```
Source: src/domain/users/services/createUser.ts
Test: tests/domain/users/services/createUser.test.ts
Pattern: tests/{mirror of src path}.test.ts
```

### Integration Tests
```
Look: tests/integration/{feature}/
Pattern: tests/integration/{feature}/*.test.ts
```

### E2E Tests
```
Look: tests/e2e/
Pattern: tests/e2e/{flow}.spec.ts
```

## ⚙️ Finding Configuration

| Config Type | Location |
|-------------|----------|
| Environment vars | `.env.example` |
| App config | `config/` |
| TypeScript | `tsconfig.json` |
| Linting | `.eslintrc.js` |
| Testing | `jest.config.js` |
| Docker | `Dockerfile`, `docker-compose.yml` |
| CI/CD | `.github/workflows/` |

## 📚 Finding Documentation

| Doc Type | Location |
|----------|----------|
| API reference | `docs/api/` |
| Architecture | `docs/architecture/` |
| Runbooks | `docs/runbooks/` |
| ADRs | `docs/adr/` |

## 🔧 Finding Scripts

| Script | Location | Usage |
|--------|----------|-------|
| Dev server | `npm run dev` | Local development |
| Build | `npm run build` | Production build |
| Migrations | `npm run db:migrate` | Run migrations |
| Seed data | `npm run db:seed` | Populate test data |

## 🗂️ By File Type

| I need... | File pattern | Example |
|-----------|--------------|---------|
| Controller | `*Controller.ts` | `UsersController.ts` |
| Service | `*Service.ts` | `UserService.ts` |
| Repository | `*Repository.ts` | `UserRepository.ts` |
| Middleware | `*Middleware.ts` | `AuthMiddleware.ts` |
| Validator | `*Validator.ts` | `UserValidator.ts` |
| DTO | `*Dto.ts` | `CreateUserDto.ts` |
```
````

## Search Commands

```bash
# Find file by name
fd "UserService"

# Find definition
grep -r "class UserService" src/

# Find usage
grep -r "UserService" src/ --include="*.ts"

# Find tests for a file
fd "createUser.test" tests/
```

## Anti-patterns

1. **Inconsistent structure**: Similar files are in different places
2. **No pattern**: Must grep every time
3. **Hidden files**: Important but hard to find
4. **No documentation**: Only known by original person

## Integration Points

- IDE search configurations
- AI retrieval playbooks
- Onboarding materials
- Code review guides

## Further Reading

- [Project Structure Patterns](https://blog.logrocket.com/node-js-project-architecture-best-practices/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
