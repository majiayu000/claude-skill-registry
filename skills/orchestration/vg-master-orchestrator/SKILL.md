---
name: vg-master-orchestrator
description: Master Orchestrator for autonomous multi-agent coordination. Use when tasks require multiple technology experts, complex workflows (TDD pattern addition, security audits), intelligent routing, or explicit orchestration requests. Coordinates 17 technology experts with real-time progress reporting.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task, SlashCommand, Skill]
---

# Master Orchestrator - Execution Instructions (v2.0.0)

## Purpose
Execute autonomous multi-agent coordination for Vigil Guard v2.0.0 tasks. Analyze, classify, route to technology experts, and synthesize results.

## Quick Reference

**Architecture:** 3-Branch Parallel Detection (24 nodes)
**Available experts:** 17 technology experts in `.claude/agents/`
**Full details:** See CLAUDE.md section "Technology Expert Agents (v3.0)"

### Technology Experts (17)

| Expert | Technology | Use For |
|--------|------------|---------|
| `orchestrator` | Coordination | Multi-expert task routing |
| `n8n-expert` | n8n | Workflows, nodes, webhooks |
| `react-expert` | React + Vite | Components, hooks, UI |
| `express-expert` | Express.js | REST APIs, middleware |
| `vitest-expert` | Vitest | Testing, TDD, fixtures |
| `clickhouse-expert` | ClickHouse | Analytics SQL, schema |
| `docker-expert` | Docker | Containers, compose (11 services) |
| `presidio-expert` | MS Presidio | PII detection, NLP |
| `security-expert` | Security | OWASP, auth, vulnerabilities |
| `git-expert` | Git | Version control, commits |
| `python-expert` | Python | Flask, FastAPI |
| `tailwind-expert` | Tailwind CSS | Styling |
| `kubernetes-expert` | Kubernetes | Cluster ops, pods, deployments |
| `helm-expert` | Helm | Charts, releases, templating |
| `nats-expert` | NATS | Messaging, JetStream (future) |
| `redis-expert` | Redis | Caching, rate limiting (future) |
| `code-audit-expert` | Code Auditing | Quality assessment, tech debt |

## v2.0.0 Architecture Context

### 3-Branch Parallel Detection System
```
Input → Validate → Config Load
         ↓
    3-Branch Executor (PARALLEL):
    ├─ Branch A: Heuristics (:5005) - 30% weight
    ├─ Branch B: Semantic (:5006) - 35% weight
    └─ Branch C: LLM Guard (:8000) - 35% weight
         ↓
    Arbiter v2 (weighted fusion)
         ↓
    Decision → PII Redaction → ClickHouse Log
```

### Key Services (11 Docker containers)
- `vigil-heuristics` (5005) - Pattern detection
- `vigil-semantic-service` (5006) - Embedding similarity
- `vigil-presidio-pii` (5001) - PII detection
- `vigil-language-detector` (5002) - Language detection
- `vigil-n8n` (5678) - Workflow engine
- `vigil-clickhouse` (8123) - Analytics DB
- `vigil-grafana` (3001) - Monitoring
- `web-ui-backend` (8787) - Config API
- `web-ui-frontend` (80) - React UI
- `vigil-prompt-guard-api` (8000) - LLM safety
- `vigil-caddy` (80/443) - Reverse proxy

## Execution Steps

### 1. Classify Task (Lightweight)

Determine strategy WITHOUT reading files:
- **Single:** One expert needed
- **Parallel:** Multiple independent experts
- **Sequential:** Experts depend on previous results
- **Workflow:** Matches pre-configured template

**Workflows:**
- PATTERN_ADDITION (TDD): vitest-expert → n8n-expert → vitest-expert
- SECURITY_AUDIT (Parallel): security-expert + vitest-expert + docker-expert
- PII_ENTITY_ADDITION: presidio-expert → express-expert → react-expert → vitest-expert

### 2. Execute with Progress Reporting

**Format:**
```
🎯 Task: [description]
🎭 Strategy: [single|parallel|sequential|workflow]

🤖 Expert: [name]-expert
├─ ▶️  Action: [action]
├─ 📝 [progress]
└─ ✅ Completed (X.Xs)

✨ Task Completed
```

### 3. Expert Invocation Methods

**Option A - Use existing skill (FASTEST):**
- `vigil-testing-e2e` for testing tasks
- `n8n-vigil-workflow` for workflow/pattern tasks
- `presidio-pii-specialist` for PII tasks
- `react-tailwind-vigil-ui` for UI tasks
- `docker-vigil-orchestration` for container tasks
- etc.

**Option B - Task tool with technology expert:**
```
Task(
  prompt="You are n8n-expert. [task description]",
  subagent_type="n8n-expert"
)
```

**Option C - Direct implementation:**
- Use Read/Write/Edit/Bash tools directly
- Only when no skill/expert available

### 4. Result Synthesis

```
═══════════════════════════════════════
✨ Task Completed in X.Xs

📋 Summary: [what was done]

🤝 Coordinated N experts:
   • n8n-expert
   • vitest-expert

💡 Next Steps:
   1. [action 1]
   2. [action 2]
```

## Critical Rules

### DO:
- ✅ Use existing skills when available (performance)
- ✅ Show real-time progress with emoji indicators
- ✅ Keep skill operations lightweight
- ✅ Reference v2.0.0 architecture (3-branch parallel, 24 nodes)
- ✅ Synthesize results concisely

### DON'T:
- ❌ Reference old vg-* agents (REMOVED in v3.0)
- ❌ Reference 40-node sequential pipeline (NOW 24-node parallel)
- ❌ Reference rules.config.json (MERGED into unified_config.json)
- ❌ Read `.claude/agents/*/AGENT.md` unless truly needed
- ❌ Just show documentation (EXECUTE the work)
- ❌ Load unnecessary context

## Token Optimization

**Problem:** This skill + CLAUDE.md can cause session hangs due to token overload.

**Solution:**
1. Classify tasks WITHOUT reading files
2. Use existing skills (they're already loaded)
3. Only read AGENT.md if truly needed
4. Keep progress reporting concise

## Error Handling

If expert fails:
1. Report error with expert name
2. Retry once
3. Suggest fallback expert
4. Continue with remaining work if possible

## Integration

**Slash command:** `/vg-orchestrate [task]` → invokes this skill
**Direct:** User can also invoke via `@vg-master-orchestrator` or Skill tool

## Version History
- v2.0.0 (2025-12): Updated for 3-branch architecture, 17 technology experts
- v2.0.1 (legacy): 10 vg-* agents (DEPRECATED)

Ready to orchestrate!
