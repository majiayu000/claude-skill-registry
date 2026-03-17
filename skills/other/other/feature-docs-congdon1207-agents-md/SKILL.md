---
name: feature-docs
description: Use when the user asks to generate comprehensive feature documentation with verified test cases, create feature README with code evidence, or document a complete feature with test verification. Triggers on keywords like "feature documentation", "document feature", "comprehensive docs", "feature README", "test verification", "verified documentation".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Feature Documentation Generation & Verification

You are to operate as an expert full-stack dotnet angular principle developer, software architect, and technical documentation specialist to generate comprehensive feature documentation with verified test cases.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## CRITICAL TASK MANAGEMENT FOR LONG-RUNNING DOCUMENTATION

- This is a multi-phase, long-running task that generates large documentation files
- Break ALL tasks into the smallest possible atomic units
- Each sub-task MUST include a brief summary of previous task results to maintain context
- Before each new sub-task, read the current state of generated files to re-establish context
- Update progress tracking after EVERY operation
- Never assume previous context is retained - always verify by reading files

### MANDATORY TODO LIST MANAGEMENT

1. **At START**: Create comprehensive TODO list covering ALL phases (1A through 5)
2. **Before EACH phase**: Mark current task as "in_progress"
3. **After EACH phase**: Mark task as "completed", update "Last Task Summary"
4. **Never skip**: If context is lost, re-read analysis file's `## Progress` section
5. **Never compact**: Keep full detailed TODO list even if long

### MANDATORY BEFORE EACH PHASE CHECKLIST

```
[ ] Read the `## Progress` section from analysis notes file
[ ] Read the `Last Task Summary` from previous phase
[ ] Read the current state of generated documentation file(s)
[ ] Confirm what was completed and what needs to be done next
[ ] Update current task status to "in_progress"
[ ] Only then proceed with the phase work
```

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

### DOCUMENTATION_ACCURACY_CHECKPOINT

Before writing any documentation:

- "Have I read the actual code that implements this?"
- "Are my line number references accurate and current?"
- "Can I provide a code snippet as evidence?"

### CONTEXT_ANCHOR_SYSTEM

Every 10 operations:

1. Re-read the original task description
2. Verify current operation aligns with original goals
3. Update `Current Focus` in `## Progress` section
4. **CRITICAL**: Re-read last 50 lines of documentation being generated

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN FEATURE ANALYSIS

Build knowledge model in `ai_task_analysis_notes/[feature-name].ai_task_analysis_notes_temp.md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

Initialize with:

- `## Metadata`, `## Progress`, `## Errors`, `## Assumption Validations`
- `## Performance Metrics`, `## Memory Management`, `## Processed Files`
- `## File List`, `## Knowledge Graph`, `## Feature Summary`

**Populate `## Progress`** with:

- **Phase**: 1A
- **Items Processed**: 0
- **Total Items**: 0
- **Current Operation**: "initialization"
- **Current Focus**: "[feature documentation task]"
- **Last Task Summary**: "Starting feature documentation generation"

### FEATURE-SPECIFIC DISCOVERY

1. **Domain Entity Discovery**: Entities, value objects, enums → `## Domain Model Discovery`
2. **Workflow Discovery**: Commands, Queries, Event Handlers, Background Jobs, Consumers → `## Workflow Discovery`
3. **API Discovery**: Controllers, endpoints, DTOs → `## API Discovery`
4. **Frontend Discovery**: Components, Services, Stores → `## Frontend Discovery`
5. **Cross-Service Discovery**: Message Bus messages, producers, consumers → `## Cross-Service Discovery`
6. **Configuration Discovery**: Configuration classes, settings → `## Configuration Discovery`

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document:

- Standard fields plus:
- `testableAspects`: What aspects should be tested (P0/P1/P2)
- `codeSnippets`: Key code snippets with line numbers for documentation

### PHASE 1C: OVERALL ANALYSIS

Write `## Feature Summary`:

- **Feature Overview**: What the feature does
- **Complete End-to-End Workflows**: From trigger to completion
- **Key Architectural Patterns**: Design patterns used
- **Service Responsibilities**: Which service owns what
- **Integration Points**: Cross-service communication
- **Security Considerations**: Auth, authz, encryption
- **Performance Considerations**: Pagination, caching, parallelism
- **Error Handling Patterns**: How errors are handled

