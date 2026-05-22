---
version: 1.0.0
name: dev-dependency
description: >
  Audit and update project dependencies. Auto-detects package managers (NuGet, npm)
  from the project or uses workflow.json project type. Runs both backend and frontend
  checks in mixed projects. Filter with "nuget" or "npm" to target one stack.
  Use when the user says "update dependencies", "check packages", "audit deps",
  "upgrade packages", or invokes /dev-dependency.
disable-model-invocation: true
user-invocable: true
argument-hint: "[nuget | npm | --audit | --patch | --minor | --major | --security]"
---

# Dependency Update — Unified Entry Point

Routes to the appropriate backend and/or frontend dependency skill based on
project type and user request.

## Step 1: Detect Stacks

Determine which package managers are present. Check in this order:

1. **Explicit filter** — if the user passed `nuget` or `npm`, use only that stack
2. **Project detection** — scan the project root:
   - NuGet: any `*.csproj`, `*.sln`, or `Directory.Packages.props` file exists
   - npm: `package.json` exists
3. **workflow.json fallback** — if detection is inconclusive, read `workflow.json`:
   - `type: "api"` or `type: "library"` → NuGet
   - `type: "frontend"` → npm
   - `type: "docs"` → npm (VitePress)
   - No workflow.json → scan for both

If both stacks are detected and no filter was given, run both.

## Step 2: Report Plan

Before running, show what will execute:

```
Dependencies: detected NuGet + npm
Running: both (use /dev-dependency nuget or /dev-dependency npm to target one)
```

Or if filtered:
```
Dependencies: running npm only (filtered)
```

Or if only one stack found:
```
Dependencies: detected NuGet only
```

## Step 3: Execute

### NuGet (if applicable)

Read and follow `.claude/skills/dev-dependency-backend/SKILL.md` completely.
Pass through any flags (--audit, --patch, --minor, --major, --security, --interactive).

### npm (if applicable)

Read and follow `.claude/skills/dev-dependency-frontend/SKILL.md` completely.
Pass through any flags.

### Both (sequential)

When running both stacks:
1. Run NuGet first (backend changes shouldn't affect frontend)
2. Show a brief summary of NuGet results
3. Run npm second
4. Show combined summary at the end

## Step 4: Combined Summary (when both ran)

```
### Dependency Update Summary

#### NuGet
- Updated: X packages (Y patch, Z minor)
- Security: N vulnerabilities fixed
- Skipped: M major updates (user deferred)

#### npm
- Updated: X packages (Y patch, Z minor)
- Security: N vulnerabilities fixed
- Skipped: M major updates (user deferred)
```

## Flags

All flags are passed through to the underlying backend/frontend skills.

| Flag | Behavior |
|------|----------|
| `nuget` | Run NuGet checks only |
| `npm` | Run npm checks only |
| `--audit` | Report only, don't update |
| `--patch` | Apply patch updates (safe) |
| `--minor` | Apply minor updates (review) |
| `--major` | Apply major updates (always asks) |
| `--security` | Security fixes only (urgent) |
| `--interactive` | Step through each update |
