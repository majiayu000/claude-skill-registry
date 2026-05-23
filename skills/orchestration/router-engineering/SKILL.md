---
name: router-engineering
description: Master orchestration for routing technical problems through 32 engineering skills - AI/ML, software development, data, APIs, and Claude Code framework
metadata:
  version: "1.3"
---

# Router: Engineering

Master orchestrator that routes technical problems, implementation questions, and development tasks through the complete engineering skill set.

---

## Decision Tree: Where to Start?

```
TECHNICAL QUESTION
    │
    ├─► "Build an AI agent" ────────────► ai-agents
    │                                      └─► MCP, guardrails, orchestration
    │
    ├─► "Fine-tune / train LLM" ────────► ai-llm
    │                                      └─► PEFT, LoRA, evaluation
    │
    ├─► "Optimize LLM inference" ───────► ai-llm-inference
    │                                      └─► vLLM, quantization, serving
    │
    ├─► "Build RAG system" ─────────────► ai-rag
    │                                      └─► Chunking, retrieval, reranking
    │
    ├─► "ML/Data science project" ──────► ai-ml-data-science
    │                                      └─► EDA, modeling, evaluation
    │
    ├─► "Time series forecasting" ──────► ai-ml-timeseries
    │                                      └─► LightGBM, Transformers, validation
    │
    ├─► "MLOps / ML security" ──────────► ai-mlops
    │                                      └─► Deployment, drift, security
    │
    ├─► "Write prompts for Claude" ─────► ai-prompt-engineering
    │                                      └─► Templates, validation, patterns
    │
    ├─► "Build backend API" ────────────► software-backend
    │                                      └─► Node.js, Python, Go, Prisma
    │
    ├─► "Build frontend app" ───────────► software-frontend
    │                                      └─► Next.js, React, Tailwind
    │
    ├─► "Build mobile app" ─────────────► software-mobile
    │                                      └─► Swift, Kotlin, React Native
    │
    ├─► "Design system architecture" ───► software-architecture-design
    │                                      └─► Microservices, CQRS, scaling
    │
    ├─► "Clean code standard" ──────────► software-clean-code-standard
    │                                      └─► CC-* rule IDs, governance, language overlays
    │
    ├─► "Web3 / blockchain" ────────────► software-crypto-web3
    │                                      └─► Solidity, Rust, smart contracts
    │
    ├─► "Security / OWASP" ─────────────► software-security-appsec
    │                                      └─► Auth, input validation, crypto
    │
    ├─► "Add i18n / localization" ─────► software-localisation
    │                                      └─► i18next, ICU, RTL, TMS
    │
    ├─► "Design REST/GraphQL API" ──────► dev-api-design
    │                                      └─► OpenAPI, versioning, errors
    │
    ├─► "Manage dependencies" ──────────► dev-dependency-management
    │                                      └─► npm, pip, cargo, security
    │
    ├─► "Plan implementation" ──────────► dev-workflow-planning
    │                                      └─► /brainstorm, /write-plan
    │
    ├─► "Build data pipeline" ──────────► data-lake-platform
    │                                      └─► dlt, SQLMesh, Iceberg, DuckDB
    │
    ├─► "Analytics engineering" ─────────► data-analytics-engineering
    │                                      └─► dbt, metrics, semantic layer
    │
    ├─► "Optimize SQL queries" ─────────► data-sql-optimization
    │                                      └─► EXPLAIN, indexing, tuning
    │
    ├─► "Create Claude Code agent" ─────► claude-code-agents
    │                                      └─► YAML frontmatter, tools
    │
    ├─► "Create slash command" ─────────► claude-code-commands
    │                                      └─► $ARGUMENTS, templates
    │
    ├─► "Create hook automation" ───────► claude-code-hooks
    │                                      └─► PreToolUse, PostToolUse, Stop
    │
    ├─► "Setup MCP server" ─────────────► claude-code-mcp
    │                                      └─► Database, filesystem, APIs
    │
    ├─► "Configure CLAUDE.md" ──────────► claude-code-project-memory
    │                                      └─► Project context, standards
    │
    ├─► "Create skill" ─────────────────► claude-code-skills
    │                                      └─► Progressive disclosure, resources/
    │
    └─► "Full technical design" ────────► COMPREHENSIVE ANALYSIS
                                           └─► Architecture + implementation plan
```

---

## Domain Detection

### Domain 1: AI/ML ENGINEERING

