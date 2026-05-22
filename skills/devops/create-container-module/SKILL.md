---
name: create-container-module
description: Scaffolds new container modules following ModuleImplementationGuide.md Section 3.1 standard structure. Creates directory layout, required files (Dockerfile, package.json, tsconfig.json, README.md, CHANGELOG.md), config files with schema validation, server.ts entry point, and OpenAPI spec. Use when creating a new microservice container, scaffolding module structure, or setting up a new service following the standard architecture.
---

# Create Container Module

Scaffolds new container modules following the standard structure from ModuleImplementationGuide.md Section 3.1.

## Quick Start

When creating a new container module:

1. Create standard directory structure
2. Generate required files (Dockerfile, package.json, tsconfig.json, README.md, CHANGELOG.md)
3. Set up configuration (config/default.yaml, config/schema.json)
4. Create src/server.ts entry point
5. Generate OpenAPI spec template

## Standard Directory Layout

Reference: ModuleImplementationGuide.md Section 3.1

```
containers/[module-name]/
├── Dockerfile
├── package.json
├── tsconfig.json
├── README.md
├── CHANGELOG.md
├── openapi.yaml
├── config/
│   ├── default.yaml
│   └── schema.json
├── src/
│   ├── server.ts
│   ├── config/
│   │   ├── index.ts
│   │   └── types.ts
│   ├── routes/
│   │   ├── index.ts
│   │   └── [resource].ts
│   ├── services/
│   │   └── [Service].ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── logger.ts
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

## Required Files

### 1. Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY containers/shared/package*.json ./containers/shared/
RUN npm install
COPY containers/[module-name] ./containers/[module-name]
COPY containers/shared ./containers/shared
WORKDIR /app/containers/shared
RUN npm run build
WORKDIR /app/containers/[module-name]
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/containers/[module-name]/dist ./dist
COPY --from=builder /app/containers/[module-name]/node_modules ./node_modules
COPY --from=builder /app/containers/[module-name]/package.json ./
EXPOSE 3XXX
CMD ["node", "dist/server.js"]
```

### 2. package.json

```json
{
  "name": "@coder/[module-name]",
  "version": "1.0.0",
  "description": "[Module Description]",
  "main": "dist/server.js",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src --ext .ts"
  },
  "dependencies": {
    "@coder/shared": "file:../shared",
    "@fastify/swagger": "^9.1.0",
    "@fastify/swagger-ui": "^5.0.0",
    "fastify": "^5.1.0",
    "js-yaml": "^4.1.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "@types/node": "^25.0.5",
    "@vitest/coverage-v8": "^2.1.0",
    "tsx": "^4.19.2",
    "typescript": "^5.9.3",
    "vitest": "^4.0.0"
  }
}
```

### 3. tsconfig.json

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### 4. config/default.yaml

Reference: ModuleImplementationGuide.md Section 4.2

```yaml
module:
  name: [module-name]
  version: 1.0.0

server:
  port: ${PORT:-3XXX}
  host: ${HOST:-0.0.0.0}

cosmos_db:
  endpoint: ${COSMOS_DB_ENDPOINT}
  key: ${COSMOS_DB_KEY}
  database_id: ${COSMOS_DB_DATABASE_ID:-castiel}
  containers:
    main: [module-name]_data

services:
  auth:
    url: ${AUTH_URL:-http://localhost:3021}
  logging:
    url: ${LOGGING_URL:-http://localhost:3014}

rabbitmq:
  url: ${RABBITMQ_URL}
  exchange: coder_events
  queue: [module-name]_service
  bindings: []

features:
  feature_flag: ${FEATURE_FLAG:-true}
```

