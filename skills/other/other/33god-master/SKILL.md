---
name: 33god-master
description: >
  Root knowledge skill for the 33GOD ecosystem. Every agent in the organization
  should preload this skill. Provides the essential mental model: what 33GOD is,
  how it's structured, what the non-negotiable rules are, and where to go deeper.
  Use this skill as your foundation before any 33GOD work. For specific tasks,
  load the appropriate specialist skill referenced below.
---

# 33GOD — Master Skill

You work inside the **33GOD ecosystem**. This skill gives you the minimum viable understanding to operate effectively. Read it, internalize it, then go do your job.

## What 33GOD Is

33GOD is an **event-driven agentic pipeline** for orchestrating software development, knowledge management, and automated workflows. **Bloodbank Events are the absolute lifeblood** of the ecosystem—what sets 33GOD apart as the most powerful agentic pipeline.

**The Event-Driven Architecture Flow:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         33GOD EVENT FLOW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. HOLYFIELDS          2. BLOODBANK           3. CANDYSTORE                │
│      (Definition)   →    (Transport)     →     (Persistence)                │
│         │                   │                       │                        │
│         │    JSON Schemas   │   RabbitMQ          │   PostgreSQL             │
│         │    Type Bindings  │   bloodbank.        │   Permanent              │
│         │                   │   events.v1         │   History                │
│         │                   │                       │                        │
│         └───────────────────┼───────────────────────┘                        │
│                             │                                                │
│                             ▼                                                │
│   4. HOLOCENE ←──────────────────────── (Query API + WS Relay)              │
│      (Visibility)                                                            │
│         │                                                                    │
│         ▼                                                                    │
│   5. AGENT INBOX ←────────────────────── agent.{name}.inbox                 │
│         │                                                                    │
│         ▼                                                                    │
│   6. HEARTBEATROUTER ←────────────────── system.heartbeat.tick              │
│         │                    (every 60 seconds)                              │
│         ▼                                                                    │
│   7. AGENT ACTION ←───────────────────── OpenClaw hooks                     │
│         │                    (injected into session)                         │
│         ▼                                                                    │
│      Task Execution                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**The elevator pitch:** Events flow through Bloodbank (RabbitMQ). Agents react. Work gets done. Humans steer. Everything is observable via Holocene.

## The Architecture in 60 Seconds

**Events are Immutable Facts** — They are added, triggered, and consumed. Once emitted, they never change. This is the foundation of 33GOD's reliability.

**Commands are Mutable Requests** — They are fired to request state changes. They may be rejected or fail. Events record what happened; commands request what should happen.

**The Golden Rule:**
```
Holyfields (Schema) → Bloodbank (Event) → Candystore (History) → Holocene (View) → Agents (Action)
```

- **Holyfields** is the canonical schema registry — defines all events
- **Bloodbank** is the central nervous system — transports all events
- **Candystore** is the memory — persists all events to PostgreSQL
- **Holocene** is the eyes — displays events via API + WebSocket
- **HeartbeatRouter** is the pulse — drives agent orchestration every 60s
- **Agents** are the hands — consume events and take action

## The 6 Domains

| Domain | What It Owns | Key Components |
|--------|-------------|----------------|
| **Infrastructure** | Event bus, schemas, persistence | Bloodbank, Holyfields, Candystore, Candybar |
| **Agent Orchestration** | Agent protocols, routing, teams | Flume, Yi, AgentForge, Holocene |
| **Workspace Management** | Worktrees, project scaffolding | iMi, Zellij-Driver |
| **Meeting & Collaboration** | Meeting capture, analysis | TheBoard, TheBoardRoom |
| **Dashboards & Voice** | UI, dictation, visualization | Holocene, HeyMa |
| **Development Tools** | Code quality, scaffolding, task running | Jelmore, Degenerate, Perth |

## Non-Negotiable Rules

These are not suggestions. They are laws.

### 1. Bloodbank Events are Everything
Events are the absolute lifeblood of 33GOD. If it didn't emit an event, it didn't happen. No direct service-to-service calls—everything through Bloodbank.

### 2. Holyfields Defines the Law
All event schemas are defined in Holyfields. No inline Pydantic models in Bloodbank that don't have a corresponding Holyfields schema. If the schema doesn't exist, write it before writing the code.

### 3. Events are Immutable, Commands are Mutable
- **Events** (past tense): `agent.task.completed`, `worktree.merged` — facts that occurred
- **Commands** (imperative): `agent.task.complete`, `worktree.merge` — requests that may fail
- Events are appended, never modified. Commands are fired, may be rejected.

### 4. The Event Flow is Sacred
```
Holyfields (Definition) → Bloodbank (Transport) → Candystore (Persistence) → Holocene (Visibility) → Agents (Action)
```

