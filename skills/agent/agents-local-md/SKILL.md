---
name: agents-local-md
description: "Generate machine-specific AGENTS.local.md with host facts and system tool details"
argument-hint: "[--force]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(uname:*)
  - Bash(hostname:*)
  - Bash(command -v:*)
  - Bash(which:*)
  - Bash(zsh --version:*)
  - Bash(tmux -V:*)
  - Bash(nvim --version:*)
  - Bash(chezmoi data:*)
  - Bash(readlink:*)
  - Bash(test -f:*)
  - Bash(test -L:*)
  - Bash(cat /etc/os-release:*)
  - Bash(stat:*)
  - Bash(date:*)
  # NOTE: Write and ln require user approval (intentional)
---

# Generate AGENTS.local.md

Probe this machine's environment and write `AGENTS.local.md` — a machine-specific context file that Claude Code auto-loads via `CLAUDE.local.md` symlink.

## Arguments

```
$ARGUMENTS
```

Options:
- `--force` — regenerate even if the file is fresh

## Instructions

### 1. Freshness Check

If `AGENTS.local.md` exists in the repo root:

```bash
stat -c %Y AGENTS.local.md 2>/dev/null || stat -f %m AGENTS.local.md 2>/dev/null
```

Read the file and extract the `Generated:` line. If ALL of these are true, report "AGENTS.local.md is current (generated DATE on HOSTNAME)" and **stop**:
- File is less than 7 days old
- Hostname in file matches current hostname
- OS in file matches current OS
- `--force` was NOT passed in arguments

Otherwise, continue to regenerate.

### 2. Probe System Identity

Gather:
```bash
uname -s        # OS kernel (Darwin/Linux)
uname -m        # Architecture (x86_64/arm64)
hostname -s     # Short hostname
cat /etc/os-release  # Linux distro details (skip on macOS)
```

Determine which system package manager is available:
- macOS: `command -v brew`
- Linux: `command -v dnf` or `command -v apt`

### 3. Probe Core System Tools

Only probe tools that **vary across systems and affect agent behavior**: **zsh, tmux, nvim**.

These are system-installed, version-significant tools where the difference between (say) zsh 5.8 vs 5.9, tmux 3.3 vs 3.5, or nvim 0.9 vs 0.11 changes what features/APIs are available. Mise-pinned tools are the same everywhere — don't list them.

For each tool, collect:
- Version: `zsh --version`, `tmux -V`, `nvim --version`
- Path: `command -v <tool>`

### 4. Chezmoi Platform Detection

```bash
chezmoi data --format json | grep -E '"os"|"arch"|"hostname"'
```

Record what chezmoi sees — this is what drives template conditionals.

### 5. Write AGENTS.local.md

Write the file to the **repo root** (`AGENTS.local.md`). Target **<30 lines**. Use this structure:

```markdown
# AGENTS.local.md

> Machine-specific context for coding agents. Auto-generated — do not edit.
> Regenerate with `/agents-local-md --force`.

Generated: YYYY-MM-DD on HOSTNAME (OS ARCH)

## System

- **OS:** Fedora 42 (Linux 6.x) / macOS 15.x (Darwin)
- **Arch:** x86_64 (amd64) / arm64
- **Hostname:** name
- **Package manager:** dnf (`/usr/bin/dnf`) / brew (`/opt/homebrew/bin/brew`)

## Core Tools

| Tool | Version | Path |
|------|---------|------|
| zsh | 5.9 | `/usr/bin/zsh` |
| tmux | 3.5a | `/usr/bin/tmux` |
| nvim | 0.11.5 | `/usr/bin/nvim` |

## Chezmoi Platform

chezmoi sees: os=`linux`, arch=`amd64`, hostname=`core`
```

**What belongs here:** facts that vary across machines and change agent behavior.

**What does NOT belong:**
- Mise-pinned tools (same everywhere)
- Third-party tools available in homebrew (latest everywhere)
- Facts already documented in the codebase (eza/dust Fedora gaps, mise wrapper alias)
- Session-ephemeral data (PID, uptime, load)
- Tool counts, shim counts, template counts

### 6. Create Symlink

```bash
ln -sf AGENTS.local.md CLAUDE.local.md
```

### 7. Verify

```bash
test -f AGENTS.local.md && echo "AGENTS.local.md exists"
test -L CLAUDE.local.md && readlink CLAUDE.local.md
git status AGENTS.local.md CLAUDE.local.md
```

Confirm:
- `AGENTS.local.md` exists with content
- `CLAUDE.local.md` symlink points to `AGENTS.local.md`
- Both are gitignored (should not appear in `git status`)

Report: "Generated AGENTS.local.md (N lines) — CLAUDE.local.md symlinked. Both gitignored."
