---
name: e2e-testing
description: |
  Test web applications end-to-end by simulating user interactions and verifying expected outcomes.
  Trigger when the user asks to: test a web app, verify a user flow, run end-to-end tests,
  QA a feature, check that a page works correctly, validate user journeys, or test a deployment.
allowed-tools: Bash(openbrowser-ai:*) Bash(curl:*) Bash(uv:*) Bash(irm:*) Read Write
---

# End-to-End Testing

Simulate real user interactions and verify web application behavior using Python code execution. Covers navigation, form interaction, content assertions, and multi-page flows.

All code runs via `openbrowser-ai -c`. The daemon starts automatically and persists variables across calls. All browser functions are async -- use `await`.

The CLI daemon also persists cookies and login state in `~/.config/openbrowser/profiles/daemon/storage_state.json`, so authenticated sessions can be reused across later runs.

## Setup

Before running, verify openbrowser-ai is installed:

```bash
openbrowser-ai --help
```

If not found, install:

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.ps1 | iex
```

## Workflow

### Step 1 -- Navigate and verify page load

```bash
openbrowser-ai -c - <<'EOF'
await navigate("https://staging.example.com")
state = await browser.get_browser_state_summary()

assert "example" in state.url.lower(), f"Unexpected URL: {state.url}"
assert state.title, "Page title is empty"
print(f"Page loaded: {state.title} ({state.url})")
EOF
```

### Step 2 -- Content assertions

```bash
openbrowser-ai -c - <<'EOF'
# Check for expected text using JS
has_welcome = await evaluate("""
(function(){ return !!document.body.textContent.match(/Welcome to Example App/i) })()
""")
assert has_welcome, "Welcome message not found"

# Check specific element content
h1_text = await evaluate("document.querySelector('h1')?.textContent?.trim()")
assert h1_text == "Example App", f'Expected "Example App", got "{h1_text}"'

# Check no error messages
error_count = await evaluate("document.querySelectorAll('.error-message').length")
assert error_count == 0, f"Found {error_count} error messages on page"

print("All content assertions passed")
EOF
```

### Step 3 -- Test user interactions (login flow)

```bash
openbrowser-ai -c - <<'EOF'
# Get form fields
state = await browser.get_browser_state_summary()
for idx, el in state.dom_state.selector_map.items():
    if el.attributes.get("type") in ("email", "text", "password") or el.tag_name == "button":
        etype = el.attributes.get("type", "")
        placeholder = el.attributes.get("placeholder", "")
        print(f"[{idx}] <{el.tag_name}> type={etype} placeholder=\"{placeholder}\"")

# Fill and submit
await input_text(index=3, text="test@example.com")
await input_text(index=4, text="test-password")
await click(index=5)  # Login button
await wait(2)

# Assert logged in
state = await browser.get_browser_state_summary()
assert "dashboard" in state.url.lower() or "welcome" in state.title.lower(), \
    f"Login may have failed. URL: {state.url}, Title: {state.title}"
print("Login test passed")
EOF
```

### Step 4 -- Test navigation flows

```bash
openbrowser-ai -c - <<'EOF'
# Click settings link
state = await browser.get_browser_state_summary()
for idx, el in state.dom_state.selector_map.items():
    if "settings" in el.get_all_children_text(max_depth=1).lower():
        await click(index=idx)
        break

await wait(1)

# Assert URL changed
path = await evaluate("window.location.pathname")
assert "/settings" in path, f"Expected /settings path, got {path}"

# Test back button
await go_back()
await wait(1)
state = await browser.get_browser_state_summary()
print(f"After back: {state.url}")
EOF
```

### Step 5 -- Test error handling

```bash
openbrowser-ai -c - <<'EOF'
# Submit form with invalid data
await input_text(index=3, text="not-an-email")
await click(index=5)
await wait(1)

# Assert validation errors appear
errors = await evaluate("""
(function(){
  const errs = document.querySelectorAll(".error, .invalid-feedback, [aria-invalid=\"true\"]");
  return Array.from(errs).map(e => e.textContent.trim());
})()
""")
assert len(errors) > 0, "Expected validation errors but found none"
print(f"Validation errors shown: {errors}")

# Assert page did not navigate
path = await evaluate("window.location.pathname")
print(f"Still on: {path}")
EOF
```

### Step 6 -- Test responsive behavior

```bash
openbrowser-ai -c - <<'EOF'
viewport = await evaluate("""
(function(){
  return {
    width: window.innerWidth,
    height: window.innerHeight
  }
})()
""")
vw = viewport["width"]
vh = viewport["height"]
print(f"Viewport: {vw}x{vh}")

# Check mobile menu visibility
mobile_display = await evaluate("""
(function(){
  const el = document.querySelector(".mobile-menu");
  return el ? window.getComputedStyle(el).display : "not found";
})()
""")
print(f"Mobile menu display: {mobile_display}")
EOF
```

### Step 7 -- Test multi-page flows

```bash
openbrowser-ai -c - <<'EOF'
test_results = []

# Cart page
await navigate("https://staging.example.com/cart")
await wait(1)
cart_title = await evaluate("document.querySelector('h1')?.textContent?.trim()")
test_results.append({"test": "cart_page_loads", "passed": cart_title is not None, "detail": cart_title})

# Checkout
cart_count = await evaluate("JSON.parse(localStorage.getItem('cart'))?.items?.length || 0")
test_results.append({"test": "cart_has_items", "passed": cart_count > 0, "detail": f"{cart_count} items"})

# Print results
import json
passed = sum(1 for t in test_results if t["passed"])
total = len(test_results)
print(f"\nResults: {passed}/{total} passed")
print(json.dumps(test_results, indent=2))
EOF
```

## Tips

- Code is piped via stdin using heredoc (`-c - <<'EOF'`), so all Python syntax works without shell escaping issues.
- Use Python `assert` statements for test assertions -- they produce clear error messages on failure.
- Always verify page state after each interaction before proceeding.
- Test both happy paths and error paths for thorough coverage.
- Use `await wait(N)` after interactions that trigger page loads or animations.
- Variables persist between `-c` calls while the daemon is running, so you can accumulate test results across calls.
- Use `evaluate()` for DOM state assertions and `browser.get_browser_state_summary()` for page metadata.

## Cleanup

This step is **mandatory**. Run it after the test run finishes, whether assertions passed or failed. Without it, the daemon keeps Chrome running until its 10-minute idle timeout, leaving a stale browser process, a locked profile, and (on macOS/Linux desktop) a visible window.

Stop the daemon, then verify it is gone:

```bash
openbrowser-ai daemon stop
openbrowser-ai daemon status
```

`daemon stop` closes every tab, exits Chrome, flushes saved cookies/login state to the profile, and shuts down the daemon process. `daemon status` should report the daemon is not running. If it still reports running, the daemon is wedged, force-kill it:

```bash
pkill -f 'openbrowser.*daemon' || true
```

E2E runs fail often by design (that is what assertions are for). Guarantee cleanup with a shell trap so a failed assertion never leaks a browser:

```bash
trap 'openbrowser-ai daemon stop >/dev/null 2>&1 || true' EXIT
# ... openbrowser-ai -c calls here ...
```

Do not rely on the idle timeout. Do not call `done()` as a substitute, `done()` only marks the task complete inside the agent loop, it does not close the browser.
