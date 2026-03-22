---
name: af-discover-scope
description: Explore new product ideas and gather project-level context for Linear Features. Use when analysing business drivers, mapping user context, identifying technical constraints, or defining success criteria.

# AgentFlow documentation fields
title: Discovery Process
created: 2025-10-29
updated: 2026-03-09
last_checked: 2026-03-09
tags: [skill, process, discovery, requirements, research]
parent: ../README.md
---

# Discovery Process

## Essential Reading

**⚠️ BEFORE starting discovery, read this comprehensive guide:**

@.claude/docs/guides/discovery-guide.md

This guide provides:
- **Complete practical example** (cost allocation system walkthrough)
- Detailed context gathering patterns and user response examples
- When to delegate to search-agent vs handle directly
- All 5 deliverable documents with real content examples
- Linear integration and feature creation workflow
- Handoff to Refinement phase checklist

**Without reading this guide first, you will create incomplete discovery documentation.**

## Quick Reference

The discovery process explores product-level ideas through structured interviews, creates comprehensive project documentation, and establishes Linear features for implementation tracking. Discovery bridges initial user requests with detailed requirements.

**Typical duration:** 2-4 hours
**End result:** Project overview, user analysis, entity model, technical ADRs, tech stack agreement, Linear epics/features

## When to Use

**✅ Appropriate for Discovery** (product/project level):
- "Create a cost allocation system that imports from Xero and generates reports"
- "Build a SaaS platform for project management"
- "Develop a learning management system"

**❌ Not Appropriate** (feature level - use Refinement instead):
- "Add user authentication"
- "Create a dashboard widget"
- "Implement email notifications"

## Git Workflow

**Discovery work happens on the `specs` branch** (see ADR-009).

```bash
# Start a discovery session
start-specs myproject           # Creates/attaches to specs worktree + tmux
```

The `specs` branch is shared by PM, UX, and QA for all pre-implementation work (Discovery + Refinement). Issue branches are only created later during Delivery phase.

**File organization on specs branch:**
- `docs/vision/` - Project overview, business case
- `docs/requirements/` - User analysis, feature roadmap
- `docs/architecture/adr/` - Technical ADRs

