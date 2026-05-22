---
name: robotframework-libdoc-search
description: Search Robot Framework library/resource/suite documentation to find matching keywords for a use case. Use when asked to find keywords, search libdoc, match a use case to keywords, or scan multiple libraries/resources for relevant keywords.
---

# Robot Framework Libdoc Search

Use this skill to search Robot Framework libraries/resources/suites for keywords that match a use case. Output JSON only.

## Command

Search in standard libraries:

```bash
python scripts/rf_libdoc.py --library BuiltIn --library OperatingSystem --search "create temp file" --pretty
```

Search multiple sources with custom weights:

```bash
python scripts/rf_libdoc.py --library SeleniumLibrary --resource resources/common.resource --search "upload file" --weights name=0.5,short_doc=0.3,doc=0.2 --limit 10 --pretty
```

## Notes
- Use `--library`, `--resource`, `--suite`, or `--spec` (repeatable). Inputs are aggregated.
- Search considers keyword name, `short_doc`, and full `doc`.
- Use `--tag` to filter keywords by tag.
- Use `--include-private` to include private keywords.
- Use `--exclude-deprecated` to drop deprecated keywords.
