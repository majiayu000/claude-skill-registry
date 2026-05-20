---
name: infra-tooling-setup-tooling
description: ESLint 9 flat config, Prettier, TypeScript configuration, Vite, Husky + lint-staged, commitlint - build tooling for monorepos
---

# Build & Tooling

> **Quick Guide:** ESLint 9 flat config with `defineConfig()` and `globalIgnores()`. typescript-eslint v8 with `projectService`. Prettier shared config. Shared TypeScript configs. Bun package manager. Vite build configuration. Husky + lint-staged for git hooks.
>
> **WARNING**: ESLint 10 (January 2026) completely removes .eslintrc support. Migrate to flat config now.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use ESLint 9 flat config with `defineConfig()` from `eslint/config` - NOT legacy .eslintrc)**

**(You MUST use `globalIgnores()` for explicit global ignore patterns - NOT bare `ignores` property)**

**(You MUST use typescript-eslint v8+ with `projectService: true` for typed linting)**

**(You MUST include eslint-plugin-only-warn to convert errors to warnings for better DX)**

**(You MUST use shared config pattern - @repo/eslint-config, @repo/prettier-config, @repo/typescript-config)**

**(You MUST enable TypeScript strict mode in ALL tsconfig.json files)**

</critical_requirements>

---

**Auto-detection:** ESLint 9 flat config, Prettier, Bun, Vite configuration, Husky pre-commit hooks, lint-staged, commitlint

**When to use:**

- Setting up ESLint 9 flat config with shared configurations
- Configuring Prettier with shared config
- Setting up Vite build configuration
- Configuring TypeScript with shared configs
- Setting up pre-commit hooks with lint-staged
- Configuring commit message validation (commitlint)

**When NOT to use:**

- Runtime code (this is build-time tooling only)
- CI/CD pipelines (see backend/ci-cd skill instead)
- Production deployment configuration
- Server-side build processes (e.g., Docker builds)

**Key patterns covered:**

- ESLint 9 flat config with only-warn plugin (errors become warnings for better DX)
- Shared configurations (@repo/eslint-config, @repo/prettier-config, @repo/typescript-config)
- Vite configuration (path aliases, environment-specific builds)
- Husky + lint-staged for pre-commit quality gates (fast, staged files only)
- Commitlint for conventional commit messages

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) (essential patterns)
  - [examples/vite.md](examples/vite.md) - Vite path aliases, vendor chunks, environment builds
  - [examples/eslint.md](examples/eslint.md) - ESLint 9 flat config, shared configs, custom rules
  - [examples/typescript.md](examples/typescript.md) - Shared TypeScript strict config
  - [examples/git-hooks.md](examples/git-hooks.md) - Husky, lint-staged, VS Code integration
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Related skills:**

- For Turborepo task pipelines, caching, and workspaces, see `setup/monorepo`
- For internal package structure and conventions, see `setup/package`
- For daily coding conventions (naming, imports, constants), see CLAUDE.md

---

<philosophy>

## Philosophy

Build tooling should be **fast, consistent, and non-blocking**. Developers shouldn't fight with tools - tools should help catch issues early while staying out of the way during development.

**When to use this skill:**

- Setting up new apps or packages in the monorepo
- Configuring linting, formatting, or type-checking
- Adding git hooks for pre-commit quality gates
- Creating shared configurations for consistency
- Optimizing build performance with Vite

**When NOT to use:**

- Runtime code (this is build-time tooling only)
- CI/CD pipelines (see separate CI/CD skill)
- Production deployment configuration
- Server-side build processes

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Vite Configuration

Vite is the build tool for frontend apps. Key features: path aliases, vendor chunk splitting, environment-specific builds.

**Path Aliases:**

- Configure in both `vite.config.ts` and `tsconfig.json`
- Common aliases: `@/`, `@components/`, `@features/`, `@lib/`, `@hooks/`, `@types/`
- Vendor chunk splitting reduces main bundle size

**Environment-Specific Builds:**

- Use `loadEnv(mode, ...)` for environment-aware config
- Conditional sourcemaps (dev only) and minification (prod only)
- Build-time constants with `define` option

See [examples/vite.md](examples/vite.md) for complete Vite configuration examples.

---

