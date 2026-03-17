---
name: chronos-release
description: Release a new version of the AllSource Chronos monorepo. Bumps versions across all services (Rust, Go, Elixir), runs full CI to green, creates a single squashed commit with an annotated immutable tag. Use when the user says "release", "new version", "bump version", "tag a release", "cut a release", or "make a release". Argument is the version number (e.g., "0.10.4") or "patch"/"minor"/"major" for auto-increment.
---

# Chronos Release Skill

Cut a release for the AllSource Chronos monorepo. Produces exactly one commit and one immutable annotated tag.

## Immutable Tags Policy

**NEVER** move, delete, or re-create an existing tag. If a release has issues after tagging, bump the version and cut a new release (e.g., v0.10.4 instead of re-tagging v0.10.3).

Before starting, verify the requested tag does not already exist:
```bash
git tag -l "v<VERSION>"
```
If it exists, abort and tell the user to choose a higher version.

## Procedure

### 1. Determine version

If the user provides a semver string, use it. If they say "patch", "minor", or "major", read the current version and increment:
```bash
grep 'version = ' apps/core/Cargo.toml | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
```

### 2. Check preconditions

- Working tree must be clean (`git status --porcelain` empty) OR the user explicitly wants to include staged changes
- Current branch should be `main` (warn if not)
- Tag `v<VERSION>` must not exist

### 3. Bump versions

```bash
make set-version VERSION=<VERSION>
```

This updates: `Cargo.toml`, `main.go`, `tracing.go`, `mix.exs` (x2), K8s manifests, `README.md`.

After running, also update `Cargo.lock`:
```bash
cd apps/core && cargo update --workspace
```

Check for any other version references that `set-version` might miss:
- `apps/control-plane/docs/openapi.yaml` (info.version field)
- `apps/core/README.md`, `apps/mcp-server-elixir/README.md` (version badges/text)
- `docs/` files referencing the old version

### 4. Run CI to green

```bash
make ci
```

If CI fails, fix all issues iteratively:
- **Rust**: `cargo +nightly fmt`, `cargo +nightly sort`, clippy fixes, doc link fixes
- **Go**: `gofmt`, golangci-lint fixes
- **Elixir**: `mix format`, `mix deps.unlock --unused`, credo fixes, test fixes

Re-run `make ci` after each round of fixes until it passes.

### 5. Commit (single squashed commit)

Stage all changes and create exactly ONE commit:

```bash
git add -A
git commit -m "$(cat <<'EOF'
release: v<VERSION> — <brief description of what changed>

<bullet list of key changes>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**Critical**: There must be exactly one new commit for the release. If you need multiple rounds of CI fixes, do NOT commit between rounds — only commit once everything is green.

### 6. Tag (immutable)

Create an annotated tag:
```bash
git tag -a v<VERSION> -m "v<VERSION> — <brief description>"
```

### 7. Verify

```bash
git log --oneline -3
git show v<VERSION> --oneline --no-patch
```

Confirm: single new commit, tag points to it.

### 8. Report

Tell the user:
- Version: v<VERSION>
- Commit: <hash>
- Tag: v<VERSION>
- CI: green
- Remind them to `git push && git push --tags` when ready

Do NOT push automatically — let the user decide when to push.

## Common CI Fix Patterns

| Tool | Common Issue | Fix |
|------|-------------|-----|
| cargo clippy | collapsible_if | Use let-chain syntax: `if cond1 && cond2 { }` |
| cargo clippy | new_without_default | Add `impl Default for T { fn default() -> Self { Self::new() } }` |
| cargo clippy | redundant_closure | `.map(Foo::bar)` instead of `.map(\|x\| Foo::bar(x))` |
| cargo sort | unsorted deps | `cargo +nightly sort` |
| cargo fmt | formatting | `cargo +nightly fmt` |
| rustdoc | broken_intra_doc_links | Wrap brackets in backticks |
| golangci-lint | goconst | Extract repeated strings to constants |
| golangci-lint | gocritic ifElseChain | Convert to switch statement |
| mix credo | alias ordering | Alphabetize alias statements |
| mix credo | cyclomatic complexity | Refactor or add `# credo:disable-for-next-line` |
| mix format | formatting | `mix format` in each Elixir app |
| mix dialyzer | pattern_match warnings | Add entries to `.dialyzer_ignore.exs` |
