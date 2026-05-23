---
name: readarr-ops
description: >
  Manage Readarr library, search for books, and monitor downloads.
  Handles service health checks and API interactions.
allowed-tools:
  - run_command
  - read_file
triggers:
  - readarr
  - manage books
  - add book
  - search book
metadata:
  short-description: Manage Readarr library and downloads
---

# readarr-ops

**Manage Readarr library, search for books, and monitor downloads.**

## Commands

- `search <term>`: Search for books/authors in Readarr.
- `nzb-search <term>`: Direct Usenet search via NZBGeek.
- `add <term>`: Search and add the first matching book (Auto-Learn).
- `health`: Check if Readarr is running and healthy.
- `ensure-running`: Start Readarr if not running.

## Usage

```bash
# Check health
./run.sh health

# Search for a book
./run.sh search "The Art of Exploitation"

# Add a book
./run.sh add "Hacking: The Art of Exploitation"
```

## Configuration

- **Readarr Path**: `~/workspace/experiments/Readarr/Readarr`
- **Data Path**: `~/workspace/experiments/Readarr/data`
- **Port**: 8787
- **API Key**: `READARR_API_KEY` env var (optional for localhost in some configs)
