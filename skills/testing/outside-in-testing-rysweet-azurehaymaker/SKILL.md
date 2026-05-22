---
name: outside-in-testing
description: |
  Generates agentic outside-in tests using gadugi-agentic-test framework for CLI, TUI, Web, and Electron apps.
  Use when you need behavior-driven tests that verify external interfaces without internal implementation knowledge.
  Creates YAML test scenarios that AI agents execute, observe, and validate against expected outcomes.
  Supports progressive complexity from simple smoke tests to advanced multi-step workflows.
version: 1.0.0
embedded_framework_version: 0.1.0
github_repo: https://github.com/rysweet/gadugi-agentic-test
issue: https://github.com/rysweet/MicrosoftHackathon2025-AgenticCoding/issues/1356
---

# Outside-In Testing Skill

## Purpose [LEVEL 1]

This skill helps you create **agentic outside-in tests** that verify application behavior from an external user's perspective without any knowledge of internal implementation. Using the gadugi-agentic-test framework, you write declarative YAML scenarios that AI agents execute, observe, and validate.

**Key Principle**: Tests describe WHAT should happen, not HOW it's implemented. Agents figure out the execution details.

## When to Use This Skill [LEVEL 1]

### Perfect For

- **Smoke Tests**: Quick validation that critical user flows work
- **Behavior-Driven Testing**: Verify features from user perspective
- **Cross-Platform Testing**: Same test logic for CLI, TUI, Web, Electron
- **Refactoring Safety**: Tests remain valid when implementation changes
- **AI-Powered Testing**: Let agents handle complex interactions
- **Documentation as Tests**: YAML scenarios double as executable specs

### Use This Skill When

- Starting a new project and defining expected behaviors
- Refactoring code and need tests that won't break with internal changes
- Testing user-facing applications (CLI tools, TUIs, web apps, desktop apps)
- Writing acceptance criteria that can be automatically verified
- Need tests that non-developers can read and understand
- Want to catch regressions in critical user workflows
- Testing complex multi-step interactions

### Don't Use This Skill When

- Need unit tests for internal functions (use test-gap-analyzer instead)
- Testing performance or load characteristics
- Need precise timing or concurrency control
- Testing non-interactive batch processes
- Implementation details matter more than behavior

## Core Concepts [LEVEL 1]

### Outside-In Testing Philosophy

**Traditional Inside-Out Testing**:

```python
# Tightly coupled to implementation
def test_calculator_add():
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
    assert calc.history == [(2, 3, 5)]  # Knows internal state
```

**Agentic Outside-In Testing**:

```yaml
# Implementation-agnostic behavior verification
scenario:
  name: "Calculator Addition"
  steps:
    - action: launch
      target: "./calculator"
    - action: send_input
      value: "add 2 3"
    - action: verify_output
      contains: "Result: 5"
```

**Benefits**:

