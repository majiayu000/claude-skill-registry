---
name: rules-generation
description: "Use after the tech-stack-confirmation skill has been completed and a confirmed tech stack document exists. This skill reads the confirmed tech stack, ADRs, and NFR documents, then generates project-specific coding rules (.claude/rules/*.md files) with YAML frontmatter `paths` scoping, based on the best practices of each selected technology. It produces 4–5 consolidated rule files focused on code quality and best practices. It should be triggered when a user asks to 'generate project rules', 'create coding standards', 'set up code quality rules', 'generate rules from tech stack', or 'create best-practice rules'. It should NOT be used for technology selection (use tech-stack-confirmation instead) or for detailed system design."
---

# Rules Generation

## Overview

Generate project-specific coding rules from a confirmed technology stack. This skill produces `.claude/rules/` files that use YAML frontmatter `paths` for conditional loading, ensuring rules only appear in context when Claude works on matching files. Rules focus on **code quality and best practices**, consolidating related concerns into fewer, deeper files rather than many fragmented ones.

**Target output**: 4–5 consolidated rule files for a typical single-language, single-framework project.

## Prerequisites

- A confirmed tech stack document (output of the `tech-stack-confirmation` skill), typically at `docs/architecture/YYYY-MM-DD-<topic>-tech-stack.md`
- ADR documents at `docs/architecture/adr/`
- An existing `.claude/rules/` directory (global rules may already exist)

## Scope Boundary

This skill covers **coding rules generation** ONLY:
- **In scope**: Reading tech stack artifacts, selecting applicable rule categories, generating consolidated rule files with `paths` scoping, deduplication with existing global rules, user review
- **Out of scope**: Technology selection (use `tech-stack-confirmation`), project scaffolding (use `project-architecture-init`), requirements gathering (use `requirement-analysis`)

If the user attempts to revisit technology selection decisions during this process, redirect: "That's a technology choice — the tech stack is already confirmed. To revise, re-run the `tech-stack-confirmation` skill."

## The Process

### Phase 1: Artifact Discovery — Locate All Inputs

**Goal**: Locate and read all tech stack artifacts produced by `tech-stack-confirmation`.

**Execution rules**:
1. Search for the confirmed tech stack document at `docs/architecture/*-tech-stack.md`
2. Search for ADR documents at `docs/architecture/adr/ADR-*.md` or `docs/architecture/adr/*-ADR-*.md`
3. Search for NFR summary if available in `docs/architecture/` or inline in the tech stack document
4. Scan existing `.claude/rules/` directory (both `~/.claude/rules/` and project-level) to identify global rules already in place
5. Read the project's `CLAUDE.md` file (if exists) for global instructions that affect rule generation

**Phase 1 output**: A summary listing:
- Tech stack document path and detected technologies (language, framework, database, testing, DevOps)
- ADR count and their titles
- Existing global rules already defined

Present this summary to the user for confirmation before proceeding.

### Phase 2: Rule Selection — Determine Consolidated Rules

**Goal**: Based on the confirmed tech stack, determine which **consolidated** rule files to generate.

**Method**: Read `references/rules-catalog.md` for the consolidated rule category catalog and selection algorithm.

**Execution rules**:
1. Apply the selection algorithm from the catalog:
   - **Always generate** (max 1 always-loaded): `git-conventions.md`
   - **Per language** (1 file): Select the consolidated language best-practices file
   - **Per framework** (1 file): Select the consolidated framework best-practices file; include security, caching, logging, API/MCP design as sections within it
   - **Per testing stack** (1 file): Generate `testing-best-practices.md`
   - **Per build/DevOps** (1 file): Generate `build-and-devops.md` if build tools, Docker, or CI/CD are in the stack
2. Cross-check with existing `.claude/rules/` files — if a global rule already covers a topic, mark it as "skip (covered by global rule: `<filename>`)"
3. For each selected rule file, note:
   - File name and `paths` glob patterns
   - Primary technologies and versions it applies to
   - ADR reference(s) tracing back to the decision
   - Sections to include (consolidated from the catalog)

**Phase 2 output**: A rule generation plan table:

| # | Rule File | Paths | Technologies | ADR Refs | Status |
|---|-----------|-------|-------------|----------|--------|
| 1 | `git-conventions.md` | (always loaded) | Git | — | To Generate |
| 2 | `java-best-practices.md` | `**/*.java` | Java 21 | ADR-001 | To Generate |
| 3 | `spring-boot-best-practices.md` | `src/main/**/*.java` | Spring Boot 3.x, ... | ADR-002, ... | To Generate |
| 4 | `testing-best-practices.md` | `src/test/**/*.java` | JUnit 5, ... | ADR-007 | To Generate |
| 5 | `build-and-devops.md` | `pom.xml`, `Dockerfile*`, ... | Maven, Docker, ... | ADR-008, ... | To Generate |