### 5. config/schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["server", "cosmos_db"],
  "properties": {
    "server": {
      "type": "object",
      "required": ["port"],
      "properties": {
        "port": { "type": "number" },
        "host": { "type": "string" }
      }
    },
    "cosmos_db": {
      "type": "object",
      "required": ["endpoint", "key", "database_id"],
      "properties": {
        "endpoint": { "type": "string" },
        "key": { "type": "string" },
        "database_id": { "type": "string" }
      }
    }
  }
}
```

### 6. src/server.ts

Reference: containers/auth/src/server.ts

```typescript
import { randomUUID } from 'crypto';
import Fastify, { FastifyInstance } from 'fastify';
import { initializeDatabase, getDatabaseClient, setupJWT } from '@coder/shared';
import swagger from '@fastify/swagger';
import swaggerUI from '@fastify/swagger-ui';
import { loadConfig } from './config';
import { log } from './utils/logger';

let app: FastifyInstance | null = null;

export async function buildApp(): Promise<FastifyInstance> {
  const config = loadConfig();
  
  const fastify = Fastify({
    logger: false,
    requestIdHeader: 'x-request-id',
    genReqId: () => randomUUID(),
    bodyLimit: 1048576,
    requestTimeout: 30000,
  });

  await fastify.register(swagger, {
    openapi: {
      openapi: '3.0.3',
      info: {
        title: '[Module Name] API',
        version: '1.0.0',
      },
      servers: [{ url: '/api/v1' }],
    },
  });

  await fastify.register(swaggerUI, {
    routePrefix: '/docs',
  });
  
  await setupJWT(fastify, {
    secret: config.jwt?.secret || process.env.JWT_SECRET || 'change-me',
  });
  
  // Initialize database
  initializeDatabase({
    endpoint: config.cosmos_db.endpoint,
    key: config.cosmos_db.key,
    database: config.cosmos_db.database_id,
    containers: config.cosmos_db.containers,
  });
  
  const db = getDatabaseClient();
  
  // Note: Tenant enforcement is handled per-route via tenantEnforcementMiddleware()
  // No need to register globally - use in route preHandler arrays
  
  // Register global error handler
  fastify.setErrorHandler((error: Error & { validation?: unknown; statusCode?: number }, request, reply) => {
    log.error('Request error', error, {
      requestId: request.id,
      path: request.url,
      method: request.method,
      service: '[module-name]',
    });
    
    // Handle validation errors
    if (error.validation) {
      return reply.status(400).send({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request',
          details: error.validation,
        },
      });
    }
    
    // Generic error response
    return reply.status(error.statusCode || 500).send({
      error: {
        code: 'INTERNAL_ERROR',
        message: process.env.NODE_ENV === 'production'
          ? 'An unexpected error occurred'
          : error.message,
      },
    });
  });
  
  // Register request/response logging hooks
  fastify.addHook('onRequest', async (request) => {
    log.debug('Request received', {
      requestId: request.id,
      method: request.method,
      path: request.url,
      service: '[module-name]',
    });
  });
  
  fastify.addHook('onResponse', async (request, reply) => {
    log.debug('Request completed', {
      requestId: request.id,
      method: request.method,
      path: request.url,
      statusCode: reply.statusCode,
      responseTime: reply.elapsedTime,
      service: '[module-name]',
    });
  });
  
  // Register routes
  const { registerRoutes } = await import('./routes');
  await registerRoutes(fastify, { db, config });
  
  // Health check endpoints (no auth required)
  fastify.get('/health', async () => {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: '[module-name]',
    };
  });
  
  fastify.get('/ready', async () => {
    const db = getDatabaseClient();
    let dbStatus = 'unknown';
    
    try {
      // Test database connection
      const container = db.getContainer(config.cosmos_db.containers.main);
      await container.read();
      dbStatus = 'ok';
    } catch (error) {
      dbStatus = 'error';
    }
    
    const allOk = dbStatus === 'ok';
    
    return {
      status: allOk ? 'ready' : 'not_ready',
      checks: {
        database: { status: dbStatus },
      },
      timestamp: new Date().toISOString(),
      service: '[module-name]',
    };
  });
  
  app = fastify;
  return fastify;
}

