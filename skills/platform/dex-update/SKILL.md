---
name: dex-update
description: Safely update Dex with one command (handles everything automatically)
---

## What This Command Does

**For non-technical users:** Updates Dex to the latest version automatically. No command line knowledge needed - just run the command and follow the prompts.

**When to use:**
- After `/dex-whats-new` shows new version available
- When you want the latest features and bug fixes

**What it handles:**
- Downloads updates automatically
- Protects your data (never touches your notes, tasks, projects)
- Resolves conflicts automatically (keeps your customizations)
- Shows clear progress and confirmation

**Time:** 2-5 minutes

---

## Process

### Step 1: Pre-Check

**A. Check if Git is available**

Try running basic git command:
```bash
git --version
```

**If Git not found:**
```
❌ Git not detected

Dex updates require Git. Here's how to install:

**Mac:** 
1. Open Terminal (Cmd+Space, type "Terminal")
2. Run: xcode-select --install
3. Click Install when prompted
4. Come back here when done

**Windows:**
1. Download from: https://git-scm.com/download/win
2. Run installer with default options
3. Restart Cursor
4. Try /dex-update again

[Skip update] — I'll do this later
```

If user skips, exit gracefully.

---

**B. Check current setup**

Run: `git remote -v`

**Scenario 1: Downloaded as ZIP (no Git)**
```
❌ Not a Git repository

Looks like you downloaded Dex as a ZIP file instead of cloning it.

**To update:**
1. Download latest version: https://github.com/davekilleen/dex/archive/refs/heads/main.zip
2. Unzip to a new folder
3. Copy these folders from your current Dex to the new one:
   • System/user-profile.yaml
   • System/pillars.yaml
   • 00-Inbox/
   • 01-Quarter_Goals/
   • 02-Week_Priorities/
   • 03-Tasks/
   • 04-Projects/
   • 05-Areas/
   • 07-Archives/
4. Delete old Dex folder
5. Rename new folder to 'dex'
6. Open in Cursor

[Show detailed guide] — Open step-by-step instructions
[Cancel] — I'll do this later
```

If detailed guide selected, open `06-Resources/Dex_System/Updating_Dex.md` (Manual Update section).

---

**Scenario 2: Cloned but no upstream remote**

If `git remote -v` shows only "origin" pointing to github.com/davekilleen/dex:

```
✓ Git repository detected

Setting up automatic updates...
```

Run:
```bash
git remote rename origin upstream
```

Continue to Step 2.

---

**Scenario 3: Already configured**

If upstream exists, continue to Step 2.

---

### Step 2: Check for Updates

Call update checker:
```
check_for_updates(force=True)
```

**If no updates available:**
```
✅ You're already on the latest version (v1.2.0)

No update needed!
```
Exit.

**If updates available, show summary:**
```
🎁 Dex v1.3.0 is available

You're on: v1.2.0
Latest: v1.3.0

What's new:
- Career coach improvements
- Task deduplication fix  
- Meeting intelligence enhancement

[View full release notes]
[Update now]
[Cancel]
```

---

### Step 3: Pre-Update Safety Check

**A. Check for uncommitted changes**

Run: `git status --porcelain`

**If there are changes:**
```
💾 Saving your work...

Dex found unsaved changes in your vault.
Let me save them before updating.
```

Run:
```bash
git add .
git commit -m "Auto-save before Dex update to v1.3.0"
```

Show:
```
✓ Your work is saved
```

**B. Create backup reference (safety net)**

Run:
```bash
git tag backup-before-v1.3.0
```

This creates a snapshot user can revert to if needed.

---

### Step 4: Download Updates

```
⬇️ Downloading updates from GitHub...
```

Run:
```bash
git fetch upstream
```

**If network error:**
```
❌ Couldn't connect to GitHub

Please check your internet connection and try again.

[Retry]
[Cancel]
```

**Success:**
```
✓ Updates downloaded
```

---

### Step 5: Check for Breaking Changes

Parse the update response from Step 2.

**If `breaking_changes: true`:**