**Triggers**: "AI", "ML", "LLM", "agent", "model", "train", "fine-tune", "RAG", "embedding", "inference", "prompt"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `ai-agents` | Multi-agent systems, MCP, orchestration |
| `ai-llm` | Fine-tuning, PEFT, LoRA, evaluation |
| `ai-llm-inference` | vLLM, quantization, serving optimization |
| `ai-rag` | Retrieval-augmented generation, search |
| `ai-ml-data-science` | EDA, feature engineering, modeling |
| `ai-ml-timeseries` | Forecasting, temporal validation |
| `ai-mlops` | Deployment, monitoring, security |
| `ai-prompt-engineering` | Prompt design, templates |

**Skill Chain - Build AI Agent**:
```
Requirements → ai-agents (architecture) → ai-rag (if retrieval needed)
    → ai-prompt-engineering (prompts) → ai-mlops (deployment)
```

### Domain 2: SOFTWARE DEVELOPMENT

**Triggers**: "build", "implement", "code", "frontend", "backend", "mobile", "API", "database"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `software-backend` | REST APIs, databases, auth, Node/Python/Go |
| `software-frontend` | Next.js, React, TypeScript, Tailwind |
| `software-mobile` | iOS (Swift), Android (Kotlin), React Native |
| `software-architecture-design` | System design, microservices, scaling |
| `software-crypto-web3` | Blockchain, smart contracts, DeFi |
| `software-security-appsec` | OWASP, auth, input validation |
| `software-code-review` | Review patterns, checklists |
| `software-ui-ux-design` | UI patterns, accessibility |
| `software-ux-research` | User research, gap analysis |
| `software-localisation` | i18n, l10n, translation workflows |

**Skill Chain - Full-Stack App**:
```
Requirements → software-architecture-design → software-backend (API)
    → software-frontend (UI) → software-security-appsec (security audit)
```

### Domain 3: DATA ENGINEERING

**Triggers**: "data pipeline", "ETL", "lakehouse", "SQL", "query optimization", "data warehouse", "metrics", "semantic layer", "dbt", "analytics engineering"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `data-lake-platform` | Pipelines, Iceberg, DuckDB, dlt |
| `data-analytics-engineering` | Metrics, semantic layer, dimensional models |
| `data-sql-optimization` | Query tuning, indexes, EXPLAIN |

**Skill Chain - Data Platform**:
```
Requirements → data-lake-platform (ingestion + storage)
    → data-analytics-engineering (models + metrics)
    → data-sql-optimization (query layer) → ai-ml-data-science (analytics)
```

### Domain 4: API & INTEGRATION

**Triggers**: "REST", "GraphQL", "gRPC", "OpenAPI", "API design", "versioning"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `dev-api-design` | API design, OpenAPI, versioning |
| `software-backend` | Implementation |
| `dev-dependency-management` | Package management, security |

**Skill Chain - API Development**:
```
dev-api-design (spec) → software-backend (implement)
    → dev-dependency-management (dependencies) → qa-testing-strategy (tests)
```

### Domain 5: CLAUDE CODE FRAMEWORK

**Triggers**: "Claude Code", "agent", "skill", "command", "hook", "MCP", "CLAUDE.md"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `claude-code-agents` | Create agents with frontmatter |
| `claude-code-commands` | Slash commands with $ARGUMENTS |
| `claude-code-hooks` | Event automation (Pre/PostToolUse) |
| `claude-code-mcp` | External data connections |
| `claude-code-project-memory` | CLAUDE.md configuration |
| `claude-code-skills` | Progressive disclosure skills |

**Skill Chain - Full Claude Code Setup**:
```
claude-code-project-memory (CLAUDE.md) → claude-code-skills (knowledge)
    → claude-code-agents (subagents) → claude-code-commands (shortcuts)
    → claude-code-hooks (automation) → claude-code-mcp (external data)
```

---

## Skill Registry

### AI/ML Skills (8)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `ai-agents` | Multi-agent systems | Architecture, MCP config, guardrails |
| `ai-llm` | LLM development | Fine-tuning config, evaluation |
| `ai-llm-inference` | Inference optimization | vLLM config, quantization |
| `ai-rag` | RAG systems | Chunking strategy, retrieval pipeline |
| `ai-ml-data-science` | Data science | EDA, models, evaluation |
| `ai-ml-timeseries` | Time series | Forecasting models, validation |
| `ai-mlops` | ML operations | Deployment, monitoring |
| `ai-prompt-engineering` | Prompt design | Templates, validation |

