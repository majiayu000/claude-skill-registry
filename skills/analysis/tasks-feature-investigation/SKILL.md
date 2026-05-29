---
name: tasks-feature-investigation
description: Use when investigating existing features, understanding logic flow, or exploring how code works.
---

# Investigating a Feature or Understanding Logic

You are to operate as an expert full-stack dotnet angular principle developer and software architect to investigate and explain how existing features work, trace logic flows, and provide comprehensive understanding of code behavior.

**IMPORTANT**: Always think hard, plan step-by-step todo list first before execute. Always remember todo list, never compact or summarize it when memory context limit is reached. Always preserve and carry your todo list through every operation. Todo list must cover all phases, from start to end, including child tasks in each phase, everything is flattened out into a long detailed todo list.

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

1. Re-read the original task description from the `## Metadata` section
2. Verify the current operation aligns with original goals
3. Check if we're solving the right problem
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

1. **Initialize** the analysis file with a `## Metadata` heading. Under it, add the full original prompt/question in a markdown box using 5 backticks:

   ```markdown
   [Full original prompt/question here]
   ```

2. **Continue adding** to the `## Metadata` section: the investigation question and full details of the `Source Code Structure` from `.ai/prompts/context.md`. Use 6 backticks for this nested markdown:

   ```markdown
   ## Investigation Question

   [Investigation question here]

   ## Source Code Structure

   [Full details from .ai/prompts/context.md]
   ```

3. **Create all required headings**:
   - `## Progress`
   - `## Investigation Questions`
   - `## Assumption Validations`
   - `## Processed Files`
   - `## File List`
   - `## Knowledge Graph`
   - `## Logic Flow Map`
   - `## Entry Points`
   - `## Data Flow`

4. **Populate `## Progress`** with:
   - **Phase**: 1
   - **Items Processed**: 0
   - **Total Items**: 0
   - **Current Operation**: "initialization"
   - **Current Focus**: "[original investigation question]"

5. **Populate `## Investigation Questions`** with:
   - Primary question being investigated
   - Sub-questions to answer
   - Expected outcomes

6. **Discovery searches** - Semantic search and grep search all keywords to find:
   - **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, front-end Components .ts**

7. **Additional targeted searches**:
   - `grep search` patterns: `.*EventHandler.*{FeatureName}|{FeatureName}.*EventHandler`
   - `grep search` patterns: `.*BackgroundJob.*{FeatureName}|{FeatureName}.*BackgroundJob`
   - `grep search` patterns: `.*Consumer.*{FeatureName}|{FeatureName}.*Consumer`
   - `grep search` patterns: `.*Service.*{FeatureName}|{FeatureName}.*Service`
   - `grep search` patterns: `.*Helper.*{FeatureName}|{FeatureName}.*Helper`
   - Include pattern: `**/*.{cs,ts,html}`

**CRITICAL:** Save ALL file paths immediately as a numbered list under `## File List`. Update the `Total Items` count in `## Progress`.

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT: MUST DO WITH TODO LIST**

Count total files in file list, split it into many batches of 10 files in priority order. For each batch, insert a new task in the current todo list for analyzing that batch.

**File Analysis Order (by priority)**:

1. Domain Entities
2. Commands
3. Queries
4. Event Handlers
5. Controllers
6. Background Jobs
7. Consumers
8. Frontend Components .ts

**CRITICAL:** You must analyze ALL files in the file list identified as belonging to the highest priority categories.

For each file, add results into `## Knowledge Graph` section. **The heading of each analyzed file must have the item order number in the heading.**

**Core fields** for each file:

- `filePath`: Full path to the file
- `type`: Component classification
- `architecturalPattern`: Design pattern used
- `content`: Purpose and logic summary
- `symbols`: Classes, interfaces, methods
- `dependencies`: Imports/using statements
- `businessContext`: Comprehensive detail of all business logic
- `referenceFiles`: Files using this file's symbols
- `relevanceScore`: 1-10
- `evidenceLevel`: "verified" or "inferred"
- `uncertainties`: Unclear aspects
- `platformAbstractions`: Platform base classes used
- `serviceContext`: Microservice ownership
- `dependencyInjection`: DI registrations
- `genericTypeParameters`: Generic type relationships

**Message Bus Analysis** (CRITICAL FOR CONSUMERS):

- `messageBusAnalysis`: When analyzing Consumer files (`*Consumer.cs` extending `PlatformApplicationMessageBusConsumer<T>`):
  1. Identify the `*BusMessage` type used
  2. Grep search ALL services to find files that send/publish this message
  3. List all producer files and their service locations in `messageBusProducers`

**Targeted Aspect Analysis** (`targetedAspectAnalysis`):

For **Front-End items**:

- `componentHierarchy`, `routeConfig`, `routeGuards`
- `stateManagementStores`, `dataBindingPatterns`, `validationStrategies`

For **Back-End items**:

