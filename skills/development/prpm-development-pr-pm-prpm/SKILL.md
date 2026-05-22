---
name: prpm-development
description: Use when developing PRPM (Prompt Package Manager) - comprehensive knowledge base covering architecture, format conversion, package types, collections, quality standards, testing, and deployment
---

# PRPM Development Knowledge Base

Complete knowledge base for developing PRPM - the universal package manager for AI prompts, agents, and rules.

## Mission

Build the npm/cargo/pip equivalent for AI development artifacts. Enable developers to discover, install, share, and manage prompts across Cursor, Claude Code, Continue, Windsurf, and future AI editors.

## Core Architecture

### Universal Format Philosophy
1. **Canonical Format**: All packages stored in normalized JSON structure
2. **Smart Conversion**: Server-side format conversion with quality scoring  
3. **Zero Lock-In**: Users convert between any format without data loss
4. **Format-Specific Optimization**: IDE-specific variants (e.g., Claude with MCP)

### Package Manager Best Practices
- **Semantic Versioning**: Strict semver for all packages
- **Dependency Resolution**: Smart conflict resolution like npm/cargo
- **Lock Files**: Reproducible installs (prpm-lock.json)
- **Registry-First**: All operations through central registry API
- **Caching**: Redis caching for converted packages (1-hour TTL)

### Developer Experience
- **One Command Install**: `prpm install @collection/nextjs-pro` gets everything
- **Auto-Detection**: Detect IDE from directory structure (.cursor/, .claude/)
- **Format Override**: `--as claude` to force specific format
- **Telemetry Opt-Out**: Privacy-first with easy opt-out
- **Beautiful CLI**: Clear progress indicators and colored output

### Git Workflow - CRITICAL RULES

**⚠️ NEVER PUSH DIRECTLY TO MAIN ⚠️**

PRPM uses a **branch-based workflow** with CI/CD automation. Direct pushes to main bypass all safety checks and can break production.

**ALWAYS follow this workflow:**

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make commits** on your branch using conventional commit format:
   ```bash
   git add [files]
   git commit -m "feat: add OpenCode format support"
   ```

### Commit Message Format

Use conventional commit prefixes for all commits:

| Prefix | Use For | Example |
|--------|---------|---------|
| `feat:` | New features | `feat: add Kiro format support` |
| `fix:` | Bug fixes | `fix: resolve publish timeout issue` |
| `docs:` | Documentation | `docs: update API reference` |
| `chore:` | Maintenance | `chore(release): publish packages` |
| `refactor:` | Code refactoring | `refactor: simplify converter logic` |
| `test:` | Test changes | `test: add roundtrip tests for Gemini` |
| `perf:` | Performance | `perf: optimize search query` |

**Why this matters:**
- Automated changelog generation
- Clear commit history
- Easier code review
- Semantic versioning automation

**Bad commits to avoid:**
```bash
# ❌ Too vague
git commit -m "fixes"
git commit -m "updates"
git commit -m "changes"

# ✅ Clear and descriptive
git commit -m "fix: resolve schema validation for Claude agents"
git commit -m "feat: add support for Droid format subtypes"
```

3. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - Automated CI tests run
   - Code review happens
   - Deployments are controlled

5. **After PR approval**, merge through GitHub UI:
   - Triggers automated deployment
   - Ensures CI passes first
   - Maintains deployment history

**Why this matters:**
- Main branch is protected and deploys to production
- Direct pushes skip CI tests, linting, type checks
- Can deploy broken code to 7500+ package registry
- Breaks audit trail and rollback capability
- GitHub Actions workflows expect PRs, not direct pushes

**If you accidentally pushed to main:**
1. **DO NOT** force push to revert - breaks CI/CD
2. Create a revert commit on a branch
3. Open PR to fix the issue properly
4. Let CI/CD handle the corrective deployment

**Exception:** Only repository admins can push to main for emergency hotfixes (with explicit approval).

## Package Types

### 🎓 Skill
**Purpose**: Knowledge and guidelines for AI assistants
**Location**: `.claude/skills/`, `.cursor/rules/`
**Examples**: `@prpm/pulumi-troubleshooting`, `@typescript/best-practices`

