---
name: mcp-development
description: MCP server development patterns including bundling, npx distribution, versioning, and collective learning. Use when building new MCP servers or improving existing ones for distribution.
---

# MCP Development Skill

**Principle**: #34 (Occam's Razor Implementation) — applies to distribution complexity too

**Source**: Agent-kernel MCP v2.1.0 development (2026-01-29). Patterns emerged from bundling implementation.

---

## When to Use This Skill

Use the mcp-development skill when:
- Building a new MCP server for distribution
- Packaging an existing MCP for npm
- Setting up auto-update distribution via npx
- Adding resource bundling (principles, skills, etc.)
- Planning collective learning / telemetry

**DO NOT use this skill for:**
- Configuring projects to USE MCP servers (use [mcp-integration](../mcp-integration/SKILL.md))
- MCP protocol internals (use MCP SDK docs)

---

## Companion Skill

| Skill | Audience | Focus |
|-------|----------|-------|
| **mcp-integration** | MCP Users | Configuring projects to adopt MCP tools |
| **mcp-development** | MCP Developers | Building, bundling, distributing MCP servers |

---

## Pattern D1: Resource Bundling

**Problem**: MCP servers often need accompanying resources (prompts, schemas, configs). Without bundling, users must manually set up paths or the MCP fails at runtime.

**Solution**: Bundle resources INTO the npm package.

### Package Structure

```
@scope/mcp-name/
├── build/              # Compiled TypeScript
│   └── index.js
├── resources/          # Bundled resources
│   ├── principles/
│   ├── commands/
│   ├── skills/
│   └── ...
├── bin/                # CLI entry point
│   └── cli.js
├── scripts/
│   └── bundle-resources.js
└── package.json
```

### Build Script

```javascript
// scripts/bundle-resources.js
import { cpSync, mkdirSync, rmSync, existsSync } from 'fs';
import { join, dirname } from 'path';

const SOURCE_DIR = '/path/to/source/.claude';
const RESOURCES_DIR = './resources';

// Clean and recreate
if (existsSync(RESOURCES_DIR)) rmSync(RESOURCES_DIR, { recursive: true });
mkdirSync(RESOURCES_DIR, { recursive: true });

// Bundle directories
const BUNDLE = ['principles', 'commands', 'skills', 'kernel'];
for (const dir of BUNDLE) {
  cpSync(join(SOURCE_DIR, dir), join(RESOURCES_DIR, dir), { recursive: true });
}
```

### package.json Scripts

```json
{
  "scripts": {
    "build": "tsc",
    "bundle": "node scripts/bundle-resources.js",
    "prepublish": "npm run build && npm run bundle"
  },
  "files": ["build", "resources", "bin"]
}
```

### Runtime Resolution

```typescript
// In MCP server index.ts
const PACKAGE_ROOT = path.resolve(__dirname, '..');
const BUNDLED_RESOURCES = path.join(PACKAGE_ROOT, 'resources');
const PROJECT_RESOURCES = path.join(process.env.CLAUDE_PROJECT_DIR || process.cwd(), '.claude');

function resolveResource(type: string): string {
  // Project-specific overrides bundled
  const projectPath = path.join(PROJECT_RESOURCES, type);
  if (existsSync(projectPath)) return PROJECT_RESOURCES;

  // Fall back to bundled
  if (existsSync(BUNDLED_RESOURCES)) return BUNDLED_RESOURCES;

  // Legacy fallback
  return PROJECT_RESOURCES;
}
```

**Key insight**: Users can override bundled resources by creating project-specific files, but the MCP works out-of-box with bundled defaults.

---

## Pattern D2: npx Distribution (Auto-Latest)

**Problem**: MCP users want the latest version without manual `npm update`. MCP developers want instant distribution of improvements.

**Solution**: Use `npx -y @scope/package@latest` in `.mcp.json`.

### User Configuration

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-name@latest"]
    }
  }
}
```

### Version Behavior

| Configuration | Behavior |
|---------------|----------|
| `npx @scope/pkg` | Uses cached version if available |
| `npx @scope/pkg@latest` | **Always checks npm for latest** |
| `npx @scope/pkg@2.1.0` | Pinned to specific version |

### CLI Entry Point

```javascript
#!/usr/bin/env node
// bin/cli.js
import { spawn } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const serverPath = join(__dirname, '..', 'build', 'index.js');