- `authorizationPolicies`, `commands`, `queries`
- `domainEntities`, `repositoryPatterns`, `businessRuleImplementations`

For **Consumer items**:

- `messageBusMessage`, `messageBusProducers`
- `crossServiceIntegration`, `handleLogicWorkflow`

**MANDATORY PROGRESS TRACKING**: After processing every 10 files, you **MUST** update `Items Processed` in `## Progress`, run a `CONTEXT_ANCHOR_CHECK`, and explicitly state your progress. After each file, add its path to the `## Processed Files` list.

### PHASE 1C: LOGIC FLOW MAPPING

Document under `## Logic Flow Map`:

1. **Entry Points**: Where does the feature start? (API endpoint, UI action, scheduled job, message consumer)

2. **Request Flow**: Trace the complete path:
   - Frontend Component → API Service → Controller
   - Controller → CQRS Command/Query Handler
   - Handler → Domain Entity operations
   - Handler → Repository operations
   - Handler → Side effects (events, notifications)

3. **Data Flow**: Track how data moves:
   - Input validation and transformation
   - Business rule application
   - Persistence operations
   - Response transformation

4. **Event Flow**: Map triggered events:
   - Domain events raised
   - Entity events produced
   - Message bus publications
   - Cross-service communications

5. **Error Handling Flow**: Document error paths:
   - Validation failures
   - Business rule violations
   - Technical exceptions
   - Error propagation

### PHASE 1D: OVERALL ANALYSIS

Write comprehensive `overallAnalysis:` summary showing:

- Complete end-to-end workflows discovered
- Key architectural patterns and relationships
- All business logic workflows: From front-end to back-end
  - Example: Front-end Component => Controller Api Service => Command/Query => EventHandler => Others (Send email, producer bus message)
  - Example: Background Job => Event Handler => Others
- Integration points and dependencies
- Cross-service dependencies identified
- Authorization and security checkpoints

---

## PHASE 2: INVESTIGATION SYNTHESIS

**Prerequisites**: Ensure ALL files are analyzed. Read the ENTIRE analysis notes file.

Generate comprehensive investigation report under `## Investigation Report` heading:

### 2.1: Feature Overview

- **Purpose**: What business problem does this feature solve?
- **Scope**: What are the boundaries of this feature?
- **Key Components**: List the main files/classes involved

### 2.2: Architecture Summary

- **Pattern**: What architectural patterns are used?
- **Layers**: How does it fit in Clean Architecture?
- **Dependencies**: What external/internal dependencies exist?

### 2.3: Logic Flow Diagram (Text-based)

```
[Entry Point] → [Validation] → [Business Logic] → [Persistence] → [Side Effects] → [Response]
```

### 2.4: Code Evidence

For each major claim, provide:

- File path and line numbers
- Code snippets as evidence
- Explanation of the code's role

### 2.5: Answer to Investigation Questions

Address each question from `## Investigation Questions` with:

- Direct answer
- Supporting evidence (file:line references)
- Confidence level (High/Medium/Low)

### PHASE 2.1: VERIFY AND REFACTOR

Verify your investigation findings align with code patterns from these files:

- `.github/copilot-instructions.md` - Platform patterns
- `.github/instructions/frontend-angular.instructions.md` - Frontend patterns
- `.github/instructions/backend-dotnet.instructions.md` - Backend patterns
- `.github/instructions/clean-code.instructions.md` - Clean code rules

---

## PHASE 3: PRESENTATION

Present findings to the user in a clear, structured format:

1. **Executive Summary**: 2-3 sentences explaining the feature
2. **Detailed Explanation**: Step-by-step logic flow
3. **Code References**: Key files and their roles
4. **Visual Flow**: Text-based diagram of the process
5. **Questions Answered**: Direct responses to user's questions

---

## Investigation Guidelines

- **Evidence-based approach**: Use grep and semantic search to verify assumptions
- **Service boundary discovery**: Find endpoints before assuming responsibilities
- **Never assume service ownership**: Verify patterns with code evidence
- **Trace complete flows**: Don't stop at surface-level understanding
- **Document uncertainties**: Mark unclear areas as "needs verification"
- **Cross-reference findings**: Validate discoveries with multiple sources
- **Platform awareness**: Understand platform base class behaviors

---

## Common Investigation Patterns

### For "How does X work?" questions:

1. Find the entry point (controller, UI component, job)
2. Trace the command/query handler
3. Map domain entity operations
4. Document side effects and events
5. Summarize the complete flow

### For "Where is X handled?" questions:

1. Search for the specific term/concept
2. Identify the owning component
3. Map dependencies and callers
4. Document the responsibility chain

### For "What happens when X?" questions:

1. Identify the trigger condition
2. Trace the execution path
3. Document all branches and conditions
4. Map outputs and side effects

### For "Why does X behave this way?" questions:

1. Find the relevant code
2. Understand the business context
3. Check for related validation/rules
4. Document the design decision rationale
