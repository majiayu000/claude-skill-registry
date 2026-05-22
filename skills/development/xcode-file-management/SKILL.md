---
name: xcode-file-management
description: Use when adding, removing, moving, or renaming Swift source files in the dd-sdk-ios Xcode project. Use when the task involves file creation, deletion, or relocation in any module (DatadogRUM, DatadogLogs, DatadogCore, etc.). Use when you would otherwise reach for Write, Bash mv/mkdir/rm, or manual pbxproj editing for file management.
---

# dd-sdk-ios Xcode File Management

## Overview

The dd-sdk-ios project is both an SPM package **and** an Xcode workspace with `.pbxproj` files. SPM builds discover files automatically, but **Xcode does not** — it requires explicit registration in `.pbxproj`. The Xcode MCP server (available from Xcode 26.3+) handles this automatically. Always use it.

## Prerequisites

The Xcode MCP server requires **Xcode 26.3+** and must be enabled in Claude Code settings. Verify it's active by checking that `XcodeListWindows` is available. If not, stop and ask the user to enable the Xcode MCP server before proceeding with file operations.

## The Rule

**Never use `Write`, `Bash mv/mkdir/rm`, or `Edit` for file creation, deletion, or movement in this project.**

Use Xcode MCP tools instead — they update the filesystem AND the `.pbxproj` in one atomic operation.

## Target Membership

Target membership is **implicit** — Xcode MCP infers the target from the navigator path where the file is placed. A file added under `DatadogLogs/` is automatically assigned to the `DatadogLogs` target. No explicit target specification is needed.

## Quick Reference

| Operation | Use This Tool | Never Use |
|-----------|--------------|-----------|
| Create file | `XcodeWrite` | `Write`, `Bash touch/cat` |
| Delete file | `XcodeRM` | `Bash rm` |
| Move / rename | `XcodeMV` | `Bash mv` |
| Create directory/group | `XcodeMakeDir` | `Bash mkdir` |
| Read file | `XcodeRead` | (either is fine) |
| Search files | `XcodeGlob`, `XcodeGrep` | (either is fine) |

## Common Rationalizations — All Wrong

| Excuse | Reality |
|--------|---------|
| "SPM auto-discovers files, pbxproj doesn't matter" | The Xcode workspace has `.pbxproj` files. They must stay in sync or Xcode breaks. |
| "It's faster to use bash" | A file invisible to Xcode causes build failures and confuses teammates. |
| "I'll update pbxproj manually after" | pbxproj is binary-adjacent XML; manual edits cause merge conflicts and corruption. |
| "The file is just temporary" | Temporary files still break the build if Xcode can't see them. |

## Example

```
# ✅ Add a new source file
XcodeWrite(
  tabIdentifier: <tab>,
  filePath: "DatadogLogs/Sources/LogBatcher.swift",
  content: "..."
)
# → Creates file on disk AND registers it in pbxproj + target membership

# ✅ Move a file
XcodeMV(
  tabIdentifier: <tab>,
  sourcePath: "DatadogLogs/Sources/LogBatcher.swift",
  destinationPath: "DatadogLogs/Sources/Batching/LogBatcher.swift"
)
# → Moves file on disk AND updates pbxproj reference

# ❌ Wrong — file created on disk but invisible to Xcode
Write(file_path: ".../DatadogLogs/Sources/LogBatcher.swift", content: "...")
```

## Getting the tabIdentifier

```python
XcodeListWindows()  # → returns tabIdentifier for open workspace
```

## Path Format

Xcode MCP uses **project navigator paths**, not filesystem paths. Use `XcodeLS` to discover them:

```python
XcodeLS(tabIdentifier: <tab>, path: "DatadogLogs")
# → ["ConsoleLogger.swift", "Feature/LogsFeature.swift", ...]
# Note: paths are relative to the Xcode group, not the filesystem root
```

To create `DatadogLogs/Sources/Foo.swift` on disk, use the navigator path `DatadogLogs/Foo.swift`.

## After File Operations

After adding files to a module, verify the build still works:

```python
BuildProject(tabIdentifier: <tab>)
```
