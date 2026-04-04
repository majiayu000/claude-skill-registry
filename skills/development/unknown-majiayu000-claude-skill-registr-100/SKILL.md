---
name: nvim-plugin-add
description: Add and configure Neovim plugins in this dotfiles repo using lazy.nvim. Use when asked to install a plugin, create its config module, update lazy.nvim imports, read plugin README/docs, and add keymaps without conflicting with existing mappings under config/nvim.
---

# Neovim plugin add (lazy.nvim)

Use this workflow when adding a new plugin to `config/nvim`.

## Workflow

1) Inspect the existing layout
- Open `config/nvim/init.lua` to confirm the lazy.nvim `spec` import list.
- Check `config/nvim/lua/plugins/` for the naming pattern of plugin config files.

2) Read upstream docs
- Read the plugin README and docs from its repo (and any `doc/*.txt` if needed).
- Prefer the upstream “recommended” or “minimal working” configuration.

3) Create a plugin config module
- Add a new file under `config/nvim/lua/plugins/<plugin-name>.lua`.
- Return a lazy.nvim spec table (same style as other plugin files).
- Keep the module self-contained; avoid global side effects.

4) Register the module in lazy.nvim
- Add `{ import = 'plugins.<plugin-name>' }` to the `spec` list in `config/nvim/init.lua`.
- Keep the ordering consistent with existing imports unless the plugin suggests a dependency order.

5) Keymap collision check
- Before adding keymaps, search existing mappings:
  - `rg -n "keymap|map\\(" config/nvim`
  - Also scan for `which-key` registrations if present.
- If a recommended mapping conflicts, choose a nearby alternative under the same mnemonic prefix.
- Use `desc` for every mapping.

6) Configure defaults and options
- Wire up plugin `setup()` with upstream defaults plus any repo-specific conventions.
- Follow existing patterns (e.g., use `vim.keymap.set`, local helper functions).
- Keep options and mappings minimal; avoid speculative tweaks.

7) Validation
- Ensure the plugin file is required by lazy.nvim and no syntax errors are introduced.
- If the change impacts keymaps, mention any new keys in the response.

## Repo conventions

- Neovim config root: `config/nvim/`.
- lazy.nvim bootstrap and imports live in `config/nvim/init.lua`.
- Plugin config modules live in `config/nvim/lua/plugins/` and return a plugin spec.
- Keep edits ASCII-only unless the file already uses non-ASCII.

## Notes on keymaps

- Prefer `<leader>` mappings and keep them consistent with existing prefixes.
- Avoid overriding single-letter normal mode bindings unless the repo already does so.
- When in doubt, add a `which-key` entry matching the new mapping.
