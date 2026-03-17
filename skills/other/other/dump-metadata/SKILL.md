---
name: dump-metadata
description: Refresh all documentation - builds server, generates grammars, fetches schemas, transforms, and docs
allowed-tools: Bash
---

# Dump Metadata

Refresh all documentation files in `/home/adesola/EpochDev/ClaudeCodeResearch/docs/`.

## What it does

1. Builds `epoch_stratifyx_server` and `generate_grammars`
2. Generates `epochscript.ebnf` grammar
3. Starts server on port 9002
4. Fetches from server endpoints:
   - `schemas.json` - JSON schemas (raw=false)
   - `transform_metadata.json` - All transforms
   - `enums.json` - All enum definitions
   - `assets.json` - Asset metadata
   - `index_constituents.json` - Index membership data
   - `fred_series.json` - FRED economic series
5. Stops server and cleans up

## Run

```bash
/home/adesola/EpochDev/ClaudeCodeResearch/cpp_tools/dump_metadata.sh
```
