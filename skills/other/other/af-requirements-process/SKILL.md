---
name: af-requirements-process
description: Use when transforming Linear features into detailed Behaviour specifications, creating mini-PRDs, or preparing features for implementation. Covers Three Amigos analysis, 8-section mini-PRD template, and human approval gates.

# AgentFlow documentation fields
title: Requirements Process
created: 2025-10-29
updated: 2026-02-26
last_checked: 2026-02-26
tags: [skill, process, requirements, behaviour, mini-prd]
parent: ../README.md
---

# Requirements Process

## Quick Reference

The requirements process transforms Linear features from Discovery into comprehensive mini-PRDs with Behaviour scenarios, visual designs, and complete technical specifications. This is the critical bridge between understanding what to build (Discovery) and building it (Delivery).

**Typical duration:** 2-6 hours per feature
**End result:** Mini-PRD, Markdown scenarios, Storybook stories, RTL tests, Selector contract

## When to Use

**✅ Use Requirements Process for:**
- Transforming Linear features into detailed specifications
- Creating Behaviour scenarios from acceptance criteria
- Defining technical implementation approaches
- Preparing features for Delivery phase

**❌ Not Requirements Phase:**
- Product-level exploration (use Discovery)
- Implementation work (use Delivery)
- Bug fixes without new behavior (go directly to Delivery)

## Git Workflow

**Requirements work happens on the `specs` branch** (see ADR-009).

```bash
# Start refinement on a specific issue
start-refine myproject LIN-123  # Creates/attaches to specs worktree + tmux
```

The `specs` branch is shared by PM, UX, and QA for all pre-implementation work. During Requirements:

| Role | Creates | Location |
|------|---------|----------|
| PM | Mini-PRD | `specs/{issue}/prd.md` |
| UX | Visual designs, Storybook | `specs/{issue}/design.md`, `stories/` |
| QA | Behaviour scenarios | `specs/{issue}/scenarios.md` |

