---
name: init
description: Initialize a new SDLC monorepo with Storybook planning hub, pnpm workspace, and git configuration. Use when starting a new project.
user-invocable: true
argument-hint: [project-name]
allowed-tools: Bash, Write, Read, Glob, Grep
---

# /sdlc:init - Initialize SDLC Monorepo

You are a project initialization specialist. Your role is to scaffold a complete SDLC monorepo project with a Storybook-based planning hub, design system, and documentation structure.

## Task

Initialize a new SDLC project with all necessary scaffolding, dependencies, and configuration.

## Arguments

- `project-name` (optional) - Name of the project. If not provided, use the current directory name.

## Workflow

### 1. Pre-flight Checks

**IMPORTANT**: Perform these checks before any file operations:

```bash
# Check if pnpm is installed
pnpm --version

# Check if git is available
git --version

# Check current directory
pwd

# List current directory contents
ls -la
```

**Decision Points**:
- If pnpm not installed: Provide installation instructions and EXIT
- If directory is not empty: Ask user for permission to proceed
- If git not available: Warn but continue

### 2. Parse Arguments

Extract project name from arguments or use current directory name:

```bash
# Get current directory name if no argument provided
basename "$(pwd)"
```

### 3. Create Monorepo Structure

Create the following directory structure:

```
.
├── docs/                           # Source artifacts (external to packages)
│   ├── sdlc.state.json            # Planning state (checkpoints, personas, artifacts)
│   ├── sdlc.state.schema.json     # JSON schema for state validation
│   ├── pm/                         # Project Management (created on demand)
│   ├── ba/                         # Business Analysis (created on demand)
│   ├── req/                        # Requirements (always created)
│   ├── arch/                       # Architecture (always created)
│   ├── security/                   # Security (created on demand)
│   ├── quality/                    # Quality (created on demand)
│   ├── test/                       # Testing (always created)
│   ├── ux/                         # UX & Design (always created)
│   ├── db/                         # Database (created on demand)
│   └── ops/                        # DevOps (created on demand)
├── packages/
│   ├── planning-hub/               # Storybook site
│   │   ├── .storybook/
│   │   ├── src/
│   │   │   ├── docs/
│   │   │   ├── components/
│   │   │   └── utils/
│   │   ├── public/
│   │   │   └── artifacts/
│   │   ├── scripts/
│   │   └── package.json
│   └── ui/                         # Design system
│       ├── src/
│       │   ├── tokens/
│       │   └── primitives/
│       └── package.json
├── references/                      # Optional local reference repos (awesome lists, etc.)
│   └── awesome/
│       ├── README.md
│       ├── seeds.tsv
│       ├── sync.sh
│       └── repos/                  # Local clones (gitignored)
├── pnpm-workspace.yaml
├── package.json
└── .gitignore
```

Use Write tool to create placeholder files in each directory:

```
docs/req/README.md
docs/arch/README.md
docs/test/README.md
docs/ux/README.md
```

**Create SDLC State File**:

Copy `${CLAUDE_PLUGIN_ROOT}/skills/init/templates/sdlc.state.json.template` to `docs/sdlc.state.json` with variable substitution:
- `{{PROJECT_NAME}}` - Project name
- `{{CREATED_AT}}` - Current ISO datetime
- `{{UPDATED_AT}}` - Current ISO datetime

Also copy `${CLAUDE_PLUGIN_ROOT}/skills/init/templates/sdlc.state.schema.json.template` to `docs/sdlc.state.schema.json`.

This state file tracks:
- Planning checkpoints (kickoff, scenarios, useCases, domainModel, dataModel, apiContract, prototypes, supporting, signoff)
- User personas
- Scenarios (as-is, visionary, evaluation)
- Use cases
- Requirements and traceability
- Generated artifacts

### 4. Copy Template Files

Use Read tool to read templates from `${CLAUDE_PLUGIN_ROOT}/skills/init/templates/` and Write tool to create files with variable substitution:

**Variables to substitute**:
- `{{PROJECT_NAME}}` - Project name from arguments
- `{{PROJECT_DESCRIPTION}}` - "SDLC project with planning hub" (default)
- `{{DATE}}` - Current date (YYYY-MM-DD format)

**Files to create**:
1. `pnpm-workspace.yaml` (from pnpm-workspace.yaml.template)
2. `package.json` (from package.json.template)
3. `.gitignore` (from .gitignore.template)
4. `AGENTS.md` (from AGENTS.md.template)

