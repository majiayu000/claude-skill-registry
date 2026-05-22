---
name: setup-container-tests
description: Creates test structure and boilerplate following ModuleImplementationGuide.md Section 12 testing requirements (80% coverage, Vitest). Generates unit test structure, creates integration test templates, sets up test fixtures, mocks external dependencies, tests tenant isolation, tests event publishing/consuming, and sets up Vitest configuration. Use when setting up tests for new services, adding test coverage, or creating integration tests.
---

# Setup Container Tests

Creates test structure following ModuleImplementationGuide.md Section 12 (Testing Requirements).

## Test Structure

Reference: containers/auth/tests/

```
tests/
├── setup.ts                    # Global test setup and mocks
├── fixtures/                   # Test data fixtures
│   └── [resource].ts          # Resource test data
├── unit/                       # Unit tests
│   ├── utils/                 # Utility function tests
│   └── services/             # Service tests
│       └── [Service].test.ts
└── integration/               # Integration tests
    └── routes/               # API route tests
        └── [resource].test.ts
```

## Vitest Configuration

Reference: containers/auth/vitest.config.mjs

### vitest.config.mjs

```javascript
import { defineConfig } from 'vitest/config';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    testTimeout: 30000,
    hookTimeout: 30000,
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
      },
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      reportsDirectory: './coverage',
      exclude: [
        'node_modules/**',
        'dist/**',
        'tests/**',
        '**/*.d.ts',
        'src/server.ts',
        '**/index.ts',
        'src/config/**',
      ],
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 60,
        statements: 70,
      },
    },
    setupFiles: ['./tests/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@coder/shared': path.resolve(__dirname, '../shared/src'),
    },
  },
});
```

## Test Setup File

Reference: containers/auth/tests/setup.ts

### tests/setup.ts

```typescript
import { vi, beforeAll, afterAll, afterEach } from 'vitest';

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.COSMOS_DB_ENDPOINT = process.env.TEST_COSMOS_DB_ENDPOINT || 'https://test.documents.azure.com:443/';
process.env.COSMOS_DB_KEY = process.env.TEST_COSMOS_DB_KEY || 'test-key';
process.env.RABBITMQ_URL = process.env.TEST_RABBITMQ_URL || '';
process.env.JWT_SECRET = process.env.TEST_JWT_SECRET || 'test-jwt-secret';
process.env.REDIS_URL = process.env.TEST_REDIS_URL || '';
process.env.PORT = '3000';
process.env.HOST = '0.0.0.0';

// Mock @coder/shared database client
vi.mock('@coder/shared', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@coder/shared')>();
  return {
    ...actual,
    getDatabaseClient: vi.fn(() => ({
      getContainer: vi.fn(() => ({
        items: {
          query: vi.fn(() => ({
            fetchAll: vi.fn().mockResolvedValue({ resources: [] }),
          })),
          create: vi.fn().mockResolvedValue({ resource: {} }),
          upsert: vi.fn().mockResolvedValue({ resource: {} }),
        },
        item: vi.fn(() => ({
          delete: vi.fn().mockResolvedValue({}),
        })),
      })),
    })),
    getCacheClient: vi.fn(() => ({
      get: vi.fn().mockResolvedValue(null),
      set: vi.fn().mockResolvedValue('OK'),
      del: vi.fn().mockResolvedValue(1),
    })),
    EventPublisher: vi.fn(() => ({
      publish: vi.fn().mockResolvedValue(undefined),
    })),
    EventConsumer: vi.fn(() => ({
      on: vi.fn(),
      start: vi.fn().mockResolvedValue(undefined),
      stop: vi.fn().mockResolvedValue(undefined),
    })),
  };
});

// Mock config loader
vi.mock('../src/config', () => ({
  loadConfig: vi.fn(() => ({
    module: { name: '[module-name]', version: '1.0.0' },
    server: { port: 3000, host: '0.0.0.0' },
    cosmos_db: {
      endpoint: process.env.COSMOS_DB_ENDPOINT,
      key: process.env.COSMOS_DB_KEY,
      database_id: 'test',
      containers: { main: '[module-name]_data' },
    },
    rabbitmq: {
      url: process.env.RABBITMQ_URL || '',
      exchange: 'test_events',
      queue: 'test_queue',
      bindings: [],
    },
  })),
}));

// Global test setup
beforeAll(async () => {
  // Setup can go here if needed
});

afterEach(() => {
  vi.clearAllMocks();
});

afterAll(async () => {
  // Cleanup can go here if needed
});
```

## Unit Test Template

### tests/unit/services/[Service].test.ts

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Service } from '../../../src/services/Service';
import { getDatabaseClient } from '@coder/shared';

