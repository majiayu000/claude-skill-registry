---
name: maestro-take-screenshots
description: Take screenshots or record videos of specific pages and components in the mobile app using Maestro. Investigates existing test flows to learn navigation paths. Use when the user wants a screenshot, screen capture, visual snapshot, or video recording of a specific page, screen, component, or feature in the app.
---

# Maestro Take Screenshots & Record Video

Capture screenshots or record videos of specific pages/components by navigating to them via Maestro on a live device.

## Prerequisites

- A device/simulator must be running with the app installed (release build)
- Get the device ID via `user-maestro-list_devices`
- If no device is running, start one with `user-maestro-start_device`

## Workflow

### Phase 1: Gather Requirements

Collect from the user (use AskQuestion when available):

1. **Target**: Which page, screen, or component to capture
2. **Capture type**: Screenshot or video (default: screenshot)
3. **Output name**: Filename for the capture (default: derive from target name)
4. **Account type** (if relevant): Single account, multiple accounts, IRA, etc.

### Phase 2: Investigate Navigation Path

Before navigating, study existing test flows to learn how to reach the target page.

#### 2a. Search for existing flows that visit the target

Use Glob and Grep to find flows related to the target page:

```
# Search flow files for references to the target
Glob: maestro/flows/**/*.yml
Grep: "<target page name>" in maestro/flows/
```

For example, if the user wants a screenshot of the Statements page, search for flows containing "Statements" or "statement".

#### 2b. Read matching flows

Read 1-2 flows that navigate to the target page. Extract the exact navigation steps:
- Which utility flows they call (login, startApp)
- Which env vars they set (USERNAME, etc.)
- Which tabs they tap (e.g., `portfolio-screen-tab`, `profile-screen-tab`)
- Which elements they tap to reach the target

#### 2c. Read utility flows if needed

If the matching flows reference utilities (e.g., `../../utils/login.yml`), read those to understand:
- What env vars are expected
- What state the app is in after they run

#### 2d. Build the navigation plan

Synthesize a step-by-step plan to get from app launch to the target page. Common navigation patterns:

| Target | Navigation |
|--------|-----------|
| Dashboard | Login → lands on dashboard by default |
| Portfolio | Login → tap `id: portfolio-screen-tab` |
| Profile | Login → tap `id: profile-screen-tab` |
| Statements | Login → tap `id: profile-screen-tab` → tap "Statements" |
| Settings | Login → tap `id: profile-screen-tab` → tap "Settings" |
| Plan Details | Login → tap `id: profile-screen-tab` → tap plan details |
| Change Portfolio | Login → tap `id: portfolio-screen-tab` → tap "Change portfolio" |
| Contributions | Login → navigate to contribution section |
| Onboarding | Special flow via dev menu URL |

These are starting points — always verify against the actual flows in the codebase.

### Phase 3: Navigate to the Target

Execute the navigation steps on the live device using `user-maestro-run_flow`.

#### 3a. Login and navigate

Build a flow YAML based on what you learned in Phase 2. Example:

```yaml
appId: com.guideline.mobile
---
- runFlow:
    file: maestro/utils/login.yml
    env:
      USERNAME: single-defcon@guideline.test
- tapOn:
    id: profile-screen-tab
- assertVisible: "Statements"
- tapOn: "Statements"
```

Run it via `user-maestro-run_flow`.

#### 3b. Verify you're on the right screen

After navigation, confirm the target is visible:
- `user-maestro-take_screenshot` — visual check
- `user-maestro-inspect_view_hierarchy` — element check

If not on the right screen, adjust navigation and retry.

### Phase 4: Capture

#### Option A: Screenshot

Use `user-maestro-run_flow` to take the screenshot:

```yaml
appId: com.guideline.mobile
---
- takeScreenshot: <output-name>
```

The screenshot saves as `<output-name>.png` in the `.maestro` directory (or the `--test-output-dir` if specified).

**Cropping to a specific component:**

```yaml
- takeScreenshot:
    path: <output-name>
    cropOn:
      id: <element-id>
    label: "Screenshot of <component>"
```

Use `user-maestro-inspect_view_hierarchy` to find the element ID to crop on.

#### Option B: Video Recording

**IMPORTANT: Do NOT use the CLI `maestro record` command.** It is extremely slow (renders frames to a cloud service or locally with heavy overhead) and frequently hangs or times out. Instead, use the MCP to start a recording, run the flow, then stop the recording. This is done by embedding `startRecording` / `stopRecording` in the flow YAML and running it via `user-maestro-run_flow`.

Use `user-maestro-run_flow` with `startRecording`/`stopRecording` in the flow:

```yaml
appId: com.guideline.mobile
---
- startRecording: <output-name>
- # ... any interactions to capture (scrolling, tapping, etc.)
- stopRecording
```

For recording a page with scroll content:

```yaml
appId: com.guideline.mobile
---
- startRecording: <output-name>
- scroll
- scroll
- stopRecording
```

The video saves as `<output-name>.mp4`.

**With optional flag** (won't fail the flow if recording isn't supported):

```yaml
- startRecording:
    path: <output-name>
    optional: true
```

For recording an entire existing flow, wrap it with `startRecording`/`stopRecording` via `runFlow`:

```yaml
appId: com.guideline.mobile
---
- startRecording: <output-name>
- runFlow:
    file: <path-to-existing-flow.yml>
- stopRecording
```

### Phase 5: Deliver Results

1. Tell the user where the file was saved
2. If screenshot, use `user-maestro-take_screenshot` to show the current screen as a preview
3. For videos, note the `.mp4` file location

## Quick Reference: Maestro Capture Commands

### takeScreenshot

```yaml
# Simple
- takeScreenshot: ScreenName

# With crop
- takeScreenshot:
    path: ScreenName
    cropOn:
      id: element-id
    label: "Description"
```

Saves as `.png`. Path is relative to Maestro workspace directory.

### startRecording / stopRecording

```yaml
- startRecording: recording-name
- # ... actions ...
- stopRecording
```

Saves as `.mp4`. Must call `stopRecording` to finalize the file.

## Examples

**"Take a screenshot of the statements page"**
1. Search flows for "statement" → find `maestro/flows/profile/statements.yml`
2. Read it to learn: login → tap profile tab → tap Statements
3. Run navigation via MCP
4. `takeScreenshot: statements-page`

**"Record a video of changing portfolio"**
1. Search flows for "changePortfolio" → find `maestro/flows/portfolio/changePortfolioSingleDefcon.yml`
2. Read it to learn the full change portfolio flow
3. Navigate to portfolio page
4. `startRecording: change-portfolio` → run the change steps → `stopRecording`

**"Screenshot the dashboard with multiple accounts"**
1. Search flows for "MultipleAccountsDashboard" → find the flow
2. Read it to learn which env vars to use (multi-account username)
3. Login with multi-account user
4. `takeScreenshot: dashboard-multiple-accounts`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find navigation path | Search flows more broadly, check `maestro/utils/` for shared patterns |
| Login fails | Check env vars, verify test account exists in staging |
| Wrong screen after navigation | Use `inspect_view_hierarchy` to see current state, adjust taps |
| Screenshot is blank/wrong | Verify the element ID for cropOn, add `waitForAnimationToEnd` before capture |
| Video recording fails | Try with `optional: true`, or check device compatibility |
| Recording is very slow / hangs | Do NOT use `maestro record` CLI. Use `startRecording`/`stopRecording` in flow YAML via `user-maestro-run_flow` MCP instead |
| Element not found for crop | Use `inspect_view_hierarchy` to find the correct ID |
