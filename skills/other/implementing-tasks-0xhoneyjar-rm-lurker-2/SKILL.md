---
parallel_threshold: 3000
timeout_minutes: 120
zones:
  system:
    path: .claude
    permission: none
  state:
    paths: [loa-grimoire, .beads]
    permission: read-write
  app:
    paths: [src, lib, app]
    permission: read
---

# Sprint Task Implementer

<objective>
Implement sprint tasks from `loa-grimoire/sprint.md` with production-grade code and comprehensive tests. Generate detailed implementation report at `loa-grimoire/a2a/sprint-N/reviewer.md`. Address feedback iteratively until senior lead and security auditor approve.
</objective>

<zone_constraints>
## Zone Constraints

This skill operates under **Managed Scaffolding**:

| Zone | Permission | Notes |
|------|------------|-------|
| `.claude/` | NONE | System zone - never suggest edits |
| `loa-grimoire/`, `.beads/` | Read/Write | State zone - project memory |
| `src/`, `lib/`, `app/` | Read-only | App zone - requires user confirmation |

**NEVER** suggest modifications to `.claude/`. Direct users to `.claude/overrides/` or `.loa.config.yaml`.
</zone_constraints>

<integrity_precheck>
## Integrity Pre-Check (MANDATORY)

Before ANY operation, verify System Zone integrity:

1. Check config: `yq eval '.integrity_enforcement' .loa.config.yaml`
2. If `strict` and drift detected -> **HALT** and report
3. If `warn` -> Log warning and proceed with caution
</integrity_precheck>

<factual_grounding>
## Factual Grounding (MANDATORY)

Before ANY synthesis, planning, or recommendation:

1. **Extract quotes**: Pull word-for-word text from source files
2. **Cite explicitly**: `"[exact quote]" (file.md:L45)`
3. **Flag assumptions**: Prefix ungrounded claims with `[ASSUMPTION]`

**Grounded Example:**
```
The SDD specifies "PostgreSQL 15 with pgvector extension" (sdd.md:L123)
```

**Ungrounded Example:**
```
[ASSUMPTION] The database likely needs connection pooling
```
</factual_grounding>

<structured_memory_protocol>
## Structured Memory Protocol

### On Session Start
1. Read `loa-grimoire/NOTES.md`
2. Restore context from "Session Continuity" section
3. Check for resolved blockers

### During Execution
1. Log decisions to "Decision Log"
2. Add discovered issues to "Technical Debt"
3. Update sub-goal status
4. **Apply Tool Result Clearing** after each tool-heavy operation

### Before Compaction / Session End
1. Summarize session in "Session Continuity"
2. Ensure all blockers documented
3. Verify all raw tool outputs have been decayed
</structured_memory_protocol>

<tool_result_clearing>
## Tool Result Clearing

After tool-heavy operations (grep, cat, tree, API calls):
1. **Synthesize**: Extract key info to NOTES.md or discovery/
2. **Summarize**: Replace raw output with one-line summary
3. **Clear**: Release raw data from active reasoning

Example:
```
# Raw grep: 500 tokens -> After decay: 30 tokens
"Found 47 AuthService refs across 12 files. Key locations in NOTES.md."
```
</tool_result_clearing>

<trajectory_logging>
## Trajectory Logging

Log each significant step to `loa-grimoire/a2a/trajectory/{agent}-{date}.jsonl`:

```json
{"timestamp": "...", "agent": "...", "action": "...", "reasoning": "...", "grounding": {...}}
```
</trajectory_logging>

<kernel_framework>
## Task (N - Narrow Scope)
Implement sprint tasks from `loa-grimoire/sprint.md` with production-grade code and tests. Generate implementation report at `loa-grimoire/a2a/sprint-N/reviewer.md`. Address feedback iteratively.

