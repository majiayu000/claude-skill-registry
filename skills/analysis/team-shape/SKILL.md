---
name: team-shape
description: "Assess team structure against Skelton's Team Topologies. Evaluate cognitive load, interaction modes, and Conway's Law alignment."
instruction_budget: 26
---

# Team Shape Assessment

Evaluate organizational design for fast flow. Source: Skelton & Pais (Team Topologies).

## Assessment Workflow

### 1. Map Current Teams
For each team, classify:
- **Stream-aligned**: Owns a user journey or business domain (most teams should be this)
- **Enabling**: Helps other teams acquire capabilities (temporary engagement)
- **Complicated subsystem**: Deep specialist knowledge (only when cognitive load justifies)
- **Platform**: Internal product that reduces cognitive load for stream-aligned teams

### 2. Evaluate Cognitive Load
For each team, assess:
- **Intrinsic load**: Problem complexity (can't reduce, only manage)
- **Extraneous load**: Bad tools/processes (SHOULD reduce -- platform teams help here)
- **Germane load**: Learning new relevant things (encourage)
- If team is overloaded: shrink domain, move complexity to platform, or split

### 3. Audit Interaction Modes
Between each pair of collaborating teams:
- **Collaboration**: Working closely together (time-box this -- it's expensive)
- **X-as-a-Service**: Consuming/providing via API (ideal steady state)
- **Facilitating**: Helping another team learn (enabling teams do this)

### 4. Conway's Law Check

Conway's Law (1968): "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's **communication** structure." Note: it's communication structures, not org chart hierarchy — two teams in the same org with poor communication will still produce fragmented systems.

**Inverse Conway Maneuver** (James Lewis, popularized by Skelton & Pais): Deliberately design team communication structures to match the desired system architecture, rather than letting architecture drift to match existing teams.

- Does architecture mirror team structure intentionally?
- Do team boundaries align with security boundaries?
- Do team APIs match system APIs?
- If architecture doesn't match team structure: is the mismatch intentional or a Conway's Law drift?

### 4b. Fracture Planes (Skelton & Pais)

When a team's cognitive load exceeds capacity, use fracture planes to identify the cleanest split point. The fracture plane that aligns with the most criteria wins:

| Fracture Plane | Description |
|---|---|
| Business domain | DDD bounded context boundary |
| Regulatory compliance | Different compliance requirements = different teams |
| Change cadence | Fast-moving vs stable components |
| Team location | Co-located vs distributed |
| Technology | Different tech stacks |
| User personas | Different user segments |
| Risk | High-risk vs low-risk components |
| Performance isolation | Components with different scaling/latency requirements |

*Source: Skelton & Pais (Team Topologies, Chapter 6)*

### 5. Recommendations
- Teams without clear type -> needs redesign
- Collaboration lasting > 1 quarter -> should evolve to X-as-a-Service
- Stream-aligned team with > 2 cross-team dependencies -> architecture needs decoupling
- Cognitive load exceeding capacity -> use fracture planes to identify split point

### 5. Bounded Context Alignment (DDD)
If the product has multiple domains or services:
- Are bounded contexts identified? (Check canvas/bounded-contexts.yml)
- Does each stream-aligned team own a coherent bounded context?
- If a context is split across teams: handoff friction. Fix team boundaries.
- If a team owns unrelated contexts: cognitive overload. Split the team or contexts.
- Context map relationships should match team interaction modes:
  Partnership = Collaboration, Customer-Supplier = X-as-a-Service, ACL = translation layer
*Source: Evans (DDD), "Architecture for Flow" (DDD + Wardley + Team Topologies)*

### 6. Capability Gap Diagnosis (DASA)
When DORA metrics indicate capability gaps, use the DASA DevOps Competency Framework's 12 skill areas to identify which team skills need development (e.g., courage, teambuilding, continuous improvement, business value optimization).

## Bounded Agency (Skelton, 2025-2026)

Skelton's "Infrastructure for Agency" framing describes how organizations should provide **boundaries that enable autonomy** rather than control that restricts it. Mycelium implements bounded agency for AI agents using the same structural principles:

| Skelton concept | Mycelium mechanism |
|---|---|
| Boundaries that enable | Guardrails (BLOCK/REVIEW/NUDGE — constrain without micromanaging) |
| Shared state | Canvas (single source of truth all agents read/write) |
| Stable interfaces | Theory gates (predictable checkpoints with explicit pass/fail) |
| Aligned domains | Diamonds (scoped units of work with clear ownership) |
| Bounded workers | Fan-out agents (isolated worktrees, scoped mandate, report back) |

Agency without boundaries produces chaos; boundaries without agency produces bureaucracy. The target is the middle.

*Source: Skelton (Infrastructure for Agency, 2025-2026)*

## Output

- Update `canvas/team-shape.yml` and `canvas/bounded-contexts.yml` with assessment results.
- **APPEND** a `### Team Shape Assessment` entry to `harness/decision-log.md` with: team types identified, cognitive load findings, Conway alignment, recommendations. (MANDATORY per G-P4)
