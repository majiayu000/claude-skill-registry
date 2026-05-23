---
name: tzurot-tooling
description: Use when adding CLI commands, dev scripts, or tooling utilities. Covers the ops CLI structure, where scripts belong, and standardized commands for linting/testing.
lastUpdated: '2026-01-24'
---

# Tooling & CLI Commands

**Use this skill when:** Adding new CLI commands, creating dev utilities, understanding where scripts belong, or using standardized lint/test commands.

## Quick Reference

```bash
# Standardized commands (use these!)
pnpm lint              # Lint all packages
pnpm lint:errors       # Show only errors (no warnings)
pnpm test              # Test all packages
pnpm test:failures     # Show only failed tests
pnpm typecheck         # Typecheck all packages

# Focused commands (changed packages only)
pnpm focus:lint        # Lint changed packages
pnpm focus:test        # Test changed packages
pnpm focus:typecheck   # Typecheck changed packages
pnpm focus:build       # Build changed packages

# Ops CLI (full power)
pnpm ops dev:lint --errors-only
pnpm ops dev:focus test -- --reporter=verbose
pnpm ops --help
```

## Where Scripts Belong

### ✅ `packages/tooling/` - CLI Commands & Utilities

**Use for:** Reusable tooling, CLI commands, development utilities.

```
packages/tooling/src/
├── cli.ts                 # Main CLI entry (pnpm ops)
├── commands/              # Command registration
│   ├── cache.ts
│   ├── context.ts         # Session context commands
│   ├── data.ts
│   ├── db.ts
│   ├── deploy.ts
│   ├── dev.ts             # Dev workflow commands
│   ├── gh.ts              # GitHub API commands
│   ├── inspect.ts         # Queue/runtime inspection
│   ├── memory.ts          # Memory cleanup commands
│   ├── release.ts         # Version bumping
│   ├── run.ts             # Generic env runner
│   └── test.ts            # Test audit commands
├── cache/                 # Cache utilities
├── context/               # Session context for AI startup
├── data/                  # Data import/export
├── db/                    # Database operations
├── deployment/            # Railway deployment
├── dev/                   # Dev workflow (focus-runner)
├── eslint/                # Custom ESLint rules
├── gh/                    # GitHub API utilities
├── inspect/               # Runtime inspection (queues)
├── memory/                # Memory deduplication
├── release/               # Version management
├── test/                  # Test audit utilities
└── utils/                 # Shared utilities
```

### ✅ `scripts/` - One-off & Data Scripts

**Use for:** Data migrations, one-time operations, CI scripts.

```
scripts/
├── data/                  # Data import scripts
├── testing/               # CI/test utilities
└── utils/                 # Misc utilities (bump-version)
```

### ❌ Anti-Patterns

```typescript
// ❌ WRONG - Ad-hoc script in scripts/ for reusable tooling
scripts/utils/smart-turbo.ts  // Should be in packages/tooling/

// ❌ WRONG - Grep chains in shell
pnpm test 2>&1 | grep -E "error|fail"  // Use pnpm test:failures

// ❌ WRONG - Direct eslint calls in package.json
"lint:errors": "eslint . --quiet"  // Use turbo for caching
```

## Adding New CLI Commands

### Step 1: Create Implementation Module

```typescript
// packages/tooling/src/myfeature/my-command.ts
export interface MyCommandOptions {
  dryRun?: boolean;
}

export async function runMyCommand(options: MyCommandOptions): Promise<void> {
  // Implementation
}
```

### Step 2: Register in commands/

```typescript
// packages/tooling/src/commands/myfeature.ts
import type { CAC } from 'cac';

export function registerMyFeatureCommands(cli: CAC): void {
  cli
    .command('myfeature:action', 'Description of action')
    .option('--dry-run', 'Preview without changes')
    .action(async (options: { dryRun?: boolean }) => {
      const { runMyCommand } = await import('../myfeature/my-command.js');
      await runMyCommand(options);
    });
}
```

### Step 3: Register in cli.ts

```typescript
// packages/tooling/src/cli.ts
import { registerMyFeatureCommands } from './commands/myfeature.js';

// ...
registerMyFeatureCommands(cli);
```

