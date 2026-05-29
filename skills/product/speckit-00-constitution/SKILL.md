---
name: speckit-00-constitution
description: Create or update project governance principles and constitution
---

# Spec-Kit Constitution

Create or update the project constitution at `.specify/memory/constitution.md`. This file defines the governing principles, constraints, and governance rules for specification-driven development.

## Scope - What Constitution Contains

**MUST contain:**
- Project governance principles (high-level, technology-agnostic)
- Non-negotiable development rules
- Quality standards and expectations
- Amendment procedures and versioning policy
- Compliance review expectations

**MUST NOT contain:**
- Technology stack (languages, frameworks, databases) - belongs in `/speckit-03-plan`
- Implementation details - belongs in `/speckit-03-plan`
- Specific tools or versions - belongs in `/speckit-03-plan`
- API designs or data models - belongs in `/speckit-03-plan`

The constitution defines the "laws" of the project. The plan defines how to implement features within those laws.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Prerequisites Check

1. Check if constitution template exists:
   ```bash
   cat .specify/memory/constitution.md 2>/dev/null || echo "NO_CONSTITUTION"
   ```

2. If file doesn't exist, copy from skill references:
   - Read the constitution template from this skill's `references/constitution-template.md`
   - Create `.specify/memory/constitution.md` with the template

## Execution Flow

1. **Load the existing constitution template** at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   - **IMPORTANT**: The user might require fewer or more principles than the template. Adapt accordingly.

2. **Collect/derive values for placeholders**:
   - If user input supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions).
   - For governance dates:
     - `RATIFICATION_DATE` is the original adoption date (if unknown, ask or mark TODO)
     - `LAST_AMENDED_DATE` is today if changes are made
   - `CONSTITUTION_VERSION` must increment according to semantic versioning:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions
     - MINOR: New principle/section added or materially expanded guidance
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements

3. **Draft the updated constitution content**:
   - Replace every placeholder with concrete text (no bracketed tokens left)
   - Preserve heading hierarchy
   - Ensure each Principle section has: succinct name, paragraph or bullet list capturing non-negotiable rules, explicit rationale
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations

4. **Consistency propagation** (validate against templates if they exist):
   - Check `.specify/templates/plan-template.md` for constitution alignment
   - Check `.specify/templates/spec-template.md` for scope/requirements alignment
   - Check `.specify/templates/tasks-template.md` for task categorization alignment

5. **Produce a Sync Impact Report** (prepend as HTML comment at top of constitution file):
   - Version change: old -> new
   - List of modified principles
   - Added/removed sections
   - Templates requiring updates
   - Follow-up TODOs if any placeholders deferred

6. **Validation before final output**:
   - No remaining unexplained bracket tokens
   - Version line matches report
   - Dates in ISO format YYYY-MM-DD
   - Principles are declarative, testable, and free of vague language

7. **Phase Separation Validation (REQUIRED)**:

   Before writing, scan the draft constitution for technology-specific content that belongs in `/speckit-03-plan`:

   **Check for violations - constitution MUST NOT mention:**
   - Programming languages (Python, JavaScript, TypeScript, Go, Rust, Java, C#, etc.)
   - Frameworks (React, Django, Express, Spring, Rails, FastAPI, etc.)
   - Databases (PostgreSQL, MySQL, MongoDB, SQLite, Redis, etc.)
   - Infrastructure (Docker, Kubernetes, AWS, GCP, Azure, etc.)
   - Specific libraries or packages
   - Version numbers of tools
   - File extensions tied to languages (.py, .js, .ts, etc.)
   - API specifications (REST, GraphQL, gRPC)

   **If violations found:**
   ```
   ╭─────────────────────────────────────────────────────────────────╮
   │  PHASE SEPARATION VIOLATION DETECTED                           │
   ├─────────────────────────────────────────────────────────────────┤
   │  Constitution contains technology-specific content:            │
   │  - [list each violation]                                       │
   │                                                                 │
   │  Technology decisions belong in /speckit-03-plan, not here.    │
   │  Constitution must be technology-agnostic to survive tech      │
   │  stack changes.                                                 │
   ├─────────────────────────────────────────────────────────────────┤
   │  ACTION: Removing technology references and generalizing...    │
   ╰─────────────────────────────────────────────────────────────────╯
   ```

   **Auto-fix:** Rewrite the violating sections to be technology-agnostic:
   - "Use Python" → "Use appropriate language for the domain"
   - "Store in PostgreSQL" → "Use persistent storage"
   - "Deploy with Docker" → "Use containerization when appropriate"

   Re-validate after fixes until no violations remain.

8. **Write the completed constitution** back to `.specify/memory/constitution.md`

9. **Output final summary** to the user with:
   - New version and bump rationale
   - Any files flagged for manual follow-up
   - Suggested commit message

## Formatting Requirements

- Use Markdown headings exactly as in the template
- Wrap long rationale lines for readability (<100 chars)
- Keep a single blank line between sections
- Avoid trailing whitespace

## Next Steps

After creating the constitution, you can:
- Run `/speckit-01-specify` to create a feature specification

The constitution will be loaded and validated by all other speckit skills.
