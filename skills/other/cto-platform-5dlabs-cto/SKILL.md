---
name: cto-platform
description: CTO Platform lifecycle expertise - Play workflow orchestration, intake processing, MCP tools, and agent sequencing. Use when managing the full development lifecycle from PRD to deployed code.
---

# CTO Platform Skill

Comprehensive knowledge of the CTO (Cognitive Task Orchestrator) platform for AI-driven development workflows.

## When to Use

- Running intake to generate tasks from PRDs
- Starting and monitoring Play workflows
- Understanding agent sequencing and responsibilities
- Debugging workflow issues

---

## Intake Workflow

### MCP Tool

```
mcp_cto_intake(project_name="my-project")
```

### Flow

```
PRD Document → mcp_cto_intake() → Linear Project Created
                                → PRD Issue with Morgan as delegate
                                → PM Webhook → Argo Workflow
                                → Morgan Pod generates tasks.json
                                → Task issues created in Linear
```

### Key Points

- `local: false` in cto-config.json = Argo workflow (production)
- `local: true` = local binary execution (debugging only)
- Morgan auto-assigned triggers intake via PM webhook

---

## Play Workflow

### MCP Tools

```
mcp_cto_play()           # Start workflow, auto-detects next task
mcp_cto_play_status()    # Query progress
mcp_cto_jobs()           # List running workflows
mcp_cto_stop_job()       # Cancel workflow
```

### Agent Sequence (Per Task)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PLAY WORKFLOW (Per Task)                           │
│                                                                              │
│   1. IMPLEMENTATION AGENT (based on task.agentHint)                         │
│      ├─ bolt (infrastructure - Task 1 ALWAYS, plus any infra tasks)        │
│      ├─ rex (Rust: axum, tokio, sqlx)                                       │
│      ├─ grizz (Go: chi, grpc, pgx)                                          │
│      ├─ nova (Node.js/Bun: Elysia, Effect, Drizzle)                         │
│      ├─ blaze (React/Web: Next.js, shadcn/ui, TailwindCSS)                  │
│      ├─ tap (Mobile: Expo, React Native)                                    │
│      └─ spark (Desktop: Electron)                                           │
│                                                                              │
│   2. SUPPORT AGENTS (sequential, run for EVERY task)                        │
│      ├─ Cleo (quality) ──── max 5 retries                                   │
│      ├─ Cipher (security) ─ max 2 retries                                   │
│      ├─ Tess (testing) ──── max 5 retries                                   │
│      └─ Atlas (integration) final merge gate                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## cto-config.json Structure

```json
{
  "version": "1.0",
  "orgName": "5DLabs",
  "defaults": {
    "intake": {
      "local": false,           // MUST be false for production
      "githubApp": "5DLabs-Morgan"
    },
    "linear": {
      "teamId": "CTOPA",
      "pmServerUrl": "http://localhost:8081"
    },
    "play": {
      "repository": "5dlabs/cto",
      "healerEndpoint": "http://localhost:8083",
      "autoMerge": true,        // Atlas auto-merges PRs
      "implementationMaxRetries": 10,
      "qualityMaxRetries": 5,
      "securityMaxRetries": 2,
      "testingMaxRetries": 5
    }
  },
  "agents": {
    "morgan": { ... },
    "bolt": { ... },
    "rex": { ... },
    // ...
  }
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `intake.local` | `false` = Argo workflow, `true` = local binary |
| `play.autoMerge` | Atlas merges PRs automatically |
| `play.healerEndpoint` | Healer API for session notifications |
| `play.*MaxRetries` | Per-agent retry limits |

---

## Execution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IN-CLUSTER EXECUTION FLOW                             │
│                                                                              │
│   MCP Tool Call (Droid/Cursor)                                              │
│       └─→ Submits Argo Workflow                                             │
│           └─→ Controller creates CodeRuns (pods)                            │
│               └─→ Each agent runs in isolated container                     │
│                   └─→ Linear sidecar streams activities                     │
│                       └─→ Healer monitors via Loki                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Local Development

### Services to Run

```bash
just dev-controller       # Controller
just dev-pm              # PM Server (:8081)
just dev-healer-play-api # Healer (:8083)

# Or all at once:
mprocs
```

### Port Forwards

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:80
kubectl port-forward svc/argo-workflows-server -n automation 2746:2746
```

---

## Autonomy Permissions

When running E2E tests with full autonomy:

1. **MAY** merge pull requests via Atlas
2. **MAY** update Linear issues directly
3. **MAY** execute all MCP tools without confirmation
4. **MAY** handle all agent transitions
5. **MAY** create and close GitHub issues

---

## Reference Documentation

- [docs/linear-integration-workflow.md](docs/linear-integration-workflow.md) - Linear webhook flow
- [docs/heal-play.md](docs/heal-play.md) - Healer monitoring
- [cto-config.template.json](cto-config.template.json) - Config field documentation
- [AGENTS.md](AGENTS.md) - Agent overview
