---
name: ado-test
description: Use when testing and verifying a bug fix or feature for an ADO ticket. Triggers on /ado-test, "test ticket", or requests to test a ticket number.
model: sonnet
---

# Test ADO Ticket

Fetch ADO ticket + linked PR → understand what changed → test the fix on acc → update ticket state to "Tested".

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, fetch/update ticket patterns, and Windows/MSYS2 notes.

## Default Test Environment

| Setting | Value |
|---------|-------|
| Environment | acc (acceptance) |
| Default publication | `testsuite.acc.bbvms.com` |
| Base URL | `https://testsuite.acc.bbvms.com/{endpoint}` |
| Email | `v.vanlaar+test@bluebillywig.com` |
| Password | `iwilltestthingsLIKEABOSS` |

## Workflow

1. **Fetch ticket** with `$expand=all` (see shared) — extract description, acceptance criteria, test notes, repro steps
2. **Extract PR URL** from `Microsoft.VSTS.Common.Resolution` field or relations (same as ado-review)
3. **Read PR diff** via `gh pr diff <NUMBER> --repo <OWNER/REPO>` — understand exactly what code changed
4. **Static code verification** — confirm changes landed, verify no stale references in codebase
5. **Remote testing** — test on acc environment; use Chrome DevTools MCP for browser tests or curl for API tests
6. **Generate test report** (see format below)
7. **Update ticket state** to "Tested" if all tests pass

## Extract PR from Ticket

PR link is typically in `Microsoft.VSTS.Common.Resolution` as an `<a href="...">` tag:

```bash
node -e "const html='RESOLUTION_HTML'; const m=html.match(/href=\"(https:\/\/github\.com\/[^\"]+)\"/); console.log(m?m[1]:'NO_PR_FOUND')"
```

Also check relations for `ArtifactLink` entries with `vstfs:///Git/PullRequestId/`. If none found, ask user.

```bash
# Once you have PR number + repo:
gh pr diff <NUMBER> --repo <OWNER/REPO>
gh pr view <NUMBER> --repo <OWNER/REPO> --json title,body,files
```

## Android SDK Testing (APK)

Use when the ticket involves the native Android SDK.

### APK Source

Repo: `bluebillywig/bbnativeplayersdk-demo`
Path: `app/apk/debug/app-debug.apk` (branch: `master`)

**Before testing, verify the APK commit matches the expected SDK version:**

```bash
gh api "repos/bluebillywig/bbnativeplayersdk-demo/commits?path=app/apk/debug/app-debug.apk&per_page=1" \
  --jq '.[0] | {sha: .sha[:7], message: .commit.message, date: .commit.author.date}'
```

The commit message should reference the SDK version from the ticket (e.g. `upped bbnativeplayersdk to 8.43-0-SNAPSHOT, apk`). If the version doesn't match the ticket, **do not proceed** — ask the user to push the correct APK first.



### Download APK (with version cache)

`/tmp/` resolves to `C:\tmp\` in MSYS2 — always use `$LOCALAPPDATA/Temp`.

Check cached APK first; only re-download if the GitHub commit SHA has changed:

```bash
APK_PATH="$LOCALAPPDATA/Temp/app-debug.apk"
SHA_PATH="$LOCALAPPDATA/Temp/app-debug.apk.sha"

# Get latest commit SHA for the APK file
LATEST_SHA=$(gh api "repos/bluebillywig/bbnativeplayersdk-demo/commits?path=app/apk/debug/app-debug.apk&per_page=1" \
  --jq '.[0].sha')
LATEST_MSG=$(gh api "repos/bluebillywig/bbnativeplayersdk-demo/commits?path=app/apk/debug/app-debug.apk&per_page=1" \
  --jq '.[0].commit.message')
echo "Latest: $LATEST_MSG ($LATEST_SHA)"