See [Work Management Guide](../../docs/guides/work-management.md#branch-strategy-adr-009) for full branching details.

## Workflow Overview

### Phase 0: Context Ingestion (Optional)

**Before asking the 4 context questions, check for existing upstream documents.**

Check `docs/context/` for ideation documents, business context documents, or any other upstream materials that stakeholders have prepared.

**If `docs/context/` exists and contains documents:**

1. **Identify document types:**
   - Ideation documents (from `af-brainstorm-ideas` skill or equivalent brainstorming)
   - Business context documents (vision statements, strategy docs, market research)
   - Any other relevant context (pitch decks, competitive analysis, meeting notes)

2. **If multiple ideation document versions exist** (v1, v2, v3...):
   - Read all versions
   - Summarize the **delta** between versions: what changed, what was refined, what was dropped
   - Present the evolution to the user: "Your thinking evolved from X to Y. Key changes: ..."

3. **Pre-populate Q1-Q4 from found documents:**
   - Problem Space / Business Driver → Q1
   - User Space → Q2
   - Known Constraints → Q3
   - Success Metrics → Q4
   - Business Context → enriches Q1 and Q4

4. **Present findings to the user:**
   - "I found [N] documents in docs/context/. Here's what I learned: ..."
   - "Based on these documents, I've pre-populated the context questions below."
   - "Let's review what I have and fill in any gaps."

5. **Identify gaps** — what the ideation documents DON'T cover:
   - Technical constraints not mentioned → will need Q3 answers
   - Tech stack preferences → will need Q3b
   - Behavioral calibration → will need Q2b (if UI)
   - Success metrics if vague → will need Q4 specifics

**If no `docs/context/` directory or it's empty:**
- Proceed directly to Phase 1 as before (no change to existing workflow)

**Important:** Ideation documents capture domain knowledge (problems, users, workflows, business rules) but deliberately exclude technical decisions (architecture, data models, tech stack). Treat ideation content as rich context for the 4 questions, not as settled technical decisions.

### Phase 1: Context Gathering (4 Questions)

**Structured interview with user - MUST ask all 4 questions:**

**Q1: Business Driver**
*"What's driving this need? What problem are you trying to solve?"*

**Captures:**
- Current pain points
- Business impact
- Value proposition

**Q2: User Context**
*"Who are the users and what's their current experience with this type of system?"*

**Captures:**
- User personas (roles, skills, needs)
- Current workflows and tools
- Pain points and frustrations

**Q2b: Behavioral Calibration** (if project has UI)
*"How do these users differ in how they interact with tools? Think about: how cautious are they with irreversible actions? Do they prefer dense or spacious layouts? How much do they trust automated processes? How often do they switch between different tasks or views?"*

**Captures (as a calibration matrix, not expanded prose):**
- Risk tolerance (Low/Med/High per persona)
- Information density preference (Low/Med/High per persona)
- Automation trust (Low/Med/High per persona)
- Context-switch frequency (Low/Med/High per persona)

**Q3: Technical Constraints**
*"Any technical constraints, existing systems, or technology preferences?"*

**Captures:**
- Existing integrations required
- Infrastructure preferences
- Budget and resource constraints
- Technology stack requirements

**Q3b: Tech Stack Selection** (informed by Q1-Q3 answers)
*Based on the answers so far, guide the user through module selection using the module registry at `.claude/docs/reference/module-registry.yml`.*

**Sub-questions to determine modules:**

- **Hosting:** "Will this be a web app, mobile app, or both?" → Determines: amplify, flutter
- **Auth:** "Does the app need user authentication?" → Determines: auth module
- **Email:** "Will the app send emails (verification, notifications, invitations)?" → Determines: email module
- **Analytics:** "Do you need product analytics, feature flags, or session replay?" → Determines: posthog module
- **Infrastructure:** "Will this use AWS multi-account (dev/test/prod) infrastructure?" → Determines: aws-infrastructure module
- **UI:** "Will the app have a web UI with component library?" → Determines: ui-styling module

**Core modules are always included:** agentflow, linear, git, documentation, testing, security, cicd.

**Output:** A **Tech Stack Agreement** — a list of selected modules that will be installed after Discovery completes. Record this in the project overview document and as a comment on the Linear epic.

**Q4: Success Criteria**
*"What does success look like? How will you measure it?"*

**Captures:**
- Measurable outcomes
- Timeline expectations
- Adoption targets
- Success metrics

### Phase 2: External Research (Optional)

**Decision point: Is external research needed?**

**Research needed when:**
- Unfamiliar APIs or integrations mentioned
- Complex domain requiring external knowledge
- Competitive analysis would inform architecture
- Technical feasibility unclear

**Research NOT needed when:**
- User provided comprehensive technical details
- Standard AgentFlow patterns apply
- Team has domain expertise
- Similar projects exist as reference

**If research needed:**
```
Invoke search-agent via Task tool:
Input: Research query focused on technical patterns, APIs, constraints
Output: Focused summary of key findings
Purpose: Protect orchestrator context with summarized results
```

### Phase 3: Create Deliverables

**MUST create 7 documentation artifacts (6 if no UI):**

#### 1. Project Overview (`/docs/requirements/project-overview.md`)
**Contains:**
- Business case (problem, impact, value proposition)
- Success criteria (measurable outcomes)
- Scope boundaries (included/excluded)
- Project vision statement

**Purpose:** Executive summary for stakeholders

#### 2. User Analysis (`/docs/requirements/user-analysis.md`)
**Contains:**
- User personas (roles, experience levels, needs)
- Key user journeys (step-by-step workflows)
- Current pain points (from Q2 responses)
- Access levels and permissions
- Behavioral calibration matrix (from Q2b, UI projects only)

**Purpose:** Drive UX decisions and feature prioritization

**Behavioral Calibration Matrix:**
For UI projects, append a calibration matrix after the persona section. This is a lightweight overlay — one table, not expanded prose. Each dimension maps directly to interaction design decisions:

| Dimension | Persona A | Persona B | ... | UI Impact |
|-----------|-----------|-----------|-----|-----------|
| Risk tolerance | Low | High | ... | Confirmation patterns, undo support |
| Info density pref | High | Med | ... | Layout density, progressive disclosure |
| Automation trust | Cautious | High | ... | Action transparency, override controls |
| Context-switch freq | Low | High | ... | State persistence, navigation patterns |

**Rules:**
- Use Low/Med/High (not numeric scales)
- Include a "UI Impact" column linking each dimension to concrete patterns
- Maximum 4-6 dimensions — calibration, not comprehensive profiling
- Infer from Q2 responses where possible; ask Q2b explicitly only if unclear

#### 3. Entity Model (`/docs/discovery/entity-model.md`)
**Contains:**
- Entities identified (users, items, orders, etc.)
- Central entity identification ("what's THE thing users care about?")
- Classification: user-facing vs behind-the-scenes
- Relationships (simple ER diagram)
- Capabilities per entity (these become Linear features)
- Composition pattern (how entities combine into views)

**Purpose:** Feature decomposition from entities. Capabilities become Linear features; prioritization happens in Linear, not in this document.

**Depth:** Discovery sketches, Refinement specifies. Capture what you know (attributes, data sources, UI components) but don't require exhaustive detail — Refinement will flesh it out.

**Note:** Replaces the Feature Roadmap deliverable. Version labels (v1, v2, future) are no longer used in Discovery — Linear's milestones, cycles, and priority flags handle prioritization.

#### 4. Technical ADRs (`/docs/architecture/adr/`)

**Setup:**
1. Create directory: `mkdir -p docs/architecture/adr`
2. Copy ADR index template: `cp .claude/templates/adr-index.md docs/architecture/adr/README.md`
3. Copy ADR template: `cp .claude/templates/adr-template.md docs/architecture/adr/`

**Create ADRs as needed:**
- ADR-001: Technology Stack Selection
- ADR-002: Integration Approach
- ADR-003: Authentication Strategy
- (Additional ADRs as complexity requires)

**Each ADR contains:**
- Status (Proposed/Accepted/Deprecated/Superseded)
- Context (problem being solved)
- Options Considered (at least 2 alternatives)
- Decision (what was decided and why)
- Consequences (positive, negative, neutral)

**ADR Index (`docs/architecture/adr/README.md`):**
- Decision Summary table (one-line per ADR)
- Quick Reference section (key facts for agents)
- Links to individual ADRs

**Purpose:** Document architectural decisions with quick-reference index for agents

#### 5. Integration Architecture (`/docs/architecture/integration-architecture.md`)
**Contains:**
- System integration overview (diagram)
- Data flow architecture
- Authentication strategy
- Deployment architecture

**Purpose:** Technical blueprint for implementation

#### 6. UX Foundation (`/docs/design/`)

**Setup:**
1. Create directory: `mkdir -p docs/design`
2. Copy brand system template: `cp .claude/templates/brand-system-spec-template.md docs/design/brand-system.md`
3. Copy design decision log template: `cp .claude/templates/design-decision-log-template.md docs/design/design-decisions.md`

**Brand System Specification (`docs/design/brand-system.md`) contains:**
- Reference class declaration (what product is this "like"?)
- Brand personality (tone, density, motion)
- Colour system (palette ramps, semantic tokens, surface stack, theme mapping)
- Typography (families, size scale, weight scale, line heights)
- Spacing and border radius scales
- Shadows and elevation (mapped to surface stack)
- Motion (durations, easing curves)
- Iconography (library, sizes, stroke)
- Component usage rules (token-to-component mapping)
- Interaction patterns (keyboard nav, state communication)
- Accessibility requirements (WCAG 2.1 AA checklist)
- Platform-specific notes (web vs mobile if applicable)
- Storybook Brand Page specification

**Design Decision Log (`docs/design/design-decisions.md`) contains:**
- Decision index (quick reference table)
- Individual decisions with context, rationale, alternatives
- Status tracking (Active, Superseded, Deprecated)

**Purpose:** Enable engineers and AI to make correct UI decisions without designer intervention. Prevent design amnesia and re-litigation.

**When to create UX Foundation:**
- **Always create** brand system spec if project has UI
- **Skip** for API-only or CLI projects
- **Reference class is critical** — if you can't name what the product is "like", the UX will be inconsistent

**UX Role in Discovery:**
- PM + UX collaborate on reference class selection
- UX leads brand system specification (colours, typography, spacing, motion)
- UX initializes design decision log (empty but structured)
- **Brand Page in Storybook** — first Storybook entry, auto-generated from token files, visual proof that the brand system works before component development begins
- Generate `tokens/` from the brand system spec, run `npm run tokens:build` to produce CSS + Tailwind output

#### 7. Tech Stack Agreement (`/docs/architecture/tech-stack-agreement.md`)
**Contains:**
- Selected modules from module registry
- Rationale for each selection (linked to Discovery findings)
- Integration guides that apply (automatically derived from module registry)
- Module dependency graph for this project
- Any modules explicitly excluded and why

**Purpose:** Drives post-Discovery module installation. Nothing is installed until this agreement is approved.

**Format:**
```yaml
# Tech Stack Agreement — {project-name}
# Generated during Discovery, approved by PM

selected_modules:
  - aws-infrastructure    # Q3: AWS multi-account required
  - amplify               # Q3b: Web app confirmed
  - auth                  # Q3b: User auth required
  - email                 # Q3b: Verification + invitation emails
  - testing               # Always included
  - ui-styling            # Q3b: Web UI with shadcn
  - cicd                  # Always included
  - posthog               # Q3b: Analytics wanted
  - security              # Always included

applicable_integrations:
  - guides/integrations/cognito-ses.md
  - guides/integrations/auth-testing.md
  - guides/integrations/amplify-esm.md
  - guides/integrations/cicd-amplify-polling.md
  - guides/integrations/ses-per-account.md

excluded_modules:
  - flutter               # No mobile app needed at this stage
```

### Phase 4: Validation and Linear Integration

**A. Documentation Validation**
```
Invoke docs-quality-agent:
Task: Validate all created documents for:
  - Frontmatter compliance
  - Bidirectional linking
  - Documentation standards
  - Fix issues automatically where safe
```

**B. Container Feature Check**

Before creating Linear features, verify container features are identified:
- *"Do the content features identified have a container/shell they live within?"*
- *"Is that container already built, or does it need its own feature?"*
- *"Are there multiple platforms (web, mobile) that need separate containers?"*

If container features are missing, create them before content features. Container features should block the content features that depend on them.

**C. Linear Features Creation**
```
Invoke af-work-management-agent:
Task: Create Linear epic and features:
  - Epic: Product/project name
  - Container Features: App shell, navigation (per platform)
  - Content Features: From entity model capabilities or top-down feature list
  - Entity Epics: Parent issues for entities with capability sub-issues
  - Blocking: Container features block their content features
  - Attach: All discovery documentation
  - Defaults: Backlog state, priority=2
```

**D. Discovery Estimates**

After creating Linear features, provide feature-level effort estimates:

```
Load af-estimate-effort:
  - For each feature: decompose by functional area, estimate hours, convert to points
  - Set story points on each Linear feature issue
  - Post a [Discovery Estimate] comment on each feature (structured format from skill)
  - Confidence is typically Low or Medium at this stage
  - These estimates will be refined during Refinement phase
```

**Linear structure uses Milestones to group related issues:**

```
📋 Milestone: "[Delivery Goal]" (e.g., "Auth MVP", "v1.0")
  ├── Issue: "[App Shell & Navigation]" (Container)  ← blocks content
  ├── Issue: "[Capability 1]" (e.g., "Login Flow")
  ├── Issue: "[Capability 2]" (e.g., "Registration")
  └── Issue: "[Capability 3]" (e.g., "Password Reset")
```

**Milestone creation:**
- Create a Milestone for each coherent delivery goal
- Group issues that should ship together
- Use descriptive names: "Auth MVP", "Task Management v1", "Q2 Release"
- Milestones replace the old "Epic" parent issue pattern

**Issue creation:**
- One issue per deliverable capability
- Container issues (app shell, navigation) block content issues
- Do NOT create sub-issues during Discovery — sub-issues are created during Refinement
- When sub-issues are later created in Refinement, they must follow the sub-issue creation policy (see `af-manage-work-state`): parent must exceed 2 days of effort, each sub-issue must be ≥2 days, and work must be genuinely independent. [Behaviour] and [UX] sub-issues are exempt.

**Entity-driven decomposition:**
- If using entity-driven approach, each entity capability becomes an issue (not a sub-issue)
- The "entity" itself is not a Linear construct — it's a conceptual grouping in your entity model document
- Capabilities are independently deliverable, so they're issues

**Prioritization:** Use Linear's native tools (milestones, cycles, priority flags) instead of version labels. Do not use v1/v2/future labels in Discovery.

**Context attached to features:**
- Project overview document
- Technical ADRs
- User analysis
- Entity model (if entity-driven)
- Search findings (if research performed)

## Container vs Content Features

When identifying features, distinguish between **two classes**:

### Container Features (Shell/Framework)
Features that provide the application structure other features live within:
- **App Shell** — layout grid, header, sidebar, main content area
- **Navigation** — view switching, routing, sidebar items, keyboard shortcuts, deep links
- **Authentication Shell** — login screens, auth guards, session management UI
- **Settings Framework** — settings page structure, preferences storage

### Content Features (Views/Pages)
Features that provide functionality within the container:
- Dashboard views, detail pages, forms, reports
- Individual workflows and user journeys
- Data visualizations and widgets

### Why This Matters

Content features depend on container features. If Discovery identifies "My View", "Project View", and "Team View" but not the app shell they sit in, then:
- Refine creates Storybook components with no shell to compose into
- Delivery agents have no designed navigation pattern to wire views into
- The shell grows ad-hoc instead of being designed

### Container Feature Rules

1. **Identify containers alongside content** — When listing features, always ask: "What container(s) do these features live within?"
2. **One container per platform** — A web/desktop app has its own shell; a mobile app has its own shell (bottom tabs, hamburger menu, etc.). Create separate container features per platform.
3. **Refine containers first** — Container features should be refined BEFORE or CONCURRENTLY with the first content feature, since content depends on the shell.
4. **Containers block content** — In Linear, container features should block content features that depend on them.

### Example: Multi-Platform Product
```
📋 "MyProduct" (Epic)
  ├── 🏗️ "Web App Shell & Navigation" (Container, v1)     ← blocks all web views
  ├── 📱 "Mobile App Shell & Navigation" (Container, v1)   ← blocks all mobile views
  ├── 📊 "Dashboard View" (Content, v1)                    ← blocked by web shell
  ├── 👤 "Profile View" (Content, v1)                      ← blocked by web + mobile shell
  └── ⚙️ "Settings View" (Content, v2)                     ← blocked by web shell
```

## Feature Decomposition Approaches

Discovery can decompose features using different approaches. Choose based on the product's nature:

| Approach | When to Use | Output |
|----------|------------|--------|
| **Top-down** (workflow/view-driven) | Users think in workflows; views are independent; simple domain | Feature list per view/workflow |
| **Entity-driven** (bottom-up) | Rich shared entities across views; incremental capability delivery; many capabilities per entity | Entity model with capability sub-issues |
| **Hybrid** | Started top-down, realized entities are shared across views | Composition views + entity capabilities |

### Top-Down Decomposition
Identify user workflows and views first, then break into features:
```
Product → Views/Workflows → Features
"Sign Up Flow" → Feature: Email signup, Feature: Social login, Feature: Email verification
```

### Entity-Driven Decomposition
Identify entities first, then derive features from capabilities:
```
Product → Entities → Capabilities → Features (as Linear sub-issues)
                  → Composition Views (reference entity capabilities)
```

**Entity-driven process:**
1. **Identify entities** — What are the "things" in the system?
2. **Find the central entity** — "What's THE entity users care most about?"
3. **Classify** — User-facing (Task, User, Project) vs behind-the-scenes (Agent, Worktree)
4. **List capabilities** per entity — Each becomes a Linear sub-issue
5. **Identify composition views** — Views that combine entity capabilities (e.g., "My View" = my tasks + my time + my costs)

**Linear structure for entity-driven:**
```
Entity (parent, labeled Epic)
  ├── Capability 1 (sub-issue)
  ├── Capability 2 (sub-issue)
  └── Capability N (sub-issue)

Composition View (separate feature)
  → References which entity capabilities it includes
```

**Important:** Mark entity parent issues as Epics in Linear. Note in the description: "This is an entity Epic. Capabilities are delivery chunks — refine as one PRD, not separate PRDs per capability."

### Discovery Sketches, Refinement Specifies

Discovery captures what you know at a sketch level. Refinement fleshes it out:
- **Discovery depth:** Entities, relationships, capabilities, indicative attributes
- **Refinement depth:** Exact API contracts, BDD scenarios, Storybook stories, selector contracts
- Deeper Discovery knowledge helps Refinement (more context) but doesn't constrain it
- Refinement always does its own Three Amigos analysis and may revise Discovery's sketch

## Atomic Features

When breaking Epics into Features, each Feature must be **atomic**:

| Principle | Description |
|-----------|-------------|
| **One thing** | Does ONE unit of functionality, not a collection |
| **Front-to-back** | From UI to backend to database |
| **Complete** | Includes happy path + all edge cases |
| **Independent** | Deliverable on its own (given dependencies exist) |
| **Dependency-creating** | Creates what it needs if not present |

**Example breakdown:**
```
Epic: Multi-Tenant Authentication
  ├── Feature: User can sign up with email
  ├── Feature: User can verify email
  ├── Feature: User can sign in
  ├── Feature: User can sign out
  └── Feature: User can reset password
```

Each Feature becomes ONE Linear Issue with ONE Mini-PRD.

See [Atomic Refinement Guide](../../docs/guides/atomic-refinement-guide.md) for full details on outside-in development and scenario coverage.

---

## Decision Points

### Should I do external research?
- **Unfamiliar API mentioned?** → YES (search-agent)
- **Standard tech stack?** → NO (use AgentFlow patterns)
- **User provided detailed docs?** → NO (sufficient context)
- **Complex integration unclear?** → YES (research patterns)

### How many ADRs should I create?
- **Minimum:** 1 (technology stack)
- **Typical:** 2-3 (stack, integration, auth)
- **Complex projects:** 4-6 (add deployment, data model, security)

### Which agent should handle which task?
- **External research** → search-agent
- **Documentation validation** → docs-quality-agent
- **Linear features** → af-work-management-agent
- **Architecture decisions** → Orchestrator directly

## Common Pitfalls

1. **Skipping context questions**
   - All 4 questions MUST be asked
   - Incomplete context leads to wrong architecture

2. **Feature-level discovery**
   - Discovery is for products/projects, not individual features
   - Redirect to Refinement phase for features

3. **Incomplete deliverables**
   - All 7 documents MUST be created (6 if API-only/no UI)
   - Partial documentation causes confusion later

4. **Missing ADRs**
   - Document all significant architectural decisions
   - Future developers need this context

5. **Not validating documentation**
   - Always run docs-quality-agent
   - Broken links/metadata cause issues later

6. **Over-researching**
   - Only research when truly needed
   - Avoid unnecessary external searches

7. **Skipping UX foundation**
   - Brand guidelines and reference class MUST be defined for UI projects
   - Without reference class, UX decisions will be inconsistent
   - Design decision log prevents re-litigation later

8. **Missing container features**
   - Discovery identifies content features (views, pages) but forgets the container they live in
   - The app shell, navigation, and layout are features too — they need Storybook, BDD, and UX specs
   - Without a container feature, content features get refined in isolation with no designed shell
   - For multi-platform products, each platform needs its own container feature (web shell vs mobile shell)
   - Always ask: "What container do these features sit within? Is it already built or does it need a feature?"

9. **Bundling capabilities into single features**
   - Each entity capability should be its own Linear sub-issue, not bundled into the entity parent
   - Bundled capabilities can't be independently prioritized, assigned, or tracked
   - Example: "Task Display", "Task Status Lifecycle", "Task Estimates" are separate sub-issues under the Task entity — not one "Task" feature
   - If a capability can be shipped independently, it should be its own issue

10. **Using version labels for prioritization**
    - Don't use v1/v2/future labels in Discovery documents or Linear
    - Use Linear's native tools: milestones, cycles, and priority flags
    - Version labels create artificial constraints that don't match how prioritization actually works

11. **Skipping tech stack selection**
    - Module selection MUST happen during Discovery, not during ad-hoc setup later
    - Without a Tech Stack Agreement, modules get installed reactively when needed, missing integration guides
    - The module registry at `.claude/docs/reference/module-registry.yml` ensures all dependencies and integrations are captured

## Integration with Other Phases

**Before Discovery:**
- ← **Setup Phase** - Project infrastructure already configured
- ← **Ideation** (optional) - Brainstorming outputs in `docs/context/` (see `af-brainstorm-ideas` skill)

**After Discovery:**
- → **Refinement phase** - Select Linear features for detailed BDD specs
- → Refinement creates Markdown scenarios and sub-issues
- → Refinement refines effort estimates (1,2,3,5,8,13)
- → Refinement obtains human approval before implementation

**Discovery provides foundation for:**
- Feature prioritization decisions
- Technical architecture choices
- User experience design
- Implementation phasing

## Success Criteria

Discovery session complete when:
- ✅ All 4 context questions answered comprehensively
- ✅ External research completed (if needed)
- ✅ All 7 deliverables created and documented (6 if no UI)
- ✅ Entity model created with central entity identified and capabilities listed
- ✅ UX foundation established: reference class declared, brand system spec created, design decision log initialized, Storybook Brand Page generated (UI projects)
- ✅ Behavioral calibration matrix included in User Analysis (UI projects only)
- ✅ Container features identified (app shell, navigation per platform) alongside content features
- ✅ Documentation validated (frontmatter, links, standards)
- ✅ Milestone(s) created for delivery goals
- ✅ Issues created (not sub-issues) for each capability, grouped under Milestones
- ✅ No sub-issues created (those come from Refinement phase)
- ✅ Container issues block content issues
- ✅ No version labels used — prioritization via Linear milestones/cycles/priority
- ✅ Discovery Estimates posted on all new/changed issues (using af-estimate-effort skill)
- ✅ Tech Stack Agreement created with selected modules and rationale
- ✅ Module dependencies and applicable integration guides identified
- ✅ Discovery documentation attached to Linear issues
- ✅ User acknowledges readiness for Refinement phase

## Detailed Reference

**For complete discovery documentation:**
- Read `.claude/docs/guides/discovery-guide.md` (full workflow with examples)

**For Linear integration:**
- Read `.claude/agents/af-work-management-agent.md` (Linear API usage)

**For ADR templates:**
- ADR template: `.claude/templates/adr-template.md`
- ADR index template: `.claude/templates/adr-index.md`
- Load `af-decide-architecture` skill for ADR guidance

**For documentation standards:**
- Load `af-enforce-doc-standards` skill
- Read `.claude/docs/standards/documentation-standards.md`

## Tips for Effective Discovery

**For orchestrators:**
- Ask all 4 questions completely, don't skip
- Take detailed notes from user responses
- Create rich, specific documentation (not generic)
- Document decisions and rationale clearly

**For users:**
- Be specific with concrete examples
- Think holistically about all user types
- Share existing tools and constraints
- Provide measurable success criteria
