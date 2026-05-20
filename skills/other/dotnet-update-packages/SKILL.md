---
name: dotnet-update-packages
description: Lists and updates outdated NuGet packages in .NET projects. Use when the user mentions updating packages, checking for outdated dependencies, or upgrading package versions.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob AskUserQuestion
---

# .NET Package Updates

> **Note:** This skill requires .NET 10 SDK or later. The `dotnet package update` command does not exist in .NET 8-9.

## When to Use

This skill applies when the user:
- Asks about outdated NuGet packages
- Wants to update dependencies in a .NET project
- Mentions package version upgrades
- Discusses dependency management in .NET

## Workflow

1. **List outdated packages** (including transitive) using:
   ```bash
   dotnet package list --outdated --include-transitive --format json
   ```

2. **Check for empty results** - If no outdated packages found, inform the user and stop

3. **Parse output** to identify:
   - Projects with outdated packages
   - Whether each package is **direct** or **transitive**

4. **Analyze project dependencies** by reading `<ProjectReference>` elements in each csproj

5. **Present findings** in a readable format showing project, package name, current → latest version

6. **Confirm with user** before making changes - ask which option:
   - All packages
   - Specific packages by name
   - Cancel

7. **Update packages per project** with `--project` parameter:
   - Update leaf projects first (no dependencies)
   - Then update dependent projects
   - Independent branches can run in parallel
   ```bash
   dotnet package update <package> --project <path-to-csproj>
   ```

8. **Verify** with `dotnet build`

9. **If build fails**, ask user:
   - Fix automatically (review errors, apply fixes)
   - Fix manually (show errors, let user handle)

10. **Report results** - summarize what was updated and the final build status

## Key Commands

| Command | Purpose |
|---------|---------|
| `dotnet package list --outdated --include-transitive --format json` | List outdated packages (incl. transitive) |
| `dotnet package update <name> --project <path>` | Update specific package in project |
| `dotnet package update --project <path>` | Update all packages in project |

## Transitive vs Direct Packages

- **Direct**: Explicitly in csproj. Update directly.
- **Transitive**: Pulled in by dependencies. Marked `[T]` in output.
  - To update: update the parent package, or add direct reference to pin version

## Error Handling

- **If `dotnet package list` fails**: Check if we're in a .NET project directory
- **If `dotnet package update` fails for a specific package**: Report it and continue with others
- **If build fails after updates**:
  1. Parse the build errors
  2. Ask user: fix automatically or manually?
  3. If automatic: analyze errors and apply fixes
  4. Re-run build to verify

## Notes

- Requires .NET 8+ SDK for `dotnet package update`
- Always use `--project` parameter to update per-project
- Update in dependency order: leaves first, then dependents
- Always confirm with user before updating
- Run build after updates to catch breaking changes