### Software Skills (10)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `software-backend` | Backend development | APIs, database, auth |
| `software-frontend` | Frontend development | Components, state, routing |
| `software-mobile` | Mobile development | iOS, Android, cross-platform |
| `software-architecture-design` | System design | Architecture diagrams, decisions |
| `software-crypto-web3` | Blockchain | Smart contracts, DeFi |
| `software-security-appsec` | Security | OWASP compliance, auth |
| `software-code-review` | Code review | Review checklists |
| `software-ui-ux-design` | UI/UX design | Design systems, accessibility |
| `software-ux-research` | UX research | User research, benchmarks |
| `software-localisation` | i18n/l10n | i18next, ICU, RTL, TMS workflows |

### Data Skills (3)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `data-lake-platform` | Data pipelines | Ingestion, transformation, storage |
| `data-analytics-engineering` | Analytics engineering | dbt, metrics, semantic layer |
| `data-sql-optimization` | SQL tuning | Query optimization, indexes |

### Development Workflow (3)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `dev-api-design` | API design | OpenAPI specs, contracts |
| `dev-dependency-management` | Dependencies | Lockfiles, security |
| `dev-workflow-planning` | Planning | Implementation plans |

### Claude Code Framework (6)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `claude-code-agents` | Agent creation | Agent YAML, tools config |
| `claude-code-commands` | Commands | Slash command templates |
| `claude-code-hooks` | Hooks | Event automation scripts |
| `claude-code-mcp` | MCP servers | Database/API connections |
| `claude-code-project-memory` | CLAUDE.md | Project configuration |
| `claude-code-skills` | Skills | Progressive disclosure docs |

---

## Routing Logic

### Keyword-Based Routing

```
KEYWORDS -> SKILL MAPPING

"agent", "multi-agent", "MCP", "guardrails" -> ai-agents
"fine-tune", "LoRA", "PEFT", "train model" -> ai-llm
"vLLM", "inference", "quantization", "serving" -> ai-llm-inference
"RAG", "retrieval", "embedding", "vector" -> ai-rag
"EDA", "feature engineering", "modeling" -> ai-ml-data-science
"time series", "forecast", "temporal" -> ai-ml-timeseries
"MLOps", "model deployment", "drift" -> ai-mlops
"prompt", "template", "instruction" -> ai-prompt-engineering

"backend", "API", "Node.js", "FastAPI", "Prisma" -> software-backend
"frontend", "Next.js", "React", "Tailwind" -> software-frontend
"mobile", "iOS", "Android", "Swift", "Kotlin" -> software-mobile
"architecture", "microservices", "CQRS" -> software-architecture-design
"blockchain", "Solidity", "Web3", "smart contract" -> software-crypto-web3
"security", "OWASP", "auth", "vulnerability" -> software-security-appsec
"code review", "review checklist" -> software-code-review
"UI", "design system", "accessibility" -> software-ui-ux-design
"UX research", "user research", "JTBD" -> software-ux-research
"i18n", "l10n", "localization", "translation", "RTL", "ICU" -> software-localisation

"data pipeline", "ETL", "lakehouse", "dlt" -> data-lake-platform
"SQL optimization", "query tuning", "EXPLAIN" -> data-sql-optimization

"REST API", "GraphQL", "OpenAPI", "gRPC" -> dev-api-design
"npm", "pip", "cargo", "dependencies" -> dev-dependency-management
"plan", "brainstorm", "implementation" -> dev-workflow-planning

"Claude Code agent", "subagent" -> claude-code-agents
"slash command", "$ARGUMENTS" -> claude-code-commands
"hook", "PreToolUse", "PostToolUse" -> claude-code-hooks
"MCP server", "database connection" -> claude-code-mcp
"CLAUDE.md", "project memory" -> claude-code-project-memory
"skill", "progressive disclosure" -> claude-code-skills
```

### Context-Based Routing

| User Context | Primary Skill | Supporting Skills |
|--------------|---------------|-------------------|
| Building AI app | `ai-agents` | `ai-rag`, `ai-prompt-engineering` |
| Optimizing LLM | `ai-llm-inference` | `ai-mlops` |
| Full-stack app | `software-architecture-design` | `software-backend`, `software-frontend` |
| Mobile app | `software-mobile` | `software-backend`, `software-ui-ux-design` |
| Data platform | `data-lake-platform` | `data-sql-optimization`, `ai-ml-data-science` |
| API development | `dev-api-design` | `software-backend`, `software-security-appsec` |
| Claude Code setup | `claude-code-project-memory` | All claude-code-* skills |

---

## Skill Chain Patterns

### Pattern 1: AI Agent Development

