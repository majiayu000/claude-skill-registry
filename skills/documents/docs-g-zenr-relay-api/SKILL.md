---
name: docs
description: Update all project documentation to match current codebase (Sofia Nakamura's workflow)
disable-model-invocation: true
---

Update project documentation: $ARGUMENTS

Follow Sofia Nakamura's documentation standards:

1. **Audit current state**: Read all documentation files and compare against actual codebase
   - Project README — API endpoints table, configuration table, examples
   - Env example file — every setting with description and default
   - App factory description block — feature list and usage info
   - OpenAPI metadata on every endpoint (summary, description, responses)

2. **README updates**:
   - API Endpoints table MUST match actual routes in the API layer
   - Configuration table MUST match all fields in the config file's Settings class
   - Examples MUST work with current API
   - Architecture diagram MUST match actual file structure
   - Docker section MUST match current Dockerfile

3. **Env example file updates**:
   - Every field in the config file's Settings class MUST have a corresponding line
   - Each variable has a comment explaining purpose, options, and default
   - Group by category

4. **OpenAPI metadata**:
   - Every endpoint in the API layer MUST have `summary` and `description`
   - Every endpoint MUST declare `responses` with status codes and models
   - Check by visiting the docs endpoint or reading route decorators

5. **API description** in the app factory:
   - Description string MUST list all current features
   - Authentication section matches actual auth behavior
   - Rate limiting section matches actual middleware behavior

6. **Output**: List every change made and every discrepancy found