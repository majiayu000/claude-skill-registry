---
name: investigate
description: '[Fix & Debug] Investigate and explain how existing features or logic work. READ-ONLY exploration with no code changes.'
version: 2.1.0
allowed-tools: Read, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

## Quick Summary

**Goal:** READ-ONLY exploration of existing features and logic — understand how code works without making changes.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Discovery** — Search codebase for related files (Entities > Commands > Events > Controllers)
2. **Knowledge Graph** — Read and document purpose, symbols, dependencies per file
3. **Flow Mapping** — Trace entry points through pipeline to exit points
4. **Analysis** — Extract business rules, validation, authorization, error handling
5. **Synthesis** — Write executive summary with key files and flow diagrams
6. **Present** — Deliver findings, offer deeper dives on subtopics

**Key Rules:**

- Strictly READ-ONLY — no code changes allowed
- Evidence-based: every claim needs `file:line` proof (grep results, read confirmations)
- Mark unverified claims as "inferred" with low confidence
- Write analysis to `.ai/workspace/analysis/[feature-name]-investigation.md`
- For UI investigation, activate `visual-component-finder` skill FIRST

# Feature Investigation

READ-ONLY exploration skill for understanding existing features. No code changes.

## Investigation Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT assume code works as named — verify by reading actual implementations
- Every finding must include `file:line` evidence (grep results, read confirmations)
- If you cannot prove a claim with a code trace, mark it as "inferred" with low confidence
- Question assumptions: "Does this actually do what I think?" → read the implementation, not just the signature
- Challenge completeness: "Is this all?" → grep for related usages, consumers, and cross-service references
- Verify relationships: "Does A really call B?" → trace the actual call path with evidence
- No "looks like it works" without proof — state what you verified and how

## Summary

**Goal:** READ-ONLY exploration of existing features and logic — understand how code works without making changes.

| Step | Action          | Key Notes                                                                      |
| ---- | --------------- | ------------------------------------------------------------------------------ |
| 1    | Discovery       | Search codebase for related files (Entities > Commands > Events > Controllers) |
| 2    | Knowledge Graph | Read and document purpose, symbols, dependencies per file                      |
| 3    | Flow Mapping    | Trace entry points through pipeline to exit points                             |
| 4    | Analysis        | Extract business rules, validation, authorization, error handling              |
| 5    | Synthesis       | Write executive summary with key files and flow diagrams                       |
| 6    | Present         | Deliver findings, offer deeper dives on subtopics                              |

**Key Principles:**

- Strictly READ-ONLY — no code changes allowed
- MUST read evidence-based-reasoning-protocol.md and knowledge-graph-template.md before starting
- Evidence-based: validate every assumption with actual code references

> **UI/Frontend Investigation?** If investigating a UI component from a screenshot, image, or visual reference, activate `visual-component-finder` skill FIRST. It uses a pre-built component index (`docs/component-index.json`) to match visuals to Angular components with >=85% confidence before deeper investigation.

## Mode Selection

| Mode            | Use When                                     | Workflow                                           |
| --------------- | -------------------------------------------- | -------------------------------------------------- |
| **Interactive** | User available, exploratory question         | Real-time collaboration, iterative tracing         |
| **Autonomous**  | Deep analysis, complex cross-service tracing | Structured 4-phase workflow with analysis artifact |

## Workflow

1. **Discovery** - Search codebase for all files related to the feature/question. Prioritize: Entities > Commands/Queries > EventHandlers > Controllers > Consumers > Components.
2. **Knowledge Graph** - Read and analyze each file. Document purpose, symbols, dependencies, data flow. Batch in groups of 10, update progress after each batch.
3. **Flow Mapping** - Trace entry points through processing pipeline to exit points. Map data transformations, persistence, side effects, cross-service boundaries.
4. **Analysis** - Extract business rules, validation logic, authorization, error handling. Document happy path and edge cases.
5. **Synthesis** - Write executive summary answering the original question. Include key files, patterns used, and text-based flow diagrams.
6. **Present** - Deliver findings using the structured output format. Offer deeper dives on subtopics.

## ⚠️ MUST READ Before Investigation

