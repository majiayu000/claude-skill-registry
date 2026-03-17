---
name: bug-diagnosis
description: Use when the user asks to debug, diagnose, fix a bug, troubleshoot errors, investigate issues, or pastes error messages/stack traces. Triggers on keywords like "bug", "error", "fix", "not working", "broken", "debug", "stack trace", "exception", "crash", "issue".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
infer: true
---

> **Skill Variant:** Use this skill for **bug diagnosis, debugging, and fixing**. For feature investigation without fixes, use `feature-investigation`. For structured autonomous debugging workflows, use `tasks-bug-diagnosis`.

# Bug Diagnosis & Debugging

You are to operate as an expert full-stack dotnet angular debugging engineer to diagnose, debug, and fix the bug described in `[bug-description-or-bug-info-file-path]`.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation. Todo list must cover all phases, from start to end, include child tasks in each phases too, everything is flatted out into a long detailed todo list.

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

Your sole objective is to build a structured knowledge model in a Markdown analysis file at `.ai/workspace/analysis/[some-sort-semantic-name-of-this-task].md` with systematic external memory management.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with:
    - `## Metadata` heading with original prompt in markdown box (use 5-6 backticks for proper nesting)
    - Task description and `Source Code Structure` from `.ai/prompts/context.md`
    - Create headings: `## Progress`, `## Errors`, `## Assumption Validations`, `## Performance Metrics`, `## Memory Management`, `## Processed Files`, `## File List`, `## Knowledge Graph`

2. **Populate `## Progress`** with:
    - **Phase**: 1
    - **Items Processed**: 0
    - **Total Items**: 0
    - **Current Operation**: "initialization"
    - **Current Focus**: "[original bug diagnosis task]"

### DEBUGGING-SPECIFIC DISCOVERY

**ERROR_BOUNDARY_DISCOVERY**: Focus on debugging-relevant patterns:

1. **Error Tracing Analysis**: Find stack traces, map error propagation paths, identify handling patterns. Document under `## Error Boundaries`.

2. **Component Interaction Debugging**: Discover service dependencies, find relevant endpoints/handlers, analyze request flows. Document under `## Interaction Map`.

3. **Platform Debugging Intelligence**: Find platform error patterns (`PlatformValidationResult`, `PlatformException`), CQRS error paths, repository error patterns. Document under `## Platform Error Patterns`.

4. **Discovery searches**:
    - Semantic and grep search all error keywords from the task
    - Prioritize: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, Frontend Components**
    - Additional targeted searches:
        - `.*EventHandler.*{EntityName}|{EntityName}.*EventHandler`
        - `.*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob`
        - `.*Consumer.*{EntityName}|{EntityName}.*Consumer`
        - `.*Service.*{EntityName}|{EntityName}.*Service`
        - `.*Helper.*{EntityName}|{EntityName}.*Helper`
        - All files with pattern: `**/*.{cs,ts,html}`
    - Save ALL file paths to `## File List`

### PHASE 1B: SYSTEMATIC FILE ANALYSIS FOR DEBUGGING

**IMPORTANT: MUST DO WITH TODO LIST**

1. Count total files in file list
2. Split into batches of 10 files in priority order
3. Each batch inserts new task in todo list for analysis
4. **CRITICAL**: Analyze ALL high-priority files: Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, Frontend Components

For each file, document in `## Knowledge Graph`:

**Core Fields:**

- `filePath`: Full path to the file
- `type`: Component classification (Entity, Command, Query, EventHandler, Controller, etc.)
- `architecturalPattern`: Design pattern used
- `content`: Summary of purpose and logic
- `symbols`: Important classes, interfaces, methods
- `dependencies`: All imported modules or using statements
- `businessContext`: Comprehensive detail all business logic, how it contributes to the requirements
- `referenceFiles`: Other files that use this file's symbols
- `relevanceScore`: Numerical score (1-10) for bug relevance
- `evidenceLevel`: "verified" or "inferred"
- `uncertainties`: Any aspects you are unsure about
- `platformAbstractions`: Platform base classes used
- `serviceContext`: Which microservice this file belongs to
- `dependencyInjection`: Any DI registrations
- `genericTypeParameters`: Generic type relationships