### 🤖 Agent  
**Purpose**: Autonomous AI agents for multi-step tasks
**Location**: `.claude/agents/`, `.cursor/agents/`
**Examples**: `@prpm/code-reviewer`, `@cursor/debugging-agent`

### 📋 Rule
**Purpose**: Specific instructions or constraints for AI behavior
**Location**: `.cursor/rules/`, `.cursorrules`
**Examples**: `@cursor/react-conventions`, `@cursor/test-first`

### 🔌 Plugin
**Purpose**: Extensions that add functionality
**Location**: `.cursor/plugins/`, `.claude/plugins/`

### 💬 Prompt
**Purpose**: Reusable prompt templates
**Location**: `.prompts/`, project-specific directories

### ⚡ Workflow
**Purpose**: Multi-step automation workflows
**Location**: `.workflows/`, `.github/workflows/`

### 🔧 Tool
**Purpose**: Executable utilities and scripts
**Location**: `scripts/`, `tools/`, `.bin/`

### 📄 Template
**Purpose**: Reusable file and project templates
**Location**: `templates/`, project-specific directories

### 🔗 MCP Server
**Purpose**: Model Context Protocol servers
**Location**: `.mcp/servers/`

## Format Conversion System

### Supported Formats

**Cursor (.mdc)**
- MDC frontmatter with `ruleType`, `alwaysApply`, `description`
- Markdown body
- Simple, focused on coding rules
- No structured tools/persona definitions

**Claude (agent format)**
- YAML frontmatter: `name`, `description`
- Optional: `tools` (comma-separated), `model` (sonnet/opus/haiku/inherit)
- Markdown body
- Supports persona, examples, instructions

**Continue (JSON)**
- JSON configuration
- Simple prompts, context rules
- Limited metadata support

**Windsurf**
- Similar to Cursor
- Markdown-based
- Basic structure

### Conversion Quality Scoring (0-100)

Start at 100 points, deduct for lossy conversions:
- Missing tools: -10 points
- Missing persona: -5 points
- Missing examples: -5 points
- Unsupported sections: -10 points each
- Format-specific features lost: -5 points

### Lossless vs Lossy Conversions
- **Canonical ↔ Claude**: Nearly lossless (95-100%)
- **Canonical ↔ Cursor**: Lossy on tools/persona (70-85%)
- **Canonical ↔ Continue**: Most lossy (60-75%)

## Collections System

Collections are curated bundles of packages that solve specific use cases.

### Collection Structure
```json
{
  "id": "@collection/nextjs-pro",
  "name": "Next.js Professional Setup",
  "description": "Complete Next.js development setup",
  "category": "frontend",
  "packages": [
    {
      "packageId": "react-best-practices",
      "required": true,
      "reason": "Core React patterns"
    },
    {
      "packageId": "typescript-strict",
      "required": true,
      "reason": "Type safety"
    },
    {
      "packageId": "tailwind-helper",
      "required": false,
      "reason": "Styling utilities"
    }
  ]
}
```

### Collection Installation Behavior

Collections can be installed using multiple identifier formats. The system intelligently resolves collections based on the format provided.

#### Installation Formats (Priority Order)

**1. Recommended Format: `collections/{slug}`**
```bash
prpm install collections/nextjs-pro
prpm install collections/nextjs-pro@2.0.0
```
- **Behavior**: Searches across ALL scopes for `name_slug = "nextjs-pro"`
- **Resolution**: Prioritizes by official → verified → downloads → created_at
- **Use Case**: User-friendly format for discovering popular collections
- **Example**: Finds `khaliqgant/nextjs-pro` even when searching `collections/nextjs-pro`

**2. Explicit Scope: `{scope}/{slug}` or `@{scope}/{slug}`**
```bash
prpm install khaliqgant/nextjs-pro
prpm install @khaliqgant/nextjs-pro
prpm install khaliqgant/nextjs-pro@2.0.0
```
- **Behavior**: Searches for specific `scope` and `name_slug` combination
- **Resolution**: Exact match only within that scope
- **Use Case**: Installing a specific author's version when multiple exist
- **Example**: Gets specifically the collection published by `khaliqgant`

