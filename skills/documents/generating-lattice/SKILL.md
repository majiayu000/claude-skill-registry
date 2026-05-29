---
name: generating-lattice
description: >-
  Generate and maintain lat.md/ knowledge graphs with bidirectional source code
  anchoring. Docs link to code via [[src/file#symbol]] wiki links; code links
  back to docs via @lat: comments. lat check validates both directions, catching
  drift when either side changes. Use when user says "lat.md", "lattice",
  "knowledge graph", "document this codebase", "add back-links", or wants
  cross-referenced architecture docs anchored to source code symbols.
metadata:
  version: 0.3.0
---

# Generating Lattice

Generate and maintain `lat.md/` knowledge graphs — structured, cross-referenced
markdown anchored to source code symbols. The output is validated by the `lat`
CLI, which catches documentation drift whenever code or docs change.

**The core mechanism is bidirectional linking:**

- **Top-down** (docs → code): `[[src/auth.js#getValidToken]]` wiki links in
  `lat.md/` files point to specific symbols in source. When a symbol is renamed
  or deleted, `lat check` catches the broken link.
- **Bottom-up** (code → docs): `// @lat: [[auth#Token Refresh]]` comments in
  source point back to the concept they implement. When a section is renamed or
  removed, `lat check` catches the dangling reference.

Without both directions, the lattice is a static essay that drifts silently.
With both, `lat check` enforces consistency.

**Dependency:** Requires **mapping-codebases** skill. The structural maps
(`_MAP.md` files) are the input that makes LLM-assisted authoring
token-efficient — read maps to understand API surfaces, then selectively read
source files only where design rationale lives.

## Installation

```bash
npm install -g lat.md
lat --version  # verify (requires Node.js 22+)
```

The `lat` CLI provides `lat check` (validation), `lat search` (semantic
search), `lat section` (browsing), `lat refs` (reference lookup), and `lat mcp`
(agent integration).

## Generation Pipeline

### Phase 1: Structural Scan

Ensure `_MAP.md` files exist. Generate them if missing:

```bash
# Install mapping-codebases dependencies
uv venv /home/claude/.venv
uv pip install tree-sitter-language-pack --python /home/claude/.venv/bin/python

# Generate maps
/home/claude/.venv/bin/python /mnt/skills/user/mapping-codebases/scripts/codemap.py /path/to/repo \
  --skip tests,.github,node_modules,vendor
```

Read the root `_MAP.md` first for high-level orientation, then drill into
subdirectory maps. The maps are the symbol inventory — they tell you what exists
and where, so you can write source code links without reading every file.

### Phase 2: Selective Source Reading

Maps reveal the API surface (exports, signatures, line numbers) without reading
full files. Read source selectively to understand design rationale:

**Read fully:** Files with complex algorithms, business logic, configuration
constants, data schemas. The maps identify these by export density and file
size.

**Read partially:** Header comments and constant blocks in large files.

**Skip:** Files where the map signature tells the full story (thin wrappers,
simple CRUD, format utilities).

### Phase 3: Generate Anchored Sections

Create `lat.md/` directory and generate markdown files. **Every section must be
anchored to source code symbols** — this is what makes `lat check` catch drift.

#### Section Structure Rules

- Every section MUST have a leading paragraph ≤250 characters (excluding
  `[[wiki link]]` content). This is the section's identity in search results.
- `lat check` validates this rule.

```markdown
# Good Section

Brief overview anchored to [[src/auth.js#refreshToken]] and [[src/api.js#fetchWithRetry]].

More detail can follow in subsequent paragraphs.
```

#### Source Code Links (the top-down anchors)

Use `[[src/path/file.ext#symbolName]]` wiki links to anchor documentation to
specific symbols. Supported extensions: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`,
`.rs`, `.go`, `.c`, `.h`.

```markdown
## Token Refresh

OAuth token lifecycle managed by [[src/auth.js#getValidToken]] with automatic
refresh via [[src/auth.js#refreshToken]]. The refresh window
([[src/auth.js#REFRESH_THRESHOLD_MS]]) triggers proactive renewal before expiry.
```

**Symbol granularity matters.** Link to the specific function, class, constant,
or method — not just the file. `[[src/auth.js#refreshToken]]` is useful;
`[[src/auth.js]]` tells you nothing that the filename didn't already say.

For class methods: `[[src/server.ts#App#listen]]`. For Rust impl methods:
`[[src/lib.rs#Greeter#greet]]`. For Python: `[[lib/utils.py#parse_args]]`.

#### Section-to-Section Links

Use `[[file#Section#Subsection]]` or short form `[[file#Section]]` when the
file stem is unique:

```markdown
The sync pipeline ([[data#Sync Pipeline]]) uses the same token refresh
mechanism described in [[auth#Token Refresh]].
```

#### Conceptual Grouping

Organize by domain concept, not file structure. A `data.md` file might reference
`db.js`, `sync.js`, and `demo.js` because they're all part of the data layer.
The `_MAP.md` files already provide file-level structure; `lat.md/` adds the
semantic layer explaining WHY things connect.

#### Index File

`lat.md/lat.md` must contain a bullet list of all files with one-sentence
descriptions using wiki links. `lat check --index` validates completeness:

```markdown
- [[architecture]] — System design, OAuth flow, routing, signals
- [[data]] — IndexedDB schema, sync pipeline, demo mode
- [[awards]] — Award computation engine, data quality rules
```

Subdirectories need their own index: `lat.md/api/api.md`.

### Phase 4: Add Back-Links in Source Code

Add `// @lat:` or `# @lat:` comments in source code pointing back to `lat.md/`
sections. **This is not optional** — back-links are what make `lat check`
detect when source code changes break documentation.

Run the back-link helper to identify where annotations are needed:

```bash
python3 SKILL_DIR/scripts/suggest_backlinks.py /path/to/repo
```

This parses all `[[src/...]]` wiki links from `lat.md/` files, looks up
referenced symbols in `_MAP.md` files for O(1) line number resolution, and
suggests `@lat:` comment placements. Requires `_MAP.md` files from Phase 1.

Comment syntax by language:
- JS/TS/Rust/Go/C: `// @lat: [[section#Subsection]]`
- Python: `# @lat: [[section#Subsection]]`

Place one `@lat:` comment per section reference, at the relevant code location —
not at the top of the file:

```javascript
// @lat: [[auth#Token Refresh]]
async function refreshToken(token) { ... }
```

To auto-apply suggestions (review the output first):

```bash
python3 SKILL_DIR/scripts/suggest_backlinks.py /path/to/repo --apply
```

### Phase 4b: Annotate Maps with Lattice Cross-References

After backlinks exist in source, annotate `_MAP.md` files so someone browsing
a code map can find the lat.md section that explains WHY a module is designed
the way it is:

```bash
python3 SKILL_DIR/scripts/annotate_maps.py /path/to/repo
```

This scans `@lat:` comments in source and adds `> Documented in:` lines to
`_MAP.md` file headers. Idempotent — safe to re-run after regenerating maps.

Example output in `_MAP.md`:
```markdown
### auth.js
> Documented in: [[auth#Token Refresh]], [[auth#Server]]
> Imports: `express`
- **refreshToken** (f) `(token)` :15
```

#### require-code-mention for Critical Sections

For sections where bidirectional traceability is essential (test specs,
invariants, key business rules), add frontmatter:

```yaml
---
lat:
  require-code-mention: true
---
```

This makes `lat check` fail if ANY leaf section in the file lacks a
corresponding `@lat:` comment in the codebase. Use for test spec files where
every test must trace to its specification.

### Phase 5: Validate

```bash
cd /path/to/repo
lat check
```

This runs ALL checks:
- **md** — every `[[wiki link]]` in `lat.md/` resolves to a real section or
  source symbol
- **code-refs** — every `@lat:` comment in source points to a real section; and
  every leaf section in `require-code-mention` files is referenced by code
- **sections** — every section has a leading paragraph ≤250 chars
- **index** — every directory in `lat.md/` has a complete index file

**All four must pass.** Fix errors iteratively until `lat check` is clean.

### Phase 6: Agent Integration

Set up files that make coding agents maintain the lattice automatically.

**Cache exclusion** — create `lat.md/.gitignore`:
```
.cache/
```

**Agent instructions** — append to `CLAUDE.md` (or `AGENTS.md`) using markers:

```markdown
%% lat:begin %%
# Before starting work

- Run `lat search` to find sections relevant to your task.
- Run `lat expand` on user prompts to expand any `[[refs]]`.

# Post-task checklist (REQUIRED — do not skip)

After EVERY task, before responding to the user:

- [ ] Update `lat.md/` if you changed functionality, architecture, or behavior
- [ ] Run `lat check` — all wiki links and code refs must pass
%% lat:end %%
```

**For full agent integration** (hooks that auto-inject search results and block
completion when `lat check` fails), run `lat init` interactively. This sets up
agent hooks in `.claude/settings.json`, `.cursor/hooks.json`, etc. The hooks
require absolute paths to the `lat` binary, which is machine-local.

## Drift Prevention: How It Works

The lattice stays in sync because changes to either side break `lat check`:

| What changed | What breaks | How lat check catches it |
|---|---|---|
| Symbol renamed in source | `[[src/file#oldName]]` wiki links in lat.md/ | `lat check --md` reports broken source ref |
| Symbol deleted | Same as above | Same — dead source link |
| Section renamed in lat.md/ | `@lat: [[old#Section]]` comments in source | `lat check --code-refs` reports dangling ref |
| Section deleted | Same as above | Same — orphaned code ref |
| New code added without docs | No back-link for new functions | Manual review (or `require-code-mention` enforcement) |
| New docs without code anchors | Sections with no `[[src/...]]` links | Manual review — but this is the failure to prevent |

**The critical gap:** new code without docs and new docs without anchors are
NOT caught automatically unless `require-code-mention` is set. The agent
integration hooks (Phase 6) address this by reminding agents to update lat.md/
after every task and running `lat check` before completion.

## Quality Criteria

A good generated lattice:
- **Passes `lat check` on all four checks** — md, code-refs, sections, index
- **Has dense source code links** — most sections reference specific symbols
  via `[[src/...#symbol]]`, not just file-level links
- **Has back-links** — source code has `@lat:` comments pointing to the
  sections that describe them
- **Captures WHY, not just WHAT** — design rationale, invariants, constraints
- **Groups by concept** — not a 1:1 mirror of the file tree
- **Concise leading paragraphs** — ≤250 chars, the section's identity in search

**Anti-patterns (what our v0.1 got wrong):**
- Sections with only section-to-section links (`[[clusters#Visual Pipeline]]`)
  and no source anchors — `lat check` cannot catch code changes
- Architectural essays that describe the codebase without linking to it —
  a static document, not a knowledge graph
- Treating back-links as optional — without `@lat:` comments, the bottom-up
  view doesn't exist and half the drift detection is missing

## Token Budget

The maps-first approach significantly reduces LLM token cost:
- Mapping-codebases (Phase 1): zero LLM tokens — pure AST extraction
- Selective reading (Phase 2): ~30-50% of source bytes vs reading everything
- Generation (Phase 3): the actual LLM work — proportional to conceptual
  complexity, not codebase size
- Back-links (Phase 4): zero LLM tokens — the suggest_backlinks.py script
  is deterministic
- Validation (Phase 5): zero LLM tokens — deterministic `lat check`
