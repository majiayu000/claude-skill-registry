---
name: ultracite
description: Ultracite multi-provider linting/formatting (Biome, ESLint, Oxlint). Use for v6/v7 setup, provider selection, Git hooks, MCP integration, AI hooks, migrations, or encountering configuration, type-aware linting, monorepo errors.
license: MIT
metadata:
  version: 2.0.0
  dependencies:
    ultracite: latest
    "@biomejs/biome": ">=1.9.0"
    eslint: ">=8.0.0 (when using ESLint provider)"
    oxlint: ">=0.1.0 (when using Oxlint provider)"
  runtime: Node.js v14.18+ (v18+ recommended)
  package_managers:
    - bun (preferred)
    - npm
    - pnpm
    - yarn
  frameworks_supported:
    - React
    - Next.js
    - Vue
    - Svelte
    - Solid
    - Angular
    - Remix
    - Qwik
    - Astro
  git_hook_managers:
    - husky
    - lefthook
    - lint-staged
  editors_supported:
    - VS Code (Biome extension)
    - Cursor
    - Claude Code
    - Zed
    - Cline
    - Windsurf
  keywords:
    - ultracite
    - biome
    - linting
    - formatting
    - code quality
    - eslint replacement
    - prettier replacement
    - typescript strict mode
    - rust linter
    - fast formatter
    - auto-fix
    - git hooks
    - pre-commit
    - husky
    - lefthook
    - lint-staged
    - react linting
    - nextjs linting
    - vue linting
    - svelte linting
    - monorepo linting
    - turborepo
    - AI coding rules
    - cursor rules
    - claude code rules
    - copilot instructions
    - accessibility linting
    - security linting
    - performance linting
    - jsx linting
    - hooks linting
    - migration from eslint
    - migration from prettier
    - biome.jsonc
    - zero config
    - code formatting
    - import sorting
    - unused imports
    - strict equality
    - type safety
    - oxlint
    - oxfmt
    - eslint integration
    - multi-provider
    - provider selection
    - mcp server
    - ai hooks
    - type-aware linting
    - ultracite doctor
    - programmatic usage
    - v6 upgrade
    - v7 upgrade
    - preset migration
---

# Ultracite Skill

**Fast, zero-config linting and formatting for modern JavaScript/TypeScript projects**

## Overview

Ultracite is a unified linting and formatting solution that supports multiple providers: **Biome** (default, Rust-based), **ESLint+Prettier+Stylelint**, and **Oxlint+Oxfmt**. It provides framework-specific presets and zero-configuration defaults, replacing traditional ESLint+Prettier setups with a faster, simpler alternative. Ultracite operates invisibly in the background, automatically formatting code and applying fixes on every save.

**Version 7 Changes**: Multi-provider architecture, preset path migration, MCP server support, AI hooks
**Version 6 Changes**: Framework-specific presets introduced (React, Next.js, Vue, Svelte, etc.)

### Core Goals

1. **Lightning-Fast Performance**: Leverages Biome's Rust implementation for instant linting/formatting
2. **Zero-Config Design**: Ships with 200+ sensible defaults optimized for modern TypeScript development
3. **Simplicity & Invisibility**: Operates with minimal user interaction
4. **Type Safety**: Enforces TypeScript strict mode and comprehensive null/undefined handling
5. **Tool Compatibility**: Works alongside other development tools without conflicts

### Key Benefits vs Alternatives

**vs ESLint + Prettier:**
- 10-100x faster performance (Rust vs JavaScript)
- Single tool instead of two
- Zero configuration needed
- Auto-fixes on save by default
- Built-in TypeScript strict mode

**vs Biome alone:**
- 200+ preconfigured rules
- Framework-specific presets (React, Next.js, Vue, Svelte)
- AI editor integration (Cursor, Claude Code, Copilot)
- Git hook integrations
- Migration tooling

## When to Use This Skill

### ✅ Ideal Projects

Use Ultracite when:
- Starting a new JavaScript/TypeScript project
- Building with React, Next.js, Vue, Svelte, or other modern frameworks
- Working in monorepos (Turborepo, Nx, Lerna)
- Teams want consistent formatting without bikeshedding
- Performance is critical (large codebases, CI/CD optimization)
- Migrating from ESLint + Prettier to a faster solution
- Using AI coding assistants (Cursor, Claude Code, Windsurf)
- TypeScript projects requiring strict type safety
- Projects with accessibility requirements (ARIA, semantic HTML)

