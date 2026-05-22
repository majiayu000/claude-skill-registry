---
name: api-contract-testing
description: Verifies API contracts between services using consumer-driven contracts, schema validation, and tools like Pact. Use when testing microservices communication, preventing breaking changes, or validating OpenAPI specifications.
---

# API Contract Testing

Verify that APIs honor their contracts between consumers and providers without requiring full integration tests.

## Key Concepts

| Term | Definition |
|------|------------|
| Consumer | Service that calls an API |
| Provider | Service that exposes an API |
| Contract | Agreed request/response format |
| Pact | Consumer-driven contract testing tool |
| Schema | Structure definition (OpenAPI, JSON Schema) |
| Broker | Central repository for contracts |

## Pact Consumer Test (TypeScript)

```typescript
import { PactV3, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'UserService'
});

describe('User API Contract', () => {
  it('returns user by ID', async () => {
    await provider
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({ method: 'GET', path: '/users/123' })
      .willRespondWith({
        status: 200,
        body: MatchersV3.like({
          id: '123',
          name: MatchersV3.string('John'),
          email: MatchersV3.email('john@example.com')
        })
      })
      .executeTest(async (mockServer) => {
        const response = await fetch(`${mockServer.url}/users/123`);
        expect(response.status).toBe(200);
      });
  });

  it('returns 404 for non-existent user', async () => {
    await provider
      .given('user does not exist')
      .uponReceiving('a request for non-existent user')
      .withRequest({ method: 'GET', path: '/users/999' })
      .willRespondWith({
        status: 404,
        body: MatchersV3.like({
          error: { code: 'NOT_FOUND', message: MatchersV3.string() }
        })
      })
      .executeTest(async (mockServer) => {
        const response = await fetch(`${mockServer.url}/users/999`);
        expect(response.status).toBe(404);
      });
  });
});
```

## Provider Verification

```typescript
import { Verifier } from '@pact-foundation/pact';

new Verifier({
  provider: 'UserService',
  providerBaseUrl: 'http://localhost:3000',
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  publishVerificationResult: true,
  providerVersion: process.env.GIT_SHA,
  stateHandlers: {
    'user 123 exists': async () => {
      await db.users.create({ id: '123', name: 'John' });
    },
    'user does not exist': async () => {
      await db.users.deleteAll();
    }
  }
}).verifyProvider();
```

## OpenAPI Validation (Express)

```javascript
const OpenApiValidator = require('express-openapi-validator');

app.use(OpenApiValidator.middleware({
  apiSpec: './openapi.yaml',
  validateRequests: true,
  validateResponses: true,
  validateSecurity: true
}));
```

## Additional Implementations

- **Python JSON Schema**: See [references/python-json-schema.md](references/python-json-schema.md)
- **Java REST Assured**: See [references/java-rest-assured.md](references/java-rest-assured.md)
- **Pact Broker CI/CD**: See [references/pact-broker-cicd.md](references/pact-broker-cicd.md)

## Best Practices

**Do:**
- Test from consumer perspective
- Use matchers for flexible matching
- Validate structure, not specific values
- Version contracts explicitly
- Test error responses
- Run tests in CI pipeline
- Test backward compatibility

**Don't:**
- Test business logic in contracts
- Hard-code specific values
- Skip error scenarios
- Ignore versioning
- Deploy without verification

## Tools

- **Pact** - Multi-language consumer-driven contracts
- **Spring Cloud Contract** - JVM ecosystem
- **OpenAPI/Swagger** - Schema-first validation
- **Dredd** - API blueprint testing
- **Spectral** - OpenAPI linting
