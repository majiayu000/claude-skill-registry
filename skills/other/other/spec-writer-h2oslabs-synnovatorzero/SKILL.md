---
name: spec-writer
description: Guide structured specification writing for AI coding agents using a 4-stage gated workflow (Specify, Plan, Tasks, Implement) and a 6-domain framework (Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries). Produces a SPEC.md file that serves as a living reference for the project. Use when user mentions writing a spec, creating a SPEC.md, setting up project guidelines, onboarding an AI agent to a codebase, or asks for structured project specification. Trigger phrases include "write a spec", "create a SPEC.md", "set up project guidelines", "spec out this project", "define project standards".
---

# Spec Writer

## Overview

Guide users through writing a structured SPEC.md for AI coding agents using a 4-stage gated workflow. The spec covers six core domains drawn from analysis of effective agent configurations: Commands, Testing, Project Structure, Code Style, Git Workflow, and Boundaries.

**Core rule:** Mirror the user's language. If they write in Chinese, respond in Chinese. If in English, respond in English. Never hardcode a language.

**Key principle:** Concrete over abstract. A real code snippet beats a paragraph of description. A runnable command beats a tool name. A specific file path beats "see the docs."

## When to Offer

Offer this workflow when:
- User says "write a spec", "create a SPEC.md", "spec out this project"
- User wants to set up project guidelines or standards for an AI agent
- User asks how to onboard an AI coding agent to their codebase
- User mentions spec-driven development or structured project documentation
- User wants to define boundaries/rules for an AI coding agent

**Initial offer:** Explain the 4-stage workflow and ask if they want to proceed or work freeform. If they decline, work freeform. If they accept, proceed to Stage 1.

## Stage 1: Specify (Vision Gathering)

**Goal:** Understand what is being built, for whom, and why. No technical details yet.

### Branching: Greenfield vs Existing

Determine which path applies:

**Greenfield project (building from scratch):**
1. Ask: What are you building? Who is it for? What problem does it solve?
2. Ask: What does success look like? How will you know the project works?
3. Ask: Any constraints or non-negotiables? (timeline, technology mandates, etc.)
4. Draft a 2-3 sentence Vision statement and Success Criteria checklist
5. Present for approval

**Existing project (adding a spec to existing code):**
1. Ask: What is this project? Point me to the codebase.
2. Explore the codebase: read `package.json`/`pyproject.toml`/`Cargo.toml`, scan directory structure, read README if present
3. Draft a Vision statement based on what exists
4. Ask: Is this accurate? What's missing or wrong?
5. Present for approval

### Stage 1 Gate

Present the Vision and Success Criteria. User must approve before advancing.

If user wants changes, iterate. Only proceed to Stage 2 when user explicitly approves.

**Output so far:** Vision section + Success Criteria checklist.

## Stage 2: Plan (Six Domain Framework)

**Goal:** Systematically collect information for all six domains.

Read [references/six-domains-checklist.md](references/six-domains-checklist.md) for the detailed checklist of what to collect, output formats, mistakes to avoid, and questions to ask for each domain.

### Workflow

1. **For each domain** (Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries), follow this loop:
   - Ask the domain-specific questions from the checklist
   - For existing projects: also probe the codebase (read configs, scan files, check for linters/formatters)
   - Draft the domain section in the checklist's output format
   - Present for user review

2. **Boundaries get special treatment:**
   - Read [references/boundary-patterns.md](references/boundary-patterns.md) for project-type-specific examples
   - Always produce all three tiers: Always, Ask First, Never
   - The "Never commit secrets" rule is mandatory in every spec
   - Adapt patterns to the specific project rather than copying generic lists

3. **Tech Stack:** Also collect the full tech stack during this stage (language, framework, database, testing framework, package manager, versions).

### Stage 2 Gate

Present a summary of all six domains plus the tech stack. User must approve before advancing.

If any domain is incomplete or wrong, iterate on that domain. Only proceed to Stage 3 when all six domains are approved.

