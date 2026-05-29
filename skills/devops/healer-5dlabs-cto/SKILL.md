---
name: healer
description: Healer monitoring expertise - detection patterns, API endpoints, dual-model architecture, and remediation workflows. Use when monitoring Play workflows or debugging agent failures.
---

# Healer Skill

Healer is the observability and self-healing layer for CTO Play workflows. It monitors pod logs via Loki, detects issues, and orchestrates remediations.

## When to Use

- Monitoring Play workflow execution
- Debugging agent failures (pre-flight, runtime)
- Understanding detection patterns (A10, A11, A12)
- Checking session status

---

## Healer API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/v1/session/start` | POST | MCP calls this on play() |
| `/api/v1/session/{play_id}` | GET | Get session details |
| `/api/v1/sessions` | GET | List all sessions |
| `/api/v1/sessions/active` | GET | List active sessions only |

### Check Active Sessions

```bash
curl http://localhost:8083/api/v1/sessions/active | jq
```

---

## Detection Patterns

### Priority 1: Pre-Flight Failures (within 60s of agent start)

| Pattern | Alert Code | Meaning |
|---------|-----------|---------|
| `tool inventory mismatch` | A10 | Agent missing declared tools |
| `Tool inventory MISMATCH` | A10 | Specific tool unavailable |
| `declared tools.*missing` | A10 | Tools in config not in CLI |
| `cto-config.*(missing\|invalid)` | A11 | Config not loaded/synced |
| `mcp.*failed to initialize` | A12 | MCP server init failure |
| `tools-server.*unreachable` | A12 | Tools-server down |

### Priority 2: Runtime Failures

| Pattern | Severity | Action |
|---------|----------|--------|
| `panicked at`, `fatal error` | Critical | Immediate escalation |
| `timeout`, `connection refused` | High | Infrastructure issue |
| `max retries exceeded` | High | Agent exhausted attempts |
| `permission denied.*filesystem` | Critical | Can't read/write files |
| `unauthorized\|invalid token` | Critical | Auth broken |

### Priority 3: Lifecycle Issues

| Pattern | Meaning |
|---------|---------|
| `template not found` | Prompt template missing |
| `prompt.*missing` | Agent instructions not loaded |
| `role.*undefined` | Agent role not set |
| `task context.*empty` | Task details not injected |

---

## Dual-Model Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DUAL-MODEL HEALER ARCHITECTURE                        │
│                                                                              │
│   DATA SOURCES                                                              │
│   ├─ Loki (all pod logs)                                                    │
│   ├─ Kubernetes (CodeRuns, Pods, Events)                                    │
│   ├─ GitHub (PRs, comments, CI status)                                      │
│   └─ CTO Config (expected tools, agent settings)                            │
│                              │                                               │
│                              ▼                                               │
│   MODEL 1: EVALUATION AGENT                                                 │
│   ├─ Parses and comprehends ALL logs                                        │
│   ├─ Correlates events across agents                                        │
│   ├─ Identifies root cause                                                  │
│   └─ Creates GitHub Issue with analysis                                     │
│                              │                                               │
│                              ▼                                               │
│   MODEL 2: REMEDIATION AGENT                                                │
│   ├─ Reads the GitHub issue                                                 │
│   ├─ Implements the fix                                                     │
│   ├─ Creates PR with changes                                                │
│   └─ Marks issue resolved                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Session Notification Flow

```
MCP play() call
    │
    ▼
POST /api/v1/session/start
    │
    └─ Payload: {
         play_id,
         repository,
         cto_config: { agents, tools },
         tasks: [...]
       }
    │
    ▼
Healer stores session with expected tools per agent
    │
    ▼
CodeRuns start with Healer already aware
```

---

## Watch Logs

### Pod Logs

```bash
# Watch all CTO pods
kubectl logs -n cto -l app.kubernetes.io/part-of=cto -f --tail=100

# Watch specific agent CodeRun
kubectl logs -n cto -l app=coderun -f
```

### Loki Query

```
{namespace="cto"} |= "error" | json
```

---

## Pre-Flight Checklist (Verify within 60s)

For every agent run, Healer verifies:

### Prompts
- [ ] Agent type identified
- [ ] Role matches task
- [ ] Template loaded
- [ ] Language context set

### MCP Tools (from CTO Config)
- [ ] CTO config loaded
- [ ] Remote tools accessible
- [ ] Local servers initialized
- [ ] Tools-server reachable

---

## Escalation

When issues detected:

1. **Evaluation Agent** creates GitHub issue with root cause
2. **Remediation Agent** attempts fix (if automatable)
3. **Discord notification** for P0/P1 critical issues
4. **Human escalation** if remediation fails

---

## Configuration

In `cto-config.json`:

```json
{
  "defaults": {
    "play": {
      "healerEndpoint": "http://localhost:8083"
    },
    "remediation": {
      "maxIterations": 3,
      "syncTimeoutSecs": 300
    }
  }
}
```

---

## Reference Documentation

- [docs/heal-play.md](docs/heal-play.md) - Full Healer specification
- [crates/healer/](crates/healer/) - Healer implementation
- [crates/healer/src/scanner.rs](crates/healer/src/scanner.rs) - Detection patterns
