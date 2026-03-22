---
name: project-init
description: Initialize AI context for an existing project — deep scan the codebase, detect tech stack, identify subprojects and major modules, generate root CLAUDE.md, ARCHITECTURE.md, TESTING.md, and directory-scoped CLAUDE.md files for subprojects and significant directories. Works with monorepos, polyglot projects, and large codebases via iterative scanning.
context: fork
---

# Project Init

Deep-scan an existing project and generate AI context files (`CLAUDE.md`, `ARCHITECTURE.md`, `TESTING.md`) for the root and all significant subprojects. After completion, Claude has the context it needs: tech stack, conventions, structure, setup, testing, security.

## 1. Initial Reconnaissance

### 1a. Root Structure Scan

```
// turbo
ls -la  # or Get-ChildItem on Windows
```

Identify stack signals:

| Signal | Indicates |
|---|---|
| `package.json`, `tsconfig.json` | Node.js / TypeScript |
| `pom.xml`, `build.gradle` | Java / Spring |
| `pyproject.toml`, `requirements.txt` | Python |
| `go.mod` | Go |
| `*.csproj`, `*.sln` | .NET |
| `Cargo.toml` | Rust |
| `Dockerfile`, `docker-compose.yml` | Containerized |
| `terraform/`, `*.tf` | Infrastructure as Code |
| `helm/`, `k8s/`, `charts/` | Kubernetes |
| Multiple `package.json` / `pom.xml` | Monorepo |
| `nx.json`, `turbo.json`, `pnpm-workspace.yaml`, `lerna.json` | Monorepo tooling |
| `content/blog/`, `posts/`, `.mdx` files with frontmatter | Blog / file-based content |
| `llms.txt` | AI search optimization |

### 1b. Detect Project Boundaries

Identify **project boundaries** — directories that are independent units:
- **Monorepo**: `apps/`, `packages/`, `services/`, `libs/` with own config files
- **Single project**: One root config, directories are modules (`src/`, `app/`, `internal/`)

Build a **project map**:

```
Project Root
├── [subproject-1] (type: service, stack: Java Spring Boot)
├── [subproject-2] (type: frontend, stack: Next.js + TypeScript)
├── [subproject-3] (type: infra, stack: Terraform)
└── [shared-lib]   (type: library, stack: TypeScript)
```

### 1c. Check for Existing Context Files

```
// turbo
find . -name "CLAUDE.md" -o -name "ARCHITECTURE.md" -o -name "TESTING.md" -o -name "FEATURES.md" | head -20
```

If files exist — read them, note gaps. Create missing files, update outdated ones (with user confirmation).

## 2. Deep Scan — Iterative

Process one boundary at a time. **Scan limits**: max 10 boundaries, 20 files per boundary, 3 levels deep. For 100+ file boundaries, summarize from directory listing and configs only.

### 2a. Per-Boundary Scan Sequence

For each subproject or the root project:

1. **Config files first** — `package.json`, `pom.xml`, `pyproject.toml`, `go.mod`, `*.csproj`, `tsconfig.json`, `.eslintrc`, `Dockerfile`
2. **Entry points** — `main.ts`, `App.tsx`, `main.py`, `Main.java`, `main.go`, `Program.cs`
3. **Directory structure** — list 2–3 levels deep to understand module organization
4. **Key patterns** — read 1–2 representative files from each major directory to understand conventions:
   - Naming patterns (files, classes, functions)
   - Import style and module organization
   - Error handling patterns
   - Testing patterns (find test files)
5. **CI/CD** — `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`, `cloudbuild.yaml`
6. **Docs** — `README.md`, `docs/`, `CONTRIBUTING.md`
7. **Content** — two patterns to detect:
   - **Static content files** — `static-content/`, `data/` dirs with TS/JS exports. Map content file → sections → consuming pages
   - **File-based content (blog/docs)** — `content/blog/`, `posts/`, MDX/MD directories. Read 1-2 sample files to extract: frontmatter format (all fields, types, required/optional), file naming convention, cover image path pattern, tags/categories, discovery assets (`llms.txt`, sitemap config, RSS feed)
