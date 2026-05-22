---
name: project-setup
description: Initialize project configuration. Auto-detect framework, package manager, database, and replace CLAUDE.md placeholders.
allowed-tools: Read, Grep, Glob, Edit, Bash(node:*), Bash(git:*), Bash(ls:*)
# context: shared (default) — intentionally NOT fork because Phase 2 requires user confirmation
---

# Project Setup

## Trigger

- Keywords: project setup, init, initialize, configure project, setup CLAUDE.md, customize placeholders

## When NOT to Use

- CLAUDE.md placeholders are already fully replaced (no `{...}` remaining)
- Non Node.js/TypeScript project (detection logic targets JS/TS ecosystem)
- Only want to modify a single placeholder -- just Edit CLAUDE.md directly

## Workflow

```
Phase 1: Detect project environment
    │
    ├─ Read package.json (dependencies, devDependencies, scripts)
    ├─ Detect lockfile (yarn.lock / pnpm-lock.yaml / package-lock.json)
    ├─ Detect entrypoints (glob src/)
    └─ Compile results
    │
Phase 2: Confirm detection results
    │
    ├─ Present detection results table
    └─ Wait for user confirmation or corrections
    │
Phase 3: Write to CLAUDE.md (unless --detect-only)
    │
    ├─ Use Edit tool to replace placeholders one by one
    └─ One Edit per placeholder
    │
Phase 4: Verify
    │
    ├─ Read CLAUDE.md to confirm no remaining placeholders
    └─ Output final summary
```

## Phase 1: Detect Project Environment

Execute the following detections in order; see `references/detection-rules.md` for detailed rules:

### 1.1 Read package.json

```
Read package.json
```

Extract:
- `name` → `{PROJECT_NAME}` candidate
- `dependencies` + `devDependencies` → framework, database detection
- `scripts` → command detection

### 1.2 Detect Package Manager

```
Glob: yarn.lock / pnpm-lock.yaml / package-lock.json
```

| File | PM |
|------|----|
| `yarn.lock` | yarn |
| `pnpm-lock.yaml` | pnpm |
| `package-lock.json` or fallback | npm |

PM result affects the prefix for `{TEST_COMMAND}`, `{LINT_FIX_COMMAND}`, `{BUILD_COMMAND}`, `{TYPECHECK_COMMAND}`.

### 1.3 Detect Framework

Determine from `dependencies`:

| Dependency | Framework |
|------|-----------|
| `@midwayjs/core` | MidwayJS 3.x |
| `@nestjs/core` | NestJS |
| `express` (no midway/nest) | Express |
| `fastify` | Fastify |
| `koa` | Koa |

### 1.4 Detect Database

Determine from `dependencies`:

| Dependency | Database |
|------|----------|
| `mongoose` / `mongodb` | MongoDB |
| `pg` / `typeorm` + `pg` | PostgreSQL |
| `mysql2` / `typeorm` + `mysql` | MySQL |
| `prisma` | Read `prisma/schema.prisma` `provider` |
| `redis` / `ioredis` | Redis (supplementary) |

### 1.5 Detect Entrypoints

```
Glob: src/configuration.ts, src/app.module.ts, src/main.ts, src/index.ts, bootstrap.js, bootstrap.ts
```

| Framework | Config Candidates | Bootstrap Candidates |
|-----------|------------------|---------------------|
| MidwayJS | `src/configuration.ts` | `bootstrap.js` or `bootstrap.ts` |
| NestJS | `src/app.module.ts` | `src/main.ts` |
| Express | `src/app.ts` or `src/index.ts` | `src/index.ts` |

### 1.6 Detect Scripts

From `package.json` `scripts` field:

| Placeholder | Preferred | Fallback | Format |
|-------------|--------|----------|------|
| `{TEST_COMMAND}` | `test:unit` | `test` | `{PM} test:unit` |
| `{LINT_FIX_COMMAND}` | `lint:fix` | `lint` | `{PM} lint:fix` |
| `{BUILD_COMMAND}` | `build` | `compile` | `{PM} build` |
| `{TYPECHECK_COMMAND}` | `typecheck` | `type-check` | `{PM} typecheck` |

