---
name: troubleshooting
description: Troubleshooting guide for The Fold - daemon issues, session corruption, file locations, and common problems. Use when ./fold isn't working, the daemon won't start, or you need to find system files.
allowed-tools: Bash, Read, Grep, Glob
---

# Troubleshooting The Fold

## Quick Fixes

### Check daemon status
```bash
./fold --status
```

### Daemon won't start
```bash
./daemon.sh stop     # Clear stale state
./daemon.sh cleanup  # Kill orphan workers
./daemon.sh start    # Or just run ./fold - it auto-starts
```

### Session state corruption
```bash
rm -rf .fold-repl/   # Nuclear option - clears all session state
./fold "(help)"      # Auto-starts fresh daemon
```

### Tests hanging
Check fuel consumption. Infinite loops exhaust fuel and return `out-of-fuel` error.

```scheme
;; In REPL, check fuel status
(fuel)
```

## File Locations

### REPL Infrastructure

| Path | Purpose |
|------|---------|
| `.fold-repl/ready` | Daemon ready file (presence indicates daemon is running) |
| `.fold-repl/requests/<session>.ss` | Session request queue |
| `.fold-repl/responses/<session>.txt` | Session response output |
| `.fold-repl/daemon.log` | Daemon log (check for errors) |
| `.fold-repl/discord-outbox/` | Discord bot message outbox |

### Persistent State

| Path | Purpose |
|------|---------|
| `.fold-sessions/` | Persistent session state (survives daemon restart) |
| `.fold-users/` | User profile data |

### Content-Addressed Store

| Path | Purpose |
|------|---------|
| `.store/` | Content-addressed store root |
| `.store/objects/` | CAS objects (blocks) |
| `.store/heads/bbs/fold-*.head` | BBS issue heads (current hash per issue) |
| `.store/heads/bbs/post-*.head` | BBS post heads (current hash per post) |

### BBS Runtime

| Path | Purpose |
|------|---------|
| `.bbs/` | BBS runtime data |
| `.bbs/counter` | Next issue ID |
| `.bbs/deps/` | Dependency tracking |
| `.bbs/index/` | Search index cache |

### Project Files

| Path | Purpose |
|------|---------|
| `TAXONOMY.sexp` | Machine-readable project taxonomy |
| `CLAUDE.md` | Agent instructions (this file) |
| `docs/agent-operating-manual.md` | Agent procedures |

## Common Issues

### "Daemon not responding"

1. Check if daemon is running: `./fold --status`
2. Check daemon log: `cat .fold-repl/daemon.log`
3. Kill and restart: `./daemon.sh stop && ./fold --status`

### "Session not found"

Sessions are ephemeral unless named with `-s`:
```bash
./fold -s mywork "(define x 10)"  # Creates named session
./fold -s mywork "x"              # Uses same session
```

### "Module not found" during require

1. Check you're in project root: `pwd` should be `/home/oso/the-fold`
2. Verify module exists: `ls lattice/<module>/`
3. Check for typos in module name

### "Out of fuel" error

The expression exceeded its fuel budget. Options:
- Simplify the expression
- Check for infinite recursion
- Increase fuel budget (if safe)

### "Hash mismatch" or CAS errors

The CAS store may be corrupted. Options:
1. Check `.store/` permissions
2. Run integrity check: `./fold "(cas-verify)"`
3. Rebuild from git: `rm -rf .store && ./fold "(cas-rebuild)"`

### BBS shows stale data

After reloading modules, refresh BBS state:
```scheme
(bbs-init!)  ; Refresh from disk
```