export async function start(): Promise<void> {
  try {
    const config = loadConfig();
    const app = await buildApp();
    
    await app.listen({
      port: config.server.port,
      host: config.server.host,
    });
    
    log.info(`[Module Name] service listening on http://${config.server.host}:${config.server.port}`, {
      port: config.server.port,
      host: config.server.host,
      service: '[module-name]',
    });
  } catch (error) {
    log.error('Failed to start [module-name] service', error, { service: '[module-name]' });
    process.exit(1);
  }
}

// Graceful shutdown handler
async function gracefulShutdown(signal: string): Promise<void> {
  log.info(`${signal} received, shutting down gracefully`, { service: '[module-name]' });
  if (app) {
    await app.close();
  }
  process.exit(0);
}

// Graceful shutdown
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Handle uncaught exceptions
process.on('uncaughtException', (error: Error) => {
  log.error('Uncaught exception', error, { service: '[module-name]' });
  gracefulShutdown('uncaughtException').catch(() => {
    process.exit(1);
  });
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason: any, promise: Promise<any>) => {
  log.error('Unhandled promise rejection', reason as Error, {
    service: '[module-name]',
    promise: promise.toString(),
  });
});

// Start server if this file is run directly
if (require.main === module) {
  start().catch((error) => {
    console.error('Fatal error starting server:', error);
    process.exit(1);
  });
}
```

### 7. src/routes/index.ts

Reference: containers/auth/src/routes/index.ts, containers/context-service/src/routes/index.ts

```typescript
/**
 * Route Registration
 * Per ModuleImplementationGuide Section 7
 */

import { FastifyInstance } from 'fastify';
import { ModuleConfig } from '../config/types';

export async function registerRoutes(
  fastify: FastifyInstance,
  deps: { db: any; config: ModuleConfig }
): Promise<void> {
  // Register resource routes
  const { setupResourceRoutes } = await import('./resource');
  await setupResourceRoutes(fastify, deps);
}
```

### 8. src/routes/[resource].ts (Example Route)

Reference: containers/context-service/src/routes/index.ts

```typescript
import { FastifyInstance } from 'fastify';
import { authenticateRequest, tenantEnforcementMiddleware } from '@coder/shared';
import { AppError } from '@coder/shared';
import { ResourceService } from '../services/ResourceService';

export async function setupResourceRoutes(
  fastify: FastifyInstance,
  deps: { db: any; config: any }
): Promise<void> {
  const service = new ResourceService(deps.db);
  
  // GET /api/v1/resources/:id
  fastify.get<{ Params: { id: string } }>(
    '/api/v1/resources/:id',
    {
      preHandler: [authenticateRequest(), tenantEnforcementMiddleware()],
      schema: {
        description: 'Get resource by ID',
        tags: ['Resources'],
        params: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
          },
        },
        response: {
          200: {
            type: 'object',
            description: 'Resource details',
          },
        },
      },
    },
    async (request, reply) => {
      // ✅ tenantId is available from tenantEnforcementMiddleware via request.user
      // The middleware extracts X-Tenant-ID header and validates it
      const tenantId = request.user!.tenantId;
      const userId = request.user!.id; // Also available from authenticateRequest
      
      const resource = await service.getResource(tenantId, request.params.id);
      if (!resource) {
        throw new AppError('Resource not found', 404, 'NOT_FOUND');
      }
      
      return reply.send({ data: resource });
    }
  );
  
  // POST /api/v1/resources
  fastify.post<{ Body: CreateResourceInput }>(
    '/api/v1/resources',
    {
      preHandler: [authenticateRequest(), tenantEnforcementMiddleware()],
      schema: {
        description: 'Create a new resource',
        tags: ['Resources'],
        body: {
          type: 'object',
          required: ['name'],
          properties: {
            name: { type: 'string' },
          },
        },
        response: {
          201: {
            type: 'object',
            description: 'Resource created successfully',
          },
        },
      },
    },
    async (request, reply) => {
      // ✅ tenantId and userId available from middleware
      const tenantId = request.user!.tenantId;
      const userId = request.user!.id;
      
      const resource = await service.createResource(tenantId, request.body);
      return reply.status(201).send({ data: resource });
    }
  );
}
```

**Note**: 
- `authenticateRequest()` validates JWT token and attaches user to `request.user`
- `tenantEnforcementMiddleware()` validates `X-Tenant-ID` header and attaches `tenantId` to `request.user.tenantId`
- Both are required in `preHandler` array for protected routes
- The gateway injects `X-Tenant-ID` header (immutable, from JWT)

### 9. openapi.yaml

Reference: ModuleImplementationGuide.md Section 7.4

```yaml
openapi: 3.0.3
info:
  title: [Module Name] API
  version: 1.0.0
