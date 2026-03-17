---
name: dependabot-check
description: Check and update vulnerable dependencies
argument-hint: "[--ecosystem=nuget|npm] [--auto-merge]"
tags: [security, dependencies, dependabot, devsecops]
user-invocable: true
---

# Dependency Vulnerability Check

Check NuGet and npm dependencies for known vulnerabilities.

## What To Do

1. **.NET dependencies**:
   ```bash
   dotnet list package --vulnerable --include-transitive
   dotnet list package --outdated
   ```

2. **npm dependencies**:
   ```bash
   npm audit --json > npm-audit.json
   npm audit fix
   ```

3. **Configure Dependabot** (.github/dependabot.yml):
   ```yaml
   version: 2
   updates:
     - package-ecosystem: "nuget"
       directory: "/src/backend"
       schedule: { interval: "weekly" }
     - package-ecosystem: "npm"
       directory: "/src/frontend"
       schedule: { interval: "weekly" }
   ```

4. **Update specific package**: `dotnet add package PackageName --version X.Y.Z`

## Arguments
- `--ecosystem=<type>`: nuget or npm
- `--auto-merge`: Auto-merge minor/patch updates