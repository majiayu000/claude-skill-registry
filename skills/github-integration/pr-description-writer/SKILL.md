---
name: pr-description-writer
description: Writes and verifies GitHub pull request descriptions with zero fabrication tolerance. Discovers project PR templates, generates descriptions from git changes, and applies technical documentation verification standards. Use when creating PR descriptions (automatically invoked by create-pr skill), verifying PR descriptions, updating PR descriptions after additional changes, discovering templates, or when user requests "write PR description" or "verify PR description".
version: 1.0.0
---

# PR Description Writer Skill

## Purpose

Write and verify GitHub pull request descriptions following project templates with zero fabrication tolerance. Ensures all claims are backed by actual code changes and applies technical documentation verification standards to prevent marketing language and unverified claims.

## Two Modes of Operation

### Create Mode (Default)

Generate new PR description from git changes:

- Analyze git diff and commit history
- Follow project PR template if found
- Verify all claims against actual changes
- Generate markdown for `gh pr create --body`

### Verify Mode

Audit existing PR description for accuracy:

- Compare description claims against git changes
- Flag fabricated features or unverified claims
- Identify marketing language
- Report verification findings

## Core Workflow

### Quick 5-Phase Process

1. **Template Discovery** - Find PR template in .github/ or docs/
2. **Change Analysis** - Analyze git diff and commit history
3. **Description Generation** - Populate template sections with verified content
4. **Verification** - Run comprehensive verification checklist (P0/P1/P2)
5. **Output Generation** - Generate final PR description with verification metadata

**For detailed step-by-step instructions for each phase, see `references/WORKFLOW-PHASES.md`.**

## Template Sections Reference

### Standard Sections (Industry Best Practices 2025)

#### Required Sections

1. **Summary** - Brief overview (1-3 bullets)
2. **Changes** - Technical details of modifications
3. **Testing** - How changes were tested
4. **Related Issues** - Closes/Fixes/Relates to syntax
5. **Checklist** - Pre-submission verification

#### Conditional Sections

6. **Breaking Changes** - Only if backwards-incompatible
7. **Migration Guide** - If breaking changes exist
8. **Performance Impact** - Only with benchmark evidence

#### Optional Sections

9. **Screenshots** - For UI changes
10. **Security Considerations** - For security-related changes
11. **Deployment Notes** - Special deployment instructions
12. **Rollback Plan** - How to revert if needed

## Critical Verification Rules

### Zero Fabrication Policy - Must Verify Against git diff

**P0 - CRITICAL (Block PR Creation)**:

- Never fabricate features, files, methods, or APIs
- Never claim performance improvements without benchmarks
- Never fabricate test coverage numbers
- All code references must match git diff

**P1 - HIGH (Should Fix)**:

- No marketing buzzwords (enterprise, blazing, cutting-edge, etc.)
- No decorative emojis in technical text
- Technical descriptions only

**For detailed verification rules with examples and violations, see `references/VERIFICATION-RULES.md`.**

## Common Issues and Solutions

### Issue: Nil Pointer in Template Parsing

```markdown
Problem: Template has nested YAML front matter
Solution: Parse only markdown headers, ignore YAML
```

### Issue: Multiple PR Templates

```markdown
Problem: .github/PULL_REQUEST_TEMPLATE/ contains multiple files
Solution: Use default.md or ask user which template
```

### Issue: No Git History Available

```markdown
Problem: New repository or shallow clone
Solution: Require full git history, inform user
```

### Issue: Conflicting Commit Messages

```markdown
Problem: Commits say different things about same change
Solution: Analyze actual code changes, use most recent commit message
```

## Integration with Other Skills

### Invoked By:

- **create-pr** skill (Step 6: Generate PR Description)
- User (manual invocation)

### Invokes:

- None (uses git commands via Bash tool)

### Works With:

- **check-history** - Provides git context
- **api-documentation-verify** - Verification pattern reference
- **safe-commit** - Commit messages already verified

### Integration in create-pr Flow:

**Before** (current):

```
create-pr Step 6: Generate PR description (embedded logic)
```

**After** (new):

```
create-pr Step 6: Invoke pr-description-writer skill
  ├─> Input: base branch, commit range, template
  ├─> Process: Analyze, verify, generate
  └─> Output: Verified PR description markdown
```

## Example Usage

### Automatic Invocation (via create-pr)

```bash
User: "create a PR"
Assistant: [create-pr invokes pr-description-writer automatically]

# pr-description-writer executes:
# 1. Finds .github/PULL_REQUEST_TEMPLATE.md
# 2. Analyzes git diff main...feature-branch
# 3. Generates verified description
# 4. Returns to create-pr for gh pr create
```

### Manual Creation

```bash
User: "write a PR description for my changes"
Assistant: "I'll use pr-description-writer to create a verified PR description"

# Skill executes in create mode:
# 1. Discovers template
# 2. Analyzes current branch vs main
# 3. Generates description
# 4. Outputs markdown
```

### Verification Mode

```bash
User: "verify the PR description for #47"
Assistant: "I'll verify the PR description against actual changes"

# Skill executes in verify mode:
# 1. Fetches PR description from GitHub
# 2. Gets PR branch and diff
# 3. Verifies all claims
# 4. Reports findings
```

## Time Estimates

**Create Mode**:

- Small PR (1-5 files, 1-3 commits): 10-15 minutes
- Medium PR (5-15 files, 3-10 commits): 15-25 minutes
- Large PR (15+ files, 10+ commits): 25-40 minutes

**Verify Mode**:

- Review existing description: 5-10 minutes

## Success Criteria

A PR description is complete and verified when:

- ✅ All template sections populated accurately
- ✅ All claims verified against git diff
- ✅ No fabricated features or methods
- ✅ No unverified performance claims
- ✅ No fabricated timing numbers
- ✅ No marketing language or buzzwords
- ✅ Test coverage numbers match actual results (or not specified)
- ✅ All mentioned files exist in git diff
- ✅ Breaking changes documented accurately (if any)
- ✅ Related issues linked correctly
- ✅ Checklist reflects actual status
- ✅ Technical descriptions only
- ✅ Verification metadata included

## Output Format

### Create Mode Output

```markdown
[Complete PR description following template]

<!-- All sections populated -->
<!-- All claims verified -->
<!-- Ready for gh pr create --body -->
```

### Verify Mode Output

```markdown
## PR Description Verification Report

**PR**: #47
**Status**: ✅ PASSED / ⚠️ WARNINGS / ❌ FAILED

### P0 Issues (Must Fix)

- None

### P1 Issues (Should Fix)

- Line 15: Marketing buzzword "enterprise-grade"
- Line 23: Unverified performance claim "10x faster"

### P2 Issues (Consider)

- Breaking changes section could be more detailed

### Recommendations

1. Remove marketing language
2. Replace performance claim with architectural fact
3. Expand breaking changes documentation

**Files Verified**: 12 files
**Claims Verified**: 18 claims
**Verification Date**: 2025-01-12T10:30:00Z
```

## References

- Technical Documentation Expert Agent (verification patterns)
- API Documentation Verify Skill (verification checklist)
- GitHub PR Best Practices: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests
- Semantic PR Guidelines: https://www.conventionalcommits.org/
- Zero Fabrication Policy: Based on technical-documentation-expert (lines 13-35, 239-340)

---

**Maintained by**: Engineering team
**Review Schedule**: Quarterly
**Last Updated**: 2025-01-12