describe('Service', () => {
  let service: Service;
  let mockDb: any;

  beforeEach(() => {
    mockDb = getDatabaseClient();
    service = new Service(mockDb);
  });

  describe('getResource', () => {
    it('should return resource for valid tenantId and id', async () => {
      const tenantId = 'tenant-123';
      const id = 'resource-456';
      
      const mockResource = { id, tenantId, name: 'Test Resource' };
      mockDb.getContainer().items.query().fetchAll.mockResolvedValue({
        resources: [mockResource],
      });

      const result = await service.getResource(tenantId, id);

      expect(result).toEqual(mockResource);
      expect(mockDb.getContainer).toHaveBeenCalledWith('[module-name]_data');
    });

    it('should throw error if tenantId is missing', async () => {
      await expect(service.getResource('', 'resource-456')).rejects.toThrow();
    });

    it('should return null if resource not found', async () => {
      mockDb.getContainer().items.query().fetchAll.mockResolvedValue({
        resources: [],
      });

      const result = await service.getResource('tenant-123', 'resource-456');

      expect(result).toBeNull();
    });
  });

  describe('tenant isolation', () => {
    it('should only return resources for specified tenant', async () => {
      const tenantId = 'tenant-123';
      const otherTenantId = 'tenant-456';
      
      mockDb.getContainer().items.query().fetchAll.mockResolvedValue({
        resources: [{ id: 'resource-1', tenantId }],
      });

      await service.getResource(tenantId, 'resource-1');

      const queryCall = mockDb.getContainer().items.query.mock.calls[0][0];
      expect(queryCall.query).toContain('c.tenantId = @tenantId');
      expect(queryCall.parameters).toContainEqual({
        name: '@tenantId',
        value: tenantId,
      });
    });
  });
});
```

## Integration Test Template

### tests/integration/routes/[resource].test.ts

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { buildApp } from '../../../src/server';
import { FastifyInstance } from 'fastify';

describe('Resource Routes', () => {
  let app: FastifyInstance;

  beforeEach(async () => {
    app = await buildApp();
  });

  describe('GET /api/v1/resource/:id', () => {
    it('should return resource with valid tenantId header', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/v1/resource/resource-123',
        headers: {
          'X-Tenant-ID': 'tenant-123',
          'Authorization': 'Bearer valid-token',
        },
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body.data).toBeDefined();
    });

    it('should return 401 without tenantId header', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/v1/resource/resource-123',
        headers: {
          'Authorization': 'Bearer valid-token',
        },
      });

      expect(response.statusCode).toBe(401);
    });
  });
});
```

## Test Fixtures

### tests/fixtures/[resource].ts

```typescript
export const mockResource = {
  id: 'resource-123',
  tenantId: 'tenant-123',
  name: 'Test Resource',
  createdAt: '2025-01-22T10:00:00Z',
  updatedAt: '2025-01-22T10:00:00Z',
};

export const mockResources = [
  mockResource,
  {
    id: 'resource-456',
    tenantId: 'tenant-123',
    name: 'Another Resource',
    createdAt: '2025-01-22T11:00:00Z',
    updatedAt: '2025-01-22T11:00:00Z',
  },
];
```

## Testing Tenant Isolation

Always test tenant isolation:

```typescript
describe('tenant isolation', () => {
  it('should not return resources from other tenants', async () => {
    const tenantId = 'tenant-123';
    const otherTenantId = 'tenant-456';
    
    // Mock query to only return resources for tenant-123
    mockDb.getContainer().items.query().fetchAll.mockResolvedValue({
      resources: [{ id: 'resource-1', tenantId }],
    });

    const result = await service.listResources(tenantId);

    expect(result).toHaveLength(1);
    expect(result[0].tenantId).toBe(tenantId);
    expect(result[0].tenantId).not.toBe(otherTenantId);
  });
});
```

## Testing Event Publishing

```typescript
import { EventPublisher } from '@coder/shared';

describe('event publishing', () => {
  it('should publish event when resource is created', async () => {
    const publishSpy = vi.spyOn(EventPublisher.prototype, 'publish');
    
    await service.createResource('tenant-123', { name: 'Test' });

    expect(publishSpy).toHaveBeenCalledWith(
      '[module].resource.created',
      expect.objectContaining({
        type: '[module].resource.created',
        organizationId: 'tenant-123',
        data: expect.objectContaining({
          name: 'Test',
        }),
      })
    );
  });
});
```

## Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:unit": "vitest run tests/unit",
    "test:int": "vitest run tests/integration"
  }
}
```

## Test Coverage Requirements

Reference: ModuleImplementationGuide.md Section 12, .cursorrules

- Minimum 80% test coverage
- Lines: 70%
- Functions: 70%
- Branches: 60%
- Statements: 70%

## Checklist

- [ ] vitest.config.mjs created
- [ ] tests/setup.ts with mocks
- [ ] Unit test structure created
- [ ] Integration test structure created
- [ ] Test fixtures created
- [ ] Tenant isolation tests included
- [ ] Event publishing/consuming tests included
- [ ] Coverage thresholds configured
- [ ] All external dependencies mocked
