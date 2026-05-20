---
name: dataflow-analysis
description: Track data flow between function parameters, calls, and arguments using taint analysis. Use when detecting vulnerabilities like command injection, buffer overflows, or tracing user input to dangerous functions.
---

# Dataflow Analysis

Perform intra-procedural dataflow analysis to track how data flows within functions.

## When to use

- Track if a function parameter flows to a function call argument
- Track if a function call's output flows to another function call's argument
- Find taint propagation paths (e.g., user input reaching dangerous functions)
- Detect vulnerabilities like command injection, buffer overflows

## Instructions

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`).

To perform dataflow analysis, use `project:calls_matching{}`:
```lua
local calls = project:calls_matching({
  to = <target_call>,
  where = function(caller)
    return caller:named("<function_name>") and caller:has_call(<target_call>)
  end,
  using = {
    -- Annotate caller parameters
    parameters = {var:named "first_param", _},
    -- Annotate callees
    callees = {
      ["malloc"] = {inputs = {var:named "size"}}, 
      ["strlen"] = {output = var:named "len", inputs = {_}},
      ["check_len"] = {inputs = {var:sanitised()}}
    }
  }
})

local results = {}

for _, c in ipairs(calls) do
  local entry = {
    caller_name = c.caller.name,
    call_address = c.call_address,
  }

  if c.inputs[1] and c.inputs[1].annotation then
    entry.arg1_annotation = c.inputs[1].annotation
    entry.arg1_source = c.inputs[1].origin.source_address
  end

  if c.inputs[2] and c.inputs[2].annotation then
    entry.arg2_annotation = c.inputs[2].annotation
    entry.arg2_source = c.inputs[2].origin.source_address
  end

  if c.output then
    entry.return_annotation = c.output.annotation
  end

  table.insert(results, entry)
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

Inputs and output are of type `OperandInfo` (see [operand-info.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/operand-info.md)). Origins are of type `OperandOrigin` (see [operand-origin.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/operand-origin.md)).

### Annotations

- `var:named "x"` - Tags a variable with the name "x". This tag follows the data through the function, allowing later checks on where it ends up (e.g., which function argument it flows into).
- `_` - Placeholder for variables that don't need to be tracked.
- `var:sanitised()` - Stops taint propagation when a tainted variable flows through that function argument.

The annotation set in `using` appears in `c.inputs[N].annotation` in the results.
For example, if annotated with `var:named "cmd"`, then `c.inputs[1].annotation == "cmd"`
indicates the first argument came from that tracked variable.

## Examples

### Function parameter -> Function argument

**Example 1: Buffer overflow via memcpy**

C code snippet:
```c
void vulnerable_function(int len, char *path) {
  char buffer[256];
  memcpy(buffer, path, len);
}
```

Lua query:
```lua
local calls = project:calls_matching{
  to = "memcpy",
  using = {
    parameters = {var:named "len", var:named "path"}
  }
}

local findings = {}
for _, call in ipairs(calls) do
  local len_src = call.inputs[3]
  local data_src = call.inputs[2]

  if (len_src ~= nil and len_src.annotation == "len") or
     (data_src ~= nil and data_src.annotation == "path") then
    table.insert(findings, {
      caller_address = tostring(call.caller_address),
      call_address = tostring(call.call_address),
    })
  end
end

return findings
```

**Example 2: Command injection via snprintf -> system**

C code snippet:
```c
void vulnerable_function(char *cmd) {
  char buffer[256];

  snprintf(buffer, sizeof(buffer), "sh -c %s", cmd);
  system(buffer);
}
```

Lua query:
```lua
local calls = project:calls_matching{
  to = "system",
  where = function(caller)
    return caller:has_call("snprintf")
  end,
  using = {
    callees = {snprintf = {inputs = {var:named "cmd", _, _}}}
  }
}

local findings = {}
for _, call in ipairs(calls) do
  local src = call.inputs[1]

  if src ~= nil and src.annotation == "cmd" then
    table.insert(findings, {
      caller_address = tostring(call.caller_address),
      call_address = tostring(call.call_address),
    })
  end
end

return findings
```

## Use cases

### Command injection

#### Shell commands built from format strings

Find calls to `system()` where the argument was built using `snprintf()`:

```lua
local calls = project:calls_matching{
  to = "system",  -- system(cmd)
  where = function(caller)
    return caller:has_call("snprintf") -- snprintf(cmd, ...)
  end,
  using = {
    callees = {snprintf = {inputs = {var:named "cmd", _, _}}}
  }
}

local findings = {}
for _, call in ipairs(calls) do
  local src = call.inputs[1]

  if src ~= nil and src.annotation == "cmd" then
    table.insert(findings, {
      snprintf_address = tostring(src.origin.source_address),
      caller_name = tostring(call.caller.name),
      caller_address = tostring(call.caller_address),
      call_address = tostring(call.call_address),
    })
  end
end

return findings
```

> NOTE: Only change the propagated value if the source changes.

Returns a JSON object containing:
- `snprintf_address` is the address of the call site to `snprintf`
- `caller_address` is the address of the function that makes the call
- `call_address` is the address of the call site to `system` (the code block address where the call is made)

## References

- [calls-matching-param.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/calls-matching-param.md) - Input format for `calls_matching`
- [calls-matching-table.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/calls-matching-table.md) - Structure of the returned table from `calls_matching`
- [regex-matcher.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/regex-matcher.md) - Regex matching utilities

URLs to additional documentation pages are available at https://vulhunt.re/llm.txt

## Related Skills

- **functions** (`/functions`) - Use this skill to find target functions by name, address, or pattern before performing dataflow analysis
- **call-sites** (`/call-sites`) - To find where functions are called without tracking data flow, use this simpler skill instead
- **decompiler** (`/decompiler`) - View decompiled code to understand function logic before setting up complex dataflow annotations