If script does not exist, set value to `# N/A (no script found)` for user to fill manually.

## Phase 2: Confirm Detection Results

Present detection results:

```markdown
## Detection Results

| Placeholder | Detected Value | Source |
|-------------|--------|------|
| `{PROJECT_NAME}` | my-app | package.json name |
| `{FRAMEWORK}` | NestJS | @nestjs/core detected |
| `{DATABASE}` | PostgreSQL | pg + typeorm detected |
| `{CONFIG_FILE}` | src/app.module.ts | glob match |
| `{BOOTSTRAP_FILE}` | src/main.ts | glob match |
| `{TEST_COMMAND}` | yarn test:unit | scripts.test:unit exists |
| `{LINT_FIX_COMMAND}` | yarn lint:fix | scripts.lint:fix exists |
| `{BUILD_COMMAND}` | yarn build | scripts.build exists |
| `{TYPECHECK_COMMAND}` | yarn typecheck | scripts.typecheck exists |

Are these correct? Please let me know if any corrections are needed.
```

Wait for user confirmation before proceeding to Phase 3.

## Phase 3: Write to CLAUDE.md

**Prerequisite**: User has confirmed, and not in `--detect-only` mode.

1. Read CLAUDE.md
2. Execute `Edit` for each placeholder (using `replace_all: true`):

```
Edit CLAUDE.md:
  old_string: "{PROJECT_NAME}"
  new_string: "my-app"
  replace_all: true
```

Replace all 9 placeholders in order.

3. If CLAUDE.md does not yet exist, copy from the plugin's CLAUDE.md template to the project root.

## Phase 4: Verify

1. Read the modified CLAUDE.md
2. Search for remaining `{` + uppercase letter pattern:

```
Grep: \{[A-Z_]+\} in CLAUDE.md
```

3. Output results:

```markdown
## Setup Complete

| Placeholder | Value |
|-------------|-------|
| ... | ... |

Remaining placeholders: 0 (or list unreplaced ones)
```

## Output Format

```markdown
## Project Setup Complete

| Placeholder | Value |
|-------------|-------|
| `{PROJECT_NAME}` | my-app |
| `{FRAMEWORK}` | NestJS |
| `{DATABASE}` | PostgreSQL |
| `{CONFIG_FILE}` | src/app.module.ts |
| `{BOOTSTRAP_FILE}` | src/main.ts |
| `{TEST_COMMAND}` | yarn test:unit |
| `{LINT_FIX_COMMAND}` | yarn lint:fix |
| `{BUILD_COMMAND}` | yarn build |
| `{TYPECHECK_COMMAND}` | yarn typecheck |

Remaining placeholders: 0
```

## Examples

### Example 1: NestJS + PostgreSQL + yarn

```
User: /project-setup
Claude: [Reads package.json, detects NestJS + pg + yarn]

Detection Results:
| Placeholder | Detected Value |
| {PROJECT_NAME} | my-nest-api |
| {FRAMEWORK} | NestJS |
| {DATABASE} | PostgreSQL |
| {CONFIG_FILE} | src/app.module.ts |
| {BOOTSTRAP_FILE} | src/main.ts |
| {TEST_COMMAND} | yarn test:unit |

Are these correct?

User: Correct
Claude: [Edits CLAUDE.md, replaces all placeholders]
Setup Complete. Remaining placeholders: 0
```

### Example 2: MidwayJS + MongoDB + pnpm

```
User: /project-setup
Claude: [Reads package.json, detects MidwayJS + mongoose + pnpm]

Detection Results:
| {FRAMEWORK} | MidwayJS 3.x |
| {DATABASE} | MongoDB |
| {TEST_COMMAND} | pnpm test:unit |

User: DB should be PostgreSQL, we have two DBs
Claude: [Corrects DATABASE to PostgreSQL + MongoDB]
[Edits CLAUDE.md]
```

### Example 3: Detect only

```
User: /project-setup --detect-only
Claude: [Detects and displays results, does not modify any files]
```

## References

See detection rules: [detection-rules.md](./references/detection-rules.md)
