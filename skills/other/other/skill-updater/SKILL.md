---
name: skill-updater
description: Apply improvements to Claude Code skills systematically. Workflow for planning updates, implementing changes, validating improvements, and documenting changes. Use when applying review recommendations, updating skills based on feedback, enhancing existing skills, or implementing systematic improvements across multiple skills.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Updater

## Overview

skill-updater provides systematic workflow for applying improvements to existing Claude Code skills based on review findings, user feedback, or identified opportunities.

**Purpose**: Systematic skill improvement and enhancement

**Integration**:
- review-multi → identifies improvements
- skill-reviewer → finds opportunities
- **skill-updater** → applies changes systematically
- skill-validator → validates changes

**Update Workflow** (5 steps):
1. **Plan Updates** - Review recommendations, prioritize, plan changes
2. **Backup Skill** - Save current version before changes
3. **Apply Changes** - Implement improvements systematically
4. **Validate Changes** - Ensure improvements effective, no regressions
5. **Document Updates** - Record what changed and why

## When to Use

- Applying review-multi recommendations
- Implementing user feedback
- Enhancing skill based on skill-reviewer findings
- Systematic improvements across skills
- Version updates (v1.0 → v1.1)

## Update Workflow

### Step 1: Plan Updates

**Process**:
1. Gather improvement recommendations (from reviews, feedback)
2. Prioritize: Critical → High → Medium → Low
3. Estimate effort per improvement
4. Plan update sequence
5. Set success criteria

---

### Step 2: Backup Skill

**Process**:
```bash
# Create backup
cp -r .claude/skills/skill-name .claude/skills/skill-name.backup-$(date +%Y%m%d)

# Or use git
git add .claude/skills/skill-name
git commit -m "Backup before updates"
```

---

### Step 3: Apply Changes

**Process**:
1. Start with highest priority
2. Make one improvement at a time
3. Test after each change
4. Mark as complete
5. Move to next

---

### Step 4: Validate Changes

**Process**:
1. Run skill-validator (structure, content, pattern)
2. Compare before/after (metrics, quality)
3. Test in real scenario (usability)
4. Verify no regressions

---

### Step 5: Document Updates

**Process**:
```markdown
## Updates Log

### Version 1.1 (2025-11-07)

Changes:
- Added Quick Reference section (user experience)
- Enhanced examples in Operation 2 (clarity)
- Fixed vague validation criteria (quality)

Impact:
- Usability improved (Quick Reference)
- Clarity improved (better examples)
- Validation more measurable

Validation: Passed skill-validator, structure score 5/5
```

---

## Quick Reference

### Update Workflow

```
Plan → Backup → Apply → Validate → Document
```

### Common Update Types

- Add Quick Reference (UX improvement)
- Enhance examples (clarity)
- Fix validation criteria (make specific)
- Add error handling (completeness)
- Optimize structure (progressive disclosure)

---

**skill-updater enables systematic, validated improvement of existing skills.**
