---
name: umbraco-skill-test-runner
description: Run tests from skill examples and generate a report (project)
version: 1.0.0
location: managed
allowed-tools: Bash, Read, Glob
---

# Skill Test Runner

Runs all tests from skill examples (unit, mocked, E2E) and outputs a JSON report.

## Usage

```bash
cd .claude/skills/umbraco-skill-test-runner/scripts
npm install --silent
npx tsx run-tests.ts
```

## Test Types

| Type | Description | Runner |
|------|-------------|--------|
| Unit | Component tests with `@open-wc/testing` | Web Test Runner |
| Mocked | Integration tests against mocked backoffice | Playwright |
| E2E | Full end-to-end against real Umbraco | Playwright |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `UMBRACO_USER_LOGIN` | - | Admin email for E2E authentication |
| `UMBRACO_USER_PASSWORD` | - | Admin password for E2E authentication |
| `UMBRACO_URL` | `https://localhost:44325` | Umbraco instance URL |

## Auto-Start Umbraco

If E2E tests are needed and Umbraco is not running, the script will automatically:
1. Start Umbraco from `./Umbraco-CMS.Skills/` using `dotnet run`
2. Wait for the instance to be ready
3. Run E2E tests
4. Stop Umbraco when done (if it was started by the script)

## Output

Generates `test-report.json` in the project root with structure:

```json
{
  "timestamp": "2024-12-26T12:00:00Z",
  "umbracoStarted": true,
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 1,
    "skipped": 1
  },
  "results": [
    {
      "example": "counter-dashboard",
      "path": "plugins/umbraco-testing-skills/.../counter-dashboard",
      "type": "unit",
      "status": "passed",
      "duration": 1234
    }
  ]
}
```

## Integration

This skill is Phase 3 of the `validate-skills` command, running after:
1. Link validation (`umbraco-skill-validator`)
2. Code analysis (`umbraco-skill-code-analyzer`)