### Pattern 2: ESLint 9 Flat Config

ESLint 9 uses flat config format (replaces legacy `.eslintrc`). Shared configs live in `packages/eslint-config/`.

**Key Requirements (ESLint 9.15+):**

- Use `defineConfig()` from `eslint/config` for type-safe configuration
- Use `globalIgnores()` for explicit global ignore patterns
- Support for `eslint.config.ts` TypeScript config files
- Use `extends` property in config objects for plugin composition
- Include `eslint-plugin-only-warn` to convert errors to warnings
- Use `eslint-config-prettier` to disable conflicting rules

**typescript-eslint v8+ Features:**

- Use `projectService: true` for automatic tsconfig discovery (replaces manual `project` option)
- Use `allowDefaultProject` for config files not in tsconfig
- `tseslint.config()` is deprecated - use ESLint's `defineConfig()` instead

**Custom Rules for Monorepo:**

- `import/no-default-export`: Enforce named exports
- `no-restricted-imports`: Prevent importing from internal package paths
- `@typescript-eslint/consistent-type-imports`: Use `import type` for types

**ESLint 10 Migration (January 2026):**

- .eslintrc files completely removed
- .eslintignore files no longer supported
- CLI flags like `--no-eslintrc`, `--env`, `--rulesdir` removed
- Minimum Node.js 20.19.0 required

See [examples/eslint.md](examples/eslint.md) for complete ESLint configuration examples.

---

### Pattern 3: Prettier Configuration (v3.0+)

Prettier configuration lives in `packages/prettier-config/` and is shared across all packages.

**Standard Config:**

- `printWidth: 100` - Balance readability with screen space
- `trailingComma: "all"` - Now the default in Prettier 3.0+ (cleaner git diffs)
- `singleQuote: false` - Match JSON format, reduce JSX escaping
- `endOfLine: "lf"` - Consistent line endings
- `bracketSameLine: false` - Replaces deprecated `jsxBracketSameLine`

**New in v3.5+:**

- TypeScript config file support (`.prettierrc.ts`) - requires Node.js 22.6.0+
- `objectWrap` option - controls multi-line object formatting (`"preserve"` or `"collapse"`)
- `experimentalOperatorPosition` option - controls binary operator placement (`"start"` or `"end"`)
- `experimentalTernaries` option (v3.1+) - alternative ternary formatting

**Usage:**

- Reference in package.json: `"prettier": "@repo/prettier-config"`
- Single source of truth prevents formatting inconsistencies

See [examples/core.md](examples/core.md) for complete Prettier configuration examples.

---

### Pattern 4: TypeScript Configuration

TypeScript configurations live in `packages/typescript-config/` with base settings extended by apps and packages.

**Strict Mode (Required):**

- `strict: true` - Enables all strict checks
- `noUncheckedIndexedAccess: true` - Prevents undefined access bugs
- `exactOptionalPropertyTypes: true` - Strict optional handling
- `noImplicitOverride: true` - Requires override keyword for inherited methods
- `noUnusedLocals: true` / `noUnusedParameters: true` - Catch dead code

**Modern Module Settings (TS 5.x):**

- `target: "ES2022"` - Stable ES target (not esnext)
- `module: "preserve"` - For bundler-based projects
- `moduleResolution: "bundler"` - Modern bundler compatibility
- `verbatimModuleSyntax: true` - Enforces explicit `import type`
- `moduleDetection: "force"` - Treats all files as modules

**Path Aliases:**

- Configure in tsconfig.json to match Vite aliases
- Use `${configDir}` template (TS 5.5+) for portable shared configs

For daily TypeScript enforcement rules (no unjustified `any`, explicit types), see CLAUDE.md.

See [examples/typescript.md](examples/typescript.md) for complete TypeScript configuration examples including TS 5.x features.

---

### Pattern 5: Git Hooks with Husky + lint-staged

Pre-commit hooks run linting on staged files only for fast feedback.

**Setup:**

- Husky hook calls `bunx lint-staged`
- lint-staged config specifies file patterns and commands
- Only lint staged files - NOT entire codebase

**VS Code Integration:**

- Format on save with Prettier
- Auto-fix ESLint on save
- Recommended extensions for team consistency

