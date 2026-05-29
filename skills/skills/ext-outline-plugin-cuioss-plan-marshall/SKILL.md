---
name: ext-outline-plugin
description: Outline extension for plugin development domain
allowed-tools: Read
---

# Plugin Development Outline Extension

> Extension for phase-2-outline in plugin development domain.

Provides domain-specific knowledge for deliverable creation in marketplace plugin development tasks. This is a knowledge document loaded as context - it does not replace the workflow.

## Domain Detection

This domain is relevant when:
1. `marketplace/bundles` directory exists
2. Request mentions "skill", "command", "agent", "bundle"
3. Files being modified are in `marketplace/bundles/*/` paths

## Domain Constraints

### Component Rules
- Skills MUST have `SKILL.md` in `skills/{skill-name}/` directory
- Commands MUST be single `.md` files in `commands/`
- Agents MUST be single `.md` files in `agents/`
- All components require YAML frontmatter with name and description
- Scripts MUST be in `skills/{skill-name}/scripts/` directory
- Scripts MUST have corresponding tests in `test/` at project root

### Dependency Rules
- Agents delegate to skills (skill loading via `Skill:` directive)
- Commands orchestrate agents or execute skills directly
- Skills should be self-contained units of knowledge
- Agents should not depend on other agents

### Verification Rules
- Standard verification: `/pm-plugin-development:plugin-doctor --component {path}`
- Scripts require: `python3 test/run-tests.py test/{bundle}/`
- Component paths:
  - Skills: `marketplace/bundles/{bundle}/skills/{skill-name}/SKILL.md`
  - Commands: `marketplace/bundles/{bundle}/commands/{command-name}.md`
  - Agents: `marketplace/bundles/{bundle}/agents/{agent-name}.md`

## Deliverable Patterns

### Grouping Strategy
| Scenario | Grouping |
|----------|----------|
| Creating 1-3 components in single bundle | One deliverable per component |
| Cross-bundle pattern change | One deliverable per bundle affected |
| Script changes | Include script + tests in same deliverable |
| Rename/migration | Group by logical unit being renamed |

### Change Type Mappings
| Request Pattern | change_type | execution_mode |
|-----------------|-------------|----------------|
| "add", "create", "new" | create | automated |
| "fix", "update" (localized) | modify | automated |
| "rename", "migrate", "refactor" | refactor | automated |
| "change format", "update pattern" | migrate | automated |

### Standard File Structures
- Skills: `marketplace/bundles/{bundle}/skills/{skill-name}/SKILL.md`
- Commands: `marketplace/bundles/{bundle}/commands/{command-name}.md`
- Agents: `marketplace/bundles/{bundle}/agents/{agent-name}.md`
- Scripts: `marketplace/bundles/{bundle}/skills/{skill-name}/scripts/{script}.py`
- Tests: `test/{bundle}/{skill-name}/test_{script}.py`

## Impact Analysis Patterns

### Detection Commands
| Change Type | Discovery Command |
|-------------|-------------------|
| Script notation rename | `grep -r "old:notation" marketplace/bundles/` |
| Output format change | `grep -r '```json' marketplace/bundles/*/agents/` |
| Skill reference update | `grep -r "Skill: {skill}" marketplace/bundles/` |
| Command usage | `grep -r "/{command}" marketplace/bundles/` |

### Discovery Script
For cross-cutting changes, use the marketplace inventory:
```bash
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory \
  --trace-plan-id {plan_id} --include-descriptions
```

### Batch Analysis Guidelines
- Process components in batches of 10-15 files
- Build explicit file enumeration for each deliverable
- NEVER use wildcards in affected files list

## Related Skills

| Skill | Purpose |
|-------|---------|
| `pm-plugin-development:plugin-architecture` | Architecture principles |
| `pm-plugin-development:plugin-script-architecture` | Script patterns and testing |
| `pm-plugin-development:plugin-create` | Component creation patterns |
| `pm-plugin-development:plugin-doctor` | Quality validation |
