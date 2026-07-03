---
name: research-repo
description: Scaffold or audit an entire research project repository organized around its source library. Use when starting, structuring, organizing, or reviewing a research repo. Build sources/{og,md,unprocessed}, references.bib, a PDF-to-Markdown converter, a repo-local process-source skill, AGENTS.md, .gitignore, .venv, and the relevant analysis/manuscript/review folders; or audit an existing layout. Not for one-PDF intake or publication replication packages.
---

# Research Repository Scaffold & Audit

## Scope and organizing principle

This skill sets up a new research repository, or audits an existing one, around a single organizing principle: **the source library is the spine of the project, and everything else grows from it.**

A research repo is not a pile of folders. It is a knowledge base (`sources/`) with work built around it. The papers you read become a tracked, LLM-readable corpus; that corpus is keyed to a bibliography; the bibliography is what your manuscript cites; the analysis and writing folders consume the corpus and produce the outputs. Get the spine right and the rest of the repo has an obvious place to live. Get it wrong — PDFs scattered, no Markdown, a bib that does not match what you actually read — and every downstream skill (`literature-review`, `citation-check`, `fact-check`, `paper-tex`) is working on sand.

The spine has five parts:

1. **`sources/og/`** — original PDFs/documents. Archival, **gitignored** (size + copyright). You rarely read these directly.
2. **`sources/md/`** — Markdown conversions, **tracked in git**. This is the LLM-readable knowledge base — *always read sources from here, not from the PDFs*.
3. **`sources/unprocessed/`** — drop zone. New PDFs land here until they are named, converted, and filed.
4. **`sources/references.bib`** — the bibliography. One entry per source, author+year resolvable to its `md/` file, so the manuscript's `\cite` keys map to documents you have actually read.
5. **A conversion script + an intake command** — `scripts/convert-sources.sh` (OpenDataLoader PDF) turns `og/*.pdf` into `md/*.md`; a `process-source` command runs the per-PDF intake (identify → rename → convert → add to bib).

Everything else — `data/`, analysis `scripts/`, `manuscript/` or `paper/`, `review/` + `codebook/`, `figures/`, `tables/`, `replication/` — is built outward from that spine, conditioned on what kind of project this is.

**This skill does the architecture.** It does not process individual PDFs (that is `process-source`) and it does not build the public replication package (that is `replication-package`). It creates or audits the structure those skills operate inside.

## Instructions

### Step 1. Resolve the target and decide the mode

Use the path supplied with the invocation; otherwise default to the current working directory and confirm once before writing into it. Then decide the mode from what is there:

- **Scaffold mode** — the directory is empty, is not yet a git repo, or has no `sources/` and no manuscript. You will build the spine and the outward folders.
- **Audit mode** — the directory already has research content (a `sources/` tree, a manuscript, analysis scripts, a bib). You will read what exists, compare it against the convention, and report present / partial / missing. **Never overwrite an existing file without explicit confirmation**; offer to create only what is missing.

If a repo is half-built (e.g. PDFs exist but no `md/`, or an `og/` with no convert script), that is audit mode with scaffolding gaps — report the gaps and offer to fill them.

### Step 2. Identify the project archetype

The bibliography is the spine of every project; the **outward** folders — and whether a PDF corpus is even appropriate — depend on what the project is. Detect the archetype from concrete signals in the directory (or ask one question if it is genuinely ambiguous). Do not force a paper-centric layout onto a literature review, or a PDF corpus onto a theory paper.

| Archetype | Concrete signals | Outward folders to scaffold |
|-----------|------------------|------------------------------|
| **Literature / systematic review** | many `sources/md/` files; a coding protocol; an inventory CSV | `review/` (inventory CSV + per-source annotations), `codebook/` (evaluation protocol), `data/` (open datasets collected) |
| **Empirical analysis / paper** | data files (`*.csv`, `*.dta`) beside estimation scripts (`*.R`, `*.do`, `*.py`); a manuscript heading to a journal | `data/`, `scripts/` (analysis), `paper/` or `manuscript/`, `figures/`, `tables/`, `replication/` |
| **Corpus / digitization** | scanned images / OCR output; a large derived corpus | `data/` (raw + derived corpus), `scripts/` (OCR/cleanup pipeline), plus `sources/` for the methods literature |
| **Lightweight / theory paper** | a manuscript and a `.bib` but no archived PDFs and no large dataset | a `paper/` or `manuscript/` folder and its `.bib`; **no `sources/` PDF corpus** unless the user asks for one |
| **Mixed** | several of the above | scaffold the union; keep one shared bibliography |

