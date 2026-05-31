---
name: byte-pattern-matching
description: Search for raw byte patterns (hex sequences, opcodes) in binary code. Use when looking for specific instruction sequences, machine code patterns, UEFI SMI handlers, or known vulnerability signatures by their byte representation.
---

# Byte Pattern Matching

Search for raw byte patterns (hex sequences) in binary code.

## When to use

- Find specific instruction sequences by their machine code bytes
- Locate code patterns when the raw opcode bytes are known
- Search for known vulnerability signatures by byte pattern
- Find UEFI-specific patterns like SMI handlers or protocol usage

## Instructions

Using the VulHunt MCP tools, open the project (`open_project`) and run the following Lua query (`query_project`), adapting it as needed:
```lua
local result = project:search_code("<byte_pattern>")

if result then
  local entry = {
    function_address = tostring(result.function_address),
    start_address = tostring(result.start_address),
    end_address = tostring(result.end_address),
    instructions = {},
  }

  for _, insn in ipairs(result.insns) do
    table.insert(entry.instructions, {
      mnemonic = insn.mnemonic,
      address = tostring(insn.address),
    })
  end

  return entry
end
```

The byte pattern is a hex string (e.g., `"554889e5................"`, where `..` matches any byte).

Returns a JSON object containing:
- `function_address` - the address of the function containing the match
- `start_address` - the start address of the matched pattern
- `end_address` - the end address of the matched pattern
- `instructions` - list of matched instructions with their mnemonics and addresses

### UEFI Platform

For UEFI targets, additional functions and options are available:
```lua
-- Search code within sw_smi_handlers
local result = project:search_code("<byte_pattern>", "sw_smi_handlers")

-- Search code within child_sw_smi_handlers
local result = project:search_code("<byte_pattern>", "child_sw_smi_handlers")

-- Search for a protocol GUID (returns a boolean)
local guid_found = project:search_guid("5B1B31A1-9562-11D2-8E3F-00A0C969723B", "EFI_LOADED_IMAGE_PROTOCOL_GUID")

-- Search for an NVRAM variable (returns a boolean)
local nvram_found = project:search_nvram("GetVariable", "PlatformLang", "8BE4DF61-93CA-11D2-AA0D-00E098032B8C") 

-- Search for a protocol (returns a boolean)
local protocol_found = project:search_protocol("LocateProtocol", "PCD_PROTOCOL_GUID", "11B34006-D85B-4D0A-A290-D5A571310EF7")

-- Search for a PPI (returns a boolean)
local ppi_found = project:search_ppi("LocatePpi", "PPIName", "9C21FD11-434A-12D3-D10D-109048052C8A")
```

> NOTE: The architecture of the loaded binary can be obtained using `project.architecture`.

## References

- [instruction.md](https://vulhunt.re/llm/docs/vulhunt-reference/types/instruction.md) - All methods and fields for an instruction

URLs to additional documentation pages are available at https://vulhunt.re/llm.txt

## Related Skills

- **code-pattern-matching** (`/code-pattern-matching`) - For higher-level semantic pattern matching in decompiled code, while byte-pattern-matching works at the raw instruction level
- **decompiler** (`/decompiler`) - Decompile matched code to understand what the byte pattern represents
