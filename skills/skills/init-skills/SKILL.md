---
name: init-skills
description: Initialize Claude skills in the current project and verify setup. Use when user says '/init-skills', 'setup skills', 'install skills', or 'add Claude skills to this project'. Can also review and verify existing skills installation.
---

# Init Skills - Setup & Verification

Automatically initializes Claude Code skills in any project and verifies they're working correctly.

## When I Activate

I activate when you:
- Type `/init-skills` or `/setup-skills`
- Say "setup Claude skills"
- Say "install skills in this project"
- Ask "are skills installed?"
- Want to verify skills are working

---

## What I Do

### 1. Check Current Status

First, I check if skills are already installed:

```bash
# Check for .claude/skills directory
# List what skills exist
# Verify each SKILL.md file
```

**Report:**
```
## Skills Status

✅ Skills installed: 6/6
- prompt-helper
- debug-buddy
- test-and-verify
- code-explainer
- research-and-implement
- quick-review

OR

❌ Skills not found
Need to initialize skills in this project.
```

---

### 2. Initialize Skills (If Needed)

If skills aren't installed, I'll run the initialization:

```bash
/Users/josh/Cursor/APPS/claudecodeskills/init-claude-skills.sh
```

**Steps:**
1. Create `.claude/skills/` directory
2. Copy all 6 skills from template
3. Verify each skill file
4. Confirm installation

---

### 3. Verify Installation

After initialization (or if skills already exist), I verify:

**Verification Checklist:**
- [ ] `.claude/skills/` directory exists
- [ ] All 6 skill folders present
- [ ] Each skill has SKILL.md file
- [ ] YAML frontmatter is valid
- [ ] Description field exists (for auto-activation)
- [ ] Skills are ready to use

---

### 4. Provide Usage Guide

After successful setup, I explain:

```
## ✅ Skills Installed Successfully!

Your 6 Claude Code skills are now active:

1. **prompt-helper** - Guides effective prompting
   Activates: "How do I ask Claude to..."

2. **debug-buddy** - Systematic debugging with /chrome
   Activates: When errors occur or code breaks

3. **test-and-verify** - Comprehensive testing
   Activates: "Test this feature"

4. **code-explainer** - Beginner-friendly explanations
   Activates: "What does this code do?"

5. **research-and-implement** - Research then build
   Activates: "Research how to add..."

6. **quick-review** - Fast code review
   Activates: "Review this code"

## Next Steps:
- Skills auto-activate when relevant
- Just talk to Claude normally
- Skills work automatically!
```

---

## Usage Examples

### Example 1: First Time Setup

**You type:** `/init-skills`

**I do:**
1. Check if skills exist → Not found
2. Run initialization script
3. Copy all 6 skills
4. Verify installation
5. Show success message with guide

---

### Example 2: Verify Existing Skills

**You type:** `/init-skills`

**I do:**
1. Check if skills exist → Found!
2. Verify all 6 skills present
3. Check each SKILL.md file
4. Report status:
   ```
   ✅ All skills installed and verified
   - prompt-helper ✓
   - debug-buddy ✓
   - test-and-verify ✓
   - code-explainer ✓
   - research-and-implement ✓
   - quick-review ✓
   ```

---

### Example 3: Partial Installation

**You type:** `/init-skills`

**I do:**
1. Check skills → Found 3/6
2. Report missing skills
3. Ask if you want to:
   - Re-initialize all (recommended)
   - Add missing only
4. Complete the installation
5. Verify all working

---

## Automatic Actions

When you invoke this skill, I will:

1. **Check Status** (always first)
   ```bash
   ls .claude/skills/
   ```

2. **Initialize if Needed**
   ```bash
   /Users/josh/Cursor/APPS/claudecodeskills/init-claude-skills.sh
   ```

3. **Verify Installation**
   ```bash
   find .claude/skills -name "SKILL.md"
   # Should return 6 files
   ```

4. **Read and Validate**
   - Check each SKILL.md has proper YAML
   - Verify description fields exist
   - Confirm all required skills present

5. **Report Success**
   - Show installed skills
   - Explain how they work
   - Provide next steps

---

## Skills Inventory

I verify these 6 skills are installed:

### 1. prompt-helper
**Purpose:** Guides you to structure effective prompts
**File:** `.claude/skills/prompt-helper/SKILL.md`
**Activates:** User needs help asking Claude for something

### 2. debug-buddy
**Purpose:** Systematic debugging with browser automation
**File:** `.claude/skills/debug-buddy/SKILL.md`
**Activates:** Errors, bugs, code doesn't work
**Features:** /chrome integration for testing

