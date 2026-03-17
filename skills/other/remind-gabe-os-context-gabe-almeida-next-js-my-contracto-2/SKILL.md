---
name: remind-gabe-os-context
description: Proactively remind about Gabe-OS workflows when context may have been lost, especially after /compact operations. Prevent manual implementation by checking for existing specs first.
---

# Gabe-OS Context Awareness Skill

**PURPOSE: Prevent loss of Gabe-OS workflow awareness, especially after context-clearing operations like `/compact`.**

## When to Activate

This skill should activate in these situations:

### 1. At Session Start (High Priority)

If this is the beginning of a conversation:
- Check if `@gabe-os/specs/` directory exists
- If yes, remind about checking for active specs
- Suggest running `/gabe-os/check-context`

### 2. Before Manual Implementation (Critical)

**ALWAYS activate before:**
- Creating new feature files
- Writing implementation code
- Making structural changes to codebase
- Starting any development work

**Check first:**
```bash
# Does specs directory exist?
ls @gabe-os/specs/ 2>/dev/null

# Are there active specs?
ls @gabe-os/specs/*/tasks.md 2>/dev/null
```

If specs exist → **STOP and remind about workflows!**

### 3. When User Requests Implementation (Critical)

If user says things like:
- "Implement [feature]"
- "Add [functionality]"
- "Create [component/file]"
- "Build [system]"
- "Write [code]"

**Before proceeding:**
1. Check for existing specs
2. Ask: "Should I use /gabe-os/implement-spec or create new spec?"
3. Don't implement manually without explicit override

### 4. Likely Post-Compact Indicators (Medium Priority)

Detect potential context loss when:
- User asks basic questions about project state
- User requests status updates
- Conversation seems to start mid-task
- User mentions being "back" or "continuing"

## Reminder Template

When activated, display this reminder:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 GABE-OS WORKFLOW CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Before I proceed, let me verify the current state...

[CHECK RESULTS]

✅ Gabe-OS is installed
✅ Found [X] active specs in @gabe-os/specs/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 RECOMMENDED APPROACH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Since active specs exist, I should:

✅ Use /gabe-os/continue-spec to resume existing work
✅ Use /gabe-os/implement-spec for spec-based implementation
✅ Let the implementer agent handle actual coding
✅ Let quality gates enforce standards

❌ NOT implement code manually
❌ NOT skip the spec workflow
❌ NOT bypass quality audits

Would you like me to:
[1] Check full context with /gabe-os/check-context
[2] Continue with existing spec using /gabe-os/continue-spec
[3] View all specs with /gabe-os/main-menu
[4] Proceed with manual implementation anyway (override)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Check Sequence

Perform these checks in order:

### Step 1: Check Installation
```bash
[ -f "gabe-os/config.yml" ] && [ -d ".claude/agents/gabe-os/" ]
```

If false → Gabe-OS not installed, no reminder needed.

### Step 2: Check for Specs
```bash
ls @gabe-os/specs/ 2>/dev/null
```

If no specs found → Safe to proceed, but still mention workflows.

### Step 3: Check Spec Status
```bash
# Count specs
spec_count=$(ls -d @gabe-os/specs/*/ 2>/dev/null | wc -l)

# Check for active (non-complete) specs
active_specs=$(grep -l "\[ \]" @gabe-os/specs/*/tasks.md 2>/dev/null | wc -l)
```

If active_specs > 0 → **HIGH PRIORITY REMINDER!**

### Step 4: Show Context
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 CURRENT STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Gabe-OS: Installed
📁 Specs: [X] total, [Y] active

Active Specs:
  🔄 [Spec 1 name] - [XX]% complete
  🔄 [Spec 2 name] - [XX]% complete

⚠️ IMPORTANT: Use /gabe-os/ commands for these specs!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Response to Common Scenarios

### Scenario A: User Asks to Implement Feature

**User:** "Add user authentication to the app"

**Response:**
```markdown
Before I start, let me check if there's an existing spec for this...

[Checks @gabe-os/specs/]

I found an existing spec: `@gabe-os/specs/2025-11-04-user-authentication/`

Should I:
[1] Resume this spec with /gabe-os/continue-spec
[2] Create a new spec if this is different
[3] View the existing spec details

(I'll use the Gabe-OS workflow, not manual implementation)
```

### Scenario B: User Says "Continue Implementation"

**User:** "Continue implementing that feature"

**Response:**
```markdown
🔍 Checking for active specs...

Found [X] in-progress specs. Which one should I continue?

[List specs with status]

Or run /gabe-os/check-context to see full details.
```

### Scenario C: Fresh Session Start

**User:** [Starts new session]

**Response:**
```markdown
[Silently check for specs]

[IF SPECS EXIST:]
🔍 I see you have [X] active specs. Would you like to:
- /gabe-os/check-context - See current state
- /gabe-os/continue-spec - Resume work
- /gabe-os/main-menu - View dashboard

[IF NO SPECS:]
[Proceed normally, no reminder needed]
```

## Critical Rules

### DO:
- ✅ Check for specs BEFORE any implementation
- ✅ Suggest /gabe-os/check-context when uncertain
- ✅ Remind about workflows before manual work
- ✅ Show current spec status when available
- ✅ Offer to use proper commands

### DON'T:
- ❌ Implement manually without checking for specs
- ❌ Skip workflow reminders to "save time"
- ❌ Assume no specs exist without checking
- ❌ Proceed without user confirmation when specs exist
- ❌ Forget about quality gates and agents

## Integration Points

This skill works with:
- **/gabe-os/check-context** - Full state verification
- **/gabe-os/continue-spec** - Resume existing work
- **/gabe-os/implement-spec** - Spec-based implementation
- **/gabe-os/main-menu** - Visual dashboard
- **implementer agent** - Actual implementation work
- **code-quality-auditor** - Quality enforcement

## Priority Levels

**CRITICAL (Block immediately):**
- User requests implementation AND specs exist
- About to write code when specs directory exists
- Manual file creation when implementer should do it

**HIGH (Strongly remind):**
- Session start with active specs
- User mentions "continuing" work
- Context loss indicators detected

**MEDIUM (Gentle reminder):**
- Before any new feature work
- When workflow commands haven't been used
- After long periods of inactivity

**LOW (Background check):**
- Periodic validation during conversation
- Before major operations

## Activation Pattern

```
IF (user_requests_implementation OR about_to_write_code OR session_start):
    CHECK for specs in @gabe-os/specs/

    IF specs_exist:
        IF active_specs > 0:
            DISPLAY critical_reminder WITH spec_status
            OFFER workflow_options
            WAIT for user_choice
        ELSE:
            MENTION workflows_available
    ELSE:
        PROCEED normally
```

## Success Metrics

This skill is successful when:
- ✅ No manual implementation when specs exist
- ✅ All work goes through implementer agent
- ✅ Quality gates are never bypassed
- ✅ User is always aware of active specs
- ✅ Workflows are followed consistently

## Failure Indicators

Watch for these anti-patterns:
- ❌ Writing code directly in chat
- ❌ Creating files without implementer agent
- ❌ Skipping quality audits
- ❌ Forgetting about existing specs
- ❌ Breaking spec → implement → verify flow

When detected, **immediately activate this skill!**
