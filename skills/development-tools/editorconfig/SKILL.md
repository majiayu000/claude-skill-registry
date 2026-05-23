---
name: editorconfig
description: Generate a .editorconfig file for a repository
---

# Generate .editorconfig

## When to use this skill

When starting work on a new repository or adding an `.editorconfig` to an
existing project that lacks one.

## How it works

Creates a minimal `.editorconfig` file with sensible defaults. The generated
config follows the repository's existing style when possible.

## Process

1. Check if `.editorconfig` already exists - if so, update it
2. Examine existing files in the repo to detect coding style:
   - Look at indentation (spaces vs tabs), indent size
   - Check line ending conventions
   - Identify file types that may need special handling
3. Generate appropriate, minimal `.editorconfig` content
   with **no unnecessary duplication**.
4. Write the file to the repository root

## Generated Config Structure

```ini
root = true

[*]
indent_style = space
indent_size = <detected or 4>
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
max_line_length = 78

[*.json]
indent_size = 2
```

## Best Practices

- Always set `root = true` at the top
- Use `[*]` for universal settings
- Add specific file type overrides after universal settings
- Keep it minimal - only specify what differs from editor defaults
