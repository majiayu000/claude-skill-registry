---
name: kit-cli
description: (ePost) Use when developing the epost-kit CLI — cac commands, @inquirer/prompts, vitest tests, TypeScript patterns
user-invocable: false
metadata:
  keywords:
    - cli
    - cac
    - inquirer
    - vitest
    - epost-kit
    - command
  agent-affinity:
    - epost-fullstack-developer
    - epost-tester
    - epost-debugger
  platforms:
    - all
---

# CLI Development Patterns

## Tech Stack
- **Runtime**: Node.js 20+
- **Language**: TypeScript 5+
- **CLI Framework**: cac
- **Prompts**: @inquirer/prompts
- **Testing**: vitest
- **Build**: tsc + tsc-alias (no bundler)

## Project Structure

```
epost-agent-kit-cli/   (standalone repo at /Users/than/Projects/epost-agent-kit-cli)
├── src/
│   ├── cli.ts              — Entry point, cac setup + fuzzy command suggestions
│   ├── commands/            — Command implementations (init, onboard, update, doctor, lint, fix-refs, verify)
│   ├── domains/             — Domain-driven modules
│   │   ├── health-checks/   — integrity-checker, skill-health-checks, doctor checks
│   │   ├── packages/        — package-resolver, profile-loader
│   │   ├── validation/      — ref-validator (lint + fix-refs)
│   │   └── ...
│   ├── services/            — File operations, template engine, transformers
│   ├── shared/              — Cross-cutting: logger, file-system, constants, path-resolver
│   └── types/               — TypeScript interfaces (PackageManifest, FileOwnership, etc.)
├── tests/
│   ├── unit/                — Unit tests by domain
│   └── integration/         — Integration tests for commands
├── dist/                    — Compiled output
└── package.json
```

## Key Commands
- `lint` — Validate references across installed agent/skill/command markdown files
- `fix-refs` — Auto-fix stale references using rename maps from package.yaml (`--apply` to write)
- `verify` — Full pre-release audit: integrity + lint + health checks + dependency graph (`--strict`, `--json`)
- `doctor` — Verify installation and environment health
- `init` — Initialize epost-agent-kit in existing project

## Key Conventions
- Custom lightweight YAML parser (`parseSimpleYaml()` in package-resolver.ts) — no js-yaml dependency
- File ownership tracking with SHA256 checksums (`.epost-metadata.json`)
- Settings merge strategies: base (overwrite), merge (deep), skip (no-op)
- Profile-based package selection via `profiles/profiles.yaml`
- Topological sort for dependency resolution (layer-based install order)
- Skill index auto-generation from installed SKILL.md files
- Import paths use `@/` alias (e.g., `@/shared/logger.js`, `@/domains/packages/package-resolver.js`)

## Testing
- Unit tests with vitest
- Run: `cd /Users/than/Projects/epost-agent-kit-cli && npm test`
