---
name: troubleshoot
description: Diagnose No Johns setup issues. Checks Python, Dolphin, ISO, arena connectivity, and common problems.
---

# Setup Troubleshooter

Diagnose and fix common No Johns setup problems. Run each check in order
and report findings at the end.

## Steps

### 1. System Check

```bash
# OS and architecture
uname -a

# Python version (must be 3.12.x, NOT 3.13)
python3.12 --version 2>/dev/null || python3 --version

# Check if venv exists
ls -la .venv/bin/python 2>/dev/null && echo "Venv OK" || echo "PROBLEM: No .venv found"

# Check venv Python version
.venv/bin/python --version 2>/dev/null
```

**Expected:** Python 3.12.x. If 3.13, pyenet won't build. If no venv, user
needs `python3.12 -m venv .venv`.

### 2. Package Check

```bash
# libmelee (critical — the Dolphin interface)
.venv/bin/python -c "import melee; print('libmelee OK')" 2>&1

# pyenet (libmelee dependency — C extension, common build failure)
.venv/bin/python -c "import enet; print('pyenet OK')" 2>&1

# nojohns CLI
.venv/bin/python -m nojohns.cli list-fighters 2>&1

# TensorFlow (only needed for Phillip)
.venv/bin/python -c "import tensorflow as tf; print(f'TF {tf.__version__} OK')" 2>&1

# slippi-ai (Phillip runtime)
.venv/bin/python -c "import slippi_ai; print('slippi-ai OK')" 2>&1
```

**Common failures:**
- `import enet` fails → pyenet build issue. See `docs/TROUBLESHOOTING.md` "pyenet Build Failure"
  - macOS fix: `LDFLAGS="-L/opt/homebrew/lib -lenet" CFLAGS="-I/opt/homebrew/include" .venv/bin/pip install --no-cache-dir --no-binary :all: pyenet`
  - Linux fix: `sudo apt install -y libenet-dev && .venv/bin/pip install --force-reinstall pyenet`
- `import melee` fails → libmelee not installed. Run `.venv/bin/pip install -e .`
- `import tensorflow` fails with `mutex lock` → TF 2.20 on macOS ARM. Fix: `.venv/bin/pip install "tensorflow==2.18.1" "tf-keras==2.18.0"`

### 3. Config Check

```bash
# Config file exists
cat ~/.nojohns/config.toml 2>/dev/null || echo "PROBLEM: No config.toml — run 'nojohns setup melee'"
```

Verify these fields in `~/.nojohns/config.toml`:

- **`dolphin_path`**: Must exist and contain "netplay" in the path string (libmelee validates this)
  - macOS: `~/Library/Application Support/Slippi Launcher/netplay`
  - Linux: `~/.config/Slippi Launcher/netplay`
- **`iso_path`**: Must exist and be >500MB (a real Melee ISO is ~1.3GB)
- **`connect_code`**: Format `XXXX#NNN` (4 letters, hash, 1-3 digits). Avoid codes with '9' on macOS Sequoia.

```bash
# Verify Dolphin path exists
DOLPHIN_PATH=$(python3 -c "
import tomllib
with open('$HOME/.nojohns/config.toml', 'rb') as f:
    c = tomllib.load(f)
print(c.get('games', {}).get('melee', {}).get('dolphin_path', 'NOT SET'))
" 2>/dev/null)
echo "Dolphin path: $DOLPHIN_PATH"
ls "$DOLPHIN_PATH" 2>/dev/null && echo "Path OK" || echo "PROBLEM: Path does not exist"

# Verify ISO exists and check size
ISO_PATH=$(python3 -c "
import tomllib
with open('$HOME/.nojohns/config.toml', 'rb') as f:
    c = tomllib.load(f)
print(c.get('games', {}).get('melee', {}).get('iso_path', 'NOT SET'))
" 2>/dev/null)
echo "ISO path: $ISO_PATH"
ls -la "$ISO_PATH" 2>/dev/null || echo "PROBLEM: ISO file not found"
```

### 4. Dolphin Check

