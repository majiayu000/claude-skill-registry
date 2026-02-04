---
name: auto-parallel
description: Enable parallel agent execution for multi-domain features with git worktree isolation
argument-hint: "[INCREMENT_ID] --frontend --backend [OPTIONS]"
allowed-tools: ["Bash(specweave auto *)"]
---

# Parallel Execution Mode

**Enable parallel agent execution for multi-domain features.**

## What is Parallel Mode?

Parallel mode spawns multiple specialized agents that work simultaneously on different parts of your feature:
- **Frontend Agent**: React, Vue, Angular, UI components
- **Backend Agent**: API, services, controllers, middleware
- **Database Agent**: Schema, migrations, queries, indexes
- **DevOps Agent**: CI/CD, Docker, Terraform, infrastructure
- **QA Agent**: Tests, E2E, coverage, validation

Each agent works in its own **git worktree** for complete isolation - no merge conflicts during development!

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--parallel` | Enable parallel mode | false |
| `--max-parallel N` | Max concurrent agents | 3 |
| `--frontend` | Spawn frontend agent | false |
| `--backend` | Spawn backend agent | false |
| `--database` | Spawn database agent | false |
| `--devops` | Spawn devops agent | false |
| `--qa` | Spawn QA agent | false |
| `--pr` | Create PRs on completion | false |
| `--draft-pr` | Create PRs in draft mode | false |
| `--merge-strategy` | Merge: auto\|manual\|pr | auto |
| `--base-branch` | Base branch for merging | main |
| `--prompt` | Analyze prompt for suggestions | - |

## Examples

**Parallel Frontend + Backend:**
```bash
/sw:auto --parallel --frontend --backend 0170-auth-feature
```

**With PR Creation:**
```bash
/sw:auto --parallel --frontend --backend --pr 0170-auth-feature
```

**Analyze Prompt for Suggestions:**
```bash
/sw:auto --prompt "Build React login with Express API and PostgreSQL"

# Output:
# ✓ Parallel execution recommended
# Detected domains: frontend, backend, database
# Suggestions:
#   --parallel --frontend --backend --database
```

**Full Stack with All Domains:**
```bash
/sw:auto --parallel --frontend --backend --database --qa 0170-feature
```

## How Parallel Mode Works

```
1. /sw:auto --parallel --frontend --backend 0170
           │
           ▼
2. Session created with 2 agents
   └─ .specweave/state/parallel/session.json
           │
           ▼
3. Git worktrees created
   ├─ .specweave/worktrees/frontend-0170/
   └─ .specweave/worktrees/backend-0170/
           │
           ▼
4. Agents work in parallel
   ├─ Frontend agent: UI components
   └─ Backend agent: API endpoints
           │
           ▼
5. Completion detected
           │
           ├─ --pr flag? → Create PRs
           │   ├─ PR #1: [0170] frontend: Auth UI
           │   └─ PR #2: [0170] backend: Auth API
           │
           └─ --merge-strategy auto? → Merge to base
               ├─ database first
               ├─ backend second
               └─ frontend last
```

## Status Dashboard

```bash
/sw:auto-status --parallel

# Output:
╔═══════════════════════════════════════════════════════════════════╗
║  PARALLEL SESSION: session-abc123                                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  Agent      │ Status  │ Progress    │ Time   │ Branch               ║
║  ───────────────────────────────────────────────────────────────── ║
║  frontend   │ 🔄 run  │ ████░░ 4/6  │  12m   │ auto/frontend-0170   ║
║  backend    │ ✅ done │ ██████ 8/8  │  25m   │ auto/backend-0170    ║
║  database   │ ✅ done │ ██████ 3/3  │   5m   │ auto/database-0170   ║
╠═══════════════════════════════════════════════════════════════════╣
║  Overall: 78% │ Completed: 2 │ Running: 1 │ Failed: 0               ║
╚═══════════════════════════════════════════════════════════════════╝
```

**Watch mode (auto-refresh):**
```bash
/sw:auto-status --parallel --watch
```

## Merge Order

Agents are merged in dependency order:
1. **Database** first (schema before API)
2. **Backend** second (API before UI)
3. **Frontend** last (depends on backend)
4. **DevOps/QA** anytime (parallel-safe)

## Stop Hook Integration

The stop hook blocks exit while parallel agents are running:

```
🔄 2 parallel agent(s) running: frontend:running, backend:pending → wait for completion
```

Exit is approved when:
- All agents are completed or failed
- Session is cancelled via `--reset`

## Configuration

In `.specweave/config.json`:

```json
{
  "auto": {
    "parallel": {
      "enabled": true,
      "maxParallel": 3,
      "defaultDomains": ["frontend", "backend"],
      "defaultMergeStrategy": "auto",
      "createPR": false,
      "draftPR": false
    }
  }
}
```

## Cross-Platform Support

Parallel mode works on all platforms:
- **macOS**: Native git worktrees
- **Linux**: Native git worktrees
- **Windows**: Long path support (\\?\\ prefix for >260 chars)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Active session exists" | `specweave auto --reset` to clean up |
| Worktree creation fails | Check git version ≥ 2.5 |
| Merge conflicts | Use `--merge-strategy manual` for control |
| PRs not created | Ensure `gh` CLI is authenticated |

## Best Practices

1. **Start with 2-3 domains**: frontend + backend is most common
2. **Use --prompt first**: Let the analyzer suggest the right flags
3. **Use --draft-pr**: Review before merging
4. **Check status often**: Use `--watch` for live updates
5. **Reset on stuck**: `specweave auto --reset` clears state

## Related

- `/sw:auto` - Main auto mode command
- `/sw:auto-status` - Check session status
