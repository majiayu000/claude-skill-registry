---
name: feature-investigation
description: Use when the user asks to investigate, explore, understand, explain, or analyze how an existing feature or logic works. Triggers on keywords like "how does", "explain", "what is the logic", "investigate", "understand", "where is", "trace", "walk through", "show me how".
allowed-tools: Read, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
infer: true
---

> **Skill Variant:** Use this skill for **investigating and understanding** existing features or logic. This is a READ-ONLY exploration skill - no code changes. For implementing new features, use `feature-implementation`. For debugging, use `bug-diagnosis`.

# Feature Investigation & Logic Exploration

You are to operate as an expert full-stack dotnet angular principal developer and software architect to investigate and explain how an existing feature or logic works in `[feature-description-or-question]`.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation. Todo list must cover all phases, from start to end, include child tasks in each phases too, everything is flatted out into a long detailed todo list.

**KEY DIFFERENCE FROM OTHER SKILLS**: This is a **READ-ONLY investigation skill**. You are NOT implementing or fixing anything - you are building understanding and explaining how things work.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT

Before every major operation:

1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION

Before claiming any relationship:

- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

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

---

## Quick Reference Checklist

Before any major operation:

- [ ] ASSUMPTION_VALIDATION_CHECKPOINT
- [ ] EVIDENCE_CHAIN_VALIDATION
- [ ] TOOL_EFFICIENCY_PROTOCOL

Every 10 operations:

- [ ] CONTEXT_ANCHOR_CHECK
- [ ] Update 'Current Focus' in `## Progress` section

Emergency:

- **Context Drift** → Re-read `## Metadata` section
- **Assumption Creep** → Halt, validate with code
- **Evidence Gap** → Mark as "inferred"

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN FEATURE INVESTIGATION

Your sole objective is to build a structured knowledge model in a Markdown analysis file at `.ai/workspace/analysis/[feature-name]-investigation.md` with systematic external memory management.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with:
    - `## Metadata` heading with original question in markdown box
    - `## Investigation Question` - clearly state what we're trying to understand
    - Create headings: `## Progress`, `## Assumptions`, `## File List`, `## Knowledge Graph`, `## Data Flow`, `## Findings`

2. **Populate `## Progress`** with:
    - **Phase**: 1
    - **Items Processed**: 0
    - **Total Items**: 0
    - **Current Operation**: "initialization"
    - **Current Focus**: "[original investigation question]"

3. **Discovery searches** to find all related files:
    - Semantic search and grep search all keywords from the question
    - Prioritize: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, Components**
    - Additional targeted searches:
        - `.*EventHandler.*{FeatureName}|{FeatureName}.*EventHandler`
        - `.*BackgroundJob.*{FeatureName}|{FeatureName}.*BackgroundJob`
        - `.*Consumer.*{FeatureName}|{FeatureName}.*Consumer`
        - `.*Service.*{FeatureName}|{FeatureName}.*Service`
        - `.*Component.*{FeatureName}|{FeatureName}.*Component`
    - Save ALL file paths to `## File List`

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT: MUST DO WITH TODO LIST**

1. Count total files, split into batches of 10 files in priority order
2. Insert batch analysis tasks into todo list

For each file, document in `## Knowledge Graph`:

- `filePath`: Full path
- `type`: Component classification
- `architecturalPattern`: Design pattern used
- `content`: Purpose and logic summary
- `symbols`: Classes, interfaces, methods
- `dependencies`: Imports/using statements
- `businessContext`: Business logic contribution
- `referenceFiles`: Files using this file's symbols
- `relevanceScore`: 1-10 (to the investigation question)
- `evidenceLevel`: "verified" or "inferred"
- `platformAbstractions`: Platform base classes
- `serviceContext`: Microservice ownership

**Investigation-Specific Fields:**

- `entryPoints`: How this code is triggered/called
- `outputPoints`: What this code produces/returns
- `dataTransformations`: How data is modified
- `externalDependencies`: External services, APIs, databases accessed
- `configurationDependencies`: Config values, feature flags, settings
- `conditionalLogic`: Key decision points and branches
- `errorScenarios`: What can go wrong, error handling

**For Consumers/Message Bus:**

- `messageBusMessage`: Message type consumed
- `messageBusProducers`: Who sends this message (grep across all services)
- `crossServiceIntegration`: Cross-service data flow

**MANDATORY**: After every 10 files, update `Items Processed` and run `CONTEXT_ANCHOR_CHECK`.

### PHASE 1C: DATA FLOW MAPPING

Under `## Data Flow`, document:

1. **Entry Points**: Where the feature begins (API endpoint, UI action, scheduled job, message)
2. **Processing Pipeline**: Step-by-step flow through the code
3. **Data Transformations**: How data changes at each step
4. **Persistence Points**: Where data is saved/loaded
5. **Exit Points**: Final outputs (responses, events, side effects)
6. **Cross-Service Flows**: If data crosses service boundaries

