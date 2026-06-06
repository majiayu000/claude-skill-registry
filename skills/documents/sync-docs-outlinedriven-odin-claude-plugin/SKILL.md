---
name: sync-docs
description: Detect documentation-vs-code drift from a git diff, apply only safe documentation corrections, and report all unsafe stale-reference issues with file:line evidence. Use when "sync docs", "update changelog", "find outdated docs", "stale code examples", "doc drift", or "docs out of date".
metadata:
  short-description: Diff-driven docs drift correction
---

# Sync Docs — correct documentation against code reality

`sync-docs` is a `correct` op-cell: restore the invariant that public docs, examples, versions, and changelog entries describe the current code. It starts from a diff, maps the changed code to coupled Markdown, applies only the safe subset, and flags every semantic drift item with evidence.

Safe means text substitution with a mechanically known target: **version-number bump** and **CHANGELOG `## [Unreleased]` entry**. Everything else is flag-only until a human or implementer verifies the intended prose change.

## When to Apply / NOT

Apply when a branch changes public APIs, imports, CLI flags, config names, package versions, exported symbols, examples, or user-visible behavior and docs may lag.

NOT apply for generated documentation refreshes, mass prose rewrites, API design review, release-note authorship from scratch, or docs whose source of truth is intentionally external. For those, report drift signals but do not edit.

## Inputs

- **Mode**: `report` (default) or `apply`. `apply` still edits only safe-fix issues.
- **Scope**:
  - `recent`: changed files from the current branch or last few commits.
  - `before-pr`: branch diff against the PR base; use before publishing.
  - `all`: scan all tracked code and docs; slower, useful after migrations.
- **Base**: explicit base ref is preferred. If absent, resolve the default branch, then fall back to `HEAD~5` for `recent`.

## Workflow

1. **Pick scope and base.** Refuse ambiguous review scope when the user expects PR readiness. Use these commands as the runnable recipe:

   ```bash
   # before-pr: whole branch against the remote default branch
   remote_head=$(git symbolic-ref --short refs/remotes/origin/HEAD || printf origin/main)
   base=${remote_head#origin/}
   git diff --name-status "origin/$base"...HEAD

   # recent: if the default-branch diff fails, run the fallback explicitly
   git diff --name-status HEAD~5..HEAD

   # all: tracked docs and code inventory, not a behavioral diff
   git ls-files
   ```

   In ODIN tool mode, use `bash` only for the `git` commands; use `find`, `search`, `read`, `lsp`, `ast_grep`, and `edit` for everything else.

2. **Compute changed code.** Keep only source/config/package files that can change docs. Exclude pure docs, vendored/generated paths, lockfiles unless version docs mention package manager output, and deleted files that were never public.

   Output shape:

   ```json
   {"status":"M|A|D|R","oldPath":"src/old.ts","path":"src/new.ts","basename":"client","modulePath":"src/new","kind":"source|manifest|config|cli"}
   ```

3. **Extract coupling terms.** For each changed code file, derive:

   - filename stem: `client`, `auth-server`.
   - full path and path without extension: `src/auth/client.ts`, `src/auth/client`.
   - import strings from the diff: `from "pkg/auth"`, `require("pkg/auth")`, dynamic imports.
   - exported/public symbols from `codegraph_search` / `codegraph_explore` when indexed.
   - fallback symbols from language syntax:

     ```bash
     ast-grep --pattern 'export function $NAME($$$)' --lang ts <file>
     ast-grep --pattern 'export class $NAME { $$$ }' --lang ts <file>
     ast-grep --pattern 'pub fn $NAME($$$)' --lang rust <file>
     git grep -nE '^(export |pub |def |class |func )' -- <file>
     ```

4. **Discover related docs.** Search only live doc surfaces first: `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `*.md` at repo root. For each coupling term, search docs and record `doc`, `line`, `term`, `referenceType` (`filename`, `full-path`, `import`, `symbol`, `url-path`, `version`). Default ignore list lives in `references/doc-issues.md`.

   Runnable fallback:

   ```bash
   git grep -n -- '*.md' README.md CHANGELOG.md docs/ -- '<term>'
   git grep -nE 'from ["'"''][^"'"'']+["'"'']|require\(["'"''][^"'"'']+["'"'']\)' -- '*.md'
   ```

   ODIN tool equivalent: `search` each escaped term across `README.md`, `CHANGELOG.md`, `docs/**/*.md`, then `read` the surrounding lines.

5. **Classify issues.** Use the taxonomy in `references/doc-issues.md`. Preserve certainty:

   - **HIGH**: manifest version mismatch with exact current version; deleted/renamed public export still documented with symbol proof; changed import path in fenced example where the old path no longer resolves.
   - **MEDIUM**: stale code example that mentions a changed file/symbol but needs semantic review; undocumented public export after entry-point/internal filtering; docs describing codegraph-reported dead code.
   - **LOW**: doc-drift from zero code-coupling or weak filename-only coupling; broad stale prose suspicion.

6. **Apply safe fixes only.** In `apply` mode:

   - **Version bump**: replace stale semver strings in docs with the manifest version when the line clearly labels a version (`version`, package badge, install snippet with `@x.y.z`). Avoid broad numeric replacement.
   - **CHANGELOG `## [Unreleased]` entry**: insert a minimal bullet under the existing section, or create the section at the top if absent. Use commit messages or changed-file summaries; do not invent product claims.

   Do not auto-edit removed exports, import paths, examples, undocumented exports, dead-code docs, or doc-drift prose. Those require intent.

