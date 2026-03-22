---
name: start
description: Use when starting reverse engineering on an unfamiliar codebase to identify layers, patterns, and structure before detailed analysis
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git:*, mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Discovering Architecture

## Overview

Dispatch a subagent to systematically explore a codebase and identify its architectural layers, technology choices, and structure. The subagent produces a machine-parseable architecture document that drives downstream layer-by-layer analysis.

**Output:** `docs/unwind/architecture.md`

## When to Use

- Starting work on an unfamiliar codebase
- Onboarding to a new project
- Before planning a migration or major refactor
- Beginning a security audit or code review

## The Process

### Step 1: Gather Repository Information

**Run these commands FIRST** to get git info for source linking:

```bash
git remote get-url origin 2>/dev/null
git branch --show-current 2>/dev/null
```

Parse the remote URL:
- SSH format: `git@github.com:owner/repo.git` → `https://github.com/owner/repo`
- HTTPS format: `https://github.com/owner/repo.git` → `https://github.com/owner/repo`
- If no remote: use `local` type with null URL

Build the repository info block:
```yaml
repository:
  type: github|gitlab|bitbucket|local
  url: https://github.com/owner/repo  # or null if local
  branch: main                         # or null if local
  link_format: https://github.com/owner/repo/blob/main/{path}#L{start}-L{end}
```

### Step 2: Check for Existing Documentation

Check if `docs/unwind/architecture.md` exists:

```
Glob: docs/unwind/architecture.md
```

- If exists: Pass to subagent as "previous analysis" for refresh mode
- If not: Fresh discovery

### Step 3: Dispatch Discovery Subagent

Dispatch an **Explore** subagent for fast codebase analysis. Note: Explore cannot write files, so you will write the output in Step 4.

**Include the repository info from Step 1 in the prompt:**

```
Task(subagent_type="Explore")
  description: "Discover codebase architecture"
  prompt: |
    [See Subagent Prompt below]

    ## Repository Information (already gathered)
    [paste the repository yaml block from Step 1]
```

The Explore agent should return the complete architecture document content as its output.

### Step 4: Write the Architecture Document

When the Explore subagent completes with the document content:

1. Create the output directory:
   ```bash
   mkdir -p docs/unwind
   ```

2. Write the content to `docs/unwind/architecture.md` using the Write tool

3. Verify the file was created

### Step 5: Present Results and Prompt User

After the subagent completes, present the results to the user:

```
## Architecture Discovery Complete

I've analyzed the codebase and created the architecture document.

**Output:** `docs/unwind/architecture.md`

### Summary
[Include the summary from the subagent - framework, layers detected, etc.]

### Detected Layers
[List layers with their confidence levels]

### Next Steps

Would you like me to:
1. **Continue with layer analysis** - Run `unwind:unwinding-codebase` to dispatch specialist subagents for each layer
2. **Review the architecture document first** - Open `docs/unwind/architecture.md` to verify the detection is accurate

[Use AskUserQuestion to let them choose]
```

**Important:** Always give the user the option to review before proceeding. The architecture document drives all subsequent analysis, so accuracy matters.

---

## Subagent Prompt

Use this prompt when dispatching the discovery subagent:

```
Explore this codebase to identify its architectural layers and structure.

## Your Task

Systematically explore the codebase and return the architecture document content. The main agent will write the file.

**Repository information has already been gathered and will be provided to you.** Use the provided `repository.link_format` for all source links.

## Phase 1: Project Identification

Identify the technology stack by looking for:

**Build System:**
- `package.json` → Node.js/JavaScript
- `pom.xml` / `build.gradle` → Java
- `requirements.txt` / `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `*.csproj` → .NET

**Framework:** Check dependencies for Spring Boot, Django, Express, Rails, Next.js, etc.

**Database:** Look for connection strings, ORM config, migration directories.

## Phase 2: Directory Mapping

Scan source directories and map to layers:

| Directory Pattern | Likely Layer |
|-------------------|--------------|
| `repository/`, `dao/`, `data/` | Database |
| `model/`, `entity/`, `domain/` | Domain Model |
| `service/`, `usecase/`, `application/` | Service Layer |
| `controller/`, `api/`, `rest/`, `graphql/` | API Layer |
| `messaging/`, `events/`, `queue/`, `kafka/` | Messaging |
| `components/`, `pages/`, `views/`, `ui/` | Frontend |

## Phase 3: Confidence Assessment

For each layer, assess confidence:
- **High**: Clear directory structure, multiple files, consistent naming
- **Medium**: Some indicators but mixed patterns
- **Low**: Minimal evidence
- **Not Detected**: No evidence found