**IMPORTANT: You MUST read these files before starting. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` — Assumption validation, evidence chains, context anchoring
- **⚠️ MUST READ** `.claude/skills/shared/knowledge-graph-template.md` — Per-file analysis structure

**If preceded by `/scout`:** Use Scout's numbered file list as analysis targets. Skip redundant discovery. Prioritize HIGH PRIORITY files first.

## Investigation Techniques

### Discovery Search Patterns

#### File Discovery by Feature Name

```regex
.*EventHandler.*{FeatureName}|{FeatureName}.*EventHandler
.*BackgroundJob.*{FeatureName}|{FeatureName}.*BackgroundJob
.*Consumer.*{FeatureName}|{FeatureName}.*Consumer
.*Service.*{FeatureName}|{FeatureName}.*Service
.*Component.*{FeatureName}|{FeatureName}.*Component
```

#### Priority Order for Analysis

1. **Domain Entities** - Core business objects
2. **Commands/Queries** - CQRS entry points (`UseCaseCommands/`, `UseCaseQueries/`)
3. **Event Handlers** - Side effects (`UseCaseEvents/`, `*EventHandler.cs`)
4. **Controllers** - API endpoints (`Controllers/`, `*Controller.cs`)
5. **Consumers** - Cross-service (`*Consumer.cs`, `*BusMessage.cs`)
6. **Background Jobs** - Scheduled processing (`*BackgroundJob*.cs`, `*Job.cs`)
7. **Components/Stores** - Frontend (`*.component.ts`, `*.store.ts`)
8. **Services/Helpers** - Supporting logic (`*Service.cs`, `*Helper.cs`)

### Dependency Tracing

#### Backend

| Looking for                    | Search pattern                                                           |
| ------------------------------ | ------------------------------------------------------------------------ |
| Who calls this method          | Grep method name across `*.cs`                                           |
| Who injects this service       | Grep interface name in constructors                                      |
| What events this entity raises | Grep `EntityEvent<EntityName>` (search for: project entity event class)  |
| Cross-service consumers        | Grep `*BusMessage` type across all services                              |
| Repository usage               | Grep `IRepository<EntityName>` or project queryable repository interface |

#### Frontend

| Looking for              | Search pattern                                                    |
| ------------------------ | ----------------------------------------------------------------- |
| Who uses this component  | Grep selector `app-component-name` in `*.html`                    |
| Who imports this service | Grep service class name in `*.ts`                                 |
| Store effects chain      | Trace `effectSimple` -> API call -> `tapResponse` -> state update |
| Route entry              | Grep component name in `*routing*.ts`                             |

### Data Flow Mapping

Document flow as text diagram:

```text
[Entry Point] --> [Step 1: Validation] --> [Step 2: Processing] --> [Step 3: Persistence]
                                                  |
                                                  v
                                          [Side Effect: Event]
```

#### Flow Documentation Checklist

1. **Entry Points** - API endpoint, UI action, scheduled job, message bus
2. **Processing Pipeline** - Step-by-step through handlers
3. **Data Transformations** - How data changes at each step
4. **Persistence Points** - Where data is saved/loaded
5. **Exit Points** - Responses, events, side effects
6. **Cross-Service Flows** - Message bus boundaries

### Common Investigation Scenarios

#### "How does feature X work?"

1. Find entry points (API, UI, job)
2. Trace through command/query handlers
3. Document entity changes
4. Map side effects (events, notifications)

#### "Where is the logic for Y?"

1. Search keywords in commands, queries, entities
2. Check event handlers for side effect logic
3. Look in helper/service classes
4. Check frontend stores and components

#### "What happens when Z occurs?"

1. Identify trigger (user action, event, schedule)
2. Trace the handler chain
3. Document all side effects
4. Map error handling

#### "Why does A behave like B?"

1. Find the relevant code path
2. Identify decision points
3. Check configuration/feature flags
4. Document business rules

### Project Pattern Recognition (see docs/project-reference/backend-patterns-reference.md and docs/project-reference/frontend-patterns-reference.md)

#### Backend Patterns

- CQRS command / query base classes - CQRS entry points
- Entity event application handler - Side effects
- Message bus consumer base class - Cross-service consumers
- Project queryable root repository - Data access
- Project validation fluent API - Validation logic
- Project authorization attributes - Authorization

#### Frontend Patterns

- Project store component base (search for: store component base class) - State management components
- Project store base (search for: store base class) - Store implementations
- `effectSimple` / `tapResponse` - Effect handling
- `observerLoadingErrorState` - Loading/error states
- API services extending project API service base class

## Evidence Collection

### Analysis File Setup

**MANDATORY (all modes):** Write analysis to `.ai/workspace/analysis/[feature-name]-investigation.md`. Re-read ENTIRE file before presenting findings in Step 6. This prevents knowledge loss during long investigations.

Analysis file structure:

```markdown
## Metadata

