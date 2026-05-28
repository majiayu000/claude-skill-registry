---
name: session-logger
description: Logs development sessions in real-time to track decisions and issues.
---

# Session Logger Skill

> **Purpose**: Record development sessions in real time to track decisions and trial/error
> **When to log**: work start, agent switch, decisions, issues, work completion
> **Output**: `{tasksRoot}/{feature-name}/session-logs/day-YYYY-MM-DD.md`

---

## Goals

### Problems
- **2025-12-19 session review**: decision process not recorded, rework cause unclear
- Context switches require reconstructing work (time waste)
- No real-time workflow tracking

### Solution
- Auto session logging during work
- Timeline-based tracking
- Structured records for decisions/issues

---

## Logging moments (auto triggers)

### 1. At work start
```markdown
## [09:00] Work started

### Request
- User message: "Implement batch management"
- Branch: feature/batch-management
- Existing context.md: none

### Initial analysis
- Task type: feature (new)
- Complexity: complex (estimated 8 files)
- Phase: planning (needs plan)
```

### 2. On agent switch
```markdown
## [09:15] Requirements Analyzer -> Context Builder

### Outputs
- Preliminary agreement created
- Key changes: single date input, remove batch execution time
- Uncertainty: none (all clarified)

### Next step
- Call Context Builder Agent
- Estimated plan time: 10m
```

### 3. On decision
```markdown
## [09:20] Decision: Use API proxy pattern

### Decision
- Client -> Next.js API Routes -> backend
- Direct calls are prohibited (CLAUDE.md rule)

### Reason
- Auth token must be handled server-side
- Activity log headers added automatically
- Stronger security

### Alternatives (considered but rejected)
- Direct client call: security risk
- Browser cookie: CORS issues
```

### 4. On issue
```markdown
## [10:15] Issue: type error

### Problem
- `ExecuteBatchApiResponse` does not recognize snake_case fields
- TypeScript error: Property 'job_execution_id' does not exist

### Cause
- Missing backend response type definition
- No camelCase conversion logic

### Fix
- Add raw response type in `_requests/types.ts`
- Split conversion logic into `mapResponse` function
- Time spent: 10m

### Prevention
- Define API response types first
- Standardize snake_case -> camelCase conversion
```

### 5. On completion
```markdown
## [11:30] Work completed

### Outputs
- Commits: 2 (7b0072e Mock, c07d9b6 API)
- New files: 8
- Docs: context.md, session-log.md

### Verification
- OK typecheck
- OK build
- OK lint

### Remaining work
- [ ] Manual testing
- [ ] Error case handling
```

---

## Session log structure

### Base template

```markdown
# {YYYY-MM-DD} {feature-name} implementation session

## Session metadata
- Start time: {HH:MM}
- End time: {HH:MM} (omit if in progress)
- Main work: {summary}
- Branch: {git branch}
- Owner: {user name}

## Timeline

### [HH:MM] Event title
- ...

### [HH:MM] Event title
- ...

## Decision log

| Time | Decision | Reason | Alternative |
|------|----------|--------|-------------|
| 09:20 | Use API proxy | Security | Direct call (rejected) |

## Issue log

### Issue #1: {title}
- **Found at**: HH:MM
- **Problem**: ...
- **Cause**: ...
- **Fix**: ...
- **Time spent**: N minutes
- **Prevention**: ...

## Blocking/Waiting

| Start | End | Reason | Impact |
|-------|-----|--------|--------|
| 09:20 | 09:25 | Waiting for API spec | 5m wait |

## Retrospective notes

### What went well
- 0% rework due to preliminary agreement

### What to improve
- Request API spec draft earlier

### Lessons learned
- Need standardized snake_case -> camelCase conversion
```

---

## How to use

### Manual trigger (user)

```
session-logger start: implement batch management
```

-> `{tasksRoot}/batch-management/session-logs/day-2025-12-20.md` created

### Auto triggers (system)

1. **Work start**: user message received -> create session log
2. **Agent switch**: agent called -> add timeline entry
3. **Decision**: important choice -> add decision log
4. **Issue**: error/problem -> add issue log
5. **Completion**: final outputs -> record completion

---

## Output example

### Actual session log (2025-12-20)