**Debugging-Specific Fields:**

- `errorPatterns`: Exception handling, validation logic
- `stackTraceRelevance`: Relation to any stack traces
- `debuggingComplexity`: Difficulty to debug (1-10)
- `errorPropagation`: How errors flow through the component
- `platformErrorHandling`: Use of platform error patterns
- `crossServiceErrors`: Any cross-service error scenarios
- `validationLogic`: Business rule validation that could fail
- `dependencyErrors`: Potential dependency failures

**For Consumer Files (CRITICAL):**

- `messageBusMessage`: Message type consumed
- `messageBusProducers`: grep search across ALL services to find files that send/publish this message
- `crossServiceIntegration`: Cross-service data flow
- `handleLogicWorkflow`: Processing workflow in HandleLogicAsync

**Targeted Aspect Analysis:**

- **For Front-End:** `componentHierarchy`, `routeConfig`, `routeGuards`, `stateManagementStores`, `dataBindingPatterns`, `validationStrategies`
- **For Back-End:** `authorizationPolicies`, `commands`, `queries`, `domainEntities`, `repositoryPatterns`, `businessRuleImplementations`
- **For Consumers:** `messageBusMessage`, `messageBusProducers`, `crossServiceIntegration`, `handleLogicWorkflow`

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive `overallAnalysis` summary showing:

- Complete end-to-end workflows discovered
- Error propagation paths
- Key architectural patterns and relationships
- All business logic workflows:
    - Front-end to back-end flow: Component => API Service => Controller => Command/Query => EventHandler => Others
    - Background job flow: Job => EventHandler => Others
- Integration points and failure points

---

## PHASE 2: MULTI-DIMENSIONAL ROOT CAUSE ANALYSIS & COMPREHENSIVE FIX STRATEGY

**IMPORTANT**: Ensure ALL files are analyzed before this phase. Read the ENTIRE Markdown analysis notes file.

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
- For each root cause:
    - **Evidence**: file:line references supporting this hypothesis
    - **Confidence**: percentage with justification
    - **Impact**: what's affected if this is the cause

### Generate Fix Strategy

Under `## Fix Strategy`, document alternatives, each including:

- `suggestedFix`: Detailed fix description with file:line targets
- `riskAssessment`: Low/Medium/High with justification
- `regressionMitigation`: Steps to prevent breaking existing functionality
- `testingStrategy`: How to verify the fix works
- `rollbackPlan`: How to undo if the fix causes issues

### PHASE 2.1: VERIFY AND REFACTOR

Verify fix strategy follows code patterns from:

- `.github/copilot-instructions.md`
- `.github/instructions/frontend-angular.instructions.md`
- `.github/instructions/backend-dotnet.instructions.md`
- `.github/instructions/clean-code.instructions.md`

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present comprehensive root cause analysis and prioritized fix strategy for my explicit approval.

**Format for Approval Request:**

```markdown
## Bug Analysis Complete - Approval Required

### Root Cause Summary

[Primary root cause with evidence]

### Proposed Fix

[Fix description with specific files and changes]

### Risk Assessment

- **Risk Level**: [Low/Medium/High]
- **Regression Risk**: [assessment]
- **Rollback Plan**: [summary]

### Confidence Level: [X%]

### Files to Modify:

1. `path/to/file.cs:line` - [change description]
2. `path/to/file.ts:line` - [change description]

**Awaiting approval to proceed with implementation.**
```

**DO NOT** proceed with implementation without explicit user approval.

---

## PHASE 4: DEBUGGING EXECUTION

Once approved:

