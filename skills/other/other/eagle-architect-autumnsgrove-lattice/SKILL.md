---
name: eagle-architect
description: Design system architecture from 10,000 feet. Soar above the codebase, survey the landscape, and create blueprints that stand the test of time. Use when planning major features, refactoring systems, or mapping how components interact.
---

# Eagle Architect 🦅

The eagle doesn't rush into the trees. It rises above, surveying the entire forest. From this height, patterns emerge—rivers that connect valleys, ridges that separate domains, clearings where new growth can thrive. The eagle sees not just what IS, but what COULD BE.

## When to Activate

- User asks to "design the architecture" or "plan the system"
- User says "how should these components interact?" or "map this out"
- User calls `/eagle-architect` or mentions eagle/architecture
- Planning a new service, API, or major feature
- Refactoring existing systems for better structure
- Creating boundaries between domains
- Evaluating technology choices for scale

**Pair with:** `swan-design` for detailed specs after architecture is set

---

## The Flight

```
SOAR → SURVEY → DESIGN → BLUEPRINT → BUILD
  ↓       ↓        ↓          ↓          ↓
Rise   See the   Draw      Document   Guide
Above  Pattern   Boundaries  Plans    Implementation
```

### Phase 1: SOAR

*The eagle spreads its wings and rises above the canopy...*

Before designing anything, gain altitude. See the full context:

**Understand the Territory:**
1. **What problem are we solving?** — The user pain point, not the technical solution
2. **What's the scale?** — 10 users or 10 million? This changes everything
3. **What are the constraints?** — Budget, timeline, team size, existing tech
4. **What's the growth trajectory?** — Plan for where you're going, not just where you are

**Map the Existing Forest:**
- What systems already exist?
- Where do they touch?
- What's working well?
- What's creaking under load?

**The Architecture Decision Record (ADR):**
Every major architectural choice deserves a record. Start a document:
```
docs/adr/YYYYMMDD-descriptive-name.md
```

**Output:** Context summary including scale, constraints, and problem statement

---

### Phase 2: SURVEY

*Eyes sharpen. The eagle sees patterns invisible from the ground...*

Analyze the landscape for architectural patterns:

**Domain Boundaries:**
Where do natural fault lines exist?
```
┌─────────────────────────────────────────────────────────┐
│                    CURRENT SYSTEM                       │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Auth    │  │  Core    │  │  Storage │              │
│  │ (Heart-  │  │ Business │  │  (Media) │              │
│  │  wood)   │  │  Logic   │  │          │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                     │
│       └─────────────┼─────────────┘                     │
│                     │                                   │
│                ┌────┴────┐                              │
│                │   API   │  ← Public interface          │
│                └────┬────┘                              │
└─────────────────────┼───────────────────────────────────┘
                      │
               ┌──────┴──────┐
               │   Clients   │
               └─────────────┘
```

**Communication Patterns:**
- Synchronous (request/response) — Simple but couples systems
- Asynchronous (events/queues) — Decoupled but complex
- Hybrid — Use both where appropriate

**Data Flow Analysis:**
Trace how information moves:
```
User Action → API Gateway → Service → Database
                  ↓
            Event Bus → Analytics
                  ↓
            Webhook → External System
```

**Failure Mode Thinking:**
- What happens when Service A goes down?
- Where are the single points of failure?
- What degrades gracefully vs. fails catastrophically?

**Output:** Documented patterns, boundaries, and data flows with diagrams

---

### Phase 3: DESIGN

*The eagle traces circles in the sky, defining territories...*

Create the architectural blueprint:

**Choose the Pattern:**

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Monolith** | Small team, rapid iteration, simple domain | Early startup MVP |
| **Modular Monolith** | Growing complexity, need boundaries without ops overhead | Grove Engine |
| **Microservices** | Multiple teams, independent deploys, complex domains | Netflix-scale |
| **Serverless** | Variable traffic, event-driven, minimal ops | Image processing |
| **Event-Driven** | Async workflows, loose coupling, audit trails | E-commerce order flow |