### ⚠️ Consider Alternatives When

**Limited framework support:**
- Need Angular/Ember-specific rules (Biome support is basic)
- Require advanced CSS linting (Stylelint still recommended)

**Specialized requirements:**
- Need specific ESLint plugins not replicated in Biome
- Require property ordering in CSS (Stylelint feature)
- Team has extensive custom ESLint configurations

**Legacy projects:**
- Large codebases with custom ESLint rules (migration effort required)
- Projects with extensive Prettier customization

**For detailed limitations and workarounds, see**: `references/limitations-and-workarounds.md`

## Interactive Components

This skill provides interactive commands and autonomous agents for streamlined workflows:

### Commands
- `/ultracite:doctor` - Validate project setup, check for v6→v7 preset paths, detect conflicts
- `/ultracite:migrate` - Interactive migration wizard (ESLint/Prettier → Ultracite, v6→v7 upgrade)

### Agents
- `config-validator` - Analyze biome.jsonc for syntax, preset paths, rule conflicts, performance
- `migration-assistant` - Guide ESLint/Prettier migrations with rule mapping and gap analysis

**See README.md for complete interactive features documentation.**

## Choosing a Provider

Ultracite v7 supports three linting providers. Choose based on your needs:

### 🚀 Biome (Default) - **Recommended for most projects**
- **Speed**: Fastest (10-100x faster than ESLint)
- **Setup**: Zero-config with 200+ preset rules
- **Best for**: New projects, TypeScript-first development, performance-critical builds
- **Limitations**: Fewer rules than ESLint, basic CSS/SCSS support

### 🔧 ESLint + Prettier + Stylelint - **Recommended for maximum compatibility**
- **Speed**: Slower but mature ecosystem
- **Setup**: Requires more configuration
- **Best for**: Projects with existing ESLint plugins, advanced CSS/SCSS linting needs
- **Limitations**: JavaScript-based (slower), requires multiple tools

### ⚡ Oxlint + Oxfmt - **Recommended for maximum speed**
- **Speed**: Fastest linting (even faster than Biome for linting only)
- **Setup**: Type-aware linting with TypeScript integration
- **Best for**: Large TypeScript codebases, type-safety-critical projects
- **Limitations**: Newer ecosystem, fewer rules than ESLint

**Provider selection** during init:
```bash
bun x ultracite init --linter biome   # Default
bun x ultracite init --linter eslint  # ESLint + Prettier + Stylelint
bun x ultracite init --linter oxlint  # Oxlint + Oxfmt
```

**Load provider-specific documentation**:
- Biome: `references/provider-biome.md`
- ESLint: `references/provider-eslint.md`
- Oxlint: `references/provider-oxlint.md`

## Version Migration Guide

### Upgrading from v6 to v7

**Breaking Change**: Preset paths have changed in v7.

**v6 paths (old)**:
```jsonc
{
  "extends": ["ultracite/core", "ultracite/react"]
}
```

**v7 paths (new)**:
```jsonc
{
  "extends": ["ultracite/biome/core", "ultracite/biome/react"]
}
```

**Migration steps**:
1. Update `ultracite` package: `bun update ultracite`
2. Update preset paths in `biome.jsonc` (add `/biome/` segment)
3. Run `npx ultracite doctor` to validate configuration
4. Test linting: `npx ultracite check .`

**New v7 features**:
- Multi-provider support (Biome, ESLint, Oxlint)
- MCP server integration for AI assistants
- AI hooks (auto-format after AI edits)
- Type-aware linting (Oxlint)
- `ultracite doctor` diagnostics command

**Load full v7 migration guide**: `references/v7-migration.md`

### Upgrading from v5 to v6

**Key Change**: Framework-specific presets introduced.

**v5 approach (old)**:
```jsonc
{
  "extends": ["ultracite/core"]
}
```

**v6 approach (new)**:
```jsonc
{
  "extends": ["ultracite/core", "ultracite/react"]  // Framework preset
}
```

**Load full v6 migration guide**: `references/v6-migration.md`

### Project Suitability Assessment

When this skill is invoked, scan the project and assess:

1. **Check existing tooling:**
   ```bash
   # Check for ESLint
   ls -la .eslintrc* eslint.config.* package.json | grep eslint

   # Check for Prettier
   ls -la .prettierrc* prettier.config.* package.json | grep prettier

   # Check for Biome
   ls -la biome.json* package.json | grep biome
   ```

