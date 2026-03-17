---
name: DOCUMENT_PROJECT_STATE
description: Generate documentation for an existing project. USE WHEN onboarded to a new codebase OR documenting legacy code. Capabilities include architectural mapping, tech stack inventory, and technical debt documentation.
---

# DOCUMENT PROJECT

**Owner:** Devon (Developer)

## Goal
To produce accurate, reality-based documentation for an existing codebase. This is about documenting *what is*, not *what should be*.

## Core Principles
- **Reality Over Theory:** Document the actual patterns, even the ugly ones.
- **Lean:** Focus on what an AI agent or new developer needs to know to work.
- **Automated Discovery:** Use tools to read the code, don't just ask the user.

## Workflow Instructions

### 1. Scope & Elicitation
- **Action:** Determine what to document.
- **Prompt:** "Are we documenting the whole system or just a specific module?"
- **Check:** Is there a PRD? If so, focus on relevant areas.

### 2. Discovery
- **Action:** Map the codebase.
- **Targets:** `package.json`, `README.md`, `src/` structure, build scripts.
- **Tool:** Use `context7` to identify frameworks and versions.

### 3. Deep Analysis
- **Action:** Read key files.
- **Focus:** Entry points, config, auth, data models, API routes.
- **Identify:**
  - **Patterns:** How is code organized?
  - **Debt:** What looks hacky or legacy?
  - **Integration:** External APIs?

### 4. Drafting the Architecture Doc
- **Action:** Assemble the insights.
- **Template:** `.claude/templates/architecture-tmpl.yaml` (conceptual reference).
- **Sections:**
  - **Overview:** System purpose.
  - **Tech Stack:** Exact versions (verified).
  - **Key Patterns:** How to write code here.
  - **Critical Files:** The map.
  - **Technical Debt:** Warnings for the agent.

### 5. Review & Save
- **Action:** Validate against reality.
- **Check:** Do the file paths exist? Are the versions correct?
- **Write:** `docs/architecture/{{project_name}}-architecture.md`.

## Anti-Patterns
- **NEVER** document theoretical best practices that aren't followed in the code.
- **NEVER** omit version numbers for core dependencies.
- **NEVER** generate generic "boilerplate" documentation.

## Output Format
A comprehensive Markdown architecture document.