**When Requirements complete (before approval):**
1. Merge specs into `develop` (direct merge, no PR — documents don't need CI)
2. THEN approve the issue in Linear (status → "Approved")
3. "Approved" means develop is ready — specs are already there
4. SE creates issue branch via `start-work` (branches from develop with specs included)

### Trunk-Based Projects

Projects configured with `branching.strategy: trunk-based` work directly on the main branch instead of a specs branch. For these projects:
- `start-refine` uses the main working directory (no specs worktree)
- All Requirements artifacts go directly to the trunk branch
- The workflow is otherwise identical

See [Work Management Guide](../../docs/guides/work-management.md#branch-strategy-adr-009) for full branching details.

## Core Principles

### What is a Feature?

A Feature is an **atomic unit of work** - one thing, front-to-back:

| A Feature IS | A Feature is NOT |
|--------------|------------------|
| One unit of functionality | A collection of loosely related work |
| Front-to-back (UI → backend → database) | Just the backend OR just the frontend |
| Complete with all edge cases | Just the happy path |
| Independently deliverable | Dependent on incomplete features |

**Each Feature gets:**
- ONE Linear Issue
- ONE Mini-PRD
- ONE E2E test file
- All its scenarios (happy path + errors + edge cases)

See [Atomic Requirements Guide](../../docs/guides/atomic-requirements-guide.md) for outside-in development and full hierarchy.

### 1. Three Amigos Analysis

Every feature MUST be analyzed from three perspectives:

**Business Perspective:**
- What value does this deliver?
- What are the success criteria?
- How does this impact users?

**Development Perspective:**
- What technical approach should we use?
- What are the dependencies?
- What could be reused or extended?

**QA Perspective:**
- What could go wrong?
- What edge cases exist?
- How do we test this?

### 2. Human-in-the-Loop

There are **two mandatory approval gates**:

**Gate 1 - Initial Approach (after Three Amigos):**
- ✋ Technical approach MUST be validated
- ✋ Scope must be confirmed
- ✋ Prevents expensive wrong-direction work

**Gate 2 - Complete Specifications (before Delivery):**
- ✋ Scenario coverage MUST be confirmed
- ✋ Visual designs MUST be approved
- ✋ All artifacts MUST have explicit sign-off

**NEVER proceed to Delivery without Gate 2 approval**

### 3. Comprehensive Specification

The mini-PRD MUST contain everything needed for implementation:
- Business context and success criteria
- Technical architecture and API contracts
- Behaviour scenarios with complete coverage (happy/error/edge)
- Visual designs as executable Storybook stories
- RTL tests locking component behavior
- Selector contract bridging design and tests
- Seed data requirements for testing
- Implementation notes (dependencies, performance, security)

## Workflow Overview

### Step 0: Scope & Context Assessment

**Before diving into analysis, assess scope and project state:**

#### 0a. Epic Detection (MANDATORY)

Evaluate if this is an Epic that needs delivery chunking:

| Signal | Indicates Epic? |
|--------|-----------------|
| Multiple distinct capabilities (2+ things it does) | YES |
| Multiple independent components that could ship separately | YES |
| Scope clearly exceeds one PR | YES |
| Title has multiple nouns ("Intake & Capture", "Auth & Tenancy") | LIKELY |
| 10+ scenarios anticipated | LIKELY |

**If Epic detected:**
1. Label as Epic in Linear (if not already)
2. Identify Delivery Chunks (atomic units that can be implemented/deployed independently)
3. Proceed with ONE PRD that includes a "Delivery Chunks" section
4. After approval, create child issues for each chunk

**Entity Epics from Discovery:** If this issue came from entity-driven Discovery, it may already be labeled as an Epic with capability sub-issues. Check the description for "This is an entity Epic" — if present, the delivery chunks are the capability sub-issues. Write one PRD covering all capabilities; each capability maps to a delivery chunk.

**Delivery Chunk Criteria:**
- Can be implemented in one PR
- Has a clear "done" state
- Can be deployed independently (given dependencies)
- Doesn't leave the system in a broken state

**Note:** One PRD per Epic is fine. Chunking is for DELIVERY, not requirements.

#### 0b. Project Context

| Question | If YES | If NO |
|----------|--------|-------|
| **Is this project live with real users?** | Brownfield - migration risk is real, prefer incremental changes | Greenfield - do it right now while changes are free |
| **Does this feature introduce new terminology?** | Glossary update required, assess ripple effects | Standard workflow |
| **Is this infrastructure or user-facing?** | Focus on authorization, isolation, data integrity | Focus on user journeys, UI states, flows |

**Greenfield Advantage:**
When there are no live users, prefer:
- Correct naming from the start (don't defer renames)
- Clean architecture (don't accumulate tech debt)
- Full schema design (not incremental patches)

**Brownfield Caution:**
When users exist, consider:
- Migration complexity and rollback plans
- Backwards compatibility requirements
- Phased rollout strategies

### Step 1: Start Requirements Refinement

**Command:** `/requirements:refine LIN-123`

**Orchestrator actions:**
1. Read Linear feature and acceptance criteria
2. Read linked Discovery documentation
3. **Assess project context** (greenfield/brownfield, terminology changes)
4. Analyze from Three Amigos perspectives
5. Present initial analysis for human feedback

**Approval Gate #1:**
User must approve initial approach before proceeding to detailed specs

**After approach approval — Initial Estimation:**
Once the approach is approved, load `af-estimation-expertise` and produce an initial refined estimate:
- Decompose by functional area (FE, BE, INFRA, TEST, UX, DOCS)
- Estimate hours per area, convert to fibonacci story points
- Confidence level: typically Medium (approach known, details to come)
- Tag as `[Refined Estimate]` in Linear comment
- Update Linear issue with story points

This estimate will be revisited after agents complete detailed specs (Step 3b).

### Step 1a: Create Specification Sub-issues

For each parent issue entering Requirements, create sub-issues for specification work.

**[Behaviour] Sub-issue:**
```
Title: [Behaviour] {Parent Title} scenarios
Label: type:behaviour
Assignee: QA role holder (or whoever wears the QA hat — see project CLAUDE.md)
Cycle: Current refinement cycle
Estimate: Typically 1-3 points (part of parent total)
Status: Approved
```

**[UX] Sub-issue (if feature has UI):**
```
Title: [UX] {Parent Title} Storybook
Label: type:ux
Assignee: UX role holder (or whoever wears the UX hat — see project CLAUDE.md)
Cycle: Current refinement cycle
Estimate: Typically 1-3 points (part of parent total)
Status: Approved
```

**Ordering:** Create and complete the [Behaviour] sub-issue first. Behaviour scenarios define WHAT the feature does; UX designs define HOW it looks. UX work uses the Behaviour scenarios as input.

After creating sub-issues, apply approval labels to the parent issue:
- Apply `approval:bdd-pending` label to parent when [Behaviour] sub-issue is created
- Apply `approval:ux-pending` label to parent when [UX] sub-issue is created (UI features only)

**Linear structure after sub-issue creation:**
```
Issue: Login Flow (8 pts) [Refining]
  ├── Sub-issue: [Behaviour] Login Flow scenarios (2 pts) [Approved] @QA, Cycle 12
  ├── Sub-issue: [UX] Login Flow Storybook (2 pts) [Approved] @UX, Cycle 12
  └── Description contains implementation checklist (not sub-issues)
```

**Parent estimate includes sub-issue effort:**
The parent's 8 points includes the 2+2 for specs plus ~4 for implementation. Sub-issue estimates are a breakdown, not additions.

**No [API] sub-issue:**
API contract work happens early in Delivery as part of implementation. It's a checklist item in the parent issue, not a separate spec artifact requiring sign-off.

### Branch for Spec Work

**Feature branch model:**
- Work on the `specs` branch (via `start-refine` command)
- Commit Behaviour scenarios and Storybook stories to this branch
- All refinement work for a cycle shares the same `specs` worktree
- PR to `develop` when all spec sub-issues for that cycle are approved

**Trunk-based model:**
- Work directly on the default branch
- Commit spec artifacts alongside other changes
- No separate specs branch

**Sub-issues do not get their own branches:**
All spec work for a refinement period goes to the same branch. The branch corresponds to the work phase, not the individual sub-issue.

### Step 2: Create Mini-PRD

**Once approach approved, orchestrator creates mini-PRD with 8 sections:**

#### Section 1: Feature Summary
- Purpose, description, success criteria
- User value proposition
- Business context

#### Section 2: Discovery Context
- Links to user research
- Related ADRs (architectural decisions)
- Technical constraints from Discovery

#### Section 3: Technical Specification
- API contracts (REST, GraphQL, gRPC, etc.)
- Database models (entities, relationships, migrations)
- Architecture diagrams (system components, data flow)
- Integration points (external services, APIs)

#### Section 4: Behaviour Scenarios
- Markdown scenario specifications (Preconditions/Steps/Expected format)
- Test type classification (E2E, Integration, Component, Unit)
- Happy path scenarios
- Error handling scenarios
- Edge case scenarios
- Selector contract references for UI scenarios

#### Section 5: Visual Specifications
- Storybook stories for all UI states
- Selector contract (shared test IDs)
- RTL tests (component behavior contracts)
- Component specifications
- Responsive behavior
- Accessibility requirements

#### Section 6: Implementation Notes
- Dependencies and prerequisites
- Seed data requirements
- Performance targets
- Security considerations
- Monitoring requirements
- Infrastructure testing requirements (see below)

##### Infrastructure Testing Requirements

When a feature requires new infrastructure code, specify testing requirements:

**Utility Modules (`lib/` or similar):**
| Module | Test Type | Coverage Target |
|--------|-----------|-----------------|
| Auth utilities | Integration | 80% |
| Email services | Unit (mocked) | 90% |
| Rate limiting | Unit | 100% |

**API Routes:**
| Route | Test Type | Coverage Target |
|-------|-----------|-----------------|
| Admin endpoints | Unit (mocked deps) | 85% |
| Public endpoints | Unit (mocked deps) | 85% |

**Rule:** Any new utility module or API route MUST have corresponding test requirements in the mini-PRD. Behaviour scenarios test user behaviour; infrastructure tests ensure the plumbing works.

#### Section 7: Effort Estimation
- Story points and total hours
- Breakdown by functional area (hours and role)
- Sub-issue estimates with hours and points roll-up (for features > 3 points)
- Confidence level and estimation basis
- Change from Discovery estimate (if applicable)

#### Section 8: Delivery Chunks (for Epics)

**Include this section when the feature is an Epic with multiple delivery chunks.**

| Chunk | Components/Scope | Dependencies | Scenarios | Estimated PRs |
|-------|------------------|--------------|-----------|---------------|
| 1. [Name] | [Components] | [Blockers] | [X-Y] | 1 |
| 2. [Name] | [Components] | [Chunk 1] | [X-Y] | 1 |
| ... | ... | ... | ... | ... |

**For each chunk, specify:**
- What's included (components, APIs, infrastructure)
- What it depends on (other chunks, external blockers)
- Which scenarios it covers (by number)
- Expected PR count (usually 1)

**After approval:** Create Linear child issues for each chunk.

#### Section 8: Delivery Checklist
- Pre-implementation checks
- During implementation milestones
- Post-deployment verification

### Step 3: Invoke Specialized Agents

**Orchestrator delegates specialized work:**

**Behaviour Agent Invocation:**
```
Task → bdd-agent
Input: Mini-PRD content, Linear issue ID, glossary path
Output:
  - Markdown scenarios in mini-PRD Section 4
  - /tests/selectors/[capability].ts (selector contract)
Purpose: Transform requirements into scenario specifications
```

**UX Design Agent Invocation (for UI features):**
```
Task → ux-design-agent
Input: Behaviour scenarios, component requirements, selector contract
Output:
  - /stories/[capability]/[feature-name].stories.tsx
  - /src/components/[feature]/[Component].test.tsx (RTL tests)
  - /docs/requirements/[feature-name]/user-flow.md
Purpose: Create visual specifications and lock behavior with RTL tests
```

**Architecture Agent Invocation (for complex features):**
```
Task → architecture-quality-agent
Input: Technical specification, existing architecture
Output: Architecture review, ADR updates
Purpose: Validate technical approach against standards
```

After agent completion, update approval labels on parent:
- bdd-agent success → Replace `approval:bdd-pending` with `approval:bdd-approved` on parent
- ux-design-agent success → Replace `approval:ux-pending` with `approval:ux-approved` on parent

### Step 3b: Agent Invocation Checklist

**MANDATORY CHECKPOINT** - Before proceeding to Step 4, verify ALL applicable items:

| Question | If YES | Action | Output |
|----------|--------|--------|--------|
| Does feature have UI components? | ✅ | Invoke `ux-design-agent` | Storybook stories, RTL tests |
| Does feature need Behaviour scenarios? | ✅ | Invoke `bdd-agent` | Markdown scenarios, selector contract |
| Is architecture complex or novel? | ✅ | Invoke `architecture-quality-agent` | Architecture review |
| Were technical decisions made during Three Amigos? | ✅ | Create ADR | ADR document in `docs/architecture/adr/` |
| Does the mini-PRD include effort estimates? | ✅ | Load `af-estimation-expertise`, finalize estimate | Story points + hours set on Linear issue, Section 7 complete |

**How to check "Does feature have UI components?"**
- Will users see new screens, forms, or interactive elements? → YES
- Are there new components to build (buttons, cards, modals)? → YES
- Does the mini-PRD Section 5 list visual specifications? → YES
- Is this pure backend/infrastructure with no UI? → NO

**Do NOT proceed to Step 4 until this checklist is complete.**

If you skipped an agent, STOP and invoke it now. It's cheaper to catch this here than after approval.

### Step 4: Quality Validation

**Completeness Checks:**
- ✅ All Linear acceptance criteria addressed
- ✅ Discovery context properly linked
- ✅ Technical approach documented
- ✅ All scenarios covered (happy/error/edge)

**Quality Checks:**
- ✅ Glossary compliance verified (scenario terms)
- ✅ Selector contract exists for UI features
- ✅ Storybook play functions test UI component behaviors (primary)
- ✅ RTL tests cover non-visual logic (hooks, utils, state management)
- ✅ No duplicated assertions between Storybook and RTL
- ✅ Design system consistency (shadcn/ui components)
- ✅ Accessibility requirements specified
- ✅ Performance targets defined
- ✅ Test type classified for each scenario

**Estimation Checks:**
- ✅ Effort estimates finalized (story points and hours set on Linear issue)
- ✅ Mini-PRD Section 7 (Effort Estimation) complete with breakdown
- ✅ For features > 3 points: sub-issues created with individual estimates
- ✅ Hours AND points roll up to parent feature (not just Linear's points roll-up)
- ✅ Estimate tagged as `[Refined Estimate]` in Linear comment

**Artifact Checks:**
- ✅ Mini-PRD document created with all 8 sections
- ✅ Scenarios use Markdown format (not Gherkin)
- ✅ Selector contract defined (`/tests/selectors/`)
- ✅ Storybook stories with play functions created and passing (for UI - primary component tests)
- ✅ RTL tests created and passing for non-visual logic (hooks, utils, state management)
- ✅ User flows documented
- ✅ Glossary updated (if new terminology introduced)
- ✅ Ripple effects assessed (if terminology changes)
- ✅ UX ripple effects documented (even for infrastructure features)
- ✅ Affected story files listed explicitly (if terminology changes)

### Step 5: Commit and Validate

**IMPORTANT:** Commit artifacts BEFORE requesting approval. The git commit hook acts as a quality gate.

**Process:**
1. Stage all requirement artifacts (mini-PRD, scenarios, selectors, ADRs)
2. Attempt commit - hook will fire with checklist
3. Work through hook checklist honestly:
   - TESTS: Storybook play functions + RTL for non-visual logic should PASS (components exist). E2E/Integration use `test.todo()` (implemented in Delivery). Never `test.skip()` — it hides gaps silently.
   - DOCUMENTATION: YES - this IS the documentation
   - VALIDATION: Run docs-quality-agent if prompted
   - ARCHITECTURE: Confirm ADRs created for decisions made
   - SECURITY: Verify no secrets in docs
4. Complete commit after addressing all items
5. Only THEN proceed to human approval

**Why commit first:**
- Hook catches missing ADRs, validation, and other issues
- Issues found before asking user to approve
- Avoids "approved but incomplete" state

### Step 6: Human Approval

**Approval Gate #2:**
Present complete mini-PRD to user for review

**Command:** `/requirements:approve LIN-123`

**Pre-conditions for approval:**
- All [Behaviour] sub-issues are Done
- All [UX] sub-issues are Done (if feature has UI)
- Parent issue has `approval:bdd-approved` label
- Parent issue has `approval:ux-approved` label (if UI feature)
- Mini-PRD is complete and committed
- Git commit hook checklist passed
- Spec artifacts merged to develop (direct merge before approval)

**Approval process:**
1. Verify commit completed (Step 5)
2. Verify all sub-issues are Done
3. Verify all artifacts exist
4. Run quality checks (docs-quality-agent) if not done in Step 5
5. **Merge specs → develop** (direct merge, no PR — documents don't need CI)
6. Get explicit human approval
7. Update Linear parent issue to "Approved"
8. "Approved" means develop is ready — specs are already there
9. Parent issue ready for scheduling into delivery cycle

### Step 7: Post-Approval - Create Child Issues (for Epics)

**If this is an Epic with Delivery Chunks (see Step 0a):**

After approval, create child issues in Linear for each chunk (via GraphQL API - see `af-linear-api-expertise`):

```bash
# Example: Create child issue with parent reference
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation { issueCreate(input: { title: \"Chunk 1: Photo Capture Flow\", teamId: \"TEAM-UUID\", parentId: \"EPIC-UUID\", description: \"Refs PRD Section 7 Chunk 1. Scenarios 1-18.\" }) { success issue { identifier } } }"
  }'
```

**For each child issue:**
1. Reference the parent PRD and chunk section
2. List which scenarios it covers
3. Set "blocked by" if depends on other chunks
4. Link to relevant components/stories

**Linear structure after approval:**
```
EPIC-123: Item Intake & Photo Capture [epic] [Approved]
  ├── EPIC-123-1: Photo Capture Flow [Approved]
  ├── EPIC-123-2: Draft Recovery [Approved] [blocked by EPIC-123-1]
  ├── EPIC-123-3: S3 Upload [Approved] [blocked by EPIC-123-1]
  └── EPIC-123-4: Lambda Thumbnails [Approved] [blocked by EPIC-123-3]
```

**Do NOT move to Delivery without approval**

## Decision Points

### Does this feature need UX Design Agent?
- **Has UI components?** → YES (invoke ux-design-agent for Storybook + RTL)
- **API/backend only?** → NO (skip visual specs and RTL)
- **Modifies existing UI?** → YES (update Storybook stories and RTL tests)

### How many scenarios should I create?
- **Minimum:** 1 happy path + 1 error case
- **Typical:** 4-6 (happy, errors, edge cases)
- **Complex features:** 8-15 (multiple paths, states, conditions)
- **Rule:** Cover all acceptance criteria + discovered edge cases

### Which test type for each scenario?
- **E2E (~10%):** Complete user journeys through real UI + real backend
- **Integration (~20%):** API/backend behavior without UI
- **Component (~20%):** UI behavior with RTL (forms, interactions, accessibility)
- **Unit (~50%):** Pure validation logic (email format, calculations)
- **Rule:** Push tests down the pyramid - use minimum scope needed

### Which agents do I need?
- **Always:** bdd-agent (for Behaviour scenario specifications)
- **UI features:** ux-design-agent (for Storybook + RTL tests)
- **Complex architecture:** architecture-quality-agent (for review)
- **Final validation:** docs-quality-agent (for documentation standards)

### Does this feature involve terminology changes?

When renaming entities, attributes, or roles (e.g., `Tenant` → `Organisation`), assess the full ripple effect:

| Layer | Check For | Action |
|-------|-----------|--------|
| **Schema** | Model names, field names, enums | Update definitions |
| **Backend** | Lambda handlers, resolvers, utilities | Update all references |
| **Auth** | Cognito attributes, JWT claims | Update attribute names |
| **UI Components** | Props, state, display text | Update components |
| **Storybook** | Story names, mock data, props | Update stories |
| **Selectors** | data-testid values | Update selector contracts |
| **Behaviour Scenarios** | Terminology in Preconditions/Steps/Expected | Update scenario text |
| **Tests** | Assertions, fixtures, helpers | Update test code |
| **Glossary** | Term definitions | Add new, deprecate old |
| **Documentation** | READMEs, guides, comments | Update all references |

**Greenfield rule:** Do all renames now while it's free.
**Brownfield rule:** Create migration plan with backwards compatibility.

### Does this feature require new ADRs?

**IMPORTANT:** Technical decisions made during Requirements phase may warrant ADRs. This is especially true when you ask the user to choose between approaches during Three Amigos analysis.

**Decision Framework (from af-architecture-expertise):**

| Decision Characteristic | ADR Needed? |
|------------------------|-------------|
| Affects multiple components or layers | YES |
| Choosing between significantly different approaches | YES |
| Hard to reverse once implemented | YES |
| Future developers would ask "why did we do this?" | YES |

**Rule:** If you presented options to the user during Three Amigos (e.g., "client-side only vs server-side validation"), that decision likely warrants an ADR.

**Process:**
1. When a technical decision is made, check against the framework above
2. If ADR warranted, create it BEFORE finalizing mini-PRD
3. Reference the ADR in mini-PRD Section 2 (Discovery Context)
4. ADR must be committed with mini-PRD

**Common decisions that need ADRs:**
- Validation strategy (client vs server vs both)
- Storage approach (localStorage vs server-side vs IndexedDB)
- API design patterns (REST vs GraphQL, sync vs async)
- Authentication flows
- Data model design

→ Load `af-architecture-expertise` for full ADR workflow and templates

---

### Does this feature have UX ripple effects?

**IMPORTANT:** Even infrastructure features may require UX changes. Always check:

1. **Search for affected stories:**
   ```bash
   grep -r "OldTerm\|oldTerm" stories/
   ```

2. **For each affected story, document in mini-PRD Section 5:**
   - File path
   - Specific changes required (renames, mock data, props)
   - New stories needed (if any)
   - `data-testid` additions required

3. **Add Component-level Behaviour scenarios** for any UI behavior changes

4. **Update Delivery Checklist** with specific UX tasks

**Common UX ripple effects:**
| Infrastructure Change | UX Impact |
|----------------------|-----------|
| Entity rename | Story file renames, display text, mock data |
| Role rename | Role badges, dropdowns, mock data in stories |
| New auth flow | Login/signup form changes, new stories |
| New status enum | Status badges, filters, mock data |
| New field on model | Form inputs, display components |

**Rule:** If terminology or auth changes, there ARE UX changes. List them explicitly.

## Common Patterns

### API-Heavy Features
**Focus on:**
- API contract definitions (REST/GraphQL/gRPC schemas)
- Request/response examples with payloads
- Error codes, messages, and handling
- Rate limiting and throttling considerations
- Authentication and authorization requirements
- Integration test scenarios

**Example:** User authentication, payment processing, data exports

### UI-Heavy Features
**Focus on:**
- Storybook stories (all states: default, loading, error, empty, success)
- Selector contract (shared data-testid values)
- RTL tests (component behavior contracts)
- Responsive breakpoints
- Interaction animations
- Accessibility (ARIA labels, keyboard nav)

**Example:** Dashboard widgets, forms, data visualization

### Data-Heavy Features
**Focus on:**
- Database schema definition (SQL/NoSQL/Graph)
- Data migration plans and rollback strategies
- Seed data requirements for testing
- Backup/recovery procedures
- Data validation rules and constraints
- Query performance and indexing strategy

**Example:** Reporting systems, bulk operations, data imports

### Infrastructure Features

Infrastructure features are foundational work that enables other features but isn't directly user-facing. Examples: schema extensions, auth configuration, new data models.

**Focus on:**
- Authorization rules and data isolation
- API contracts (GraphQL schema, Lambda signatures)
- Data integrity and validation
- Integration test scenarios (not E2E user journeys)
- Seed data for dependent features
- Glossary updates for new entities

**Scenarios emphasize:**
- CRUD operations with correct authorization
- Tenant/shop isolation (cross-boundary rejection)
- Role-based access control
- Data validation and error handling
- Edge cases (empty states, max limits, invalid input)

**Scenarios de-emphasize:**
- Full UI user journeys
- New Storybook stories (unless admin UI exists)

**BUT STILL CHECK for UX ripple effects:**
- Terminology changes → existing stories need updating
- Auth changes → login/signup forms need updating
- Role changes → badges and dropdowns need updating

Always run: `grep -r "OldTerm" stories/` to find affected files.

**Example:** Schema migrations, new data models, Cognito configuration, Lambda handlers

## File Outputs

### Requirements Phase Creates (Specifications)

```
.claude/templates/
  └── glossary.yml          # UPDATE: Add new terms, deprecate old

docs/requirements/[feature-name]/
  ├── mini-prd.md           # Complete specification
  │   ├── Section 4: Scenarios (Markdown format)
  │   └── Section 5: Selector contract references
  └── user-flow.md          # Mermaid flow diagrams

tests/selectors/
  └── [capability].ts       # Selector contract (shared test IDs)

stories/
  ├── [Component].stories.tsx       # Shared component stories
  └── [capability]/                 # Feature-specific stories
      └── [Feature].stories.tsx

src/components/[feature]/
  └── [Component].test.tsx  # RTL tests (colocated with components)
```

### Glossary Updates (When Introducing Terminology)

When a feature introduces new entities, roles, or statuses, update the glossary:

```yaml
# .claude/templates/glossary.yml

# Add new terms
Organisation:
  definition: "A charity or business using the platform (formerly Tenant)"
  replaces: Tenant  # Mark what it replaces

Shop:
  definition: "A physical location within an Organisation"

org_admin:
  definition: "Organisation-wide administrator role"
  replaces: owner

# Deprecate old terms
Tenant:
  deprecated: true
  replaced_by: Organisation
  removal_version: "2.0"
```

### Selector Contracts (Bridge Between Stories/RTL/E2E)

Selector contracts are the single source of truth for `data-testid` values:

```typescript
// tests/selectors/organisation.ts
export const organisationSelectors = {
  // Form fields
  nameInput: 'organisation-name-input',
  logoUpload: 'organisation-logo-upload',
  submitButton: 'organisation-submit-button',

  // Display elements
  nameDisplay: 'organisation-name-display',
  statusBadge: 'organisation-status-badge',
} as const;
```

**Usage contract:**
- **Storybook stories** → `data-testid={organisationSelectors.nameInput}`
- **RTL tests** → `screen.getByTestId(organisationSelectors.nameInput)`
- **E2E tests** → `page.getByTestId(organisationSelectors.nameInput)`

This ensures refactoring a selector updates all consumers.

### Delivery Phase Creates (Executable Tests)

```
tests/
  ├── e2e/
  │   └── [feature].spec.ts        # Playwright E2E specs
  ├── integration/
  │   └── [feature].test.ts        # Jest integration tests
  ├── unit/
  │   └── [module].test.ts         # Jest unit tests
  ├── selectors/                   # From Requirements
  ├── fixtures/                    # Test data
  └── helpers/                     # Shared test utilities

amplify/seed/
  └── [feature].ts          # Seed data for testing (if needed)
```

### Key Principle

- **Requirements** creates scenarios (specifications) in mini-PRD
- **Delivery** generates executable test files FROM those specifications
- **Selector contract** bridges both phases (shared source of truth)

## Seed Data Requirements

When scenarios have preconditions like "Given a Super Admin account exists", Requirements phase must specify seed data:

**In mini-PRD Section 6 (Implementation Notes):**

```markdown
### Seed Data Requirements

**Users:**
| Email | Password | Type | Attributes |
|-------|----------|------|------------|
| superadmin@example.com | SuperAdmin123! | Platform | platform_role: super_admin |
| orgadmin@example.com | OrgAdmin123! | Organisation | role: admin, tenant_id: {seed} |

**Organisations:**
| Name | Tenant ID | Status |
|------|-----------|--------|
| Test Org | auto-generated | active |

**Location:** `/amplify/seed/[feature].ts`
**Command:** `npm run seed`
```

Seed data is idempotent - checks existence before creating.

## Common Pitfalls

1. **Skipping Three Amigos analysis**
   - All three perspectives MUST be considered
   - Missing perspective leads to incomplete specs

2. **Proceeding without human approval**
   - NEVER skip either approval gate
   - Gate 1 prevents wrong-direction work
   - Gate 2 prevents incomplete implementation

3. **Incomplete scenario coverage**
   - Must include happy path, errors, edge cases
   - Missing scenarios = bugs in production

4. **Missing selector contract**
   - UI scenarios MUST reference selectors
   - Components MUST use data-testid from contract
   - Tests MUST import selectors

5. **Missing RTL tests**
   - Requirements phase creates RTL tests
   - Engineering keeps them passing during implementation
   - RTL tests are the "design contract"

6. **Generic specifications**
   - Mini-PRDs must be specific and detailed
   - Generic specs lead to implementation ambiguity

7. **Missing technical details**
   - API contracts MUST be complete
   - Database schemas MUST be defined
   - Missing details cause delays in Delivery

8. **Ignoring glossary**
   - Behaviour scenarios MUST use glossary terms
   - Inconsistent terminology confuses stakeholders

9. **All scenarios as E2E**
   - Push tests down the pyramid
   - E2E only for critical complete journeys
   - Most scenarios should be Component or Unit

10. **Deferring renames in greenfield projects**
    - No live users = no migration risk
    - "Do it right now" beats "fix it later"
    - Deferred renames accumulate as tech debt

11. **Forgetting glossary updates**
    - New entities MUST be added to glossary
    - Old terms MUST be marked deprecated
    - Inconsistent terminology causes confusion across teams

12. **Missing ripple effect assessment**
    - Terminology changes touch many layers
    - Schema → handlers → auth → UI → stories → tests → docs
    - Incomplete assessment leads to broken references

13. **Assuming infrastructure features have no UX impact**
    - Entity renames affect story files and display text
    - Auth changes affect login/signup forms
    - Role changes affect badges, dropdowns, permissions UI
    - Always grep stories/ for affected terms
    - List specific story file changes in Section 5

14. **Forgetting ADRs for decisions made during requirements**
    - If you asked the user to choose between approaches → probably needs ADR
    - Technical decisions made in Three Amigos should be evaluated
    - Create ADR BEFORE finalizing mini-PRD, not after
    - Reference ADR in mini-PRD Section 2

15. **Requesting approval before committing**
    - Always commit artifacts before asking for human approval
    - Git commit hook acts as quality gate (tests, docs, architecture, security)
    - Hook catches issues that should be fixed before approval
    - Avoids approving incomplete specifications

16. **Skipping UX Design Agent for UI features**
    - If feature has UI components → MUST invoke ux-design-agent
    - Creates Storybook stories (visual specifications)
    - Creates RTL tests (component behavior contracts)
    - Missing stories = incomplete specifications
    - Use Step 3b checklist to catch this before proceeding

17. **Missing Epic detection and delivery chunking**
    - Large features with multiple capabilities should be recognized as Epics
    - One PRD is fine, but must include Delivery Chunks section
    - Without chunks, Engineering faces overwhelming context
    - After approval, create child issues for each chunk
    - See Step 0a for Epic detection signals

## Integration with Other Phases

**Before Requirements:**
- ← **Discovery Phase** - Provides Linear features and project context

**After Requirements:**
- → **Delivery Phase** - Implements mini-PRD specifications
- → Delivery uses scenarios as test specifications
- → Delivery keeps RTL tests passing
- → Delivery writes E2E tests from scenario specs

**Requirements provides:**
- Complete implementation blueprint
- Scenario specifications for test generation
- Selector contract for consistent testing
- RTL tests as component behavior contracts
- Approval to begin development
- Effort estimates (story points where 1 point = half day)

## Detailed Reference

**For complete requirements documentation:**
- Read `.claude/docs/guides/requirements-guide.md` (full workflow with examples)

**For scenario creation:**
- Load `af-bdd-expertise` skill
- Read `.claude/docs/guides/testing-guide.md`

**For mini-PRD template:**
- Read `.claude/templates/mini-prd-template.md`

**For agent interactions:**
- Read `.claude/agents/bdd-agent.md`
- Read `.claude/agents/ux-design-agent.md`
- Read `.claude/agents/af-work-management-agent.md`

## Success Criteria

Requirements complete when:
- ✅ Scope assessed - Epic detected and labeled if applicable (Step 0a)
- ✅ Project context assessed (greenfield/brownfield)
- ✅ Three Amigos analysis performed and approved (Gate 1)
- ✅ Complete mini-PRD created with all sections (7 for features, 8 for epics)
- ✅ Delivery Chunks documented (for Epics - Section 7)
- ✅ Markdown scenarios cover all acceptance criteria + edge cases
- ✅ Selector contract defined for UI features
- ✅ Storybook stories with play functions created and passing (for UI features - primary component tests)
- ✅ RTL tests created and passing for non-visual logic (hooks, utils, state management)
- ✅ Seed data requirements documented
- ✅ Glossary updated (if new terminology)
- ✅ Ripple effects documented (if terminology changes)
- ✅ ADRs created for architectural decisions made during requirements
- ✅ All artifacts committed (git commit hook checklist passed)
- ✅ All artifacts validated by quality agents
- ✅ Human has explicitly approved specifications (Gate 2)
- ✅ Linear issue moved to "Approved"
- ✅ Child issues created for each Delivery Chunk (for Epics - Step 7)
