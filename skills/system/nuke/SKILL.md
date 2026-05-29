---
name: nuke
description: Kill all shella processes and reset state. Nuclear option when things are broken. Use with caution.
disable-model-invocation: true
allowed-tools: Bash(lsof:*), Bash(kill:*), Bash(rm:*), Bash(pkill:*)
---

# Nuke Shella State

Kill all shella processes and optionally clear state. This is destructive - only run when explicitly requested.

## Steps

1. **Confirm with user** before proceeding. This will:
   - Kill all processes on ports 47100-47200
   - Optionally delete registry.json (layout and instance state)

2. **Kill processes on shella ports**:
   ```bash
   lsof -i :47100-47200 -P -n -t 2>/dev/null | xargs -r kill -9
   ```

3. **Kill any remaining shella-related node processes** (if needed):
   ```bash
   pkill -f "shella" 2>/dev/null || true
   ```

4. **Optionally clear state** (ask user first):
   ```bash
   rm -f ~/.local/state/shella/registry.json
   rm -f ~/.local/state/shella/dev.log
   ```

5. **Verify clean**:
   ```bash
   lsof -i :47100-47200 -P -n 2>/dev/null | grep LISTEN
   ```
   Should return nothing.

## After Nuking

Tell the user to restart with:
```bash
npm run dt dev daemon
```

Or for full stack:
```bash
npm run dt dev all
```
