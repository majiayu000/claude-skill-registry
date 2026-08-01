---
name: session-recovery
description: Seamlessly recover from session interruptions, crashes, or context switches
  without losing progress.
---

# 🔄 Session Recovery Skill

---
name: session-recovery
description: Recover context and continue work after session interruptions or restarts
---

## 🎯 Purpose

Seamlessly recover from session interruptions, crashes, or context switches without losing progress.

## 📋 When to Use

- Starting a new conversation
- After IDE restart
- Switching between projects
- Resuming interrupted work

## 🚨 Recovery Triggers

| Trigger | Action |
|---------|--------|
| New session | Load last context |
| User says "continue" | Resume last task |
| IDE restart | Restore state |
| Crash recovery | Check incomplete tasks |

## 📝 Recovery Process

### Step 1: Detect Context
```markdown
Check for:
1. [ ] Active task files (task.md, active.md)
2. [ ] Recent git changes
3. [ ] Unsaved work
4. [ ] Error logs
```

### Step 2: Load Context
```markdown
Read in order:
1. memory/active.md → Current task
2. memory/summary.md → Project context
3. memory/decisions.md → Recent decisions
4. task.md → Pending items
```

### Step 3: Summarize State
```markdown
"Last session you were working on [task].
Progress was [X]% complete.
You were in the middle of [specific action].
Would you like to continue?"
```

### Step 4: Resume or Restart
```markdown
Options:
- Continue from last point
- Start fresh with context
- Switch to different task
```

## 🗂️ Context Files

| File | Purpose | Priority |
|------|---------|----------|
| `active.md` | Current task | 🔴 High |
| `task.md` | Task checklist | 🔴 High |
| `summary.md` | Project overview | 🟡 Medium |
| `decisions.md` | Architecture choices | 🟡 Medium |
| `changelog.md` | Recent changes | 🟢 Low |

## 📋 Recovery Template

```markdown
## 🔄 Session Recovery

### Last Session
- **Date**: [date]
- **Duration**: [time]
- **Project**: [name]

### Work in Progress
- Task: [description]
- Progress: [X]%
- Last action: [what was happening]

### Pending Items
- [ ] Item 1
- [ ] Item 2

### Files Modified
- `file1.js` - [changes]
- `file2.css` - [changes]

### Would you like to:
1. Continue from last point
2. Review changes first
3. Start fresh
```

## 🔧 Auto-Recovery Features

### 1. State Persistence
```javascript
// Save state before session ends
saveState({
  currentTask: taskName,
  progress: percentage,
  openFiles: fileList,
  recentActions: actionLog
});
```

### 2. Crash Detection
```javascript
// Check for incomplete state
if (activeTask && !taskCompleted) {
  recoveryMode = true;
  loadLastCheckpoint();
}
```

### 3. Git Integration
```bash
# Check uncommitted changes
git status --porcelain

# Get recent commits
git log --oneline -5
```

## 💡 Best Practices

1. **Save frequently**: Update active.md during work
2. **Checkpoint**: Mark milestones in progress
3. **Commit often**: Small, frequent commits
4. **Document blockers**: Note where you got stuck

## 🔗 Related Skills

- `memory-system` - Memory management
- `progress-tracking` - Track where you left off
- `git-workflow` - Version control recovery
