---
name: coding
cluster: coding
description: "Root: language selection, paradigm guidance, code quality SOLID/DRY/YAGNI, PR standards"
tags: ["coding","programming","software"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "code programming write implement software development language"
---

# coding

## Purpose
This skill enables OpenClaw to assist with coding tasks, including selecting programming languages, guiding on paradigms (e.g., OOP, functional), enforcing code quality principles like SOLID, DRY, and YAGNI, and adhering to PR standards such as meaningful commits and code reviews.

## When to Use
Use this skill when writing new code, refactoring existing code, or reviewing pull requests. Apply it for language selection in multi-language projects, paradigm decisions in complex systems, or quality checks to avoid anti-patterns. Ideal for developers facing decisions on code structure or standards compliance.

## Key Capabilities
- Language selection: Automatically suggests languages based on project needs, e.g., recommending Python for scripting or Java for enterprise apps.
- Paradigm guidance: Provides advice on paradigms like OOP (e.g., use classes for encapsulation) or functional programming (e.g., prefer immutability).
- Code quality enforcement: Checks for SOLID principles (e.g., Single Responsibility: ensure classes have one reason to change) and DRY/YAGNI (e.g., detect duplicated code blocks).
- PR standards: Validates commits against rules like atomic changes and descriptive messages.
- Integration with tools: Parses Git diffs for PR reviews or analyzes code snippets for quality metrics.

## Usage Patterns
To use this skill, invoke OpenClaw via CLI or API, specifying inputs like code snippets or project context. For language selection, provide project requirements; for paradigm guidance, include code samples. Always pass an API key via environment variable, e.g., set `$OPENCLAW_API_KEY` before commands. Structure requests with JSON payloads containing fields like "language", "code", and "paradigm". Handle responses by parsing JSON for suggestions or corrections. Example pattern: Pipe code through OpenClaw for real-time feedback in a CI/CD pipeline.

## Common Commands/API
Use the OpenClaw CLI for quick tasks or the REST API for programmatic access. CLI commands require `$OPENCLAW_API_KEY` set. API endpoints use POST requests with JSON bodies.

- CLI Command: `openclaw code --language python --paradigm oop --check solid < input.txt`
  - Flags: `--language` specifies the language (e.g., "python", "java"); `--paradigm` sets guidance type (e.g., "oop"); `--check` enables quality checks (e.g., "solid", "dry").
  - Output: JSON with suggestions, e.g., {"suggestion": "Use a class for this function."}

- API Endpoint: POST to `/api/coding/assist`
  - Body: JSON like {"code": "def add(a, b): return a + b", "language": "python", "checks": ["dry", "yagni"]}
  - Headers: Include `Authorization: Bearer $OPENCLAW_API_KEY`
  - Response: JSON object, e.g., {"quality_score": 8, "issues": ["Function violates DRY principle"]}

- Code Snippet for API Call (Python):
  ```python
  import requests
  api_key = os.environ.get('OPENCLAW_API_KEY')
  response = requests.post('https://api.openclaw.ai/api/coding/assist', headers={'Authorization': f'Bearer {api_key}'}, json={'code': 'some code', 'language': 'js'})
  print(response.json()['suggestion'])
  ```

- Config Format: Use JSON for configurations, e.g.,
  ```
  {
    "default_language": "python",
    "checks": ["solid", "dry"],
    "paradigm": "functional"
  }
  ```
  Save as `.openclaw-config.json` in your project root for CLI overrides.

## Integration Notes
Integrate this skill into IDEs like VS Code via extensions or scripts that call the API. For CI/CD, use it in GitHub Actions by adding a step: `run: openclaw code --check solid --input path/to/code.py`. Ensure `$OPENCLAW_API_KEY` is stored securely, e.g., in GitHub Secrets as `OPENCLAW_API_KEY`. For web apps, embed API calls in backend services, handling rate limits (e.g., 100 requests/min). Test integrations with mock responses to avoid live API hits during development.

## Error Handling
When errors occur, check HTTP status codes from API responses (e.g., 401 for unauthorized, indicating missing `$OPENCLAW_API_KEY`). For CLI, parse error messages like "Error: Invalid language specified" and retry with corrections. Implement retry logic for transient errors (e.g., 5xx status codes) using exponential backoff. In code, wrap API calls in try-except blocks:
  ```python
  try:
      response = requests.post(url, headers=headers, json=data)
      response.raise_for_status()
  except requests.exceptions.HTTPError as e:
      print(f"Error: {e.response.status_code} - {e.response.text}")
  ```
  Log errors with context, such as the input code, for debugging.

## Concrete Usage Examples
1. **Example 1: Generating Code with Language Selection**
   - Task: Write a simple function in Python using OOP paradigm.
   - Command: `openclaw code --language python --paradigm oop --prompt "Implement a counter class"`
   - Expected: Output JSON with code like {"code": "class Counter: def __init__(self): self.count = 0"}
   - How: Set `$OPENCLAW_API_KEY`, run the command, and integrate the response into your project.

2. **Example 2: Code Quality Review for PR**
   - Task: Check a JavaScript snippet for DRY and SOLID violations.
   - API Call: POST to `/api/coding/assist` with body {"code": "function add(a) { return a + 1; } function addTwo(b) { return b + 2; }", "language": "js", "checks": ["dry"]}
   - Expected: Response like {"issues": ["Functions are similar; consider a generic add function to follow DRY"]}
   - How: Use the response to refactor code before committing, e.g., merge functions in your editor.

## Graph Relationships
- Related to: debugging (shares code analysis capabilities), testing (enforces quality for testability), deployment (guides on production-ready code).
- Clusters: coding (primary), software (secondary for broader development tasks).
