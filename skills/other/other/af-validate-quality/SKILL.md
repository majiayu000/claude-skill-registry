---
name: af-validate-quality
description: Validate documentation quality and run freshness audits. Use when checking frontmatter, verifying link integrity, enforcing documentation standards, or auditing stale content.

# AgentFlow documentation fields
title: Quality Process
created: 2025-10-29
updated: 2025-12-11
last_checked: 2025-12-11
tags: [skill, process, quality, validation, documentation]
parent: ../README.md
related:
  - ../../docs/guides/quality-guide.md
  - ../../docs/standards/documentation-standards.md
---

# Quality Process

## When to Use This Skill

Load this skill when you need to:
- Validate documentation before commits
- Run quality checks on changed files
- Audit documentation freshness
- Repair frontmatter issues
- Coordinate quality validation workflows
- Understand when and how to validate
- Invoke quality agents appropriately

**Common triggers**:
- Pre-commit hook reminder appears
- After creating or modifying documentation
- Before creating pull requests
- During brownfield onboarding
- When orchestrator requests validation
- User explicitly requests quality checks

## Quick Reference

The quality process ensures documentation and code maintain AgentFlow standards through validation, repair, and continuous auditing. Quality is multi-dimensional:

**Documentation Quality**:
- Frontmatter schema compliance
- Bidirectional link verification
- Freshness checking (30-day threshold)
- Content quality assessment

**Code Quality**:
- TSDoc/JSDoc compliance
- Test coverage validation
- Linting and type checking
- BDD scenario alignment

**Architecture Quality**:
- ADR completeness and currency
- Pattern consistency
- Documentation alignment

**Process Quality**:
- Phase adherence
- Approval gates
- Context preservation

## Rules

### Critical Quality Rules

1. **Never skip validation before commits** unless changes are truly trivial (typos, whitespace only)
2. **Always run incremental validation by default** - faster and focused on recent work
3. **Use full audits sparingly** - before releases, weekly schedules, or on explicit request
4. **Auto-repair safe issues** - frontmatter fixes, stale dates, broken internal links
5. **Report unsafe issues** - outdated content, missing docs, architectural decisions
6. **Track validation state** - use `.claude/validation-state.json` for git-aware incremental checks
7. **Respect exemptions** - don't validate `.claude/work/` or `.gitignore` files
8. **Coordinate agents** - docs-quality-agent for docs, code-quality-agent for code, architecture-quality-agent for ADRs

### Validation Decision Rules

**Run docs-quality-agent when**:
- `.md` files changed in `.claude/` or `docs/`
- Framework components modified (agents, skills, commands)
- Documentation content created or updated
- Pre-commit hook suggests validation

**Run code-quality-agent when**:
- Source code files changed
- Tests added or modified
- Dependencies updated
- Before creating pull requests

**Run architecture-quality-agent when**:
- Major architectural decisions made
- ADRs created or updated
- System design changed
- Patterns modified across codebase

**Skip validation when**:
- Pure typo fixes (no semantic changes)
- Whitespace/formatting only
- Debug log removal
- Comment updates

## Workflows

### 1. Pre-Commit Validation Workflow

**Trigger**: `.claude/hooks/git-commit-reminder` hook blocks first commit attempt

**Procedure**:
```
1. Attempt commit
   git commit -m "message"

2. Hook blocks with reminder
   "Have you run validation?"

3. Assess changes
   git diff --name-only HEAD  # What changed?

4. Run appropriate validation
   - Docs changed? → Task tool → docs-quality-agent
   - Code changed? → npm test && npm run lint
   - Both? → Run both validations

5. Review validation output
   - Fix any errors found
   - Address warnings
   - Confirm quality standards met

6. Retry commit (second attempt allowed)
   git commit -m "message"  # Proceeds
```

**Key points**:
- First attempt = reminder (always blocks)
- Second attempt = allowed (assumes you validated)
- Don't bypass by immediately retrying without validation
- Hook is a behavioral guardrail, respect it

### 2. Incremental Validation Workflow

**When**: During development, after making changes

**Procedure**:
```
1. Invoke docs-quality-agent (incremental mode is default)

2. Agent loads validation state
   - Reads .claude/validation-state.json
   - Identifies last validated commit
   - Gets changed files since then

3. Agent validates only changed files
   - Runs validation scripts on changes
   - Checks frontmatter, links, freshness
   - Reports issues found

4. Agent performs safe auto-repairs
   - Adds missing frontmatter fields
   - Updates stale dates
   - Fixes broken internal links

5. Agent reports unsafe issues
   - Outdated content needing rewrite
   - Missing documentation
   - Broken external links

6. Agent updates validation state
   - Records current commit as validated
   - Saves timestamp
   - Tracks files validated
```

