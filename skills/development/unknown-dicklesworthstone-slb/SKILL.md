---
name: slb
description: >-
  Simultaneous Launch Button - Two-person rule for destructive commands. Use when
  coordinating dangerous operations between agents, requiring peer review for rm -rf,
  git push --force, kubectl delete, DROP TABLE, or terraform destroy.
---

<!-- TOC: Quick Start | THE EXACT PROMPT | Risk Tiers | Workflow | References -->

# SLB — Simultaneous Launch Button

> **Core Capability:** Two-person rule for running potentially destructive commands from AI coding agents. When an agent wants to run something risky, SLB requires peer review and explicit approval before execution.

## Why This Exists

Coding agents can get tunnel vision, hallucinate, or misunderstand context. A second reviewer (ideally with a different model/tooling) catches mistakes before they become irreversible.

**Critical:** Commands run in YOUR shell environment, not on a server. The daemon is a NOTARY (verifies approvals), not an executor.

---

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/slb/main/scripts/install.sh | bash

# Initialize project
cd /path/to/project
slb init

# Start session
slb session start --agent "GreenLake" --program "claude-code" --model "opus"
```

---

## THE EXACT PROMPT — Basic Workflow

```bash
# 1. Run a dangerous command (blocks until approved)
slb run "rm -rf ./build" --reason "Clean build artifacts" --session-id <id>

# 2. Another agent reviews and approves
slb pending                    # See what's waiting
slb review <request-id>        # View full details
slb approve <request-id> --session-id <reviewer-id> --comment "Looks safe"

# 3. Original command executes automatically after approval
```

---

## Risk Tiers

| Tier | Approvals | Auto-approve | Examples |
|------|-----------|--------------|----------|
| **CRITICAL** | 2+ | Never | `rm -rf /`, `DROP DATABASE`, `terraform destroy`, `git push --force` |
| **DANGEROUS** | 1 | Never | `rm -rf ./build`, `git reset --hard`, `kubectl delete`, `DROP TABLE` |
| **CAUTION** | 0 | After 30s | `rm file.txt`, `git branch -d`, `npm uninstall` |
| **SAFE** | 0 | Immediately | `rm *.log`, `git stash`, `kubectl delete pod` |

---

## Essential Commands

| Category | Command | Description |
|----------|---------|-------------|
| Session | `slb session start --agent <name>` | Start agent session |
| Session | `slb session list` | Show active sessions |
| Request | `slb run "<cmd>" --reason "..."` | Run dangerous command |
| Review | `slb pending` | List pending requests |
| Review | `slb approve <id> --session-id <id>` | Approve request |
| Review | `slb reject <id> --reason "..."` | Reject request |
| Hook | `slb hook install` | Install Claude Code hook |
| Pattern | `slb patterns test "<cmd>"` | Check command tier |

---

## Claude Code Hook

```bash
# Install hook
slb hook install

# Hook actions:
# - allow: Command proceeds (SAFE tier)
# - ask: User prompted (CAUTION tier)
# - block: Blocked, must use `slb request` (DANGEROUS/CRITICAL tier)
```

---

## Execution Verification (5 Gates)

| Gate | Check |
|------|-------|
| **1. Status** | Request must be APPROVED |
| **2. Expiry** | Approval TTL must not have elapsed |
| **3. Hash** | SHA-256 hash must match (tamper detection) |
| **4. Tier** | Risk tier must still match |
| **5. First-Executor** | Atomic claim prevents race conditions |

---

## Emergency Override

For true emergencies, humans can bypass with extensive logging:

```bash
slb emergency-execute "rm -rf /tmp/broken" --reason "System emergency"
```

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Pattern matching & tiers | [PATTERNS.md](references/PATTERNS.md) |
| Configuration | [CONFIG.md](references/CONFIG.md) |
| Security design | [SECURITY.md](references/SECURITY.md) |
