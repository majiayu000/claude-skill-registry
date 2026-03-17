---
name: scaffold
description: >
  Use when creating a new greenfield .NET 9 + React 19 project structure.
  Optionally accepts a spec file path or inline MVP description.
user-invocable: true
allowed-tools: Bash, Write, Read, Glob
argument-hint: ~/repos/playground/my-new-project [spec-file-or-text]
---

# Scaffold: .NET 9 + React 19 Project

Creates a complete greenfield project structure ready for development.

**Tech stack:** .NET 9, ASP.NET Core, React 19, Vite, TypeScript, Tailwind CSS v4, Zustand, SQLite.

## Input

`$ARGUMENTS` contains one or two arguments:

1. **`$1`** (required) — absolute or relative path to the project root directory (e.g., `~/repos/playground/my-app`).
2. **`$2`** (optional) — an MVP spec, either as:
   - A **file path** to a spec/outline document (e.g., `~/docs/mvp-outline.md`)
   - **Inline text** describing the MVP (e.g., `"A marketplace where freelancers sell AI skills"`)

**Parsing rules:** Split `$ARGUMENTS` on the first whitespace to get `$1`. Everything after that first whitespace is `$2`. If `$2` is quoted, strip the surrounding quotes.

**Validation:** If `$1` is empty or missing, STOP with error: "Usage: /scaffold <project-path> [spec-file-or-text]".

Expand `~` to the user's home directory. Resolve relative paths against the current working directory.

If the target directory already exists AND contains a `CLAUDE.md` file, STOP: "Project already exists at {path}."

### Detecting spec type (when `$2` is present)

1. Expand `~` in `$2` and resolve relative paths.
2. Check if the resolved path exists as a file on disk (use `test -f`).
   - **If file exists:** treat `$2` as a spec file path. Read its full contents.
   - **If file does not exist:** treat `$2` as inline text.

## Steps

### 1. Create directory structure

```bash
mkdir -p {path}/backend {path}/frontend {path}/_docs
```

Result:
```
{path}/
├── backend/
├── frontend/
└── _docs/
```

### 2. Process spec (only when `$2` is provided)

**Skip this step entirely if `$2` was not provided.**

#### 2a. Store the full spec

- **If `$2` is a file path:** Read the file contents and write them VERBATIM to `{path}/_docs/spec.md`.
- **If `$2` is inline text:** Write the text as-is to `{path}/_docs/spec.md`.

The file `_docs/spec.md` must contain the FULL original input, unmodified.

#### 2b. Extract the project mission

Read the spec content (whether from file or inline text) and distill a **1-3 sentence project mission** that captures the core concept. This is a brief description of WHAT the project is, not HOW to build it.

Store the result as `{mission}` — it will be used in step 4 (CLAUDE.md).

**Guidelines for extraction:**
- Focus on the core product/service concept
- Strip implementation details, phases, and technical plans
- If the input is already short (1-3 sentences), use it directly as the mission
- If the input is long (a brainstorm doc, full spec, etc.), synthesize the essence

### 3. Create `.gitignore`

Write this EXACT content to `{path}/.gitignore`:

```
# .NET
bin/
obj/
*.user
.vs/

# Node
node_modules/
dist/
.vite/

# IDE
.idea/

# OS
.DS_Store

# Environment
.env
.env.local

# SQLite
*.db
*.db-journal
```

### 4. Create `CLAUDE.md`

Derive `{project_name}` from the directory name (e.g., `/tmp/my-app` → `my-app`).

Write this EXACT template to `{path}/CLAUDE.md`:

````markdown
# CLAUDE.md — {project_name}

## Project
{project_description}

## Tech Stack
- Backend: .NET 9, ASP.NET Core, EF Core 9, SQLite
- Frontend: React 19, Vite, TypeScript, Tailwind CSS v4, Zustand

## Implementation Status
<!-- Updated after each feature completion -->

*No features implemented yet.*

## Commands

### Backend
```bash
cd backend && dotnet restore && dotnet build && dotnet run
```

### Frontend
```bash
cd frontend && npm install && npm run dev
```

### Tests
```bash
cd backend && dotnet test
cd frontend && npm test
```
````

**Substitution for `{project_description}`:**
- **If `$2` was NOT provided:** use `{to be populated}`
- **If `$2` WAS provided:** use `{mission}` from step 2b (1-3 sentences, NOT the full spec — the full spec lives in `_docs/spec.md`)

### 5. Create minimal backend with health endpoint

Run from within the project directory:

```bash
cd {path}/backend && dotnet new web -n Api
```

Then **overwrite** `{path}/backend/Api/Program.cs` with this EXACT content:

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod());
});

var app = builder.Build();
app.UseCors();

app.MapGet("/health", () => Results.Ok(new { status = "healthy" }));

app.Run();
```

This provides:
- `/health` endpoint for E2E test startup detection
- Permissive CORS for local dev
- Minimal foundation for backend implementation

### 6. Git init + initial commit

```bash
cd {path} && git init && git add . && git commit -m "chore: initial scaffold"
```

## Self-Verify Gate Checklist

After completing all steps, verify EVERY item. If ANY item fails, fix it before reporting success.

**Always verify (8 items):**

- [ ] Directory `backend/` exists
- [ ] Directory `frontend/` exists
- [ ] Directory `_docs/` exists
- [ ] File `CLAUDE.md` exists at project root
- [ ] File `.gitignore` exists at project root
- [ ] File `backend/Api/Program.cs` exists AND contains `/health` endpoint
- [ ] `.git/` exists (git repo initialized)
- [ ] At least one commit exists (`git log --oneline -1` succeeds)

**Additionally verify when spec was provided (+3 items):**

- [ ] File `_docs/spec.md` exists
- [ ] `_docs/spec.md` contains the full original spec content (not truncated)
- [ ] `CLAUDE.md` `## Project` section contains a brief mission (NOT the placeholder `{to be populated after Phase 0}`)

**Verification commands:**
```bash
cd {path}
test -d backend && echo "PASS: backend/" || echo "FAIL: backend/"
test -d frontend && echo "PASS: frontend/" || echo "FAIL: frontend/"
test -d _docs && echo "PASS: _docs/" || echo "FAIL: _docs/"
test -f CLAUDE.md && echo "PASS: CLAUDE.md" || echo "FAIL: CLAUDE.md"
test -f .gitignore && echo "PASS: .gitignore" || echo "FAIL: .gitignore"
grep -q "/health" backend/Api/Program.cs && echo "PASS: /health endpoint" || echo "FAIL: /health endpoint"
test -d .git && echo "PASS: .git/" || echo "FAIL: .git/"
git log --oneline -1 && echo "PASS: commit exists" || echo "FAIL: no commits"
```

**Additional verification when spec was provided:**
```bash
test -f _docs/spec.md && echo "PASS: _docs/spec.md" || echo "FAIL: _docs/spec.md"
grep -q "to be populated" CLAUDE.md && echo "FAIL: CLAUDE.md still has placeholder" || echo "PASS: CLAUDE.md has mission"
```

Report without spec: "Scaffold complete at {path}. All 8 gate items verified."
Report with spec: "Scaffold complete at {path}. All 11 gate items verified (spec seeded)."
