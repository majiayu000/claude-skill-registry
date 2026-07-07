---
name: form-filling
description: |
  Fill out web forms, submit data, and handle login or registration flows.
  Trigger when the user asks to: fill a form, submit data on a website, log in to a site,
  register an account, complete a checkout, enter information into fields, or automate form submission.
allowed-tools: Bash(openbrowser-ai:*) Bash(curl:*) Bash(uv:*) Bash(irm:*) Read Write
---

# Form Filling

Automate filling web forms including login, registration, checkout, and multi-step form wizards using Python code execution.

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

### Step 1 -- Navigate to the form page

```bash
openbrowser-ai -c - <<'EOF'
await navigate("https://example.com/login")
state = await browser.get_browser_state_summary()
print(f"Page: {state.title} ({state.url})")
print(f"Interactive elements: {len(state.dom_state.selector_map)}")
EOF
```

### Step 2 -- Discover form fields

```bash
openbrowser-ai -c - <<'EOF'
# List all interactive elements with their indices
state = await browser.get_browser_state_summary()
for index, element in state.dom_state.selector_map.items():
    tag = element.tag_name
    text = element.get_all_children_text(max_depth=2)[:60]
    placeholder = element.attributes.get("placeholder", "")
    input_type = element.attributes.get("type", "")
    name = element.attributes.get("name", "")
    print(f"[{index}] <{tag}> type={input_type} name={name} placeholder=\"{placeholder}\" text=\"{text}\"")
EOF
```

### Step 3 -- Fill text inputs

```bash
openbrowser-ai -c - <<'EOF'
# Fill fields using their indices from Step 2
await input_text(index=5, text="user@example.com")
await input_text(index=7, text="secure-password")
EOF
```

For fields that need clearing first:

```bash
openbrowser-ai -c - <<'EOF'
await click(index=5)
await evaluate("document.activeElement.select()")
await input_text(index=5, text="new-value")
EOF
```

### Step 4 -- Handle dropdowns

Standard HTML select elements:

```bash
openbrowser-ai -c - <<'EOF'
await select_dropdown(index=12, text="United States")
EOF
```

To see available options first:

```bash
openbrowser-ai -c - <<'EOF'
options = await dropdown_options(index=12)
print(options)
EOF
```

Custom dropdown components:

```bash
openbrowser-ai -c - <<'EOF'
await evaluate("""
(function(){
  const select = document.querySelector("select#country");
  select.value = "US";
  select.dispatchEvent(new Event("change", { bubbles: true }));
})()
""")
EOF
```

### Step 5 -- Handle checkboxes and radio buttons

```bash
openbrowser-ai -c - <<'EOF'
await click(index=15)  # Click checkbox/radio

# Verify state
checked = await evaluate("""document.querySelector("input[name=agree]").checked""")
print(f"Checkbox checked: {checked}")
EOF
```

### Step 6 -- Submit the form

```bash
openbrowser-ai -c - <<'EOF'
await click(index=20)  # Click submit button
await wait(2)

# Verify submission
state = await browser.get_browser_state_summary()
print(f"After submit: {state.url}")
EOF
```

Or submit via JavaScript:

```bash
openbrowser-ai -c - <<'EOF'
await evaluate("document.querySelector(\"form\").submit()")
EOF
```

### Step 7 -- Verify submission result

```bash
openbrowser-ai -c - <<'EOF'
# Check for success/error messages
result = await evaluate("""
(function(){
  const success = document.querySelector(".success, .alert-success, [role=\"alert\"]");
  const error = document.querySelector(".error, .alert-danger, .validation-error");
  return {
    success: success?.textContent?.trim(),
    error: error?.textContent?.trim(),
    url: window.location.href
  };
})()
""")
print(result)
EOF
```

### Step 8 -- Handle multi-step forms

```bash
openbrowser-ai -c - <<'EOF'
for step in range(1, 5):
    # Discover fields for current step
    state = await browser.get_browser_state_summary()
    print(f"Step {step}: {len(state.dom_state.selector_map)} elements")

    # Fill fields (indices vary per step)
    # ... fill fields here ...

    # Click Next/Continue
    # Find the next button
    for idx, el in state.dom_state.selector_map.items():
        text = el.get_all_children_text(max_depth=1).lower()
        if "next" in text or "continue" in text:
            await click(index=idx)
            await wait(2)
            break
EOF
```

## Tips

- Code is piped via stdin using heredoc (`-c - <<'EOF'`), so all Python syntax works without shell escaping issues.
- Always discover fields with `browser.get_browser_state_summary()` before typing -- do not guess element indices.
- For sensitive data (passwords, tokens), confirm with the user before entering values.
- Use `evaluate()` to bypass custom components that do not respond to standard click/type.
- Variables persist between `-c` calls while the daemon is running, so you can store field indices in one call and use them in the next.
- Check for CAPTCHA or bot detection; notify the user if manual intervention is needed.

## Cleanup

This step is **mandatory**. Run it after the form submission finishes, whether the submit succeeded or the form rejected the input. Without it, the daemon keeps Chrome running until its 10-minute idle timeout, leaving a stale browser process, a locked profile, and (on macOS/Linux desktop) a visible window with the form still on screen.

Stop the daemon, then verify it is gone:

```bash
openbrowser-ai daemon stop
openbrowser-ai daemon status
```

`daemon stop` closes every tab, exits Chrome, flushes saved cookies/login state to the profile (so the next run reuses the login), and shuts down the daemon process. `daemon status` should report the daemon is not running. If it still reports running, the daemon is wedged, force-kill it:

```bash
pkill -f 'openbrowser.*daemon' || true
```

Form runs can fail mid-workflow (validation error, CAPTCHA, network drop). Guarantee cleanup with a shell trap so a half-filled form never leaks a browser:

```bash
trap 'openbrowser-ai daemon stop >/dev/null 2>&1 || true' EXIT
# ... openbrowser-ai -c calls here ...
```

Do not rely on the idle timeout. Do not call `done()` as a substitute, `done()` only marks the task complete inside the agent loop, it does not close the browser.