Most projects have a literature corpus **and** head to a paper. When in doubt, scaffold the spine plus `data/`, `scripts/`, and the manuscript folder, and let the project grow the rest.

**Some repos legitimately keep no PDF corpus** — a theory paper, or a short empirical paper with a hand-maintained `.bib`. There the spine is the bibliography alone: do **not** force a `sources/og`/`sources/md` tree. Audit the `.bib` wherever it lives (often `paper/references.bib`) and *offer* — never impose — a source library if the user wants one.

### Step 3. Scaffold the sources spine

For any project that reads and archives a literature, this is the core. (For a corpus-free repo — the lightweight/theory archetype in Step 2 — scaffold only the bibliography and the manuscript folder, then skip to Step 4.) Create:

```text
<repo>/
├── sources/
│   ├── og/                 # original PDFs/docs — gitignored
│   ├── md/                 # Markdown conversions — tracked
│   ├── unprocessed/        # drop zone for new PDFs
│   ├── references.bib      # bibliography (one entry per source)
│   └── README.md           # the convention, written down
├── scripts/
│   └── convert-sources.sh  # PDF/docx → Markdown (OpenDataLoader PDF + pandoc)
├── .agents/
│   └── skills/
│       └── process-source/
│           └── SKILL.md    # repo-local per-PDF intake skill
├── AGENTS.md               # canonical project conventions for Codex
├── CLAUDE.md -> AGENTS.md  # optional cross-platform compatibility symlink
├── .gitignore
└── .venv/                  # python env for opendataloader-pdf (created in setup)
```

**First, make sure the repo is under version control** — the whole tracked/gitignored split (`og/` ignored, `md/` tracked) only takes effect once git exists:

```bash
git rev-parse --git-dir >/dev/null 2>&1 || git init
```

Write the templates from the **Templates** section below. Then set up the conversion environment — but verify the toolchain first, because `convert-sources.sh` runs under `set -euo pipefail` and will abort opaquely if the Java backend is missing:

```bash
command -v python3 && python3 --version
command -v java && java -version          # OpenDataLoader PDF needs Java 11+; if absent, stop and tell the user to install it
python3 -m venv .venv
.venv/bin/pip install --upgrade pip opendataloader-pdf
```

Optionally create a `CLAUDE.md` compatibility symlink so Claude Code reads the same canonical instructions. Do not overwrite an existing file:

```bash
test -e CLAUDE.md || ln -s AGENTS.md CLAUDE.md
```

Finally, smoke-test the pipeline so you hand off something that works, not just something that exists — on an empty `og/` it should print `Nothing new to convert.`:

```bash
./scripts/convert-sources.sh
```

### Step 4. Build outward (archetype-conditioned)

Create only the outward folders the archetype calls for (Step 2). Leave them empty with a one-line purpose in the README — the project fills them. Common folders and what they hold:

- **`data/`** — datasets. Raw inputs and derived analysis-ready files. Large/binary data is gitignored (see template); document restricted data rather than committing it.
- **`scripts/`** — analysis and utility code (the convert script already lives here).
- **`review/`** + **`codebook/`** (review projects) — the inventory CSV (one row per source), per-source prose annotations, and the coding protocol that governs them. This is where the `sources/md/` corpus gets turned into structured evidence.
- **`manuscript/`** or **`paper/`** — the draft. Cites `sources/references.bib`. Hand this to `paper-tex` to typeset.
- **`figures/`**, **`tables/`** — generated outputs. Pair with the `figures` / `tables` skills.
- **`replication/`** — the public reproducibility package. **Do not hand-build this here** — when the paper is ready, call `replication-package` to scaffold it properly.
- **`logs/`**, **`meetings/`** — session logs and notes; usually local-only (gitignored).

### Step 5. Document the intake pipeline

The spine only stays trustworthy if every new source flows through the same pipeline. Write it into `sources/README.md` and the `process-source` command, and state it to the user:

```
drop in sources/unprocessed/  →  identify (title/authors/year/venue)
  →  rename to author-year-slug, move to sources/og/
  →  ./scripts/convert-sources.sh  (→ sources/md/<name>.md)
  →  add a BibTeX entry to sources/references.bib
  →  (review projects: add inventory row + annotation)
```

