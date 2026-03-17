---
name: crowdin-context-cli
description: Documents Crowdin CLI context download and upload for AI enrichment. Use when downloading or uploading strings context for Crowdin, managing context files, or running crowdin context commands.
---

# Crowdin Context CLI

Use the Crowdin CLI for context download and upload. Config is read from `crowdin.yml` by default; override with `-c, --config=<path>` if needed.

```
crowdin context <command> [options]
```

## context download

Download strings context to a separate file for enrichment by AI Agent.

```
crowdin context download [CONFIG OPTIONS] [OPTIONS]
```

- `--to=<path>` — File path to download the context to. Default: `crowdin-context.jsonl`
- `-f, --file=<glob>` — Filter strings by Crowdin file paths (glob). Multiple paths can be specified
- `--label=<label>` — Filter strings by labels. Multiple labels can be specified
- `-b, --branch=<name>` — Filter by branch name
- `--croql=<expr>` — CroQL expression
- `--since=<YYYY-MM-DD>` — Only strings created after this date
- `--format=<value>` — Output format. Supported values: `jsonl`
- `--status=<value>` — Filter by context status. Supported values: `empty`, `ai`, `manual`

Config options (if not using a config file): `-T, --token`, `-i, --project-id`, `--base-url`, `--base-path`. Use `-c, --config=<path>` to override config file (default: `crowdin.yml` or `crowdin.yaml`).

## context upload

Upload strings context. Only files previously downloaded by `context download` are supported.

```
crowdin context upload [CONFIG OPTIONS] [OPTIONS]
```

- `--from=<path>` — File path to upload the context from. Default: `crowdin-context.jsonl`
- `--overwrite` — Also update strings where `ai_context` is empty (removes their AI section). Default: false
- `--dryrun` — Print command output without execution

## JSONL format

One JSON object per line. Fields:

- `id` — String ID in Crowdin
- `key` — String key
- `text` — Source text
- `file` — Crowdin file path
- `context` — Existing source context
- `ai_context` — AI context to set (**edit this field before uploading**)

Example line:

```json
{"file":"/src/locales/en.po","ai_context":"","context":"#: src/App.tsx:54","id":3125833,"text":"Click on the Vite and React logos to learn more","key":"Click on the Vite and React logos to learn more"}
```

## Typical Workflow

1. Download: `crowdin context download` (writes to `crowdin-context.jsonl` by default) or `crowdin context download --to=path/to/file.jsonl`
2. Edit the file - fill in `ai_context` for each string (use [context-extraction](../context-extraction/SKILL.md) to help).
3. Upload: `crowdin context upload` (reads from `crowdin-context.jsonl` by default) or `crowdin context upload --from=path/to/file.jsonl`
