---
name: denji
description: Manage SVG icons as framework components using Denji CLI. Use when the user needs to add, remove, list, or manage SVG icons in React, Preact, Solid, Qwik, Vue, or Svelte projects. Triggers include requests to "add an icon", "set up icons", "manage SVG icons", "remove an icon", "list icons", or any task involving Iconify icons as framework components.
allowed-tools: Bash(npx denji:*)
metadata:
  author: fellipeutaka
  version: "0.4.0"
---

# Managing SVG Icons with Denji

Denji converts Iconify SVG icons into typed framework components. Icons are fetched, optimized (SVGO), and generated as native components for your framework.

## Core Workflow

```bash
# 1. Initialize project
npx denji init --framework react --output ./src/icons.tsx

# 2. Add icons (prefix:name format from Iconify)
npx denji add lucide:check lucide:x lucide:arrow-right

# 3. Use in your code
```

```tsx
import { Icons } from "./icons";

<Icons.Check className="size-4 text-green-500" />
<Icons.X className="size-4 text-red-500" />
```

## Commands

### `denji init`

Initialize a Denji project. Creates `denji.json` config and icons template.

```bash
npx denji init
npx denji init --framework react --output ./src/icons.tsx
npx denji init --framework svelte --output ./src/icons --output-type folder
npx denji init --framework react --no-typescript --output ./src/icons.jsx
npx denji init --a11y hidden --forward-ref
```

| Flag | Description |
|------|-------------|
| `--framework <name>` | `react`, `preact`, `solid`, `qwik`, `vue`, `svelte` |
| `--output <path>` | Output path for icons file/folder |
| `--output-type <type>` | `file` (single file) or `folder` (one file per icon) |
| `--typescript` / `--no-typescript` | TypeScript or JavaScript (default: TS) |
| `--a11y <strategy>` | `hidden`, `img`, `title`, `presentation`, or `false` |
| `--forward-ref` / `--no-forward-ref` | Use forwardRef (React/Preact only) |
| `--track-source` / `--no-track-source` | Track Iconify source via `data-icon` attr |
| `-c, --cwd <path>` | Working directory |

Missing flags trigger interactive prompts.

### `denji add <icons...>`

Add icons from Iconify. Icons use `prefix:name` format.

```bash
npx denji add lucide:check
npx denji add lucide:check mdi:home radix-icons:cross-2
npx denji add lucide:star --name FavoriteStar
npx denji add lucide:info --a11y img
```

| Flag | Description |
|------|-------------|
| `--name <name>` | Custom component name (single icon only) |
| `--a11y <strategy>` | Override a11y strategy for this icon |
| `-c, --cwd <path>` | Working directory |

Icon naming: `lucide:arrow-right` becomes `ArrowRight` (PascalCase). Override with `--name`.

Adding an existing icon updates it in place.

### `denji remove <icons...>`

Remove icons by component name. Aliases: `rm`, `delete`, `del`.

```bash
npx denji remove Check
npx denji rm Check Home ArrowRight
```

| Flag | Description |
|------|-------------|
| `-c, --cwd <path>` | Working directory |

### `denji list`

List all icons in your project.

```bash
npx denji list
npx denji list --json
```

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |
| `-c, --cwd <path>` | Working directory |

Shows component names and Iconify source (if `trackSource: true`).

### `denji clear`

Remove all icons. Aliases: `clr`, `reset`.

```bash
npx denji clear
npx denji clear --yes
```

| Flag | Description |
|------|-------------|
| `-y, --yes` | Skip confirmation prompt |
| `-c, --cwd <path>` | Working directory |

## Config (`denji.json`)

The `$schema` field depends on how Denji is installed:

- **Locally installed** (`npm i -D denji`): `"./node_modules/denji/configuration_schema.json"`
- **Not installed** (using `npx`, `bunx`, `pnpx`, `yarn dlx`): `"https://denji-docs.vercel.app/configuration_schema.json"`

```json
{
  "$schema": "./node_modules/denji/configuration_schema.json",
  "framework": "react",
  "output": "./src/icons.tsx",
  "typescript": true,
  "a11y": "hidden",
  "trackSource": true,
  "react": {
    "forwardRef": true
  },
  "hooks": {
    "postAdd": ["npx biome check --write ./src/icons.tsx"],
    "postRemove": ["npx biome check --write ./src/icons.tsx"]
  }
}
```

Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `framework` | string | Required. `react`, `preact`, `solid`, `qwik`, `vue`, `svelte` |
| `output` | string or object | Required. Path string or `{ type: "file"\|"folder", path: "..." }` |
| `typescript` | boolean | Default: `true` |
| `a11y` | string or false | `hidden`, `img`, `title`, `presentation`, `false` |
| `trackSource` | boolean | Default: `true`. Adds `data-icon` attr |
| `hooks` | object | Lifecycle hooks (see below) |

### Output Modes

**File mode** (default for React, Preact, Solid, Qwik, Vue): All icons in one file.

```json
{ "output": "./src/icons.tsx" }
```

**Folder mode** (required for Svelte, optional for others): One file per icon + barrel export.

```json
{ "output": { "type": "folder", "path": "./src/icons" } }
```

### Hooks

Run shell commands at lifecycle points:

```json
{
  "hooks": {
    "preAdd": ["echo 'Adding icons...'"],
    "postAdd": ["npx prettier --write ./src/icons.tsx"],
    "preRemove": [],
    "postRemove": [],
    "preClear": [],
    "postClear": [],
    "preList": [],
    "postList": []
  }
}
```

## Common Patterns

### Dynamic Icons

```tsx
import { Icons, type IconName } from "./icons";

function DynamicIcon({ name, ...props }: { name: IconName } & Icons.IconProps) {
  const Icon = Icons[name];
  return <Icon {...props} />;
}

<DynamicIcon name="Check" className="size-4" />
```

### Accessibility

```tsx
// Decorative icon (hidden from screen readers)
<button>
  <Icons.Check aria-hidden="true" />
  Save
</button>

// Semantic icon (announced by screen readers)
<Icons.Check role="img" aria-label="Success" />

// Icon-only button
<button aria-label="Close">
  <Icons.X aria-hidden="true" />
</button>
```

### Formatting with Hooks

```json
{
  "hooks": {
    "postAdd": ["npx biome check --write ./src/icons.tsx"],
    "postRemove": ["npx biome check --write ./src/icons.tsx"]
  }
}
```

### Using forwardRef (React/Preact)

```json
{
  "framework": "react",
  "react": { "forwardRef": true }
}
```

```tsx
const ref = useRef<SVGSVGElement>(null);
<Icons.Check ref={ref} className="size-4" />
```

## Framework Quick Reference

| Framework | Extensions | Default Output | Config Key | Notes |
|-----------|-----------|----------------|------------|-------|
| React | `.tsx`/`.jsx` | file | `react` | `forwardRef` option |
| Preact | `.tsx`/`.jsx` | file | `preact` | `forwardRef` option (via `preact/compat`) |
| Solid | `.tsx`/`.jsx` | file | `solid` | Refs work natively as props |
| Qwik | `.tsx`/`.jsx` | file | `qwik` | Uses `component$()` in folder mode |
| Vue | `.ts`/`.js` | file | `vue` | Uses `h()` render functions |
| Svelte | `.svelte` | folder (only) | `svelte` | Svelte 5 `$props()` runes |

## Deep-Dive References

| Reference | Content |
|-----------|---------|
| [references/configuration.md](references/configuration.md) | Full config schema, all framework options, output normalization |
| [references/framework-patterns.md](references/framework-patterns.md) | Per-framework code examples, file vs folder imports, TypeScript types |
