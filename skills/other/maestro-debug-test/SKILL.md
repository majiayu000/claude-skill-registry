---
name: maestro-debug-test
description: Run a Maestro E2E test, and if it fails, diagnose and fix it in a loop until it passes. Analyzes failure screenshots, failed steps, and device view hierarchy via Maestro MCP to determine root cause, applies fixes, and re-runs. Use when the user says "debug this test", "fix this maestro test", "why is this test failing", or wants to get a Maestro test passing.
---

# Debug Maestro Test

Run a Maestro test and, if it fails, enter a diagnose-fix-rerun loop until it passes.

The user provides a path to a `.yml` flow file. If relative, resolve from workspace root.

## Step 1: Run the test

Verify the path exists, clean previous results, and run:

```bash
ls <resolved-path>
rm -rf build/maestro-results
maestro test --test-output-dir=build/maestro-results <resolved-path>
```

If the user specifies extra flags (e.g. `--include-tags`, `--device`), append them.

- **Exit code 0** → All tests passed. Report success and stop.
- **Non-zero** → Test failed. Continue to Step 2.

## Step 2: Diagnose

#### 2a. Locate failure artifacts

```bash
ls -la build/maestro-results/$(ls -t build/maestro-results/ | head -1)/
```

Look for: `screenshot-❌-*.png`, `commands-*.json`, `ai-*.json`

#### 2b. Read the failure screenshot

Use the Read tool on `screenshot-❌-*.png` to see visual state at failure time.

#### 2c. Read the test flow

Read the `.yml` file and all sub-flows it references (`runFlow` entries). Identify the **failed step** from the test output.

#### 2d. Inspect the live device

The device is frozen at the failure point. Use **both** Maestro MCP tools:

- `user-maestro-take_screenshot` — current visual state
- `user-maestro-inspect_view_hierarchy` — all elements with text, IDs, bounds, and states

Search the hierarchy for:

- The element the test was looking for (exact text or ID match)
- Similar elements with slightly different text, IDs, or casing
- Whether the expected element exists but is off-screen or hidden

**Note:** Secure text inputs (password fields) may show placeholder text in screenshots even when they have values. The hierarchy `value` field will show masked dots (e.g. `•••••••••••`). Don't assume a password field is empty just because the screenshot shows the placeholder label.

#### 2e. Try the failed command via MCP

Use `user-maestro-run_flow` to attempt the exact failing command on the live device:

```yaml
appId: com.guideline.mobile
---
- tapOn: <the selector that failed>
```

- **Command succeeds** → The element IS accessible, but wasn't ready during the test run. This is a **timing issue**. Fix with `extendedWaitUntil` to wait for the element before acting on it.
- **Command fails** → The element genuinely doesn't exist or has changed. Proceed to 2f to determine why.

#### 2f. Compare expected vs actual

|             | Expected (from test YAML)             | Actual (from device)                                       |
| ----------- | ------------------------------------- | ---------------------------------------------------------- |
| **Screen**  | What screen should the test be on?    | What screen is actually showing?                           |
| **Element** | What text/ID is the test looking for? | Is it present? Under a different name?                     |
| **State**   | What state should the app be in?      | Is it loading, showing an error, or on a different screen? |

#### 2g. Determine root cause

| Category                   | Symptoms                                                          | How to confirm                                                          |
| -------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Accessibility tree lag** | Element visible in screenshot, MCP command works, but test failed | Hierarchy is empty/sparse despite full visual render. MCP tap succeeds. |
| **Text changed**           | Element not found, but similar text in hierarchy                  | Search for partial match                                                |
| **ID changed**             | ID not found in hierarchy                                         | Search by visible text instead                                          |
| **Wrong screen**           | Expected element doesn't exist anywhere                           | Screenshot shows unexpected screen                                      |
| **Loading/timing**         | Spinner or skeleton visible                                       | Hierarchy contains loading indicators                                   |
| **Off-screen**             | Element in hierarchy but not in screenshot                        | Bounds outside viewport                                                 |
| **Conditional flow**       | A `when` guard skipped a required step                            | Check env vars and conditional logic                                    |
| **New modal/sheet**        | Overlay blocking interaction                                      | Screenshot/hierarchy show modal                                         |
| **Behavior change**        | Data or content the test asserted is missing/different             | Element exists but content changed — **prompt the user (Step 2h)**      |

## Step 2h: Prompt the user when behavior changes are ambiguous

**CRITICAL:** Before applying any fix, evaluate whether the failure is a **test issue** or a **possible app bug**. If the diagnosis shows the app's actual behavior has changed (not just a selector rename or timing problem), you MUST stop and ask the user before modifying the test.

**Always prompt when:**

