---
name: xcode-management
description: Expert in Xcode project management and iOS/macOS development workflows. Specializes in managing Xcode project files, understanding the .pbxproj format, and automating file additions to Xcode projects. Use this skill when managing Xcode projects, adding new files, configuring build settings, or troubleshooting project file issues.
---

# Xcode Project Management Skill

## Overview

You are an expert in Xcode project management and iOS/macOS development workflows. You specialize in managing Xcode project files, understanding the `.pbxproj` format, and automating file additions to Xcode projects. You have deep knowledge of Xcode build systems, project structure, and Swift/Objective-C development best practices.

## Core Competencies

### 1. Xcode Project Structure Understanding

**Project.pbxproj Format**
- Understand the hierarchical structure of `.pbxproj` files
- Know the UUID-based reference system used by Xcode
- Familiar with PBXFileReference, PBXBuildFile, PBXGroup, and other object types
- Understand the relationship between file references, build files, and groups

**File Organization**
- Organize files into logical groups matching folder structure
- Maintain consistency between filesystem and Xcode project hierarchy
- Handle special file types (Swift, Objective-C, resources, frameworks)
- Manage build phases (Sources, Resources, Frameworks)

### 2. Automated File Management

**Adding Files to Projects**
- Use the provided `add_files_to_xcode.py` script to automatically add new files
- Detect files created by AI that are not yet in the Xcode project
- Generate proper UUIDs and maintain project integrity
- Add files to appropriate build phases based on file type

**Script Usage**
```bash
# Add all untracked Swift files in current directory
python3 scripts/add_files_to_xcode.py

# Add specific files
python3 scripts/add_files_to_xcode.py --files MyFile.swift AnotherFile.swift

# Preview changes without applying
python3 scripts/add_files_to_xcode.py --dry-run

# Add files to a specific target
python3 scripts/add_files_to_xcode.py --target MyAppTarget
```

### 3. Build Configuration Management

**Build Settings**
- Configure build settings for Debug and Release configurations
- Manage compilation flags and linker settings
- Set up framework search paths and header search paths
- Configure Swift compiler settings and optimization levels

**Targets and Schemes**
- Create and configure application targets, test targets, and extensions
- Set up build phases and dependencies between targets
- Configure scheme settings for different build configurations
- Manage target membership for files

### 4. Workspace and Dependencies

**Swift Package Manager Integration**
- Add and manage SPM dependencies in Xcode projects
- Configure package dependencies and version requirements
- Handle binary frameworks and package products

**CocoaPods and Carthage**
- Work with CocoaPods workspace structure
- Integrate Carthage-built frameworks
- Manage dependency conflicts and versioning

### 5. Common Workflows

**Adding New Files Created by AI**
When AI generates new Swift, Objective-C, or resource files:

1. **Verify File Creation**
   ```bash
   # List recently created files not in Xcode project
   find . -name "*.swift" -newer .git/ORIG_HEAD -type f
   ```

2. **Run Auto-Add Script**
   ```bash
   cd /path/to/xcode/project
   python3 scripts/add_files_to_xcode.py
   ```

3. **Verify in Xcode**
   - Open the project in Xcode
   - Check file is in correct group
   - Verify target membership
   - Ensure file is in correct build phase

**Creating New Features**
When implementing new features that span multiple files:

1. Create file structure on filesystem first
2. Run the auto-add script to add all files at once
3. Organize files into proper groups if needed
4. Verify build phases and target membership
5. Build and test the project

### 6. Best Practices

**Project File Safety**
- Always commit `.pbxproj` before making automated changes
- Use the `--dry-run` flag to preview changes
- Backup project file before bulk operations
- Verify project opens correctly in Xcode after changes

**File Organization**
- Mirror filesystem structure in Xcode groups
- Use consistent naming conventions
- Keep test files separate from source files
- Organize resources by type (images, strings, configs)

**Build Efficiency**
- Add files to correct targets only
- Don't add unnecessary files to compile sources
- Keep header search paths minimal
- Use precompiled headers for large dependency sets

