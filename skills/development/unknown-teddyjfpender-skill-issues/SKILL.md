---
name: cairo-modules-files
description: Explain how Cairo modules are split across files and folders, and how `mod` declarations map to files; use when a request involves organizing modules into multiple files in Cairo.
---

# Cairo Modules in Files

## Overview
Explain how module declarations map to files and folders in a Cairo package.

## Quick Use
- Read `references/modules-files.md` before answering.
- Show the relationship between `mod` declarations and file names.
- Remind that `use` does not load modules; only `mod` does.

## Response Checklist
- Declare a module with `mod name;` in the parent file.
- Place the module body in `name.cairo` or `name/mod.cairo`.
- Declare submodules in the module file and place them in `name/submodule.cairo`.

## Example Requests
- "Where should I put `mod hosting;`?"
- "How do I split a module into multiple files?"
- "Why doesn't `use` load my module?"

## Cairo by Example
- [File hierarchy](https://cairo-by-example.xyz/mod/split)
