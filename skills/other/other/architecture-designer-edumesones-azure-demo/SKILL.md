---
name: architecture-designer
description: Define technical architecture and create ADRs. Triggers on "Help me define the architecture", "Define architecture", "Let's design the architecture".
globs: ["docs/architecture/**", "docs/decisions/**", "docs/project.md"]
---

# Architecture Designer (Fase 0)

Transform project requirements into concrete architectural decisions with proper ADR documentation.

## Triggers

- "Help me define the architecture"
- "Define architecture"
- "Let's design the architecture"
- "Help me with technical architecture"
- `/architecture`

## Prerequisites

- `docs/project.md` should exist with project definition
- If not exists, suggest: "Let's first interview about the project"

## Purpose

Create:
1. **Architecture overview** in `docs/architecture/_index.md`
2. **ADRs** (Architecture Decision Records) in `docs/decisions/`
3. **Technical foundation** for feature development

## Process

### 1. Read Project Context

```bash
# Read project definition
cat docs/project.md

# Check existing architecture docs
ls -la docs/architecture/ 2>/dev/null
ls -la docs/decisions/ 2>/dev/null
```

### 2. Identify Key Decisions

Based on project.md, identify decisions needed:

| Category | Typical Decisions |
|----------|-------------------|
| **Language/Runtime** | Python, Node, Go, Rust |
| **Framework** | FastAPI, Django, Express, Next.js |
| **Database** | PostgreSQL, MongoDB, SQLite, Redis |
| **Authentication** | JWT, OAuth, Session, API Keys |
| **Hosting** | AWS, GCP, Azure, Vercel, Self-hosted |
| **API Style** | REST, GraphQL, gRPC |
| **Frontend** | React, Vue, Gradio, CLI |
| **Caching** | Redis, Memcached, In-memory |
| **Queue/Async** | Celery, RQ, SQS, None |
| **Monitoring** | CloudWatch, Datadog, Prometheus |

### 3. Interview for Each Decision

For each major decision, ask:

```
"For [CATEGORY], I see a few options:

A) [Option A] - [Pros: X, Y] [Cons: Z]
B) [Option B] - [Pros: X, Y] [Cons: Z]
C) [Option C] - [Pros: X, Y] [Cons: Z]

Based on your project (MVP timeline, team size, scale needs),
I'd recommend [X] because [reason].

What's your preference?"
```

### 4. Create ADRs

For each decision, create `docs/decisions/ADR-NNN-title.md`

### 5. Create Architecture Overview

Update `docs/architecture/_index.md` with:
- System diagram
- Tech stack table linking to ADRs
- Project structure
- Key patterns

### 6. Interview Rules

```
ARCHITECTURE INTERVIEW RULES

1. Always provide options with trade-offs
   Never ask "what database?" - ask "PostgreSQL or MongoDB? Here's why..."

2. Make recommendations based on project context
   "Given your MVP timeline, I recommend X"

3. Create ADR immediately after each decision
   Don't wait until the end

4. Challenge over-engineering
   "Do you really need Kubernetes for MVP? ECS is simpler."

5. Document the WHY, not just the WHAT
   Future you will thank present you
```

### 7. Completion Check

Before ending, verify:
- [ ] All major categories have decisions
- [ ] Each decision has an ADR
- [ ] Architecture overview exists
- [ ] Project structure is defined
- [ ] No conflicting decisions

### 8. Handoff

When complete:

```
Architecture defined. Created:
- docs/architecture/_index.md (overview)
- docs/decisions/ADR-001-*.md through ADR-00N-*.md

Next step:
"Define MVP features" -> Creates feature folders ready for implementation

Or: "Let's start with the first feature"
```
