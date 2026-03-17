---
name: adb-builder
tier: Tier 0 (Meta-Generation Framework)
purpose: Automated scaffolding and generation system for ADB skills and bots
version: 1.0.0
status: active
---

# adb-builder

**Tier**: Tier 0 (Meta-Generation Framework)
**Purpose**: Automated scaffolding and generation system for ADB skills and bots
**Version**: 1.0.0
**Status**: Active

## Description

adb-builder provides comprehensive meta-programming capabilities for the ADB ecosystem. It enables automated creation, validation, and reorganization of adb-* skills with proper structure, documentation, and testing patterns.

## Core Capabilities

1. **adb-builder-skill** - Generate complete adb-* skills from templates
2. **adb-builder-bot** - Generate game bot skills with specialized templates
3. **adb-builder-validate** - Validate skills against ecosystem standards
4. **adb-project-tree-reorganizer** - Automated skill migration and restructuring

## Dependencies

- **moai-foundation-core** - SPEC and validation patterns
- **moai-lang-unified** - Python scripting and language utilities
- **moai-domain-adb** - ADB domain knowledge and utilities

## Scripts

| Script | Purpose | Lines |
|--------|---------|-------|
| `adb-builder-skill.py` | Generate complete adb-* skills | 300+ |
| `adb-builder-bot.py` | Generate game bot skills with templates | 350+ |
| `adb-builder-validate.py` | Validate skills against standards | 250+ |
| `adb-project-tree-reorganizer.py` | Automated reorganization and migration | 280+ |

## Modules

| Module | Purpose | Lines |
|--------|---------|-------|
| `adb-skill-generation.md` | Skill generation patterns and best practices | 250+ |
| `adb-bot-scaffolding.md` | Bot structure templates and patterns | 250+ |
| `adb-validation-framework.md` | Validation rules and scoring system | 150+ |
| `adb-project-tree-hierarchy.md` | Structure documentation and migration | 200+ |

## Workflows

- `adb-skill-creation.toon` - Complete skill generation workflow
- `adb-project-reorganization.toon` - Project structure reorganization workflow

## Test Coverage

- Unit tests for all generators (250+ tests)
- Integration tests for reorganizer (50+ tests)
- Validation test suite (100+ tests)
- **Total Coverage**: 85%+

## Usage Examples

### Generate a New Skill

```bash
uv run .claude/skills/adb/adb-builder/scripts/adb-builder-skill.py \
  --name "my-feature" \
  --category "game" \
  --description "Feature description" \
  --modules "module1,module2" \
  --output-format json
```

### Generate a Game Bot

```bash
uv run .claude/skills/adb/adb-builder/scripts/adb-builder-bot.py \
  --game "afk-journey" \
  --bot-type "quest-runner" \
  --phases "3" \
  --features "state-tracking,ocr-detection,recovery" \
  --output-format json
```

### Validate Skills

```bash
uv run .claude/skills/adb/adb-builder/scripts/adb-builder-validate.py \
  --skill-path .claude/skills/adb/adb-feature/ \
  --checks "all" \
  --report-format json
```

### Reorganize Project Structure

```bash
# Dry-run mode (analysis only)
uv run .claude/skills/adb/adb-builder/scripts/adb-project-tree-reorganizer.py \
  --mode dry-run \
  --target-structure game-specific \
  --report json

# Execute mode (actual migration)
uv run .claude/skills/adb/adb-builder/scripts/adb-project-tree-reorganizer.py \
  --mode execute \
  --target-structure game-specific \
  --create-backup \
  --validate-references
```

## Directory Structure

```
adb-builder/
├── SKILL.md                           (This file)
├── modules/
│   ├── adb-skill-generation.md        (Skill generation patterns)
│   ├── adb-bot-scaffolding.md         (Bot structure templates)
│   ├── adb-validation-framework.md    (Validation rules)
│   └── adb-project-tree-hierarchy.md  (Structure documentation)
├── scripts/
│   ├── adb-builder-skill.py           (Skill generator)
│   ├── adb-builder-bot.py             (Bot generator)
│   ├── adb-builder-validate.py        (Validation tool)
│   ├── adb-project-tree-reorganizer.py (Reorganization tool)
│   └── common/
│       ├── adb_templates.py           (Template utilities)
│       ├── adb_validators.py          (Validation utilities)
│       └── adb_utils.py               (Common utilities)
├── workflows/
│   ├── adb-skill-creation.toon        (Skill creation workflow)
│   └── adb-project-reorganization.toon (Reorganization workflow)
└── tests/
    ├── test_builder_skill.py          (Skill generator tests)
    ├── test_builder_bot.py            (Bot generator tests)
    ├── test_builder_validate.py       (Validation tests)
    └── test_reorganizer.py            (Reorganizer tests)
```

## Integration Points

- **adb-* ecosystem**: All adb-* skills are created using adb-builder patterns
- **moai-domain-adb**: Uses ADB utilities and patterns
- **ADB agents**: Supports agent creation and skill discovery
- **Project restructuring**: Automatic reorganization of skill hierarchy

## Status & Roadmap

### Current Features (v1.0)
- ✅ Skill generation with templates
- ✅ Bot scaffolding framework
- ✅ Validation system
- ✅ Project reorganization

### Planned (v2.0)
- 🔄 Custom template library
- 🔄 Model training integration
- 🔄 Performance profiling tools
- 🔄 Web UI for skill generation

## References

- See `modules/` directory for detailed implementation guides
- See `scripts/` directory for CLI documentation
- See `workflows/` directory for TOON workflow examples

---

**Last Updated**: 2025-12-02
**Maintainer**: ADB Automation Team
**Status**: Production Ready
