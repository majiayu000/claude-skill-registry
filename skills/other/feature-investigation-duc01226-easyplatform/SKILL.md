---
name: feature-investigation
version: 1.1.1
description: "[Investigation] Use when the user asks to investigate, explore, understand, explain, or analyze how an existing feature or logic works. Triggers on keywords like "how does", "explain", "what is the logic", "investigate", "understand", "where is", "trace", "walk through", "show me how"."
allowed-tools: Read, Grep, Glob, Task, WebFetch, WebSearch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Investigate and explain how existing features or logic work through READ-ONLY code exploration -- no modifications.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Setup** — Create analysis file, define investigation scope and metadata
2. **Discovery (Phase 1A)** — Glob/Grep to find all relevant files across backend and frontend
3. **Deep Analysis (Phase 1B)** — Read each file, build knowledge graph of relationships
4. **Synthesis (Phase 2)** — Map workflows, integration points, data flows, business logic
5. **Report** — Present findings with evidence chains and code references

**Key Rules:**

- READ-ONLY: never modify code, only explore and explain
- Every claim must have code evidence (no speculation or hallucination)
- Use anti-hallucination protocols: validate assumptions, chain evidence, anchor to original question
- Re-read original question every 10 operations to prevent context drift

> **Skill Variant:** READ-ONLY exploration - no code changes. For implementing features, use `feature-implementation`. For debugging, use `debug`.

# Feature Investigation & Logic Exploration

Investigate and explain how existing features or logic work as an expert full-stack .NET/Angular architect.

**KEY PRINCIPLE**: READ-ONLY investigation. Build understanding and explain how things work.

## Investigation Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

- Do NOT assume code works as named — verify by reading actual implementations
- Every finding must include `file:line` evidence (grep results, read confirmations)
- If you cannot prove a claim with a code trace, mark it as "inferred" with low confidence
- Question assumptions: "Does this actually do what I think?" → read the implementation, not just the signature
- Challenge completeness: "Is this all?" → grep for related usages, consumers, and cross-service references
- Verify relationships: "Does A really call B?" → trace the actual call path with evidence
- No "looks like it works" without proof — state what you verified and how

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY finding.
**95%+** verified fact | **80-94%** with caveats | **60-79%** "partially verified" | **<60% "inferred — needs verification", NOT fact.**

**IMPORTANT**: Always use TaskCreate to plan step-by-step tasks.

---

## Prerequisites

**⚠️ CRITICAL**: Read all protocol sections below before starting investigation.

---

## Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT

Before every major operation:

1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION

Before claiming any relationship:

- "I believe X calls Y because..." -> show actual code
- "This follows pattern Z because..." -> cite specific examples
- "Service A owns B because..." -> grep for actual boundaries

### TOOL_EFFICIENCY_PROTOCOL

- Batch multiple Grep searches into single calls with OR patterns
- Use parallel Read operations for related files
- Combine semantic searches with related keywords

### CONTEXT_ANCHOR_SYSTEM

Every 10 operations:

1. Re-read the original question from the `## Metadata` section
2. Verify the current operation aligns with answering the question
3. Check if we're investigating the right thing
4. Update the `Current Focus` bullet point within the `## Progress` section

### Quick Reference Checklist

Before any major operation:

- [ ] ASSUMPTION_VALIDATION_CHECKPOINT
- [ ] EVIDENCE_CHAIN_VALIDATION
- [ ] TOOL_EFFICIENCY_PROTOCOL

Every 10 operations:

- [ ] CONTEXT_ANCHOR_CHECK
- [ ] Update 'Current Focus' in `## Progress` section

Emergency:

- **Context Drift** -> Re-read `## Metadata` section
- **Assumption Creep** -> Halt, validate with code
- **Evidence Gap** -> Mark as "inferred"

---

## Analysis File Structure

Create at `.ai/workspace/analysis/[feature-name]-investigation.analysis.md`:

```markdown
## Metadata

**Original Prompt:** [Full original question/prompt]

**Task Description:** [Parsed investigation question]

**Investigation Scope:** [What needs to be understood]

**Source Code Structure:**

- Backend: services directory/{ServiceA,ServiceB,ServiceC}/
- Frontend: frontend directory/apps/, frontend directory/libs/
- Platform: framework directory/

## Progress

- **Phase**: 1A
- **Items Processed**: 0
- **Total Items**: 0
- **Current Operation**: "initialization"
- **Current Focus**: "[original task summary]"

## Errors

[Track all errors encountered during analysis]

## Assumption Validations

[Document all assumptions and their validation status]

## Performance Metrics

[Track operation times and efficiency]

## Memory Management

[Track context usage and optimization strategies]

## Processed Files

[Numbered list of processed files with status]

## File List

[Complete numbered list of all discovered files - populated during discovery]

## Knowledge Graph

[Detailed analysis of each file - populated during Phase 1B]

## Workflow Analysis

[End-to-end workflow documentation]

## Integration Points

[Cross-service and cross-component integration analysis]

## Business Logic Mapping

[Complete business logic workflows and rules]

## Data Flow Analysis

[How data flows through the system]

## Platform Pattern Usage

[Documentation of platform patterns used]
```

