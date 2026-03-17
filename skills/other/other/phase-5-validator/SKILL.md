---
name: phase-5-validator
description: Validates Finalization Phase completion before workflow concludes. Checks documentation updates, file registry, git commits, deployment readiness, and lessons learned contributions.
---

# Phase 5 (Finalization) Validation Skill

**Purpose**: Automate validation that all work is properly documented, committed, and ready for deployment/handoff.

**When to Use**: Final validation before marking workflow complete.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage (no parameters required)
bash .claude/skills/phase-5-validator/execute.sh

# Show help
bash .claude/skills/phase-5-validator/execute.sh --help
```

**Parameters**:
- No parameters required - validates current project state

**Script validates**:
- 🚨 BLOCKING: Single source of truth (no bash duplication in skills)
- 🚨 BLOCKING: Lessons learned file sizes (max 2,000 lines)
- Git & version control (commits, messages, branch status, conflicts)
- Documentation (file registry, PROGRESS.md, feature docs, CLAUDE.md)
- Lessons learned (new entries, format, cross-references)
- Deployment readiness (tests passing, no blocking issues, deployment notes)
- Cleanup (temp files, session work, orphaned files)

**Exit codes**:
- 0: Finalization complete, workflow can conclude
- 1: BLOCKING violations OR quality gates not met

**CRITICAL**: This validator has BLOCKING AUTHORITY and can prevent workflow completion.

## Quality Gate Checklist

### 🚨 Single Source of Truth (BLOCKING - Not Scored)
- [ ] **ALL skills validated for duplication** (MANDATORY)
- [ ] No bash command duplication in agent definitions
- [ ] No procedural duplication in lessons learned
- [ ] No automation duplication in process docs
- [ ] Skills properly referenced (not duplicated)

**CRITICAL**: This check runs FIRST with BLOCKING AUTHORITY.
**Any violations = immediate failure before scoring begins.**

---

### 🚨 Lessons File Sizes (BLOCKING - Not Scored)
- [ ] **ALL lessons files checked for size** (MANDATORY)
- [ ] No files exceeding 1700 line maximum
- [ ] Files approaching 90% threshold identified
- [ ] Multi-file structure properly maintained
- [ ] Size violations provide split instructions

**CRITICAL**: This check runs SECOND with BLOCKING AUTHORITY.
**Files exceeding 1700 lines = immediate failure before scoring begins.**

---

### Git & Version Control (25 points)
- [ ] All changes committed (10 points)
- [ ] Commit messages follow standards (5 points)
- [ ] Branch is up to date (5 points)
- [ ] No merge conflicts (5 points)

### Documentation (30 points)
- [ ] File registry updated (10 points)
- [ ] PROGRESS.md updated (5 points)
- [ ] Feature documentation complete (10 points)
- [ ] CLAUDE.md updated if needed (5 points)

### Lessons Learned (20 points)
- [ ] New lessons documented (10 points)
- [ ] Lessons follow format (5 points)
- [ ] Cross-references added (5 points)

### Deployment Readiness (15 points)
- [ ] All tests passing (5 points)
- [ ] No blocking issues (5 points)
- [ ] Deployment notes present (5 points)

### Cleanup (10 points)
- [ ] Temporary files removed (3 points)
- [ ] Session work archived (3 points)
- [ ] Orphaned files resolved (4 points)

## Usage Examples

### From Orchestrator
```
Use the phase-5-validator skill to check if work is ready to finalize
```

### Manual Validation
```bash
# Run finalization validation
bash .claude/skills/phase-5-validator.md
```

## Common Issues

### Issue: File Registry Not Updated
**CRITICAL**: Every file operation must be logged.

**Solution**:
```bash
# Update file registry
echo "| $(date +%Y-%m-%d) | /path/to/file | CREATED | Purpose | Task | ACTIVE | - |" >> docs/architecture/file-registry.md
```

### Issue: Uncommitted Changes
**Solution**:
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "feat: implement user management feature

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Issue: Missing Documentation
**Required documents**:
- business-requirements.md
- functional-spec.md
- database-design.md
- ui-ux-design.md
- implementation-notes.md
- deployment-notes.md

### Issue: Temporary Files
**Solution**:
```bash
# Find and remove
find . -name "*.tmp" -delete
find . -name "*.bak" -delete

# Or move to session-work
mkdir -p session-work/$(date +%Y-%m-%d)
mv status.md session-work/$(date +%Y-%m-%d)/
```

## Mandatory Finalization Checklist

Before marking workflow complete:

0. **🚨 Single Source of Truth (BLOCKING - FIRST CHECK)**
   - [ ] ALL skills validated for duplication (MANDATORY)
   - [ ] No bash commands duplicated in agent definitions
   - [ ] No procedures duplicated in lessons learned
   - [ ] No automation duplicated in process docs
   - [ ] Skills properly referenced from other docs
   - **ANY VIOLATIONS = IMMEDIATE WORKFLOW FAILURE**

1. **Git**
   - [ ] All changes committed
   - [ ] Commit messages follow standards
   - [ ] Branch clean (no conflicts)

2. **Documentation**
   - [ ] File registry current
   - [ ] Feature docs complete
   - [ ] PROGRESS.md updated
   - [ ] Deployment notes written

3. **Lessons Learned**
   - [ ] New patterns documented
   - [ ] Problems and solutions recorded
   - [ ] Cross-references added

4. **Quality**
   - [ ] All tests passing (100%)
   - [ ] No blocking issues
   - [ ] Code reviewed

5. **Cleanup**
   - [ ] Temporary files removed
   - [ ] Session work organized
   - [ ] No orphaned files

## Output Format

```json
{
  "phase": "finalization",
  "status": "pass|fail",
  "singleSourceOfTruth": {
    "validated": true,
    "skillsChecked": 13,
    "violations": 0,
    "blocking": false,
    "note": "CRITICAL: This check runs FIRST. Any violations = immediate failure."
  },
  "score": 87,
  "maxScore": 100,
  "percentage": 87,
  "requiredPercentage": 80,
  "git": {
    "uncommittedChanges": 0,
    "commitMessage": "standards-compliant",
    "upToDate": true,
    "conflicts": false
  },
  "documentation": {
    "fileRegistry": "updated",
    "progress": "updated",
    "featureDocs": "complete",
    "claude": "not-needed"
  },
  "lessonsLearned": {
    "newLessons": 2,
    "formatCompliant": true,
    "crossReferences": true
  },
  "deployment": {
    "testsPass": true,
    "blockingIssues": 0,
    "notesPresent": true
  },
  "cleanup": {
    "tempFiles": 0,
    "sessionWork": "organized",
    "orphanedFiles": 0
  },
  "readyToFinalize": true,
  "nextSteps": [
    "Deploy to staging (if approved)",
    "Close workflow",
    "Update project status"
  ]
}
```

## Integration with Quality Gates

Quality gate thresholds by work type:

- **Feature**: 80% required
- **Bug Fix**: 75% required
- **Hotfix**: 70% required
- **Documentation**: 90% required
- **Refactoring**: 85% required

## Progressive Disclosure

**Initial Context**: Show quick status check (committed, documented, tested)
**On Request**: Show full scoring breakdown
**On Failure**: Show specific missing items with actionable fixes
**On Pass**: Show next steps and finalization instructions

---

**Remember**: Finalization is about ensuring nothing is forgotten. Documentation, commits, and lessons learned ensure the work is sustainable and maintainable long-term.
