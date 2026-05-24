---
name: nvim-config
description: Configure Neovim editor with init.lua, plugin management, LSP setup, keymaps, and options. Use when setting up Neovim, adding plugins, configuring language servers, or customizing keybindings. Keywords: neovim, nvim, init.lua, vim, plugin, LSP, keymap, configure, vimscript
allowed-tools: Read, Write, Edit, Bash(cat:*), Bash(nvim:*)
---

# Neovim Configuration Skill

Manages Neovim configuration through Lua-based init files and modular configuration structure.

## Important Context

This dotfiles repository has a **symlinked** Neovim configuration:
- Configuration location: `config/nvim/`
- Symlinked to: `~/.config/nvim/` (XDG standard)
- **All changes are applied globally** to the Neovim installation

**Current state:** Configuration directory exists but is empty (ready for initial setup)

## Neovim Configuration Structure

### Modern Lua-Based Configuration (Recommended)

```
config/nvim/
├── init.lua                    # Main entry point
├── lua/
│   ├── config/
│   │   ├── options.lua        # Editor options (tab size, line numbers, etc.)
│   │   ├── keymaps.lua        # Custom keybindings
│   │   ├── autocmds.lua       # Autocommands
│   │   └── lazy.lua           # Plugin manager setup (lazy.nvim)
│   └── plugins/
│       ├── lsp.lua            # LSP configuration
│       ├── treesitter.lua     # Syntax highlighting
│       ├── telescope.lua      # Fuzzy finder
│       └── ...                # Other plugin configs
└── after/
    └── plugin/                # Plugin-specific overrides
```

### Legacy Vimscript (For Vim Compatibility)

```
config/nvim/
├── init.vim                   # Main entry point (Vimscript)
├── plugin/                    # Plugin configurations
└── after/plugin/              # Late-loading configs
```

**Note:** Use either `init.lua` OR `init.vim`, not both. Lua is recommended for new configurations.

---

## Configuration Categories

### 1. Editor Options

Set in `lua/config/options.lua`:

```lua
-- Basic editor settings
vim.opt.number = true              -- Show line numbers
vim.opt.relativenumber = true      -- Relative line numbers
vim.opt.tabstop = 4                -- Tab width
vim.opt.shiftwidth = 4             -- Indent width
vim.opt.expandtab = true           -- Use spaces instead of tabs
vim.opt.smartindent = true         -- Auto-indent new lines

-- UI enhancements
vim.opt.termguicolors = true       -- True color support
vim.opt.signcolumn = "yes"         -- Always show sign column
vim.opt.wrap = false               -- No line wrapping
vim.opt.cursorline = true          -- Highlight current line

-- Search settings
vim.opt.ignorecase = true          -- Case-insensitive search
vim.opt.smartcase = true           -- Case-sensitive if uppercase used
vim.opt.hlsearch = true            -- Highlight search results

-- Split behavior
vim.opt.splitright = true          -- Vertical splits go right
vim.opt.splitbelow = true          -- Horizontal splits go below

-- Performance
vim.opt.updatetime = 250           -- Faster completion
vim.opt.timeoutlen = 300           -- Faster key sequence timeout

-- Backup and undo
vim.opt.backup = false             -- No backup files
vim.opt.swapfile = false           -- No swap files
vim.opt.undofile = true            -- Persistent undo
```

**Access via Vimscript:**
```vim
set number
set relativenumber
set tabstop=4
```

### 2. Keymaps

Set in `lua/config/keymaps.lua`:

