---
name: cass-memory
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when starting non-trivial work, mining lessons, or preventing repeated mistakes with cm procedural memory."
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | THE EXACT PROMPT | Architecture | Commands | References -->

# cass-memory — CASS Memory System (cm)

> **Core Capability:** Transforms scattered agent sessions into persistent, cross-agent procedural memory. A pattern discovered in Cursor **automatically** helps Claude Code on the next session.

## Quick Start

```bash
# Initialize with a starter playbook
cm init --starter typescript

# THE ONE COMMAND: run before any non-trivial task
cm context "implement user authentication" --json

# Check system health
cm doctor --json
```

---

## THE EXACT PROMPT — Session Start

```
Before starting this task, run:

cm context "<task description>" --json

Read the output carefully:
- relevantBullets: Rules from playbook scored by relevance
- antiPatterns: Things that have caused problems before
- historySnippets: Past sessions (yours and other agents')
- suggestedCassQueries: Deeper investigation if needed

Reference rule IDs when following them (e.g., "Following b-8f3a2c...")
```

---

## THE EXACT PROMPT — Rule Feedback

```
# When a rule helped
cm mark b-8f3a2c --helpful

# When a rule caused problems
cm mark b-xyz789 --harmful --reason "Caused regression"

# Or leave inline comments (parsed during reflection)
// [cass: helpful b-8f3a2c] - this saved me from a rabbit hole
// [cass: harmful b-x7k9p1] - wrong for our use case
```

---

## THE EXACT PROMPT — Trauma Guard Setup

```
# Install safety hooks to prevent dangerous commands
cm guard --install       # Claude Code hook
cm guard --git          # Git pre-commit hook
cm guard --status       # Check installation

# Add custom trauma patterns
cm trauma add "DROP TABLE" --description "Mass deletion" --severity critical

# Scan past sessions for trauma patterns
cm trauma scan --days 30
```

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPISODIC MEMORY (cass)                           │
│   Raw session logs from all agents — the "ground truth"             │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ cass search
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    WORKING MEMORY (Diary)                           │
│   Structured session summaries: accomplishments, decisions, etc.    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ reflect + curate (automated)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCEDURAL MEMORY (Playbook)                     │
│   Distilled rules with confidence tracking and decay                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Essential Commands

| Command | Purpose |
|---------|---------|
| `cm context "<task>" --json` | Get rules + history for task |
| `cm mark <id> --helpful/--harmful` | Record feedback |
| `cm playbook list` | View all rules |
| `cm top 10` | Top effective rules |
| `cm doctor --json` | System health |
| `cm guard --install` | Install safety hooks |

---

## Agent Protocol

```
1. START:    cm context "<task>" --json
2. WORK:     Reference rule IDs when following them
3. FEEDBACK: Leave inline comments when rules help/hurt
4. END:      Just finish. Learning happens automatically.
```

**You do NOT need to:**
- Run `cm reflect` (automation handles this)
- Run `cm mark` manually (use inline comments)
- Manually add rules to the playbook

---

## Confidence Decay

Rules aren't immortal. Confidence decays without revalidation:

| Mechanism | Effect |
|-----------|--------|
| **90-day half-life** | Confidence halves every 90 days without feedback |
| **4x harmful multiplier** | One mistake counts 4x as much as one success |
| **Maturity progression** | `candidate` → `established` → `proven` |

---

## Anti-Pattern Learning

Bad rules don't just get deleted. They become warnings:

```
"Cache auth tokens for performance"
    ↓ (3 harmful marks)
"PITFALL: Don't cache auth tokens without expiry validation"
```

---

## Starter Playbooks

```bash
cm starters                    # List available
cm init --starter typescript   # Initialize with starter
cm playbook bootstrap react    # Apply to existing playbook
```

| Starter | Focus |
|---------|-------|
| **general** | Universal best practices |
| **typescript** | TypeScript/Node.js |
| **react** | React/Next.js |
| **python** | Python/FastAPI/Django |
| **rust** | Rust service patterns |

---

## Token Budget Management

| Flag | Effect |
|------|--------|
| `--limit N` | Cap number of rules |
| `--min-score N` | Only rules above threshold |
| `--no-history` | Skip historical snippets |
| `--json` | Structured output |

---

## Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| No cass | Playbook-only scoring, no history |
| No playbook | Empty playbook, commands still work |
| No LLM | Deterministic reflection |
| Offline | Cached playbook + local diary |

---

## Installation

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/cass_memory_system/main/install.sh \
  | bash -s -- --easy-mode --verify

# From source
git clone https://github.com/Dicklesworthstone/cass_memory_system.git
cd cass_memory_system
bun install && bun run build
sudo mv ./dist/cass-memory /usr/local/bin/cm
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `cass not found` | Install cass first |
| `API key missing` | Set `ANTHROPIC_API_KEY` |
| `Playbook corrupt` | Run `cm doctor --fix` |

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Cognitive architecture | [ARCHITECTURE.md](references/ARCHITECTURE.md) |
| Trauma guard system | [TRAUMA-GUARD.md](references/TRAUMA-GUARD.md) |
| MCP server integration | [MCP-SERVER.md](references/MCP-SERVER.md) |
| Onboarding workflow | [ONBOARDING.md](references/ONBOARDING.md) |
