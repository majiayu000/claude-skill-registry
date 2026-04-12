---
name: team-shape
description: "Assess team structure against Skelton's Team Topologies. Evaluate cognitive load, interaction modes, and Conway's Law alignment."
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
- Does architecture mirror team structure intentionally?
- Do team boundaries align with security boundaries?
- Do team APIs match system APIs?

### 5. Recommendations
- Teams without clear type -> needs redesign
- Collaboration lasting > 1 quarter -> should evolve to X-as-a-Service
- Stream-aligned team with > 2 cross-team dependencies -> architecture needs decoupling

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

Update canvas/team-shape.yml and canvas/bounded-contexts.yml with assessment results.
