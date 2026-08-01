---
name: build-and-test
description: Build, test, and serve the documentation site using Zensical (recommended)
  or MkDocs.
---

# Skill: Build and Test Documentation

Build, test, and serve the documentation site using Zensical (recommended) or MkDocs.

## When to Use

- Before committing documentation changes
- After adding or modifying pages
- Debugging build errors
- Previewing changes locally

## Quick Commands

```bash
# Build and serve with Zensical (primary, 20x faster)
make serve

# Or using doc-cli
./doc-cli.sh serve

# Build only (no serve)
make build
```

### Legacy MkDocs Commands

```bash
# Serve with MkDocs (legacy, slower)
make mkdocs-serve

# Build with MkDocs
make mkdocs-build
```

## Build Systems Comparison

| System | Build Time | Use Case |
|--------|------------|----------|
| Zensical | ~0.4s | Primary development, production |
| MkDocs | ~8s | Legacy support, versioning with mike |

## Build Process

### 1. Setup (First Time)

```bash
make setup
```

This installs:
- Python dependencies from `requirements.txt`
- Zensical and MkDocs
- Local plugins from `mkdocs_plugins/` (editable install)

### 2. Build

```bash
# Zensical (primary)
make build

# MkDocs (legacy)
make mkdocs-build
```

Output goes to `site/` directory. Build will:
- Compile all markdown to HTML
- Process navigation structure
- Validate internal links

### 3. Serve Locally

```bash
# Zensical on port 8001 (primary)
make serve

# MkDocs on port 8000 (legacy)
make mkdocs-serve
```

Zensical features:
- Blazing fast rebuilds (~0.4s)
- Hot reload on file changes
- Modern architecture

If MkDocs hot reload stops working, use `make serve-clean` or see [Hot Reload Troubleshooting](hot-reload-troubleshooting.md).

## Using Doc-CLI

The doc-cli provides an interactive menu:

```bash
./doc-cli.sh
```

Available commands:
- `serve` - Start Zensical dev server (port 8001)
- `build` - Build with Zensical
- `mkdocs-serve` - Start MkDocs dev server (legacy)

## Environment Variables

```bash
# Custom Zensical server address
DEV_ADDR=0.0.0.0:8080 make serve
```

## Troubleshooting

### "Page not in nav" Warning

Expected for problem sub-pages. These are linked from parent pages, not nav.

### Port Already in Use

```bash
# Kill existing server
pkill -f zensical
pkill -f mkdocs

# Then restart
make serve
```

### Import Errors (MkDocs only)

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$PYTHONPATH:$(pwd)
make build
```

## Checklist

- [ ] Run `make setup` if dependencies changed
- [ ] Run `make build` to validate
- [ ] Check for ERROR messages
- [ ] Run `make serve` to preview
- [ ] Verify navigation works
- [ ] Check responsive layout