```bash
# macOS: Check Gatekeeper isn't blocking Dolphin
# (only relevant on macOS)
if [[ "$(uname)" == "Darwin" ]]; then
    DOLPHIN_APP="$HOME/Library/Application Support/Slippi Launcher/netplay/Slippi Dolphin.app"
    if [ -d "$DOLPHIN_APP" ]; then
        echo "Dolphin app found"
        xattr -l "$DOLPHIN_APP" 2>/dev/null | grep -q quarantine && \
            echo "PROBLEM: Gatekeeper quarantine active. Fix: xattr -cr \"$DOLPHIN_APP\"" || \
            echo "Gatekeeper OK"
    else
        echo "PROBLEM: Dolphin.app not found at expected location"
        echo "Open Slippi Launcher and let it download Dolphin"
    fi
fi

# Linux: Check Dolphin binary exists
if [[ "$(uname)" == "Linux" ]]; then
    NETPLAY_DIR="$HOME/.config/Slippi Launcher/netplay"
    if [ -d "$NETPLAY_DIR" ]; then
        echo "Slippi netplay dir found"
        find "$NETPLAY_DIR" -name "dolphin-emu" -o -name "*.AppImage" 2>/dev/null
    else
        echo "PROBLEM: Slippi netplay directory not found"
    fi
fi
```

### 5. Phillip Check

```bash
# Model weights exist
MODEL="fighters/phillip/models/all_d21_imitation_v3.pkl"
if [ -f "$MODEL" ]; then
    SIZE=$(wc -c < "$MODEL")
    echo "Model weights: $SIZE bytes"
    if [ "$SIZE" -lt 1000000 ]; then
        echo "PROBLEM: Model file too small — may be corrupted"
    else
        echo "Model OK"
    fi
else
    echo "PROBLEM: Model weights not found. Run: nojohns setup melee phillip"
fi

# slippi-ai installed
if [ -d "fighters/phillip/slippi-ai" ]; then
    echo "slippi-ai repo OK"
else
    echo "PROBLEM: slippi-ai not cloned. Run: nojohns setup melee phillip"
fi
```

### 6. Network Check

```bash
# Arena reachable
ARENA_URL=$(python3 -c "
import tomllib
with open('$HOME/.nojohns/config.toml', 'rb') as f:
    c = tomllib.load(f)
print(c.get('arena', {}).get('url', 'https://nojohns-arena-production.up.railway.app'))
" 2>/dev/null || echo "https://nojohns-arena-production.up.railway.app")

echo "Arena URL: $ARENA_URL"
curl -s --max-time 5 "$ARENA_URL/health" 2>/dev/null || echo "PROBLEM: Arena unreachable"
```

### 7. Known Issues Reference

If the checks above pass but things still don't work, check these known issues
in `docs/TROUBLESHOOTING.md`:

| Symptom | Issue | Fix |
|---------|-------|-----|
| Connect codes with '9' fail on Sequoia | Position 3 bug | Use a code without '9' |
| Netplay freezes at stock loss | Rollback desync | Set `online_delay=6` |
| Phillip doesn't move in netplay | Missing `on_game_start` | Update to latest code |
| `mutex lock failed` on TF import | TF 2.20 bug on ARM | Install TF 2.18.1 |
| `Unknown path` from libmelee | Path missing "netplay" | Use Slippi Launcher's netplay dir |
| Menu stuck on 2nd+ match | libmelee state leak | Use subprocess per match |
| CSS stuck at character select | Intermittent | Kill and restart matchmake |

### 8. Report

After running all checks, print a summary:

```
=== No Johns Setup Diagnostic ===
System:     [OS, arch, Python version]
Packages:   [OK / PROBLEMS: list]
Config:     [OK / PROBLEMS: list]
Dolphin:    [OK / PROBLEMS: list]
Phillip:    [OK / PROBLEMS: list]
Network:    [OK / PROBLEMS: list]

[For each PROBLEM, include the specific fix command]
```

If everything passes: "Setup looks good. Try `nojohns fight random do-nothing` for a smoke test."
