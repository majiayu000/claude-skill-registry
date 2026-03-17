---
name: skill-review
description: |
  Audit claude-skills repository documentation with systematic 9-phase review: standards compliance, official docs verification via Context7/WebFetch, code examples accuracy, cross-file consistency, and version drift detection. Auto-fixes unambiguous issues with severity classification.

  Use when: investigating skill issues, major package updates detected (e.g., v1.x → v2.x), skill not verified >90 days, before marketplace submission, or troubleshooting outdated API patterns, contradictory examples, broken links, version drift.

license: MIT
metadata:
  version: 1.0.0
  last_verified: 2025-11-08
  production_tested: better-auth v2.0.0 audit (2025-11-08)
  token_savings: ~80%
  errors_prevented: 20+
  official_docs: https://github.com/jezweb/claude-skills
  triggers:
    - "review this skill"
    - "review the X skill"
    - "audit the skill"
    - "check if X needs updates"
    - "is X skill current"
    - "verify X documentation"
    - "X skill seems outdated"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Edit
  - Write
---

# Skill Review Skill

## Overview

The skill-review skill provides a comprehensive, systematic process for auditing skills in the claude-skills repository. It combines automated technical validation with AI-powered verification to ensure skills remain accurate, current, and high-quality.

**Use this skill when**:
- Investigating suspected issues in a skill
- Major package version updates released (e.g., better-auth 1.x → 2.x)
- Skill last verified >90 days ago
- Before submitting skill to marketplace
- User reports errors following skill instructions
- Examples seem outdated or contradictory

**Production evidence**: Successfully audited better-auth skill (2025-11-08), found 6 critical/high issues including non-existent API imports, removed 665 lines of incorrect code, implemented v2.0.0 with correct patterns.

---

## Quick Start

### Invoke via Slash Command

```
/review-skill <skill-name>
```

**Example**:
```
/review-skill better-auth
```

### Invoke via Skill (Proactive)

When Claude notices potential issues, it can suggest:
```
User: "I'm having trouble with better-auth and D1"

Claude: "I notice the better-auth skill was last verified 6 months ago.
Would you like me to review it? Better-auth recently released v1.3
with D1 changes."
```

---

## What This Skill Does

### 9-Phase Systematic Audit

1. **Pre-Review Setup** (5-10 min)
   - Install skill locally: `./scripts/install-skill.sh <skill-name>`
   - Check current version and last verified date
   - Test skill discovery

2. **Standards Compliance** (10-15 min)
   - Validate YAML frontmatter (name, description, license)
   - Check keyword comprehensiveness
   - Verify third-person description style
   - Ensure directory structure matches spec

3. **Official Documentation Verification** (15-30 min)
   - Use Context7 MCP or WebFetch to verify API patterns
   - Check GitHub for recent updates and issues
   - Verify package versions against npm registry
   - Compare with production repositories

4. **Code Examples & Templates Audit** (20-40 min)
   - Verify import statements exist in current packages
   - Check API method signatures match official docs
   - Ensure schema consistency across files
   - Test templates build and run

5. **Cross-File Consistency** (15-25 min)
   - Compare SKILL.md vs README.md examples
   - Verify "Bundled Resources" section matches actual files
   - Ensure configuration examples consistent

6. **Dependencies & Versions** (10-15 min)
   - Run `./scripts/check-versions.sh <skill-name>`
   - Check for breaking changes in package updates
   - Verify "Last Verified" date is recent

7. **Issue Categorization** (10-20 min)
   - Classify by severity: 🔴 Critical / 🟡 High / 🟠 Medium / 🟢 Low
   - Document with evidence (GitHub URL, docs link, npm changelog)

8. **Fix Implementation** (30 min - 4 hours)
   - Auto-fix unambiguous issues
   - Ask user only for architectural decisions
   - Update all affected files consistently
   - Bump version if breaking changes

9. **Post-Fix Verification** (10-15 min)
   - Test skill discovery
   - Verify templates work
   - Check no contradictions remain
   - Commit with detailed changelog

### Automated Checks (via script)

The skill runs `./scripts/review-skill.sh <skill-name>` which checks:
- ✅ YAML frontmatter syntax and required fields
- ✅ Package version currency (npm)
- ✅ Broken links (HTTP status)
- ✅ TODO markers in code
- ✅ File organization (expected directories exist)
- ✅ "Last Verified" date staleness

### Manual Verification (AI-powered)

Claude performs:
- 🔍 API method verification against official docs
- 🔍 GitHub activity and issue checks
- 🔍 Production repository comparisons
- 🔍 Code example correctness
- 🔍 Schema consistency validation

---

## Process Workflow

### Step 1: Run Automated Checks

```bash
./scripts/review-skill.sh <skill-name>
```

Interpret output to identify technical issues.

### Step 2: Execute Manual Verification

For **Phase 3: Official Documentation Verification**:

1. Use Context7 MCP (if available):
   ```
   Use Context7 to fetch: /websites/<package-docs>
   Search for: [API method from skill]
   ```

2. Or use WebFetch:
   ```
   Fetch: https://<official-docs-url>
   Verify: [specific patterns]
   ```

3. Check GitHub:
   ```
   Visit: https://github.com/<org>/<repo>/commits/main
   Check: Last commit, recent changes
   Search issues: [keywords from skill]
   ```

4. Find production examples:
   ```
   WebSearch: "<package> cloudflare production github"
   Compare: Do real projects match our patterns?
   ```

For **Phase 4: Code Examples Audit**:

- Verify all imports exist (check official docs)
- Check API method signatures match
- Ensure schema consistency across files
- Test templates actually work

