---
name: decompiler
description: Decompile a function to C-like pseudocode for human-readable analysis. Use to understand function logic, review control flow, or prepare for code pattern matching.
---

# Decompiler

Decompile a function in a binary to C-like pseudocode.

## When to use

- View the decompiled source code of a function
- Analyze function logic and control flow
- Understand what a function does before deeper analysis

## Instructions

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`), adapting it as needed:
```lua
local d = project:decompile(<target_function>)

return tostring(d)
```

Possible values for `<target_function>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as an AddressValue
  - To build an AddressValue, use for example: `AddressValue.new(0x1234)`
- A regex, e.g. `{matching = "<regex>", kind = "symbol", all = true}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes", all = true}`

> `all` is a boolean. If set to `true`, it returns a table containing all matching functions. If `false` (default), it returns only the first matching value. The for loop is not necessary if the function target is only one (i.e. `all` is not set to true)


Returns the decompiled C-like pseudocode as a string.

## Related Skills

- **functions** (`/functions`) — Use this skill to locate specific functions by name, address, pattern, or behavioral criteria (e.g., functions that call a particular API) before decompiling them.
- **code-pattern-matching** (`/code-pattern-matching`) - Search for specific code patterns in the decompiled output