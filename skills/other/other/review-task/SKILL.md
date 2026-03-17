---
name: review-task
description: Tech lead review of task implementation. Use when user says "zkontroluj task", "review task", "zhodnot implementaci", or runs /review-task.
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, Task, AskUserQuestion
---

# Review Task (Tech Lead Mode)

Perform a thorough tech lead review of task implementation - analyze code quality, verify against specs, check best practices from official documentation.

## Usage

```
/review-task              # Deep review with comprehensive web research (default)
/review-task 02           # Review specific task
/review-task --quick      # Quick review - skip web research
```

## Current State

Current branch:
!git branch --show-current

Recent commits on this branch:
!git log --oneline -10

Changed files vs main:
!git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~5

## Process

### Step 1: Identify Task to Review

**Auto-detection order:**
1. If on feature branch `phase-XX/task-YY-*` → use that task
2. If argument provided → use specified task number
3. Find task with `🔵 in_progress` status in current phase

**Locate task file:**
```bash
# Find current phase from branch or recent work
PHASE_DIR=$(ls -d specification/phase-*/ | tail -1)
TASK_FILE=$(ls "$PHASE_DIR/tasks/task-${TASK_NUM}"*.md 2>/dev/null | head -1)
```

### Step 2: Gather Context

Read these files in parallel:
1. **Task specification** - the task .md file (scope, requirements)
2. **Phase specification** - the phase.md file (objectives, related specs)
3. **Related high-level specs** - linked specification documents
4. **Implementation files** - all files changed for this task

**Find changed files:**
```bash
# Files changed in this task's commits
git diff --name-only main...HEAD

# Or if on main, find by commit messages with task prefix [XX-YY]
git log --oneline --name-only --grep="\[${PHASE}-${TASK}\]" main | grep -v "^\w"
```

### Step 3: Analyze Implementation

For each changed/created file, evaluate:

#### Code Quality Checklist
- [ ] **SOLID principles** - Single responsibility, proper abstractions
- [ ] **Clean Architecture** - Correct layer placement (Domain → Application → Infrastructure → API)
- [ ] **DDD patterns** - Proper use of entities, value objects, aggregates, domain events
- [ ] **Error handling** - Appropriate exceptions, validation, edge cases
- [ ] **Naming conventions** - Clear, consistent, following project standards
- [ ] **Code duplication** - No unnecessary repetition, proper abstractions
- [ ] **Dependency injection** - Correct service registration and lifetimes

#### .NET Specific Checks
- [ ] **Async/await** - Proper async patterns, no blocking calls
- [ ] **Nullable reference types** - Proper null handling
- [ ] **IDisposable** - Resources properly disposed
- [ ] **EF Core** - Efficient queries, no N+1 problems
- [ ] **Configuration** - Proper use of IOptions, no hardcoded values

### Step 4: Verify Against Specifications

Compare implementation with task scope:
1. Are all scope items implemented?
2. Does implementation match the design in related specs?
3. Are there any deviations that need justification?

### Step 5: Web Research (Best Practices)

Use `WebSearch` and `WebFetch` to verify implementation against official docs and best practices.

**Key research areas based on technologies used:**

| Technology | What to verify |
|------------|----------------|
| YARP | Official configuration patterns, middleware order |
| MassTransit | Consumer patterns, retry policies, outbox |
| EF Core | Query patterns, migrations, concurrency |
| .NET Aspire | Service defaults, health checks, telemetry |
| gRPC | Proto best practices, error handling |
| Rate Limiting | .NET 8+ built-in patterns |

**Search queries to use:**
- `{technology} best practices site:learn.microsoft.com`
- `{technology} official documentation`
- `{pattern} .NET implementation guide`

**IMPORTANT:** Always cite sources when recommending changes based on web research.

### Step 6: Generate Review Report

Structure the output as follows:

```markdown
# Task Review: [Task Name]

## Summary
[1-2 sentence overall assessment]

## Specification Compliance
| Scope Item | Status | Notes |
|------------|--------|-------|
| Item 1 | ✅/⚠️/❌ | ... |

## Strengths 💪
- [What was done well]
- [Good patterns used]
- [Proper architecture decisions]

## Issues Found 🔍

### Critical (must fix)
- [ ] **[Issue title]** in `file:line`
  - Problem: ...
  - Suggestion: ...
  - Reference: [link to docs]

### Improvements (should fix)
- [ ] **[Issue title]** in `file:line`
  - Problem: ...
  - Suggestion: ...

### Nitpicks (optional)
- [ ] ...

## Best Practices Verification
| Area | Status | Source |
|------|--------|--------|
| [Pattern] | ✅/⚠️ | [MS Docs link] |

## Recommendations
1. [Prioritized action items]
2. ...

## Questions for Developer
- [Clarifying questions if any]
```

## Arguments

- `$ARGUMENTS` - Task number or flags
  - `02` - specific task number
  - `--quick` - skip web research, just code review
  - `--trace <correlation-id>` - aggregate logs across services by CorrelationId

## Review Depth Levels

| Flag | Code Analysis | Spec Check | Web Research |
|------|---------------|------------|--------------|
| (default) | Full | Yes | Comprehensive |
| `--quick` | Full | Yes | Skip |

## Log Trace Mode (--trace)

When debugging issues during review, use the `--trace` flag to aggregate logs across all services by CorrelationId.

**Usage:**
```bash
/review-task --trace 228617a4-175a-4384-a8e2-ade916a78c3f
```

**What it does:**
1. Searches all service log files (gateway, order, product, notification, analytics)
2. Finds all entries matching the CorrelationId
3. Sorts entries chronologically across services
4. Displays a unified trace of the request flow

**Log format (Serilog):**
```
[{Timestamp:HH:mm:ss} {Level:u3}] [{CorrelationId}] {Message:lj}
```

Example output:
```
[08:54:42 INF] [228617a4-...] Proxying to http://localhost/api/orders
[08:54:42 INF] [228617a4-...] Creating order for customer...
[08:54:42 INF] [228617a4-...] Reserving stock via gRPC...
[08:54:43 ERR] [228617a4-...] gRPC error in ReserveStock
```

**Tool script:**
```bash
./tools/e2e-test/trace-correlation.sh <correlation-id> [--all-logs] [--json]
```

Options:
- `--all-logs` - Search all log files, not just latest per service
- `--json` - Output as JSON for programmatic use

## Output Example

```
# Task Review: YARP Configuration

## Summary
Solid implementation of YARP reverse proxy with good route configuration.
Minor improvements needed in error handling and health check integration.

## Specification Compliance
| Scope Item | Status | Notes |
|------------|--------|-------|
| Configure YARP routes | ✅ | All routes properly defined |
| Add health checks | ⚠️ | Missing destination health checks |
| Load from config | ✅ | Using appsettings.json correctly |

## Strengths 💪
- Clean separation of route configurations
- Proper use of typed configuration binding
- Good middleware ordering

## Issues Found 🔍

### Critical (must fix)
None

### Improvements (should fix)
- [ ] **Missing destination health checks** in `Program.cs:45`
  - Problem: YARP health probing not configured
  - Suggestion: Add `.LoadFromConfig().AddHealthChecks()`
  - Reference: https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks

### Nitpicks (optional)
- [ ] Consider extracting route names to constants

## Best Practices Verification
| Area | Status | Source |
|------|--------|--------|
| YARP config | ✅ | MS Docs - YARP Configuration |
| Middleware order | ✅ | ASP.NET Core fundamentals |

## Recommendations
1. Add health checks for backend services
2. Consider adding request/response logging middleware
```

## Integration

This skill works with the task workflow:
1. `/start-task XX` - begin working
2. `/commit` - commit changes
3. **`/review-task` - get tech lead feedback before finishing**
4. `/finish-task` - complete after addressing review

## Safety Rules

1. NEVER modify any files - this is a read-only review
2. ALWAYS cite sources for recommendations from web research
3. ALWAYS be constructive - balance criticism with praise
4. ALWAYS prioritize issues (critical vs nice-to-have)
5. If unsure about a pattern, research it before flagging as issue
