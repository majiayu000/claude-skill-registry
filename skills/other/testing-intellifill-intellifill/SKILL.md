---
name: testing
description: Write tests for IntelliFill using Jest (backend) and Vitest (frontend). Use when adding unit tests, integration tests, or component tests.
---

# Testing Skill

This skill provides comprehensive guidance for writing tests in IntelliFill using Jest (backend) and Vitest (frontend).

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Backend Testing (Jest)](#backend-testing-jest)
3. [Frontend Testing (Vitest)](#frontend-testing-vitest)
4. [Mocking Patterns](#mocking-patterns)
5. [Integration Tests](#integration-tests)
6. [Coverage Requirements](#coverage-requirements)
7. [CI/CD Integration](#cicd-integration)

## Testing Philosophy

IntelliFill follows these testing principles:

1. **Test behavior, not implementation** - Focus on what the code does, not how
2. **Write tests first** - TDD when possible
3. **Keep tests simple** - Tests should be easier to understand than the code
4. **Mock external dependencies** - Database, APIs, file system
5. **Test edge cases** - Happy path + error cases
6. **Maintainable tests** - Refactor tests like production code

### Test Pyramid

```
        E2E Tests (Cypress/Playwright)
              /\
             /  \
            /    \
           /      \
          /________\
         Integration Tests
        /            \
       /              \
      /                \
     /                  \
    /____________________\
        Unit Tests
```

## Backend Testing (Jest)

IntelliFill backend uses Jest for testing.

### Jest Configuration

```javascript
// quikadmin/jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/__tests__/**',
  ],
  coverageThresholds: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};
```

### Test Setup

```typescript
// quikadmin/src/test/setup.ts
import { PrismaClient } from '@prisma/client';

// Global test setup
beforeAll(async () => {
  // Setup test database
  process.env.DATABASE_URL = process.env.TEST_DATABASE_URL;
});

afterAll(async () => {
  // Cleanup
});

// Global mocks
jest.mock('../utils/logger', () => ({
  info: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  debug: jest.fn(),
}));
```

### Service Test Template

```typescript
// quikadmin/src/services/__tests__/document.service.test.ts
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { DocumentService } from '../document.service';
import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended';

// Create mock Prisma client
const prismaMock = mockDeep<PrismaClient>() as unknown as DeepMockProxy<PrismaClient>;

describe('DocumentService', () => {
  let documentService: DocumentService;

  beforeEach(() => {
    // Create service with mocked dependencies
    documentService = new DocumentService({ prisma: prismaMock });
  });

  afterEach(() => {
    mockReset(prismaMock);
  });

  describe('getById', () => {
    it('should return document when found', async () => {
      const mockDocument = {
        id: 'doc-1',
        name: 'Test Document',
        userId: 'user-1',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      prismaMock.document.findFirst.mockResolvedValue(mockDocument);

      const result = await documentService.getById('doc-1', 'user-1');

      expect(result).toEqual(mockDocument);
      expect(prismaMock.document.findFirst).toHaveBeenCalledWith({
        where: { id: 'doc-1', userId: 'user-1' },
      });
    });

    it('should throw error when document not found', async () => {
      prismaMock.document.findFirst.mockResolvedValue(null);

      await expect(
        documentService.getById('doc-1', 'user-1')
      ).rejects.toThrow('Document not found');
    });

    it('should not return document from different user', async () => {
      prismaMock.document.findFirst.mockResolvedValue(null);

      await expect(
        documentService.getById('doc-1', 'wrong-user')
      ).rejects.toThrow('Document not found');
    });
  });

  describe('create', () => {
    it('should create document successfully', async () => {
      const createData = {
        name: 'New Document',
        content: 'Test content',
      };

      const mockCreated = {
        id: 'doc-1',
        ...createData,
        userId: 'user-1',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      prismaMock.document.create.mockResolvedValue(mockCreated);

      const result = await documentService.create({
        userId: 'user-1',
        data: createData,
      });

      expect(result).toEqual(mockCreated);
      expect(prismaMock.document.create).toHaveBeenCalledWith({
        data: {
          ...createData,
          userId: 'user-1',
        },
      });
    });

    it('should handle database errors', async () => {
      prismaMock.document.create.mockRejectedValue(
        new Error('Database error')
      );

      await expect(
        documentService.create({
          userId: 'user-1',
          data: { name: 'Test' },
        })
      ).rejects.toThrow('Database error');
    });
  });

  describe('list', () => {
    it('should return paginated documents', async () => {
      const mockDocuments = [
        { id: 'doc-1', name: 'Doc 1', userId: 'user-1' },
        { id: 'doc-2', name: 'Doc 2', userId: 'user-1' },
      ];

      prismaMock.document.findMany.mockResolvedValue(mockDocuments);
      prismaMock.document.count.mockResolvedValue(10);

      const result = await documentService.list({
        userId: 'user-1',
        page: 1,
        limit: 20,
      });

      expect(result.items).toEqual(mockDocuments);
      expect(result.total).toBe(10);
      expect(result.page).toBe(1);
      expect(result.totalPages).toBe(1);
    });

    it('should filter by search query', async () => {
      const mockDocuments = [{ id: 'doc-1', name: 'Test Document' }];

      prismaMock.document.findMany.mockResolvedValue(mockDocuments);
      prismaMock.document.count.mockResolvedValue(1);

      await documentService.list({
        userId: 'user-1',
        page: 1,
        limit: 20,
        search: 'test',
      });

      expect(prismaMock.document.findMany).toHaveBeenCalledWith({
        where: {
          userId: 'user-1',
          OR: [
            { name: { contains: 'test', mode: 'insensitive' } },
            { description: { contains: 'test', mode: 'insensitive' } },
          ],
        },
        skip: 0,
        take: 20,
        orderBy: { createdAt: 'desc' },
      });
    });
  });
});
```

### API Route Test Template

```typescript
// quikadmin/src/api/__tests__/documents.routes.test.ts
import request from 'supertest';
import express from 'express';
import documentRoutes from '../documents.routes';
import { PrismaClient } from '@prisma/client';
import { mockDeep } from 'jest-mock-extended';

// Mock dependencies
jest.mock('../../middleware/supabaseAuth', () => ({
  authMiddleware: (req: any, res: any, next: any) => {
    req.user = { id: 'user-1', email: 'test@example.com' };
    next();
  },
}));

const prismaMock = mockDeep<PrismaClient>();

describe('Document Routes', () => {
  let app: express.Application;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/api/documents', documentRoutes);
  });

  describe('GET /api/documents', () => {
    it('should return list of documents', async () => {
      const mockDocuments = [
        { id: 'doc-1', name: 'Test Doc' },
        { id: 'doc-2', name: 'Another Doc' },
      ];

      prismaMock.document.findMany.mockResolvedValue(mockDocuments);
      prismaMock.document.count.mockResolvedValue(2);

      const response = await request(app)
        .get('/api/documents')
        .set('Authorization', 'Bearer token')
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(response.body.data.items).toEqual(mockDocuments);
    });

    it('should require authentication', async () => {
      // Remove auth mock temporarily
      jest.unmock('../../middleware/supabaseAuth');

      const response = await request(app)
        .get('/api/documents')
        .expect(401);

      expect(response.body).toHaveProperty('success', false);
    });
  });

  describe('POST /api/documents', () => {
    it('should create document with valid data', async () => {
      const newDoc = {
        name: 'New Document',
        description: 'Test description',
      };

      const mockCreated = {
        id: 'doc-1',
        ...newDoc,
        userId: 'user-1',
      };

      prismaMock.document.create.mockResolvedValue(mockCreated);

      const response = await request(app)
        .post('/api/documents')
        .set('Authorization', 'Bearer token')
        .send(newDoc)
        .expect(201);

      expect(response.body.data).toEqual(mockCreated);
    });

    it('should validate required fields', async () => {
      const response = await request(app)
        .post('/api/documents')
        .set('Authorization', 'Bearer token')
        .send({}) // Missing required fields
        .expect(400);

      expect(response.body).toHaveProperty('success', false);
      expect(response.body).toHaveProperty('error');
    });

    it('should reject invalid data types', async () => {
      const response = await request(app)
        .post('/api/documents')
        .set('Authorization', 'Bearer token')
        .send({
          name: 123, // Should be string
        })
        .expect(400);

      expect(response.body.success).toBe(false);
    });
  });

  describe('DELETE /api/documents/:id', () => {
    it('should delete document', async () => {
      prismaMock.document.findFirst.mockResolvedValue({
        id: 'doc-1',
        userId: 'user-1',
      });
      prismaMock.document.delete.mockResolvedValue({ id: 'doc-1' });

      await request(app)
        .delete('/api/documents/doc-1')
        .set('Authorization', 'Bearer token')
        .expect(204);
    });

    it('should return 404 for non-existent document', async () => {
      prismaMock.document.findFirst.mockResolvedValue(null);

      await request(app)
        .delete('/api/documents/nonexistent')
        .set('Authorization', 'Bearer token')
        .expect(404);
    });
  });
});
```

## Frontend Testing (Vitest)

IntelliFill frontend uses Vitest for testing.

### Vitest Configuration

```typescript
// quikadmin-web/vite.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.tsx'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/__tests__/**',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Test Setup

```typescript
// quikadmin-web/src/test/setup.tsx
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
```

### Component Test Template

```typescript
// quikadmin-web/src/components/__tests__/DocumentCard.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DocumentCard } from '../DocumentCard';

describe('DocumentCard', () => {
  const mockDocument = {
    id: 'doc-1',
    name: 'Test Document',
    description: 'Test description',
    status: 'completed',
    createdAt: '2024-01-01T00:00:00Z',
  };

  it('renders document information', () => {
    render(<DocumentCard document={mockDocument} />);

    expect(screen.getByText('Test Document')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    render(<DocumentCard document={mockDocument} onClick={onClick} />);

    fireEvent.click(screen.getByText('Test Document'));

    expect(onClick).toHaveBeenCalledTimes(1);
    expect(onClick).toHaveBeenCalledWith(mockDocument);
  });

  it('shows loading state', () => {
    render(<DocumentCard document={mockDocument} loading />);

    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('applies correct status styling', () => {
    const { container } = render(
      <DocumentCard document={mockDocument} status="completed" />
    );

    const card = container.firstChild;
    expect(card).toHaveClass('border-green-500');
  });

  it('handles delete action', async () => {
    const onDelete = vi.fn();
    render(<DocumentCard document={mockDocument} onDelete={onDelete} />);

    // Open menu
    fireEvent.click(screen.getByLabelText('Document actions'));

    // Click delete
    fireEvent.click(screen.getByText('Delete'));

    await waitFor(() => {
      expect(onDelete).toHaveBeenCalledWith('doc-1');
    });
  });
});
```

### Store Test Template

```typescript
// quikadmin-web/src/stores/__tests__/documentStore.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useDocumentStore } from '../documentStore';
import * as api from '@/services/api';

// Mock API
vi.mock('@/services/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('useDocumentStore', () => {
  beforeEach(() => {
    // Reset store
    useDocumentStore.setState({
      documents: [],
      loading: false,
      error: null,
    });
    vi.clearAllMocks();
  });

  it('fetches documents successfully', async () => {
    const mockDocuments = [
      { id: 'doc-1', name: 'Doc 1' },
      { id: 'doc-2', name: 'Doc 2' },
    ];

    vi.mocked(api.api.get).mockResolvedValue({ data: mockDocuments });

    const { result } = renderHook(() => useDocumentStore());

    await act(async () => {
      await result.current.fetchDocuments();
    });

    expect(result.current.documents).toEqual(mockDocuments);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    vi.mocked(api.api.get).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useDocumentStore());

    await act(async () => {
      await result.current.fetchDocuments();
    });

    expect(result.current.documents).toEqual([]);
    expect(result.current.error).toBeTruthy();
  });

  it('deletes document optimistically', async () => {
    const mockDocuments = [
      { id: 'doc-1', name: 'Doc 1' },
      { id: 'doc-2', name: 'Doc 2' },
    ];

    useDocumentStore.setState({ documents: mockDocuments });

    vi.mocked(api.api.delete).mockResolvedValue({});

    const { result } = renderHook(() => useDocumentStore());

    await act(async () => {
      await result.current.deleteDocument('doc-1');
    });

    expect(result.current.documents).toHaveLength(1);
    expect(result.current.documents[0].id).toBe('doc-2');
  });
});
```

## Mocking Patterns

### Mock Prisma Client

```typescript
import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended';

const prismaMock = mockDeep<PrismaClient>() as unknown as DeepMockProxy<PrismaClient>;

// Mock specific methods
prismaMock.document.findMany.mockResolvedValue([...]);
prismaMock.document.create.mockResolvedValue({...});
```

### Mock API Calls

```typescript
import { vi } from 'vitest';
import * as api from '@/services/api';

vi.mock('@/services/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

// In tests
vi.mocked(api.api.get).mockResolvedValue({ data: [...] });
```

### Mock File System

```typescript
import fs from 'fs';
import { vi } from 'vitest';

vi.mock('fs', () => ({
  readFileSync: vi.fn(),
  writeFileSync: vi.fn(),
  existsSync: vi.fn(),
}));

// In tests
vi.mocked(fs.readFileSync).mockReturnValue(Buffer.from('test data'));
```

### Mock Environment Variables

```typescript
beforeEach(() => {
  process.env.NODE_ENV = 'test';
  process.env.DATABASE_URL = 'postgresql://test';
});

afterEach(() => {
  delete process.env.DATABASE_URL;
});
```

## Integration Tests

### API Integration Test

```typescript
// quikadmin/src/api/__tests__/integration/documents.integration.test.ts
import request from 'supertest';
import app from '../../../app';
import prisma from '../../../utils/prisma';

describe('Documents API Integration', () => {
  let authToken: string;
  let userId: string;

  beforeAll(async () => {
    // Create test user and get token
    const response = await request(app)
      .post('/api/auth/v2/register')
      .send({
        email: 'test@example.com',
        password: 'password123',
      });

    authToken = response.body.token;
    userId = response.body.user.id;
  });

  afterAll(async () => {
    // Cleanup
    await prisma.document.deleteMany({ where: { userId } });
    await prisma.user.delete({ where: { id: userId } });
    await prisma.$disconnect();
  });

  it('should complete full document lifecycle', async () => {
    // Create document
    const createResponse = await request(app)
      .post('/api/documents')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'Integration Test Doc' })
      .expect(201);

    const docId = createResponse.body.data.id;

    // Get document
    await request(app)
      .get(`/api/documents/${docId}`)
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    // Update document
    await request(app)
      .patch(`/api/documents/${docId}`)
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'Updated Name' })
      .expect(200);

    // Delete document
    await request(app)
      .delete(`/api/documents/${docId}`)
      .set('Authorization', `Bearer ${authToken}`)
      .expect(204);

    // Verify deleted
    await request(app)
      .get(`/api/documents/${docId}`)
      .set('Authorization', `Bearer ${authToken}`)
      .expect(404);
  });
});
```

## Coverage Requirements

IntelliFill enforces minimum test coverage:

```javascript
coverageThresholds: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70,
  },
}
```

### Running Coverage

```bash
# Backend
cd quikadmin
npm run test:coverage

# Frontend
cd quikadmin-web
bun run test:coverage
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd quikadmin && npm ci
      - run: cd quikadmin && npm run test:coverage

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: oven-sh/setup-bun@v1
      - run: cd quikadmin-web && bun install
      - run: cd quikadmin-web && bun run test:coverage
```

## Best Practices

1. **Test file naming** - `*.test.ts` for all test files
2. **Descriptive test names** - Use "should" format
3. **Arrange-Act-Assert** - Clear test structure
4. **One assertion per test** - Keep tests focused
5. **Mock external dependencies** - Don't hit real APIs/DB
6. **Test edge cases** - Null, undefined, empty arrays
7. **Cleanup after tests** - Reset mocks and state
8. **Use factories** - Create test data with factories
9. **Avoid brittle tests** - Don't test implementation details
10. **Keep tests fast** - Unit tests should run in milliseconds

## References

- [Jest Documentation](https://jestjs.io/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [jest-mock-extended](https://github.com/marchaos/jest-mock-extended)
