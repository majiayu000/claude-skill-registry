---
name: functions
description: Find and list functions in a binary by name, address, regex, or byte pattern. Use as the starting point for binary analysis, to locate specific functions, or to enumerate all functions matching criteria.
---

# Functions

Find and list functions in a binary by name, address, or pattern.

## When to use

- Find a function by name or address
- List all functions matching a regex or byte pattern
- Get function metadata (address, size)
- Search for functions that match specific criteria (e.g., functions that call a certain API)

## Instructions

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`), adapting it as needed:
```lua
local fs = project:functions(<target_function>)

-- Single result (FunctionContext)
if type(fs) ~= "table" then
  return {
      function_name = tostring(fs.name),
      function_address = tostring(fs.address),
      function_total_bytes = tostring(fs.total_bytes)
  }
end

-- Multiple results (FunctionContext[])
local results = {}
for _, f in ipairs(fs) do
  table.insert(results, {
      function_name = tostring(f.name),
      function_address = tostring(f.address),
      function_total_bytes = tostring(f.total_bytes)
    })
end

return results
```

Possible values for `<target_function>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as an AddressValue
  - To build an AddressValue, use for example: `AddressValue.new(0x1234)`
- A regex, e.g. `{matching = "<regex>", kind = "symbol", all = true}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes", all = true}`

If no argument is passed to `project:functions()`, all functions are returned

> `all` is a boolean. If set to `true`, it returns a table containing all matching functions. If `false` (default), it returns only the first matching value. The for loop is not necessary if the function target is only one (i.e. `all` is not set to true)

Returns a JSON object containing:
- `function_name` is the function name
- `function_address` is the function address
- `function_total_bytes` is the function length in bytes, calculated as the sum of the sizes of all its code blocks

It is also possible to get all functions satisfying certain criteria:
```lua
local function search_criteria(f)
      return f:named(<target_call>) and f:has_call(<target_call>)
    end

local fs = project:functions_where(search_criteria)
```

Possible values for `<target_call>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as AddressValue instances
  - Create one with `AddressValue.new(<hex_addr>)` (e.g., `<hex_addr> = 0x1234`)
- A regex, e.g. `{matching = "<regex>", kind = "symbol"}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes"}`

## References

- [project-handle.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/project-handle.md) - All methods and fields for `project`
- [function-context.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/function-context.md) - All methods and fields for returned functions
- [calls-to-query.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/calls-to-query.md) - Format for `<target_call>` parameter

URLs to additional documentation pages are available at https://vulhunt.re/llm.txt

## Related Skills

- **decompiler** (`/decompiler`) - Decompile functions to understand their implementation and logic
- **call-sites** (`/call-sites`) - Find where functions are called and analyze their usage patterns
- **byte-pattern-matching** (`/byte-pattern-matching`) - Alternative method to find functions by searching for specific instruction sequences
- **dataflow-analysis** (`/dataflow-analysis`) - Track data flow within functions to detect vulnerabilities