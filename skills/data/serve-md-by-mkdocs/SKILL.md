---
name: serve-md-by-mkdocs
description: Serve markdown/docs/text notes with MkDocs using a specified work directory as the output folder (scripts/config/site).
---

# Serve Markdown by MkDocs (DocView)

Use this skill when you want a quick, web-based viewer for Markdown scattered across a repo (not necessarily `docs/`), while preserving the original directory structure.

Typical user phrasing that should trigger this skill:
- “serve markdowns/docs/md/textfiles/etc with mkdocs, using `<work_dir>` as the work dir”

Interpretation:
- `<work_dir>` is the **work directory** (create it if missing; reuse it if it exists). This folder holds the refresh script, a scanner script, a YAML manifest, the MkDocs config (if needed), a staged symlink tree, and `site/` build output.
- By default, staged symlinks are placed under a subdirectory (default: `<work_dir>/_staged/`) so you can ignore them with a local `<work_dir>/.gitignore` while keeping scripts/config tracked if you want.

This skill’s default approach is:
- generate a staged tree under `<work_dir>/_staged/` (typically symlinks; can be adapted to copying)
- generate `<work_dir>/mkdocs.yml` only if missing (existing config is preserved)
- enable Mermaid + KaTeX by default (via `pymdown-extensions` + KaTeX/Mermaid JS/CSS includes)
- run `<mkdocs_cmd> serve` (use MkDocs defaults unless you specify otherwise)

## Dependency Resolution (MkDocs)

This skill must **locate an existing** `mkdocs` first. Do not auto-install it.

Resolution order (stop at the first one that works):

1) **Project Pixi environment** (preferred when available):

```bash
pixi run mkdocs --version
```

If that works, use `<mkdocs_cmd>` = `pixi run mkdocs`.

2) **Active virtualenv / venv** (if the user is already in one):

```bash
mkdocs --version
python -m mkdocs --version
```

If either works, use `<mkdocs_cmd>` = `mkdocs` (or `python -m mkdocs` if the console script is not available).

3) **Global Pixi tools** (if the user installed tools via `pixi global` and exposed them on `PATH`):

```bash
pixi global list
mkdocs --version
```

If that works, use `<mkdocs_cmd>` = `mkdocs`.

4) **uv tools** (only if `mkdocs` is already installed as a tool; do not trigger installs):

```bash
uv tool list
uv tool dir
mkdocs --version
```

If `uv tool list` shows `mkdocs` but `mkdocs` is not on `PATH`, run it via the uv tools directory:

```bash
tool_dir="$(uv tool dir)"
"${tool_dir}/mkdocs/bin/mkdocs" --version
```

If that works, use `<mkdocs_cmd>` = `mkdocs` (or use the explicit path from above).

5) **System Python** (last resort):

```bash
python3 -m mkdocs --version
python -m mkdocs --version
```

If either works, use `<mkdocs_cmd>` = `python3 -m mkdocs` (or `python -m mkdocs`).

If none of the above finds a working `mkdocs`, **fail fast** and report “missing dependency: mkdocs”. Never attempt to install `mkdocs` automatically; let the user install it in their preferred environment manager.

## Plugin Installation (after MkDocs is found)

Once `mkdocs` is found, the agent **may** auto-install any *MkDocs plugins/themes/markdown extensions* needed by `<work_dir>/mkdocs.yml`, but must install them into the **same environment** that provides `<mkdocs_cmd>`.

Guidance:

- Preferred verification step: run `<mkdocs_cmd> build -f <work_dir>/mkdocs.yml` (or `<mkdocs_cmd> serve -f <work_dir>/mkdocs.yml`) and look for missing-module errors (for example: `No module named ...`, missing `mkdocs-material`, missing `pymdown-extensions`, missing `mkdocs-extrafiles`, etc).
- Install only what’s needed to satisfy the config (theme/plugins/markdown_extensions). Do not install `mkdocs` itself automatically.

Notes:
- Mermaid and KaTeX support in this skill’s scaffolded config does **not** require an MkDocs plugin; it uses built-in `extra_javascript`/`extra_css` plus `pymdown-extensions` (`pymdownx.superfences` and `pymdownx.arithmatex`).

Environment-specific install strategy:

1) If `<mkdocs_cmd>` is `pixi run mkdocs` (project Pixi):

- Prefer updating the project manifest (do not `pip install` directly):

```bash
pixi add --pypi mkdocs-material pymdown-extensions
```

Add other required plugins similarly (example):

```bash
pixi add --pypi mkdocs-extrafiles mkdocs-include-markdown-plugin
```

Then re-run `<mkdocs_cmd> build -f <work_dir>/mkdocs.yml` to verify.

2) If `<mkdocs_cmd>` comes from a venv / system Python:

- Install into that Python (use the same interpreter that runs MkDocs):

```bash
python -m pip install mkdocs-material pymdown-extensions
```

