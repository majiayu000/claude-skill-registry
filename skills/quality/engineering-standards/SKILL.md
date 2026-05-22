---
name: engineering-standards
description: Comprehensive engineering standards for monorepo projects with Claude Code, covering hooks, testing, documentation, quality gates, and best practices. Use when setting up new projects, validating compliance, or extracting patterns from existing codebases.
version: "1.0.0"
last_updated: "2026-01-13"
---

# Engineering Standards

Comprehensive standards for building production-grade applications with Claude Code, capturing proven patterns for hooks, testing, documentation, quality gates, and monorepo architecture.

## When to Use This Skill

- **Setting up a new project** - Bootstrap with all best practices from day one
- **Validating existing projects** - Check compliance with standards
- **Extracting patterns** - Pull proven patterns from mature codebases
- **Standardizing practices** - Ensure consistency across multiple projects
- **Onboarding team members** - Reference for engineering expectations

## Quick Reference

### Validation & Compliance

```bash
# Check if project follows standards
python scripts/validate-compliance.py

# Generate detailed compliance report
python scripts/generate-report.py --format markdown --output report.md

# Quick validation
./scripts/check-standards.sh
```

### Bootstrap New Project

```bash
# Create new project with all standards
python scripts/bootstrap-project.py \
  --project-name "My Project" \
  --project-type nextjs \
  --output-path ./new-project

# Bootstrap with framework
python scripts/bootstrap-project.py \
  --project-name "My App" \
  --project-type monorepo \
  --framework makerkit \
  --output-path ./my-app
```

### Extract Patterns from Existing Project

```bash
# Sync patterns from mature codebase
python scripts/sync-from-project.py \
  --source-project /path/to/project \
  --extract all \
  --update-standards

# Extract specific categories
python scripts/sync-from-project.py \
  --source-project /path/to/project \
  --extract hooks,testing,patterns
```

## Standards Categories

### 🎣 Hooks & Automation

**[HOOKS_GUIDE.md](HOOKS_GUIDE.md)** - Git hooks and Claude Code hooks

- **Pre-commit hooks** (<2s target): Format, WIP validation, migration idempotency, RLS validation
- **Pre-push hooks** (30-60s): Lint, typecheck, lockfile sync, DB validation
- **Claude Code hooks**: PreToolUse (forbidden patterns), PostToolUse (migration warnings)
- **Lefthook configuration**: Parallel execution, THOROUGH mode, skip patterns

**Key patterns**: Migration idempotency (`IF NOT EXISTS`), version suffix detection, root file blocking

### 🧪 Testing Standards

