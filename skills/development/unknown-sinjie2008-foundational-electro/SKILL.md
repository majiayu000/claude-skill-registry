---
name: project-specification-writer
description: Generate a complete software specification document for the current project/repo, including architecture, data model, key processes, pseudocode, and Mermaid diagrams (context, container/deployment, module relations, sequence, ER, class, flowchart, state).
metadata:
  short-description: Generate a full spec doc (12 required sections + diagrams).
---

# Project Specification Writer (Instruction-only)

## Goal
When invoked, produce a **single, comprehensive specification document** for the **current repository/project** with **all required sections**:

1. Architecture and technology choices  
2. Data model  
3. Key processes  
4. Pseudocode  
5. System context diagram  
6. Container/deployment overview  
7. Module relationship diagram (Backend / Frontend)  
8. Sequence diagram  
9. ER diagram  
10. Class diagram (key backend classes)  
11. Flowchart  
12. State diagram  

**Default output file:** `docs/specification.md`  
(If `docs/` does not exist, create it. If user requests another path, follow it.)

---

## Invocation behavior
### Minimal questions policy
Ask **at most 5** clarifying questions **only if** the repo does not contain enough information to avoid unsafe guessing.  
If information is missing, proceed with best-effort inference and add an **“Assumptions & Open Questions”** section near the top.

### No hallucinations rule
Do **not** invent details. If you cannot locate evidence in the repo, label as:
- **Assumption**
- **Unknown/TBD**
- **Open question**

---

## Repo reconnaissance workflow (do this first)
1. Identify repo root and high-level structure:
   - Look for: `README*`, `docs/`, `architecture/`, `ADR*`, `design*`, `SPEC*`.
2. Detect tech stack and runtime:
   - Backend signals: `pyproject.toml`, `requirements.txt`, `go.mod`, `pom.xml`, `build.gradle`, `.csproj`, `package.json` (server), `Dockerfile`
   - Frontend signals: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `vite.config.*`, `next.config.*`
3. Detect data layer:
   - DB migrations: `migrations/`, `prisma/schema.prisma`, `alembic/`, `db/schema.sql`, `knexfile.*`
   - ORM models: `models/`, `entities/`, `schema/`
4. Detect deployment:
   - `docker-compose.yml`, `Dockerfile*`, `k8s/`, `helm/`, `.github/workflows/*`, `terraform/`
5. Collect “evidence pointers” while reading (file paths + brief notes).  
   You will use these pointers throughout the spec.

---

## Output requirements (strict)
- Produce **one Markdown document**.
- Use **clear headings** matching the 12 required items.
- All diagrams must be in fenced Mermaid blocks:  
  \`\`\`mermaid  
  ...  
  \`\`\`
- Each section must be **project-specific** (grounded in repo findings).
- Keep diagrams at the right abstraction level:
  - **Context/Container**: high-level systems and deployed containers/services
  - **Module diagram**: major frontend/backend modules and their dependencies
  - **Class diagram**: only key backend classes (5–15), not every class

---

# Specification Document Template (write exactly this structure)

# {{Project Name}} — Specification
**Version:** {{date}}  
**Repo:** {{repo identifier if known}}  
**Primary stack:** {{inferred stack}}  

## Assumptions & Open Questions
- Assumption: ...
- Open question: ...

## 1. Architecture and technology choices
### 1.1 Architecture overview
- System style (e.g., monolith, modular monolith, microservices)
- Key components and responsibilities
- Trust boundaries (auth, secrets, network zones) if applicable

### 1.2 Technology choices (with rationale)
Provide a table:
| Area | Choice | Evidence | Why this choice | Alternatives considered |
|---|---|---|---|---|

### 1.3 Non-functional requirements (NFRs)
- Performance, availability, security, observability, compliance, cost
- What the repo suggests (or what’s missing)

## 2. Data model
### 2.1 Conceptual model
- List core entities and what they represent
- Identify ownership and lifecycle boundaries

### 2.2 Logical model (tables/collections)
Provide a table:
| Entity/Table | Primary key | Key fields | Relationships | Notes |
|---|---|---|---|---|

### 2.3 Data integrity & constraints
- Uniqueness, foreign keys, soft delete, audit fields, tenancy strategy, etc.

## 3. Key processes
List 3–7 “key processes” (system behaviors) using this structure:
- **Process name**
  - Trigger:
  - Inputs:
  - Outputs:
  - Key steps:
  - Error cases:
  - Observability (logs/metrics/traces):

## 4. Pseudocode
For each key process, provide pseudocode:
- Use clear function signatures
- Include validation, error handling, retries/transactions where relevant

Example format:
```text
function ProcessName(input):
  validate input
  begin transaction (if needed)
  ...
  return result
