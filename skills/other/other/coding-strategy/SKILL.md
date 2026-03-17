---
name: coding-strategy
description: >
  Consult before ANY coding task. Chooses the optimal coding agent strategy based on task complexity,
  available free tokens, parallelism potential, and provider quotas. Covers: OpenClaw sub-agents,
  Codex CLI, Claude Flow swarms/hive-minds, Jules (Google), GitHub Copilot coding models,
  Augment Code, Kimi K2.5, and OpenAI gpt-5.3-codex. All agents must read this before writing code.
---

# Coding Strategy Skill

**Read this before ANY coding task.** Even small ones. The goal: maximize free tokens, spread load across providers, and pick the right tool for the job.

---

## Provider Inventory

### Tier 1 — Free / Subscription-Included (use first)

| Provider | Access | Best For | How to Invoke |
|----------|--------|----------|---------------|
| **GitHub Copilot** | Token auth (subscription) | Fast tasks, code completion, reviews | `sessions_spawn` with `model: "github-copilot/claude-sonnet-4.5"` or any copilot model |
| **OpenAI Codex CLI** | OAuth ($20/mo subscription) | Complex single-file tasks, full-auto mode | `exec pty:true command:"codex exec --full-auto 'prompt'" workdir:/path` |
| **Kimi K2.5** | API key (kimi-coding) | Reasoning-heavy tasks, architecture, large context | `sessions_spawn` with `model: "kimi-coding/k2p5"` |
| **Jules** (Google) | API key: `op://DeLoSecrets/Jules/API Key` | Async background coding, PR generation | See Jules section below |
| **Augment (auggie)** | CLI at `~/.bun/bin/auggie` | Code generation, refactoring, indexing | See Augment section below |

### Tier 2 — Pay-per-token (use intentionally)

| Provider | Access | Best For | Cost |
|----------|--------|----------|------|
| **Anthropic Sonnet** | Token auth | Complex multi-step coding, tool use | Moderate |
| **Anthropic Opus** | Token auth | Architecture decisions, hard debugging | Expensive — use sparingly |
| **OpenAI gpt-5.3-codex** | API key | Heavy coding, long context | Moderate-high |
| **Google Gemini Pro** | Gemini CLI auth | Large context analysis, doc generation | Moderate |

### Tier 3 — Orchestration (for complex multi-file work)

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| **Claude Flow Swarm** | 15-agent hierarchical mesh | Large features spanning many files |
| **Claude Flow Hive-Mind** | Queen-led consensus coordination | Architecture decisions, code review |
| **OpenClaw sub-agents** | `sessions_spawn` parallel workers | Independent tasks that don't need shared state |

---

## Decision Matrix

### Step 1: Classify the task

| Task Type | Examples | Complexity |
|-----------|----------|------------|
| **Trivial** | Fix a typo, add an import, rename variable | Single file, <10 lines |
| **Small** | Add a function, write a test, fix a bug | Single file, <100 lines |
| **Medium** | New component, API endpoint, refactor module | 2-5 files, <500 lines |
| **Large** | New feature, service, cross-cutting refactor | 5-20 files, architecture changes |
| **Epic** | New product scaffold, major migration | 20+ files, multi-day |

### Step 2: Pick the strategy

| Complexity | Strategy | Provider Priority |
|------------|----------|-------------------|
| **Trivial** | Do it inline (you ARE a coding agent) | No external agent needed |
| **Small** | Single sub-agent | GitHub Copilot → Kimi K2.5 → Codex CLI |
| **Medium** | Single sub-agent OR Codex CLI (full-auto) | Codex CLI → Kimi K2.5 → Sonnet sub-agent |
| **Large** | Claude Flow swarm OR parallel sub-agents | Claude Flow → parallel Codex instances → Jules (async) |
| **Epic** | Claude Flow hive-mind + parallel Codex + Jules | All hands on deck — spread across every provider |

### Step 3: Maximize free tokens

**Always exhaust free/subscription tiers before pay-per-token:**

1. **GitHub Copilot models** — included in subscription, use freely
2. **Codex CLI** — $20/mo flat, use `--full-auto` or `--yolo` liberally
3. **Kimi K2.5** — generous free tier, great for reasoning
4. **Jules** — included in Google Max plan, async background work
5. **Augment** — free tier tokens available
6. THEN fall back to Anthropic Sonnet/Opus or OpenAI API

---

## Provider-Specific Instructions

### Codex CLI (OpenAI)
```bash
# One-shot task (PTY required!)
exec pty:true workdir:/path/to/repo command:"codex exec --full-auto 'Your task description'"

# Background for longer work
exec pty:true workdir:/path/to/repo background:true command:"codex exec --full-auto 'Your task. When done, run: openclaw gateway wake --text \"Done: brief summary\" --mode now'"

# YOLO mode (no sandbox, no approvals — fastest)
exec pty:true workdir:/path/to/repo command:"codex exec --yolo 'Your task'"

# Code review
exec pty:true workdir:/path/to/repo command:"codex review --base origin/main"
```

**Key:** Codex needs a git repo. Model: `gpt-5.3-codex`. Config: `~/.codex/config.toml`.

### Claude Flow (Multi-Agent Orchestration)
```bash
# Initialize in project (one-time)
exec workdir:/path/to/repo command:"claude-flow init"

# Swarm — hierarchical 15-agent mesh for large features
exec pty:true workdir:/path/to/repo background:true command:"claude-flow swarm start -o 'Build the REST API with auth, tests, and docs' -s development"

# Hive-Mind — consensus-based for architecture decisions
exec pty:true workdir:/path/to/repo background:true command:"claude-flow hive-mind init -t hierarchical-mesh"
# Then spawn workers:
exec pty:true command:"claude-flow hive-mind spawn --claude"
# Submit task:
exec command:"claude-flow hive-mind task 'Refactor auth module for OAuth2 support'"

# Check status
exec command:"claude-flow swarm status"
exec command:"claude-flow hive-mind status"
```

