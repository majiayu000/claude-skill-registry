---
name: skill-neovim-research
description: Research Neovim APIs, plugin patterns, and Lua development. Invoke for lua-language research tasks.
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
context:
  - project/neovim/domain/neovim-api.md
  - project/neovim/domain/lua-patterns.md
  - project/neovim/domain/plugin-ecosystem.md
---

# Neovim Research Skill

Specialized research agent for Neovim configuration and Lua plugin development tasks.

## Trigger Conditions

This skill activates when:
- Task language is "lua"
- Research involves Neovim APIs, plugins, or configuration
- Codebase exploration for Lua patterns is needed

## Research Strategies

### 1. Local Codebase First

Always check existing code first:
```
1. Grep for relevant patterns in lua/ and after/
2. Glob for similar modules in lua/neotex/
3. Read existing implementations
4. Understand existing patterns before proposing new ones
```

### 2. Neovim API Research

For Neovim-specific patterns:
```
1. WebSearch "neovim lua {concept}"
2. WebFetch neovim.io documentation
3. Check existing patterns in lua/neotex/core/
4. Reference the neovim-lua.md rule for standards
```

### 3. Plugin Research

For plugin-specific patterns:
```
1. Read plugin documentation via WebFetch
2. Check existing plugin configs in lua/neotex/plugins/
3. Search GitHub repos for patterns
4. Review plugin-specific tests in tests/
```

## Research Areas

### Neovim API Patterns
- vim.api.* (buffer, window, command APIs)
- vim.fn.* (Vimscript function bridge)
- vim.opt.* (option setting)
- vim.keymap.set() (keymapping)
- vim.api.nvim_create_autocmd() (autocommands)
- vim.lsp.* (language server protocol)

### Plugin APIs
- lazy.nvim (plugin management, lazy loading)
- telescope.nvim (fuzzy finder patterns)
- nvim-treesitter (syntax parsing)
- nvim-lspconfig (LSP configuration)
- which-key.nvim (keybinding documentation)

### Lua Patterns
- Module structure (local M = {})
- Error handling (pcall)
- Table manipulation
- String patterns
- Metatable usage

### Testing Patterns
- busted framework
- plenary.nvim test utilities
- Assertion patterns (is_nil/is_not_nil for match)
- Test organization (*_spec.lua)

### Configuration Patterns
- Options organization
- Keymap centralization
- Autocommand grouping
- Plugin lazy loading strategies

## Execution Flow

```
1. Receive task context (description, focus)
2. Extract key concepts (API type, plugin, pattern)
3. Search local codebase for related patterns
4. Search web for Neovim/plugin documentation
5. Analyze implementation approaches
6. Synthesize findings
7. Create research report
8. Return results
```

## Research Report Format

Create report at `.claude/specs/{N}_{SLUG}/reports/research-{NNN}.md`:

```markdown
# Neovim Research Report: Task #{N}

**Task**: {title}
**Date**: {date}
**Focus**: {focus}

## Summary

{Overview of findings}

## Codebase Findings

### Related Files
- `lua/neotex/path/to/file.lua` - {description}

### Existing Patterns
```lua
-- Pattern name
local function example()
  -- ...
end
```

### Similar Implementations
- {Description of similar code}

## Neovim API Findings

### Relevant APIs
| API | Purpose | Example |
|-----|---------|---------|
| `vim.api.nvim_*` | {purpose} | {code} |

### Best Practices
- {Practice and rationale}

## Plugin Integration

### Related Plugins
- {Plugin} - {how it relates}

### Integration Patterns
- {Pattern description}

## Recommended Approach

1. {Step 1 with specific patterns to use}
2. {Step 2}

## Code Sketch

```lua
-- Proposed implementation approach
local M = {}

function M.setup(opts)
  -- ...
end

return M
```

## Testing Strategy

- Unit tests: {approach with busted}
- Integration tests: {approach with plenary}

## Potential Challenges

- {Challenge and mitigation}

## References

- {Neovim documentation links}
- {Plugin documentation links}
- {Related codebase files}
```

## Return Format

```json
{
  "status": "completed",
  "summary": "Found N relevant patterns for implementation",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/reports/research-001.md",
      "type": "research",
      "description": "Neovim/Lua research report"
    }
  ],
  "patterns_found": [
    {"name": "pattern_name", "location": "lua/neotex/file.lua", "relevance": "high"}
  ],
  "apis_needed": [
    "vim.api.nvim_create_autocmd",
    "vim.keymap.set"
  ],
  "plugins_relevant": [
    {"name": "telescope.nvim", "relevance": "integration point"}
  ],
  "recommended_approach": "Description of recommended approach"
}
```

## Key Resources

### Official Documentation
- https://neovim.io/doc/user/lua.html - Neovim Lua guide
- https://neovim.io/doc/user/api.html - Neovim API reference
- https://neovim.io/doc/user/lsp.html - LSP integration

### Plugin Documentation
- https://lazy.folke.io/ - lazy.nvim plugin manager
- https://github.com/nvim-telescope/telescope.nvim - Fuzzy finder
- https://github.com/nvim-treesitter/nvim-treesitter - Syntax parsing
- https://luals.github.io/ - Lua language server

### Community Resources
- https://github.com/nanotee/nvim-lua-guide - Comprehensive Lua guide
- https://github.com/rockerBOO/awesome-neovim - Plugin collection

## Key Codebase Locations

- **Entry point**: `nvim/init.lua`
- **Core config**: `nvim/lua/neotex/config/`
- **Plugin configs**: `nvim/lua/neotex/plugins/`
- **Core utilities**: `nvim/lua/neotex/core/`
- **Utilities**: `nvim/lua/neotex/util/`
- **Tests**: `nvim/tests/`
- **Standards**: `nvim/CLAUDE.md`, `nvim/docs/CODE_STANDARDS.md`
- **Rules**: `.claude/rules/neovim-lua.md`

## Quick Exploration Commands

```lua
-- Check available API functions
:lua print(vim.inspect(vim.api))

-- Check option values
:lua print(vim.inspect(vim.opt.tabstop:get()))

-- Check loaded modules
:lua print(vim.inspect(package.loaded))

-- Find keymap conflicts
:verbose map <key>
```
