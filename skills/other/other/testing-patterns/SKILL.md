---
name: testing-patterns
description: |
  Agent-based declarative testing with YAML test specs. Tests run in sub-agents to preserve
  main context while executing many tests. Supports MCP servers, APIs, and browser automation.

  Use when: testing MCP servers, running integration tests, validating tool behavior after changes,
  or creating regression test suites. Keywords: yaml tests, agent testing, mcp test, integration tests.
license: MIT
---

# Testing Patterns

A pragmatic approach to testing that emphasises:
- **Live testing** over mocks
- **Agent execution** to preserve context
- **YAML specs** as documentation and tests
- **Persistent results** committed to git

## Philosophy

This is **not traditional TDD**. Instead:

1. **Test in production/staging** with good logging
2. **Use agents** to run tests (keeps main context clean)
3. **Define tests declaratively** in YAML (human-readable, version-controlled)
4. **Focus on integration** (real servers, real data)

### Why Agent-Based Testing?

Running 50 tests in the main conversation would consume your entire context window. By delegating to a sub-agent:

- Main context stays clean for development
- Agent can run many tests without context pressure
- Results come back as a summary
- Failed tests get detailed investigation

## Commands

| Command | Purpose |
|---------|---------|
| `/create-tests` | Discover project, generate test specs + testing agent |
| `/run-tests` | Execute tests via agent(s), report results |
| `/coverage` | Generate coverage report and identify uncovered code paths |

**Quick workflow:**
```
/create-tests        → Generates tests/specs/*.yaml + .claude/agents/test-runner.md
/run-tests           → Spawns agent, runs all tests, saves results
/run-tests api       → Run only specs matching "api"
/run-tests --failed  → Re-run only failed tests
/coverage            → Run tests with coverage, analyse gaps
/coverage --threshold 80  → Fail if below 80%
```

## Getting Started in a New Project

This skill provides the **pattern and format**. Claude designs the actual tests based on your project context.

**What happens when you ask "Create tests for this project":**

1. **Discovery** - Claude examines the project:
   - What MCP servers are configured?
   - What APIs or tools exist?
   - What does the code do?

2. **Test Design** - Claude creates project-specific tests:
   - Test cases for the actual tools/endpoints
   - Expected values based on real behavior
   - Edge cases relevant to this domain

3. **Structure** - Using patterns from this skill:
   - YAML specs in `tests/` directory
   - Optional testing agent in `.claude/agents/`
   - Results saved to `tests/results/`

**Example:**

```
You: "Create tests for this MCP server"

Claude: [Discovers this is a Google Calendar MCP]
        [Sees tools: calendar_events, calendar_create, calendar_delete]
        [Designs test cases:]

        tests/calendar-events.yaml:
        - list_upcoming_events (expect: array, count_gte 0)
        - search_by_keyword (expect: contains search term)
        - invalid_date_range (expect: error status)

        tests/calendar-mutations.yaml:
        - create_event (expect: success, returns event_id)
        - delete_nonexistent (expect: error, contains "not found")
```

**The skill teaches Claude:**
- How to structure YAML test specs
- What validation rules are available
- How to create testing agents
- When to use parallel execution

**Your project provides:**
- What to actually test
- Expected values and behaviors
- Domain-specific edge cases

## YAML Test Spec Format

```yaml
name: Feature Tests
description: What these tests validate

# Optional: defaults applied to all tests
defaults:
  tool: my_tool_name
  timeout: 5000

tests:
  - name: test_case_name
    description: Human-readable purpose
    tool: tool_name  # Override default if needed
    params:
      action: search
      query: "test input"
    expect:
      contains: "expected substring"
      not_contains: "should not appear"
      status: success
```

### Validation Rules

| Rule | Description | Example |
|------|-------------|---------|
| `contains` | Response contains string | `contains: "from:john"` |
| `not_contains` | Response doesn't contain | `not_contains: "error"` |
| `matches` | Regex pattern match | `matches: "after:\\d{4}"` |
| `json_path` | Check value at JSON path | `json_path: "$.results[0].name"` |
| `equals` | Exact value match | `equals: "success"` |
| `status` | Check success/error | `status: success` |
| `count_gte` | Array length >= N | `count_gte: 1` |
| `count_eq` | Array length == N | `count_eq: 5` |
| `type` | Value type check | `type: array` |

See `references/validation-rules.md` for complete documentation.

## Creating a Testing Agent

Testing agents inherit MCP tools from the session. Create an agent that:

1. Reads YAML test specs
2. Executes tool calls with params
3. Validates responses against expectations
4. Reports results

### Agent Template

**CRITICAL**: Do NOT specify a `tools` field if you need MCP access. When you specify ANY tools, it becomes an allowlist and `"*"` is interpreted literally (not as a wildcard). Omit `tools` entirely to inherit ALL tools from the parent session.

