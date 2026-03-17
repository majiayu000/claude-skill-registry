---
name: doc-validate-markdown
description: Validate markdown files for formatting, links, and style compliance using markdownlint. Use before committing documentation changes.
mcp_fallback: none
category: doc
user-invocable: false
---

# Validate Markdown Skill

Validate markdown formatting and style compliance.

## When to Use

- Before committing documentation
- Markdown linting errors in CI
- Creating new documentation
- Updating existing docs

## Quick Reference

```bash
# Check all markdown
npx markdownlint-cli2 "**/*.md"

# Check specific file
npx markdownlint-cli2 README.md

# Fix auto-fixable issues
npx markdownlint-cli2 --fix "**/*.md"
```

## Common Issues & Fixes

### MD040: Code blocks need language

**❌ Wrong** - missing language:

```text
code here
```

**✅ Correct** - has language:

```python
code here
```

### MD031: Blank lines around blocks

**❌ Wrong** - no blank lines between text and code block.

**✅ Correct** - add one blank line before the opening fence and one after the closing fence.

### MD013: Line too long

Keep lines under 120 characters. Break long sentences at natural boundaries (clauses, lists).

## Configuration

`.markdownlint.yaml`:

```yaml
line-length:
  line_length: 120
  code_blocks: false
  tables: false
```

## Validation Checklist

- [ ] All code blocks have language specified (` ```python `)
- [ ] All code blocks have blank lines before and after
- [ ] All lists have blank lines before and after
- [ ] All headings have blank lines before and after
- [ ] No lines exceed 120 characters
- [ ] File ends with newline
- [ ] No trailing whitespace

## Error Handling

| Error | Fix |
|-------|-----|
| MD040: Missing language tag | Add language: ` ```mojo ` |
| MD031: Missing blank lines | Add blank line before/after block |
| MD013: Line too long | Break line at 120 characters |
| MD022: Heading spacing | Add blank line before/after heading |

## Workflow

```bash
# 1. Validate your changes
npx markdownlint-cli2 "**/*.md"

# 2. If issues, fix auto-fixable ones
npx markdownlint-cli2 --fix "**/*.md"

# 3. Manually fix remaining issues

# 4. Verify no errors
npx markdownlint-cli2 "**/*.md"

# 5. Commit
git add .
git commit -m "docs: update documentation"
```

## References

- Related skill: `quality-run-linters` for complete linting
- Configuration: `.markdownlint.yaml`
- Markdown standards: CLAUDE.md