2. **Identify framework:**
   - Check `package.json` for `react`, `next`, `vue`, `svelte`, etc.
   - Recommend appropriate preset

3. **Assess project size:**
   - Large projects (1000+ files) benefit most from Rust performance
   - Small projects may not notice speed difference

4. **Check TypeScript config:**
   - If `tsconfig.json` exists, note that Ultracite requires `strictNullChecks: true`
   - Warn if disabled (will generate many warnings)

5. **Recommend or warn:**
   ```
   ✅ RECOMMENDED: This TypeScript + React project is ideal for Ultracite
   - 500+ files will benefit from Rust performance
   - React preset available
   - Can replace existing ESLint + Prettier setup

   ⚠️ CONSIDER: This project uses advanced ESLint plugins
   - Custom rule: eslint-plugin-custom-security
   - May need to retain ESLint for these specific rules
   - Could use Ultracite for formatting only
   ```

## Installation & Setup

### Prerequisites

- Node.js v14.18+ (v18+ recommended)
- Package manager: Bun (preferred), npm, pnpm, or yarn
- `package.json` file in project root

### Quick Start (Interactive)

```bash
# Using Bun (preferred for speed)
bun x ultracite init

# With provider selection (v7+)
bun x ultracite init --linter biome   # Default, fastest
bun x ultracite init --linter eslint  # ESLint + Prettier + Stylelint
bun x ultracite init --linter oxlint  # Oxlint + Oxfmt (type-aware)

# Using npm
npx ultracite init

# Using pnpm
pnpm dlx ultracite init

# Using yarn
yarn dlx ultracite init
```

The interactive setup will:
1. Prompt for provider selection (Biome, ESLint, Oxlint) - **v7+ only**
2. Install Ultracite and provider dependencies
3. Prompt for framework selection (React, Next.js, Vue, etc.)
4. Ask about editor setup (VS Code, Cursor, etc.)
5. Offer AI agent rules installation (Cursor, Claude Code, Copilot)
6. Prompt for Git hook integration (Husky, Lefthook, lint-staged)
7. Offer to migrate from existing tools (ESLint, Prettier)
8. Create/merge configuration file (`biome.jsonc`, `.eslintrc.js`, etc.)
9. Update `.vscode/settings.json` for editor integration
10. Enable `strictNullChecks` in `tsconfig.json` (if TypeScript)

### Non-Interactive Setup (CI/Automation)

```bash
# Auto-detect settings, skip prompts
bunx ultracite init --quiet

# Specify options explicitly (v7+)
bunx ultracite init \
  --linter biome \
  --pm bun \
  --frameworks react,next \
  --editors vscode \
  --agents cursor,claude \
  --integrations husky \
  --migrate eslint,prettier \
  --quiet
```

**Available flags:**
- `--linter`: Provider selection (biome, eslint, oxlint) - **v7+ only**
- `--pm`: Package manager (bun, npm, pnpm, yarn)
- `--frameworks`: react, next, solid, vue, qwik, angular, remix, svelte
- `--editors`: vscode, zed
- `--agents`: cursor, claude, cline, copilot, windsurf, etc.
- `--integrations`: husky, lefthook, lint-staged
- `--migrate`: eslint, prettier, biome
- `--quiet`: Skip all prompts (auto-enabled when `CI=true`)

### Manual Setup (Advanced)

```bash
# 1. Install dependencies
bun add -D ultracite @biomejs/biome

# 2. Create biome.jsonc
cat > biome.jsonc << 'EOF'
{
  "$schema": "https://biomejs.dev/schemas/2.3.8/schema.json",
  "extends": ["ultracite/core"]
}
EOF

# 3. Create VS Code settings
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
EOF

# 4. Enable TypeScript strict mode
# Add to tsconfig.json:
{
  "compilerOptions": {
    "strictNullChecks": true
  }
}
```

### Verify Installation

```bash
# Check installation
bunx ultracite doctor

# Expected output:
# ✔ Biome is installed
# ✔ Configuration file found: biome.jsonc
# ✔ Editor integration configured
# ✔ TypeScript strict mode enabled
```

## Configuration

### Basic Configuration

**File structure:**
```
project-root/
├── biome.jsonc              # Main configuration
├── .vscode/settings.json    # VS Code integration
├── tsconfig.json            # TypeScript config (strictNullChecks required)
└── package.json
```

