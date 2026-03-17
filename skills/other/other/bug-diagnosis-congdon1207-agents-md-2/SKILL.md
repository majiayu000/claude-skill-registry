---
name: bug-diagnosis
description: Use when the user asks to debug, diagnose, fix a bug, troubleshoot errors, investigate issues, or pastes error messages/stack traces. Triggers on keywords like "bug", "error", "fix", "not working", "broken", "debug", "stack trace", "exception", "crash", "issue".
---

# Bug Diagnosis & Debugging

You are to operate as an expert full-stack dotnet angular debugging engineer to diagnose, debug, and fix bugs.

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

## PHASE 1: EXTERNAL MEMORY-DRIVEN BUG ANALYSIS

Build a structured knowledge model in `ai_task_analysis_notes/[bug-name].ai_task_analysis_notes_temp.md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with a `## Metadata` heading. Under it, add the full original prompt/error in a markdown box using 5 backticks:

   ```markdown
   [Full original prompt/error here]
   ```

2. **Continue adding** to the `## Metadata` section: the bug description and full details of the `Source Code Structure` from `ai-prompt-context.md`. Use 6 backticks for this nested markdown:

   ```markdown
   ## Bug Description

   [Bug description here]

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
   - `## Error Boundaries` (debugging-specific)
   - `## Interaction Map` (debugging-specific)
   - `## Platform Error Patterns` (debugging-specific)

4. **Populate `## Progress`** with:
   - **Phase**: 1
   - **Items Processed**: 0
   - **Total Items**: 0
   - **Current Operation**: "initialization"
   - **Current Focus**: "[original bug diagnosis task]"

5. **Additional searches to ensure no critical infrastructure is missed**:
   - `grep search` patterns: `.*EventHandler.*{EntityName}|{EntityName}.*EventHandler`
   - `grep search` patterns: `.*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob`
   - `grep search` patterns: `.*Consumer.*{EntityName}|{EntityName}.*Consumer`
   - `grep search` patterns: `.*Service.*{EntityName}|{EntityName}.*Service`
   - `grep search` patterns: `.*Helper.*{EntityName}|{EntityName}.*Helper`
   - Include pattern: `**/*.{cs,ts,html}`

**CRITICAL:** Save ALL file paths immediately as a numbered list under `## File List`. Update the `Total Items` count in `## Progress`.

### DEBUGGING-SPECIFIC DISCOVERY

**ERROR_BOUNDARY_DISCOVERY**: Focus on debugging-relevant patterns:

1. **Error Tracing Analysis**: Find stack traces, map error propagation paths, identify handling patterns. Document under `## Error Boundaries`.

2. **Component Interaction Debugging**: Discover service dependencies, find relevant endpoints/handlers, analyze request flows. Document under `## Interaction Map`.

3. **Platform Debugging Intelligence**: Find platform error patterns (`PlatformValidationResult`, `PlatformException`), CQRS error paths, repository error patterns. Document under `## Platform Error Patterns`.

4. **Discovery searches**:
   - Semantic and grep search all error keywords
   - Prioritize: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers**
   - Save ALL file paths to `## File List`

### PHASE 1B: SYSTEMATIC FILE ANALYSIS FOR DEBUGGING

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

**Debugging-specific fields**:

- `errorPatterns`: Exception handling, validation logic
- `stackTraceRelevance`: Relation to stack traces
- `debuggingComplexity`: Difficulty to debug (1-10)
- `errorPropagation`: How errors flow through component
- `platformErrorHandling`: Use of platform error patterns
- `crossServiceErrors`: Cross-service error scenarios
- `validationLogic`: Business rule validation that could fail
- `dependencyErrors`: Potential dependency failures

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
- Error propagation paths
- All business logic workflows: From front-end to back-end
  - Example: Front-end Component => Controller Api Service => Command/Query => EventHandler => Others (Send email, producer bus message)
  - Example: Background Job => Event Handler => Others
- Integration points and failure points
- Cross-service dependencies identified

---

## PHASE 2: MULTI-DIMENSIONAL ROOT CAUSE ANALYSIS

**Prerequisites**: Ensure ALL files are analyzed. Read the ENTIRE analysis notes file.

Perform systematic analysis under `## Root Cause Analysis`:

### Root Cause Dimensions

1. **Technical Root Causes**: Code defects, architectural issues
2. **Business Logic Root Causes**: Rule violations, validation failures
3. **Process Root Causes**: Missing validation, inadequate testing
4. **Data Root Causes**: Data corruption, integrity violations
5. **Environmental Root Causes**: Configuration issues, deployment problems
6. **Integration Root Causes**: API contract violations, communication failures

### Document

- `potentialRootCauses` ranked by probability
- Generate `## Fix Strategy` with alternatives:
  - `suggestedFix`
  - `riskAssessment`
  - `regressionMitigation`
  - `testingStrategy`
  - `rollbackPlan`

### PHASE 2.1: VERIFY AND REFACTOR

First, verify and ensure your fix strategy follows code patterns and conventions from these files:

- `.github/copilot-instructions.md` - Platform patterns
- `.github/instructions/frontend-angular.instructions.md` - Frontend patterns
- `.github/instructions/backend-dotnet.instructions.md` - Backend patterns
- `.github/instructions/clean-code.instructions.md` - Clean code rules

Then verify and ensure your fix satisfies clean code rules.

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present comprehensive root cause analysis and prioritized fix strategy for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: DEBUGGING EXECUTION

Once approved:

1. Before creating or modifying **ANY** file, you **MUST** first load its relevant entry from your `## Knowledge Graph`
2. Execute the fix plan
3. Use all DEBUGGING_SAFEGUARDS
4. If any step fails, **HALT**, report the failure, and return to the APPROVAL GATE
5. Test the fix thoroughly

---

## SUCCESS VALIDATION

Before completion:

1. Verify fix resolves the bug without regressions
2. Document under `## Debugging Validation` heading:
   - Bug reproduction steps (before)
   - Fix verification steps (after)
   - Regression testing results
3. Summarize changes in `changelog.md`

---

## Debugging Guidelines

- **Evidence-based debugging**: Start with actual error messages, stack traces, and logs
- **Platform error patterns**: Use `PlatformValidationResult` and `PlatformException` patterns
- **Hypothesis-driven approach**: Test one hypothesis at a time with evidence
- **Minimal impact fixes**: Prefer targeted fixes over broad refactoring
- **Verify before claiming**: Never assume - always trace the actual code path
- **Service boundary discovery**: Find endpoints before assuming responsibilities
- **Never assume service ownership**: Verify patterns with code evidence
