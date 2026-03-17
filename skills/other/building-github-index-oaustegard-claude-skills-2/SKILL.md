---
name: building-github-index
description: Generate progressive disclosure indexes for GitHub repositories to use as Claude project knowledge. Use when setting up projects referencing external documentation, creating searchable indexes of technical blogs or knowledge bases, combining multiple repos into one index, or when user mentions "index", "github repo", "project knowledge", or "documentation reference".
metadata:
  version: 0.0.1
---

# Building GitHub Index

Create markdown indexes of GitHub repositories optimized for Claude project knowledge. Indexes enable retrieval of source content (.md, .qmd, .ipynb) via GitHub API without parsing rendered HTML/CSS/JS noise.

## Quick Start

```bash
python scripts/github_index.py owner/repo -o index.md
python scripts/github_index.py owner/repo1 owner/repo2 -o combined.md
python scripts/github_index.py owner/repo --include-patterns "docs/**" "blog/**"
```

## Script Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output file (default: `github_index.md`) |
| `--token` | GitHub PAT; also reads `GITHUB_TOKEN` env var |
| `--include-patterns` | Only index matching globs: `"docs/**" "blog/**"` |
| `--exclude-patterns` | Skip matching globs: `"test/**" "drafts/**"` |
| `--max-files` | Cap files per repo (default: 200) |
| `--skip-fetch` | Tree only, no content fetch; faster but filename-derived descriptions |

**Default exclusions:** `node_modules`, `.git`, `__pycache__`, `venv`, `dist`, `build`, `_site`, `.next`, plus underscore-prefixed files.

**Rate limits:** 60/hr unauthenticated, 5000/hr with token.

## Output Structure

```markdown
# {Repo Name} - Content Index

**Repository:** {url}
**Branch:** `{branch}`

## Retrieval Method
{API curl commands}

---

## {Category}

| Description | Path |
|-------------|------|
| {What this covers} | `{path/to/file.md}` |

## Key Themes
{Concepts that reduce need to fetch}
```

Lead rows with **description** (relevance matching), path second (retrieval key).

## API Access

Fetch tree (enumerate files):
```bash
curl -sL "https://api.github.com/repos/OWNER/REPO/git/trees/BRANCH?recursive=1"
```

Fetch file content:
```bash
curl -s "https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=BRANCH" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

Include retrieval instructions in generated indexes.

## Manual Index Creation

When script doesn't fit or for curated indexes:

1. Get tree, filter to content files (.md, .qmd, .ipynb)
2. Fetch files, extract frontmatter (title/description from YAML between `---` markers)
3. Group by directory structure or theme
4. Write tables: Description | Path
5. Add Key Themes section for frequent queries

## Quality Standards

**Descriptions**: Lead with problem/question addressed. Include searchable terms. Under 100 chars.

**Categories**: Semantic groupings, not flat lists. Subcategories help navigation.

**Themes**: Extract after reviewing content. Summarize frequently-asked concepts.

## Network Requirements

Project allowlist: `api.github.com` (required), `raw.githubusercontent.com` (optional).

## Related Skills

- `accessing-github-repos` - Private repos, PAT setup
- `mapping-codebases` - Code structure (functions/classes) vs documentation