**Optional (recommended): Local reference repos (awesome lists)**

Create:
- `references/awesome/README.md` (from references/awesome/README.md.template)
- `references/awesome/seeds.tsv` (from references/awesome/seeds.tsv.template)
- `references/awesome/sync.sh` (from references/awesome/sync.sh.template)

Then make the sync script executable:

```bash
chmod +x references/awesome/sync.sh
```

### 4.5. Set Up Quality Gates

**Create root-level quality configuration**:

1. Read templates from `${CLAUDE_PLUGIN_ROOT}/skills/init/templates/quality-gates/root/` and write to project root with variable substitution:
   - `tsconfig.base.json` (shared TypeScript strict config)
   - `eslint.config.mjs` (complexity + maintainability rules)
   - `vitest.workspace.ts` (multi-package test config)
   - `.dependency-cruiser.js` (circular dependency detection)
   - `knip.json` (dead code detection, workspace-aware)
   - `.prettierrc.json` (code formatting)
   - `.editorconfig` (editor consistency)
   - `.prettierignore` (formatting ignore patterns)

2. Create `.husky/` directory and hooks:
   ```bash
   mkdir -p .husky
   ```

   Create `.husky/pre-commit` (from husky-pre-commit.template)
   Create `.husky/pre-push` (from husky-pre-push.template)

3. Create `.github/workflows/` directory and CI configuration:
   ```bash
   mkdir -p .github/workflows
   ```

   Create `.github/workflows/ci.yml` (from ci.yml.template)

4. Create `scripts/` directory and validation script:
   ```bash
   mkdir -p scripts
   ```

   Create `scripts/validate-packages.js` (from validate-packages.js.template)

5. Create `docs/development/` directory and documentation:
   ```bash
   mkdir -p docs/development
   ```

   Create `CONTRIBUTING.md` (from CONTRIBUTING.md.template)
   Create `docs/development/QUALITY_STANDARDS.md` (from quality-gates/docs/QUALITY_STANDARDS.md.template)
   Create `docs/development/PACKAGE_CREATION.md` (from quality-gates/docs/PACKAGE_CREATION.md.template)

6. Append quality-specific entries to `.gitignore` (from .gitignore-additions.template):
   ```bash
   # Read .gitignore-additions.template and append to existing .gitignore
   ```

### 5. Initialize Storybook Package

Create `packages/planning-hub/package.json`:

```json
{
  "name": "planning-hub",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "storybook": "pnpm run sync:artifacts:watch & storybook dev -p 6006",
    "build": "pnpm run sync:artifacts && storybook build",
    "sync:artifacts": "node scripts/sync-artifacts.js",
    "sync:artifacts:watch": "node scripts/sync-artifacts.js --watch"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "mdx-mermaid": "^2.0.3",
    "swagger-ui-react": "^5.31.0",
    "js-yaml": "^4.1.0"
  },
  "devDependencies": {
    "@storybook/addon-a11y": "^8.4.7",
    "@storybook/addon-essentials": "^8.4.7",
    "@storybook/addon-links": "^8.4.7",
    "@storybook/addon-themes": "^8.4.7",
    "@storybook/react": "^8.4.7",
    "@storybook/react-vite": "^8.4.7",
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "storybook": "^8.4.7",
    "vite": "^6.0.5",
    "chokidar": "^4.0.3",
    "fs-extra": "^11.2.0",
    "@types/fs-extra": "^11.0.4"
  }
}
```

### 5.5. Add Quality Configs to planning-hub

1. Create `packages/planning-hub/tsconfig.json`:
   ```json
   {
     "extends": "../../tsconfig.base.json",
     "compilerOptions": {
       "jsx": "react-jsx",
       "outDir": "dist"
     },
     "include": ["src", "scripts", ".storybook"]
   }
   ```

2. Create `packages/planning-hub/vitest.config.ts`:
   ```typescript
   import { defineConfig } from 'vitest/config';
   import react from '@vitejs/plugin-react';

   export default defineConfig({
     plugins: [react()],
     test: {
       globals: false,
       environment: 'jsdom',
       coverage: {
         provider: 'v8',
         reporter: ['text', 'html'],
         include: ['src/**/*.{ts,tsx}'],
         exclude: ['src/**/*.stories.tsx', 'src/**/*.test.tsx', 'scripts/**'],
         thresholds: {
           lines: 95,
           functions: 95,
           statements: 95,
           branches: 90,
           perFile: true,
         },
       },
     },
   });
   ```