**Output so far:** Vision + Success Criteria + Tech Stack + all six domains in draft form.

## Stage 3: Tasks (Decomposition and Scaffolding)

**Goal:** Assemble the approved content into a SPEC.md file using the template scaffold.

Read [references/spec-template.md](references/spec-template.md) for the output template.

### Workflow

1. Create a new file `SPEC.md` (or the user's preferred filename/location) using the template scaffold
2. Fill in each template section with the content approved in Stages 1-2
3. For any optional sections (Architecture Notes, Version History), ask if the user wants them included
4. Set Version History to `1.0 | [today's date] | Initial specification`

### Stage 3 Gate

Present the complete SPEC.md draft. User must approve the assembled document.

Key review points to highlight:
- Does the assembled document flow well as a whole?
- Are there contradictions between sections?
- Is anything missing that became obvious when seeing everything together?

Iterate until user approves.

## Stage 4: Implement (Validation and Finalization)

**Goal:** Validate completeness, finalize the spec, and establish it as the project's living reference.

### Workflow

1. **Self-check:** Re-read the complete SPEC.md and verify:
   - All six domains have substantive content (not placeholders)
   - Boundaries has all three tiers
   - Commands section has actual runnable commands with flags
   - Code Style section has at least one real code snippet
   - Success Criteria are measurable

2. **Script validation:** Run the validation script:
   ```bash
   uv run python [skill-path]/scripts/validate_spec.py [spec-path]
   ```
   Replace `[skill-path]` with the path to this skill's directory and `[spec-path]` with the SPEC.md file path.

3. **Fix any failures:** If validation finds gaps, go back to the relevant section and fix it. Re-run until all checks pass.

4. **Final presentation:** Show the user the validation results and the complete SPEC.md. Ask for final approval.

### Stage 4 Gate

User gives final approval. The spec is done.

## Post-Completion

After the spec is approved:

1. **Living document guidance:** Remind the user that SPEC.md is a living document:
   - Update it when requirements change
   - Update it when technical decisions are made
   - Track changes in Version History
   - Commit it to version control alongside code

2. **Integration suggestions:**
   - Place SPEC.md at the project root or in a `specs/` directory
   - Reference it from CLAUDE.md or agents.md if applicable
   - Consider adding the validation script to CI

3. **Next steps:** Ask if the user wants to:
   - Start implementing based on the spec
   - Create task breakdowns from the spec
   - Review an existing spec against this framework

## Handling Deviations

**User wants to skip stages:** Allow it, but warn that skipping Stage 2 (Plan) risks an incomplete spec. If they skip, note which domains weren't covered.

**User wants a partial spec:** Support single-domain mode — e.g., "just help me define boundaries." Follow the Stage 2 workflow for that domain only, then validate just that section.

**User has an existing SPEC.md to audit:** Run `validate_spec.py` on it first, then walk through any FAIL items using the six-domains checklist.

**User is updating, not creating:** Read the existing SPEC.md, identify what changed, update the relevant sections, bump the version in Version History.

## Quality Principles

1. **Concrete over abstract:** A runnable command beats a tool name. A code snippet beats a style description. A file path beats "see the docs."

2. **Boundaries are non-negotiable:** Every spec must have all three tiers. "Never commit secrets" is always included. Generic boundaries ("don't break things") are rejected — push for specifics.

3. **Six domains are mandatory:** No spec is complete without all six. If the user insists on skipping one, note the gap explicitly in the spec.

4. **The spec is for an AI agent, not a human:** Write for parsability. Use headers, lists, and code blocks. Avoid prose paragraphs where structured formats work better.

5. **Medium freedom template:** The six domains are fixed scaffolding. Content within each domain is flexible and adapts to the project. Don't force patterns that don't fit.

6. **Validate deterministically:** Always run the validation script. Human judgment catches semantic issues; the script catches structural ones. Both matter.
