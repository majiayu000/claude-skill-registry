---
name: nav-task
description: Manage Navigator task documentation - create implementation plans, archive completed tasks, update task index. Use when user starts new feature, completes work, or says "document this feature".
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Navigator Task Manager Skill

Create and manage task documentation - implementation plans that capture what was built, how, and why.

## When to Invoke

Invoke this skill when the user:
- Says "document this feature", "archive this task"
- Says "create task doc for...", "document what I built"
- Completes a feature and mentions "done", "finished", "complete"
- Starts new feature and says "create implementation plan"

**DO NOT invoke** if:
- User is asking about existing tasks (use Read, not creation)
- Creating SOPs (that's nav-sop skill)
- Updating system docs (different skill)

## Execution Steps

### Step 1: Determine Task ID

**If user provided task ID** (e.g., "TASK-01", "GH-123"):
- Use their ID directly

**If no ID provided**:
- Read `.agent/.nav-config.json` for `task_prefix`
- Check existing tasks: `ls .agent/tasks/*.md`
- Generate next number: `{prefix}-{next-number}`
- Example: Last task is TASK-05, create TASK-06

### Step 2: Determine Action (Create vs Archive)

**Creating new task** (starting feature):
```
User: "Create task doc for OAuth implementation"
→ Action: CREATE
→ Generate empty implementation plan template
```

**Archiving completed task** (feature done):
```
User: "Document this OAuth feature I just built"
→ Action: ARCHIVE
→ Generate implementation plan from conversation
```

### Step 3A: Create New Task (If Starting Feature)

Generate task document from template:

```markdown
# TASK-{XX}: {Feature Name}

**Status**: 🚧 In Progress
**Created**: {YYYY-MM-DD}
**Assignee**: {from PM tool or "Manual"}

---

## Context

**Problem**:
[What problem does this solve?]

**Goal**:
[What are we building?]

**Success Criteria**:
- [ ] [Specific measurable outcome]
- [ ] [Another outcome]

---

## Implementation Plan

### Phase 1: {Name}
**Goal**: [What this phase accomplishes]

**Tasks**:
- [ ] [Specific task]
- [ ] [Another task]

**Files**:
- `path/to/file.ts` - [Purpose]

### Phase 2: {Name}
...

---

## Technical Decisions

| Decision | Options Considered | Chosen | Reasoning |
|----------|-------------------|--------|-----------|
| [What] | [Option A, B, C] | [Chosen] | [Why] |

---

## Dependencies

**Requires**:
- [ ] {prerequisite task or setup}

**Blocks**:
- [ ] {tasks waiting on this}

---

## Notes

[Any additional context, links, references]

---

## Completion Checklist

Before marking complete:
- [ ] Implementation finished
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code reviewed (if team)
- [ ] Deployed/merged

---

**Last Updated**: {YYYY-MM-DD}
```

Save to: `.agent/tasks/TASK-{XX}-{slug}.md`

### Step 3B: Archive Completed Task (If Feature Done)

Generate task document from conversation:

1. **Analyze conversation** (last 30-50 messages):
   - What was built?
   - How was it implemented?
   - What decisions were made?
   - What files were modified?

2. **Generate implementation plan**:

```markdown
# TASK-{XX}: {Feature Name}

**Status**: ✅ Completed
**Created**: {YYYY-MM-DD}
**Completed**: {YYYY-MM-DD}

---

## What Was Built

[1-2 paragraph summary of the feature]

---

## Implementation

### Phase 1: {Actual phase completed}
**Completed**: {Date}

**Changes**:
- Created `src/auth/oauth.ts` - OAuth provider integration
- Modified `src/routes/auth.ts` - Added login/logout endpoints
- Updated `src/config/passport.ts` - Passport configuration

**Key Code**:
```typescript
// Example of key implementation
export const oauthLogin = async (req, res) => {
  // Implementation details
};
```

### Phase 2: {Next phase}
...

---

## Technical Decisions

| Decision | Options | Chosen | Reasoning |
|----------|---------|--------|-----------|
| Auth library | next-auth, passport.js, auth0 | passport.js | Better control over OAuth flow, smaller bundle |
| Token storage | localStorage, cookies, sessionStorage | httpOnly cookies | XSS protection, automatic transmission |
| Session store | memory, Redis, PostgreSQL | Redis | Fast, scalable, separate from DB |

---

## Files Modified

- `src/auth/oauth.ts` (created) - OAuth integration
- `src/routes/auth.ts` (modified) - Added auth endpoints
- `src/config/passport.ts` (created) - Passport setup
- `tests/auth.test.ts` (created) - Auth tests
- `README.md` (updated) - OAuth setup instructions

---

## Challenges & Solutions

**Challenge**: OAuth callback URL mismatch
- **Problem**: Redirects failed in production
- **Solution**: Added environment-specific callback URLs
- **Commit**: abc1234

**Challenge**: Session persistence across restarts
- **Problem**: Users logged out on server restart
- **Solution**: Redis session store
- **Commit**: def5678

---

## Testing

- ✅ Unit tests: `src/auth/*.test.ts` (15 tests, 100% coverage)
- ✅ Integration tests: OAuth flow end-to-end
- ✅ Manual testing: Tested with Google, GitHub providers

---

## Documentation

- ✅ README updated with OAuth setup instructions
- ✅ Environment variables documented in `.env.example`
- ✅ API endpoints documented in `docs/api.md`

---

## Related

**SOPs Created**:
- `.agent/sops/integrations/oauth-setup.md`

**System Docs Updated**:
- `.agent/system/project-architecture.md` (added auth section)

---

**Completed**: {YYYY-MM-DD}
**Implementation Time**: {X hours/days}
```

Save to: `.agent/tasks/TASK-{XX}-{slug}.md`

### Step 3.5: Verify Interpretation (ToM Checkpoint - Archive Mode Only) [EXECUTE]

**IMPORTANT**: This step MUST be executed when archiving tasks (not creating new ones).

**Before committing archive documentation, confirm interpretation with user**.

**Display verification** (only for ARCHIVE action):
```
I extracted this from our session:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What was built:
- {FEATURE_SUMMARY}

Key decisions captured:
- {DECISION_1}: {REASONING_1}
- {DECISION_2}: {REASONING_2}

Files changed: {COUNT} total
- {FILE_1} ({ACTION}: {PURPOSE})
- {FILE_2} ({ACTION}: {PURPOSE})

Challenges solved:
- {CHALLENGE_1}: {SOLUTION_1}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Corrections needed? [Enter to proceed / type corrections]
```

**Always verify for ARCHIVE** because:
- Extracting from conversation is inference-based
- User may have made decisions not explicitly stated
- Some files may have been modified outside conversation
- Ensures accurate historical record

**Skip verification for CREATE** because:
- Template is mostly empty
- User fills in details themselves
- No inference risk

### Step 4: Update Navigator Index

Edit `.agent/DEVELOPMENT-README.md` to add task to index:

```markdown
## Active Tasks

- **TASK-{XX}**: {Feature Name} (Status: In Progress/Completed)
  - File: `.agent/tasks/TASK-{XX}-{slug}.md`
  - Started: {Date}
  - [Completed: {Date}]
```

Keep index organized (active tasks first, completed below).

### Step 5: Update PM Tool (If Configured)

**If PM tool is Linear**:
```typescript
create_comment({
  issueId: "TASK-XX",
  body: "📚 Implementation plan documented: .agent/tasks/TASK-XX-feature.md"
})
```

**If PM tool is GitHub**:
```bash
gh issue comment {ISSUE-NUMBER} -b "📚 Implementation plan: .agent/tasks/TASK-XX-feature.md"
```

**If PM tool is none**:
Skip PM update.

### Step 6: Confirm Success

Show completion message:

```
✅ Task documentation created!

Task: TASK-{XX} - {Feature Name}
File: .agent/tasks/TASK-{XX}-{slug}.md
Size: {X} KB (~{Y} tokens)

📋 Contains:
- Implementation phases
- Technical decisions
- Files modified
- [If archived: Challenges & solutions]
- [If archived: Testing & documentation]

🔗 Navigator index updated
[If PM tool: PM tool comment added]

To reference later:
Read .agent/tasks/TASK-{XX}-{slug}.md
```

## Task Document Template Structure

### For New Tasks (Planning)
1. Context (problem/goal)
2. Implementation plan (phases)
3. Technical decisions (to be made)
4. Dependencies
5. Completion checklist

### For Completed Tasks (Archive)
1. What was built (summary)
2. Implementation (actual phases)
3. Technical decisions (what was chosen)
4. Files modified
5. Challenges & solutions
6. Testing & documentation

## Common Use Cases

### Starting New Feature
```
User: "Create task doc for payments integration"
→ Generates TASK-07-payments.md
→ Empty template for planning
→ User fills in as they work
```

### Completing Feature
```
User: "Document the auth feature I just finished"
→ Analyzes conversation
→ Generates TASK-06-auth.md
→ Complete implementation record
→ Archives for future reference
```

### Mid-Feature Update
```
User: "Update TASK-05 with OAuth decision"
→ Reads existing TASK-05-auth.md
→ Adds to Technical Decisions section
→ Preserves rest of document
```

## Error Handling

**Navigator not initialized**:
```
❌ .agent/tasks/ directory not found

Run /nav:init to set up Navigator structure first.
```

**Task ID already exists (for creation)**:
```
⚠️  TASK-{XX} already exists

Options:
1. Read existing task
2. Use different ID
3. Archive/overwrite existing

Your choice [1-3]:
```

**Insufficient context to archive**:
```
⚠️  Not enough conversation context to generate implementation plan

Consider:
- Provide more details about what was built
- Manually create task doc
- Skip archiving

Continue with template? [y/N]:
```

## Success Criteria

Task documentation is successful when:
- [ ] Task file created in `.agent/tasks/`
- [ ] Filename follows convention: `TASK-{XX}-{slug}.md`
- [ ] Contains all required sections
- [ ] Navigator index updated
- [ ] PM tool updated (if configured)
- [ ] User can reference task later

## Scripts

**generate_task.py**: Create task documentation from conversation
- Input: Conversation history, task ID
- Output: Formatted task markdown

**update_index.py**: Update DEVELOPMENT-README.md task index
- Input: New task info
- Output: Updated index

## Best Practices

**Good task slugs**:
- `oauth-implementation` (descriptive)
- `stripe-payment-flow` (clear purpose)
- `user-profile-page` (specific feature)

**Bad task slugs**:
- `feature` (too vague)
- `fix` (not descriptive)
- `task1` (meaningless)

**When to create task docs**:
- ✅ Starting major feature (> 1 day work)
- ✅ Completing any feature (archive)
- ✅ Complex implementation (capture decisions)
- ❌ Tiny bug fixes (use SOPs instead)
- ❌ Exploratory work (wait until direction clear)

## Notes

Task docs are **living documents**:
- Created when starting feature (template)
- Updated during implementation (decisions)
- Finalized when complete (archive)

They serve as:
- Planning tool (before implementation)
- Progress tracker (during implementation)
- Historical record (after completion)
- Knowledge base (for team/future)

This skill provides same functionality as `/nav:doc feature` command but with natural language invocation.
