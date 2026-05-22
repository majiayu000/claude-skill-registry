---
name: building-github-index
description: Generate progressive disclosure indexes for GitHub repositories to use as Claude project knowledge. Use when setting up projects referencing external documentation, creating searchable indexes of technical blogs or knowledge bases, combining multiple repos into one index, or when user mentions "index", "github repo", "project knowledge", or "documentation reference".
metadata:
  version: 2.0.0
---

# Building GitHub Index

Create markdown indexes of GitHub repositories optimized for Claude project knowledge. Indexes enable retrieval via GitHub API with semantic descriptions for effective matching.

## Quick Start

```bash
# Documentation repos (markdown/notebooks)
python scripts/github_index.py owner/repo -o index.md

# Code repos (extract symbols via tree-sitter)
python scripts/github_index.py owner/repo --code-symbols -o index.md

# Multiple repos combined
python scripts/github_index.py owner/repo1 owner/repo2 -o combined.md
```

## Script Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output file (default: `github_index.md`) |
| `--token` | GitHub PAT; also reads `GITHUB_TOKEN` env |
| `--include-patterns` | Only index matching globs: `"docs/**" "src/**"` |
| `--exclude-patterns` | Skip matching globs: `"test/**"` |
| `--max-files` | Cap files per repo (default: 200) |
| `--skip-fetch` | Tree only, no content fetch (fast, filename-only descriptions) |
| `--code-symbols` | Include code files, extract function/class names via tree-sitter |

## Description Extraction Priority

1. **YAML frontmatter** - `title:` and `description:` fields
2. **Markdown headings** - First h1/h2 as title, subsequent as topics
3. **Notebook cells** - First markdown cell heading
4. **Code symbols** - Public function/class names (with `--code-symbols`)
5. **Path-derived** - Convert filename to words (fallback)

## When Descriptions Fail

Some repos have stub files (links to external docs, empty readmes). In these cases:

**Manual curation recommended.** Use the tree output and domain knowledge:

```bash
# Get tree structure only (fast)
python scripts/github_index.py owner/repo --skip-fetch -o skeleton.md
# Then manually enhance descriptions based on domain knowledge
```

For code-heavy repos with embedded apps:
- Directory names encode purpose: `acc_wav_gen` → "ACC waveform generation"
- Peripheral acronyms map to functions: AFEC=ADC, MCAN=CAN, TWIHS=I2C
- Operation modes: blocking, interrupt, dma, polled

## Output Format

```markdown
# {Repo} - Content Index

**Repository:** {url}
**Branch:** `{branch}`

## Retrieval Method
{API curl commands}

---

## {Category}

| Description | Path |
|-------------|------|
| {What this covers} | `{path/file.md}` |
```

Description column leads (relevance matching), path follows (retrieval key).

## API Access

Enumerate files:
```bash
curl -sL "https://api.github.com/repos/OWNER/REPO/git/trees/BRANCH?recursive=1"
```

Fetch content:
```bash
curl -s "https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=BRANCH" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

## Network

Allowlist: `api.github.com`, `raw.githubusercontent.com`

## Related Skills

- `accessing-github-repos` - Private repos, PAT setup, tarball download
- `mapping-codebases` - Detailed code structure (methods, imports, line numbers)

## Condensed Format (pk_index.py)

For token-constrained project knowledge, use the condensed script:

```bash
python scripts/pk_index.py owner/repo -o repo_pk.md
```

Produces ~80% smaller output:
- Single line per file: `path` — description
- Symbols only (no signatures)
- 15 files max per category
- No retrieval instructions section

Ideal when adding multiple repo indexes to project knowledge.
