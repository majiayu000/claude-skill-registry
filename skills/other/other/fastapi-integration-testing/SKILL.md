---
name: fastapi-integration-testing
description: >-
  Provides a comprehensive guide and templates for creating integration tests for
  FastAPI applications. Use this skill when you need to set up or write integration
  tests involving a database, authentication, file uploads, or error handling.
  It includes patterns for pytest fixtures, test client usage, and test data factories.

---

# FastAPI Integration Testing Skill

This skill provides patterns, templates, and guides for writing robust integration tests for your FastAPI application.

## Core Concepts

The approach is centered around `pytest` and uses:
-   A real database (SQLite by default) for data-dependent tests.
-   Transaction-based cleanup to ensure test isolation.
-   FastAPI's `TestClient` for making requests to the application.
-   Fixtures for setting up test context (like database sessions and authenticated clients).
-   Factories for generating test data.

## Getting Started: The Workflow

1.  **Setup Your Test Environment**: Configure your `conftest.py` to manage the test database and provide a `TestClient`.
    -   **See**: `references/setup.md`
    -   **Template**: `assets/conftest_template.py`

2.  **Write Your First Test**: Create a test file and write a simple test for a public endpoint.
    -   **See**: `references/testing_endpoints.md`
    -   **Template**: `assets/test_api_template.py`

## Advanced Testing Scenarios

Once you have the basic setup, you can tackle more complex scenarios.

### Testing Protected Endpoints
To test endpoints that require authentication, create a fixture that provides a pre-authenticated client.
-   **Guide**: `references/authentication.md`

### Testing File Uploads
Learn how to use the `TestClient` to simulate file uploads in your tests.
-   **Guide**: `references/file_uploads.md`

### Verifying Error Responses
Ensure your application returns correct and informative errors for bad requests or missing resources.
-   **Guide**: `references/error_responses.md`

### Generating Test Data
Use the factory pattern to easily create test data for your models. This is highly recommended for complex applications.
-   **Guide**: `references/factories.md`