**3. Name-Only Format: `{slug}`** (Legacy/Fallback)
```bash
prpm install nextjs-pro
prpm install nextjs-pro@1.0.0
```
- **Behavior**: Defaults to `scope = "collection"`, then falls back to cross-scope search
- **Resolution**: First tries scope="collection", then searches all scopes
- **Use Case**: Quick installs when collection origin doesn't matter
- **Recommendation**: Prefer `collections/{slug}` for clarity

#### Registry Resolution Logic

**Implementation Location**: `app/packages/registry/src/routes/collections.ts:485-519`

```typescript
// When scope is 'collection' (default from CLI for collections/* prefix):
if (scope === 'collection') {
  // Search across ALL scopes, prioritize by:
  // 1. Official collections (official = true)
  // 2. Verified authors (verified = true)
  // 3. Most downloads
  // 4. Most recent
  SELECT * FROM collections
  WHERE name_slug = $1
  ORDER BY official DESC, verified DESC, downloads DESC, created_at DESC
  LIMIT 1
} else {
  // Explicit scope: exact match only
  SELECT * FROM collections
  WHERE scope = $1 AND name_slug = $2
  ORDER BY created_at DESC
  LIMIT 1
}
```

#### CLI Resolution Logic

**Implementation Location**: `app/packages/cli/src/commands/collections.ts:487-504`

```typescript
// Parse collection spec:
// - collections/nextjs-pro → scope='collection', name_slug='nextjs-pro'
// - khaliqgant/nextjs-pro → scope='khaliqgant', name_slug='nextjs-pro'
// - @khaliqgant/nextjs-pro → scope='khaliqgant', name_slug='nextjs-pro'
// - nextjs-pro → scope='collection', name_slug='nextjs-pro'

const matchWithScope = collectionSpec.match(/^@?([^/]+)\/([^/@]+)(?:@(.+))?$/);
if (matchWithScope) {
  [, scope, name_slug, version] = matchWithScope;
} else {
  // No scope: default to 'collection'
  [, name_slug, version] = collectionSpec.match(/^([^/@]+)(?:@(.+))?$/);
  scope = 'collection';
}
```

#### Version Resolution

Collections support semantic versioning:

```bash
# Latest version (default)
prpm install collections/nextjs-pro

# Specific version
prpm install collections/nextjs-pro@2.0.4

# With scope and version
prpm install khaliqgant/nextjs-pro@2.0.4
```

**Registry Behavior**:
- Without version: Returns latest (most recent `created_at`)
- With version: Exact match required

#### Discovery Prioritization

When searching across all scopes (`collections/*` format), the system prioritizes:

1. **Official Collections** (official = true)
   - Curated by PRPM maintainers
   - Highest trust level

2. **Verified Authors** (verified = true)
   - Known community contributors
   - GitHub verified

3. **Download Count** (downloads DESC)
   - Most popular collections
   - Community validation

4. **Recency** (created_at DESC)
   - Latest versions
   - Actively maintained

#### Error Handling

**Collection Not Found**:
```bash
prpm install collections/nonexistent
# ❌ Failed to install collection: Collection not found
```

**Scope-Specific Not Found**:
```bash
prpm install wrongscope/nextjs-pro
# ❌ Failed to install collection: Collection not found
# Suggestion: Try 'collections/nextjs-pro' to search all scopes
```

### Collection Best Practices

1. **Required vs Optional**: Clearly mark essential vs nice-to-have packages
2. **Reason Documentation**: Every package explains why it's included
3. **IDE-Specific Variants**: Different packages per editor when needed
4. **Installation Order**: Consider dependencies
5. **Scope Naming**:
   - Use your username/org as scope for personal collections
   - Reserve "collection" scope for official PRPM collections
6. **User-Friendly IDs**: Use descriptive slugs (e.g., "nextjs-pro" not "np-setup")
7. **Version Incrementing**: Bump versions on meaningful changes (follow semver)

## Quality & Ranking System

### Multi-Factor Scoring (0-100)

**Popularity** (0-30 points):
- Total downloads (weighted by recency)
- Stars/favorites
- Trending velocity

**Quality** (0-30 points):
- User ratings (1-5 stars)
- Review sentiment
- Documentation completeness

**Trust** (0-20 points):
- Verified author badge
- Original creator vs fork
- Publisher reputation
- Security scan results

