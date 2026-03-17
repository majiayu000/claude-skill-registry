---
name: testing-patterns
description: Jest testing strategies, test organization, factory patterns for test data, mocking strategies for authentication and external services, real-time message processor testing, test-driven development workflow, unit vs integration testing, fake timer usage for time-dependent tests, and testing best practices for ree-board project
model: sonnet
---

# Testing Patterns

## When to Use This Skill

Activate this skill when:

- Writing new tests
- Setting up test infrastructure
- Mocking external dependencies
- Testing server actions
- Testing real-time message processors
- Testing React components
- Implementing test-driven development
- Debugging failing tests

## Core Patterns

### Test Organization

**File Structure:**
```
lib/
├── actions/
│   └── post/
│       ├── createPost.ts
│       └── createPost.test.ts
├── realtime/
│   ├── messageProcessors.ts
│   └── __tests__/
│       └── messageProcessors.test.ts
└── utils/
    ├── md5.ts
    └── md5.test.ts
```

**Naming Convention:**
- Unit tests: `<filename>.test.ts`
- Test directories: `__tests__/`

### Test Structure (AAA Pattern)

**Arrange, Act, Assert:**

```typescript
describe('createPost', () => {
  it('should create a post with valid data', async () => {
    // Arrange
    const boardId = 'board-123';
    const content = 'Test post';
    const type = 'went_well';

    // Act
    const result = await createPost(boardId, content, type);

    // Assert
    expect(result).toBeDefined();
    expect(result.content).toBe(content);
    expect(result.type).toBe(type);
  });
});
```

### Mocking Authentication

**Pattern for Testing Server Actions:**

```typescript
// __tests__/createPost.test.ts
import { createPost } from '../createPost';
import { getKindeServerSession } from '@kinde-oss/kinde-auth-nextjs/server';

// Mock Kinde authentication
jest.mock('@kinde-oss/kinde-auth-nextjs/server');

describe('createPost', () => {
  const mockUserId = 'user-123';

  beforeEach(() => {
    // Setup mock authenticated user
    (getKindeServerSession as jest.Mock).mockReturnValue({
      getUser: jest.fn().mockResolvedValue({
        id: mockUserId,
        email: 'test@example.com'
      })
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('creates post for authenticated user', async () => {
    const post = await createPost('board-1', 'Content', 'went_well');
    expect(post.userId).toBe(mockUserId);
  });

  it('throws error for unauthenticated user', async () => {
    // Override mock for this test
    (getKindeServerSession as jest.Mock).mockReturnValue({
      getUser: jest.fn().mockResolvedValue(null)
    });

    await expect(
      createPost('board-1', 'Content', 'went_well')
    ).rejects.toThrow('Unauthorized');
  });
});
```

### Factory Patterns for Test Data

**Create Reusable Test Data Generators:**

```typescript
// __tests__/factories/postFactory.ts
import { nanoid } from 'nanoid';

export const createMockPost = (overrides?: Partial<Post>): Post => ({
  id: nanoid(),
  boardId: 'board-123',
  userId: 'user-123',
  content: 'Test post content',
  type: 'went_well',
  voteCount: 0,
  createdAt: new Date(),
  ...overrides
});

export const createMockPosts = (count: number): Post[] =>
  Array.from({ length: count }, () => createMockPost());

// Usage in tests
it('filters posts by type', () => {
  const posts = [
    createMockPost({ type: 'went_well' }),
    createMockPost({ type: 'to_improve' }),
    createMockPost({ type: 'went_well' })
  ];

  const filtered = filterPostsByType(posts, 'went_well');
  expect(filtered).toHaveLength(2);
});
```

### Testing Real-Time Message Processors

**Pattern with Fake Timers:**

```typescript
// lib/realtime/__tests__/messageProcessors.test.ts
import { processPostUpdate } from '../messageProcessors';

describe('Message Processors', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();  // ✅ Use fake timers for time-dependent tests
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('processes valid messages', () => {
    const validMessage = {
      type: 'post:update',
      postId: 'post-123',
      content: 'Updated content',
      userId: 'user-123',
      timestamp: Date.now()
    };

    expect(() => processPostUpdate(validMessage)).not.toThrow();
  });

  it('rejects stale messages', () => {
    const consoleSpy = jest.spyOn(console, 'warn').mockImplementation();

    const staleMessage = {
      type: 'post:update',
      postId: 'post-123',
      content: 'Old content',
      userId: 'user-123',
      timestamp: Date.now() - 35000  // 35 seconds ago
    };

    processPostUpdate(staleMessage);

    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining('Stale message'),
      expect.any(Object)
    );

    consoleSpy.mockRestore();
  });

  it('validates message structure', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

    const invalidMessage = {
      type: 'post:update',
      // Missing required fields
    };

    processPostUpdate(invalidMessage);

    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining('Invalid message'),
      expect.objectContaining({ details: expect.any(Array) })
    );

    consoleSpy.mockRestore();
  });
});
```

### Testing with Signals

**Reset Signal State:**

```typescript
import { postsSignal, filterSignal } from '@/lib/signal/postSignals';
import { createMockPost } from './factories/postFactory';

describe('Post Signals', () => {
  beforeEach(() => {
    // ✅ Reset signals before each test
    postsSignal.value = [];
    filterSignal.value = 'all';
  });

  it('filters posts correctly', () => {
    postsSignal.value = [
      createMockPost({ type: 'went_well' }),
      createMockPost({ type: 'to_improve' })
    ];

    filterSignal.value = 'went_well';

    expect(filteredPosts.value).toHaveLength(1);
    expect(filteredPosts.value[0].type).toBe('went_well');
  });
});
```

