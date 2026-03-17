---
description: Find function, struct, or variable definitions using ctags indexes
triggers:
  - find symbol
  - find function
  - find struct
  - find definition
  - locate symbol
  - locate function
  - search for symbol
  - where is defined
  - find ctag
  - ctags search
---

# Find Symbol Using ctags

This skill searches for symbol definitions (functions, structs, variables, classes) in the ctags indexes.

## How It Works

The repository has two ctags indexes:
- **Firmware (C code):** `inav/tags`
- **Configurator (JS code):** `inav-configurator/tags`

## Usage

When the user asks to find a symbol, search both indexes:

```bash
# Search firmware (C code)
grep "^SYMBOL_NAME\b" inav/tags | head -20

# Search configurator (JS code)
grep "^SYMBOL_NAME\b" inav-configurator/tags | head -20
```

Replace `SYMBOL_NAME` with the actual symbol to search for.

## Parsing the Output

Each line in the tags file contains tab-separated fields:

1. **Symbol name** - The identifier being searched for
2. **File path** - Where the symbol is defined
3. **Search pattern** - Usually `/^...$/` or line number
4. **Extensions** - Key-value pairs like `kind:f`, `line:123`, `signature:(args)`

**Common kind values:**
- `f` = function
- `s` = struct
- `v` = variable
- `c` = class
- `m` = member/method
- `t` = typedef
- `d` = #define/macro
- `p` = prototype

## Reporting Results

Present the results in a clear format:

```
Found in firmware (C code):
- File: src/main/flight/pid.c:145
  Kind: function
  Signature: void pidController(timeUs_t currentTimeUs)

- File: src/main/flight/pid.h:23
  Kind: prototype

Found in configurator (JS code):
- File: js/controllers/configuration.js:89
  Kind: function
```

Use the format `file_path:line_number` to allow easy navigation.

## Limitations

- **JavaScript indexing is limited:** ctags doesn't parse ES6+ features well
  - For JS code, Claude's built-in Grep tool often works better
  - Use Grep with pattern like: `function.*symbolName` or `class symbolName`

- **C firmware indexing works well** for functions, structs, variables, and macros

## Regenerating Indexes

If source files have changed significantly and symbols aren't found:

```bash
# Firmware (C code)
cd inav
ctags -R --fields=+niazS --extras=+q --exclude=lib --exclude=build --exclude=tools --exclude=.git -f tags .

# Configurator (JS code)
cd inav-configurator
ctags -R --fields=+niazS --extras=+q --exclude=node_modules --exclude=.git --exclude=out --exclude=.vite --exclude=dist -f tags .
```

## Examples

**User asks:** "Where is pidController defined?"

**You should:**
1. Run grep on both tags files with pattern `^pidController\b`
2. Parse the results to extract file path and line number
3. Report in the format: `src/main/flight/pid.c:145`

**User asks:** "Find the navConfig struct"

**You should:**
1. Search for `^navConfig\b` in both indexes
2. Look for entries with `kind:s` (struct) or `kind:t` (typedef)
3. Report all matches with file locations

---

## Related Skills

- **wiki-search** - Search documentation for implementation guidance
- **msp-protocol** - Look up MSP commands and structures
