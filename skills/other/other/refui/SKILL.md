---
name: refui
description: "Use when working with rEFui (refui) applications where you cannot rely on reading the library source. Covers the retained-mode + signals mental model, DOM/HTML/Reflow renderers, JSX setup (classic pragma vs automatic runtime), directives (on:/class:/style:/attr:/prop:/m: macros), HMR via refurbish/refui/hmr, debugging “UI not updating” issues, and migrating React/Vue/Solid/Svelte patterns to rEFui."
---

# rEFui

## Overview

Apply rEFui’s retained-mode + signals model correctly, choose the right JSX mode/renderer, and fix reactivity/lifecycle issues without importing patterns from other UI frameworks.

## General guide

### Mental model (retained mode)

- Component bodies are **setup**: they run once; they do not “re-render”.
- JSX is evaluated once; **signals** update the already-built UI incrementally.
- If something “doesn’t update”, you almost always read `.value` too early (non-reactively) or mutated in place without `trigger()`.

### Signals & reactivity

- State: `const count = signal(0)`
- Reactive JSX: `{count}` (not `{count.value}`)
- Derived: `const label = $(() => `Count: ${count.value}`)` and then `{label}`
- In-place mutation: call `sig.trigger()` after mutating arrays/objects.

```jsx
import { signal, $ } from 'refui'

const Counter = () => {
	const count = signal(0)
	return (
		<button on:click={() => count.set(count.value + 1)}>
			{$(() => `Count: ${count.value}`)}
		</button>
	)
}
```

### Effects & cleanup

- Reactive effect: `watch(() => { ...reads signals... })`
- Setup/cleanup: `useEffect(() => { ...; return () => cleanup })`
- Teardown-only: `onDispose(() => cleanup)`
- Scheduling: if you need “after updates applied”, `await nextTick()`.

### Control flow components

- Conditional UI: `<If condition={cond}>{() => <Then />}{() => <Else />}</If>`
- Lists: `<For entries={items} track="id">{({ item, index }) => ...}</For>`
- Inline dynamic subtree with lifecycle: `<Fn ctx={something}>{(ctx) => ...}</Fn>`
- `For` has **no** `fallback`; for empty states, wrap with `<If>`.

```jsx
import { signal, $, If, For } from 'refui'

const App = () => {
	const items = signal([{ id: 1, name: 'A' }])
	return (
		<If condition={$(() => items.value.length)}>
			{() => <For entries={items} track="id">{({ item }) => <div>{item.name}</div>}</For>}
			{() => <div>Empty</div>}
		</If>
	)
}
```

### Async UI

- `<Async>` for a single promise boundary.
- `<Suspense>` to group multiple async subtrees under one fallback.
- `lazy(() => import(...))` for code-splitting; pair with fallback boundaries.
See `references/async-suspense-transition.md` for the “rules of engagement”.

### Context

Use context for shared subtree values. If consumers must react to changes, provide a signal as the context value.

```jsx
import { signal, $, createContext, useContext } from 'refui'

const Theme = createContext(signal('light'), 'Theme')

const Button = () => {
	const theme = useContext(Theme)
	return <button class:dark={$(() => theme.value === 'dark')}>OK</button>
}
```

Non-Reflow/custom renderer: wrap Provider children in a function so they inherit context: `<Theme value={x}>{() => <Button />}</Theme>`.

### Mounting (DOM / HTML)

- DOM renderer (browser): `createDOMRenderer(defaults).render(target, App)`
- HTML renderer (SSR/SSG): `createHTMLRenderer().serialize(createElement(App, props))`
- JSX + renderer selection: see `references/jsx-and-renderers.md` (automatic vs classic transform).

```jsx
import { createDOMRenderer } from 'refui/dom'
import { defaults } from 'refui/browser'

createDOMRenderer(defaults).render(document.getElementById('app'), App)
```

### DOM directives (browser preset)

- Events: `on:click={fn}` (+ `on-once:*`, `on-passive:*`, `on-capture:*`)
- Classes/styles: `class:active={boolOrSignal}`, `style:color={valueOrSignal}`
- Attributes vs props: `attr:*` (SVG/read-only), `prop:*` (force property write)
- Macros: `m:*` for reusable DOM behaviors (renderer-registered handlers)

## Default Policy: Use rEFui Built-ins First

