---
name: vendix-core
description: >
  Vendix monorepo patterns, workspace structure, and shared libraries.
  Trigger: When working with monorepo structure, shared libs, or cross-app code.
license: MIT
metadata:
  author: vendix
  version: "1.0"
---

## When to Use

Use this skill when:
- Creating or modifying shared libraries
- Working with monorepo workspace configuration
- Understanding the Vendix architecture
- Adding dependencies across apps

## Critical Patterns

### Pattern 1: Monorepo Structure

Vendix uses npm workspaces:

```
Vendix/
├── apps/
│   ├── frontend/          # Angular 20 app
│   └── backend/           # NestJS app
├── libs/
│   ├── shared/            # Shared utilities
│   ├── ui/                # UI components
│   └── types/             # TypeScript types
├── package.json           # Root package with workspaces
├── package-lock.json      # Root lockfile
└── docker-compose.yml     # Dev environment
```

### Pattern 2: Workspace Configuration

Root package.json defines workspaces:

```json
{
  "private": true,
  "workspaces": [
    "apps/*",
    "libs/*"
  ],
  "scripts": {
    "dev": "npm run start:dev -w apps/backend & npm run start -w apps/frontend",
    "build": "npm run build -w apps/backend && npm run build:prod -w apps/frontend",
    "install:all": "npm install -ws"
  }
}
```

### Pattern 3: Creating Shared Libraries

```bash
# Generate Angular library
cd apps/frontend
ng generate library libs/my-lib --prefix=vendix

# Or create manually in libs/
mkdir -p libs/my-lib/src/lib
```

### Pattern 4: Importing from Shared Libraries

```typescript
// In apps/frontend
import { MyService } from '@vendix/my-lib';

// In apps/backend
import { MyUtil } from '@vendix/shared';
```

### Pattern 5: Library Path Mapping

**apps/frontend/tsconfig.json**:
```json
{
  "compilerOptions": {
    "paths": {
      "@vendix/shared": ["../../libs/shared/src"],
      "@vendix/ui": ["../../libs/ui/src"],
      "@vendix/types": ["../../libs/types/src"]
    }
  }
}
```

**apps/backend/tsconfig.json**:
```json
{
  "compilerOptions": {
    "paths": {
      "@vendix/shared": ["../../libs/shared/src"],
      "@vendix/types": ["../../libs/types/src"]
    }
  }
}
```

## Decision Tree

```
Creating shared code?
├── Is it UI-related?          → libs/ui/
├── Is it business logic?      → libs/shared/
├── Is it types/interfaces?    → libs/types/
└── Is it app-specific?        → Keep in apps/

Adding dependency?
├── Is it used by both apps?   → Install in root
├── Is it frontend-only?       → Install in apps/frontend
├── Is it backend-only?        → Install in apps/backend
└── Run npm install -ws        → Install in all workspaces

Running development?
├── Need both apps?            → npm run dev
├── Need frontend only?        → npm run start -w apps/frontend
├── Need backend only?         → npm run start:dev -w apps/backend
└── Need Docker?               → docker compose up -d
```

## Code Examples

### Example 1: Shared Utility Library

```typescript
// libs/shared/src/lib/utils.ts
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
  }).format(price);
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 15);
}

// Export in public-api.ts
export * from './lib/utils';
```

### Example 2: Shared Types

```typescript
// libs/types/src/lib/user.types.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

export interface CreateUserData {
  email: string;
  name: string;
  password: string;
}

// Export in public-api.ts
export * from './lib/user.types';
```

### Example 3: Using Shared Library in Frontend

```typescript
// apps/frontend/src/app/services/user.service.ts
import { User, CreateUserData } from '@vendix/types';
import { formatPrice } from '@vendix/shared';

@Injectable({ providedIn: 'root' })
export class UserService {
  createUser(data: CreateUserData): Observable<User> {
    // implementation
  }
}
```

### Example 4: Using Shared Library in Backend

```typescript
// apps/backend/src/users/users.service.ts
import { User, CreateUserData } from '@vendix/types';

@Injectable()
export class UsersService {
  async create(data: CreateUserData): Promise<User> {
    return this.prisma.user.create({ data });
  }
}
```

## Commands

```bash
# Install all dependencies
npm run install:all

# Start development (both apps)
npm run dev

# Start specific app
npm run start -w apps/frontend
npm run start:dev -w apps/backend

# Build all apps
npm run build

# Install dependency in specific workspace
npm install <package> -w apps/frontend
npm install <package> -w apps/backend

# Install dependency in all workspaces
npm install <package> -ws

# Add dependency to root
npm install <package> --save-exact
```

## Docker Development

```bash
# Start all services (Postgres, backend, frontend)
docker compose up -d

# Rebuild and start
docker compose up --build -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Stop services
docker compose down

# Stop with volumes
docker compose down --volumes
```

## Resources

- **Frontend**: [apps/frontend/](../../../apps/frontend/)
- **Backend**: [apps/backend/](../../../apps/backend/)
- **Shared Libs**: [libs/](../../../libs/)
- **Docker**: [docker-compose.yml](../../../docker-compose.yml)
