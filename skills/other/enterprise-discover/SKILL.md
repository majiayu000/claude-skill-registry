---
name: enterprise-discover
description: "Deep codebase learning agent. Run FIRST on any new project, any new worktree, or whenever hardcoded paths break. Produces stack-profile.json, stack-traps.json, and stack-best-practices.json that all enterprise-* skills consume. Supports incremental mode — only re-scans what changed since last profile. Without this, the pipeline guesses — and guesses wrong."
---

# Enterprise Discover — Deep Stack Learning Agent

You are profiling a codebase you have never seen before. Your job: produce structured JSON profiles that tell every downstream enterprise skill exactly where things live, how to run tests, what conventions to follow, and what landmines to avoid.

This skill exists because hardcoded paths kill portability. When enterprise-build assumes `npx jest` and the project uses `pytest`, the pipeline breaks. Discovery eliminates these assumptions.

---

## WHEN TO TRIGGER

- **Always**: as Stage 0 of `/enterprise` on any project without existing profile JSONs
- **Always**: when switching to a new codebase or monorepo package
- **Always**: when a downstream skill fails due to wrong paths, wrong test commands, or wrong conventions
- **On demand**: `/enterprise-discover` standalone
- **Incremental**: when profile exists but `profiled_commit != HEAD` — only re-run affected phases

---

## OUTPUT FILES

All files written to `.claude/enterprise-state/`:

| File | Purpose |
|------|---------|
| `stack-profile.json` | Structure, commands, conventions — the primary config |
| `stack-traps.json` | Type/schema/convention traps that will break code |
| `stack-best-practices.json` | Framework-specific guidance from web research |
| `project-profile.md` | Human-readable summary (generated FROM stack-profile.json) |

Schema reference: `references/stack-profile-schema.md`

---

## INCREMENTAL MODE

When `.claude/enterprise-state/stack-profile.json` exists:

1. Read `profiled_commit` from the JSON
2. Compare: `git diff --stat <profiled_commit>...HEAD`
3. If no changes: **SKIP** — announce "Profile is current" and exit
4. Classify what changed:
   - New dependencies (package.json, Gemfile, etc.) → re-run Phase 1 + Phase 2-G
   - New migrations or schema changes → re-run Phase 2-E, 2-F
   - New source files only → re-run Phase 2-D (auth patterns check)
   - Config file changes → re-run Phase 1
5. Merge updates into existing JSON — preserve manually-added traps in `stack-traps.json`
6. Update `profiled_commit` and `profiled_at`

---

## PIPELINE: 5 PHASES

### Phase 1: SCAN (3 parallel agents)

Launch three agents simultaneously:

**Agent A — Stack Detection:**
- Check for stack indicator files at project root and one level down:
  - `package.json` → Node.js (check `dependencies` for framework: express, fastify, koa, next, nest)
  - `Gemfile` → Ruby (check for rails, sinatra)
  - `requirements.txt` / `pyproject.toml` / `setup.py` → Python (check for django, flask, fastapi)
  - `go.mod` → Go
  - `Cargo.toml` → Rust
  - `pom.xml` / `build.gradle` → Java/Kotlin
  - `composer.json` → PHP (check for laravel, symfony)
  - `mix.exs` → Elixir
  - `*.csproj` / `*.sln` → C#/.NET
- Detect monorepo tool: `turbo.json`, `nx.json`, `lerna.json`, `pnpm-workspace.yaml`, `workspaces` in package.json
- Detect package manager from lockfiles: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun)
- Record: `stack.*`, `workspace_packages[]`

**Agent B — Directory Mapping + Conventions:**
- Map directory structure: `ls` on root, each workspace package
- Identify source dirs, test dirs, migration dirs, config files, entry points
- Sample 5+ source files from main source directory:
  - Naming convention (camelCase, snake_case, PascalCase)
  - Import style (CommonJS require, ES modules import, path aliases)
  - Error handling pattern (custom classes, try/catch, Result types)
  - Logger (console, winston, pino, structlog, slog)
  - Service pattern (class-based, function exports, modules)
  - Scan 5 largest source files for de facto size limits
