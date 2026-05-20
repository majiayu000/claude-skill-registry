---
name: codedocs
version: 0.2.0
description: >
  Use this skill when generating AI-agent-friendly documentation for a git repo or
  directory, answering questions about a codebase from existing docs, or incrementally
  updating documentation after code changes. Triggers on codedocs:generate, codedocs:ask,
  codedocs:update, "document this codebase", "generate docs for this repo", "what does
  this project do", "update the docs after my changes", or any task requiring structured
  codebase documentation that serves AI agents, developers, and new team members.
category: engineering
tags: [documentation, codebase, onboarding, architecture, ai-agent, code-understanding]
recommended_skills: [technical-writing, internal-docs, clean-code, developer-experience, open-source-management]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Codedocs

Codedocs generates structured, layered documentation for any git repository or code
directory - documentation designed to be consumed by AI agents first and human developers
second. Instead of flat READMEs that lose context, codedocs produces a `docs/` tree with
an architecture overview, per-module deep dives, cross-cutting pattern files, and a
manifest that tracks what has been documented and when. Once docs exist, the skill answers
questions from the docs (not by re-reading source code), and supports incremental updates
via targeted scope or git-diff detection.

---

## Activation Banner

**At the very start of every codedocs invocation**, before any other output, display this ASCII art banner:

```
 ██████╗ ██████╗ ██████╗ ███████╗██████╗  ██████╗  ██████╗███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔════╝
██║     ██║   ██║██║  ██║█████╗  ██║  ██║██║   ██║██║     ███████╗
██║     ██║   ██║██║  ██║██╔══╝  ██║  ██║██║   ██║██║     ╚════██║
╚██████╗╚██████╔╝██████╔╝███████╗██████╔╝╚██████╔╝╚██████╗███████║
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝╚══════╝
```

Follow the banner immediately with the active sub-command and target path, e.g.:
`codedocs:generate · src/ → docs/`

---

## When to use this skill

Trigger this skill when the user:
- Wants to generate documentation for a codebase, repo, or directory
- Asks "what does this project do" or "explain this codebase"
- Needs onboarding docs for new team members joining a project
- Wants AI-agent-readable documentation for a repo
- Asks a question about a codebase that already has codedocs output
- Needs to update existing docs after code changes or a new feature
- Wants to document only a specific module or subdirectory
- Asks to refresh docs based on recent git commits or a diff

Do NOT trigger this skill for:
- Writing standalone technical documents (RFCs, ADRs, runbooks) - use `internal-docs`
- API reference docs for external consumers - use `technical-writing`
- README creation for open-source packaging - use `open-source-management`

---

## Key principles

1. **Docs-first answers** - Once codedocs output exists, always answer questions from the
   docs before falling back to source code. The docs are the cached, structured knowledge
   layer. Only read source code when docs are missing, stale, or insufficient for the
   specific question.

2. **Language-agnostic detection** - Detect the tech stack from manifest files (package.json,
   Cargo.toml, go.mod, requirements.txt, pyproject.toml, composer.json, pom.xml, build.gradle,
   Gemfile, mix.exs, etc.) and directory conventions. Never assume a specific language.

3. **Modules map to code, patterns cut across** - Module docs correspond to distinct code
   directories or bounded contexts (auth, api, database). Pattern docs capture cross-cutting
   concerns (error handling, testing strategy, logging conventions) that span multiple modules.
   This split prevents duplication and matches how developers think about code.

4. **Manifest-driven incremental updates** - The `.codedocs.json` manifest tracks every
   documented module, its source path, and the git SHA at documentation time. Updates use
   this manifest to know what changed, what to re-scan, and what to skip.

5. **Output is configurable, structure is not** - The output directory (default `docs/`) is
   configurable. The internal structure (OVERVIEW.md, INDEX.md, .codedocs.json, modules/, patterns/)
   is fixed. Consistency across repos means any agent or developer knows where to look.