**Key:** Claude Flow has hooks in `.claude-flow/` that enable self-learning. Projects with heavy Claude Flow use should have `claude-flow init` run first.

### Jules (Google AI Coding Agent)
Jules works asynchronously — submit tasks via the Google AI Studio / Jules interface, it creates PRs.

```bash
# Get the API key
JULES_KEY=$(op read "op://DeLoSecrets/Jules/API Key")

# Jules is primarily browser-based at jules.google.com
# For API access, check current docs — the API surface is evolving
# Key pattern: submit task → Jules works in background → creates PR → you review

# For now, use browser automation or the web interface:
# 1. Navigate to jules.google.com
# 2. Connect repo
# 3. Submit task description
# 4. Jules creates a branch + PR asynchronously
```

**API Key:** `op://DeLoSecrets/Jules/API Key`
**Best for:** Async background tasks where you don't need the result immediately. Submit the task, let Jules work, pull the PR when ready. Great for fire-and-forget work while other agents handle synchronous tasks.

### Augment Code (auggie CLI)
```bash
# One-shot task (print mode)
exec pty:true workdir:/path/to/repo command:"auggie -p 'Your task description'"

# Interactive mode
exec pty:true workdir:/path/to/repo background:true command:"auggie 'Your task description'"

# Quiet mode (only final output)
exec pty:true workdir:/path/to/repo command:"auggie -q 'Your task'"

# With image input
exec pty:true workdir:/path/to/repo command:"auggie --image screenshot.png 'Implement this UI'"

# Ask mode (read-only, no edits — good for analysis)
exec pty:true workdir:/path/to/repo command:"auggie --ask 'Explain the auth flow in this codebase'"
```

**Binary:** `~/.bun/bin/auggie`
**Best for:** Code generation, refactoring, codebase-aware tasks. Has workspace indexing for deep context.
**Note:** First run in a new workspace triggers an indexing step. Use `--print` from workspace root to index.

### OpenClaw Sub-Agents (Built-in)
```python
# Spawn a coding sub-agent on a free provider
sessions_spawn(
    task="Implement the user settings page with React and TypeScript",
    model="github-copilot/claude-sonnet-4.5",  # FREE via subscription
    label="settings-page"
)

# Spawn on Kimi for reasoning-heavy work
sessions_spawn(
    task="Architect the event sourcing system for order processing",
    model="kimi-coding/k2p5",  # Free tier
    label="event-sourcing-arch"
)

# Parallel workers — different providers, different tasks
sessions_spawn(task="Write unit tests for auth module", model="github-copilot/gpt-5.2-codex", label="auth-tests")
sessions_spawn(task="Write integration tests for API", model="kimi-coding/k2p5", label="api-tests")
sessions_spawn(task="Update API documentation", model="github-copilot/gemini-3-flash-preview", label="api-docs")
```

### GitHub Copilot Models (via OpenClaw)
Available models through `github-copilot/` prefix — all included in subscription:
- `github-copilot/claude-sonnet-4.5` — best all-rounder
- `github-copilot/claude-opus-4.6` — heavy reasoning
- `github-copilot/claude-haiku-4.5` — fast, cheap tasks
- `github-copilot/gpt-5.2-codex` — strong coding
- `github-copilot/gpt-4o` — general purpose
- `github-copilot/gemini-3-pro-preview` — large context
- `github-copilot/gemini-3-flash-preview` — fast, large context
- `github-copilot/grok-code-fast-1` — fast coding

---

## Parallelism Patterns

### Pattern 1: Fan-Out (independent tasks)
```
Task: "Build user dashboard"
├── Sub-agent 1 (copilot/sonnet): "Build UserProfile component"
├── Sub-agent 2 (kimi-k2.5): "Build ActivityFeed component"
├── Sub-agent 3 (codex CLI): "Build SettingsPanel component"
└── Sub-agent 4 (copilot/gemini): "Write tests for all components"
```

### Pattern 2: Pipeline (sequential dependencies)
```
Step 1 (kimi-k2.5): "Design the API schema and types"
  → Step 2 (codex --full-auto): "Implement the API endpoints"
    → Step 3 (copilot/sonnet): "Write integration tests"
      → Step 4 (copilot/haiku): "Generate API documentation"
```

### Pattern 3: Claude Flow Swarm (complex features)
```bash
claude-flow swarm start -o "Build complete auth system: OAuth2, JWT, RBAC, tests, docs" -s development
# Swarm auto-coordinates 15 agents across the feature
```

### Pattern 4: Review Army (batch PR reviews)
```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'
# Deploy parallel Codex reviewers
exec pty:true background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"
exec pty:true background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"
```

---

## Rules

1. **Always check this skill before coding** — even for small tasks
2. **Free tokens first** — exhaust GitHub Copilot, Codex CLI, Kimi, Jules, Augment before paying
3. **PTY required for Codex CLI** — `pty:true` always
4. **Codex needs a git repo** — won't run outside one
5. **Never run coding agents in `~/.openclaw/`** — they'll read soul docs and get weird
6. **Notify on completion** — append `openclaw gateway wake` to long-running prompts
7. **Track what's running** — use `process action:list` and `sessions_list` to monitor
8. **Spread the load** — don't burn one provider when others have free tokens
9. **Claude Flow for 5+ file changes** — swarms are more efficient than manual coordination
10. **Jules for async** — submit and forget, pull PR when ready
