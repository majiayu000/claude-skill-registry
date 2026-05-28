---
name: root-package-json-config
description: Root package.json configuration for MetaSaver monorepos. Use when creating or auditing root package.json files to ensure workspace configuration, required scripts (build, dev, lint, test:unit, prettier:fix, clean), turbo pipeline scripts, packageManager field, and only devDependencies at root (no dependencies except cross-platform binaries).
---

# Root package.json Configuration Skill

Provides root package.json template and validation logic for MetaSaver monorepo configuration.

## Purpose

Configure pnpm workspaces, monorepo scripts, package manager, devDependencies, and cross-platform compatibility.

## Template

Located at: `templates/root-package.json.template`

## The 5 Root Package.json Standards

| Rule | Requirement             | Details                                                                                             |
| ---- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| 1    | Monorepo metadata       | name: `@metasaver/*`, private: true, packageManager: `pnpm@*`, engines (node, pnpm), type: "module" |
| 2    | Standard scripts        | build, clean, dev, lint*, prettier*, test*, db*, docker*, setup*                                    |
| 3    | DevDependencies only    | ENSURE ONLY devDependencies (except cross-platform binaries). Place all tooling in devDependencies  |
| 4    | Workspaces in YAML      | USE pnpm-workspace.yaml instead of workspaces field in package.json                                 |
| 5    | Cross-platform binaries | PLACE turbo-linux-64, turbo-windows-64 in dependencies (NOT optionalDependencies)                   |

### Rule 1: Monorepo Metadata

```json
{
  "name": "@metasaver/project-name",
  "private": true,
  "packageManager": "pnpm@10.20.0",
  "engines": { "node": ">=22.0.0", "pnpm": ">=10.20.0" },
  "type": "module"
}
```

### Rule 2: Required Scripts (18 total)

| Category    | Scripts                                          |
| ----------- | ------------------------------------------------ |
| Build       | build, clean, dev                                |
| Lint/Format | lint, lint:fix, lint:tsc, prettier, prettier:fix |
| Test        | test:unit, test:coverage, test:watch             |
| Database    | db:generate, db:migrate, db:seed, db:studio      |
| Docker      | docker:up, docker:down, docker:logs              |
| Setup       | setup:npmrc, setup:env, setup:all                |

### Rule 3: Required DevDependencies

Core: `@commitlint/cli`, `@metasaver/core-eslint-config`, `@metasaver/core-prettier-config`, `dotenv`, `husky`, `lint-staged`, `prettier`, `turbo`, `typescript`

### Rule 4: No Workspaces Field

Use `pnpm-workspace.yaml` instead.

### Rule 5: Cross-Platform Binaries

```json
{
  "dependencies": {
    "turbo-linux-64": "2.6.1",
    "turbo-windows-64": "2.6.1"
  }
}
```

## Validation

Validation checks (pseudo-code):

```javascript
// Rule 1: Metadata
validate(config.name?.startsWith("@metasaver/"), config.private === true, config.packageManager?.startsWith("pnpm@"), config.engines?.node, config.engines?.pnpm);

// Rule 2: Scripts (18 required)
const required = ["build", "clean", "dev", "lint", "lint:fix", "lint:tsc", "prettier", "prettier:fix", "test:unit", "test:coverage", "db:generate", "db:migrate", "db:seed", "db:studio", "docker:up", "docker:down", "setup:npmrc", "setup:env"];
validate(required.every((s) => config.scripts?.[s]));

// Rule 3: DevDependencies
const devDeps = ["@commitlint/cli", "@metasaver/core-eslint-config", "@metasaver/core-prettier-config", "dotenv", "husky", "lint-staged", "prettier", "turbo", "typescript"];
validate(devDeps.every((d) => config.devDependencies?.[d]));

// Rule 4: No workspaces field
validate(!config.workspaces);

// Rule 5: Cross-platform binaries
validate(config.dependencies?.["turbo-linux-64"], config.dependencies?.["turbo-windows-64"]);
```

## Best Practices

1. Use template as starting point
2. ENSURE all scripts use turbo for orchestration
3. PLACE cross-platform binaries in dependencies (not devDependencies)
4. VERIFY only devDependencies at root (place all tooling in devDependencies only)
5. RE-AUDIT after making changes

## Integration

- Repository type: Use `/skill scope-check` if not provided
- Workflow: `/skill audit-workflow`
- Remediation: `/skill remediation-options`
- Related: `pnpm-workspace-config`, `turbo-config`
