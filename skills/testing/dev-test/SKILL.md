---
name: dev-test
description: "This skill should be used when the user needs to 'debug web applications', 'test UI interactions', 'capture screenshots or network requests', 'test desktop automation', or needs to select between testing tools. Routes to platform-specific E2E testing skills: Chrome MCP for debugging, Playwright for CI/CD, Hammerspoon for macOS, Linux for X11/Wayland."
---


## Where This Fits

```
Main Chat                          Task Agent
─────────────────────────────────────────────────────
dev-implement
  → dev-ralph-loop (loads dev-tdd)
    → dev-delegate
      → Task agent ──────────────→ uses dev-test (this skill)
                                     ↓ loads dev-tdd again
                                   has TDD protocol + gates
                                     → routes to specific tool
```

<EXTREMELY-IMPORTANT>
## Load TDD Enforcement (REQUIRED)

Before choosing testing tools, you MUST load the TDD skill to ensure gate compliance:

```
Skill(skill="workflows:dev-tdd")
```

This loads:
- Task reframing (your job is writing tests, not features)
- **The Execution Gate** (6 mandatory gates before E2E testing)
- **GATE 5: READ LOGS** (mandatory - cannot skip)
- The Iron Law of TDD (test-first approach)

**Read dev-tdd skill content now before selecting testing tools.**
</EXTREMELY-IMPORTANT>

**This skill routes to the right testing tool.** The loaded `dev-tdd` skill provides TDD protocol details.

## Contents

