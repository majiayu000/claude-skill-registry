---
name: scan
description: 'Control scanners via scan-mcp MCP server to capture documents, photos,
  receipts, and pages. Use when user mentions scanning, scanners, or document types.
  CRITICAL: call start_scan_job with {} (no para'
---

---
name: scan
description: Control scanners via scan-mcp MCP server to capture documents, photos, receipts, and pages. Use when user mentions scanning, scanners, or document types. CRITICAL: call start_scan_job with {} (no params) unless user specifies requirements—server handles intelligent device selection and defaults. Override only for explicit needs like photos (Flatbed+Color+high-res) or duplex stacks (ADF Duplex).
---

# Scanner Control via scan-mcp

## THE GOLDEN RULE

**Trust the server defaults.** When the user requests a scan without specific requirements:
- Call `start_scan_job({})` with NO parameters
- Do NOT call `list_devices` unless the user explicitly asks for a specific scanner
- Do NOT gather device capabilities "just in case"
- Server auto-selects device, resolution (300dpi), color mode (Lineart), source (ADF Duplex → ADF → Flatbed)

**Only override parameters when the user's intent clearly requires it.**

## Decision Tree

```
User request → Analyze intent:

1. Generic scan ("scan this", "scan document")
   → start_scan_job({}) immediately

2. User asks for specific scanner ("use the Epson")
   → list_devices, then start_scan_job({ device_id })

3. Document type needs special handling ("photo", "duplex")
   → Override only specific params needed
```

## Common Overrides

| User Intent | Parameters |
|------------|------------|
| Generic scan | `{}` |
| Photo scan | `{ source: "Flatbed", color_mode: "Color", resolution_dpi: 600 }` |
| Duplex stack | `{ duplex: true }` |
| OCR-optimized | `{ color_mode: "Gray", resolution_dpi: 300 }` |

**For more mappings**, see [EXAMPLES.md](EXAMPLES.md).

## Standard Workflow

1. Call `start_scan_job(params)` → receive `{ job_id, run_dir, state }`
2. Poll `get_job_status({ job_id })` until `state: "completed"`
3. Results in `run_dir`:
   - `page_*.tiff` (captured pages)
   - `doc_*.tiff` (assembled document)
   - `manifest.json` (metadata)
   - `events.jsonl` (event log)

## Quick Troubleshooting

**If scan fails:**
1. `get_manifest({ job_id })` — check state and parameters
2. `get_events({ job_id })` — find error details in `scanner_failed` events
3. Common fixes:
   - "No devices" → Ask user to check scanner power/connection
   - "Feeder jam" → Try `{ source: "Flatbed" }`

**For detailed troubleshooting**, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Reference Materials

- **[TOOLS.md](TOOLS.md)** — Complete tool reference with all parameters
- **[EXAMPLES.md](EXAMPLES.md)** — User intent → parameter mappings with reasoning
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Detailed troubleshooting flows
- **[CONFIG.md](CONFIG.md)** — Environment variables and configuration
