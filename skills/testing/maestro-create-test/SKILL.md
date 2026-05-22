---
name: maestro-create-test
description: Interactively create a Maestro E2E test flow by inspecting the live device screen and building the YAML step by step. Use when the user wants to create a new Maestro test, write a new E2E flow, build a test from the device, or says "create a maestro test" or "record a test flow".
---

# Create Maestro Test (Interactive)

Build a Maestro test YAML by exploring the live app — research the codebase for navigation paths, use the maestro-explore approach to figure out what commands to run, then record each verified step into the test file.

## Prerequisites

- A device/simulator must be running with the app installed
- The app should be in the state where the test should begin (usually login screen)
- Get the device ID via `user-maestro-list_devices`

## MCP Tool Usage Rules

**CRITICAL: Understand the two flow execution tools and when to use each.**

### `run_flow` — inline ad-hoc commands only

Use for single commands or short sequences that don't reference external files. The YAML is written to a temp file, so `runFlow: file:` references with relative paths **will break**.

```yaml
# GOOD — inline commands
- tapOn:
    id: portfolio-screen-tab

# GOOD — multiple inline commands
- tapOn: "Change portfolio"
- waitForAnimationToEnd
- assertVisible: "All Portfolios"

# BAD — file references break because temp file is in /tmp
- runFlow:
    file: ../../utils/login.yml
```

### `run_flow_files` — run existing .yml flow files

Use when you need to run an existing flow file (login, startApp, etc.) that lives in the workspace. Pass the **workspace-relative path**.

```
run_flow_files(device_id, flow_files="maestro/flows/portfolio/changePortfolioSingleDefcon.yml")
```

You can also pass env vars via the `env` parameter.

### Summary

| Need | Tool | Example |
|------|------|---------|
| Run a saved flow file | `run_flow_files` | Login flow, existing test |
| Tap / scroll / assert on live device | `run_flow` | `- tapOn: "Settings"` |
| Navigate with file + inline steps | `run_flow_files` first, then `run_flow` for subsequent steps | Login via file, then tap around inline |

## Workflow

### Phase 1: Gather Requirements

Collect from the user (use AskQuestion when available):

1. **Test name**: descriptive name for the flow file
2. **What to test**: the user journey to cover
3. **Starting point**: which screen to begin from
4. **Account type** (optional): single account, multiple accounts, IRA, etc. (affects login user)

### Phase 2: Learn Project Conventions

Before writing anything, study the existing test suite to learn the project's patterns.

#### 2a. Discover project structure

Use Glob to find the test directory layout:

```
maestro/**/*.yml
maestro/**/*.yaml
```

Identify:
- Where flows live (e.g., `maestro/flows/`, organized by feature?)
- Where utilities/shared flows live (e.g., `maestro/utils/`)
- Any config files (e.g., `maestro/config.yml`)

#### 2b. Read 2-3 existing tests

Pick tests that are **similar to what the user wants to create** (same feature area or similar complexity). Read them fully to learn:

- **Header format**: `appId`, `env`, `tags`, `jsEngine`, separator (`---`)
- **How tests start**: utility flows for app launch, login, navigation
- **Selector conventions**: do they prefer `id:` vs `text:`? naming patterns?
- **Assertion style**: how often, what gets asserted, regex patterns in env vars?
- **Env var patterns**: how defaults are defined and overridden
- **Comment style**: how and where comments are used
- **Relative paths**: depth from flow files to utils (e.g., `../../utils/`)

#### 2c. Read utility flows

Read the shared utility flows (login, startApp, etc.) to understand:
- What env vars they expect
- What state the app is in after they run
- Any conditional logic or platform handling

#### 2d. Synthesize conventions

From what you read, extract the concrete patterns to follow. Do NOT assume patterns — only use what you actually observed in the codebase.

### Phase 3: Research Navigation Paths

Before touching the device, search the codebase to figure out how to reach each screen in the test journey. This is the key to building steps efficiently.

#### 3a. Search existing Maestro flows

```
Grep: "<target screen/feature keywords>" in maestro/flows/
Glob: maestro/flows/**/*.yml
```

If an existing flow already navigates to the target screen, read it to extract the exact navigation path. This can shortcut entire sections of the test.

#### 3b. Search the source code

```
Grep: "<target keywords>" in src/
```

Look for screen names, navigation routes, tab labels, or accessibility IDs that match screens you need to visit. This tells you what elements to tap and what IDs to use as selectors.

#### 3c. Build a navigation hypothesis

From your research, form a hypothesis for each screen the test needs to reach:
- Which tab? (dashboard, portfolio, profile)
- How deep? (top-level, nested screen, modal)
- Any prerequisite state? (specific account type, feature flag)
- What selectors to use? (IDs or text found in source)