## Context (L - Logical Structure)
- **Input**: `loa-grimoire/sprint.md` (tasks), `loa-grimoire/prd.md` (requirements), `loa-grimoire/sdd.md` (architecture)
- **Feedback loops**:
  - `loa-grimoire/a2a/sprint-N/auditor-sprint-feedback.md` (security audit - HIGHEST PRIORITY)
  - `loa-grimoire/a2a/sprint-N/engineer-feedback.md` (senior lead review)
- **Integration context**: `loa-grimoire/a2a/integration-context.md` (if exists) for context preservation, documentation locations, commit formats
- **Current state**: Sprint plan with acceptance criteria
- **Desired state**: Working, tested implementation + comprehensive report

## Constraints (E - Explicit)
- DO NOT start new work without checking for audit feedback FIRST (highest priority)
- DO NOT start new work without checking for engineer feedback SECOND
- DO NOT assume feedback meaning—ask clarifying questions if unclear
- DO NOT skip tests—comprehensive test coverage is non-negotiable
- DO NOT ignore existing codebase patterns—follow established conventions
- DO NOT skip reading context files—always review PRD, SDD, sprint.md
- DO link implementations to source discussions if integration context requires
- DO update relevant documentation if specified in integration context
- DO format commits per org standards if defined
- DO follow SemVer for version updates

## Verification (E - Easy to Verify)
**Success** = All acceptance criteria met + comprehensive tests pass + detailed report at expected path

Report MUST include:
- Executive Summary
- Tasks Completed (files/lines modified, approach, test coverage)
- Technical Highlights (architecture, performance, security, integrations)
- Testing Summary (test files, scenarios, how to run)
- Known Limitations
- Verification Steps for reviewer
- Feedback Addressed section (if iteration after feedback)

## Reproducibility (R - Reproducible Results)
- Write tests with specific assertions: NOT "it works" → "returns 200 status, response includes user.id field"
- Document specific file paths and line numbers: NOT "updated auth" → "src/auth/middleware.ts:42-67"
- Include exact commands to reproduce: NOT "run tests" → "npm test -- --coverage --watch=false"
- Reference specific commits or branches when relevant
</kernel_framework>

<uncertainty_protocol>
- If requirements are ambiguous, reference PRD and SDD for clarification
- If feedback is unclear, ASK specific clarifying questions before proceeding
- Say "I need clarification on [X]" when feedback meaning is uncertain
- Document interpretations and reasoning in report for reviewer attention
- Flag technical tradeoffs explicitly for reviewer decision
</uncertainty_protocol>

<grounding_requirements>
Before implementing:
1. Check `loa-grimoire/a2a/sprint-N/auditor-sprint-feedback.md` FIRST (security audit)
2. Check `loa-grimoire/a2a/sprint-N/engineer-feedback.md` SECOND (senior lead)
3. Check `loa-grimoire/a2a/integration-context.md` for organizational context
4. Read `loa-grimoire/sprint.md` for acceptance criteria
5. Read `loa-grimoire/sdd.md` for technical architecture
6. Read `loa-grimoire/prd.md` for business requirements
7. Quote requirements when implementing: `> From sprint.md: Task 1.2 requires...`
</grounding_requirements>

<citation_requirements>
- Reference sprint task IDs when implementing
- Cite SDD sections for architectural decisions
- Include file paths and line numbers in report
- Quote feedback items when addressing them
- Reference test file paths and coverage metrics
</citation_requirements>

<workflow>
## Phase -2: Beads Integration Check

Check if Beads is available for task lifecycle management:

```bash
.claude/scripts/check-beads.sh --quiet
```

**If INSTALLED**, use Beads for task lifecycle:
- `bd ready` - Get next actionable task (JIT retrieval)
- `bd update <task-id> --status in_progress` - Mark task started (done automatically)
- `bd close <task-id>` - Mark task completed (done automatically)
- Task state persists across context windows

**If NOT_INSTALLED**, use markdown-based tracking from sprint.md.

**IMPORTANT**: Users should NOT run bd commands manually. This agent handles the entire Beads lifecycle internally:

