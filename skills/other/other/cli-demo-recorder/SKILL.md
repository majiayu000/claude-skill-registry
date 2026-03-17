---
name: cli-demo-recorder
description: Create demo videos for CLI and TUI tools. Use when user asks to "record a demo",
  "make a demo GIF", "create a demo video", "record my CLI tool", "asciinema demo",
  "demo recording script". Covers asciinema+agg+ffmpeg pipeline, tmux recording, multi-shell,
  and dual-purpose demo+test harnesses in Python, Rust, TypeScript, and Bash.
version: 5.1.0
---

# CLI Demo Recorder

Record polished demo videos for CLI tools — either as **direct subprocess recordings** (CLI tools, no AI session) or **real TUI recordings** (interactive AI sessions via tmux).

**Use this skill when:** A demo GIF/video is needed for a CLI tool, plugin, or terminal application.
**Invoke with:** `/cli-demo-recorder` or "Help me record a demo for my CLI tool"

---

## Choose Your Pathway [Both]

Pick the pathway based on whether the tool has an interactive TUI session. Wrong choice → recording captures nothing useful.

| Tool type | Interactive TUI? | Uses AI/LLM? | Correct pathway |
|-----------|-----------------|--------------|-----------------|
| Pure CLI (aise, git, curl) | No | No | **CLI**: harness IS the recording |
| CLI + AI session (claude -p) | No TUI | Yes | **CLI**: verify output is useful |
| Plugin/hook for TUI tool | Via TUI | Yes | **TUI live**: tmux + pane |
| Plugin with hook-only acts | Via hook | No | **TUI scripted**: `run_hook()` + `--play` |
| Spawns interactive TUI | Yes | Maybe | **TUI live**: drive TUI via tmux |
| Batch/config tool | No | No | **CLI**: `capture_output=False` |

**WARNING**: Using `subprocess.run(capture_output=True)` for a CLI demo silences recording entirely — asciinema captures nothing. See CLI pathway for the correct pattern.

---

## How It Works [Both]

### Phase 1: Plan (15–30 min)
1. **Read the tool's docs first** — before writing a single act
2. **Choose 5–7 features** that are visible, immediate, and self-explanatory to newcomers
3. **Skip invisible features** (background daemons, auto-save without visible output)
4. **Choose your pathway** (see table above) — this determines the entire harness design

### Phase 2: Build the Harness (30–60 min)
- **CLI**: Python script that calls `subprocess.run(..., capture_output=False)`. asciinema records `python test_demo.py --run-acts`.
- **TUI scripted**: Python script that calls `run_hook()` directly for each act. asciinema records `python test_demo.py --play`.
- **TUI live**: Python script that creates a tmux session, sends prompts via `send-keys`, and asciinema attaches to that session.

### Phase 3: Record and Verify (10–30 min)
- **CLI**: `python tests/test_demo.py --record` → checks cast text fragments
- **TUI**: `python tests/test_demo.py --record` → parse JSONL for tool calls

### Phase 4: Convert [Both]
```bash
agg demo.cast demo.gif \
    --theme dracula \
    --font-size 14 \        # 14-16; smaller fits more content
    --renderer fontdue \    # vector-quality anti-aliased text
    --speed 0.75 \          # 0.75x — readable without pausing
    --idle-time-limit 10    # 10s — preserves full banner display

# MP4: 4-strategy fallback (best compression first)
# Strategy 1: libx265 HEVC (tune=animation — ~50% smaller than libx264 at same quality)
ffmpeg -y -i demo.gif -movflags faststart \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    -c:v libx265 -preset slow -crf 28 -tune animation \
    -pix_fmt yuv420p -tag:v hvc1 demo.mp4 2>/dev/null \
  || ffmpeg -y -i demo.gif -movflags faststart \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    -c:v libx264 -preset slow -crf 28 -tune animation \
    -pix_fmt yuv420p demo.mp4 2>/dev/null \
  || ffmpeg -y -i demo.gif -movflags faststart \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    -c:v h264_videotoolbox -q:v 65 -pix_fmt yuv420p -color_range tv demo.mp4 2>/dev/null \
  || ffmpeg -y -i demo.gif -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    -pix_fmt yuv420p demo.mp4
```

**Important**: Convert GIF → MP4 (not cast → MP4). The GIF is already processed; going cast → MP4 directly misses the speed/idle adjustments from agg. Use `tune=animation` (not `tune=fast`) — terminal recordings have flat colors and sharp edges that match animation compression.

**Total:** ~75–120 minutes for a polished, verified demo.

---

## CLI Pathway [CLI Only]

### Architecture: Harness IS the Recording

For CLI tools, the Python harness runs as the command that asciinema records. No tmux, no pane attachment.

```
asciinema rec demo.cast --command "python test_demo.py --run-acts"
                                                        ↑ harness runs here
  → harness types $ prompt, runs subprocess with capture_output=False
  → asciinema captures all stdout from the process
  → agg demo.cast demo.gif
```

