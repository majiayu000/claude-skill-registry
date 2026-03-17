---
name: nvim-config-ops
description: API-reference skill for this Neovim repo. Use when an agent needs fast lookup of callable/public functions in `lua/user/*`, key Neovim Lua APIs (`vim.api`, `vim.lsp`, `vim.diagnostic`), and file hotspots for plugin/debug/config work.
---

# Neovim Config API Reference

This skill is API-listing-first.
Use it to avoid broad source scanning.

## Repo Public APIs
Load detailed lists from:
- `references/repo-public-api.md`
- `references/plugin-hotspots.md`
- `references/repo-map.md`

## Neovim Runtime APIs (Quick Index)

### vim.api
```lua
vim.api.nvim_create_autocmd(...)
vim.api.nvim_create_augroup(...)
vim.api.nvim_create_user_command(...)
vim.api.nvim_set_hl(...)
vim.api.nvim_get_current_buf()
vim.api.nvim_get_current_win()
vim.api.nvim_buf_get_lines(...)
vim.api.nvim_buf_set_lines(...)
vim.api.nvim_win_set_cursor(...)
vim.api.nvim_feedkeys(...)
```

### vim.lsp
```lua
vim.lsp.get_clients(...)
vim.lsp.get_client_by_id(...)
vim.lsp.enable(...)
vim.lsp.config(...)
vim.lsp.buf.definition(...)
vim.lsp.buf.implementation(...)
vim.lsp.buf.references(...)
vim.lsp.buf.rename(...)
vim.lsp.buf.code_action(...)
vim.lsp.buf.format(...)
vim.lsp.codelens.refresh(...)
vim.lsp.inlay_hint.enable(...)
vim.lsp.log.get_filename()
```

### vim.diagnostic
```lua
vim.diagnostic.config(...)
vim.diagnostic.get(...)
vim.diagnostic.open_float(...)
vim.diagnostic.goto_prev(...)
vim.diagnostic.goto_next(...)
vim.diagnostic.disable(...)
vim.diagnostic.enable(...)
```

## Operational Rules
- Pinpoint likely target files first.
- Prefer debug-first commands before patching.
- Keep minimal diffs.
- Format edited Lua files with `stylua <file>`.
