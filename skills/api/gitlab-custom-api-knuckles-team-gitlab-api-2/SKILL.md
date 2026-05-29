---
name: gitlab-custom-api
description: "Handles custom GitLab API requests. Use for any endpoint not covered by other skills. Triggers: advanced API calls, extensions."
---

### Overview
Fallback for arbitrary requests.

### Available Tools
- `api_request`: Make a custom API request to a GitLab instance.
  - **Parameters**:
    - `method` (str): Optional. - The HTTP method to use ('GET', 'POST', 'PUT', 'DELETE')
    - `endpoint` (str): Optional. - The API endpoint to send the request to
    - `data` (Optional[Dict[str, Any]]): Optional. - Data to include in the request body (for non-JSON payloads)
    - `json` (Optional[Dict[str, Any]]): Optional. - JSON data to include in the request body
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Specify method, endpoint, data/json.

### Examples
- GET: `api_request` with method="GET", endpoint="projects/123/issues".
- POST: With data={"title": "New issue"}.

### Error Handling
- Validate endpoints.
