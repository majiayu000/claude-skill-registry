---
name: surge
description: Blazing fast TUI download manager with multi-connection downloads. Use when: (1) Fast downloads with parallel connections, (2) Queue management, (3) Server/daemon mode for headless downloads, (4) Beautiful TUI interface, (5) Multiple mirror support.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision tree, troubleshooting, self-checks"
metadata:
  openclaw:
    requires:
      bins:
        - surge
    emoji: "⚡"
    category: "utility"
    homepage: https://github.com/surge-downloader/Surge
---

# Surge

Blazing fast TUI download manager with multi-connection downloads.

## When This Skill Activates

This skill triggers when user wants to download files fast with parallel connections or manage downloads via TUI.

## Reasoning Framework

| Step | Action | Why |
|------|--------|-----|
| 1 | **INSTALL** | Install surge binary (brew/go/binary) |
| 2 | **START** | Launch server mode or TUI |
| 3 | **ADD** | Add URLs to download queue |
| 4 | **MANAGE** | Monitor, pause, resume, or remove downloads |
| 5 | **RETRIEVE** | Get completed files from output directory |

---

## Install

```bash
# macOS
brew install surge-downloader/tap/surge

# Go
go install github.com/surge-downloader/surge@latest

# Or download binary from releases
```

---

## Decision Tree

### What are you trying to do?

```
├── Quick single download
│   └── Use: surge add "URL" -o ./folder
│
├── Multiple files (batch)
│   └── Use: surge add -b urls.txt -o ./folder
│
├── Headless/daemon downloads
│   └── Use: surge server + surge add
│
├── Beautiful TUI interface
│   └── Use: surge (no args, starts TUI)
│
└── Manage running downloads
    └── Use: surge ls/pause/resume/rm
```

---

## Basic Usage

### Start TUI Mode

```bash
surge
```

### Start Server Mode (Headless)

```bash
# Start server daemon
surge server

# Add download via CLI
surge add "https://example.com/file.zip"

# List downloads
surge ls
```

---

## Commands

| Command | Description |
|---------|-------------|
| `surge server` | Start headless daemon |
| `surge add <url>` | Add download to queue |
| `surge ls` | List downloads |
| `surge pause <id>` | Pause download |
| `surge resume <id>` | Resume download |
| `surge rm <id>` | Remove download |
| `surge token` | Get API token |

---

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output PATH` | Output directory | ./downloads |
| `-b, --batch FILE` | Batch file with URLs | - |
| `--exit-when-done` | Exit when complete | false |
| `--host HOST` | Target server | localhost:9090 |
| `--token TOKEN` | API token | - |

---

## Common Examples

```bash
# Download single file
surge add "https://example.com/file.zip" -o ~/Downloads

# Batch download from file
surge add -b urls.txt -o ./downloads

# Start server with output folder
surge server -o /tmp/downloads

# Add to running server
surge add "https://url.com/file.zip"

# Pause/Resume
surge pause 1
surge resume 1

# Remove from queue
surge rm 1
```

---

## Server Mode

### Workflow

```bash
# Terminal 1: Start server
surge server

# Terminal 2: Add downloads
surge add "https://file1.zip"
surge add "https://file2.zip" -o /other/folder

# Check status
surge ls

# Server runs in background, downloads continue
```

### API Token

```bash
# Get token for remote control
surge token

# Use token to connect
surge add "URL" --token YOUR_TOKEN --host remote:9090
```

---

## Troubleshooting

### Problem: surge: command not found

- **Cause:** Surge not installed
- **Fix:** `brew install surge-downloader/tap/surge` or `go install github.com/surge-downloader/surge@latest`

### Problem: Connection refused

- **Cause:** Server not running
- **Fix:** Start server first: `surge server`

### Problem: Permission denied

- **Cause:** Output folder not writable
- **Fix:** Check folder permissions or use `-o` with writable path

### Problem: Download failed

- **Cause:** URL invalid or network issue
- **Fix:** Verify URL, check network connectivity

### Problem: Too many connections

- **Cause:** Server limit reached
- **Fix:** Wait for current downloads or pause some

---

## Self-Check

- [ ] Surge installed: `surge --version`
- [ ] Output directory exists and is writable
- [ ] For server mode: server is running (`surge ls` to check)
- [ ] For remote: token and host correct

---

## Notes

- Multi-connection downloads up to 32 parallel connections
- TUI mode for interactive downloads
- Server mode for headless/daemon operation
- Batch file support for bulk downloads
- Automatic retry on failure
- Benchmarks: 1.38× faster than aria2, 2× faster than curl/wget

---

## Quick Reference

| Task | Command |
|------|---------|
| Start TUI | `surge` |
| Start server | `surge server` |
| Add download | `surge add "URL" -o ./folder` |
| Batch download | `surge add -b urls.txt` |
| List downloads | `surge ls` |
| Pause/Resume | `surge pause <id>` / `surge resume <id>` |
| Remove | `surge rm <id>` |

---
