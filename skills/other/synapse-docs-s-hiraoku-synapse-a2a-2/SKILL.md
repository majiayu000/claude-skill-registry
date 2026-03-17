---
name: synapse-docs
description: This skill manages all documentation for the Synapse A2A project. It should be used when code changes require documentation updates, when checking documentation consistency, or when manually invoked via /synapse-docs. Triggers automatically when modifying files in synapse/, plugins/, or templates/ directories, and when README.md, guides/, or docs/ need updates.
---

# Synapse Docs

This skill ensures Synapse A2A documentation stays synchronized with code changes.

## When This Skill Activates

### Automatic Triggers

1. **Code changes in core modules** - `synapse/*.py`, `synapse/commands/*.py`
2. **Profile changes** - `synapse/profiles/*.yaml`
3. **Template changes** - `synapse/templates/.synapse/*`
4. **Plugin/Skill changes** - `plugins/synapse-a2a/**/*`
5. **Configuration changes** - `pyproject.toml` (version, dependencies, entry points)

### Manual Invocation

- `/synapse-docs` - Run full documentation check and update

## Workflow

### Phase 1: Detect Changes

When code is modified, identify affected documentation by consulting `references/code-doc-mapping.md`.

**Quick Reference - Common Patterns:**

| Change Type | Primary Docs | Secondary Docs |
|-------------|--------------|----------------|
| CLI command | `README.md`, `guides/usage.md` | `guides/references.md`, `CLAUDE.md` |
| API endpoint | `README.md`, `guides/references.md` | `guides/enterprise.md` |
| Environment variable | `README.md`, `guides/settings.md` | `templates/.synapse/settings.json` |
| Profile setting | `guides/profiles.md` | `CLAUDE.md` |
| Skill content | `plugins/*/SKILL.md` | `.claude/skills/`, `.agents/skills/` |

### Phase 2: Propose Updates

For each affected document:

1. Read the current content
2. Identify the specific section to update
3. Propose the minimal necessary change
4. Present changes to user for approval

**Update Principles:**

- Maintain existing document style and tone
- Update only affected sections
- Keep README.md concise; put details in guides/
- Ensure consistency across related documents

### Phase 3: Synchronize Related Files

After updating primary documents, check for required synchronization:

**Skill Synchronization:**
```
plugins/synapse-a2a/skills/ → .claude/skills/
plugins/synapse-a2a/skills/ → .agents/skills/
```

**Template Consistency:**
```
synapse/templates/.synapse/ should match documentation in guides/settings.md
```

### Phase 4: Verify Consistency

Run consistency checks:

1. **CLI commands** - Compare `README.md` ↔ `guides/usage.md` ↔ `guides/references.md`
2. **API endpoints** - Compare `README.md` ↔ `guides/references.md`
3. **Port ranges** - Compare `README.md` ↔ `guides/multi-agent-setup.md` ↔ `CLAUDE.md`
4. **Environment variables** - Compare `README.md` ↔ `guides/settings.md` ↔ `templates/settings.json`

## Document Categories

### User-Facing (High Priority)

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| `README.md` | First impression, quick start | Every feature change |
| `guides/usage.md` | How to use | CLI/API changes |
| `guides/settings.md` | Configuration reference | Setting changes |
| `guides/troubleshooting.md` | Problem solving | New issues discovered |

### Developer-Facing

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| `CLAUDE.md` | Development guide for Claude Code | Architecture/test changes |
| `guides/architecture.md` | Internal design | Component changes |
| `docs/*.md` | Technical specifications | Design changes |

### Plugin/Skill

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| `plugins/synapse-a2a/README.md` | Plugin installation | Plugin changes |
| `plugins/*/skills/*/SKILL.md` | Skill instructions | Feature changes |

## Reference Files

For detailed document inventory and code-to-doc mappings, consult:

- `references/doc-inventory.md` - Complete list of all documents and their roles
- `references/code-doc-mapping.md` - Source file to document relationships

## Special Cases

### Version Updates

When `pyproject.toml` version changes:

1. Update `CHANGELOG.md` with release notes
2. Check if `README.md` test badge needs updating
3. Update `plugins/synapse-a2a/.claude-plugin/plugin.json` version if needed

### New Feature Addition

For major new features:

1. Add to `README.md` feature table
2. Create or update relevant guide in `guides/`
3. Update `CLAUDE.md` if development workflow affected
4. Add to `guides/README.md` navigation if new guide created

### Deprecation

When deprecating features:

1. Mark as deprecated in relevant docs
2. Add migration guide if needed
3. Update `CHANGELOG.md`
4. Remove from quick start examples in `README.md`