```yaml
---
name: my-tester
description: |
  Tests [domain] functionality. Reads YAML test specs and validates responses.
  Use when: testing after changes, running regression tests.
# tools field OMITTED - inherits ALL tools from parent (including MCP)
model: sonnet
---

# [Domain] Tester

## How It Works

1. Find test specs: `tests/*.yaml`
2. Parse and execute each test
3. Validate responses
4. Report pass/fail summary

## Test Spec Location

tests/
├── feature-a.yaml
├── feature-b.yaml
└── results/
    └── YYYY-MM-DD-HHMMSS.md

## Execution

For each test:
1. Call tool with params
2. Capture response
3. Apply validation rules
4. Record PASS/FAIL

## Reporting

Save results to `tests/results/YYYY-MM-DD-HHMMSS.md`
```

See `templates/test-agent.md` for complete template.

## Results Format

Test results are saved as markdown for git history:

```markdown
# Test Results: feature-name
**Date**: 2026-02-02 14:30
**Commit**: abc1234
**Summary**: 8/9 passed (89%)

## Results

- test_basic_search - PASSED (0.3s)
- test_with_filter - PASSED (0.4s)
- test_edge_case - FAILED

## Failed Test Details

### test_edge_case
- **Expected**: Contains "expected value"
- **Actual**: Response was empty
- **Params**: `{ action: search, query: "" }`
```

Save to: `tests/results/YYYY-MM-DD-HHMMSS.md`

## Workflow

### 1. Create Test Specs

```yaml
# tests/search.yaml
name: Search Tests
defaults:
  tool: my_search_tool

tests:
  - name: basic_search
    params: { query: "hello" }
    expect: { status: success, count_gte: 0 }

  - name: filtered_search
    params: { query: "hello", filter: "recent" }
    expect: { contains: "results" }
```

### 2. Create Testing Agent

Copy `templates/test-agent.md` and customise for your domain.

### 3. Run Tests

```
"Run the search tests"
"Test the API after my changes"
"Run regression tests for gmail-mcp"
```

### 4. Review Results

Results saved to `tests/results/`. Commit them for history:

```bash
git add tests/results/
git commit -m "Test results: 8/9 passed"
```

## Parallel Test Execution

Run multiple test agents simultaneously to speed up large test suites:

```
"Run these test suites in parallel:
- Agent 1: tests/auth/*.yaml
- Agent 2: tests/search/*.yaml
- Agent 3: tests/api/*.yaml"
```

Each agent:
- Has its own context (won't bloat main conversation)
- Can run 10-50 tests independently
- Returns a summary when done
- Inherits MCP tools from parent session

**Why parallel agents?**
- 50 tests in main context = context exhaustion
- 50 tests across 5 agents = clean context + faster execution
- Each agent reports pass/fail summary, not every test detail

**Batching strategy:**
- Group tests by feature area or MCP server
- 10-20 tests per agent is ideal
- Too few = overhead of spawning not worth it
- Too many = agent context fills up

## MCP Testing

For MCP servers, the testing agent inherits configured MCPs:

```bash
# Configure MCP first
claude mcp add --transport http gmail https://gmail.mcp.example.com/mcp

# Then test
"Run tests for gmail MCP"
```

Example MCP test spec:

```yaml
name: Gmail Search Tests
defaults:
  tool: gmail_messages

tests:
  - name: search_from_person
    params: { action: search, searchQuery: "from John" }
    expect: { contains: "from:john" }

  - name: search_with_date
    params: { action: search, searchQuery: "emails from January 2026" }
    expect: { matches: "after:2026" }
```

## API Testing

For REST APIs, use Bash tool:

```yaml
name: API Tests
defaults:
  timeout: 5000

tests:
  - name: health_check
    command: curl -s https://api.example.com/health
    expect: { contains: "ok" }

  - name: get_user
    command: curl -s https://api.example.com/users/1
    expect:
      json_path: "$.name"
      type: string
```

## Browser Testing

For browser automation, use Playwright tools:

```yaml
name: UI Tests

tests:
  - name: login_page_loads
    steps:
      - navigate: https://app.example.com/login
      - snapshot: true
    expect: { contains: "Sign In" }

  - name: form_submission
    steps:
      - navigate: https://app.example.com/form
      - type: { ref: "#email", text: "test@example.com" }
      - click: { ref: "button[type=submit]" }
    expect: { contains: "Success" }
```

## Tips

1. **Start with smoke tests**: Basic connectivity and auth
2. **Test edge cases**: Empty results, errors, special characters
3. **Use descriptive names**: `search_with_date_filter` not `test1`
4. **Group related tests**: One file per feature area
5. **Add after bugs**: Every fixed bug gets a regression test
6. **Commit results**: Create history of test runs

## What This Is NOT

- Not a Jest/Vitest replacement (use those for unit tests)
- Not enforcing TDD (use what works for you)
- Not a test runner library (the agent IS the runner)
- Not about mocking (we test real systems)

## When to Use

| Scenario | Use This | Use Traditional Testing |
|----------|----------|------------------------|
| MCP server validation | Yes | No |
| API integration | Yes | Complement with unit tests |
| Browser workflows | Yes | Complement with component tests |
| Unit testing | No | Yes (Jest/Vitest) |
| Component testing | No | Yes (Testing Library) |
| Type checking | No | Yes (TypeScript) |

## Related Resources

- `templates/test-spec.yaml` - Generic test spec template
- `templates/test-agent.md` - Testing agent template
- `references/validation-rules.md` - Complete validation rule reference
