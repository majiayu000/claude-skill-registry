---
name: Context Preserver
description: Automatically save and restore development context to minimize cognitive load when resuming work. Use when switching tasks, taking breaks, or returning after interruptions. Captures mental state, file locations, and next steps. Designed for ADHD developers with high context-switching costs.
version: 1.0.0
---

# Context Preserver

**Never lose your place. Resume in 5 minutes. Eliminate "Where was I?" moments.**

## Core Principle

ADHD brains have high context-switching costs and limited working memory. Every interruption means 15-30 minutes of "getting back into it." The solution: Automatically capture and restore mental state so you can resume work in under 5 minutes.

**Key Insight:** The act of saving context is therapeutic - it signals "I can stop safely."

---

## The Context Problem

### Problem 1: High Context-Switching Cost

**Issue:** After breaks, spend 15-30 min remembering what you were doing
**Result:** Lost productivity, frustration, avoidance of breaks

###Problem 2: Working Memory Limits
**Issue:** Can't hold complex state in mind
**Result:** Constant re-reading code, forgetting next steps

### Problem 3: Interruption Anxiety

**Issue:** Fear of losing place prevents taking needed breaks
**Result:** Burnout, health issues, reduced quality

### Problem 4: "Where Was I?" Syndrome

**Issue:** Return to work with no idea what you were doing
**Result:** Thrashing, starting over, wasted time

---

## Phase 1: Automatic Context Capture

### What Gets Saved (Auto-Every 15 Minutes)

**File Context:**

- Current file path
- Line number and function
- Related files (imports, dependencies)
- Git branch

**Mental State:**

- What you were thinking
- What you just finished
- What you're about to do
- Blockers or questions

**Environment:**

- Dev server status
- Open terminals
- Database state
- API keys loaded

**Time Context:**

- When you started
- How long you've been working
- When you plan to stop

### Automated Saves

#### Trigger 1: Every 15 Minutes (Background)

```markdown
[15:30] Auto-save triggered

Context saved:

- File: src/components/login.tsx:42
- Function: handleSubmit()
- Status: Adding API call
- Next: Error handling for 401
- Time working: 45 min

✅ Saved to .adhd/context.json
✅ Micro-commit created (WIP)
```

#### Trigger 2: Before Breaks (Manual Command)

```bash
# You run: ./save-context.sh --break lunch

Context saved for lunch break:
- Current task: Implementing password reset
- Progress: 70% complete
- File: src/auth/reset.ts:67
- Next step: Test email delivery
- Resume command ready: ./resume.sh

✅ Safe to take break!
```

#### Trigger 3: On Claude Session End (Auto)

```markdown
[Session ending]

Preserving your context:

- Saved current task
- Created WIP commit
- Noted next 3 steps
- Logged session progress

Resume anytime: Just start new Claude session
Context will load automatically
```

#### Trigger 4: On Interruption (Auto-Detect)

```markdown
[No activity detected for 10 min]

Looks like you got interrupted!
Auto-saved context:

- Last active: 10 min ago
- Working on: Dashboard layout
- File: src/pages/dashboard.tsx:125
- Next: Add user stats widget

When you return: Context ready to resume
```

---

## Phase 2: Context Structure

### The .adhd/context.json File

```json
{
  "timestamp": "2025-10-22T15:30:00Z",
  "session": {
    "started": "2025-10-22T14:00:00Z",
    "duration_minutes": 90,
    "breaks_taken": 1,
    "focus_sessions": 3
  },
  "files": {
    "current": {
      "path": "src/components/login.tsx",
      "line": 42,
      "column": 12,
      "function": "handleSubmit",
      "content_preview": "async function handleSubmit(e: FormEvent) {"
    },
    "related": ["src/api/auth.ts", "src/types/user.ts"]
  },
  "mental_state": {
    "doing": "Adding API call to /auth/login endpoint",
    "just_finished": "Added email validation",
    "next_steps": [
      "Add fetch call to /auth/login",
      "Handle 401/500 errors",
      "Add loading state to button"
    ],
    "blockers": ["Need to check API error format"],
    "notes": "Using fetch (not axios) per team standard"
  },
  "environment": {
    "branch": "feature/auth-flow",
    "uncommitted_changes": true,
    "dev_server_running": true,
    "last_command": "npm run dev"
  },
  "progress": {
    "current_task": "Build authentication flow",
    "phase": "Phase 2: API Integration",
    "percent_complete": 60,
    "estimated_remaining": "45 minutes"
  }
}
```

---

## Phase 3: Automatic Context Restoration

### Quick Resume (< 5 Minutes)

#### One-Command Resume

