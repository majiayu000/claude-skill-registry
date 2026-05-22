---
name: doc-validation-rfc-37
description: >
  Validate documentation structure, freshness, and RFC-37 compliance using
  bitso-documentation-linter. Ensures docs/ folder structure (api, decisions,
  concepts, how-tos, runbooks) and Confluence mirroring metadata. Use when
  validating documentation or checking for sync issues.
compatibility: All repositories with docs/ folder; requires bitso-documentation-linter
metadata:
  version: "1.0.0"
  rfc: "RFC-37"
  linter: "bitso-documentation-linter"
---

# RFC-37 Documentation Validation

Validates documentation structure and synchronization following [RFC-37](https://bitsomx.atlassian.net/wiki/spaces/BAB/pages/4485840987/RFC-37+Service+documentation+standardization) standards.

## When to use this skill

- Validating documentation structure against RFC-37
- Checking if documentation is synchronized with code
- Running documentation linting before commits
- Setting up documentation validation in CI/CD
- Fixing documentation linting violations
- Verifying Confluence mirroring configuration

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L19-L27)
- [Quick Start](#quick-start) (L67-L106)
- [Standard Directory Structure](#standard-directory-structure) (L107-L123)
- [Documentation Validation Checks](#documentation-validation-checks) (L124-L135)
- [Pre-Push Documentation Check](#pre-push-documentation-check) (L136-L175)
- [Available Functions](#available-functions) (L176-L203)
- [Documentation Tools by Project Type](#documentation-tools-by-project-type) (L204-L212)
- [Best Practices](#best-practices) (L213-L234)
- [References](#references) (L235-L244)
- [Assets](#assets) (L245-L252)
- [Related Skills](#related-skills) (L253-L259)

### Available Resources

**📚 references/** - Detailed documentation
- [ai fixes](references/ai-fixes.md)
- [confluence metadata](references/confluence-metadata.md)
- [go](references/go)
- [installation](references/installation.md)
- [java](references/java)
- [python](references/python)
- [rfc 37](references/rfc-37.md)
- [typescript](references/typescript)
- [validation rules](references/validation-rules.md)

**🔧 scripts/** - Automation scripts
- [check docs updated](scripts/check-docs-updated.ts)

**📦 assets/** - Templates and resources
- [doclinterrc.yml.template](assets/doclinterrc.yml.template)
- [local-execution.md.template](assets/local-execution.md.template)
- [mark.toml.template](assets/mark.toml.template)

---

## Quick Start

### 1. Install the linter

```bash
brew tap bitsoex/homebrew-bitso
brew install bitso-documentation-linter
```

See [references/installation.md](references/installation.md) for alternative installation methods.

### 2. Create directory structure

```bash
mkdir -p docs/{decisions,how-tos,runbooks}
mkdir -p docs/my-service/{concepts,getting-started}
```

### 3. Create Confluence config

```bash
# Copy and edit the template
cp assets/mark.toml.template docs/mark.toml
```

See [references/confluence-metadata.md](references/confluence-metadata.md) for configuration details.

### 4. Run validation

```bash
# Basic validation
doclinter --repo-path . --verbose

# Preview Confluence tree
doclinter tree --repo-path .

# Via skills CLI
node .scripts/skills-cli.ts doc-validation-rfc-37 validate
```

## Standard Directory Structure

```
docs/
├── api/                    # API documentation
│   ├── async/              # Event-driven APIs
│   ├── grpc/               # gRPC APIs
│   └── rest/               # REST APIs
├── decisions/              # Architecture Decision Records (required)
├── how-tos/                # Step-by-step guides (required)
│   └── local-execution.md  # REQUIRED for all services
├── runbooks/               # Operational procedures (required)
└── <service-name>/         # Service-specific docs
    ├── concepts/           # Architecture, design (required)
    └── getting-started/    # Quick start (required)
```

## Documentation Validation Checks

| Check | What It Does | Severity |
|-------|-------------|----------|
| **README presence** | Verifies README.md exists | Error |
| **Broken links** | Checks internal Markdown links | Warning |
| **API docs** | Looks for generated API documentation | Info |
| **Freshness** | Compares doc timestamps to code | Warning |
| **RFC-37 structure** | Validates `docs/` folder structure | Error |
| **Confluence metadata** | Validates mark.toml and parent IDs | Error |
| **Local execution** | Checks for required local-execution.md | Error |

## Pre-Push Documentation Check

The system verifies documentation is updated when significant files change.

### Architecture Files That Trigger Doc Checks

```javascript
const ARCHITECTURE_FILES = [
  'technology-hierarchy.json',
  'repo-overrides.json',
  'managed-paths.json',
  '.scripts/convert-rules.ts',
  '.scripts/targeting.ts',
  '.scripts/safe-sync.ts',
  '.scripts/ci-distribute.ts',
  '.github/workflows/ci.yaml'
];
```

### Expected Documentation Updates

When architecture files change, update one of:

- `docs/ai-ide-management/concepts/architecture.md`
- `docs/ai-ide-management/how-tos/targeting-and-inheritance.md`
- `docs/ai-ide-management/overview.md`
- `README.md`

### Skipping the Check

```bash
# For a single commit (when docs truly aren't needed)
AI_AGENTS_SKIP_DOCS_CHECK=1 git commit -m "chore: minor config tweak"

# Or document why in commit message
git commit -m "fix: typo in config

No docs update needed - cosmetic change only"
```

## Available Functions

### Via Skills CLI

```bash
node .scripts/skills-cli.ts doc-validation-rfc-37 validate
node .scripts/skills-cli.ts doc-validation-rfc-37 lint
```

### Programmatic Usage

```javascript
import {
  validateDocs,      // Run all documentation checks
  checkReadme,       // Verify README presence
  checkBrokenLinks,  // Find broken internal links
  checkApiDocs,      // Look for API documentation
  checkFreshness,    // Compare doc/code timestamps
  DOC_TOOLS          // Recommended tools by project type
} from './.scripts/lib/skills/doc-sync.ts';

const result = await validateDocs('.', { quiet: false });

console.log('Passed:', result.passed);
console.log('Issues:', result.issues);
console.log('Warnings:', result.warnings);
```

## Documentation Tools by Project Type

| Project | Tools | Commands |
|---------|-------|----------|
| **Java/Gradle** | Javadoc, Checkstyle | `./gradlew javadoc` |
| **Node.js** | TypeDoc, JSDoc, markdownlint | `npx typedoc`, `npx markdownlint "**/*.md"` |
| **Python** | Sphinx, pydocstyle, MkDocs | `sphinx-build`, `pydocstyle` |
| **Go** | godoc, go doc | `go doc -all` |

## Best Practices

### 1. Document As You Code

- Update docs in the same PR as code changes
- Use the pre-push hook to catch missing updates
- Keep README.md as the single source of truth

### 2. Structure Documentation

Follow RFC-37 structure for consistency (see directory structure above).

### 3. Link Related Docs

Use relative links between documentation files.

### 4. Keep Docs Fresh

- Run freshness checks periodically
- Update docs when APIs change
- Review docs during code reviews

## References

| Reference | Description |
|-----------|-------------|
| [references/rfc-37.md](references/rfc-37.md) | RFC-37 summary and requirements |
| [references/validation-rules.md](references/validation-rules.md) | All 10 linter rules with examples |
| [references/confluence-metadata.md](references/confluence-metadata.md) | Confluence config (mark.toml, metadata) |
| [references/installation.md](references/installation.md) | Linter installation guide |
| [references/ai-fixes.md](references/ai-fixes.md) | AI-assisted documentation fixes |

## Assets

| Asset | Description |
|-------|-------------|
| [assets/mark.toml.template](assets/mark.toml.template) | Confluence config template |
| [assets/doclinterrc.yml.template](assets/doclinterrc.yml.template) | Linter config template |
| [assets/local-execution.md.template](assets/local-execution.md.template) | Local execution doc template |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [doc-generation-rfc-37](.claude/skills/doc-generation-rfc-37/SKILL.md) | AI-assisted documentation generation |
| [quality-checks](.claude/skills/quality-checks/SKILL.md) | Quality gate orchestration |
| [git-hooks](.claude/skills/git-hooks/SKILL.md) | Pre-commit/pre-push hook setup |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/doc-validation-rfc-37/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

