---
name: specify
version: "1.0.0"
description: "This skill should be used when the user asks to 'specify a feature', 'write requirements', 'define what we're building', 'capture requirements', 'document the spec', or before invoking /architecture-tech-lead for non-trivial features. Produces formal specifications (WHAT/WHY) that feed into architecture and planning phases."
---

# Specify - Requirements Before Design

Formalize requirements into structured specifications before architecture/planning. Focus exclusively on WHAT and WHY - never HOW.

**Position in flow:** `/brainstorming` → `/specify` → `/clarify` (auto) → `/architecture-tech-lead` → `/task-planner`

---

## Arguments

- `/specify "feature description"` - Create new specification
- `/specify --update` - Update existing spec with new info
- `/specify --status` - Show spec completeness

---

## Output

Creates `.claude/specs/{YYYY-MM-DD}-{slug}/spec.md`

Structure:
```
.claude/specs/2025-01-29-user-auth/
├── spec.md          # Main specification
└── clarifications/  # Resolved uncertainty log (created by /clarify)
```

---

## Specification Process

### 1. Extract Short Name

From description, derive 2-4 word slug:
- Action-noun format: `user-auth`, `email-validation`, `payment-flow`
- Preserve technical terms
- Lowercase, hyphenated

### 2. Explore Context

Before writing spec:
- Check existing specs: `ls .claude/specs/`
- Review related code areas
- Understand current state

### 3. Write Specification

Load `references/spec-template.md` and populate sections.

**Critical constraint:** Spec describes WHAT users need and WHY. NO implementation details:
- No tech stack mentions
- No API designs
- No database schemas
- No framework references
- No code patterns

If tempted to write HOW, mark as `[NEEDS CLARIFICATION: technical approach TBD]` and move on.

### 4. Mark Uncertainties

For ANY ambiguity, use marker syntax:

```markdown
- FR-003: System MUST validate user input [NEEDS CLARIFICATION: validation rules undefined]
```

Categories of uncertainty:
- **Business logic** - rules, thresholds, behaviors
- **Scope boundaries** - what's in/out
- **Edge cases** - error states, limits
- **Technical** - feasibility questions (arch-lead resolves these)
- **User expectations** - unclear acceptance criteria

### 5. Auto-Trigger Clarify

After writing spec, count markers:

```bash
grep -c "NEEDS CLARIFICATION" .claude/specs/*/spec.md
```

If count > 3: Invoke `/clarify` before proceeding.

If count <= 3: Note markers for arch-lead to address during research phase.

---

## Spec Template Reference

See `references/spec-template.md` for full template. Key sections:

### User Scenarios (Required)

```markdown
## User Scenarios

### US1: [P1] Account Creation
**As a** new user
**I want to** create an account with email
**So that** I can access personalized features

**Why P1:** Core functionality, blocks all other features

**Acceptance Scenarios:**
- Given valid email and password, When I submit, Then account is created and confirmation sent
- Given existing email, When I submit, Then error shown with login link
- Given weak password, When I submit, Then requirements shown inline
```

Priority levels:
- **P1** - Must have, blocks other work
- **P2** - Should have, significant value
- **P3** - Nice to have, defer if needed

### Functional Requirements (Required)

```markdown
## Functional Requirements

- FR-001: System MUST allow email/password registration
- FR-002: System MUST send confirmation email within 60 seconds
- FR-003: System MUST enforce password policy [NEEDS CLARIFICATION: policy rules]
- FR-004: System SHOULD support OAuth providers [NEEDS CLARIFICATION: which providers?]
```

Use MUST/SHOULD/MAY (RFC 2119):
- **MUST** - Absolute requirement
- **SHOULD** - Strong recommendation, exceptions need justification
- **MAY** - Optional, nice-to-have

### Success Criteria (Required)

```markdown
## Success Criteria

- SC-001: 95% of registrations complete without error
- SC-002: Confirmation emails delivered within 60 seconds (p95)
- SC-003: Password validation feedback in <100ms
- SC-004: Zero accounts created with invalid email format
```

Criteria MUST be:
- **Measurable** - specific numbers, not "fast" or "reliable"
- **Verifiable** - can write test/metric for it
- **Technology-agnostic** - no "Redis cache hit rate"

### Out of Scope (Required)

```markdown
## Out of Scope

Explicitly NOT part of this feature:
- Social login (separate spec)
- Account deletion (future work)
- Profile editing (separate spec)
- Admin user management
```

Prevents scope creep during implementation.

---

## Quality Checks

Before finalizing spec, verify:

| Check | Criteria |
|-------|----------|
| No HOW | Zero tech stack, API, or implementation mentions |
| Testable | Every FR has clear pass/fail condition |
| Measurable | Every SC has specific metric |
| Scoped | Out of Scope section populated |
| Prioritized | All user scenarios have P1/P2/P3 |
| Uncertain marked | Ambiguities use `[NEEDS CLARIFICATION]` |

---

## Handoff to Architecture

When spec is ready (markers <= 3 or clarified):

1. Commit spec: `git add .claude/specs/ && git commit -m "spec: {slug}"`
2. Invoke arch-lead: `/architecture-tech-lead`
3. Arch-lead reads spec, produces plan with technical decisions

Arch-lead resolves technical uncertainties during research phase.

---

## Constraints

- NEVER include implementation details
- NEVER skip User Scenarios section
- NEVER use vague success criteria ("fast", "reliable")
- ALWAYS mark uncertainties explicitly
- ALWAYS include Out of Scope section
- Auto-trigger /clarify if >3 markers
