---
name: caam
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when switching AI coding CLI accounts quickly to recover from subscription rate limits or OAuth friction."
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | Daily Operations | Rotation Doctrine | Flywheel Integration | References -->

# CAAM — Coding Agent Account Manager

> **Core Problem:** You hit rate limits on your $200/mo Claude Max subscription. Browser OAuth takes 30-60 seconds. CAAM swaps accounts in ~50ms.

**Don't re-learn the command surface here.** `caam --help` (and per-subcommand `--help`) self-describes every command and flag; the full catalog also lives in [COMMANDS.md](references/COMMANDS.md). This skill carries the operating doctrine: how to seed the vault, when to rotate vs cooldown, and how CAAM fits the agent fleet.

## How It Works (why it's safe)

Each AI CLI stores OAuth tokens in plain files (e.g. `~/.claude.json`, `~/.codex/auth.json`, `~/.gemini/oauth_credentials.json`). CAAM backs them up to a local vault and restores them on activate. **No daemons, no databases, no network calls** — just `cp` with extra steps. Vault layout: [VAULT.md](references/VAULT.md).

Supported tools: Claude Code, Codex CLI, Gemini CLI (each on its own subscription).

## Quick Start — Seeding the Vault

```bash
# Install
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/coding_agent_account_manager/main/install.sh?$(date +%s)" | bash

# Backup current account
caam backup claude alice@gmail.com

# Clear, login with another account, backup that too
caam clear claude
claude  # /login with bob@gmail.com
caam backup claude bob@gmail.com

# Switch instantly forever
caam activate claude alice@gmail.com   # ~50ms, no browser
```

A profile must be **backed up once** before it can ever be activated. Seed every account you own up front — mid-rate-limit is the wrong time to discover an empty vault.

## Daily Operations

The four moves that cover almost every session:

```bash
caam status                    # which profile is active per tool (content-hash matched)
caam activate claude --auto    # rotation picks best profile (health, recency, cooldowns)
caam cooldown set claude       # mark current profile rate-limited (60min default); rotation skips it
caam next claude               # preview what rotation would select, without switching
```

### Zero-Friction Aliases

```bash
# Add to .bashrc/.zshrc
alias claude='caam run claude --'
alias codex='caam run codex --'
alias gemini='caam run gemini --'

# Now these auto-failover on rate limits
claude "explain this code"
```

### Project Associations

Link profiles to directories so work and personal accounts never cross:

```bash
cd ~/projects/work-app
caam project set claude work@company.com
caam activate claude            # in this directory, auto-uses work@company.com
```

## Rotation Doctrine

- **Hit a rate limit → `caam cooldown set <tool>` BEFORE switching.** Rotation can only skip profiles it knows are burned. Switching without marking the cooldown sends the next `--auto` right back into the limited account.
- **Prefer `--auto` over hand-picking** once ≥2 profiles exist — the default `smart` algorithm weighs cooldown, health, recency, and jitter. (`round_robin`/`random` exist; details in [COMMANDS.md](references/COMMANDS.md).)
- **Check `caam status` after any activate** — content-hash matching tells you what is actually live, not what you intended.
- The interactive dashboard is `caam tui` (blocks the terminal — keybindings self-described in-app). Agents should stick to the non-interactive commands above.

## Flywheel Integration

| Tool | Integration |
|------|-------------|
| **NTM** | Each tmux pane uses a different account via isolated profiles — see [ISOLATED-PROFILES.md](references/ISOLATED-PROFILES.md) |
| **Agent Mail** | Agents coordinate account switching across sessions |
| **CASS** | Search sessions by account for usage patterns |

## References

| Topic | Reference |
|-------|-----------|
| Complete commands | [COMMANDS.md](references/COMMANDS.md) |
| Isolated profiles | [ISOLATED-PROFILES.md](references/ISOLATED-PROFILES.md) |
| Vault structure | [VAULT.md](references/VAULT.md) |

## Validation

```bash
caam --version                          # verify installation
caam status                             # check all profiles
caam activate claude --auto && caam status   # test switch
```
