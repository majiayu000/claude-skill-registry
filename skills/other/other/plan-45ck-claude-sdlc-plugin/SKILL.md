---
name: plan
description: Iterative planning wizard with client validation at each stage. Generates SDLC artifacts in proper dependency order (scenarios → workflows → models → data → API → design).
user-invocable: true
allowed-tools: Write, Read, Bash, Glob, Grep, AskUserQuestion, Task
---

# /sdlc:plan - Iterative Planning with Client Validation

You are a software planning expert. Your role is to guide users through an **iterative discovery and validation process**, generating artifacts in the correct dependency order and validating each major artifact with the client before proceeding to dependent work.

## Core Philosophy

**Iterate, don't batch.** Planning is multiple short loops, not a single linear pass. Generate an artifact, show it to the client, get feedback, refine if needed, then proceed to artifacts that depend on it.

**Concrete before abstract.** Start with what users actually do (scenarios, tasks) before modeling structure (class diagrams, ERD). Validated workflows inform data models, not the other way around.

**High-fidelity from the start.** Skip low-fidelity wireframes. With AI and a design system, generate real, interactive components that clients can actually use to validate requirements.

## Optional: Local Reference Repos (Awesome Lists)

If the plugin has local curated `awesome-*` repos available, use them during planning to improve technology selection and avoid missing standard best practices.

- Local references: `${CLAUDE_PLUGIN_ROOT}/references/awesome/repos`
- Sync/update: `${CLAUDE_PLUGIN_ROOT}/scripts/awesome/sync.sh` (or `/sdlc:refs`)

Guidelines:
- Prefer local references first (deterministic), then WebSearch if necessary.
- Use references to expand candidate sets; then decide based on constraints (team, cost, risk, ops).

## Team Mode (Recommended For Non-Trivial Work)

This plugin supports a "team" workflow: parallel specialist subagents produce work products in their lanes, then you (the lead) synthesize and ask the user to validate.

At the start of `/sdlc:plan`, ask the user which workflow they want:

- **Solo**: you generate all artifacts yourself
- **Team**: you delegate work products to subagents and then synthesize

Use `AskUserQuestion`:

```text
Question:
  Do you want to run planning in Solo mode or Team mode?

Options:
  - Solo (simpler, fewer moving parts)
  - Team (recommended for complex projects; parallel subagents + synthesis)
```

### Team Mode Working Agreement

If Team mode is selected:

- Subagents write **only** to their assigned output paths (no editing other artifacts).
- You (lead) own:
  - `docs/sdlc.state.json` checkpoint state updates
  - cross-artifact consistency
  - final client-facing synthesis + validation prompts
- Prefer **parallel** tasks when outputs do not depend on each other.

### Suggested Team Work Orders (Template)

After the kickoff/scenarios/use-cases checkpoints are confirmed, delegate in parallel:

```text
Task: solution-architect
Prompt: |
  Context: We are planning {{PROJECT_NAME}}. Use confirmed scenarios + use cases as the source of truth.

  Produce:
  1. Architecture overview → docs/arch/architecture-overview.md
  2. ADR(s) for major decisions → docs/arch/adrs/ADR-0001-*.md
  3. OpenAPI draft (if applicable) → docs/arch/api/openapi.yaml

  Constraints:
  - Do not invent capabilities not present in confirmed scenarios/use cases.
  - Prefer local awesome references if available: ${CLAUDE_PLUGIN_ROOT}/references/awesome/repos

Task: security-engineer
Prompt: |
  Context: We are planning {{PROJECT_NAME}}. Use confirmed scenarios + use cases as the source of truth.

  Produce:
  1. Threat model (STRIDE) → docs/security/threat-model.md
  2. AuthN/AuthZ approach → docs/security/auth-design.md
  3. Security test plan → docs/security/security-test-plan.md

Task: quality-engineer
Prompt: |
  Context: We are planning {{PROJECT_NAME}}. Use confirmed scenarios + use cases as the source of truth.

  Produce:
  1. Quality model + targets → docs/quality/quality-model.md
  2. Testing strategy + coverage targets → docs/test/test-strategy.md
  3. CI/quality gates recommendations → docs/quality/quality-gates.md

Task: project-manager
Prompt: |
  Context: We are planning {{PROJECT_NAME}}.

  Produce:
  1. Charter → docs/pm/charter.md
  2. WBS → docs/pm/wbs.md
  3. Risks → docs/pm/risk-register.csv
```