**Benefits**:
- Fast (seconds, not minutes)
- Focused on your recent work
- Catches issues immediately
- Scales with project size

### 3. Full Audit Workflow

**When**: Before releases, weekly schedule, explicit request

**Procedure**:
```
1. Invoke quality agent with full audit directive
   Task tool → docs-quality-agent with "full audit"

2. Agent validates ALL files
   - Every .md file in .claude/ and docs/
   - All code files for TSDoc
   - Complete link graph
   - All ADRs

3. Agent generates comprehensive report
   - Total files validated
   - All issues found (errors + warnings)
   - Repairs made
   - Issues requiring human review

4. Review and address findings
   - Fix critical issues first
   - Plan for warnings
   - Update stale documentation
   - Create missing docs

5. Re-run until clean
   - All validation scripts pass
   - No critical issues
   - Warnings addressed or planned
```

**Use cases**:
- Before releasing new version
- Weekly maintenance (scheduled)
- After major refactoring
- Brownfield onboarding baseline

### 4. Quality Agent Invocation Workflow

**For documentation validation**:
```
Task tool → docs-quality-agent

# Agent procedure:
1. Load quality-process skill (this skill)
2. Load documentation-standards skill
3. Determine scope (incremental vs full)
4. Run validation scripts
5. Perform safe repairs
6. Report results
```

**For code validation**:
```
Task tool → code-quality-agent

# Agent procedure:
1. Load testing-expertise skill
2. Run linting: npm run lint
3. Run type check: npm run type-check
4. Run tests: npm test
5. Check coverage: npm run test:coverage
6. Validate TSDoc compliance
7. Report results
```

**For architecture validation**:
```
Task tool → architecture-quality-agent

# Agent procedure:
1. Review recent changes (git log -n 10)
2. Identify architectural decisions
3. Check for corresponding ADRs
4. Validate ADR currency
5. Check pattern consistency
6. Report findings
```

### 5. Brownfield Onboarding Workflow

**When**: Adding AgentFlow to existing projects

**Procedure**:
```
1. Run audit command
   /docs:audit-project

2. docs-quality-agent performs brownfield audit
   - Scans for existing documentation
   - Assesses quality (None/Poor/Scattered/Good)
   - Generates inventory
   - Identifies gaps

3. Review audit report
   - Overall assessment
   - Documentation inventory
   - Recommendations

4. Follow migration plan
   - Add frontmatter to existing docs
   - Create missing README files
   - Establish bidirectional links
   - Fill documentation gaps

5. Establish baseline
   - Run full validation
   - Fix critical issues
   - Create improvement plan
   - Set up continuous validation
```