1. On start: Run `bd ready` to find first unblocked task
2. Before implementing: Auto-run `bd update <task-id> --status in_progress`
3. After completing: Auto-run `bd close <task-id>`
4. Repeat until sprint complete

## Phase -1: Context Assessment & Parallel Task Splitting (CRITICAL—DO THIS FIRST)

Assess context size to determine if parallel splitting is needed:

```bash
wc -l loa-grimoire/prd.md loa-grimoire/sdd.md loa-grimoire/sprint.md loa-grimoire/a2a/*.md 2>/dev/null
```

**Thresholds:**
| Size | Lines | Strategy |
|------|-------|----------|
| SMALL | <3,000 | Sequential implementation |
| MEDIUM | 3,000-8,000 | Consider parallel if >3 independent tasks |
| LARGE | >8,000 | MUST split into parallel |

**If MEDIUM/LARGE:** See `<parallel_execution>` section below.

**If SMALL:** Proceed to Phase 0.

## Phase 0: Check Feedback Files and Integration Context (BEFORE NEW WORK)

### Step 1: Security Audit Feedback (HIGHEST PRIORITY)

Check `loa-grimoire/a2a/sprint-N/auditor-sprint-feedback.md`:

**If exists + "CHANGES_REQUIRED":**
- Sprint FAILED security audit
- MUST address ALL CRITICAL and HIGH priority security issues
- Address MEDIUM and LOW if feasible
- Update report with "Security Audit Feedback Addressed" section
- Quote each audit issue with your fix and verification steps

**If exists + "APPROVED - LETS FUCKING GO":**
- Sprint passed security audit
- Proceed to check engineer feedback

**If missing:**
- No security audit yet
- Proceed to check engineer feedback

### Step 2: Senior Lead Feedback

Check `loa-grimoire/a2a/sprint-N/engineer-feedback.md`:

**If exists + NOT "All good":**
- Senior lead requested changes
- Address all feedback items systematically
- Update report with "Feedback Addressed" section

**If exists + "All good":**
- Sprint approved by senior lead
- Proceed with new work or wait for security audit

**If missing:**
- First implementation
- Proceed with implementing sprint tasks

### Step 3: Integration Context

Check `loa-grimoire/a2a/integration-context.md`:

**If exists**, read for:
- Context preservation requirements (link to source discussions)
- Documentation locations (where to update status)
- Commit message formats (e.g., "[LIN-123] Description")
- Available MCP tools

## Phase 1: Context Gathering and Planning

1. Review core documentation:
   - `loa-grimoire/sprint.md` - Primary task list and acceptance criteria
   - `loa-grimoire/prd.md` - Product requirements and business context
   - `loa-grimoire/sdd.md` - System design and technical architecture

2. Analyze existing codebase:
   - Understand current architecture and patterns
   - Identify existing components to integrate with
   - Note coding standards and conventions
   - Review existing test patterns

3. Create implementation strategy:
   - Break down tasks into logical order
   - Identify task dependencies
   - Plan test coverage for each component

## Phase 2: Implementation

### Beads Task Loop (if Beads installed)

```bash
# 1. Get next actionable task
TASK=$(bd ready --format json | head -1)
TASK_ID=$(echo $TASK | jq -r '.id')

# 2. Mark in progress (automatic - user never sees this)
bd update $TASK_ID --status in_progress

# 3. Implement the task...

# 4. Mark complete (automatic - user never sees this)
bd close $TASK_ID

# 5. Repeat for next task
```

The user only runs `/implement sprint-1`. All bd commands are invisible.

### For each task:
1. Implement according to specifications
2. Follow established project patterns
3. Write clean, maintainable, documented code
4. Consider performance, security, scalability
5. Handle edge cases and errors gracefully

**Testing Requirements:**
- Comprehensive unit tests for all new code
- Test both happy paths and error conditions
- Include edge cases and boundary conditions
- Follow existing test patterns
- Ensure tests are readable and maintainable

**Code Quality Standards:**
- Self-documenting with clear names
- Comments for complex logic
- DRY principles
- Consistent formatting
- Future maintainability

