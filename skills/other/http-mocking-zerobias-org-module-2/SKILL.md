---
name: http-mocking
description: HTTP mocking with nock - the only allowed mocking library
---

# Nock HTTP Mocking Patterns

## Critical Rule: ONLY nock for HTTP Mocking

**This is a CRITICAL rule that MUST be enforced:**

✅ **ONLY `nock`** is allowed for HTTP mocking
❌ **NEVER** use `jest.mock`, `sinon`, or `fetch-mock`

See failure-conditions skill Rule 4 for enforcement.

## Core Principles

1. **Mock at HTTP level** - Mock the network request, not internal methods
2. **Match requests accurately** - Include method, path, headers, query params
3. **Return realistic responses** - Use response formats matching real API
4. **Clean up after tests** - Use `afterEach(() => nock.cleanAll())`
5. **Verify mocks called** - Assert `expect(nock.isDone()).toBe(true)`

## Basic HTTP Mock Pattern

```typescript
import nock from 'nock';

describe('WebhookProducer', () => {
  afterEach(() => {
    nock.cleanAll();  // Clean up after each test
  });

  it('should list webhooks successfully', async () => {
    // Mock the HTTP request
    nock('https://api.github.com')
      .get('/repos/octocat/Hello-World/hooks')
      .reply(200, [
        {
          id: '12345678',
          name: 'web',
          active: true,
          events: ['push', 'pull_request'],
          config: {
            url: 'https://example.com/webhook',
            content_type: 'json'
          },
          created_at: '2024-01-01T00:00:00Z'
        }
      ]);

    // Execute the test
    const producer = new WebhookProducer(httpClient);
    const webhooks = await producer.list('octocat', 'Hello-World');

    // Assertions
    expect(webhooks).toHaveLength(1);
    expect(webhooks[0].id).toBeDefined();
    expect(nock.isDone()).toBe(true);  // Verify mock was called
  });
});
```

## Mock with Request Headers

```typescript
nock('https://api.github.com', {
  reqheaders: {
    'Authorization': 'Bearer test-token',
    'Accept': 'application/vnd.github.v3+json'
  }
})
  .get('/repos/octocat/Hello-World/hooks')
  .reply(200, mockData);
```

## Mock Error Responses

```typescript
it('should handle 404 error', async () => {
  nock('https://api.github.com')
    .get('/repos/octocat/Hello-World/hooks/999')
    .reply(404, {
      message: 'Not Found',
      documentation_url: 'https://docs.github.com/rest'
    });

  // Test error handling
  await expect(
    producer.get('octocat', 'Hello-World', '999')
  ).rejects.toThrow(ResourceNotFoundError);

  expect(nock.isDone()).toBe(true);
});
```

## Mock POST Request

```typescript
it('should create webhook', async () => {
  const requestBody = {
    name: 'web',
    config: {
      url: 'https://example.com/webhook',
      content_type: 'json'
    },
    events: ['push'],
    active: true
  };

  nock('https://api.github.com')
    .post('/repos/octocat/Hello-World/hooks', requestBody)
    .reply(201, {
      id: '12345678',
      ...requestBody,
      created_at: '2024-01-01T00:00:00Z'
    });

  const webhook = await producer.create('octocat', 'Hello-World', config);

  expect(webhook.id).toBeDefined();
  expect(nock.isDone()).toBe(true);
});
```

## Mock with Query Parameters

```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks')
  .query({ per_page: 20, page: 1 })
  .reply(200, mockData);
```

## Reusable Mock Fixtures

```typescript
// test/fixtures/webhookMocks.ts
export const mockWebhookResponse = {
  id: '12345678',
  name: 'web',
  active: true,
  events: ['push', 'pull_request'],
  config: {
    url: 'https://example.com/webhook',
    content_type: 'json'
  },
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z'
};

export function mockListWebhooks(owner: string, repo: string, data: any[]) {
  return nock('https://api.github.com')
    .get(`/repos/${owner}/${repo}/hooks`)
    .reply(200, data);
}
```

## Validation Checklist

```bash
# Verify ONLY nock is used
grep "from ['\"]nock['\"]" test/unit/*.ts
# Should show nock imports

# Ensure NO forbidden mocking libraries
grep -E "jest\.mock|sinon|fetch-mock" test/*.ts
# Should return nothing (exit code 1)

# Verify mock cleanup present
grep "nock.cleanAll()" test/unit/*.ts
# Should show in afterEach blocks

# Verify mock verification present
grep "nock.isDone()" test/unit/*.ts
# Should show in test assertions
```

## Anti-Patterns: What NOT to Do

### ❌ WRONG: Using jest.mock

```typescript
// ❌ NO! Don't mock at method level
jest.mock('./WebhookProducer');
```

**Why wrong:** Mocks internal implementation instead of HTTP layer.

### ❌ WRONG: Using sinon

```typescript
// ❌ NO! Don't use sinon
import sinon from 'sinon';
const stub = sinon.stub(producer, 'list');
```

**Why wrong:** Not allowed - violates testing rules.

### ❌ WRONG: Using fetch-mock

```typescript
// ❌ NO! Use nock instead
import fetchMock from 'fetch-mock';
```

**Why wrong:** Not allowed - only nock is permitted.

### ✅ CORRECT: Using nock

```typescript
// ✅ YES! Mock at HTTP level with nock
import nock from 'nock';
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks')
  .reply(200, mockData);
```

**Why correct:** Mocks at HTTP level using approved library.

## Standard Output Format

When documenting HTTP mocking strategy:

```markdown
# HTTP Mocking Strategy: {ProducerName}

## Mock Library
✅ **nock** (ONLY allowed library)

## Mock Patterns Created

### List Operation
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks')
  .reply(200, [mockWebhookResponse]);
```

### Get Operation
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks/12345678')
  .reply(200, mockWebhookResponse);
```

### Error Case
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks/999')
  .reply(404, { message: 'Not Found' });
```

## Mock Cleanup
✅ afterEach(() => nock.cleanAll())

## Mock Verification
✅ expect(nock.isDone()).toBe(true)

## Validation
✅ Only nock used
✅ HTTP level mocking
✅ Realistic responses
✅ Proper cleanup
✅ Mock verification
```

## Success Criteria

HTTP mocking implementation MUST meet all criteria:

- ✅ Only nock library used (no jest.mock, sinon, fetch-mock)
- ✅ All HTTP requests mocked at network level
- ✅ Realistic mock responses (match API format)
- ✅ Proper cleanup after tests (`nock.cleanAll()`)
- ✅ Mock verification in tests (`nock.isDone()`)
- ✅ Reusable mock patterns/fixtures where appropriate
- ✅ Request matching includes method, path, headers (when relevant)