```
⚠️ Important: This update includes major changes

Dex v2.0.0 includes breaking changes that require extra steps:

[Show what's changing]

This is safe to proceed, but:
• Some folders may be renamed
• Configuration format may change  
• Migration will run automatically

[Continue with update]
[Cancel — I'll read the details first]
```

If cancelled:
- Show link to release notes
- Exit gracefully
- User can run `/dex-update` again when ready

---

### Step 6: Apply Updates

```
🔄 Applying updates...
```

**A. Merge updates**

Run:
```bash
git merge upstream/main --no-edit
```

**B. Handle merge outcome**

**Case 1: Clean merge (no conflicts)**
```
✓ Updates applied successfully
```

Continue to Step 7.

---

**Case 2: Merge conflicts**

Check which files have conflicts:
```bash
git status | grep "both modified"
```

**Automatic conflict resolution:**

For each conflicting file:

1. **If file is in protected list** (user data):
   - 00-Inbox/, 01-07/: Keep user version
   - System/user-profile.yaml: Keep user version
   - System/pillars.yaml: Keep user version
   
   Run: `git checkout --ours <file>`

2. **If file is in core list** (Dex updates):
   - .claude/skills/*.md: Keep upstream version
   - core/mcp/*.py: Keep upstream version
   - .scripts/*.cjs: Keep upstream version
   
   Run: `git checkout --theirs <file>`

3. **If file is CLAUDE.md** (hybrid):
   - Check if user has `CLAUDE-custom.md`
   - If yes: Keep upstream version of CLAUDE.md
   - If no: Keep user version, but suggest creating CLAUDE-custom.md

4. **Mark as resolved:**
   ```bash
   git add <file>
   ```

**After resolving all conflicts:**
```bash
git commit --no-edit
```

**Show to user:**
```
✓ Updates applied successfully

Handled conflicts automatically:
• Kept your notes and customizations
• Updated core Dex features
• Protected your data

[See what changed]
```

---

**Case 3: Merge failed (rare)**

```
❌ Update couldn't complete automatically

This is rare, but sometimes updates need manual review.

**What happened:**
[Error message]

**Options:**
[Restore to before update] — Uses the backup we created
[Get help] — Opens GitHub issue template
```

If restore:
```bash
git merge --abort
git reset --hard backup-before-v1.3.0
```

---

### Step 7: Post-Update Steps

**A. Check for migration needs**

If breaking_changes was true, check for migration script:

```bash
ls core/migrations/v*-to-v*.sh
```

If found:
```
🔧 Running migration...

This update requires a one-time migration to update your data structure.
This is safe and automatic.
```

Run:
```bash
./core/migrations/v1-to-v2.sh --auto
```

Show migration output.

**B. Update dependencies**

```
📦 Updating dependencies...
```

Run:
```bash
npm install
pip3 install -r core/mcp/requirements.txt
```

---

### Step 8: Verification

```
✓ Update complete! Now testing...
```

**Quick smoke test:**

1. Check key files exist:
   - `03-Tasks/Tasks.md`
   - `System/user-profile.yaml`
   - `.claude/skills/daily-plan/SKILL.md`

2. Check MCP configuration:
   - `.mcp.json` exists

3. Try loading user profile:
   - Read `System/user-profile.yaml`

**If all pass:**
```
✅ Update successful!
```

**If something fails:**
```
⚠️ Update completed but found an issue

[Details of what failed]

Your data is safe, but you may want to:
[Restore to previous version]
[Report this issue]
[Continue anyway]
```

---

### Step 9: Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Dex Updated: v1.2.0 → v1.3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What's new:
• Career coach improvements
• Task deduplication fix
• Meeting intelligence enhancement

Your data:
✓ All notes preserved
✓ All tasks preserved  
✓ All customizations preserved

[View full changelog]
[Start using new features]
```

**If there were conflicts:**
```
🔍 Changes applied:
• Updated 12 core files
• Kept 5 of your customized files
• Protected all your data folders

[See detailed change list]
```

---

### Step 10: Track Usage (Silent)

Update usage log:
```
System/usage_log.md
- [ ] Update Dex (/dex-update) → [x] Update Dex (/dex-update)
```

---

## Error Recovery

### If Update Fails at Any Point

User always has escape hatch:

```
🔙 Restoring to before update...
```

Run:
```bash
git merge --abort 2>/dev/null || true
git reset --hard backup-before-v1.3.0
git clean -fd
```

```
✓ Restored to v1.2.0

Nothing was changed. Your Dex is exactly as it was.

[Try update again]
[Report issue]
[Cancel]
```

---

## Migration Support (for Breaking Changes)

### Auto-Migration Flag

If migration script supports `--auto` flag, run non-interactively:

```bash
./core/migrations/v1-to-v2.sh --auto
```

**Migration script must:**
- Accept `--auto` flag
- Skip confirmation prompts
- Return exit code 0 on success
- Log to `System/.migration-log`

### Manual Migration Required

If script doesn't support `--auto`:

```
⚠️ Manual step required

This update needs you to run a migration script.

Don't worry - it's one command and takes 30 seconds.

**In Cursor's terminal (bottom panel), run:**

./core/migrations/v1-to-v2.sh

**Then come back here when it's done.**

[I've run the migration — continue]
[Show me what the migration does]
[Cancel update]
```

---

## Alternative: ZIP Download Path

For users who can't/won't use Git, provide manual instructions:

```
📥 Manual Update Method

If automatic updates don't work, you can update manually:

1. **Download latest Dex:**
   https://github.com/davekilleen/dex/archive/refs/heads/main.zip

2. **Copy your data:**
   From OLD Dex folder, copy these to NEW Dex folder:
   
   ✓ System/user-profile.yaml
   ✓ System/pillars.yaml
   ✓ 00-Inbox/ (entire folder)
   ✓ 01-Quarter_Goals/ (entire folder)
   ✓ 02-Week_Priorities/ (entire folder)
   ✓ 03-Tasks/ (entire folder)
   ✓ 04-Projects/ (entire folder)
   ✓ 05-Areas/ (entire folder)
   ✓ 07-Archives/ (entire folder)
   ✓ .env (if it exists)

3. **DON'T copy:**
   ✗ .claude/skills/ (use new version)
   ✗ core/mcp/ (use new version)
   ✗ README.md (use new version)

4. **Open new folder in Cursor**

5. **Run /setup to verify**

[Download now]
[Copy step-by-step instructions to clipboard]
```

---

## Settings

User can configure update behavior in `System/user-profile.yaml`:

```yaml
updates:
  auto_check: true              # Check during /daily-plan
  check_interval_days: 7        # How often to check
  auto_update: false            # Never auto-update without asking
  backup_before_update: true    # Always create backup tag
```

---

## Related Commands

- `/dex-whats-new` - Check what's new without updating
- `/dex-rollback` - Undo last update (if something went wrong)
- `/dex-update-settings` - Configure update preferences

---

## Non-Technical User Experience

**User sees in daily plan:**
```
🎁 Dex v1.3.0 is available. Run /dex-whats-new for details.
```

**User runs:**
```
/dex-update
```

**User sees:**
```
✓ Git detected
✓ Updates downloaded
✓ No conflicts
✓ Dependencies updated
✅ Update complete! v1.2.0 → v1.3.0
```

**Total clicks:** 1 (just ran the command)
**Total time:** 2 minutes
**Technical knowledge required:** Zero

---

## Philosophy

**Automatic where possible:**
- Git commands run silently
- Conflicts resolved automatically
- Dependencies updated automatically
- Migrations run automatically (when safe)

**Interactive where necessary:**
- Breaking changes: confirm understanding
- Manual migration: clear instructions
- Errors: always offer restoration

**Safe always:**
- Backup created before any changes
- User data never at risk (gitignored)
- One-command rollback if issues
- Clear status at every step

**No jargon:**
- Don't say "merge conflict" - say "overlapping changes"
- Don't say "upstream" - say "main Dex repository"
- Don't say "git fetch" - say "downloading updates"
- Don't say "rebase" - just don't use rebase