**Minimal biome.jsonc:**
```jsonc
{
  "$schema": "https://biomejs.dev/schemas/2.3.8/schema.json",
  "extends": ["ultracite/core"],

  // Optional: Add framework preset
  // "extends": ["ultracite/core", "ultracite/react"],

  // Optional: Customize rules
  "linter": {
    "rules": {
      "suspicious": {
        "noConsoleLog": "off"  // Disable specific rule
      }
    }
  },

  // Optional: Exclude files
  "files": {
    "ignore": ["dist", "build", "coverage", "**/*.generated.ts"]
  }
}
```

### Framework Presets

- **`ultracite/react`**: React Hooks, JSX a11y, component best practices
- **`ultracite/nextjs`**: React + Next.js App Router, image optimization, document structure
- **`ultracite/vue`**: Vue 3 Composition API, template syntax, reactivity
- **`ultracite/svelte`**: Svelte 4/5 syntax, reactive declarations

**Usage**:
```jsonc
{
  "extends": ["ultracite/core", "ultracite/react"]
}
```

### Core Preset

The `ultracite/core` preset includes **200+ rules** across 7 categories:

- **Accessibility**: ARIA validation, semantic HTML, keyboard navigation
- **Correctness**: Type safety, unused code removal, exhaustive dependencies
- **Performance**: Code optimization, barrel file warnings
- **Security**: Prevents `eval()`, XSS risks, unsafe patterns
- **Style**: Consistent patterns, `const` preference, import organization
- **Suspicious**: Catches loose equality, debugger statements, typos
- **Complexity**: Cognitive complexity limits

**Formatting defaults**: 2 spaces, 80 chars/line, LF endings, single quotes

**For detailed framework presets, rule descriptions, and advanced configuration, see**: `references/configuration-guide.md`

## Usage

### IDE Integration (Recommended)

**VS Code Setup:**

1. Install Biome extension: `biomejs.biome`
2. Verify `.vscode/settings.json`:
   ```json
   {
     "editor.defaultFormatter": "biomejs.biome",
     "editor.formatOnSave": true,
     "editor.codeActionsOnSave": {
       "quickfix.biome": "explicit",
       "source.organizeImports.biome": "explicit"
     }
   }
   ```
3. Disable conflicting extensions (ESLint, Prettier)

**Features:**
- Auto-format on save
- Auto-fix on save (removes unused imports, fixes order, applies strict equality)
- Format on paste
- Problems panel for unfixable issues
- Quick fixes via lightbulb indicators

### CLI Usage

**Check code (lint only)**:
```bash
bunx ultracite check
bunx ultracite check src/
bunx ultracite check --diagnostic-level error  # Only errors
```

**Fix code (auto-fix)**:
```bash
bunx ultracite check --write
bunx ultracite check --write src/
```

**Format code (format only)**:
```bash
bunx ultracite format --write
bunx ultracite format --write src/
```

**Package.json scripts**:
```json
{
  "scripts": {
    "lint": "ultracite check",
    "lint:fix": "ultracite check --write",
    "format": "ultracite format --write"
  }
}
```

## Git Hook Integrations

Ultracite auto-detects and integrates with:
- **Husky**: Node.js-based hook manager
- **Lefthook**: Fast Go-based hook manager
- **lint-staged**: Runs linters on staged files only

**Quick setup**:
```bash
# Husky
bunx ultracite init --integrations husky

# Lefthook
bunx ultracite init --integrations lefthook

# lint-staged
bunx ultracite init --integrations lint-staged
```

**Example `.husky/pre-commit`**:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

ultracite check --staged --write
```

**For complete Git hook setup guides (Husky, Lefthook, lint-staged), see**: `references/git-hooks-setup.md`

## AI Editor Rules

Ultracite generates AI editor rules that teach AI assistants about your linting/formatting standards.

**Supported editors:**
- Cursor (`.cursorrules`)
- Claude Code (`.windsurfrules`)
- GitHub Copilot (`.github/copilot-instructions.md`)
- Continue.dev (`.continuerules`)
- Codeium (`.codeiumrules`)
- Zed (`.zedrules`)

**Generate rules**:
```bash
bunx ultracite generate-ai-rules
bunx ultracite generate-ai-rules --all  # All editors
bunx ultracite generate-ai-rules --editor=cursor  # Specific editor
```

**For complete AI editor integration guide and customization, see**: `references/ai-editor-integration.md`

## Monorepo Support

Ultracite optimizes for monorepos with:
- Shared base configurations
- Package-specific overrides
- Turborepo/Nx caching integration
- Performance optimization for large workspaces

**Example monorepo structure**:
```
monorepo/
├── biome.json              # Shared base config
├── apps/
│   └── web/
│       └── biome.json      # Next.js-specific overrides
└── packages/
    └── ui/
        └── biome.json      # React-specific overrides
