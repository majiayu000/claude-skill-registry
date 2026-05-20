---
name: ln-781-build-verifier
description: Builds all detected projects and verifies successful compilation
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-781-build-verifier

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-780-bootstrap-verifier

---

## Purpose

Detects project types, restores dependencies, executes builds, and verifies successful compilation.

**Scope:**
- Auto-detect project types from file markers
- Restore dependencies using appropriate package manager
- Execute build commands for each project
- Verify build artifacts exist

**Out of Scope:**
- Running tests (handled by ln-782)
- Container operations (handled by ln-783)
- Workflow orchestration (handled by ln-780)

---

## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| Called by ln-780 orchestrator | Yes |
| Standalone build verification | Yes |
| CI/CD pipeline build step | Yes |
| Test execution needed | No, use ln-782 |

---

## Workflow

### Step 1: Detect Project Types

Scan project root for type markers.

| Marker File | Project Type | Build System |
|------------|--------------|--------------|
| package.json | Node.js/Frontend | npm/yarn/pnpm |
| *.csproj | .NET | dotnet |
| setup.py / pyproject.toml | Python | pip/poetry |
| go.mod | Go | go build |
| Cargo.toml | Rust | cargo |
| pom.xml | Java/Maven | mvn |
| build.gradle | Java/Gradle | gradle |

### Step 2: Restore Dependencies

For each detected project, restore dependencies before building.

| Project Type | Dependency Restoration |
|--------------|----------------------|
| Node.js | Install packages from lock file |
| .NET | Restore NuGet packages |
| Python | Install from requirements or pyproject |
| Go | Download modules |
| Rust | Fetch crates |

### Step 3: Build Projects

Execute build for each project type in Release/Production mode.

| Project Type | Build Mode | Expected Outcome |
|--------------|-----------|------------------|
| Node.js | Production | Bundled assets in dist/ or build/ |
| .NET | Release | Compiled DLLs in bin/Release/ |
| Python | Editable install | Package installed in environment |
| Go | Production | Compiled binary |
| Rust | Release | Optimized binary in target/release/ |

### Step 4: Verify Build Artifacts

Confirm build outputs exist.

| Project Type | Artifact Check |
|--------------|---------------|
| Node.js | dist/ or build/ directory exists, contains files |
| .NET | DLL files in bin/Release/{framework}/ |
| Python | Package importable |
| Go | Binary executable exists |
| Rust | Binary in target/release/ |

### Step 5: Report Results

Return structured results to orchestrator.

**Result Structure:**

| Field | Description |
|-------|-------------|
| projectName | Name of the project |
| projectType | Detected type (nodejs, dotnet, python, etc.) |
| status | success / failed |
| duration | Build time in seconds |
| outputPath | Path to build artifacts |
| errorMessage | Error details if failed |

---

## Error Handling

| Error Type | Recovery Action |
|------------|----------------|
| Dependency restore failed | Check network, verify lock file integrity |
| Compilation errors | Log full error output, report as failed |
| Missing build tool | Report required tool installation |
| Timeout | Report timeout, suggest increasing limit |

---

## Critical Rules

1. **Always restore dependencies first** - builds may fail without fresh dependencies
2. **Use production/release mode** - development builds may hide issues
3. **Verify artifacts exist** - successful exit code is not sufficient
4. **Report all projects** - include both successful and failed builds

---

## Definition of Done

- [ ] All project types detected
- [ ] Dependencies restored for each project
- [ ] Build executed for each project
- [ ] Artifacts verified to exist
- [ ] Results returned to orchestrator

---

## Reference Files

- Parent: `../ln-780-bootstrap-verifier/SKILL.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
