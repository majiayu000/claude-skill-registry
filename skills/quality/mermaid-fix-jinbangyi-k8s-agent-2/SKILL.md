---
name: mermaid-fix
description: Fix and validate Mermaid diagrams using mermaid-cli (mmdc). Use when Claude needs to fix parsing errors in Mermaid diagrams, validate diagrams, or when encountering Mermaid syntax issues. This skill reads rules from .claude/rules/mermaid.md and updates it with newly discovered patterns.
---

# Mermaid Fix

Fixes Mermaid diagram parsing errors using mermaid-cli and discovers new rules.

## Quick Start

1. **Read existing rules**: Load `.claude/rules/mermaid.md` for known patterns
2. **Extract diagrams**: Find all Mermaid code blocks in the target file(s)
3. **Validate with mmdc**: Run `mmdc -i <temp_file> -o /dev/null` to check syntax
4. **Fix errors**: Apply fixes based on mmdc error output
5. **Update rules**: Add newly discovered error patterns to mermaid.md

## Validation Command

```bash
# Create temp file, validate, check exit code
mmdc -t neutral -i diagram.mmd -o /dev/null
# Exit code 0 = valid, non-zero = error
```

## Common Fixes

Based on existing rules in `mermaid.md`:

| Error Pattern | Fix |
|--------------|-----|
| `Graph TD` | Change to lowercase: `graph TD` |
| `<br/>`, `<b>`, `<i>` in labels | Remove HTML tags, use plain text |
| `dmzSubnet` style naming | Use hyphens: `dmz-subnet` |
| Missing `graph` direction | Add `LR`, `TD`, `RL`, or `BT` |

## Discovering New Rules

When you encounter a new error pattern:

1. **Document the error**: Capture the error message from mmdc
2. **Identify the fix**: What change resolved the error?
3. **Update mermaid.md**: Add a new rule entry with:
   - Rule number (next sequential)
   - Category name
   - Pattern description
   - Fix/avoidance guidance

Example new rule format:

```markdown
**N. Category Name**
- Error pattern: `<what causes the error>`
- Fix: `<how to resolve>`
- Example: `<before -> after>`
```

## Workflow Steps

### Quick Mode (Markdown Files with Multiple Diagrams)

For markdown files containing multiple Mermaid diagrams, use concurrent validation:

```bash
# Validate all diagrams in a markdown file concurrently (4 workers by default)
python3 .claude/skills/mermaid-fix/scripts/validate_markdown_mermaid.py <path/to/file.md>

# Specify number of parallel workers
python3 .claude/skills/mermaid-fix/scripts/validate_markdown_mermaid.py <path/to/file.md> --workers 8
```

### Step-by-Step Mode

1. Read the target file(s) containing Mermaid diagrams
2. For each diagram:
   - Extract the Mermaid code block
   - Write to a temporary `.mmd` file
   - Run `mmdc` to validate
   - If error: fix based on error message and known rules
   - If new pattern: document for mermaid.md update
3. Replace fixed diagrams in source file(s)
4. If new patterns were discovered, update `.claude/rules/mermaid.md`

## Constraints

- Preserve the diagram's semantic meaning
- Only fix syntax/structure issues
- Do not "optimize" or "improve" the visual design (use `/optimize-mermaid` for that)
- Test each fix with mmdc before applying