CACHED_SHA=$(cat "$SHA_PATH" 2>/dev/null || echo "none")
if [ "$LATEST_SHA" = "$CACHED_SHA" ] && [ -f "$APK_PATH" ]; then
  echo "APK up to date, using cached version"
else
  echo "New version detected — downloading..."
  # Remove old APK before downloading new one
  rm -f "$APK_PATH"
  curl -sL -o "$APK_PATH" \
    "https://github.com/bluebillywig/bbnativeplayersdk-demo/raw/master/app/apk/debug/app-debug.apk"
  echo "$LATEST_SHA" > "$SHA_PATH"
  echo "Downloaded: $(ls -lh "$APK_PATH" | awk '{print $5}')"
fi
```

### Setup Emulator

`emulator` is not on PATH. Use full path. `ANDROID_SDK_ROOT` must be set. Use PowerShell to detach the process (bash `&` doesn't work for Windows GUI apps):

```bash
# List AVDs
/c/Users/vince/AppData/Local/Android/Sdk/emulator/emulator.exe -list-avds

# Start (PowerShell detaches properly; bash & does not)
powershell.exe -Command "Start-Process -FilePath 'C:\Users\vince\AppData\Local\Android\Sdk\emulator\emulator.exe' -ArgumentList '-avd','<AVD_NAME>','-no-snapshot-load' -WindowStyle Normal"

# Poll for boot (takes ~45s)
for i in $(seq 1 30); do
  BOOT=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r\n')
  if [ "$BOOT" = "1" ]; then echo "BOOTED"; break; fi
  echo "[$i] waiting..."; sleep 5
done
```

**Available AVDs:** `Medium_Phone_API_35` (system image missing — don't use), `Pixel_8_Pro` (API 36, works ✅)

### Install & Launch

```bash
adb install -r "$LOCALAPPDATA/Temp/app-debug.apk"

# Launch (package name for bbnativeplayersdk-demo):
adb shell monkey -p com.bluebillywig.bbnativeplayersdk_demo -c android.intent.category.LAUNCHER 1
```

### Screenshot

`screencap -p` flag is deprecated on newer API levels. Use `exec-out` pipe:

```bash
adb exec-out screencap -p > "$LOCALAPPDATA/Temp/screen.png"
# Then Read: C:\Users\vince\AppData\Local\Temp\screen.png
```

### UI Interaction

Get exact tap coordinates from UI dump — **always use `MSYS_NO_PATHCONV=1`** to prevent path translation:

```bash
MSYS_NO_PATHCONV=1 adb shell uiautomator dump /data/local/tmp/ui.xml
MSYS_NO_PATHCONV=1 adb shell "cat /data/local/tmp/ui.xml" > "$LOCALAPPDATA/Temp/ui.xml"
node << 'NS'
const xml = require('fs').readFileSync(require('path').join(require('os').tmpdir(), 'ui.xml'), 'utf8');
[...xml.matchAll(/text="([^"]+)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/g)].forEach(m => {
  const cx = Math.round((+m[2] + +m[4]) / 2), cy = Math.round((+m[3] + +m[5]) / 2);
  console.log(`"${m[1]}" => tap ${cx},${cy}`);
});
NS
adb shell input tap <X> <Y>
```

For NumberPicker scroll: `adb shell input swipe <x> <from_y> <x> <to_y> 300` (swipe up = next item).

### Capture Logs

```bash
adb logcat -c  # clear buffer
MSYS_NO_PATHCONV=1 adb logcat -d -s BBNativePlayer:* BBNativePlayerView:* ProgramController:* \
  | grep -i "seek\|error\|exception" | head -40