```markdown
# 2025-12-20 batch management implementation session

## Session metadata
- Start time: 09:00
- End time: 11:30
- Main work: implement batch management
- Branch: feature/batch-management
- Owner: Moon

## Timeline

### [09:00] Work started
- User request: "Implement batch management"
- Moonshot Agent analysis: feature, complex, planning phase
- Uncertainties: UI spec version, API spec draft

### [09:05] User response (clarified requirements)
- UI spec: v3 (confirmed 2025-12-18)
- API spec: POST /api/admin/shelf/product/batch-executions
- Date input: single date (yyyy-mm-dd)

### [09:10] Requirements Analyzer complete
- Agreement created: .claude/docs/agreements/batch-management.md
- Key changes: single date input, remove batch execution time
- Next: Context Builder

### [09:20] Context Builder complete
- context.md created: {tasksRoot}/batch-management-context.md
- Target files: 8 new, 2 modified
- Estimated time: 2.5 hours

### [09:45] Implementation Phase 1 complete (Mock)
- Type definitions, mock data, UI components
- commit 7b0072e: batch management first commit
- Verification: typecheck OK, build OK

### [10:30] Implementation Phase 2 complete (API)
- API routes, fetch functions, data mapping
- commit c07d9b6: batch management API applied
- Verification: API call OK

### [11:00] Verification complete
- typecheck OK, build OK, lint OK
- Activity log headers confirmed

### [11:30] Documentation complete
- context.md final update
- session-log.md created
- flow-report.md created

## Decision log

| Time | Decision | Reason | Alternative |
|------|----------|--------|-------------|
| 09:10 | Single date input | UI spec v3 | Date range (v2, rejected) |
| 09:20 | Use API proxy | CLAUDE.md rule | Direct call (forbidden) |
| 10:00 | Mock first | Wait for API spec | Implement after API spec |

## Issue log

### Issue #1: Type error (snake_case not converted)
- **Found at**: 10:15
- **Problem**: ExecuteBatchApiResponse missing job_execution_id
- **Cause**: snake_case -> camelCase conversion missing
- **Fix**: add mapResponse function, split types
- **Time spent**: 10m
- **Prevention**: define API response types first

## Blocking/Waiting

| Start | End | Reason | Impact |
|-------|-----|--------|--------|
| 09:20 | 09:25 | API spec confirmation (waiting on user) | 5m |

## Retrospective notes

### What went well
- 0% rework thanks to preliminary agreement
- Early error discovery via step-by-step verification
- Clear timeline makes tracking easy

### What to improve
- Request API spec draft earlier
- Define snake_case conversion standards earlier

### Lessons learned
- 30m on requirements clarity -> saved 4h (ROI 800%)
- Real-time session logging preserves decision context
```

---

## Usage scenarios

### Scenario 1: Work across multiple days

**Day 1 (Mock implementation)**
```markdown
# 2025-12-20 batch management implementation session (Day 1)

## [16:00] Work paused (waiting on API)
- Phase 1 complete: mock-based UI
- Phase 2 pending: API spec confirmation
- Next: API integration (tomorrow)
```

**Day 2 (API integration)**
```markdown
# 2025-12-21 batch management implementation session (Day 2)

## [09:00] Work resumed
- Day 1 status: Mock complete (commit 7b0072e)
- Today: API integration
- pending-questions.md check: none (API spec confirmed)

## [09:30] Start API integration
- Implement API routes...
```

### Scenario 2: Issue tracking

```markdown
## Issue log

### Issue #1: Date format mismatch
- **Found at**: 10:20
- **Problem**: backend expects yyyyMMdd, UI uses yyyy-mm-dd
- **Cause**: missing date format conversion
- **Fix**: add toApiDate, formatApiDate
- **Time spent**: 15m
- **Prevention**: standardize date format utilities

### Issue #2: Activity log header missing
- **Found at**: 11:00
- **Problem**: fetchCount includes activity log headers
- **Cause**: CLAUDE.md rule not followed (count excludes headers)
- **Fix**: remove headers
- **Time spent**: 5m
- **Prevention**: re-check CLAUDE.md activity log section
```

---

## Related agents/skills

### Inputs (consumed)
- Moonshot Agent: task type, complexity, phase decision
- Requirements Analyzer: preliminary agreement, question list
- Context Builder: implementation plan, checkpoints
- Implementation Agent: commit messages, changed files
- Verification Agent: verification results

### Outputs (provided)
- Documentation Agent: session log -> flow report
- Efficiency Tracker: timeline -> time allocation analysis
- User: real-time progress status

---

## File structure

```
{tasksRoot}/
└── {feature-name}/
    `-- session-logs/
        |-- day-2025-12-20.md  # Day 1
        |-- day-2025-12-21.md  # Day 2
        `-- day-2025-12-22.md  # Day 3
```

---

## Tips

### 1. Auto-create at work start
- First user message -> auto-create session log
- Feature name auto-extracted (e.g., "batch management" -> `batch-management`)