**Recency** (0-10 points):
- Last updated date (<30 days = 10 points)
- Release frequency
- Active maintenance

**Completeness** (0-10 points):
- Has README
- Has examples
- Has tags
- Complete metadata

## Technical Stack

### CLI (TypeScript + Node.js)
- **Commander.js**: CLI framework
- **Fastify Client**: HTTP client for registry
- **Tar**: Package tarball creation/extraction
- **Chalk**: Terminal colors
- **Ora**: Spinners for async operations

### Registry (TypeScript + Fastify + PostgreSQL)
- **Fastify**: High-performance web framework
- **PostgreSQL**: Primary database with GIN indexes
- **Redis**: Caching layer for converted packages
- **GitHub OAuth**: Authentication provider
- **Docker**: Containerized deployment

### Testing
- **Vitest**: Unit and integration tests
- **100% Coverage Goal**: Especially for format converters
- **Round-Trip Tests**: Ensure conversion quality
- **Fixtures**: Real-world package examples

## Testing Standards

### Test Pyramid
- **70% Unit Tests**: Format converters, parsers, utilities
- **20% Integration Tests**: API routes, database operations, CLI commands
- **10% E2E Tests**: Full workflows (install, publish, search)

### Coverage Goals
- **Format Converters**: 100% coverage (critical path)
- **CLI Commands**: 90% coverage
- **API Routes**: 85% coverage
- **Utilities**: 90% coverage

### Key Testing Patterns
```typescript
// Format converter test
describe('toCursor', () => {
  it('preserves data in roundtrip', () => {
    const result = toCursor(canonical);
    const back = fromCursor(result.content);
    expect(back).toEqual(canonical);
  });
});

// CLI command test
describe('install', () => {
  it('downloads and installs package', async () => {
    await handleInstall('test-pkg', { as: 'cursor' });
    expect(fs.existsSync('.cursor/rules/test-pkg.md')).toBe(true);
  });
});
```

## Development Workflow

### Package Manager: npm (NOT pnpm)

**⚠️ CRITICAL: PRPM uses npm, not pnpm ⚠️**

- **Lock file**: `package-lock.json` (npm)
- **Install dependencies**: `npm install`
- **Run scripts**: `npm run <script>`
- **Workspace commands**: `npm run <script> --workspace=<package>`

**DO NOT use pnpm:**
- The repository has `package-lock.json`, not `pnpm-lock.yaml`
- Using pnpm will create conflicts and inconsistencies
- CI/CD uses npm for builds and deployments
- All documentation assumes npm

**Common commands:**
```bash
# Install all dependencies
npm install

# Install in specific workspace
npm install --workspace=@pr-pm/cli

# Run tests
npm test

# Build all packages
npm run build

# Run CLI locally
npm run dev --workspace=prpm
```

### When Adding Features
1. **Check Existing Patterns**: Look at similar commands/routes
2. **Update Types First**: TypeScript interfaces drive implementation
3. **Write Tests**: Create test fixtures and cases
4. **Document**: Update README and relevant docs
5. **Environment Variables**: If adding new env vars, update `.env.example` immediately
6. **Telemetry**: Add tracking for new commands (with privacy)

### When Fixing Bugs
1. **Write Failing Test**: Reproduce the bug in a test
2. **Fix Minimally**: Smallest change that fixes the issue
3. **Check Round-Trip**: Ensure conversions still work
4. **Update Fixtures**: Add bug case to test fixtures

### Dependency Management Best Practices

**AVOID Runtime Dependencies (Dynamic Imports)**

❌ **Bad**: Using dynamic imports for runtime dependencies
```typescript
// BAD - tar-stream is imported dynamically at runtime
const tarStream = await import('tar-stream');
```

**Problems with Dynamic Imports:**
1. **Module Resolution Failures**: In production (Elastic Beanstalk, Docker), dynamic imports can fail to resolve even if the package is installed as a transitive dependency
2. **Build Complexity**: TypeScript compilation doesn't validate dynamic imports
3. **Deployment Issues**: Package may not be in the module resolution path in production
4. **Harder to Debug**: Failures happen at runtime, not at build time

