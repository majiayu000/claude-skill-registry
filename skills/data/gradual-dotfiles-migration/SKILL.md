---
name: gradual-dotfiles-migration
description: How to progressively migrate config from dotfiles to home-manager on Darwin. Use when moving shell config, nvim config, or other dotfiles-managed files to workstation.
---

# Gradual Dotfiles Migration

On Darwin, dotfiles and home-manager coexist. This skill covers how to migrate config safely without breaking the working system.

## The Setup

| Platform | Config Source | Notes |
|----------|---------------|-------|
| **Devbox** | Workstation (home-manager) | Full control, no dotfiles |
| **Darwin** | Dotfiles + workstation overlay | Gradual migration in progress |

On Darwin, `home.darwin.nix` disables several home-manager programs to avoid conflicts:

```nix
programs.bash.enable = lib.mkForce false;    # dotfiles owns .bashrc
programs.neovim.enable = lib.mkForce false;  # dotfiles owns nvim
programs.ssh.enable = lib.mkForce false;     # dotfiles owns .ssh/config
# GPG is now fully migrated to home-manager (services.gpg-agent)
```

## The Key Limitation

**Home-manager cannot overlay files into a symlinked directory.**

If dotfiles creates `~/.config/nvim/lua/user/` as a symlink to the dotfiles repo, home-manager cannot deploy individual files into it. It will try to create a real directory, breaking the symlink and all other files in that directory.

### What Doesn't Work

```nix
# DON'T DO THIS if dotfiles symlinks the parent directory
xdg.configFile."nvim/lua" = {
  source = "${assetsPath}/nvim/lua";
  recursive = true;
  force = true;  # This won't help - it still breaks the symlink
};
```

### What Works

**Option 1: Deploy individual files to a non-symlinked location**

```nix
# Safe: ccremote.lua is a single file, not inside a symlinked directory
xdg.configFile."nvim/lua/ccremote.lua".source = "${assetsPath}/nvim/lua/ccremote.lua";
```

**Option 2: Let dotfiles own the entire directory**

Keep the config in dotfiles until ready to migrate the whole thing at once.

**Option 3: Full migration (flip the switch)**

```nix
# Enable home-manager to own the program entirely
programs.neovim.enable = true;  # Remove the mkForce false

# Now home-manager owns ~/.config/nvim/ - remove from dotfiles first!
```

## Safe Migration Patterns

### Pattern 1: Single File Deployment

Best for: Adding one new file that doesn't conflict with dotfiles structure.

```nix
# Works: deploying a single file alongside dotfiles-managed files
xdg.configFile."nvim/lua/ccremote.lua".source = "${assetsPath}/nvim/lua/ccremote.lua";
```

Requires: The target path must not be inside a symlinked directory.

**When deploying Lua modules that Lazy needs to load**, update the Lazy plugin spec to require it:

```lua
-- In deprecated-dotfiles lua/plugins/vim-obsession.lua
{
  "tpope/vim-obsession",
  config = function()
    require("user.sessions")  -- Loads HM-deployed module
  end,
}
```

### Pattern 2: Nix Plugin Without Init.lua Takeover

Best for: Installing a Nix-managed plugin on Darwin while dotfiles still owns init.lua.

Neovim auto-loads plugins from `~/.local/share/nvim/site/pack/*/start/`. Use `xdg.dataFile` to install there:

```nix
# Install vim-obsession via Nix, but let dotfiles keep init.lua
xdg.dataFile."nvim/site/pack/nix/start/vim-obsession" = {
  source = pkgs.vimPlugins.vim-obsession;
  recursive = true;
};
```

Then either:
- Remove/disable the Lazy spec for that plugin, OR
- Keep Lazy spec but mark it disabled when Nix version exists

This lets you migrate plugins one-by-one from Lazy to Nix without big-bang neovim migration.

### Pattern 3: Parallel Directory

Best for: New functionality that dotfiles doesn't have.

```nix
# Works: creating a new directory that dotfiles doesn't manage
xdg.configFile."myapp/config" = {
  source = "${assetsPath}/myapp/config";
  recursive = true;
};
```

