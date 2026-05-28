---
name: rfc-37-documentation
description: >
  Bitso's service documentation standardization based on RFC-37. Validates
  directory structure, Confluence metadata, and content with bitso-documentation-linter.
  Use when creating, validating, or fixing markdown documentation for Confluence mirroring.
compatibility: All repositories with docs/ folder; requires bitso-documentation-linter
metadata:
  version: "3.0"
  rfc: "RFC-37"
  linter: "bitso-documentation-linter"
  # Note: linter_repo removed - repository is internal/private
---

# RFC-37 Documentation Standardization

Implements [RFC-37](https://bitsomx.atlassian.net/wiki/spaces/BAB/pages/4485840987/RFC-37+Service+documentation+standardization) for standardized markdown documentation that mirrors to Confluence.

## When to use this skill

- Creating documentation for a new service
- Validating existing documentation structure
- Fixing documentation linting violations
- Setting up Confluence mirroring configuration
- Understanding documentation requirements

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L19-L26)
- [Quick Start](#quick-start) (L58-L87)
- [Standard Directory Structure](#standard-directory-structure) (L88-L104)
- [Required Documentation](#required-documentation) (L105-L115)
- [Validation](#validation) (L116-L135)
- [Available Scripts](#available-scripts) (L136-L152)
- [References](#references) (L153-L162)
- [Assets](#assets) (L163-L170)
- [External Documentation](#external-documentation) (L171-L179)
- [Related Skills](#related-skills) (L180-L184)

### Available Resources

**📚 references/** - Detailed documentation
- [ai fixes](references/ai-fixes.md)
- [confluence metadata](references/confluence-metadata.md)
- [installation](references/installation.md)
- [rfc 37](references/rfc-37.md)
- [validation rules](references/validation-rules.md)

**📦 assets/** - Templates and resources
- [doclinterrc.yml](assets/doclinterrc.yml.template)
- [local execution.md](assets/local-execution.md.template)
- [mark.toml](assets/mark.toml.template)

---

## Quick Start

1. **Install the linter** (see [references/installation.md](references/installation.md)):

   ```bash
   brew tap bitsoex/homebrew-bitso
   brew install bitso-documentation-linter
   ```

2. **Create directory structure**:

   ```bash
   mkdir -p docs/{decisions,how-tos,runbooks}
   mkdir -p docs/my-service/{concepts,getting-started}
   ```

3. **Create Confluence config** (see [references/confluence-metadata.md](references/confluence-metadata.md)):

   ```bash
   # Copy and edit the template
   cp assets/mark.toml.template docs/mark.toml
   ```

4. **Validate**:

   ```bash
   doclinter --repo-path . --verbose
   doclinter tree --repo-path .  # Preview Confluence hierarchy
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

## Required Documentation

Every service MUST have:

1. **Local Execution** (`docs/how-tos/local-execution.md`)
   - Use template: [assets/local-execution.md.template](assets/local-execution.md.template)

2. **Service Concepts** (`docs/<service>/concepts/`)
   - Architecture diagrams (C4 recommended)
   - Key components and dependencies

## Validation

Run the linter to check compliance:

```bash
# Basic validation
doclinter --repo-path .

# Verbose with metrics
doclinter --repo-path . --verbose

# Preview Confluence tree
doclinter tree --repo-path .

# With Confluence API validation
CONFLUENCE_ENABLED=true doclinter --repo-path .
```

For full validation rules, see [references/validation-rules.md](references/validation-rules.md).

## Available Scripts

Scripts are implemented in `.scripts/lib/skills/rfc-37.ts`:

```bash
# Via skills CLI
node .scripts/skills-cli.ts rfc-37 validate
node .scripts/skills-cli.ts rfc-37 lint
```

| Function | Description |
|----------|-------------|
| `validate(dir)` | Validate RFC-37 directory structure |
| `lint(dir)` | Run full documentation linting |
| `checkLinterInstalled()` | Check if doclinter is available |
| `generateTree(dir)` | Generate Confluence tree preview |

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

## External Documentation

The linter has extensive documentation at [github.com/bitsoex/bitso-documentation-linter](https://github.com/bitsoex/bitso-documentation-linter):

- [Local Execution Guide](https://github.com/bitsoex/bitso-documentation-linter/blob/main/docs/how-tos/local-execution.md)
- [Configuration Reference](https://github.com/bitsoex/bitso-documentation-linter/blob/main/docs/bitso-documentation-linter/concepts/configuration.md)
- [CLI Options](https://github.com/bitsoex/bitso-documentation-linter/blob/main/docs/bitso-documentation-linter/concepts/cli-options.md)
- [AI Fixes Guide](https://github.com/bitsoex/bitso-documentation-linter/blob/main/docs/how-tos/how-to-fix-documentation-using-ai.md)

## Related Skills

- `agent-hooks` - For integrating linting into IDE hooks
- `quality-gateway` - For comprehensive quality checks
- `doc-sync` - For keeping docs in sync with code
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/rfc-37-documentation/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

