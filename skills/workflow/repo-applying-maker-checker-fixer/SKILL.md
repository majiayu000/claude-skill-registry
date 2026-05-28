---
description: Three-stage content quality workflow pattern (Maker creates, Checker validates, Fixer remediates). Use when working with content quality workflows, validation processes, audit reports, or implementing maker/checker/fixer agent roles.
---

# Maker-Checker-Fixer Pattern

This Skill provides guidance on the three-stage content quality workflow pattern used across repository agent families for systematic content creation, validation, and remediation.

## Purpose

Use this Skill when:

- Implementing content quality workflows
- Working with maker/checker/fixer agents
- Validating content against conventions
- Applying validated fixes from audit reports
- Understanding agent family structures
- Deciding when to use maker vs fixer for content changes

## The Three Stages

### Stage 1: Maker (Content Creation & Updates)

**Role**: Creates NEW content and updates EXISTING content with all dependencies

**Characteristics**:

- User-driven operation (responds to "create" or "update" requests)
- Comprehensive scope (creates target content AND updates related files)
- Cascading changes (adjusts indices, cross-references, dependencies)
- Proactive management (anticipates what needs updating)

**Tool Pattern**: `Write`, `Edit` (content modification)

**Color**: Blue (writer agents) or Yellow (special case: wow\_\_rules-maker uses bash)

**When to Use Maker**:

- User explicitly requests content creation or updates
- Creating NEW content from scratch
- Making significant changes to EXISTING content
- Need comprehensive dependency management
- User-driven workflow (user says "create" or "update")

**Example Workflow**:

```markdown
User: "Create new TypeScript generics tutorial"

Maker:

1. Creates main content file
2. Creates bilingual version (if applicable)
3. Updates navigation files
4. Ensures overview/index links correct
5. Follows weight ordering convention
6. Uses accessible colors in diagrams
7. Validates all internal links
8. Delivers complete, ready-to-publish content
```

### Stage 2: Checker (Validation)

**Role**: Validates content against conventions and generates audit reports

**Characteristics**:

- Validation-driven (analyzes existing content)
- Non-destructive (does NOT modify files being checked)
- Comprehensive reporting (generates detailed audit in `generated-reports/`)
- Evidence-based (re-validation in fixer prevents false positives)

**Tool Pattern**: `Read`, `Glob`, `Grep`, `Write`, `Bash` (read-only + report generation)

- `Write` needed for audit report files
- `Bash` needed for UTC+7 timestamps

**Color**: Green (checker agents)

**When to Use Checker**:

- ✅ REQUIRED: New content created from scratch
- ✅ REQUIRED: Major refactoring or updates
- ✅ REQUIRED: Before publishing to production
- ✅ REQUIRED: Complex content (tutorials, Hugo)
- ✅ REQUIRED: Critical files (AGENTS.md, conventions)
- ⚠️ OPTIONAL: Small updates to high-quality content

**Criticality Categorization**:

Checkers categorize findings by importance/urgency:

- 🔴 **CRITICAL** - Breaks functionality, blocks users (must fix before publication)
- 🟠 **HIGH** - Significant quality degradation, convention violations (should fix)
- 🟡 **MEDIUM** - Minor quality issues, style inconsistencies (fix when convenient)
- 🟢 **LOW** - Suggestions, optional improvements (consider for future)

**Report Format**: Findings grouped by criticality with emoji indicators

**Example Workflow**:

```markdown
User: "Check the new TypeScript tutorial"

Checker:

1. Reads tutorial file
2. Validates frontmatter (date format, required fields, weight)
3. Checks content structure (heading hierarchy, links)
4. Validates Hugo conventions (absolute paths, no .md)
5. Checks content quality (alt text, accessible colors)
6. Generates audit report: generated-reports/ayokoding-web\_\_2025-12-14--20-45\_\_audit.md
7. Reports findings summary in conversation
8. Does NOT modify the tutorial file
```

### Stage 3: Fixer (Remediation)

**Role**: Applies validated fixes from checker audit reports

**Characteristics**:

- Validation-driven (works from audit reports, not user requests)
- Re-validation before fixing (confirms issues still exist)
- Confidence-based (only applies HIGH confidence fixes automatically)
- Safe application (skips MEDIUM and FALSE_POSITIVE)
- Audit trail (generates fix reports for transparency)

**Tool Pattern**: `Read`, `Edit`, `Glob`, `Grep`, `Write`, `Bash`

- `Edit` for applying fixes (NOT `Write`)
- `Write` for fix report generation
- `Bash` for timestamps

**Color**: Purple (fixer agents)

**When to Use Fixer**:

- ✅ Checker has generated an audit report
- ✅ Issues are convention violations (not content gaps)
- ✅ Fixes are mechanical (field values, formatting)
- ✅ Validation-driven workflow

**When to SKIP Fixer (Manual Preferred)**:

- ❌ Issues require human judgment (narrative quality)
- ❌ Fixes are context-dependent
- ❌ Checker reports unclear/ambiguous
- ❌ User prefers manual control

