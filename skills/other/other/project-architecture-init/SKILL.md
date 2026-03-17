---
name: project-architecture-init
description: "This skill should be used after the requirement-analysis and tech-stack-confirmation skills have been completed (PRD, technology stack decisions, and ADRs already exist). It reads existing artifacts and produces three deliverables: (1) a detailed architecture design document defining package structure, module boundaries, and dependency rules, (2) a runnable walking skeleton that validates all technology integrations, and (3) automated safeguards including unit tests, integration tests, architecture fitness functions, and CI pipeline configuration. Triggers on requests like 'initialize project architecture', 'scaffold project', 'set up project structure', 'create walking skeleton', 'generate design document from tech stack', or 'bootstrap project from PRD'."
---

# Project Architecture Init

## Overview

This skill transforms existing PRD, technology stack decisions, and ADRs into a production-ready project foundation. It focuses on three deliverables that the upstream skills have NOT yet produced: (1) a detailed architecture design document mapping package structure, module boundaries, and dependency rules, (2) a runnable initialized environment (walking skeleton), and (3) automated safeguards — unit tests, integration tests, architecture fitness functions, and CI pipeline.

## Prerequisites

Before using this skill, verify that these artifacts already exist (produced by upstream skills):

1. **PRD document** — produced by the `requirement-analysis` skill
2. **Technology stack document** — produced by the `tech-stack-confirmation` skill, containing:
   - Development language, framework, and build tool
   - Database and caching choices
   - Testing tools and frameworks
   - DevOps / infrastructure choices
   - Key dependencies list
   - Architecture overview diagram
3. **ADR files** — produced by the `tech-stack-confirmation` skill, documenting the rationale behind each technology choice

If any artifact is missing, prompt the user to complete the prerequisite skill first. Do NOT re-do technology selection or create new ADRs for decisions already recorded — reference existing ones.

## What This Skill Does NOT Do

To avoid duplication with upstream skills:

- **Does NOT** re-evaluate technology choices (that is `tech-stack-confirmation`)
- **Does NOT** create ADRs for technology selections already decided (they exist)
- **Does NOT** re-derive the architecture overview diagram (it exists in the tech-stack document)
- **Does NOT** gather or refine requirements (that is `requirement-analysis`)

## Workflow

Execute these steps in order. Each step produces concrete output before proceeding to the next.

### Step 1: Read and Analyze Existing Artifacts

Gather all inputs before making any design decisions.

#### Process

1. Read the PRD to extract:
   - Core business domains and functional modules (e.g., order, user, payment)
   - Non-functional requirements that impact architecture (performance, concurrency, security)
   - Integration points with external systems

2. Read the technology stack document to extract:
   - Chosen language, framework, and build tool
   - Database and caching decisions
   - Testing tool selections
   - Architecture overview diagram
   - Key dependencies

3. Read all existing ADRs to understand decision rationale and constraints

4. Identify the business modules by analyzing the PRD's functional requirements:
   - Group related features into cohesive modules
   - Identify module-to-module communication needs
   - Determine which modules share data vs. operate independently

#### Output of Step 1

A summary containing:
- List of identified business modules with their responsibilities
- Module dependency graph (which modules communicate with which)
- Mapping of PRD features to modules
- Framework-specific constraints from ADRs that affect package structure

### Step 2: Design Package Structure and Dependency Rules

Derive the concrete project directory structure from Step 1 analysis and the technology stack.

#### Process

1. **Define module boundaries** — Each business domain identified in Step 1 becomes a module directory. Within each module, apply three-layer separation:
   - `api/` — Controllers, handlers, request/response DTOs (framework-coupled)
   - `core/` — Business logic, domain models, service interfaces (pure, framework-free)
   - `infrastructure/` — Repository implementations, external API clients, message producers (framework-coupled)

2. **Define dependency rules** based on dependency inversion:
   - `core` depends on NOTHING — pure business logic only
   - `api` depends on `core` interfaces
   - `infrastructure` implements `core`-defined interfaces
   - Cross-module communication only through public interfaces (no direct internal access)

3. **Map existing tech stack to directory structure**:
   - Place framework-specific global config in root `infrastructure/` (not per-module)
   - Place shared DTOs, constants, utilities in `common/`
   - Place the application entry point in `startup/`
   - Test directories mirror source structure: `tests/unit/`, `tests/integration/`, `tests/e2e/`

