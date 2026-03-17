---
name: testing-integration
cluster: testing
description: "Integration: API testing Supertest/httpx, test containers, service integration, contract testing Pact"
tags: ["integration-test","api-test","contract-test","testing"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "integration test api supertest database container contract pact"
---

## Purpose
This skill facilitates integration testing for APIs and services, focusing on tools like Supertest (Node.js), httpx (Python), Testcontainers for managing test environments, and Pact for contract testing. It ensures end-to-end verification of service interactions, database integrations, and API contracts.

## When to Use
Use this skill when verifying API endpoints in a real environment, testing service integrations (e.g., with databases or external services), running containerized tests, or enforcing contracts between microservices. Apply it in CI/CD pipelines for regression testing or when mocking dependencies is insufficient.

## Key Capabilities
- Perform HTTP API testing with Supertest for Node.js apps, including mocking and assertions.
- Use httpx in Python for asynchronous HTTP requests and integration with databases.
- Manage test containers via Testcontainers to spin up isolated environments (e.g., Docker-based databases).
- Conduct contract testing with Pact to define and verify API provider-consumer agreements.
- Support for service integration testing, such as linking APIs to external services or databases.

## Usage Patterns
To use this skill, first install required dependencies (e.g., via npm or pip). Set up test files in your project, configure environments with variables like `$API_BASE_URL`, and run tests using a test runner. For API tests, structure code to send requests and assert responses. For contract testing, define pacts in separate files and verify them against providers. Always isolate tests with containers to avoid side effects. Example pattern: Import the tool, define a test function, send requests, and handle assertions within 2-3 lines.

## Common Commands/API
- **Supertest (Node.js)**: Use `supertest` to test Express apps. Command: `npm install supertest`. Code snippet:
  ```javascript
  const request = require('supertest');
  const app = require('./app');
  request(app).get('/api/users').expect(200);
  ```
  CLI flag: Run with `npx jest --runInBand` for sequential tests.
- **httpx (Python)**: For async HTTP testing. Command: `pip install httpx`. Code snippet:
  ```python
  import httpx
  response = httpx.get('http://example.com/api/data', headers={'Authorization': f'Bearer {os.environ.get("API_KEY")}'}).json()
  assert response['status'] == 'success'
  ```
  API endpoint: Pass URLs like `https://api.service.com/endpoint` with query params (e.g., `?limit=10`).
- **Testcontainers**: Spin up containers for integration. Command: Add to pom.xml or requirements. Code snippet:
  ```java
  GenericContainer container = new GenericContainer("postgres:13").withExposedPorts(5432);
  container.start();
  String jdbcUrl = container.getJdbcUrl();
  ```
  Config format: Use Docker image specs in YAML, e.g., `image: postgres:13` with env vars like `$DB_PASSWORD`.
- **Pact (Contract Testing)**: Define and verify contracts. Command: `npm install @pact-foundation/pact` or `pip install pact-python`. Code snippet:
  ```javascript
  const { Pact } = require('@pact-foundation/pact');
  const pact = new Pact({ consumer: 'MyConsumer', provider: 'MyProvider' });
  pact.addInteraction({ state: 'default', uponReceiving: 'a request' });
  ```
  API: Use endpoints like `/pacts/provider/MyProvider/consumer/MyConsumer/verification` for verification, with auth via `$PACT_BROKER_TOKEN`.

## Integration Notes
Integrate this skill by adding it to your build tools: For Node.js, include in Jest or Mocha configs; for Python, use pytest fixtures. Set env vars like `$DATABASE_URL` for database connections or `$SERVICE_API_KEY` for authenticated requests. For container integration, ensure Docker is installed and use Testcontainers to link services (e.g., expose ports via `withExposedPorts(8080)`). When combining with Pact, publish pacts to a broker (e.g., via `pact-broker publish --broker-url=$PACT_BROKER_URL`). Config format: Use JSON for Pact files, e.g., `{ "interactions": [...] }`, and ensure compatibility with CI tools like GitHub Actions by adding steps like `run: docker-compose up -d`.

## Error Handling
Handle errors by wrapping requests in try-catch blocks. For Supertest, check response status and body: e.g., if `.expect(200)` fails, log the error with `console.error(response.error)`. In httpx, catch `httpx.HTTPError` for network issues, e.g.:
```python
try:
    response = httpx.get(url)
    response.raise_for_status()
except httpx.HTTPError as e:
    print(f"Error: {e} - Check $API_BASE_URL")
```
For Testcontainers, verify container startup with `container.isRunning()` before tests. In Pact, use `pact.verify()` and handle mismatches by reviewing pact files. Common patterns: Use env vars for retries (e.g., `$RETRY_COUNT=3`) and log detailed errors with stack traces.

## Concrete Usage Examples
1. **API Integration Test with Supertest**: To test a user endpoint in a Node.js app with a database, first set `$DB_URL=postgres://user:pass@localhost:5432/db`. Write a test file: Import Supertest, send a GET request, and assert the response. Run with `npx jest tests/integration.test.js`. This verifies the API connects to the database and returns data.
   
2. **Contract Test with Pact**: For a consumer-provider setup, define a pact in a file (e.g., `pacts/my-pact.json`) with interactions. Use `pact.verify()` against the provider endpoint (e.g., `http://provider.com`), passing `$PACT_BROKER_TOKEN`. Run via `npx pact-verifier --provider-base-url=$PROVIDER_URL`. This ensures the consumer's expectations match the provider's implementation.

## Graph Relationships
- Related to cluster: "testing" (e.g., shares tags with unit-testing skills).
- Connected to skills: "api-development" via integration-test tag for API workflows.
- Links to: "contract-management" through contract-test tag for Pact-based verification.
- Associated with: "database-integration" due to test containers for database testing.