When implementing a requirement, prefer rEFui’s built-in primitives (signals/components/extras/renderers) over custom plumbing. Only fall back to a custom implementation when:
- rEFui has no built-in primitive that matches the requirement, and
- the project’s rEFui version lacks an equivalent helper, and
- you can’t express it cleanly as a DOM macro (`m:*`) or small reusable component.

Before writing code, consult `references/dos-and-donts.md` to avoid React-style mistakes.

## Quick Triage (do this first)

1. Identify **JSX mode** in the target repo:
	 - **Automatic runtime**: look for `jsx: 'automatic'` + `jsxImportSource: 'refui'` (Vite/esbuild) or `jsxImportSource: "refui"` (tsconfig/Bun).
	 - **Classic transform**: look for `jsxFactory: 'R.c'` + `jsxFragment: 'R.f'` (Vite/esbuild) or `/** @jsx R.c */` file pragmas.
2. Identify the **host renderer**:
	 - Browser apps: `createDOMRenderer(defaults)` from `refui/dom` + `refui/browser` (or `refui/presets/browser` in older repos).
	 - SSR/SSG: `createHTMLRenderer()` from `refui/html`, then `serialize()`.
	 - Reflow logic-only modules: `refui/reflow` (often injected via `jsxInject: import { R } from 'refui/reflow'` in classic mode).
3. Confirm **rEFui version** (it changes API details across repos). Prefer the repo’s local docs or installed `refui` exports.

If you want an automated scan for JSX mode + common pitfalls, run `node scripts/refui-audit.mjs <path>` from inside this skill folder.

## When Usage Is Unclear (consult MCP docs)

If you are unsure about a rEFui API, behavior, or best practice and cannot inspect the library source:

- Use **Context7 MCP** to pull authoritative, up-to-date library docs/snippets:
	- First resolve the library: `mcp__context7__resolve-library-id` with `libraryName: "refui"`.
	- Then query: `mcp__context7__query-docs` for the specific API/task (e.g. “`For` track vs indexed”, “`createDOMRenderer` macros”, “`nextTick` vs `tick` semantics”, “classic vs automatic JSX setup”).
- Use **DeepWiki MCP** for repository-level questions (when the upstream repo is available):
	- `mcp__deepwiki__read_wiki_structure` then `mcp__deepwiki__ask_question` on `SudoMaker/rEFui` for conceptual/system questions or “where is X documented?”.

If MCP docs still leave ambiguity, ask the user for: the `refui` version, their bundler config (Vite/esbuild/Bun/TS/Babel), and a minimal repro snippet.

## “Which rEFui feature should I use?” (fast mapping)

Use these references when choosing a built-in solution:
- Idiot-proof do/don’t checklist: `references/dos-and-donts.md`
- Async UI: `references/async-suspense-transition.md`
- Overlays/teleports/rich HTML/custom elements: `references/portals-parse-custom-elements.md`
- Lists/identity/caching/perf: `references/lists-cache-memo.md`
- Project setup: `references/project-setup.md`

## Non-Negotiables (retained mode)

- Do not write React/Vue/Solid/Svelte primitives (`useState`, hooks, VDOM assumptions, `$:` blocks, etc.). Map them to rEFui signals/effects.
- Treat component bodies as **setup** (constructor-ish). JSX is evaluated once; signals drive incremental updates afterward.
- Keep reactive reads reactive:
	- ✅ Use a signal directly: `<div>{count}</div>`
	- ✅ Wrap derived expressions: `<div>{$(() => `Count: ${count.value}`)}</div>` or `<div>{computed(() => ...)}</div>`
	- ❌ Avoid inline `.value` in JSX: `<div>{count.value}</div>` (evaluates once, won’t update)
- Remember scheduling: signal effects/computed flush at the end of the tick; use `await nextTick()` when you must observe derived updates.

## Hard Rules (idiot-proof guardrails)

- This is **not React**. Component bodies run once; JSX does not re-run. Do not expect re-renders.
- Do not invent props. If the API is unclear, open the .d.ts or use MCP. Example: `For` has **no** `fallback` prop.
- `If` / `For` / templates accept a **single** renderable. If you need multiple nodes, wrap them in a container or fragment.
- `For` empty state: wrap it in `If` and provide a false branch. Example:
	- `<If condition={$(() => items.value.length)}><For entries={items} track="id">{({ item }) => <Row item={item} />}</For><Empty /></If>`