### 3. test-and-verify
**Purpose:** Comprehensive testing before moving forward
**File:** `.claude/skills/test-and-verify/SKILL.md`
**Activates:** After building features or fixing bugs
**Features:** /chrome integration, GIF recording

### 4. code-explainer
**Purpose:** Explains code in beginner-friendly terms
**File:** `.claude/skills/code-explainer/SKILL.md`
**Activates:** User wants to understand code

### 5. research-and-implement
**Purpose:** Researches best practices then implements
**File:** `.claude/skills/research-and-implement/SKILL.md`
**Activates:** Building unfamiliar features
**Features:** /chrome integration for research

### 6. quick-review
**Purpose:** Fast code review for quality and security
**File:** `.claude/skills/quick-review/SKILL.md`
**Activates:** Before commits or when requesting review

---

## Troubleshooting

### Issue: Script Path Not Found

**Error:**
```
init-claude-skills.sh: No such file or directory
```

**Fix:**
Verify the script exists:
```bash
ls /Users/josh/Cursor/APPS/claudecodeskills/init-claude-skills.sh
```

If missing, I'll help you locate it or re-create it.

---

### Issue: Permissions Error

**Error:**
```
Permission denied
```

**Fix:**
```bash
chmod +x /Users/josh/Cursor/APPS/claudecodeskills/init-claude-skills.sh
```

---

### Issue: Partial Installation

**Symptom:** Only some skills installed

**Fix:**
1. Remove partial installation:
   ```bash
   rm -rf .claude/skills
   ```
2. Re-run initialization
3. Verify all 6 skills present

---

## Output Format

### Success Report

```
╔════════════════════════════════════════╗
║     Claude Skills Status Report        ║
╔════════════════════════════════════════╗

✅ Skills Installation: COMPLETE

Installed Skills (6/6):
  ✓ prompt-helper
  ✓ debug-buddy
  ✓ test-and-verify
  ✓ code-explainer
  ✓ research-and-implement
  ✓ quick-review

📍 Location: .claude/skills/

🎯 Status: All skills active and ready

💡 Usage:
   Skills auto-activate based on context.
   Just ask Claude naturally - skills will help automatically!

🚀 You're ready to code with skill support!
```

---

### Installation Report

```
╔════════════════════════════════════════╗
║   Initializing Claude Skills...        ║
╔════════════════════════════════════════╗

→ Creating .claude/skills directory...
→ Copying skills from template...
→ Installing prompt-helper... ✓
→ Installing debug-buddy... ✓
→ Installing test-and-verify... ✓
→ Installing code-explainer... ✓
→ Installing research-and-implement... ✓
→ Installing quick-review... ✓

✅ Installation Complete!

All 6 skills successfully installed and verified.
```

---

## Quick Actions

When invoked, I can also:

### List All Skills
Shows what skills are available and what they do

### Verify Setup
Checks that all skills are properly formatted and working

### Reinstall Skills
If something's broken, I can clean and reinstall

### Show Skill Details
Explain what each skill does and when it activates

---

## Integration with Other Skills

After initialization:
- **prompt-helper** will guide your questions
- **debug-buddy** will help fix errors
- **test-and-verify** will test your code
- **code-explainer** will explain what you built
- **research-and-implement** will help with new features
- **quick-review** will check quality before commits

All work together automatically!

---

## Slash Command Usage

Invoke this skill with:
- `/init-skills`
- `/setup-skills`
- `/verify-skills`
- "Setup Claude skills"
- "Install skills"
- "Are skills installed?"

I'll handle the rest automatically!

---

## Cost-Conscious Operation

This skill:
- ✅ Runs initialization script (fast, minimal tokens)
- ✅ Verifies files exist (simple file checks)
- ✅ One-time setup per project
- ✅ No ongoing cost after installation
- ✅ Skills themselves are cost-optimized

---

## Success Criteria

Setup is successful when:
- ✅ `.claude/skills/` directory exists
- ✅ All 6 SKILL.md files present
- ✅ Each skill has valid YAML frontmatter
- ✅ All skills ready to auto-activate
- ✅ User understands how to use them

---

## Follow-Up Actions

After successful setup, I can:
1. Test a skill activation (try prompt-helper)
2. Explain any specific skill in detail
3. Show examples of how skills work
4. Help customize skills for your project
5. Verify skills work with a real task

---

**Just type `/init-skills` whenever you need to set up or verify Claude skills in a project!**
