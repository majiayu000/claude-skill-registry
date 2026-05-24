---
name: ghe-design
description: Reference material for Athena when writing requirements. NOT a template - Athena writes requirements freely based on the domain. This skill provides guidance patterns that may be useful, not constraints to follow.
---

## IRON LAW: User Specifications Are Sacred

**THIS LAW IS ABSOLUTE AND ADMITS NO EXCEPTIONS.**

1. **Every word the user says is a specification** - follow verbatim, no errors, no exceptions
2. **Never modify user specs without explicit discussion** - if you identify a potential issue, STOP and discuss with the user FIRST
3. **Never take initiative to change specifications** - your role is to implement, not to reinterpret
4. **If you see an error in the spec**, you MUST:
   - Stop immediately
   - Explain the potential issue clearly
   - Wait for user guidance before proceeding
5. **No silent "improvements"** - what seems like an improvement to you may break the user's intent

**Violation of this law invalidates all work produced.**

## Background Agent Boundaries

When running as a background agent, you may ONLY write to:
- The project directory and its subdirectories
- The parent directory (for sub-git projects)
- ~/.claude (for plugin/settings fixes)
- /tmp

Do NOT write outside these locations.

---

## GHE_REPORTS Rule (MANDATORY)

**ALL reports MUST be posted to BOTH locations:**
1. **GitHub Issue Thread** - Full report text (NOT just a link!)
2. **GHE_REPORTS/** - Same full report text (FLAT structure, no subfolders!)

**Report naming:** `<TIMESTAMP>_<title or description>_(<AGENT>).md`
**Timestamp format:** `YYYYMMDDHHMMSSTimezone`

**ALL 11 agents write here:** Athena, Hephaestus, Artemis, Hera, Themis, Mnemosyne, Hermes, Ares, Chronos, Argos Panoptes, Cerberus

**REQUIREMENTS/** is SEPARATE - permanent design documents, never deleted.

**Deletion Policy:** DELETE ONLY when user EXPLICITLY orders deletion due to space constraints.

---

# GHE Design Skill for Athena

## Core Philosophy: Requirements Are Free-Form

**CRITICAL**: Requirements documents are NOT constrained by templates.

Every domain has unique needs:
- **Mathematical specifications** need formal notation, proofs, invariants
- **Game mechanics** need interaction flows, state machines, physics models
- **Financial systems** need legal bounds, compliance protocols, audit trails
- **Distributed architectures** need consistency models, failure modes, CAP tradeoffs
- **Security specifications** need threat models, attack surfaces, trust boundaries
- **UI/UX features** need wireframes, accessibility, responsive behavior
- **Data pipelines** need schemas, transformations, validation rules
- **Hardware interfaces** need timing diagrams, protocols, signal specifications
- **Legal/compliance** need regulatory references, audit requirements, retention policies

**Athena writes requirements in whatever structure best serves the domain.**

The REQ-TEMPLATE.md is a **reference of possible sections**, not a mandatory structure. Use what's relevant, ignore what's not, add what's missing.

---

## Guiding Principles

### 1. Clarity Over Format
The goal is for Hephaestus to understand WHAT to build. Structure serves clarity, not the reverse.

### 2. Domain-Appropriate Language
Write in the language of the domain:
- Mathematical notation for algorithms
- State diagrams for interactive systems
- Legal language for compliance
- Network diagrams for distributed systems
- Threat models for security
- Timing diagrams for real-time systems
- Entity relationships for data models

### 3. Completeness Over Brevity
Include everything needed to implement. If Hephaestus will have questions, answer them preemptively.

### 4. References Over Repetition
Link to external documentation, specifications, standards. Don't copy-paste entire RFCs or API docs.

### 5. Verifiable Acceptance
Every requirement should have a way to verify it was met. "Working correctly" is not verifiable. "Returns HTTP 200 with JSON payload matching schema X" is verifiable.

---

## What MUST Be Present

Despite free-form structure, every requirements document MUST have:

1. **Clear identification**: REQ-NNN with version
2. **What is being built**: Unambiguous description
3. **Why it's needed**: User story or business justification
4. **How to verify completion**: Acceptance criteria (testable)
5. **External references**: Links to APIs, specs, assets, related issues

Everything else is domain-dependent.

---

## Domain-Specific Patterns

### Pattern: Mathematical/Algorithmic

```markdown
# REQ-042: Collision Detection Algorithm

## Problem Statement
Detect collisions between N convex polygons in 2D space.

## Mathematical Foundation
Using the Separating Axis Theorem (SAT):
- For convex polygons P and Q
- If there exists an axis where projections don't overlap → no collision
- Test all edge normals of both polygons

## Invariants
- Algorithm MUST be O(n*m) where n,m are vertex counts
- False positives: 0 (exact detection)
- False negatives: 0 (no missed collisions)

## Edge Cases
- Touching edges (0 penetration) → collision = true
- Nested polygons → collision = true
- Degenerate polygons (< 3 vertices) → undefined behavior

## References
- [SAT Explanation](https://www.sevenson.com.au/programming/sat/)
- [GJK Alternative](https://blog.winter.dev/2020/gjk-algorithm/)
```

### Pattern: Game Mechanics

```markdown
# REQ-043: Player Jump Mechanic

## State Machine
```
GROUNDED → (jump pressed) → JUMPING
JUMPING → (apex reached) → FALLING
FALLING → (ground contact) → GROUNDED
JUMPING/FALLING → (wall contact) → WALL_SLIDING
WALL_SLIDING → (jump pressed) → WALL_JUMPING
```

## Physics Parameters
- Jump velocity: 12 m/s
- Gravity: 35 m/s² (falling), 20 m/s² (rising)
- Coyote time: 100ms
- Jump buffer: 150ms

## Feel Requirements
- Jump must feel "snappy" not "floaty"
- Variable jump height based on button hold duration
- Reference: Celeste jump feel

## Assets Required
- Jump sound: `assets/sfx/jump.wav`
- Land sound: `assets/sfx/land.wav`
- Particle effect: `assets/vfx/jump_dust.prefab`
```

### Pattern: Financial/Legal

```markdown
# REQ-044: Payment Processing

## Regulatory Compliance
- PCI DSS Level 1 (we never store card numbers)
- GDPR Article 17 (right to erasure of payment history)
- SOX compliance for audit trails

## Transaction Flow
1. User initiates payment
2. Create idempotency key (UUID v4)
3. Call Stripe PaymentIntent API
4. On success: record transaction, send receipt
5. On failure: log error, notify user, DO NOT retry automatically

## Legal Constraints
- Refunds MUST be processed within 5 business days
- Transaction records retained for 7 years
- User can request payment history export (JSON format)

## Audit Requirements
- Every transaction logged with: timestamp, user_id, amount, status, idempotency_key
- Logs immutable (append-only)
- Access to logs restricted to finance role

## References
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [Stripe API](https://stripe.com/docs/api/payment_intents)
- Internal: `docs/legal/payment-policy.pdf`
```

### Pattern: Distributed Systems

```markdown
# REQ-045: Event Sourcing System

## Consistency Model
- Event store: strongly consistent (single leader)
- Read models: eventually consistent (< 500ms lag acceptable)
- Partition tolerance: yes (events replicated across 3 zones)

## CAP Tradeoffs
Prioritize: Consistency + Partition Tolerance
Sacrifice: Availability during network partitions

## Failure Modes
| Failure | Detection | Response |
|---------|-----------|----------|
| Leader down | Heartbeat timeout (3s) | Promote follower |
| Network partition | Split-brain detection | Reject writes on minority |
| Disk full | Monitoring alert | Stop accepting events |

## Event Schema
```json
{
  "event_id": "uuid",
  "aggregate_id": "uuid",
  "sequence": "int64",
  "type": "string",
  "payload": "json",
  "timestamp": "iso8601",
  "metadata": {"causation_id": "uuid", "correlation_id": "uuid"}
}
```

## References
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS](https://martinfowler.com/bliki/CQRS.html)
```

### Pattern: Security

```markdown
# REQ-046: Authentication System

## Threat Model
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| Credential stuffing | High | High | Rate limiting, breach detection |
| Session hijacking | Medium | High | Secure cookies, short TTL |
| MITM | Low | Critical | TLS 1.3 only, HSTS |

## Trust Boundaries
- Browser ↔ CDN: Untrusted (TLS required)
- CDN ↔ API: Semi-trusted (mTLS)
- API ↔ Database: Trusted (private network)

## Authentication Flow
1. User submits credentials
2. Validate against bcrypt hash (cost factor 12)
3. Check breach database (HaveIBeenPwned API)
4. Issue JWT (RS256, 15min expiry)
5. Issue refresh token (opaque, 7 day expiry, stored in httpOnly cookie)

## Security Headers Required
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

## References
- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Best Practices](https://auth0.com/blog/jwt-security-best-practices/)
```

---

## Minimum Viable Requirements Document

For simple features, this is enough:

```markdown
# REQ-047: Add Dark Mode Toggle

## What
A toggle in settings that switches between light and dark themes.

## Why
Users requested it. Reduces eye strain in low-light environments.

## Acceptance
- [ ] Toggle persists across sessions (localStorage)
- [ ] System preference detected on first visit
- [ ] Transition is smooth (200ms)
- [ ] All components respect theme (no hard-coded colors)

## Assets
- Design: `assets/mockups/dark-mode.pdf`
- Colors: `design-tokens/dark-theme.json`
```

---

## Performance Philosophy

**"Premature optimization is the root of all bugs."**

In requirements:
1. Specify WHAT, not HOW FAST
2. Defer performance targets until feature works
3. Add targets only when profiling reveals bottlenecks

```markdown
## Performance (Defer Until Working)

Performance requirements will be added after:
1. Feature is fully functional
2. User testing reveals actual issues
3. Profiling provides data

Known considerations for future optimization:
- Large lists may need virtualization
- Images may need lazy loading
```

---

## Summary

Athena's job is to translate user intent into clear, verifiable requirements using whatever structure best serves the domain. Templates are references, not constraints. The only mandatory elements are: identification, description, justification, acceptance criteria, and external references.

Write requirements that Hephaestus can implement without ambiguity.