### 5. Heartbeats Drive the System
`system.heartbeat.tick` fires every 60 seconds. Agents consume via `agent.{name}.inbox`. HeartbeatRouter processes and injects into agent sessions. This is how agents know to act.

### 6. Agent Name IS the Route
Event routing follows `agent.{name}.{action}`. No platform prefixes. The name is the identity and the address.
```
agent.cack.message.received    ✅
agent.lenoon.task.assigned     ✅
openclaw.agent.cack.message    ❌ NO platform prefixes
```

### 7. Schema-First
Holyfields defines contracts. Everything else generates from them. No inline Pydantic models in Bloodbank that don't have a corresponding Holyfields schema. If the schema doesn't exist, write it before writing the code.

### 8. GOD Docs Are the Contract
Every component and domain has a `GOD.md`. If reality has drifted from the doc, the doc is wrong and must be fixed **before** new work begins. Lead architects' #1 job is maintaining their domain's GOD doc.

Read the `god-docs` skill for the full GOD Doc system specification.

### 9. BMAD Everywhere
Every project must be initialized with `npx bmad-method install`. Must have `_bmad/` and `_bmad_output/`. No exceptions.

### 10. All Work Is Ticketed
No rogue commits. No "I'll create the ticket later." All tickets belong to an epic. All WIP is in the current sprint. Plane workspace: `lasertoast`.

### 11. One Compose, One Stack
Services discover each other by name on the Docker network. No host-port gymnastics. The `docker-compose.yml` at `~/code/33GOD/` is the single source of truth for the running stack.

## Key Locations

| What | Where |
|------|-------|
| **Monorepo root** | `~/code/33GOD/` |
| **System GOD doc** | `~/code/33GOD/docs/GOD.md` |
| **Domain GOD docs** | `~/code/33GOD/docs/domains/{domain}/GOD.md` |
| **Component GOD docs** | `~/code/33GOD/{component}/GOD.md` |
| **Docker Compose** | `~/code/33GOD/docker-compose.yml` |
| **Bloodbank API** | `http://localhost:8682` |
| **Holocene UI** | `http://holocene.delo.sh` |
| **Plane board** | Workspace `lasertoast` |

## How to Work on 33GOD

1. **Before touching anything**: Read the system GOD doc and the relevant component/domain GOD doc
2. **Check Plane**: Is there a ticket? If not, create one
3. **Use iMi worktrees**: All work happens in managed worktrees (see specialist skill)
4. **Commit with accountability**: Every commit traces back to a ticket
5. **Update the GOD doc**: If your work changed the architecture, update the doc. This is not optional.

## Chain of Command

Technical decisions flow through the org chart. Don't skip levels.

```
Jarad (CEO) → Cack (CTO) → Grolf (Dir of Eng) → Domain Leads (Lenoon, etc.)
```

- **Cack** relays priorities from Jarad, coordinates across all efforts
- **Grolf** owns all cross-domain technical decisions
- **Domain leads** (e.g., Lenoon for Infrastructure) own their domain's architecture and GOD docs
- **If you have a technical question**: ask your lead, not Jarad

## Specialist Skills (Load When Needed)

These skills go deeper on specific workflows. Load the right one for your task:

| Skill | When to Load |
|-------|-------------|
| `god-docs` | Creating, auditing, or maintaining GOD Docs |
| `33god-creating-and-working-with-projects` | Starting a new project, creating worktrees, task execution |
| `33god-development-lifecycle` | Cross-component coordination, platform-wide status, BMAD orchestration |
| `33god-service-development` | Building new microservices, event consumers, FastStream handlers |
| `33god-workflow-generator` | Generating workflow implementations from descriptions |

## Quick Reference: Event Conventions

- **Exchange**: `bloodbank.events.v1` (TOPIC)
- **Agent events**: `agent.{name}.{action}` (e.g., `agent.cack.task.completed`)
- **Webhook events**: `webhook.{source}.{action}` (e.g., `webhook.plane.issue.updated`)
- **System events**: `system.{component}.{action}` (e.g., `system.bloodbank.health.check`)

## Quick Reference: Tech Stack

- **Python**: uv for package management, FastStream for consumers, FastAPI for HTTP
- **Node/TypeScript**: bun preferred, pnpm acceptable
- **Infrastructure**: Docker Compose, RabbitMQ, Redis, Traefik
- **Task running**: mise (not make, not npm scripts)
- **Secrets**: 1Password CLI (`op`) — never hardcode credentials

---

*This is your foundation. The GOD docs are the living truth. When in doubt, read the GOD doc. When the GOD doc is wrong, fix it. That's the 33GOD way.*
