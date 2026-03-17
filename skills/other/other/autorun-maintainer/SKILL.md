---
name: autorun-maintainer
description: Expertise in maintaining, debugging, and deploying the autorun hook system for Claude Code and Gemini CLI. Use when the user asks to "fix hooks", "deploy autorun", "debug hook errors", "update autorun version", or when troubleshooting "invisible failures" where safety guards appear inactive, piped commands are blocked, or work appears to have "reverted" after a session.
---

# Autorun Maintainer Skill: The Definitive Guide

You are a Senior QA and Release Engineer specialized in the autorun hook ecosystem. Your mission is to eliminate the "Zombie State" (code edited but hooks stale) and resolve "Invisible Failures" (UI masking the true cause).

---

## 1. The Debugging Philosophy: "Trust No UI"

Claude Code's "hook error" is a generic mask. **Never trust the UI.** You MUST follow the **Diagnostic Hierarchy** to find the root cause:

### Step 1: Plumbing Check (`~/.autorun/hook_entry_debug.log`)
*   **Binary Selection**: Verify `get_autorun_bin()` found the correct venv.
*   **Exit Codes**: Did the CLI exit with `0` (Allow/Ask) or `2` (Blocking Workaround)?
*   **Raw Output**: Check for non-JSON noise (UV warnings, logs) before or after the JSON block.
*   **Validation**: Did `extract_json()` isolate exactly one valid block via `json.loads`?

### Step 2: Logic Check (`~/.autorun/daemon.log`)
*   **FullPayload**: Check `FullPayload`. Are expected keys present (e.g., `_pid`, `_cwd`)?
*   **Timing**: Check `DAEMON PROCESSING END`. If duration > 9000ms, it will trigger a Claude timeout.
*   **Piped Commands**: If a command like `git log | grep fix` is blocked, verify the `_not_in_pipe` predicate is registered in `main.py:_PREDICATES`.

### Step 3: Source Check (`~/.autorun/daemon_startup.log`)
*   **Stale Code**: Is the daemon loading from `.../cache/...` (STALE) or `.../plugins/autorun/src/...` (FRESH)?
*   **Identity**: Confirm the **Commit Hash** and **PID** change on every restart.

---

## 2. Platform Schema Deep Dive (Claude v2.1.41)

Claude Code performs strict JSON validation. A single extra field in a lifecycle event causes a silent failure.

### The "Hook Error" Matrix
| Symptom | Event Type | Cause | Resolution |
| :--- | :--- | :--- | :--- |
| **"Invalid Input"** | `Stop`, `SessionStart` | Sent `decision` or `reason`. | **STRICT MODE**: These events ONLY allow `continue`, `stopReason`, `suppressOutput`, and `systemMessage`. |
| **"Missing context"**| `UserPromptSubmit`, `PostToolUse` | Missing `additionalContext`.| Map feedback to `additionalContext` inside `hookSpecificOutput`. |
| **"JSON failed"** | `PreToolUse` | Missing `permissionDecision`.| Must exist at top-level AND in `hookSpecificOutput`. |
| **"Double print"** | All | `hook_entry.py` printed noise. | Refactor `hook_entry.py` to isolate and print exactly one JSON block. |