Create a text-based flow diagram:

```
[Entry] → [Step 1] → [Step 2] → [Step 3] → [Exit]
              ↓           ↓
         [Side Effect] [Database]
```

---

## PHASE 2: COMPREHENSIVE ANALYSIS

### PHASE 2A: WORKFLOW ANALYSIS

Document under `## Workflow Analysis`:

1. **Happy Path**: Normal successful execution flow
2. **Error Paths**: How errors are handled at each stage
3. **Edge Cases**: Special conditions and their handling
4. **Authorization**: Permission checks and security gates
5. **Validation**: Input validation at each layer

### PHASE 2B: ARCHITECTURAL ANALYSIS

Document under `## Architectural Analysis`:

1. **Layers Involved**: Domain, Application, Infrastructure, Presentation
2. **Patterns Used**: CQRS, Repository, Event Sourcing, etc.
3. **Service Boundaries**: Which microservices are involved
4. **Integration Points**: External systems, message bus, APIs
5. **State Management**: Frontend state patterns (stores, signals)

### PHASE 2C: BUSINESS LOGIC EXTRACTION

Document under `## Business Logic`:

1. **Core Business Rules**: What rules govern this feature
2. **Validation Rules**: Input/data validation
3. **Calculations**: Any computations performed
4. **State Transitions**: Entity state changes
5. **Side Effects**: Notifications, events, external calls

---

## PHASE 3: FINDINGS SYNTHESIS

### PHASE 3A: EXECUTIVE SUMMARY

Write a clear, concise answer to the original question under `## Executive Summary`:

- **One-paragraph answer** to the user's question
- **Key files** involved (top 5-10 most important)
- **Key patterns** used

### PHASE 3B: DETAILED EXPLANATION

Under `## Detailed Explanation`:

1. **Step-by-step walkthrough** of how the feature works
2. **Code references** with file:line for each step
3. **Why it works this way** - architectural decisions

### PHASE 3C: VISUAL REPRESENTATION

Under `## Diagrams`:

1. **Sequence Diagram** (text-based) showing component interactions
2. **Data Flow Diagram** showing data transformations
3. **Component Diagram** showing file relationships

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Component  │────>│   Command   │────>│   Handler   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               v
                                        ┌─────────────┐
                                        │ Repository  │
                                        └─────────────┘
```

### PHASE 3D: RELATED DISCOVERIES

Under `## Related Discoveries`:

- **Connected Features**: Other features that interact with this one
- **Shared Components**: Reusable code discovered
- **Potential Issues**: Any concerns or technical debt noticed
- **Documentation Gaps**: Missing or outdated documentation

---

## PHASE 4: PRESENTATION

Present your findings to the user in a clear, organized format:

1. **Start with the answer** - directly address their question
2. **Provide evidence** - show the code that supports your answer
3. **Explain the flow** - walk through the logic step by step
4. **Offer deeper dives** - mention areas you can explain further

### Response Format

```markdown
## Answer

[Direct answer to the question in 1-2 paragraphs]

## How It Works

### 1. [First Step]

[Explanation with code reference at `file:line`]

### 2. [Second Step]

[Explanation with code reference at `file:line`]

...

## Key Files

| File                  | Purpose   |
| --------------------- | --------- |
| `path/to/file.cs:123` | [Purpose] |

## Data Flow

[Text diagram showing the flow]

## Want to Know More?

I can explain further:

- [Topic 1]
- [Topic 2]
- [Topic 3]
```

---

## Investigation Guidelines

- **Evidence-based investigation**: Every claim must have code evidence
- **Service boundary awareness**: Understand which service owns what
- **Platform pattern recognition**: Identify Easy.Platform patterns used
- **Cross-service tracing**: Follow message bus flows across services
- **Read-only exploration**: Never suggest changes unless asked
- **Question-focused**: Always tie findings back to the original question
- **Layered explanation**: Start simple, offer deeper detail if requested

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
- `IPlatformQueryableRootRepository` / `IPlatformQueryableRootRepository` - Data access
- `PlatformValidationResult` - Validation logic
- `[PlatformAuthorize]` - Authorization

### Frontend Patterns to Look For

- `AppBaseVmStoreComponent` - State management components
- `PlatformVmStore` - Store implementations
- `effectSimple` / `tapResponse` - Effect handling
- `observerLoadingErrorState` - Loading/error states
- API services extending `PlatformApiService`

---

## See Also

- `feature-implementation` skill - For implementing new features (code changes)
- `bug-diagnosis` skill - For debugging and fixing issues
- `tasks-feature-implementation` skill - Autonomous feature implementation variant
- `.ai/prompts/context.md` - Platform patterns and context
- `CLAUDE.md` - Codebase instructions
