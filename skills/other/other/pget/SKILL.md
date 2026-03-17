---
name: pget
description: Parallel file download and optional tar extraction using the pget CLI (single URL or multifile manifest). Use when you need high‑throughput downloads from HTTP(S)/S3/GCS, want to split a large file into chunks for speed, or want to download and extract a .tar/.tar.gz in one step.
---

# Pget

## Overview
Use pget for fast, parallel downloads and optional in‑memory tar extraction. Prefer it over curl/wget for large files or batch downloads.

## Quick start
- **Single file**: `pget <url> <dest>`
- **Extract tar after download**: `pget <url> <dest> -x`
- **Multi-file manifest**: `pget multifile <manifest-path>` (or `-` for stdin)

## Tasks

### 1) Download a single large file quickly
1. Choose destination path.
2. Run:
   ```bash
   pget <url> <dest>
   ```
3. Tune if needed:
   - `--concurrency <n>` to change chunk parallelism
   - `--chunk-size 125M` (or other size)
   - `--retries <n>`
   - `--force` to overwrite

### 2) Download and extract a tar archive
Use when the URL points to a `.tar`, `.tar.gz`, or similar.
```bash
pget <url> <dest> -x
```
This extracts in‑memory without writing the tar to disk first.

### 3) Download many files with a manifest
1. Create a manifest with `URL` + space + `DEST` per line.
2. Run:
   ```bash
   pget multifile /path/to/manifest.txt
   # or
   cat manifest.txt | pget multifile -
   ```
3. Tune:
   - `--max-concurrent-files <n>`
   - `--max-conn-per-host <n>`

## Notes & pitfalls
- Use `--force` if the destination exists and you need overwrite.
- `--connect-timeout` accepts duration (e.g., `10s`).
- `--log-level debug` or `--verbose` for troubleshooting.

## References
- Load `references/pget.md` for full option list and examples.
