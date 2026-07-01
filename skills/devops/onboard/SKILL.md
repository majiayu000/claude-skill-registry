---
name: onboard
description: Collects bounded project context and synthesizes a newcomer orientation tour. Use when the user asks to be onboarded, oriented, given a tour, or shown where to start in a repo.
metadata:
  short-description: New-codebase orientation tour
---

# Onboard — codebase orientation tour

Run an `extend` op for a developer entering an unfamiliar repository. Extend their working context with a compact, evidence-backed map: what the project is, where execution starts, what areas are active, which commands are real, and which 2-3 files to read first.

The output is not a repo summary dump. It is an orientation artifact followed by an `ask` decision: explore an area, trace a feature, make a first change, or find where help is useful.

## When to Apply / NOT

Apply:
- New repository, context switch, unfamiliar PR, or implementation planning before touching code.
- User asks for a tour, starting point, orientation, project summary, or "where do I begin?".
- A local checkout exists, even if it is not a git repo.

NOT:
- User already named a concrete bug or failing test — orient only if the fix path is unclear.
- User wants a full architectural critique, security audit, or performance investigation.
- User asks for exhaustive symbol indexing. Onboard is bounded by depth and optimized for first useful map.

## Inputs

- `path`: repository root; default current working directory.
- `depth`: `quick | normal | deep`; default `normal`.
- Optional focus: area, feature, language, package, or entry point. Focus constrains the deep-read and follow-up guidance, not the initial collection contract.

## Workflow

### 1. Parse scope and depth

Normalize the root path first. Reject nonexistent paths. Preserve the requested depth in the output header.

Depth controls collection cost only; the synthesized orientation always uses the same seven sections.

### 2. Collect bounded context

Collect facts before explaining. Never fabricate a section from filenames alone. Use this native order:

1. **Manifest parse.** Inspect root manifests and workspace manifests:
   - JavaScript / TypeScript: `package.json`, `pnpm-workspace.yaml`, `lerna.json`, `turbo.json`, `nx.json`.
   - Rust: `Cargo.toml`, `[workspace]`, `crates/*/Cargo.toml`.
   - Go: `go.mod`, `go.work`, `cmd/*`, `Makefile` targets.
   - Python: `pyproject.toml`, `setup.py`, `requirements*.txt`, `tox.ini`, `noxfile.py`, `libs/*/pyproject.toml`, `packages/*/pyproject.toml`.
   - Java / JVM: `pom.xml`, `.mvn/`, `build.gradle`, `build.gradle.kts`, `settings.gradle`, `settings.gradle.kts`.
   - Build-only fallback: `Makefile`, `CMakeLists.txt`, `meson.build`, `configure.ac`.
2. **Structure walk, max depth 3.** Prefer ODIN `find`; headless equivalent:
   `fd -d 3 -t d . "$ROOT" -E node_modules -E .git -E dist -E target -E out -E .next -E .nuxt -E __pycache__ -E coverage -E .cache -E vendor`.
   If `fd` is absent: `find "$ROOT" -maxdepth 3 -type d \( -name node_modules -o -name .git -o -name dist -o -name target -o -name out -o -name .next -o -name .nuxt -o -name __pycache__ -o -name coverage -o -name .cache -o -name vendor \) -prune -o -type d -print`.
3. **README and local rules.** Read `README*`, `CLAUDE.md`, and `AGENTS.md`, capped at about 5KB each. Follow a one-line README redirect if it points to another Markdown file.
4. **CI and runtime services.** Inspect `.github/workflows/*.{yml,yaml}`, `.gitlab-ci.yml`, `Dockerfile`, `docker-compose*.yml`, `Procfile`, `compose.yaml`, and deploy manifests present at the root.
5. **Git info.** If git exists, collect branch, remote, commit count, last commit, shallow status, recent owners, and hotspots:
   - `git rev-parse --show-toplevel`
   - `git branch --show-current`
   - `git rev-list --count HEAD`
   - `git log -1 --format='%ci %h %s'`
   - `git remote get-url origin`
   - `git shortlog -sn --all -- .`
   - `git --no-pager log --since='180 days ago' --format='' --name-only -- .`
