---
name: pooch
description: |
  Data file fetching and caching for geoscience applications. Download sample
  datasets with automatic caching, checksum verification, and multiple download
  sources. Use when Claude needs to: (1) Download datasets from URLs or DOIs,
  (2) Cache files locally with automatic verification, (3) Verify file integrity
  with SHA256/MD5 hashes, (4) Extract compressed archives (ZIP, TAR, GZIP),
  (5) Create data registries for reproducible workflows, (6) Fetch from Zenodo
  or other repositories.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Data Download, Caching, Reproducibility, File Management, Pooch, Checksum, Data Registry, Scientific Data]
dependencies: [pooch>=1.7.0]
complements: [xarray]
workflow_role: data-loading
---

# Pooch - Data File Fetching

## Quick Reference

```python
import pooch

# Download single file
file_path = pooch.retrieve(
    url="https://example.com/data.csv",
    known_hash="sha256:abc123...",  # None to skip verification
    fname="data.csv",
    path=pooch.os_cache("myproject")
)

# Create registry for multiple files
REGISTRY = pooch.create(
    path=pooch.os_cache("myproject"),
    base_url="https://example.com/data/",
    registry={"data.csv": "sha256:abc123...", "model.nc": "sha256:def456..."}
)
data_file = REGISTRY.fetch("data.csv")

# Generate hash for local file
file_hash = pooch.file_hash("/path/to/file.csv")
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `pooch.retrieve()` | Download single file with caching |
| `pooch.create()` | Create custom data registry |
| `pooch.file_hash()` | Generate SHA256/MD5 hash of file |
| `pooch.os_cache()` | Get OS-specific cache directory |

## Essential Operations

### Download Files
```python
# With hash verification
file_path = pooch.retrieve(
    url="https://example.com/data.nc",
    known_hash="sha256:abc123..."
)

# Without verification (development only)
file_path = pooch.retrieve(url="https://example.com/data.nc", known_hash=None)

# From Zenodo DOI
file_path = pooch.retrieve(
    url="doi:10.5281/zenodo.1234567/data.zip",
    known_hash="sha256:abc123..."
)
```

### Extract Archives
```python
# ZIP archive
files = pooch.retrieve(
    url="https://example.com/data.zip",
    known_hash="sha256:abc123...",
    processor=pooch.Unzip()
)

# Decompress single gzip file
file_path = pooch.retrieve(
    url="https://example.com/data.csv.gz",
    known_hash="sha256:abc123...",
    processor=pooch.Decompress(name="data.csv")
)
```

### Additional Options
```python
# Progress bar for large downloads
file_path = pooch.retrieve(url=url, known_hash=hash, progressbar=True)

# HTTP authentication
file_path = pooch.retrieve(
    url="https://example.com/protected/data.csv",
    known_hash=None,
    downloader=pooch.HTTPDownloader(auth=("user", "pass"))
)
```

## Processor Options

| Processor | Purpose |
|-----------|---------|
| `Unzip()` | Extract ZIP archives |
| `Untar()` | Extract TAR/TAR.GZ archives |
| `Decompress()` | Decompress gzip, bz2, lzma, xz |

## Cache Locations

| OS | Default Path |
|----|--------------|
| Linux | `~/.cache/<project>` |
| macOS | `~/Library/Caches/<project>` |
| Windows | `C:\Users\<user>\AppData\Local\<project>\Cache` |

## Error Handling

```python
try:
    file_path = pooch.retrieve(url=url, known_hash=hash)
except pooch.exceptions.HTTPDownloadError:
    print("Download failed - check URL")
except pooch.exceptions.DownloadError:
    print("Network issue")
```

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **pooch** | Reproducible data downloads, hash verification, caching | Not a version control system |
| **urllib/requests** | Simple one-off downloads, custom HTTP logic | No caching, no hash verification |
| **DVC** | Data version control alongside git | Heavier setup, requires remote storage |
| **wget** | Quick command-line downloads | No Python integration, no caching logic |

**Use pooch when** you need reproducible data downloads with automatic caching and
integrity verification, especially for scientific data registries.

**Consider alternatives when** you need full data version control with git integration
(use DVC), simple one-off downloads without caching needs (use requests), or
command-line batch downloads (use wget).

## Common Workflows

### Set up reproducible data download with registry
- [ ] Identify all required data files and their URLs
- [ ] Generate SHA256 hashes with `pooch.file_hash()` for each file
- [ ] Create registry with `pooch.create()` specifying base URL and file hashes
- [ ] Fetch files with `REGISTRY.fetch()` in analysis scripts
- [ ] Add processors for compressed files (`Unzip()`, `Untar()`, `Decompress()`)
- [ ] Test registry by clearing cache and re-fetching
- [ ] Document registry in project README for collaborators

## References

- **[Registry Configuration](references/registry.md)** - Create and manage file registries

## Scripts

- **[scripts/create_registry.py](scripts/create_registry.py)** - Generate registry from local files
