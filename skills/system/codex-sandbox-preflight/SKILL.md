---
name: codex-sandbox-preflight
description: "Use at the start of a Codex session (especially sandboxed) to run `scripts/codex-sandbox-preflight.sh` and interpret network + writable_roots constraints."
---

# Codex sandbox preflight

## When to use
- Start of a new Codex session (default).
- You see sandbox-ish errors like `PermissionError: [Errno 1] Operation not permitted`, `seccomp`, or unexpected “Permission denied” when paths look writable.
- You need to know if network is disabled in the tool sandbox before attempting auth, installs, `git push`, etc.

## Workflow
1) Run the preflight helper:
```bash
scripts/codex-sandbox-preflight.sh
```

2) If you’re in a normal shell and want to see what happens when network is enabled inside the sandbox:
```bash
scripts/codex-sandbox-preflight.sh --with-network
```

3) Summarize results (don’t paste the full output unless asked):
- Tool sandbox network: `socket()` allowed vs blocked (and DNS if allowed).
- Writable roots: whether `~/.config/wbg-auth` is writable inside the sandbox.
- Config drift: whether `~/.codex/config.toml` is symlinked to dotfiles or has diverged.

## Interpretation cheatsheet
- `INFO- socket() syscall blocked`:
  - Tool sandbox has network disabled (expected in many sandboxed sessions).
  - Avoid network-dependent commands/tools inside the sandbox.
  - To allow sandbox network, start Codex with `-c sandbox_workspace_write.network_access=true` (still sandboxed, but with egress).
- `WARN missing_writable_root=$HOME/.config/wbg-auth` (or similar) / sandbox write fails for `~/.config/wbg-auth`:
  - `wbg-auth` will crash on startup due to log file creation.
  - Fix by adding `~/.config/wbg-auth` to `sandbox_workspace_write.writable_roots` in `~/.codex/config.toml`.

## Notes / pitfalls
- Running this from inside an already-restricted tool sandbox cannot “prove” that enabling network would work; outer seccomp will still block `socket()`. Use `--with-network` from a normal shell for that.
- This helper must never print secrets; it only checks tool presence, config linkage, writability, and basic DNS.
