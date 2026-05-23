---
name: xcode-package-swift-misidentification
description: "Use when an iOS app builds successfully but the simulator does not launch due to Package.swift misidentification."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# Xcode Package.swift Misidentification Diagnosis

**Extracted:** 2026-02-11
**Context:** iOS app builds succeed but simulator doesn't launch

## Problem

When a project directory contains both `Package.swift` and `.xcodeproj`, Xcode may open the directory as a Swift Package instead of the Xcode project. This causes:

- Build succeeds (the library target in Package.swift compiles)
- Simulator doesn't launch (no app target exists in the package)
- No obvious error messages

## Diagnosis

Check DerivedData `info.plist` to see what Xcode actually opened:

```bash
# List recent DerivedData entries
ls -lt ~/Library/Developer/Xcode/DerivedData/ | head -5

# Check WorkspacePath
plutil -p ~/Library/Developer/Xcode/DerivedData/<project-dir>/info.plist
```

**Key indicator:** `WorkspacePath` points to the directory (e.g., `/path/to/project`) instead of the `.xcodeproj` file (e.g., `/path/to/project/Project.xcodeproj`).

Also check what was actually built:

```bash
ls ~/Library/Developer/Xcode/DerivedData/<project-dir>/Build/Products/Debug-iphonesimulator/
```

If you see only `.o` / `.swiftmodule` files (no `.app`), the package was built instead of the app.

## Solution

Open the `.xcodeproj` file directly:

```bash
open /path/to/project/Project.xcodeproj
```

Do NOT open the directory with `xed .` or double-click when both `Package.swift` and `.xcodeproj` exist.

## When to Use

- iOS app "builds but doesn't run" on simulator
- Build products contain only library artifacts, not `.app`
- Project has both `Package.swift` and `.xcodeproj` at the root