servers:
  - url: /api/v1
paths:
  /health:
    get:
      summary: Health check
      responses:
        '200':
          description: Service is healthy
```

### 10. README.md

```markdown
# [Module Name] Module

[Description]

## Features

- Feature 1
- Feature 2

## Quick Start

### Prerequisites
- Node.js 20+
- Azure Cosmos DB NoSQL account

### Installation
\`\`\`bash
npm install
\`\`\`

### Configuration
\`\`\`bash
cp config/default.yaml config/local.yaml
\`\`\`

### Running
\`\`\`bash
npm run dev
\`\`\`

## API Reference

See [OpenAPI Spec](./openapi.yaml)

## Events

### Published Events
- \`[module].event.name\`

### Consumed Events
- \`other.event.name\`
```

### 11. src/utils/logger.ts

Reference: containers/auth/src/utils/logger.ts

```typescript
/**
 * Structured Logger
 * Per ModuleImplementationGuide Section 15.2
 */

const LOG_LEVELS = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3,
} as const;

type LogLevel = keyof typeof LOG_LEVELS;

const currentLevel: LogLevel = (process.env.LOG_LEVEL as LogLevel) || 'info';

function shouldLog(level: LogLevel): boolean {
  return LOG_LEVELS[level] <= LOG_LEVELS[currentLevel];
}

function formatLog(level: LogLevel, message: string, meta?: Record<string, any>): string {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level: level.toUpperCase(),
    service: '[module-name]',
    message,
    ...meta,
  };
  return JSON.stringify(logEntry);
}

export const log = {
  error(message: string, error?: Error | unknown, meta?: Record<string, any>): void {
    if (shouldLog('error')) {
      const errorMeta = error instanceof Error 
        ? { error: error.message, stack: process.env.NODE_ENV !== 'production' ? error.stack : undefined }
        : error 
          ? { error: String(error) }
          : {};
      console.error(formatLog('error', message, { ...errorMeta, ...meta }));
    }
  },
  
  warn(message: string, meta?: Record<string, any>): void {
    if (shouldLog('warn')) {
      console.warn(formatLog('warn', message, meta));
    }
  },
  
  info(message: string, meta?: Record<string, any>): void {
    if (shouldLog('info')) {
      console.info(formatLog('info', message, meta));
    }
  },
  
  debug(message: string, meta?: Record<string, any>): void {
    if (shouldLog('debug')) {
      console.debug(formatLog('debug', message, meta));
    }
  },
};
```

### 12. CHANGELOG.md

```markdown
# Changelog

## [1.0.0] - YYYY-MM-DD

### Added
- Initial module creation
- Core functionality
```

## Validation Checklist

- [ ] All required files created
- [ ] Directory structure matches Section 3.1
- [ ] Config uses environment variables (no hardcoded values)
- [ ] Server.ts follows auth container pattern
- [ ] OpenAPI spec created
- [ ] TypeScript config extends root tsconfig.json
- [ ] Logger utility created in src/utils/logger.ts
- [ ] All imports use @coder/shared (no direct module imports)
- [ ] Health check endpoints implemented (/health, /ready)
