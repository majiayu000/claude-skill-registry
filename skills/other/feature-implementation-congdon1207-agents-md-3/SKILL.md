---
name: feature-implementation
description: Use when the user asks to implement a new feature, enhancement, add functionality, build something new, or create new capabilities. Triggers on keywords like "implement", "add feature", "build", "create new", "develop", "enhancement".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
---

# Implementing a New Feature or Enhancement

You are to operate as an expert full-stack dotnet angular principle developer, software architecture to implement new requirements.

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
- Batch Write operations when creating multiple files

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

## PHASE 1: EXTERNAL MEMORY-DRIVEN KNOWLEDGE MODEL CONSTRUCTION

Your sole objective is to build a structured knowledge model in a Markdown analysis file at `ai_task_analysis_notes/[semantic-name].ai_task_analysis_notes_temp.md` with systematic external memory management.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with a `## Metadata` heading. Under it, add the full original prompt in a markdown box using 5 backticks:

   ```markdown
   [Full original prompt here]
   ```

2. **Continue adding** to the `## Metadata` section: the task description and full details of the `Source Code Structure` from `ai-prompt-context.md`. Use 6 backticks for this nested markdown:

   ```markdown
   ## Task Description

   [Task description here]

   ## Source Code Structure

   [Full details from ai-prompt-context.md]
   ```

3. **Create all required headings**:
   - `## Progress`
   - `## Errors`
   - `## Assumption Validations`
   - `## Performance Metrics`
   - `## Memory Management`
   - `## Processed Files`
   - `## File List`
   - `## Knowledge Graph`

4. **Populate `## Progress`** with:
   - **Phase**: 1
   - **Items Processed**: 0
   - **Total Items**: 0
   - **Current Operation**: "initialization"
   - **Current Focus**: "[original task summary]"

5. **Discovery searches** - Semantic search and grep search all keywords to find:
   - **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, front-end Components .ts**

6. **Additional targeted searches to ensure no critical infrastructure is missed**:
   - `grep search` patterns: `.*EventHandler.*{EntityName}|{EntityName}.*EventHandler`
   - `grep search` patterns: `.*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob`
   - `grep search` patterns: `.*Consumer.*{EntityName}|{EntityName}.*Consumer`
   - `grep search` patterns: `.*Service.*{EntityName}|{EntityName}.*Service`
   - `grep search` patterns: `.*Helper.*{EntityName}|{EntityName}.*Helper`
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
- `businessContext`: Comprehensive detail of all business logic, how it contributes to requirements
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

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive `overallAnalysis:` summary showing:

- Complete end-to-end workflows discovered
- Key architectural patterns and relationships
- All business logic workflows: From front-end to back-end
  - Example: Front-end Component => Controller Api Service => Command/Query => EventHandler => Others (Send email, producer bus message)
  - Example: Background Job => Event Handler => Others
- Integration points and dependencies
- Cross-service dependencies identified

---

## PHASE 2: PLAN GENERATION

**Prerequisites**: Ensure ALL files are analyzed. Read the ENTIRE analysis notes file.

Generate detailed implementation plan under `## Plan` heading:

- Follow coding conventions from platform documentation
- Think step-by-step with todo list
- Reference patterns for each step

### PHASE 2.1: VERIFY AND REFACTOR

First, verify and ensure your implementation plan follows code patterns and conventions from these files:

- `.github/copilot-instructions.md` - Platform patterns
- `.github/instructions/frontend-angular.instructions.md` - Frontend patterns
- `.github/instructions/backend-dotnet.instructions.md` - Backend patterns
- `.github/instructions/clean-code.instructions.md` - Clean code rules

Then verify and ensure your implementation plan satisfies clean code rules.

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present the plan for explicit user approval. **DO NOT** proceed without it.

---

## PHASE 4: EXECUTION

Once approved:

1. Before creating or modifying **ANY** file, you **MUST** first load its relevant entry from your `## Knowledge Graph`
2. Use all **EXECUTION_SAFEGUARDS**
3. If any step fails, **HALT**, report the failure, and return to the APPROVAL GATE

---

## SUCCESS VALIDATION

Before completion:

1. Verify implementation against all requirements
2. Document under `## Success Validation` heading
3. Summarize changes in `changelog.md`

---

## Coding Guidelines

- **Evidence-based approach**: Use grep and semantic search to verify assumptions
- **Service boundary discovery**: Find endpoints before assuming responsibilities
- **Never assume service ownership**: Verify patterns with code evidence
- **Platform-first approach**: Use established templates
- **Cross-service sync**: Use event bus, not direct database access
- **CQRS adherence**: Follow established Command/Query patterns
- **Clean architecture respect**: Maintain proper layer dependencies
