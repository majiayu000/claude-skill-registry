---
name: data-pipeline-patterns
version: "1.0"
description: Team conventions for Python data pipelines — stage structure, JSON output format, debugging workflow, and anti-patterns. Supplements standard patterns with team-specific rules.
---

# Data Pipeline Patterns — Team Conventions

Claude already knows validation, error handling, and retry patterns. This covers our team's specific stage structure and conventions.

## When to Activate

- Building or modifying data pipeline stages
- Debugging pipeline failures (empty data, schema mismatches)
- Reviewing pipeline code

## Standard Stage Structure

Every pipeline stage follows this pattern:

```python
def main(argv=None):
    args = parse_args(argv)

    # 1. Load input
    input_data = load_json_file(Path(args.file))
    if input_data is None:
        sys.exit(1)

    # 2. Validate input
    if not validate_json_structure(input_data, ["required_key"], "Input file"):
        sys.exit(1)

    # 3. Process
    result = process(input_data)

    # 4. Save output with metadata
    output = {
        "metadata": {
            "source_file": str(args.file),
            "generated_at": datetime.now().isoformat(),
            "items_processed": len(result),
        },
        "data": result
    }
    save_json_file(output, output_path)
```

**Key rules:** Each stage is independently runnable (CLI + importable). Validate input before processing. Include metadata in every output. Fail fast on invalid input. Checkpoint every N items on long operations.

## JSON Data File Conventions

- All output files: `metadata` dict + `data` (list or dict)
- Metadata always has: `source_file`, `generated_at`, count fields
- Use `_` prefix for derived/computed fields
- Dates as ISO 8601 strings (`2026-03-15T10:00:00`)
- Save with `indent=2` and `ensure_ascii=False`

## Debugging Pipeline Failures

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Empty output file | Input had no matching items | Check filters, validate input data |
| Missing keys in output | Schema changed upstream | Update validation, check input stage |
| API timeout | Service overloaded or VPN down | Add retry logic, check connectivity |
| Rate limit errors (429) | Too many API calls | Add backoff, reduce batch size |
| Partial output | Stage crashed mid-processing | Add checkpointing |
| Wrong data types | API returned unexpected format | Add type validation at boundaries |
| Duplicate items | Pagination overlap | Deduplicate by key field |

## Anti-Patterns

- **Processing without validation** — always check input before transforming
- **Swallowing errors** — never `except: pass` in pipeline stages
- **Hardcoded file paths** — use arguments or config, never absolute paths
- **No logging** — every stage should log what it's doing and how many items
- **Monolithic stages** — if a stage does 3 things, split it into 3 stages
- **Missing metadata** — every output file should be self-describing
