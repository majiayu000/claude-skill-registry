---
name: manual-e2e-testing
description: "Run manual E2E tests for Flutter/mobile apps using Appium and Dart MCPs. Use when verifying mobile app behavior. Not for screenshot-based testing or non-mobile E2E."
user-invocable: true
---

# Manual E2E Testing with Appium & Dart MCP

Appium MCP and Dart MCP testing workflows with hot reload and widget tree analysis.

## Core Philosophy: Text-First Testing

**Why avoid screenshots?**

- Vision LLMs are unreliable for precise UI validation
- Visual changes break tests unnecessarily
- Hard to verify logical state changes
- Text and properties are more reliable
- Element states are programmatically verifiable

## Dual MCP Architecture

**Appium MCP** handles:

- Element discovery and interaction
- UI state verification through programmatic access
- Text content retrieval and validation
- Scrolling and gesture simulation

**Dart MCP** handles:

- Widget tree introspection and analysis
- Runtime error diagnosis and stack traces
- Hot reload capabilities for faster iteration
- App state inspection and debugging

**Combined workflow:**

1. Connect to Dart Tooling Daemon + Create Appium session
2. Widget analysis with `get_widget_tree`
3. Element discovery with Appium
4. State validation (both Appium + Dart)
5. Error diagnosis with `get_runtime_errors`
6. Hot reload for rapid iteration

## Pre-Test Setup

**Step 1: Verify Emulator**

```bash
adb devices
```

- Ensure device shows as "device" (not "offline" or "unauthorized")
- If no device: `emulator -avd <device_name>`

**Step 2: Clear App Data**

```bash
adb shell pm clear com.voicenoteplus.app
```

**Step 3: Connect to Dart Tooling Daemon**

- Use `mcp__dart__connect_dart_tooling_daemon`

**Step 4: Launch Flutter App**

- Ensure running: `flutter run`

**Step 5: Create Appium Session**

- Platform: `android`
- Capabilities: platformVersion, deviceName, automationName

**Step 6: Verify App Launch**

- Find element by ID: `com.voicenoteplus.app:id/dashboard`
- Cross-verify with widget tree

## Element Discovery

**Priority Order:**

1. **Resource IDs** (most stable)
   - Example: `com.voicenoteplus.app:id/record_button`
2. **Accessibility IDs** (second most stable)
   - Example: `Record`, `Settings`, `Save`
3. **Class names** (moderately stable)
   - Example: `android.widget.Button`
4. **XPath** (least stable, last resort)
   - Example: `//*[contains(@content-desc, "Record")]`

**Binary test:** "Is element stable across app updates?" → Use resource ID or accessibility ID.

## Validation Techniques

### Text Content Verification

```bash
mcp__appium-mcp__appium_get_text
  elementUUID: [from discovery]
```

- Verify button text contains expected content
- Check transcription area state
- Verify state changes

### Element State Checks

```bash
mcp__appium-mcp__appium_get_element_attribute
  elementUUID: [from discovery]
  attribute: enabled
```

- Check `enabled` attribute
- Check `displayed` attribute

### Widget Tree Analysis

```bash
mcp__dart__get_widget_tree
  summaryOnly: false
```

- Extract complete widget hierarchy
- Verify layout structure
- Analyze widget composition

### Runtime Error Analysis

```bash
mcp__dart__get_runtime_errors
  clearRuntimeErrors: true
```

- Check for runtime exceptions
- Analyze stack traces
- Verify no errors during interactions

## Test Procedures

### Basic Interaction Test

1. Pre-check: Runtime errors
2. Widget tree analysis
3. Find element by accessibility ID
4. Verify initial state
5. Tap element
6. Wait for state change
7. Verify state changed (both Appium + Dart)

### Complete Workflow

1. Start recording
2. Verify recording indicator
3. Simulate audio capture
4. Monitor runtime state
5. Stop recording
6. Verify transcription
7. Verify toolbar state