**Rule of thumb:** Pre-commit should take < 10 seconds. Anything slower goes to pre-push or CI.

See [examples/git-hooks.md](examples/git-hooks.md) for complete Husky + lint-staged examples.

</patterns>

---

<decision_framework>

## Decision Framework

### ESLint vs Biome

```
Need linting and formatting?
├─ Large monorepo (1000+ files)?
│   ├─ Speed is critical bottleneck?
│   │   └─ YES → Consider Biome (20x faster)
│   └─ NO → ESLint 9 + Prettier
└─ Greenfield project?
    ├─ Want single tool for lint + format?
    │   └─ YES → Consider Biome
    └─ Need mature plugin ecosystem?
        └─ YES → ESLint 9 + Prettier ✓
```

**Current recommendation:** ESLint 9 + Prettier (mature, stable, extensive plugin ecosystem)

### When to Use Git Hooks

```
What to run pre-commit?
├─ Fast (< 10 seconds)?
│   ├─ Lint with auto-fix → YES ✓
│   ├─ Format with Prettier → YES ✓
│   └─ Type check (--noEmit) → YES ✓
└─ Slow (> 10 seconds)?
    ├─ Full test suite → NO (run in CI)
    ├─ Full build → NO (run in CI)
    └─ E2E tests → NO (run in CI)
```

See [reference.md](reference.md) for additional decision frameworks.

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- ❌ Using legacy .eslintrc format instead of ESLint 9 flat config (**WILL BREAK in ESLint 10, January 2026**)
- ❌ Using `tseslint.config()` instead of ESLint's native `defineConfig()` (deprecated)
- ❌ Using bare `ignores` property instead of `globalIgnores()` helper (ambiguous behavior)
- ❌ Missing eslint-plugin-only-warn (errors block developers during development)
- ❌ Disabling TypeScript strict mode (allows implicit any and null bugs)
- ❌ Not using shared configs in monorepo (configs drift causing inconsistency)

**Medium Priority Issues:**

- ⚠️ Running full test suite in pre-commit hook (too slow, encourages --no-verify)
- ⚠️ No editor integration for Prettier/ESLint (manual formatting is forgotten)
- ⚠️ Hardcoded config values in each package instead of shared config
- ⚠️ Using manual `project` option instead of `projectService: true` in typescript-eslint
- ⚠️ Using deprecated `jsxBracketSameLine` option in Prettier (use `bracketSameLine` instead)

**Gotchas & Edge Cases:**

- ESLint 9 flat config uses different plugin syntax than legacy .eslintrc
- only-warn plugin must be loaded AFTER other plugins to convert their errors
- TypeScript path aliases must be configured in BOTH tsconfig and build tool (Vite/Next)
- Prettier and ESLint can conflict - must use eslint-config-prettier to disable conflicting rules
- `defineConfig()` auto-flattens arrays - no spread operators needed
- `projectService` requires typescript-eslint v8+ (was experimental in v6-v7 as `EXPERIMENTAL_useProjectService`)
- ESLint 10 requires Node.js 20.19.0+ (upgrade Node before upgrading ESLint)
- Prettier TypeScript config files (`.prettierrc.ts`) require Node.js 22.6.0+ and `--experimental-strip-types` flag before Node v24.3.0
- Prettier 3.0+ APIs are async - plugins using sync APIs need migration (use `@prettier/sync` for sync wrappers)

See [reference.md](reference.md) for full anti-patterns documentation.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use ESLint 9 flat config with `defineConfig()` from `eslint/config` - NOT legacy .eslintrc)**

**(You MUST use `globalIgnores()` for explicit global ignore patterns - NOT bare `ignores` property)**

**(You MUST use typescript-eslint v8+ with `projectService: true` for typed linting)**

**(You MUST include eslint-plugin-only-warn to convert errors to warnings for better DX)**

**(You MUST use shared config pattern - @repo/eslint-config, @repo/prettier-config, @repo/typescript-config)**

**(You MUST enable TypeScript strict mode in ALL tsconfig.json files)**

**Failure to follow these rules will cause inconsistent tooling, implicit any types, and blocked developers.**

**WARNING: ESLint 10 (January 2026) completely removes .eslintrc support. Plan migration now.**

</critical_reminders>
