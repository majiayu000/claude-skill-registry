---
name: gj-tool
description: Build, run, test, and debug GrooveTech apps (Orchestrator, Pfizer, GMP, Media Server). Use gj commands - never construct xcodebuild commands manually.
allowed-tools: Bash, Read, Grep, Glob
---

# gj Tool Skill

**This skill is for GrooveTech Xcode projects. Use `gj` for all build/run/test operations.**

## Quick Reference

```bash
# Build & Run
gj run <app>              # Build + run + stream logs
gj run --device <app>     # Build + run on physical AVP device
gj run --ext <app>        # Run with extension/AVPStreamKit logs
gj run --clean <app>      # Clean build then run
gj build <app>            # Build only (no launch)
gj launch <app>           # Launch only (skip build)

# Logs & Debugging
gj logs <app> "pattern"   # Search logs (use as assertions)
gj logs <app> -f             # Follow logs in real-time (like tail -f)
gj logs <app> "error" -f     # Follow with pattern filter
gj crash <app>            # View latest crash log (.ips) - first 80 lines
gj crash <app> --full     # Show complete crash log with full backtrace
gj crash <app> --list     # List all crash logs
gj crash <app> --open     # Open crash in Console.app
gj diagnose <app>         # **USE THIS FIRST** - diagnose ANY crash/termination
gj diagnose <app> <log>   # Diagnose specific log file

# UI Automation (Simulator only; NOT ms. Tap automation reliable on iOS simulator only.)
gj ui screenshot <app>    # Capture screenshot
gj ui describe <app>      # Dump accessibility tree
gj ui tap-button <app> "label"  # Tap by accessibility label (iOS simulator only)
gj ui tap <app> x y       # Tap at coordinates (iOS simulator only)
gj ui home <app>          # Press Digital Crown (visionOS)

# Testing
gj test P0                # E2E connection tests
gj test --list            # List available tests

# Management
gj stop <app>             # Stop log streaming
gj clear <app>            # Clear logs and screenshots
gj status                 # Show simulators, devices, streams
gj devices                # List connected AVP devices

# Utilities
gj tui [app]              # Interactive log viewer (TUI)
gj sessions [path]        # CASS TUI for agent history
```

**Apps:** `orchestrator` (o), `pfizer` (p), `gmp` (g), `ms` (s), `all` (a)

---

## ⚠️ Known Limitations

### visionOS Tap Automation is Broken

`gj ui tap` and `gj ui tap-button` **do not work** on visionOS apps (Pfizer, GMP). The visionOS simulator reports incorrect accessibility frames (all elements at position 0,0).

**Working on visionOS:**
- `gj ui screenshot <app>` ✓
- `gj ui home <app>` ✓
- `gj run <app>` ✓
- `gj logs <app>` ✓

**Not working on visionOS:**
- `gj ui tap <app> x y` ✗
- `gj ui tap-button <app> "label"` ✗

**Workaround:** Manual testing in Simulator.app, or rely on log assertions.

See: `gj-tool/KNOWN_ISSUES.md` for full details.

### macOS Media Server UI Automation (Not Supported)

`gj ui ... ms` is **not supported** (UI commands are simulator-only). To trigger CloudSync, use the Media Server UI manually, then verify with `gj logs ms "CloudSync"`.

### Device Logging: OSLog Not Captured

When running on **physical devices** via `gj run --device <app>`, only `print()` statements appear in device logs. **OSLog entries are NOT captured** (they go to the unified logging system, not stdout).

**Workaround:** Add `print()` alongside OSLog for device-visible diagnostics:
```swift
log.info("Download speed: \(speed)MB/s")
print("📊 Download speed: \(speed)MB/s")  // Visible via gj logs
```

**Simulator runs** capture both OSLog and print() normally.

---

## Testing Philosophy

**Prefer quick validation over full E2E tests during iteration.**

```
Need to verify something?
├── Quick check?      → gj logs <app> "pattern"
├── Visual check?     → gj ui screenshot <app>
├── Test interaction? → gj ui tap-button + gj logs (Orchestrator only)
├── Full validation?  → gj test P0
└── Pre-commit?       → gj test all
```

### Using Logs as Assertions

```bash
# ASSERT: Connection established (output should exist)
gj logs orchestrator "tcp_connection_established"

# ASSERT: No errors (output should be empty)
gj logs orchestrator "error"
```

### Debugging Crashes & Unexpected Terminations

**ALWAYS start with `gj diagnose`** - it queries system logs and identifies the crash type even when the app log ends abruptly.

```bash
# FIRST: Run diagnose to get crash evidence from system logs
gj diagnose <app>         # Diagnoses most recent log
gj diagnose <app> <log>   # Diagnose specific log file

# What diagnose shows:
# - CRASH CONFIRMED (AMFI/corpse evidence from system logs)
# - Crash type: fatal 309 = EXC_RESOURCE, EXC_BREAKPOINT, etc.
# - Rate-limit warnings (no .ips when too many crashes)
# - Errors before crash from app log
# - Related .ips crash reports

# If diagnose shows EXC_BREAKPOINT and there's an .ips file:
gj crash <app> --full     # Full backtrace from .ips

# Search runtime logs for errors
gj logs <app> "error"
gj logs <app> "fatal"
```

**Common crash types:**
- `EXC_BREAKPOINT` → Code assertion/trap, .ips file has backtrace
- `EXC_RESOURCE (fatal 309)` → System killed for resource limits, often rate-limited (no .ips)

---

## Full Documentation

| Doc | Location | Contents |
|-----|----------|----------|
| **Comprehensive agent guide** | `gj-tool/docs/AGENT-INSTRUCTIONS.md` | Testing philosophy, accessibility labels, workflows |
| **Quick reference** | `~/.agent-config/docs/gj-tool.md` | Command reference |
| **UI automation** | `~/.agent-config/docs/ui-automation.md` | AXe integration, finding labels |
| **Known issues** | `gj-tool/KNOWN_ISSUES.md` | visionOS limitations |

**For detailed accessibility labels and testing workflows, read `docs/AGENT-INSTRUCTIONS.md` in the gj-tool repo.**

---

## If gj Not Found

```bash
cd "/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/gj-tool"
./install.sh
gj version  # Expected: 1.5.0
```