### Settings Configuration

1. Navigate to settings
2. Verify API key field
3. Input API key
4. Verify input
5. Save settings
6. Verify success message

**Binary test:** "Does this validate state changes programmatically?" → Use text content and element attributes.

## Error Handling

### Retry Pattern

- **Attempt 1**: Try immediately
- **If fails**: Wait 1 second, retry
- **If fails**: Wait 2 seconds, retry
- **If fails**: Wait 4 seconds, retry
- **After 3 attempts**: Report failure

### Fallback Strategy Chain

1. Try ID-based discovery
2. Try accessibility-based discovery
3. Try class-based discovery
4. Try XPath as last resort
5. Report which strategy succeeded

### State Verification

- **Before action**: Verify element present
- **During action**: Monitor state changes
- **After action**: Verify expected state
- **If state incorrect**: Retry or report failure

## Best Practices

**Before Testing:**

- Verify emulator running
- Clear app data
- Connect Dart Tooling Daemon early
- Launch Flutter app
- Create Appium session
- Check runtime errors
- Get initial widget tree

**During Testing:**

- Always verify element presence before interaction
- Cross-verify widget state with Dart MCP
- Use text content for validation (not visual)
- Implement retry logic
- Log every step with timestamps
- Verify state changes after each action
- Use accessibility IDs when available
- Use hot reload for rapid iteration

**After Testing:**

- Delete Appium session
- Check final runtime errors
- Save test execution log
- Document issues found

## Common Pitfalls

**Don't Use:**

- Screenshots for validation
- Hard-coded pixel coordinates
- Visual color/position assertions
- Unstable XPath expressions
- Timing sleeps

**Do Use:**

- Text content verification
- Element attribute checks
- State-based waiting
- Accessibility IDs
- Page source text search
- Structured logging

**Binary test:** "Is this validation programmatically checkable?" → If no, redesign the test.

## Essential Tools Reference

**Appium MCP:**

- `appium_find_element` - Locate element
- `appium_get_text` - Read text content
- `appium_click` - Tap element
- `appium_set_value` - Enter text
- `appium_get_page_source` - Get page source
- `appium_scroll` - Scroll screen

**Dart MCP:**

- `get_widget_tree` - Get widget hierarchy
- `get_runtime_errors` - Retrieve exceptions
- `get_selected_widget` - Inspect focused widget
- `hot_reload` - Apply changes without restart
- `hot_restart` - Restart with changes
- `get_app_logs` - Retrieve Flutter output

---

<critical_constraint>
MANDATORY: Use text/content validation, not screenshots
MANDATORY: Cross-verify widget state with Dart MCP alongside Appium
MANDATORY: Prefer resource/accessibility IDs over XPath for element discovery
MANDATORY: Implement retry logic with exponential backoff
MANDATORY: Verify element presence before any interaction
No exceptions. Text-first validation is reliable; visual validation is not.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

## Validation Pattern

Use native tools to validate skill structure:

**Glob: Verify skill structure exists**

- `Glob: pattern "**/SKILL.md" in skill directory` → Main skill file
- `Glob: pattern "**/references/*.md"` → Reference files
- `Glob: pattern "**/scripts/*.sh"` → Scripts directory

**Grep: Verify frontmatter**

- `Grep: search for "^name: manual-e2e-testing" in SKILL.md` → Name field
- `Grep: search for "^description:" in SKILL.md` → Description field
- `Grep: search for "^---" in SKILL.md` → Frontmatter markers

**Read: Check file contents**

- `Read: SKILL.md` → Verify structure and content
- `Read: references/` → Verify reference files exist

**Validation workflow**:

1. `Glob: pattern "**/SKILL.md"` in skill dir → Confirm main file exists
2. `Glob: pattern "**/references/"` → Verify references directory
3. `Grep: search for "^name:\|^description:"` → Verify required fields
4. `Grep: search for "<critical_constraint>"` → Check for constraints

---
