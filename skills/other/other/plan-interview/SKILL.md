---
name: plan-interview
description: Adaptive interview-driven spec generation. Use when converting rough plans into comprehensive specifications, needing structured requirements gathering, or transforming ideas into implementation-ready documentation.
---

# Plan Interview Skill

Transform rough plans into comprehensive, implementation-ready specifications through adaptive, structured interviews.

## When to Use

- Converting a plan or idea into a detailed specification
- Gathering requirements through structured questioning
- Transforming rough documentation into implementation-ready specs
- Ensuring all edge cases, risks, and stakeholders are considered before implementation

## Available Components

### Command: `/plan-interview:interview [plan-file]`

Adaptive interview that calibrates depth based on plan complexity:

| Complexity | Signals | Questions |
|------------|---------|-----------|
| **Simple** | Single feature, clear scope | 10-15 |
| **Moderate** | Multi-component, some integrations | 18-23 |
| **Complex** | Cross-system, many stakeholders | 22-28 |

**Usage:**
```bash
/plan-interview:interview docs/feature-plan.md
# Output: docs/feature-plan-spec.md
```

### Agent: `spec-reviewer`

Autonomous quality analysis of specifications across 4 dimensions:
- **Completeness** (25 pts) - All sections populated?
- **Consistency** (25 pts) - No contradictions?
- **Clarity** (25 pts) - No ambiguous language?
- **Edge Cases** (25 pts) - Error handling defined?

Triggers when you say "review my spec" or "check specification quality".

## Interview Phases

1. **Foundations & Scope** - Stakeholders, success criteria, constraints, MVP scope
2. **Technical Deep-Dive** - Architecture, data models, scalability, security
3. **User Experience** - Personas, flows, cognitive load, error recovery
4. **Risks & Tradeoffs** - Risk categorization, blast radius, contingency plans
5. **Operationalization** - Testing, deployment, monitoring
6. **Wrap-Up** (optional) - Only for complex plans with remaining gaps

## Interview Philosophy

**Core Principle**: Depth over breadth. Better to deeply understand critical aspects than superficially cover everything.

**Key Techniques**:
- Non-obvious questions - Skip what the plan already answers
- Edge probing - What happens in unusual cases?
- Assumption surfacing - Make implicit beliefs explicit
- Contradiction detection - Flag when answers don't align
- Adaptive depth - Probe deeper on complex areas, move faster on clear ones

## Spec Output Structure

Generated specs include:
- Overview (problem, solution, success criteria, stakeholders)
- Functional and non-functional requirements
- Technical design (architecture, data models, APIs, security)
- User experience (personas, flows, states, edge cases)
- Risks and mitigations (risk register, tradeoffs, contingency plans)
- Implementation notes (key decisions, dependencies, migration)
- Operationalization (testing, deployment, monitoring)
- Open questions and out-of-scope items
- Phasing (MVP vs future)

## References

Load these for deeper guidance during interviews:
- `references/phase-1-clarifications.md` - Foundations questions and pitfalls
- `references/phase-2-technical.md` - Architecture discussion patterns
- `references/phase-3-ux.md` - Persona development, UX patterns
- `references/phase-4-risks.md` - Risk assessment frameworks
- `references/interview-techniques.md` - Cross-cutting interview skills
- `references/example-spec.md` - Annotated high-quality spec example
