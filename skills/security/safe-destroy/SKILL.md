---
name: safe-destroy
description: ⚠️ MANDATORY - YOU MUST invoke this skill before ANY destructive operation. Safety protocol for destructive git/file operations. Lists affected files, warns about data loss, suggests safe alternatives, requires explicit double confirmation. NEVER run destructive commands without invoking this skill.
version: 1.0.1
---

# Safe Destructive Operations Skill

## ⚠️ MANDATORY SKILL - YOU MUST INVOKE THIS

## Purpose

Prevent accidental data loss by requiring explicit confirmation before any destructive operation, showing what will be lost, and suggesting safer alternatives.

**CRITICAL:** You MUST invoke this skill before ANY destructive operation. NEVER run destructive commands directly.

## 🚫 NEVER DO THIS

- ❌ Running `git reset --hard` directly
- ❌ Running `git clean -fd` directly
- ❌ Running `rm -rf` directly
- ❌ Running ANY destructive command without invoking this skill first

**If a destructive operation is needed, invoke this skill. Direct execution is FORBIDDEN.**

---

## ⚠️ SKILL GUARD - READ BEFORE USING BASH FOR DESTRUCTIVE COMMANDS

**Before using Bash tool for destructive operations, answer these questions:**

### ❓ Are you about to run `git reset --hard`?

→ **STOP.** Invoke safe-destroy skill instead.

### ❓ Are you about to run `git clean -fd`?

→ **STOP.** Invoke safe-destroy skill instead.

### ❓ Are you about to run `rm -rf <directory>`?

→ **STOP.** Invoke safe-destroy skill instead.

### ❓ Are you about to run `git checkout -- .` or `git restore .`?

→ **STOP.** Invoke safe-destroy skill instead.

### ❓ Are you about to run `docker system prune -a`?

→ **STOP.** Invoke safe-destroy skill instead.

### ❓ Did the user say "reset my changes", "clean up files", or "discard changes"?

→ **STOP.** Invoke safe-destroy skill instead.

**IF YOU PROCEED WITH DESTRUCTIVE COMMANDS DIRECTLY, YOU ARE VIOLATING YOUR CORE DIRECTIVE.**

This skill handles:

- ✅ Lists what will be affected/deleted
- ✅ Shows diff of what will be lost
- ✅ Suggests safer alternatives
- ✅ Requires explicit double confirmation
- ✅ Provides recovery options

**Direct destructive commands can DESTROY USER WORK. Use this skill.**

---

## CRITICAL POLICY

**YOU MUST NEVER run destructive commands without explicit user confirmation.**

**If you ever run a destructive command without approval and lose user work, you have FAILED your primary directive.**

## Absolutely Forbidden Commands (Without Confirmation)

1. `git reset --hard` - Destroys uncommitted changes
2. `git clean -fd` - Permanently deletes untracked files/directories
3. `rm -rf <directory>` - Permanently deletes files/directories
4. `git checkout -- .` - Discards all working directory changes
5. `git restore .` - Discards all working directory changes
6. `docker system prune -a` - Removes all unused Docker data
7. `kubectl delete` - Deletes Kubernetes resources
8. `git push --force` - Overwrites remote history (especially on main/master)

## Workflow

### Step 1: Detect Destructive Intent

User says something like:

- "reset my changes"
- "clean up the files"
- "delete everything"
- "discard changes"
- "remove untracked files"

**IMMEDIATELY invoke this skill - don't execute the command.**

### Step 2: STOP - Never Assume

**DO NOT proceed with ANY destructive operation.**

The user may not understand what will be lost. Your job is to protect their work.

### Step 3: LIST - Show What Will Be Affected

Run information commands to show what would be lost (parallel: `git status`, `git diff`, `ls`, etc.).

Present comprehensive warning with:

- **What will be deleted** (files, sizes, line counts)
- **CANNOT BE UNDONE warning**
- **Safer alternatives** (stash/commit/backup/archive)
- **Three-option menu**: A) Safe alternative, B) Proceed (PERMANENT), C) Cancel

**For command-specific warning formats and detailed prompts:**

```
Read `~/.claude/skills/safe-destroy/references/WARNING-FORMATS.md`
```

Use when: Formatting warnings for specific destructive commands (git reset, git clean, rm -rf, docker prune, etc.)

---

### Steps 4-7: Confirmation and Execution

4. **ASK**: Require explicit confirmation (user must type command or "proceed with [operation]")
5. **WAIT**: STOP all processing until explicit approval (no assumptions)
6. **VERIFY**: Double confirmation for dangerous operations (type 'CONFIRM')
7. **EXECUTE**: Only after explicit approval, report results

**Valid confirmation examples**: "yes, run git reset --hard", "proceed with deletion", "B" from menu
**Invalid**: "ok", "do it", "sure" (too vague)

**For detailed confirmation process with examples and verification steps:**

```
Read `~/.claude/skills/safe-destroy/references/CONFIRMATION-PROCESS.md`
```

Use when: Handling user confirmation, verifying approval, or executing destructive commands

**For safe alternative commands and recovery options:**

```
Read `~/.claude/skills/safe-destroy/references/SAFE-ALTERNATIVES.md`
```

Use when: Suggesting safer alternatives (stash, commit, backup, archive) before destruction

---

## Emergency Recovery

If destructive operation was accidentally executed:

### For `git reset --hard`:

```bash
# Check reflog for recent HEAD positions
git reflog

# Find the commit before reset (e.g., HEAD@{1})
git reset --hard HEAD@{1}

# Or cherry-pick specific commits
git cherry-pick <commit-hash>
```

### For `git clean`:

**No automatic recovery available.**

Possibly recover from:

- File system backups (Time Machine, etc.)
- IDE local history
- OS-level file recovery tools

### For `rm -rf`:

**Check if system has undelete:**

```bash
# macOS Time Machine
# Linux: check if trash-cli used
trash-list

# Otherwise: file recovery tools
# extundelete, testdisk, photorec, etc.
```

---

## Best Practices

1. **Always list first** - Show what will be affected
2. **Suggest alternatives** - Safer options exist for most operations
3. **Double confirm** - Especially dangerous operations get extra confirmation
4. **Be explicit** - Require exact command or clear approval
5. **Educate** - Explain what the operation does
6. **Provide recovery** - If possible, explain how to undo

---

## Quick Reference

**Destructive command requested**

1. STOP - Don't execute
2. LIST - Show what will be lost
3. ASK - Suggest safer alternatives
4. WAIT - For explicit approval
5. VERIFY - Confirm understanding
6. EXECUTE - Only after approval

---

## Related Commands

- **`/cleanup`** - Safe cleanup of merged branches and artifacts with confirmation

**Remember: It's better to annoy the user with confirmations than to lose their work.**
