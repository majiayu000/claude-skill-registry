---
name: mobile-testing-maestro
description: Maestro mobile E2E testing - YAML flows, selectors, flow control, environment variables, JavaScript expressions, device interactions, Maestro Studio, Maestro Cloud CI, tags, test suites
---

# Maestro Mobile UI Testing Patterns

> **Quick Guide:** Write E2E tests as declarative YAML flows. Use `id` selectors for stable element targeting (not text that changes with localization). Use `runFlow` to compose reusable subflows (login, setup). Use `waitForAnimationToEnd` before assertions on animated screens. Use `onFlowStart`/`onFlowComplete` hooks for setup/teardown. Maestro auto-retries assertions for up to 7 seconds before failing. Current stable: CLI 2.4.0.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `id` selectors (accessibility identifiers) as primary selectors - text selectors break with localization or copy changes)**

**(You MUST use `runFlow` for reusable sequences (login, onboarding) - NEVER duplicate steps across flow files)**

**(You MUST use `waitForAnimationToEnd` before assertions on screens with animations or transitions - assertions on animated elements are flaky)**

**(You MUST pair every `startRecording` with a `stopRecording` - unpaired commands produce corrupted or missing video files)**

**(You MUST use environment variables or `env` blocks for credentials and environment-specific values - NEVER hardcode secrets in YAML flows)**

</critical_requirements>

---

**Auto-detection:** Maestro, maestro, .maestro, maestro test, maestro cloud, maestro studio, launchApp, tapOn, assertVisible, assertNotVisible, inputText, scrollUntilVisible, runFlow, evalScript, runScript, swipe, hideKeyboard, waitForAnimationToEnd, onFlowStart, onFlowComplete, maestro.yaml, config.yaml tags

**When to use:**

- Writing E2E UI tests for iOS and Android mobile apps
- Automating user workflows (login, checkout, onboarding) with YAML flows
- Testing cross-platform behavior from a single flow file
- Running mobile tests in CI with Maestro Cloud
- Recording test execution for debugging or documentation
- Testing deep links, location, permissions, and device interactions

**When NOT to use:**

- Unit testing business logic (use your unit test framework)
- API-only testing without UI (use direct HTTP tests)
- Testing web-only applications without mobile component
- Performance profiling or load testing (Maestro is for functional UI flows)

**Key patterns covered:**

- Flow structure with appId, YAML commands, and selectors
- Selector strategies: id (preferred), text, point, relational, state
- Flow control: runFlow, repeat, retry, conditions (when), hooks
- Environment variables and parameterized flows
- JavaScript expressions: inline `${}`, evalScript, runScript, output object
- Device interactions: swipe, scroll, setLocation, openLink, permissions
- Workspace configuration: tags, test discovery, execution order
- Maestro Studio for visual flow creation and element inspection
- Maestro Cloud for CI integration with GitHub Actions

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Flow structure, selectors, assertions, input, navigation
- [examples/flow-control.md](examples/flow-control.md) - runFlow, repeat, retry, conditions, hooks, JavaScript
- [examples/device-interactions.md](examples/device-interactions.md) - Swipe, scroll, location, links, permissions, recording
- [reference.md](reference.md) - Command reference, CLI commands, workspace config, decision frameworks

---

<philosophy>

## Philosophy

Maestro takes a fundamentally different approach from code-based testing frameworks: **tests are declarative YAML, not imperative code**. This makes flows readable by anyone on the team, not just developers. The framework handles the hard parts of mobile testing automatically -- waiting for elements, retrying taps, tolerating animation delays -- so flows focus on _what_ to test, not _how_ to wait.

**Core principles:**