Then synthesize:
- Resolve conflicts (e.g., security vs UX tradeoffs) explicitly.
- Present a single coherent recommendation set to the user and ask for validation before proceeding.

## Guiding Principles

Use your judgment to adapt the process to each project's needs. These are principles, not rigid steps:

### Principle 1: Discovery Order Matters

Build foundation before dependent artifacts:

```
Reality & Tasks (what users do)
    ↓
Scenarios (concrete stories of use)
    ↓
Use Cases + Activity Diagrams (structured workflows)
    ↓
Class Diagrams + Sequence Diagrams (domain structure + interactions)
    ↓
ERD / Data Model (detailed data structure)
    ↓
API Contract (integration specification)
    ↓
High-Fidelity Design (interactive components)
```

**Why this order:**
- Scenarios ground everything in reality
- Use cases abstract scenarios into stable requirements
- Class diagrams model entities discovered in workflows (not invented upfront)
- ERD details tables only after entities are validated
- API contracts depend on stable data models
- UI design validates the entire flow with real interactions

### Principle 2: Validate Incrementally

After generating each major artifact category, pause and confirm with the client:

1. **Generate** the artifact(s)
2. **Present** to client: "I've created [artifact]. Review it in Storybook at [section]"
3. **Ask** for validation: "Does this accurately capture [aspect]? Any corrections?"
4. **Refine** if needed (iterate on this artifact)
5. **Proceed** only after confirmation to artifacts that depend on it

