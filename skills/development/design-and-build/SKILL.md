---
name: design-and-build
description: Use when making architecture decisions, setting up CI/CD, managing technical debt, or choosing branching strategies - enforces ADR requirements and prevents resume-driven design
---

# Design and Build

## Overview

This skill implements the **Technical Solution (TS)**, **Product Integration (PI)**, and **Configuration Management (CM)** process areas from the CMMI-based SDLC prescription.

**Core principle**: Architecture decisions require documentation (ADRs). Emergency shortcuts require retrospective documentation. "Best practice" is never justification - requirements are.

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` Section 3.2 for complete policy and practice definitions.

---

## When to Use

Use this skill when:
- Making architecture or design decisions (technology choice, patterns, structure)
- Setting up build/integration systems (CI/CD, deployment pipelines)
- Managing technical debt (tracking, prioritization, paydown)
- Establishing configuration management (branching strategy, release process)
- Facing "should we use X?" questions where X is trendy technology
- Team experiencing git chaos, integration hell, or debt spiral

**Do NOT use for**:
- Implementation details within existing architecture → Use domain-specific skills (python-engineering, web-backend)
- Testing strategy → Use quality-assurance skill
- Requirements or specification → Use requirements-lifecycle skill

---

## Quick Reference

| Situation | Primary Reference Sheet | Key Decision |
|-----------|------------------------|--------------|
| "Should we use microservices?" | Architecture & Design | Requires ADR. Use decision framework: team size, domain complexity, ops maturity. |
| "Git workflow is chaos" | Configuration Management | Diagnose root cause first. GitFlow (L3 releases) vs GitHub Flow (continuous) vs Trunk (high maturity). Requires ADR. |
| "70% of time on bugs" | Technical Debt Management | CODE RED. Feature freeze, architectural audit, classify debt (architectural/tactical/unpayable). |
| "Setting up CI/CD" | Build & Integration | Requirements gathering first. Platform choice requires ADR. Start simple, add stages incrementally. |
| "Quick fix vs proper solution" | Level 2→3→4 Scaling | Level 3 requires retrospective ADR within 48 hours. Document as HOTFIX with paydown commitment. |

---

## Level-Based Governance

**CRITICAL**: This skill enforces governance based on project maturity level.

### Level Detection

Check for project level in:
1. `CLAUDE.md`: `CMMI Target Level: 3`
2. User message: "This is a Level 3 project..."
3. **Default if unspecified**: Level 3

### ADR Requirements by Level

| Level | ADR Required For | Exception Protocol |
|-------|------------------|-------------------|
| **Level 2** | Major architecture decisions (platform choice, deployment strategy) | Informal discussion OK, document decision in wiki/README |
| **Level 3** | ALL architectural decisions (tech stack, branching strategy, design patterns, CI/CD platform) | Emergency HOTFIX: Retrospective ADR within 48 hours mandatory |
| **Level 4** | Everything in L3 + quantitative justification with metrics | No exceptions - statistical baselines required |

### Emergency Exception Protocol (HOTFIX Pattern)

**When**: Production emergency, immediate fix needed, no time for full ADR process

**Level 3 Requirements**:
1. Fix the emergency (restore service)
2. Document the fix in issue tracker with "HOTFIX" label
3. Create retrospective ADR within **48 hours**:
   - Incident timeline
   - Why proper fix wasn't feasible
   - Technical debt introduced
   - Paydown commitment with date (max 2 weeks)
4. Track paydown as high-priority ticket

**Violation**: Skipping retrospective ADR = governance failure. See Enforcement section below.

**HOTFIX Frequency Limit**: >5 HOTFIXes per month = systemic problem requiring architectural audit, not process exception.

### What Counts as "Architectural Decision"? (Level 3)

**Architectural decisions** (ADR required):
- Technology platform choice (language, framework, database, cache, message queue)
- Branching strategy (GitFlow, GitHub Flow, trunk-based)
- CI/CD platform (GitHub Actions, Azure Pipelines, Jenkins)
- Deployment strategy (blue/green, canary, rolling)
- Design patterns with broad impact (event-driven, microservices, monolith)
- Module boundaries and interfaces (how system decomposes)
- Authentication/authorization approach (OAuth, JWT, session-based)
- Data storage strategy (SQL vs NoSQL, caching strategy, data partitioning)

**Implementation details** (no ADR required, track in code/PR):
- Specific library choice within chosen framework (e.g., logging library in Python)
- Variable/function naming conventions
- Code organization within module (file structure)
- Test framework choice (if it doesn't affect architecture)

**Borderline decisions** (when in doubt, write ADR):
- If change affects >3 modules or files → ADR
- If reversal would take >1 day → ADR
- If future developers would ask "why did they choose this?" → ADR

---

## Enforcement and Escalation

**Level 3 Requirements**:
- Platform enforcement: Branch protection, CI gates, ADR linking
- Process enforcement: ADR review before implementation, HOTFIX tracking
- Metrics: % architectural changes with ADRs (target: 100%)
- Violations escalate: Team lead → Engineering manager → Governance committee

**For detailed enforcement mechanisms, escalation paths, and compliance metrics**, see `level-scaling.md`.

---

## Anti-Patterns and Red Flags

### Resume-Driven Design

**Detection**: User says "I've heard X is best practice" or "Everyone uses Y"

**Red Flags**:
- Technology mentioned before requirements
- Appeal to popularity ("everyone uses microservices")
- Buzzword bingo (serverless, Kubernetes, blockchain)
- Can't articulate WHAT PROBLEM they're solving

**Counter**:
1. "What requirements drive this choice?"
2. "What alternatives exist?"
3. "Why is current approach inadequate?"
4. If they can't answer → "You're doing resume-driven design. Requirements first, technology second."

**Forcing function**: Require ADR with alternatives analysis. If they can't justify with measurable requirements, ADR review will reject it.

### Architecture Astronaut

**Detection**: Over-engineered solution for simple problem

**Red Flags**:
- Microservices for CRUD app
- Service mesh for 2 services
- Event sourcing for simple data model
- "Future-proof" without concrete future requirements

**Counter**: "What's the SIMPLEST solution that meets requirements? Start there. Add complexity when demonstrated need exists, not hypothetically."

### Cowboy Coding

**Detection**: No reviews, no standards, "works on my machine"

**Red Flags**:
- Skipping pull requests
- Force pushing to main
- No CI/CD
- "I'll add tests later"

**Counter**: Enforce basic CM practices. Level 2 minimum: branch protection, required PR reviews, CI runs on PRs.

### Debt Spiral

**Detection**: Increasing % of time on bugs, velocity declining

**Red Flags**:
- >50% time on bugs = WARNING
- >60% time on bugs = CODE RED
- Every feature breaks something else
- Team morale declining

**Counter**: See Technical Debt Management reference sheet. CODE RED triggers feature freeze.

---

## Reference Sheets

Load these on-demand for detailed guidance:

| Reference Sheet | When to Use | Link |
|-----------------|-------------|------|
| **Architecture & Design** | Making technology choices, selecting patterns, designing system structure | [architecture-and-design.md](./architecture-and-design.md) |
| **Implementation Standards** | Establishing coding standards, code review process, documentation requirements | [implementation-standards.md](./implementation-standards.md) |
| **Configuration Management** | Git chaos, branching strategy decisions, release management | [configuration-management.md](./configuration-management.md) |
| **Build & Integration** | Setting up CI/CD, build optimization, deployment pipelines | [build-and-integration.md](./build-and-integration.md) |
| **Technical Debt Management** | Team spending >40% time on bugs, debt accumulating, velocity declining | [technical-debt-management.md](./technical-debt-management.md) |
| **Level 2→3→4 Scaling** | Understanding what rigor is appropriate for your project tier | [level-scaling.md](./level-scaling.md) |

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| "Emergency exempts process" | Creates pattern where "urgent" = skip governance, accumulating undocumented debt | Use HOTFIX pattern: retrospective ADR within 48 hours, mandatory |
| "I'll document it later" | Later never comes, loses audit trail | Document NOW (ADR takes 15 min) or schedule retrospective (48 hours max) |
| "This is too simple for ADR" | Simple decisions have big impact, lose rationale for future | If it's truly simple, ADR takes 10 min. If it takes longer, it wasn't simple. |
| "Everyone uses X, so we should" | Resume-driven design, not requirements-driven | Require measurable justification. "Everyone" is not a requirement. |
| "20% debt allocation" when 70% bugs | Treats crisis as normal problem, ensures slow death | >60% bugs = CODE RED. Feature freeze, not incremental paydown. |
| "Pick branching strategy" without diagnosis | Treats symptom (conflicts) not cause (architecture? communication?) | Root cause analysis FIRST. Git strategy is symptom, not disease. |
| Generic CI/CD template without context | Wastes time on wrong solution | Requirements gathering FIRST: build characteristics, deployment context, risk profile |

---

## Integration with Other Skills

| When You're Doing | Also Use | For |
|-------------------|----------|-----|
| Designing Python architecture | `axiom-python-engineering` | Python-specific patterns and idioms |
| Designing web API | `axiom-web-backend` | REST/GraphQL best practices |
| Making architecture decision | `governance-and-risk` | Formal DAR process for critical choices |
| Setting up testing | `quality-assurance` | Test strategy and coverage |
| Choosing platforms | `platform-integration` | GitHub vs Azure DevOps specifics |

---

## Real-World Impact

**Without this skill**: Teams experience:
- Undocumented architecture decisions that haunt future developers
- Resume-driven design leading to over-engineered solutions
- Git chaos with daily conflicts and lost work
- Debt spirals consuming 70%+ of time
- Emergency shortcuts becoming permanent anti-patterns

**With this skill**: Teams achieve:
- Defensible audit trail through ADRs
- Technology choices driven by requirements, not hype
- Structured configuration management reducing conflicts by 80%+
- Early crisis detection preventing debt spirals
- Emergency protocols that maintain governance without blocking urgency

---

## Next Steps

1. **Determine project level**: Check CLAUDE.md or ask user for CMMI target level (default: Level 3)
2. **Identify situation**: Use Quick Reference table to find relevant reference sheet
3. **Load reference sheet**: Read detailed guidance for specific domain
4. **Enforce ADR requirements**: Level 3 requires ADR for architectural decisions - no exceptions without HOTFIX protocol
5. **Apply decision frameworks**: Use systematic evaluation, not gut feelings or hype
6. **Counter anti-patterns**: Watch for resume-driven design, debt spirals, cowboy coding
7. **Measure success**: Establish baseline, set targets, schedule retrospectives

**Remember**: "Best practice" is never justification. Requirements are. If you can't articulate the requirement, you can't justify the architecture.