### Mocking External Services

**Ably Mock:**

```typescript
// Mock Ably
jest.mock('ably/react', () => ({
  useChannel: jest.fn(() => ({
    channel: {
      publish: jest.fn(),
      subscribe: jest.fn(),
      unsubscribe: jest.fn()
    }
  })),
  useConnectionStateListener: jest.fn()
}));

it('publishes message to channel', () => {
  const { result } = renderHook(() => usePostUpdates());

  result.current.publishUpdate('post-123', 'New content');

  expect(mockPublish).toHaveBeenCalledWith(
    'post:update',
    expect.objectContaining({
      postId: 'post-123',
      content: 'New content'
    })
  );
});
```

**Database Mock:**

```typescript
// Mock Drizzle
jest.mock('@/db', () => ({
  db: {
    query: {
      postTable: {
        findFirst: jest.fn(),
        findMany: jest.fn()
      }
    },
    insert: jest.fn(() => ({
      values: jest.fn(() => ({
        returning: jest.fn()
      }))
    }))
  }
}));
```

### Testing Async Operations

**Pattern with Promises:**

```typescript
it('handles async server action', async () => {
  const result = await createPost('board-1', 'Content', 'went_well');

  expect(result).toBeDefined();
  expect(result.id).toBeTruthy();
});

it('handles async errors', async () => {
  // Mock failure
  jest.spyOn(db, 'insert').mockRejectedValue(new Error('DB Error'));

  await expect(
    createPost('board-1', 'Content', 'went_well')
  ).rejects.toThrow('DB Error');
});
```

## Anti-Patterns

### ❌ Not Cleaning Up Mocks

**Bad:**
```typescript
describe('Tests', () => {
  it('test 1', () => {
    jest.spyOn(console, 'log').mockImplementation();
    // ❌ Never restored
  });

  it('test 2', () => {
    // console.log still mocked!
  });
});
```

**Good:**
```typescript
describe('Tests', () => {
  it('test 1', () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    // test code
    consoleSpy.mockRestore();  // ✅ Cleaned up
  });

  // OR use afterEach
  afterEach(() => {
    jest.restoreAllMocks();
  });
});
```

### ❌ Testing Implementation Details

**Bad:**
```typescript
it('uses Array.filter internally', () => {
  const filterSpy = jest.spyOn(Array.prototype, 'filter');
  filterPosts(posts, 'went_well');
  expect(filterSpy).toHaveBeenCalled();  // ❌ Tests implementation
});
```

**Good:**
```typescript
it('returns only went_well posts', () => {
  const filtered = filterPosts(posts, 'went_well');
  expect(filtered.every(p => p.type === 'went_well')).toBe(true);  // ✅ Tests behavior
});
```

### ❌ Not Using Fake Timers for Time-Dependent Tests

**Bad:**
```typescript
it('filters stale messages', async () => {
  const oldMessage = { timestamp: Date.now() - 35000 };
  // ❌ Test depends on real time passage
  await new Promise(resolve => setTimeout(resolve, 100));
  expect(isStale(oldMessage)).toBe(true);
});
```

**Good:**
```typescript
it('filters stale messages', () => {
  jest.useFakeTimers();
  const now = Date.now();
  const oldMessage = { timestamp: now - 35000 };

  jest.setSystemTime(now);
  expect(isStale(oldMessage)).toBe(true);  // ✅ Deterministic

  jest.useRealTimers();
});
```

### ❌ Shared State Between Tests

**Bad:**
```typescript
let sharedState = [];  // ❌ Shared between tests

it('test 1', () => {
  sharedState.push(1);
  expect(sharedState).toHaveLength(1);
});

it('test 2', () => {
  // Fails because sharedState has item from test 1
  expect(sharedState).toHaveLength(0);
});
```

**Good:**
```typescript
describe('Tests', () => {
  let testState: number[];

  beforeEach(() => {
    testState = [];  // ✅ Reset before each test
  });

  it('test 1', () => {
    testState.push(1);
    expect(testState).toHaveLength(1);
  });

  it('test 2', () => {
    expect(testState).toHaveLength(0);  // ✅ Passes
  });
});
```

## Integration with Other Skills

- **[nextjs-app-router](../nextjs-app-router/SKILL.md):** Test server actions and components
- **[rbac-security](../rbac-security/SKILL.md):** Mock authentication in tests
- **[drizzle-patterns](../drizzle-patterns/SKILL.md):** Mock database operations
- **[ably-realtime](../ably-realtime/SKILL.md):** Test message processors
- **[signal-state-management](../signal-state-management/SKILL.md):** Reset signals in tests

## Project-Specific Context

### Key Files
- `jest.config.js` - Jest configuration
- `lib/realtime/__tests__/` - Message processor tests
- `lib/utils/md5.test.ts` - Example utility test

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  }
};
```

### Running Tests

```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test lib/utils/md5.test.ts

# Run in watch mode
pnpm test --watch

# Run with coverage
pnpm test --coverage
```

### Common Test Patterns in Project

**Message Processor Test:**
```typescript
describe('processPostUpdate', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('processes valid message', () => {
    const message = createValidMessage();
    expect(() => processPostUpdate(message)).not.toThrow();
  });
});
```

**Server Action Test:**
```typescript
describe('createPost', () => {
  beforeEach(() => {
    mockKindeAuth();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('creates post', async () => {
    const post = await createPost(boardId, content, type);
    expect(post).toBeDefined();
  });
});
```

---

**Last Updated:** 2026-01-10