6. **Native signals.** Prefer codegraph MCP if the repo is indexed:
   - Entry points and execution surfaces: `codegraph_explore("entry points main binaries commands framework configs tests")`.
   - Symbol lookup: `codegraph_search` for `main`, `App`, `server`, `cli`, route handlers, exported package entry points.
   - Call flow from an entry point: `codegraph_callees` or `codegraph_explore` naming the entry symbol and likely module names.
   - File inventory: `codegraph_files` for package/module boundaries.

   If no index exists, fallback to AST and text search:
   - JavaScript/TypeScript: `ast-grep -p 'function main($$$) { $$$ }'`, `ast-grep -p 'export default $$$'`, plus `git grep -nE 'createServer|listen\(|commander|yargs|cac\(|vite|next|astro|svelte'`.
   - Rust: `ast-grep -p 'fn main() { $$$ }'`, `git grep -nE '^\[\[bin\]\]|^path\s*=|fn main\('`.
   - Go: `git grep -nE '^package main$|func main\('`.
   - Python: `git grep -nE 'if __name__ == .__main__.|console_scripts|click\.command|typer\.Typer|argparse'`.
   - Java/JVM: `git grep -nE 'public static void main|@SpringBootApplication|application.yml|plugins \{|mainClass'`.
   - Tests: `fd '(test|spec|_test)\.(js|jsx|ts|tsx|rs|go|py|java|kt)$' "$ROOT"`.
7. **Whole-repo digest.** Use repomix for compressed context:
   - MCP: `pack_codebase(directory="$ROOT", compress=true)`.
   - CLI fallback: `npx -y repomix "$ROOT" --compress -o /tmp/onboard-repomix.xml`.
   Use the digest to confirm stack, top-level modules, and naming conventions. Do not paste it into the final response.

### 3. Synthesize the seven-section orientation

Use the template in `references/orientation.md`. Keep the first pass concise; the target is a 2-3 minute read. Sections are ordered and named exactly:

1. **What it does** — one or two plain-language sentences from README + manifest.
2. **Tech stack + CI** — languages, framework, package manager, build/test tools, CI jobs.
3. **Where execution starts** — entry points grouped by kind: binaries/CLIs, server/app boot, framework-loaded config, libraries/exports, tests/benches.
4. **Project structure, annotated** — top directories with purpose and unusual layout notes.
5. **Active development — hotspots + owners** — top churn files, recent maintainers, areas under change.
6. **Code health** — slop/drift/test gaps only when evidence exists. Certainty grades: HIGH from tools, MEDIUM from repeated patterns, LOW from inference.
7. **Getting started — exact runnable commands** — clone/install/build/test/run commands copied from manifests, CI, or observed scripts.

### 4. Deep-read 2-3 real files

After the orientation, read actual source before claiming architecture.

Read, in priority order:
1. Primary entry point: structural entry point from codegraph/AST, package `bin`, Cargo `[[bin]]`, Go `cmd/*`, Python console script, or framework config.
2. Largest module by file count from the 3-level structure walk.
3. One representative test file.

If fewer exist, read what exists and state the degradation. Tie the files together with file paths and concrete calls/imports. Avoid "likely" architecture except where labeled `[INFERENCE]`.

### 5. Ask for the next move

Close the first turn with the `ask` tool. Use one axis, single-select, one Recommended option:

- `explore_area` — **Explore an area** (Recommended for first-time onboarding): pick a directory/package and read its central exports plus most-imported file.
- `trace_feature` — **Trace a feature**: ask for the feature name, locate its entry point, trace call/import flow, deep-read 2-3 key files.
- `first_change` — **Make a first change**: ask for desired change, map risk using hotspots/owners/tests, identify exact files to inspect before editing.
- `where_help` — **Where can I help?**: combine hotspots, test gaps, stale docs, low-owner areas, and small cleanup candidates into file-level recommendations.

If the `ask` tool is unavailable in the current harness, present the same four options as a numbered prompt and stop after the question.

## Anti-patterns

- **Raw JSON dump**: collection output is evidence, not user-facing text.
- **Filename architecture**: never explain flow before reading source.
- **Exhaustive tree spam**: annotate structure; do not paste a directory listing.
- **Command invention**: runnable commands come from manifests, CI, Makefile, or README. Otherwise mark `[INFERENCE]` and prefer no command.
- **Repo-health moralizing**: code health helps a newcomer steer. It is not a cleanup assignment unless the user chooses that path.
- **Cross-tool cache dependency**: no external analyzer binary or persistent intelligence cache. Recompute signals natively.

## Validation Gates

| Gate | Pass criteria | Blocking |
|---|---|---|
| Root resolved | Existing directory selected; depth is quick/normal/deep | Yes |
| Core collection | Manifest/README/structure/git/CI attempted with degradation noted | Yes |
| Native signals | Codegraph or AST/text fallback used for entry points and conventions | Yes |
| Repomix digest | MCP or CLI repomix attempted; failure recorded without blocking orientation | No |
| Seven sections | All applicable sections emitted in order; empty sections omitted only with reason | Yes |
| Deep read | At least one real source file read; target is 2-3 files | Yes |
| Commands grounded | Getting-started commands trace to manifest/CI/README/Makefile | Yes |
| Interaction | Ends with `ask` next-step options or numbered fallback prompt | Yes |

## Degradation

Use explicit certainty labels. `HIGH` means observed by tool output. `MEDIUM` means multiple independent weak signals. `LOW` means local inference required. Missing data is reported once at the affected section, not repeated throughout the tour.
