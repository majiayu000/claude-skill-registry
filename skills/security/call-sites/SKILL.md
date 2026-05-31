---
name: call-sites
description: Find all locations where functions are called in a binary. Use when analyzing callers of a function, checking call relationships, or identifying which functions invoke a specific API.
---

# Call Sites

Find function call sites in a binary.

## When to use

- Find all locations where a specific function is called
- Identify callers of a function
- Check if a function contains calls to other specific functions
- Filter call sites based on caller criteria

## Instructions

### List function calls

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`) to get all the function calls:
```lua
local calls = project:calls_matching{
  to = <target_call>,
}

local results = {}
for _, call in ipairs(calls) do
  table.insert(results, {
      caller_address = tostring(call.caller_address),
      call_address = tostring(call.call_address),
    })
end

return results
```

Possible values for `<target_call>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as AddressValue instances
  - Create one with `AddressValue.new(<hex_addr>)` (e.g., `<hex_addr> = 0x1234`)
- A regex, e.g. `{matching = "<regex>", kind = "symbol"}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes"}`

Returns a JSON object containing:
- `caller_address` is the address of the function that makes the call
- `call_address` is the address of the call site (specifically, the code block address where the call is made)

#### List function calls with criteria

To restrict the search to function calls where the caller also contains other calls, or the caller is a specific function, use:
```lua
local calls = project:calls_matching{
  to = <target_call>,
  where = function(caller)
    return caller:named("<name>") and caller:has_call(<target_call>)
  end
}
```

### List function calls in a certain function

To verify whether a certain function calls another function, run:
```lua
local f = project:functions(<target_function>)
local has_call = f:has_call(<target_call>)

return tostring(has_call)
```

> The returned function object contains these fields: `f.name`, `f.address`, `f.total_bytes`

To get the list of call-sites within a function, run:
```lua
local f = project:functions(<target_function>)
local calls = f:calls(<target_call>)

local call_addresses = {}
for _, c in ipairs(calls) do
  table.insert(call_addresses, tostring(c))
end

return call_addresses
```

Possible values for `<target_function>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as an AddressValue
  - To build an AddressValue, use for example: `AddressValue.new(0x1234)`
- A regex, e.g. `{matching = "<regex>", kind = "symbol", all = true}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes", all = true}`

> `all` is a boolean. If set to `true`, it returns a table containing all matching functions. If `false` (default), it returns only the first matching value. The for loop is not necessary if the function target is only one (i.e. `all` is not set to true)


## References

- [calls-matching-param.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/calls-matching-param.md) - Input format for `calls_matching`
- [calls-matching-table.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/calls-matching-table.md) - Structure of the returned table from `calls_matching`

URLs to additional documentation pages are available at https://vulhunt.re/llm.txt

## Related Skills

- **functions** (`/functions`) - Use this skill first to find and list functions before analyzing their call sites
- **dataflow-analysis** (`/dataflow-analysis`) - For advanced call analysis with taint tracking and data flow between function parameters and arguments
- **decompiler** (`/decompiler`) - View decompiled code of caller functions to better understand the calling context
