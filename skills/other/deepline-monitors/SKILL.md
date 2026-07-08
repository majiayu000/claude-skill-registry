---
name: deepline-monitors
description: "ACCESS-GATED beta. Deepline Monitors (dashboard name: Signal Radars) — provider event feeds (job posts, email replies, funding, intent) that stream into your warehouse and trigger plays. Only use if you have monitor access: run `deepline monitors status` first; if it reports no access, do NOT use this recipe — every command returns monitor_access_required. Ask a Deepline admin (Admin → Rollouts) for access."
---

# Deepline Monitors (Signal Radars)

## Quick Start

```bash
npm install -g deepline
# Fallback for secure sandboxes: mkdir -p "$HOME/.local" && npm config set prefix "$HOME/.local" && export PATH="$HOME/.local/bin:$PATH" && npm install -g deepline --registry https://code.deepline.com/api/v2/npm/
deepline auth register --wait auto
deepline auth wait --timeout 120 # completes Cowork/browser approval; no-op if already connected
deepline auth status
deepline -h
```

This is a recipe shortcut. It pre-selects the deepline-monitors recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the deepline-monitors recipe at `../deepline-gtm/recipes/deepline-monitors.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