### Step 4: Add Package.json Shortcut (Optional)

```json
{
  "scripts": {
    "myfeature": "pnpm ops myfeature:action"
  }
}
```

## Turbo Integration

All CI-like commands should use Turbo for caching:

```json
{
  "scripts": {
    "lint": "turbo run lint",
    "lint:errors": "turbo run lint --output-logs=errors-only -- --quiet --format=pretty"
  }
}
```

**Key flags:**

- `--output-logs=errors-only` - Only show output from failed tasks
- `-- --quiet` - Pass `--quiet` to eslint (suppress warnings)
- `-- --format=pretty` - Use pretty formatter for errors

## Dev Commands Reference

| Command                               | Description                            |
| ------------------------------------- | -------------------------------------- |
| `pnpm ops dev:lint`                   | Lint changed packages                  |
| `pnpm ops dev:lint --all`             | Lint all packages                      |
| `pnpm ops dev:lint --errors-only`     | Lint with only errors shown            |
| `pnpm ops dev:test`                   | Test changed packages                  |
| `pnpm ops dev:test --all`             | Test all packages                      |
| `pnpm ops dev:typecheck`              | Typecheck changed packages             |
| `pnpm ops dev:focus <task>`           | Run any turbo task on changed packages |
| `pnpm ops dev:update-deps`            | Update all dependencies to latest      |
| `pnpm ops dev:update-deps --dry-run`  | Preview dependency updates             |
| `pnpm ops guard:boundaries`           | Check for architecture violations      |
| `pnpm ops guard:boundaries --verbose` | Detailed boundary check output         |

## Testing Requirements

**All tooling code must have unit tests.** The tooling package follows the same coverage requirements as other packages.

```bash
# Run tooling tests
pnpm --filter @tzurot/tooling test
```

When adding new tooling:

1. **Implementation modules** (`src/myfeature/*.ts`) - Must have `*.test.ts`
2. **Command registration** (`src/commands/*.ts`) - No tests needed (thin wrappers)
3. **Utilities** (`src/utils/*.ts`) - Must have `*.test.ts`

Test examples exist at:

- `packages/tooling/src/dev/focus-runner.test.ts`
- `packages/tooling/src/eslint/*.test.ts`

## Essential Command Categories

### Database Operations

```bash
pnpm ops db:status --env dev       # Check migration status
pnpm ops db:migrate --env dev      # Run migrations
pnpm ops db:safe-migrate --env dev # Create migration with validation
```

### GitHub Operations (use instead of broken `gh pr edit`)

```bash
pnpm ops gh:pr-comments <n>        # Get all comments
pnpm ops gh:pr-reviews <n>         # Get all reviews
pnpm ops gh:pr-edit <n> --title "..." # Edit PR
```

### Session & Debugging

```bash
pnpm ops context                   # Show session context for AI startup
pnpm ops inspect:queue --env dev   # Debug BullMQ jobs
pnpm ops logs --env dev            # Fetch Railway logs
```

### Test Audits

```bash
pnpm ops test:audit                # Run coverage ratchet audits (CI)
pnpm ops test:audit-services --update  # Update baseline after closing gaps
```

**📚 See**: `docs/reference/tooling/OPS_CLI_REFERENCE.md` for complete command reference with all options.

## Why This Structure?

1. **Caching** - Turbo caches results; ad-hoc scripts don't
2. **Discoverability** - `pnpm ops --help` shows all commands
3. **Consistency** - Same patterns across all tooling
4. **Testability** - Tooling modules can have unit tests
5. **Type Safety** - TypeScript throughout

## Package.json Shortcuts

Key shortcuts (full list in docs):

- `pnpm focus:lint/test/build` - Run on changed packages only
- `pnpm bump-version` - Version management
- `pnpm test:summary` - Summarize test results

## Related Skills

- **tzurot-code-quality** - ESLint rules, lint fixes
- **tzurot-testing** - Test patterns, coverage
- **tzurot-deployment** - Railway deployment commands
- **tzurot-db-vector** - Database migration commands
- **tzurot-git-workflow** - Git operations, PR workflow

## References

- Tooling package: `packages/tooling/`
- Turbo config: `turbo.json`
- Root scripts: `package.json`