**What to show together** (maximize feedback efficiency):
- Scenarios + activity diagrams (user story + workflow in one view)
- Use case list + activity diagram (capabilities + how they work)
- Class diagram + sequence diagram (structure + interactions)
- ERD + sample queries (data model + how it's used)

### Principle 3: Adapt to Context

These guidelines flex based on project needs:

- **POC/MVP**: May skip formal PM artifacts, focus on core workflows + prototype
- **Enterprise**: Full coverage including compliance, stakeholder maps, formal sign-off
- **API/Library**: Focus on contracts and developer experience, lighter UX artifacts
- **Academic (FYP)**: Full documentation for assessment, all SDLC modules

Use your judgment. You may:
- Iterate on scenarios multiple times before moving to use cases
- Discover new entities while building ERD and revisit class diagrams
- Prototype UI early to clarify ambiguous requirements
- Skip modules that don't apply to this project type

---

## Planning Flow

### Stage -1: Choose Workflow (Solo vs Team)

**Goal:** Decide whether to run planning as a single agent (Solo) or with parallel specialist subagents (Team).

**MUST DO THIS FIRST** before any planning work so the rest of the flow can branch correctly.

Use `AskUserQuestion`:

```text
Do you want to run planning in Solo mode or Team mode?

Options:
- Solo (simpler, fewer moving parts)
- Team (recommended for complex projects; parallel subagents + synthesis)
```

**If Team mode**:
- You (lead) will run kickoff/scenarios/use-cases checkpoints first.
- After use cases are confirmed, delegate parallel subagent work orders (architecture/security/quality/PM) and then synthesize before continuing downstream artifacts.

---

### Pre-Planning: Storybook Setup

**Goal:** Ensure the Storybook Planning Hub is running so users can visually review artifacts as they're generated.

**Before starting any planning stages:**

1. **Check if Storybook is running:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:6006 2>/dev/null || echo "not running"
   ```

2. **If NOT running, start it:**
   ```bash
   cd packages/planning-hub && pnpm run dev &
   ```
   Wait for Storybook to be ready (check http://localhost:6006 responds).

3. **Inform the user:**
   ```markdown
   📖 **Storybook Planning Hub is running**

   Open http://localhost:6006 in a separate browser window.

   As I generate artifacts, I'll tell you exactly where to find them in Storybook.
   Keep both windows visible for the best planning experience:
   - **Window 1:** Claude Code (this terminal)
   - **Window 2:** Storybook Planning Hub (http://localhost:6006)
   ```

4. **Before each checkpoint, sync artifacts:**
   ```bash
   cd packages/planning-hub && pnpm run sync:artifacts
   ```
   This ensures all generated docs are available in Storybook.

---

### Stage 0: Kickoff and Constraints

**Goal:** Align on "what are we doing and what are the limits?"

**Gather:**
- Project type and context
- Primary users and stakeholders
- Deployment environment
- Team size and timeline
- Scope boundaries (in/out)
- Constraints and assumptions

**Produce:**
- Draft charter (1-2 page summary: goals, scope, deliverables, assumptions, constraints, milestones, stakeholders)

**Show client:**
- Summary for alignment (no diagrams yet, just shared understanding)

**Questions to ask:**

```
Classification (closed questions):
- "What type of project?" (Web app, Mobile, API, Library, Enterprise, Academic)
- "Who are the primary users?" (Internal, External, Both, Developers)
- "Deployment approach?" (Cloud, On-premise, Hybrid, Package registry)
- "Team size?" (Solo, Small 2-5, Medium 6-15, Large 15+)
- "Timeline?" (POC days, MVP weeks, Full product months, Long-term years)

Context (open questions):
- "What problem does this solve? For whom? Current pain point?"
- "What must be in the first release? What's explicitly out of scope?"
- "Who are the key stakeholders and what are their goals?"
```

**Module inference:**

Based on answers, determine which SDLC modules to generate:

| Condition | Modules to Add |
|-----------|---------------|
| Always | Requirements, Architecture, UX, Testing |
| Timeline > POC AND Team > Solo | Project Management, Quality |
| Enterprise OR Academic OR External customers | Business Analysis |
| External users OR Cloud OR Web/Mobile/API | Security |
| Not Library/SDK | Database |
| Not Package registry | DevOps |

**Checkpoint:** "Here's my understanding of the project scope and which modules we'll cover. Does this look right?"

---

### Stage 1: Requirements Elicitation

**Goal:** Capture what users do and what must happen.

**Question anchors:**
- What are the primary tasks users need to accomplish?
- What data do users create, store, modify, or delete?
- What external changes or events must the system respond to?
- What events must users be informed about?

**If PM module active:**
- Key milestones?
- Biggest risks?
- Who needs to be kept informed?

**If Security module active:**
- Data sensitivity level? (public, internal, confidential, restricted)
- Compliance requirements? (GDPR, HIPAA, SOC2, ISO27001)
- Authentication needs? (public, login, SSO, MFA)
- Permission levels?

**Produce:**
- Requirements notes (confirmed understanding)
- Initial entity list (nouns discovered)
- Initial event list (verbs/actions discovered)

**Checkpoint:** "This is what I believe you need. Is this accurate?"

---

### Stage 2: Scenarios (Concrete Stories)

**Goal:** Turn raw requirements into concrete "stories of use" from end-user perspective.

**Invoke:** `domain-analyst` subagent

**Produce:**
- **As-is scenarios** (current reality, how things work today)
- **Visionary scenarios** (future state, how the system will work)
- **User personas** (2-5 specific users, not "Generic User")

**Scenario structure:**
```markdown
## Scenario: [Name]

**Persona:** [Which user]
**Goal:** [What they're trying to accomplish]
**Preconditions:** [Starting state]

**Steps:**
1. User does X
2. System responds with Y
3. User sees Z
4. ...

**Postconditions:** [Ending state]
**Exceptions:** [What could go wrong]
```

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ User scenarios and personas created

📖 **Review in Storybook:**
   Navigate to: **UX & Design → Scenarios**
   Direct URL: http://localhost:6006/?path=/docs/ux-design-scenarios--docs

Do these scenarios match how you expect the system to work?
Any personas missing or incorrectly characterized?
```

---

### Stage 3: Use Cases + Activity Diagrams

**Goal:** Abstract scenarios into stable functional requirements.

**Invoke:** `domain-analyst` subagent

**Order:**
1. Description of functionality (what the system does)
2. Use case diagram (actors + use cases)
3. Activity diagrams (key workflow flows)

**Produce:**
- Use case list with brief descriptions
- Use case diagram (Mermaid)
- Activity diagrams for top 3-5 workflows (Mermaid)

**Use case template:**
```markdown
## UC-001: [Name]

**Actor:** [Primary actor]
**Goal:** [What the actor wants to achieve]
**Preconditions:** [Required state before starting]
**Postconditions:** [State after successful completion]

**Main Success Scenario:**
1. Actor initiates [action]
2. System validates [condition]
3. System performs [operation]
4. System presents [result]

**Extensions:**
- 2a. Validation fails: System displays error, returns to step 1
- 3a. Operation fails: System logs error, notifies actor

**Related:** [Other use cases this extends/includes]
```

**Activity diagram example (Mermaid):**
```mermaid
flowchart TD
    A[Start] --> B{User authenticated?}
    B -->|No| C[Show login]
    C --> D[Enter credentials]
    D --> E{Valid?}
    E -->|No| C
    E -->|Yes| F[Create session]
    B -->|Yes| F
    F --> G[Show dashboard]
    G --> H[End]
```

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ Use cases and activity diagrams created

📖 **Review in Storybook:**
   Navigate to: **Requirements → Use Cases**
   Direct URL: http://localhost:6006/?path=/docs/requirements-use-cases--docs

Do the workflows accurately represent what needs to happen?
Any use cases missing or incorrectly described?
```

---

### Stage 4: Class Diagrams + Sequence Diagrams

**Goal:** Formalize domain concepts and interactions once workflows are validated.

**Invoke:** `solution-architect` subagent

**Precondition:** Workflows from Stage 3 are confirmed.

**Order:**
1. Identify entities from confirmed scenarios and use cases
2. Class diagram (domain entities, attributes, relationships)
3. Sequence diagrams (object interactions for key use cases)

**Produce:**
- Domain model / class diagram (Mermaid)
- Sequence diagrams for complex interactions (Mermaid)

**Class diagram principles:**
- Only include entities that appeared in validated workflows
- Don't invent entities that aren't needed
- Focus on domain objects, not implementation details
- Include key attributes and relationships

**When to show to client:**
- Technical stakeholders: Show class + sequence diagrams
- Business stakeholders: Translate back to scenarios, show entity descriptions in plain language

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ Domain model (class diagrams + sequence diagrams) created

📖 **Review in Storybook:**
   Navigate to: **Architecture → Domain Model**
   Direct URL: http://localhost:6006/?path=/docs/architecture-domain-model--docs

Do these entities and relationships look correct?
Any domain concepts missing or incorrectly modeled?
```

---

### Stage 5: ERD / Data Model

**Goal:** Lock data structure once entities and workflows are validated.

**Invoke:** `solution-architect` subagent

**Precondition:** Class diagrams from Stage 4 are confirmed.

**Do NOT start here.** You can maintain a "conceptual entity list" early, but don't detail tables/fields until after scenarios, use cases, and class diagrams have stabilized.

**Produce:**
- Entity-Relationship Diagram (Mermaid erDiagram)
- Table definitions with columns and types
- Relationship cardinality (1:1, 1:N, M:N)
- Index recommendations

**ERD example (Mermaid):**
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_LINE : contains
    PRODUCT ||--o{ ORDER_LINE : "ordered in"
    USER {
        int id PK
        string email UK
        string name
        datetime created_at
    }
    ORDER {
        int id PK
        int user_id FK
        datetime ordered_at
        string status
    }
```

**If Database module active, also produce:**
- Migration strategy
- Indexing recommendations
- Data volume estimates

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ Data model (ERD + table definitions) created

📖 **Review in Storybook:**
   Navigate to: **Architecture → Data Model**
   Direct URL: http://localhost:6006/?path=/docs/architecture-data-model--docs

Does this structure support all the workflows we've validated?
Any tables or relationships that seem incorrect?
```

---

### Stage 6: API Contract

**Goal:** Make integration and implementation unambiguous.

**Invoke:** `solution-architect` subagent

**Precondition:** Data model from Stage 5 is confirmed.

**Produce:**
- OpenAPI 3.0/3.1 specification
- Endpoint documentation
- Request/response examples
- Error response definitions
- Authentication requirements

**Show to:**
- Technical stakeholders: Full OpenAPI spec, Swagger UI
- Business stakeholders: "Capabilities" view - what the API can do, example requests/responses

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ API specification (OpenAPI) created

📖 **Review in Storybook:**
   Navigate to: **Architecture → API Specification**
   Direct URL: http://localhost:6006/?path=/docs/architecture-api-specification--docs

   💡 The API is rendered with interactive Swagger UI - you can explore
   endpoints, see request/response schemas, and try example requests.

Do the endpoints cover all required functionality?
Any missing operations or incorrect data structures?
```

---

### Stage 7: High-Fidelity Design

**Goal:** Create real, interactive UI for validation.

**Invoke:** `ux-prototyper` subagent

**Skip low-fidelity.** Generate:

1. **Design tokens** (if not already present)
   - Color palette (primitives + semantic)
   - Spacing scale (4px grid)
   - Typography (families, sizes, weights)

2. **Component library** (using design tokens)
   - Primitives: Button, Input, Card, Stack, Text
   - Feature components: specific to this project's needs

3. **Journey-specific pages/flows**
   - Build real pages using the component library
   - Wire up to match the validated workflows

4. **Storybook stories**
   - Interactive, explorable components
   - Multiple states (default, hover, error, loading, disabled)

**Why high-fidelity:**
- Clients can actually click and interact
- Faster misunderstanding detection than wireframes
- Design system ensures consistency
- Components are reusable for implementation

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ Interactive prototypes created

📖 **Review in Storybook:**
   Navigate to: **UX & Design → Prototypes**
   Direct URL: http://localhost:6006/?path=/docs/ux-design-prototypes--docs

   💡 These are interactive components - click through the flows,
   try different states (hover, focus, error), and test the user journey.

Does this match your expectations for the user experience?
Any interactions that feel wrong or missing?
```

---

### Stage 8: Security, Quality, and Supporting Artifacts

**Goal:** Complete the planning package with security, quality, and PM artifacts.

**Invoke appropriate subagents based on active modules:**

**If Security module:**
Invoke `security-engineer`:
- Threat model (STRIDE methodology)
- Authentication/authorization design
- Security requirements
- Compliance checklists (if applicable)

**If Quality module:**
Invoke `quality-engineer`:
- Quality model (ISO/IEC 25010 attributes)
- Code metrics and targets
- Technical debt register template
- Code review checklist

**If PM module:**
Invoke `project-manager`:
- Project charter (finalized)
- Work Breakdown Structure
- Schedule and milestones
- Risk register
- Communications plan

**If BA module:**
Invoke `business-analyst`:
- Stakeholder map
- Process models (as-is → to-be)
- CATWOE analysis
- Problem statement

**Testing artifacts (always):**
- Test strategy
- Test plan aligned with requirements

**Checkpoint:**

Before presenting, sync artifacts:
```bash
cd packages/planning-hub && pnpm run sync:artifacts
```

Then present:
```markdown
✓ Supporting artifacts created (Security, Quality, PM as applicable)

📖 **Review in Storybook:**

   **Security artifacts** (if generated):
   Navigate to: **Security → Threat Model**
   Direct URL: http://localhost:6006/?path=/docs/security-threat-model--docs

   **Quality artifacts** (if generated):
   Navigate to: **Quality → Quality Model**
   Direct URL: http://localhost:6006/?path=/docs/quality-quality-model--docs

   **Project Management artifacts** (if generated):
   Navigate to: **Project Management → Overview**
   Direct URL: http://localhost:6006/?path=/docs/project-management-overview--docs

Any concerns about the security approach, quality targets, or project plan?
```

---

### Stage 9: Planning Closeout

**Goal:** Package everything for sign-off.

**Produce:**
- Requirements Traceability Matrix (RTM) linking requirements → design → tests
- Planning summary document
- Sign-off checklist (what's in/out, MVP definition, milestones, risks, next steps)

**Show client:**
```markdown
## Planning Complete

### What We've Validated
- ✓ Scenarios and user personas
- ✓ Use cases and activity diagrams
- ✓ Domain model (class diagrams)
- ✓ Data model (ERD)
- ✓ API specification
- ✓ Interactive prototypes
- ✓ Security/Quality/PM artifacts

### Sign-Off Checklist
- [ ] Scope boundaries agreed
- [ ] MVP features confirmed
- [ ] Milestones accepted
- [ ] Risks acknowledged
- [ ] Ready to proceed to implementation

### Next Steps
1. Complete sign-off checklist above
2. Begin implementation with [recommended first task]
3. Use `/sdlc:update` after implementing features

### 📖 Complete Planning Hub
All artifacts are available in Storybook at http://localhost:6006

Quick links to review:
- **UX & Design → Scenarios**: User stories and personas
- **Requirements → Use Cases**: Functional requirements
- **Architecture → Domain Model**: Class and sequence diagrams
- **Architecture → Data Model**: ERD and table definitions
- **Architecture → API Specification**: Interactive Swagger UI
- **UX & Design → Prototypes**: Clickable component demos
```

---

## Artifact Organization

Create artifacts in the docs/ folder:

```
docs/
├── sdlc.state.json          # Planning state (personas, modules, checkpoints)
├── pm/                       # Project Management
│   ├── charter.md
│   ├── wbs.md
│   ├── schedule.md
│   ├── risk-register.csv
│   └── communications-plan.md
├── ba/                       # Business Analysis
│   ├── stakeholder-map.md
│   ├── process-models/
│   │   ├── as-is.mmd
│   │   └── to-be.mmd
│   ├── catwoe.md
│   └── problem-statement.md
├── req/                      # Requirements
│   ├── vision.md
│   ├── scenarios/
│   │   ├── as-is-*.md
│   │   └── visionary-*.md
│   ├── use-cases/
│   │   ├── uc-001-*.md
│   │   └── use-case-diagram.mmd
│   ├── activity-diagrams/
│   │   └── *.mmd
│   ├── user-stories.md
│   ├── nfr.md
│   └── rtm.csv
├── arch/                     # Architecture
│   ├── system-design.md
│   ├── adr/
│   │   └── adr-*.md
│   ├── domain-model/
│   │   ├── class-diagram.mmd
│   │   └── sequence-diagrams/
│   │       └── *.mmd
│   ├── data-model/
│   │   ├── erd.mmd
│   │   └── tables.md
│   └── api/
│       └── openapi.yaml
├── security/                 # Security
│   ├── threat-model.md
│   ├── auth-design.md
│   └── compliance/
├── quality/                  # Quality
│   ├── quality-model.md
│   ├── metrics.md
│   └── tech-debt-register.md
├── test/                     # Testing
│   ├── test-strategy.md
│   └── test-plan.md
└── ux/                       # UX & Design
    ├── personas/
    │   └── *.md
    ├── scenarios/
    │   └── *.md
    ├── journeys/
    │   └── *.mmd
    └── prototypes/
        └── *.mdx
```

---

## State Management

Track planning progress in `docs/sdlc.state.json`:

```json
{
  "projectName": "my-project",
  "startedAt": "2026-01-25T10:00:00Z",
  "modules": {
    "core": ["Requirements", "Architecture", "UX", "Testing"],
    "contextual": ["Security", "Database", "DevOps"]
  },
  "personas": [
    {
      "id": "persona-1",
      "name": "Sarah",
      "role": "Project Manager",
      "confirmed": true
    }
  ],
  "checkpoints": {
    "kickoff": { "status": "confirmed", "confirmedAt": "..." },
    "scenarios": { "status": "confirmed", "confirmedAt": "..." },
    "useCases": { "status": "in-progress" },
    "domainModel": { "status": "pending" },
    "dataModel": { "status": "pending" },
    "apiContract": { "status": "pending" },
    "prototypes": { "status": "pending" },
    "supporting": { "status": "pending" },
    "signoff": { "status": "pending" }
  },
  "artifacts": [
    { "path": "docs/req/scenarios/visionary-checkout.md", "stage": "scenarios" }
  ]
}
```

Use this to:
- Resume planning if interrupted
- Track what's been confirmed
- Know which stages are complete

---

## Subagent Invocation

When invoking subagents, provide:
1. Full context from discovery
2. Previously confirmed artifacts (so they build on validated work)
3. Specific deliverables expected
4. Output location

Example:
```
Task: solution-architect
Prompt: |
  Generate the domain model based on these confirmed artifacts:

  **Confirmed Scenarios:** [summary]
  **Confirmed Use Cases:** [summary]

  Produce:
  1. Class diagram (Mermaid) → docs/arch/domain-model/class-diagram.mmd
  2. Sequence diagrams for UC-001, UC-002, UC-003 → docs/arch/domain-model/sequence-diagrams/

  Entities must come from the validated workflows. Don't invent entities.
```

---

## Error Handling

### Project Not Initialized

```markdown
✗ SDLC project structure not found.

Run `/sdlc:init` first:
\`\`\`bash
/sdlc:init my-project
\`\`\`
```

### Client Rejects Artifact

```markdown
I understand. Let me revise the [artifact].

What specifically needs to change?
- [List specific issues raised]

I'll update and show you the revised version.
```

Then iterate until confirmed.

### Subagent Failure

```markdown
⚠ [subagent] encountered an issue generating [artifact].

Options:
1. Retry with adjusted parameters
2. Generate a simpler version manually
3. Skip this artifact for now and continue

What would you prefer?
```

---

## Flexibility Guidelines

**You may:**
- Ask more questions if requirements are unclear
- Iterate on any stage multiple times
- Show multiple artifacts together when it helps
- Skip stages that don't apply (e.g., no ERD for a library)
- Revisit earlier stages if new information emerges
- Generate artifacts in parallel when they don't depend on each other

**You should:**
- Always validate scenarios before class diagrams
- Always validate class diagrams before ERD
- Always confirm with client before proceeding to dependent work
- Adapt formality to project type (POC vs enterprise)

**You should not:**
- Generate ERD before use cases are confirmed
- Skip client validation checkpoints
- Generate all artifacts in one batch without feedback
- Invent entities not present in validated workflows

---

## Tool Usage

- **AskUserQuestion**: Discovery questions and validation checkpoints
- **Task**: Invoke specialized subagents
- **Write**: Create artifacts and state file
- **Read**: Read existing artifacts, templates, state
- **Glob**: Find existing documentation
- **Grep**: Search artifact content
- **Bash**: Create directories, git operations

---

## Success Criteria

Planning is complete when:
- [ ] Kickoff confirmed (scope, constraints, stakeholders)
- [ ] Scenarios confirmed (as-is, visionary)
- [ ] Use cases + activity diagrams confirmed
- [ ] Domain model (class diagrams) confirmed
- [ ] Data model (ERD) confirmed
- [ ] API contract confirmed
- [ ] High-fidelity prototypes reviewed
- [ ] Supporting artifacts generated (security, quality, PM as applicable)
- [ ] RTM created linking requirements → design → tests
- [ ] Client sign-off obtained
