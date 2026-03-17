---
name: api-integration-test-scaffolder
description: "Generates integration tests for frontend → backend → Genkit flow connections. Use when creating E2E API tests."
---

# API Integration Test Scaffolder Workflow

This skill creates comprehensive integration tests that validate the complete data flow from frontend to backend to AI flows.

## Workflow Steps

1. **Identify integration to test:**
   - Ask for frontend service function (e.g., `aiServices.generateKscResponses`)
   - Find corresponding backend endpoint
   - Identify associated Genkit flow (if any)
   - Determine test scenario (success, validation, error)

2. **Generate integration test file:**
   - Read template: `.claude/skills/api-integration-test-scaffolder/templates/integration_test.py.tpl`
   - Replace placeholders:
     - `{{TEST_NAME}}` - Descriptive test name
     - `{{ENDPOINT_PATH}}` - API endpoint path
     - `{{REQUEST_DATA}}` - Sample request payload
     - `{{EXPECTED_RESPONSE}}` - Expected response structure
     - `{{GENKIT_FLOW}}` - Associated Genkit flow name
   - Write to: `backend/app/tests/integration/test_{{feature_name}}_integration.py`

3. **Include test scenarios:**
   - ✅ **Happy path**: Valid request → successful response
   - ⚠️ **Validation**: Invalid data → 422 validation error
   - 🔒 **Authentication**: Unauthorized → 401 error
   - ❌ **Error handling**: Server error → 500 with proper message
   - 🔄 **Genkit flow**: Verify flow execution and caching
   - 📊 **Response validation**: Type checking, required fields

4. **Add mock setup:**
   - Mock Firebase Auth dependencies
   - Mock Genkit flow responses (optional)
   - Mock external services (email, storage, etc.)
   - Set up test database/Firestore

5. **Report success:**
   - Show test file path
   - Display test coverage (scenarios included)
   - Provide command to run tests
   - Show example test execution output

## Template Structure

```python
# backend/app/tests/integration/test_{{FEATURE}}_integration.py

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.{{MODEL}} import {{REQUEST_MODEL}}, {{RESPONSE_MODEL}}


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class Test{{FEATURE}}Integration:
    \"\"\"Integration tests for {{FEATURE}} frontend → backend → flow.\"\"\"

    @patch("app.core.dependencies.get_current_user")
    async def test_complete_flow_success(self, mock_auth, async_client):
        # Test implementation
        pass

    # Additional test methods...
```

## Example Usage

```
User: Create an integration test for the KSC generation feature
Assistant: I'll create a comprehensive integration test...

Files created:
- backend/app/tests/integration/test_ksc_generation_integration.py

Test scenarios included:
✅ Happy path: Valid job description → KSC responses
⚠️ Validation: Empty job description → 422 error
🔒 Authentication: No auth token → 401 error
🔄 Genkit flow: Verify generateKscResponse flow execution
📊 Response validation: Check response structure and types

Run tests:
pytest backend/app/tests/integration/test_ksc_generation_integration.py -v
```
