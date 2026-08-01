---
name: format-processor
description: Process and analyze {{FORMAT}} files. Use when {{TRIGGER_CONTEXTS}}.
  Supports {{CAPABILITIES}}.
---

---
name: {{FORMAT}}-processor
description: Process and analyze {{FORMAT}} files. Use when {{TRIGGER_CONTEXTS}}. Supports {{CAPABILITIES}}.
---

# {{FORMAT}} Processor

## Operations

### Read / Extract

Extract content from {{FORMAT}} files:

```bash
bun run scripts/process.ts extract input.{{ext}}
```

**Output formats:**
- `--json` — Structured JSON (default)
- `--text` — Plain text
- `--markdown` — Markdown formatted

### Transform

Transform {{FORMAT}} files:

```bash
bun run scripts/process.ts transform input.{{ext}} --option value
```

### Create

Create new {{FORMAT}} files:

```bash
bun run scripts/process.ts create output.{{ext}} --from data.json
```

## Common Workflows

### Extract and Analyze

1. Extract content: `bun run scripts/process.ts extract file.{{ext}}`
2. Process the JSON output
3. Generate insights or summaries

### Batch Processing

Process multiple files:

```bash
for f in *.{{ext}}; do
  bun run scripts/process.ts extract "$f" > "${f%.{{ext}}}.json"
done
```

## Requirements

- Bun runtime
- {{LIBRARY_NAME}}: `bun add {{library-package}}`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Invalid path | Check file exists and path is correct |
| Parse error | Corrupted file | Verify file is valid {{FORMAT}} |
| Permission denied | Read/write access | Check file permissions |

## Tips

- Use `--verbose` for detailed processing info
- Large files may take longer; use `--progress` to monitor
- Output is JSON by default for easy parsing
