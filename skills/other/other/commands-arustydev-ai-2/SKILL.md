---
description: Review and refine a skill to follow best practices including progressive disclosure, token budgets, and proper structure
argument-hint: <skill-path> [--check-only] [--create-issues]
---

# Refine Skill

Review and refine a Claude Code skill to follow best practices from the [official documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## Arguments

- `$1` - Path to skill directory (required). Example: `components/skills/my-skill`
- `--check-only` - Only analyze, don't make changes (optional)
- `--create-issues` - Create GitHub issues for findings (optional)

## Workflow

### Phase 1: Validate Skill Exists

1. Check if `$1/SKILL.md` exists
2. If not found, report error and suggest correct path
3. Read SKILL.md to understand current structure

### Phase 2: Structural Analysis

Use TodoWrite to track issues found.

**Check these criteria:**

#### 2.1 Token Budget (Critical)

> **See:** [meta-skill-validation-dev/checklists/structure.md](../skills/meta-skill-validation-dev/checklists/structure.md) for thresholds and progressive disclosure patterns.

If over budget (> 500 lines), identify content to split using progressive disclosure.

#### 2.2 Description Quality

> **See:** [meta-skill-validation-dev/checklists/frontmatter.md](../skills/meta-skill-validation-dev/checklists/frontmatter.md) for description requirements, trigger words, and voice guidelines.

#### 2.3 Progressive Disclosure Patterns

> **See:** [meta-skill-validation-dev/checklists/structure.md](../skills/meta-skill-validation-dev/checklists/structure.md) for patterns and directory structure expectations.

#### 2.4 Content Quality Checklist

> **See:** [meta-skill-validation-dev/checklists/quality.md](../skills/meta-skill-validation-dev/checklists/quality.md) for content quality criteria including templates, examples, terminology, and portability checks.

#### 2.5 Script Quality (if applicable)

If `scripts/` exists, check:

| Criterion               | Check                                       |
| ----------------------- | ------------------------------------------- |
| Dependencies documented | README or requirements.txt exists           |
| Executable              | Has shebang or clear execution instructions |
| Verifiable output       | Creates intermediate outputs for debugging  |

### Phase 3: Generate Report

Create a structured analysis report:

```markdown
# Skill Analysis: <skill-name>

## Summary

| Metric                 | Status   | Value        |
| ---------------------- | -------- | ------------ |
| SKILL.md lines         | ✅/⚠️/❌ | X lines      |
| Description            | ✅/⚠️/❌ | <assessment> |
| Structure              | ✅/⚠️/❌ | <assessment> |
| Progressive disclosure | ✅/⚠️/❌ | <assessment> |

## Issues Found

### Critical (Must Fix)

- [ ] Issue 1
- [ ] Issue 2

### Warnings (Should Fix)

- [ ] Warning 1
- [ ] Warning 2

### Suggestions (Nice to Have)

- [ ] Suggestion 1

## Recommended Changes

<Specific, actionable recommendations>
```

### Phase 4: Apply Refinements (if not --check-only)

If issues were found and `--check-only` was NOT specified:

1. **Ask for confirmation** before making changes
2. Apply changes in order of priority:
   - Critical issues first
   - Warnings second
   - Suggestions only if requested

**Common refinements:**

#### Split oversized SKILL.md

If > 500 lines, identify content to move:

| Content Type           | Move To                   |
| ---------------------- | ------------------------- |
| Detailed examples      | `examples/`               |
| Reference tables       | `tables/` or `reference/` |
| Deep-dive explanations | `reference/`              |
| Templates/checklists   | `FORMS.md`                |
| Code samples           | `examples/`               |

Replace moved content with navigation links:

```markdown
> **See also:** [reference/detailed-topic.md](./reference/detailed-topic.md)
```

#### Add table of contents

For reference files > 100 lines, add TOC:

```markdown
## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
```

#### Improve description

Transform vague descriptions:

```yaml
# Before
description: Helps with code conversion

# After
description: Guide for translating code between programming languages. Use when converting code, planning migrations, or looking up type/idiom mappings.
```

#### Add navigation section

Add Quick Navigation to SKILL.md:

```markdown
## Quick Navigation

| Resource                   | Purpose                  |
| -------------------------- | ------------------------ |
| [FORMS.md](./FORMS.md)     | Templates and checklists |
| [examples/](./examples/)   | Code examples            |
| [reference/](./reference/) | Deep-dive documentation  |
```

### Phase 5: Validate Changes

After applying refinements:

1. Re-run Phase 2 checks
2. Verify all critical issues resolved
3. Report final status

### Phase 6: Create GitHub Issues (if --create-issues)

If `--create-issues` flag is specified, create issues for each finding.

#### 6.1 Determine Repository

1. Check if in a git repository: `git rev-parse --is-inside-work-tree`
2. Get remote URL: `git remote get-url origin`
3. Parse owner/repo from URL

#### 6.2 Issue Templates and Creation

> **See:** [meta-skill-validation-dev/templates/issue-templates.md](../skills/meta-skill-validation-dev/templates/issue-templates.md) for:
> - Issue categorization (Critical/Warning/Suggestion)
> - Issue body templates
> - Title format conventions
> - Batch vs individual issue strategy
> - Umbrella issue template for 7+ findings

**Create issues using:**

```bash
gh issue create \
  --repo <owner>/<repo> \
  --title "<type>(skills): <skill-name> <brief-description>" \
  --body "<issue-body>" \
  --label "skills,<severity-label>"
```

#### 6.3 Report Created Issues

After creating issues, report:

```markdown
## GitHub Issues Created

| Issue | Type | Title |
|-------|------|-------|
| #123 | fix | fix(skills): my-skill exceeds 500 line budget |
| #124 | enhance | enhance(skills): my-skill add navigation section |
| #125 | docs | docs(skills): my-skill improve description |

**Next steps:**
1. Review created issues
2. Prioritize and assign
3. Address in order of severity
```

## Examples

```bash
# Analyze a skill (no changes)
/refine-skill components/skills/my-skill --check-only

# Analyze and apply refinements
/refine-skill components/skills/my-skill

# Refine a skill in current directory
/refine-skill .

# Analyze and create GitHub issues for findings
/refine-skill components/skills/my-skill --create-issues

# Check only + create issues (no local changes, just report and track)
/refine-skill components/skills/my-skill --check-only --create-issues

# Batch analyze multiple skills and create issues
for skill in components/skills/*/; do
  /refine-skill "$skill" --check-only --create-issues
done
```

## Quality Checklist Reference

> **See:** [meta-skill-validation-dev](../skills/meta-skill-validation-dev/) for complete checklists:
> - [checklists/frontmatter.md](../skills/meta-skill-validation-dev/checklists/frontmatter.md) - Name and description
> - [checklists/structure.md](../skills/meta-skill-validation-dev/checklists/structure.md) - Token budget, progressive disclosure
> - [checklists/quality.md](../skills/meta-skill-validation-dev/checklists/quality.md) - Content quality
> - [checklists/8-pillars.md](../skills/meta-skill-validation-dev/checklists/8-pillars.md) - Pillar coverage (lang/convert skills)

## Notes

- Always backup before major refactoring
- Some skills may intentionally be compact and not need splitting
- Prioritize readability over strict line counts
- Consider the 8-pillar framework for conversion skills

### GitHub Integration

- Requires `gh` CLI authenticated or GitHub MCP server configured
- Issues are created in the repository where the skill lives
- Labels (`skills`, `bug`, `enhancement`, `documentation`) are created if they don't exist
- Use `--check-only --create-issues` to track without making local changes
- Umbrella issues link related findings for easier project management

## References

| Resource | Purpose |
|----------|---------|
| [meta-skill-validation-dev](../skills/meta-skill-validation-dev/) | Shared validation checklists and issue templates |
| [meta-skill-authoring-dev](../skills/meta-skill-authoring-dev/) | Guidance for creating new skills |
| [Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) | Official Claude Code documentation |