Present this plan to the user for confirmation. The user may:
- Remove rules they consider unnecessary
- Add custom rule categories
- Adjust scope, paths, or priority

Proceed only after user approval.

### Phase 3: Rule Generation — Write Rule Files

**Goal**: Generate each approved rule file with concrete, actionable, version-specific content using the Claude Code `.claude/rules/` format.

**Method**: Read `references/rule-file-template.md` for the standard rule file structure with YAML frontmatter.

**Execution rules**:
1. Generate rules **one file at a time**, presenting each to the user for review before proceeding to the next
2. For each rule file:
   a. Follow the template structure from `references/rule-file-template.md`
   b. **Include YAML frontmatter with `paths`** for path-scoped rules, or omit for always-loaded rules
   c. Include the ADR reference header linking the rule to the technology decision
   d. Write **Mandatory Rules** (M-NNN) — non-negotiable best practices for the specific technology and version
   e. Write **Recommended Rules** (R-NNN) — strong suggestions with documented rationale
   f. Include **DO/DON'T code examples** in the project's primary language for every mandatory rule
   g. Add a **Checklist** section for pre-commit verification
3. Write each approved rule file to the project's `.claude/rules/` directory
4. Respect existing global rules:
   - Never overwrite files in `~/.claude/rules/` (user's global rules)
   - Project-level rules go to `<project-root>/.claude/rules/`
   - If a project-level rule overlaps with a global rule, add a reference: `> Extends global rule: ~/.claude/rules/<filename>`
5. Content constraints:
   - All code examples, log messages, and exception messages must use English (per project global rule)
   - No hardcoded magic values — use named constants with environment variable support (per project global rule)
   - Every rule must be concrete and actionable, not vague platitudes
   - Prefer quantifiable thresholds over subjective guidance

**Interaction model**:
- Present ONE rule file at a time
- Allow the user to approve, modify, or reject each rule file
- If rejected, revise based on feedback and re-present

**Phase 3 output**: Complete set of rule files written to `.claude/rules/`.

### Phase 4: Integration & Summary — Ensure Consistency

**Goal**: Verify all generated rules are consistent with each other and with existing global rules, then present a final summary.

**Execution rules**:
1. Cross-check all generated rule files for contradictions (e.g., one rule mandates a pattern another forbids)
2. Verify all ADR references are valid
3. Verify all `paths` patterns are correct and non-overlapping where it matters
4. Check that existing global rules (from `~/.claude/rules/` and project `CLAUDE.md`) are not contradicted by new rules
5. If conflicts are found, present them to the user for resolution

**Phase 4 output**: A final summary report:

1. **Rules generated** — count and file paths with their `paths` scoping
2. **Rules skipped** — count and reasons (covered by global rules)
3. **Technologies covered** — list of all technologies with corresponding rule files
4. **ADR coverage** — verify every ADR has at least one corresponding rule file
5. **Global rule compatibility** — confirm no conflicts with existing global rules
6. **Recommended next steps** — suggest running `project-architecture-init` if not yet done

## Key Principles

- **Consolidated files** — merge related concerns into one file per domain (4–5 files total, not 15+)
- **Paths-scoped** — every rule file uses YAML frontmatter `paths` unless truly cross-cutting; this prevents all rules from loading into context simultaneously
- **Code quality focus** — prioritize coding standards, error handling, and best practices over operational/infra rules
- **One rule file at a time** — never present all rules simultaneously; allow user review per file
- **Version-specific** — rules must reference the exact technology version from the tech stack, not generic advice
- **ADR-traceable** — every rule file must link back to the ADR that confirmed the technology
- **No duplication** — check existing global rules before generating; reference rather than repeat
- **Concrete over vague** — "method body must not exceed 30 lines" beats "keep methods short"
- **DO/DON'T examples** — mandatory rules require both correct and incorrect code examples
- **English code artifacts** — all code, logs, and exceptions in generated rules use English
- **Incremental validation** — present each phase output to the user before proceeding

## Resources

### references/
- `rules-catalog.md` — Consolidated rule category catalog organized by technology domain, with the selection algorithm for determining which rules to generate and `paths` patterns for each category
- `rule-file-template.md` — Standard template structure for generated rule files using Claude Code YAML frontmatter format, including `paths` glob pattern reference and content guidelines
