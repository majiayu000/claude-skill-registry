---
name: thor-lens
description: THOR Lens workflows for forensic timeline analysis. A web UI that imports THOR v11 audit trail JSONL logs for interactive exploration. Requires THOR v11 (audit trail not available in v10).
---

# THOR Lens Skill

THOR Lens is a forensic timeline viewer that transforms THOR v11 audit trail files into an interactive exploration interface.

**Critical Boundary**:

- THOR Lens is a **web UI application** - users interact in the browser
- The CLI handles **build**, **import**, and **serve** - not scanning
- THOR Lens **does not scan** - it visualizes data from THOR scans
- Requires **THOR v11** audit trail output (v10 does not produce this format)
- **Not compatible with THOR Lite** - Lite cannot generate audit trail output

## Quickstart

```bash
# 1. Clone and build
git clone https://github.com/NextronSystems/thor-lens.git
cd thor-lens
make build

# 2. Import an audit trail
./thorlens import --log /path/to/audit.jsonl --case mycase

# 3. Serve and open browser
./thorlens serve --case ./cases/mycase --port 8080
# Open http://127.0.0.1:8080
```

## When to Use THOR Lens

- Investigating timelines from THOR v11 scans
- Correlating events across time ranges
- Exploring high-score detections and their context
- Annotating findings with tags, comments, bookmarks
- MCP integration with Claude Code for AI-assisted analysis

## References

- [Quickstart](reference/quickstart.md) - Get running in 5 minutes
- [Build & Prerequisites](reference/build-and-prereqs.md) - Go, Node.js, make requirements
- [Import & Cases](reference/import-and-cases.md) - Importing audit trails, case structure
- [Serve & UI](reference/serve-and-ui.md) - Web server, UI features, keyboard shortcuts
- [MCP Integration](reference/mcp-integration.md) - Claude Code setup, MCP tools
- [Audit Trail Generation](reference/audit-trail-generation.md) - THOR v11 commands for audit trail

## Troubleshooting

- [Common Issues](troubleshooting/common-issues.md) - Build, import, serve problems
- [Empty UI](troubleshooting/empty-ui.md) - Why the timeline shows nothing
- [MCP Issues](troubleshooting/mcp-issues.md) - Connection and configuration problems

## Examples

- [End-to-End Local](examples/end-to-end-local.md) - Full workflow on local machine
- [Case from Mounted Image](examples/case-from-mounted-image.md) - Forensic image workflow
- [Case from SSHFS](examples/case-from-sshfs.md) - Remote system via SSH mount

## Helper Scripts

- [scripts/validate_audit_trail.sh](scripts/validate_audit_trail.sh) - Check audit trail file validity
- [scripts/case_inventory.sh](scripts/case_inventory.sh) - List case contents and stats

## Key Facts

| Item | Value |
|------|-------|
| Upstream repo | https://github.com/NextronSystems/thor-lens |
| Default port | 8080 |
| Case storage | `./cases/<name>/` |
| Input format | JSONL (`.jsonl` or `.jsonl.gz`) |
| MCP stdio | `./thorlens serve --case <path> --mcp-stdio` |
| MCP HTTP | `http://localhost:8080/mcp` (default) |

## Workflow Rules

1. Always verify audit trail was generated with THOR v11 before importing
2. Use `--virtual-map` and `-j` during THOR scans to preserve path/hostname context
3. MCP stdio mode is recommended for Claude Code integration
4. Never expose MCP HTTP endpoint publicly (no authentication)
5. If user has THOR Lite, explain that Lens is not an option - Lite lacks audit trail capability. See [THOR Lite limitations](../thor-lite/reference/limitations.md).
