---
description: "Generar documentación automática. README, API docs, JSDoc, Storybook stories."
user-invocable: true
argument-hint: "[readme|api|jsdoc|component] [path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Docs Skill

Genera documentación automática analizando el código fuente.

## Comandos

### README - Generar README.md

```bash
/docs readme
```

**Analiza:**
- package.json (nombre, descripción, scripts)
- Estructura de carpetas
- Stack tecnológico
- Variables de entorno (.env.example)

**Genera:**
```markdown
# Project Name

Brief description from package.json

## Features

- Feature 1 (detected from code)
- Feature 2
- Feature 3

## Tech Stack

- Next.js 15
- React 19
- TypeScript
- Prisma + PostgreSQL

## Quick Start

\`\`\`bash
# Install dependencies
pnpm install

# Setup environment
cp .env.example .env

# Run database migrations
pnpm db:migrate

# Start development server
pnpm dev
\`\`\`

## Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server |
| `pnpm build` | Build for production |
| `pnpm test` | Run tests |
| `pnpm lint` | Run linter |

## Project Structure

\`\`\`
src/
├── app/          # Next.js pages
├── components/   # React components
├── services/     # Business logic
├── hooks/        # Custom hooks
└── lib/          # Utilities
\`\`\`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection | Yes |
| NEXTAUTH_SECRET | Auth secret | Yes |

## License

MIT
```

### API - Documentación de API

```bash
/docs api
/docs api src/app/api/
```

**Analiza:**
- Route handlers en app/api/
- Schemas de Zod
- Types de request/response

**Genera:**
```markdown
# API Reference

## Authentication

All endpoints require Bearer token:
\`\`\`
Authorization: Bearer <token>
\`\`\`

## Endpoints

### Users

#### GET /api/users

List all users.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | number | 1 | Page number |
| limit | number | 20 | Items per page |

**Response:**
\`\`\`json
{
  "data": [
    { "id": "1", "email": "user@example.com" }
  ],
  "pagination": {
    "page": 1,
    "total": 100
  }
}
\`\`\`

#### POST /api/users

Create a new user.

**Request Body:**
\`\`\`typescript
{
  email: string;  // Valid email
  name: string;   // 2-100 chars
}
\`\`\`
```

### JSDOC - Agregar JSDoc a Funciones

```bash
/docs jsdoc src/services/user.service.ts
```

**Transforma:**
```typescript
// Antes
async function createUser(data: CreateUserInput) {
  return prisma.user.create({ data });
}

// Después
/**
 * Creates a new user in the database.
 *
 * @param data - The user data to create
 * @param data.email - User's email address
 * @param data.name - User's display name
 * @returns The created user with generated ID
 * @throws {ValidationError} If email is invalid
 * @throws {ConflictError} If email already exists
 *
 * @example
 * ```typescript
 * const user = await createUser({
 *   email: 'user@example.com',
 *   name: 'John Doe',
 * });
 * ```
 */
async function createUser(data: CreateUserInput) {
  return prisma.user.create({ data });
}
```

### COMPONENT - Documentar Componentes React

```bash
/docs component src/components/Button.tsx
```

**Genera:**
```typescript
/**
 * Button component for user interactions.
 *
 * @component
 * @example
 * ```tsx
 * <Button variant="primary" onClick={handleClick}>
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps {
  /** The visual style of the button */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Whether the button is disabled */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button content */
  children: React.ReactNode;
}
```

## Opciones

```bash
/docs readme --output docs/README.md
/docs api --format openapi
/docs jsdoc --all  # Todas las funciones exportadas
```

## Output

```
📚 DOCUMENTATION GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Created/Updated:
  ✅ README.md (new)
  ✅ docs/API.md (new)
  ✅ src/services/user.service.ts (updated with JSDoc)

Documentation Coverage:
  Functions: 45/52 (87%)
  Components: 12/15 (80%)
  API Routes: 8/8 (100%)

Next Steps:
  1. Review generated documentation
  2. Add examples where needed
  3. Run: pnpm build:docs
```