> Original question: [user's exact question]

## Investigation Question

[Clearly stated investigation goal]

## Progress

- **Phase**: 1
- **Items Processed**: 0 / [total]
- **Current Focus**: [original question]

## File List

[All discovered files, grouped by priority]

## Knowledge Graph

[Per-file analysis entries - see template below]

## Data Flow

[Flow diagrams and pipeline documentation]

## Findings

[Populated in Phase 2+]
```

### Per-File Analysis Entry

For each file, document in `## Knowledge Graph`:

#### Core Fields

- `filePath`: Full path
- `type`: Component classification (Entity, Command, Handler, Controller, Component, Store, etc.)
- `architecturalPattern`: Design pattern used
- `content`: Purpose and logic summary
- `symbols`: Key classes, interfaces, methods
- `dependencies`: Imports/injections
- `relevanceScore`: 1-10 (to investigation question)
- `evidenceLevel`: "verified" or "inferred"

#### Investigation-Specific Fields

- `entryPoints`: How this code is triggered/called
- `outputPoints`: What this code produces/returns
- `dataTransformations`: How data is modified
- `conditionalLogic`: Key decision points and branches
- `errorScenarios`: What can go wrong, error handling
- `externalDependencies`: External services, APIs, databases

#### Cross-Service Fields (if applicable)

- `messageBusMessage`: Message type consumed/produced
- `messageBusProducers`: Who sends this message
- `crossServiceIntegration`: Cross-service data flow

**Rule:** After every 10 files, update progress and re-check alignment with original question.

### Structured Findings Format

#### Phase 2: Comprehensive Analysis

##### Workflow Analysis

1. **Happy Path** - Normal successful execution flow
2. **Error Paths** - How errors are handled at each stage
3. **Edge Cases** - Special conditions
4. **Authorization** - Permission checks
5. **Validation** - Input validation at each layer

##### Business Logic Extraction

1. **Core Business Rules** - What rules govern this feature
2. **State Transitions** - Entity state changes
3. **Side Effects** - Notifications, events, external calls

#### Phase 3: Synthesis

##### Executive Summary

- One-paragraph answer to user's question
- Top 5-10 key files
- Key patterns used

##### Detailed Explanation

- Step-by-step walkthrough with `file:line` references
- Architectural decisions explained

##### Diagrams

```text
+-----------+     +-----------+     +-----------+
| Component |---->|  Command  |---->|  Handler  |
+-----------+     +-----------+     +-----------+
                                          |
                                          v
                                    +-----------+
                                    |Repository |
                                    +-----------+
```

## Output Format

```markdown
## Answer

[Direct answer in 1-2 paragraphs]

## How It Works

### 1. [Step] - [Explanation with `file:line` reference]

### 2. [Step] - [Explanation with `file:line` reference]

## Key Files

| File | Purpose |
| ---- | ------- |

## Data Flow

[Text diagram: Entry -> Processing -> Persistence -> Side Effects]

## Want to Know More?

- [Subtopic 1]
- [Subtopic 2]
```

## Guidelines

- **Evidence-based**: Every claim needs code evidence. Mark unverified claims as "inferred".
- **Question-focused**: Tie all findings back to the original question.
- **Read-only**: Never suggest changes unless explicitly asked.
- **Layered explanation**: Start simple, offer deeper detail on request.

## Related Skills

- `feature` - Implementing new features (code changes)
- `debug` - Debugging and fixing issues
- `scout` - Quick codebase discovery (run before investigation)

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

---

## Investigation & Recommendation Protocol

> Moved from CLAUDE.md. This protocol applies when recommending code changes (removal, refactoring, replacement) — not just feature investigation. It ensures evidence-based architectural decisions and prevents mistakes like the Npgsql IDbContextFactory incident.

**📚 Reference:** See `.claude/skills/shared/evidence-based-reasoning-protocol.md` for comprehensive evidence-based reasoning protocols with verification commands and forbidden phrases. See `.claude/docs/anti-hallucination-patterns.md` for bad vs good response examples.

### Golden Rule: Evidence Before Conclusion

**NEVER recommend code changes (removal, refactoring, replacement) without completing this validation chain:**

```
1. Interface/API identified
   ↓
2. ALL implementations found (Grep: "class.*:.*IInterfaceName")
   ↓
3. ALL registrations traced (Grep: "AddScoped.*IInterfaceName|AddSingleton.*IInterfaceName")
   ↓
4. ALL usage sites verified (Grep: "IInterfaceName" in context of injection/calls)
   ↓
5. Cross-service impact: Check ALL project services (ServiceB, ServiceA, ServiceC, ServiceD)
   ↓
6. Impact assessment: What breaks if removed?
   ↓
7. Confidence declaration: X% confident based on [evidence list]
   ↓
ONLY THEN → Output recommendation
```

**If ANY step incomplete → STOP and gather more evidence OR state "Insufficient evidence to recommend removal"**

### Mistake Patterns & Prevention

| Mistake Pattern                | Prevention Rule                                | Grep Pattern                                 |
| ------------------------------ | ---------------------------------------------- | -------------------------------------------- |
| **"This is unused"**           | Require proof of zero references               | `grep -r "TargetName" --include="*.cs"`      |
| **"Remove this registration"** | Trace interface → impl → ALL call sites        | `grep "IInterfaceName" -A 5 -B 5`            |
| **"Replace X with Y"**         | Impact analysis: what depends on X?            | `grep "using.*X\|: X\|<X>" --include="*.cs"` |
| **"This can be simplified"**   | Verify edge cases preserved                    | Check tests, usage contexts                  |
| **"Dual registration"**        | Compare services: ServiceA vs ServiceB pattern | Cross-service comparison required            |

### Breaking Change Risk Matrix

Before recommending ANY architectural change, assess risk level:

| Risk Level | Criteria                                                      | Required Evidence                                                               |
| ---------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **HIGH**   | Removing registrations, deleting classes, changing interfaces | Full usage trace + impact analysis + cross-service check (all project services) |
| **MEDIUM** | Refactoring methods, changing signatures, updating patterns   | Usage trace + test verification + cross-service check (all project services)    |
| **LOW**    | Renaming variables, formatting, adding comments               | Code review only                                                                |

**For HIGH/MEDIUM risk changes:** Require explicit confidence declaration with evidence summary before proceeding.

### Evidence Hierarchy

1. **Code Evidence (Primary)** — Actual usage in codebase (Grep results, Read file confirmations)
2. **Test Evidence** — Unit/integration tests covering the code path
3. **Documentation** — Comments, docs explaining purpose
4. **Inference** — Logical deduction (LOWEST priority, must be validated)

**Rule:** Recommendations based on inference alone are FORBIDDEN. Always upgrade to code evidence.

### Validation Checklist for Code Removal

Before recommending removal of ANY code element, verify ALL of these:

- [ ] **No static references** — `grep -r "ClassName" --include="*.cs"` returns 0 results
- [ ] **No string literals** — `grep -r "\"ClassName\"|'ClassName'"` returns 0 results
- [ ] **No dynamic invocations** — Check reflection, factory patterns, message bus registrations
- [ ] **No DI container registrations** — Search `services.Add*<ClassName>` patterns
- [ ] **No configuration references** — Check appsettings.json, environment variables
- [ ] **No test dependencies** — Check test projects for usage
- [ ] **Cross-service impact** — Search ALL project's microservices (ServiceB, ServiceA, ServiceC, ServiceD)

**Confidence Declaration:** If checklist not 100% complete, state: "Confidence: <90% — did not verify [missing items]"

### Interface → Implementation → Usage Trace Protocol

For any interface-based recommendation:

```bash
# Step 1: Find ALL implementations
grep -r "class.*:.*ITargetInterface" --include="*.cs"

# Step 2: Find ALL registrations
grep -r "AddScoped\|AddSingleton\|AddTransient.*ITargetInterface" --include="*.cs"

# Step 3: Find ALL injection points
grep -r "ITargetInterface" --include="*.cs" -A 5 -B 5

# Step 4: Find ALL usage in found implementations
# Read each file from Step 3, trace method calls

# Step 5: Cross-service check (MANDATORY - all project services)
for svc in ServiceB ServiceA ServiceC Accounts ServiceD; do
    grep -r "ITargetInterface" "services directory/$svc" --include="*.cs"
done

# ONLY if ALL steps show zero usage → recommend removal
```

### Comparison Pattern (Service vs Service)

When investigating service-specific implementations:

1. **Find working reference service** — Identify service where feature works correctly
2. **Compare implementations** — Side-by-side file comparison
3. **Identify differences** — List what's different between working vs non-working
4. **Verify each difference** — Understand WHY each difference exists
5. **Recommend changes** — Based on proven working pattern, not assumptions

### Confidence Levels (Required for Architectural Recommendations)

Every recommendation for code removal/refactoring MUST include confidence level:

- **95-100%** — Full trace completed, all checklist items verified, all project services checked
- **80-94%** — Main usage paths verified, some edge cases unverified
- **60-79%** — Implementation found, usage partially traced
- **<60%** — Insufficient evidence → DO NOT RECOMMEND, gather more evidence first

**Format:** `Confidence: 85% — Verified main usage in ServiceC, did not check ServiceA/ServiceB`

### When to Activate This Protocol

Trigger the full validation chain for:

- Any recommendation to remove registrations, classes, interfaces
- Architectural changes affecting multiple services
- "This seems unused" observations
- Cross-service dependency analysis
- Breaking change impact assessment
