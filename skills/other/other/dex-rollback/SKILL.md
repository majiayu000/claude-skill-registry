---
name: dex-rollback
description: Undo the last Dex update if something went wrong
---

## What This Command Does

**Restores Dex to the version before your last update.** Use this if something broke after updating.

**When to use:**
- Feature you relied on stopped working
- Data looks wrong after update
- System feels unstable
- Want to go back for any reason

**Safe to use:** Your notes, tasks, and projects are never at risk.

---

## Process

### Step 1: Check if Rollback is Possible

**A. Verify Git repository**

Run: `git --version`

If Git not found:
```
❌ Git not detected

Rollback requires Git. Your data is safe, but automated rollback isn't available.

**To manually restore:**
1. If you have a backup folder, copy your data back
2. Or re-download Dex and copy your folders (00-07, System/)

[Show manual restore guide]
```

**B. Check for backup tag**

Run: `git tag | grep backup-before`

If no backup found:
```
❌ No backup found

Looks like you haven't updated recently, or the backup wasn't created.

Your current version: v1.3.0

Options:
[Download previous version manually]
[Cancel]
```

**C. Identify what version to restore to**

Run: `git tag | grep backup-before | tail -1`

Example: `backup-before-v1.3.0` means restore to before v1.3.0 update.

---

### Step 2: Confirm Rollback

```
🔙 Rollback Dex Update

You're about to restore Dex to the version before your last update.

Current version: v1.3.0
Will restore to: v1.2.0 (last backup)

**What happens:**
✓ Dex features restored to v1.2.0
✓ Your notes, tasks, projects stay as they are
✓ Any new skills from v1.3.0 will be removed

**This is safe:**
• Your data folders (00-07) are not affected
• Your configuration (user-profile, pillars) stays
• You can update again later if you want

[Confirm rollback]
[Cancel]
```

---

### Step 3: Save Current State

Before rolling back, save any uncommitted changes:

```
💾 Saving current state...
```

Run:
```bash
git add .
git commit -m "Auto-save before rollback to v1.2.0" || true
```

Create a "before rollback" tag in case they want to undo the rollback:

```bash
git tag before-rollback-$(date +%Y%m%d-%H%M%S)
```

```
✓ Current state saved
```

---

### Step 4: Perform Rollback

```
🔄 Rolling back to v1.2.0...
```

Run:
```bash
git reset --hard backup-before-v1.3.0
```

This restores all Dex files to the state before update.

**Note:** User data folders (00-07) remain untouched because:
1. They're gitignored (not tracked)
2. `git reset` only affects tracked files

---

### Step 5: Cleanup

**A. Remove dependencies from newer version**

```
📦 Cleaning up...
```

Run:
```bash
npm install
pip3 install -r core/mcp/requirements.txt
```

This ensures dependencies match the older version.

**B. Remove migration markers (if exist)**

```bash
rm -f .migration-v*-complete
rm -f .migration-version
```

---

### Step 6: Verification

```
✓ Rollback complete! Now testing...
```

**Quick checks:**

1. Verify version in package.json:
   ```bash
   cat package.json | grep version
   ```

2. Check key files:
   - `03-Tasks/Tasks.md`
   - `System/user-profile.yaml`
   - `.claude/skills/daily-plan/SKILL.md`

3. Test user profile loads:
   ```
   Read System/user-profile.yaml
   ```

**If all pass:**
```
✅ Rollback successful!
```

**If issues:**
```
⚠️ Rollback completed but found an issue

[Details]

Your data is safe. You may want to:
[Report this issue]
[Try rolling back again]
[Continue anyway]
```

---

### Step 7: Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Rolled Back: v1.3.0 → v1.2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dex restored to: v1.2.0
Your data: All preserved (notes, tasks, projects)

You're back to the version from before your last update.

**What now?**
• Everything should work as before
• You can try updating again later with /dex-update
• If issues persist, try /setup to verify configuration

**Want to report what went wrong?**
[Open issue on GitHub] — Help improve future updates
```

---

## Undo Rollback (Advanced)

If user rolled back by mistake and wants to go forward again:

```
Did you roll back by mistake?

