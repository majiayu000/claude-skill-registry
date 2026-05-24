---
name: lua-guide
description: |
  Lua language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Lua files (.lua), or when the user mentions Lua/LuaJIT/Neovim/Love2D.
  Provides table patterns, metatable guidelines, coroutine usage,
  and embedding conventions specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: lua
  extensions: ".lua"
---

# Lua Guide

> Applies to: Lua 5.4+, LuaJIT 2.1, Neovim Plugins, Love2D, Embedded Scripting

## Core Principles

1. **Tables Are Everything**: Arrays, maps, objects, modules, and namespaces -- master them
2. **Local by Default**: Always declare variables `local`; globals are a performance and correctness hazard
3. **Explicit Error Handling**: Use `pcall`/`xpcall` for recoverable errors; `error()` for programmer mistakes
4. **Minimal Metatables**: Use metatables for genuine OOP needs, not as decoration on simple data
5. **Embed-Friendly Design**: Lua exists to be embedded; keep the host/script boundary clean and narrow

## Guardrails

### Code Style

- Use `local` for every variable and function unless it must be global
- Naming: `snake_case` for variables/functions, `PascalCase` for class-like tables, `UPPER_SNAKE_CASE` for constants
- Indent with 2 spaces; one statement per line; avoid semicolons
- Use `[[ ... ]]` long strings for multi-line text and SQL/HTML templates
- Prefer `#tbl` over `table.getn()` for sequence length

### Tables

- Arrays are 1-based; `for i = 1, #arr` not `for i = 0, #arr - 1`
- Use `ipairs` for sequential iteration, `pairs` for hash-map iteration
- Do not mix array indices and string keys in the same table (undefined `#` behavior)
- Use `table.insert` / `table.remove` for array ops; avoid manual index gaps
- Freeze config tables by setting a `__newindex` metamethod that errors

### Error Handling

- Use `pcall(fn, ...)` to catch errors; `xpcall(fn, handler, ...)` for tracebacks
- Return `nil, err_msg` from functions that can fail (idiomatic two-value return)
- Reserve `error("msg", level)` for violated preconditions (programmer errors)
- Never silently swallow errors; always log or propagate

```lua
local function read_config(path)
  local f, err = io.open(path, "r")
  if not f then return nil, "cannot open config: " .. err end
  local content = f:read("*a")
  f:close()
  return content
end

local ok, result = xpcall(dangerous_operation, debug.traceback)
if not ok then log.error("failed: %s", result) end
```

### Performance

- Localize hot functions: `local insert = table.insert`
- Avoid closures inside hot loops (allocates every iteration)
- Use `table.concat` instead of `..` concatenation in loops
- LuaJIT: avoid `pairs()` in hot paths (not JIT-compiled); prefer arrays with `ipairs`
- LuaJIT: use FFI (`ffi.new`, `ffi.cast`) for C struct access instead of Lua tables

### Embedding

- Keep the Lua-to-host API surface small (<20 registered functions)
- Validate all arguments from Lua in C/host bindings
- Set memory limits via `lua_setallocf` or `lua_gc` configuration
- Use `debug.sethook` instruction-count hooks for untrusted scripts

## Key Patterns

### Module Pattern

```lua
local M = {}
local TIMEOUT_MS = 5000

local function validate(data)
  assert(type(data) == "table", "expected table, got " .. type(data))
  assert(data.name, "missing required field: name")
end

function M.process(data)
  validate(data)
  return { status = "ok", name = data.name }
end

return M
```

### OOP via Metatables

```lua
local Animal = {}
Animal.__index = Animal

function Animal.new(name, sound)
  return setmetatable({ name = name, sound = sound }, Animal)
end

function Animal:speak()
  return string.format("%s says %s", self.name, self.sound)
end

-- Inheritance
local Dog = setmetatable({}, { __index = Animal })
Dog.__index = Dog

function Dog.new(name)
  return setmetatable(Animal.new(name, "woof"), Dog)
end

function Dog:fetch(item)
  return string.format("%s fetches the %s", self.name, item)
end
```

### Coroutines