### The "Ask" vs "Deny" Strategy
*   **The Conflict**: Claude Code ignores `permissionDecision: "deny"` at exit 0.
*   **The Resolution**: 
    *   For **AI-only feedback**, use **Exit 2 + Stderr** (Bug #4669).
    *   For **User-facing redirection** (e.g., "Use trash instead of rm"), use **`decision: "ask"`**. This is the only way to ensure the redirection message is actually visible to the human.
*   **Gemini Symmetry**: Always map `ask` -> `deny` for Gemini in `core.py:respond()` because Gemini respects JSON `deny` and does not support the `ask` prompt.

---

## 3. Deployment & Synchronization Architecture

### The "9-Location Bug" (Legacy)
Historically, fixes failed because the code was copied into 9 separate locations. We now use **Symlink Architecture**:
*   **UV Tool**: `uv tool install --editable .`
*   **Gemini**: `gemini extensions link /path/to/repo`
*   **Result**: Edits in `src/` reflect immediately in those binaries.

### The "Stale Code Trap"
Source edits in `src/` are **IGNORED** by the persistent daemon until `autorun --restart-daemon` is run. **NEVER** assume code is active just because you saved the file.

### The "One-Liner of Truth" (Mandatory)
```bash
uv run --project plugins/autorun python -m autorun --install --force && \
cd plugins/autorun && uv tool install --force --editable . && cd ../.. && \
autorun --restart-daemon
```

### Critical Installer Fixes:
1.  **Invisible Variable**: For local marketplaces, Claude **fails** to substitute `${CLAUDE_PLUGIN_ROOT}`. `install.py` MUST manually substitute this in the `~/.claude/plugins/cache/` directory.
2.  **Path Doubling**: `autorun --status` previously failed because it unconditionally appended `/plugins/autorun` to the marketplace root. Discovery must be **idempotent**.

---

## 4. Stability & Performance Insights

*   **1GB Buffer Limit**: Client and server must synchronize on a high buffer limit (e.g., 1GB). Large session transcripts (500MB+) will crash the hook with `asyncio.LimitOverrunError` if left at default (64KB).
*   **Session ID Fallback**: If `CLAUDE_SESSION_ID` is missing, `core.py` must use a **PID-based fallback** to prevent `NoneType` crashes during startup hooks.
*   **Socket Polling**: `restart_daemon.py` must use `is_daemon_responding()` socket checks rather than `time.sleep()`. Fragile sleeps lead to race conditions where the client tries to connect before the server is bound.
*   **Plan Recovery**: `plan_export.py` uses a "Fresh Context" workaround (Option 1). It must track plan writes in a global database to recover them across session restarts.

---

## 5. UI/UX: Formatting & Anti-Duplication

*   **Avoid Double-Escaping**: Never call `json.dumps` on strings that will be put into a dict. This causes literal `\n` in the UI. Pass raw strings; let the final `print(json.dumps())` handle encoding.
*   **Anti-Reversion Warning**: Beware of context "compaction." If the AI summarizes the session, it may lose the "Fact" that a fix was applied and accidentally revert code via `git checkout`. **Always verify the disk state after compaction.**

---

## 6. Official & Internal References

*   **Claude Hooks Reference**: [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
*   **Claude Schema Output**: [https://code.claude.com/docs/en/hooks#json-output](https://code.claude.com/docs/en/hooks#json-output)
*   **Gemini Hooks Reference**: [https://geminicli.com/docs/hooks/reference/](https://geminicli.com/docs/hooks/reference/)
*   **Claude Bug #4669 (Exit 2)**: [https://claude.com/blog/how-to-configure-hooks](https://claude.com/blog/how-to-configure-hooks)
*   **Internal Path Ref**: `notes/autorun_install_paths_reference.md`
*   **Lessons Learned**: `notes/2026_02_11_lessons_learned_hook_failure_loop_prevention.md`

---

## 7. Mandatory Verification Checklist

Before declaring a task "Complete," you MUST:
1.  [ ] **Schema Test**: `echo '{"hook_event_name":"PreToolUse", "tool_name":"Bash", "tool_input":{"command":"rm test"}}' | autorun`
2.  [ ] **Metadata Test**: `autorun --version` (Verify commit matches current git).
3.  [ ] **Restart Test**: Confirm PID in `~/.autorun/daemon.lock` has changed.
4.  [ ] **Path Test**: Verify `~/.claude/plugins/cache/autorun/autorun/0.10.0/hooks/hooks.json` does NOT contain `${CLAUDE_PLUGIN_ROOT}`.
5.  [ ] **Pipes Test**: `cargo build 2>&1 | head -50` (Should be ALLOWED).
6. [ ] **Status Test**: `autorun --status` (Ensure paths aren't doubled).

---

## 8. Detailed Architectural Inventory (The 9 Locations)

If synchronization fails, verify these locations for stale code:
1.  **Git Source**: `plugins/autorun/src/autorun/`
2.  **Dev Venv**: `plugins/autorun/.venv/lib/python*/site-packages/autorun/`
3.  **Build Artifacts**: `plugins/autorun/build/` (DELETE THIS)
4.  **Claude Cache**: `~/.claude/plugins/cache/autorun/autorun/0.10.0/`
5.  **UV Tool**: `~/.local/share/uv/tools/autorun/` (Must be editable)
6.  **Gemini Extension**: `~/.gemini/extensions/ar/` (Must be symlink)
7.  **Gemini Venv**: `~/.gemini/extensions/ar/.venv/`
8.  **Gemini Workspace**: `~/.gemini/extensions/pdf-extractor/`
9.  **Gemini Build**: `~/.gemini/extensions/ar/build/` (DELETE THIS)

---

## 9. Loop Detection Checklist

You are in a "Failure Loop" if:
*   [ ] **Tests Pass, Hooks Fail**: Unit tests use source directly; hooks use stale binaries.
*   [ ] **"Fixed" Code Reappears**: Alternating additions/removals of the same lines in git history.
*   [ ] **Multiple Daemons**: `pgrep -f "autorun.daemon" | wc -l` > 1.
*   [ ] **User Reports Broken rm**: Safety guards appear inactive despite "Fix" commits.

---

## 10. Common Technical Pitfalls

*   **Stdin Consumption**: Never read `sys.stdin` inside `try_cli()`. Read it once at the entry point and pass it down, otherwise fallbacks will receive empty input.
*   **UV Warnings**: Using deprecated fields like `tool.uv.default-extras` in `pyproject.toml` causes warnings on `stderr`. Claude Code treats this as a hook error.
*   **PID Management**: Always use `pkill -f "autorun.daemon"` after changes. Stale processes bind the socket and prevent new code from running.
*   **Bytecode Cache**: `__pycache__` can persist stale logic. The restart script must purge these explicitly.

---

## 11. Testing Strategy (Triple-Layer)

1.  **Unit (integrations.py)**: Test predicate logic (e.g., `_not_in_pipe`).
2.  **Integration (main.py)**: Test `should_block_command()` with real predicates.
3.  **E2E (hook_entry.py)**: Test the full subprocess execution path with fake JSON payloads.

### Synthetic Verification Examples:
```bash
# SessionStart
echo '{"hook_event_name":"SessionStart"}' | autorun

# PreToolUse (rm block)
echo '{"hook_event_name":"PreToolUse", "tool_name":"Bash", "tool_input":{"command":"rm test"}}' | autorun

# Piped Command (Allow check)
echo '{"hook_event_name":"PreToolUse", "tool_name":"Bash", "tool_input":{"command":"git log | grep fix"}}' | autorun
```

---

## 12. Daemon Architecture & Lifecycle

The daemon is the high-performance "Brain" of autorun. It minimizes hook latency to **1-5ms**.

### Core Components:
1.  **Unix Domain Socket (`~/.autorun/daemon.sock`)**: High-speed communication path. Bypasses the overhead of TCP/IP.
2.  **Shared Magic State (`shelve`)**: Persistent key-value store. Allows hooks to share state (e.g., `autorun_stage`) across multiple independent subprocess invocations.
3.  **Watchdog Mechanism**: The daemon monitors parent PIDs. If the spawning CLI (Claude/Gemini) dies, the daemon self-terminates after an idle timeout (30min) to prevent resource leakage.
4.  **Tri-Layer Session Identity**:
    *   Layer 1: `CLAUDE_SESSION_ID` / `GEMINI_SESSION_ID` (Direct).
    *   Layer 2: Parent PID fallback (If env var is lost).
    *   Layer 3: Current Working Directory fallback.

### Critical Daemon Gotchas:
*   **Socket Binding**: If the `.sock` file exists but no process is running, `client.py` will fail to connect. The restart script MUST clean up stale socket files.
*   **Zombie Daemons**: Multiple daemons running from different code versions will cause non-deterministic hook behavior. One might allow `rm` while another blocks it. **Always audit with `pgrep`**.
*   **Blocking vs. Non-Blocking IO**: The daemon uses `asyncio`. Any synchronous `time.sleep()` or blocking subprocess call in a hook handler will freeze ALL hooks for ALL active sessions.

---

## 13. Full Hook Repair & Connectivity Guide

If hooks fail to connect or present errors, follow this repair guide.

### Connectivity Failure Matrix

| Symptom | Probable Cause | Diagnostic Command | Repair Action |
| :--- | :--- | :--- | :--- |
| **"Connection Refused"** | Daemon not running or socket stale. | `ls -l ~/.autorun/daemon.*` | Run `autorun --restart-daemon`. |
| **"No such file" (Hook CLI)**| `${CLAUDE_PLUGIN_ROOT}` missing. | `cat hooks/hook_entry_debug.log` | Run `autorun --install --force`. |
| **"ImportError"** | Python deps missing in venv. | `uv pip list --project plugins/autorun` | Run `uv sync --project plugins/autorun`. |
| **"Hang" (Claude wait)** | Daemon frozen or buffer full. | `ps aux | grep autorun.daemon` | `pkill -f daemon` + `autorun --restart-daemon`. |
| **"Hook Error" (UI)** | Stderr noise or bad JSON. | `tail -n 20 ~/.autorun/hook_entry_debug.log`| Check for double-printing or UV warnings. |

### The "Silent Fail-Open" Trap
Claude Code fails **OPEN**. If a hook script crashes, the tool (e.g., `rm`) will execute **without** warning.
*   **Verification**: If `rm` doesn't block, check `hook_entry_debug.log`. If it's empty, the script didn't even start (path issue).

### Connectivity Specs:
*   **Protocol**: JSON-over-STDIN (In), JSON-over-STDOUT (Out).
*   **Socket Type**: `AF_UNIX` (Unix Domain Socket).
*   **Default Timeout**: 10 seconds (Claude), 5 seconds (Gemini).
*   **Buffer Limit**: 1GB (Synchronized in `client.py` and `core.py`).

### Reference Guide for Repairs:
*   **Official Hook Specs**: [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
*   **Claude JSON Output Ref**: [https://code.claude.com/docs/en/hooks#json-output](https://code.claude.com/docs/en/hooks#json-output)
*   **Gemini Hook Reference**: [https://geminicli.com/docs/hooks/reference/](https://geminicli.com/docs/hooks/reference/)
*   **Asyncio Stream Ref**: [https://docs.python.org/3/library/asyncio-stream.html](https://docs.python.org/3/library/asyncio-stream.html)

---

## 14. Deep Dive: Solving the "Hook Error" Loop

The "Hook Error" was the most persistent failure mode. It manifests as a generic UI message but represents three distinct layers of failure.

### Layer 1: The Schema Violation ("Invalid Input")
Claude Code's JSON validator is **event-specific**. A field valid for one event will crash another.

*   **Symptom**: `Stop: hook error: JSON validation failed: - : Invalid input`
*   **The Trap**: Sending `decision` or `reason` in a lifecycle event.
*   **The Schema Source of Truth**:
    *   **PreToolUse**: MUST have `permissionDecision` at root AND in `hookSpecificOutput`. Top-level `decision` must be `"approve"` or `"block"`.
    *   **UserPromptSubmit / PostToolUse**: MUST have `additionalContext` in `hookSpecificOutput`.
    *   **Stop / SessionStart**: MUST NOT have `decision`, `reason`, or `hookSpecificOutput`.
*   **Solution**: The `validate_hook_response()` method in `core.py` acts as a strict whitelist filter per event type.

### Layer 2: The Plumbing Noise ("Double-Printing")
Any non-JSON output on `stdout` causes a parsing error.

*   **Symptom**: `Hook JSON output validation failed: Unexpected token '{' at position 120`
*   **The Trap**:
    1.  **Double JSON**: `client.py` prints JSON, then `hook_entry.py` prints it again.
    2.  **UV Noise**: `uv run` printing "warning: tool.uv.default-extras is deprecated".
    3.  **Logs**: Stray `print("Debug: ...")` in the source code.
*   **Solution**: 
    1.  Refactor `hook_entry.py` to use `extract_json()` which finds exactly one `{...}` block using `json.loads` validation.
    2.  Use `logger.info` (file-only) instead of `print` for all internal status messages.

### Layer 3: The Execution Gap ("No such file")
The hook script is registered but cannot be found or executed.

*   **Symptom**: `Stop hook error: can't open file '${CLAUDE_PLUGIN_ROOT}/hooks/hook_entry.py': [Errno 2] No such file or directory`
*   **The Trap**:
    1.  **Missing Substitution**: Claude fails to replace `${CLAUDE_PLUGIN_ROOT}` for local marketplaces.
    2.  **Partial Install**: `hooks/` directory skipped during `shutil.copytree` due to path logic.
*   **Solution**:
    1.  `install.py` must manually `sed`-replace the variables in `~/.claude/plugins/cache/`.
    2.  Verify existence with: `ls -l ~/.claude/plugins/cache/autorun/autorun/0.10.0/hooks/hook_entry.py`.

### Layer 4: The Silent Ignore (Bug #4669)
The hook "succeeds" (exit 0) but the safety guard is ignored.

*   **Symptom**: `rm` command prompts for "remove file?" instead of being blocked.
*   **The Trap**: Claude Code ignores `permissionDecision: "deny"` if the process exits with code 0.
*   **Solution**: **The Exit 2 Workaround**. You MUST print the reason to `stderr` and `sys.exit(2)` to trigger an actual block that the AI sees.

---

## 15. Stream Protocol & Stderr/Stdout Sensitivity

Claude Code interprets `stdout` and `stderr` differently based on the exit code. Mismanaging these streams is the primary cause of "Hook Errors."

### The `stderr` Sensitivity Rules
| Exit Code | `stderr` Content | Claude Code Result |
| :--- | :--- | :--- |
| **0** (Success) | **Any characters** | **FAILURE**: Treated as "hook error". JSON is ignored. |
| **0** (Success) | **Empty** | **SUCCESS**: JSON is parsed and processed. |
| **2** (Block) | **Reason string** | **SUCCESS**: Tool blocked. Reason is fed to AI as feedback. |
| **2** (Block) | **Empty** | **SUCCESS**: Tool blocked. AI gets generic "Tool failed" message. |

**Meta-Rule**: NEVER use `print()` for logging in hook paths. Use a file-only logger (e.g., `logging_utils.py`) to keep `stdout`/`stderr` pristine.

### The "Exactly One JSON" Rule (`stdout`)
Claude's parser is fragile. If `stdout` contains anything other than a single valid JSON block, it fails.
*   **The Problem**: `uv run` warnings, daemon status logs, or multiple `print(json.dumps())` calls.
*   **The Fix**: `hook_entry.py` must use a robust extractor:
    1.  Capture all `stdout`.
    2.  Use a sliding window or regex to find the **last** `{...}` block.
    3.  Validate with `json.loads()`.
    4.  Print **only** that block and exit.

### UI Clutter: The Triple-Print & Double-Escape
*   **Triple-Print**: Claude displays three fields simultaneously: `systemMessage`, `hookSpecificOutput.permissionDecisionReason`, and `stderr` (at exit 2).
    *   *Solution*: For `deny` decisions, **empty** the top-level fields in `core.py:respond()` to show only one clean message.
*   **Double-Escape**: Occurs when you manually escape a string (e.g., replacing `\n` with `\\n`) and then pass it to `json.dumps()`.
    *   *Result*: User sees literal `\n` text instead of newlines.
    *   *Solution*: Always pass **raw strings** through the internal logic. Let the final `json.dumps()` at the system boundary handle the encoding.