✅ **Good**: Declare all dependencies explicitly
```typescript
// GOOD - Import normally at the top
import * as tarStream from 'tar-stream';
```

**Dependency Guidelines:**
1. **Explicit Dependencies**: Always declare dependencies in package.json, never rely on transitive dependencies
2. **Static Imports**: Use static imports whenever possible for compile-time validation
3. **Production Dependencies**: If you import it, it should be in `dependencies`, not `devDependencies`
4. **Build-Time Validation**: Let TypeScript catch missing dependencies at build time, not runtime

### Environment Variable Management

**ALWAYS Update .env.example When Adding New Environment Variables**

Environment variables are configuration points. When adding new ones, follow this checklist:

1. **Add to `.env.example` immediately** - Don't wait until later
2. **Group logically** - Place in appropriate section (DATABASE, AUTH, etc.)
3. **Add clear comments** - Explain what it does and where to get values
4. **Include examples** - Show format (e.g., `sk-ant-api03-...` for API keys)
5. **Mark optional vs required** - Comment out optional variables with `#`
6. **Update production notes** - Add to deployment checklist if needed

**Example:**
```bash
# ==============================================================================
# NEW FEATURE SECTION
# ==============================================================================

# Description of what this variable does
# Get from: https://where-to-get-it.com
NEW_FEATURE_API_KEY=your-key-here

# Optional feature flag (default: false)
# ENABLE_NEW_FEATURE=true
```

**Why this matters:**
- New developers need to know what env vars to set
- `.env.example` is the source of truth for configuration
- Missing env vars cause runtime errors that are hard to debug
- Production deployments fail without proper env var documentation

**Finding missing env vars:**
```bash
# Search for all process.env usage
grep -rh "process.env\." packages/ --include="*.ts" --include="*.tsx" | \
  grep -o "process\.env\.[A-Z_][A-Z0-9_]*" | sort -u

# Compare with .env.example to find gaps
```

### When Designing APIs
- **REST Best Practices**: Proper HTTP methods and status codes
- **Versioning**: All routes under `/api/v1/`
- **Pagination**: Limit/offset for list endpoints
- **Filtering**: Support query params for filtering
- **OpenAPI**: Document with Swagger/OpenAPI specs

## Security Standards

- **No Secrets in DB**: Never store GitHub tokens, use session IDs
- **SQL Injection**: Parameterized queries only
- **Rate Limiting**: Prevent abuse of registry API
- **Content Security**: Validate package contents before publishing

## Performance Considerations

- **Batch Operations**: Use Promise.all for independent operations
- **Database Indexes**: GIN for full-text, B-tree for lookups
- **Caching Strategy**: Cache converted packages, not raw data
- **Lazy Loading**: Don't load full package data until needed
- **Connection Pooling**: Reuse PostgreSQL connections

## Deployment

### AWS Infrastructure

#### Registry Backend (Elastic Beanstalk)
- **Environment**: Node.js 20 on 64bit Amazon Linux 2023
- **Instance**: t3.micro (cost-optimized)
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache Redis
- **DNS**: Route 53
- **SSL**: ACM certificates

#### Webapp (S3 Static Export) ⚠️ CRITICAL
**The webapp MUST be deployable as a static site via S3/CloudFront.**

**Requirements:**
- Next.js with `output: 'export'` configuration
- **NO server-side rendering (SSR)** - all pages must be static or client-side rendered
- **NO API routes** - all API calls go to the registry backend
- **Dynamic routes require `generateStaticParams()`** - return empty array `[]` for client-side only routes
- All data fetching must be client-side (useEffect, fetch, etc.)

**Common Issues:**
1. **Dynamic routes in client components** ⚠️ CANNOT USE BOTH
   - Error: `Page "page" cannot use both "use client" and export function "generateStaticParams()"`
   - **Solution**: Use query strings instead of path parameters
   - ❌ Wrong: `/playground/shared/[token]/page.tsx` with `'use client'`
   - ✅ Correct: `/playground/shared/page.tsx` with `?token=xxx` query param
   - Implementation: Use `useSearchParams()` instead of `useParams()`
   - **IMPORTANT**: Must wrap `useSearchParams()` in `<Suspense>` boundary
   - Example:
     ```typescript
     // ❌ Dynamic route (doesn't work with 'use client')
     // /app/shared/[token]/page.tsx
     const params = useParams();
     const token = params.token;

     // ✅ Query string with Suspense (works with 'use client')
     // /app/shared/page.tsx
     import { Suspense } from 'react';

     function Content() {
       const searchParams = useSearchParams();
       const token = searchParams.get('token');
       // ... component logic
     }

     export default function Page() {
       return (
         <Suspense fallback={<div>Loading...</div>}>
           <Content />
         </Suspense>
       );
     }
     ```

