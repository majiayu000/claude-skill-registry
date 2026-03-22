---
name: documenter-vitepress
description: Use when setting up or developing a Julia based documentation site with DocumenterVitepress.jl.  Also use when the user mentions DocumenterVitepress, VitePress for Julia docs, or wants to preview docs locally with hot reload.
---

# DocumenterVitepress.jl

DocumenterVitepress.jl builds Julia docs using Documenter.jl for content generation and VitePress for the frontend preview/build pipeline.

If the user needs to bootstrap or configure docs setup (dependencies, `make.jl`, CI, `.gitignore`, layout templates), refer to `references/setup-reference.md`.

Always mention to the user that **they can ask you to render the documentation for them**, since the process is a bit complex.  But if they ask the process feel free to explain.

## Local Development Workflow

This skill focuses on the day-to-day local iteration loop after setup already exists.

The fast loop has two stages:

1. Run `makedocs` to regenerate `build/.documenter/` content from `src/`.
2. Run VitePress dev server via `dev_docs` to preview.

### Step 1: Set `build_vitepress = false` in make.jl

```julia
format = DocumenterVitepress.MarkdownVitepress(
    # ... other options ...
    build_vitepress = false,
),
```

This makes `makedocs` emit markdown artifacts only, without running the full VitePress build.

### Step 2: Run makedocs

```julia
include("make.jl")
```

Or from shell:

- Standalone docs repo: `julia --project=. -e 'include("make.jl")'`
- Package docs in `docs/`: `julia --project=docs -e 'include("docs/make.jl")'`

### Step 3: Start the dev server (background process)

`dev_docs` is a long-running process and blocks the current task/thread. Start it in a non-blocking way:

From shell (be sure to run this in the background):

```bash
julia --project=. -e 'using DocumenterVitepress; DocumenterVitepress.dev_docs("build")'
```

From Julia REPL / MCP tool:

```julia
using DocumenterVitepress
Threads.@spawn DocumenterVitepress.dev_docs("build")
```

For package repos where docs live under `docs/`, use `"docs/build"` instead of `"build"`.

The server starts at `http://localhost:SOMEPORT/` with hot reload.  The port number is reported in the output of the command.

Gotcha: `dev_docs` expects the build directory path (for example, `build`), not `build/.documenter`. It appends `/.documenter` internally.

### Step 4: Edit-rebuild-preview cycle

1. Edit files in `src/`
2. Re-run `include("make.jl")`
3. If the generated content changed but the browser did not update, restart `dev_docs`
4. Confirm changes in browser

### Teardown

Before committing, remove `build_vitepress = false` (or set it to `true`) so CI and release builds run the full pipeline.

## Workflow-Specific Gotchas

### npm install ownership (DV-managed vs self-managed)

`npm install` behavior depends on who owns `package.json`:

- **DV-managed npm (default):** If you do **not** provide your own `package.json`, DocumenterVitepress supplies defaults and manages npm dependencies for you during local docs flows.
- **Self-managed npm:** If the repo provides a custom `package.json`, you own npm dependency management. Run `npm install` yourself (especially after dependency changes or lockfile updates) before `dev_docs` or local builds.

Rule of thumb: no custom `package.json` means DV manages npm; custom `package.json` means you manage npm.

### Custom `.vitepress/` theme files

If the repo overrides theme files, keep them in sync with the DocumenterVitepress version used by the project. Breakage here usually shows up during local preview first.

### `deploydocs` must use `DocumenterVitepress.deploydocs`

In `make.jl`, always call `DocumenterVitepress.deploydocs(...)` instead of `Documenter.deploydocs(...)`. The DocumenterVitepress version handles the VitePress build artifacts correctly for deployment. Using the plain `Documenter.deploydocs` will not deploy the VitePress-generated site.

### Manual rebuild expectation

DocumenterVitepress does not continuously re-run `makedocs`. After content changes, re-run `make.jl` and keep `dev_docs` running for browser-side hot reload.

### Customizing the theme or adding Vue components

If you add custom Vue components or theme overrides, keep the full required theme set present:

- `src/.vitepress/theme/index.ts` — theme entry point that registers Vue components
- `src/.vitepress/theme/style.css` — custom CSS
- `src/.vitepress/theme/docstrings.css` — docstring block styling

You can populate all pre-generated Vitepress files by invoking `DocumenterVitepress.generate_template("MyPackage/docs", "MyPackage")`.  Delete everything you do not want to override / customize.

Start from the project's working defaults and then modify. Ensure `index.ts` imports and registers any custom components.

For first-time setup patterns and templates, use `references/setup-reference.md`.