**Priority-Based Execution**:

Fixers combine criticality (importance) × confidence (certainty) → priority:

| Priority         | Combination                      | Action                               |
| ---------------- | -------------------------------- | ------------------------------------ |
| **P0** (Blocker) | CRITICAL + HIGH                  | Auto-fix immediately, block if fails |
| **P1** (Urgent)  | HIGH + HIGH OR CRITICAL + MEDIUM | Auto-fix or urgent review            |
| **P2** (Normal)  | MEDIUM + HIGH OR HIGH + MEDIUM   | Auto-fix (if approved) or review     |
| **P3-P4** (Low)  | LOW combinations                 | Suggestions only                     |

**Execution Order**: P0 → P1 → P2 → P3-P4

**Example Workflow**:

```markdown
User: "Apply fixes from latest ayokoding-web audit"

Fixer:

1. Auto-detects latest: generated-reports/ayokoding-web\_\_2025-12-14--20-45\_\_audit.md
2. Parses findings (25 issues)
3. Re-validates each finding:
   - 18 findings → HIGH confidence (apply)
   - 4 findings → MEDIUM confidence (skip, manual review)
   - 3 findings → FALSE_POSITIVE (skip, report for checker improvement)
4. Applies 18 fixes
5. Generates fix report: generated-reports/ayokoding-web\_\_2025-12-14--20-45\_\_fix.md
6. Summary: 18 fixed, 4 manual review, 3 false positives
```

## Common Workflows

### Basic: Create → Validate → Fix

```
1. User: "Create new tutorial"
2. Maker: Creates content + dependencies
3. User: Reviews, looks good
4. Checker: Validates, finds minor issues
5. User: Reviews audit, approves fixes
6. Fixer: Applies validated fixes
7. Done: Production-ready
```

### Iterative: Maker → Checker → Fixer → Checker

```
1. User: "Update existing content"
2. Maker: Updates content + dependencies
3. Checker: Validates, finds issues
4. User: Reviews audit, approves fixes
5. Fixer: Applies fixes
6. Checker: Re-validates to confirm
7. Done: Content verified clean
```

**When to use**: Critical content, major refactoring, uncertain fixer confidence

## Agent Families Using This Pattern

Seven agent families implement this pattern:

1. **repo-rules-\*** - Repository-wide consistency
2. **ayokoding-web-\*** - Hugo content (ayokoding-web)
3. **docs-tutorial-\*** - Tutorial quality
4. **ose-platform-web-content-\*** - Hugo content (ose-platform-web)
5. **readme-\*** - README quality
6. **docs-\*** - Documentation factual accuracy
7. **plan-\*** - Plan completeness and structure

Each family has:

- **Maker** (Blue) - Creates/updates content
- **Checker** (Green) - Validates, generates audits
- **Fixer** (Purple/Yellow) - Applies validated fixes

## Best Practices

1. **Always run checker before publication** - Catches issues early
2. **Review audit reports before fixing** - Understand what will change
3. **Use maker for user-driven creation** - Not fixer
4. **Use fixer for validation-driven fixes** - Not maker
5. **Re-run checker after major fixes** - Verify fixes worked
6. **Report false positives** - Improves checker accuracy over time

## Common Mistakes

- ❌ **Using fixer for content creation** - Use maker instead (fixer is for fixing issues, not creating)
- ❌ **Skipping checker validation** - Always validate before publication
- ❌ **Manual fixes for mechanical issues** - Use fixer for efficiency
- ❌ **Auto-applying MEDIUM confidence fixes** - Needs manual review
- ❌ **Not re-validating before fixing** - Prevents false positive fixes

## Integration with Conventions

The pattern integrates with:

- **[Criticality Levels Convention](../../../../governance/development/quality/criticality-levels.md)** - Checkers categorize by criticality, fixers use for priority
- **[Fixer Confidence Levels Convention](../../../../governance/development/quality/fixer-confidence-levels.md)** - Fixers assess confidence, combine with criticality
- **[Temporary Files Convention](../../../../governance/development/infra/temporary-files.md)** - Checker/fixer reports stored in `generated-reports/`
- **[Repository Validation Methodology](../../../../governance/development/quality/repository-validation.md)** - Standard validation patterns
- **[AI Agents Convention](../../../../governance/development/agents/ai-agents.md)** - Agent structure, tool permissions, color coding

## References

- **[Maker-Checker-Fixer Pattern Convention](../../../../governance/development/pattern/maker-checker-fixer.md)** - Complete pattern documentation
- **[Criticality Levels Convention](../../../../governance/development/quality/criticality-levels.md)** - Severity classification
- **[Fixer Confidence Levels Convention](../../../../governance/development/quality/fixer-confidence-levels.md)** - Confidence assessment

## Related Skills

- `criticality-confidence-system` (Phase 2) - Deep dive into criticality/confidence levels and priority matrix
- `repository-architecture` - Understanding the six-layer governance and where patterns fit

---

**Note**: This Skill provides action-oriented guidance. The authoritative convention document contains complete implementation details, examples, and all seven agent families.
