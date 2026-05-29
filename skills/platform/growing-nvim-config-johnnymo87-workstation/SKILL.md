---
name: growing-nvim-config
description: How to incrementally add Neovim configuration in this NixOS/home-manager setup. Use this when adding keybindings, settings, or plugins to nvim.
---

# Growing Neovim Config

This repo uses a "migrate only when needed" approach to Neovim configuration. Config lives in real `.lua` files, deployed by home-manager.

**Platform note:** This skill describes the devbox setup where home-manager fully owns nvim. On Darwin, dotfiles still manages nvim and we only overlay `ccremote.lua`. See [gradual-dotfiles-migration](../gradual-dotfiles-migration/SKILL.md) for Darwin migration patterns.

## Architecture

```
assets/nvim/lua/user/*.lua    →    ~/.config/nvim/lua/user/*.lua
                                         ↑
                              extraLuaConfig does require("user.*")
```

Home-manager's `programs.neovim` owns `~/.config/nvim/init.vim`. We avoid collisions by only managing files under `lua/user/`.

## Current Setup

**users/dev/home.nix:**
```nix
programs.neovim = {
  enable = true;
  defaultEditor = true;
  viAlias = true;
  vimAlias = true;
  extraLuaConfig = ''
    require("user.settings")
    require("user.mappings")
  '';
};

xdg.configFile."nvim/lua/user" = {
  source = "${assetsPath}/nvim/lua/user";
  recursive = true;
};
```

**assets/nvim/lua/user/settings.lua:**
```lua
vim.g.clipboard = "osc52"           -- OSC 52 clipboard provider
vim.opt.clipboard = "unnamedplus"   -- Sync unnamed register with +
```

**assets/nvim/lua/user/mappings.lua:**
```lua
vim.keymap.set("t", "<C-w>a", [[<C-\><C-n>]], { noremap = true, silent = true })
```

## Adding New Config

1. **Create a Lua file** in `assets/nvim/lua/user/`:
   ```lua
   -- assets/nvim/lua/user/options.lua
   vim.opt.number = true
   vim.opt.relativenumber = true
   ```

2. **Add the require** in `home.nix`:
   ```nix
   extraLuaConfig = ''
     require("user.settings")
     require("user.options")
     require("user.mappings")
   '';
   ```

3. **Apply**: `home-manager switch --flake .#dev`

## Plugin Strategy

**Current approach: lazy.nvim (not Nix-managed)**

When you need plugins, bootstrap lazy.nvim in your Lua config. It writes to `~/.local/share/nvim/`, which works fine on NixOS.

```lua
-- assets/nvim/lua/user/plugins.lua (future)
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({ "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git", lazypath })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  -- plugin specs here
})
```

**Alternative approaches (for later):**
- Nix-managed plugins via `programs.neovim.plugins` — more reproducible, but bigger migration
- Hybrid with `lazy-nix-helper.nvim` — lazy.nvim loads Nix store paths

Stick with lazy.nvim until you feel pain (offline builds, reproducibility needs).

## Key Files

| File | Purpose |
|------|---------|
| `users/dev/home.nix` | `extraLuaConfig` with requires |
| `assets/nvim/lua/user/` | Actual Lua config files |

## Gotchas

- **Don't create `assets/nvim/init.lua`** — home-manager owns that path via `programs.neovim`
- **The `lua/user/` directory is deployed recursively** — add files freely, they'll appear after `home-manager switch`
