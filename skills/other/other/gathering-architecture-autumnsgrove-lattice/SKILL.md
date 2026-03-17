---
name: gathering-architecture
description: The drum sounds. Eagle, Crow, Swan, and Elephant gather for system architecture. Use when designing major systems from vision to implementation.
---

# Gathering Architecture 🌲🦅

The drum echoes high in the canopy. The Eagle soars above, seeing the forest's patterns. The Crow perches nearby, tilting its head at what others won't question. The Swan glides across the lake, elegant designs taking form. The Elephant moves below, building what was envisioned. Together they transform a clearing into a cathedral of code—systems that stand for seasons.

## When to Summon

- Designing new systems or services
- Major architectural decisions
- Refactoring core infrastructure
- Creating platforms that other features build upon
- When vision, design, and implementation must align

---

## Grove Tools for This Gathering

Use `gw` and `gf` throughout. Quick reference for architecture work:

```bash
# Orientation — understand the project before designing
gw context

# Explore the existing architecture
gf --agent search "pattern"         # Find code patterns
gf --agent class "ServiceName"      # Find class/component definitions
gf --agent routes                   # Map route structure

# Understand dependencies and change impact
gf --agent deps                     # Dependency graph
gf --agent impact "module"          # Blast radius of changes
```

---

## The Gathering

```
SUMMON → ORGANIZE → EXECUTE → VALIDATE → COMPLETE
   ↓         ↲          ↲          ↲          ↓
Receive  Dispatch   Animals    Verify   Architecture
Request  Animals    Work       Design   Defined
```

### Animals Mobilized

1. **🦅 Eagle** — Design system architecture from 10,000 feet
2. **🐦‍⬛ Crow** — Challenge the design before it's cast in code
3. **🦢 Swan** — Write detailed technical specifications
4. **🐘 Elephant** — Implement the architectural foundation

---

### Phase 1: SUMMON

_The drum sounds. The canopy rustles..._

Receive and parse the request:

**Clarify the System:**

- What problem does this solve?
- What are the scale requirements?
- What are the constraints?
- What's the growth trajectory?

**Nature Metaphor:**

> "Every architecture needs a nature metaphor. What does this system resemble?
>
> - Heartwood (core that holds everything)
> - Wisp (gentle guiding light)
> - Porch (place to gather and talk)
> - Something else?"

**Confirm:**

> "I'll mobilize an architecture gathering for: **[system description]**
>
> This will involve:
>
> - 🦅 Eagle designing the high-level architecture
> - 🐦‍⬛ Crow challenging the design before it's cast in spec
> - 🦢 Swan writing the detailed specification
> - 🐘 Elephant implementing the foundation
>
> Proceed with the gathering?"

---

### Phase 2: ORGANIZE

_The birds circle. The elephant waits below..._

Dispatch in sequence:

**Dispatch Order:**

```
Eagle ──→ Crow ──→ Swan ──→ Elephant
  │         │        │           │
  │         │        │           │
Design   Challenge  Write      Build
System   Design    Spec       Foundation
```

**Dependencies:**

- Eagle must complete before Crow (needs architecture to challenge)
- Crow must complete before Swan (design strengthened before specifying)
- Swan must complete before Elephant (needs detailed spec)

---

### Phase 3: EXECUTE

_The architecture takes form from sky to earth..._

Execute each phase by loading and running each animal's dedicated skill:

---

**🦅 EAGLE — DESIGN**

Load skill: `eagle-architect`

Execute the full Eagle workflow focused on [the system being designed].
Handoff: architecture overview (system boundaries, component interactions, technology choices, scale constraints, nature metaphor, ADRs) → Swan for specification

---

**🐦‍⬛ CROW — CHALLENGE**

Load skill: `crow-reason`

Execute the Crow in Red Team mode against the Eagle's architecture overview. Challenge assumptions, find weak points, stress-test boundaries. The Crow's Roost summary feeds into the Swan — design decisions are strengthened before they're cast in spec.
Handoff: strengthened architecture with Roost summary (challenges resolved, risks acknowledged) → Swan for specification

---

**🦢 SWAN — SPECIFY**

Load skill: `swan-design`

Execute the full Swan workflow using the Eagle's architecture overview, strengthened by the Crow's challenges.
Handoff: complete technical specification (API contracts, database schema, flow diagrams, implementation checklist) → Elephant for foundation building

---

**🐘 ELEPHANT — BUILD**

Load skill: `elephant-build`

Execute the full Elephant workflow using the Swan's technical specification as the build plan.
Handoff: working foundation (core infrastructure, base modules, API skeleton, database migrations, essential tests) → VALIDATE phase

---

### Phase 4: VALIDATE

_The structure stands. Each animal verifies their work..._

**Validation Checklist:**

- [ ] Eagle: Architecture addresses all requirements
- [ ] Crow: Design challenged and strengthened
- [ ] Swan: Specification is complete and implementable
- [ ] Elephant: Foundation is solid and tested

**Review Points:**

```
After Eagle:
  → Review architecture with stakeholders
  → Confirm boundaries and trade-offs
  → Approve before Crow challenges

After Crow:
  → Review Roost summary
  → Confirm which challenges are resolved vs accepted risks
  → Approve strengthened design before Swan begins

After Swan:
  → Review spec for completeness
  → Verify all sections present
  → Confirm implementation ready

After Elephant:
  → Test foundation thoroughly
  → Verify patterns established
  → Confirm next features can build upon it
```

---

### Phase 5: COMPLETE

_The gathering ends. Architecture stands ready..._

**Completion Report:**

```markdown
## 🌲 GATHERING ARCHITECTURE COMPLETE

### System: [Name]

### Animals Mobilized

🦅 Eagle → 🐦‍⬛ Crow → 🦢 Swan → 🐘 Elephant

### Architecture Decisions

- **Pattern:** [e.g., Event-driven microservices]
- **Scale Target:** [e.g., 10k concurrent users]
- **Key Trade-offs:** [summary]

### Artifacts Created

- Architecture Overview (`docs/architecture/[system].md`)
- Technical Specification (`docs/specs/[system]-spec.md`)
- ADRs ([list])
- Foundation Code ([location])
- Base Tests ([location])

### Ready for

- Feature development on this foundation
- Team onboarding using the spec
- Future architecture reviews

### Time Elapsed

[Duration]

_The forest has a new landmark._ 🌲
```

---

## Example Gathering

**User:** "/gathering-architecture Design the notification system"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing for: Notification system. Send email, push, SMS to users. Scale: millions of notifications/day."

2. 🌲 **ORGANIZE** — "Sequence: Eagle (architecture) → Crow (challenge) → Swan (spec) → Elephant (foundation)"

3. 🌲 **EXECUTE** —
   - 🦅 Eagle: "Event-driven: App emits events → Queue → Workers → Providers. Scales horizontally."
   - 🐦‍⬛ Crow: "Red Team mode. Challenged: operational complexity for small team, eventual consistency with account deletion, microservice gravity. Strengthened: modular monolith with clean service boundary, extract later."
   - 🦢 Swan: "Complete spec incorporating Crow's strengthened position, with flow diagrams, API contracts, provider adapter interface"
   - 🐘 Elephant: "Event bus, queue infrastructure, base notification service, database schema"

4. 🌲 **VALIDATE** — "Architecture handles scale, spec complete, foundation tested"

5. 🌲 **COMPLETE** — "Notification platform ready for feature development"

---

_From vision to foundation, the forest grows._ 🌲
