---
name: feature
version: 2.0.1
description: "[Implementation] Use when the user asks to implement a new feature, enhancement, add functionality, build something new, or create new capabilities. Triggers on keywords like "implement", "add feature", "build", "create new", "develop", "enhancement"."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` and `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

## Quick Summary

**Goal:** Implement new features or enhancements with comprehensive knowledge graph analysis and external memory management.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Phase 1A: Discovery** — Initialize analysis file, semantic/grep search, build file list
2. **Phase 1B: Knowledge Graph** — Analyze files in batches of 10, document business context, dependencies
3. **Phase 1C: Overall Analysis** — Comprehensive end-to-end workflow summary
4. **Phase 2: Plan Generation** — Detailed implementation plan following project patterns
5. **Phase 3: Approval Gate** — Present plan, await user confirmation
6. **Phase 4: Execution** — Implement with safeguards, update external memory

**Key Rules:**

- **External Memory**: All analysis in `.ai/workspace/analysis/{task}.analysis.md`
- **Evidence-Based**: grep/search to verify assumptions, never assume service ownership
- **High Priority**: Domain Entities, Commands, Queries, EventHandlers, Controllers, BackgroundJobs, Consumers, Components MUST be analyzed
- **Approval Required**: STOP at Phase 3, do NOT proceed without user confirmation

> **Skill Variant:** Use this skill for **interactive feature development** where the user is actively engaged and can provide feedback. For autonomous feature implementation, use `tasks-feature-implementation`. For investigating existing features without changes, use `feature-investigation`.

# Implementing a New Feature or Enhancement

You are to operate as an expert full-stack dotnet angular principal developer, software architecture to implement the new requirements in `[task-description-or-task-info-file-path]`.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation. Todo list must cover all phases, from start to end, include child tasks in each phases too, everything is flatted out into a long detailed todo list.

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN KNOWLEDGE MODEL CONSTRUCTION

Your sole objective is to build a structured knowledge model in a Markdown analysis file at `.ai/workspace/analysis/[some-sort-semantic-name-of-this-task].analysis.md` with systematic external memory management.

### PHASE 1A: INITIALIZATION AND DISCOVERY

First, **initialize** the analysis file with a `## Metadata` heading and under it is the full original prompt in a markdown box, like this: `markdown [content of metadata in here]` (MUST 5 chars for start and end of markdown box), then continue add the task description and full details of the `Source Code Structure` from `.ai/docs/prompt-context.md` into this `## Metadata` section, with all content in `## Metadata` section must be in a markdown box, like this: `markdown [content of metadata in here]` (MUST 6 chars for start and end of markdown box).

You **MANDATORY IMPORTANT MUST** also create the following top-level headings:

- `## Progress`
- `## Errors`
- `## Assumption Validations`
- `## Performance Metrics`
- `## Memory Management`
- `## Processed Files`
- `## File List`
- `## Knowledge Graph`

Populate the `## Progress` section with:

- **Phase**: 1
- **Items Processed**: 0
- **Total Items**: 0
- **Current Operation**: "initialization"
- **Current Focus**: "[original task summary]"

Next, do semantic search and grep search all keywords of the task to find all related files, prioritizing the discovery of core logic files like **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers and front-end Components .ts**.

**CRITICAL:** Save ALL file paths immediately as a numbered list under a `## File List` heading.

After semantic search, perform additional targeted searches to ensure no critical infrastructure is missed:

- `grep search` with patterns: `.*EventHandler.*{EntityName}|{EntityName}.*EventHandler`
- `grep search` with patterns: `.*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob`
- `grep search` with patterns: `.*Consumer.*{EntityName}|{EntityName}.*Consumer`
- `grep search` with patterns: `.*Service.*{EntityName}|{EntityName}.*Service`
- `grep search` with patterns: `.*Helper.*{EntityName}|{EntityName}.*Helper`
- All files (include pattern: `**/*.{cs,ts,html}`)

