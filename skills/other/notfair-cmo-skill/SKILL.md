---
name: cmo
argument-hint: "<or just run '/notfair:cmo'>"
description: >
  Launch the local NotFair CMO portal (a browser UI for specialist marketing agents)
  on this machine and open it in the browser. Use when the user asks to "open notfair-cmo",
  "launch the CMO", "open the marketing portal", "start the local CMO", or any phrasing
  that implies they want the local web UI for NotFair's marketing agents instead of the
  Claude Code CLI flow. The portal source lives at `notfair-cmo/` in this repo and is
  published to npm as `notfair-cmo`.
allowed-tools:
  - Bash
  - Read
---

# /notfair:cmo

Open the local NotFair CMO portal in the user's browser.

The portal is a Node app (`notfair-cmo`) that runs on `http://127.0.0.1:3000` and lets the user chat with specialist marketing agents (CMO, Google Ads, SEO), schedule recurring work, and watch tool calls stream inline. Source: [`notfair-cmo/`](../notfair-cmo/). Distributed via `npx notfair-cmo@latest`.

This skill **does not implement the portal** — it only launches it. If you need to change portal behavior, edit `notfair-cmo/` and ship via its own npm release.

---

## Default port

`3000` unless the user specifies otherwise (`--port`). If 3000 is busy, the portal's CLI auto-probes the next 5 ports.

---

## Step 1: Probe — is it already running?

```bash
PORT=3000
if curl -fsS --max-time 1 -o /dev/null "http://127.0.0.1:$PORT/" 2>/dev/null; then
  echo "RUNNING"
else
  echo "NOT_RUNNING"
fi
```

- If `RUNNING` → skip to **Step 4 (open browser)**.
- If `NOT_RUNNING` → continue to Step 2.

---

## Step 2: Preflight — run `notfair-cmo doctor`

The portal ships a `doctor` command that checks Node ≥ 20, `openclaw` on PATH, OpenClaw gateway reachable, an LLM provider configured, writable data dir, and a free port. It exits non-zero with `Fix:` lines on failure.

```bash
npx -y notfair-cmo@latest doctor 2>&1
```

- Exit 0 → continue to Step 3.
- Exit non-zero → **stop**. Surface the doctor output verbatim (it contains the `Fix:` instructions). Do not attempt to launch.

If `npx` itself is missing (no Node installed), surface: *"Node 20+ is required. Install from https://nodejs.org or via `nvm install 20`, then re-run `/notfair:cmo`."*

---

## Step 3: Launch the portal (detached)

Background it so the skill returns control. The portal opens the browser itself via its `open` dependency, but we double-tap in Step 4 in case it's already running headlessly.

```bash
LOG=$(mktemp -t notfair-cmo.XXXXXX.log)
nohup npx -y notfair-cmo@latest start --no-open > "$LOG" 2>&1 &
echo "Launched notfair-cmo (PID $!), log: $LOG"
```

Wait for the port to respond (up to 30s):

```bash
for i in $(seq 1 30); do
  if curl -fsS --max-time 1 -o /dev/null "http://127.0.0.1:$PORT/" 2>/dev/null; then
    echo "READY"
    break
  fi
  sleep 1
done
```

If after 30s the port still doesn't respond, surface the last 40 lines of `$LOG` and stop.

---

## Step 4: Open the browser

```bash
URL="http://127.0.0.1:$PORT/"
if command -v open >/dev/null 2>&1; then
  open "$URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL"
elif command -v wslview >/dev/null 2>&1; then
  wslview "$URL"
else
  echo "Could not auto-open a browser. Visit: $URL"
fi
echo "NotFair CMO is open at $URL"
```

---

## Arguments

If the user passes a port (`/notfair:cmo --port 4001` or just `/notfair:cmo 4001`), substitute it for `PORT` above and pass `--port <n>` to `notfair-cmo start`.

---

## What this skill does *not* do

- It does not configure LLM providers — that's OpenClaw's `agents.defaults.model`. The doctor surfaces the right error if missing.
- It does not install OpenClaw. If `openclaw` isn't on PATH, the doctor's `Fix:` line names the install command.
- It does not create projects or run agents — the user does that from the browser UI.

If the user wants to see project source / open issues, point them at `notfair-cmo/` in this repo.