```python
# ✅ CORRECT — output flows to terminal, asciinema captures it
subprocess.run("mytool subcommand", shell=True, capture_output=False, env=DEMO_ENV)

# ❌ WRONG for CLI demos — captures output into Python, asciinema sees nothing
result = subprocess.run(["mytool", "subcommand"], capture_output=True)
```

### Core Helpers [CLI Only]

```python
_TIMED = False  # True only inside --run-acts (recording mode); _DEMO_WITH_TIMING also common

def pause(seconds: float) -> None:
    """No-op in pytest; sleeps during recording. Errors 1+2: timing ≠ spacing."""
    if _TIMED:
        time.sleep(seconds)

def _type(text: str, delay: float = 0.04) -> None:
    if _TIMED:
        for ch in text:
            sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    else:
        sys.stdout.write(text); sys.stdout.flush()

def _run(cmd: str) -> None:
    """Show typed $ prompt, then run command.
    capture_output=False is CRITICAL — output must flow to terminal.
    """
    _type(f"\n\033[1;32m$\033[0m ", delay=0)
    _type(cmd + "\n", delay=0.045)
    pause(0.3)
    subprocess.run(cmd, env=DEMO_ENV, shell=True, capture_output=False, text=True)

def section(title: str) -> None:
    """Visual section divider between acts.

    3 newlines BEFORE bar = visual gap from previous act (change this for spacing).
    pause() durations = reading time (change separately for timing).
    These are INDEPENDENT knobs — do not conflate them.

    bar_len = max(68, len(title) + 6) prevents bars shorter than title.
    """
    bar_len = max(68, len(title) + 6)
    bar = "─" * bar_len
    sys.stdout.write(f"\n\n\n\033[90m{bar}\033[0m\n")
    sys.stdout.write(f"\033[1;96m  {title}\033[0m\n")
    sys.stdout.write(f"\033[90m{bar}\033[0m\n")
    sys.stdout.flush()
```

### Intro Banner [CLI Only]

For CLI tools, the banner is a Python string printed directly to stdout:

```python
def banner() -> None:
    W = 68  # compute padding on PLAIN text only — no ANSI codes inside len() math
    def row(text: str = "", style: str = "") -> str:
        content = (" " + text).ljust(W)  # W visible chars; no ANSI in length
        return f"\033[90m  ║\033[0m{style}{content}\033[0m\033[90m║\033[0m"
    # ❌ WRONG — ANSI codes inflate len(), misalign padding:
    # bad = f"\033[1m{text}\033[0m".ljust(W)
    lines = [
        f"\033[90m  ╔{'═'*W}╗\033[0m",
        row("mytool — tagline here", "\033[1;96m"),
        row(),
        row("This demo shows:", "\033[90m"),
        row("  1. Feature one", "\033[90m"),
        row("  2. Feature two", "\033[90m"),
        f"\033[90m  ╚{'═'*W}╝\033[0m",
    ]
    print("\n" + "\n".join(lines) + "\n")
```

### Privacy Isolation [CLI Only]

```python
# DEMO_DATA_DIR: committed synthetic fixtures (no real user data)
# TOOL_ISOLATION_VAR: env var that redirects the tool's data reads
# Examples: CLAUDE_CONFIG_DIR (aise), XDG_DATA_HOME, APP_DATA_DIR
DEMO_DATA_DIR = Path(__file__).parent / "tool-demo"
DEMO_ENV = {**os.environ, "TOOL_ISOLATION_VAR": str(DEMO_DATA_DIR)}
```

### Date-Shifting Fixtures [CLI Only]

Required when demo acts use `--since Nd`, `--after DATE`, or any time-relative filter.

```python
def create_dated_demo_dir() -> Path:
    """Copy DEMO_DATA_DIR to temp dir with timestamps shifted to near today.
    Without this: fixtures from months ago → 0 results for --since 3d.
    The committed fixture files are NEVER modified — only the temp copy is shifted.
    Adapt _TS_RE and shift logic to match your tool's timestamp format.
    """
    _TS_RE = re.compile(r'"timestamp":\s*"(\d{4}-\d{2}-\d{2}T[^"]+)"')
    # find max timestamp in fixtures, compute delta to (today - 1 day)
    tmp = Path(tempfile.mkdtemp(prefix="tool-demo-dated-"))
    shutil.copytree(DEMO_DATA_DIR, tmp / "data")
    for f in (tmp / "data").rglob("*.jsonl"):
        f.write_text(_TS_RE.sub(lambda m: shift_ts(m, delta), f.read_text()))
    return tmp
```

### Recording [CLI Only]

```python
def record(cast_file: Path) -> None:
    dated_dir = create_dated_demo_dir()
    record_env = {**os.environ, "TOOL_ISOLATION_VAR": str(dated_dir)}
    try:
        subprocess.run([
            asciinema, "rec", str(cast_file),
            "--command", f"{sys.executable} {__file__} --run-acts",
            "--window-size", "160x48",   # 100x35 for narrow tools
            "--capture-env", "TERM,COLORTERM,TOOL_ISOLATION_VAR",
        ], env=record_env, check=True)
    finally:
        shutil.rmtree(dated_dir, ignore_errors=True)
```