High Priority files MUST be analyzed: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers and front-end Components .ts**.

Update the `Total Items` count in the `## Progress` section.

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT MUST DO WITH TODO LIST**

Count total files in file list, split it into many batches of 10 files in priority order, each group insert in the current todo list new task for Analyze each batch of files group for all of files in file list.

**CRITICAL:** You must analyze all files in the file list identified as belonging to the highest IMPORTANT priority categories: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers and front-end Components .ts**.

For each file in the `## File List` (following the prioritized order if applicable), read and analyze it, add result into `## Knowledge Graph` section. The heading of each analyzed file must have the item order number in heading. Each file analyzing result detail the following information:

**Core Fields:**

- **`filePath`**: The full path to the file
- **`type`**: The component's classification
- **`architecturalPattern`**: The main design pattern used
- **`content`**: A summary of purpose and logic
- **`symbols`**: Important classes, interfaces, methods
- **`dependencies`**: All imported modules or `using` statements
- **`businessContext`**: Comprehensive detail all business logic, how it contributes to the requirements
- **`referenceFiles`**: Other files that use this file's symbols
- **`relevanceScore`**: A numerical score (1-10)
- **`evidenceLevel`**: "verified" or "inferred"
- **`uncertainties`**: Any aspects you are unsure about
- **`platformAbstractions`**: Any platform base classes used
- **`serviceContext`**: Which microservice this file belongs to
- **`dependencyInjection`**: Any DI registrations
- **`genericTypeParameters`**: Generic type relationships

**For Consumer Files (CRITICAL):**

- **`messageBusAnalysis`**: When analyzing any Consumer file (files ending with `Consumer.cs` that extend `PlatformApplicationMessageBusConsumer<T>`), identify the `*BusMessage` type used. Then perform a grep search across ALL services to find files that **send/publish** this message type. List all producer files and their service locations in the `messageBusProducers` field. This analysis is crucial for understanding cross-service integration.

**Targeted Aspect Analysis:**
Populate `specificAspects:` key with deeper analysis:

- **For Front-End items:** `componentHierarchy`, `routeConfig`, `routeGuards`, `stateManagementStores`, `dataBindingPatterns`, `validationStrategies`
- **For Back-End items:** `authorizationPolicies`, `commands`, `queries`, `domainEntities`, `repositoryPatterns`, `businessRuleImplementations`
- **For Consumer items:** `messageBusMessage`, `messageBusProducers`, `crossServiceIntegration`, `handleLogicWorkflow`

**MANDATORY PROGRESS TRACKING**: After processing every 10 files, you **MANDATORY IMPORTANT MUST** update `Items Processed` in `## Progress`, run a `CONTEXT_ANCHOR_CHECK`, and explicitly state your progress. After each file, add its path to the `## Processed Files` list.

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive `overallAnalysis:` summary showing:

- Complete end-to-end workflows discovered
- Key architectural patterns and relationships
- All business logic work flow: From front-end to back-end. (Example: Front-end Component => Controller Api Service => Command/Query => EventHandler => Others (Send email, producer bus message); From background job => event handler => others)
- Integration points and dependencies

---

## PHASE 2: PLAN GENERATION

You MUST ensure all files are analyzed. Then read the ENTIRE Markdown analysis notes file. Then Generate a detailed implementation plan under a `## Plan` heading. Your plan **MANDATORY IMPORTANT MUST** follow coding convention and patterns in `.ai/docs/prompt-context.md`, must ultrathink and think step-by-step todo list to make code changes, for each step must read `.ai/docs/prompt-context.md` to follow code convention and patterns.

### PHASE 2.1: VERIFY AND REFACTOR

First, verify and ensure your implementation plan that code patterns, solution must follow code patterns and example in these files:

- `.github/copilot-instructions.md`
- `.github/instructions/frontend-angular.instructions.md`
- `.github/instructions/backend-dotnet.instructions.md`

