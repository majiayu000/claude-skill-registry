---
name: af-manage-work-state
description: Manage work state, Linear issues, and task context across session boundaries. Use when updating current-task.md, tracking phase progress, logging decisions, or recovering from context compaction.

# AgentFlow documentation fields
title: Work Management Expertise
created: 2025-10-29
updated: 2026-03-09
last_checked: 2026-03-09
tags: [skill, expertise, work-management, linear, tracking, session, compaction]
parent: ../README.md
related:
  - ../../docs/guides/work-management.md
---

# Work Management Expertise

## When to Use This Skill

Load this skill when you need to:
- Start or resume work on a task
- Manage work state across sessions/compaction
- Create and manage Linear issues
- Transition issues through AgentFlow phases
- Recover context after compaction
- Generate project reports and metrics

**Common triggers**:
- Session start (hook reminds you)
- Pre-compaction (hook reminds you)
- Starting new work (`/task:start`)
- Resuming work (`/task:continue`)
- Completing work (`/task:complete`)
- Discovery/Refinement/Delivery phase transitions

## Quick Reference

### Work State Assets

| Asset | Location | Purpose | Survives |
|-------|----------|---------|----------|
| **current-task.md** | `.claude/work/` | Project-level task state, Linear link | Everything (git) |
| **Plan files** | `~/.claude/plans/` | Detailed implementation steps | Compaction ✅ |
| **Todos** | `~/.claude/todos/` | Real-time session tracking | Compaction ✅ |
| **Linear issue** | Linear API | Source of truth for work items | External ✅ |

### Hooks

| Hook | When | Action |
|------|------|--------|
| **SessionStart** | Session begins/resumes | Reminds to read current-task.md |
| **PreCompact** | Before compaction | Reminds to update current-task.md |
| **git-commit-reminder** | git commit | Quality checklist (tests, docs) |

### Linear States

```
Discovered → Refining → Approved → In Progress → In Review → Dev → Test → Live
    │           │          │             │            │         │      │      │
 backlog     started   unstarted      started      started   ←── completed ──→
```

**Phase mapping:**

| Status | Type | AgentFlow Phase |
|--------|------|-----------------|
| **Discovered** | backlog | Discovery |
| **Refining** | started | Refinement |
| **Approved** | unstarted | Refinement complete, ready for delivery |
| **In Progress** | started | Delivery |
| **In Review** | started | Delivery (PR created) |
| **Dev/Test/Live** | completed | Deployed |

---

## Part 1: Work State Management

### Work Management Lifecycle

#### 1. Starting Work

**Command:** `/task:start <LINEAR-ID>`

**Actions:**
1. Fetch Linear issue details
2. Create/update `.claude/work/current-task.md`
3. Update Linear status → "In Progress"
4. Load any existing plan file reference

#### 2. During Work

**TodoWrite** tracks real-time progress (survives compaction).

**Plan files** capture detailed implementation steps:
- Created via plan mode
- Stored at `~/.claude/plans/[random-name].md`
- Reference stored in current-task.md

**current-task.md** maintains project-level state:
- Linear issue reference
- Plan file path(s)
- Progress summary
- Next steps

#### 3. Compaction Recovery

**PreCompact hook** reminds you to update current-task.md.

**After compaction:**
1. Read current-task.md for Linear context and plan references
2. Read plan file if referenced
3. Check TodoWrite for in-session progress
4. Continue work

#### 4. Completing Work

**Command:** `/task:complete`

**Precondition:** Work has been deployed (Linear status should already be "Live" via CI/CD automation).

**Actions:**
1. Verify Linear status is "Live" (or at minimum "Dev")
2. Add completion comment summarizing implementation
3. Clear current-task.md for next task

**Note:** `/task:complete` is for cleanup after deployment, not status changes. The status flow (In Review → Dev → Test → Live) is handled by CI/CD webhooks.

### current-task.md Template

```yaml
---
linear_issue: JCN-4
linear_url: https://linear.app/juncan/issue/JCN-4
status: in_progress
started: 2026-01-04
---

## Task
[Brief description from Linear]

## Plans
- 2026-01-04: ~/.claude/plans/validated-swinging-walrus.md (current)
- 2026-01-03: ~/.claude/plans/earlier-plan.md (superseded)

## Progress
- [x] Phase 1: Code fix
- [x] Phase 2: Dev environment
- [ ] Phase 3: Test environment

## Next Steps
- Delete staging branch in Amplify
- Verify deployment

## Notes
- SES production approval pending (24-48hrs)
```

### Work State Rules

