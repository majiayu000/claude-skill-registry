---
name: persona-coordination
description: Use when coordinating multi-persona team workflows, planning artifact handoffs between personas, or resolving cross-persona conflicts.
invocation: reference
---

# Persona Coordination Patterns

Guide to orchestrating Arc's 8 expert personas for cohesive OpenSpec planning, Beads decomposition, and team execution.

## Persona Roles Overview

| Persona | Role | OpenSpec Artifacts | Beads Type |
|---------|------|-------------------|-----------|
| `persona-backend-architect` | System design lead | Architecture, service boundaries, API contracts | Service/integration Beads |
| `persona-frontend-developer` | UI/component design | Component hierarchy, data flow, performance budgets | Component/page Beads |
| `persona-security-auditor` | Risk analysis, threat modeling | Threat models, security controls, compliance matrix | Security control Beads |
| `persona-typescript-pro` | Type system design | Type architecture, tsconfig, API types | Type definition Beads |
| `persona-tdd-orchestrator` | Test strategy | Test pyramid, coverage targets, verification gates | Test Beads (execute first) |
| `persona-debugger` | Root cause analysis, prevention | Root cause docs, regression prevention patterns | Regression test Beads |
| `persona-research-synthesizer` | Evidence gathering, synthesis | Research briefs, evidence matrices, confidence levels | Research validation Beads |
| `persona-ux-researcher` | User insights, usability | Personas, journeys, heuristic evaluations | User-driven requirement Beads |

## Coordination Pairs

### 1. Backend-Architect ↔ Security-Auditor

**Flow**: Architecture → Threat Modeling → Hardened Architecture

- **Backend** produces initial architecture (services, APIs, integration points)
- **Security** performs STRIDE/PASTA threat analysis on architecture
- **Security** identifies controls needed: auth flows, encryption, rate limiting, validation
- **Backend** incorporates security controls into final architecture design
- **Output**: OpenSpec architecture with integrated security requirements

**Example Handoff**:
```
Backend: "Design REST API for user service with OAuth 2.0"
  ↓
Security: "Threat model identifies: token leakage, CSRF on endpoints, injection risks"
  ↓
Backend: "Revise design: add token encryption, CSRF tokens, input validation layers"
  ↓
Joint OpenSpec: Architecture + threat model + control matrix
```

### 2. Frontend-Developer ↔ TypeScript-Pro ↔ TDD-Orchestrator

**Flow**: Component Design → Type Safety → Test Strategy

- **Frontend** defines component hierarchy, data flow, state strategy
- **TypeScript** designs type architecture (API types, component props, domain types)
- **TDD** designs test pyramid (unit tests for types, integration for components, E2E for flows)
- **Frontend** implements using types and test-first discipline
- **Output**: Typed, tested, performance-optimized components

**Example Handoff**:
```
Frontend: "Dashboard needs user profile widget + chart integration"
  ↓
TypeScript: "Define UserProfile interface, ChartData discriminated union, props types"
  ↓
TDD: "Test pyramid: unit tests for type validation, integration for widget props, E2E for chart rendering"
  ↓
Frontend: "Write tests → implement components with strict typing"
  ↓
Beads Output: 
  - Type definition Bead (frontend: pending)
  - Component unit test Bead (frontend: blocked by types)
  - Chart integration test Bead (frontend: blocked by component)
  - Component implementation Bead (frontend: blocked by tests)
```

### 3. TDD-Orchestrator ↔ All Technical Personas

**Flow**: Testability as Cross-Cutting Concern

- **TDD** coordinates with each technical persona to ensure testability
- **TDD** + Backend: API contract tests, integration test strategy
- **TDD** + Frontend: Component/hook unit tests, accessibility tests
- **TDD** + TypeScript: Type assertion tests, type coverage
- **TDD** + Security: Security test vectors, penetration test gating
- **Output**: Comprehensive test matrix covering all concerns

**Example Coordination**:
```
TDD: "Establish test pyramid: 60% unit, 25% integration, 10% E2E, 5% security"
  ↓
Backend: "Provide integration test fixtures for API endpoints"
  ↓
Frontend: "Provide component test utilities and accessibility checklist"
  ↓
TypeScript: "Provide type assertion test templates"
  ↓
Security: "Provide OWASP test vectors and penetration test suite"
  ↓
TDD creates Beads: Test infrastructure → API tests → Component tests → Security tests → Implementation
```

### 4. Debugger ↔ All Personas (Reactive)

**Flow**: Root Cause → Prevention Pattern → Bead Enhancement

