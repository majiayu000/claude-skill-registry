---
name: r-renv
description: >
  R renv package management for data science projects. Use when working with renv (renv.lock,
  renv::restore, renv::snapshot) in R analysis projects. Do NOT load for projects that do not
  use R or renv.
user-invocable: false
---

# R Environment Management

## rig: R Version Manager

Use `rig` to install and switch between multiple R versions.

### Essential Commands

```bash
rig list              # View installed versions
rig add release       # Install latest stable R
rig add 4.4           # Install specific version
rig default 4.4       # Set system default
rig default           # Show current default
```

### Per-Project R Version (Positron)

Pin the R version in `.positron/settings.json` (not committed to git):

**macOS (Apple Silicon)**:
```json
{
  "r.rpath.mac": "/Library/Frameworks/R.framework/Versions/4.4-arm64/Resources/bin/R"
}
```

**macOS (Intel)**:
```json
{
  "r.rpath.mac": "/Library/Frameworks/R.framework/Versions/4.4-x86_64/Resources/bin/R"
}
```

Alternative: Use Positron's Command Palette (Cmd+Shift+P) → "R: Select R Binary".

---

## renv: Package Management

Most R projects use **renv** for reproducible package management.

### Key Commands

```r
renv::status()        # Check sync status
renv::restore()       # Install packages from lockfile
renv::snapshot()      # Record current packages to lockfile
renv::install("pkg")  # Install a package
renv::update()        # Update all packages
```

### How renv Works

- **Activates automatically** via `.Rprofile` when R starts in the project directory
- **Warnings about "project out-of-sync"** are informational, not errors
- **When running R scripts via Bash**, renv still activates but may show warnings — these don't prevent execution

### Workflow

1. If you see "project out-of-sync" warning → run `renv::status()` to see details
2. To sync packages with lockfile → run `renv::restore()`
3. After installing new packages → run `renv::snapshot()` then commit `renv.lock` to git

### Git Tracking

**Commit**: `renv.lock`, `renv/activate.R`, `.Rprofile`
**Ignore**: `renv/library/`, `renv/staging/`, `renv/local/`

---

## Bioconductor

Bioconductor packages have coordinated releases tied to R versions.

### Installation

```r
install.packages("BiocManager")
BiocManager::install("DESeq2")
BiocManager::install(c("limma", "edgeR", "tximport"))
renv::snapshot()  # Always snapshot after installing
```

With renv, you can also use:

```r
renv::install("bioc::DESeq2")
```

### Version Synchronization

| R Version | Bioconductor Version |
|-----------|---------------------|
| R 4.3.x   | Bioconductor 3.18  |
| R 4.4.x   | Bioconductor 3.19–3.20 |
| R 4.5.x   | Bioconductor 3.21  |

Check your current version:

```r
BiocManager::version()
```

If renv reports Bioconductor version mismatches, verify that `BiocManager::version()` matches what's expected for your R version.

---

## Troubleshooting

### "Project out-of-sync"
→ Run `renv::status()` to see details. Run `renv::restore()` to sync, or `renv::snapshot()` if you've installed new packages.

### Failed package installation
→ Try `renv::install("package", rebuild = TRUE)`

### Starting fresh
→ `renv::deactivate()`, remove `renv/` and `.Rprofile`, then `renv::init()`