1. **Declarative over imperative** - YAML flows describe user intent, not implementation details
2. **Built-in tolerance** - Maestro auto-waits up to 7 seconds for elements, auto-retries taps, and handles animation delays without explicit waits
3. **Single flow, multiple platforms** - One YAML file can test both iOS and Android with platform conditions for differences
4. **Composition over duplication** - Extract reusable sequences (login, setup, teardown) into subflows with `runFlow`
5. **Stable selectors** - Use accessibility identifiers (`id`) over visible text to survive localization and copy changes

**Mental model:**

Maestro flows are recipes. Each step is an action a user would take. The framework handles timing, retries, and platform differences. You describe the journey, Maestro drives the car.

**When to use Maestro:**

- Smoke tests for critical user journeys (login, purchase, onboarding)
- Regression tests for flows that broke before
- Cross-platform verification with a single flow file
- Visual recording of test runs for stakeholder review

**When NOT to use Maestro:**

- Isolated unit tests for business logic
- API contract testing without UI
- Performance benchmarking or load testing
- Complex data-driven testing requiring heavy programmatic logic (Maestro's JS support is limited compared to full test frameworks)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Flow Structure and Basic Commands

Every flow starts with a configuration block (appId, optional env/tags) separated from commands by `---`. Commands execute sequentially top to bottom.

```yaml
appId: com.example.app
tags:
  - smoke
  - auth
---
- launchApp
- tapOn:
    id: "email_input"
- inputText: "user@example.com"
- tapOn:
    id: "password_input"
- inputText: "secure_password"
- tapOn:
    id: "login_button"
- assertVisible:
    id: "home_screen"
```

**Why good:** appId identifies the app under test, tags enable filtering with --include-tags/--exclude-tags, id selectors are stable across localizations, sequential commands read like a user story

See [examples/core.md](examples/core.md) for complete flow structure with env blocks, labels, and clearState.

---

### Pattern 2: Selector Strategies

Use `id` (accessibility identifier) as the primary selector. Fall back to `text` for static labels, `point` for coordinates only as last resort. Combine selectors for precision.

```yaml
# Preferred: id selector (stable, language-independent)
- tapOn:
    id: "submit_button"

# Fallback: text selector (breaks with i18n changes)
- tapOn:
    text: "Submit"

# Relational: below/above/childOf for disambiguation
- tapOn:
    text: "Delete"
    below: "Shopping Cart"

# State selectors: filter by element state
- tapOn:
    id: "toggle_switch"
    enabled: true
```

**Why good:** id selectors survive text changes, relational selectors disambiguate duplicate labels, state selectors prevent tapping disabled elements

See [examples/core.md](examples/core.md) for all selector types including index, point, and combined selectors.

---

### Pattern 3: Reusable Subflows with runFlow

Extract repeated sequences into separate flow files. Pass context via `env` parameters. Use `label` for clear test reports.

```yaml
# Main flow: checkout-test.yaml
appId: com.example.app
---
- runFlow:
    file: subflows/login.yaml
    env:
      USERNAME: "test_user@example.com"
      PASSWORD: "test_password"
    label: "Log in as test user"
- tapOn:
    id: "cart_icon"
- runFlow:
    file: subflows/complete-checkout.yaml
    label: "Complete purchase flow"
- assertVisible:
    id: "order_confirmation"
```

```yaml
# Subflow: subflows/login.yaml
appId: com.example.app
---
- tapOn:
    id: "email_input"
- inputText: ${USERNAME}
- tapOn:
    id: "password_input"
- inputText: ${PASSWORD}
- tapOn:
    id: "login_button"
```

**Why good:** login sequence defined once and reused across all flows, env parameters make subflows configurable, labels improve test report readability

See [examples/flow-control.md](examples/flow-control.md) for inline subflows, conditional flows, and nested composition.

---

### Pattern 4: Conditions and Platform-Specific Logic

Use `when` with `platform`, `visible`, `notVisible`, or JavaScript `true` expressions to handle differences between iOS and Android or optional UI states.

```yaml
# Platform-specific permission handling
- runFlow:
    when:
      platform: Android
    commands:
      - tapOn: "Allow"

- runFlow:
    when:
      platform: iOS
    commands:
      - tapOn: "Allow While Using App"

# Dismiss optional popup if visible
- runFlow:
    when:
      visible: "Rate this app"
    commands:
      - tapOn: "Not now"
```

**Why good:** single flow handles both platforms, visibility conditions handle non-deterministic UI (popups, tooltips), no test failure on missing optional elements

See [examples/flow-control.md](examples/flow-control.md) for JavaScript conditions and combined conditions.

---

### Pattern 5: Environment Variables and Parameterized Flows

Pass runtime values via CLI flags (`-e`), shell variables (`MAESTRO_` prefix), or `env` blocks in flow files. Use `${}` syntax for interpolation with JavaScript fallback defaults.

```yaml
appId: com.example.app
env:
  BASE_URL: "https://staging.example.com"
  DEFAULT_USER: "qa_user@example.com"
---
- launchApp
- tapOn:
    id: "email_input"
- inputText: ${USERNAME || DEFAULT_USER}
```

```bash
# Override from CLI
maestro test -e USERNAME=admin@example.com -e PASSWORD=secret flow.yaml
```

**Why good:** secrets never hardcoded in flow files, env blocks provide defaults, CLI overrides enable multi-environment testing, `||` fallback prevents failures when variables are missing

See [examples/flow-control.md](examples/flow-control.md) for built-in variables, runScript with env, and shell variable patterns.

---

### Pattern 6: Hooks for Setup and Teardown

Use `onFlowStart` and `onFlowComplete` in the configuration block for consistent setup/teardown across all flows. `onFlowComplete` runs even if the flow fails.

```yaml
appId: com.example.app
onFlowStart:
  - clearState
  - runFlow:
      file: subflows/login.yaml
      env:
        USERNAME: "test_user@example.com"
        PASSWORD: "test_password"
onFlowComplete:
  - runFlow: subflows/cleanup.yaml
---
- tapOn:
    id: "settings_icon"
- assertVisible:
    id: "settings_screen"
```

**Why good:** clearState ensures clean app state, login runs before every flow, cleanup always runs (even on failure), prevents test pollution between flows

**Hook failure behavior:** If `onFlowStart` fails, the main flow is skipped but `onFlowComplete` still executes. If `onFlowComplete` fails, the flow is marked as failed even if the main test passed.

See [examples/flow-control.md](examples/flow-control.md) for hooks with environment variables and script-based teardown.

---

### Pattern 7: JavaScript Expressions

Use inline `${}` for simple interpolation, `evalScript` for variable computation, and `runScript` for complex logic in external `.js` files. All share a global `output` object.

```yaml
# Inline expression
- inputText: user_${Date.now()}@test.com

# evalScript for computation
- evalScript: ${output.timestamp = Date.now()}
- inputText: ${output.timestamp}

# runScript for complex logic (external file)
- runScript: scripts/generate-test-data.js
- inputText: ${output.generatedEmail}
```

**Why good:** inline expressions handle simple dynamic values, evalScript sets variables without UI interaction, runScript keeps complex logic in testable JS files, output object passes data between steps

See [examples/flow-control.md](examples/flow-control.md) for HTTP requests in scripts, DataFaker, and output namespacing.

</patterns>

---

<decision_framework>

## Decision Framework

### Selector Choice

```
Can you add an accessibility identifier (testID/accessibilityIdentifier)?
|-- YES -> Use id selector (most stable)
+-- NO  -> Is the text static and unique on screen?
    |-- YES -> Use text selector
    +-- NO  -> Is there a unique parent or sibling?
        |-- YES -> Use relational selector (below, childOf, etc.)
        +-- NO  -> Use point selector as last resort (fragile)
```

### Flow Organization

```
Is this sequence used in 2+ flows?
|-- YES -> Extract to subflows/ directory, call with runFlow
+-- NO  -> Keep inline in the flow

Does the flow need setup/teardown?
|-- YES -> For ALL flows: use onFlowStart/onFlowComplete in config.yaml
|          For ONE flow: use runFlow at start/end of that flow
+-- NO  -> Start with launchApp directly

Is there platform-specific behavior?
|-- YES -> Use when: platform: Android/iOS conditions
+-- NO  -> Single flow handles both platforms
```

### When to Use JavaScript

```
Need a dynamic value (timestamp, random ID)?
|-- YES -> Inline ${} expression (e.g., ${Date.now()})
+-- NO  -> Need to compute and store a value?
    |-- YES -> evalScript for simple computation
    +-- NO  -> Need HTTP calls, file I/O, or complex logic?
        |-- YES -> runScript with external .js file
        +-- NO  -> Plain YAML commands are sufficient
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `text` selectors for buttons/labels that will be localized - breaks when language changes. Use `id` (accessibility identifiers) instead.
- Duplicating login/setup steps in every flow file - extract to subflow and call with `runFlow`
- Missing `stopRecording` after `startRecording` - produces corrupted or zero-byte video files
- Hardcoding credentials or API keys in YAML flow files - use environment variables with `-e` or `MAESTRO_` prefix
- Using arbitrary `sleep` or `extendedWaitUntil` with long timeouts instead of `waitForAnimationToEnd` - Maestro's built-in tolerance handles most timing issues automatically

**Medium Priority Issues:**

- Not using `clearState` or `clearKeychain` in setup - test results depend on leftover app state from previous runs
- Not using `tags` for flow categorization - makes it impossible to run targeted subsets (smoke, regression, etc.)
- Using `point` selectors (coordinates) as primary strategy - breaks on different screen sizes and resolutions
- Not using `label` on runFlow calls - test reports show file paths instead of meaningful step descriptions
- Putting all flows in the root directory without subdirectories - becomes unmanageable beyond 20+ flows

**Gotchas and Edge Cases:**

- `assertVisible` auto-retries for 7 seconds before failing - this is a feature, not a bug. Don't add explicit waits before assertions.
- CLI parameters are always strings - use `parseInt()` or comparison in JavaScript if you need numeric logic
- `MAESTRO_` prefixed shell variables are automatically available in flows but only via CLI, not Maestro Studio
- The string `"false"` is truthy in JavaScript - use explicit `=== "true"` comparison in `when: true:` conditions
- `onFlowComplete` runs even when the flow fails - design teardown logic that doesn't assume success
- `runFlow` with `commands` (inline) and `runFlow` with `file` (external) are mutually exclusive - you cannot use both in the same runFlow call
- Template literals (backticks) do not work inside `evalScript` because the command is already wrapped in `${}` - use string concatenation instead
- `console.log` in `evalScript` writes to `maestro.log`, not the terminal - use `runScript` for terminal-visible logging
- `retry` maxRetries is capped at 3 - for more attempts, restructure the flow logic
- Maestro Cloud `--async` flag returns immediately without waiting for results - poll the API or use webhooks for completion
- FlashList / RecyclerView items may not have stable accessibility IDs - use `scrollUntilVisible` with text fallback for list items

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `id` selectors (accessibility identifiers) as primary selectors - text selectors break with localization or copy changes)**

**(You MUST use `runFlow` for reusable sequences (login, onboarding) - NEVER duplicate steps across flow files)**

**(You MUST use `waitForAnimationToEnd` before assertions on screens with animations or transitions - assertions on animated elements are flaky)**

**(You MUST pair every `startRecording` with a `stopRecording` - unpaired commands produce corrupted or missing video files)**

**(You MUST use environment variables or `env` blocks for credentials and environment-specific values - NEVER hardcode secrets in YAML flows)**

**Failure to follow these rules will produce flaky tests, broken recordings, and security-exposed credentials in version control.**

</critical_reminders>