Then verify and ensure your implementation plan satisfy clean code rules in `.github/instructions/clean-code.instructions.md`

---

## PHASE 3: APPROVAL GATE

You must present the plan for my explicit approval. **DO NOT** proceed without it.

**Format for Approval Request:**

```markdown
## Implementation Plan Complete - Approval Required

### Summary

[Brief description of what will be implemented]

### Files to Create

1. `path/to/file.cs` - [purpose]
2. `path/to/file.ts` - [purpose]

### Files to Modify

1. `path/to/existing.cs:line` - [change description]
2. `path/to/existing.ts:line` - [change description]

### Implementation Order

1. [Step 1]
2. [Step 2]
3. [Step N]

### Risks & Considerations

- [Risk 1]
- [Risk 2]

**Awaiting approval to proceed with implementation.**
```

---

## PHASE 4: EXECUTION

Once approved, execute the plan. Before creating or modifying **ANY** file, you **MANDATORY IMPORTANT MUST** first load its relevant entry from your `## Knowledge Graph`. Use all **EXECUTION_SAFEGUARDS**. If any step fails, **HALT**, report the failure, and return to the APPROVAL GATE.

**EXECUTION_SAFEGUARDS:**

- Verify file exists before modification
- Read current content before editing
- Check for conflicts with existing code
- Validate changes against platform patterns

---

## SUCCESS VALIDATION

Before completion, verify the implementation against all requirements. Document this under a `## Success Validation` heading and summarize changes in `changelog.md`.

---

## Coding Guidelines

- **Evidence-based approach:** Use `grep` and semantic search to verify assumptions
- **Service boundary discovery:** Find endpoints before assuming responsibilities
- **Never assume service ownership:** Verify patterns with code evidence
- **Platform-first approach:** Use established templates
- **Cross-service sync:** Use an event bus, not direct database access
- **CQRS adherence:** Follow established Command/Query patterns
- **Clean architecture respect:** Maintain proper layer dependencies

---

## Architecture Reference

### Backend Layers

```
Presentation:   Controllers, API endpoints
Application:    Commands, Queries, EventHandlers, DTOs
Domain:         Entities, ValueObjects, Expressions
Infrastructure: Repositories, External services, Messaging
```

### Key CQRS Flow

```
Controller → Command/Query → Handler → Repository → Entity
                                  ↓
                            EventHandler → Side Effects (notifications, external APIs)
```

### Message Bus Flow

```
Service A: EntityEventProducer → message broker → Service B: Consumer
```

### Frontend Flow

```
Component → Store.effect() → ApiService → Backend
     ↑           ↓
   Template ← Store.state
```

### Platform Patterns

```csharp
// Command/Query handlers
PlatformCqrsCommandApplicationHandler<TCommand, TResult>
PlatformCqrsQueryApplicationHandler<TQuery, TResult>

// Entity event handlers (for side effects)
PlatformCqrsEntityEventApplicationHandler<TEntity>

// Message bus consumers
PlatformApplicationMessageBusConsumer<TMessage>

// Repositories
service-specific repository<TEntity>
service-specific repository<TEntity>
```

### Frontend Patterns

```typescript
// Component hierarchy
project base component (search for: base component class)            // Simple display
project store component base (search for: store component base class)     // State management
project form component base (search for: form component base class)        // Forms with validation

// Store pattern
project store base (search for: store base class)<TState>
effectSimple(() => api.call().pipe(tapResponse(...)))
```

---

## See Also

- `.ai/docs/AI-DEBUGGING-PROTOCOL.md` - Debugging protocol
- `.ai/docs/prompt-context.md` - Platform patterns and context
- `CLAUDE.md` - Codebase instructions
- `feature-investigation` skill - For exploring existing features (READ-ONLY)
- `tasks-feature-implementation` skill - Autonomous variant

## Related

- `planning`
- `code-review`
- `test-spec`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
