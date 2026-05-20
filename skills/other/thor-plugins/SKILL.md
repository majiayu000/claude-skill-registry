---
name: thor-plugins
description: Write, package, and use THOR plugins to extend scanner functionality. THOR v11+ only.
---

# THOR Plugins Skill

Goal: Help users write custom THOR plugins and integrate them into scans.

## Overview

THOR Plugins (v11+) allow extending THOR with custom functionality written in Go:

- Parse file formats THOR doesn't natively support
- Implement complex detection logic beyond YARA/Sigma
- Post-process findings (upload samples, enrich data, trigger alerts)

Plugins are ZIP archives containing Go code, executed by THOR via the yaegi interpreter.

## Requirements

- THOR v11 or later (plugins not available in v10 or THOR Lite)
- Go installed for development (go 1.21+)
- Basic Go programming knowledge

## Key Concepts

1. **Plugin Structure**: ZIP containing `plugin.go`, `metadata.yml`, optional `vendor/` directory
2. **Init Function**: Entry point `func Init(config, logger, actions)` called at scan start
3. **Hooks**: Register callbacks for YARA/Sigma matches or post-processing
4. **Scanner Interface**: Within hooks, scan extracted data, log messages, add findings

## Plugin Types by Use Case

| Use Case | Hook Type | Example |
|----------|-----------|---------|
| Parse custom file format | `AddRuleHook` with YARA trigger | ZIP parser, Defender quarantine extractor |
| Log/alert on matches | `AddRuleHook` | Registry autorun logger |
| Upload/collect samples | `AddPostProcessingHook` | HTTP sample collector |
| Enrich findings | `AddPostProcessingHook` | VirusTotal lookup, MITRE tagging |

## Workflow

1. Start from template or existing example
2. Define YARA rule to trigger on target files (if needed)
3. Implement hook callback with custom logic
4. Create `metadata.yml` with plugin info
5. Package as ZIP: `zip -r plugin.zip *.go metadata.yml vendor/`
6. Place in THOR's `plugins/` directory
7. Run THOR - plugin loads automatically

## Reference Documentation

- [Getting Started](reference/getting-started.md) - Create your first plugin
- [Plugin API](reference/plugin-api.md) - Full API reference
- [Packaging](reference/packaging.md) - How to package and deploy plugins

## Examples

- [examples/zipparser.md](examples/zipparser.md) - Parse and scan ZIP contents
- [examples/defender-quarantine.md](examples/defender-quarantine.md) - Decrypt Defender quarantine files
- [examples/httpcollector.md](examples/httpcollector.md) - Upload samples via HTTP
- [examples/registry-autoruns.md](examples/registry-autoruns.md) - Log registry autorun entries

## Common Pitfalls

- Plugins use yaegi interpreter - no `unsafe` or `syscall` packages
- External dependencies must be vendored (`go mod vendor`)
- Plugin ZIP must have `package main` in root .go file
- YARA rules in plugins need unique tags for hooks
- Post-processing hooks only fire on findings, not all scanned files

## Debugging

```bash
# Run THOR with debug to see plugin loading
./thor-macosx --debug | grep -i plugin

# Check plugin initialization messages
./thor-macosx 2>&1 | grep "plugin"
```