The per-PDF mechanics are the `process-source` skill's job — the scaffolded `process-source.md` command points at it. Do not reimplement that logic here; this skill guarantees the pipeline *exists and is wired*, `process-source` *runs* it.

### Step 6. The BibTeX contract

The bibliography — `sources/references.bib`, or wherever the project keeps it (e.g. `paper/references.bib`) — is the contract between the manuscript and the knowledge base: a `\cite` key is only trustworthy if it resolves to a source you have actually read and filed in `sources/md/`. Keep it honest:

- **One entry per source**, added at intake (Step 5), never in a batch at the end.
- **Citekey** follows the project's own key style (e.g. `hainmueller_hopkins_yamamoto_2014` or `hainmueller-etal-2014-conjoint`). Do not impose a scheme on an existing project — but keep every key **author+year resolvable to its `md/` filename**, because `citation-check` and `fact-check` map keys to source files by author and year. The filename uses `author-year-slug`; the bib key can differ in punctuation but must point at the same work.
- **`sources/missing.bib`** (optional, recommended) — a second bib for works that are cited but have **no PDF in `og/`**: paywalled articles with no preprint mirror, books, dissertations, and authoritative web resources (a standard, a DOI registry). Record why each is missing and how to acquire it. This keeps "cited but unread/unfiled" visible instead of silently absent. Some projects track the same information in a `needs_updates.md`-style flag file instead; either works, as long as cited-but-unfiled sources stay visible.
- The bib is the single source of truth for citations across the repo — `paper-tex`, `citation-check`, and `fact-check` all read it.

### Step 7. Audit checklist (audit mode)

Read the existing repo and report each item as **present / partial / missing**. Offer to fix only the gaps; never overwrite without confirmation. If the repo keeps no PDF corpus by design (the lightweight/theory archetype), mark the PDF-corpus items **n/a for this archetype**, not *missing*, and audit the bibliography wherever it actually lives — discover it with `find . -name '*.bib' -not -path './.venv/*' -not -path './.git/*'`.

**Spine**
- [ ] `sources/og/`, `sources/md/`, `sources/unprocessed/` all exist.
- [ ] `sources/og/` is gitignored; `sources/md/` is tracked (the LLM-readable corpus must be in git).
- [ ] Every `og/*.pdf` has a matching `md/*.md` (no unconverted sources). List the orphans.
- [ ] Every `md/*.md` has a `references.bib` entry, and every bib entry resolves to a source (flag bib entries with no file and files with no bib — *drift in either direction*).
- [ ] Filenames follow `author-year-slug` (lowercase, hyphens, ≤3 authors then `firstauthor-etal`).
- [ ] `sources/references.bib` exists; keys are author+year resolvable to filenames.
- [ ] `sources/README.md` documents the convention.

**Detection recipes** (run from the repo root; approximate starting points, not gospel):

```bash
# Orphan PDFs — in og/ but never converted to md/
comm -23 <(cd sources/og && ls *.pdf 2>/dev/null | sed 's/\.pdf$//' | sort) \
         <(cd sources/md && ls *.md  2>/dev/null | sed 's/\.md$//'  | sort)

# Bib keys present in the bibliography
grep -oE '^@[a-zA-Z]+\{[^,]+' sources/references.bib | sed 's/^@[a-zA-Z]*{//' | sort

# Filenames that violate author-year-slug (lowercase-hyphen, four-digit year, slug)
ls sources/og | grep -vE '^[a-z0-9]+(-[a-z0-9]+)*-(19|20)[0-9]{2}-[a-z0-9-]+\.(pdf|docx)$'
```

Compare `md/` stems against the bib keys by author+year (keys may use underscores where filenames use hyphens) to surface drift in either direction — a source with no bib entry, or a bib entry with no source.

**Pipeline**
- [ ] `scripts/convert-sources.sh` exists and points at this repo's `sources/og` → `sources/md`.
- [ ] `.venv/` with `opendataloader-pdf` is set up (or setup is documented); Java 11+ available.
- [ ] A `process-source` command (or the global skill) is available for intake.

**Repo conventions**
- [ ] `AGENTS.md` documents the project and its conventions; any `CLAUDE.md` compatibility file agrees with it.
- [ ] `.gitignore` excludes `sources/og/`, `.venv/`, large data, secrets, and OS/editor cruft.
- [ ] Outward folders match the archetype and have a stated purpose (README).
- [ ] No secrets, answer keys, or restricted data in the tracked path.

