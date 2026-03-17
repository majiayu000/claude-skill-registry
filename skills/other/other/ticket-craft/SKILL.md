---
name: ticket-craft
description: Create Jira/Asana/Linear tickets optimized for Claude Code execution - AI-native ticket writing
---

# Ticket Craft Skill

*Write software tickets that AI agents can execute autonomously.*

**Purpose:** Define a ticket format that combines software engineering best practices (INVEST, Given-When-Then, Definition of Ready) with Claude Code-specific context requirements. Every ticket created with this skill is "Claude Code Ready" - meaning an agent can pick it up and execute it without asking clarifying questions.

**Works with:** Jira, Asana, Linear, GitHub Issues, or any ticket system.

---

## Core Principle

```
┌─────────────────────────────────────────────────────────────────┐
│  A TICKET IS A PROMPT                                            │
│  ──────────────────────────────────────────────────────────────  │
│                                                                  │
│  Traditional tickets are written for humans who can:             │
│  - Ask clarifying questions in Slack                             │
│  - Draw on institutional knowledge                               │
│  - Infer intent from vague descriptions                          │
│                                                                  │
│  AI agents cannot do any of this.                                │
│                                                                  │
│  Every ticket must be SELF-CONTAINED:                            │
│  - Explicit file references (not "the auth module")              │
│  - Pattern references (not "follow our conventions")             │
│  - Verification criteria (not "make sure it works")              │
│  - Constraints (not just what to do, but what NOT to do)         │
│  - Test commands (not "run the tests")                           │
│                                                                  │
│  If Claude Code can execute it without asking a question,        │
│  the ticket is ready. If it can't, it's not.                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## The INVEST+C Criteria

Standard INVEST plus **C for Claude-Ready**:

| Criterion | Question | Fails If... |
|-----------|----------|-------------|
| **I** - Independent | Can this be completed without waiting on another ticket? | Blocked by undocumented dependencies |
| **N** - Negotiable | Is there room to adjust implementation approach? | Over-specifies implementation details |
| **V** - Valuable | Can you articulate who benefits and how? | No clear user or business value |
| **E** - Estimable | Does the team understand enough to size it? | Too vague or too large to estimate |
| **S** - Small | Can one person finish this in 1-3 days? | More than 5 acceptance criteria |
| **T** - Testable | Can you write a pass/fail test for it? | Uses vague language like "fast" or "good UX" |
| **C** - Claude-Ready | Can an AI agent execute this without clarifying questions? | Missing file refs, patterns, verification, or constraints |

---

## Ticket Types

### 1. Feature Ticket

```markdown
## [PROJ-XXX] {Verb} {Feature} for {User}

**Type:** Feature
**Priority:** {Critical | High | Medium | Low}
**Points:** {1 | 2 | 3 | 5 | 8}
**Labels:** {frontend, backend, api, database, etc.}
**Epic:** {Parent epic}

---

### User Story
As a {specific persona},
I want to {specific action},
so that {measurable benefit}.

### Background
{1-2 paragraphs on why this matters. Link to product brief, user research,
or business justification. Include any relevant metrics or user feedback.}

### Acceptance Criteria

**AC1: {Happy path scenario}**
Given {precondition},
when {action},
then {expected result}.

**AC2: {Edge case / error scenario}**
Given {precondition},
when {action},
then {expected result}.

**AC3: {Boundary condition}**
Given {precondition},
when {action},
then {expected result}.

### Out of Scope
- {Explicitly state what this ticket does NOT include}
- {Prevents scope creep and keeps ticket small}

---

### Claude Code Context

#### Relevant Files (read these first)
- `src/services/example.ts` - Existing service to extend
- `src/models/example.ts` - Data model definition
- `src/api/routes/example.ts` - Existing endpoint patterns to follow

#### Pattern Reference
Follow the pattern in `src/services/user.ts` for service layer implementation.
Follow the pattern in `src/api/routes/users.ts` for route definition.
Follow the pattern in `tests/services/user.test.ts` for test structure.

#### Database Changes
- {Table to create/modify, columns, types}
- {Migration file location: `supabase/migrations/` or `prisma/migrations/`}
- {RLS policies if using Supabase}