```bash
# You run: ./resume.sh

╔══════════════════════════════════════╗
║  Resuming Work Session              ║
║  Last saved: 12:15 PM (1 hour ago) ║
╚══════════════════════════════════════╝

📂 Restoring context...

✅ Opened: src/components/login.tsx
✅ Cursor positioned: Line 42
✅ Dev server started
✅ Git branch: feature/auth-flow

💭 You were:
  - Adding API call to /auth/login
  - Just finished: Email validation
  - Next: Handle 401/500 errors

📊 Progress: 60% complete
⏱️ Estimated remaining: 45 minutes

🎯 Next micro-task: Add fetch call (15 min)

[Opens file at exact line in VS Code]
[Starts dev server]
[Shows mental state notes]

✅ Ready to code! Resume time: 4 minutes
```

### Claude Automatic Resume

When you start new Claude session:

```markdown
You: [start new session]

Claude: Welcome back! I see you were working on authentication flow.

Let me catch you up:

📍 Last Location:
File: src/components/login.tsx:42
Function: handleSubmit()

💭 Mental State (from 1 hour ago):

- You were adding API call to /auth/login
- Email validation is done ✅
- Next: Handle 401/500 errors

📊 Progress: 60% complete (Phase 2/3)

🎯 Quick options:
A) Resume where you left off (add fetch call)
B) See full context (detailed notes)
C) Start something new

What would you like to do?
```

---

## Phase 4: Mental State Capture Techniques

### Capturing "What Were You Thinking?"

#### The 3-Question Method (Auto-Prompted)

Every 30 minutes, Claude asks:

```markdown
[Quick context check - 1 minute]

To help you resume later:

1. What are you working on right now?

   > Adding password reset functionality

2. What's the next small step?

   > Test email delivery locally

3. Any blockers or questions?
   > Need to configure SendGrid API key

✅ Saved! This will help Future You.
```

#### Stream-of-Consciousness Notes

```markdown
## Mental State Notes (Auto-saved)

15:00 - Started password reset feature
15:15 - Generated reset token, stored in DB
15:30 - Building email template now
15:35 - Wondering if I should use SendGrid or Postmark
15:40 - Going with SendGrid (already have account)
15:45 - Configured API key, testing send...
[Break]

Resume thoughts:

- Was about to test email delivery
- SendGrid configured, key in .env
- Next: Trigger reset email from form
```

### Breadcrumb Trail

```markdown
## Breadcrumb Trail (Auto-generated)

14:00 ✅ Created reset-password.tsx
14:15 ✅ Added form with email input
14:30 ✅ Connected to /api/reset-password
14:45 ✅ Generated reset token
15:00 ✅ Stored token in database
15:15 🔄 Building email template ← YOU ARE HERE
15:30 ⬜ Test email delivery
15:45 ⬜ Add reset confirmation page

You're making great progress! 🎉
```

---

## Phase 5: Context-Aware Workflows

### Before-Break Checklist (Auto-Triggered)

```markdown
[You haven't saved context in 45 min]

⏸️ Taking a break soon?

Quick save checklist:

- [ ] Commit current work (WIP okay!)
- [ ] Write next step (one sentence)
- [ ] Note any blockers
- [ ] Close unneeded tabs (reduce clutter)

Takes 2 minutes, saves 20 minutes later!

[Save Context Now] [Remind Me in 15m] [I'm not taking a break]
```

### End-of-Day Ritual (Auto-Prompted at 5pm)

```markdown
[17:00] End of day approaching!

🌙 Let's wrap up for easy tomorrow start:

1. Current Progress:
   Built authentication flow
   Progress: 75% complete
   Status: Working well, needs testing

2. Tomorrow's First Task:
   → Test password reset flow (30 min)
   → File: src/auth/reset.ts
   → Should be quick!

3. Blockers for Tomorrow:
   None! Ready to go.

4. Wins Today:
   ✅ Completed login form
   ✅ Added validation
   ✅ Connected to API
   ✅ Fixed bug #234

5. Mental Dump:
   [Anything else to remember?]
   > Remember to check email error handling

✅ Context saved! Tomorrow You will thank you. 🙏

[Finish Day] [Keep Working]
```

---

## Phase 6: Git Integration

### Automated Micro-Commits

Every context save creates a WIP commit:

```bash
# Auto-runs every 15 min
git add .
git commit -m "WIP: $(cat .adhd/context.json | jq -r '.mental_state.doing') [15:30]"

# Example commits:
git commit -m "WIP: Adding API call to login endpoint [15:30]"
git commit -m "WIP: Testing password reset flow [15:45]"
git commit -m "PAUSE: About to add error handling [16:00]"
```

### Resume from Git History

```bash
# See what you were doing
git log -1 --pretty=%B

# Output:
WIP: Testing password reset flow [15:45]

# Context notes:
- File: src/auth/reset.ts:67
- Next: Add error toast for failed reset
- Blocker: None
```