1. **current-task.md is the project-level source of truth** - Always keep it updated
2. **Plan files are session artifacts** - Reference them in current-task.md
3. **TodoWrite is real-time tracking** - Complements, doesn't replace current-task.md
4. **Update before compaction** - PreCompact hook reminds you
5. **Read after session start** - SessionStart hook reminds you
6. **Record plan files** - Add path to current-task.md when created

---

## Part 2: Linear Operations

### Tool Selection

1. **`linearis` CLI** (recommended) - Simple, handles state name→UUID automatically
2. **GraphQL API** - For operations the CLI doesn't support
3. **Linear MCP** - Avoid, currently flaky

**CLI limitations:** Cannot create teams, workflow states, or issue relations. Use GraphQL for those.

**Reference:** Load `af-query-linear-api` skill for GraphQL operations

### Prerequisites

- `LINEAR_API_KEY` environment variable set

### Quick Operations (linearis CLI)

**Read issue:**
```bash
linearis issues read AF-123
linearis issues read AF-123 | jq '.title, .state.name'
```

**Update issue state:**
```bash
linearis issues update AF-123 --state "In Progress"
linearis issues update AF-123 --state "Waiting for Feedback"
```

**Add comment:**
```bash
linearis issues comment AF-123 "Progress update: completed implementation"
```

**Search issues:**
```bash
linearis issues search "team:AF state:\"In Progress\""
```

**Create issue (ALWAYS use team UUID, not abbreviation - abbreviations route to wrong team):**
```bash
# Look up UUID first
project-registry agentflow linear.team_id
# Then use it
linearis issues create --team "79b48ab6-d677-4f3a-8228-86e30ce923a3" "[Feature] New capability" -d "Details..."
```

For GraphQL API (advanced operations like history, relations), see `af-query-linear-api`.

### Linear Rules

7. **Every AgentFlow feature MUST have a Linear issue** - Traceability required
8. **Issue titles MUST be descriptive** - "[Capability] - [Brief description]"
9. **All commits MUST reference Linear ID** - "JCN-4: [commit message]"
10. **Never skip states** - Follow workflow sequence
11. **Update status regularly** - At least daily for In Progress issues
12. **Link artifacts to issues** - Feature files, Storybook, API docs
13. **BDD sub-tasks use type labels** - `type:bdd`, `type:visual`, `type:api`

### Sub-Issue Creation Policy

**Default to checklists over sub-issues.** Most work should be tracked as a checklist in the parent issue description, not as separate sub-issues.

**Exempt sub-issues (always created):**
- **[Behaviour]** sub-issues — part of BDD workflow, exempt from size rules
- **[UX]** sub-issues — part of BDD workflow, exempt from size rules

**All other sub-issues must pass BOTH gates:**

1. **Size gate** — only create sub-issues when the parent issue exceeds **2 days (12 hours)** of human effort. If the parent is ≤2 days, keep everything as a checklist.
2. **Sub-issue minimum** — each sub-issue must represent at least **2 days (12 hours)** of work. Smaller pieces stay as checklist items.
3. **Independence test** — even if the size gate is met, only create a sub-issue if the work is genuinely independent (different person, different phase, or can be delivered/tested separately).

**When in doubt, use a checklist.** A parent issue with a clear checklist is better than a parent with five 1-point sub-issues.

### Issue Description vs Comments

**Description** = current state of truth. Overwrite, don't append. Always reflects "now."
**Comments** = chronological decision log. Append-only, phase-tagged.

| Aspect | Description | Comments |
|--------|-------------|----------|
| Update mode | Overwrite (replace with current state) | Append-only (never edit/delete) |
| Purpose | What this issue IS right now | How we got here |
| Format | Clean snapshot | Phase-tagged: `[Discovery]`, `[Refinement]`, `[Delivery]` |

**Agent rules for reading:**
1. Read description first (current truth)
2. Read ALL comments (chronological decision log)
3. Description wins if it conflicts with comments
4. Pay attention to phase-tagged comments matching current phase
5. Read oldest-first to understand evolution, but latest + description = truth
6. Never delete old comments — they're the historical record

**Agent rules for writing:**
- Description: Update to reflect current state (overwrite entire description)
- Comments: Append with phase tag, e.g. `[Delivery] PR #42 created: <link>`

### Labels as Approval Signals

Labels signal human decisions for environment progression:

| Label | Added by | Meaning |
|-------|----------|---------|
| `approved:test` | QA or PM | "Dev is validated, deploy to test" |
| `approved:live` | PM | "Test is validated, deploy to production" |
| `approval:bdd-pending` | Orchestrator | BDD scenarios being written |
| `approval:bdd-approved` | Orchestrator | BDD scenarios approved |
| `approval:ux-pending` | Orchestrator | UX design being created |
| `approval:ux-approved` | Orchestrator | UX design approved |

