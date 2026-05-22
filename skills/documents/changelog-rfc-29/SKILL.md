---
name: changelog-rfc-29
description: >
  RFC-29 compliant changelog management with Common Changelog format and Unreleased
  section extension. Validates changelog on commits, generates from git history,
  and ensures all merged PRs are documented. Use when setting up changelog workflows
  or retrofitting existing repositories.
compatibility: Requires Node.js 20+; works with any Git repository
metadata:
  version: "1.1.0"
  targeting:
    include:
      - repo: "bitsoex/ai-code-instructions"
  tags:
    - changelog
    - rfc-29
    - documentation
    - versioning
---

# Changelog (RFC-29)

Enforce and validate changelogs following the [Common Changelog](https://common-changelog.org/) specification with an [Unreleased section extension](references/unreleased-extension.md) for in-progress work.

## When to Use This Skill

- Setting up changelog workflow in a new repository
- Retrofitting changelog from git history
- Validating changelog format in pre-commit/pre-push hooks
- Ensuring PR coverage in changelog during CI
- Understanding Common Changelog format requirements

## Skill Contents

### Sections

- [When to Use This Skill](#when-to-use-this-skill) (L25-L32)
- [Quick Start](#quick-start) (L73-L106)
- [Format Specification](#format-specification) (L107-L164)
- [Validation Rules](#validation-rules) (L165-L194)
- [Scripts](#scripts) (L195-L282)
- [Migration](#migration) (L283-L315)
- [Integration](#integration) (L316-L373)
- [Exclusions](#exclusions) (L374-L399)
- [Related Skills](#related-skills) (L400-L407)
- [Troubleshooting](#troubleshooting) (L408-L445)

### Available Resources

**📚 references/** - Detailed documentation
- [common changelog spec](references/common-changelog-spec.md)
- [hallmark feature analysis](references/hallmark-feature-analysis.md)
- [migration guide](references/migration-guide.md)
- [unreleased extension](references/unreleased-extension.md)

**🔧 scripts/** - Automation scripts
- [check updated](scripts/check-updated.ts)
- [constants](scripts/constants.ts)
- [coverage](scripts/coverage.ts)
- [import releases](scripts/import-releases.ts)
- [migrate](scripts/migrate.ts)
- [parse](scripts/parse.ts)
- [retrofit](scripts/retrofit.ts)
- [semver](scripts/semver.ts)
- [validate](scripts/validate.ts)

**📦 assets/** - Templates and resources
- [changelog template](assets/changelog-template.md)
- [exclusion patterns](assets/exclusion-patterns.json)

---

## Quick Start

### Creating a new CHANGELOG.md

Copy the template and customize:

```bash
cp global/skills/changelog-rfc-29/assets/changelog-template.md CHANGELOG.md
```

### Validating an existing changelog

```bash
pnpm run skills:changelog
# or
node .scripts/skills-cli.ts changelog validate
```

### Checking PR coverage

```bash
pnpm run skills:changelog:coverage
# or
node .scripts/skills-cli.ts changelog coverage
```

### Retrofitting from git history

```bash
pnpm run skills:changelog:retrofit
# or
node .scripts/skills-cli.ts changelog retrofit
```

## Format Specification

### File Structure

```markdown
# Changelog

> Optional description or note about the changelog format.

## [Unreleased]

### Added

- Add new feature ([#123](https://github.com/org/repo/pull/123))

## [2.0.0] - 2026-01-19

_Optional notice about this release._

### Changed

- **Breaking:** Major refactor ([#100](https://github.com/org/repo/pull/100))

### Added

- Add feature X ([#95](https://github.com/org/repo/pull/95))

### Fixed

- Fix bug Y ([#90](https://github.com/org/repo/pull/90))

[Unreleased]: https://github.com/org/repo/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/org/repo/releases/tag/v2.0.0
```

### Category Order

Categories MUST appear in this order (only include those with changes):

1. **Changed** - modifications to existing functionality
2. **Added** - new features
3. **Removed** - removed features
4. **Fixed** - bug fixes

### Change Format

Each change must:

1. Start with imperative verb (Add, Fix, Remove, Update, etc.)
2. Include at least one reference (PR number or commit hash)
3. Use `**Breaking:** ` prefix for breaking changes

```markdown
- Add user authentication ([#45](https://github.com/org/repo/pull/45))
- **Breaking:** Remove deprecated API ([#50](https://github.com/org/repo/pull/50))
- Fix memory leak in worker pool ([`abc1234`](https://github.com/org/repo/commit/abc1234))
```

## Validation Rules

### Format Validation

| Rule | Description |
|------|-------------|
| File exists | CHANGELOG.md must exist |
| Header | Must start with `# Changelog` |
| Version format | Semver without 'v' prefix (e.g., `2.0.0`) |
| Date format | ISO 8601 (YYYY-MM-DD) |
| Category names | Only: Changed, Added, Removed, Fixed |
| Category order | Changed > Added > Removed > Fixed |
| References | Each change must have at least one |

### Pre-commit Check

When committing, the changelog check:

1. Gets list of staged files
2. Filters out excluded paths (tests, config, generated files)
3. If significant files are staged, requires CHANGELOG.md to also be staged

### Coverage Validation

Ensures every merged PR is documented:

1. Extracts PR numbers from git history
2. Extracts PR numbers from CHANGELOG.md
3. Reports any PRs missing from changelog

## Scripts

### parse.js

Parse CHANGELOG.md into structured data:

```javascript
import { parseChangelog, extractReferences, parseVersion } from './scripts/parse.ts';

const content = fs.readFileSync('CHANGELOG.md', 'utf-8');
const parsed = parseChangelog(content);

// parsed = {
//   title: 'Changelog',
//   releases: [
//     { version: 'Unreleased', date: null, groups: [...] },
//     { version: '2.0.0', date: '2026-01-19', notice: '...', groups: [...] }
//   ]
// }
```

### validate.js

Validate changelog format:

```javascript
import { validateChangelog } from './scripts/validate.ts';

const result = await validateChangelog('/path/to/repo');
// result = { passed: true/false, errors: [], warnings: [] }
```

### check-updated.js

Pre-commit hook integration:

```javascript
import { checkChangelogUpdated } from './scripts/check-updated.ts';

const result = await checkChangelogUpdated('/path/to/repo');
// result = { passed: true/false, message: '...', errors: [] }
```

### retrofit.js

Generate changelog from git history:

```javascript
import { retrofitChangelog } from './scripts/retrofit.ts';

const result = await retrofitChangelog({
  rootDir: '/path/to/repo',
  version: '2.0.0',
  date: '2026-01-19',
  repoUrl: 'https://github.com/org/repo'
});
// result = { markdown: '...', prCount: 106, categorized: {...} }
```

### coverage.js

Validate PR coverage:

```javascript
import { validateCoverage } from './scripts/coverage.ts';

const result = await validateCoverage('/path/to/repo');
// result = { passed: true/false, missingPRs: [], extraPRs: [] }
```

### migrate.js

Convert existing changelogs to Common Changelog format:

```bash
node global/skills/changelog-rfc-29/scripts/migrate.ts --input CHANGELOG.md --dry-run
node global/skills/changelog-rfc-29/scripts/migrate.ts --input CHANGELOG.md --output CHANGELOG.new.md
```

### import-releases.js

Import GitHub releases as changelog entries:

```bash
node global/skills/changelog-rfc-29/scripts/import-releases.ts --repo bitsoex/my-repo --dry-run
node global/skills/changelog-rfc-29/scripts/import-releases.ts --repo bitsoex/my-repo --output CHANGELOG.md
```

## Migration

For repositories with existing changelogs or release history, see the [Migration Guide](references/migration-guide.md).

### Migration Scenarios

| Current State | Approach |
|---------------|----------|
| Keep a Changelog format | Use `migrate.js` to convert |
| GitHub releases | Use `import-releases.js` to import |
| Git tags only | Use `retrofit.js` to generate |
| No versioning | Copy template, start fresh |

### Converting from Keep a Changelog

```bash
# Preview changes
node global/skills/changelog-rfc-29/scripts/migrate.ts --input CHANGELOG.md --dry-run

# Convert in place
node global/skills/changelog-rfc-29/scripts/migrate.ts --input CHANGELOG.md
```

### Importing GitHub Releases

```bash
# Preview import
node global/skills/changelog-rfc-29/scripts/import-releases.ts --repo bitsoex/my-repo --dry-run

# Generate changelog from releases
node global/skills/changelog-rfc-29/scripts/import-releases.ts --repo bitsoex/my-repo --output CHANGELOG.md
```

## Integration

### Pre-commit Hook

Add to `.scripts/lib/validation.ts`:

```javascript
{
  name: 'Changelog updated',
  command: null,
  customCheck: 'checkChangelogUpdated',
  scope: 'pre-commit',
  blocking: true,
  required: true
}
```

### Pre-push Hook

Add to `.scripts/lib/validation.ts`:

```javascript
{
  name: 'Changelog format',
  command: ['node', '.scripts/skills-cli.ts', 'changelog', 'validate'],
  scope: 'pre-push',
  blocking: true,
  required: true
}
```

### CI Workflow

Add to `.github/workflows/ci.yaml`:

```yaml
- name: Validate Changelog Format
  if: github.event_name == 'pull_request'
  run: pnpm run skills:changelog

- name: Validate PR Coverage
  if: github.event_name == 'pull_request'
  run: pnpm run skills:changelog:coverage
```

### Package.json Scripts

```json
{
  "scripts": {
    "skills:changelog": "node .scripts/skills-cli.ts changelog validate",
    "skills:changelog:check": "node .scripts/skills-cli.ts changelog check-updated",
    "skills:changelog:coverage": "node .scripts/skills-cli.ts changelog coverage",
    "skills:changelog:retrofit": "node .scripts/skills-cli.ts changelog retrofit"
  }
}
```

## Exclusions

Files matching these patterns do NOT require changelog updates.

See [assets/exclusion-patterns.json](assets/exclusion-patterns.json) for the full list.

### Infrastructure

- `.github/` - CI/CD workflows
- `.gitignore`, `.nvmrc` - config files
- `pnpm-lock.yaml` - lock files

### Tests

- `tests/` - test files only

### Generated Content

- `.tmp/`, `coverage/`, `output/` - build outputs
- `.claude/skills/` - distributed content

### Configuration

- `vitest.config.js`, `eslint.config.js` - tooling config
- `.coderabbit.yaml`, `.doclinterrc.yml` - linter config

## Related Skills

| Skill | Purpose |
|-------|---------|
| [quality-checks](.claude/skills/quality-checks/SKILL.md) | Orchestrates quality checks including changelog |
| [git-hooks](.claude/skills/git-hooks/SKILL.md) | Hook infrastructure for pre-commit/pre-push |
| [pr-workflow](.claude/skills/pr-workflow/SKILL.md) | PR creation and management |

## Troubleshooting

### "CHANGELOG.md must be updated"

Your commit includes significant files but CHANGELOG.md is not staged.

**Fix:** Add an entry to the `[Unreleased]` section:

```markdown
## [Unreleased]

### Added

- Describe your change ([#YOUR_PR](https://github.com/org/repo/pull/YOUR_PR))
```

### "Category X is out of order"

Categories must appear in order: Changed > Added > Removed > Fixed.

**Fix:** Reorder your categories to match the expected order.

### "Change has no reference"

Every change must reference a PR or commit.

**Fix:** Add a reference in parentheses:

```markdown
- Your change description ([#123](https://github.com/org/repo/pull/123))
```

### "Invalid version format"

Version must be valid semver without 'v' prefix.

**Good:** `## [2.0.0] - 2026-01-19`
**Bad:** `## [v2.0.0] - 2026-01-19`
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/changelog-rfc-29/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

