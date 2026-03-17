---
name: manage-skills
description: Manage and maintain VRP Toolkit skills through compliance checking, audit tracking, and documentation synchronization. Use when (1) adding or modifying skills, (2) checking skill compliance with project standards, (3) auditing SKILLS.md vs skills directory consistency, (4) recording skill changes to SKILLS_LOG.md, or (5) performing periodic skill health checks. Ensures skills stay independent, under 500 lines, properly structured, and well-documented.
---

# Manage Skills

Meta-skill for managing, auditing, and maintaining all VRP Toolkit skills.

## Core Functions

### 1. Audit Skills Directory
Compare actual skills in `.claude/skills/` with SKILLS.md documentation.

**Usage:**
```bash
python .claude/skills/manage-skills/scripts/audit_skills.py
```

**Reports:**
- Skills in directory vs SKILLS.md
- Missing from documentation
- Missing from directory
- Sync status

### 2. Check Skill Compliance
Validate skills against VRP Toolkit standards.

**Usage:**
```bash
# Check specific skill
python .claude/skills/manage-skills/scripts/check_compliance.py skill-name

# Check all skills
python .claude/skills/manage-skills/scripts/check_compliance.py --all
```

**Checks:**
- **Independence**: Skill doesn't embed other skills' content
- **Size**: SKILL.md ≤ 500 lines (body, excluding frontmatter)
- **Structure**: Required files present, no prohibited files
- **Frontmatter**: Valid YAML with name and description
- **References**: All reference files mentioned in SKILL.md

See [compliance_checklist.md](references/compliance_checklist.md) for detailed standards.

### 3. Update SKILLS.md Index
Sync skills documentation in SKILLS.md with actual skills.

**When:**
- After adding new skill
- After removing skill
- After significantly modifying skill description

**See:** [update_procedures.md](references/update_procedures.md) → Section 1

### 4. Record Changes in SKILLS_LOG.md
Log all skill modifications for tracking and history.

**When:**
- After any skill change (add/update/remove/rename/split/merge)

**Template:**
```markdown
## YYYY-MM-DD - [Action]: [skill-name]
**Action:** [Added/Updated/Removed/Renamed/Split/Merged]
**Reason:** [Why this change was made]
**Changes:**
- [Specific change 1]
- [Specific change 2]
**Compliance Notes:** [Any compliance issues addressed]
**Impact:** [How this affects other skills or workflows]
```

**See:** [update_procedures.md](references/update_procedures.md) → Section 2

## Workflow Patterns

### Pattern A: Add New Skill
```
1. Create skill using skill-creator
2. Run: audit_skills.py
   → Check if new skill appears in directory
3. Update SKILLS.md skills index (Section 1)
4. Record in SKILLS_LOG.md
5. Run: check_compliance.py skill-name
   → Verify new skill is compliant
```

### Pattern B: Modify Existing Skill
```
1. Make changes to skill
2. Run: check_compliance.py skill-name
   → Check for violations (size, independence, etc.)
3. If issues found, fix them
4. Update SKILLS.md description if needed
5. Record changes in SKILLS_LOG.md
```

### Pattern C: Periodic Audit
```
1. Run: audit_skills.py
   → Check directory vs SKILLS.md sync
2. Run: check_compliance.py --all
   → Check all skills for compliance
3. Review warnings and errors
4. Plan fixes or improvements
5. Update SKILLS_LOG.md with findings
```

### Pattern D: Fix Compliance Issues

**Size Violation (>500 lines):**
```
1. Identify extractable sections
2. Move to references/ or create new skill
3. Update SKILL.md references
4. Re-run check_compliance.py
5. Record in SKILLS_LOG.md
```

**Independence Violation:**
```
1. Find embedded content from other skills
2. Replace with reference: "See [skill-name] for..."
3. Re-run check_compliance.py
4. Record in SKILLS_LOG.md
```

See [update_procedures.md](references/update_procedures.md) for detailed procedures on:
- Renaming skills
- Splitting large skills
- Merging similar skills
- Archiving deprecated skills

## Integration with Other Skills

**Works with:**
- **skill-creator** - Use to create new skills before managing them
- **update-migration-log** - Similar logging pattern for migrations
- **update-task-board** - Similar documentation sync pattern

**DO NOT embed workflows from these skills** - Reference them instead.

## Compliance Standards Quick Reference

```yaml
Independence:
  ✓ Can reference other skills: "See [skill-name] for..."
  ✗ Cannot embed workflows from other skills

Size:
  ✓ SKILL.md ≤ 500 lines (excluding frontmatter)
  ⚠ Warning at 400 lines
  ✗ Error at 500 lines

Structure:
  ✓ Required: SKILL.md with valid frontmatter
  ✓ Optional: scripts/, references/, assets/
  ✗ Prohibited: README.md, CHANGELOG.md, etc.

Frontmatter:
  ✓ Required fields: name, description
  ✓ Description: 50-200 words with use cases
  ✗ Extra fields discouraged

References:
  ✓ All refs linked from SKILL.md
  ✓ Max 1 level deep (no nested dirs)
  ⚠ Warning if ref >500 lines
```

Full details: [compliance_checklist.md](references/compliance_checklist.md)

## Files in This Skill

```
manage-skills/
├── SKILL.md                          # This file
├── scripts/
│   ├── audit_skills.py              # Directory vs CLAUDE.md audit
│   └── check_compliance.py          # Compliance validation
├── references/
│   ├── compliance_checklist.md      # Detailed compliance standards
│   └── update_procedures.md         # Step-by-step update procedures
└── assets/
    └── SKILLS_LOG_template.md       # Template for SKILLS_LOG.md
```

## Tips

1. **Run audit after adding skills** - Catches missing documentation immediately
2. **Check compliance before packaging** - Prevents distribution of non-compliant skills
3. **Keep SKILLS_LOG.md updated** - Provides history for troubleshooting
4. **Review warnings seriously** - They often indicate real issues
5. **Split before 500 lines** - Easier to split at 400 than fix at 600

## Limitations

- Does not automatically fix compliance issues (manual fixes required)
- Cannot detect semantic overlap between skills (manual review needed)
- Windows encoding issues with emoji in scripts (uses ASCII fallback)