3. Update `packages/planning-hub/package.json` to add quality scripts:
   Merge these scripts into the existing scripts:
   ```json
   {
     "scripts": {
       "typecheck": "tsc --noEmit",
       "lint": "eslint . --max-warnings=0",
       "test": "vitest",
       "test:coverage": "vitest run --coverage"
     }
   }
   ```

### 6. Create Storybook Configuration

Use Read to get templates and Write to create:

1. `packages/planning-hub/.storybook/main.ts` (from storybook/main.ts.template)
2. `packages/planning-hub/.storybook/preview.ts` (from storybook/preview.ts.template)
3. `packages/planning-hub/.storybook/manager.ts` (from storybook/manager.ts.template)

### 7. Create Initial Documentation

Create these initial MDX pages in `packages/planning-hub/src/docs/`:

**Overview.mdx**:
```mdx
import { Meta } from '@storybook/blocks';

<Meta title="Overview" />

# {{PROJECT_NAME}} Planning Hub

Welcome to the planning hub for **{{PROJECT_NAME}}**.

This interactive documentation site provides comprehensive SDLC artifacts across all project phases.

## Getting Started

1. **Review the Vision** - Understand the project goals and scope
2. **Explore Requirements** - Review user stories and functional requirements
3. **Study Architecture** - Examine system design and technical decisions
4. **Check UX Designs** - View user journeys and interface mockups
5. **Review Test Plans** - Understand verification and validation strategy

## How to Use This Hub

- **Navigation**: Use the sidebar to browse different sections
- **Search**: Use Storybook's search feature (Ctrl/Cmd+K) to find specific content
- **Updates**: This hub automatically syncs with the docs/ folder

## Next Steps

Run `/sdlc:plan` to start planning your first feature with an interactive discovery wizard.

---

**Last Updated**: {{DATE}}
```

**Quick Start.mdx**:
```mdx
import { Meta } from '@storybook/blocks';

<Meta title="Quick Start" />

# Quick Start Guide

## Development Workflow

### 1. Start the Planning Hub

\`\`\`bash
pnpm dev:storybook
\`\`\`

Opens at http://localhost:6006

### 2. Plan a Feature

\`\`\`bash
/sdlc:plan
\`\`\`

Follow the interactive wizard to generate planning artifacts.

### 3. Implement

Build your feature according to the plan.

### 4. Update Progress

\`\`\`bash
/sdlc:update
\`\`\`

Syncs artifacts with implementation status.

## Available Commands

### Planning Hub

- \`pnpm dev:storybook\` - Start development server
- \`pnpm build:storybook\` - Build static site
- \`pnpm sync:artifacts\` - Manually sync docs/ to Storybook
- \`pnpm sync:artifacts:watch\` - Watch for changes

### Formatting

- \`pnpm format\` - Format all files with Prettier

## Project Structure

\`\`\`
├── docs/                  # Source artifacts (edit these)
│   ├── req/              # Requirements
│   ├── arch/             # Architecture
│   ├── ux/               # UX & Design
│   └── test/             # Testing
├── packages/
│   ├── planning-hub/     # This Storybook site
│   └── ui/               # Design system
└── package.json
\`\`\`

## Tips

- **Edit in docs/**: All artifacts live in the docs/ folder
- **Auto-reload**: Changes in docs/ trigger Storybook reload
- **Commit often**: Track artifact evolution in git
- **Share the hub**: Deploy Storybook for team collaboration

---

**Need Help?** Check the SDLC plugin README for troubleshooting.
```

### 8. Create Artifact Sync Script

Create `packages/planning-hub/scripts/sync-artifacts.js`:

```javascript
#!/usr/bin/env node

import chokidar from 'chokidar';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DOCS_DIR = path.resolve(__dirname, '../../../docs');
const PUBLIC_ARTIFACTS = path.resolve(__dirname, '../public/artifacts');

async function syncArtifacts() {
  try {
    console.log('Syncing artifacts from docs/ to public/artifacts/...');
    await fs.ensureDir(PUBLIC_ARTIFACTS);
    await fs.copy(DOCS_DIR, PUBLIC_ARTIFACTS, {
      overwrite: true,
      errorOnExist: false,
    });
    console.log('✓ Artifacts synced successfully');
  } catch (error) {
    console.error('✗ Error syncing artifacts:', error);
    process.exit(1);
  }
}

// Check for --watch flag
const isWatchMode = process.argv.includes('--watch');

if (isWatchMode) {
  console.log('Watching docs directory for changes...');

  // Initial sync
  await syncArtifacts();

  // Watch for changes
  const watcher = chokidar.watch(DOCS_DIR, {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true,
    ignoreInitial: true,
  });

  watcher
    .on('add', filepath => {
      console.log(`File added: ${path.relative(DOCS_DIR, filepath)}`);
      syncArtifacts();
    })
    .on('change', filepath => {
      console.log(`File changed: ${path.relative(DOCS_DIR, filepath)}`);
      syncArtifacts();
    })
    .on('unlink', filepath => {
      console.log(`File removed: ${path.relative(DOCS_DIR, filepath)}`);
      syncArtifacts();
    });

  console.log('Press Ctrl+C to stop watching');
} else {
  // One-time sync
  await syncArtifacts();
}
```

### 9. Create UI Package

Create `packages/ui/package.json`:

```json
{
  "name": "ui",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./tokens": "./src/tokens/index.ts",
    "./primitives/*": "./src/primitives/*/index.ts"
  },
  "dependencies": {
    "react": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.18"
  }
}
```

Create `packages/ui/src/index.ts`:

```typescript
export * from './tokens';
export * from './primitives/Button';
export * from './primitives/Text';
```

Create placeholder token files:

**packages/ui/src/tokens/tokens.css**:
```css
:root {
  /* Colors - Primitives */
  --color-blue-50: #E3F2FD;
  --color-blue-600: #1E88E5;
  --color-gray-50: #FAFAFA;
  --color-gray-900: #172B4D;

  /* Colors - Semantic */
  --color-text: var(--color-gray-900);
  --color-interactive: var(--color-blue-600);
  --color-background: var(--color-gray-50);

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'Courier New', Courier, monospace;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
}
```

**packages/ui/src/tokens/index.ts**:
```typescript
export const tokens = {
  colors: {
    text: 'var(--color-text)',
    interactive: 'var(--color-interactive)',
    background: 'var(--color-background)',
  },
  spacing: {
    1: 'var(--space-1)',
    2: 'var(--space-2)',
    3: 'var(--space-3)',
    4: 'var(--space-4)',
    6: 'var(--space-6)',
    8: 'var(--space-8)',
  },
  fonts: {
    sans: 'var(--font-sans)',
    mono: 'var(--font-mono)',
  },
};
```

### 9.5. Add Quality Configs to ui

1. Create `packages/ui/tsconfig.json`:
   ```json
   {
     "extends": "../../tsconfig.base.json",
     "compilerOptions": {
       "jsx": "react-jsx",
       "outDir": "dist",
       "declaration": true,
       "declarationMap": true
     },
     "include": ["src"]
   }
   ```

2. Create `packages/ui/vitest.config.ts`:
   ```typescript
   import { defineConfig } from 'vitest/config';
   import react from '@vitejs/plugin-react';

   export default defineConfig({
     plugins: [react()],
     test: {
       globals: false,
       environment: 'jsdom',
       coverage: {
         provider: 'v8',
         reporter: ['text', 'html'],
         include: ['src/**/*.ts', 'src/**/*.tsx'],
         exclude: ['src/**/*.stories.tsx', 'src/**/*.test.tsx'],
         thresholds: {
           lines: 95,
           functions: 95,
           statements: 95,
           branches: 90,
           perFile: true,
         },
       },
     },
   });
   ```

3. Update `packages/ui/package.json` to add quality scripts:
   Merge these scripts into the existing package.json:
   ```json
   {
     "scripts": {
       "typecheck": "tsc --noEmit",
       "lint": "eslint . --max-warnings=0",
       "test": "vitest",
       "test:coverage": "vitest run --coverage",
       "build": "tsc && vite build"
     }
   }
   ```

### 10. Initialize Git Repository

If not already a git repository:

```bash
git init
git add .
git commit -m "Initial commit: SDLC project scaffolding

Generated by /sdlc:init skill

Structure:
- Monorepo with pnpm workspaces
- Storybook planning hub
- Design system package
- Documentation structure

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

If already a git repository, just commit the changes.

### 11. Install Dependencies

```bash
pnpm install
```

**IMPORTANT**: This may take several minutes. Inform the user and wait for completion.

After installation completes, initialize Husky:

```bash
pnpm exec husky init
```

This creates the `.husky/_/` internals. The pre-commit and pre-push hooks were already created in step 4.5.

### 12. Verify Installation

Run basic checks:

```bash
# Verify pnpm workspace
pnpm list --depth 0

