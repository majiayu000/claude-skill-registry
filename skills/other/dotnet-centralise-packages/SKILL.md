---
name: dotnet-centralise-packages
description: Converts a .NET solution to use Central Package Management (CPM). Use when the user wants to centralize, consolidate, or unify NuGet package versions across projects.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob AskUserQuestion
---

Convert the current .NET solution to use Central Package Management, centralizing all package versions in a single `Directory.Packages.props` file.

## Steps

1. **Find the solution file** (*.sln) in the current directory
   - If no .sln found, warn and stop

2. **List all packages** (including transitive)
   ```bash
   dotnet package list --include-transitive --format json
   ```

3. **Parse JSON output** to extract:
   - All unique packages across all projects
   - Their versions
   - Whether each package is **direct** or **transitive**
   - If same package has different versions, use the highest version

4. **Check for existing CPM files**
   - If `Directory.Packages.props` exists, ask user: overwrite or merge
   - Note existing `Directory.Build.props` content if present

5. **Create `Directory.Packages.props`** next to the .sln file:
   ```xml
   <Project>
     <ItemGroup>
       <PackageVersion Include="PackageName" Version="X.Y.Z" />
       <!-- one entry per unique package -->
     </ItemGroup>
   </Project>
   ```

6. **Create or update `Directory.Build.props`** next to the .sln file:
   - If file exists, add the property to existing content
   - If file doesn't exist, create it:
   ```xml
   <Project>
     <PropertyGroup>
       <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
     </PropertyGroup>
   </Project>
   ```

7. **Update all .csproj files**:
   - Remove `Version` attribute from all `<PackageReference>` elements
   - Before: `<PackageReference Include="Newtonsoft.Json" Version="13.0.3" />`
   - After: `<PackageReference Include="Newtonsoft.Json" />`

8. **Run build** to verify:
   ```bash
   dotnet build
   ```

9. **If build fails**, ask the user:
   - **Fix automatically**: Review errors and attempt fixes
   - **Fix manually**: Show errors and let user handle

10. **Report results**:
    - List all created/modified files
    - Show package count centralized
    - Confirm build status

## Transitive vs Direct Packages

- **Direct packages**: Explicitly in csproj via `<PackageReference>`. These get centralized.
- **Transitive packages**: Pulled in as dependencies. Generally NOT centralized unless:
  - User explicitly wants to pin a transitive package version
  - A transitive package needs a security update

When centralizing:
- Only add **direct** packages to `Directory.Packages.props` by default
- Report transitive packages separately for awareness
- If user wants to pin a transitive, add it as a `<PackageVersion>` entry

## Version Conflict Resolution

When the same package has different versions across projects:
- Automatically use the highest/latest version
- No user prompt needed

## Error Handling

- If no .sln found: warn about solution-level CPM requirement
- If `Directory.Packages.props` already exists: ask to overwrite or merge
- If build fails after conversion: offer automatic fix or manual intervention
