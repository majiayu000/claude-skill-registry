---
name: code-pattern-matching
description: Search for code patterns in decompiled output using Weggli semantic matching. Use when finding vulnerable code constructs like unchecked memcpy, buffer operations, or specific function call patterns in pseudocode.
---

# Code Pattern Matching

Search for code patterns in decompiled output using the Weggli pattern matching engine.

## When to use

- Find specific code patterns in decompiled functions (e.g., `memcpy(dst, src, len)`)
- Search for vulnerable code constructs across functions
- Match variable usage patterns with semantic constraints
- Locate specific function call patterns with regex filtering

## Instructions

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`), adapting it as needed:
```lua
local decomp = project:decompile(<target_function>)

local matches = decomp:query({
  raw = true,  -- If true, the query will be used as-is; otherwise, it will be wrapped in {{}}
  query = [[<query>]]
})

return matches:dump() -- matches:dump() already returns a table
```

The `<query>` parameter is a query written in Weggli, the default pattern matching engine.

Possible values for `<target_function>`:
- A string, e.g. `"system"`
- An AddressValue
  - VulHunt APIs return addresses as an AddressValue
  - To build an AddressValue, use for example: `AddressValue.new(0x1234)`
- A regex, e.g. `{matching = "<regex>", kind = "symbol", all = true}`
- A byte pattern, e.g. `{matching = "41544155", kind = "bytes", all = true}`

> `all` is a boolean. If set to `true`, it returns a table containing all matching functions. If `false` (default), it returns only the first matching value. The for loop is not necessary if the function target is only one (i.e. `all` is not set to true)


Returns a JSON object containing all matched code and their addresses.

### Additional Options

```lua
decomp:query{
    raw = true,
    unique = true,                      -- captured variables must refer to different nodes
    query = [[ $FN($DST, $SRC, $SIZE); ]],
    regexes = {
        "$FN=memcpy|memmove|strncpy",   -- function name must match one of these
        "$SIZE!=^[0-9]+$",              -- size must NOT be a plain numeric constant
    }
}
```

## References

- [decompiled-function.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/decompiled-function.md) - Query syntax and methods for decompiled function objects
- [syntax-match-result.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/syntax-match-result.md) - Structure of returned match results

URLs to additional documentation pages are available at https://vulhunt.re/llm.txt

## Related Skills

- **decompiler** (`/decompiler`) - Required prerequisite for code pattern matching; use it to decompile functions before searching for patterns
- **functions** (`/functions`) - Use this to find target functions before decompiling and pattern matching