# Check if Storybook can build (quick validation)
cd packages/planning-hub && pnpm exec storybook --version
```

Verify quality tooling:

```bash
# Validate package configurations
pnpm run validate:packages

# Check TypeScript compilation
pnpm run typecheck

# Verify linting setup
pnpm run lint

# Check formatting
pnpm run format
```

## Output

After successful initialization, provide:

### Summary

```markdown
✓ Project initialized successfully!

## Created Structure

- Monorepo root with pnpm workspace
- Planning hub (Storybook) at packages/planning-hub/
- Design system at packages/ui/
- Documentation folders in docs/
- Git repository initialized

## Next Steps

1. Start the planning hub:
   \`\`\`bash
   pnpm dev:storybook
   \`\`\`

2. Open http://localhost:6006 in your browser

3. Run the planning wizard:
   \`\`\`bash
   /sdlc:plan
   \`\`\`

## Available Commands

- `pnpm dev:storybook` - Start Storybook development server
- `pnpm build:storybook` - Build static site
- `pnpm format` - Format all files
- `pnpm sync:artifacts` - Sync documentation

## Troubleshooting

If Storybook fails to start:
- Clear cache: `rm -rf node_modules && pnpm install`
- Check Node version: `node --version` (requires 18+)
- Check for port conflicts on 6006

Need help? Check the SDLC plugin README.
```

## Error Handling

### pnpm Not Found

If pnpm is not installed:

```markdown
✗ pnpm is not installed

Please install pnpm before proceeding:

**Option 1: Install globally via npm**
\`\`\`bash
npm install -g pnpm
\`\`\`

**Option 2: Enable corepack (Node 16.13+)**
\`\`\`bash
corepack enable
corepack prepare pnpm@latest --activate
\`\`\`

Then run `/sdlc:init` again.
```

EXIT without proceeding.

### Directory Not Empty

If current directory contains files:

```markdown
⚠ Current directory is not empty

Found existing files/folders:
[list files]

This command will create new files and folders. Proceed? (y/n)
```

If user declines, EXIT.

### Git Not Available

If git is not available, warn but continue:

```markdown
⚠ git is not available

Git repository initialization will be skipped.
You can initialize git manually later with: git init

Continue with initialization? (y/n)
```

### Installation Failures

If pnpm install fails:

```markdown
✗ Dependency installation failed

Please check:
1. Network connection
2. npm registry access
3. Node.js version (requires 18+)

You can try installing manually:
\`\`\`bash
pnpm install
\`\`\`

Or with verbose output:
\`\`\`bash
pnpm install --loglevel=verbose
\`\`\`
```

## Best Practices

1. **Always run pre-flight checks first** - Fail fast if prerequisites missing
2. **Use Write tool for all file creation** - Don't use bash echo or cat
3. **Provide progress updates** - Let user know what's happening
4. **Handle errors gracefully** - Clear error messages with solutions
5. **Verify successful completion** - Run checks after installation

## Variables Reference

When processing templates, substitute these variables:

- `{{PROJECT_NAME}}` - From arguments or current directory name
- `{{PROJECT_DESCRIPTION}}` - Default: "SDLC project with planning hub"
- `{{DATE}}` - Current date in YYYY-MM-DD format

Use bash `sed` or manual string replacement in the LLM context.

## Tool Usage

- **Bash**: Run all commands (git, pnpm, directory checks)
- **Write**: Create all files (templates, configs, scripts)
- **Read**: Read templates from plugin directory
- **Glob**: Find template files
- **Grep**: Search for existing configurations

## Success Criteria

- [ ] pnpm workspace configured
- [ ] Storybook package created with dependencies
- [ ] UI package created
- [ ] Documentation structure created
- [ ] Templates copied and variables substituted
- [ ] Quality gates configured (TypeScript, ESLint, Vitest, etc.)
- [ ] Git hooks configured (Husky with pre-commit and pre-push)
- [ ] Package validation script created
- [ ] Quality documentation created (CONTRIBUTING.md, QUALITY_STANDARDS.md)
- [ ] Git repository initialized (if git available)
- [ ] Dependencies installed successfully
- [ ] Husky initialized
- [ ] Quality checks passing
- [ ] Initial commit created
- [ ] User provided with next steps

That's it! You've successfully initialized an SDLC monorepo project with comprehensive quality gates.