### Initial Frame Cleanup [Both]

Asciinema records shell initialization (prompt, env vars, RC files) before the harness starts. This produces a messy first frame with shell artifacts instead of a clean banner. Fix this with a post-recording trim that finds the banner marker, walks back to the preceding clear-screen escape, drops all prior events, and rebases timestamps to t=0.

```python
def trim_cast_to_banner(cast_file: Path, banner_marker: str = "mytool") -> None:
    """Trim shell init events so the banner is the first visible frame.

    Modifies cast_file in place. Preserves the JSON header line.
    """
    lines = cast_file.read_text().splitlines()
    if len(lines) < 2:
        return

    header = lines[0]   # JSON header — always line 1
    events = lines[1:]

    # Find the first event containing the banner marker text.
    banner_idx = None
    for i, line in enumerate(events):
        if banner_marker in line:
            banner_idx = i
            break

    if banner_idx is None:
        print(f"[trim] marker {banner_marker!r} not found — skipping trim")
        return

    # Walk back to the clear-screen escape just before the banner.
    clear_idx = banner_idx
    for i in range(banner_idx - 1, -1, -1):
        if "\\u001b[H\\u001b[2J" in events[i] or "\\033[H\\033[2J" in events[i]:
            clear_idx = i
            break

    kept = events[clear_idx:]
    if not kept:
        return

    # Rebase timestamps: first kept event becomes t=0.
    first_ts = json.loads(kept[0])[0]
    rebased = []
    for line in kept:
        evt = json.loads(line)
        evt[0] = round(evt[0] - first_ts, 6)
        rebased.append(json.dumps(evt))

    cast_file.write_text(header + "\n" + "\n".join(rebased) + "\n")
    trimmed = len(events) - len(kept)
    print(f"[trim] Removed {trimmed} events before banner (kept {len(kept)})")
```

Call after recording, before conversion: `trim_cast_to_banner(CAST_FILE, banner_marker="mytool_name")`.
For Rust and TypeScript implementations, see `references/rust-demos.md` and `references/typescript-demos.md`.

### Write Acts First, Then Matching Tests [CLI Only]

**Root cause of test/demo drift:** writing tests independently of demo acts.

```
✅ Correct workflow:
1. Finalize run_demo_acts() — fix the EXACT command string for each act
2. Write TestDemoFree using those SAME command strings, verbatim
3. Never add --format, --limit, or extra flags to tests that aren't in the demo

❌ Wrong workflow:
  demo act:  mytool messages search keyword --context 1
  test:      mytool messages search keyword --format plain --full-uuid
  → test passes, demo shows different output, test proves nothing about the demo
```

Rule: if a test needs a different flag to verify output, either (a) add that flag to the demo act too, or (b) verify a property that the demo's actual output satisfies.

### Verification [CLI Only]

Check that expected text appears in the cast file:

```python
def verify_recording(cast_file: Path) -> bool:
    content = cast_file.read_text()
    checks = [
        ("Sessions:",      "Act 1: stats label present"),
        ("authentication", "Act 4: search result shows keyword"),
    ]
    return all(fragment in content for fragment, _ in checks)
```

### Deterministic Fixture IDs [CLI Only]

```python
# IDs follow a recognizable pattern — easy to spot in recordings
_S1 = str(uuid.UUID("cafe0001-cafe-cafe-cafe-000000000001"))
# Stable tool-call IDs across runs:
_id = hashlib.md5(f"{session_id}{timestamp}{path}".encode()).hexdigest()[:8]
```

### Closing Message [CLI Only]

```python
# Always read install command from pyproject.toml or README — never guess
sys.stdout.write(
    "\033[1;32m  ══════════════════════════════════════\033[0m\n"
    "\033[1;32m  ✓  Demo complete — {tool name and tagline}\033[0m\n"
    "\033[1;32m  ══════════════════════════════════════\033[0m\n"
    "\n"
    "  Install:  {exact command from pyproject.toml/README}\n"
    "\n"
)
```

---

## TUI Pathway [TUI Only]

### Architecture: Why tmux + Real TUI

The first working version of a demo typically shows **simulated** output — the harness calls the hook directly and prints what the hook would say. This is wrong for two reasons:

1. **It's not what users see.** Users see the full interactive TUI: tool call blocks, the AI's conversational response, the block message embedded in that response.
2. **The hook may not have fired at all.** This is unknowable without recording actual tool calls.

**Correct architecture (TUI live):**
```
Python harness
  → creates tmux session
  → asciinema attaches: asciinema rec --command "tmux attach-session -t SESSION"
  → background thread: tmux send-keys "claude --dangerously-skip-permissions" Enter
  → polls trust/safety dialog → auto-confirms with Enter
  → polls for TUI input prompt (❯) — requires 3 consecutive idles
  → tmux send-keys "{prompt}" Enter
  → waits 1.5s, then polls until 3 consecutive idles
  → next act...
  → claude exits → tmux session ends → asciinema finishes
```

