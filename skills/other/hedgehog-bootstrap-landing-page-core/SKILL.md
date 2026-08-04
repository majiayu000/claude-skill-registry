---
name: hedgehog-bootstrap-landing-page-core
description: Use once, at the start of a new Hedgehog project on the landing-page core, to land the pre-verified Astro + Tailwind v4 workspace and verify it's green. Runs as the only move of the `bootstrap` agent on this core — there are no add-on steps, unlike full-stack-app. Invoked automatically by `planner` after Confirm & Lock.
---

# Hedgehog Bootstrap — landing-page Core

Lands the whole of a `landing-page` project's workspace — there's no
add-on layer to run after it, unlike `full-stack-app`'s
`hedgehog-bootstrap` — by copying a pre-built, pre-verified workspace
(`src/golden-cores/landing-page/` in the Hedgehog package) rather than
generating it live: Astro workspace, Tailwind v4 CSS-first token-layer
config, the library set this core is built on (Motion, Lenis, SplitType,
ogl, Lucide).
This piece is deterministic — the same commands produce the same output
on every project — so the output is committed once, upstream, and copied
here instead of re-derived by an agent on every run.

This skill has no per-project decisions to make: no add-ons, no
dependency beyond confirming its own commit hasn't already landed,
nothing to ask. Landing-page's core is identical on every project
running it.

## What lands

Everything under `src/golden-cores/landing-page/` in the installed
Hedgehog package, copied to the repo root:

- Root: `astro.config.mjs`, `package.json` (with the `dev` script —
  `astro dev` — and every library in the stack pinned), `tsconfig.json`,
  `eslint.config.mjs`, `.prettierrc.js`, `.gitignore`, `pnpm-lock.yaml`.
- `src/pages/index.astro` — a minimal placeholder page (proves the build
  pipeline works end to end), replaced by `landing-builder`'s own output
  at the build phase.
- `src/styles/global.css` — the Tailwind v4 CSS-first import and the
  `@theme` token block: no component classes, no plugin beyond the base.
  Ships with placeholder tokens (a neutral starting palette, a system
  type stack, a 1.25-ratio `--text-*` scale, a 4px spacing unit) that
  `landing-systems` overwrites entirely at its own phase — including
  swapping the system type stack for real `@fontsource-variable` faces.
  This block existing and being wired into the build is what core
  guarantees, not any specific token values.
- `src/sections/`, `src/shapes/`, `src/assets/` — empty, with a
  `.gitkeep`; real content starts at the systems and build phases.

`node_modules` is not part of the copy — `pnpm install` regenerates it
from the committed `pnpm-lock.yaml`.

## Steps

### 1. Confirm this hasn't already run

Check for `astro.config.mjs` at the repo root, or a prior
`feat(landing): workspace` commit
(`git log --grep="^feat(landing): workspace"`). Either means core already
landed — stop, don't re-copy. If something about the landed core seems
wrong, that's a Correction Protocol case (`hedgehog-landing-loop`), not a
re-copy: patch the specific file at its source.

### 2. Land `src/golden-cores/landing-page/`

`hedgehog init --landing-page` copies `src/golden-cores/landing-page/` to
the repo root at install time, the same way it copies `src/agents` to
this host's own agents directory — check whether the core files are
already present (same check as step 1) before copying again. On a project that ran plain
`init` (no core flag) and only reaches `landing-page` because `planner`
picked it at Phase 0, this hasn't happened yet: copy
`src/golden-cores/landing-page/`'s contents to the repo root now. Also
merge this core's `CLAUDE.md` section into root `CLAUDE.md`
(`src/templates/CLAUDE.core.landing-page.md` fills the shell's
`{{CORE_SECTION}}` placeholder left unfilled by a deferred install) —
skip this if the section is already filled. Either way, by the end of
this step every file listed in "What lands" above should be on disk.

### 3. Install

```bash
pnpm install
```

Resolves against the committed `pnpm-lock.yaml` — this should be fast
and produce no lockfile changes. A lockfile diff here means the shipped
`pnpm-lock.yaml` doesn't match `package.json` — that's a packaging bug in
`src/golden-cores/landing-page`, not something to patch locally (see **If
verification fails**, below).

### 4. Verify

```bash
pnpm astro check
pnpm build
```

Both must be clean: no type errors from the first command, a successful
build with no warnings from the second. This is the live check that
proves core isn't correct by trusting the copy, but by actually running
the same gate every phase in this core's loop runs.

### 5. Commit

```
feat(landing): workspace
```

One commit for all of core, landed as a verified copy. That commit
existing is the record that core landed — `bootstrap` checks for it via
the commit log, not a checklist line.

## Known issues baked into the landing-page core

These are already fixed in the committed tree — listed here so anyone
regenerating `src/golden-cores/landing-page` (see
`scripts/regenerate-landing-page-core.sh`) knows why the tree looks the
way it does, and doesn't reintroduce the bug by "cleaning up" what looks
like an unnecessary pin.

- **`typescript` must stay pinned to the `^5` line, not `7.x`.**
  `@astrojs/check` (which `astro check` calls into) relies on a
  programmatic TypeScript API that the 7.x native compiler doesn't
  expose yet — running `astro check` against TS 7 fails immediately with
  "does not expose the programmatic API that `astro check` relies on"
  (tracked at github.com/withastro/roadmap/discussions/1321). Re-check
  this pin when bumping TypeScript; it may be resolved upstream by then.
- **`create-astro`'s scaffold ships its own `AGENTS.md`/`CLAUDE.md`
  symlink, `README.md`, and `pnpm-workspace.yaml`**, as if this were a
  standalone repo rather than a tree that lands at a Hedgehog project's
  root. All four are stripped before syncing — they'd otherwise collide
  with (or silently shadow) the project's real root `CLAUDE.md` and
  Hedgehog's own workspace conventions.

## If verification fails

A clean copy of `src/golden-cores/landing-page` that fails `astro check`
or `pnpm build`, or needs a lockfile change, means the shipped template
itself is broken — not a per-project problem to hand-patch around. Stop
and report exactly what failed. Fixing this means updating
`src/golden-cores/landing-page` at its source (via
`scripts/regenerate-landing-page-core.sh` in the Hedgehog repo itself)
and shipping a new package version — never patch a consuming project's
copy to route around a broken template and call core done.

## Constraints

- Run once per project, as the `bootstrap` agent's only move on this
  core — never invoked on its own by a user.
- No add-on awareness, because this core has no add-ons. If a future
  landing-page variation genuinely needs one (a CMS integration, a form
  backend), that's a new core decision for `planner`'s Phase 0, not an
  add-on bolted onto this one.
- Don't hand-edit any file this step lands to work around a verification
  failure. Fix `src/golden-cores/landing-page` at the source instead (see
  **If verification fails**).
- Don't write any Chain Method phase content (adjectives, tokens,
  signature element, sequence, or the built page) — that's
  `landing-strategist` through `landing-builder`'s work, after this
  Bootstrap box is checked.
