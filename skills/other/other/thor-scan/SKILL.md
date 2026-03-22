---
name: thor-scan
description: Run THOR scans and propose the exact command line for Windows, Linux, or macOS. Use when the user wants to scan a host, a directory, a mounted image, or a memory dump with THOR v10/v11.
---
# THOR Scan Skill

Goal: produce a safe, reproducible THOR command line and minimal preflight checks.

Rules

- Prefer THOR v10 stable unless the user explicitly wants v11 TechPreview features.
- Always start with environment detection: OS, THOR path, license presence, and whether thor-util exists.
- Identify if user has full THOR or THOR Lite (different binaries, different capabilities).
- Avoid "magic flags". Explain why each non-trivial flag is used.
- Default to focusing on forensic / lab workflows; if it's live endpoint scanning, keep it conservative.

Preflight checklist

1. List the THOR install directory first (`ls` or `dir`). This immediately tells you:
   - Which THOR version you have (binary names contain "lite" for THOR Lite)
   - What binaries and tools are available
   - What license files exist
2. Verify the correct binary exists:
   - Full THOR: `thor64.exe` (Windows), `thor-linux-64` (Linux), `thor-macosx` (macOS)
   - THOR Lite: `thor64-lite.exe` (Windows), `thor-lite-linux-64` (Linux), `thor-lite-macos` (macOS)
3. If recommending `--lab` mode, check license type first:
   - `grep -i forensiclab *.lic` - if found, `--lab` is available
   - If not found (or THOR Lite), use alternative: `-a Filescan --intense --norescontrol --cross-platform`
4. Check thor-util presence for update/diagnostics/report tasks.
5. Identify scan target type:
   - live path, mounted image, memory dump, extracted dumps, SSHFS-mounted remote
6. Choose scan mode and output location; keep outputs deterministic.
7. If THOR Lite: note that lab mode and Sigma are unavailable. See [THOR Lite limitations](../thor-lite/SKILL.md).

Important flag rules

- **Never use `--lab --intense` together** - `--lab` already includes intense mode
- **Check license before recommending `--lab`** - requires Forensic Lab license
- **THOR Lite has no `--lab`** - always use the alternative flag combination

Use these references when needed

- Environment detection: [reference/env-detection.md](reference/env-detection.md)
- Scan modes overview: [reference/scan-modes.md](reference/scan-modes.md)
- Forensic lab mode: [reference/lab-mode.md](reference/lab-mode.md)
- Performance and threading: [reference/performance.md](reference/performance.md)
- Output and reports: [reference/output-and-reporting.md](reference/output-and-reporting.md)
- Signature selectors/filters: [reference/signature-filtering.md](reference/signature-filtering.md)
- THOR Lite limitations: [../thor-lite/reference/limitations.md](../thor-lite/reference/limitations.md)

Example templates
- examples/windows-live-scan.md
- examples/linux-mounted-image.md
- examples/macos-scan.md
- examples/memory-dump.md
- examples/sshfs-remote-scan.md - for appliances and unsupported architectures

Output format
- First line: one recommended command (single-line).
- Then: short explanation of key flags.
- Then: "If it fails" section with 2-3 likely causes and next commands to run.