2. **Server components in static export**
   - All pages with dynamic content must use `'use client'` directive
   - Shared session pages, playground interfaces, etc. are client-rendered

3. **Environment variables**
   - Build-time: Embedded in static bundle (public/exposed)
   - Runtime: Fetched via API from registry backend

**Why S3 Static Export?**
- Cost: $0.023/GB vs $30+/month for server hosting
- Scale: CloudFront CDN handles traffic spikes
- Reliability: No server maintenance or downtime
- Performance: Pre-rendered static pages are instant

### GitHub Actions Workflows
- **Test & Deploy**: Runs on push to main
- **NPM Publish**: Manual trigger for releases
- **Homebrew Publish**: Updates tap formula
- **Webapp Deploy**: Builds static export and deploys to S3

### Publishing PRPM to NPM

**Publishable Packages:**
- `prpm` - CLI (public)
- `@prpm/registry-client` - HTTP client (public)
- Registry and Infra are private (deployed, not published)

**Process:**
1. Go to Actions → NPM Publish
2. Select version bump (patch/minor/major)
3. Choose packages (all or specific)
4. Run workflow

**Homebrew Formula:**
- Formula repository: `khaliqgant/homebrew-prpm`
- Auto-updates on NPM publish
- Requires `HOMEBREW_TAP_TOKEN` secret

**Version Bumping:**
```bash
# CLI and client together
npm version patch --workspace=prpm --workspace=@prpm/registry-client

# Individual package
npm version minor --workspace=prpm
```

### Publish Command Troubleshooting

The publish command is a complex flow. Common issues and fixes:

| Issue | Cause | Fix |
|-------|-------|-----|
| `Schema not found` | Schemas not copied to dist | Ensure build copies schemas: check `tsup.config.ts` |
| `Cannot find module '@pr-pm/types'` | Types not built first | Run `npm run build --workspace=@pr-pm/types` first |
| `Type export missing` | tsup not exporting types | Check `dts: true` in tsup.config.ts |
| `Version mismatch` | Workspaces out of sync | Bump all related packages together |
| `Tarball too large` | Including unnecessary files | Check `.npmignore` or `files` in package.json |
| `Authentication failed` | Token expired/missing | Re-run `prpm login` or check `PRPM_TOKEN` |

**Build Order for Publishing:**
```bash
# Always build in dependency order
npm run build --workspace=@pr-pm/types
npm run build --workspace=@pr-pm/converters
npm run build --workspace=@pr-pm/registry-client
npm run build --workspace=prpm
```

**Pre-Publish Checklist:**
1. ✅ All tests pass: `npm test`
2. ✅ Types compile: `npm run typecheck`
3. ✅ Build succeeds: `npm run build`
4. ✅ Version bumped in all affected packages
5. ✅ Schemas copied to dist (for CLI)
6. ✅ No uncommitted changes

**Debugging Publish Issues:**
```bash
# Check what will be published
npm pack --workspace=prpm --dry-run

# Verify package contents
tar -tzf prpm-*.tgz

# Check for missing exports
node -e "console.log(require('./packages/cli/dist/index.js'))"
```

## Common Patterns

### CLI Command Structure
```typescript
export async function handleCommand(args: Args, options: Options) {
  const startTime = Date.now();
  try {
    const config = await loadUserConfig();
    const client = getRegistryClient(config);
    const result = await client.fetchData();
    console.log('✅ Success');
    await telemetry.track({ command: 'name', success: true });
  } catch (error) {
    console.error('❌ Failed:', error.message);
    await telemetry.track({ command: 'name', success: false });
    process.exit(1);
  }
}
```

### CLI Error Handling Pattern

**Use `CLIError` instead of `process.exit()` for testable CLI errors.**

