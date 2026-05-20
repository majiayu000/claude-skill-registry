---
name: overleaf
description: Sync and manage Overleaf LaTeX projects from the command line. Pull projects locally, push changes back, compile PDFs, and download compile outputs like .bbl files for arXiv submissions. Use when working with LaTeX, Overleaf, academic papers, or arXiv.
license: MIT
metadata:
  author: aloth
  version: "1.1"
  cli: olcli
  install: brew tap aloth/tap && brew install olcli
---

# Overleaf Skill

Manage Overleaf LaTeX projects via the `olcli` CLI.

## Installation

```bash
# Homebrew (recommended)
brew tap aloth/tap && brew install olcli

# npm
npm install -g @aloth/olcli
```

## Authentication

Get your session cookie from Overleaf:

1. Log into [overleaf.com](https://www.overleaf.com)
2. Open DevTools (F12) → Application → Cookies
3. Copy the value of `overleaf_session2`

```bash
olcli auth --cookie "YOUR_SESSION_COOKIE"
```

Verify with:
```bash
olcli whoami
```

Debug authentication issues:
```bash
olcli check
```

Clear stored credentials:
```bash
olcli logout
```

## Common Workflows

### Pull a project to work locally

```bash
olcli pull "My Paper"
cd My_Paper/
```

### Edit and sync changes

```bash
# After editing files locally
olcli push              # Upload changes only
olcli sync              # Bidirectional sync (pull + push)
```

### Compile and download PDF

```bash
olcli pdf                      # Compile and download
olcli pdf -o paper.pdf         # Custom output name
olcli compile                  # Just compile (no download)
```

### Download .bbl for arXiv submission

```bash
olcli output bbl               # Download compiled .bbl
olcli output bbl -o main.bbl   # Custom filename
olcli output --list            # List all available outputs
```

### Upload figures or assets

```bash
olcli upload figure1.png "My Paper"          # Upload to project root
olcli upload diagram.pdf                      # Auto-detect project from .olcli.json
```

### Download specific files

```bash
olcli download main.tex "My Paper"           # Download single file
olcli zip "My Paper"                          # Download entire project as zip
```

## arXiv Submission Workflow

Complete workflow for preparing an arXiv submission:

```bash
# 1. Pull your project
olcli pull "Research Paper"
cd Research_Paper

# 2. Compile to ensure everything builds
olcli compile

# 3. Download the .bbl file (arXiv requires .bbl, not .bib)
olcli output bbl -o main.bbl

# 4. Download any other needed outputs
olcli output aux -o main.aux    # If needed

# 5. Package for submission
zip arxiv.zip *.tex main.bbl figures/*.pdf

# 6. Verify the package compiles locally (optional)
# Then upload arxiv.zip to arxiv.org
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `olcli auth --cookie <value>` | Authenticate with session cookie |
| `olcli whoami` | Check authentication status |
| `olcli logout` | Clear stored credentials |
| `olcli check` | Show config paths and credential sources |
| `olcli list` | List all projects |
| `olcli info [project]` | Show project details |
| `olcli pull [project] [dir]` | Download project files |
| `olcli push [dir]` | Upload local changes |
| `olcli sync [dir]` | Bidirectional sync |
| `olcli upload <file> [project]` | Upload a single file |
| `olcli download <file> [project]` | Download a single file |
| `olcli zip [project]` | Download as zip archive |
| `olcli compile [project]` | Trigger compilation |
| `olcli pdf [project]` | Compile and download PDF |
| `olcli output [type]` | Download compile outputs |

## Tips

- **Auto-detect project**: Run commands from a synced directory (contains `.olcli.json`) to skip the project argument
- **Dry run**: Use `olcli push --dry-run` to preview changes before uploading
- **Force overwrite**: Use `olcli pull --force` to overwrite local changes
- **Project ID**: You can use project ID instead of name (24-char hex from URL)
- **Debug auth**: Run `olcli check` to see where credentials are loaded from