- **Debugger** invoked when test fails or issue emerges
- **Debugger** identifies root cause and architectural gap
- **Debugger** escalates to lead if issue requires design revision
- **Debugger** + TDD: Creates regression test Bead to prevent recurrence
- **Output**: Enhanced Beads with regression tests and prevention patterns

**Example**:
```
Test fails: "Component unmounts before async data loads"
  ↓
Debugger: "Root cause: missing loading state management, race condition in cleanup"
  ↓
Debugger + TDD: "Create regression test for race condition"
  ↓
Debugger + Frontend: "Add Suspense boundary and loading state to component Bead"
  ↓
New Bead created: "Add loading state tests" (unblocks component Bead)
```

### 5. Research-Synthesizer ↔ Backend/Frontend/UX Personas

**Flow**: Research Evidence → Design Decisions → Confidence Assessment

- **Research** provides evidence matrices backing architecture/UX decisions
- **Backend**: Research on API design patterns, resilience patterns, scale research
- **Frontend**: Research on performance patterns, accessibility standards, user interaction patterns
- **UX**: Research on user workflows, mental models, pain points
- **Output**: Evidence-backed OpenSpec with confidence levels

**Example**:
```
Backend: "Should we use REST or GraphQL for content API?"
  ↓
Research: "Review 15 sources on API paradigm trade-offs, summarize evidence matrix"
  ↓
Research Output: "GraphQL recommended for flexible queries (high confidence), 
                   REST better for caching strategies (high confidence), 
                   REST widely understood in team (medium confidence)"
  ↓
Backend + Research: "OpenSpec documents GraphQL decision with evidence and confidence"
```

### 6. UX-Researcher ↔ Frontend-Developer ↔ Security-Auditor

**Flow**: User Evidence → Design Constraints → Usability + Security

- **UX** provides personas, journey maps, insight statements from user research
- **Frontend** designs components and flows aligned to user insights
- **Security** ensures usability doesn't compromise security (e.g., password managers, biometric auth)
- **Frontend** validates design against heuristics
- **Output**: User-centered, secure component specs

**Example**:
```
UX: "Research shows 60% of users expect biometric login on mobile"
  ↓
Frontend: "Design biometric auth flow + fallback password"
  ↓
Security: "Biometric tokens require secure enclave, rate limiting on failures"
  ↓
Frontend: "Add security controls without blocking biometric UX"
  ↓
UX: "Heuristic evaluation validates design matches user expectations"
  ↓
Bead spec: Biometric auth with secure fallback + accessibility
```

## OpenSpec Artifact Flow

```
/arc:core:plan (single unified plan)
    ↓
/arc:core:spec (persona contributions converge):
    ├─ Backend-Architect → proposal.md (architecture scope)
    ├─ TDD-Orchestrator → design.md (test strategy section)
    ├─ Security-Auditor → design.md (threat model, controls)
    ├─ TypeScript-Pro → design.md (type architecture)
    ├─ Frontend-Developer → design.md (component/UX architecture)
    ├─ UX-Researcher → design.md (user research, personas)
    ├─ Research-Synthesizer → design.md (evidence matrix)
    └─ All → tasks.md (phased, cross-persona tasks)
         + tests.md (unified test spec)
         + specs/*.md (capability specs with all concerns)
    ↓
/arc:core:beads (Beads decomposition respects coordination):
    ├─ Type definition Beads (TypeScript-Pro)
    ├─ Test Beads (TDD-Orchestrator, depends on types) ← P1
    ├─ Security validation Beads (Security-Auditor, depends on tests)
    ├─ Component/API Beads (Frontend/Backend, depends on tests)
    ├─ Integration Beads (all personas, cross-file dependencies)
    └─ Verification Beads (all verify agents, post-execution)
    ↓
/arc:core:execute --mode team:
    Lead: Coordinates personas, enforces TDD ordering, resolves conflicts
    Workers (persona agents): Implement assigned Beads, hand off to next
```

## Team Mode Assignment Strategies

### Strategy 1: Pure Specialization (Recommended)

Assign each persona to its specialty area; let lead coordinate handoffs.

```bash
/arc:core:execute --mode team \
  --assign persona-backend-architect:api-service \
  --assign persona-frontend-developer:ui-components \
  --assign persona-tdd-orchestrator:testing \
  --assign persona-security-auditor:hardening \
  --assign persona-typescript-pro:types
```

**Lead responsibilities**:
- Enforce TDD ordering (types → tests → implementation)
- Detect cross-persona dependencies (e.g., API type Bead blocks component Bead)
- Resolve conflicts (two personas modifying same file)
- Escalate untestable designs

### Strategy 2: Layered Execution

Phases executed sequentially with tight persona coordination.