```lua
-- Set leader key
vim.g.mapleader = " "              -- Space as leader key
vim.g.maplocalleader = " "

-- Helper function for mappings
local map = function(mode, lhs, rhs, opts)
  opts = opts or {}
  opts.silent = opts.silent ~= false
  vim.keymap.set(mode, lhs, rhs, opts)
end

-- General mappings
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear highlights" })

-- Window navigation
map("n", "<C-h>", "<C-w>h", { desc = "Move to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Move to bottom window" })
map("n", "<C-k>", "<C-w>k", { desc = "Move to top window" })
map("n", "<C-l>", "<C-w>l", { desc = "Move to right window" })

-- Window resizing
map("n", "<C-Up>", "<cmd>resize +2<cr>", { desc = "Increase height" })
map("n", "<C-Down>", "<cmd>resize -2<cr>", { desc = "Decrease height" })
map("n", "<C-Left>", "<cmd>vertical resize -2<cr>", { desc = "Decrease width" })
map("n", "<C-Right>", "<cmd>vertical resize +2<cr>", { desc = "Increase width" })

-- Buffer navigation
map("n", "<S-h>", "<cmd>bprevious<cr>", { desc = "Previous buffer" })
map("n", "<S-l>", "<cmd>bnext<cr>", { desc = "Next buffer" })

-- Better indenting
map("v", "<", "<gv")
map("v", ">", ">gv")

-- Move lines
map("n", "<A-j>", "<cmd>m .+1<cr>==", { desc = "Move line down" })
map("n", "<A-k>", "<cmd>m .-2<cr>==", { desc = "Move line up" })
map("v", "<A-j>", ":m '>+1<cr>gv=gv", { desc = "Move selection down" })
map("v", "<A-k>", ":m '<-2<cr>gv=gv", { desc = "Move selection up" })
```

**Mapping modes:**
- `n` - Normal mode
- `i` - Insert mode
- `v` - Visual mode
- `x` - Visual block mode
- `t` - Terminal mode
- `c` - Command mode

### 3. Plugin Management (lazy.nvim)

Set in `lua/config/lazy.lua`:

```lua
-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Configure plugins
require("lazy").setup({
  spec = {
    { import = "plugins" },     -- Import all plugin specs from lua/plugins/
  },
  defaults = {
    lazy = false,               -- Load plugins immediately
    version = false,            -- Use latest git commit
  },
  install = { colorscheme = { "habamax" } },
  checker = { enabled = true }, -- Check for updates
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
```

**Plugin specification format:**
```lua
return {
  "plugin-author/plugin-name",
  dependencies = { "dependency-plugin" },
  config = function()
    -- Plugin configuration
  end,
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find files" },
  },
  event = "VeryLazy",           -- Lazy load on event
  cmd = "PluginCommand",        -- Lazy load on command
  ft = "filetype",              -- Lazy load on filetype
}
```

### 4. LSP Configuration

Set in `lua/plugins/lsp.lua`:

```lua
return {
  "neovim/nvim-lspconfig",
  dependencies = {
    "williamboman/mason.nvim",           -- LSP installer
    "williamboman/mason-lspconfig.nvim", -- Mason-lspconfig bridge
    "hrsh7th/cmp-nvim-lsp",              -- LSP completion source
  },
  config = function()
    -- Mason setup (LSP installer)
    require("mason").setup()
    require("mason-lspconfig").setup({
      ensure_installed = {
        "lua_ls",        -- Lua
        "rust_analyzer", -- Rust
        "gopls",         -- Go
        "pyright",       -- Python
        "ts_ls",         -- TypeScript
      },
    })

    -- LSP keymaps (set on attach)
    local on_attach = function(client, bufnr)
      local map = function(keys, func, desc)
        vim.keymap.set("n", keys, func, { buffer = bufnr, desc = "LSP: " .. desc })
      end

      map("gd", vim.lsp.buf.definition, "Goto Definition")
      map("gr", vim.lsp.buf.references, "Goto References")
      map("gI", vim.lsp.buf.implementation, "Goto Implementation")
      map("<leader>D", vim.lsp.buf.type_definition, "Type Definition")
      map("<leader>rn", vim.lsp.buf.rename, "Rename")
      map("<leader>ca", vim.lsp.buf.code_action, "Code Action")
      map("K", vim.lsp.buf.hover, "Hover Documentation")
    end

    -- Capabilities (for completion)
    local capabilities = require("cmp_nvim_lsp").default_capabilities()

    -- Server configurations
    local lspconfig = require("lspconfig")

    lspconfig.lua_ls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        Lua = {
          diagnostics = { globals = { "vim" } },
          workspace = { checkThirdParty = false },
          telemetry = { enable = false },
        },
      },
    })

    lspconfig.rust_analyzer.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        ["rust-analyzer"] = {
          cargo = { allFeatures = true },
          checkOnSave = { command = "clippy" },
        },
      },
    })

    lspconfig.gopls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        gopls = {
          analyses = {
            unusedparams = true,
          },
          staticcheck = true,
        },
      },
    })
  end,
}
```

### 5. Autocommands

Set in `lua/config/autocmds.lua`:

```lua
-- Highlight on yank
vim.api.nvim_create_autocmd("TextYankPost", {
  callback = function()
    vim.highlight.on_yank()
  end,
})

-- Auto-format on save
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.go",
  callback = function()
    vim.lsp.buf.format()
  end,
})

-- Close certain filetypes with 'q'
vim.api.nvim_create_autocmd("FileType", {
  pattern = { "help", "qf", "man", "notify" },
  callback = function(event)
    vim.bo[event.buf].buflisted = false
    vim.keymap.set("n", "q", "<cmd>close<cr>", { buffer = event.buf, silent = true })
  end,
})

-- Restore cursor position
vim.api.nvim_create_autocmd("BufReadPost", {
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    if mark[1] > 0 and mark[1] <= vim.api.nvim_buf_line_count(0) then
      vim.api.nvim_win_set_cursor(0, mark)
    end
  end,
})
```

---

## Main Entry Point (init.lua)

**Minimal structure:**

```lua
-- Set leader keys before loading plugins
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Load core configurations
require("config.options")
require("config.keymaps")
require("config.autocmds")
require("config.lazy")  -- Plugin manager setup
```

---

## Essential Plugins

### Core Plugins

**1. Color Scheme:**
```lua
-- lua/plugins/colorscheme.lua
return {
  "folke/tokyonight.nvim",
  lazy = false,
  priority = 1000,
  config = function()
    vim.cmd([[colorscheme tokyonight-night]])
  end,
}
```

**2. Treesitter (Syntax Highlighting):**
```lua
-- lua/plugins/treesitter.lua
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  config = function()
    require("nvim-treesitter.configs").setup({
      ensure_installed = { "lua", "vim", "rust", "go", "python", "typescript" },
      highlight = { enable = true },
      indent = { enable = true },
    })
  end,
}
```

**3. Telescope (Fuzzy Finder):**
```lua
-- lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find files" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "Live grep" },
    { "<leader>fb", "<cmd>Telescope buffers<cr>", desc = "Buffers" },
  },
}
```

**4. Completion (nvim-cmp):**
```lua
-- lua/plugins/completion.lua
return {
  "hrsh7th/nvim-cmp",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-path",
    "L3MON4D3/LuaSnip",
  },
  config = function()
    local cmp = require("cmp")
    cmp.setup({
      mapping = cmp.mapping.preset.insert({
        ["<C-b>"] = cmp.mapping.scroll_docs(-4),
        ["<C-f>"] = cmp.mapping.scroll_docs(4),
        ["<C-Space>"] = cmp.mapping.complete(),
        ["<CR>"] = cmp.mapping.confirm({ select = true }),
      }),
      sources = {
        { name = "nvim_lsp" },
        { name = "buffer" },
        { name = "path" },
      },
    })
  end,
}
```

---

## Workflow Instructions

### Initial Setup (Empty Configuration)

**Create minimal init.lua:**
```lua
-- config/nvim/init.lua
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
```

**Or create full modular structure:**
1. Create `init.lua` with module imports
2. Create `lua/config/` directory with options, keymaps, autocmds
3. Create `lua/plugins/` directory for plugin specs
4. Set up lazy.nvim plugin manager

### Modifying Existing Configuration

**Always start by reading:**
```
Read config/nvim/init.lua
Read config/nvim/lua/config/options.lua
Read config/nvim/lua/config/keymaps.lua
```

**Use Edit tool for precise changes:**
1. Read current configuration
2. Identify exact section to modify
3. Use Edit to replace specific content
4. Preserve Lua syntax and structure

### Adding Plugins

**Create new plugin spec:**
```lua
-- config/nvim/lua/plugins/myplugin.lua
return {
  "author/plugin-name",
  dependencies = {},
  config = function()
    -- Plugin setup
  end,
}
```

### Adding Keymaps

**Append to keymaps.lua:**
```lua
-- Add to lua/config/keymaps.lua
map("n", "<leader>gg", "<cmd>LazyGit<cr>", { desc = "Open LazyGit" })
```

### Configuring LSP Servers

**Add to mason ensure_installed:**
```lua
ensure_installed = {
  "lua_ls",
  "rust_analyzer",
  "new_server_name",  -- Add new server
}
```

**Add server-specific configuration:**
```lua
lspconfig.new_server.setup({
  on_attach = on_attach,
  capabilities = capabilities,
  settings = {
    -- Server-specific settings
  },
})
```

---

## Common Configuration Tasks

### 1. Set Theme