4. **Design logging and observability infrastructure** — Reference `references/logging-architecture-guide.md` for tech-stack-specific recommendations:
   - Select logging framework appropriate for the chosen tech stack
   - Place logging configuration in root `infrastructure/` alongside other cross-cutting config
   - Define structured log format: JSON for production, human-readable for development
   - Establish log level conventions per layer (ERROR/WARN/INFO/DEBUG)
   - Design correlation ID propagation for request tracing
   - Define sensitive data protection rules (no tokens, credentials, or PII in logs)

5. **For projects without clear multi-module boundaries** (small projects, single-purpose services):
   - Use a simplified flat module structure
   - Still enforce the api/core/infrastructure separation within the single module
   - Skip cross-module communication rules

#### Directory Structure Template

Adapt to the specific technology stack. Use language-appropriate conventions (e.g., `src/main/java/` for Java, `src/` for TypeScript, package directories for Go):

```
project-root/
├── {source-root}/                 # e.g., src/main/java/com/example or src/
│   ├── infrastructure/            # Global config (CORS, exception handling, auth filters)
│   ├── common/                    # Shared utilities, DTOs, constants
│   ├── modules/
│   │   ├── {module-a}/
│   │   │   ├── api/               # Controller / Handler layer
│   │   │   ├── core/              # Business logic (pure, no framework dependencies)
│   │   │   └── infrastructure/    # DB access, external API clients
│   │   └── {module-b}/
│   │       └── ... (same structure)
│   └── {entry-point}              # Application main class / entry file
├── {frontend-dir}/                # If applicable
├── docs/
│   ├── architecture.md            # ← THIS SKILL PRODUCES THIS
│   └── adr/                       # ← Already exists from tech-stack-confirmation
├── tests/
│   ├── unit/                      # Mirror source module structure
│   ├── integration/               # Require running services / containers
│   └── e2e/                       # Full stack tests (if applicable)
├── {ci-config}                    # .github/workflows/ or .gitlab-ci.yml
└── {build-config}                 # pom.xml / package.json / go.mod / etc.
```

### Step 3: Produce Architecture Design Document

Generate the architecture design document at `docs/architecture.md`.

#### Process

1. Copy the template from this skill's `assets/architecture-doc-template.md`
2. Fill in each section using data from Steps 1 and 2:

| Section | Content Source |
|---------|---------------|
| System Overview | PRD summary |
| Architecture Style | Existing ADRs + Step 1 analysis |
| Tech Stack Summary | Directly from tech-stack document (reference, do not duplicate) |
| Package Structure | Step 2 directory design |
| Dependency Rules | Step 2 dependency inversion rules |
| Module Communication | Step 1 module dependency graph |
| External Dependencies | Reference tech-stack document's Key Dependencies table |
| Test Architecture | Test pyramid derived from testing stack choices |
| Coverage Targets | Per-layer thresholds |
| Architecture Fitness Functions | Derived from dependency rules |
| CI/CD Pipeline | Quality gates and pipeline stages |
| Logging & Observability | Step 2 logging design + `references/logging-architecture-guide.md` |

3. **Cross-reference existing ADRs** in the architecture document — link to them, do not re-create them. If new architectural decisions arise during design (e.g., a new inter-module communication pattern), create additional ADRs using the template from `assets/adr-template.md`.

**Reference:** Load `references/test-architecture-guide.md` for test pyramid definitions per tech stack and coverage threshold recommendations.

**Reference:** Load `references/logging-architecture-guide.md` for logging framework selection, structured log format specifications, and log level conventions per tech stack.

### Step 4: Scaffold the Walking Skeleton

Create the minimum viable project that validates all technology integrations work together. Zero business logic — only technical validation.

#### Process

1. **Create all directories** from the architecture design document

2. **Initialize build configuration** with all dependencies from the tech-stack document:
   - Framework dependencies (already listed in tech-stack Key Dependencies)
   - Test dependencies (already listed in tech-stack Testing Stack)
   - Code quality tools (already listed in tech-stack DevOps Stack)

3. **Implement a health check endpoint** that:
   - Lives in a `health/` or `system/` module following the designed package structure
   - Returns a success response
   - Optionally verifies external connectivity (database, cache, etc.) based on tech-stack choices

4. **Configure logging infrastructure**:
   - Set up the logging framework with structured output (JSON for production profile, human-readable for development)
   - Implement correlation ID filter/middleware that generates or propagates a request ID
   - Configure log level defaults: INFO for application code, WARN for third-party libraries
   - Verify log output by starting the application and confirming structured log entries appear

5. **Write the first unit test** — Test the health check using mocks, validating the api → core → infrastructure dependency chain works

6. **Write the first integration test** — Test using real infrastructure:
   - If database was chosen: use Testcontainers (or equivalent) for real DB validation
   - If cache was chosen: verify cache integration
   - If external API is the main dependency: use WireMock (or equivalent) for HTTP mock