// Handle --help, --info, --version
if (process.argv.includes('--help')) {
  console.log('Usage: npx @scope/mcp-name [options]');
  process.exit(0);
}

// Default: run MCP server
spawn('node', [serverPath], { stdio: 'inherit' });
```

### package.json Configuration

```json
{
  "name": "@scope/mcp-name",
  "bin": {
    "mcp-name": "./bin/cli.js"
  }
}
```

**Key insight**: The `-y` flag auto-confirms install, and `@latest` forces npm registry check on every invocation.

**Trade-off**: Slightly slower startup (~1-2s npm check) but always current.

---

## Pattern D3: Semantic Versioning for MCP

**Problem**: How to version MCP servers when they have both code AND bundled resources?

**Solution**: Version represents the **combined capability**.

### Version Components

| Change | Version Bump | Example |
|--------|--------------|---------|
| New MCP tool | MINOR | 2.0.0 → 2.1.0 |
| Tool behavior change | MINOR | 2.1.0 → 2.2.0 |
| Bundled resource update | PATCH | 2.1.0 → 2.1.1 |
| Breaking tool schema change | MAJOR | 2.1.0 → 3.0.0 |
| Bug fix (code or resources) | PATCH | 2.1.1 → 2.1.2 |

### CHANGELOG Pattern

```markdown
## [2.1.0] - 2026-01-29

### Added
- Resource bundling: 11 principles, 59 commands, 31 skills
- npx distribution support via bin/cli.js
- --info flag to show bundled resources

### Changed
- Path resolution now checks bundled resources as fallback
```

---

## Pattern D4: Collective Learning Hooks (Future)

**Vision**: MCP servers collect opt-in telemetry to improve bundled resources for all users.

### Telemetry Points

| Event | Data Collected | Insight |
|-------|----------------|---------|
| Tool invocation | Tool name, timestamp | Which tools are popular |
| Gradient evaluation | Components, outcome | What patterns lead to success |
| Resource load | Resource type, name | Which resources are used |
| Error occurrence | Tool name, error type | What fails frequently |

### Privacy Principles

1. **Opt-in only**: Never collect without explicit consent
2. **Aggregate only**: No personally identifiable data
3. **Transparent**: Users can see what's collected
4. **Beneficial**: Data directly improves the product

### Feedback Loop

```
Users → Telemetry → Aggregate Analysis → Improved Bundle → New Version → Users
```

**Status**: Future work. See Linear issue for collective learning implementation.

---

## Anti-Patterns

### A1: Coupling to Source Repo

MCP server requires files from the source repository at runtime.

**Fix**: Bundle everything needed into the npm package.

### A2: Hardcoded Paths

MCP assumes specific file paths that only work on developer's machine.

**Fix**: Use `__dirname` relative paths and environment variable overrides.

### A3: Missing bin Entry

Package has no CLI entry point, can't be invoked via npx.

**Fix**: Add `bin` field to package.json with a proper shebang script.

### A4: @latest Without -y

Using `npx @scope/pkg@latest` without `-y` causes interactive prompts.

**Fix**: Always use `npx -y @scope/pkg@latest` in MCP configs.

### A5: No Version Logging

MCP server doesn't log its version on startup, making debugging hard.

**Fix**: Log version in server initialization: `console.error("MCP v2.1.0 running")`

---

## Checklist: Publishing MCP to npm

```
□ TypeScript compiled (npm run build)
□ Resources bundled (npm run bundle)
□ bin/cli.js has shebang (#!/usr/bin/env node)
□ package.json has correct "files" array
□ package.json has "bin" entry
□ Version bumped appropriately
□ CHANGELOG updated
□ README has npx usage example
□ Tested locally with `npx .` in package dir
□ npm publish --access public
```

---

## See Also

- [mcp-integration](../mcp-integration/SKILL.md) — For MCP users (adoption)
- Principle #34: Occam's Razor — Minimal complexity in distribution too
- MCP SDK Documentation — Protocol internals
