---
name: data-structure-protocol
description: >-
  Build and navigate DSP (Data Structure Protocol) — graph-based long-term structural memory of codebases for LLM agents.
  Stores entities (modules, functions), their dependencies (imports), public API (shared/exports), and reasons for every connection.
  Use when: (1) project has a .dsp/ directory, (2) user asks to set up DSP or bootstrap project structure,
  (3) creating/modifying/deleting code files in a DSP-tracked project, (4) navigating project structure, understanding dependencies,
  or finding modules, (5) user mentions DSP, dsp-cli, .dsp, or structure mapping.
---

# Data Structure Protocol (DSP)

DSP builds a dependency graph of project entities in a `.dsp/` directory. Each entity (module, function, external dependency) gets a UID, description, import list, and export index. The graph answers: what exists, why it exists, what depends on what, and who uses what.

**DSP is NOT documentation for humans or AST dump.** It captures _meaning_ (purpose), _boundaries_ (imports/exports), and _reasons for connections_ (why).

## Agent Prompt

Embed this context when working on a DSP-tracked project:

> **This project uses DSP (Data Structure Protocol).**
> The `.dsp/` directory is the entity graph of this project: modules, functions, dependencies, public API. It is your long-term memory of the code structure.
>
> **Core rules:**
>
> 1. **Before changing code** — find affected entities via `dsp-cli search`, `find-by-source`, or `read-toc`. Read their `description` and `imports` to understand context.
> 2. **When creating a file/module** — call `dsp-cli create-object`. For each exported function — `create-function` (with `--owner`). Register exports via `create-shared`.
> 3. **When adding an import** — call `dsp-cli add-import` with a brief `why`. For external dependencies — first `create-object --kind external` if the entity doesn't exist yet.
> 4. **When removing import / export / file** — call `remove-import`, `remove-shared`, `remove-entity` respectively. Cascade cleanup is automatic.
> 5. **When renaming/moving a file** — call `move-entity`. UID does not change.
> 6. **Don't touch DSP** if only internal implementation changed without affecting purpose or dependencies.
> 7. **Bootstrap** — if `.dsp/` is empty, traverse the project from root entrypoint via DFS on imports, documenting every file.
>
> **Key commands:**
> ```
> dsp-cli init
> dsp-cli create-object <source> <purpose> [--kind external] [--toc ROOT_UID]
> dsp-cli create-function <source> <purpose> [--owner UID] [--toc ROOT_UID]
> dsp-cli create-shared <exporter_uid> <shared_uid> [<shared_uid> ...]
> dsp-cli add-import <importer_uid> <imported_uid> <why> [--exporter UID]
> dsp-cli remove-import <importer_uid> <imported_uid> [--exporter UID]
> dsp-cli remove-shared <exporter_uid> <shared_uid>
> dsp-cli remove-entity <uid>
> dsp-cli move-entity <uid> <new_source>
> dsp-cli update-description <uid> [--source S] [--purpose P] [--kind K]
> dsp-cli get-entity <uid>
> dsp-cli get-children <uid> [--depth N]
> dsp-cli get-parents <uid> [--depth N]
> dsp-cli search <query>
> dsp-cli find-by-source <path>
> dsp-cli read-toc [--toc ROOT_UID]
> dsp-cli get-stats
> ```

## Using the CLI

The script is at `scripts/dsp-cli.py` relative to this skill directory.

```
python <skill-path>/scripts/dsp-cli.py [--root <project-root>] <command> [args]
```

`--root` defaults to current working directory. All paths in arguments are repo-relative.

## Core Concepts

- **Code = graph.** Nodes are Objects and Functions. Edges are `imports` and `shared/exports`.
- **Identity by UID, not file path.** Path is an attribute; renames/moves don't change UID.
- **"Shared" creates an entity.** If something becomes public (exported), it gets its own UID.
- **Import tracks both "from where" and "what".** One code import may create two DSP links: to the module and to the specific shared entity.
- **Full import coverage.** Every imported file/asset must be an Object in `.dsp` — code, images, styles, configs, everything.
- **`why` lives next to the imported entity** in its `exports/` directory (reverse index).
- **Start from roots.** Each root entrypoint has its own TOC file.
- **External deps — record only.** `kind: external`, no deep dive into `node_modules`/`site-packages`/etc. But `exports index` works — shows who imports it.

## UID Format

- Objects: `obj-<8 hex>` (e.g., `obj-a1b2c3d4`)
- Functions: `func-<8 hex>` (e.g., `func-7f3a9c12`)

UID marker in source code — comment `@dsp <uid>` before declaration:

```js
// @dsp func-7f3a9c12
export function calculateTotal(items) { ... }
```

```python
# @dsp obj-e5f6g7h8
class UserService:
```

## Workflows

### Setting Up DSP

1. Run `dsp-cli init` to create `.dsp/` directory.
2. Identify root entrypoint(s) — `package.json` main, framework entry, etc.
3. Run bootstrap (DFS from root). See [bootstrap.md](references/bootstrap.md).

### Creating Entities (when writing new code)

1. Create module: `dsp-cli create-object <path> <purpose>`
2. Create functions: `dsp-cli create-function <path>#<symbol> <purpose> --owner <module-uid>`
3. Register exports: `dsp-cli create-shared <module-uid> <func-uid> [<func-uid> ...]`
4. Register imports: `dsp-cli add-import <this-uid> <imported-uid> <why> [--exporter <module-uid>]`
5. External deps: `dsp-cli create-object <package-name> <purpose> --kind external`

### Navigating the Graph (when reading/understanding code)

- **Find entity by file**: `dsp-cli find-by-source <path>`
- **Search by keyword**: `dsp-cli search <query>`
- **Read TOC**: `dsp-cli read-toc` → get all UIDs, then `get-entity` for details
- **Dependency tree down**: `dsp-cli get-children <uid> --depth N`
- **Dependency tree up**: `dsp-cli get-parents <uid> --depth N`
- **Impact analysis**: `dsp-cli get-recipients <uid>` — who depends on this entity
- **Path between entities**: `dsp-cli get-path <from> <to>`

### Updating (when modifying code)

- Purpose changed: `dsp-cli update-description <uid> --purpose <new>`
- File moved: `dsp-cli move-entity <uid> <new-path>`
- Import reason changed: `dsp-cli update-import-why <importer> <imported> <new-why>`

### Deleting (when removing code)

- Import removed: `dsp-cli remove-import <importer> <imported> [--exporter UID]`
- Export removed: `dsp-cli remove-shared <exporter> <shared>`
- File/module deleted: `dsp-cli remove-entity <uid>` (cascading cleanup)

### Diagnostics

- `dsp-cli detect-cycles` — circular dependencies
- `dsp-cli get-orphans` — unused entities
- `dsp-cli get-stats` — project graph overview

## When to Update DSP

| Code Change | DSP Action |
|---|---|
| New file/module | `create-object` + `create-function` + `create-shared` + `add-import` |
| New import added | `add-import` (+ `create-object --kind external` if new external dep) |
| Import removed | `remove-import` |
| Export added | `create-shared` (+ `create-function` if new function) |
| Export removed | `remove-shared` |
| File renamed/moved | `move-entity` |
| File deleted | `remove-entity` |
| Purpose changed | `update-description` |
| Internal-only change | **No DSP update needed** |

## References

- **[Storage format](references/storage-format.md)** — `.dsp/` directory structure, file formats, TOC
- **[Bootstrap procedure](references/bootstrap.md)** — initial project markup (DFS algorithm)
- **[Operations reference](references/operations.md)** — detailed semantics of all operations with import examples