7. **Flag the rest.** Emit a compact report sorted by severity, then file path:

   ```text
   HIGH docs/api.md:42 removed-export `createClient` no current public symbol; changed in src/client.ts
   MEDIUM README.md:88 stale-code-example imports old path `pkg/client`; verify replacement `pkg/auth/client`
   LOW docs/legacy.md:? doc-drift zero code-coupling; no live filename/import/symbol references
   ```

8. **Return fix ledger.** For every edit, record `file`, `line`, `type`, `before`, `after`, and evidence source. For every flag-only item, record `reasonFlagOnly`.

## Native Detection Recipes

### Code graph first

When the repo is indexed, use the codegraph MCP for symbol truth:

- `codegraph_search`: locate changed public symbols by name.
- `codegraph_callers` / `codegraph_callees`: determine whether docs describe dead wrappers or removed API surfaces.
- `codegraph_impact`: judge blast radius before calling an export undocumented.
- `codegraph_files`: confirm entry points and module layout.

Fallback when not indexed:

```bash
git grep -nE 'export (function|class|const|let|var)|export \{|module\.exports|pub (fn|struct|enum|trait)|^def |^class ' -- ':!node_modules' ':!generated'
ast-grep --pattern 'import $X from $Y' --lang ts src
ast-grep --pattern 'from $M import $$$N' --lang python .
```

### Manifest versions

Read manifests directly and compare against doc mentions:

- JavaScript/TypeScript: `package.json` `version`.
- Rust: `Cargo.toml` `package.version`.
- Python: `pyproject.toml` `project.version`, fallback `setup.cfg` / `setup.py` only as MEDIUM.
- Go: module version is usually tag-derived; do not auto-fix unless a manifest line gives an exact version.

Search docs for labeled semver:

```bash
git grep -nE '(version|v|@)[[:space:]:="'"'']*[0-9]+\.[0-9]+\.[0-9]+' -- '*.md'
```

### CHANGELOG evidence

Use commits only as evidence, not as prose authority:

```bash
git --no-pager log --oneline --no-merges "origin/$base"..HEAD
git diff --name-only "origin/$base"...HEAD
```

If `CHANGELOG.md` has no `## [Unreleased]`, create one immediately below the title. If it exists, insert under an appropriate subsection only when the subsection already exists; otherwise add a plain bullet under `## [Unreleased]`.

## Anti-patterns

- **Regex-only confidence on public API removal**: require codegraph, LSP, ast-grep, or exact diff evidence before HIGH.
- **Mass replacing version-looking numbers**: examples, ports, years, protocol versions, and dates are not package versions.
- **Fixing examples by guess**: changed import path is usually flag-only unless the diff explicitly contains a one-to-one rename.
- **Treating CHANGELOG as drift**: append-only history has intentionally low code coupling.
- **Reporting generated/versioned docs as stale**: they are snapshots unless explicitly in scope.
- **Inventing release notes**: changelog bullets must cite commits or changed files.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Scope resolved | Base ref, scope, changed files, and ignored paths are listed | Stop with exact missing base or empty diff |
| Evidence attached | Every issue has `file:line` when a line exists, plus the changed code source | Do not report line-specific claims without a read/search hit |
| Safe-fix boundary | Only version bump and CHANGELOG Unreleased entry are in `fixes` | Reclassify everything else as flag-only |
| Version fix exactness | Replacement value comes from manifest; matched line is version-labeled | Do not edit |
| Changelog restraint | Entry cites commit/file evidence and lands under `## [Unreleased]` | Do not edit |
| Post-edit check | Re-read edited ranges; no unrelated prose changed | Revert the edit and report flag-only |
| Residual flags | All non-safe issues remain in the report with reason | Completion blocked until listed |

## Output Contract

Return both machine-readable and human-readable surfaces when possible:

```json
{
  "opCell": "correct",
  "scope": "recent|all|before-pr",
  "base": "origin/main",
  "changedCode": [{"status":"M","path":"src/client.ts"}],
  "relatedDocs": [{"doc":"README.md","line":42,"term":"createClient","referenceType":"symbol"}],
  "fixesApplied": [{"type":"version-mismatch","file":"README.md","line":12,"before":"1.2.0","after":"1.3.0"}],
  "flagged": [{"type":"stale-code-example","severity":"MEDIUM","file":"docs/api.md","line":88,"reasonFlagOnly":"example intent cannot be inferred safely"}]
}
```

Completion means the safe fixes are applied or explicitly unavailable, and all remaining drift is flagged. A clean report with no edits is valid only after the diff-to-doc mapping and taxonomy pass ran.