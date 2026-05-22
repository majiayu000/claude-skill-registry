---
name: Contract Testing with Pact
description: Consumer-driven contract testing skill using Pact, covering consumer tests, provider verification, Pact Broker integration, and CI/CD workflows.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [pact, contract-testing, consumer-driven, api, microservices, provider-verification]
testingTypes: [contract, api]
frameworks: [pact]
languages: [typescript, java]
domains: [api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Contract Testing with Pact Skill

You are an expert QA engineer specializing in consumer-driven contract testing with Pact. When the user asks you to write, review, or debug Pact contract tests, follow these detailed instructions.

## Core Principles

1. **Consumer-driven** -- The consumer defines the contract; the provider must honor it.
2. **Pact as contract** -- Pact files are the single source of truth for API compatibility.
3. **Independent deployability** -- Contract tests ensure services can be deployed independently.
4. **Broker as hub** -- The Pact Broker mediates contract sharing and verification tracking.
5. **Can-i-deploy** -- Always verify deployment compatibility before deploying to production.

## How Pact Works

```
Consumer Side                    Provider Side
┌─────────────┐                  ┌─────────────┐
│  Consumer    │                  │  Provider   │
│  Test        │                  │  Test       │
│             │                  │             │
│  1. Define   │    Pact File    │  3. Verify   │
│     expected │  ─────────────> │     against  │
│     behavior │                  │     running  │
│             │                  │     service  │
│  2. Generate │                  │             │
│     Pact     │                  │  4. Publish  │
│     file     │                  │     results  │
└─────────────┘                  └─────────────┘
        │                               │
        │       ┌───────────────┐       │
        └──────>│  Pact Broker  │<──────┘
                │               │
                │  Stores pacts │
                │  Tracks       │
                │  verification │
                │  can-i-deploy │
                └───────────────┘
```

## Project Structure (TypeScript Consumer)

```
consumer-service/
  src/
    clients/
      user-api-client.ts
      product-api-client.ts
    models/
      user.model.ts
  tests/
    contract/
      user-api.consumer.pact.spec.ts
      product-api.consumer.pact.spec.ts
    pacts/           <-- Generated Pact files
      consumer-user-service.json
  jest.config.ts
  package.json
```

## Project Structure (TypeScript Provider)

```
provider-service/
  src/
    routes/
      users.routes.ts
    services/
      user.service.ts
  tests/
    contract/
      user-api.provider.pact.spec.ts
    utils/
      provider-states.ts
  jest.config.ts
  package.json
```

## Consumer Test (TypeScript)

### Setup

```bash
npm install --save-dev @pact-foundation/pact
```

### Consumer API Client

```typescript
// src/clients/user-api-client.ts
import axios, { AxiosInstance } from 'axios';

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

export interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

export class UserApiClient {
  private http: AxiosInstance;

  constructor(baseUrl: string) {
    this.http = axios.create({ baseUrl });
  }

  async getUser(id: string): Promise<User> {
    const response = await this.http.get(`/api/users/${id}`);
    return response.data;
  }

  async createUser(data: CreateUserRequest): Promise<User> {
    const response = await this.http.post('/api/users', data);
    return response.data;
  }

  async listUsers(page: number = 1): Promise<{ data: User[]; total: number }> {
    const response = await this.http.get(`/api/users?page=${page}`);
    return response.data;
  }

  async deleteUser(id: string): Promise<void> {
    await this.http.delete(`/api/users/${id}`);
  }
}
```

### Consumer Pact Test

```typescript
// tests/contract/user-api.consumer.pact.spec.ts
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import path from 'path';
import { UserApiClient } from '../../src/clients/user-api-client';

const { like, eachLike, string, uuid, integer, regex } = MatchersV3;

const provider = new PactV3({
  consumer: 'frontend-app',
  provider: 'user-service',
  dir: path.resolve(process.cwd(), 'tests/pacts'),
  logLevel: 'warn',
});

describe('User API Consumer Contract', () => {
  describe('GET /api/users/:id', () => {
    it('should return a user when the user exists', async () => {
      // Arrange: Define the expected interaction
      provider
        .given('a user with ID user-123 exists')
        .uponReceiving('a request to get a user by ID')
        .withRequest({
          method: 'GET',
          path: '/api/users/user-123',
          headers: {
            Accept: 'application/json',
          },
        })
        .willRespondWith({
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: like('user-123'),
            email: regex(/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'user@example.com'),
            name: string('John Doe'),
            role: regex(/^(admin|user|viewer)$/, 'user'),
          },
        });

      // Act & Assert: Execute against the mock provider
      await provider.executeTest(async (mockServer) => {
        const client = new UserApiClient(mockServer.url);
        const user = await client.getUser('user-123');

        expect(user.id).toBe('user-123');
        expect(user.email).toBeDefined();
        expect(user.name).toBeDefined();
        expect(user.role).toBeDefined();
      });
    });

    it('should return 404 when the user does not exist', async () => {
      provider
        .given('no user with ID nonexistent exists')
        .uponReceiving('a request to get a non-existent user')
        .withRequest({
          method: 'GET',
          path: '/api/users/nonexistent',
          headers: {
            Accept: 'application/json',
          },
        })
        .willRespondWith({
          status: 404,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            message: string('User not found'),
            statusCode: integer(404),
          },
        });

      await provider.executeTest(async (mockServer) => {
        const client = new UserApiClient(mockServer.url);

        await expect(client.getUser('nonexistent')).rejects.toThrow();
      });
    });
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const requestBody = {
        email: 'new@example.com',
        name: 'New User',
        password: 'SecurePass123!',
      };

      provider
        .given('the email new@example.com is not taken')
        .uponReceiving('a request to create a new user')
        .withRequest({
          method: 'POST',
          path: '/api/users',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: requestBody,
        })
        .willRespondWith({
          status: 201,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: uuid('550e8400-e29b-41d4-a716-446655440000'),
            email: string('new@example.com'),
            name: string('New User'),
            role: string('user'),
          },
        });

      await provider.executeTest(async (mockServer) => {
        const client = new UserApiClient(mockServer.url);
        const user = await client.createUser(requestBody);

        expect(user.id).toBeDefined();
        expect(user.email).toBe('new@example.com');
        expect(user.name).toBe('New User');
      });
    });
  });

  describe('GET /api/users', () => {
    it('should return a paginated list of users', async () => {
      provider
        .given('there are users in the system')
        .uponReceiving('a request to list users')
        .withRequest({
          method: 'GET',
          path: '/api/users',
          query: { page: '1' },
          headers: {
            Accept: 'application/json',
          },
        })
        .willRespondWith({
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            data: eachLike({
              id: uuid(),
              email: string('user@example.com'),
              name: string('Test User'),
              role: string('user'),
            }),
            total: integer(10),
          },
        });

      await provider.executeTest(async (mockServer) => {
        const client = new UserApiClient(mockServer.url);
        const result = await client.listUsers(1);

        expect(result.data.length).toBeGreaterThan(0);
        expect(result.total).toBeGreaterThanOrEqual(result.data.length);
      });
    });
  });
});
```

## Provider Verification (TypeScript)

```typescript
// tests/contract/user-api.provider.pact.spec.ts
import { Verifier } from '@pact-foundation/pact';
import path from 'path';
import { app } from '../../src/app'; // Your Express/Fastify app

describe('User Service Provider Contract Verification', () => {
  let server: any;

  beforeAll(async () => {
    server = app.listen(3001);
  });

  afterAll(async () => {
    server.close();
  });

  it('should validate the expectations of the frontend-app consumer', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3001',
      provider: 'user-service',

      // Option 1: From local pact files
      pactUrls: [
        path.resolve(process.cwd(), '../consumer-service/tests/pacts/frontend-app-user-service.json'),
      ],

      // Option 2: From Pact Broker
      // pactBrokerUrl: 'https://your-broker.pactflow.io',
      // pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      // consumerVersionSelectors: [
      //   { mainBranch: true },
      //   { deployedOrReleased: true },
      // ],

      // Provider states setup
      stateHandlers: {
        'a user with ID user-123 exists': async () => {
          // Seed the database with test data
          await db.users.create({
            id: 'user-123',
            email: 'user@example.com',
            name: 'John Doe',
            role: 'user',
          });
          return { description: 'User user-123 created' };
        },

        'no user with ID nonexistent exists': async () => {
          // Ensure the user does not exist
          await db.users.deleteMany({ id: 'nonexistent' });
          return { description: 'Ensured user does not exist' };
        },

        'the email new@example.com is not taken': async () => {
          await db.users.deleteMany({ email: 'new@example.com' });
          return { description: 'Email new@example.com is available' };
        },

        'there are users in the system': async () => {
          await db.users.createMany({
            data: [
              { id: 'user-1', email: 'u1@example.com', name: 'User 1', role: 'user' },
              { id: 'user-2', email: 'u2@example.com', name: 'User 2', role: 'admin' },
            ],
          });
          return { description: 'Seeded 2 users' };
        },
      },

      // Publish verification results
      publishVerificationResult: process.env.CI === 'true',
      providerVersion: process.env.GIT_COMMIT || '1.0.0',
      providerVersionBranch: process.env.GIT_BRANCH || 'main',

      // Logging
      logLevel: 'warn',
    });

    await verifier.verifyProvider();
  });
});
```

## Java Consumer (JUnit 5 + Pact)

```java
package com.example.consumer;

import au.com.dius.pact.consumer.dsl.PactDslJsonBody;
import au.com.dius.pact.consumer.dsl.PactDslWithProvider;
import au.com.dius.pact.consumer.junit5.PactConsumerTestExt;
import au.com.dius.pact.consumer.junit5.PactTestFor;
import au.com.dius.pact.consumer.MockServer;
import au.com.dius.pact.core.model.V4Pact;
import au.com.dius.pact.core.model.annotations.Pact;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "user-service")
public class UserApiConsumerPactTest {

    @Pact(consumer = "frontend-app")
    public V4Pact getUserByIdPact(PactDslWithProvider builder) {
        return builder
            .given("a user with ID user-123 exists")
            .uponReceiving("a request to get user by ID")
            .path("/api/users/user-123")
            .method("GET")
            .headers("Accept", "application/json")
            .willRespondWith()
            .status(200)
            .headers(Map.of("Content-Type", "application/json"))
            .body(new PactDslJsonBody()
                .stringType("id", "user-123")
                .stringMatcher("email", "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$", "user@example.com")
                .stringType("name", "John Doe")
                .stringMatcher("role", "^(admin|user|viewer)$", "user")
            )
            .toPact(V4Pact.class);
    }

    @Test
    @PactTestFor(pactMethod = "getUserByIdPact")
    void testGetUserById(MockServer mockServer) {
        UserApiClient client = new UserApiClient(mockServer.getUrl());
        User user = client.getUser("user-123");

        assertThat(user.getId()).isEqualTo("user-123");
        assertThat(user.getEmail()).isNotEmpty();
        assertThat(user.getName()).isNotEmpty();
    }
}
```

## Java Provider Verification

```java
package com.example.provider;

import au.com.dius.pact.provider.junit5.PactVerificationContext;
import au.com.dius.pact.provider.junit5.PactVerificationInvocationContextProvider;
import au.com.dius.pact.provider.junitsupport.*;
import au.com.dius.pact.provider.junitsupport.loader.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestTemplate;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Provider("user-service")
@PactBroker(
    url = "${PACT_BROKER_URL}",
    authentication = @PactBrokerAuth(token = "${PACT_BROKER_TOKEN}")
)
public class UserApiProviderPactTest {

    @LocalServerPort
    private int port;

    @BeforeEach
    void setUp(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", port));
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verifyPact(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("a user with ID user-123 exists")
    void userExists() {
        userRepository.save(new User("user-123", "user@example.com", "John Doe", "user"));
    }

    @State("no user with ID nonexistent exists")
    void userDoesNotExist() {
        userRepository.deleteById("nonexistent");
    }

    @State("the email new@example.com is not taken")
    void emailAvailable() {
        userRepository.deleteByEmail("new@example.com");
    }
}
```

## Pact Broker Integration

### Publishing Pacts

```bash
# Using Pact CLI
pact-broker publish ./tests/pacts \
  --consumer-app-version=$(git rev-parse --short HEAD) \
  --branch=$(git rev-parse --abbrev-ref HEAD) \
  --broker-base-url=https://your-broker.pactflow.io \
  --broker-token=${PACT_BROKER_TOKEN}
```

### Can-I-Deploy

```bash
# Check if consumer can deploy
pact-broker can-i-deploy \
  --pacticipant=frontend-app \
  --version=$(git rev-parse --short HEAD) \
  --to-environment=production \
  --broker-base-url=https://your-broker.pactflow.io \
  --broker-token=${PACT_BROKER_TOKEN}

# Check if provider can deploy
pact-broker can-i-deploy \
  --pacticipant=user-service \
  --version=$(git rev-parse --short HEAD) \
  --to-environment=production \
  --broker-base-url=https://your-broker.pactflow.io \
  --broker-token=${PACT_BROKER_TOKEN}
```

### Record Deployment

```bash
# After successful deployment
pact-broker record-deployment \
  --pacticipant=user-service \
  --version=$(git rev-parse --short HEAD) \
  --environment=production \
  --broker-base-url=https://your-broker.pactflow.io \
  --broker-token=${PACT_BROKER_TOKEN}
```

## CI/CD Integration

### Consumer CI Pipeline

```yaml
name: Consumer Contract Tests
on: [push, pull_request]

jobs:
  consumer-contract-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci
      - run: npm run test:contract

      - name: Publish Pacts
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker publish tests/pacts \
            --consumer-app-version=${{ github.sha }} \
            --branch=${{ github.ref_name }} \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}

      - name: Can I Deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant=frontend-app \
            --version=${{ github.sha }} \
            --to-environment=production \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
```

### Provider CI Pipeline

```yaml
name: Provider Contract Verification
on:
  push:
    branches: [main]
  # Webhook trigger from Pact Broker when new pacts are published
  repository_dispatch:
    types: [pact-changed]

jobs:
  provider-verification:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      - name: Verify Provider Contracts
        run: npm run test:provider-contract
        env:
          PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
          GIT_COMMIT: ${{ github.sha }}
          GIT_BRANCH: ${{ github.ref_name }}
          CI: true

      - name: Can I Deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant=user-service \
            --version=${{ github.sha }} \
            --to-environment=production \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
```

## Pact Matchers Reference

```typescript
import { MatchersV3 } from '@pact-foundation/pact';

const {
  like,           // Match by type, not exact value
  eachLike,       // Array where each element matches the example
  string,         // String type matcher
  integer,        // Integer type matcher
  decimal,        // Decimal type matcher
  boolean,        // Boolean type matcher
  uuid,           // UUID format matcher
  datetime,       // Date-time format matcher
  date,           // Date format matcher
  time,           // Time format matcher
  regex,          // Regex pattern matcher
  fromProviderState, // Value from provider state
  arrayContaining,   // Array contains these elements (in any order)
  atLeastOneLike,    // Array with at least N elements matching
} = MatchersV3;

// Examples
const body = {
  id: uuid(),
  name: string('John'),
  age: integer(30),
  score: decimal(95.5),
  active: boolean(true),
  email: regex(/^.+@.+\..+$/, 'john@example.com'),
  createdAt: datetime("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", '2024-01-15T10:30:00.000Z'),
  tags: eachLike('tag1'),
  address: like({
    street: string('123 Main St'),
    city: string('Anytown'),
  }),
};
```

## Best Practices

1. **Test the contract, not the implementation** -- Pact tests verify the API shape, not business logic.
2. **Use matchers, not exact values** -- `like()` and `regex()` make contracts resilient.
3. **Keep provider states minimal** -- Just enough to make the interaction work.
4. **Run can-i-deploy before every deployment** -- It is your safety net against breaking changes.
5. **Publish verification results from CI** -- Not from local machines.
6. **Use consumer version selectors** -- Target `mainBranch` and `deployedOrReleased` pacts.
7. **Tag versions in the broker** -- Tag deployed versions to track what is in each environment.
8. **Test error scenarios** -- Include 404, 400, and 401 interactions.
9. **Version pacts by git commit** -- Use `git rev-parse --short HEAD` as the version.
10. **Automate webhook triggers** -- Configure the Pact Broker to trigger provider verification on new pacts.

## Anti-Patterns to Avoid

1. **Using Pact as an integration test** -- Pact tests run against mocks, not real services.
2. **Exact value matching everywhere** -- Makes contracts brittle; use type matchers.
3. **Testing every field combination** -- One interaction per use case is enough.
4. **Sharing pact files via email/chat** -- Use a Pact Broker for proper lifecycle management.
5. **Skipping provider states** -- Without states, provider tests fail unpredictably.
6. **Not publishing verification results** -- The broker cannot track compatibility without results.
7. **Ignoring can-i-deploy** -- Deploying without checking compatibility causes outages.
8. **Consumer testing provider internals** -- Test only what the consumer actually uses.
9. **One giant pact file** -- Organize interactions by consumer feature/use case.
10. **Not testing error responses** -- Consumers must handle errors correctly.
