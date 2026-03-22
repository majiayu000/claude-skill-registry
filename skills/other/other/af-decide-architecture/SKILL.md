---
name: af-decide-architecture
description: Make architectural decisions and create ADRs for technology trade-offs. Use when reviewing code for architectural compliance, documenting decision context, or evaluating architecture patterns.

title: Architecture Expertise
created: 2026-01-05
updated: 2026-01-06
last_checked: 2026-01-06
tags: [skill, expertise, architecture, adr, patterns, decisions]
parent: ../README.md
related:
  - ../af-setup-gaininsight-stack/SKILL.md
  - ../af-build-amplify-features/SKILL.md
  - ../../templates/adr-template.md
  - ../../templates/adr-index.md
---

# Architecture Expertise

Guidance for making, documenting, and enforcing architectural decisions in consumer projects.

## When to Use This Skill

Load this skill when you need to:
- Decide if a change warrants an ADR
- Create or update an ADR
- Review code changes for architectural compliance
- Understand existing architectural decisions quickly
- Detect architectural drift from documented decisions

**Common triggers:**
- Discovery phase: Creating initial project ADRs
- Refinement phase: Reviewing architecture for complex features
- Delivery phase: Checking if implementation introduces new patterns
- Git commit hook: "Does this align with existing ADRs?"

---

## Rules

### Critical Rules (MUST)

1. **MUST read ADR index before making architectural decisions.** The index at `docs/architecture/adr/README.md` provides quick context without reading all ADRs.

2. **MUST create an ADR when** the decision:
   - Affects multiple components or layers
   - Involves choosing between significantly different approaches
   - Is hard to reverse once implemented
   - Would make future developers ask "why did we do this?"

3. **MUST follow ADR lifecycle.** Status transitions: `Proposed → Accepted → [Active | Superseded | Deprecated]`

4. **MUST update ADR index when ADRs change.** The index is the quick reference - keep it current.

5. **MUST document alternatives considered.** An ADR without alternatives isn't a decision record.

### Process Rules (SHOULD)

6. **SHOULD create ADRs in Discovery phase.** Initial architectural decisions (tech stack, integrations, auth) happen early.

7. **SHOULD reference existing ADRs in mini-PRDs.** Section 6 of mini-PRD lists related ADRs.

8. **SHOULD use architecture-quality-agent for complex reviews.** Invoke when many files changed or patterns modified.

9. **SHOULD propose ADR before implementing new patterns.** Don't let code outpace documentation.

### Quality Rules (MAY)

10. **MAY defer ADR for experimental code.** Spikes and prototypes can precede formal ADRs.

11. **MAY supersede rather than modify.** If decision fundamentally changes, create new ADR and mark old as superseded.

---

## ADR Decision Framework

### When to Create an ADR

```
Is this decision...
├── Affecting multiple components? ─────────────► YES → Create ADR
├── Choosing between different approaches? ─────► YES → Create ADR
├── Hard to reverse once implemented? ──────────► YES → Create ADR
├── Something future devs would question? ──────► YES → Create ADR
└── None of the above? ─────────────────────────► NO  → Document in code/comments
```

### ADR Sizing

| Scope | ADR Needed? | Example |
|-------|-------------|---------|
| Library choice | Maybe | "Why lodash vs native?" - probably not. "Why Redux vs Context?" - yes |
| Data model design | Yes | Table structure, relationships, indexing strategy |
| Authentication approach | Yes | Cognito vs Auth0, session vs JWT |
| API design pattern | Yes | REST vs GraphQL, BFF pattern |
| Infrastructure choice | Yes | Amplify vs custom, serverless vs containers |
| Code organization | Maybe | Folder structure - probably not. Monorepo vs polyrepo - yes |

---

## Workflows

### Workflow: Reading Architectural Context

**When:** Starting work on a feature or reviewing changes

**Procedure:**
1. Read ADR index: `docs/architecture/adr/README.md`
2. Note relevant decisions from the "Decision Summary" table
3. Only read full ADRs if you need deeper context
4. Proceed with awareness of architectural constraints

**Context economics:** Index is ~50 lines. Full ADRs are ~100+ lines each.

### Workflow: Creating an ADR

**When:** Making a significant architectural decision

**Procedure:**
1. Copy template: `cp .claude/templates/adr-template.md docs/architecture/adr/adr-XXX-[name].md`
2. Fill in all sections - especially "Options Considered"
3. Set status to "Proposed"
4. Add to ADR index (children array + tables)
5. Get human approval before changing status to "Accepted"
6. Update index "Decision Summary" with one-line summary

**Success criteria:**
- Template fully populated
- At least 2 alternatives documented
- Index updated with summary
- Human approved

