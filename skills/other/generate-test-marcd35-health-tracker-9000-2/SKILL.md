---
name: generate-test
description: Generate Jest test suite with mocks and common test cases. Use when creating tests for components, repositories, or API routes.
allowed-tools: Read, Write, Glob, Grep
---

# Generate Test

Generate a Jest test suite following Health Tracker 9000 testing patterns.

## Usage

When user requests to create tests, ask for:

1. **Test target** (component, repository, API route, or utility)
2. **Target name** (e.g., "MealLogForm", "WaterLogRepository")
3. **Main functionality** to test
4. **Edge cases** or error scenarios

## Implementation Pattern

Based on `src/__tests__/components/forms/MealLogForm.test.tsx` pattern.

### Component Test Structure

Create file: `src/__tests__/{target-type}/{location}/{TargetName}.test.tsx`

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FormName } from '@/components/forms/FormName';
import { useHealthStore } from '@/lib/store/healthStore';

// Mock the store
jest.mock('@/lib/store/healthStore');
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn(),
  },
}));

const mockAddItem = jest.fn();

describe('FormName', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (useHealthStore as jest.Mock).mockReturnValue({
      addItem: mockAddItem,
      isLoading: false,
    });
  });

  it('renders the form correctly', () => {
    render(<FormName />);
    expect(screen.getByLabelText('Field 1 Label')).toBeInTheDocument();
    expect(screen.getByLabelText('Field 2 Label')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(<FormName />);
    const submitButton = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(screen.getByText('Field 1 is required')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    render(<FormName />);
    const field1Input = screen.getByLabelText('Field 1 Label') as HTMLInputElement;
    const field2Input = screen.getByLabelText('Field 2 Label') as HTMLInputElement;
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(field1Input, { target: { value: 'test value' } });
    fireEvent.change(field2Input, { target: { value: '100' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAddItem).toHaveBeenCalledWith(
        expect.objectContaining({
          field1: 'test value',
          field2: '100',
        })
      );
    });
  });

  it('clears form after successful submission', async () => {
    render(<FormName />);
    const field1Input = screen.getByLabelText('Field 1 Label') as HTMLInputElement;
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(field1Input, { target: { value: 'test' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(field1Input.value).toBe('');
    });
  });

  it('disables form while loading', () => {
    (useHealthStore as jest.Mock).mockReturnValue({
      addItem: mockAddItem,
      isLoading: true,
    });

    render(<FormName />);
    const submitButton = screen.getByRole('button', { name: /submit/i });
    expect(submitButton).toBeDisabled();
  });
});
```

### Repository Test Structure

Create file: `src/__tests__/lib/database/repositories/{EntityName}.test.ts`

```typescript
import { EntityRepository } from '@/lib/database/repositories/entityRepository';
import { getDatabase } from '@/lib/database/connection';

jest.mock('@/lib/database/connection');

describe('EntityRepository', () => {
  let repo: EntityRepository;
  let mockDb: any;

  beforeEach(() => {
    jest.clearAllMocks();
    mockDb = {
      prepare: jest.fn(),
    };
    (getDatabase as jest.Mock).mockReturnValue(mockDb);
    repo = new EntityRepository();
  });

  it('adds entity correctly', () => {
    const mockStmt = { run: jest.fn() };
    mockDb.prepare.mockReturnValue(mockStmt);

    const result = repo.addEntity({ field1: 'value1', field2: 'value2' });

    expect(result).toHaveProperty('id');
    expect(result).toHaveProperty('createdAt');
    expect(result.field1).toBe('value1');
    expect(mockStmt.run).toHaveBeenCalled();
  });

  it('gets entity by id', () => {
    const mockStmt = { get: jest.fn() };
    mockDb.prepare.mockReturnValue(mockStmt);
    mockStmt.get.mockReturnValue({
      id: '123',
      field_1: 'value1',
      field_2: '{"nested": "data"}',
    });

    const result = repo.getEntityById('123');

    expect(result).toEqual(
      expect.objectContaining({
        id: '123',
        field1: 'value1',
      })
    );
  });

  it('returns null for non-existent entity', () => {
    const mockStmt = { get: jest.fn() };
    mockDb.prepare.mockReturnValue(mockStmt);
    mockStmt.get.mockReturnValue(undefined);

    const result = repo.getEntityById('nonexistent');

    expect(result).toBeNull();
  });

  it('throws error when updating non-existent entity', () => {
    const mockStmt = { get: jest.fn() };
    mockDb.prepare.mockReturnValue(mockStmt);
    mockStmt.get.mockReturnValue(undefined);

    expect(() => {
      repo.updateEntity('nonexistent', {});
    }).toThrow('Entity not found');
  });

  it('deletes entity correctly', () => {
    const mockStmt = { run: jest.fn() };
    mockDb.prepare.mockReturnValue(mockStmt);

    repo.deleteEntity('123');

    expect(mockStmt.run).toHaveBeenCalledWith('123');
  });
});
```

### API Route Test Structure

Create file: `src/__tests__/app/api/{resource}/route.test.ts`

```typescript
import { POST, DELETE } from '@/app/api/resource/route';
import { ResourceRepository } from '@/lib/database/repositories/resourceRepository';

jest.mock('@/lib/database/repositories/resourceRepository');
jest.mock('@/lib/database/repositories/dailySummaryRepository');

describe('Resource API Route', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('POST creates new resource', async () => {
    const mockRepo = {
      addResource: jest.fn().mockReturnValue({ id: '123', field: 'value' }),
    };
    (ResourceRepository as jest.Mock).mockImplementation(() => mockRepo);

    const request = new Request('http://localhost:3000/api/resource', {
      method: 'POST',
      body: JSON.stringify({ field: 'value', date: '2024-01-15' }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toEqual({ id: '123', field: 'value' });
  });

  it('DELETE removes resource', async () => {
    const mockRepo = { deleteResource: jest.fn() };
    (ResourceRepository as jest.Mock).mockImplementation(() => mockRepo);

    const request = new Request('http://localhost:3000/api/resource?id=123', {
      method: 'DELETE',
    });

    const response = await DELETE(request);

    expect(response.status).toBe(200);
    expect(mockRepo.deleteResource).toHaveBeenCalledWith('123');
  });

  it('DELETE returns 400 when id missing', async () => {
    const request = new Request('http://localhost:3000/api/resource', {
      method: 'DELETE',
    });

    const response = await DELETE(request);

    expect(response.status).toBe(400);
  });
});
```

## Key Conventions

- Test file location mirrors source structure in `src/__tests__/`
- File naming: `{SourceName}.test.ts(x)`
- Mock external dependencies (stores, API calls, database)
- beforeEach to clear mocks between tests
- Use React Testing Library patterns for components
- Test user interactions, not implementation
- Test error cases and edge cases
- Use descriptive test names (should be readable as documentation)
- Mock data should be realistic

## Test Coverage Targets

For components:

- Renders correctly
- Handles user input
- Validates data
- Shows error states
- Manages loading states
- Calls store actions

For repositories:

- CRUD operations work
- Row mapping correct
- Error handling
- Null checks

For API routes:

- POST creates records
- GET retrieves records
- DELETE removes records
- Error handling (400, 500)
- Proper HTTP status codes

## Steps

1. Ask user for test target, name, and functionality
2. Create file: `src/__tests__/{path}/{Name}.test.ts(x)`
3. Mock dependencies (stores, database, APIs)
4. Write beforeEach to clear mocks
5. Write test cases for main functionality
6. Write test cases for error scenarios
7. Format with Prettier

## Implementation Checklist

- [ ] Test file in correct location
- [ ] Dependencies properly mocked
- [ ] beforeEach clears mocks
- [ ] Tests use descriptive names
- [ ] Main functionality tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Uses appropriate testing library
- [ ] No implementation details tested
- [ ] Proper assertions used