### 2. Real-time updates
- Add timeline entry on each agent switch
- Record decisions/issues in structured format

### 3. Review at end of day
- Write retrospective notes
- Update pending-questions.md
- WIP commit (e.g., `chore: wip mock ready for api`)

### 4. Resume next day
- Review previous session log
- Resume from the last timeline entry
- Resolve pending-questions first

### 5. Token limit awareness and session handoff
- **Per `.claude/docs/guidelines/document-memory-policy.md`**: Keep daily logs under 5000 tokens
- If exceeding limit, start a new day file early
- Archive old session logs if needed
- **Long session handling**: When context grows too large, create `HANDOFF.md` → `/clear` for new session (see section below)

---

## 🔄 Session Handoff (HANDOFF.md)

### When to use?
- When conversation context window is over 80% full
- When complex work spans multiple stages
- When response quality degrades due to token limits
- When work needs to be handed off to the next agent (or new session)

### Trigger prompt example

```
"Summarize the current work state into HANDOFF.md. Explain what you tried, 
what worked, what didn't work, so that the next agent with fresh context 
can just load that file and continue the work."
```

### HANDOFF.md template

```markdown
# {Task Name} - Handoff Document

## Goal
{Final goal and specific current objectives}

Example:
- Reduce Claude Code's system prompt by ~45% (currently at 11%, need ~34% more)

## Current Progress

### What's Been Done
- {Completed work 1}
- {Completed work 2}
- {Completed work 3}

### What Worked
- {Effective approach 1}
- {Effective approach 2}

### What Didn't Work
- {Failed approach 1} (reason: {why it failed})
- {Failed approach 2} (reason: {why it failed})

## Next Steps
1. {Next task 1}
2. {Next task 2}
3. {Next task 3}

## Important Context
- Related files: {key file paths}
- Branch: {current branch}
- Last commit: {commit hash}
- Notes: {important things the new session should know}
```

### Real HANDOFF.md example

```markdown
# System Prompt Slimming - Handoff Document

## Goal
Reduce Claude Code's system prompt by ~45% (currently at 11%, need ~34% more).

## Current Progress

### What's Been Done
- Removed verbose examples from tool descriptions
- Shortened permission explanations
- Consolidated redundant instructions

### What Worked
- Regex-based pattern matching for finding repetitive text
- Testing each change individually before committing

### What Didn't Work
- Removing safety warnings (caused unexpected behavior)
- Over-aggressive minification (broke JSON parsing)

## Next Steps
1. Target the MCP server descriptions (estimated 2k tokens)
2. Simplify the hooks documentation
3. Test thoroughly after each change
```

### Handoff workflow

```
1. Detect session is getting long
   ↓
2. Request HANDOFF.md creation
   ↓
3. Save to {tasksRoot}/{feature-name}/HANDOFF.md
   ↓
4. Run /clear to reset session
   ↓
5. Load HANDOFF.md in new session
   ↓
6. Continue the work
```

### New session start prompt example

```
"Read {tasksRoot}/{feature-name}/HANDOFF.md and continue the work."
```

### File location

```
{tasksRoot}/
└── {feature-name}/
    ├── HANDOFF.md           # Session handoff document
    └── session-logs/
        ├── day-2025-12-20.md
        └── day-2025-12-21.md
```

---

## Expected impact

### Qualitative impact
1. **Preserve decision rationale**: record why choices were made
2. **Track trial and error**: prevent repeating the same mistakes
3. **Visible workflow**: understand progress in real time
4. **Easy context switching**: reduce reconstruction time

### Quantitative impact
- **Context switch time**: 30m -> 5m (83% reduction)
- **Issue recurrence**: 0% repeated issues
- **Retrospective quality**: improved via structured data

---

**Enabling this skill records all work automatically.**

---

## 🧠 Memory Integration (Optional)

> This section is only active when MCP Memory is configured in `settings.local.json`.

### When to Save

| Event | Key Pattern | Example |
|-------|-------------|---------|
| Major decision | `decision:{feature}:{topic}` | API pattern, architecture choice |
| Work completed | `progress:{feature}` | "Phase 1 complete, Mock ready" |
| Issue resolved | `solution:{issue-type}` | snake_case conversion method |

### Save Format

```typescript
mcp__memory__save({
  key: "decision:{feature-name}:api-pattern",
  value: JSON.stringify({
    decision: "Use proxy pattern",
    reason: "Security and auth token handling",
    date: "YYYY-MM-DD",
    relatedFiles: ["src/api/routes.ts"]
  })
})
```

### When to Load

- At session start via pre-flight-check
- When working on related feature
- After `/clear` to restore context

