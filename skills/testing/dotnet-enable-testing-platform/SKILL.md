---
name: dotnet-enable-testing-platform
description: Enables the Microsoft Testing Platform runner in global.json. Use when the user wants to enable or migrate to the new .NET testing platform.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob AskUserQuestion
---

Enable the Microsoft Testing Platform runner for a .NET solution by configuring `global.json`.

The Microsoft Testing Platform is a modern, extensible test runner that provides improved performance, better diagnostics, and native support for parallel test execution.

## Steps

1. **Find the solution file** (*.sln) in the current directory
   - If no .sln found, warn and stop

2. **Check for existing global.json** in the solution root directory
   - Read contents if file exists

3. **Create or update global.json**:
   - If file **does not exist**, create it:
     ```json
     {
       "test": {
         "runner": "Microsoft.Testing.Platform"
       }
     }
     ```
   - If file **exists**, merge the `test` section while preserving all other content:
     - Parse existing JSON
     - Add or update the `test.runner` property
     - Preserve `sdk`, `msbuild-sdks`, and any other existing sections

4. **Verify JSON validity**:
   ```bash
   dotnet build
   dotnet test
   ```

5. **If build fails**, report the error and ask user how to proceed

6. **Report results**:
   - Confirm global.json was created or updated
   - Show the final global.json content
   - Confirm build status
   - Confirm tests run successfully

## Example global.json Configurations

**Minimal (new file):**
```json
{
  "test": {
    "runner": "Microsoft.Testing.Platform"
  }
}
```

**Merged (existing file with SDK pinning):**
```json
{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestMinor"
  },
  "test": {
    "runner": "Microsoft.Testing.Platform"
  }
}
```

## Error Handling

- If no .sln found: warn and stop
- If global.json exists but is invalid JSON: report error and ask user
- If build fails after update: show errors and ask user how to proceed