6. **Coverage is a first-class metric** - Documentation that covers 40% of a codebase is
   often worse than none - it gives a false sense of completeness. Always run coverage
   verification before presenting the plan. Target 70%+ for mid-size repos. Report coverage
   percentage in OVERVIEW.md and the manifest. See `references/coverage-strategy.md` for targets.

7. **Go deep, not just wide** - For large repos, top-level modules are just the starting point.
   Any module with 15+ source files must be analyzed for sub-modules. Scan recursively through
   the full directory tree - a huge repo should generate 30-80 doc files, not 8-12.

---

## Core concepts

**Output structure** - Codedocs always produces the same directory tree. OVERVIEW.md is the
entry point covering architecture, tech stack, project structure tree, and module map.
GETTING_STARTED.md is the authoritative local development guide with every runnable command
in the repo. INDEX.md is the file-to-module lookup table. The modules/ directory contains one
markdown file per major code module (with optional sub-module directories for large modules).
The patterns/ directory contains cross-cutting concern docs. The `.codedocs.json` manifest
tracks metadata, coverage stats, and SHAs for incremental updates. See
`references/output-structure.md` for the full spec.

**Four sub-commands** - The skill exposes four operations: `generate` for full or scoped
documentation creation, `ask` for docs-first Q&A, `update` for incremental refresh, and
`status` for coverage reporting. Each has its own workflow and parameters. See the common
tasks below and the corresponding reference files for detailed workflows.

**Sub-modules** - When a module directory has 15+ source files with distinct internal groupings,
it is split into sub-modules. The parent module doc becomes an index; sub-module docs live at
`modules/<parent>/<child>.md`. This keeps docs focused and prevents any single file from
becoming an unreadably long catch-all.

**Coverage verification** - Before presenting the generation plan, codedocs computes what
percentage of source files are covered by the proposed module set. If below target, it
expands the scan to find additional modules. Coverage is tracked in the manifest and reported
in OVERVIEW.md. See `references/coverage-strategy.md`.

**Discovery phase** - Before writing any docs, the generate command runs a discovery phase:
scan the directory tree, identify the tech stack from manifest files, map module boundaries
from directory structure and import graphs, and detect cross-cutting patterns from shared
utilities and conventions. This phase produces the plan that drives doc generation.

**Staleness detection** - The update command compares the current git SHA against the SHA
recorded in `.codedocs.json` for each module. Modules with changed files since last
documentation are flagged as stale. The `--diff` flag uses `git diff` to identify exactly
which files changed, enabling surgical updates to only the affected module docs.

---

## Common tasks

### 1. Generate full codebase documentation

**Command:** `codedocs:generate [path] [--output docs/]`

Workflow:
1. **Discover** - Scan the target path (default: repo root). Identify language/framework
   from manifest files. Map directory structure to candidate modules. Detect entry points
   (main files, index files, route definitions, CLI entry points).
2. **Plan** - Present the user with a proposed doc plan: list of modules to document,
   patterns detected, estimated scope, and coverage percentage. Confirm before proceeding if the plan is large or ambiguous.
3. **Write OVERVIEW.md** - Architecture summary, tech stack, annotated project structure
   tree, entry points, key concepts, and module map with one-line descriptions.
4. **Write GETTING_STARTED.md** - Full local development guide: prerequisites, installation,
   environment setup, dev server, test commands, build commands, lint/format, database
   workflow, common dev tasks, and how to reproduce CI locally. Sourced from package.json
   scripts, Makefile targets, CI config, and any existing README setup sections.
5. **Write module docs** - For each module: purpose, public API/exports, internal structure,
   dependencies (what it imports), dependents (what imports it), and key implementation notes.
6. **Write pattern docs** - For each cross-cutting pattern: description, where it appears,
   conventions to follow, and examples from the codebase.
7. **Write manifest** - Create `.codedocs.json` with module list, source paths, git SHA,
   generation timestamp, coverage stats, and config. See `references/output-structure.md`.

