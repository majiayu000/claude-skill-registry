# ActivityWatch connector

ActivityWatch is optional but strongly recommended. FlowHunt audit works without it (using Gmail, Calendar, Slack, and task data), but AW adds a unique signal: how much time you actually spend in each app and browser tab. Without AW, the audit relies on content patterns from your connected sources. With AW, it also knows your time distribution. It runs 100% locally, no cloud, no telemetry, open source. Data lives in `~/.local/share/activitywatch/` (Linux) / `~/Library/Application Support/activitywatch/` (macOS) / `%LOCALAPPDATA%\activitywatch\` (Windows).

## CRITICAL: the browser extension is not optional

A fresh ActivityWatch install only sees **application windows**. That means you get "Brave — 3h" but you do NOT see **which tabs, which URLs, which pages**. For FlowHunt that is a disaster: the single biggest source of automation signal in most users' data is "what websites am I clicking around on inside my browser" — Gmail, Jira, Notion, LinkedIn, internal dashboards. Without browser-level titles, 50-70% of the audit value is gone.

**You MUST install the browser extension during setup.** This is non-negotiable. Every Chromium-based browser (Chrome, Brave, Edge, Arc, Opera, Vivaldi) uses the same Chrome Web Store extension. Firefox has its own. Safari has no prebuilt path and should be swapped for another browser if the user cares about FlowHunt.

Skipping the extension is only acceptable when the user explicitly tells you "I don't use a browser for work" — which is virtually nobody. Even then, re-check before finishing setup.

## Install — per OS

### macOS

```bash
brew install --cask activitywatch
```

After install, launch the tray app:

```bash
open -a ActivityWatch
```

macOS will prompt for **Accessibility** and **Screen Recording** permissions. Both must be granted. ActivityWatch does NOT take screenshots — Screen Recording permission is what macOS requires in order to read the title bar of foreground windows. Explain this to the user so they don't panic.

Permissions are set in System Settings → Privacy & Security → Accessibility (add `aw-qt` / `ActivityWatch`) and same path → Screen Recording. After granting, the ActivityWatch app must be restarted.

### Linux

No apt/yum/dnf package exists. Download the latest tarball from https://activitywatch.net/downloads/ and run `./aw-qt` from the extracted directory. For autostart, create a systemd user unit pointing to `aw-qt`.

### Windows

`winget install ActivityWatch.ActivityWatch` if winget is available, otherwise download the `.exe` installer from https://activitywatch.net/downloads/. Launch from the Start menu. Tray icon appears in the system tray.

## Browser extension install — per browser

### Chrome / Brave / Edge / Arc / Opera / Vivaldi / any Chromium

Open this URL for the user via `open` (macOS) / `xdg-open` (Linux) / `start` (Windows):

```
https://chromewebstore.google.com/detail/activitywatch-web-watcher/nglaklhklhcoonedhgnpgddginnjdadi
```

Click "Add to Chrome" (or equivalent). Confirm the permission dialog. Done. The extension will immediately start reporting active-tab titles to the local ActivityWatch server.

### Firefox

```
https://addons.mozilla.org/en-US/firefox/addon/aw-watcher-web/
```

Same drill. Firefox 58 or newer.

### Safari

No prebuilt extension is distributed. Building it from source requires Xcode, Apple Developer signing, and `xcrun safari-web-extension-converter`. For FlowHunt purposes, tell Safari-only users: "Dla pełnego audytu przerzuć się na Brave albo Chrome na czas flowhunta, Safari nie ma gotowej wtyczki."

## Verifying the extension is working

After the user installs the extension, verify the web bucket exists:

```bash
curl -fsS http://localhost:5600/api/0/buckets/ | jq 'keys[] | select(test("aw-watcher-web"))'
```

If the output is empty, the extension is not connected yet. Common reasons:

- User clicked "Add" but did not enable the extension on all sites (check chrome://extensions, ensure "On all sites")
- Browser has not loaded any page since enabling (tell user to visit any URL)
- Ad blocker / privacy extension is blocking `localhost:5600` requests (rare but real — Brave Shields can do this; tell user to allow `localhost:5600` in Brave Shields)

Do not proceed to the next connector until the extension bucket appears.

## AFK (away-from-keyboard) detection

ActivityWatch ships an AFK watcher that marks the user as "afk" after 3 minutes of no input (default). FlowHunt's `aw-query.sh` filters events to `not-afk` only, so time spent with the laptop open while the user is in a meeting (not touching keyboard/mouse) is excluded from the audit. This is almost always correct behavior — meeting time is captured by the Calendar connector, not by window focus.

If the user complains that their meeting time is missing, explain: "Calendar connector is the right source for meeting time. ActivityWatch AFK filter is deliberate and correct."

## Verifying everything is healthy

Final health check after setup:

```bash
# Server responding
curl -fsS http://localhost:5600/api/0/info | jq -r '.hostname, .version'

# Buckets present (expect at least window + afk + web)
curl -fsS http://localhost:5600/api/0/buckets/ | jq 'keys'
```

If all three return sensible data, ActivityWatch setup is complete.