```

**For complete monorepo setup, Turborepo/Nx integration, and performance tips, see**: `references/monorepo-configuration.md`

## Migration from ESLint/Prettier/Biome

**Automatic migration**:
```bash
bunx ultracite migrate eslint
bunx ultracite migrate prettier
bunx ultracite migrate biome
```

**Manual migration:**
1. Analyze current configuration
2. Map rules to Biome equivalents
3. Create `biome.json` with equivalent rules
4. Update package.json scripts
5. Remove old dependencies
6. Test thoroughly

**For complete migration guides with detailed rule mappings, see**: `references/migration-guides.md`

## Known Limitations

**CSS/SCSS**: Biome does not lint CSS. Workaround: Use Stylelint
**Framework gaps**: Limited Angular/Astro support. Workaround: Use `ultracite/core` + manual rules
**ESLint plugins**: Many ESLint plugins have no Biome equivalent. Workaround: Run ESLint alongside Ultracite for specific plugins
**File types**: No Markdown, YAML, HTML linting. Workaround: Use dedicated tools (markdownlint, yamllint, htmlhint)

**For complete list of limitations and detailed workarounds, see**: `references/limitations-and-workarounds.md`

## Troubleshooting

**Common issues:**
- VS Code not formatting on save → Install Biome extension, configure settings
- ESLint conflicts → Disable ESLint or run selectively
- Parse errors → Configure JSX support in `biome.json`
- Pre-commit hooks failing → Use `bunx` instead of global install
- CI failures → Pin Bun/Node versions, increase memory limit

**For complete troubleshooting guide, see**: `references/troubleshooting.md`

## Templates & Scripts

### Initial Setup Script

See `scripts/install-ultracite.sh` for automated setup.

### Migration Script

See `scripts/migrate-to-ultracite.sh` for ESLint/Prettier migration.

### Example Configurations

See `references/` directory for:
- `configuration-guide.md`: Framework presets and rule details
- `git-hooks-setup.md`: Husky, Lefthook, lint-staged setup
- `ai-editor-integration.md`: Cursor, Claude Code, Copilot rules
- `monorepo-configuration.md`: Turborepo, Nx, pnpm workspaces
- `migration-guides.md`: ESLint, Prettier, Biome migration
- `troubleshooting.md`: Common issues and solutions
- `limitations-and-workarounds.md`: Known gaps and fixes

## Package Versions

**Current versions (verified 2025-11-27):**
- `ultracite`: latest
- `@biomejs/biome`: >=1.9.0

**Check for updates:**
```bash
npm view ultracite version
npm view @biomejs/biome version
```

**Update:**
```bash
bun update ultracite @biomejs/biome
```

## Resources

**Official Documentation:**
- https://www.ultracite.ai/introduction
- https://www.ultracite.ai/setup
- https://www.ultracite.ai/configuration
- https://biomejs.dev/

**Examples:**
- https://www.ultracite.ai/examples

**Troubleshooting:**
- https://www.ultracite.ai/troubleshooting
- https://www.ultracite.ai/faq

**Community:**
- GitHub Issues: https://github.com/ultracite/ultracite
- Biome Discord: https://discord.gg/biome

## When to Load References

Load reference files on-demand based on user questions or task requirements:

**`references/provider-biome.md`**: When user asks about:
- Biome provider specifics
- Biome-only configuration
- Biome performance optimization
- Biome preset paths (v7: `ultracite/biome/*`)
- Biome rule customization

**`references/provider-eslint.md`**: When user asks about:
- ESLint provider setup
- ESLint + Prettier + Stylelint integration
- ESLint plugin configuration
- ESLint migration to Ultracite
- Advanced CSS/SCSS linting

**`references/provider-oxlint.md`**: When user asks about:
- Oxlint provider setup
- Type-aware linting features
- Oxlint performance benefits
- Oxlint vs Biome comparison
- TypeScript integration

**`references/v6-migration.md`**: When user asks about:
- Upgrading from v5 to v6
- Framework preset introduction
- v6 configuration changes
- v6 breaking changes

**`references/v7-migration.md`**: When user asks about:
- Upgrading from v6 to v7
- Preset path migration (`ultracite/core` → `ultracite/biome/core`)
- Multi-provider setup
- v7 breaking changes
- `ultracite doctor` command

**`references/mcp-integration.md`**: When user asks about:
- MCP server setup
- AI assistant integration via MCP
- Model Context Protocol
- MCP server configuration

**`references/ai-hooks.md`**: When user asks about:
- AI hooks setup (distinct from AI rules)
- Auto-format after AI edits
- Editor hook configuration
- Post-edit formatting automation

**`references/configuration-guide.md`**: When user asks about:
- Framework presets (React, Next.js, Vue, Svelte)
- Core preset rules (200+ rules breakdown)
- Rule customization methods
- File exclusion patterns
- Advanced configuration

**`references/git-hooks-setup.md`**: When user asks about:
- Pre-commit hooks
- Husky integration
- Lefthook integration
- lint-staged setup
- CI/CD integration
- Hook troubleshooting

**`references/ai-editor-integration.md`**: When user asks about:
- AI editor rules generation
- Cursor integration
- Claude Code integration
- GitHub Copilot setup
- Custom AI rules
- Editor-specific setup

**`references/monorepo-configuration.md`**: When user asks about:
- Monorepo setup
- Turborepo integration
- Nx integration
- Package-specific overrides
- Workspace configuration
- Performance optimization

**`references/migration-guides.md`**: When user asks about:
- ESLint migration
- Prettier migration
- Biome migration
- Rule mapping
- Migration checklist
- Post-migration steps

**`references/troubleshooting.md`**: When user asks about:
- VS Code issues
- ESLint/Prettier conflicts
- Parse errors
- Pre-commit hook failures
- CI failures
- TypeScript strictness errors
- Installation issues
- Performance problems

**`references/limitations-and-workarounds.md`**: When user asks about:
- CSS linting
- Framework support gaps
- ESLint plugin ecosystem
- File type support
- Editor integration
- Migration limitations

## Summary

Ultracite provides a unified linting and formatting solution with multi-provider support:

✅ **Use when:**
- Starting new projects
- Building with React/Next/Vue/Svelte
- Working in monorepos
- Want consistent formatting without configuration
- Performance matters (Biome/Oxlint providers)
- Need ESLint compatibility (ESLint provider)
- Using AI coding assistants
- Require type-aware linting (Oxlint)

⚠️ **Consider alternatives when:**
- Need specific ESLint plugins not supported by any provider
- Advanced CSS linting required (though ESLint provider includes Stylelint)
- Legacy framework support needed

**Key advantages:**
- **Multi-provider**: Choose Biome (fastest), ESLint (most compatible), or Oxlint (type-aware)
- **Version 7**: Preset path migration, MCP server, AI hooks, multi-provider architecture
- **Version 6**: Framework-specific presets (React, Next.js, Vue, Svelte, etc.)
- 10-100x faster than traditional ESLint + Prettier (Biome/Oxlint)
- Zero configuration (200+ rules preconfigured for Biome)
- Framework-specific presets
- AI editor integration + AI hooks
- Git hook support
- TypeScript strict mode enforced

**Installation:**
```bash
bun x ultracite init --linter biome   # Default (v7+)
bun x ultracite init --linter eslint  # ESLint provider (v7+)
bun x ultracite init --linter oxlint  # Oxlint provider (v7+)
```

**Most common workflow:**
1. Install with `bun x ultracite init`
2. Select framework preset (React, Next.js, etc.)
3. Choose Git hook integration (Husky, Lefthook, lint-staged)
4. Enable AI editor rules (Cursor, Claude Code, Copilot)
5. Optionally migrate from ESLint/Prettier
6. Code with auto-formatting on save
7. Commit with pre-commit hooks ensuring quality

**Remember:**
- Always check for existing Git hook managers before installing
- Assess project suitability (scan for ESLint/Prettier/frameworks)
- Recommend or warn based on project characteristics
- Enable `strictNullChecks` in TypeScript projects
- Use framework-specific presets for best results
- Load reference files on-demand based on user questions