**Background thread pattern (TUI live recording):**
```python
demo_t = threading.Thread(target=_demo_thread, daemon=True)
demo_t.start()
# asciinema in foreground records the tmux session
asciinema_proc = subprocess.Popen([asciinema, "rec", cast_file,
    "--command", f"tmux attach-session -t {session.session_name}", ...])
demo_t.join(timeout=600)
time.sleep(1)
asciinema_proc.terminate()
```

**Wrong for TUI tools:**
```python
# ❌ Headless subprocess — output not shown in TUI, not recorded by asciinema
result = subprocess.run(["mytool", "--do-thing"], capture_output=True)

# ❌ claude -p stays on command line, no TUI, asciinema captures nothing useful
subprocess.run(["claude", "-p", "delete this file"])
```

### TUI Scripted Pathway [TUI Only]

For tools with hook-level acts (no Claude TUI needed), use scripted mode:
- Acts call `run_hook()` subprocess directly
- No API key required, $0.00 cost
- asciinema records `python test_demo.py --play` as the command
- Output is formatted to explain features to newcomers

```python
# Scripted recording: asciinema records this process directly
asciinema_cmd = [asciinema, "rec", cast_file, "--overwrite",
    "--command", f"{sys.executable} {Path(__file__)} --play",
    "--idle-time-limit", "3"]  # shorter idle limit for scripted mode
subprocess.run(asciinema_cmd)
```

### Setting Up the Work Directory [TUI Only]

Use a short, fixed path — not `tempfile.TemporaryDirectory()`. Long paths appear in every tool call and look unprofessional.

```python
# ❌ Long noisy path in every tool call:
work_dir = Path(tempfile.mkdtemp())
# → /private/var/folders/9f/jr_p974d3j318tmvrfkjl55w0000gp/T/tmpAbcDef

# ✅ Clean, short path:
import os
work_dir = Path(f"/tmp/mytool-demo-{os.getpid()}")
work_dir.mkdir(parents=True, exist_ok=True)
```

### Mock Git Repo Setup [TUI Only]

```python
def setup_mock_project(work_dir: Path) -> None:
    # Use GIT_CONFIG_NOSYSTEM to prevent system git config bleed-in
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1"}
    run = lambda cmd: subprocess.run(cmd, cwd=work_dir, capture_output=True, env=env)

    run(["git", "init"])
    run(["git", "config", "user.email", "demo@example.dev"])
    run(["git", "config", "user.name", "Demo User"])
    run(["git", "config", "commit.gpgsign", "false"])  # required — signing may be global

    (work_dir / "main.py").write_text(
        "#!/usr/bin/env python3\n\n# FIXME: add input validation\ndef main():\n    pass\n"
    )
    (work_dir / "config.yaml").write_text("debug: false\nversion: 1.0\n")
    (work_dir / "project_data.csv").write_text("id,name\n1,important\n2,data\n")
    (work_dir / "auth.py").write_text(
        "# WIP: refactoring\ndef login(user, pwd):\n    pass  # stub\n"
    )
    run(["git", "add", "main.py", "config.yaml"])
    run(["git", "commit", "-m", "initial commit"])
    # Leave auth.py and project_data.csv uncommitted for demo acts
```

### Tmux Plumbing: Common Failures [TUI Only]

**Pane index must be queried, not hardcoded:**
```python
# ❌ Breaks when tmux base-index=1 (common configuration):
pane = "session_name:0.0"

# ✅ Query actual window and pane index after creating the session:
result = subprocess.run(
    ["tmux", "list-panes", "-t", session_name, "-F", "#{window_index}:#{pane_index}"],
    capture_output=True, text=True
)
pane = f"{session_name}:{result.stdout.strip()}"
```

**Sending special characters: use `-l` flag (literal):**
```python
# ❌ tmux interprets / as a search, { as repeat count:
subprocess.run(["tmux", "send-keys", "-t", pane, "/ar:plannew"])

# ✅ -l flag sends text literally without tmux special-char interpretation:
subprocess.run(["tmux", "send-keys", "-t", pane, "-l", text])
# Required for: /command, {text}, !, and any prompt with special chars
```

**Kill stale asciinema before re-recording:**
```python
# Without this: re-running --record with the same session name produces two
# asciinema processes writing to the same .cast file simultaneously (corrupt cast).
import signal
result = subprocess.run(["pgrep", "-f", f"asciinema.*{session_name}"],
                        capture_output=True, text=True)
for pid_str in result.stdout.strip().splitlines():
    try:
        os.kill(int(pid_str.strip()), signal.SIGTERM)
    except (ValueError, ProcessLookupError):
        pass
```

**Detecting the CLI's input prompt:**
```python
# ❌ Looks for ASCII > — misses Claude Code's Unicode ❯ prompt:
if ">" in pane_content:
    return True

# ✅ Check for Unicode prompt AND a reasonable idle state:
prompts = ["❯", ">", "$ ", "% "]
if any(p in pane_content for p in prompts):
    return True
```