### Workflow: Architecture Review (Pre-Commit)

**When:** Git commit hook prompts about architecture

**Procedure:**
1. Read ADR index for current decisions
2. Check if changes introduce new patterns not covered by ADRs
3. Check if changes contradict existing ADRs
4. If new pattern needed: propose ADR before proceeding
5. If aligned: proceed with commit

**Quick check questions:**
- Does this add a new library/framework? → Check for existing ADR
- Does this change data access patterns? → Check data ADRs
- Does this modify authentication flow? → Check auth ADRs
- Does this introduce a new API pattern? → Check API ADRs

### Workflow: Using Architecture Quality Agent

**When:** Complex changes across many files, or periodic architecture audit

**Invocation:**
```
Task tool → af-architecture-quality-agent
Input: Validation scope (discovery | requirements | delivery | full)
Output: ADRs validated, issues found, drift detected
```

**When to invoke:**
- Multiple ADRs affected by changes
- Quarterly architecture review
- Before major releases
- After significant refactoring

---

## Common Architectural Decisions

### For GainInsight Standard Projects

These are typical decisions - use as starting points, not prescriptions:

| Area | Common Decision | Why | ADR Template Section |
|------|-----------------|-----|---------------------|
| **Authentication** | Cognito with custom attributes | Managed service, tenant isolation via claims | Auth, Security |
| **Data Storage** | DynamoDB single-table | Scalability, cost, Amplify integration | Data layer |
| **API Layer** | AppSync + Lambda resolvers | GraphQL, real-time, managed | API, Integration |
| **Multi-tenancy** | Row-level via `tenant_id` | Simpler than schema-per-tenant | Security, Data |
| **Business Logic** | Lambda-first | IAM permissions, testability, audit | API, Architecture |
| **Frontend State** | React Context + Amplify hooks | Simplicity, Amplify integration | Frontend |

### Decision Trade-offs to Document

**Authentication:**
- Cognito: Managed, AWS-integrated, limited customization
- Auth0: More features, additional cost, external dependency

**Multi-tenancy:**
- Row-level: Simpler, shared resources, careful about queries
- Schema-per-tenant: Isolation, complexity, cost scaling

**API:**
- AppSync: Managed GraphQL, subscriptions, limited custom logic
- API Gateway + Lambda: More control, more configuration

---

## Phase Integration

### Discovery Phase
- **Create:** Initial ADRs for tech stack, integrations, auth
- **Output:** `docs/architecture/adr/` with 3-5 foundational ADRs
- **Index:** Populated with decision summaries

### Refinement phase
- **Reference:** Mini-PRD Section 6 lists related ADRs
- **Review:** Architecture agent validates complex features
- **Update:** ADRs if requirements reveal new constraints

### Delivery Phase
- **Check:** Git hook prompts for ADR alignment
- **Enforce:** Implementation follows documented decisions
- **Evolve:** New patterns → new ADRs before merging

### Quality (Cross-Phase)
- **Validate:** Architecture agent checks ADR compliance
- **Detect:** Identify drift between code and ADRs
- **Maintain:** Keep index current, archive outdated ADRs

---

## Common Pitfalls

### 1. ADR Without Alternatives
**Problem:** "We decided to use X" without explaining why not Y or Z.
**Solution:** Always document at least 2 alternatives, even if one is "do nothing."

### 2. Stale ADR Index
**Problem:** Index doesn't reflect current ADRs.
**Solution:** Update index whenever ADRs change. It's the quick reference.

### 3. Code Outpaces Documentation
**Problem:** New patterns in code without corresponding ADRs.
**Solution:** Propose ADR before implementing. Use git hook as reminder.

### 4. Over-ADR'ing
**Problem:** ADR for every small decision clutters the record.
**Solution:** Use the decision framework. Not everything needs an ADR.

### 5. Ignoring Superseded ADRs
**Problem:** Old decisions still referenced, causing confusion.
**Solution:** Mark as superseded, link to replacement, update index.

---

## Templates

| Template | Purpose | Location |
|----------|---------|----------|
| ADR Template | Individual decision record | `.claude/templates/adr-template.md` |
| ADR Index | Summary for quick reference | `.claude/templates/adr-index.md` |

## Essential Reading

- [Amplify Expertise](../af-build-amplify-features/SKILL.md) - Four-tier architecture patterns
- [GainInsight Standard](../af-setup-gaininsight-stack/SKILL.md) - Infrastructure patterns
- [Architecture Quality Agent](../../agents/af-architecture-quality-agent.md) - Automated validation

---

**Remember:**
1. Read index first, full ADRs only when needed
2. Create ADR before implementing new patterns
3. Document alternatives, not just decisions
4. Keep index current - it's the agent's quick reference