**See**: [Quality Guide - Brownfield Onboarding](../../docs/guides/quality-guide.md#5-brownfield-onboarding-validation)

## Decision Points

### When should I run validation?

**YES - Run validation**:
- Before any git commit (non-trivial changes)
- After creating new documentation
- After modifying framework components
- Before creating pull requests
- Weekly scheduled audits
- After major refactoring
- During brownfield onboarding

**MAYBE - Assess first**:
- After code changes → Only if code has TSDoc or doc links
- After config changes → Only if functionality impacted
- After minor updates → Check if semantic changes

**NO - Skip validation**:
- Pure typo fixes (no semantic change)
- Whitespace/formatting only
- Debug log removal
- Timestamp updates

### Which agent should I invoke?

**docs-quality-agent**:
- Documentation files changed (`.md`)
- Framework components modified
- Pre-commit hook suggests it
- User requests docs validation

**code-quality-agent**:
- Source code changed
- Tests added/modified
- Before creating PR
- User requests code validation

**architecture-quality-agent**:
- Architectural decisions made
- ADRs created/updated
- System design changed
- Pattern modifications

**All agents sequentially**:
- Full audit requested
- Before releases
- After major changes

### Should I auto-repair or report?

**Auto-repair (safe)**:
- Missing frontmatter fields → Add with defaults
- Stale `last_checked` dates → Update to current
- Malformed tags → Convert to array format
- Broken internal links → Fix if new path known
- Parent-child mismatches → Add to children array

**Report for human review (unsafe)**:
- Outdated content → Needs rewriting
- Missing documentation → Needs creation
- Broken external links → Needs decision
- Circular relationships → Needs restructure
- Architectural drift → Needs ADR review

## Common Pitfalls

### 1. Bypassing Pre-Commit Validation
**Problem**: Immediately retrying commit without running validation

**Why it's bad**: Hook reminder is a behavioral guardrail to prevent quality debt

**Solution**: Run suggested validation before second attempt

**Example**:
```bash
# WRONG
git commit -m "message"  # Blocked by hook
git commit -m "message"  # Immediately retry ❌

# RIGHT
git commit -m "message"  # Blocked by hook
Task tool → docs-quality-agent  # Run validation
git commit -m "message"  # Now retry ✅
```

### 2. Forgetting Documentation Freshness
**Problem**: Not updating `last_checked` even when content is current

**Why it's bad**: Creates false positives in stale documentation reports

**Solution**: Update date after review, even if no changes

**Example**:
```yaml
# After reviewing and confirming content is current
last_checked: 2025-12-09  # Update this
```

### 3. Breaking Bidirectional Links
**Problem**: Adding child without updating parent, or moving files without updating references

**Why it's bad**: Validation fails, navigation breaks, documentation orphaned

**Solution**: Update both sides of relationship

**Example**:
```yaml
# When adding new-child.md
# In new-child.md
parent: ../README.md

# ALSO update parent
# In README.md
children:
  - ./existing.md
  - ./new-child.md  # Add this
```

### 4. Using Full Audits for Everything
**Problem**: Running full validation when incremental would suffice

**Why it's bad**: Slow feedback, wastes time, reduces validation frequency

**Solution**: Use incremental by default, full audits sparingly

**When to use each**:
- **Incremental**: Daily development, after changes, pre-commit
- **Full**: Releases, weekly schedule, brownfield baseline

### 5. Validating Operational Context Files
**Problem**: Running validation on `.claude/work/` files

**Why it's bad**: These are exempt - dynamic working files, not documentation

**Solution**: Skip `.claude/work/` directory

**Exempt locations**:
- `.claude/work/` - Operational context
- `.gitignore` files - Not tracked
- `node_modules/` - Dependencies
- `build/`, `dist/` - Generated output

## Quick Reference Tables

### Validation Script Quick Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `validate-frontmatter.ts` | Check YAML schema | After creating/modifying docs |
| `validate-links.ts` | Verify bidirectional links | After moving files or changing structure |
| `check-stale-docs.ts` | Find outdated docs | Weekly schedule, before releases |
| `repair-frontmatter.ts` | Auto-fix metadata | When validation reports frontmatter issues |
| `validate-tsdoc.ts` | Check code documentation | After code changes, before PR |

### Quality Agent Quick Reference

| Agent | Use For | Outputs |
|-------|---------|---------|
| docs-quality-agent | Documentation validation | files_validated, issues_found, repairs_made |
| code-quality-agent | Code quality checks | lint_errors, type_errors, test_failures, coverage |
| architecture-quality-agent | ADR and design validation | decisions_needing_adr, outdated_adrs, inconsistencies |

### Validation Trigger Decision Matrix

| Change Type | Validation Needed | Tool to Use |
|-------------|-------------------|-------------|
| `.md` files in `.claude/` | ✅ Yes | docs-quality-agent |
| `.md` files in `docs/` | ✅ Yes | docs-quality-agent |
| `.ts`/`.js` source code | ✅ Yes | code-quality-agent + tests |
| Test files | ✅ Yes | npm test |
| ADR files | ✅ Yes | architecture-quality-agent |
| Config files | ⚠️ Maybe | Verify functionality |
| Typo fixes | ❌ No | Skip validation |
| Whitespace/formatting | ❌ No | Skip validation |

## Integration with AgentFlow Phases

### Setup Phase
- Run **full quality audit** to establish baseline
- Validate framework documentation is current
- Ensure validation scripts operational
- Set up git hooks for continuous validation

### Discovery Phase
- Validate requirement documents as created
- Check **freshness of reference documentation**
- Ensure Linear features properly documented
- Run incremental validation after each document

### Refinement phase
- Validate **BDD feature files** with bdd-expertise
- Ensure mini-PRDs have proper metadata
- Verify visual specifications complete
- Run docs-quality-agent **before approval**

### Delivery Phase
- Validate **code documentation** (TSDoc) during implementation
- Run tests continuously (TDD workflow)
- Check code-to-doc links
- **Pre-commit validation on every commit**
- Full quality check **before creating PR**

## Comprehensive Documentation

For complete quality guidance including:
- Quality dimensions (documentation, code, architecture, process)
- Detailed validation workflows
- Quality metrics and targets
- Troubleshooting common issues
- Best practices
- Quality agent reference

**See**: [Quality Guide](../../docs/guides/quality-guide.md) (comprehensive 900+ line guide)

## Related Documentation

- [Documentation Standards](../../docs/standards/documentation-standards.md) - Metadata and linking requirements
- [Documentation System Guide](../../docs/guides/documentation-system.md) - Three-layer architecture and workflows
- [Testing Guide](../../docs/guides/testing-guide.md) - Test coverage and TDD practices
- [docs-quality-agent](../../agents/af-docs-quality-agent.md) - Documentation validation agent
- [code-quality-agent](../../agents/af-code-quality-agent.md) - Code validation agent
- [architecture-quality-agent](../../agents/af-architecture-quality-agent.md) - Architecture validation agent