#### API Contract
```
POST /api/{resource}
Request: { field1: string, field2: number }
Response: { id: string, field1: string, created_at: string }
Error: { error: string, code: number }
```

#### Constraints
- Do NOT modify {specific files or modules}
- Do NOT add new dependencies without approval
- Follow existing error handling in `src/core/exceptions.ts`
- {Any performance budgets: response time < 200ms, bundle size < 50KB}

#### Verification
```bash
# Run specific tests
npm test -- --grep "{feature name}"

# Lint check
npm run lint

# Type check
npm run typecheck

# Full validation
npm test -- --coverage
```

#### Environment Variables
- Existing: {list vars already in .env that are relevant}
- New required: {list any new vars needed}

---

### Dependencies
- Blocked by: {PROJ-XXX} ({brief description})
- Blocks: {PROJ-YYY} ({brief description})

### Design
- Mockup: {link to Figma/design if applicable}
```

---

### 2. Bug Ticket

```markdown
## [BUG-XXX] Fix: {Component} - {Symptom}

**Type:** Bug
**Priority:** {Critical | High | Medium | Low}
**Points:** {1 | 2 | 3 | 5}
**Labels:** {regression, ux-bug, data-bug, security-bug}
**Severity:** {Blocks users | Degrades experience | Cosmetic}

---

### Bug Summary
{One sentence: what is broken and who is affected.}

### Environment
- Browser/OS: {e.g., Chrome 120 / macOS 14.2}
- Environment: {Production | Staging | Local}
- User type: {Anonymous | Authenticated | Admin}
- First observed: {date}

### Steps to Reproduce
1. {Navigate to / perform action}
2. {Perform next action}
3. {Perform next action}
4. **Observe:** {incorrect behavior}

### Expected Behavior
{What should happen instead.}

### Actual Behavior
{What actually happens. Include error messages, console output, screenshots.}

### Impact
- Users affected: {percentage or count}
- Frequency: {every time | intermittent | specific conditions}
- Workaround: {exists / none}

---

### Claude Code Context

#### Suspected Root Cause
{Where the bug likely lives, if known.}
- File: `src/components/LoginForm.tsx:87`
- Issue: `isSubmitting` state set to `true` on validation error but never reset

#### Relevant Files
- `src/components/LoginForm.tsx` - Form component with the bug
- `tests/components/LoginForm.test.tsx` - Existing tests (gap here)
- `src/hooks/useAuth.ts` - Auth hook used by the form

