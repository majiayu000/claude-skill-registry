---
name: testing
cluster: testing
description: "Root: testing pyramid unit/integration/e2e, TDD/BDD, coverage strategy, naming conventions"
tags: ["testing","tdd","bdd","quality"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "testing tdd bdd unit integration e2e coverage quality pyramid"
---

# testing

## Purpose
This skill enables OpenClaw to assist with comprehensive testing strategies, including the testing pyramid (unit, integration, e2e), TDD/BDD methodologies, code coverage analysis, and naming conventions to ensure high-quality code. It focuses on integrating testing into development workflows for robust software.

## When to Use
Use this skill when writing or reviewing code that requires test-driven development, such as implementing new features in a project, debugging failures, or ensuring coverage thresholds. Apply it in scenarios like agile sprints, CI/CD pipelines, or when refactoring code to maintain quality.

## Key Capabilities
- Generate unit tests using TDD: Create tests for functions with assertions based on input/output.
- Support BDD with Gherkin syntax: Parse feature files and generate step definitions.
- Analyze testing pyramid: Recommend distribution (e.g., 70% unit, 20% integration, 10% e2e).
- Enforce coverage strategies: Set thresholds (e.g., >80%) and identify uncovered lines.
- Apply naming conventions: Enforce patterns like `testFunctionName` for tests.
- Integrate with tools: Use APIs to run tests via Jest, Pytest, or Selenium.

## Usage Patterns
To use this skill, invoke OpenClaw with specific commands in your chat or script. Start by providing code snippets for analysis, then request test generation. For TDD, alternate between writing tests and code. In BDD, supply user stories first. Always specify the test type (unit, integration, e2e) to tailor outputs. Configure via a JSON file, e.g., set `"coverageThreshold": 80` in `.openclaw/config.json`. For automation, chain with build tools like Make or npm scripts.

## Common Commands/API
Invoke via OpenClaw CLI or API. Use environment variable `$OPENCLAW_API_KEY` for authentication in API calls.

- CLI Command: Run unit tests with `claw test run --type unit --file src/myfile.js --coverage true`
  Example snippet:
  ```
  claw test run --type unit --file tests/unit.js
  // Output: Test results with coverage report
  ```

- API Endpoint: POST to `https://api.openclaw.ai/v1/test/run` with JSON body `{ "type": "integration", "paths": ["src/"], "threshold": 85 }`
  Example snippet:
  ```
  curl -H "Authorization: Bearer $OPENCLAW_API_KEY" \
  -d '{"type":"e2e","paths":["tests/e2e/"]}' https://api.openclaw.ai/v1/test/run
  ```

- Common Flags: `--type [unit/integration/e2e]` for test level, `--coverage` for reports, `--bdd` for Gherkin parsing.
- Config Format: Use YAML for test configs, e.g.,
  ```
  tests:
    unit: true
    coverage: 90
  ```
To generate a TDD test, say: "Generate a unit test for this function: def add(a, b): return a + b"

## Integration Notes
Integrate this skill with existing tools by exporting results to formats like JUnit XML or HTML reports. For CI/CD, add hooks in GitHub Actions or Jenkins, e.g., run `claw test run --type e2e` as a step. If using frameworks, map OpenClaw outputs to Jest configs by specifying adapters in `.openclaw/config.json`, like `"adapter": "jest"`. Ensure API compatibility by setting the env var `$OPENCLAW_API_KEY` in your pipeline scripts. For multi-service apps, combine with monitoring tools via webhooks to trigger tests on code changes.

## Error Handling
When errors occur, check for common issues like invalid test types or authentication failures. Use try-catch in scripts, e.g.,
```
try {
  await claw.test.run({ type: 'unit' });
} catch (error) {
  console.error(error.message);  // e.g., "API key missing"
}
```
Handle API errors by verifying `$OPENCLAW_API_KEY` and response codes (e.g., 401 for unauthorized). For test failures, parse OpenClaw outputs for specifics, like "Assertion failed on line 5". Retry transient errors with exponential backoff, and log details in JSON format for debugging.

## Usage Examples
1. **TDD for a simple function**: Provide code like `def multiply(a, b): return a * b`, then command: "Write a unit test for this using pytest." OpenClaw responds with: 
   ```
   def test_multiply():
       assert multiply(2, 3) == 6
       assert multiply(0, 5) == 0
   ```
   Run it via `claw test run --type unit --file tests.py`.

2. **BDD for user story**: Supply: "Feature: User login", then: "Generate step definitions." OpenClaw outputs:
   ```
   Given("user is on login page") do
     visit '/login'
   end
   ```
   Integrate by running `claw test run --bdd --file features/login.feature`.

## Graph Relationships
- Related to: "tdd" (direct link for TDD workflows)
- Related to: "bdd" (shared for behavior-driven testing)
- Related to: "quality" (overlaps on code coverage and standards)
- Connected via: "testing" cluster for pyramid strategies
- No direct edges to unrelated clusters like "deployment"
