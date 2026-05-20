---
name: nean-stack
description: Stack decisions for NEAN apps (NestJS, Angular, Nx monorepo). Reference before scaffolding or architecture work.
---

## Locked decisions

| Layer          | Decision                                                  |
| -------------- | --------------------------------------------------------- |
| Monorepo       | Nx with integrated monorepo                               |
| Frontend       | Angular 21+ (standalone, zoneless), TypeScript required   |
| UI Components  | PrimeNG 21+ + Tailwind CSS v4                             |
| State          | NgRx (signals-based where appropriate)                    |
| Backend        | NestJS 11+ with TypeScript                                |
| ORM            | TypeORM with PostgreSQL                                   |
| Validation     | class-validator + class-transformer                       |
| Shared Types   | `libs/shared/types` (DTOs, interfaces, enums)             |
| Auth           | Passport.js (JWT + Refresh tokens)                        |
| Authorization  | CASL (attribute-based access control)                     |
| API Docs       | Swagger/OpenAPI via @nestjs/swagger                       |
| Environments   | local → staging → production                              |
| Secrets        | `.env` files for dev; cloud provider secrets for prod     |
| Containers     | Docker for production; optional for development           |

## Project layout

```
<app-name>/
├── apps/
│   ├── api/                    # NestJS backend
│   │   └── src/
│   │       ├── app/            # Root module
│   │       ├── modules/        # Feature modules
│   │       └── main.ts         # Entry point
│   └── web/                    # Angular frontend
│       └── src/
│           ├── app/            # Root component + routing
│           └── main.ts         # Bootstrap
├── libs/
│   ├── shared/
│   │   └── types/              # DTOs, interfaces, enums (used by both)
│   ├── api/
│   │   ├── database/           # TypeORM config, entities
│   │   └── common/             # Interceptors, filters, pipes
│   └── web/                    # (added as needed for feature libs)
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.web
│   ├── docker-compose.yml
│   └── nginx.conf
├── nx.json
├── package.json
└── tsconfig.base.json
```

## When to add additional services

Only justified if:

- Long-running jobs exceed typical request timeouts
- WebSocket/persistent connections required at scale
- Separate scaling requirements for specific workloads
- Compliance requires service isolation
- Background job processing (consider Bull/BullMQ first)

Default: keep API in single NestJS application with modules.

## Reference

For versions, env setup, and deployment patterns, see `reference/nean-stack-reference.md`