See `references/generate-workflow.md` for the complete discovery heuristics, module
boundary detection logic, and OVERVIEW.md template.

### 2. Ask a question about the codebase

**Command:** `codedocs:ask "<question>"`

Workflow:
1. **Check for docs** - Look for `.codedocs.json` in the output directory. If missing,
   suggest running `codedocs:generate` first.
2. **Route the question** - Determine which doc file(s) are relevant. Architecture questions
   go to OVERVIEW.md. Module-specific questions go to the relevant module doc. Cross-cutting
   questions go to pattern docs.
3. **Read docs first** - Load the relevant doc file(s) and attempt to answer from them.
4. **Fall back to source** - If the docs don't contain enough detail, read the relevant
   source files. Flag in the response: "Note: this answer required reading source code -
   consider running `codedocs:update` to capture this in the docs."
5. **Cite sources** - Always cite which doc file or source file the answer came from.

See `references/ask-workflow.md` for the question routing logic and fallback strategy.

### 3. Update docs incrementally (targeted scope)

**Command:** `codedocs:update --scope path/to/module`

Workflow:
1. **Read manifest** - Load `.codedocs.json` to find the existing module mapping.
2. **Re-scan the scoped path** - Run the discovery phase only on the specified path.
3. **Diff against existing docs** - Compare the new discovery against the current module
   doc. Identify new exports, removed functions, changed dependencies.
4. **Update the module doc** - Rewrite only the sections that changed.
5. **Update OVERVIEW.md** - If the module's one-line description or dependency graph changed,
   update the module map in OVERVIEW.md.
6. **Update manifest** - Bump the git SHA and timestamp for the updated module.

### 4. Update docs from git diff

**Command:** `codedocs:update --diff [base..head]`

Workflow:
1. **Get changed files** - Run `git diff --name-only base..head` (default: last documented
   SHA from manifest to HEAD).
2. **Map files to modules** - Using the manifest's source path mappings, determine which
   documented modules contain changed files.
3. **Re-generate affected modules** - For each affected module, re-run the module doc
   generation workflow.
4. **Detect new modules** - If changed files are in directories not yet documented, flag
   them as new module candidates and prompt the user.
5. **Update manifest** - Bump SHAs for all updated modules.

See `references/update-workflow.md` for the diff detection logic and new module handling.

### 5. Generate docs for a specific subdirectory

**Command:** `codedocs:generate path/to/subdir [--output path/to/subdir/docs/]`

Same workflow as full generation but scoped to a subdirectory. The output defaults to a
`docs/` folder inside the specified path. Useful for monorepos where each package needs
its own documentation.

### 6. Check documentation coverage

**Command:** `codedocs:status`

Workflow:
1. **Read manifest** - Load `.codedocs.json`. If missing, suggest running `codedocs:generate`.
2. **Compute coverage** - Count total source files in the repo vs files covered by documented
   modules.
3. **Detect staleness** - For each module, compare the manifest SHA against the latest git
   commit SHA on that module's source path.
4. **Find gaps** - List directories in the repo not covered by any module doc.
5. **Report** - Print a structured status report: coverage percentage, stale modules, gap
   directories, and recommendations.