```

### Find Package Name (if unknown)

```bash
adb shell pm list packages | grep -i <appname>
```

### Uninstall

```bash
adb uninstall <com.package.name>
```

---

## Browser Testing (Chrome DevTools MCP)

### Login to OVP

1. Open: `mcp__chrome-devtools__new_page url="https://testsuite.acc.bbvms.com"` (redirects to `/ovp/#/login`)
2. Snapshot: `mcp__chrome-devtools__take_snapshot` — get form UIDs
3. Fill form (email=uid 1_6, password=uid 1_8):
   ```
   mcp__chrome-devtools__fill_form elements=[
     {"uid": "1_6", "value": "v.vanlaar+test@bluebillywig.com"},
     {"uid": "1_8", "value": "iwilltestthingsLIKEABOSS"}
   ]
   ```
4. Click Sign in (uid 1_11): `mcp__chrome-devtools__click uid="1_11"`
5. Verify: URL changes to `/ovp/#/home`

### Authenticated API calls (after login)

Use `evaluate_script` to make session-authenticated API calls:

```javascript
mcp__chrome-devtools__evaluate_script function="async () => {
  const response = await fetch('/sapi/endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'sesstoken': 'set' },
    body: JSON.stringify({ ... })
  });
  return { status: response.status, body: await response.text() };
}"
```

Session maintained via `VMS_SESSION` cookie. `sesstoken: set` required for write operations.

## API Testing (curl / rpctoken)

For `/sapi/` endpoints without browser session, use `rpctoken`:
- **API key format**: `{id}-{secret}` (from OVP: Publication Settings > Upload credentials)
- **rpctoken**: `{id}-{totp_code}` — TOTP via HOTP algorithm, 120s window, 10-digit output

```bash
curl -H "rpctoken: {id}-{totp_code}" "https://testsuite.acc.bbvms.com/sapi/mediaclip?id=1"
```

## Update Ticket to "Tested"

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
curl -s -H "Authorization: Basic $B64" -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/<ID>?api-version=7.0" \
  -d '[{"op":"replace","path":"/fields/System.State","value":"Tested"}]'
```

## Test Report Format

```markdown
## Test Results: ADO #<ID> — <Title>

**Environment:** testsuite.acc.bbvms.com
**State:** Tested ✅ / Failed ❌

### What was tested
<brief description>

### Results

| Test | Result | Notes |
|------|--------|-------|
| <test name> | ✅/❌ | <details> |

### Static Code Verification ✅/❌
<findings — stale refs, imports, etc.>

### Conclusion
**ADO #<ID> fix verified/failed.** <1-sentence summary>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `-u ":$ADO_PAT"` for auth | Use manual base64 (see shared) |
| Testing on prod | Default to acc environment |
| Skipping ticket fetch | Always read ticket first — acceptance criteria drive the test |
| Not checking for stale code | Search codebase even for "simple" fixes |
| Setting state without testing | Verify all criteria before moving to "Tested" |
| Writing to `/tmp/` | Resolves to `C:\tmp\` — use `$LOCALAPPDATA/Temp` or `require('os').tmpdir()` |
| `adb shell uiautomator dump /sdcard/...` | MSYS2 translates path — use `MSYS_NO_PATHCONV=1 adb shell uiautomator dump /data/local/tmp/ui.xml` |
| `adb pull /sdcard/...` | MSYS2 translates `/sdcard` → `C:\...\sdcard` — use `adb shell "cat /path"` instead |
| Starting emulator with `&` in bash | Doesn't detach on Windows — use `powershell.exe -Command "Start-Process ..."` |
| `emulator` not on PATH | Full path: `/c/Users/vince/AppData/Local/Android/Sdk/emulator/emulator.exe` |
| `screencap -p /sdcard/...` | Use `adb exec-out screencap -p > "$LOCALAPPDATA/Temp/screen.png"` instead |
| Reading screenshot with Read tool | Path must be Windows: `C:\Users\vince\AppData\Local\Temp\screen.png` |
| Tapping wrong coords | Get exact coords via uiautomator dump + node; screen is 1344x2992 on Pixel_8_Pro |
| `Medium_Phone_API_35` AVD | System image not installed — use `Pixel_8_Pro` (API 36) |
