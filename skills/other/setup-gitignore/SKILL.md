---
name: setup-gitignore
description: Initialize or idempotently revise the repo's .gitignore by composing gitignore.io templates, AI-tooling/IDE patterns, and confirmed noise from git status. Use when the user says "set up gitignore", "fix gitignore", or untracked files keep appearing in git status.
---

Initialize or idempotently revise the current repo's `.gitignore` — never the global excludesfile.

## Scope

Per-repo only. Never read or write `~/.gitignore`, `~/.config/git/ignore`, or run `git config --global`. The user's global excludesfile handles cross-machine noise; this skill handles language/tool specifics for the current repo.

## Sources composed (in order)

1. **gitignore.io** — templates keyed by detected language/framework (requires network)
2. **AI tooling** — bundled patterns from `references/AI-TOOLING.md`
3. **IDE / editor** — bundled patterns from `references/IDE-EDITOR.md`
4. **Empirical** — untracked paths from `git status`, confirmed interactively

## Workflow

### 1. Detect repo root

```sh
git rev-parse --show-toplevel
```

Abort with a clear error if not inside a git repo.

### 2. Detect languages

Read `references/LANGUAGE-DETECTION.md` for the manifest → gitignore.io key table. Scan manifests:

```sh
fd --max-depth 2 -t f
```

Match filenames against the detection table; build a comma-separated key list (e.g., `rust,node,typescript`). If no manifests detected, use an empty key list (bundled blocks still apply).

### 3. Snapshot existing .gitignore

If `.gitignore` exists, snapshot it before any modification:

```sh
cp .gitignore /tmp/gitignore-snapshot-$(date +%s).bak
```

### 4. Surface empirical noise

```sh
git status -s -uall | rg '^\?\?' | rg -v '^\?\? \.gitignore'
```

Cluster untracked paths by top-level directory or extension. **Present clusters to the user and wait for explicit confirmation.** Do not add any empirical pattern without confirmation.

### 5. Compose

Run `scripts/compose-gitignore.sh <csv>` to fetch and merge gitignore.io templates. If the network call fails, tell the user and ask whether to continue with bundled-only mode.

Append the bundled blocks after the API output in order:

```
# === AI TOOLING ===
<contents of references/AI-TOOLING.md>

# === IDE / EDITOR ===
<contents of references/IDE-EDITOR.md>

# === EMPIRICAL ===
<user-confirmed patterns, one per line>
```

### 6. Merge or init

- **No existing `.gitignore`**: write the composed output directly.
- **Existing `.gitignore`**: merge each `# === SECTION ===` block idempotently — patterns already present in the file are deduplicated (first occurrence wins). Preserve all user content outside section headers. Show the full diff via `difft`; write only after user confirms.

### 7. Verify

```sh
git status -s -uall | rg '^\?\?' | wc -l
```

Report untracked count before and after. List any paths still untracked so the user can decide whether to add further patterns.

## Idempotence contract

Re-running the skill on a repo where the skill already ran produces no diff. Section headers act as stable merge anchors. User content outside sections is never modified.