**[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Vitest, Playwright, and Flutter testing

- **Vitest configuration**: Separate TEST instance, 80% coverage threshold, jsdom environment
- **Playwright patterns**: Dual-client architecture for RLS testing, auth-based projects
- **Flutter testing**: Unit tests with Riverpod mocking, widget tests, golden tests
- **Test organization**: By feature, integration vs unit separation

**Key patterns**: Dual-client RLS validation, coverage gates, TEST instance isolation

### 📝 Documentation Standards

**[DOCUMENTATION_GUIDE.md](DOCUMENTATION_GUIDE.md)** - WIP files, guides, architecture docs

- **Location-based classification**: `docs/wip/active/`, `docs/guides/`, `docs/architecture/`
- **WIP management**: `WIP_{gerund}_{YYYY_MM_DD}.md` naming, 7-day staleness limit
- **Forbidden patterns**: Root `.md` files (except CLAUDE.md, README.md), "deferred" work
- **Retention policies**: Archive after completion, structured investigation docs

**Key patterns**: Temporary vs permanent docs, naming conventions, staleness validation

### 📖 CLAUDE.md Standards

**[CLAUDE_MD_GUIDE.md](CLAUDE_MD_GUIDE.md)** - Structure and best practices

- **Required sections**: Tech Stack, Project Structure, Essential Commands, Critical Rules
- **Subdirectory pattern**: Focused context per package (apps/web/CLAUDE.md, etc.)
- **Integration**: Use `cortex-doc-standards` for generation and validation
- **Best practices**: Concise, scannable, actionable content

**Key patterns**: Progressive disclosure, variable substitution, no duplicated context

### ✅ Quality Gates

**[QUALITY_GATES_GUIDE.md](QUALITY_GATES_GUIDE.md)** - Lint, typecheck, format, build

- **Lint standards**: ESLint rules, oxlint for fast checks, custom plugins (i18n, providers)
- **Type checking**: TypeScript strict mode, affected packages only
- **Formatting**: Prettier auto-fix on pre-commit
- **Build validation**: Production build must succeed before merge

**Key patterns**: Sequential quality command, caching strategies, parallel execution

### 🔀 Git Workflow

**[GIT_WORKFLOW_GUIDE.md](GIT_WORKFLOW_GUIDE.md)** - Branches, commits, PRs

- **Branch strategy**: Worktree-based for features (`~/project-worktrees/`)
- **Branch naming**: `feat/`, `fix/`, `refactor/`, `docs/`
- **Commit format**: Conventional commits with Claude co-author
- **PR workflow**: Templates, review requirements, merge strategies

**Key patterns**: Worktree isolation, co-authoring with Claude, no force push to main

### 🏗️ Monorepo Standards

**[MONOREPO_GUIDE.md](MONOREPO_GUIDE.md)** - Turborepo, pnpm, workspaces

- **Package structure**: `apps/` vs `packages/`, shared dependencies
- **pnpm workspaces**: Configuration, workspace protocol, version management
- **Turborepo**: Build caching, task pipelines, affected packages
- **Type generation**: Cross-package type references, syncpack for versions

**Key patterns**: Dependency-aware builds, lockfile discipline, affected optimizations

### 🔒 Security Standards

**[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** - Secrets, RLS, auth, env vars

- **Environment variables**: `.env.local`, 1Password integration, Vercel gotcha (trailing newlines)
- **RLS-first pattern**: userClient + RLS by default, admin client only with validation
- **Migration security**: Idempotency validation, SQL injection prevention
- **Auth wrappers**: `withAuth`, `withAuthParams`, `withSuperAdmin` patterns

**Key patterns**: Never hardcode secrets, audit logging for admin operations

### 🎨 Architectural Patterns

**[PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)** - Common architectural patterns

- **Service layer**: Result pattern (no exceptions), BaseService abstraction
- **Server actions**: `withAuthParams` integration, revalidation patterns
- **Server vs Client components**: When to use each, async params handling
- **Data isolation**: `account_id` vs `client_id` patterns
- **N+1 prevention**: Batch queries + in-memory aggregation

**Key patterns**: Result<T, E>, soft delete, RLS-first data access

## Common Workflows

### Workflow 1: Bootstrap New Project

```bash
# 1. Create project with standards
python scripts/bootstrap-project.py \
  --project-name "My New App" \
  --project-type nextjs \
  --output-path ./my-new-app

# 2. Review and customize
cd ./my-new-app
cat CLAUDE.md  # Review and customize project-specific details

# 3. Install dependencies
pnpm install

# 4. Verify setup
pnpm quality  # Should pass all gates

# 5. Start development
pnpm dev
```

**Expected outcome**: Fully functional project with hooks, tests, quality gates, and documentation structure.

### Workflow 2: Validate Existing Project

```bash
# 1. Run validation from project root
python /path/to/engineering-standards/scripts/validate-compliance.py

# 2. Review findings
# Output shows: ✓ passed, ⚠ warnings, ✗ failures

# 3. Generate detailed report
python /path/to/engineering-standards/scripts/generate-report.py \
  --format markdown \
  --output compliance-report.md

# 4. Fix issues (example: version suffixes)
# If found: src/components/user-form-v2.tsx
# Rename to: src/components/user-form.tsx

# 5. Re-validate
python /path/to/engineering-standards/scripts/validate-compliance.py
```

**Expected outcome**: 95%+ compliance, clear action items for any gaps.

### Workflow 3: Extract Patterns from Mature Project

```bash
# 1. Analyze source project
python scripts/sync-from-project.py \
  --source-project /path/to/mature-project \
  --extract all \
  --dry-run

# 2. Review extracted patterns
# Output: New patterns found (hooks, testing, architectural)

# 3. Update standards (with approval)
python scripts/sync-from-project.py \
  --source-project /path/to/mature-project \
  --extract all \
  --update-standards

# 4. Version bump
# Edit SKILL.md: version: "1.0.0" → "1.1.0"
# Update CHANGELOG.md with new patterns

# 5. Sync to other projects
# Use bootstrap or validate workflows in other projects
```

**Expected outcome**: Standards updated with proven patterns from production codebases.

### Workflow 4: Set Up Project-Specific CLAUDE.md

```bash
# 1. Generate using cortex-doc-standards
npx cortex-doc-standards rules init --type nextjs --name "My Project"

# 2. Generate CLAUDE.md
npx cortex-doc-standards generate-claude

# 3. Customize with project-specific patterns
# Add: Tech Stack, Project Structure, Essential Commands

# 4. Validate structure
npx cortex-doc-standards validate --file CLAUDE.md

# 5. Add subdirectory CLAUDE.md files
# Create: apps/web/CLAUDE.md, packages/ui/CLAUDE.md
# Focus each on package-specific patterns
```

**Expected outcome**: Comprehensive CLAUDE.md with proper structure and project context.

## Integration with cortex-doc-standards

This skill **references** the `cortex-doc-standards` package for CLAUDE.md generation and validation, rather than duplicating its logic:

### Using cortex-doc-standards

```bash
# Install
npm install -D @akson/cortex-doc-standards

# Initialize configuration
npx cortex-doc-standards rules init \
  --type nextjs \
  --name "Project Name"

# Generate CLAUDE.md from rules
npx cortex-doc-standards generate-claude

# Validate existing CLAUDE.md
npx cortex-doc-standards validate --file CLAUDE.md
```

### Integration Points

- **Bootstrap script**: Calls `cortex-doc-standards generate-claude` during setup
- **Validation script**: Uses `cortex-doc-standards validate` for CLAUDE.md checks
- **CLAUDE_MD_GUIDE.md**: Documents structure and best practices (not generation logic)

**Benefits**: Single source of truth for CLAUDE.md validation, focused scope separation.

## Configuration

Standards behavior is configured in `config/rules-config.json`:

```json
{
  "hooks": {
    "pre_commit_timeout_seconds": 2,
    "pre_push_timeout_seconds": 60,
    "require_idempotent_migrations": true
  },
  "testing": {
    "coverage_threshold": 80,
    "require_separate_test_instance": true
  },
  "documentation": {
    "wip_staleness_days": 7,
    "block_root_md_files": true
  },
  "quality": {
    "require_strict_typescript": true,
    "require_prettier": true
  },
  "security": {
    "require_rls_first": true,
    "require_env_example": true
  }
}
```

**Project-specific variables** are in `config/project-variables.json`:

```json
{
  "project_name": "{{PROJECT_NAME}}",
  "project_type": "{{PROJECT_TYPE}}",
  "framework": "{{FRAMEWORK}}",
  "package_manager": "pnpm"
}
```

## Validation Scripts

### validate-compliance.py

Checks 30+ validations across 8 categories:

1. **Hooks presence**: lefthook.yml, .claude/settings.json
2. **Documentation structure**: CLAUDE.md, docs/ directories
3. **Testing configuration**: Vitest/Playwright configs, coverage thresholds
4. **Quality gates**: ESLint, TypeScript strict mode, Prettier
5. **Git configuration**: .gitignore, branch protections
6. **Security**: .env.local.example, no hardcoded secrets
7. **Naming conventions**: kebab-case, no version suffixes
8. **Migration standards**: IF NOT EXISTS, idempotency

**Exit codes**: 0=full compliance, 1=warnings, 2=critical failures

### bootstrap-project.py

20+ setup steps:

- Create directory structure (apps/, packages/, docs/)
- Copy templates with variable substitution
- Generate configurations (package.json, tsconfig.json, .gitignore)
- Initialize git and install lefthook
- Generate cortex-doc-standards config
- Create placeholder documentation

**Exit codes**: 0=success, 1=error

### sync-from-project.py

Pattern extraction workflow:

1. Analyze source project (hooks, testing, patterns)
2. Compare with current standards
3. Update standards with new patterns (with approval)
4. Generate change report with version bump recommendation

**Exit codes**: 0=success, 1=no changes, 2=error

### generate-report.py

Compliance reporting with:

- Executive summary (compliance %, grade A-F)
- Category-by-category breakdown
- Detailed findings and recommendations
- Historical comparison (if previous reports exist)

**Formats**: Markdown, JSON, HTML

## Success Criteria

A well-configured project following these standards should:

✅ **Pre-commit hooks run in < 2 seconds** (format, validation, idempotency checks)
✅ **Pre-push hooks run in < 60 seconds** (lint, typecheck, lockfile validation)
✅ **Test coverage is ≥ 80%** (branches, functions, lines, statements)
✅ **Migrations are idempotent** (all use IF NOT EXISTS / IF EXISTS patterns)
✅ **No version suffixes** (-v2, -new, -enhanced, -updated, -unified)
✅ **Documentation follows structure** (WIP files properly located, no root .md files)
✅ **Quality gates pass** (lint, typecheck, format, build succeed)
✅ **Security practices followed** (RLS-first, no hardcoded secrets, env example exists)
✅ **CLAUDE.md is comprehensive** (required sections, subdirectory files for packages)
✅ **Git workflow is clean** (conventional commits, co-authoring, no force push to main)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Hooks timeout | Too many files or slow operations | Review hook configuration, increase timeout for specific checks |
| Validation fails on custom patterns | Project uses non-standard structure | Add project-specific exceptions to `rules-config.json` |
| Bootstrap fails on dependencies | Missing pnpm or tools | Install prerequisites: `brew install pnpm lefthook` |
| Type errors after migration | Types not regenerated | Run `pnpm supabase:web:typegen` or `pnpm flutter:typegen` |
| Compliance report shows false positives | Custom project structure | Use `--skip-check` flags or customize validation rules |

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version**: 1.0.0 (2026-01-13)

## Related Resources

### Detailed Guides (Progressive Disclosure)

- **[HOOKS_GUIDE.md](HOOKS_GUIDE.md)** - Pre-commit, pre-push, Claude Code hooks
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Vitest, Playwright, Flutter testing
- **[CLAUDE_MD_GUIDE.md](CLAUDE_MD_GUIDE.md)** - CLAUDE.md structure and best practices
- **[QUALITY_GATES_GUIDE.md](QUALITY_GATES_GUIDE.md)** - Lint, typecheck, format, build
- **[GIT_WORKFLOW_GUIDE.md](GIT_WORKFLOW_GUIDE.md)** - Branches, commits, PRs
- **[DOCUMENTATION_GUIDE.md](DOCUMENTATION_GUIDE.md)** - WIP files, guides, architecture
- **[MONOREPO_GUIDE.md](MONOREPO_GUIDE.md)** - Turborepo, pnpm workspaces
- **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** - Secrets, RLS, auth, env vars
- **[PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)** - Architectural patterns

### External Tools

- [cortex-doc-standards](https://github.com/antoineschaller/cortex-packages/tree/main/packages/doc-standards) - CLAUDE.md validation
- [Lefthook](https://github.com/evilmartians/lefthook) - Fast git hooks
- [Turborepo](https://turbo.build/repo) - Monorepo build system
- [Vitest](https://vitest.dev/) - Testing framework
- [Playwright](https://playwright.dev/) - E2E testing

### Related Skills

- `ai-skill-manager` - Manage and sync Claude Code skills
- `database-migration-manager` - Database migrations and RLS
- `flutter-development` - Flutter mobile app patterns
- `cicd-pipeline` - GitHub Actions and deployment

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0
**Maintainer**: Engineering Team