1. **Execute the fix plan** following the approved strategy
2. **Use DEBUGGING_SAFEGUARDS**:
    - Make minimal, targeted changes
    - Preserve existing behavior where possible
    - Add comments for non-obvious fixes
3. **Follow platform patterns** from documentation

---

## SUCCESS VALIDATION

Verify fix resolves the bug without regressions. Document under `## Debugging Validation`:

- **Bug Reproduction Steps (Before)**: How to reproduce the original bug
- **Fix Verification Steps (After)**: How to verify the fix works
- **Regression Testing Results**: Confirmation no existing functionality broke

---

## Debugging Guidelines

- **Evidence-based debugging**: Start with actual error messages, stack traces, and logs
- **Platform error patterns**: Use `PlatformValidationResult` and `PlatformException` patterns
- **Hypothesis-driven approach**: Test one hypothesis at a time with evidence
- **Minimal impact fixes**: Prefer targeted fixes over broad refactoring
- **Verify before claiming**: Never assume - always trace the actual code path
- **Service boundary awareness**: Understand which service owns what
- **Cross-service tracing**: Follow message bus flows across services

---

## Platform Error Patterns Reference

### Backend Validation Patterns

```csharp
// Use platform validation fluent API
return base.Validate()
    .And(_ => condition, "Error message")
    .AndAsync(async req => await ValidateAsync(req))
    .AndNotAsync(async req => await CheckForbiddenAsync(req), "Not allowed");

// Use EnsureFound for null checks
await repository.GetByIdAsync(id).EnsureFound($"Not found: {id}");

// Use EnsureValid for validation results
await entity.ValidateAsync(repository, ct).EnsureValidAsync();

// Use PlatformException for domain errors
throw new PlatformDomainException("Business rule violated");
```

### Frontend Error Handling

```typescript
// Use platform loading/error state
this.apiService
    .getData()
    .pipe(
        this.observerLoadingErrorState('loadData'),
        this.tapResponse(
            data => this.updateState({ data }),
            error => this.handleError(error)
        ),
        this.untilDestroyed()
    )
    .subscribe();
```

---

## Quick Verification Checklist

Before removing/changing ANY code:

- [ ] Searched static imports?
- [ ] Searched string literals in code?
- [ ] Checked dynamic invocations (attr, prop, runtime)?
- [ ] Read actual implementations?
- [ ] Traced who depends on this?
- [ ] Assessed what breaks if removed?
- [ ] Documented evidence clearly?
- [ ] Declared confidence level?

**If ANY unchecked → DO MORE INVESTIGATION**
**If confidence < 90% → REQUEST USER CONFIRMATION**

---

## Common Bug Categories

### Data Issues

- Missing null checks
- Incorrect data transformations
- Race conditions in async operations
- Stale cache data

### Validation Issues

- Missing or incorrect validation rules
- Validation bypassed in certain paths
- Async validation not awaited

### Cross-Service Issues

- Message bus delivery failures
- Entity sync out of order (check LastMessageSyncDate)
- API contract mismatches
- Missing dependency waits

### Frontend Issues

- Component lifecycle issues
- State management bugs
- Form validation not triggered
- API error handling missing

### Authorization Issues

- Missing role checks
- Incorrect company context
- Permission not propagated across services

---

## Red Flags & Warning Signs

### Watch For

- "Looks like..." or "Probably..." - These are assumptions, not facts
- "Should be straightforward" - Famous last words
- "Only used in one place" - Verify that place isn't critical
- "Template doesn't use it" - Check for dynamic property access

### Danger Zones

- Modifying platform base classes
- Changing cross-service contracts
- Database schema changes
- Entity event handlers (side effects)
- Background job scheduling

---

## See Also

- `.github/AI-DEBUGGING-PROTOCOL.md` - Comprehensive debugging protocol
- `.ai/prompts/context.md` - Platform patterns and context
- `CLEAN-CODE-RULES.md` - Coding standards
