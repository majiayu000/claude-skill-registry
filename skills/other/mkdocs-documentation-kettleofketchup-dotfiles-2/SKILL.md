---
name: mkdocs-documentation
description: MkDocs Material documentation management. This skill should be used when writing, formatting, or validating documentation in docs/. Covers admonitions, Mermaid diagrams, code blocks with annotations, content tabs, navigation setup, and mkdocs testing. Always check project-specific docs at docs/dev/ai/skills/ and docs/dev/ai/agents/ for project-specific Claude skill and Claude agent documentation when available.
---

# MkDocs Material Documentation

Write and maintain documentation using MkDocs Material in the `docs/` directory.

## Project-Specific Claude Documentation

**Always check first for project-specific Claude configurations:**
- `docs/dev/ai/skills/SKILL-NAME.md` - Project-specific Claude skill docs
- `docs/dev/ai/agents/AGENT-NAME.md` - Project-specific Claude agent docs

These take precedence over general patterns.

## Quick Reference

| Task | Reference |
|------|-----------|
| Callout boxes | [admonitions.md](references/admonitions.md) |
| Flowcharts, diagrams | [diagrams.md](references/diagrams.md) |
| Syntax highlighting | [code-blocks.md](references/code-blocks.md) |
| Multi-option examples | [content-tabs.md](references/content-tabs.md) |
| Links, nav structure | [navigation.md](references/navigation.md) |
| Build, validate | [testing.md](references/testing.md) |

## Common Patterns

### Admonition with Code

```markdown
!!! example "Usage"

    ```python
    from module import func
    func()
    ```
```

### Tabbed Installation

````markdown
=== "pip"

    ```bash
    pip install package
    ```

=== "poetry"

    ```bash
    poetry add package
    ```
````

### Feature Documentation

```markdown
## Feature Name

!!! info "Requirements"
    List prerequisites here.

### Configuration

```yaml
setting: value
```

### Usage

Description with examples.

!!! warning
    Important caveats.
```

## Workflow

1. **Write content** - Use references for formatting syntax
2. **Preview** - `mkdocs serve` for live reload
3. **Validate** - `mkdocs build --strict` catches issues
4. **Document Claude features** - Update `docs/dev/ai/skills/` or `docs/dev/ai/agents/` if adding project-specific Claude skills or agents

## Validation Commands

```bash
# Dev server with live reload
mkdocs serve

# Strict build (CI validation)
mkdocs build --strict

# Quick dirty reload during editing
mkdocs serve --dirty
```
