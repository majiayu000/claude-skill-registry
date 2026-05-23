---
name: add-shadcn-component
description: Add shadcn/ui components via pnpm dlx, then normalize generated Tailwind color classes to Scaffa theme tokens
---

# Add shadcn Component

Add one or more shadcn/ui components, then replace any generated “design system” color utility classes with Scaffa’s Tailwind theme tokens.

## Usage

```
/add-shadcn-component <component...>
```

Example:

```
/add-shadcn-component button dropdown-menu dialog
```

## Prerequisites (assumed)

1. shadcn is initialized for the renderer and `src/renderer/components.json` exists (assume true; do not check).
2. The renderer theme tokens are defined in `src/renderer/styles.css` (Tailwind v4 `@theme` tokens).

If shadcn is not initialized yet, STOP and ask the user to run init first.

## What This Skill Does

1. Adds shadcn components using `pnpm dlx … add <componentList>`
2. Identifies the files that were created/modified
3. Rewrites generated Tailwind color classes to Scaffa theme tokens (surfaces/fg/border/focus/selected/etc.)
4. Runs a build to verify TypeScript + CSS compilation
5. Lands the change (commit + `bd sync` + push), respecting the repo workflow

## Instructions

You MUST follow these steps in order.

### Phase 1: Add the component(s)

1. Run shadcn from the same folder as `src/renderer/components.json`:
   ```bash
   pushd src/renderer
   ```

2. While still in `src/renderer`, add the requested components.

   Preferred (explicit) command:
   ```bash
   pnpm dlx shadcn@latest add <component...>
   ```

   If this repo’s shadcn init documented a shorter alias (e.g. `pnpm dlx add ...`), use the repo’s convention instead, but keep the semantics identical: “run shadcn add for these components”.

3. Return to the repo root:
   ```bash
   popd
   ```

4. Capture what changed:
   ```bash
   git status --porcelain
   ```

### Phase 2: Normalize generated colors to Scaffa theme tokens

Scaffa’s renderer uses Tailwind v4 theme tokens defined in `src/renderer/styles.css` (e.g. `bg-surface-panel`, `bg-surface-card`, `bg-surface-overlay`, `text-fg-muted`, `border-default`, `ring-focus`, `bg-selected`, etc).

The shadcn generator commonly emits palette tokens like `bg-background`, `text-foreground`, `border-border`, `ring-ring`, `bg-primary`, `text-muted-foreground`, etc. Those MUST be replaced with Scaffa tokens.

Prefer Scaffa’s **surface role** tokens over numeric surface levels:
- `bg-surface-app`, `bg-surface-panel`, `bg-surface-pane` *(reserved; currently aliases panel)*, `bg-surface-card`, `bg-surface-overlay`, `bg-surface-inset`
- For text/borders/rings, keep using `text-fg*`, `border-*`, `ring-focus`, etc.

#### 2.1 Required mapping (default)

Use this mapping as the baseline. Adjust only if the component semantics demand it.

- Backgrounds
  - `bg-background` → `bg-surface-app`
  - `bg-card` → `bg-surface-card`
  - `bg-popover` → `bg-surface-overlay`
  - `bg-muted` → `bg-surface-inset`
  - `bg-accent` → `bg-hover`
  - `bg-primary` → `bg-selected`
  - `bg-secondary` → `bg-surface-card`
  - `bg-destructive` → `bg-danger`

- Text
  - `text-foreground` → `text-fg`
  - `text-muted-foreground` → `text-fg-muted`
  - `text-popover-foreground` → `text-fg`
  - `text-card-foreground` → `text-fg`
  - `text-primary-foreground` → `text-selected-fg`
  - `text-secondary-foreground` → `text-fg`
  - `text-accent-foreground` → `text-fg`
  - `text-destructive-foreground` → `text-fg-inverse`
  - `text-destructive` → `text-danger`

- Borders
  - `border-border` → `border-default`
  - `border-input` → `border-default`
  - `border-ring` → `border-focus`
  - `border-destructive` → `border-danger`

- Rings / focus
  - `ring-ring` → `ring-focus`
  - `outline-ring` → `outline-focus`

  For common shadcn focus patterns:
  - `focus-visible:ring-ring` → `focus-visible:ring-focus`
  - `focus-visible:ring-offset-background` → `focus-visible:ring-offset-surface-app`

If you encounter shadcn tokens not covered above (e.g. `bg-input`, `text-primary`, etc.), prefer mapping them to the closest Scaffa semantic token from `src/renderer/styles.css` rather than introducing a new color.

#### 2.2 How to apply the mapping safely

1. Find newly added/modified component files (from `git status`).
2. Search within those files for shadcn palette tokens:
   ```bash
   rg -n \"bg-(background|card|popover|muted|accent|primary|secondary|destructive)|text-(foreground|muted-foreground|popover-foreground|card-foreground|primary-foreground|secondary-foreground|accent-foreground|destructive(-foreground)?)|border-(border|input|ring|destructive)|ring-ring|ring-offset-background|outline-ring\" <file-or-folder>
   ```
3. Replace only the **color tokens**. Do not “re-style” spacing, sizing, or layout unless necessary for compile or obvious correctness.
4. After edits, re-run the search to ensure no shadcn palette tokens remain in the touched files.

### Phase 3: Verify

Run a production build:

```bash
pnpm build
```

### Phase 4: Landing protocol

1. Stage changes:
   ```bash
   git add <files>
   ```

2. Commit code changes (do NOT include `.beads/issues.jsonl`):
   ```bash
   git commit -m \"feat(ui): add shadcn <components> (Scaffa theme)\"
   ```

3. Persist beads updates (if any) and push:
   ```bash
   git pull --rebase
   # If this session is explicitly "no beads", skip `bd sync`.
   bd sync
   git push
   git status  # MUST show up to date
   ```

## Notes / Gotchas

- This repo uses Tailwind v4 `@theme` tokens; prefer `bg-surface-*`, `text-fg*`, `border-*`, `ring-focus`, `bg-selected`, etc over shadcn’s palette tokens.
- Prefer surface roles (`bg-surface-app/panel/card/overlay/inset`) over numeric surface levels (`bg-surface-0..3`) when choosing container backgrounds.
- If a generated component requires additional tokens not in the Scaffa theme, file a ticket instead of inventing new one-off colors inside components.