8. **UI conventions** — grep for icon libs (`lucide`, `solar`, `phosphor`), animation libs (`framer-motion`, `gsap`), component libs (`shadcn`, `radix`, `mui`), icon registries
9. **AI tooling** — `.codeiumignore`, `.cursorignore`, `.gitignore` — paths AI tools cannot access

### 2b. Identify Significant Directories

Identify directories warranting their own scoped `CLAUDE.md`. **Criteria** (any one): 10+ files with distinct responsibility, clear architectural layer, different conventions than parent, public API surface, generated code, infrastructure code.

**Common significant directories:**

| Stack | Significant Directories |
|---|---|
| Java Spring Boot | `controller/`, `service/`, `repository/`, `model/`, `config/`, `exception/` |
| Next.js / React | `app/`, `components/`, `lib/`, `hooks/`, `api/`, `middleware/` |
| FastAPI / Python | `routers/`, `services/`, `models/`, `schemas/`, `dependencies/` |
| Go | `cmd/`, `internal/`, `pkg/`, `handler/`, `store/`, `middleware/` |
| .NET | `Controllers/`, `Services/`, `Models/`, `Data/`, `Middleware/` |

## 3. Generate Root CLAUDE.md

Use the matching stack-specific template from `templates/agentsmd/` as a starting point. If no stack matches, use `templates/agentsmd/universal.agentmd.template.md`. Fill in all sections based on deep scan results from Step 2.

**Critical rules:**
- State the **tech stack explicitly** — this drives Claude Code's role activation via (agent)
- Include **real setup commands** — extracted from config files and CI, copy-pastable
- Link to `ARCHITECTURE.md` and `TESTING.md` in the Architecture reference and Testing Instructions sections
- **Map content architecture** (if applicable) — which content files drive which pages. Prevents repeated `code_search` during content edits
- **Document UI conventions** (if applicable) — icon set + variant + registry, animation library, component library
- **Document blog conventions** (if applicable) — frontmatter format, file naming, discovery assets. Enables `/blog-post` workflow
- Keep **concise** — avoid repeating what scoped CLAUDE.md files will cover

## 4. Generate ARCHITECTURE.md

**Apply `Agent(system-architect)` role** for this step. The system architect owns the ARCHITECTURE.md file — creation, updates, and reviews.

Use `templates/architecture.template.md` as the starting point. Fill in all 11 sections based on the deep scan results from Step 2.

**Rules:**
- Mermaid/ASCII diagrams for all visual elements
- Document what exists now, not aspirations. Include versions
- Focus on relationships and data flows
- **Monorepos**: Root ARCHITECTURE.md (system-wide) + per-subproject for each service with own build config. Skip doc-only, config-only, type-only dirs

## 5. Generate TESTING.md

**Apply `Agent(qa-engineer)` role** for this step. The QA engineer owns the TESTING.md file — creation, updates, and reviews.

Use `templates/testing.template.md` as the starting point. Fill in all sections based on the deep scan results from Step 2.

### 5a. Root TESTING.md

Create `TESTING.md` at the project root using `templates/testing.template.md` (root template section). Fill in all placeholders based on deep scan results from Step 2. All sections in the template are required — remove only those marked with `<!-- Remove ... -->` comments.

**Key data sources**: test config files → test types and commands; CI pipeline → pipeline stages; directory listing → test organization; `.env.example` → credential structure.

### 5b. Per-Service TESTING.md (Monorepos)

For each subproject/service identified in Step 1b, create a scoped `TESTING.md` using `templates/testing.template.md` (per-service template section at the bottom of the file).