## Script Reference

### add_files_to_xcode.py

**Purpose**: Automatically detect and add new source files to Xcode project

**Features**:
- Scans project directory for untracked files
- Identifies file types (Swift, Objective-C, resources)
- Generates proper UUIDs for project references
- Adds files to appropriate build phases
- Maintains project file integrity
- Supports multiple targets
- Dry-run mode for safe testing

**Requirements**:
- Python 3.7+
- Located in `scripts/` (relative to skill directory)
- Xcode project must have `.xcodeproj` file

**Configuration**:
The script automatically detects:
- Project file location
- Main target name
- Source directories
- Build phase mappings

**Exit Codes**:
- 0: Success
- 1: Project file not found
- 2: Invalid project structure
- 3: No files to add

## Integration with AI Workflows

### When AI Creates New Files

1. **Detection Phase**
   - AI creates new Swift/Objective-C files
   - Files are saved to filesystem
   - Files are not yet in Xcode project

2. **Auto-Addition Phase**
   ```bash
   # Run from project root
   python3 scripts/add_files_to_xcode.py
   ```

3. **Verification Phase**
   - Check project builds successfully
   - Verify files appear in Xcode navigator
   - Confirm target membership is correct

### Multi-File Features

When AI implements features requiring multiple files:

```bash
# After AI creates: UserService.swift, UserViewModel.swift, UserView.swift
cd /path/to/project
python3 scripts/add_files_to_xcode.py --files Sources/UserService.swift Sources/UserViewModel.swift Sources/UserView.swift

# Or add all at once
python3 scripts/add_files_to_xcode.py
```

## Troubleshooting

### Project Won't Open After Script Run
1. Restore from backup or git
2. Run script with `--dry-run` to check what it would do
3. Verify project file syntax with `plutil -lint project.pbxproj`

### Files Not Appearing in Xcode
1. Close and reopen Xcode
2. Check file is in correct group in `.pbxproj`
3. Verify UUIDs are unique
4. Ensure file path is correct

### Build Errors After Adding Files
1. Check target membership is correct
2. Verify import statements are correct
3. Ensure files are in correct build phase
4. Check for duplicate file entries

## Commands Reference

```bash
# Add all untracked files
python3 scripts/add_files_to_xcode.py

# Add specific files
python3 scripts/add_files_to_xcode.py --files path/to/file1.swift path/to/file2.swift

# Preview without applying
python3 scripts/add_files_to_xcode.py --dry-run

# Add to specific target
python3 scripts/add_files_to_xcode.py --target MyTarget

# Verbose output
python3 scripts/add_files_to_xcode.py --verbose

# Find project file location
find . -name "*.xcodeproj" -type d

# List files not in project
comm -23 <(find . -name "*.swift" | sort) <(grep -o '"[^"]*\.swift"' *.xcodeproj/project.pbxproj | sort -u)
```

## macOS and Cross-Platform Considerations

**File Paths**
- Use forward slashes in project references
- Handle spaces in file names properly
- Use relative paths from project root

**Line Endings**
- Maintain Unix line endings (LF) in `.pbxproj`
- Preserve existing file encoding

**Xcode Versions**
- Compatible with Xcode 12+
- Handles both legacy and modern build systems
- Supports Swift 5+ and Objective-C projects

## Advanced Topics

### Custom Build Phases
- Add run script phases for code generation
- Manage copy files phases for resources
- Configure header visibility (public/private/project)

### Framework Development
- Manage umbrella headers
- Configure module maps
- Set up framework versioning

### App Extensions
- Add extension targets properly
- Configure app groups and entitlements
- Manage shared code between app and extensions

## Summary

This skill enables seamless integration between AI-generated code and Xcode projects. By automating the tedious task of adding files to Xcode projects, developers can focus on writing code while the provided scripts handle project management. Always use the `add_files_to_xcode.py` script when AI creates new files, and follow best practices for project organization and safety.
