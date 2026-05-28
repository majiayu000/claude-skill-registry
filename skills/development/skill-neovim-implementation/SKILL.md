---
name: skill-neovim-implementation
description: Implement Neovim plugins and configurations with TDD. Invoke for lua-language implementation tasks.
allowed-tools: Read, Write, Edit, Bash(nvim:*, luacheck)
context:
  - project/neovim/standards/lua-style-guide.md
  - project/neovim/standards/testing-standards.md
  - project/neovim/patterns/plugin-definition.md
---

# Neovim Implementation Skill

Specialized implementation agent for Neovim configuration and Lua plugin development with test-driven development.

## Trigger Conditions

This skill activates when:
- Task language is "lua"
- Implementation involves Neovim plugins, configurations, or utilities
- /implement command is invoked for a Lua task
- Plan exists with phases ready for execution

## TDD Workflow

Follow strict test-driven development:

```
1. Load implementation plan
2. Identify target functionality
3. Write failing test first (busted/plenary)
4. Implement minimal code to pass
5. Run test to verify pass
6. Refactor while tests pass
7. Repeat for each feature
8. Verify with full test suite
```

### TDD Rules

1. **Write test first** - Never implement without a failing test
2. **Minimal implementation** - Only write code to make the test pass
3. **Refactor under green** - Only refactor when all tests pass
4. **One feature at a time** - Focus on single functionality per cycle

## Testing Commands

### Run All Tests

```bash
# Run all tests with plenary
nvim --headless -c "PlenaryBustedDirectory tests/"

# With minimal init (faster, isolated)
nvim --headless -c "PlenaryBustedDirectory tests/ {minimal_init = 'tests/minimal_init.lua'}"
```

### Run Specific Tests

```bash
# Run single test file
nvim --headless -c "PlenaryBustedFile tests/path/to/spec.lua"

# Run tests matching pattern
nvim --headless -c "PlenaryBustedDirectory tests/ {pattern = 'picker'}"
```

### Lint Lua Code

```bash
# Check for syntax errors
luacheck lua/ --codes

# Check specific file
luacheck lua/neotex/path/to/file.lua
```

## Test File Structure

Create test files following this pattern:

```lua
-- tests/module_name_spec.lua
describe("ModuleName", function()
  local module

  before_each(function()
    -- Reset state before each test
    package.loaded["neotex.module_name"] = nil
    module = require("neotex.module_name")
  end)

  describe("function_name", function()
    it("should do expected behavior", function()
      local result = module.function_name(input)
      assert.equals(expected, result)
    end)

    it("should handle edge case", function()
      local result = module.function_name(edge_input)
      assert.is_nil(result)
    end)
  end)
end)
```

### Assertion Patterns

```lua
-- Use is_nil/is_not_nil for pattern matching
assert.is_not_nil(str:match("pattern"))   -- Match found
assert.is_nil(str:match("pattern"))       -- Match not found

-- Equality
assert.equals(expected, actual)
assert.same(expected_table, actual_table)

-- Boolean
assert.is_true(condition)
assert.is_false(condition)

-- Errors
assert.has_error(function() error_func() end)
```

## Module Structure Patterns

### Lua Module Directory

```
nvim/
├── lua/neotex/
│   ├── core/           # Core utilities (loader, options, keymaps)
│   │   └── module.lua
│   ├── plugins/        # Plugin configurations
│   │   ├── ai/         # AI integrations
│   │   ├── editor/     # Editor enhancements
│   │   ├── lsp/        # Language server configs
│   │   ├── text/       # Format-specific (LaTeX, Markdown)
│   │   ├── tools/      # Development tools
│   │   └── ui/         # UI components
│   └── util/           # Utility functions
├── after/ftplugin/     # Filetype-specific settings
└── tests/              # Test suites
```

### Standard Module Template

```lua
-- lua/neotex/category/module-name.lua
local M = {}

--- Brief description of the module
--- @module neotex.category.module-name

--- Function description
--- @param input string Input parameter
--- @return string|nil result Result or nil on failure
function M.function_name(input)
  if not input then
    return nil
  end
  -- Implementation
  return result
end

--- Setup function for configuration
--- @param opts table? Optional configuration
function M.setup(opts)
  opts = opts or {}
  -- Apply configuration
end

return M
```

### Plugin Definition Pattern

