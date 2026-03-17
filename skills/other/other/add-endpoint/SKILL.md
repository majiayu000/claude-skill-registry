---
name: add-endpoint
description: Add a new API endpoint following all project standards
---

Add a new API endpoint: $ARGUMENTS

Follow this workflow:

1. **Plan**: Identify which router file the endpoint belongs in (see Routers in project config)

2. **Schema**: Add typed request/response schemas (see stack concepts for schema library) to the models/schemas file if needed
   - All fields explicitly typed — no untyped/any fields
   - Use validation constraints (see stack concepts)

3. **Service**: Add business logic to the service layer if needed
   - Thread-safe with lock mechanism
   - Audit log via the project's audit logger for state changes
   - Typed exceptions for error cases

4. **Route**: Add the endpoint to the router
   - Thin handler — delegate to the service class
   - Use the auth-protected DI dependency for protected endpoints, or the public DI dependency for public endpoints
   - Include route handler metadata: response schema, summary, description, responses (see stack concepts)
   - Static routes before parameterized routes
   - Map domain exceptions to HTTP status codes (see exception mapping in project config)

5. **Tests**: Add tests in the corresponding test file (see test file mapping in project config)
   - Success path test
   - Validation error test (422)
   - Service/device error test (503)

6. **Verify**: Run the test command and the type-check command (see project config)

7. **Docs**: Update project documentation if a new endpoint was added