- Catalog config files: linting, TypeScript, testing, CI/CD, env, editor, project instructions
- Record: `structure.*`, `conventions.*`

**Agent C — Git Analysis:**
- `git remote -v` → remote type (github, gitlab, bitbucket)
- `git branch -a` → all branches, detect default and protected
- `git log --oneline -10` → recent commit style (conventional, free-form, ticket-prefixed)
- Check CLAUDE.md/AGENTS.md for branch rules
- Record: `git.*`

### Phase 2: DEEP ANALYZE (4 parallel agents, needs Phase 1 results)

**Agent D — Auth Pattern Detection:**
```bash
# Search for auth patterns across the codebase
grep -rn "middleware.*auth\|authenticate\|requireAuth\|@login_required\|permission_classes\|before_action.*authenticate\|Authorization.*header" $SOURCE_DIR --include="*.$EXT" -l
```
- Identify middleware name, file path, user object, user fields
- Check route registration for auth middleware application pattern
- Check for public-before-auth route ordering
- Record: `auth.*`, `routes.*`

**Agent E — Multi-Tenancy Detection:**
```bash
# Search for tenant isolation patterns
grep -rn "tenant_id\|organization_id\|org_id\|account_id\|workspace_id\|team_id" $SOURCE_DIR --include="*.$EXT"
# Check for RLS policies
grep -rn "CREATE POLICY\|ROW LEVEL SECURITY" $MIGRATION_DIR --include="*.sql"
```
- Identify tenant field name, enforcement mechanism
- Find exceptions (tables without tenant scoping)
- Record: `multi_tenancy.*`

**Agent F — Type/Schema Trap Detection:**
- Read migration files to catalog all tables and column types
- Cross-reference foreign keys: check type consistency (UUID vs integer, text vs varchar)
- Check for timestamp columns using TIMESTAMP instead of TIMESTAMPTZ
- Check for naming inconsistencies across tables
- Record: `stack-traps.json` entries

**Agent G — Test Infrastructure Verification:**
```bash
# Verify test framework is installed and configured
$TEST_FRAMEWORK --version
# Check test config files exist
ls jest.config* vitest.config* pytest.ini .rspec 2>/dev/null
# Run a quick test to confirm the command works
$TEST_CMD --listTests 2>/dev/null | head -5
```
- Detect test framework, config, naming patterns
- Verify test command actually works (dry run)
- Detect coverage configuration
- Record: `commands.test_*`, `structure.test_dirs.*`

### Phase 3: RESEARCH (web search, needs Phase 1 results)

Search for current best practices for the detected stack:

```
Search: "[framework] [version] best practices [current year]"
Search: "[test framework] configuration patterns [current year]"
Search: "[database] migration best practices"
Search: "[framework] security checklist"
```

Synthesize findings into `stack-best-practices.json` with:
- Category (testing, security, database, error_handling, performance, deployment)
- Practice description
- Rationale
- Source

**Skip if**: web search is unavailable or rate-limited. The pipeline works without best practices.

### Phase 4: SYNTHESIZE

1. Merge all agent results into `stack-profile.json`
2. Generate `stack-traps.json` from Phase 2-F findings
3. Generate `stack-best-practices.json` from Phase 3 findings
4. Validate: run the test command once to confirm it works
   ```bash
   # Validation: does the test command actually run?
   $TEST_CMD 2>&1 | tail -5
   ```
   If test command fails: flag as `"test_command_verified": false` in profile
5. Generate `project-profile.md` from `stack-profile.json` (human-readable)

### Phase 5: PRESENT