```lua
-- lua/neotex/plugins/category/plugin-name.lua
return {
  "author/plugin-name",
  event = "VeryLazy",  -- or specific events: BufReadPre, InsertEnter
  dependencies = {
    "dep/plugin",
  },
  opts = {
    -- Configuration options passed to setup()
    option_key = "value",
  },
  config = function(_, opts)
    require("plugin-name").setup(opts)
  end,
}
```

### Complex Plugin with Keymaps

```lua
return {
  "author/plugin-name",
  event = "VeryLazy",
  keys = {
    { "<leader>xx", "<cmd>PluginCommand<cr>", desc = "Plugin: Description" },
    { "<leader>xy", function() require("plugin").action() end, desc = "Plugin: Action" },
  },
  opts = {
    -- Options
  },
  config = function(_, opts)
    local plugin = require("plugin-name")
    plugin.setup(opts)

    -- Additional configuration after setup
  end,
}
```

## Error Handling Patterns

### Using pcall for Safe Calls

```lua
local function safe_require(module_name)
  local ok, module = pcall(require, module_name)
  if not ok then
    vim.notify(
      "Failed to load " .. module_name .. ": " .. tostring(module),
      vim.log.levels.WARN
    )
    return nil
  end
  return module
end

-- Usage
local telescope = safe_require("telescope")
if telescope then
  telescope.setup({})
end
```

### Graceful Degradation

```lua
local function with_fallback(primary_fn, fallback_fn)
  local ok, result = pcall(primary_fn)
  if ok then
    return result
  end
  return fallback_fn()
end
```

### User Notifications

```lua
-- Info level
vim.notify("Operation completed", vim.log.levels.INFO)

-- Warning level
vim.notify("Missing optional dependency", vim.log.levels.WARN)

-- Error level
vim.notify("Critical error: " .. err, vim.log.levels.ERROR)
```

## Implementation Flow

```
1. Receive task context with plan path
2. Load and parse implementation plan
3. Find resume point (first non-completed phase)
4. For each remaining phase:
   a. Update phase status to [IN PROGRESS]
   b. Write tests for phase features
   c. Run tests (should fail)
   d. Implement features
   e. Run tests (should pass)
   f. Verify with luacheck
   g. Update phase status to [COMPLETED]
   h. Git commit
5. Run full test suite
6. Create implementation summary
7. Return results
```

## Summary Format

Create summary at `.claude/specs/{N}_{SLUG}/summaries/implementation-summary-{DATE}.md`:

```markdown
# Implementation Summary: Task #{N}

**Completed**: {date}
**Duration**: {time}

## Changes Made

{Overview of implemented features}

## Files Created

- `lua/neotex/path/to/file.lua` - {description}

## Files Modified

- `lua/neotex/path/to/file.lua` - {change description}

## Tests Added

- `tests/path/to/spec.lua` - {test coverage}

## Test Results

```
N tests passed
0 tests failed
Coverage: X%
```

## Verification

- All tests pass
- luacheck reports no errors
- Plugin loads correctly

## Notes

{Any important notes or follow-ups}
```

## Return Format

```json
{
  "status": "completed|partial",
  "summary": "Implementation complete with TDD",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/summaries/...",
      "type": "summary",
      "description": "Implementation summary"
    }
  ],
  "phases_completed": 3,
  "phases_total": 3,
  "files_created": [
    "lua/neotex/path/to/file.lua"
  ],
  "files_modified": [
    "lua/neotex/existing/file.lua"
  ],
  "tests_added": [
    "tests/path/to/spec.lua"
  ],
  "test_results": {
    "passed": 10,
    "failed": 0,
    "total": 10
  }
}
```

## Key Codebase Locations

- **Entry point**: `nvim/init.lua`
- **Core config**: `nvim/lua/neotex/config/`
- **Plugin configs**: `nvim/lua/neotex/plugins/`
- **Core utilities**: `nvim/lua/neotex/core/`
- **Utilities**: `nvim/lua/neotex/util/`
- **Tests**: `nvim/tests/`
- **Standards**: `nvim/CLAUDE.md`, `nvim/docs/CODE_STANDARDS.md`
- **Rules**: `.claude/rules/neovim-lua.md`

## Quality Standards

- **Indentation**: 2 spaces, expandtab
- **Line length**: ~100 characters
- **Naming**: lowercase_with_underscores
- **Comments**: LuaDoc style for public APIs
- **Error handling**: pcall for external dependencies
- **Testing**: All public APIs must have tests
