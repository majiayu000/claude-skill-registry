---
name: robotframework-libdoc-explain
description: Explain Robot Framework keywords and their arguments from library/resource/suite documentation. Use when asked how to use a keyword, what arguments it takes, or to retrieve detailed keyword docs from libdoc across one or more libraries/resources.
---

# Robot Framework Libdoc Explain

Use this skill to retrieve detailed keyword docs and argument usage from Robot Framework libraries/resources/suites. Output JSON only.

## Command

Explain a keyword in standard libraries:

```bash
python scripts/rf_libdoc.py --library BuiltIn --keyword "Log" --pretty
```

Explain across multiple sources:

```bash
python scripts/rf_libdoc.py --library SeleniumLibrary --resource resources/common.resource --keyword "Open Browser" --pretty
```

Fallback to search if exact keyword not found:

```bash
python scripts/rf_libdoc.py --library SeleniumLibrary --keyword "Open Brows" --search "open browser" --pretty
```

## Notes
- Use `--library`, `--resource`, `--suite`, or `--spec` (repeatable). Inputs are aggregated.
- Exact keyword matches return `keyword_matches` with argument breakdown.
- If no exact match, the script returns `matches` using name + `short_doc` + `doc` search.
- Use `--tag`, `--include-private`, `--exclude-deprecated` as filters.