**Confirming trust/safety dialogs:**
```python
# ❌ Exact string breaks if dialog wording changes between versions:
if "Yes, I trust this folder" in content:
    send_key("Enter")

# ✅ Keyword detection survives wording changes:
trust_keywords = ["trust", "safe", "quick safety check", "allow"]
if any(kw in content.lower() for kw in trust_keywords):
    send_key("Enter")
```

**Preventing false "done" detection:**
```python
# ❌ One idle check gives false positives — AI briefly shows input prompt
# between chained tool calls (tool A finishes → shows ❯ → calls tool B)
if is_at_input_prompt(pane):
    return  # premature!

# ✅ Require 3 consecutive idle checks (~1.5s total) to confirm truly done.
# Also: sleep 1.5s FIRST to let Claude begin responding.
time.sleep(1.5)
idle_count = 0
while True:
    if is_at_input_prompt(pane):
        idle_count += 1
        if idle_count >= 3:
            return
    else:
        idle_count = 0
    time.sleep(0.5)
```

**Plan approval is a different prompt state — do not use `wait_for_response()`:**

```python
# ❌ Wrong: wait_for_response() doesn't recognize plan approval UI
session.send_prompt("/mytool:plannew Add input validation to auth.py")
session.wait_for_response(timeout=300)  # may hang or return early
session.send_prompt("/mytool:planrefine")  # sent before plan was accepted!

# ✅ Right: use a separate wait that detects the plan approval prompt
session.send_prompt("/mytool:plannew Add input validation to auth.py")
session.wait_for_plan_approval(timeout=300)
pause(7.0)      # let viewers read the plan
session.approve_plan()   # dynamically finds and presses the right option
pause(3.0)
session.send_prompt("/mytool:planrefine")
```

**Choosing which plan option to press — do not hardcode the number:**

```python
# ❌ Wrong: hardcoded — breaks when menu reorders
session._send_key("2\n")  # "2" may mean "clear context" in some versions

# ✅ Right: parse actual menu; use exact word sets from autorun DemoSession
_ACCEPT_WORDS = ("yes", "proceed", "accept", "bypass")
_CLEAR_WORDS = ("clear context", "new conversation", "fresh context", "clear history")
# Regex handles ❯ cursor prefix:
m = re.match(r'[❯\s]*(\d+)\.\s+(.+)', stripped_line)
# Select line with accept word AND no clear word; fallback to "1"
```

**Shell command overlap:**
```python
# ❌ Fixed sleep may not be enough if previous command runs longer:
session.send_command("python3 banner.py")
time.sleep(1.0)
session.send_command("claude")  # overlap!

# ✅ Wait for shell prompt after each command:
session.send_command("python3 banner.py")
wait_for_shell_prompt(pane, timeout=10)
session.send_command("claude")
```

### Intro Banner [TUI Only]