## Phase 4: Cross-Cutting Concerns

Identify aspects spanning multiple layers:
- Authentication/Authorization
- Logging
- Error Handling
- Caching
- Validation

## Phase 5: Return Architecture Document

**DO NOT attempt to write the file** - you don't have write permissions. Instead, return the complete architecture document content in your response. The main agent will write it to `docs/unwind/architecture.md`.

Return the document in this exact format:

```markdown
# Architecture Discovery: [Project Name]

> **For Claude:** REQUIRED SUB-SKILL: Use unwind:unwinding-codebase to analyze each layer.

## Discovery Metadata

- **Generated:** [ISO timestamp]
- **Project Root:** [path]
- **Framework:** [detected framework]
- **Language:** [primary language]

## Repository Information

```yaml
repository:
  type: github|gitlab|bitbucket|local
  url: https://github.com/owner/repo  # or null if local
  branch: main                         # or null if local
  link_format: https://github.com/owner/repo/blob/main/{path}#L{start}-L{end}
```

**For all downstream agents:** Use `link_format` to create source links. Replace `{path}`, `{start}`, `{end}` with actual values.

## Layer Configuration

```yaml
layers:
  database:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points:
      - path/to/data/layer/
    dependencies: []

  domain_model:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points:
      - path/to/domain/
    dependencies: [database]

  service_layer:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points:
      - path/to/services/
    dependencies: [domain_model]

  api:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points:
      - path/to/controllers/
    dependencies: [service_layer]

  messaging:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points: []
    dependencies: [service_layer]

  frontend:
    status: detected|not_detected
    confidence: high|medium|low
    entry_points: []
    dependencies: [api]

cross_cutting:
  authentication:
    touches: [api, service_layer]
    entry_points:
      - path/to/security/
```

## Database Layer

**Status:** [Detected/Not Detected] | **Confidence:** [High/Medium/Low]

**Entry Points:**
- [directories/files]

**Initial Observations:**
- [What you found - technology, patterns, notable aspects]

---

[Repeat for each layer with status != not_detected]

---

## Cross-Cutting Concerns

### Authentication
**Touches:** [layers]
[Observations]

### [Other concerns...]

---

## Discovery Notes

- [Unknowns, questions, areas needing clarification]
```

{REFRESH_CONTEXT}

## Output

After creating the architecture document, provide a brief summary:
- Project type and framework
- Which layers were detected (with confidence)
- Any notable findings or concerns
```

---

## Refresh Mode Context

If previous architecture.md exists, add this to the subagent prompt:

```
## Previous Analysis

A previous architecture analysis exists. Compare the current codebase state to this previous analysis and:

1. Note any changes in the `## Changes Since Last Discovery` section
2. Update layer status/confidence if changed
3. Add new entry points discovered
4. Remove entry points that no longer exist
5. Update the `last_analyzed` timestamp

Previous analysis:
[CONTENTS OF EXISTING architecture.md]
```

---

## Layer Detection Reference

### Database Layer Indicators
- Directories: `repository/`, `dao/`, `data/`, `persistence/`
- Files: `*Repository.java`, `*_repository.py`, `*.repo.ts`
- ORM: Hibernate, SQLAlchemy, Prisma, TypeORM, Sequelize
- Migrations: Flyway, Liquibase, Alembic, Prisma migrations

### Domain Model Indicators
- Directories: `domain/`, `model/`, `entity/`, `entities/`
- Files: `*Entity.java`, `models.py`, `*.entity.ts`
- Patterns: `@Entity`, `class Model`, aggregates, value objects

### Service Layer Indicators
- Directories: `service/`, `services/`, `usecase/`, `application/`
- Files: `*Service.java`, `*_service.py`, `*.service.ts`
- Patterns: `@Service`, `@Transactional`, business logic methods

### API Layer Indicators
- Directories: `controller/`, `api/`, `rest/`, `routes/`, `graphql/`
- Files: `*Controller.java`, `views.py`, `*.controller.ts`
- Patterns: `@RestController`, `@router`, route definitions

### Messaging Layer Indicators
- Directories: `messaging/`, `events/`, `queue/`, `kafka/`, `rabbitmq/`
- Files: `*Listener.java`, `*Consumer.py`, `*.handler.ts`
- Configs: Kafka, RabbitMQ, SQS configuration

### Frontend Layer Indicators
- Directories: `components/`, `pages/`, `views/`, `ui/`, `src/app/`
- Files: `*.tsx`, `*.vue`, `*.component.ts`
- Configs: React, Vue, Angular, Next.js, Nuxt