```
START
  │
  ▼
ai-agents ──────────────────► Agent Architecture
  │
  ▼
ai-rag (if retrieval) ──────► Retrieval Pipeline
  │
  ▼
ai-prompt-engineering ──────► Prompt Templates
  │
  ▼
ai-mlops ───────────────────► Deployment Config
  │
  ▼
agent-fleet-operations ─────► Service Design
  │
  ▼
PRODUCTION AGENT
```

### Pattern 2: Full-Stack Application

```
START
  │
  ▼
software-architecture-design ► System Design
  │
  ├──────────────────────────────────────────┐
  ▼                                          ▼
software-backend ──► API         software-frontend ──► UI
  │                                          │
  └────────────────────┬─────────────────────┘
                       ▼
         software-security-appsec ──► Security Audit
                       │
                       ▼
                  DEPLOYED APP
```

### Pattern 3: Data Platform

```
START
  │
  ▼
data-lake-platform ─────────► Ingestion + Storage
  │
  ▼
data-sql-optimization ──────► Query Layer
  │
  ▼
ai-ml-data-science ─────────► Analytics
  │
  ▼
software-frontend ──────────► Dashboard
  │
  ▼
DATA PLATFORM LIVE
```

### Pattern 4: Claude Code Framework Setup

```
START
  │
  ▼
claude-code-project-memory ─► CLAUDE.md
  │
  ▼
claude-code-skills ─────────► Domain Knowledge
  │
  ▼
claude-code-agents ─────────► Specialized Agents
  │
  ▼
claude-code-commands ───────► User Shortcuts
  │
  ▼
claude-code-hooks ──────────► Automation
  │
  ▼
claude-code-mcp ────────────► External Data
  │
  ▼
COMPLETE CLAUDE CODE SETUP
```

---

## Comprehensive Analysis Mode

For full technical analysis, invoke skills in parallel:

### Layer 1: Requirements & Design (Parallel)

| Skill | Output | Purpose |
|-------|--------|---------|
| `software-architecture-design` | System design | Architecture decisions |
| `dev-api-design` | API contracts | Interface design |
| `software-ui-ux-design` | UI patterns | User interface |

### Layer 2: Implementation (Based on Stack)

| Stack | Primary Skills |
|-------|----------------|
| AI/ML | `ai-agents`, `ai-rag`, `ai-llm` |
| Full-stack | `software-backend`, `software-frontend` |
| Mobile | `software-mobile`, `software-backend` |
| Data | `data-lake-platform`, `data-sql-optimization` |

### Layer 3: Quality & Security

| Skill | Purpose |
|-------|---------|
| `software-security-appsec` | Security audit |
| `software-code-review` | Code quality |
| Route to → `router-operations` | Testing, deployment |

---

## Cross-Router Handoffs

### To router-startup

When user shifts to business concerns:
- "How should I price this?" → `startup-business-models`
- "Who are competitors?" → `startup-competitive-analysis`
- "Go to market strategy?" → `startup-go-to-market`

### To router-operations

When user shifts to operations:
- "How do I test this?" → `qa-testing-strategy`
- "Deploy to production" → `ops-devops-platform`
- "Monitor performance" → `qa-observability`

### From router-startup

When router-startup detects technical needs:
- "Build the MVP" → Route here for implementation
- "Technical architecture" → Route here for design

---

## Output Templates

### Quick Analysis Output

```markdown
## Technical Analysis: {{TOPIC}}

**Domain Detected**: {{DOMAIN}}
**Primary Skill**: {{SKILL}}
**Supporting Skills**: {{LIST}}

### Recommended Approach
1. {{STEP_1}} - Use {{SKILL}}
2. {{STEP_2}} - Use {{SKILL}}
3. {{STEP_3}} - Use {{SKILL}}

### Key Considerations
- {{CONSIDERATION_1}}
- {{CONSIDERATION_2}}

### Skills to Invoke
- {{SKILL_1}}: {{WHY}}
- {{SKILL_2}}: {{WHY}}
```

---

## Resources

| Resource | Purpose |
|----------|---------|
| `resources/routing-logic.md` | Detailed routing rules |
| `resources/skill-chain-patterns.md` | Implementation patterns |
| `resources/technology-selection.md` | Stack recommendations |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/technical-analysis-report.md` | Full analysis |
| `templates/architecture-decision.md` | ADR template |
| `templates/implementation-plan.md` | Implementation planning |

## Data

| File | Purpose |
|------|---------|
| `data/skill-registry.json` | Engineering skills index |
| `data/sources.json` | Reference sources |