7. **Configure code quality tools** as specified in the tech-stack DevOps section:
   - Linter / style checker configuration
   - Static analysis configuration
   - Coverage tool with thresholds from the architecture document

#### Validation Checklist

After scaffolding, execute and verify:

- [ ] Build completes without errors (no dependency version conflicts)
- [ ] Unit test passes
- [ ] Integration test passes
- [ ] Linter / style check passes
- [ ] Coverage report generates successfully
- [ ] Health check endpoint responds correctly when application starts

### Step 5: Set Up Architecture Fitness Functions

Implement automated tests that protect the dependency rules defined in Step 2.

#### Required Fitness Functions

1. **Layer dependency enforcement** — Verify at build/test time:
   - `core` layer does not import from `api` or `infrastructure` layers
   - `core` layer does not import framework-specific packages
   - No circular dependencies between modules

   Tool selection per tech stack (reference `references/test-architecture-guide.md`):
   - **Java/Kotlin**: ArchUnit
   - **TypeScript/JavaScript**: dependency-cruiser or eslint-plugin-import
   - **Python**: import-linter
   - **Go**: go-arch-lint

2. **Coverage thresholds** — Configure to fail on threshold violation:
   - core modules: ≥ 80% line coverage
   - api modules: ≥ 60% line coverage
   - infrastructure modules: ≥ 50% line coverage

3. Run `scripts/validate_architecture.py <project-root>` for structural validation (required directories, test mirroring, circular dependency detection)

### Step 6: Configure CI Pipeline

Create the CI pipeline configuration for the platform specified in the tech-stack document.

#### Pipeline Stages

```
1. Checkout
2. Environment Setup (runtime version from tech-stack)
3. Dependency Installation
4. Lint / Style Check
5. Unit Tests + Coverage Report
6. Integration Tests
7. Architecture Fitness Function Tests
8. Build Artifact
9. (Optional) Deploy to Dev — if specified in tech-stack
```

#### Quality Gates (CI must fail if any gate fails)

- All unit tests pass
- All integration tests pass
- Coverage meets per-layer thresholds
- Linter reports zero errors
- Architecture fitness function tests pass

### Step 7: Final Validation and Handoff

Execute all verification commands and confirm green output before declaring completion.

#### Verification Sequence

```bash
# 1. Build (no dependency conflicts)
{build-command}

# 2. Unit tests + coverage
{unit-test-command}

# 3. Integration tests
{integration-test-command}

# 4. Lint / style check
{lint-command}

# 5. Architecture structure validation
python3 {skill-path}/scripts/validate_architecture.py {project-root}

# 6. Architecture fitness function tests
{fitness-test-command}
```

All commands must produce green output. If any fail, fix before proceeding.

#### Deliverable Checklist

- [ ] `docs/architecture.md` — Architecture design document with package structure, dependency rules, test strategy
- [ ] Project directory structure matches the architecture document
- [ ] Walking skeleton: health check endpoint + first unit test + first integration test
- [ ] Architecture fitness function tests enforcing dependency rules
- [ ] Linter, formatter, and coverage tools configured
- [ ] CI pipeline configuration file with all quality gates
- [ ] All verification commands produce green output
- [ ] Existing ADRs cross-referenced (not duplicated); new ADRs created only for new decisions

## Resources

### scripts/

- **`validate_architecture.py`** — Validates project directory structure against architecture rules. Checks required directories, required files, test structure mirroring, and circular dependencies. Usage: `python3 scripts/validate_architecture.py <project-root> [--config <config.json>]`

### references/

- **`architecture-5whys-guide.md`** — Guide for conducting supplementary "5 Whys" analysis when Step 1 reveals architectural questions not already covered by existing ADRs. Contains question templates for deployment, data, communication, testing, and observability dimensions, plus scenario examples.
- **`logging-architecture-guide.md`** — Logging and observability reference. Contains logging framework selection per tech stack (Java, TypeScript, Python, Go), structured log format specifications, log level conventions, correlation ID strategies, sensitive data protection rules, and configuration templates.
- **`test-architecture-guide.md`** — Test architecture reference. Contains test pyramid definitions per tech stack (Java, TypeScript, Python, Go), test data management strategies, architecture fitness function patterns, coverage thresholds, logging test patterns, and test directory structure recommendations.

### assets/

- **`architecture-doc-template.md`** — Template for the architecture design document. Copy to `docs/architecture.md` and fill in per Step 3.
- **`adr-template.md`** — Template for additional Architecture Decision Records. Use only for NEW decisions that arise during design — do not re-create ADRs from `tech-stack-confirmation`.
