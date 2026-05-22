---
name: hud-manual-testing
description: Manual testing workflow for Claude HUD to verify core functionality. Use when asked to "test the app", "verify the app works", "run manual tests", "test after changes", or after implementing significant features. Performs full reset, launches app, and guides through verification checklist.
---

# Claude HUD Manual Testing

Verify core functionality works after code changes. Uses the project's reset script and debugging tools.

## When to Use

- After implementing significant features
- After fixing state detection bugs
- Before commits affecting session tracking
- When user asks to "test the app" or "verify it works"

## Testing Workflow

### 1. Full Reset

Reset to clean state to test first-run experience and verify nothing depends on stale data:

```bash
./scripts/dev/reset-for-testing.sh
```

This clears:
- App UserDefaults (layout, setup state)
- `~/.capacitor/` (sessions, locks, activity)
- Hook script and registrations
- Rebuilds app and launches it

### 2. First-Run Verification

After reset, verify the onboarding flow:

1. **Setup screen appears** - App should detect missing hooks
2. **Hook installation works** - Click install, verify success
3. **Empty project list** - No projects pinned yet

### 3. Core Functionality Checklist

Test each feature manually:

| Feature | How to Test | Expected |
|---------|-------------|----------|
| **Add project** | Click +, select a project folder | Project appears in list |
| **Session detection** | Start Claude in that project | State shows Ready/Working |
| **State transitions** | Type prompt, wait for response | Working → Ready transitions |
| **Lock detection** | Check `ls ~/.capacitor/sessions/` | Lock dir exists while Claude runs |
| **Session end** | Exit Claude session | State returns to Idle |

### 4. Debug Commands

If issues occur, check these:

```bash
# Watch hook events in real-time
tail -f ~/.capacitor/hud-hook-debug.log

# View current session states
cat ~/.capacitor/sessions.json | jq .

# Check active locks
ls -la ~/.capacitor/sessions/

# Check for process
ps aux | grep -E "(claude|hud-hook)"
```

### 5. Quick Restart (No Reset)

For iterative testing without full reset:

```bash
./scripts/dev/restart-app.sh
```

This rebuilds Rust + Swift and restarts the app, keeping state intact.

## Common Issues

### State stuck on Working/Waiting

Check if lock holder is alive:
```bash
cat ~/.capacitor/sessions/*.lock/pid | xargs -I {} ps -p {}
```

If PID is dead but lock exists, the cleanup should remove it on next app launch.

### Hook events not firing

Verify hooks are registered:
```bash
cat ~/.claude/settings.json | jq '.hooks'
```

Should show entries for SessionStart, UserPromptSubmit, etc. pointing to `hud-state-tracker.sh`.

### UniFFI checksum mismatch

Regenerate bindings:
```bash
cargo build -p hud-core --release
cd core/hud-core && cargo run --bin uniffi-bindgen generate --library ../../target/release/libhud_core.dylib --language swift --out-dir ../../apps/swift/bindings/
cp ../../apps/swift/bindings/hud_core.swift ../../apps/swift/Sources/ClaudeHUD/Bridge/
rm -rf ../../apps/swift/.build
```

## Verification Summary

After testing, confirm:

- [ ] App launches without crash
- [ ] Hooks install successfully on first run
- [ ] Projects can be added/removed
- [ ] Session states reflect actual Claude activity
- [ ] States transition correctly (Idle → Ready → Working → Ready → Idle)
- [ ] No orphaned lock holders accumulate