See `references/coverage-strategy.md` for coverage targets, the status report format, and
strategies for improving coverage on large repos.

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Re-reading source code when docs exist | Wastes context window and time; docs are the structured cache | Always check for `.codedocs.json` first; read docs before source |
| Documenting every file individually | Creates noise; most files are internal implementation details | Document at the module level; only call out key files within a module |
| Skipping the discovery/plan phase | Jumping straight to writing produces unstructured, incomplete docs | Always run discovery first; present the plan to the user for approval |
| Hardcoding language assumptions | Breaks on polyglot repos or unfamiliar stacks | Detect from manifest files; handle multiple languages in one repo |
| Ignoring the manifest on updates | Leads to full re-generation when only one module changed | Always read `.codedocs.json` to scope updates to changed modules only |
| Mixing module docs and pattern docs | Cross-cutting concerns documented in one module become invisible | Use the patterns/ directory for anything that spans 2+ modules |
| Writing docs without git SHA tracking | Makes incremental updates impossible; no way to know what's stale | Always populate the manifest with per-module git SHAs |
| Stopping at top-level directories | A huge repo generates only 8-12 files; most of the codebase is invisible | Run the full recursive census (Step 3), verify coverage, and scan deeper |
| One flat doc for a 50-file module | The doc is too long to be useful; every question returns the same giant file | Split modules with 15+ files into sub-modules (`modules/<parent>/<child>.md`) |
| Not checking coverage before presenting plan | Low-coverage plans look complete but leave most of the repo undocumented | Always run Step 6 (coverage verification) before showing the plan |
| Skipping INDEX.md | AI agents can't map a specific file to its module doc | Always generate INDEX.md as part of the output |
| Skipping GETTING_STARTED.md | Developers and agents can't run the project without hunting through package.json and README | Always generate GETTING_STARTED.md; source commands from scripts, Makefile, and CI config |
| Copying README verbatim into GETTING_STARTED.md | READMEs are often incomplete or outdated; the guide adds no value | Extract commands from README but expand with context, fill gaps, and verify against actual scripts |

---

## Gotchas

1. **Manifest SHA drift causes phantom staleness** - If the repo has uncommitted changes when `codedocs:generate` runs, the recorded git SHA doesn't match the working tree. Subsequent `codedocs:update` runs see all files as stale and attempt full re-generation. Run codedocs against a clean working tree or committed state where possible.

2. **Coverage counts source files, not lines** - A large 2,000-line file and a small 50-line config file each count as one source file for coverage. A 70% coverage score can hide an undocumented core module if it happens to be split into many small files. Review the gap directory list in `codedocs:status` rather than trusting the percentage alone.

3. **Sub-module splitting creates orphaned parent docs** - When a module with 15+ files is split into sub-modules, the parent `modules/<name>.md` should become an index pointing to sub-modules. If you create `modules/api/routes.md` and `modules/api/middleware.md` but leave the original `modules/api.md` intact unchanged, agents get conflicting information from two sources about the same code.

4. **Polyglot repos confuse module boundary detection** - A repo with both a Python backend and a TypeScript frontend may have overlapping directory names (`utils/`, `types/`, `config/`) at different levels. The discovery phase can conflate these into one module. Explicitly verify module boundaries during the plan phase for monorepos or polyglot projects.

5. **GETTING_STARTED.md sourced only from README** - READMEs are often incomplete or outdated. Commands listed in `package.json` scripts, `Makefile` targets, and CI config files frequently include critical developer workflows not mentioned in the README. Always cross-check all three sources when generating GETTING_STARTED.md.

---

## References

For detailed workflows and schemas, read the relevant file from `references/`:

- `references/generate-workflow.md` - Complete discovery heuristics, recursive census,
  multi-level module boundary detection, sub-module splitting, coverage verification,
  tech stack identification, and all output templates (OVERVIEW.md, module doc, pattern doc,
  INDEX.md). Load when running codedocs:generate.
- `references/ask-workflow.md` - Question routing logic, doc-first resolution strategy,
  source code fallback rules, and citation format. Load when running codedocs:ask.
- `references/update-workflow.md` - Diff detection logic, manifest-driven scoping, new
  module detection, and OVERVIEW.md sync rules. Load when running codedocs:update.
- `references/output-structure.md` - Complete `.codedocs.json` manifest schema (v1.1 with
  coverage stats and sub-modules), directory layout spec including sub-module directories
  and INDEX.md, and file format guidelines. Load when creating or validating output.
- `references/coverage-strategy.md` - Coverage targets by repo size, the codedocs:status
  report format, prioritization framework for large repos, and coverage improvement
  strategies. Load when running codedocs:status or when coverage is below target.

Only load a references file if the current task requires deep detail on that topic.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