Run the banner as a script inside the tmux pane — not from the Python harness (it won't appear in the asciinema recording):

```python
_BANNER_SCRIPT = r'''#!/usr/bin/env python3
import sys
CYAN, BOLD, RESET, GRAY = "\033[96m", "\033[1m", "\033[0m", "\033[90m"
W = 70  # compute padding on PLAIN text — no ANSI in len() math
def pad(text): return text + " " * (W - len(text) - 2)
lines = [
    ("", ""),
    (f"  ╔{'═'*W}╗", CYAN),
    (f"  ║  {pad('mytool — safety plugin for Claude Code + Gemini CLI')}║", CYAN),
    (f"  ╠{'═'*W}╣", CYAN),
    (f"  ║  {pad('Install once. Runs silently in the background.')}║", CYAN),
    (f"  ║  {pad('This demo shows:')}║", CYAN),
    (f"  ║    {pad('1. Dangerous commands blocked + safe redirect')}║", CYAN),
    (f"  ║    {pad('2. File policy — restrict to existing files only')}║", CYAN),
    (f"  ╚{'═'*W}╝", CYAN),
    ("", ""),
]
for text, color in lines:
    sys.stdout.write(color + text + RESET + "\n")
sys.stdout.flush()
'''

def act0_live(session, tmp_dir):
    banner_path = tmp_dir / "_demo_banner.py"
    banner_path.write_text(_BANNER_SCRIPT)
    session.run_shell_cmd(f"python3 {banner_path}; rm {banner_path}", wait=1.0)
    pause(10.0)  # Let viewers read all items — this is the only chance
    session.run_shell_cmd("mytool --status", wait=2.0)
    pause(6.0)
```

### Prompt Engineering [TUI Only]

For TUI demos where hooks must fire, prompt engineering is the core skill. The cause of a hook not firing is always the prompt or context — not the tool's behavior.

**Key techniques** (full guide in `references/prompt-engineering.md`):
- Prefix with "Using the Bash tool, run:" to force Bash over native Grep/Read/Edit
- Use unconditionally-blocked commands (`rm`, `sed`, `git clean -f`) over conditional ones
- Add "do not override any safety blocks" to prevent AI self-override
- Use keyword detection for trust dialogs, not exact string matching
- Parse plan approval menus dynamically with word sets, not hardcoded indices

---

## Shared Sections [Both]

### Act Design: Newcomers First

Every act must answer "what just happened and why does it matter?" for someone who has never seen your tool before.

**Good act structure:**
1. Viewer sees a natural-language prompt that makes sense to them
2. The tool responds visibly (block message, table output, corrected command)
3. The response is short enough to read in 7–10 seconds

**CLI acts** = `section(title)` + `_run(cmd)` + `pause(N)` pairs.
**TUI acts** = `session.send_prompt(text)` + `session.wait_for_response()` + `pause(N)` pairs.

**Features to show:** Dangerous command blocked + redirect. Policy/mode toggle. Custom rule lifecycle. Auto-saved artifact with `ls` immediately after.

**Features to skip:** Background daemon operations. Multi-window features. Requires prior tool knowledge. Config file editing.

### Pacing [Both]

```python
def pause(seconds: float) -> None:
    """Sleep if in timed mode; no-op in pytest."""
    if _TIMED:   # or _DEMO_WITH_TIMING — both are the same concept, different names
        time.sleep(seconds)

# Standard timing:
pause(2.0)   # Before every prompt — let viewers finish reading previous response
pause(7.0)   # After short response — let viewers read the block message
pause(10.0)  # After complex response — plan creation, long output
pause(10.0)  # After intro banner — all items must be readable
```

**`pause()` ≠ `section()` spacing — they are independent knobs:**
- `pause(N)` = reading time. Change when viewers can't finish reading.
- `section()` `\n\n\n` before bar = visual gap between acts. Change when acts look crammed.
- Do NOT change both when only one needs adjustment.

### Dual-Purpose File Pattern [Both]

```python
#!/usr/bin/env python3
"""
Demo harness — dual purpose:
  CLI:     python tests/test_demo.py --record    (records asciinema cast)
  TUI:     python tests/test_demo.py --record    (asciinema attaches to tmux)
  Pytest:  pytest tests/test_demo.py::TestDemoFree   # $0.00 always
           pytest tests/test_demo.py::TestDemoRealMoney  # requires opt-in
"""
import pytest, argparse

@pytest.mark.skipif(
    not os.environ.get("DEMO_ENABLE_REAL_MONEY"),
    reason="Set DEMO_ENABLE_REAL_MONEY=1 to run live Claude tests"
)
class TestDemoRealMoney: ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--record",    action="store_true", help="Record to .cast → GIF/MP4")
    parser.add_argument("--run-acts",  action="store_true", help="Run acts (CLI: recorded command)")
    parser.add_argument("--play",      action="store_true", help="Scripted acts, no AI ($0.00)")
    parser.add_argument("--gif-only",  action="store_true", help="Convert existing cast to GIF")
    parser.add_argument("--verify",    action="store_true", help="Verify last recording")
    parser.add_argument("--setup",     action="store_true", help="Regenerate test fixtures")
    parser.add_argument("--no-cleanup",action="store_true", help="Keep tmux session (debug)")
    args = parser.parse_args()
```

**`--no-cleanup`**: Keep tmux session alive after demo finishes. Critical for diagnosing why a hook didn't fire.

**Tool dependencies must be optional**: `asciinema`, `agg`, `ffmpeg` are NOT project dependencies:

```python
agg_bin = shutil.which("agg") or shutil.which("/tmp/agg")
if not agg_bin:
    print("[demo] agg not found — cast recorded but GIF skipped")
    print("[demo] Install: brew install agg  or  cargo install agg")
    return

ffmpeg_bin = shutil.which("ffmpeg")
if not ffmpeg_bin:
    print("[demo] ffmpeg not found — MP4 skipped (GIF only)")
```

**gitignore output files:**
```gitignore
*.gif
*.cast
*.mp4
*.webm
```

### Test Suite Alongside the Demo [Both]

```python
class TestDemoFree:
    """$0.00 — verify behavior without a live AI session."""

    # CLI: run exact demo commands against DEMO_ENV fixtures
    def test_stats_output(self):
        result = subprocess.run("mytool stats", env=DEMO_ENV, shell=True,
                                capture_output=True, text=True)
        assert "Sessions:" in result.stdout

    # TUI: call run_hook() directly
    def test_rm_blocked(self, tmp_path):
        rc, _, stderr = run_hook("Bash", {"command": "rm file.txt"}, root)
        assert rc == 2
        assert "trash" in stderr.lower()
```

**Acts first, then tests** — finalize each act's exact command string, then write tests that run the same command verbatim. Never write tests first and let them drift from the demo.

**Dry-run each act against fixtures BEFORE writing assertions** — verify the expected output actually appears. Don't assume fixture data will trigger behavior.

### Tool Path Discovery [Both]

```python
def find_tool_root() -> Path:
    candidates = [
        Path(__file__).parent.parent,  # tests/ → tool/
        Path.home() / ".tool" / "current",
    ]
    cache_base = Path.home() / ".cache" / "tool" / "versions"
    if cache_base.is_dir():
        for version_dir in sorted(cache_base.iterdir(), reverse=True):
            if (version_dir / "pyproject.toml").exists():
                candidates.append(version_dir)
                break
    for c in candidates:
        if (c / "pyproject.toml").exists():
            return c
    raise RuntimeError(f"Tool not found. Searched: {candidates}")
```

### Resolution Targets [Both]

| Quality | Terminal | Font | Approx Output | Use Case |
|---------|----------|------|---------------|----------|
| Full HD (1080p) | 160x48 | 18 | ~1750x1230 | GitHub README, presentations |
| 2K | 160x48 | 20 | ~1960x1380 | High-DPI displays |
| Minimum viable | 160x48 | 16 | ~1560x1098 | Acceptable for web |
| **NOT acceptable** | 80x24 | any | <1000px wide | Too small for text readability |

**Rule:** Never use 80x24 for demo recordings. Minimum 160x48 cols/rows with font-size 16+.

### GIF and Video Settings [Both]

Note: `--idle-time-limit` appears in two contexts with different values:
- `asciinema rec` flag: limits idle gaps DURING recording (scripted: 3s; TUI live: 5s)
- `agg` flag: limits idle gaps IN GIF output (both pathways: 10s — preserves banner)

| Setting | CLI | TUI scripted | TUI live |
|---------|-----|-------------|----------|
| `--window-size` (asciinema) | `160x48` | auto from terminal | `{cols}x{rows}` |
| `--idle-time-limit` (asciinema) | — | `3` | `5` |
| `--font-size` (agg) | `16-18` | `16-18` | `16-18` |
| `--speed` (agg) | `0.75` | `0.75` | `0.75` |
| `--idle-time-limit` (agg) | `10` | `10` | `10` |
| `--last-frame-duration` (agg) | `5` (hold closing frame) | — | — |
| `--renderer fontdue` | yes | yes | yes |
| `--theme dracula` | yes | yes | yes |

**MP4 codec strategies (4-strategy fallback, best first):**
1. `libx265 crf=28 tune=animation` — HEVC, ~50% smaller than libx264, needs `tag:v hvc1` for macOS. Note: HEVC not supported in Firefox; use libx264 if embedding in web pages
2. `libx264 crf=24 tune=animation` — broadest browser compat (Chrome, Firefox, Safari); CRF 24 in x264 gives similar visual quality to CRF 28 in x265
3. `h264_videotoolbox -q:v 65` — macOS hardware encoder, VBR, fast but larger files
4. `ffmpeg default` — last resort

**CRF note:** CRF 24 in libx264 and CRF 28 in libx265 produce approximately equivalent visual quality. Both are visually lossless for terminal text. Use `tune=animation` for terminal recordings (flat colors + sharp edges) — do not use `tune=fast`.

**Settings that did not work:**
- `--font-size 20` at 160x48: text too large, content gets cut off at edges
- `--speed 1.5`: too fast for viewers to read block messages
- `--idle-time-limit 5` (agg): banner and status pauses get cut short in GIF

### Common Pitfalls [Both]

See `references/common-pitfalls.md` for the full 30+ pitfall table covering CLI, TUI, and shared issues including recording failures, timing problems, prompt engineering failures, and encoding pitfalls.

---

## Concrete Examples

Working examples with act lists, design decisions, prompt evolution, and recording parameters:

- **CLI pathway**: `references/examples/aise-cli-example.md` — aise (ai_session_tools), 7 CLI acts
- **TUI pathway**: `references/examples/autorun-tui-example.md` — autorun for Claude Code, 7 TUI acts with prompt debugging history

---

## Tool Stack [Both]

| Tool | Purpose | Install | Required for |
|------|---------|---------|-------------|
| `asciinema` | Record terminal session to `.cast` | `brew install asciinema` | Both |
| `agg` | Convert `.cast` → animated GIF | `brew install agg` or `cargo install agg` | Both |
| `ffmpeg` | Convert GIF → MP4 | `brew install ffmpeg` | Both |
| `tmux` | Full TUI session isolation and control | `brew install tmux` | TUI only |

---

## References

| File | Content |
|------|---------|
| `references/hook-based-tools.md` | Forcing Bash tool calls for hook-based tool demos |
| `references/common-pitfalls.md` | 30+ catalogued pitfalls with root causes and fixes |
| `references/prompt-engineering.md` | TUI prompt strategies for reliable AI tool invocation |
| `references/rust-demos.md` | Rust demo harness patterns (AtomicBool, multi-shell, cargo bins) |
| `references/typescript-demos.md` | TypeScript/Node demo patterns (spawn, Vitest) |
| `references/tmux-integration.md` | tmux recording patterns (multi-pane, multi-shell, idle detection) |
| `references/cast-merging.md` | Merging multiple .cast files into single recordings |
| `references/alternative-tools.md` | VHS, t-rec, and other recording tools vs asciinema |
| `references/examples/aise-cli-example.md` | Working CLI demo: aise (7 acts, privacy isolation) |
| `references/examples/autorun-tui-example.md` | Working TUI demo: autorun (7 acts, prompt evolution) |

---

## Version History

**v5.1.0** — 2026-03-11
- Added Initial Frame Cleanup section: `trim_cast_to_banner()` removes shell init artifacts from .cast first frame
- Added Rust and TypeScript implementations in respective reference files
- Added initial frame cleanup pitfall to `references/common-pitfalls.md`

**v5.0.0** — 2026-03-11
- Added trigger phrases to description for reliable skill activation
- Added `version` field to frontmatter
- Added Resolution Targets table: minimum 160x48 at font-size 16+, Full HD at font-size 18
- Updated font-size recommendation from 14-16 to 16-18 for Full HD output
- Documented CRF equivalence: CRF 24 (x264) = CRF 28 (x265) visual quality
- Extracted Common Pitfalls (30+ items) to `references/common-pitfalls.md`
- Extracted Prompt Engineering section to `references/prompt-engineering.md`
- Extracted concrete examples to `references/examples/`
- Added `references/rust-demos.md` — Rust harness patterns from canal (AtomicBool, multi-shell, cargo bins)
- Added `references/typescript-demos.md` — TypeScript/Node harness patterns (spawnSync, Vitest)
- Added `references/tmux-integration.md` — multi-pane, multi-shell, idle detection, trust dialogs
- Added `references/cast-merging.md` — asciinema cat, programmatic merging, transitions
- Added `references/alternative-tools.md` — VHS (charmbracelet) and t-rec comparison
- Added References table listing all 10 reference files
- Reduced SKILL.md from 5,921 to ~3,300 words (under 5,000 hard limit)
- Converted second-person prose to imperative form
- Removed TODO markers from prose (code examples use FIXME/stub instead)

**v4.0.0** — 2026-03-05
- Added "Choose Your Pathway" section: CLI vs TUI scripted vs TUI live vs Mixed decision table
- Section labels throughout: [CLI Only], [TUI Only], [Both] — readers skip irrelevant parts
- Added complete CLI pathway (no tmux): harness IS the recorded process
- Fixed "Wrong architecture" block: retitled "Wrong for TUI tools" (not universally wrong)
- Added 10 session-error pitfalls with root causes, labeled by pathway
- Added `_run()`, `_TIMED`/`_DEMO_WITH_TIMING` (same concept, two names), `pause()`, `section()` for CLI
- Clarified: `pause()` timing ≠ `section()` newline spacing — independent knobs
- Added "Write Acts First, Then Matching Tests" rule (prevents test/demo drift)
- Added synthetic fixture data: deterministic IDs, date-shifting, `TOOL_ISOLATION_VAR`
- Added privacy isolation via `DEMO_ENV` + generic `TOOL_ISOLATION_VAR` pattern
- Added `--run-acts` / `--gif-only` / `--verify` / `--setup` / `--play` CLI flag patterns
- Added CLI verification: cast text fragments (vs TUI JSONL tool-call parsing)
- Added aise CLI example (peer to autorun TUI example); aise-specific details labeled
- Added TUI scripted pathway (hook-only, $0.00): acts call `run_hook()` directly
- Added `send-keys -l` (literal flag) to TUI plumbing — required for slash commands and braces
- Added `_kill_stale_recording_procs()` — prevents corrupt casts on re-record
- Added `GIT_CONFIG_NOSYSTEM=1` + `commit.gpgsign=false` to mock git repo setup
- Added background thread pattern for TUI live recording (acts thread + asciinema foreground)
- Updated GIF settings table: separate asciinema vs agg `--idle-time-limit` rows
- Added `libx265 tune=animation` as strategy 1 in MP4 fallback (4 strategies total)
- Noted `section()` auto-sizing improvement: replace hardcoded width with `max(68, len(title) + 6)`
- All pitfall rows labeled [CLI], [TUI], or [Both] for fast scanning

**v3.0.0** — 2026-03-01
- Complete rewrite based on 20+ commits of real failures and fixes from autorun demo
- Added architecture section: why tmux + real TUI (vs simulated/headless)
- Added work directory setup: short fixed paths vs tempfile.TemporaryDirectory
- Added tmux plumbing section: pane index, Unicode prompt, trust dialog, false-done detection, shell overlap
- Added prompt engineering failure table with exact failed prompts and fixes
- Added self-override prevention; bash exec doesn't work in TUI; dynamic UI string detection
- Added concrete example: autorun prompt evolution showing all 6 attempts for act2
- Added test suite structure, CLI flags structure, GIF settings

**v2.0.0** — 2026-03-01
- Rewrote as general-purpose (was autorun-specific)
- Added newcomers-first, pacing, verification sections

**v1.0.0** — 2026-03-01
- Initial release
