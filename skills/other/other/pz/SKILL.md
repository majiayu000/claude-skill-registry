---
name: pz
description: The Paperzilla CLI (pz) for searching, filtering, and browsing high-signal academic papers. Use when the user wants to check their research feeds, list projects, or find new papers. Note: Requires a Paperzilla account.
metadata:
  {
    "openclaw":
      {
        "emoji": "🦖",
        "requires": { "bins": ["pz"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "paperzilla-ai/tap/pz",
              "bins": ["pz"],
              "label": "Install Paperzilla CLI (brew)",
              "os": ["darwin"]
            }
          ]
      }
  }
---

# Paperzilla CLI (pz) 🦖

A command-line tool for [Paperzilla](https://paperzilla.ai), an AI-powered scientific paper discovery platform.

## Install

macOS:
```bash
brew install paperzilla-ai/tap/pz
```

Windows (Scoop):
```bash
scoop bucket add paperzilla-ai https://github.com/paperzilla-ai/scoop-bucket
scoop install pz
```

Linux:
```bash
curl -sL https://github.com/paperzilla-ai/pz/releases/latest/download/pz_linux_amd64.tar.gz | tar xz
sudo mv pz /usr/local/bin/
```

## Authentication

Log in with your Paperzilla account before doing anything else:
```bash
pz login
```

## Core Commands

### List Projects
Lists your available projects and their IDs.
```bash
pz project list
```

### Browse Feed
Fetches the papers for a given project ID.
```bash
pz feed <project-id>
```

**Filter & Export Flags:**
- `--must-read` : Filter only for must-read papers.
- `--limit 5` : Limit the number of returned results.
- `--since YYYY-MM-DD` : Filter papers published after a specific date.
- `--json` : Output in JSON format (excellent for parsing with other tools or piping into Claude/Gemini).

Example:
```bash
pz feed 12345 --must-read --limit 5 --json
```

### Feed Reader Integration (RSS/Atom)
Get an Atom feed URL you can add to any feed reader (Vienna RSS, NetNewsWire, Feedly, etc.):
```bash
pz feed <project-id> --atom
```
This prints a URL with an embedded feed token. Running `--atom` again after revoking will generate a new token.

## API Configuration
By default, it connects to `https://paperzilla.ai`. To override, set `PZ_API_URL`.
```bash
export PZ_API_URL="https://custom.paperzilla.ai"
```