---

## File Discovery Search Patterns

```bash
# Domain Entities (HIGH PRIORITY)
grep: "class.*{EntityName}.*:.*RootEntity|RootAuditedEntity"

# Commands & Queries (HIGH PRIORITY)
grep: ".*Command.*{EntityName}|{EntityName}.*Command"
grep: ".*Query.*{EntityName}|{EntityName}.*Query"

# Event Handlers (HIGH PRIORITY)
grep: ".*EventHandler.*{EntityName}|{EntityName}.*EventHandler"

# Controllers (HIGH PRIORITY)
grep: ".*Controller.*{EntityName}|{EntityName}.*Controller"

# Background Jobs (MEDIUM PRIORITY)
grep: ".*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob"

# Message Bus Consumers (MEDIUM PRIORITY)
grep: ".*Consumer.*{EntityName}|{EntityName}.*Consumer"
grep: "PlatformApplicationMessageBusConsumer.*{EntityName}"

# Services & Helpers (LOW PRIORITY)
grep: ".*Service.*{EntityName}|{EntityName}.*Service"
grep: ".*Helper.*{EntityName}|{EntityName}.*Helper"

# Frontend Components & Stores (HIGH PRIORITY)
grep: "{feature-name}" in **/*.{ts,html}
grep: ".*Store.*{FeatureName}|{FeatureName}.*Store"
grep: ".*Component.*{FeatureName}|{FeatureName}.*Component"
```

### File List Organization

```markdown
## File List

### High Priority - Core Logic (MUST ANALYZE FIRST)

1. [Domain Entity path]
2. [Command/Query Handler path]
3. [Event Handler path]
4. [Controller path]
5. [Frontend Component path]
   ...

### Medium Priority - Supporting Infrastructure

10. [Background Job path]
11. [Consumer path]
12. [API Service path]
    ...

### Low Priority - Configuration/Utilities

20. [Helper path]
21. [Utility path]
    ...

**Total Files**: [count]
```

---

## Knowledge Graph Entry Template

For each file, document:

````markdown
### {ItemNumber}. {FilePath}

**File Analysis:**

- **filePath**: Full path to the file
- **type**: Entity | Command | Query | EventHandler | Controller | BackgroundJob | Consumer | Component | Store | Service | Helper
- **architecturalPattern**: CQRS | Repository | Event-Driven | Component-Store | etc.
- **content**: Summary of purpose and logic
- **symbols**: Important classes, interfaces, methods
- **dependencies**: All imported modules or `using` statements
- **businessContext**: What business problem, rules, contribution to feature
- **referenceFiles**: Other files that use this file's symbols
- **relevanceScore**: 1-10 for current investigation
- **evidenceLevel**: "verified" or "inferred"
- **uncertainties**: Aspects you are unsure about
- **platformAbstractions**: Platform base classes used
- **serviceContext**: Which microservice (ServiceB, ServiceA, ServiceC)
- **dependencyInjection**: DI registrations
- **genericTypeParameters**: Generic type relationships

**Message Bus Analysis (FOR CONSUMERS ONLY):**

- **messageBusMessage**: Message type consumed
- **messageBusProducers**: Files that publish this message (MUST grep across ALL services)
- **crossServiceIntegration**: Cross-service data flow description

**Targeted Aspect Analysis:**

**For Frontend Components:**

- `componentHierarchy`, `routeConfig`, `routeGuards`, `stateManagementStores`
- `dataBindingPatterns`, `validationStrategies`, `apiIntegration`, `userInteractionFlow`

**For Backend Components:**

- `authorizationPolicies`, `commands`, `queries`, `domainEntities`
- `repositoryPatterns`, `businessRuleImplementations`, `eventHandlers`, `backgroundJobs`

**For Consumer Components:**

- `messageBusMessage`, `messageBusProducers`, `crossServiceIntegration`
- `handleLogicWorkflow`, `dependencyWaiting`

**Code Examples:**

```csharp
// Include relevant code snippets that demonstrate key logic
```
````

**Key Insights:**

