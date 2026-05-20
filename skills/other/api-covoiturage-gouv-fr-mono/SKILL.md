---
name: api
description: Use when working on the Deno/TypeScript backend API — creating actions, repositories, service providers, or modifying routing. Covers ILOS framework patterns, decorators, SQL queries, and Docker stack.
---

# API Developer Skill

> **Read `api/README.md` first** for setup, commands, and configuration.

## ILOS Framework (IoC)

The API uses a custom IoC framework (ILOS) with Inversify for dependency injection.

### Key Decorators

| Decorator | Purpose |
|-----------|---------|
| `@handler()` | Defines action handlers with service, method, middlewares, API routes |
| `@serviceProvider()` | Decorates service providers with handlers, commands, validators |
| `@provider()` | Marks injectable service classes |
| `@middleware()` | Marks middleware classes |
| `@command()` | CLI commands with signature and options |

### Key Components

- **Kernel** (`api/src/pdc/proxy/Kernel.ts`): Registers all service providers, connections, and commands
- **Service Providers**: Each domain module is a service provider that registers actions and repositories
- **Actions**: Extend `Action` class, implement `handle(params, context)` method
- **Repositories**: Database access layer using PostgreSQL

## Service Provider Structure

Each service follows this pattern:

```
services/<name>/
├── <Name>ServiceProvider.ts   # Registers all components
├── actions/                   # Action handlers
├── repositories/              # Database access
├── contracts/                 # TypeScript interfaces
├── commands/                  # CLI commands (optional)
└── config/                    # Service configuration
```

## Action Pattern

```typescript
@handler({
  service: "acquisition",
  method: "create",
  middlewares: [
    ["validate", CreateJourneyParamsValidator],
    "scopeToSelf",
  ],
  apiRoute: {
    path: "/v3/journeys",
    method: "POST",
    rateLimiter: { max: 2000 },
  },
})
export class CreateJourneyAction extends Action {
  async handle(params: ParamsType, context: ContextType): Promise<ResultType> {
    // Implementation
  }
}
```

## Repository Pattern

Always use the `sql` template literal for parameterized queries:

```typescript
import { sql } from "@/lib/pg/sql.ts";

const result = await this.connection.getClient().query(sql`
  SELECT * FROM carpools WHERE id = ${id}
`);
```

No ORM is used. `DenoPostgresConnection.ts` is the current provider (replaces `LegacyPostgresConnection.ts`).

## API Routing

- **External REST**: `GET/POST/PUT/DELETE /v3/{service}/{action}`
- **Internal RPC**: `POST /rpc` with `{ "method": "service:action", "params": {...} }`

Routes defined in `api/src/pdc/proxy/HttpTransport.ts`.
External routes should be defined in the Action decorator.
Internal RPC calls are being migrated to shared providers in `api/src/pdc/providers`.

## Service Modules

Located in `api/src/pdc/services/`:

| Service | Purpose |
|---------|---------|
| `acquisition` | Trip data capture from operators |
| `auth` | Authentication (JWT, ProConnect, Dex) |
| `dashboard` | CRUD for users, operators, territories for `app-partners` |
| `export` | Data export functionality |
| `policy` | Carpooling campaigns |
| `operator` | Operator management |
| `territory` | Territory/jurisdiction management |
| `apdf` | APDF reporting |
| `cee` | Mobility tax incentive (CEE) |
| `honor` | PDF certificate generation |
| `observatory` | Public statistics APIs |
| `geo` | Geolocation services |
| `company` | Company lookup (INSEE API) |

## Shared Types

Domain interfaces in `shared/` directory — import with `@pdc/shared/{domain}`.
Being deprecated as the older frontend was removed in favor of app-partners.

## Docker Compose Overlays

- `docker-compose.base.yml` - Service definitions (no exposed ports)
- `docker-compose.dev.yml` - Exposes ports for localhost development (default `just dc`)
- `docker-compose.proxy.yml` - Adds Traefik for *.covoiturage.test domains
- `docker-compose.e2e.yml` - E2E test configuration (`just dc_e2e`)

Run `just add-hosts` to add domain aliases to /etc/hosts.

## Deno Configuration

`api/deno.jsonc`:
- Import aliases: `@/` maps to `./src/` (use Deno's _Organise Imports_ LSP feature)
- Legacy decorators enabled for Inversify
- Line width: 120 for formatting

## Development Notes

- NixOS users: Add `DOCKER_SOCK=/run/user/1000/docker.sock` to `api/.env`
- Use `just seed-local-users` for test accounts (requires `APP_ENV=local`)
- Keep test databases with `APP_POSTGRES_KEEP_TEST_DATABASES=true`, then clean with `just drop_test_databases`
- Pre-commit: Talisman for secret detection configured in `.talismanrc`. Run `pre-commit install` when hook not found.
