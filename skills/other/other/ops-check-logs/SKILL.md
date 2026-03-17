---
name: ops-check-logs
description: Check application logs from local processes, browser console, React Native device logs, or remote AWS CloudWatch. Supports log tailing, filtering, and error searching across all platforms.
allowed-tools:
  - Bash
  - Read
---

# Ops: Check Logs

View and search logs across all platforms and environments.

**Argument**: `$ARGUMENTS` — target and optional filter (e.g., `dev errors`, `staging api`, `local`, `browser`, `device ios`, `production {function}`)

## Path Convention

- **Frontend**: Current project directory (`.`)
- **Backend**: `${BACKEND_DIR:-../backend-v2}` — set `BACKEND_DIR` in `.claude/settings.local.json` if your backend is elsewhere

## Discovery

1. Read backend `package.json` to discover `logs:*`, `logs:watch:*`, and `aws:signin:*` scripts
2. Extract function names from `logs:{env}` scripts (typically set via `FUNCTION_NAME` env var)
3. Read `.env.{environment}` to find Sentry DSN for error correlation

## Local Process Logs

Local services run in foreground processes. Their logs are captured in the terminal where they were started.

- **Frontend**: stdout from `bun start:local` or `bun start:dev` (Metro bundler)
- **Backend**: stdout from `IS_OFFLINE=true bun run start:local` (Serverless Offline)

If services were started via the `ops-run-local` skill with `run_in_background`, check the background task output file.

## Browser Console Logs (Expo Web)

For inspecting JavaScript errors, warnings, and `console.log` output in the browser at runtime.

### Via Playwright MCP Tools (automated)

Use when you need to capture browser logs programmatically during UAT or debugging.

1. **Load Playwright tools** — use `ToolSearch` to search for `playwright browser`.

2. **Navigate to the app**:
   - `browser_navigate` to the target URL (discover from `e2e/constants.ts` or `.env.*` files)

3. **Capture console messages**:
   - `browser_console_messages` — returns all `console.log`, `console.warn`, `console.error` output

4. **Check for failed network requests**:
   - `browser_network_requests` — shows all HTTP requests including 4xx/5xx failures

5. **Run custom JS to inspect state**:
   - `browser_evaluate` with script: `JSON.stringify(performance.getEntriesByType('resource').filter(r => r.duration > 1000).map(r => ({name: r.name, duration: r.duration})))`

### Via Browser DevTools (manual)

When a developer is debugging interactively:

1. Open the app in Chrome (`http://localhost:8081`)
2. Open Chrome DevTools: `Cmd+Option+I` (macOS) or `F12`
3. **Console tab** — JS errors, warnings, and log output
4. **Network tab** — failed API requests (filter by `4xx` or `5xx`)
5. **Performance tab** — runtime performance profiling

## React Native Device Logs

For inspecting logs on iOS and Android devices/simulators when running the native app.

### React Native DevTools (primary — press `j`)

The modern debugging tool for Expo apps (React Native 0.76+):

1. Start the app: `bun start:local` or `bun start:dev`
2. Press `j` in the Metro terminal to open React Native DevTools
3. Available tabs:
   - **Console** — interactive JS console connected to the app
   - **Sources** — set breakpoints, step through code
   - **Network** — inspect fetch requests and media loads
   - **Memory** — heap snapshots and memory profiling

### Expo Developer Menu (press `m`)

Press `m` in the Metro terminal to open the Developer Menu on the connected device:
- Toggle performance monitor (RAM, JS heap, Views, FPS)
- Toggle element inspector
- Open JS debugger
- Reload app

### iOS Logs

```bash
# Via Expo CLI (logs appear in Metro terminal automatically)
# Just run the app — console.log output streams to the terminal

# Via Xcode Console (native-level logs)
# Open Xcode > Devices and Simulators (Shift+Cmd+2) > Open Console

# Via macOS Console app (simulator logs)
# Open Console.app > filter by process name
```

### Android Logs

```bash
# Via Expo CLI (logs appear in Metro terminal automatically)
# Just run the app — console.log output streams to the terminal

# Via adb logcat (native-level logs, verbose)
adb logcat *:E  # Errors only
adb logcat -s ReactNativeJS  # React Native JS logs only
adb logcat -s ReactNativeJS:V *:S  # JS logs verbose, suppress everything else

# Via Android Studio Logcat
# Open Android Studio > View > Tool Windows > Logcat
# Filter by package name or "ReactNativeJS"
```

### Production Crash Logs (Device)

For production crash investigation on native platforms:
- **iOS**: Xcode Crashes Organizer (TestFlight/App Store builds)
- **Android**: Google Play Console > Crashes section
- **Both**: Sentry captures JS-level crashes — use `ops-monitor-errors` skill

## Remote Logs (CloudWatch via Serverless Framework)

Discover available log scripts from the backend `package.json` (matching `logs:*` and `logs:watch:*`).

### Prerequisites

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run aws:signin:{env}
```

### View Recent Logs

```bash
cd "${BACKEND_DIR:-../backend-v2}"
FUNCTION_NAME={fn} bun run logs:{env}
```

### Tail Logs (follow mode)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
FUNCTION_NAME={fn} bun run logs:watch:{env}
```

## Remote Logs (AWS CLI — Advanced Filtering)

For more advanced filtering, use the AWS CLI directly. Discover the AWS profile from backend `package.json` `aws:signin:*` scripts.

### Discover Log Groups

```bash
aws logs describe-log-groups \
  --profile {aws-profile} \
  --region us-east-1 \
  --query 'logGroups[].logGroupName' \
  --output text | tr '\t' '\n'
```

### Filter for Errors (last 30 minutes)

```bash
aws logs filter-log-events \
  --profile {aws-profile} \
  --region us-east-1 \
  --log-group-name "{log-group}" \
  --start-time $(date -v-30M +%s000) \
  --filter-pattern "ERROR" \
  --query 'events[].message' \
  --output text
```

### Tail Live Logs

```bash
aws logs tail "{log-group}" \
  --profile {aws-profile} \
  --region us-east-1 \
  --follow \
  --since 10m
```

## EAS Build Logs

For frontend build issues:

```bash
# List recent builds
eas build:list --limit 5

# View specific build details
eas build:view {build-id}
```

## Output Format

Report log findings as:

| Source | Timestamp | Level | Context | Message |
|--------|-----------|-------|---------|---------|
| CloudWatch | 2024-01-15T10:30:00Z | ERROR | api | Connection timeout to RDS |
| Browser | — | ERROR | console | TypeError: Cannot read property 'name' |
| Device | — | WARN | ReactNativeJS | VirtualizedList: missing keys |

Include a summary of findings: total errors, warnings, and any patterns observed.