### Phase 4: Scaffold the File

Create the test file following the conventions discovered in Phase 2:

- Place it in the correct directory matching existing organization
- Use the same header format (appId, env, tags, separator) as existing tests
- Use the same startup/login flows with the same env var patterns
- Calculate the correct relative path to utils

### Phase 5: Bootstrap the App State

Get the device to the starting point using the appropriate tool:

- If an existing flow file gets you there, use `run_flow_files` with the workspace-relative path
- Otherwise, write a temp flow file in `maestro/flows/_temp_explore.yml` with login + initial navigation, then run it via `run_flow_files` to avoid relative-path issues

**Path depth matters:** flows in `maestro/flows/` use `../utils/`, flows in `maestro/flows/subdir/` use `../../utils/`.

Default users (choose based on test needs):
- `single-defcon@guideline.test` — single 401k account
- `multi-defcon@guideline.test` — multiple accounts

Record the startup steps in the YAML file.

### Phase 6: Build Steps Iteratively (Explore Loop)

Use the explore approach to figure out and verify each step. Repeat this loop until the test journey is complete.

#### Step 1 — Inspect

1. `user-maestro-inspect_view_hierarchy` — get all elements with text, IDs, bounds, states
2. `user-maestro-take_screenshot` — visual context of current screen

#### Step 2 — Decide

Combine your Phase 3 research with what you see on screen. Scan the hierarchy for:

- **Target found?** — If the next screen/element in the test journey is visible, proceed to interact with it
- **Clue elements** — Buttons, tabs, or list items that match your navigation hypothesis
- **Scrollable content** — If the target might be below the fold, scroll first

Decision priority:
1. Use a selector you found in Phase 3 research (ID from source code or existing test)
2. Tap an element that exactly or partially matches the target
3. Tap a navigation element that likely leads to the target (based on hypothesis)
4. Scroll down to reveal more content
5. Back out and try a different path

Use the selector and assertion conventions you learned in Phase 2. Refer to Maestro command docs if needed (`user-maestro-query_docs` or `user-maestro-cheat_sheet`).

Common actions:
- **Verify content**: `assertVisible`
- **Tap element**: `tapOn` (use the selector style from existing tests)
- **Enter text**: `tapOn` field + `inputText`
- **Scroll**: `scrollUntilVisible` before tapping off-screen elements
- **Dismiss optional UI**: `tapOn` with `optional: true`
- **Wait for loading**: `extendedWaitUntil`

#### Step 3 — Execute

Run the command via `run_flow` with inline commands (no file references) to verify it works on the live device.

If it fails:
- Inspect the hierarchy again and adjust the selector
- Try alternative selectors found in Phase 3 research
- Check if an element is `enabled` or obscured by a modal

#### Step 4 — Record

Once the command succeeds, append it to the YAML file being built.

Add assertions after significant actions, matching the assertion density you observed in existing tests.

#### Step 5 — Backtrack if needed

If a path doesn't lead where you expect:
1. Go back via `run_flow`: `- back` or tap the back/close button inline
2. Try the next most likely path from your Phase 3 hypothesis
3. If your hypothesis was wrong, re-inspect and re-research as needed

#### Step 6 — Repeat

Go back to Step 1 with the device now in its new state.

### Phase 7: Finalize

1. **Review** the complete YAML for consistency with existing tests:
   - Does it follow the same patterns you observed?
   - Are assertions present after key navigation/actions?
   - Are env vars used where existing tests use them?
   - Are comments used in the same style as existing tests?

2. **Run end-to-end** via `user-maestro-run_flow_files` to confirm it passes

3. If it fails, use the Phase 6 explore loop to fix the failing step

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No device found | Run `user-maestro-list_devices` and `user-maestro-start_device` |
| `run_flow` fails with "Flow file does not exist" | You used `runFlow: file:` inside `run_flow`. Use `run_flow_files` for file-based flows, or inline the commands directly |
| Element not in hierarchy | Scroll down, or check if it's behind a modal/sheet |
| Tap does nothing | Try `retryTapIfNoChange: true` or check `enabled` state |
| Login flow fails | Verify the test account exists and credentials are correct |
| Flaky on re-run | Add `waitForAnimationToEnd` or `extendedWaitUntil` before assertions |
| Target might be behind a feature flag | Ask the user about account requirements |
| Target only appears on certain account types | Try different test users |
| Screen loads but is empty | Add `- waitForAnimationToEnd` before inspecting |
| Back button doesn't work | Try `user-maestro-back` (Android) or tap the back chevron by ID |
