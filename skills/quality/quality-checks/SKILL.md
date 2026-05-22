---
name: quality-checks
description: >
  Orchestrate quality checks at lifecycle points (pre-edit, post-edit, on-stop).
  Coordinates test, doc, style, and security checks to ensure consistent code quality.
  Use when making significant code changes or before completing a task.
compatibility: Requires Node.js 24+; works with any codebase
metadata:
  version: "1.0.0"
---

# Quality Checks

Run comprehensive quality gate checks on code changes. Orchestrates quality checks at key lifecycle points in the development workflow.

## When to Use This Skill

- Before starting significant code changes (pre-edit baseline)
- After completing code changes (post-edit validation)
- Before marking a task as complete (final quality gate)
- When asked to run "quality check" or "quality gate"

## Skill Contents

### Sections

- [When to Use This Skill](#when-to-use-this-skill) (L16-L22)
- [Sub-Skills](#sub-skills) (L49-L59)
- [Lifecycle Hooks](#lifecycle-hooks) (L60-L67)
- [IDE Integration](#ide-integration) (L68-L78)
- [Quality Checks](#quality-checks) (L79-L101)
- [Commands](#commands) (L102-L109)
- [Assets](#assets) (L110-L116)
- [References](#references) (L117-L122)
- [Test Result Caching](#test-result-caching) (L123-L137)
- [Related Skills](#related-skills) (L138-L146)

### Available Resources

**📚 references/** - Detailed documentation
- [test result caching](references/test-result-caching.md)

**📦 assets/** - Templates and resources
- [claude quality hooks](assets/claude-quality-hooks.md)
- [cursor quality integration](assets/cursor-quality-integration.md)

---

## Sub-Skills

Quality checks orchestrate these sub-skills:

| Sub-Skill | Purpose | Skill Location |
|-----------|---------|----------------|
| `testing-standards` | Validates test coverage | [SKILL.md](.claude/skills/testing-standards/SKILL.md) |
| `doc-validation-rfc-37` | Validates documentation | [SKILL.md](.claude/skills/doc-validation-rfc-37/SKILL.md) |
| `coding-standards` | Enforces code style | [SKILL.md](.claude/skills/coding-standards/SKILL.md) |
| `security-review` | Checks for vulnerabilities | [SKILL.md](.claude/skills/security-review/SKILL.md) |

## Lifecycle Hooks

| Hook | When | Purpose |
|------|------|---------|
| `pre-edit` | Before changes | Capture baseline metrics |
| `post-edit` | After changes | Validate changes meet standards |
| `on-stop` | Before completion | Final quality gate |

## IDE Integration

The quality gateway integrates with AI IDEs through hooks:

| IDE | Integration Method | Reference |
|-----|-------------------|-----------|
| Claude Code | Native hooks in settings.json | `assets/claude-quality-hooks.md` |
| Cursor IDE | Rules + Commands | `assets/cursor-quality-integration.md` |

For hook implementation patterns, see the [ai-agent-hooks](.claude/skills/ai-agent-hooks/SKILL.md) skill.

## Quality Checks

### Pre-Edit (Baseline)

Before making changes:
1. Record current test coverage
2. Note existing linting errors
3. Capture documentation state

### Post-Edit (Validation)

After making changes:
1. Verify test coverage maintained or improved
2. Check for new linting errors
3. Validate documentation is in sync

### On-Stop (Final Gate)

Before completing:
1. Run full test suite
2. Verify no regressions
3. Check all quality thresholds met

## Commands

| Command | Purpose |
|---------|---------|
| `/quality-check` | Run full quality gate |
| `/add-tests` | Generate missing tests |
| `/sync-docs` | Update documentation |

## Assets

| Asset | Description |
|-------|-------------|
| `assets/claude-quality-hooks.md` | Claude Code hook configurations |
| `assets/cursor-quality-integration.md` | Cursor IDE integration guide |

## References

| Reference | Description |
|-----------|-------------|
| `references/test-result-caching.md` | How to save and reuse test results |

## Test Result Caching

Always save test output to `.tmp/` instead of running tests multiple times:

```bash
# Run once and save
pnpm test 2>&1 | tee .tmp/pnpm-test-latest.txt

# Then grep from file (don't run tests again!)
grep "FAIL" .tmp/pnpm-test-latest.txt
tail -20 .tmp/pnpm-test-latest.txt
```

See [references/test-result-caching.md](references/test-result-caching.md) for all tools.

## Related Skills

| Skill | Purpose |
|-------|---------|
| [ai-agent-hooks](.claude/skills/ai-agent-hooks/SKILL.md) | Hook implementation patterns |
| [testing-standards](.claude/skills/testing-standards/SKILL.md) | Test coverage validation |
| [doc-validation-rfc-37](.claude/skills/doc-validation-rfc-37/SKILL.md) | Documentation validation |
| [coding-standards](.claude/skills/coding-standards/SKILL.md) | Code style enforcement |
| [security-review](.claude/skills/security-review/SKILL.md) | Security vulnerability checks |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/quality-checks/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