1. **Print summary** — stack, key commands, notable conventions, trap count
2. **Flag unknowns** — any section that could not be determined. Do not guess.
3. **Flag conflicts** — if discovered conventions conflict with CLAUDE.md instructions, flag both. CLAUDE.md wins.
4. **Save to memory** — if a memory backend is available, save profile summary
5. **Hand off** — if invoked as Stage 0 of `/enterprise`, proceed to TRIAGE. If standalone, stop.

---

## PROJECT PROFILE TEMPLATE (generated from JSON)

```markdown
# Project Profile
<!-- Generated by /enterprise-discover from stack-profile.json -->
<!-- profiled_commit: [GIT_SHA] -->
<!-- profiled_at: [ISO_DATE] -->

## Stack
- **Language**: [stack.language]
- **Framework**: [stack.framework] [stack.framework_version]
- **Runtime**: [stack.runtime] [stack.runtime_version]
- **Package manager**: [stack.package_manager]
- **Monorepo**: [stack.monorepo_tool or "no"]

## Structure
- **Backend source**: [structure.source_dirs.backend]
- **Frontend source**: [structure.source_dirs.frontend or "none"]
- **Test dirs**: [structure.test_dirs.*]
- **Migration dir**: [structure.migration_dir]

## Commands
- **Test (all)**: `[commands.test_all]`
- **Test (single)**: `[commands.test_single]`
- **Build**: `[commands.build_frontend or "none"]`
- **Lint**: `[commands.lint or "none"]`

## Auth
- **Middleware**: `[auth.middleware_name]` at `[auth.middleware_path]`
- **User object**: `[auth.user_object]`
- **Pattern**: [auth.pattern]

## Multi-Tenancy
- **Enabled**: [multi_tenancy.enabled]
- **Field**: `[multi_tenancy.field]`
- **Enforcement**: [multi_tenancy.enforcement]
- **Exceptions**: [multi_tenancy.exceptions]

## Database
- **Type**: [database.type]
- **ORM**: [database.orm]
- **Migrations**: [database.migration_system]

## Conventions
- **File naming**: [conventions.file_naming]
- **Import style**: [conventions.import_style]
- **File extensions**: [conventions.file_extensions]
- **File size limits**: soft [conventions.file_size_soft_limit], hard [conventions.file_size_hard_limit]

## Git
- **Default branch**: [git.default_branch]
- **Protected**: [git.protected_branches]
- **Commit style**: [git.commit_style]

## Traps (from stack-traps.json)
[List each trap with severity and description]

## Workspace Packages (monorepo only)
| Package | Path | Purpose |
|---------|------|---------|
[workspace_packages entries]
```

---

## USAGE BY DOWNSTREAM SKILLS

### Stack Resolution Preamble (copy into each skill)

Every enterprise skill must read the profile at start:

```
## STACK RESOLUTION
Read `.claude/enterprise-state/stack-profile.json` at skill start.
Extract variables:
  $TEST_CMD       = commands.test_all
  $TEST_SINGLE    = commands.test_single
  $SOURCE_DIR     = structure.source_dirs.backend
  $FRONTEND_DIR   = structure.source_dirs.frontend
  $BUILD_CMD      = commands.build_frontend
  $TEST_FRAMEWORK = commands.test_framework
  $AUTH_MIDDLEWARE = auth.middleware_name
  $TENANT_FIELD   = multi_tenancy.field
  $TENANT_ENABLED = multi_tenancy.enabled
  $FILE_EXTENSIONS = conventions.file_extensions
  $BRANCH_MAIN    = git.default_branch

If no profile exists: BLOCKED — run /enterprise-discover first.
```

### Conditional Blocks

```
# Only if multi-tenancy is enabled
if $TENANT_ENABLED:
  verify every INSERT includes $TENANT_FIELD
  verify every SELECT scopes by $TENANT_FIELD

# Only if auth middleware exists
if $AUTH_MIDDLEWARE != "":
  verify protected routes use $AUTH_MIDDLEWARE

# Only if frontend exists
if $FRONTEND_DIR != "":
  run $BUILD_CMD to verify build
```