```
Phase 1 (Planning): All personas → OpenSpec artifacts
Phase 2 (Types): TypeScript-Pro → type definition Beads
Phase 3 (Tests): TDD-Orchestrator → test Beads (all concerns)
Phase 4 (Security): Security-Auditor → security control Beads
Phase 5 (Implementation): Backend/Frontend → impl Beads (TDD order)
Phase 6 (Verification): Verify agents → compliance Beads
```

### Strategy 3: Research-Driven (For High-Uncertainty Work)

Research personas lead early; technical personas follow with evidence-backed designs.

```
Phase 1: UX-Researcher + Research-Synthesizer → user evidence + decision matrix
Phase 2: Backend/Frontend informed by Phase 1 → architecture + components
Phase 3: Security + TDD ensure evidence-backed designs are secure + tested
Phase 4: Execute with high confidence
```

## Artifact Handoff Checklist

### Backend-Architect → Security-Auditor
- [ ] Architecture diagram with all services, boundaries, integration points
- [ ] API contract definitions (endpoints, auth flows, error handling)
- [ ] Data flow diagram (what data moves where)
- **Security provides**: Threat model, control matrix, security test vectors

### Frontend-Developer → TypeScript-Pro
- [ ] Component hierarchy and composition boundaries
- [ ] Data flow and state management strategy
- [ ] API integration points and contract expectations
- **TypeScript provides**: Prop types, API types, validation types

### TypeScript-Pro → TDD-Orchestrator
- [ ] Type definitions and type architecture
- [ ] Type assertion test templates
- [ ] Type coverage targets
- **TDD provides**: Unit test pyramid, type coverage gates, test vector

### TDD-Orchestrator → Implementers (Backend/Frontend)
- [ ] Test suite structure (unit/integration/E2E)
- [ ] Test fixtures and mock strategies
- [ ] Coverage targets and gating criteria
- [ ] Cross-persona test integration points
- **Implementers provide**: Tests → Implementation (red-green-refactor)

### UX-Researcher → Frontend-Developer
- [ ] Personas with behavior and mental models
- [ ] Journey maps with emotional mapping
- [ ] Accessibility requirements (WCAG 2.1 AA minimum)
- [ ] Heuristic evaluation criteria
- **Frontend provides**: User-validated components

### All Technical → Debugger (On Failure)
- [ ] Test failure with stack trace
- [ ] Reproduction steps
- [ ] Recent code changes
- **Debugger provides**: Root cause + prevention pattern Bead

## Example: Full Workflow with Personas

### Scenario: Building OAuth 2.0 Login System

**Phase 1: Planning**
```
User: "Design secure OAuth 2.0 login with biometric fallback"
/arc:core:plan
  → plan.md with context
```

**Phase 2: OpenSpec (Personas Converge)**
```
Backend-Architect: 
  - OAuth 2.0 flow architecture
  - Token refresh strategy
  - Service boundaries (auth service, user service)

Security-Auditor:
  - STRIDE threat model: token leakage, CSRF, phishing
  - Controls: PKCE, secure token storage, rate limiting
  - Compliance: GDPR for data retention

TypeScript-Pro:
  - OAuth types (AccessToken, RefreshToken)
  - Session type interface
  - API client typed for auth endpoints

TDD-Orchestrator:
  - Unit tests: token validation, PKCE generation
  - Integration tests: OAuth flow end-to-end
  - Security tests: CSRF protection, token expiry
  - E2E tests: user login → protected resource

UX-Researcher:
  - Research: Users expect 2FA, 45% use biometric
  - Persona: "Mobile user, privacy-conscious"
  - Journey: Launch app → see login → biometric prompt → logged in

Frontend-Developer:
  - Biometric login button
  - Password fallback screen
  - Session timeout warning
  - Accessibility: keyboard navigation, screen reader

/arc:core:spec
  → proposal.md (scope, decision)
  → design.md (architecture + threat model + types + test strategy + UX research)
  → tests.md (all tests across concerns)
  → tasks.md (phased tasks with persona assignments)
```

