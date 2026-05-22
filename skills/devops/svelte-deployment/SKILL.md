---
name: svelte-deployment
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Svelte deployment guidance. Use for adapters, Vite config, pnpm setup, library authoring, PWA, or production builds.
---

# Svelte Deployment

## Quick Start

**pnpm 10+:** Add prepare script (postinstall disabled by default):

```json
{
	"scripts": {
		"prepare": "svelte-kit sync"
	}
}
```

**Vite 7:** Update both packages together:

```bash
pnpm add -D vite@7 @sveltejs/vite-plugin-svelte@6
```

## Adapters

```bash
# Static site
pnpm add -D @sveltejs/adapter-static

# Node server
pnpm add -D @sveltejs/adapter-node

# Cloudflare
pnpm add -D @sveltejs/adapter-cloudflare
```

## Reference Files

- [library-authoring.md](references/library-authoring.md) - Publishing
  Svelte packages
- [pwa-setup.md](references/pwa-setup.md) - Offline-first with workbox
- [cloudflare-gotchas.md](references/cloudflare-gotchas.md) -
  Streaming issues

## Notes

- Cloudflare may strip `Transfer-Encoding: chunked` (breaks streaming)
- Library authors: include `svelte` in keywords AND peerDependencies
- Single-file bundle: `kit.output.bundleStrategy: 'single'`
- **Last verified:** 2025-01-14

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->