```lua
local function producer(items)
  return coroutine.wrap(function()
    for _, item in ipairs(items) do
      coroutine.yield(item)
    end
  end)
end

local function filter(predicate, iter)
  return coroutine.wrap(function()
    for item in iter do
      if predicate(item) then coroutine.yield(item) end
    end
  end)
end

local nums = producer({ 1, 2, 3, 4, 5, 6 })
local evens = filter(function(n) return n % 2 == 0 end, nums)
for v in evens do print(v) end  --> 2, 4, 6
```

### Custom Iterator

```lua
local function range(start, stop, step)
  step = step or 1
  local i = start - step
  return function()
    i = i + step
    if i <= stop then return i end
  end
end

for n in range(1, 10, 2) do print(n) end  --> 1, 3, 5, 7, 9
```

### Neovim Lua API

```lua
local api, keymap = vim.api, vim.keymap
local M = {}

function M.setup(opts)
  opts = vim.tbl_deep_extend("force", { enabled = true, width = 80 }, opts or {})
  if not opts.enabled then return end

  local group = api.nvim_create_augroup("MyPlugin", { clear = true })
  api.nvim_create_autocmd("BufWritePre", {
    group = group, pattern = "*.lua",
    callback = function(ev)
      local lines = api.nvim_buf_get_lines(ev.buf, 0, -1, false)
      for i, line in ipairs(lines) do lines[i] = line:gsub("%s+$", "") end
      api.nvim_buf_set_lines(ev.buf, 0, -1, false, lines)
    end,
  })

  keymap.set("n", "<leader>mp", function()
    vim.notify("MyPlugin activated", vim.log.levels.INFO)
  end, { desc = "Activate MyPlugin" })
end

return M
```

## Testing

### Busted (Recommended)

```lua
local mymodule = require("mymodule")

describe("mymodule.process", function()
  it("returns ok for valid input", function()
    local result = mymodule.process({ name = "test" })
    assert.are.equal("ok", result.status)
  end)

  it("raises on missing name", function()
    assert.has_error(function() mymodule.process({}) end, "missing required field: name")
  end)
end)
```

### Testing Standards

- Test files: `spec/*_spec.lua` (busted) or `test_*.lua` (luaunit)
- Test names describe behavior: `it("returns nil when file not found")`
- Coverage: >80% for library modules, >60% overall
- Test edge cases: `nil`, empty tables, boundary values, type mismatches
- Run: `busted --verbose`

## Tooling

### Luacheck

```lua
-- .luacheckrc
std = "lua54+busted"          -- or "luajit+busted"
globals = { "vim" }           -- for Neovim plugins
max_line_length = 120
max_cyclomatic_complexity = 10
```

### StyLua

```toml
# stylua.toml
column_width = 100
indent_type = "Spaces"
indent_width = 2
quote_style = "AutoPreferDouble"
call_parentheses = "Always"
```

### Essential Commands

```bash
lua myfile.lua                # Run Lua script
luajit myfile.lua             # Run with LuaJIT
busted --verbose              # Run tests
luacheck .                    # Lint
stylua .                      # Format
luarocks install busted       # Install test framework
luarocks install luacheck     # Install linter
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- OOP via metatables, module patterns, coroutine pipelines

## External References

- [Lua 5.4 Reference Manual](https://www.lua.org/manual/5.4/)
- [Programming in Lua (4th ed)](https://www.lua.org/pil/)
- [LuaJIT Documentation](https://luajit.org/luajit.html)
- [LuaJIT FFI Tutorial](https://luajit.org/ext_ffi_tutorial.html)
- [Neovim Lua Guide](https://neovim.io/doc/user/lua-guide.html)
- [Busted Testing Framework](https://lunarmodules.github.io/busted/)
- [Luacheck Linter](https://github.com/mpeterv/luacheck)
- [StyLua Formatter](https://github.com/JohnnyMorganz/StyLua)
- [Love2D Wiki](https://love2d.org/wiki/Main_Page)
- [Lua Style Guide](https://github.com/Olivine-Labs/lua-style-guide)