**Rules:**
- Include actual commands — copy-pastable, tested
- Reference root `.env` for credentials (`test_` prefixed vars), do not duplicate
- List key test scenarios for critical paths (auth, payments, data mutations)
- Keep service-specific — do not repeat root TESTING.md content

### 5c. Single-Project (Non-Monorepo)

For single-project repos, create only root `TESTING.md` (no per-service files). Include all service-level detail directly in the root file.

## 6. Generate Scoped CLAUDE.md Files

For each significant directory identified in Step 2b, create a scoped `CLAUDE.md`:

```markdown
# CLAUDE.md

## Purpose
[1 sentence: what this directory contains and its role in the architecture]

## Conventions
[Directory-specific patterns, naming, file organization]

## Key Files
[Important files with brief descriptions]

## Patterns
[Code patterns used in this directory — how to add new items]

## Testing
[How to test code in this directory specifically]

## Do NOT
[Directory-specific anti-patterns and constraints]
```

**Rules for scoped CLAUDE.md:**
- **Never repeat root CLAUDE.md content** — reference it if needed
- **Be directory-specific** — only include information relevant to THIS directory
- **Include "how to add new X"** — the most common operation in each directory
- **Keep it short** — 20–50 lines. Developers read these frequently
- **State constraints** — what should NOT be in this directory

### Example

**`src/controllers/AGENTS.md`** — Purpose, naming convention (`{Resource}Controller.java`), injection rules (constructor, never repositories directly), validation (`@Valid`), "Adding a New Controller" steps.

## 7. Review and Confirm

Present a summary of all files to be created:

```
## Project Init Summary

### Files to create:
- [ ] CLAUDE.md (root) — [X lines]
- [ ] ARCHITECTURE.md (root) — [X lines]
- [ ] TESTING.md (root) — [X lines]
- [ ] [service-1]/TESTING.md — [X lines] (monorepo only)
- [ ] [service-2]/TESTING.md — [X lines] (monorepo only)
- [ ] src/controllers/AGENTS.md — [X lines]
- [ ] src/services/AGENTS.md — [X lines]
- [ ] ...

### Project map:
[project boundary diagram from Step 1b]

### Tech stack detected:
[list of technologies, frameworks, tools]
```

**Wait for user APPROVE before writing files.** User may skip directories, add undetected ones, or adjust content.

## 8. Write Files

After approval, create all files. For each file:
1. Write the content
2. Verify it was created successfully
3. Report any issues

If updating existing files — show the diff and request confirmation.

## 9. Verify

After all files are created:

```
// turbo
find . -name "CLAUDE.md" -o -name "ARCHITECTURE.md" -o -name "TESTING.md" | sort
```

Verify:
- [ ] Root `CLAUDE.md` exists and contains correct tech stack
- [ ] Root `CLAUDE.md` links to `TESTING.md` in Testing Instructions section
- [ ] Root and per-subproject `ARCHITECTURE.md` files exist
- [ ] Root `TESTING.md` exists with all test types, commands, infrastructure
- [ ] Per-service `TESTING.md` files exist for each subproject (monorepos)
- [ ] All significant directories have scoped `CLAUDE.md`
- [ ] No redundancy between root and scoped files
- [ ] All test commands are accurate and copy-pastable
- [ ] No secrets, PII, or hardcoded credentials in any file (especially `.env` test values)

## Integration

- **Precedes**: All other workflows — run this first on a new project
- **Templates**: `templates/agentsmd/*.agentmd.template.md`, `templates/architecture.template.md`, `templates/testing.template.md`
- **Roles**: `Agent(system-architect)` (ARCHITECTURE.md creation/review), `Agent(qa-engineer)` (TESTING.md creation/review), `Agent(cloud-architect)` (cloud infrastructure context), `Agent(devops-architect)` (CI/CD architecture context)
- **Skills**: `testing-procedures` skill (test strategy, coverage targets)
- **Enables**: `/feature-plan`, `/feature-dev`, `/bugfix`, `/test-local`, `/run-tests`