### Pattern 5: Full Program Migration

Best for: When you're ready to move everything at once.

1. **On Darwin, remove from dotfiles first:**
   ```bash
   cd ~/Code/deprecated-dotfiles
   rm -rf .config/nvim
   git commit -am "chore: migrate nvim to workstation"
   ```

2. **Enable in home-manager:**
   ```nix
   # Remove the mkForce false
   programs.neovim.enable = true;
   ```

3. **Apply:**
   ```bash
   darwin-rebuild switch --flake .#hostname
   ```

### Pattern 6: prepareForHM Cleanup

For files that might exist from dotfiles, add cleanup:

```nix
home.activation.prepareForHM = lib.hm.dag.entryBefore ["checkLinkTargets"] ''
  rm -f ~/.config/nvim/lua/ccremote.lua 2>/dev/null || true
'';
```

### Pattern 7: NVIM_APPNAME for Parallel Testing

Best for: Testing a new neovim config without breaking the existing one.

Neovim supports `NVIM_APPNAME` to select a separate config/data/state namespace:

```bash
# Run with workstation-managed config
NVIM_APPNAME=nvim-workstation nvim

# Config lives in ~/.config/nvim-workstation/
# Data lives in ~/.local/share/nvim-workstation/
```

This lets you:
- Keep dotfiles config untouched as `nvim`
- Build new HM-managed config as `nvim-workstation`
- Flip between them with a shell alias
- Merge when ready

### Pattern 8: Resilient Lua Modules

Best for: Shared modules that might load before their dependencies.

When deploying Lua modules that depend on plugins (which may load in different order on Nix vs Lazy), make them resilient:

```lua
-- Check if Obsession command exists before using it
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    if vim.fn.exists(":Obsession") == 2 then
      vim.cmd("silent! Obsess")
    end
  end,
})
```

This removes ordering sensitivity between Nix packpath autoload vs Lazy event loading.

## Platform-Specific Config

Use conditionals when behavior differs between platforms:

```lua
-- In Lua files
if vim.env.SSH_TTY then
  vim.g.clipboard = "osc52"  -- Remote: use OSC 52
end
-- Local macOS uses native clipboard automatically
```

```nix
-- In Nix
lib.optionalAttrs (!pkgs.stdenv.isDarwin) {
  # Linux-only config
}
```

## Current Migration Status

| Program | Devbox | Darwin | Notes |
|---------|--------|--------|-------|
| Neovim | Workstation | Dotfiles + overlays | ccremote.lua, sessions.lua via Pattern 1 |
| Bash | Workstation | Dotfiles | Need full migration |
| SSH | Workstation | Dotfiles | Need full migration |
| GPG | Workstation | Workstation (pinentry-op) | 1Password Touch ID integration |
| Tmux | Workstation | Workstation | Fully migrated |
| Claude | Workstation | Workstation | Fully migrated |

## Detecting Drift

Dotfiles includes a verification script to detect missing or broken symlinks:

```bash
cd ~/Code/dotfiles  # or wherever your dotfiles clone is
./verify.sh         # Check all expected symlinks
./install.sh        # Fix any issues
```

The script:
- Checks core symlinks (shell, git, vim, nvim, tmux)
- Allows files to be managed by home-manager (won't flag nix store symlinks)
- Reports INFO for regular files that might be home-manager managed
- Returns exit code 1 if any errors found

Run `verify.sh` after migrations or if things break unexpectedly.

## Lessons Learned

1. **Don't try recursive overlay into symlinked directories** - it breaks everything
2. **Test on Darwin before pushing** - devbox success doesn't guarantee Darwin works
3. **Single file deployments are safest** during gradual migration
4. **Full migration is cleaner** when you're ready to move a whole program
5. **Run verify.sh after migrations** - catches missing symlinks early
6. **Nix plugins can coexist with Lazy** - use `xdg.dataFile` to install to pack path
7. **Update Lazy specs to load HM-deployed modules** - use `config = function() require(...) end`
8. **Make shared modules resilient** - check if dependencies exist before using them