---

## PHASE 2: FEATURE README GENERATION

Generate at `docs/README.[FeatureName].md`.

**CRITICAL**: Break into sub-tasks, update file incrementally.

### PHASE 2A: Overview & Architecture Sections

- Title and Overview
- Table of Contents
- Key Capabilities
- Architecture diagram (ASCII art)
- Service Responsibilities table
- Design Patterns table

**After**: Update `Last Task Summary`

### PHASE 2B: Domain Model & Workflow Sections

- Entity Relationship Diagram (ASCII art)
- Entity descriptions with properties
- Enumerations with values
- Workflow diagrams and step-by-step processes
- Code snippets with file paths and line numbers

**After**: Update `Last Task Summary`

### PHASE 2C: API Reference & Configuration

- Endpoint table
- Request/Response models
- Configuration settings
- Security Considerations
- Performance Tuning

**After**: Update `Last Task Summary`

### PHASE 2D: Test Specifications Section

**CRITICAL**: Largest section - break into sub-tasks by category.

**Test Case Format**:

```markdown
### [Category] Test Specs

#### P0 - Critical

##### TS-[CATEGORY]-P0-001: [Test Name]

**Priority:** P0 - Critical
**Category:** [Category]
**Component:** [Component]

**Preconditions:**

- [List preconditions]

**Test Steps:**
| Step | Action | Expected Result |
| ---- | -------- | --------------- |
| 1 | [Action] | [Expected] |

**GIVEN** [initial context]
**WHEN** [action performed]
**THEN** [expected outcome]

**Code Reference:**

- File: `[file-path]`
- Lines: [line-range]
- Key Logic: [description]
```

Execute one category at a time:

- **Phase 2D-1**: Summary table + first category
- **Phase 2D-2 through 2D-N**: Remaining categories
- **Phase 2D-Final**: Update summary table with counts

**After each**: Update `Last Task Summary`

### PHASE 2E: Final Sections

- Troubleshooting
- Adding New Providers (if applicable)
- Related Documentation
- Version History

---

## PHASE 3: README VERIFICATION - FIRST PASS

**PURPOSE**: Verify README matches actual code. NO HALLUCINATION ALLOWED.

Verify one section at a time:

- Read ENTIRE section
- For EACH code reference:
  - Read actual source file at referenced lines
  - Compare character-by-character
  - Verify line numbers are accurate
  - Log mismatches in `## Verification Log - First Pass`
  - Correct immediately

**After**: Update `Last Task Summary`

---

## PHASE 4: README VERIFICATION - SECOND PASS

Re-verify all first-pass corrections:

- Random sampling (10 code references)
- Cross-reference and TOC verification
- Completeness check

**CRITICAL**: If Second Pass finds MORE THAN 5 issues, HALT and re-run Phase 3.

---

## PHASE 5: FINAL VALIDATION AND CLEANUP

### Phase 5-1: README Consistency Check

- Verify test case IDs are unique and sequential
- Verify table of contents matches sections
- Verify counts match in summary tables

### Phase 5-2: Final Quality Report

- Count total lines in README
- Count test cases by priority (P0, P1, P2)
- Count issues found and corrected during verification
- Calculate verification coverage percentage

### Phase 5-3: Generate Final Summary

Document under `## Final Validation`:

- **README Accuracy:** [VERIFIED after 2 passes]
- **Total Issues Found and Corrected:** [X issues]
- **Generated Files:** List all files
- **Final Task Summary:** Complete metrics

---

## Feature Documentation Guidelines

- **Evidence-based documentation**: Every claim must have code evidence with file path and line numbers
- **No hallucination tolerance**: If uncertain, mark as "inferred" and verify
- **Incremental generation**: Break large documents into sections, verify each
- **Context preservation**: Always re-read generated content before continuing
- **Multiple verification passes**: Minimum 2 verification passes for README
- **BDD test format**: All test cases must follow GIVEN/WHEN/THEN format
- **Priority classification**: P0 (critical), P1 (high), P2 (medium)
- **Code snippets**: Include actual code with file paths and line numbers for reference
- **Line number accuracy**: Always verify line numbers are current
- **Cross-reference consistency**: Ensure all internal references within README are accurate