```typescript
// ❌ BAD - Untestable, tests can't catch process.exit()
if (!packageId) {
  console.error('Package ID is required');
  process.exit(1);
}

// ✅ GOOD - Testable with CLIError
import { CLIError } from '../utils/cli-error.js';

if (!packageId) {
  throw new CLIError('Package ID is required', { exitCode: 1 });
}
```

**Why CLIError?**
- Tests can catch and verify error conditions
- Consistent error formatting across CLI
- Exit codes are explicit and documented
- Enables reliable CI testing (PR #110 refactor)

**CLIError Usage:**
```typescript
import { CLIError, createError, createSuccess } from '../utils/cli-error.js';

// Simple error
throw new CLIError('Something went wrong');

// With exit code
throw new CLIError('Invalid format specified', { exitCode: 1 });

// With suggestions
throw new CLIError('Package not found', {
  exitCode: 1,
  suggestion: 'Try running: prpm search <query>'
});

// Helper functions for consistent messaging
createError('Operation failed');     // Returns formatted error
createSuccess('Package installed'); // Returns formatted success
```

**Testing CLI Errors:**
```typescript
import { describe, it, expect } from 'vitest';
import { CLIError } from '../utils/cli-error.js';

describe('install command', () => {
  it('throws CLIError for missing package', async () => {
    await expect(handleInstall('')).rejects.toThrow(CLIError);
  });

  it('provides helpful error message', async () => {
    try {
      await handleInstall('');
    } catch (error) {
      expect(error).toBeInstanceOf(CLIError);
      expect(error.message).toContain('Package ID is required');
    }
  });
});
```

### Registry Route Structure
```typescript
server.get('/:id', {
  schema: { /* OpenAPI schema */ },
}, async (request, reply) => {
  const { id } = request.params;
  if (!id) return reply.code(400).send({ error: 'Missing ID' });
  const result = await server.pg.query('SELECT...');
  return result.rows[0];
});
```

### Format Converter Structure
```typescript
export function toFormat(pkg: CanonicalPackage): ConversionResult {
  const warnings: string[] = [];
  let qualityScore = 100;
  const content = convertSections(pkg.content.sections, warnings);
  const lossyConversion = warnings.some(w => w.includes('not supported'));
  if (lossyConversion) qualityScore -= 10;
  return { content, format: 'target', warnings, qualityScore, lossyConversion };
}
```

## Naming Conventions

- **Files**: kebab-case (`registry-client.ts`, `to-cursor.ts`)
- **Types**: PascalCase (`CanonicalPackage`, `ConversionResult`)
- **Functions**: camelCase (`getPackage`, `convertToFormat`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_REGISTRY_URL`)
- **Database**: snake_case (`package_id`, `created_at`)
- **API Requests/Responses**: snake_case (`package_id`, `session_id`, `created_at`)
  - **Important**: All API request and response fields use snake_case to match PostgreSQL database conventions
  - Internal service methods may use camelCase, but must convert to snake_case at API boundaries
  - TypeScript interfaces for API types should use snake_case fields
  - Examples: `PlaygroundRunRequest.package_id`, `CreditBalance.reset_at`

## Documentation Standards

- **Inline Comments**: Explain WHY, not WHAT
- **JSDoc**: Required for public APIs
- **README**: Keep examples up-to-date
- **Markdown Docs**: Use code blocks with language tags
- **Changelog**: Follow Keep a Changelog format
- **Continuous Accuracy**: Documentation must be continuously updated and tended to for accuracy
  - When adding features, update relevant docs immediately
  - When fixing bugs, check if docs need corrections
  - When refactoring, verify examples still work
  - Review docs quarterly for outdated information
  - Keep CLI docs, README, and Mintlify docs in sync

## Reference Documentation

See supporting files in this skill directory for detailed information:
- `format-conversion.md` - Complete format conversion specs
- `package-types.md` - All package types with examples
- `collections.md` - Collections system and examples
- `quality-ranking.md` - Quality and ranking algorithms
- `testing-guide.md` - Testing patterns and standards
- `deployment.md` - Deployment procedures

Remember: PRPM is infrastructure. It must be rock-solid, fast, and trustworthy like npm or cargo.
