---
name: constitution-generator
description: |
  Generate tailored project constitution input for the /speckit.constitution command. Use when starting a new project, bootstrapping governance, or when user asks to "create a constitution", "set up project principles", "define coding standards", or needs help with /speckit.constitution input. Conducts structured discovery through clarifying questions about project scale, risk profile, lifespan, architecture, team size, and delivery expectations, then recommends appropriate engineering principles, patterns, and practices matched to the project's characteristics.
---

# Constitution Generator

Generate input for `/speckit.constitution` by discovering project characteristics and recommending matched principles.

## Workflow

### Phase 1: Project Discovery

Ask questions to understand the project. Group related questions; don't overwhelm with all at once.

**Round 1 - Project Nature:**
- Is this a hackathon/prototype, internal tool, commercial product, or open-source project?
- What's the expected lifespan? (days/weeks, months, years, indefinite)
- Solo developer or team? If team, how many contributors?

**Round 2 - Technical Profile:**
- What's the architecture style? (monolith, modular, distributed/microservices, CLI tool, library/SDK)
- What's the primary tech stack? (language, frameworks)
- Will this system be public-facing, internal, or both?

**Round 3 - Risk & Operations:**
- How critical is uptime? (best-effort, business hours, 99%+, mission-critical)
- Are there security/regulatory constraints? (financial, healthcare, PII, none specific)
- What's your expected release cadence? (continuous, weekly, monthly, infrequent)

**Round 4 - Quality Expectations:**
- How important is test coverage? (manual testing fine, critical paths only, comprehensive)
- Do you need audit trails or data replay? (yes/no)
- What's more important right now: shipping fast or building for longevity?

### Phase 2: Principle Selection

Based on discovery, select principles from the catalog below. Only suggest what matches the project profile.

**Selection Rules:**

| Project Characteristic | Suggested Principles |
|----------------------|---------------------|
| Hackathon/prototype | MVP Speed, Demo-First, Skip Tests, Good Enough Architecture |
| Solo personal tool | Ship Fast Fix What Hurts, Build for Joy, Dogfood Relentlessly |
| Team project | Single Responsibility, Conventional Commits, Code Review Required |
| Long-lived system | Modularity, Documentation Standards, Semantic Versioning |
| High uptime (99%+) | Fail Fast & Loud, Graceful Degradation, Observability First |
| Public/multi-tenant | Zero Trust, Least Privilege, Input Validation Required |
| Financial/regulated | Security by Default, Audit Trails, No Silent Failures |
| CLI tool | Unix Philosophy, Text I/O Protocol, Predictable Exit Codes |
| Distributed system | CAP Awareness, Idempotency, Circuit Breaking |
| Complex domain | Domain-Driven Design (selective), Clear Naming |
| Fast iteration needed | YAGNI, KISS, Refactor When It Hurts |

**Anti-patterns to avoid:**
- Don't suggest TDD for hackathons
- Don't suggest Event Sourcing unless audit/replay is explicitly needed
- Don't suggest DDD for simple CRUD apps
- Don't suggest SRE practices unless uptime ≥99.5% expected
- Don't suggest Zero Trust for single-user local tools

### Phase 3: Generate Constitution Input

Format output as markdown suitable for `/speckit.constitution` command input. Structure:

```markdown
## Preamble
[1-2 sentences describing project goal and philosophy]

## Core Principles

### I. [Principle Name]
**[One-line summary of the principle]**

- **Rule 1**: [Specific, actionable rule]
- **Rule 2**: [Specific, actionable rule]
- ...

**Rationale**: [Why this principle matters for this project]

### II. [Next Principle]
...

## Development Standards
[Only include sections relevant to the project]

### [Standard Category]
- [Specific standard]
- [Specific standard]

## Governance

### Amendment Procedure
- Changes require documented rationale
- Version follows semver (MAJOR.MINOR.PATCH)
- MAJOR: Breaking principle changes
- MINOR: New principles/sections
- PATCH: Clarifications

### Compliance
- Constitution supersedes other practices
- Complexity requires explicit justification
```

## Principle Catalog

### Speed & Simplicity

**MVP Speed**: Ship smallest working version fast. Cut features aggressively. Skip premature optimization. Refactor when it hurts, not before.

**Ship Fast, Fix What Hurts**: Build smallest useful thing, dogfood immediately, iterate on real pain. Ignore hypothetical requirements.

**KISS**: Do simplest thing that works. If you can't explain it in one sentence, it's too complex.

