---
name: ios-add-file
description: Add a Swift file to an Xcode project without opening Xcode. Programmatically edits project.pbxproj to include the file. Use when adding new Swift files to iOS projects from command line.
---

# iOS Add File to Project

## Overview

Adds a Swift source file to an Xcode project by directly editing the `project.pbxproj` file. This allows command-line development workflows without opening Xcode IDE. The process involves generating UUIDs and updating four sections of the project file.

## When to Use

Invoke this skill when the user:
- Asks to "add a file to the Xcode project"
- Wants to "add Swift file to project"
- Says "include this file in the build"
- Needs to add source files without Xcode GUI
- Mentions editing project.pbxproj

## Prerequisites

- Xcode project exists (.xcodeproj directory)
- The Swift file is already created in the project directory
- Backup of project.pbxproj is recommended before editing
- `uuidgen` command available (standard on macOS)

## Instructions

### 1. Create the Swift File

First, create the actual Swift file in the project directory:
```bash
cat > ProjectName/FileName.swift << 'EOF'
import Foundation

class FileName {
    // Your code here
}
EOF
```

### 2. Generate UUIDs

Generate two unique identifiers:
```bash
BUILD_UUID=$(uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]')
FILE_UUID=$(uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]')

echo "Build UUID: $BUILD_UUID"
echo "File UUID: $FILE_UUID"
```

### 3. Edit project.pbxproj

Open `ProjectName.xcodeproj/project.pbxproj` in a text editor and add entries to four sections:

#### a) PBXBuildFile Section

Add after `/* Begin PBXBuildFile section */`:
```
        $BUILD_UUID /* FileName.swift in Sources */ = {
            isa = PBXBuildFile;
            fileRef = $FILE_UUID /* FileName.swift */;
        };
```

#### b) PBXFileReference Section

Add after `/* Begin PBXFileReference section */`:
```
        $FILE_UUID /* FileName.swift */ = {
            isa = PBXFileReference;
            lastKnownFileType = sourcecode.swift;
            path = FileName.swift;
            sourceTree = "<group>";
        };
```

#### c) PBXGroup Section

Find the project's main group (usually named after the project) and add to `children` array:
```
        XXXXXXXX /* ProjectName */ = {
            isa = PBXGroup;
            children = (
                YYYYYYYY /* ExistingFile1.swift */,
                ZZZZZZZZ /* ExistingFile2.swift */,
                $FILE_UUID /* FileName.swift */,
                ...
            );
```

#### d) PBXSourcesBuildPhase Section

Find the Sources build phase and add to `files` array:
```
        SSSSSSSS /* Sources */ = {
            isa = PBXSourcesBuildPhase;
            buildActionMask = 2147483647;
            files = (
                TTTTTTTT /* ExistingFile1.swift in Sources */,
                UUUUUUUU /* ExistingFile2.swift in Sources */,
                $BUILD_UUID /* FileName.swift in Sources */,
            );
```

### 4. Verify Build

Test that the project still builds:
```bash
xcodebuild -project ProjectName.xcodeproj \
    -scheme SchemeName \
    -destination 'platform=iOS Simulator,name=iPhone 17 Pro' \
    LD="clang" \
    build
```

### 5. Inform User

Let the user know:
- The file has been added to the project
- Build verification passed (or report errors)
- The file is now part of the build system
- They can use the new code in other Swift files

## Key Points

**UUID Format**:
- Must be unique within the project
- Lowercase, no hyphens (use `tr -d '-' | tr '[:upper:]' '[:lower:]'`)
- 32 characters long

**Comments**:
- Comments like `/* FileName.swift */` are optional but helpful
- Make the project file human-readable

**Order**:
- Order within sections doesn't matter
- But all entries must be present in all four sections

**Backup**:
- Always backup project.pbxproj before manual editing
- Use git to track changes

## Common Issues

**Build fails after adding**:
- Check UUIDs are unique (not duplicating existing ones)
- Verify all four sections were updated correctly
- Ensure file path matches actual file location
- Check for syntax errors (missing commas, brackets)

**File doesn't appear in build**:
- Must be in both PBXFileReference AND PBXSourcesBuildPhase
- Check that PBXBuildFile links FILE_UUID correctly

**Project won't open in Xcode**:
- Syntax error in project.pbxproj
- Restore from backup
- Check for unmatched braces or missing semicolons

## Automation Potential

This process can be scripted with:
- Shell script using sed/awk
- Python script parsing the project file
- Ruby xcodeproj gem for more robust editing

For now, manual editing with verification is recommended.

## Example Success

This technique was successfully used to add Logger.swift to the NoobTest/Firefly project without opening Xcode, enabling command-line-only development workflows.

## Alternative: xcodeproj Ruby Gem

For more complex scenarios, consider the `xcodeproj` gem:
```bash
gem install xcodeproj
```

But for simple file additions, manual editing works well.
