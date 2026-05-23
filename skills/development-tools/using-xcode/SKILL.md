---
name: using-xcode
description: Use this before running `xcodebuild` or working with Xcode - tells you the specifics of how we use Xcode and its tools
---

## Building Xcode projects

When running Xcode builds, use the `xcodebuild-wrapper` script over `xcodebuild`. This wrapper:

- returns build data in a structured way for LLM use
- accepts the same arguments as `xcodebuild`

Don't tail or abbreviate its output.

Example:

```bash
./xcodebuild-wrapper build -scheme "Actions For Obsidian (macOS)"
```

**Location**: `~/.claude/skills/using-xcode/xcodebuild-wrapper`

## Derived Data

**DO NOT** attempt to delete or remove the derived data folder unless explicitly told so.