## Phase 3: Documentation and Reporting

Create report at `loa-grimoire/a2a/sprint-N/reviewer.md`:

Use template from `resources/templates/implementation-report.md`.

Key sections:
- Executive Summary
- Tasks Completed (with files, approach, tests)
- Technical Highlights
- Testing Summary
- Known Limitations
- Verification Steps

## Phase 4: Feedback Integration Loop

1. Monitor for feedback files
2. When feedback received:
   - Read thoroughly
   - If unclear: ask specific clarifying questions
   - Never assume about vague feedback
3. Address feedback systematically
4. Generate updated report
</workflow>

<parallel_execution>
## When to Split

- SMALL (<3,000 lines): Sequential
- MEDIUM (3,000-8,000 lines) with >3 independent tasks: Consider parallel
- LARGE (>8,000 lines): MUST split

## Option A: Parallel Feedback Checking (Phase 0)

When multiple feedback sources exist:

```
Spawn 2 parallel Explore agents:

Agent 1: "Read loa-grimoire/a2a/sprint-N/auditor-sprint-feedback.md:
1. Does file exist?
2. If yes, verdict (CHANGES_REQUIRED or APPROVED)?
3. If CHANGES_REQUIRED, list all CRITICAL/HIGH issues with file paths
Return: structured summary"

Agent 2: "Read loa-grimoire/a2a/sprint-N/engineer-feedback.md:
1. Does file exist?
2. If yes, verdict (All good or changes requested)?
3. If changes, list all feedback items with file paths
Return: structured summary"
```

## Option B: Parallel Task Implementation (Phase 2)

When sprint has multiple independent tasks:

```
1. Read sprint.md and identify all tasks
2. Analyze task dependencies
3. Group into parallel batches:
   - Batch 1: Tasks with no dependencies (parallel)
   - Batch 2: Tasks depending on Batch 1 (after Batch 1)

For independent tasks, spawn parallel agents:
Agent 1: "Implement Task 1.2 - read acceptance criteria, review patterns, implement, write tests, return summary"
Agent 2: "Implement Task 1.3 - read acceptance criteria, review patterns, implement, write tests, return summary"
```

## Consolidation

1. Collect results from all parallel agents
2. Verify no conflicts between implementations
3. Run integration tests across all changes
4. Generate unified report
</parallel_execution>

<output_format>
See `resources/templates/implementation-report.md` for full structure.

Key sections:
- Executive Summary
- Tasks Completed (files, approach, tests)
- Technical Highlights
- Testing Summary
- Known Limitations
- Verification Steps
- Feedback Addressed (if iteration)
</output_format>

<success_criteria>
- **Specific**: Every task implemented per acceptance criteria
- **Measurable**: Test coverage metrics included
- **Achievable**: All sprint tasks completed
- **Relevant**: Implementation matches PRD/SDD
- **Time-bound**: Report generated for review
</success_criteria>

<semver_requirements>
## Version Format: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backwards-compatible additions)
- **PATCH**: Bug fixes (backwards-compatible fixes)

### When to Update Version

| Change | Bump | Example |
|--------|------|---------|
| New feature implementation | MINOR | 0.1.0 → 0.2.0 |
| Bug fix | PATCH | 0.2.0 → 0.2.1 |
| Breaking API change | MAJOR | 0.2.1 → 1.0.0 |

### Version Update Process

1. Determine bump type based on changes
2. Update package.json version
3. Update CHANGELOG.md with sections: Added, Changed, Fixed, Removed, Security
4. Reference version in completion comments
</semver_requirements>

<checklists>
See `resources/REFERENCE.md` for complete checklists:
- Pre-Implementation Checklist
- Code Quality Checklist
- Testing Checklist
- Documentation Checklist
- Versioning Checklist

**Red Flags (immediate action required):**
- No tests for new code
- Hardcoded secrets
- Skipped error handling
- Ignored existing patterns
</checklists>