### Step 3: Categorize Issues

**🔴 CRITICAL** - Breaks functionality:
- Non-existent API methods/imports
- Invalid configuration
- Missing required dependencies

**🟡 HIGH** - Causes confusion:
- Contradictory examples across files
- Inconsistent patterns
- Outdated major versions

**🟠 MEDIUM** - Reduces quality:
- Stale minor versions (>90 days)
- Missing documentation sections
- Incomplete error lists

**🟢 LOW** - Polish issues:
- Typos, formatting inconsistencies
- Missing optional metadata

### Step 4: Fix Issues

**Auto-fix** when:
- ✅ Fix is unambiguous (correct import from docs)
- ✅ Evidence is clear
- ✅ No architectural impact

**Ask user** when:
- ❓ Multiple valid approaches
- ❓ Breaking change decision
- ❓ Architectural choice

**Format for questions**:
```
I found [issue]. There are [N] approaches:

1. [Approach A] - [Pros/Cons]
2. [Approach B] - [Pros/Cons]

Recommendation: [Default based on evidence]

Which would you prefer?
```

### Step 5: Version Bump Assessment

If breaking changes:
- Major: v1.0.0 → v2.0.0 (API patterns change)
- Minor: v1.0.0 → v1.1.0 (new features, backward compatible)
- Patch: v1.0.0 → v1.0.1 (bug fixes only)

### Step 6: Generate Audit Report

```markdown
## Skill Review Report: <skill-name>

**Date**: YYYY-MM-DD
**Trigger**: [Why review performed]
**Time Spent**: [Duration]

### Findings

🔴 CRITICAL (N): [List with evidence]
🟡 HIGH (N): [List with evidence]
🟠 MEDIUM (N): [List with evidence]
🟢 LOW (N): [List with evidence]

### Remediation

**Files Modified**: [List]
**Version Update**: [old] → [new]
**Breaking Changes**: Yes/No

### Verification

✅ Discovery test passed
✅ Templates work
✅ Committed: [hash]

### Recommendation

[Final assessment]
```

---

## Example: better-auth Audit

### Findings

**Issue #1: Non-existent d1Adapter** 🔴 CRITICAL

*Location*: `references/cloudflare-worker-example.ts:17`

*Problem*: Imports `d1Adapter` from `'better-auth/adapters/d1'` which doesn't exist

*Evidence*:
- Official docs: https://better-auth.com/docs/integrations/drizzle
- GitHub: No `d1Adapter` export in codebase
- Production: 4 repos use Drizzle/Kysely

*Fix*: Replace with `drizzleAdapter` from `'better-auth/adapters/drizzle'`

### Result

- **Files deleted**: 3 (obsolete patterns)
- **Files created**: 3 (correct patterns)
- **Lines changed**: +1,266 net
- **Version**: v1.0.0 → v2.0.0
- **Time**: 3.5 hours

---

## Bundled Resources

This skill references:

1. **`planning/SKILL_REVIEW_PROCESS.md`** - Complete 9-phase manual guide
2. **`scripts/review-skill.sh`** - Automated validation script
3. **`.claude/commands/review-skill.md`** - Slash command definition

---

## When Claude Should Invoke This Skill

**Proactive triggers**:
- User mentions skill seems outdated
- Package major version mentioned
- User reports errors following skill
- Checking metadata shows >90 days since verification

**Explicit triggers**:
- "review the X skill"
- "audit better-auth skill"
- "is cloudflare-worker-base up to date?"
- "check if tailwind-v4-shadcn needs updating"

---

## Token Efficiency

**Without this skill**: ~25,000 tokens
- Trial-and-error verification
- Repeated doc lookups
- Inconsistent fixes across files
- Missing evidence citations

**With this skill**: ~5,000 tokens
- Systematic process
- Clear decision trees
- Evidence-based fixes
- Comprehensive audit trail

**Savings**: ~80% (20,000 tokens)

---

## Common Issues Prevented

1. **Fake API adapters** - Non-existent imports
2. **Stale API methods** - Changed signatures
3. **Schema inconsistency** - Different table names
4. **Outdated scripts** - Deprecated approaches
5. **Version drift** - Packages >90 days old
6. **Contradictory examples** - Multiple conflicting patterns
7. **Broken links** - 404 documentation URLs
8. **YAML errors** - Invalid frontmatter syntax
9. **Missing keywords** - Poor discoverability
10. **Incomplete bundled resources** - Listed files don't exist

---

## Best Practices

1. **Always cite sources** - GitHub URL, docs link, npm changelog
2. **No assumptions** - Verify against current official docs
3. **Be systematic** - Follow all 9 phases
4. **Fix consistency** - Update all files, not just one
5. **Document thoroughly** - Detailed commit messages
6. **Test after fixes** - Verify skill still works

---

## Known Limitations

- Link checking requires network access
- Package version checks need npm installed
- Context7 MCP availability varies by package
- Production repo search may need GitHub API
- Manual phases require human judgment

---

## Version History

**v1.0.0** (2025-11-08)
- Initial release
- 9-phase systematic audit process
- Automated script + manual guide
- Slash command + skill wrapper
- Production-tested on better-auth v2.0.0 audit

---

## Additional Resources

- **Full Process Guide**: `planning/SKILL_REVIEW_PROCESS.md`
- **Repository**: https://github.com/jezweb/claude-skills
- **Example Audit**: See process guide Appendix B (better-auth v2.0.0)

---

**Last verified**: 2025-11-08 | **Version**: 1.0.0