**YAGNI**: No speculative features. Build when needed, not "just in case."

**Good Enough Architecture**: Use patterns you know. Boring and fast beats novel and slow.

**Make It Work, Then Make It Fast**: Correctness first. Measure before optimizing. "Fast enough" is good enough.

### Code Quality

**Single Responsibility**: Each component does one thing well. Don't blur lines between concerns.

**Modularity**: Well-defined boundaries. Explicit dependencies. No circular dependencies.

**Composition Over Inheritance**: Prefer composing simple parts over complex inheritance hierarchies.

**Encapsulate What Varies**: Isolate the parts that change from the parts that stay the same.

**Rule of Three**: Don't generalize until the third repetition.

### Testing

**Integration Tests First**: Test real workflows against real environments. Mocks are last resort.

**Test What Matters**: Focus on catching bugs, not coverage metrics. Test critical paths, skip trivialities.

**Tests Optional (Hackathon)**: Manual testing acceptable. Automated tests only if they save debugging time.

**Don't Test Your Mocks**: If tests pass but real integration fails, tests are useless.

### Error Handling

**Fail Fast & Loud**: Crash early with clear context. No silent failures.

**Fail Safe**: When failure happens, fail to a safe state.

**Human-Readable Errors**: "API connection failed: returned 503. Check network." Not "ECONNREFUSED".

**Actionable Feedback**: Every error suggests a fix or next step.

**Graceful Degradation**: If a service is down, say so clearly. Don't pretend everything is fine.

### Documentation

**README First**: Installation, setup, and basic usage must be documented.

**Comment the Why**: Not the what. Assume reader understands the language.

**Code as Documentation**: Clear naming > comments. Comments for non-obvious decisions only.

**Documentation as Code**: Keep docs next to code. Update together.

### Operations

**Observability First**: You can't fix what you can't see. Logs, metrics, traces.

**Infrastructure as Code**: If it's not in code, it doesn't exist.

**Automate What Hurts**: If it's repeated and painful, automate it.

**Runbooks Over Tribal Knowledge**: Write down how to fix things.

### Security

**Zero Trust**: Assume networks are hostile. Verify everything.

**Least Privilege**: Minimum access needed. No more.

**Secure by Default**: Opt into risk, not safety.

**Defense in Depth**: Multiple layers of protection.

**Input Validation Required**: Validate at system boundaries. Use schemas (Zod, etc.).

**Never Log Secrets**: Private keys, tokens, passwords never in logs or output.

### Team & Process

**Conventional Commits**: `type(scope): subject` format for clear, searchable history.

**Trunk-Based Development**: Short-lived branches. Merge frequently.

**Code Review Required**: All changes reviewed before merge.

**Blameless Postmortems**: Learn from failures without blame.

**Strong Opinions, Weakly Held**: Commit to decisions but change when evidence warrants.

### Architecture Patterns

**Unix Philosophy**: Single purpose. Text I/O. Composable. Predictable exit codes.

**Hexagonal/Ports & Adapters**: Isolate business logic from I/O.

**Locality of Behavior**: Put things that change together, together.

**Stable Dependencies**: Depend on things less likely to change.

**API First Design**: Design the contract before implementation.

### Delivery

**Small Batches**: Ship small, ship often. Smaller changes = smaller risks.

**Done Means Deployed**: Code isn't done until it's running somewhere.

**Feature Flags Over Branches**: Deploy dark, enable incrementally.

**Continuous Delivery**: Always be in a deployable state.

### Product Focus

**Solve Real Problems**: Not imaginary ones. Follow demand, don't anticipate it.

**Defaults Are Product Decisions**: Make the right thing easy.

**Evidence Over Opinions**: Measure outcomes, not output.

**If It's Not Used, It Doesn't Exist**: Features require adoption to be "done".

### UX Principles

**Frictionless Setup**: One command to install, one to run.

**Speed Is a Feature**: Fast feedback loops. Progress for anything >500ms.

**Predictability Over Flashiness**: Do what users expect.

**Design for the Primary Use Case**: Not the edge cases.

## Output Quality Checklist

Before presenting the constitution:
- [ ] Principles match project profile discovered in Phase 1
- [ ] No over-engineering (no DDD for CRUD, no TDD for hackathons, etc.)
- [ ] Each principle has specific, actionable rules
- [ ] Rationales explain why this matters for THIS project
- [ ] Governance section included
- [ ] Format is ready to paste into /speckit.constitution
