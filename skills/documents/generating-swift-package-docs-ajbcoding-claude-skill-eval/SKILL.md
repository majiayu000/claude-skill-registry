---
name: generating-swift-package-docs
description: Use when encountering unfamiliar import statements; when exploring a dependency's API; when user asks "what's import X?", "what does import X do?", or about package documentation. - Generates comprehensive API documentation for Swift package dependencies on-demand. This skill helps you quickly obtain documentation for packages used in Xcode projects when you encounter unfamiliar module imports. Automatically resolves modules to packages and caches documentation for reuse. This is the primary tool for understanding individual `import` statements.
allowed-tools: Bash, Read
---

Generates comprehensive API documentation for Swift package dependencies in Xcode projects.

## How to Use This Skill

When the user asks about an unfamiliar Swift module import (e.g., "what's import AppUpdating?"):

1. **Identify the module name** from the user's question (e.g., "AppUpdating")

2. **Find the Xcode project path** - look for a `.xcodeproj` file in the current working directory or ask the user

3. **Run the documentation generator script**: `./scripts/generate_docs.py "<module_name>" "<path_to.xcodeproj>"` (script path is relative to skill directory)

4. **The script will**:
   - Automatically determine which package provides the module
   - Check if documentation already exists in `<project>/dependency-docs/`
   - If not, generate documentation using `interfazzle` and cache it
   - Print the path to the documentation file on stdout

5. **Use the documentation** on the returned file path as needed

## Example

```
./scripts/generate_docs.py "AppUpdating" /path/to/your/project.xcodeproj
```

This returns a file path like:

```
/path/to/your/project/dependency-docs/MyAppUpdater-1.35.md
```

Then read this file and provide the user with relevant information about the AppUpdating module.

## Prerequisites

- Project must be built at least once (DerivedData must exist)
- `interfazzle` CLI tool must be installed
- Python 3.6+

## Error Handling

If the script fails:

- Verify the project has been built (DerivedData exists)
- Check that the .xcodeproj path is correct
- Ensure `interfazzle` is installed and in PATH
- Check stderr output for specific error messages

## Important Notes

- The script outputs the documentation file path to stdout
- Status messages go to stderr (you can ignore these)
- If documentation already exists, it returns immediately with the cached path

## Additional Documentation

For comprehensive details, see [reference.md](reference.md).