**Phase 3: Beads**
```
/arc:core:beads
  Epic: oauth2-biometric-login

  Bead 1 (TypeScript): Define OAuth types (INDEPENDENT)
    - Files: src/types/auth.ts
    - Verification: `tsc --noEmit`
  
  Bead 2 (TDD): Unit tests for token validation (DEPENDS ON: Bead 1)
    - Files: tests/auth.unit.test.ts
    - Verification: `npm test tests/auth.unit.test.ts`
  
  Bead 3 (Security): PKCE implementation test (DEPENDS ON: Bead 2)
    - Files: tests/oauth.security.test.ts
    - Verification: `npm test tests/oauth.security.test.ts`
  
  Bead 4 (Backend): OAuth token service (DEPENDS ON: Bead 1,2,3)
    - Files: src/services/oauth.ts
    - Verification: `npm test tests/auth.unit.test.ts && npm test tests/oauth.security.test.ts`
  
  Bead 5 (Frontend): Biometric login component (DEPENDS ON: Bead 1,4)
    - Files: src/components/BiometricLogin.tsx, tests/BiometricLogin.test.tsx
    - Verification: `npm test src/components/BiometricLogin.test.tsx && npx axe tests/BiometricLogin.html`
  
  Bead 6 (Security): Penetration test OAuth flow (DEPENDS ON: Bead 4,5)
    - Files: tests/oauth.pentest.ts
    - Verification: `npm test tests/oauth.pentest.ts`
```

**Phase 4: Team Execution**
```
/arc:core:execute --mode team \
  --assign persona-typescript-pro:types \
  --assign persona-tdd-orchestrator:testing \
  --assign persona-security-auditor:hardening \
  --assign persona-backend-architect:api-service \
  --assign persona-frontend-developer:ui-components

Lead coordinates:
  1. TypeScript-Pro: Complete Bead 1 (types) → CLOSED
  2. TDD-Orchestrator: Claim Bead 2 (unit tests), BLOCKED (depends on types)
     → Types complete, TDD starts Bead 2 → CLOSED
  3. Security-Auditor: Claim Bead 3 (security tests), BLOCKED (depends on unit tests)
     → Unit tests complete, Security starts Bead 3 → CLOSED
  4. Backend-Architect: Claim Bead 4 (OAuth service), BLOCKED (depends on all tests)
     → All tests complete, Backend starts Bead 4 → CLOSED
  5. Frontend-Developer: Claim Bead 5 (biometric component), BLOCKED (depends on service)
     → Service complete, Frontend starts Bead 5 → CLOSED
  6. Security-Auditor: Claim Bead 6 (pentest), BLOCKED (depends on component)
     → Component complete, Security starts Bead 6 → CLOSED

All Beads closed → /arc:core:verify runs post-execution verification
```

## Conflict Resolution

### Shared File Conflict (Two Personas Need to Modify Same File)

**Example**: Backend and TypeScript both need to update `src/types/api.ts`

**Lead resolution**:
1. Identify which Bead must complete first (usually TypeScript types first)
2. Serialize access: TypeScript Bead #1 executes and closes
3. Backend Bead #2 waits in BLOCKED state
4. Once TypeScript Bead closes, pull latest state before Backend starts
5. Enforce: only one persona modifies at a time

### Design Conflict (Persona Has Different Opinion on Architecture)

**Example**: Backend prefers REST, Frontend wants GraphQL for flexibility

**Lead resolution**:
1. Escalate to lead (do not let personas argue)
2. Lead requests trade-off analysis from each:
   - Backend: REST caching benefits, learning curve, maturity
   - Frontend: GraphQL query flexibility, bundle size, complexity
3. Lead decides, updates OpenSpec with decision record
4. Both personas implement decision (no override)

### Untestable Requirement (TDD Finds Design Gap)

**Example**: TDD-Orchestrator flags: "How do we test biometric auth in CI/CD?"

**Lead resolution**:
1. TDD escalates to lead with concern
2. Lead + Frontend + TDD determine: mock biometric API vs. E2E with real API
3. Update OpenSpec `tests.md` with decision
4. Create new type Bead (mock interface) if needed
5. TDD resumes with updated test strategy

## Anti-Patterns to Avoid

### ❌ Silent Downgrades
Don't let Security say "we'll skip encryption to ship faster" or TDD say "we'll test after." Escalate to lead.

### ❌ Persona Scope Creep
Backend shouldn't implement frontend logic; Frontend shouldn't design databases. Stick to specialty.

### ❌ Vague Handoffs
"Check the design doc" is not sufficient. Each Bead must be self-contained with all context.

### ❌ Skipping Coordination
Building component without type definitions; implementing without tests; releasing without security audit.

### ❌ Lead Implementing
Lead coordinates only, never implements. If no workers available, defer or pause.

## Success Metrics

✅ **All 8 personas contributed to OpenSpec**  
✅ **Beads explicitly encode coordination (dependencies, labels)**  
✅ **TDD ordering enforced (tests before impl, types before tests)**  
✅ **Each Bead self-contained (no "see OpenSpec" references)**  
✅ **All Beads passed verification before closing**  
✅ **No silent downgrades (escalations documented)**  
✅ **Cross-persona integration verified (types work in components, API types match backend)**