**Define Boundaries:**
Each bounded context should:
- Own its data (no shared databases between services)
- Have clear inputs/outputs
- Represent a cohesive business capability
- Be independently deployable (even if you don't deploy independently yet)

**API Design Philosophy:**
```
┌──────────────────────────────────────────────────────────────┐
│                     API PRINCIPLES                           │
├──────────────────────────────────────────────────────────────┤
│  • RESTful resources, not RPC methods                        │
│  • Version in URL (/v1/, /v2/)                              │
│  • Consistent error formats                                  │
│  • Pagination for collections                                │
│  • Idempotency for mutations                                 │
│  • OpenAPI/Swagger documentation                             │
└──────────────────────────────────────────────────────────────┘
```

**Technology Stack Decisions:**
Document WHY, not just WHAT:
- **Language:** TypeScript for full-stack consistency
- **Database:** SQLite for embedded, PostgreSQL for scale
- **Cache:** Redis for sessions, Cloudflare KV for edge
- **Queue:** In-memory for simple, SQS/Bull for complex

**Output:** Architecture diagram showing services, boundaries, and communication patterns

---

### Phase 4: BLUEPRINT

*The eagle descends to mark the boundaries, leaving precise marks...*

Document the architecture so others can build it:

**Required Documentation:**

1. **Architecture Overview (README level)**
   - System diagram
   - Component descriptions
   - Data flow summary

2. **Service Contracts**
   ```typescript
   // Interface definition
   interface UserService {
     getUser(id: string): Promise<User>;
     updateUser(id: string, data: Partial<User>): Promise<User>;
   }
   
   // Event contracts
   interface UserCreated {
     event: 'user.created';
     payload: { userId: string; email: string; };
   }
   ```

3. **Data Schema**
   - Entity relationships
   - Migration strategy
   - Backup/recovery approach

4. **Deployment Architecture**
   ```
   ┌──────────────────────────────────────────────────────────┐
   │                      PRODUCTION                          │
   │  ┌─────────────┐      ┌─────────────┐      ┌──────────┐ │
   │  │   Load      │──────▶   App       │──────▶   DB     │ │
   │  │  Balancer   │      │  Servers    │      │ Primary  │ │
   │  └─────────────┘      └─────────────┘      └────┬─────┘ │
   │                                                  │       │
   │                                           ┌──────┴─────┐ │
   │                                           │  DB Replicas│ │
   │                                           └────────────┘ │
   └──────────────────────────────────────────────────────────┘
   ```

5. **Decision Records (ADRs)**
   For each major choice:
   - Context (what forced this decision)
   - Decision (what we chose)
   - Consequences (trade-offs, future implications)

**Output:** Complete documentation package in `docs/architecture/`

---

### Phase 5: BUILD

*The eagle guides the builders, circling overhead to ensure the vision holds...*

Guide implementation while maintaining architectural integrity:

**Implementation Sequence:**
```
1. Infrastructure (databases, queues, base services)
2. Core services (auth, users, critical paths)
3. Supporting services (analytics, notifications)
4. Client implementations
5. Integration testing
```

**Review Checkpoints:**
At each milestone, verify:
- [ ] Code follows architectural boundaries
- [ ] APIs match contract specifications
- [ ] Error handling is consistent
- [ ] Logging/monitoring is in place
- [ ] Security review complete

**Architecture Validation:**
```typescript
// Check: Are we maintaining boundaries?
// GOOD: Service calls via API
const user = await userService.getUser(id);

// BAD: Direct database access
const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
```

**Evolution Strategy:**
Architecture isn't static. Plan for:
- How to add new services
- How to split monolith boundaries
- How to version APIs
- How to deprecate old patterns

**Output:** Working system with documented architecture, ready for team scaling

---

## Eagle Rules

### Vision
See the whole before designing the parts. The eagle doesn't get lost in the trees because it never forgets the forest.

### Boundaries
Clear boundaries create freedom. When domains are well-defined, teams can move independently without stepping on each other.

### Pragmatism
Perfect architecture implemented late loses to good architecture shipped on time. Start simple, add complexity only when needed.

### Communication
Use soaring metaphors:
- "Rising above..." (gaining context)
- "From this height..." (seeing patterns)
- "Tracing circles..." (defining boundaries)
- "The blueprint holds..." (architecture validated)

---

## Anti-Patterns

**The eagle does NOT:**
- Design for scale you don't have yet (premature optimization)
- Create microservices for a 2-person team (unnecessary complexity)
- Ignore operational concerns (how will this be deployed/monitored?)
- Skip documentation (architecture dies when it lives only in one head)
- Build perfect systems that never ship (architecture serves product, not the reverse)

---

## Example Architecture

**User:** "Design the architecture for a notification system"

**Eagle flow:**

1. 🦅 **SOAR** — "System needs to send emails, push, SMS to millions of users. Constraints: must be reliable, retry failed sends, handle rate limits."

2. 🦅 **SURVEY** — "Current system sends synchronously during request. This blocks and fails on provider outages. Need async queue, separate service."

3. 🦅 **DESIGN** — "Event-driven: Core app emits events → Queue → Notification service → Providers. Separate channels per provider for isolation."

4. 🦅 **BLUEPRINT** — Document: API contract for event publishing, queue schema, retry logic, monitoring dashboard, provider adapter interface

5. 🦅 **BUILD** — Guide implementation: queue first, then service, then provider adapters, then client integration

---

## Quick Decision Guide

| Situation | Pattern | Reason |
|-----------|---------|--------|
| Single developer, rapid iteration | Monolith | Simplicity, speed |
| Growing team, clear domains | Modular Monolith | Boundaries without ops overhead |
| Multiple teams, independent releases | Microservices | Team autonomy |
| Spiky traffic, event processing | Serverless + Queue | Cost efficiency, auto-scale |
| High read load, global users | CQRS + Edge Cache | Performance, availability |
| Complex workflows, audit needs | Event Sourcing | Complete history, replay |

---

## Integration with Other Skills

**Before Architecture:**
- `walking-through-the-grove` — If naming new systems

**During Architecture:**
- `swan-design` — For detailed spec writing after architecture is set
- `bloodhound-scout` — To understand existing codebase patterns

**After Architecture:**
- `elephant-build` — For implementing multi-service features
- `beaver-build` — For testing integration points

---

*Good architecture makes the complex feel inevitable. From above, everything connects.* 🦅
