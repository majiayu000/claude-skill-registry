---
name: testing-unit
cluster: testing
description: "Unit: Jest/Vitest, pytest, Go test/testify, RSpec, XCTest, JUnit5. Mocking, stubs, isolation"
tags: ["unit-test","jest","pytest","testing"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "unit test jest vitest pytest mock stub isolate rspec xctest"
---

## Purpose

This skill equips the AI to assist with unit testing using frameworks like Jest/Vitest for JavaScript, pytest for Python, Go's testify, RSpec for Ruby, XCTest for Swift, and JUnit5 for Java. It focuses on mocking dependencies, creating stubs, and ensuring test isolation to verify code behavior in controlled environments.

## When to Use

Use this skill when writing new unit tests, debugging existing ones, or refactoring code that requires isolated testing. Apply it for TDD workflows, mocking external APIs or databases, or ensuring functions work independently. For example, use it when a function depends on a network call—mock it to test locally without real dependencies.

## Key Capabilities

- **Mocking**: Create mocks for functions or modules, e.g., in Jest with `jest.mock('module')` to replace real implementations.
- **Stubbing**: Define stub responses, like in pytest using `monkeypatch.setattr()` to fake object methods.
- **Isolation**: Run tests in isolation, such as using Go's testify to assert without side effects, or JUnit5's `@TempDir` for isolated file operations.
- **Framework-Specific**: Support for Jest/Vitest assertions (e.g., `expect().toBe()`), pytest fixtures for setup/teardown, RSpec's `double` for mocks, XCTest's `setUp()` for isolation, and JUnit5's `@Mock` annotations.
- **Config Formats**: Use Jest's `jest.config.js` with `{ testEnvironment: 'node', setupFilesAfterEnv: ['<rootDir>/setupTests.js'] }` for custom mocks; pytest's `pytest.ini` with `[pytest] addopts = -v` for verbose output.

## Usage Patterns

To accomplish unit testing tasks, follow these steps: 1) Identify dependencies to mock (e.g., HTTP calls). 2) Set up mocks or stubs in your test file. 3) Write assertions to verify outputs. 4) Run tests with appropriate flags. For TDD, write a failing test first, then implement code. In Jest, structure tests with `describe()` blocks; in pytest, use fixtures for shared setup. Always isolate tests by avoiding global state—use `beforeEach()` in Jest or `@pytest.fixture(scope='function')` in pytest.

## Common Commands/API

- **Jest/Vitest**: Run tests with `npx jest --watchAll` for interactive mode; mock modules via `jest.mock('axios', () => ({ get: jest.fn().mockResolvedValue({ data: {} }) }));`. API: Use `expect(value).toEqual(expected)` for assertions.
- **pytest**: Execute with `pytest tests/ -v --cov` for coverage; stub functions with `def test_function(monkeypatch): monkeypatch.setattr('module.func', lambda: 'stubbed')`. API: Leverage `@pytest.fixture` for isolation, e.g., `def mock_db(): return {'query': lambda: []}`.
- **Go (testify)**: Build with `go test -v ./...` and use `mock.Mock` from testify; e.g., `mockCtrl := gomock.NewController(t); mockObj := NewMockInterface(mockCtrl); mockObj.EXPECT().Method().Return(value)`.
- **RSpec**: Run via `rspec spec/`; create doubles with `double('Object', method: -> 'stubbed')`. API: Use `expect { code }.to change { something }`.
- **XCTest**: Compile and run with `xcodebuild test`; mock in Swift using `protocol` stubs, e.g., `class MockService: ServiceProtocol { func fetchData() -> Data { return Data() } }`.
- **JUnit5**: Execute via `./gradlew test`; use Mockito with `@ExtendWith(MockitoExtension.class) public class TestClass { @Mock private Dependency dep; @InjectMocks private ClassUnderTest cut; }`. If integrating external services, set env vars like `$API_KEY` for authentication in tests.

## Integration Notes

Integrate this skill by embedding unit tests into CI/CD pipelines, e.g., add Jest to a GitHub Actions workflow with `run: npm test`. For multi-language projects, use a monorepo setup with tools like Nx for Jest and pytest. Configure environment variables for secrets, e.g., export `$DATABASE_URL` in your test runner. Link with code coverage tools like Istanbul for Jest or Coverage.py for pytest; ensure mocks respect these by using `--no-cov` flags when debugging. For API-dependent tests, inject env vars like `$SERVICE_API_KEY` into your test command, e.g., `pytest --api-key=$SERVICE_API_KEY`.

## Error Handling

Handle common errors prescriptively: For assertion failures in Jest, check stack traces and use `jest.fn().mockImplementation()` to debug mocks; if a mock isn't called, add `.toHaveBeenCalled()` assertions. In pytest, catch fixture errors by wrapping in try/except, e.g., `def test_with_fixture(fix): try: fix.setup() except Exception as e: pytest.fail(str(e))`. For Go, use testify's `assert.NoError(t, err)` to fail tests on errors. In RSpec, handle doubles with `allow(double).to receive(:method).and_raise(Error)`. For JUnit5, use `@Test(expected = Exception.class)` for expected failures. Always isolate error-prone code with stubs to prevent cascading failures; rerun with verbose flags like `jest --debug` or `pytest -s` for detailed output.

## Concrete Usage Examples

1. **Jest Mock Example**: To test a function that fetches data, mock the fetch API:  
   `jest.mock('node-fetch'); const fetch = require('node-fetch'); fetch.mockResolvedValue({ json: () => Promise.resolve({ data: 'mocked' }) }); test('fetches data', async () => { expect(await fetchData()).toEqual('mocked'); });`

2. **pytest Fixture Example**: To isolate a database-dependent test, use a fixture:  
   `import pytest @pytest.fixture def mock_db(): return {'query': lambda: [{'id': 1}]} def test_query(mock_db): assert mock_db['query']()[0]['id'] == 1`

## Graph Relationships

- Related to: testing-integration (for broader testing workflows), code-debugging (for fixing test failures)
- Clusters with: testing (as part of the testing cluster), code-execution (for running tests in isolated environments)
- Depends on: environment-setup (for managing test dependencies like mocks)
