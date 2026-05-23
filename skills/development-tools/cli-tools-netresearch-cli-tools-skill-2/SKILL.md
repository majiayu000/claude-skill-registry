---
name: cli-tools
description: "Agent Skill: CLI tool management. Use when commands fail with 'command not found', installing tools, or checking project environments. By Netresearch."
---

# CLI Tools Skill

Manage CLI tool installation, environment auditing, and updates.

## Capabilities

1. **Reactive**: Auto-install missing tools on "command not found"
2. **Proactive**: Audit project dependencies and tool versions
3. **Maintenance**: Batch update all managed tools

## Triggers

**Reactive** (auto-install):
```
bash: <tool>: command not found
```

**Proactive** (audit): "check environment", "what's missing", "update tools"

## Workflows

### Missing Tool Resolution

#### Phase 1: Diagnostic (BEFORE attempting install)

1. **Check if tool exists elsewhere:**
   ```bash
   which <tool>           # Is it installed but not in PATH?
   command -v <tool>      # Alternative check
   type -a <tool>         # Show all locations
   ```

2. **Why might it be missing?**
   - **PATH issue**: Tool installed but shell can't find it (check `~/.local/bin`, `/usr/local/bin`)
   - **Version conflict**: Multiple versions installed, wrong one active
   - **Shell state**: Installed in current session but shell hash table stale (`hash -r`)
   - **Package manager isolation**: Installed via pip/npm/cargo but not in global PATH

3. **If tool exists but not in PATH:**
   ```bash
   # Find the binary
   find /usr -name "<tool>" 2>/dev/null
   find ~/.local -name "<tool>" 2>/dev/null

   # Add to PATH temporarily
   export PATH="$PATH:/path/to/tool/directory"
   ```

#### Phase 2: Installation

1. Extract tool name from error
2. Lookup in `references/binary_to_tool_map.md` (e.g., `rg` → `ripgrep`)
3. Install: `scripts/install_tool.sh <tool> install`

#### Phase 3: Verification (AFTER install)

1. **Confirm installation succeeded:**
   ```bash
   which <tool>           # Should show path
   <tool> --version       # Should show version
   ```

2. **If "command not found" persists after install:**
   ```bash
   hash -r                # Clear shell's command hash
   source ~/.bashrc       # Reload shell configuration
   # Or start a new shell session
   ```

3. **Retry original command**

### Environment Audit

```bash
scripts/check_environment.sh audit .
```

## Scripts

| Script | Purpose |
|--------|---------|
| `install_tool.sh` | Install/update/uninstall tools |
| `auto_update.sh` | Batch update package managers |
| `check_environment.sh` | Audit environment |
| `detect_project_type.sh` | Detect project type |

## Catalog (74 tools)

Core CLI, Languages, Package Managers, DevOps, Linters, Security, Git Tools

## Troubleshooting

### PATH Issues

When a tool installs but still shows "command not found":

1. **Check where it was installed:**
   ```bash
   # Common install locations
   ls -la ~/.local/bin/<tool>
   ls -la ~/.cargo/bin/<tool>
   ls -la ~/.npm-global/bin/<tool>
   ls -la /usr/local/bin/<tool>
   ```

2. **Ensure PATH includes common directories:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
   ```

3. **Reload shell configuration:**
   ```bash
   source ~/.bashrc        # or ~/.zshrc
   hash -r                 # Clear command cache
   exec $SHELL             # Restart shell
   ```

### Installation Blocked (Permission/System Restrictions)

When system prevents normal installation, use these alternatives:

1. **Docker (no install required):**
   ```bash
   # Run tool in container
   docker run --rm -v "$PWD:/work" -w /work <tool-image> <tool> <args>

   # Create alias for convenience
   alias <tool>='docker run --rm -v "$PWD:/work" -w /work <tool-image> <tool>'
   ```

2. **Manual binary download:**
   ```bash
   # Download release binary directly
   curl -L <release-url> -o ~/.local/bin/<tool>
   chmod +x ~/.local/bin/<tool>
   ```

3. **Compile from source:**
   ```bash
   git clone <repo-url>
   cd <repo>
   make && make install PREFIX=~/.local
   ```

4. **Use package manager with user scope:**
   ```bash
   pip install --user <tool>
   npm install -g <tool> --prefix ~/.npm-global
   cargo install <tool>  # Installs to ~/.cargo/bin
   ```

## References

- `references/binary_to_tool_map.md` - Binary to catalog mapping
- `references/project_type_requirements.md` - Project type requirements

---

> **Contributing:** https://github.com/netresearch/cli-tools-skill
