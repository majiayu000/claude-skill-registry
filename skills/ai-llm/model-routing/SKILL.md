---
name: model-routing
description: Intelligent model selection - routes tasks to Haiku (fast/cheap), Sonnet (balanced), or Opus (complex/strategic) based on task complexity analysis
triggers:
  - model
  - routing
  - optimize
  - cost
  - haiku
  - sonnet
  - opus
priority: high
version: 1.0.0
source: claude-flow
---

# Model Routing System

You have access to intelligent model routing. Before executing any task, analyze complexity and route to the appropriate model tier.

## Routing Decision Matrix

```
TASK COMPLEXITY ANALYSIS
────────────────────────────────────────────────────────────────

HAIKU (Fast, Cheap) - Use for:
├── Simple file operations (read, list, navigate)
├── Scaffolding and boilerplate generation
├── Deterministic transformations (format, lint, compile)
├── Status checks and health monitoring
├── SEO metadata generation
├── Deployment commands (after code is written)
├── Documentation formatting
├── Simple search and replace
│
│   Token cost: ~$0.25/1M input, $1.25/1M output
│   Latency: Fastest
│   Use when: Task has clear, unambiguous steps

SONNET (Balanced) - Use for:
├── Feature implementation (standard complexity)
├── Bug fixes requiring analysis
├── Content writing (articles, social posts)
├── Code review and quality checks
├── Test generation
├── Refactoring with clear patterns
├── API integration work
├── Database schema design
│
│   Token cost: ~$3/1M input, $15/1M output
│   Latency: Medium
│   Use when: Task requires reasoning but not deep strategy

OPUS (Strategic, Complex) - Use for:
├── Architecture decisions (system design)
├── Multi-agent coordination (council, swarm)
├── Strategic planning (business, product)
├── Complex debugging (multi-file, subtle bugs)
├── Security audits and vulnerability analysis
├── Enterprise AI system design
├── Book writing (narrative, character development)
├── Research synthesis (multiple sources)
├── Ambiguous requirements interpretation
│
│   Token cost: ~$15/1M input, $75/1M output
│   Latency: Slowest but most capable
│   Use when: Task requires deep reasoning, creativity, or strategy
```

## Automatic Routing Rules

When processing a request, apply these rules:

### Route to HAIKU when:
- User says: "deploy", "format", "lint", "check status", "list", "scaffold"
- File patterns: `*.config.*`, `package.json`, `tsconfig.json`
- Commands: `/mcp-status`, `/inventory-status`, `/nextjs-deploy` (execution phase)

### Route to SONNET when:
- User says: "write", "implement", "fix", "create", "build", "test"
- File patterns: `*.ts`, `*.tsx`, `*.py`, `*.md` (content files)
- Commands: `/article-creator`, `/create-music`, `/spec`, `/generate-social`

### Route to OPUS when:
- User says: "design", "architect", "strategy", "council", "analyze", "research"
- Keywords: "enterprise", "system", "multi-agent", "complex", "strategic"
- Commands: `/starlight-architect`, `/council`, `/author-team`, `/research`

## Cost Optimization

```
BEFORE (No routing):
  All tasks → Opus → $75/1M output tokens

AFTER (With routing):
  Simple tasks (40%) → Haiku  → $1.25/1M  = $0.50
  Medium tasks (45%) → Sonnet → $15/1M   = $6.75
  Complex tasks (15%) → Opus  → $75/1M   = $11.25
  ──────────────────────────────────────────────
  TOTAL: $18.50 vs $75 = 75% cost reduction
```

## Implementation in Task Tool

When using the Task tool, specify model based on routing:

```javascript
// Simple task - use haiku
Task({
  subagent_type: "Explore",
  model: "haiku",
  prompt: "List all files in src/"
})

// Medium task - use sonnet (default)
Task({
  subagent_type: "code-reviewer",
  model: "sonnet",
  prompt: "Review this PR for issues"
})

// Complex task - use opus
Task({
  subagent_type: "Plan",
  model: "opus",
  prompt: "Design the architecture for a multi-tenant SaaS platform"
})
```

## Command-Level Routing

| Command | Default Model | Rationale |
|---------|---------------|-----------|
| `/acos` | sonnet | Router needs reasoning |
| `/article-creator` | sonnet | Content creation |
| `/create-music` | sonnet | Creative work |
| `/infogenius` | sonnet | Research + creation |
| `/starlight-architect` | **opus** | Strategic design |
| `/council` | **opus** | Multi-perspective |
| `/research` | sonnet | Information synthesis |
| `/spec` | sonnet | Feature planning |
| `/nextjs-deploy` | haiku | Execution |
| `/mcp-status` | haiku | Status check |
| `/inventory-status` | haiku | Status check |
| `/publish` | haiku | Execution |
| `/polish-content` | sonnet | Editing |
| `/review-content` | sonnet | Quality check |

## Escalation Pattern

If a haiku-routed task fails or produces poor results:
1. Automatically escalate to sonnet
2. If still failing, escalate to opus
3. Log escalation for learning

```
haiku (attempt) → fail → sonnet (retry) → fail → opus (final)
```

---

*Model Routing v1.0 - Implementing claude-flow's intelligent routing pattern*