Then re-run `<mkdocs_cmd> build -f <work_dir>/mkdocs.yml` to verify.

3) If `<mkdocs_cmd>` comes from a uv tool install:

- Install into the uv tool environment (only after confirming it exists; do not trigger installs of MkDocs itself):

```bash
tool_dir="$(uv tool dir)"
ls -la "${tool_dir}/mkdocs/bin"  # inspect this directory to find the tool's python
"${tool_dir}/mkdocs/bin/python" -m pip install mkdocs-material pymdown-extensions
```

Then re-run the uv-provided MkDocs command to verify.

## When to Use

- You have Markdown scattered across multiple folders (notes, design docs, runbooks, PRDs, etc).
- You want “browse everything” without curating `nav:` in the main `mkdocs.yml`.
- You want a dedicated service name/port separate from the main docs site.

## Parameters to Collect

1) **Work directory**: e.g. `docview-prd`, `docview-reports`, `tmp/docview-issues`
2) **Site title**: e.g. `PRD View`
3) **Serve address/port**:
   - Default: keep it local (MkDocs default is typically `127.0.0.1:8000`)
   - If the user asks to “make it public”: bind `0.0.0.0` (for example `0.0.0.0:8000` or `0.0.0.0:<port>`)
4) **Scan inputs** (repo-relative paths or glob patterns): e.g. `<docs_dir> <notes_dir>` or `<docs_dir>/**` or `**/*.md`
5) Optional: include/exclude rules (hidden dirs, externals, and whether to respect gitignore when discovering files)

## Workflow

### 0) If `<work_dir>` already exists, look for “refresh” cues first

If the user points to an existing `<work_dir>`, they may mean “refresh/rebuild” rather than “re-scaffold”.

Before generating anything, check for these files inside `<work_dir>`:

- `refresh-docs-tree.sh`: if present, prefer running it to recreate the staged tree (typically under `_staged/`, or your chosen `--staging-dir`), while preserving existing rules and defaults.
- `mkdocs.yml`: if present, prefer reusing it (preserves `dev_addr` / ports, theme/plugins, etc).
- `docview.yml`: if present, prefer reusing it (preserves the default scan patterns, exclusions, and gitignore policy).
- `README.md`: often documents the env var names (like `*_DIRS` / `*_REPO_ROOT`) and default scan patterns.

Typical “refresh intent” actions:

```bash
bash <work_dir>/refresh-docs-tree.sh
<mkdocs_cmd> serve -f <work_dir>/mkdocs.yml
```

Only re-scaffold (and overwrite) if the user explicitly asks to “regenerate config/script” (use `--force`).

### 1) Create (or reuse) a dedicated work dir

Run the scaffolder (writes a new service folder with a `refresh-docs-tree.sh`, `.gitignore`, and README):

```bash
pixi run python magic-context/skills/devel/serve-md-by-mkdocs/scripts/scaffold_docview_service.py \
  --work-dir <work_dir> \
  --site-name "Reports View" \
  --staging-dir _staged \
  --default-target .
```

Then run:

```bash
bash <work_dir>/refresh-docs-tree.sh
<mkdocs_cmd> serve -f <work_dir>/mkdocs.yml
```

If you want a non-default bind address/port, either:
- scaffold with `--dev-addr <addr:port>` (bakes it into `<work_dir>/mkdocs.yml`), or
- scaffold with `--public` (bakes `0.0.0.0:8000` into `<work_dir>/mkdocs.yml`), or
- override at runtime: `<mkdocs_cmd> serve -f <work_dir>/mkdocs.yml -a 0.0.0.0:<port>`

### 2) Re-index specific paths/patterns (without re-scaffolding)

Once `<work_dir>/refresh-docs-tree.sh` exists, you can point it at specific paths:

- `bash <work_dir>/refresh-docs-tree.sh <docs_dir> <notes_dir>`
- or set the generated `*_DIRS` env var shown in `<work_dir>/README.md`
- or edit `<work_dir>/docview.yml` to change the default patterns used when you run `bash <work_dir>/refresh-docs-tree.sh` with no args/env override

## Manifest (`<work_dir>/docview.yml`)

`<work_dir>/docview.yml` captures your “what should be staged” intent for symlink creation.

Schema:

- `magic-context/skills/devel/serve-md-by-mkdocs/schemas/docview.schema.json`

Key fields:

- `mkdocs.dev_addr`: records the intended bind address/port (and is used to generate `<work_dir>/mkdocs.yml` only when that file is missing)
- `scan.include_globs`: glob patterns used to discover Markdown (repo-relative)
- `scan.exclude_globs`: glob patterns excluded from Markdown discovery
- `scan.force_globs`: glob patterns to scan even if gitignored (explicit user intent)
- `scan.auto_exclude_generated`: if true (default), avoid scanning DocView/MDView workdirs and their generated trees
- `scan.respect_gitignore`: default `true` (do not scan gitignored dirs/files for Markdown discovery)
- `assets.include_images`: default `true` (stage local images referenced by selected Markdown)