#### Test Gap Analysis
- Existing tests cover: {what's currently tested}
- Missing test: {what test would have caught this bug}

#### Bug Fix Workflow (TDD)
1. Write a failing test that reproduces the bug
2. Verify the test fails (confirms the bug exists)
3. Fix the bug with minimum code change
4. Verify the test passes
5. Run full test suite to check for regressions

#### Verification
```bash
# Run the specific test
npm test -- --grep "LoginForm submit"

# Run related tests
npm test -- src/components/LoginForm.test.tsx

# Full regression check
npm test
```

#### Constraints
- Fix the bug only - do NOT refactor surrounding code
- Do NOT change the component's public API
- Ensure all existing tests continue to pass
```

---

### 3. Tech Debt Ticket

```markdown
## [TECH-XXX] Refactor: {Area} - {Improvement}

**Type:** Tech Debt
**Priority:** {High | Medium | Low}
**Points:** {3 | 5 | 8}
**Labels:** {refactor, performance, maintainability, testing}

---

### Problem Statement
{What is wrong with the current implementation and why it matters.
Include concrete pain points: slow CI, frequent bugs, developer confusion.}

### Current State
- File: `{path}` ({N} lines)
- Test coverage: {X}%
- Cyclomatic complexity: {N}
- Related bugs: {PROJ-XXX, PROJ-YYY}
- Pain frequency: {how often this causes issues}

### Proposed Change
{What specifically should change and why this approach.}

### Acceptance Criteria
- [ ] {Specific structural change completed}
- [ ] All existing tests pass without modifying test assertions
- [ ] No public API changes (existing consumers unaffected)
- [ ] Test coverage >= {X}%
- [ ] {Measurable improvement metric}

### Risk Assessment
- Risk level: {Low | Medium | High}
- Mitigation: {run full regression, deploy behind flag, etc.}

### Business Justification
{Why this is worth doing now. E.g., "Reduces average bug fix time from 4h to 1h"
or "Enables upcoming feature PROJ-XXX which requires clean separation."}

---

### Claude Code Context

#### Relevant Files
- `{file}` - Current implementation to refactor
- `{test file}` - Existing tests (must not break)
- `{dependent file}` - Consumer of the API being refactored

#### Pattern Reference
Follow the pattern established in `{good example file}` for the new structure.

#### Constraints
- Do NOT change public APIs or exports
- Do NOT modify test assertions (tests should pass as-is)
- Do NOT introduce new dependencies
- Keep backwards compatibility

#### Verification
```bash
# Existing tests must pass unchanged
npm test

# No type errors
npm run typecheck

# Lint clean
npm run lint

# Coverage target
npm test -- --coverage
```
```

---

### 4. Epic Breakdown Ticket

```markdown
## [EPIC-XXX] {Epic Name}

**Type:** Epic
**Priority:** {Critical | High | Medium}
**Target:** {Sprint/milestone}

---

### Objective
{One paragraph: what this epic achieves and why it matters.}

### Success Metrics
- {Measurable outcome 1}
- {Measurable outcome 2}

### User Workflows
{The user journey this epic covers, broken into steps.}
1. {Step 1: Discovery/Entry}
2. {Step 2: Core Action}
3. {Step 3: Completion/Result}

### Ticket Breakdown

| # | Ticket | Type | Points | Dependencies |
|---|--------|------|--------|-------------|
| 1 | {title} | Feature | 3 | None |
| 2 | {title} | Feature | 5 | #1 |
| 3 | {title} | Feature | 3 | None |
| 4 | {title} | Feature | 2 | #2, #3 |
| 5 | {title} | Tech Debt | 3 | None |

### Slicing Strategy
{How the epic was broken down. Reference the technique used.}

### Agent Team Mapping
{If using agent teams, how features map to agents.}
- Feature Agent 1: Tickets #1, #2
- Feature Agent 2: Tickets #3, #4
- Parallel execution: #1 and #3 can run simultaneously
- Sequential: #2 depends on #1, #4 depends on #2 and #3
```

---

## Epic Slicing Techniques

When breaking an epic into tickets, use one of these strategies:

| Technique | When to Use | Example |
|-----------|-------------|---------|
| **By workflow step** | Clear user journey | Browse > Play > Save > Share |
| **By data variation** | Multiple data types | Text posts, images, videos |
| **By user role** | Different permissions | Anonymous, authenticated, admin |
| **By CRUD** | Data operations | Create, Read, Update, Delete |
| **Happy path first** | Incremental delivery | Success flow first, then errors |
| **By boundary** | System integration | Frontend, API, database separately |

### Rules of Thumb
- Each ticket: **1-3 days** of work for one developer/agent
- More than **5 acceptance criteria** = split the ticket
- More than **8 story points** = definitely split
- Every ticket should be **independently deployable** (even behind a flag)
- Order tickets: **simplest, most foundational first**

---

## The Claude Code Ready Checklist

Before a ticket is ready for an AI agent to execute, verify:

```
┌─────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE READY CHECKLIST                                     │
│  ──────────────────────────────────────────────────────────────  │
│                                                                  │
│  CONTEXT                                                         │
│  ☐ Relevant files listed with full paths                         │
│  ☐ Pattern reference points to a real file to follow             │
│  ☐ API contract defined (request/response shapes)                │
│  ☐ Database changes specified (tables, columns, migrations)      │
│  ☐ Environment variables listed (existing + new)                 │
│                                                                  │
│  SCOPE                                                           │
│  ☐ Out of Scope section explicitly states what NOT to do         │
│  ☐ Constraints section lists files/modules NOT to modify         │
│  ☐ Ticket covers one logical change (atomic)                     │
│  ☐ Estimable at ≤ 5 story points                                │
│                                                                  │
│  VERIFICATION                                                    │
│  ☐ Test command provided (exact command, not "run tests")        │
│  ☐ Lint command provided                                         │
│  ☐ Typecheck command provided                                    │
│  ☐ Acceptance criteria are Given-When-Then or checkboxed         │
│  ☐ Each criterion is independently pass/fail testable            │
│                                                                  │
│  QUALITY                                                         │
│  ☐ Title is imperative verb + object + context                   │
│  ☐ Title under 80 characters                                     │
│  ☐ Description explains WHY, not just WHAT                       │
│  ☐ 2-5 acceptance criteria (not more)                            │
│  ☐ No vague language ("fast", "good UX", "clean")               │
│                                                                  │
│  If any box is unchecked, the ticket is NOT ready.               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns (Never Do These)

### 1. The Title-Only Ticket
```
Title: Fix login
Description: (empty)
```
**Why it fails:** No context, no acceptance criteria, no file references. Claude Code will guess and likely guess wrong.

### 2. The Novel
```
Title: Implement new onboarding
Description: (3 pages mixing UI, backend, analytics, email, and future ideas)
```
**Why it fails:** Not small, not independent. Agent teams can't parallelize this. Split into 5+ tickets.

### 3. The Vague Requirement
```
Acceptance Criteria:
- Should be fast
- UX should be good
- Should work on mobile
```
**Why it fails:** Unmeasurable, untestable. Replace with: "Response time < 200ms", "Passes WCAG 2.1 AA", "No horizontal scroll at 320px viewport."

### 4. The Over-Specified Solution
```
Title: Use Redis to cache user sessions
Description: Install Redis, configure connection pooling, set TTL to 3600...
```
**Why it fails:** Prescribes the solution instead of the problem. Should describe "Session lookups take 500ms, need < 50ms" and let the agent choose the approach.

### 5. The Missing Files Ticket
```
Description: Update the auth module to support OAuth.
```
**Why it fails for AI:** "The auth module" could be 20 files. Claude Code needs: `src/services/auth.ts`, `src/middleware/auth.ts`, `src/routes/auth.ts` - specific paths.

### 6. The No-Verification Ticket
```
Acceptance Criteria:
- OAuth login works
- Users can sign in with Google
```
**Why it fails:** No test command, no verification steps. Claude Code performs dramatically better when it can verify its own work.

---

## Good vs Bad Examples

### Bad: Vague Feature Ticket
```
Title: Add rate limiting to the API
Description: We need rate limiting on our endpoints.
```

### Good: Claude Code Ready Feature Ticket
```
Title: Add sliding window rate limiter to /api/generate endpoint

User Story:
As an API consumer, I want requests to be rate-limited
so that the service remains available under heavy load.

Acceptance Criteria:
AC1: Given an authenticated user making requests,
     when they exceed 10 requests per minute,
     then return 429 with Retry-After header.

AC2: Given a rate-limited user,
     when the window expires,
     then requests succeed again.

AC3: Given an unauthenticated request,
     when it hits /api/generate,
     then return 401 (rate limiting only applies to authed users).

Claude Code Context:
- Pattern: Follow `src/middleware/throttle.ts` for middleware structure
- File: Create `src/middleware/rateLimit.ts`
- Test: Create `tests/middleware/rateLimit.test.ts`
- Route: Modify `src/api/routes/generate.ts` to add middleware
- Constraint: Do NOT modify existing middleware or other endpoints

Verification:
  npm test -- --grep "rate-limit"
  npm run lint
  npm run typecheck
```

---

## Mapping Tickets to Agent Teams

When using the agent-teams workflow, tickets map directly to the 10-task pipeline:

| Ticket Section | Maps To | Agent |
|---------------|---------|-------|
| Title + Description | Task 1: `{name}-spec` | Feature Agent |
| Acceptance Criteria | Task 3: `{name}-tests` | Feature Agent (writes tests from AC) |
| Pattern Reference | Task 5: `{name}-implement` | Feature Agent (follows pattern) |
| Verification section | Task 6-7: verify + validate | Quality Agent + Feature Agent |
| Constraints | Enforced throughout | All agents |
| Claude Code Context | Loaded at start | Feature Agent reads first |

### Ticket → Agent Team Flow
```
1. Create ticket using templates above
2. Ticket becomes the feature spec in _project_specs/features/
3. Team Lead reads spec, creates 10-task dependency chain
4. Feature Agent uses ticket's Claude Code Context to start
5. Quality Agent uses ticket's Acceptance Criteria to verify
6. Review Agent reviews against ticket's Constraints
7. Security Agent scans based on ticket's scope
8. Merger Agent creates PR referencing the ticket ID
```

---

## Ticket Title Conventions

| Type | Format | Example |
|------|--------|---------|
| Feature | `Add {feature} for {user}` | Add episode bookmarking for listeners |
| Enhancement | `Improve {what} in {where}` | Improve search performance in episode feed |
| Bug | `Fix: {Component} - {Symptom}` | Fix: PlayerBar - audio stops on tab switch |
| Tech Debt | `Refactor: {Area} - {Goal}` | Refactor: AuthService - extract token management |
| Security | `Security: {What} in {Where}` | Security: add input sanitization to comment API |
| Chore | `Chore: {What}` | Chore: upgrade React from 18 to 19 |

**Rules:**
- Start with an imperative verb (Add, Fix, Improve, Refactor, Remove)
- Under 80 characters
- Include the component/area affected
- Be specific enough to distinguish from other tickets

---

## Story Points for AI Agents

AI agents estimate differently than humans. Use this calibration:

| Points | Scope | Agent Time | Example |
|--------|-------|-----------|---------|
| **1** | Single file, < 20 lines changed | ~5 min | Fix a typo, update a config value |
| **2** | 1-2 files, straightforward | ~15 min | Add a field to a form, update an API response |
| **3** | 2-4 files, clear path | ~30 min | New API endpoint following existing pattern |
| **5** | 4-8 files, some decisions | ~1 hour | New feature with tests, models, and routes |
| **8** | 8+ files, complex | ~2 hours | Integration with external service, new data model |
| **13** | Too large, split required | - | Full authentication system, major refactor |

**Rule:** If > 5 points, consider splitting. If 13, always split.

---

## Integration with Ticket Systems

### Jira
- Use custom field "Claude Code Context" for the AI-specific section
- Use labels: `claude-ready`, `needs-context`, `ai-blocked`
- Link tickets with "blocks/blocked by" for dependency chains

### Asana
- Use custom fields for Priority, Points, Type
- Use subtasks for the 10-task pipeline steps
- Use tags: `claude-ready`, `needs-refinement`

### Linear
- Use issue templates with the Claude Code Context section built-in
- Use labels for ticket type and claude-readiness
- Use projects to group tickets into epics

### GitHub Issues
- Use issue templates (`.github/ISSUE_TEMPLATE/`)
- Use labels: `feature`, `bug`, `tech-debt`, `claude-ready`
- Use milestones for epics

---

## Command: /create-ticket

When the user asks to create a ticket, follow this workflow:

### Step 1: Gather Context
Ask the user:
1. What type? (Feature / Bug / Tech Debt)
2. Brief description of what needs to be done
3. Which part of the codebase is involved?

### Step 2: Auto-Detect Context
- Read the relevant files to understand current implementation
- Identify the pattern to follow from existing code
- Find existing tests to understand test conventions
- Check for related files that might be affected

### Step 3: Generate Ticket
Use the appropriate template above, filling in:
- All Claude Code Context fields (auto-detected)
- Acceptance criteria (derived from description)
- Verification commands (from project's CLAUDE.md or package.json)
- Constraints (based on codebase analysis)

### Step 4: Validate with Checklist
Run the Claude Code Ready Checklist against the generated ticket.
Flag any unchecked items for the user to address.

### Step 5: Output
Present the ticket in the template format, ready to paste into Jira/Asana/Linear.

---

## Definition of Ready (for Sprint)

A ticket can enter a sprint when:

- [ ] Passes INVEST+C criteria
- [ ] Claude Code Ready Checklist is complete
- [ ] Dependencies are identified and unblocked
- [ ] Story points assigned
- [ ] Design/mockups attached (if applicable)
- [ ] Acceptance criteria reviewed by team

## Definition of Done

A ticket is done when:

- [ ] All acceptance criteria verified (pass/fail)
- [ ] Tests written and passing
- [ ] Code reviewed (no Critical/High issues)
- [ ] Security scan passed
- [ ] Lint and typecheck clean
- [ ] Coverage >= 80% for new code
- [ ] PR created with full pipeline results
- [ ] Documentation updated (if applicable)