### Step 8. Report

Output a short report:

1. Mode (scaffold / audit) and detected archetype.
2. The tree created (scaffold) or the present/partial/missing diff (audit).
3. For audits: orphan PDFs, bib drift, naming violations, and pipeline gaps, each with a one-line fix.
4. The next three actions (typically: set up `.venv` and run `convert-sources.sh`; drop the first PDFs in `unprocessed/` and run `$process-source`; fill in `AGENTS.md` placeholders).

Do not commit unless asked.

## Templates

### `sources/README.md`

````markdown
# Sources

The source library is the spine of this project. Read sources from `md/`, never the PDFs.

## Structure

- `og/` — original PDFs and documents (gitignored; not pushed)
- `md/` — LLM-readable Markdown conversions (tracked in git)
  - `<name>_images/` folders hold figures/tables extracted from the PDF
- `unprocessed/` — drop zone for new PDFs awaiting intake
- `references.bib` — bibliography (one entry per source)
- `missing.bib` — cited works with no PDF available (paywalled, books, web resources)

## Naming convention

`author-year-slug`, lowercase with hyphens:

- Up to three authors → use all three; more → `firstauthor-etal`
- Then year, then a 2–4 word content slug
- Example: `hainmueller-hopkins-yamamoto-2014-causal-inference-conjoint`

The PDF in `og/` carries this name through to `md/`.

## Adding a source

1. Drop the PDF (or `.docx`) into `sources/unprocessed/`
2. Run the `process-source` command (or do it by hand): rename to `author-year-slug`,
   move to `og/`, run `./scripts/convert-sources.sh`, add a `references.bib` entry
3. The convert script only touches files without a matching `.md` — re-running is safe
4. Commit the new `md/<name>.md` (and its `_images/`); `og/` stays local

## Requirements

- Python venv at `.venv/` with `opendataloader-pdf` installed
- `pandoc` (for `.docx`) · Java 11+ (OpenDataLoader PDF backend)

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip opendataloader-pdf
```

## Why Markdown?

PDFs are awkward for LLMs. The Markdown versions preserve text, headings, and
references in a form agents can read directly, enabling source-grounded analysis
and writing. OpenDataLoader PDF: https://github.com/opendataloader-project/opendataloader-pdf
````

### `scripts/convert-sources.sh`

```bash
#!/usr/bin/env bash
# Convert new PDFs/docx in sources/og/ to Markdown in sources/md/.
# Skips files that already have a corresponding .md.
# Usage: ./scripts/convert-sources.sh          # incremental (new files only)
#        ./scripts/convert-sources.sh --all     # reconvert everything
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCES="$PROJECT_ROOT/sources/og"
OUTPUT="$PROJECT_ROOT/sources/md"
VENV="$PROJECT_ROOT/.venv"

FORCE=false
[[ "${1:-}" == "--all" ]] && FORCE=true

mkdir -p "$OUTPUT"
source "$VENV/bin/activate"

converted=0