- [The Iron Law](#the-iron-law-of-testing)
- [Browser Testing Decision Tree](#browser-testing-decision-tree)
- [Platform Detection](#platform-detection)
- [Sub-Skills Reference](#sub-skills-reference)
- [Unit & Integration Tests](#unit--integration-tests)

<EXTREMELY-IMPORTANT>
## The Iron Law of Testing

**YOU MUST WRITE E2E TESTS FOR USER-FACING FEATURES. This is not negotiable.**

When your changes affect what users see or interact with, you MUST:
1. Write an E2E test that simulates user behavior
2. Run it and verify it PASSES (not just unit tests)
3. Document: "E2E: [test name] passes with [evidence]"
4. Include screenshot/snapshot for visual changes

**Unit tests prove components work. E2E tests prove YOUR feature works for users.**

### Rationalization Prevention

When you catch yourself thinking these rationalizations, STOP—you're about to skip E2E tests:

| Thought | Why You're Wrong | Do Instead |
|---------|-----------------|-----------|
| "Unit tests are enough" | Your unit tests don't test user flows. | Write E2E. |
| "E2E is too slow" | You're choosing slow tests < shipped bugs. | Write E2E. |
| "I'll add E2E later" | You won't. Your future self won't either. | Write it NOW. |
| "This is just backend" | Does it affect user output? Then YOU need E2E. | Write E2E. |
| "The tool setup is complex" | Your complexity = complex failure modes. E2E finds them. | Write E2E. |
| "The UI is unchanged" | Your assumption isn't proven. | Prove it with a visual snapshot. |
| "Manual testing is faster" | You're LYING about coverage to yourself. | Write E2E. |
| "It's just a small change" | Your small change breaks UIs. E2E proves it doesn't. | Write E2E. |
| "User can verify" | NO. You don't trust users with QA. | Automated verification or it didn't happen. |
| **"Log checking is my E2E test"** | **You're confusing observability with verification.** | **Verify your actual outputs.** |
| **"Screenshots are too hard to capture"** | **Your avoidance = hard to debug in production later.** | **Automate it.** |

### Fake E2E Detection - STOP

**If your "E2E test" does any of these, it's NOT E2E:**

| Pattern | Why It's Fake | Real E2E Alternative |
|---------|---------------|----------------------|
| `grep "success" logs.txt` | Only proves code ran | Verify actual output file/UI/API response |
| `assert mock.called` | Tests mock, not real system | Use real integration, verify real data |
| `cat output.txt \| wc -l` | File exists ≠ correct content | Read file, assert exact expected content |
| "I ran it manually" | No automation = no evidence | Capture manual test as automated test |
| Check log for icon name | Observability, not verification | Screenshot + visual diff of rendered icon |
| Exit code 0 | Process succeeded ≠ output correct | Verify the actual output data |

**The test:** If removing the actual implementation still passes your "E2E test", it's fake.

**Example of fake E2E that caught nothing:**
```python
# FAKE E2E - only checks logs
def test_icon_theme_change():
    run_command("set-theme papirus")
    logs = read_logs()
    assert "papirus" in logs  # ❌ FAKE - only proves code ran
    # BUG: 89% of icons weren't changed, test still passed!
```

**Real E2E that would have caught the bug:**
```python
# REAL E2E - verifies actual output
def test_icon_theme_change():
    run_command("set-theme papirus")
    screenshot = capture_desktop()
    assert visual_diff(screenshot, "expected_papirus.png") < threshold  # ✅ REAL
    # This would have shown 89% of icons were wrong
```

### Red Flags - STOP If Thinking:

If you catch yourself thinking these patterns, STOP—you're about to skip E2E:

| Thought | Why You're Wrong | Do Instead |
|---------|-----------------|-----------|
| "Tests pass" (only unit) | Your unit tests ≠ E2E | Write E2E test |
| "Code looks correct" | You're only looking ≠ running user flow | Run E2E |
| "It worked when I tried it" | Your manual testing ≠ automated | Capture as E2E |
| "Screenshot shows it works" | Your static screenshot ≠ interaction test | Add automation |
</EXTREMELY-IMPORTANT>

## Browser Testing Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    BROWSER TESTING REQUIRED?                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  Need to debug JS errors or API calls?       │
        │  (console.log, network requests, XHR)        │
        └─────────────────────────────────────────────┘
                    │                    │
                   YES                   NO
                    │                    │
                    ▼                    ▼
        ┌───────────────────┐  ┌──────────────────────────┐
        │   CHROME MCP      │  │  Running in CI/CD?        │
        │   (debugging)     │  │  (headless, automated)    │
        └───────────────────┘  └──────────────────────────┘
                                      │           │
                                     YES          NO
                                      │           │
                                      ▼           ▼
                        ┌──────────────┐  ┌───────────────────┐
                        │ PLAYWRIGHT   │  │ Cross-browser     │
                        │ MCP          │  │ needed?           │
                        └──────────────┘  └───────────────────┘
                                                │          │
                                               YES         NO
                                                │          │
                                                ▼          ▼
                                    ┌──────────────┐ ┌────────────┐
                                    │ PLAYWRIGHT   │ │ Either OK  │
                                    │ MCP          │ │ (prefer    │
                                    └──────────────┘ │ Playwright)│
                                                     └────────────┘
```

<EXTREMELY-IMPORTANT>
### Iron Laws: Browser MCP Selection

**YOU MUST USE CHROME MCP FOR API/CONSOLE DEBUGGING. NO EXCEPTIONS.**
**YOU MUST USE PLAYWRIGHT MCP FOR CI/CD TESTING. NO EXCEPTIONS.**

### Quick Decision Table

| Need | Tool | Why |
|------|------|-----|
| Debug console errors | **Chrome MCP** | `read_console_messages` |
| Inspect API calls/responses | **Chrome MCP** | `read_network_requests` |
| Execute custom JS in page | **Chrome MCP** | `javascript_tool` |
| Record interaction as GIF | **Chrome MCP** | `gif_creator` |
| Headless/CI automation | **Playwright MCP** | Headless mode |
| Cross-browser testing | **Playwright MCP** | Firefox/WebKit support |
| Standard E2E suite | **Playwright MCP** | Test isolation, maturity |
| Interactive debugging | **Chrome MCP** | Real browser, console access |

### Capability Comparison

| Capability | Playwright MCP | Chrome MCP |
|------------|---------------|------------|
| Navigate/click/type | ✅ | ✅ |
| Accessibility tree | ✅ `browser_snapshot` | ✅ `read_page` |
| Screenshots | ✅ | ✅ |
| **Console messages** | ❌ | ✅ `read_console_messages` |
| **Network requests** | ❌ | ✅ `read_network_requests` |
| **JavaScript execution** | ❌ | ✅ `javascript_tool` |
| **GIF recording** | ❌ | ✅ `gif_creator` |
| **Headless mode** | ✅ | ❌ (requires visible browser) |
| **Cross-browser** | ✅ (Chromium/Firefox/WebKit) | ❌ (Chrome only) |
| Natural language find | ❌ | ✅ `find` |

### Rationalization Prevention (Browser MCP)

| Thought | Why You're Wrong | Do Instead |
|---------|-----------------|-----------|
| "I'll check the console manually" | You can't capture all edge cases manually. | Use Chrome MCP `read_console_messages` |
| "I can infer the API response" | Your inference is wrong. Real data differs. | Use Chrome MCP `read_network_requests` |
| "Playwright can do everything" | You're wrong. It cannot read console or network. | Use Chrome MCP for debugging |
| "Chrome MCP is enough for CI" | You're ignoring constraints—it requires visible browser. | Use Playwright MCP for CI/CD |
| "I'll just look at DevTools" | Your manual inspection is not automated. | Automate with Chrome MCP |
| "Headless doesn't matter" | You're wrong. Your CI/CD requires headless. | Use Playwright MCP |
</EXTREMELY-IMPORTANT>

## Platform Detection

Detect the operating system and display server to select the appropriate testing tool:

```bash
# Detect platform for desktop automation
case "$(uname -s)" in
    Darwin) echo "macOS - use dev-test-hammerspoon" ;;
    Linux)
        if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
            echo "Linux/Wayland - use dev-test-linux (ydotool)"
        else
            echo "Linux/X11 - use dev-test-linux (xdotool)"
        fi
        ;;
esac
```

### Desktop Automation Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                   DESKTOP AUTOMATION REQUIRED?                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Platform?      │
                    └─────────────────┘
                    /        |         \
                 macOS    Linux      Windows
                   │         │           │
                   ▼         ▼           ▼
        ┌──────────────┐ ┌─────────┐ ┌─────────┐
        │ HAMMERSPOON  │ │ LINUX   │ │ NOT     │
        │ (dev-test-   │ │ (dev-   │ │ SUPPORTED│
        │ hammerspoon) │ │ test-   │ └─────────┘
        └──────────────┘ │ linux)  │
                         └─────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Display Server?  │
                    └───────────────────┘
                         /         \
                    Wayland        X11
                       │            │
                       ▼            ▼
                 ┌──────────┐ ┌──────────┐
                 │ ydotool  │ │ xdotool  │
                 └──────────┘ └──────────┘
```

## Sub-Skills Reference

<EXTREMELY-IMPORTANT>
### Tool Availability Gate

**Verify tools are available BEFORE proceeding. Missing tools = FULL STOP.**

Each sub-skill has its own availability gate. Load the appropriate skill and follow its gate.
</EXTREMELY-IMPORTANT>

### Browser Testing

| Skill | Use Case | Key Capabilities |
|-------|----------|------------------|
| `Skill(skill="workflows:dev-test-chrome")` | Debugging, console/network inspection | `read_console_messages`, `read_network_requests`, `javascript_tool` |
| `Skill(skill="workflows:dev-test-playwright")` | CI/CD, headless, cross-browser E2E | Headless mode, Firefox/WebKit, test isolation |

### Desktop Automation

| Skill | Platform | Primary Tool |
|-------|----------|--------------|
| `Skill(skill="workflows:dev-test-hammerspoon")` | macOS | Hammerspoon (`hs`) |
| `Skill(skill="workflows:dev-test-linux")` | Linux | ydotool (Wayland) / xdotool (X11) |

## Unit & Integration Tests

### Test Discovery

Locate test directories and identify the test framework used in the project:

```bash
# Find test directory
ls -d tests/ test/ spec/ __tests__/ 2>/dev/null

# Find test framework
cat package.json 2>/dev/null | grep -E "(test|jest)"
cat pyproject.toml 2>/dev/null | grep -i pytest
cat Cargo.toml 2>/dev/null | grep -i "\[dev-dependencies\]"
cat meson.build 2>/dev/null | grep -i test
```

### Common Test Frameworks

| Language | Framework | Command |
|----------|-----------|---------|
| Python | pytest | `pytest tests/ -v` |
| JavaScript | jest | `npm test` |
| TypeScript | vitest | `npx vitest` |
| Rust | cargo | `cargo test` |
| C/C++ | meson | `meson test -C build -v` |
| Go | go test | `go test ./...` |

### CLI Application Testing

Execute CLI applications with test inputs and verify outputs against expected results:

```bash
# Run with test inputs
./app --test-mode input.txt > output.txt

# Compare to expected
diff expected.txt output.txt

# Check exit code
./app --validate file && echo "PASS" || echo "FAIL"
```

## Output Requirements

**Every test run MUST be documented in LEARNINGS.md:**

```markdown
## Test Run: [Description]

**Tool:** [Chrome MCP / Playwright / Hammerspoon / ydotool / pytest / etc.]

**Command:**
```bash
pytest tests/ -v
```

**Output:**
```
tests/test_feature.py::test_basic PASSED
tests/test_feature.py::test_edge_case PASSED
tests/test_feature.py::test_error FAILED

1 failed, 2 passed
```

**Result:** 2/3 PASS, 1 FAIL

**Next:** Fix test_error failure
```

## Integration

For TDD protocol (RED-GREEN-REFACTOR), see:
```
Skill(skill="workflows:dev-tdd")
```

This skill is invoked by Task agents during `dev-implement` phase.
