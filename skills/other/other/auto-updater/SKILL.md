---
name: auto-updater
description: Automatically apply improvements to skills and the ecosystem based on system-reviewer findings and best-practices-learner insights. Workflow for automated improvement identification, priority assessment, safe application, validation, and rollback capability. Use when applying systematic improvements, automating enhancement cycles, bulk updating multiple skills, or implementing ecosystem-wide improvements.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Auto Updater

## Overview

auto-updater automatically applies improvements to skills and ecosystem components based on identified patterns and learnings.

**Purpose**: Automated application of validated improvements across ecosystem

**The 5-Step Auto-Update Workflow**:
1. **Identify Improvements** - Gather recommendations from reviews and learnings
2. **Assess Safety** - Determine which can be safely automated
3. **Apply Updates** - Implement improvements automatically
4. **Validate Changes** - Ensure improvements effective, no regressions
5. **Rollback if Needed** - Revert changes if validation fails

**Safety**: Always validates before finalizing, can rollback

## When to Use

- Applying systematic improvements across multiple skills
- Implementing guideline updates ecosystem-wide
- Automating common enhancement patterns
- Bulk updates (e.g., add Quick Reference to all skills missing it)

## Auto-Update Workflow

### Step 1: Identify Improvements

**Sources**:
- system-reviewer recommendations
- best-practices-learner documented patterns
- review-multi common findings
- Manual improvement requests

**Output**: List of potential improvements

**Time**: 15-30 minutes

---

### Step 2: Assess Safety

**Safe to Automate**:
- Structural additions (add Quick Reference section)
- Content additions (add examples in standard locations)
- Format standardization (consistent heading levels)
- Documentation updates (README enhancements)

**NOT Safe to Automate**:
- Logic changes (requires understanding context)
- Content rewrites (needs judgment)
- Major refactoring (risk too high)
- Custom implementations

**Output**: Classified improvements (auto-safe vs manual-only)

**Time**: 20-40 minutes

---

### Step 3: Apply Updates

**Process**:
1. Backup affected skills (git commit or copy)
2. Apply improvement to each skill
3. Log changes made
4. Track success/failure per skill

**Approach**: One skill at a time, validate each before moving to next

**Time**: Varies by improvement and skill count

---

### Step 4: Validate Changes

**For Each Updated Skill**:
1. Run skill-validator (pass/fail)
2. Run review-multi structure check (score maintained?)
3. Visual inspection (looks correct?)
4. Mark as validated or flagged for review

**Output**: Validation results per skill

**Time**: 10-15 minutes per skill

---

### Step 5: Rollback if Needed

**If Validation Fails**:
1. Identify which skill failed
2. Restore from backup (git revert or copy back)
3. Analyze why it failed
4. Mark improvement as manual-only for that skill

**Output**: Rolled back skill, failure analysis

---

## Example Auto-Update

```
Auto-Update: Add Quick Reference to All Skills Missing It

Step 1: Identify
- Improvements: Add Quick Reference section
- Target Skills: planning-architect, task-development, todo-management
- Count: 3 skills to update

Step 2: Assess Safety
- ✅ Safe: Adding new section (doesn't modify existing content)
- ✅ Safe: Standard format (use template)
- ✅ Safe: Low risk (can validate easily)
- Decision: Auto-update approved

Step 3: Apply
- Backup: Git commit all 3 skills
- Apply to planning-architect: ✅ Success
- Apply to task-development: ✅ Success
- Apply to todo-management: ✅ Success
- Changes: 3/3 skills updated

Step 4: Validate
- planning-architect: 5/5 structure (maintained)
- task-development: 5/5 structure (maintained)
- todo-management: 5/5 structure (maintained)
- All validations: ✅ PASS

Step 5: Rollback
- Not needed (all validations passed)

Result: ✅ 3 skills successfully auto-updated
Time: 90 minutes (vs 3-4 hours manual)
Impact: 100% Quick Reference coverage achieved
Quality: All skills maintained 5/5 scores
```

---

## Quick Reference

### 5-Step Auto-Update Workflow

| Step | Focus | Time | Safety |
|------|-------|------|--------|
| Identify | Gather improvements | 15-30m | N/A |
| Assess Safety | Classify auto-safe | 20-40m | Critical |
| Apply | Implement changes | Varies | Backup first |
| Validate | Check quality maintained | 10-15m/skill | Essential |
| Rollback | Revert if fails | 5m/skill | Safety net |

### Safe vs Unsafe Automation

**Safe to Automate**:
- Adding standard sections
- Format standardization
- Documentation additions
- Structural improvements (following patterns)

**NOT Safe**:
- Logic changes
- Content rewrites
- Major refactoring
- Custom implementations

**Rule**: If requires judgment or understanding → Manual only

---

**auto-updater enables safe, validated, automated improvement application across multiple skills simultaneously.**