---

## Phase 7: Interruption Handling

### Types of Interruptions

#### Type 1: Meetings (Scheduled)

```markdown
[14:45] Meeting in 15 minutes

Auto-save triggering:

- Current work committed
- Context snapshot created
- Resume script generated

After meeting: Run ./resume.sh
Estimated resume time: 5 minutes
```

#### Type 2: Urgent Bug (Unplanned)

```markdown
You: "Urgent bug in production, need to switch"

Claude: No problem! Let me save your context first.

✅ Saved: Authentication flow work
✅ Stashed: Uncommitted changes
✅ Switched: To main branch

Work on the bug, I'll help you resume after.

Resume command: ./resume-auth-work.sh
```

#### Type 3: Loss of Focus (ADHD Wander)

```markdown
[You've been browsing docs for 20 min]

💭 Gentle reminder:

You were working on: Password reset form
Current file: src/auth/reset.tsx:45
Next step: Add email input field (5 min)

Research is good, but maybe time to apply?

[Resume Coding] [Continue Research] [Take Break]
```

---

## Phase 8: Advanced Context Features

### Context Sharing

```bash
# Share context with teammate
./export-context.sh

Generated: context-snapshot.md

Send this to teammate for pairing:
- What you're working on
- Current progress
- What you need help with
- Exact file locations
```

### Context History

```markdown
# View past contexts

./context-history.sh

Recent Work Sessions:

1. 2025-10-22 14:00 - Auth flow (90 min) ✅ Completed
2. 2025-10-22 10:30 - Dashboard UI (2 hours) 🔄 In progress
3. 2025-10-21 15:00 - Bug fix #234 (45 min) ✅ Completed

[Load Context] [Delete] [Archive]
```

### Smart Context Suggestions

```markdown
[Starting new session]

Claude: I notice you often work on:

- Authentication (70% of time)
- Dashboard UI (20%)
- Bug fixes (10%)

Would you like to:
A) Resume auth flow (where you left off)
B) Continue dashboard work (60% complete)
C) Check open bugs
D) Start something new

Based on your patterns, auth flow is most likely.
```

---

## Phase 9: Context Patterns

### Pattern 1: Deep Work Session

```markdown
[Session Start]
Auto-save every: 15 minutes
Break reminders: Every 60 minutes
Context snapshots: On demand

[Session End]
Final save includes:

- Total focus time
- Tasks completed
- Progress made
- Tomorrow's start point
```

### Pattern 2: Context-Switching Project

```markdown
Project A → Project B

Auto-stash Project A:

- Commit WIP
- Save context
- Close related tabs

Load Project B:

- Restore last context
- Open relevant files
- Show next task

Switch time: < 5 minutes
```

### Pattern 3: Pair Programming

```markdown
Before pairing:

- Export current context
- Share with partner
- They see exactly what you're doing

After pairing:

- Update context with decisions made
- Log next steps
- Easy solo resume
```

---

## Automation Scripts

### Setup (One-Time)

```bash
cd your-project
mkdir .adhd
cp ~/ai-dev-standards/TEMPLATES/adhd/scripts/* ./
chmod +x .adhd/*.sh

# Scripts installed:
# - save-context.sh (manual save)
# - resume.sh (quick resume)
# - context-history.sh (view history)
# - export-context.sh (share with team)
```

### Daily Usage (All Automatic)

```bash
# Morning: One command start
./resume.sh

# During work: Auto-saves every 15 min
# (runs in background)

# Before break: Quick save
./save-context.sh --break lunch

# After break: One command resume
./resume.sh

# End of day: Auto-prompted at 5pm
# (saves automatically)
```

---

## Anti-Patterns

### ❌ Manual Context Notes

**Bad:** Expecting yourself to manually write notes
**Why:** ADHD brain won't do it consistently
**Good:** Automated saves every 15 min

### ❌ Perfect Documentation

**Bad:** Writing detailed status reports
**Why:** Wastes time, won't be maintained
**Good:** Stream-of-consciousness quick notes

### ❌ Single Context File

**Bad:** Overwriting same context file
**Why:** Loses history, can't go back
**Good:** Timestamped history, can browse past contexts

---

## Success Metrics

You're using this skill well when:

- ✅ Resume time < 5 minutes (from 30 minutes before)
- ✅ Never ask "where was I?"
- ✅ Take breaks without anxiety
- ✅ Context auto-saves (you don't think about it)
- ✅ Easy to switch between projects

---

## Related Skills

- **task-breakdown-specialist** - Breaks down next steps
- **focus-session-manager** - Manages work sessions
- **adhd-workflow-architect** - Designs automated workflows

---

**Save your place. Eliminate anxiety. Resume in 5 minutes.** 💾