[Important observations about this file's role in the overall feature]

````

---

## Overall Analysis Template

```markdown
## Overall Analysis

### 1. Complete End-to-End Workflows Discovered

**Workflow: {Feature Name} - Main Flow**

````

[User Action] -> [Frontend Component] -> [API Service] -> [Controller]
|
[Command/Query Handler]
|
[Domain Entity] -> [Repository]
|
[Event Handler] -> [Side Effects]

```

**Detailed Flow:**

1. **Frontend Entry Point**: `Component.ts:line` - User interaction, validation, API call
2. **API Layer**: `Controller.cs:line` - Endpoint, authorization, command dispatch
3. **Application Layer**: `CommandHandler.cs:line` - Validation, business logic, repository ops
4. **Domain Layer**: `Entity.cs:line` - Business rules, state changes, domain events
5. **Event Handling**: `EventHandler.cs:line` - Events handled, side effects, integrations
6. **Cross-Service**: `Consumer.cs:line` - Message consumed, producer service, sync logic

### 2. Key Architectural Patterns and Relationships

- **CQRS**: Commands, queries, separation of concerns
- **Event-Driven**: Domain events, handlers, message bus
- **Repository**: Repositories used, query builders, extensions
- **Frontend**: Component hierarchy, state management, forms

### 3. Business Logic Workflows

Frontend-to-backend flow tree and cross-service integration flow.

### 4. Integration Points and Dependencies

API endpoints, message bus integration, database dependencies, external services.

### 5. Business Rules Discovered

Validation rules, business constraints, authorization rules.

### 6. Platform Pattern Usage

Backend: CQRS, repository, event handlers, message bus, background jobs, validation
Frontend: Component hierarchy, stores, forms, API services, reactive patterns

### 7. Key Insights and Observations

Critical findings, recommendations, uncertainties requiring clarification.
```

---

## Presentation Template

```markdown
## Answer

[Direct answer to the question in 1-2 paragraphs]

## How It Works

### 1. [First Step]

[Explanation with code reference at `file:line`]

### 2. [Second Step]

[Explanation with code reference at `file:line`]

## Key Files

| File                  | Purpose   |
| --------------------- | --------- |
| `path/to/file.cs:123` | [Purpose] |

## Data Flow
```

[Text diagram showing the flow]

```

## Want to Know More?

I can explain further:

- [Topic 1]
- [Topic 2]
- [Topic 3]
```

---

## Common Investigation Scenarios

### "How does feature X work?"

1. Find entry points (API, UI, job)
2. Trace through command/query handlers
3. Document entity changes
4. Map side effects (events, notifications)

### "Where is the logic for Y?"

1. Search for keywords in commands, queries, entities
2. Check event handlers for side effect logic
3. Look in helper/service classes
4. Check frontend stores and components

### "What happens when Z occurs?"

1. Identify the trigger (user action, event, schedule)
2. Trace the handler chain
3. Document all side effects
4. Map error handling

### "Why does A behave like B?"

1. Find the relevant code path
2. Identify decision points
3. Check configuration/feature flags
4. Document business rules

---

## Platform-Specific Investigation Patterns

### Backend Patterns to Look For

- `PlatformCqrsCommand` / `PlatformCqrsQuery` - CQRS entry points
- `PlatformCqrsEntityEventApplicationHandler` - Side effects
- `PlatformApplicationMessageBusConsumer` - Cross-service consumers
- `service-specific repository` / `service-specific repository` - Data access
- `PlatformValidationResult` - Validation logic
- `[PlatformAuthorize]` - Authorization

### Frontend Patterns to Look For

- `project store component base (search for: store component base class)` - State management components
- `project store base (search for: store base class)` - Store implementations
- `effectSimple` / `tapResponse` - Effect handling
- `observerLoadingErrorState` - Loading/error states
- API services extending `PlatformApiService`

---

## Investigation Flow

### Phase 1A: Initialize & Discover

1. **Create analysis file** at `.ai/workspace/analysis/[feature-name]-investigation.analysis.md`
    - **Use the Analysis File Structure template** above
2. **Search for all related files** using grep patterns organized by priority
    - **Use the File Discovery Search Patterns** above
3. **Save all discovered paths** as numbered list under `## File List`, organized by priority
4. Update `Total Items` count in `## Progress`

### Phase 1B: Knowledge Graph Construction

1. Count total files, split into batches of 10 (priority order)
2. Insert batch analysis tasks into todo list
3. For each file, document in `## Knowledge Graph`
    - **Use the Knowledge Graph Entry Template** above
4. **Every 10 files**: Update progress, run CONTEXT_ANCHOR_CHECK

### Phase 1C: Overall Analysis

After ALL files analyzed, write comprehensive analysis:

- End-to-end workflows, architectural patterns, business logic
- Integration points, business rules, platform patterns, key insights
- **Use the Overall Analysis Template** above

### Phase 2: Presentation

Present findings in clear format with: Answer, How It Works (with code refs), Key Files table, Data Flow diagram, "Want to Know More?" topics.

- **Use the Presentation Template** above

---

## Anti-Hallucination Protocols (Investigation-Specific)

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` and `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

---

## Investigation Guidelines

- **Evidence-based**: Every claim must have code evidence
- **Service boundary awareness**: Understand which service owns what
- **Platform pattern recognition**: Identify platform framework patterns used
- **Cross-service tracing**: Follow message bus flows across services
- **Read-only exploration**: Never suggest changes unless asked
- **Question-focused**: Always tie findings back to the original question
- **Layered explanation**: Start simple, offer deeper detail if requested

---

## See Also

- `feature-implementation` - For implementing new features (code changes)
- `debug` - For debugging and fixing issues
- `planning` - For creating implementation plans

## References

**Note:** All content from `references/investigation-protocols.md` has been merged into this skill file above. The reference file is kept for historical purposes.

| File                                    | Contents                                         |
| --------------------------------------- | ------------------------------------------------ |
| `references/investigation-protocols.md` | (Archived - content merged into this skill file) |

---

## Task Planning Notes

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
