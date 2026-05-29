---
name: hermes-cron-local-script-notify
description: Create lightweight Hermes cron jobs that offload work into a local pre-run script, avoid chat-context overhead, and send macOS notifications for success/failure.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Hermes, Cron, Codex, macOS, Notifications, Keepalive]
    related_skills: [codex, hermes-agent]
---

# Hermes cron jobs with local script + macOS notifications

Use this when the user wants a scheduled task that should be as lightweight and deterministic as possible, especially for local keepalive pings, one-shot Codex CLI calls, or simple background automations.

## When to use

- User wants a cron task but does **not** want the future run to carry a lot of chat/tool context
- User wants the real work done by a local shell/Python script instead of a full agent workflow
- User wants macOS desktop notifications on success/failure
- User wants to keep the Hermes cron schedule, but make execution minimal

## Key idea

Do the real work in a cron `script`, and make the cron prompt trivial.

This keeps the autonomous run lighter because:
- the script executes locally before the cron prompt
- the prompt only needs to echo the script result
- attached `skills` can be cleared (`skills=[]`) if not needed

## Recommended pattern

1. Write a local script under `~/.hermes/scripts/`
2. Put the real logic there
3. Use `cronjob(action='create' or 'update', script='...')`
4. Keep the cron prompt tiny, e.g. "只把脚本 stdout 的最后一行原样输出"
5. If minimizing overhead matters, clear skills with `skills=[]`

## Example: lightweight Codex keepalive on macOS

### Why this approach

If the goal is just "poke Codex every few hours" or "refresh a 5h window", don't load a Codex skill and don't make the cron agent reason about how to call Codex. Instead, call Codex directly from a local script.

### Important findings

- `codex exec` can run outside a git repo with `--skip-git-repo-check`
- For simple chat-like one-shots, `git init` is optional and usually unnecessary
- Add `--ephemeral` if you want a lighter one-shot that does not persist session files
- If you immediately `cronjob(action='run')` a newly created recurring job, `next_run_at` may temporarily reflect the manual run rather than the next clean scheduled slot. If the user wants a clean schedule display, avoid immediate test-runs and test the script directly instead.

### Example script

Save as `~/.hermes/scripts/codex_keepalive_notify.py`

