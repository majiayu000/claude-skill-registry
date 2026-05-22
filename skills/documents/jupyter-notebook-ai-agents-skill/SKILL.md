---
name: Notebook KISS Builder & Verifier (Pixi + DuckDB)
description: Create/refactor Jupyter notebooks for AI-agent workflows with per-directory Pixi kernels (pixi.toml), narrative-first KISS structure (markdown above every code cell), robust data loading (DuckDB + TSV/Parquet), beautiful plots, and strict "run-all-cells" validation before reporting completion.
---

## When to trigger this skill
Use this skill whenever the user asks to **create, refactor, clean up, lint, or productionize** a Jupyter notebook (or a Jupytext notebook script) and they care about:
- **Reproducibility** (restart + run-all should work end-to-end)
- **Per-directory environments** via `pixi.toml` (Pixi + pixi-kernel)
- **Readable narrative** (concise markdown guidance above each code cell)
- **Reliable data access** (DuckDB + tabular files, correct paths)
- **Presentation quality** (plots and markdown are visually polished)

If the task is not notebook-centric (e.g., pure library code), do **not** trigger.

## Non‑negotiables (hard rules)
1. **KISS notebook**: short, linear, top-to-bottom, no hidden dependencies between cells.
2. **Markdown-first**: every code cell must be preceded by a markdown cell that:
   - states intent in 1–3 sentences or bullets,
   - tells what artifact/output will appear,
   - notes assumptions (paths, schema, expected shapes).
3. **Reproducible execution gate**: never claim “done” until:
   - you restart the kernel (clean state) and execute **all cells in order**,
   - you inspect outputs for correctness/sanity (not just “no exceptions”),
   - you fix any warnings/errors that impact correctness.
4. **Paths must be correct**: data files are loaded using paths anchored to the notebook/project directory (see `docs/data_loading_duckdb.md`). Avoid hard-coded home directories.
5. **Pretty, tight plots**: minimize whitespace; use a cohesive, non-default palette; label axes; include units; readable figure sizes.

## Progressive disclosure (keep context lean)
The core rules live here. Load additional guidance only as needed:

- Notebook structure & markdown style: `docs/notebook_structure.md`
- Pixi + Jupyter kernel setup: `docs/pixi_jupyter.md`
- Data loading patterns (DuckDB + TSV/Parquet): `docs/data_loading_duckdb.md`
- Plot styling rules (tight layout, palettes): `docs/plot_style.md`
- Verification & “definition of done”: `docs/verification.md`

Templates:
- Jupytext-first notebook template: `templates/kiss_notebook_template.py`
- Minimal `pixi.toml` example: `templates/pixi.toml`
- Optional DuckDB bootstrap: `templates/duckdb_bootstrap.sql`

Automation scripts (if filesystem + Python execution is available):
- Execute notebook end-to-end: `scripts/execute_notebook.py`
- Lint structure (markdown above code): `scripts/lint_notebook_structure.py`

## Recommended workflow (agent playbook)
Follow this sequence; do not skip the validation gate.

### 1) Plan the notebook (outline first)
- Create/confirm the notebook’s narrative outline:
  - Title + 3-line purpose
  - Environment & reproducibility notes
  - Data sources (files, DBs), schema expectations
  - Analysis/EDA/modeling steps
  - Results + conclusions + next steps

### 2) Scaffold the notebook
- Use the template in `templates/kiss_notebook_template.py`.
- Keep sections small; each section should have:
  - a markdown heading,
  - 1–3 code cells max.

### 3) Implement data access robustly
- Establish `PROJECT_ROOT` and `DATA_DIR`.
- Validate file existence before reading.
- Prefer DuckDB for heavy joins/aggregations; keep pandas for presentation.

### 4) Create high-quality plots
- Use the plot style helper (see `docs/plot_style.md`).
- No chart junk; tight margins; consistent typography.

### 5) Validation gate (mandatory)
- Restart kernel → run all cells.
- If you have CLI access, also run `scripts/execute_notebook.py` for a clean execution.
- Check outputs:
  - row counts, null rates, unique keys, value ranges,
  - plot renders and labels,
  - any randomness is seeded.

### 6) Report completion only after passing the gate
When reporting back, include:
- how you ran the notebook (restart+run-all, scripts),
- where data paths point,
- what key outputs/figures were produced,
- any caveats (e.g., external files required).