# PDFs via OpenDataLoader PDF
for pdf in "$SOURCES"/*.pdf; do
    [ -f "$pdf" ] || continue
    base="$(basename "$pdf" .pdf)"
    if [[ "$FORCE" == false && -f "$OUTPUT/$base.md" ]]; then
        continue
    fi
    echo "Converting $base.pdf..."
    opendataloader-pdf "$pdf" --format markdown --output-dir "$OUTPUT/"
    converted=$((converted + 1))
done

# .docx via pandoc
for docx in "$SOURCES"/*.docx; do
    [ -f "$docx" ] || continue
    base="$(basename "$docx" .docx)"
    if [[ "$FORCE" == false && -f "$OUTPUT/$base.md" ]]; then
        continue
    fi
    echo "Converting $base.docx..."
    pandoc "$docx" -t markdown -o "$OUTPUT/$base.md"
    converted=$((converted + 1))
done

if [[ $converted -eq 0 ]]; then
    echo "Nothing new to convert."
else
    echo "Converted $converted file(s). Markdown sources in $OUTPUT/"
fi
```

For large corpora, a parallel variant (`xargs -P N` over `opendataloader-pdf`) speeds bulk conversion; the incremental script above is the default and is safe to re-run.

### `.agents/skills/process-source/SKILL.md`

```markdown
---
name: process-source
description: Process new papers from sources/unprocessed through the repository's complete source-intake pipeline. Use when adding PDFs or documents to this research project.
---

# Process unprocessed sources

Check `sources/unprocessed/` for new PDFs/docs. For each one:

1. **Identify** — read it; determine title, authors, year, venue.
2. **Rename & move** — to `sources/og/` using `author-year-slug` (see `sources/README.md`).
3. **Convert** — run `./scripts/convert-sources.sh` to generate `sources/md/<name>.md`.
4. **BibTeX** — add an entry to `sources/references.bib` (author+year resolvable to the filename).
5. **(Review projects)** — classify per `codebook/` and add an inventory row + annotation.
6. **Clean up** — remove the file from `sources/unprocessed/`.

Flag anything needing human review (paywalled, poor OCR, data-integrity concerns).
If a cited work has no obtainable PDF, record it in `sources/missing.bib` instead.

Prefer this project's conventions; defer to the global `process-source` skill for the generic mechanics.
```

### `AGENTS.md`

```markdown
# <Project name>

<One paragraph: what this project is, who it is for, and its current phase.>

## Repository structure

The source library is the spine. See `sources/README.md` for the intake convention.

- `sources/md/` — LLM-readable Markdown corpus. **Always read sources from here, not the PDFs.**
- `sources/unprocessed/` — drop zone for new PDFs.
- `sources/references.bib` — bibliography; the citation contract for the manuscript.
- `scripts/` — conversion and analysis code.
- <archetype folders: review/ + codebook/  |  data/ + paper/ + figures/ + tables/ + replication/>

## Conventions

- Source naming: `author-year-slug` (lowercase, hyphens).
- New sources flow through the intake pipeline (`$process-source`), never dropped straight into `md/`.
- Read from `sources/md/`; cite from `sources/references.bib`.
- Large data, original PDFs, `.venv/`, and secrets are gitignored.
```

### `.gitignore`

```text
# Original PDFs and large binaries — keep local, don't push
sources/og/
*.pdf
*.xlsx
*.dta
*.7z
*.zip

# Large data files (keep code, not data)
data/**/*.csv
data/**/*.tsv
data/**/*.png

# Python environment
.venv/

# Sensitive — never commit
.env
.env.*
*.pem
*.key
*ANSWER_KEY*
*do_not_share*

# Local-only working areas
logs/

# macOS / R / editors
.DS_Store
.Rhistory
.vscode/
.idea/
```

> Adjust the data rules to the project: if a dataset is public and small, track it; if it is large or restricted, gitignore it and document it in the README. The default keeps original PDFs out of git (copyright + size) while keeping the `md/` corpus tracked.

## When to reach for this skill vs. siblings

- **`research-repo`** (this) — create or audit the *working* repository's structure, anchored on `sources/`. Use at project start, or when a repo has grown messy.
- **`process-source`** (a global skill, not part of this plugin) — run the per-PDF intake into the structure this skill creates. Use every time a new paper arrives.
- **`replication-package`** — scaffold or audit the *public* reproducibility package built from the finished paper. Use near submission. (This skill creates the working repo; that one creates the archive.)
- **`literature-review` / `citation-check` / `fact-check`** — consumers of the `sources/md/` + `references.bib` knowledge base this skill establishes.

## Quality checks

- [ ] Mode (scaffold / audit) and archetype decided **before** any file is written; nothing overwritten without confirmation.
- [ ] Outward folders fit the archetype; no `sources/` PDF corpus forced onto a repo that does not want one.
- [ ] Scaffold mode initialized git (if needed), verified the toolchain (python3 + Java 11+), and smoke-tested `convert-sources.sh`.
- [ ] The spine is wired: bibliography present and author+year resolvable to `md/` filenames; `sources/og/` gitignored, `sources/md/` tracked; convert script points at this repo and uses OpenDataLoader PDF (+ pandoc).
- [ ] `AGENTS.md` exists; any optional `CLAUDE.md` symlink points to it.
- [ ] Audit mode reported present / partial / n-a / missing and ran the detection recipes for orphan PDFs, bib drift, and naming.
- [ ] Architecture only: per-PDF intake deferred to `process-source`, the public package to `replication-package`.
- [ ] Final report lists the next three concrete actions.