Example (abridged):

```yaml
version: 1
scan:
  auto_exclude_generated: true
  respect_gitignore: true
  include_globs: ["**/*.md"]
  exclude_globs: ["<big_dir>/**"]
  force_globs: ["<gitignored_dir>/**"]
assets:
  include_images: true
```

Rules:

- By default, Markdown discovery respects `.gitignore` and uses `scan.include_globs` from the manifest.
- By default, discovery excludes any directories that start with `.` (controlled by `scan.include_hidden: false`).
- By default, discovery also auto-excludes DocView/MDView workdirs (including their staged trees like `_staged/` or `docs/`, and `site/`) using file/dir-structure heuristics, to avoid self-indexing loops and duplicate pages.
- If you explicitly want to scan a gitignored location, add it under `scan.force_globs` (or pass it as an explicit arg to `refresh-docs-tree.sh`, which is treated as strong intent).
- Referenced image assets are still staged even if gitignored, as long as the file exists.

Default scan behavior (when you don’t specify scan locations): the scaffolder writes `scan.include_globs` so the refresh script scans the whole workspace for Markdown (for example `**/*.md`) while respecting `.gitignore`.

### 3) Add Pixi tasks (optional but recommended)

Add three tasks under `[tool.pixi.tasks]`:

- `<task_prefix>-refresh`: `bash <work_dir>/refresh-docs-tree.sh`
- `<task_prefix>-serve`: `bash <work_dir>/refresh-docs-tree.sh && mkdocs serve -f <work_dir>/mkdocs.yml`
- `<task_prefix>-build`: `bash <work_dir>/refresh-docs-tree.sh && mkdocs build -f <work_dir>/mkdocs.yml`

Pick a port based on your local context (or rely on MkDocs defaults).

Note: Pixi tasks run inside the project Pixi environment. Only add these tasks if `mkdocs` (and any referenced theme/plugins/extensions from `<work_dir>/mkdocs.yml`) are available in that environment.

## Verification (required)

After running `bash <work_dir>/refresh-docs-tree.sh`, verify that all symlinks under the staging directory are valid (no broken links):

```bash
find <work_dir>/<staging_dir> -xtype l -print
```

Expected: no output.

`<staging_dir>` is usually `_staged` (or whatever you set via `--staging-dir`; it should match `docs_dir` in `<work_dir>/mkdocs.yml`).

If there is output, rerun the refresh and/or check whether the target source files were moved/deleted, or whether your selected paths/patterns (`*_DIRS` or CLI args) include paths that no longer exist.

Note: refresh may emit warnings like “missing asset referenced by …” when Markdown references images that don’t exist on disk; those files won’t be staged.

Also verify that the work dir contains the scanner script which decides what gets staged (Markdown + referenced image assets):

- `<work_dir>/scan-files-to-stage.py`

## Notes / Gotchas

- **Git hygiene**: by default, `<work_dir>/.gitignore` ignores the staging subdir (like `_staged/`), `site/`, `mkdocs.yml`, and `repo-root.txt`. Keep or change this based on whether you want staged symlinks tracked.
- **Gitignore-aware scanning**: by default, file discovery respects `.gitignore` (gitignored files/dirs won’t be scanned). However, if a selected Markdown page references a gitignored image file, it will still be staged (symlinked) as long as the file exists.
- **Auto-excluding generated workdirs**: by default, the scanner avoids scanning DocView/MDView workdirs (including this one) to prevent recursion/duplication. Set `scan.auto_exclude_generated: false` in `<work_dir>/docview.yml` if you intentionally want to index those directories.
- **Manifest is required**: `<work_dir>/docview.yml` is always created by this skill, and `<work_dir>/scan-files-to-stage.py` treats a missing manifest as an error.
- **No-symlink alternative**: if you prefer not to stage via symlinks/copies, consider using the `mkdocs-extrafiles` plugin to map external `src` paths into virtual `dest` paths under `docs_dir`.
- **Symlinks**: the default implementation uses symlinks. On Windows, symlink creation may require elevated permissions or Developer Mode; if this is a blocker, reimplement the refresh step by *copying* files instead of linking.
- **Mermaid**: enable `pymdownx.superfences` with a `mermaid` fence + Material integration (the scaffolder emits this).
- **KaTeX (math)**: the scaffolder also emits `pymdownx.arithmatex` + KaTeX auto-render via `extra_javascript`/`extra_css` (you can swap to MathJax if preferred).
- **Mermaid/KaTeX init scripts**: the scaffolder writes `<work_dir>/javascripts/mermaid-init.js` and `<work_dir>/javascripts/katex-init.js`, and `refresh-docs-tree.sh` stages them into `docs_dir` so MkDocs can serve them.