```python
#!/usr/bin/env python3
import shutil
import subprocess
import tempfile
from pathlib import Path

PROMPT = "只回复：你好，不要输出任何其他内容。"
TITLE = "Codex Cron"
SUCCESS_MSG = "Codex keepalive 成功：你好"


def shorten(text: str, limit: int = 120) -> str:
    text = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def notify(message: str) -> bool:
    notifier = shutil.which("terminal-notifier")
    if notifier:
        res = subprocess.run([notifier, "-title", TITLE, "-message", message], capture_output=True, text=True)
        if res.returncode == 0:
            return True
    osa = shutil.which("osascript")
    if osa:
        safe_message = message.replace('\\', '\\\\').replace('"', '\\"')
        safe_title = TITLE.replace('\\', '\\\\').replace('"', '\\"')
        script = f'display notification "{safe_message}" with title "{safe_title}"'
        res = subprocess.run([osa, "-e", script], capture_output=True, text=True)
        if res.returncode == 0:
            return True
    return False


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codex-keepalive-") as tmp:
        tmp_path = Path(tmp)
        out_file = tmp_path / "last_message.txt"
        cmd = [
            "codex", "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--color", "never",
            "--cd", str(tmp_path),
            "--output-last-message", str(out_file),
            PROMPT,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        msg = out_file.read_text(encoding="utf-8", errors="replace").strip() if out_file.exists() else ""

        if res.returncode == 0 and msg == "你好":
            print("OK 你好" if notify(SUCCESS_MSG) else "OK 你好 | notify-unavailable")
            return 0

        combined = "\n".join(part for part in [msg, res.stderr, res.stdout] if part).strip()
        reason = shorten(combined or f"exit {res.returncode}")
        notify(f"Codex keepalive 失败：{reason}")
        print(f"ERR {reason}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Validate it first:

```python
terminal(command="python3 -m py_compile ~/.hermes/scripts/codex_keepalive_notify.py")
terminal(command="python3 ~/.hermes/scripts/codex_keepalive_notify.py", timeout=240)
```

### Update/create cron job

```python
cronjob(
  action="update",
  job_id="<job_id>",
  schedule="30 8,13,18,23 * * *",
  deliver="origin",
  skills=[],
  script="codex_keepalive_notify.py",
  prompt="预运行脚本已经完成工作。只把脚本 stdout 的最后一行原样输出，不要添加解释。"
)
```

## Making it actually fire automatically

Creating/updating the cron job is not sufficient by itself. Hermes cron depends on the Hermes gateway scheduler.

Recommended checks:

1. Install/start the gateway if the user expects jobs to run after closing the current Hermes chat/CLI:
   - `hermes gateway install` on macOS user sessions
   - `hermes gateway status`
   - `hermes cron status`
2. Treat `hermes cron status` as the most authoritative quick check for whether jobs will actually fire.
3. On macOS, also verify persistence with:
   - `launchctl list | grep 'ai.hermes.gateway'`
   - `hermes status --all` (look for Gateway Service loaded/not loaded)

Important macOS behavior:
- `hermes gateway install` creates a LaunchAgent at `~/Library/LaunchAgents/ai.hermes.gateway.plist`
- This is an Aqua user-session service: closing the Hermes CLI is fine, but local scripts/notifications will not run while the machine is asleep or the user is fully logged out of the GUI session
- If the gateway comes up late and misses a scheduled time by more than its grace window, Hermes may fast-forward to the next slot instead of backfilling the missed run; check `~/.hermes/logs/gateway.log`

## Verifying success

Check all three:

1. The local script works when run directly
2. The user receives the macOS notification
3. `cronjob(action='list')` shows sane values for:
   - `next_run_at`
   - `last_run_at`
   - `last_status`
   - `last_delivery_error`

## Notification icon pitfall on macOS

If you use `terminal-notifier` without extra flags, the notification icon is the `terminal-notifier` app icon, not the title text and not the app you are conceptually automating.

In Homebrew terminal-notifier 2.0.0 this can look like an orange icon with a white starburst/flower.

To change it, use one of:
- `-sender com.apple.Terminal` for Terminal icon
- `-sender <bundle-id>` for another app icon
- `-appIcon <png-or-url>` for a custom icon

Do not assume a title like `Codex Cron` will change the icon automatically.

## Timeout troubleshooting and recovering the script's last stdout line

Hermes runs cron `script`s with `subprocess.run(..., capture_output=True, timeout=_SCRIPT_TIMEOUT)`. If the script times out, the cron prompt only receives a generic error like:

```text
Script timed out after 120s: /Users/<user>/.hermes/scripts/your_script.py
```

Important consequence:
- the LLM does **not** automatically receive the script's partial stdout/stderr on timeout
- if the prompt asks to repeat the script's last stdout line, you may need to recover it manually from side effects the script left behind

### Recovery pattern

Use this when the timed-out script itself is designed to write its meaningful result to a file before exiting or hanging.

For the Codex keepalive pattern above:
1. Read the script source and identify the tempdir prefix and output file path pattern
   - here: `tempfile.TemporaryDirectory(prefix="codex-keepalive-")`
   - and `out_file = tmp_path / "last_message.txt"`
2. Search temp locations for surviving directories/files
   - on macOS commonly under `/var/folders/.../T/`
   - search for `last_message.txt` or the known prefix
3. Check file mtimes against the cron run time from `~/.hermes/logs/gateway.log` or the cron session timestamp
4. Read the recovered file and use its final line as the best-grounded answer

### Why this works

If the child command (for example `codex exec --output-last-message <file>`) already wrote its last message file before the parent Python script timed out, that file can still survive briefly in the temp directory even though Hermes only reports the generic timeout string.

### Freshness check before trusting recovered output

Do **not** assume every leftover temp artifact belongs to the current failed run.

Use this checklist:
1. Compare the artifact mtime with the current cron run time (`last_run_at`, current session timestamp, or nearby gateway/agent log timestamps)
2. Prefer temp directories created at or very near the current scheduled run
3. If the only recoverable file is clearly from an older run, treat it as stale evidence
4. In that stale-evidence case, prefer the exact script error injected into the cron prompt (for example `Script timed out after 120s: ...`) instead of reusing an old success payload

This avoids incorrectly replaying a previous run's `last_message.txt` when the current run produced no trustworthy recoverable stdout.

### Useful forensic locations

When investigating cron behavior after the fact, check:
- `~/.hermes/cron/output/<job_id>/` for archived prompt/response markdown from prior runs
- `~/.hermes/sessions/session_cron_<job_id>_*.json` for the full cron conversation history
- `~/.hermes/logs/agent.log` and `~/.hermes/logs/gateway.log` for nearby timestamps and scheduler activity

These are especially helpful for correlating whether a recovered temp artifact is from the same run.

## Pitfalls

- Avoid immediate manual `run` if the user wants a clean `next_run_at`
- `skills=[]` is important when the point is minimal overhead
- A cron prompt still exists; keep it tiny and deterministic
- Test scripts directly before wiring them into cron
- Hermes cron will not fire unless the gateway scheduler is actually alive
- On macOS, Focus mode / notification permissions can hide successful notifications even when the command returns success
- If `terminal-notifier` is used without `-sender`/`-appIcon`, the icon will be terminal-notifier's own app icon, not the conceptual app being automated; use `-sender com.apple.Terminal` if the user wants a Terminal-looking notification
- For cron-only local use with no messaging platforms enabled, idle gateway overhead is low (roughly tens of MB RSS and near-zero CPU), but it is still a user-level background process and should be explained clearly to the user
- Do not set `GATEWAY_ALLOW_ALL_USERS=true` unless the user explicitly wants open access; for cron-only local use it is unnecessary
- On script timeout, Hermes reports only the timeout error string by default; do not assume partial stdout was preserved unless you verify the scheduler implementation or recover it from files/logs