We saved your state before rollback. You can restore it:

[Restore to v1.3.0] — Undo this rollback
[Stay on v1.2.0] — Keep rollback
```

If user chooses restore:

```bash
RESTORE_TAG=$(git tag | grep before-rollback | tail -1)
git reset --hard $RESTORE_TAG
```

---

## Manual Rollback (No Git)

If Git not available or no backup tags:

```
📥 Manual Rollback Method

To restore an older version without Git:

1. **Download your desired version:**
   
   For v1.2.0:
   https://github.com/davekilleen/dex/releases/tag/v1.2.0
   
   Click "Source code (zip)"

2. **Copy your data:**
   
   From CURRENT Dex, copy to DOWNLOADED Dex:
   
   ✓ System/user-profile.yaml
   ✓ System/pillars.yaml
   ✓ 00-Inbox/
   ✓ 01-Quarter_Goals/
   ✓ 02-Week_Priorities/
   ✓ 03-Tasks/
   ✓ 04-Projects/
   ✓ 05-Areas/
   ✓ 07-Archives/
   ✓ .env (if exists)

3. **Replace folders:**
   
   • Move current Dex folder to trash (or rename to dex-old)
   • Rename downloaded folder to 'dex'
   • Open in Cursor

4. **Verify:**
   
   Run /setup to check everything works

[See version history] — All Dex releases
[Copy instructions]
```

---

## Rollback Limitations

**What rollback restores:**
- ✓ Dex skills
- ✓ MCP servers
- ✓ Core features
- ✓ Documentation

**What rollback preserves (doesn't touch):**
- ✓ Your notes (00-Inbox, 04-Projects, 05-Areas)
- ✓ Your tasks (03-Tasks/)
- ✓ Your configuration (user-profile, pillars)
- ✓ Your API keys (.env)

**What you might lose:**
- ⚠️ New features added since v1.2.0
- ⚠️ Bug fixes introduced in v1.3.0
- ⚠️ New skills that came with update

---

## Troubleshooting

### "Rollback completed but /daily-plan doesn't work"

Likely MCP servers need restart:

1. Close Cursor completely
2. Reopen your Dex folder
3. Try /daily-plan again

### "My tasks look different after rollback"

Your task data is unchanged. What might look different:
- Task display format (if update changed rendering)
- Task sorting (if update changed logic)

**Your actual tasks are safe.** Check `03-Tasks/Tasks.md` directly - everything is there.

### "Can I rollback multiple versions?"

Yes, if backups exist:

```bash
git tag | grep backup-before
```

Shows all available backups:
```
backup-before-v1.1.0
backup-before-v1.2.0
backup-before-v1.3.0
```

To rollback to specific version:
```bash
git reset --hard backup-before-v1.1.0
```

But easier: tell `/dex-rollback` which version you want, and it handles it.

---

## Prevention Better Than Cure

**To avoid needing rollback:**

1. **Read release notes before updating**
   - Run `/dex-whats-new` first
   - Check for breaking changes warning
   - Understand what's changing

2. **Update during low-stakes time**
   - Not right before important meeting
   - Not during crunch deadline
   - Give yourself time to test

3. **Test after updating**
   - Run `/daily-plan`
   - Open a person page
   - Check key workflows

4. **Keep regular backups**
   - Use Time Machine (Mac) or File History (Windows)
   - Or manually copy Dex folder weekly

---

## Related Commands

- `/dex-update` - Update to latest version
- `/dex-whats-new` - Check what's available
- `/setup` - Verify Dex configuration

---

## Philosophy

**Rollback should be:**
- One command away
- Always available
- Completely safe
- No data loss ever

**User confidence:**
"I can try updates knowing I can undo them instantly"

**No shame in rolling back:**
Updates should improve things. If they don't for you, rolling back is the right choice. Help us by reporting what went wrong.

## Track Usage (Silent)

Update `System/usage_log.md` to mark Dex rollback as used.

**Analytics (Silent):**

Call `track_event` with event_name `dex_rollback_completed` and properties:
- `restored_version`

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