- Use `.value` inside `computed` / `$(() => ...)` / `watch` / event handlers, not directly in JSX text/attrs.

## Default Patterns (copy these mentally)

- State: `const x = signal(initial)`
- Derived: `const y = $(() => /* uses x.value */)` (or `computed(() => ...)`)
- Effects: `watch(fn)` for reactive computations; `useEffect(setup)` for setup+cleanup; `onDispose(cleanup)` for teardown.
- Lists:
	- Keyed: `<For entries={items} track="id">{({ item }) => ...}</For>`
	- Unkeyed (perf experiments / reorder heavy): `UnKeyed` from `refui/extras/unkeyed.js`
	- If mutating arrays/objects in place: call `sig.trigger()` after mutation.
- Async:
	- `<Async future={promise} fallback={...} catch={...}>{({ result }) => ...}</Async>`
	- `<Suspense>` for grouping async subtrees
	- `async` components are supported; pair with fallbacks when needed.
- DOM directives/events (DOM renderer):
	- Events: `on:click={...}`, plus options `on-once:*`, `on-passive:*`, `on-capture:*`
	- Attributes vs props: prefer `attr:` for SVG or when a DOM prop is read-only; use `prop:` to force a property set.
	- Preset directives (browser preset): `class:x={boolSignal}`, `style:color={valueOrSignal}`
	- Macros: `m:name={value}` where `name` is registered on the renderer.
- Refs/handles:
	- `$ref={sig}` to receive a node/instance in `sig.value`
	- `$ref={(node) => ...}` callback form
	- Prefer `expose` prop for imperative child handles (v0.8.0+).

## Workflows

### Fix “UI not updating”

1. Search for JSX `{something.value}` and decide if it must be reactive:
	 - Replace with `{something}` when `something` is already a signal.
	 - Wrap derived text/attrs with `$(() => ...)` / `computed(() => ...)` / `t\`...\``.
2. If you mutated an object/array held by a signal in-place, add `sig.trigger()` (or replace with a new object/array).
3. If you read derived values immediately after writes, insert `await nextTick()` before reading computed/DOM-dependent values.
4. If an effect runs “forever”, ensure it’s created inside a component scope and cleaned up via `useEffect`/`onDispose`.

### Add a feature safely

1. Keep renderer creation at the entry point; do not create renderers inside components.
2. Localize state: prefer per-component signals over global blobs; use `extract`/`derivedExtract` to reduce fan-out.
3. For repeated DOM behaviors, register a macro and use it via `m:*` rather than duplicating manual DOM code.
4. For lists, choose keyed `<For>` unless you have a measured reason to use unkeyed.

### Set up a new project (when asked)

1. Ask only: preferred package manager (`npm`/`pnpm`/`yarn`/`bun`) and language (JS/TS). Do not ask runtime.
2. Default to JSX automatic runtime + JavaScript + `refui` latest from npm unless the user specifies otherwise.
3. Follow `references/project-setup.md`.

## Repo Navigation (load only if needed)

Read these files when you need deeper details:

- `references/project-triage.md` for determining JSX mode/renderer/version from a project that uses rEFui as a dependency.
- `references/project-setup.md` for scaffolding a new project (default: JSX automatic runtime + pure JS).
- `references/jsx-and-renderers.md` for choosing classic vs automatic and DOM/HTML/Reflow specifics.
- `references/reactivity-pitfalls.md` for high-signal debugging checklists and anti-patterns.
- `references/dos-and-donts.md` for per-API/component do’s and don’ts that prevent React-mindset mistakes.
- `references/async-suspense-transition.md` for `<Async>`, `<Suspense>`, `lazy`, and `Transition`.
- `references/portals-parse-custom-elements.md` for portals/teleports, HTML parsing, and custom elements.
- `references/lists-cache-memo.md` for `<For>`, identity, `UnKeyed`, caching, and memoization.

## Resources

### `scripts/`
- `scripts/refui-audit.mjs`: quick scan for JSX mode + common `.value`-in-JSX pitfalls.

### `references/`
- `references/project-triage.md`
- `references/jsx-and-renderers.md`
- `references/reactivity-pitfalls.md`
- `references/dos-and-donts.md`
- `references/async-suspense-transition.md`
- `references/portals-parse-custom-elements.md`
- `references/lists-cache-memo.md`
- `references/project-setup.md`
