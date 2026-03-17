---
name: xcode-project
description: Add files and frameworks to Xcode projects programmatically
---

# /xcode-project - Xcode Project Management

## Purpose

Safely add Swift source files, frameworks, and xcframeworks to Xcode projects without manual Xcode intervention. This skill handles the complex project.pbxproj file structure automatically.

## Usage

```
/xcode-project add-files <path1> [path2...]     # Add Swift files to project
/xcode-project add-framework <path>              # Add framework/xcframework
/xcode-project list-files                        # List source files in project
/xcode-project verify                            # Verify project integrity
```

## How It Works

The skill uses a Ruby script (`scripts/xcode-project-helper.rb`) that leverages the `xcodeproj` gem to safely manipulate project.pbxproj files. This is the same library used by CocoaPods and fastlane.

### Adding Source Files

When adding Swift files:
1. Creates PBXFileReference entry
2. Adds to appropriate PBXGroup (based on file path)
3. Adds to PBXSourcesBuildPhase for compilation

```
/xcode-project add-files UnaMentis/Services/TTS/NewService.swift
```

### Adding Frameworks

When adding frameworks/xcframeworks:
1. Creates PBXFileReference entry
2. Adds to Frameworks group
3. Adds to PBXFrameworksBuildPhase (Link Binary With Libraries)
4. For embedded frameworks, adds to PBXCopyFilesBuildPhase

```
/xcode-project add-framework UnaMentis/Frameworks/MyLib.xcframework
```

### Options

- `--embed` - Embed framework (copy to app bundle)
- `--no-embed` - Link only, don't embed (default for system frameworks)
- `--target <name>` - Specify target (default: first app target)
- `--group <path>` - Specify group for file placement

## Prerequisites

The Ruby xcodeproj gem must be installed:
```bash
gem install xcodeproj
```

Or using bundler (recommended):
```bash
cd <repository-root>
bundle install
```

## Examples

**Add a single Swift file:**
```
/xcode-project add-files UnaMentis/Services/TTS/KyutaiPocketTTSService.swift
```

**Add multiple files:**
```
/xcode-project add-files UnaMentis/Services/TTS/PocketTTSBindings.swift UnaMentis/Services/TTS/KyutaiPocketModelManager.swift
```

**Add an xcframework:**
```
/xcode-project add-framework UnaMentis/Frameworks/PocketTTS.xcframework
```

**Add framework with embedding:**
```
/xcode-project add-framework UnaMentis/Frameworks/MyDynamicLib.framework --embed
```

## Project Structure

The skill understands the UnaMentis project structure:
- `UnaMentis/` - Main app source
- `UnaMentis/Frameworks/` - Third-party frameworks
- `UnaMentis/Services/` - Service layer code
- `UnaMentisTests/` - Unit tests
- `UnaMentisUITests/` - UI tests

Files are automatically placed in the correct group based on their path.

## Error Handling

The script validates:
- File exists on disk before adding
- File not already in project (prevents duplicates)
- Framework architecture compatibility
- Project file integrity after modification

If errors occur, the original project file is preserved (backup created).

## Workflow Integration

Use this skill when:
1. Adding new Swift source files created by Claude
2. Integrating new frameworks or xcframeworks
3. After generating UniFFI bindings
4. When moving files between groups

This prevents the manual project.pbxproj editing that can cause:
- Missing file references
- Incorrect build phases
- UUID collisions
- Project corruption

## Verification

After adding files, verify with:
```
/xcode-project verify
```

This checks:
- All referenced files exist on disk
- All source files are in build phases
- No duplicate entries
- Framework linking is correct

## See Also

- [Xcode Project Format](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Projects.html)
- [xcodeproj gem](https://github.com/CocoaPods/Xcodeproj)