```lua
-- lua/plugins/colorscheme.lua
return {
  "catppuccin/nvim",
  name = "catppuccin",
  priority = 1000,
  config = function()
    vim.cmd([[colorscheme catppuccin-mocha]])
  end,
}
```

### 2. Configure Tab Behavior

```lua
-- lua/config/options.lua
vim.opt.tabstop = 2        -- Tab width
vim.opt.shiftwidth = 2     -- Indent width
vim.opt.expandtab = true   -- Use spaces
```

### 3. Enable Format on Save

```lua
-- lua/config/autocmds.lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*",
  callback = function()
    vim.lsp.buf.format()
  end,
})
```

### 4. Add File Explorer (neo-tree)

```lua
-- lua/plugins/neo-tree.lua
return {
  "nvim-neo-tree/neo-tree.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  keys = {
    { "<leader>e", "<cmd>Neotree toggle<cr>", desc = "Toggle file explorer" },
  },
}
```

### 5. Configure Go Development

```lua
-- Ensure gopls is installed
ensure_installed = { "gopls" }

-- Add Go-specific settings
lspconfig.gopls.setup({
  on_attach = on_attach,
  capabilities = capabilities,
  settings = {
    gopls = {
      gofumpt = true,              -- Use gofumpt formatter
      analyses = {
        unusedparams = true,
        shadow = true,
      },
      staticcheck = true,
    },
  },
})

-- Auto-format Go files on save
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.go",
  callback = function()
    vim.lsp.buf.format()
  end,
})
```

---

## Best Practices

1. **Modular structure** - Separate options, keymaps, plugins into distinct files
2. **Lazy loading** - Use lazy.nvim to load plugins on demand
3. **Descriptive keymaps** - Always include `desc` for which-key integration
4. **LSP-first** - Use LSP for language features instead of custom scripts
5. **Persistent undo** - Enable `undofile` for undo history across sessions
6. **Leader key** - Use space as leader for custom mappings
7. **Performance** - Disable unused built-in plugins in lazy.nvim config

## Neovim-Specific Features

**Lua API advantages:**
- Better performance than Vimscript
- Native async support
- Cleaner syntax for configuration
- First-class LSP support

**XDG Base Directory:**
- Config: `~/.config/nvim/`
- Data: `~/.local/share/nvim/`
- State: `~/.local/state/nvim/`
- Cache: `~/.cache/nvim/`

**Built-in LSP:**
- No plugin required for basic LSP functionality
- Use `vim.lsp.buf.*` for LSP operations
- Configure servers via `nvim-lspconfig`

---

## Troubleshooting

### Check Configuration Location

```vim
:echo stdpath('config')  " Should show ~/.config/nvim
```

### Reload Configuration

```vim
:source $MYVIMRC         " Reload init file
:Lazy sync               " Update plugins
```

### Check Plugin Status

```vim
:Lazy                    " Open plugin manager UI
:checkhealth             " Run health checks
```

### LSP Issues

```vim
:LspInfo                 " Check attached servers
:Mason                   " Manage LSP servers
:LspRestart              " Restart LSP servers
```

### Verify Symlink

```bash
ls -la ~/.config/nvim    # Should point to dotfiles/config/nvim
```

---

## Quick Reference

**Current Configuration:**
- Location: `config/nvim/` (symlinked to `~/.config/nvim/`)
- State: Empty (ready for initial setup)
- Format: Lua-based (recommended)

**Standard Init Structure:**
```
init.lua                 → Main entry point
lua/config/
  ├── options.lua        → Editor settings
  ├── keymaps.lua        → Keybindings
  ├── autocmds.lua       → Autocommands
  └── lazy.lua           → Plugin manager
lua/plugins/
  ├── colorscheme.lua    → Theme
  ├── lsp.lua            → LSP configuration
  ├── treesitter.lua     → Syntax highlighting
  └── ...                → Other plugins
```

**Essential Commands:**
- `:Lazy` - Plugin manager
- `:Mason` - LSP server installer
- `:checkhealth` - Diagnostic checks
- `:LspInfo` - LSP status
- `:Telescope` - Fuzzy finder

**Useful Options:**
- `vim.opt.number` - Line numbers
- `vim.opt.expandtab` - Spaces instead of tabs
- `vim.opt.shiftwidth` - Indent width
- `vim.opt.termguicolors` - True color support
- `vim.opt.undofile` - Persistent undo