**Environment labels trigger agent actions:**
1. Human adds `approved:test` → agent wakes, prepares PR (develop → test)
2. Agent asks on Zulip: "PR ready, shall I merge?"
3. Human confirms → agent merges → status → "Test" → label removed
4. Agent posts Linear comment: `[Delivery] Deployed to test environment`

### Workflow: Feature Issue Creation (Discovery)

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation CreateIssue($title: String!, $teamId: String!, $description: String) { issueCreate(input: { title: $title, teamId: $teamId, description: $description }) { success issue { identifier url } } }",
    "variables": {
      "title": "[Capability] - Feature Description",
      "teamId": "TEAM_UUID",
      "description": "## Business Context\n[Why this feature matters]\n\n## Acceptance Criteria\n- Criterion 1\n- Criterion 2"
    }
  }' | jq
```

### Workflow: Transitioning to Refinement (Refining)

```bash
# Move to Refining (get state UUID first from team's workflow states)
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"REFINING_STATE_UUID\" }) { success } }"}'
```

### Workflow: Approving Refinement

```bash
# Human approves - move to Approved
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"APPROVED_STATE_UUID\" }) { success } }"}'

# Add approval comment
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"AF-123\", body: \"Refinement approved\\n- Mini-PRD: Complete\\n- BDD scenarios: Covered\\n- Ready for scheduling\" }) { success } }"}'
```

### Workflow: Starting Delivery (In Progress)

```bash
# Move to In Progress
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"IN_PROGRESS_STATE_UUID\" }) { success } }"}'

# Update progress regularly
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"AF-123\", body: \"Progress update:\\n- Feature logic implemented\\n- Integration tests in progress\" }) { success } }"}'
```

### Workflow: Code Review (In Review)

```bash
# PR created - move to In Review
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"IN_REVIEW_STATE_UUID\" }) { success } }"}'

curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"AF-123\", body: \"PR created: https://github.com/...\" }) { success } }"}'
```

### Workflow: Deployment (Dev → Test → Live)

```bash
# After merge to develop
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"DEV_STATE_UUID\" }) { success } }"}'

# After promotion to test
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"TEST_STATE_UUID\" }) { success } }"}'

# After production deployment
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-123\", input: { stateId: \"LIVE_STATE_UUID\" }) { success } }"}'
```

**Note:** For state UUIDs, query your team's workflow states first. See `af-query-linear-api` for helper scripts.

---

## Common Patterns

### Starting Fresh Work

```
1. /task:start JCN-4
2. Review Linear issue details
3. Enter plan mode if complex
4. Record plan file path in current-task.md
5. Begin implementation with TodoWrite tracking
```

### Resuming After Break

```
1. SessionStart hook reminds about current-task.md
2. Read .claude/work/current-task.md
3. Read referenced plan file (if any)
4. Check TodoWrite for last session progress
5. Continue from "Next Steps"
```

### Recovering After Compaction

```
1. Context compressed - details lost
2. Read .claude/work/current-task.md (survives - on disk)
3. Read plan file (survives - on disk)
4. Check TodoWrite (survives - on disk)
5. Restore context and continue
```

---

## Common Pitfalls

### Work State Pitfalls

1. **Not Updating current-task.md**
   - Problem: Context lost after compaction/session restart
   - Solution: Update progress and next steps regularly

2. **Orphaned Plan Files**
   - Problem: Plan file exists but not referenced in current-task.md
   - Solution: Always record plan file path when created

3. **Ignoring Hooks**
   - Problem: Miss context recovery reminders
   - Solution: Act on SessionStart and PreCompact hook messages

### Linear Pitfalls

4. **Skipping State Transitions**
   - Problem: Breaks workflow tracking
   - Solution: Follow state sequence strictly

5. **Vague Issue Titles**
   - Problem: Unclear, hard to search
   - Solution: Use "[Capability] - [Description]" pattern

6. **Not Linking Commits**
   - Problem: Lost traceability
   - Solution: All commits reference Linear issue ID

---

## Essential Reading

**For complete workflows and examples:**
- [Work Management Guide](../../docs/guides/work-management.md)

**For AgentFlow phases:**
- Load `af-discover-scope` for Discovery patterns
- Load `af-refine-specifications` for Refinement patterns
- Load `af-deliver-features` for Delivery patterns

**Official Linear documentation:**
- [Linear API](https://developers.linear.app/)

---

**Remember:**
1. current-task.md bridges sessions and compaction
2. Plan files and Todos survive compaction (on disk)
3. Hooks remind you to save/restore context
4. Linear is the external source of truth
5. Always update before compaction, always read after session start
6. Never skip Linear state transitions