- Data that the test expected to be visible is missing entirely (e.g., a price or percentage no longer appears)
- The UI layout or content has structurally changed (e.g., fewer columns, different data in a view)
- An element that previously existed is gone and there's no obvious replacement
- The test was asserting specific business logic (e.g., "this tab shows percentages") and that behavior appears to have changed

**Fix without prompting when:**

- A selector (text or ID) was renamed but the element still exists with the same purpose
- A timing issue caused the test to miss an element that is genuinely present
- An element moved off-screen but is still in the hierarchy
- A new modal or sheet appeared that just needs dismissing

When prompting, **always use the `AskQuestion` tool** (never ask conversationally). Present the context in the question prompt and provide structured options:

1. Summarize what the test expected vs. what the app actually shows
2. Note whether this looks like an intentional UI change or a potential regression
3. Offer options such as:
   - "Update the test to match the new behavior"
   - "This is an app bug — skip this fix"
   - "I need to investigate more before deciding"

**Scope fixes precisely.** When a failure affects one specific tab/view/state, only fix that specific case. Do not blanket-apply the same fix to similar assertions in other tabs/views unless you have confirmed each one independently. For example, if "Last 7 days" no longer shows percentages, do NOT assume "Your all time" and "# of shares" also changed — check each one separately.

## Step 3: Fix and continue via MCP

After diagnosing (and prompting the user if needed per Step 2h), apply the fix to the YAML **and** continue running the remaining steps on the live device using `user-maestro-run_flow`. This avoids restarting the entire test from scratch for each fix.

### 3a. Apply the fix to the YAML

Edit the test file (or sub-flow) with the minimal change needed. Preserve headers, comments, and existing patterns.

**Choosing the right fix — always check the screenshot first:**

1. **Take a screenshot** (`user-maestro-take_screenshot`) to see the actual screen.
2. **Is the element visible on screen?**
   - **Yes, on screen** → Timing issue. Use `extendedWaitUntil` to wait for the element.
   - **Yes, but below the fold / off-screen** → Use `scrollUntilVisible` to scroll to it.
   - **No, wrong screen entirely** → Fix navigation or conditional logic.

**Never use `scrollUntilVisible` for timing.** It should only be used when the element is genuinely off-screen. For timing issues, use `extendedWaitUntil`.

Common fixes:

| Symptom                                              | Fix                                                                     |
| ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Element on screen but test couldn't find it (timing) | Add `extendedWaitUntil` with visible selector (default timeout: 5000ms) |
| MCP command works but test failed (timing)           | Add `extendedWaitUntil` before the step (default timeout: 5000ms)       |
| Element below the fold / off-screen                  | Add `scrollUntilVisible` before the tap/assert                          |
| Screen still loading (spinner visible)               | Add `extendedWaitUntil` for post-loading content                        |
| Text not found                                       | Update selector to match current accessibility text                     |
| New modal/sheet                                      | Add optional dismiss: `tapOn: text: "Got it", optional: true`           |
| Element ID renamed                                   | Update `id` to match current hierarchy                                  |
| Navigation path changed                              | Add/update tap steps for new intermediate screens                       |
| Conditional skipped needed step                      | Set env var or make step unconditional                                  |

### 3b. Run remaining steps via MCP

Instead of re-running the full test from the beginning, use `user-maestro-run_flow` to execute the **remaining commands** from the failure point forward. Build a YAML snippet containing the commands that haven't run yet (from the failed step onward, incorporating your fix).

```yaml
appId: com.guideline.mobile
---
# The fixed version of the failed step
- <fixed command>
# Remaining steps from the flow that haven't executed yet
- <next command>
- <next command>
...
```

- **All remaining steps pass** → The fix works. Proceed to Step 4 for a full re-run to confirm.
- **A later step fails** → You found the next issue without restarting. Diagnose it (go back to Step 2) using the device's current state.
- **The fixed step still fails** → The fix was wrong. Re-diagnose with the new information.

This is much faster than a full re-run because the app is already logged in and navigated to the right screen.

## Step 4: Full re-run to confirm

Once all steps pass via MCP, do a clean full re-run to make sure everything works end-to-end:

```bash
rm -rf build/maestro-results
maestro test --test-output-dir=build/maestro-results <resolved-path>
```

- **Test passed** → Report the fix summary and stop.
- **Test failed** → Go back to Step 2. The failure may be a timing issue that only appears on a cold start.
- **3+ full re-run failures on the same step** → Stop and report. It may be an app bug, not a test issue.

## Reporting

After each loop iteration, briefly report:

1. **Failed step** and root cause
2. **Fix applied** (what changed and why)
3. **Re-run result** (pass / new failure / same failure)

When the loop ends (pass or bail), give a final summary of all changes made.