- Tests survive refactoring (internal changes don't break tests)
- Readable by non-developers (YAML is declarative)
- Platform-agnostic (same structure for CLI/TUI/Web/Electron)
- AI agents handle complexity (navigation, timing, screenshots)

### The Gadugi Agentic Test Framework [LEVEL 2]

Gadugi-agentic-test is a Python framework that:

1. **Parses YAML test scenarios** with declarative steps
2. **Dispatches to specialized agents** (CLI, TUI, Web, Electron agents)
3. **Executes actions** (launch, input, click, wait, verify)
4. **Collects evidence** (screenshots, logs, output captures)
5. **Validates outcomes** against expected results
6. **Generates reports** with evidence trails

**Architecture**:

```
YAML Scenario → Scenario Loader → Agent Dispatcher → Execution Engine
                                          ↓
                     [CLI Agent, TUI Agent, Web Agent, Electron Agent]
                                          ↓
                           Observers → Comprehension Agent
                                          ↓
                                   Evidence Report
```

### Progressive Disclosure Levels [LEVEL 1]

This skill teaches testing in three levels:

- **Level 1: Fundamentals** - Basic single-action tests, simple verification
- **Level 2: Intermediate** - Multi-step flows, conditional logic, error handling
- **Level 3: Advanced** - Custom agents, visual regression, performance validation

Each example is marked with its level. Start at Level 1 and progress as needed.

## Quick Start [LEVEL 1]

### Installation

```bash
# Install gadugi-agentic-test framework
pip install gadugi-agentic-test

# Verify installation
gadugi-agentic-test --version
```

### Your First Test (CLI Example)

Create `test-hello.yaml`:

```yaml
scenario:
  name: "Hello World CLI Test"
  description: "Verify CLI prints greeting"
  type: cli

  prerequisites:
    - "./hello-world executable exists"

  steps:
    - action: launch
      target: "./hello-world"

    - action: verify_output
      contains: "Hello, World!"

    - action: verify_exit_code
      expected: 0
```

Run the test:

```bash
gadugi-agentic-test run test-hello.yaml
```

Output:

```
✓ Scenario: Hello World CLI Test
  ✓ Step 1: Launched ./hello-world
  ✓ Step 2: Output contains "Hello, World!"
  ✓ Step 3: Exit code is 0

PASSED (3/3 steps successful)
Evidence saved to: ./evidence/test-hello-20250116-093045/
```

### Understanding the YAML Structure [LEVEL 1]

Every test scenario has this structure:

```yaml
scenario:
  name: "Descriptive test name"
  description: "What this test verifies"
  type: cli | tui | web | electron

  # Optional metadata
  tags: [smoke, critical, auth]
  timeout: 30s

  # What must be true before test runs
  prerequisites:
    - "Condition 1"
    - "Condition 2"

  # The test steps (executed sequentially)
  steps:
    - action: action_name
      parameter1: value1
      parameter2: value2

    - action: verify_something
      expected: value

  # Optional cleanup
  cleanup:
    - action: stop_application
```

## Application Types and Agents [LEVEL 2]

### CLI Applications [LEVEL 1]

**Use Case**: Command-line tools, scripts, build tools, package managers

**Supported Actions**:

- `launch` - Start the CLI program
- `send_input` - Send text or commands via stdin
- `send_signal` - Send OS signals (SIGINT, SIGTERM)
- `wait_for_output` - Wait for specific text in stdout/stderr
- `verify_output` - Check stdout/stderr contains/matches expected text
- `verify_exit_code` - Validate process exit code
- `capture_output` - Save output for later verification

**Example** (see `examples/cli/calculator-basic.yaml`):

```yaml
scenario:
  name: "CLI Calculator Basic Operations"
  type: cli

  steps:
    - action: launch
      target: "./calculator"
      args: ["--mode", "interactive"]

    - action: send_input
      value: "add 5 3\n"

    - action: verify_output
      contains: "Result: 8"
      timeout: 2s

    - action: send_input
      value: "multiply 4 7\n"

    - action: verify_output
      contains: "Result: 28"

    - action: send_input
      value: "exit\n"

    - action: verify_exit_code
      expected: 0
```

### TUI Applications [LEVEL 1]

**Use Case**: Terminal user interfaces (htop, vim, tmux, custom dashboard TUIs)

**Supported Actions**:

- `launch` - Start TUI application
- `send_keypress` - Send keyboard input (arrow keys, enter, ctrl+c, etc.)
- `wait_for_screen` - Wait for specific text to appear on screen
- `verify_screen` - Check screen contents match expectations
- `capture_screenshot` - Save terminal screenshot (ANSI art)
- `navigate_menu` - Navigate menu structures
- `fill_form` - Fill TUI form fields

**Example** (see `examples/tui/file-manager-navigation.yaml`):

```yaml
scenario:
  name: "TUI File Manager Navigation"
  type: tui

  steps:
    - action: launch
      target: "./file-manager"

    - action: wait_for_screen
      contains: "File Manager v1.0"
      timeout: 3s

    - action: send_keypress
      value: "down"
      times: 3

    - action: verify_screen
      contains: "> documents/"
      description: "Third item should be selected"

    - action: send_keypress
      value: "enter"

    - action: wait_for_screen
      contains: "documents/"
      timeout: 2s

    - action: capture_screenshot
      save_as: "documents-view.txt"
```

### Web Applications [LEVEL 1]

**Use Case**: Web apps, dashboards, SPAs, admin panels

**Supported Actions**:

- `navigate` - Go to URL
- `click` - Click element by selector or text
- `type` - Type into input fields
- `wait_for_element` - Wait for element to appear
- `verify_element` - Check element exists/contains text
- `verify_url` - Validate current URL
- `screenshot` - Capture browser screenshot
- `scroll` - Scroll page or element

**Example** (see `examples/web/dashboard-smoke-test.yaml`):

```yaml
scenario:
  name: "Dashboard Smoke Test"
  type: web

  steps:
    - action: navigate
      url: "http://localhost:3000/dashboard"

    - action: wait_for_element
      selector: "h1.dashboard-title"
      timeout: 5s

    - action: verify_element
      selector: "h1.dashboard-title"
      contains: "Analytics Dashboard"

    - action: verify_element
      selector: ".widget-stats"
      count: 4
      description: "Should have 4 stat widgets"

    - action: click
      selector: "button.refresh-data"

    - action: wait_for_element
      selector: ".loading-spinner"
      disappears: true
      timeout: 10s

    - action: screenshot
      save_as: "dashboard-loaded.png"
```

### Electron Applications [LEVEL 2]

**Use Case**: Desktop apps built with Electron (VS Code, Slack, Discord clones)

**Supported Actions**:

- `launch` - Start Electron app
- `window_action` - Interact with windows (focus, minimize, close)
- `menu_click` - Click application menu items
- `dialog_action` - Handle native dialogs (open file, save, confirm)
- `ipc_send` - Send IPC message to main process
- `verify_window` - Check window state/properties
- All web actions (since Electron uses Chromium)

**Example** (see `examples/electron/single-window-basic.yaml`):

```yaml
scenario:
  name: "Electron Single Window Test"
  type: electron

  steps:
    - action: launch
      target: "./dist/my-app"
      wait_for_window: true
      timeout: 10s

    - action: verify_window
      title: "My Application"
      visible: true

    - action: menu_click
      path: ["File", "New Document"]

    - action: wait_for_element
      selector: ".document-editor"

    - action: type
      selector: ".document-editor"
      value: "Hello from test"

    - action: menu_click
      path: ["File", "Save"]

    - action: dialog_action
      type: save_file
      filename: "test-document.txt"

    - action: verify_window
      title_contains: "test-document.txt"
```

## Test Scenario Anatomy [LEVEL 2]

### Metadata Section

```yaml
scenario:
  name: "Clear descriptive name"
  description: "Detailed explanation of what this test verifies"
  type: cli | tui | web | electron

  # Optional fields
  tags: [smoke, regression, auth, payment]
  priority: high | medium | low
  timeout: 60s # Overall scenario timeout
  retry_on_failure: 2 # Retry count

  # Environment requirements
  environment:
    variables:
      API_URL: "http://localhost:8080"
      DEBUG: "true"
    files:
      - "./config.json must exist"
```

### Prerequisites

Prerequisites are conditions that must be true before the test runs. The framework validates these before execution.

```yaml
prerequisites:
  - "./application binary exists"
  - "Port 8080 is available"
  - "Database is running"
  - "User account test@example.com exists"
  - "File ./test-data.json exists"
```

If prerequisites fail, the test is skipped (not failed).

### Steps

Steps execute sequentially. Each step has:

- **action**: Required - the action to perform
- **Parameters**: Action-specific parameters
- **description**: Optional - human-readable explanation
- **timeout**: Optional - step-specific timeout
- **continue_on_failure**: Optional - don't fail scenario if step fails

```yaml
steps:
  # Simple action
  - action: launch
    target: "./app"

  # Action with multiple parameters
  - action: verify_output
    contains: "Success"
    timeout: 5s
    description: "App should print success message"

  # Continue even if this fails
  - action: click
    selector: ".optional-button"
    continue_on_failure: true
```

### Verification Actions [LEVEL 1]

Verification actions check expected outcomes. They fail the test if expectations aren't met.

**Common Verifications**:

```yaml
# CLI: Check output contains text
- action: verify_output
  contains: "Expected text"

# CLI: Check output matches regex
- action: verify_output
  matches: "Result: \\d+"

# CLI: Check exit code
- action: verify_exit_code
  expected: 0

# Web/TUI: Check element exists
- action: verify_element
  selector: ".success-message"

# Web/TUI: Check element contains text
- action: verify_element
  selector: "h1"
  contains: "Welcome"

# Web: Check URL
- action: verify_url
  equals: "http://localhost:3000/dashboard"

# Web: Check element count
- action: verify_element
  selector: ".list-item"
  count: 5

# Electron: Check window state
- action: verify_window
  title: "My App"
  visible: true
  focused: true
```

### Cleanup Section

Cleanup runs after all steps complete (success or failure). Use for teardown actions.

```yaml
cleanup:
  - action: stop_application
    force: true

  - action: delete_file
    path: "./temp-test-data.json"

  - action: reset_database
    connection: "test_db"
```

## Advanced Patterns [LEVEL 2]

### Conditional Logic

Execute steps based on conditions:

```yaml
steps:
  - action: launch
    target: "./app"

  - action: verify_output
    contains: "Login required"
    id: login_check

  # Only run if login_check passed
  - action: send_input
    value: "login admin password123\n"
    condition: login_check.passed
```

### Variables and Templating [LEVEL 2]

Define variables and use them throughout the scenario:

```yaml
scenario:
  name: "Test with Variables"
  type: cli

  variables:
    username: "testuser"
    api_url: "http://localhost:8080"

  steps:
    - action: launch
      target: "./app"
      args: ["--api", "${api_url}"]

    - action: send_input
      value: "login ${username}\n"

    - action: verify_output
      contains: "Welcome, ${username}!"
```

### Loops and Repetition [LEVEL 2]

Repeat actions multiple times:

```yaml
steps:
  - action: launch
    target: "./app"

  # Repeat action N times
  - action: send_keypress
    value: "down"
    times: 5

  # Loop over list
  - action: send_input
    value: "${item}\n"
    for_each:
      - "apple"
      - "banana"
      - "cherry"
```

### Error Handling [LEVEL 2]

Handle expected errors gracefully:

```yaml
steps:
  - action: send_input
    value: "invalid command\n"

  # Verify error message appears
  - action: verify_output
    contains: "Error: Unknown command"
    expected_failure: true

  # App should still be running
  - action: verify_running
    expected: true
```

### Multi-Step Workflows [LEVEL 2]

Complex scenarios with multiple phases:

```yaml
scenario:
  name: "E-commerce Purchase Flow"
  type: web

  steps:
    # Phase 1: Authentication
    - action: navigate
      url: "http://localhost:3000/login"

    - action: type
      selector: "#username"
      value: "test@example.com"

    - action: type
      selector: "#password"
      value: "password123"

    - action: click
      selector: "button[type=submit]"

    - action: wait_for_url
      contains: "/dashboard"

    # Phase 2: Product Selection
    - action: navigate
      url: "http://localhost:3000/products"

    - action: click
      text: "Add to Cart"
      nth: 1

    - action: verify_element
      selector: ".cart-badge"
      contains: "1"

    # Phase 3: Checkout
    - action: click
      selector: ".cart-icon"

    - action: click
      text: "Proceed to Checkout"

    - action: fill_form
      fields:
        "#shipping-address": "123 Test St"
        "#city": "Testville"
        "#zip": "12345"

    - action: click
      selector: "#place-order"

    - action: wait_for_element
      selector: ".order-confirmation"
      timeout: 10s

    - action: verify_element
      selector: ".order-number"
      exists: true
```

## Level 3: Advanced Topics [LEVEL 3]

### Custom Comprehension Agents

The framework uses AI agents to interpret application output and determine if tests pass. You can customize these agents for domain-specific logic.

**Default Comprehension Agent**:

- Observes raw output (text, HTML, screenshots)
- Applies general reasoning to verify expectations
- Returns pass/fail with explanation

**Custom Comprehension Agent** (see `examples/custom-agents/custom-comprehension-agent.yaml`):

```yaml
scenario:
  name: "Financial Dashboard Test with Custom Agent"
  type: web

  # Define custom comprehension logic
  comprehension_agent:
    model: "gpt-4"
    system_prompt: |
      You are a financial data validator. When verifying dashboard content:
      1. All monetary values must use proper formatting ($1,234.56)
      2. Percentages must include % symbol
      3. Dates must be in MM/DD/YYYY format
      4. Negative values must be red
      5. Chart data must be logically consistent

      Be strict about formatting and data consistency.

    examples:
      - input: "Total Revenue: 45000"
        output: "FAIL - Missing currency symbol and comma separator"
      - input: "Total Revenue: $45,000.00"
        output: "PASS - Correctly formatted"

  steps:
    - action: navigate
      url: "http://localhost:3000/financial-dashboard"

    - action: verify_element
      selector: ".revenue-widget"
      use_custom_comprehension: true
      description: "Revenue should be properly formatted"
```

### Visual Regression Testing [LEVEL 3]

Compare screenshots against baseline images:

```yaml
scenario:
  name: "Visual Regression - Homepage"
  type: web

  steps:
    - action: navigate
      url: "http://localhost:3000"

    - action: wait_for_element
      selector: ".page-loaded"

    - action: screenshot
      save_as: "homepage.png"

    - action: visual_compare
      screenshot: "homepage.png"
      baseline: "./baselines/homepage-baseline.png"
      threshold: 0.05 # 5% difference allowed
      highlight_differences: true
```

### Performance Validation [LEVEL 3]

Measure and validate performance metrics:

```yaml
scenario:
  name: "Performance - Dashboard Load Time"
  type: web

  performance:
    metrics:
      - page_load_time
      - first_contentful_paint
      - time_to_interactive

  steps:
    - action: navigate
      url: "http://localhost:3000/dashboard"
      measure_timing: true

    - action: verify_performance
      metric: page_load_time
      less_than: 3000 # 3 seconds

    - action: verify_performance
      metric: first_contentful_paint
      less_than: 1500 # 1.5 seconds
```

### Multi-Window Coordination (Electron) [LEVEL 3]

Test applications with multiple windows:

```yaml
scenario:
  name: "Multi-Window Chat Application"
  type: electron

  steps:
    - action: launch
      target: "./chat-app"

    - action: menu_click
      path: ["Window", "New Chat"]

    - action: verify_window
      count: 2

    - action: window_action
      window: 1
      action: focus

    - action: type
      selector: ".message-input"
      value: "Hello from window 1"

    - action: click
      selector: ".send-button"

    - action: window_action
      window: 2
      action: focus

    - action: wait_for_element
      selector: ".message"
      contains: "Hello from window 1"
      timeout: 5s
```

### IPC Testing (Electron) [LEVEL 3]

Test Inter-Process Communication between renderer and main:

```yaml
scenario:
  name: "Electron IPC Communication"
  type: electron

  steps:
    - action: launch
      target: "./my-app"

    - action: ipc_send
      channel: "get-system-info"

    - action: ipc_expect
      channel: "system-info-reply"
      timeout: 3s

    - action: verify_ipc_payload
      contains:
        platform: "darwin"
        arch: "x64"
```

### Custom Reporters [LEVEL 3]

Generate custom test reports:

```yaml
scenario:
  name: "Test with Custom Reporting"
  type: cli

  reporting:
    format: custom
    template: "./report-template.html"
    include:
      - screenshots
      - logs
      - timing_data
      - video_recording

    email:
      enabled: true
      recipients: ["team@example.com"]
      on_failure_only: true

  steps:
    # ... test steps ...
```

## Framework Integration [LEVEL 2]

### Running Tests

**Single test**:

```bash
gadugi-agentic-test run test-scenario.yaml
```

**Multiple tests**:

```bash
gadugi-agentic-test run tests/*.yaml
```

**With options**:

```bash
gadugi-agentic-test run test.yaml \
  --verbose \
  --evidence-dir ./test-evidence \
  --retry 2 \
  --timeout 60s
```

### CI/CD Integration

**GitHub Actions** (`.github/workflows/agentic-tests.yml`):

```yaml
name: Agentic Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install gadugi-agentic-test
        run: pip install gadugi-agentic-test

      - name: Run tests
        run: gadugi-agentic-test run tests/agentic/*.yaml

      - name: Upload evidence
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-evidence
          path: ./evidence/
```

### Evidence Collection

The framework automatically collects evidence for debugging:

```
evidence/
  scenario-name-20250116-093045/
    ├── scenario.yaml          # Original test scenario
    ├── execution-log.json     # Detailed execution log
    ├── screenshots/           # All captured screenshots
    │   ├── step-1.png
    │   ├── step-3.png
    │   └── step-5.png
    ├── output-captures/       # CLI/TUI output
    │   ├── stdout.txt
    │   └── stderr.txt
    ├── timing.json            # Performance metrics
    └── report.html            # Human-readable report
```

## Best Practices [LEVEL 2]

### 1. Start Simple, Add Complexity

Begin with basic smoke tests, then add detail:

```yaml
# Level 1: Basic smoke test
steps:
  - action: launch
    target: "./app"
  - action: verify_output
    contains: "Ready"

# Level 2: Add interaction
steps:
  - action: launch
    target: "./app"
  - action: send_input
    value: "command\n"
  - action: verify_output
    contains: "Success"

# Level 3: Add error handling and edge cases
steps:
  - action: launch
    target: "./app"
  - action: send_input
    value: "invalid\n"
  - action: verify_output
    contains: "Error"
  - action: send_input
    value: "command\n"
  - action: verify_output
    contains: "Success"
```

### 2. Use Descriptive Names and Descriptions

```yaml
# Bad
scenario:
  name: "Test 1"
  steps:
    - action: click
      selector: "button"

# Good
scenario:
  name: "User Login Flow - Valid Credentials"
  description: "Verifies user can log in with valid email and password"
  steps:
    - action: click
      selector: "button[type=submit]"
      description: "Submit login form"
```

### 3. Verify Critical Paths Only

Don't test every tiny detail. Focus on user-facing behavior:

```yaml
# Bad - Tests implementation details
- action: verify_element
  selector: ".internal-cache-status"
  contains: "initialized"

# Good - Tests user-visible behavior
- action: verify_element
  selector: ".welcome-message"
  contains: "Welcome back"
```

### 4. Use Prerequisites for Test Dependencies

```yaml
scenario:
  name: "User Profile Edit"

  prerequisites:
    - "User testuser@example.com exists"
    - "User is logged in"
    - "Database is seeded with test data"

  steps:
    # Test assumes prerequisites are met
    - action: navigate
      url: "/profile"
```

### 5. Keep Tests Independent

Each test should set up its own state and clean up:

```yaml
scenario:
  name: "Create Document"

  steps:
    # Create test user (don't assume exists)
    - action: api_call
      endpoint: "/api/users"
      method: POST
      data: { email: "test@example.com" }

    # Run test
    - action: navigate
      url: "/documents/new"
    # ... test steps ...

  cleanup:
    # Remove test user
    - action: api_call
      endpoint: "/api/users/test@example.com"
      method: DELETE
```

### 6. Use Tags for Organization

```yaml
scenario:
  name: "Critical Payment Flow"
  tags: [smoke, critical, payment, e2e]
  # Run with: gadugi-agentic-test run --tags critical
```

### 7. Add Timeouts Strategically

```yaml
steps:
  # Quick operations - short timeout
  - action: click
    selector: "button"
    timeout: 2s

  # Network operations - longer timeout
  - action: wait_for_element
    selector: ".data-loaded"
    timeout: 10s

  # Complex operations - generous timeout
  - action: verify_element
    selector: ".report-generated"
    timeout: 60s
```

## Testing Strategies [LEVEL 2]

### Smoke Tests

Minimal tests that verify critical functionality works:

```yaml
scenario:
  name: "Smoke Test - Application Starts"
  tags: [smoke]

  steps:
    - action: launch
      target: "./app"
    - action: verify_output
      contains: "Ready"
      timeout: 5s
```

Run before every commit: `gadugi-agentic-test run --tags smoke`

### Happy Path Tests

Test the ideal user journey:

```yaml
scenario:
  name: "Happy Path - User Registration"

  steps:
    - action: navigate
      url: "/register"
    - action: type
      selector: "#email"
      value: "newuser@example.com"
    - action: type
      selector: "#password"
      value: "SecurePass123!"
    - action: click
      selector: "button[type=submit]"
    - action: wait_for_url
      contains: "/welcome"
```

### Error Path Tests

Verify error handling:

```yaml
scenario:
  name: "Error Path - Invalid Login"

  steps:
    - action: navigate
      url: "/login"
    - action: type
      selector: "#email"
      value: "invalid@example.com"
    - action: type
      selector: "#password"
      value: "wrongpassword"
    - action: click
      selector: "button[type=submit]"
    - action: verify_element
      selector: ".error-message"
      contains: "Invalid credentials"
```

### Regression Tests

Prevent bugs from reappearing:

```yaml
scenario:
  name: "Regression - Issue #123 Password Reset"
  tags: [regression, bug-123]
  description: "Verifies password reset email is sent (was broken in v1.2)"

  steps:
    - action: navigate
      url: "/forgot-password"
    - action: type
      selector: "#email"
      value: "user@example.com"
    - action: click
      selector: "button[type=submit]"
    - action: verify_element
      selector: ".success-message"
      contains: "Reset email sent"
```

## Philosophy Alignment [LEVEL 2]

This skill follows amplihack's core principles:

### Ruthless Simplicity

- **YAML over code**: Declarative tests are simpler than programmatic tests
- **No implementation details**: Tests describe WHAT, not HOW
- **Minimal boilerplate**: Each test is focused and concise

### Modular Design (Bricks & Studs)

- **Self-contained scenarios**: Each YAML file is independent
- **Clear contracts**: Steps have well-defined inputs/outputs
- **Composable actions**: Reuse actions across different test types

### Zero-BS Implementation

- **No stubs**: Every example in this skill is a complete, runnable test
- **Working defaults**: Tests run with minimal configuration
- **Clear errors**: Framework provides actionable error messages

### Outside-In Thinking

- **User perspective**: Tests verify behavior users care about
- **Implementation agnostic**: Refactoring doesn't break tests
- **Behavior-driven**: Focus on outcomes, not internals

## Common Pitfalls and Solutions [LEVEL 2]

### Pitfall 1: Over-Specifying

**Problem**: Test breaks when UI changes slightly

```yaml
# Bad - Too specific
- action: verify_element
  selector: "div.container > div.row > div.col-md-6 > span.text-primary.font-bold"
  contains: "Welcome"
```

**Solution**: Use flexible selectors

```yaml
# Good - Focused on behavior
- action: verify_element
  selector: ".welcome-message"
  contains: "Welcome"
```

### Pitfall 2: Missing Waits

**Problem**: Test fails intermittently due to timing

```yaml
# Bad - No wait for async operation
- action: click
  selector: ".load-data-button"
- action: verify_element
  selector: ".data-table" # May not exist yet!
```

**Solution**: Always wait for dynamic content

```yaml
# Good - Wait for element to appear
- action: click
  selector: ".load-data-button"
- action: wait_for_element
  selector: ".data-table"
  timeout: 10s
- action: verify_element
  selector: ".data-table"
```

### Pitfall 3: Testing Implementation Details

**Problem**: Test coupled to internal state

```yaml
# Bad - Tests internal cache state
- action: verify_output
  contains: "Cache hit ratio: 85%"
```

**Solution**: Test user-visible behavior

```yaml
# Good - Tests response time
- action: verify_response_time
  less_than: 100ms
  description: "Fast response indicates caching works"
```

### Pitfall 4: Flaky Assertions

**Problem**: Assertions depend on exact timing or formatting

```yaml
# Bad - Exact timestamp match will fail
- action: verify_output
  contains: "Created at: 2025-11-16 09:30:45"
```

**Solution**: Use flexible patterns

```yaml
# Good - Match pattern, not exact value
- action: verify_output
  matches: "Created at: \\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}"
```

### Pitfall 5: Not Cleaning Up

**Problem**: Tests leave artifacts that affect future runs

```yaml
# Bad - No cleanup
steps:
  - action: create_file
    path: "./test-data.json"
  - action: launch
    target: "./app"
```

**Solution**: Always use cleanup section

```yaml
# Good - Cleanup ensures clean slate
steps:
  - action: create_file
    path: "./test-data.json"
  - action: launch
    target: "./app"

cleanup:
  - action: delete_file
    path: "./test-data.json"
```

## Example Library [LEVEL 1]

This skill includes 15 complete working examples organized by application type and complexity level:

### CLI Examples

1. **calculator-basic.yaml** [LEVEL 1] - Simple CLI arithmetic operations
2. **cli-error-handling.yaml** [LEVEL 2] - Error messages and recovery
3. **cli-interactive-session.yaml** [LEVEL 2] - Multi-turn interactive CLI

### TUI Examples

4. **file-manager-navigation.yaml** [LEVEL 1] - Basic TUI keyboard navigation
5. **tui-form-validation.yaml** [LEVEL 2] - Complex form filling and validation
6. **tui-performance-monitoring.yaml** [LEVEL 3] - TUI performance dashboard testing

### Web Examples

7. **dashboard-smoke-test.yaml** [LEVEL 1] - Simple web dashboard verification
8. **web-authentication-flow.yaml** [LEVEL 2] - Multi-step login workflow
9. **web-visual-regression.yaml** [LEVEL 2] - Screenshot-based visual testing

### Electron Examples

10. **single-window-basic.yaml** [LEVEL 1] - Basic Electron window test
11. **multi-window-coordination.yaml** [LEVEL 2] - Multiple window orchestration
12. **electron-menu-testing.yaml** [LEVEL 2] - Application menu interactions
13. **electron-ipc-testing.yaml** [LEVEL 3] - Main/renderer IPC testing

### Custom Agent Examples

14. **custom-comprehension-agent.yaml** [LEVEL 3] - Domain-specific validation logic
15. **custom-reporter-integration.yaml** [LEVEL 3] - Custom test reporting

See `examples/` directory for full example code with inline documentation.

## Framework Freshness Check [LEVEL 3]

This skill embeds knowledge of gadugi-agentic-test version 0.1.0. To check if a newer version exists:

```bash
# Run the freshness check script
python scripts/check-freshness.py

# Output if outdated:
# WARNING: Embedded framework version is 0.1.0
# Latest GitHub version is 0.2.5
#
# New features in 0.2.5:
# - Native Playwright support for web testing
# - Video recording for all test types
# - Parallel test execution
#
# Update with: pip install --upgrade gadugi-agentic-test
```

The script checks the GitHub repository for releases and compares against the embedded version. This ensures you're aware of new features and improvements.

**When to Update This Skill**:

- New framework version adds significant features
- Breaking changes in YAML schema
- New application types supported
- Agent capabilities expand

## Integration with Other Skills [LEVEL 2]

### Works Well With

**test-gap-analyzer**:

- Use test-gap-analyzer to find untested functions
- Write outside-in tests for critical user-facing paths
- Use unit tests (from test-gap-analyzer) for internal functions

**philosophy-guardian**:

- Ensure test YAML follows ruthless simplicity
- Verify tests focus on behavior, not implementation

**pr-review-assistant**:

- Include outside-in tests in PR reviews
- Verify tests cover changed functionality
- Check test readability and clarity

**module-spec-generator**:

- Generate module specs that include outside-in test scenarios
- Use specs as templates for test YAML

### Example Combined Workflow

```bash
# 1. Analyze coverage gaps
claude "Use test-gap-analyzer on ./src"

# 2. Write outside-in tests for critical paths
claude "Use outside-in-testing to create web tests for authentication"

# 3. Verify philosophy compliance
claude "Use philosophy-guardian to review new test files"

# 4. Include in PR
git add tests/agentic/
git commit -m "Add outside-in tests for auth flow"
```

## Troubleshooting [LEVEL 2]

### Test Times Out

**Symptom**: Test exceeds timeout and fails

**Causes**:

- Application takes longer to start than expected
- Network requests are slow
- Element never appears (incorrect selector)

**Solutions**:

```yaml
# Increase timeout
- action: wait_for_element
  selector: ".slow-loading-element"
  timeout: 30s # Increase from default

# Add intermediate verification
- action: launch
  target: "./app"
- action: wait_for_output
  contains: "Initializing..."
  timeout: 5s
- action: wait_for_output
  contains: "Ready"
  timeout: 20s
```

### Element Not Found

**Symptom**: `verify_element` or `click` fails with "element not found"

**Causes**:

- Incorrect CSS selector
- Element not yet rendered (timing issue)
- Element in iframe or shadow DOM

**Solutions**:

```yaml
# Add wait before interaction
- action: wait_for_element
  selector: ".target-element"
  timeout: 10s
- action: click
  selector: ".target-element"

# Use more specific selector
- action: click
  selector: "button[data-testid='submit-button']"

# Handle iframe
- action: switch_to_iframe
  selector: "iframe#payment-frame"
- action: click
  selector: ".pay-now-button"
```

### Test Passes Locally, Fails in CI

**Symptom**: Test works on dev machine but fails in CI environment

**Causes**:

- Different screen size (web/Electron)
- Missing dependencies
- Timing differences (slower CI machines)
- Environment variable differences

**Solutions**:

```yaml
# Set explicit viewport size (web/Electron)
scenario:
  environment:
    viewport:
      width: 1920
      height: 1080

# Add longer timeouts in CI
- action: wait_for_element
  selector: ".element"
  timeout: 30s  # Generous for CI

# Verify prerequisites
prerequisites:
  - "Chrome browser installed"
  - "Environment variable API_KEY is set"
```

### Output Doesn't Match Expected

**Symptom**: `verify_output` fails even though output looks correct

**Causes**:

- Extra whitespace or newlines
- ANSI color codes in output
- Case sensitivity

**Solutions**:

```yaml
# Use flexible matching
- action: verify_output
  matches: "Result:\\s+Success" # Allow flexible whitespace

# Strip ANSI codes
- action: verify_output
  contains: "Success"
  strip_ansi: true

# Case-insensitive match
- action: verify_output
  contains: "success"
  case_sensitive: false
```

## Reference: Action Catalog [LEVEL 3]

### CLI Actions

| Action             | Parameters                       | Description                            |
| ------------------ | -------------------------------- | -------------------------------------- |
| `launch`           | `target`, `args`, `cwd`, `env`   | Start CLI application                  |
| `send_input`       | `value`, `delay`                 | Send text to stdin                     |
| `send_signal`      | `signal`                         | Send OS signal (SIGINT, SIGTERM, etc.) |
| `wait_for_output`  | `contains`, `matches`, `timeout` | Wait for text in stdout/stderr         |
| `verify_output`    | `contains`, `matches`, `stream`  | Check output content                   |
| `verify_exit_code` | `expected`                       | Validate exit code                     |
| `capture_output`   | `save_as`, `stream`              | Save output to file                    |

### TUI Actions

| Action               | Parameters                        | Description              |
| -------------------- | --------------------------------- | ------------------------ |
| `launch`             | `target`, `args`, `terminal_size` | Start TUI application    |
| `send_keypress`      | `value`, `times`, `modifiers`     | Send keyboard input      |
| `wait_for_screen`    | `contains`, `timeout`             | Wait for text on screen  |
| `verify_screen`      | `contains`, `matches`, `region`   | Check screen content     |
| `capture_screenshot` | `save_as`                         | Save terminal screenshot |
| `navigate_menu`      | `path`                            | Navigate menu structure  |
| `fill_form`          | `fields`                          | Fill TUI form fields     |

### Web Actions

| Action             | Parameters                                | Description            |
| ------------------ | ----------------------------------------- | ---------------------- |
| `navigate`         | `url`, `wait_for_load`                    | Go to URL              |
| `click`            | `selector`, `text`, `nth`                 | Click element          |
| `type`             | `selector`, `value`, `delay`              | Type into input        |
| `wait_for_element` | `selector`, `timeout`, `disappears`       | Wait for element       |
| `verify_element`   | `selector`, `contains`, `count`, `exists` | Check element state    |
| `verify_url`       | `equals`, `contains`, `matches`           | Validate URL           |
| `screenshot`       | `save_as`, `selector`, `full_page`        | Capture screenshot     |
| `scroll`           | `selector`, `direction`, `amount`         | Scroll page/element    |
| `select_option`    | `selector`, `value`                       | Select dropdown option |
| `checkbox`         | `selector`, `checked`                     | Check/uncheck checkbox |

### Electron Actions

| Action          | Parameters                             | Description                |
| --------------- | -------------------------------------- | -------------------------- |
| `launch`        | `target`, `args`, `wait_for_window`    | Start Electron app         |
| `window_action` | `window`, `action`                     | Interact with windows      |
| `menu_click`    | `path`                                 | Click menu items           |
| `dialog_action` | `type`, `action`, `filename`           | Handle dialogs             |
| `ipc_send`      | `channel`, `data`                      | Send IPC message           |
| `ipc_expect`    | `channel`, `timeout`                   | Wait for IPC message       |
| `verify_window` | `title`, `visible`, `focused`, `count` | Check window state         |
| All web actions |                                        | Electron includes Chromium |

### Common Parameters

| Parameter             | Type       | Description                          |
| --------------------- | ---------- | ------------------------------------ |
| `timeout`             | Duration   | Maximum wait time (e.g., "5s", "2m") |
| `description`         | String     | Human-readable step explanation      |
| `continue_on_failure` | Boolean    | Don't fail scenario if step fails    |
| `id`                  | String     | Step identifier for conditionals     |
| `condition`           | Expression | Execute step only if condition true  |

## Quick Reference: YAML Template [LEVEL 1]

```yaml
scenario:
  # Required fields
  name: "Test Name"
  description: "What this test verifies"
  type: cli | tui | web | electron

  # Optional metadata
  tags: [smoke, critical]
  timeout: 60s

  # What must be true before running
  prerequisites:
    - "Condition 1"
    - "Condition 2"

  # Environment setup
  environment:
    variables:
      VAR_NAME: "value"

  # Variables for templating
  variables:
    username: "testuser"

  # Test steps (executed in order)
  steps:
    - action: launch
      target: "./app"

    - action: send_input
      value: "command\n"

    - action: verify_output
      contains: "Success"
      timeout: 5s

  # Cleanup (always runs)
  cleanup:
    - action: stop_application
```

## Skill Usage Examples [LEVEL 1]

### Invoke This Skill

```
Claude, use the outside-in-testing skill to create a CLI test for my calculator app.

Claude, use outside-in-testing to generate web tests for the login flow.

Claude, create TUI tests using the outside-in-testing skill for file navigation.
```

### What You'll Get

1. **Complete YAML test scenario** matching your requirements
2. **Inline documentation** explaining each section
3. **Best practices applied** (timeouts, waits, verification)
4. **Appropriate complexity level** (1, 2, or 3 based on needs)
5. **Instructions for running** the test

### Example Request and Response

**User**: "Create a web test for user login with valid credentials"

**Claude** (using this skill):

```yaml
scenario:
  name: "User Login - Valid Credentials"
  description: "Verifies user can successfully log in with valid email and password"
  type: web
  tags: [smoke, auth, critical]

  prerequisites:
    - "User test@example.com exists with password 'TestPass123!'"
    - "Application is running on http://localhost:3000"

  steps:
    # Navigate to login page
    - action: navigate
      url: "http://localhost:3000/login"
      description: "Open login page"

    # Wait for page to fully load
    - action: wait_for_element
      selector: "form.login-form"
      timeout: 5s
      description: "Wait for login form to render"

    # Fill in email field
    - action: type
      selector: "input[name='email']"
      value: "test@example.com"
      description: "Enter email address"

    # Fill in password field
    - action: type
      selector: "input[name='password']"
      value: "TestPass123!"
      description: "Enter password"

    # Submit form
    - action: click
      selector: "button[type='submit']"
      description: "Click login button"

    # Wait for redirect to dashboard
    - action: wait_for_url
      contains: "/dashboard"
      timeout: 10s
      description: "Should redirect to dashboard after successful login"

    # Verify user is logged in
    - action: verify_element
      selector: ".user-profile"
      contains: "test@example.com"
      description: "User email should appear in profile widget"

    # Capture evidence
    - action: screenshot
      save_as: "successful-login.png"
      description: "Save screenshot of logged-in state"
# To run this test:
# 1. Save as test-login-valid.yaml
# 2. Run: gadugi-agentic-test run test-login-valid.yaml
# 3. Check evidence in ./evidence/user-login-valid-credentials-TIMESTAMP/
```

## Related Resources [LEVEL 1]

### Official Documentation

- **GitHub Repository**: https://github.com/rysweet/gadugi-agentic-test
- **Framework Docs**: See repo README and docs/ folder
- **Issue Tracker**: https://github.com/rysweet/MicrosoftHackathon2025-AgenticCoding/issues/1356

### Related Skills

- **test-gap-analyzer**: Find untested code paths
- **philosophy-guardian**: Review test philosophy compliance
- **pr-review-assistant**: Include tests in PR reviews
- **module-spec-generator**: Generate specs with test scenarios

### Further Reading

- Outside-in vs inside-out testing approaches
- Behavior-driven development (BDD) principles
- AI-powered testing best practices
- Test automation patterns

## Changelog [LEVEL 3]

### Version 1.0.0 (2025-11-16)

- Initial skill release
- Support for CLI, TUI, Web, and Electron applications
- 15 complete working examples
- Progressive disclosure levels (1, 2, 3)
- Embedded gadugi-agentic-test framework documentation (v0.1.0)
- Freshness check script for version monitoring
- Full integration with amplihack philosophy
- Comprehensive troubleshooting guide
- Action reference catalog

---

**Remember**: Outside-in tests verify WHAT your application does, not HOW it does it. Focus on user-visible behavior, and your tests will remain stable across refactorings while providing meaningful validation of critical workflows.

Start at Level 1 with simple smoke tests, and progressively add complexity only when needed. The framework's AI agents handle the hard parts - you just describe what should happen.
