---
name: read-repo-references
description: Learn from reference materials and prior art in the .references/ directory
---

# Read Repo References

Use this skill when you need inspiration or guidance from prior art and reference implementations.

## When to Use

- Designing new features that have established patterns elsewhere
- Stuck on architecture decisions
- Need to understand how similar tools solve a problem

## Reference Structure

References live in `.references/<name>/` with this format:

```
.references/
└── <reference-name>/
    ├── REF.md              # Required: metadata and description
    └── [local files]       # Optional: PDFs, markdown, code samples
```

## REF.md Format

```yaml
---
name: reference-name
type: link | local | hybrid
url: https://...               # Required if type includes link
description: Brief description
---

# Reference Name

Notes on key patterns, architecture, and relevance...
```

## Reference Types

- **link**: Points to external resource (GitHub repo, docs). Use WebFetch or browse the URL.
- **local**: Contains files directly. Read the files in the reference directory.
- **hybrid**: Both a link and local supplementary materials.

## How to Use References

1. **List available references**:
   ```bash
   ls .references/
   ```

2. **Read a reference**:
   ```bash
   cat .references/<name>/REF.md
   ```

3. **For link-type references**: The REF.md contains the URL and notes about what to look for. Fetch specific files from the URL as needed.

4. **For local-type references**: Read the files directly from the reference directory.

5. **Apply learnings**: Extract relevant patterns and adapt them to the current project's conventions.

## Best Practices

- Read REF.md first to understand what the reference offers
- Focus on patterns relevant to your current task
- Adapt patterns to fit the project, don't copy blindly
- Note any new insights in `.agents/notes/` for future reference
