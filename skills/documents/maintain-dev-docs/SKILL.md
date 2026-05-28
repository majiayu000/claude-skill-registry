---
name: maintain-dev-docs
description: Maintain project /docs/: specs, tasks, features, readme. Use for: project setup, feature additions, instruction improvements, or syncing documentation with code.
---
# Development Documentation Maintainer

## Overview
This skill helps maintain comprehensive, evolving development documentation for software projects. It establishes a consistent pattern for capturing ideas, specifications, tasks, and implementation details in a `/docs/` folder that grows with your project. Ensures consistent WIP documentation evolution across brainstorm, specification, tasks, and feature implementation. Assists humans and AI agents track progress being made, tasks prioritization, objectives, instructions, and decisions during an iterative development process.

Use this skill when:
- Starting a new project with initial ideas
- Adding features to an existing project
- Updating technical specifications
- Documentation needs to be created or synchronized with code
- Instructions for project setup, configuration, or implemented features need modified in the README.md
- Adding/updating project tasks in TASKS.md based upon current progress, new feature ideas/improvements, or changes in feature development priorities.

The skill ensures AI coding assistants (Claude Code, GitHub Copilot, Antigravity, ect.) have consistent, up-to-date context about what you're building, architectural decisions made, and what remains to be done.

### Documentation Structure

This skill manages five core documentation files in `/docs/`:

```
docs/
├── BRAINSTORM.md          # Initial ideas, evolving as project grows
├── SPECIFICATION.md       # Architecture, tech stack, API design, general requirements
├── TASKS.md              # Hierarchical task list organized by phases
├── PHASE0.md             # Detailed/prioritized implementation specs for Phase 0
├── PHASE1.md             # Detailed/prioritized implementation specs for Phase 1 (created as needed)
├── README.md             # User-facing documentation and getting started
└── features/             # Optional: individual feature documentation
    └── feature-name.md
```

---

## Quick Start Workflows

### New Project Initialization

Use this workflow when starting a project from scratch:

1. **Create documentation structure**: Initialize `/docs/` folder with core files
2. **Start with brainstorm**: Capture initial ideas in `BRAINSTORM.md`
   - Project purpose and objectives
   - Target users
   - Success criteria
   - Open questions
3. **Create specification**: Transform brainstorm into `SPECIFICATION.md`
   - **CRITICAL**: Ask about and document database provider, LLM providers, logging, observability
   - Define architecture and tech stack
   - Outline API and data models
   - List general functional/non-functional requirements
4. **Build task list**: Create `TASKS.md` with hierarchical structure
   - Organize by phases (Phase 0, Phase 1, etc.)
   - Nest tasks under each phase
   - Use checkboxes for tracking
5. **Detail Phase 0**: Create `PHASE0.md` with implementation specs
   - Detailed feature requirements
   - Database schemas and migrations
   - API endpoints with examples
   - LLM integration details (if applicable)
   - Logging and observability setup
   - Testing/verification requirements
6. **Create README**: Write `README.md` for users
   - Project description
   - Implemented feature descriptions & instructions for use
   - Getting started instructions
   - Prerequisites and installation
   - Basic usage examples

### Existing Project Adaptation

Use this workflow when a project already has some documentation:

1. **Assess current documentation**: Check which files exist in `/docs/`
2. **Identify gaps**: Determine which core files are missing
3. **Create missing files**: Use templates to generate missing documentation
4. **Adapt to existing structure**: If documentation exists in different format:
   - Extract relevant content
   - Map to standard structure
   - Preserve existing information
5. **Fill in critical information**: Ensure architecture decisions are documented
   - Database provider
   - LLM providers (if applicable)
   - Logging solution
   - Observability setup
6. **Integrate workflow**: Begin using the documentation system for future changes

### Feature Addition

Use this workflow when adding new features to a project:

1. **Update specification** (if needed): Add to `SPECIFICATION.md` if introducing:
   - New external services or APIs
   - New technology or framework
   - Changes to architecture
2. **Add tasks**: Update `TASKS.md`
   - Add new tasks under appropriate phase
   - Mark tasks as completed when done
3. **Update phase file**: Add detailed specs to relevant `PHASE#.md`
   - Feature requirements
   - Database changes
   - API endpoints
   - Frontend components
   - LLM integration details
   - Logging and testing requirements
4. **Create feature doc** (if complex): For substantial features, create `features/feature-name.md`
5. **Update README**: If feature is user-facing, update `README.md`
   - Add to features list
   - Update usage examples
   - Update installation if needed

### Phase Transition

Use this workflow when moving from one development phase to another:

1. **Review current phase**: Ensure all tasks in current phase are complete
2. **Mark tasks complete**: Update `TASKS.md`
   - Check off completed tasks
   - Move to "Completed Tasks" section if desired
3. **Update specification**: Update phase overview in `SPECIFICATION.md`
4. **Create next phase file**: Generate `PHASE[N+1].md` with:
   - Phase overview and goals
   - Success criteria
   - Detailed implementation specifications
   - Dependencies and risks
5. **Plan next phase tasks**: Add new phase tasks to `TASKS.md`

---

## Documentation Files Overview

### BRAINSTORM.md
**Purpose**: Capture initial ideas and evolving requirements

**When to update**:
- Starting a new project
- Brainstorming new features
- Pivoting project direction
- Recording open questions

**Content includes**:
- Initial ideas and inspiration
- Project purpose and objectives
- Target users and use cases
- Success criteria
- Constraints and considerations
- Open questions

This is your "thinking space" where ideas can be messy and evolving. As ideas solidify, they move into SPECIFICATION.md.

### SPECIFICATION.md
**Purpose**: Document architecture, tech stack, and general requirements

**When to update**:
- After solidifying ideas from brainstorm
- Adding new technology or framework
- Making architectural decisions
- Integrating new external services
- Changing infrastructure

**Content includes**:
- **Architecture & Tech Stack** (REQUIRED):
  - Database provider
  - LLM providers and models (if applicable)
  - Backend/frontend frameworks
  - Deployment platform
  - Logging and observability solutions
- **API & Data Models**:
  - Key endpoints
  - Core data structures
  - External integrations
- **General Requirements**:
  - High-level functional requirements
  - Non-functional requirements (performance, security, scalability)
- **Phase Overview**:
  - Brief description of each implementation phase

Keep this document general. Detailed implementation specs belong in PHASE#.md files.

For full template, see [references/templates.md](references/templates.md).

### TASKS.md
**Purpose**: Track all project tasks in hierarchical structure

**When to update**:
- Creating new phase
- Adding new features or tasks
- Completing tasks (check them off immediately)
- Reprioritizing work
- Discovering forgotten tasks

**Content includes**:
- Hierarchical task structure organized by phases
- Checkboxes for tracking completion
- Nested subtasks under main tasks
- Completed tasks section (optional)

**Structure**:
```markdown
### Phase 0: Foundation
- [ ] Setup & Infrastructure
  - [ ] Initialize project structure
  - [ ] Configure database
  - [ ] Setup logging & observability
- [ ] Core Models
  - [ ] Define data schemas
  - [ ] Create migrations
```

Update this file frequently. Check off tasks as you complete them to maintain accurate progress tracking.

### PHASE#.md
**Purpose**: Detailed implementation specifications for each development phase

**When to update**:
- Creating a new phase
- Adding features to a phase
- Documenting implementation details
- Updating as implementation progresses

**Content includes**:
- Phase overview and goals
- Success criteria
- Detailed feature specifications:
  - Requirements (functional and non-functional)
  - Database changes (schemas, migrations)
  - API endpoints (with request/response examples)
  - Frontend components
  - LLM integration (prompts, models, error handling)
  - Logging and observability (what to log, metrics to track)
  - Testing requirements
  - Security considerations
- Dependencies and risks
- Timeline estimates (optional)

Phase files contain the DETAILED specs. specification.md stays general, PHASE#.md files go deep.

For full template, see [references/templates.md](references/templates.md).

### README.md
**Purpose**: User-facing documentation and getting started guide

**When to update**:
- Initial project setup
- Adding user-facing features
- Changing installation process
- Updating usage instructions
- Modifying prerequisites

**Content includes**:
- Project description
- Feature list
- Prerequisites
- Installation instructions
- Configuration steps
- Usage examples
- Links to detailed documentation

This is what users see first. Keep it clear, concise, and up-to-date with current functionality.

### features/feature-name.md (Optional)
**Purpose**: Detailed documentation for complex individual features

**When to create**:
- Feature is substantial and complex
- Feature requires extensive documentation
- Feature involves multiple components
- Implementation discussions need dedicated space

**Content includes**:
- Feature overview
- Requirements and specifications
- Implementation details
- Usage examples
- Edge cases and considerations

---

## Critical Reminders

### ALWAYS ASK AND DOCUMENT

When creating or updating `SPECIFICATION.md`, these four items are REQUIRED:

- [ ] **Database provider** and rationale (PostgreSQL, MySQL, MongoDB, SQLite, etc.)
- [ ] **LLM providers** and models (OpenAI, Anthropic, local, etc.) - if applicable to the project
- [ ] **Logging solution** (Winston, Serilog, built-in, etc.)
- [ ] **Observability/monitoring** setup (Prometheus, CloudWatch, Sentry, etc.)

If any of these are unclear, ASK the user before proceeding. These architectural decisions are critical and must be documented from the start.

### Built-in Reminder Checklist

Before committing code changes, verify:

**Architecture Decisions**:
- [ ] Database provider documented in SPECIFICATION.md
- [ ] LLM providers specified (if project uses LLMs)
- [ ] Logging solution configured
- [ ] Observability/monitoring setup

**Documentation Sync**:
- [ ] SPECIFICATION.md reflects current architecture
- [ ] tasks.md checkboxes up to date
- [ ] Phase files match current implementation
- [ ] README.md user-facing information current

**Feature Additions**:
- [ ] New integrations added to SPECIFICATION.md
- [ ] Tasks added to tasks.md
- [ ] Relevant PHASE#.md file updated
- [ ] Feature-specific docs created if needed

### Using the Reminder Script

For a comprehensive checklist, run the reminder script:

```bash
ts-node /path/to/project/docs/check-reminders.ts
```

Or if integrated into your project:

```bash
npm run check-docs
```

The script outputs a formatted checklist covering all critical documentation maintenance items.

---

## Update Workflows

### When to Update specification.md

Update specification.md when:
- **Adding new technology**: New framework, library, or service
- **Making architectural changes**: Database migration, deployment changes
- **Integrating external services**: Third-party APIs, payment processors
- **Changing infrastructure**: Logging, monitoring, hosting platform
- **Updating general requirements**: New non-functional requirements

Do NOT add detailed implementation specs here. Those belong in PHASE#.md files.

### When to Update tasks.md

Update tasks.md when:
- **Starting new phase**: Add all tasks for the phase
- **Completing tasks**: Check off tasks immediately upon completion
- **Adding features**: Add new tasks under appropriate phase
- **Discovering forgotten tasks**: Add them as soon as identified
- **Reprioritizing**: Reorganize task order or move between phases

Keep this file current. It's your source of truth for progress tracking.

### When to Update PHASE#.md Files

Update phase files when:
- **Planning implementation**: Before starting to code a feature
- **Documenting decisions**: As you make implementation choices
- **Adding detail**: When specs need clarification
- **Recording changes**: When implementation differs from original plan
- **Updating requirements**: When feature requirements evolve

Update phase files BEFORE and DURING implementation, not just after.

### When to Update README.md

Update README.md when:
- **Adding user-facing features**: New functionality users will interact with
- **Changing setup process**: Installation, configuration, or prerequisites
- **Updating usage**: New commands, APIs, or workflows
- **Fixing setup issues**: Installation problems or common errors
- **Adding dependencies**: New required software or services

Keep README.md synchronized with what users actually experience.

### Keeping Feedback Loops Short

**Best practice**: Update documentation incrementally, not in large batches.

**Before starting work**:
1. Update specification.md if introducing new tech
2. Add tasks to tasks.md
3. Document detailed specs in PHASE#.md

**During implementation**:
1. Update phase files as you make decisions
2. Create feature docs for complex features
3. Note any deviations from original plan

**After completing work**:
1. Check off tasks in tasks.md
2. Update README.md if user-facing
3. Verify docs sync with code

**Before committing**:
1. Run through reminder checklist
2. Verify all relevant docs updated
3. Commit docs with code changes

This workflow ensures documentation never falls far behind code.

---

## Best Practices

### Update Before Committing

**Always update documentation before committing code**. This ensures:
- Documentation and code stay synchronized
- Future you/teammates understand current state
- AI assistants have accurate context
- Changes are documented when fresh in mind

Include documentation updates in the same commit as code changes when possible.

### Keep Specification General, Phase Files Detailed

**specification.md**: High-level architecture and general requirements
- "The API will use REST endpoints"
- "Authentication will use JWT tokens"
- "Database will be PostgreSQL"

**PHASE#.md**: Detailed implementation specifications
- "POST /api/auth/login endpoint accepts {email, password} and returns {token, user}"
- "JWT tokens expire after 24 hours with refresh token pattern"
- "User table schema: id (UUID), email (unique), password_hash, created_at"

This separation prevents specification.md from becoming overwhelming while ensuring details are captured.

### Use Hierarchical Task Structure

Organize tasks with clear hierarchy:

```markdown
### Phase 0: Foundation
- [ ] Observability & Development Verification System
  - [ ] Log schema
  - [ ] Local log output and logging service
- [ ] Define Schemas
  - [ ] Initial base types & interfaces
  - [ ] DTOs
  - [ ] Standard API requests & responses
  - [ ] Database model relationships
```

This makes it clear:
- What definitions and major features are planned
- What has yet to be built and in prioritized order to build foundational & prerequisite features first
- A general history and what's been completed (checkboxes for simple toggles)

### Create Feature-Specific Docs for Complex Features

If a feature requires extensive discussion, create `features/feature-name.md`:
- Keeps phase files manageable & prioritized
- Provides dedicated space for feature details
- Easier to reference and share
- Better organization for complex projects

Examples of when to create feature docs:
- GraphRAG for semantic search
- Dashboard displaying a script execution summary
- New web component or page
- New API route with multiple endpoints
- Payment processing integration
- Real-time messaging system
- Authentication flows
- Multi-step workflows

### Keep Docs in Sync with Code

Documentation that's out of sync is worse than no documentation. It misleads and confuses.

**Strategies**:
- Update docs in same commit as code
- Use reminder checklist before committing
- Review docs during code review
- Set up git hooks for reminders (optional)
- Make doc updates part of "done" definition

### Document Decisions, Not Just Facts

When documenting, include WHY decisions were made:

**Just facts**:
> Database: PostgreSQL

**Facts + rationale**:
> Database: PostgreSQL
> Rationale: Need strong ACID guarantees for financial transactions, team has PostgreSQL experience, excellent JSON support for flexible schemas

The "why" helps future maintainers understand trade-offs and avoid questioning decisions later.

### Start Simple, Grow as Needed

Don't create `features/` folder until you have a feature that needs it. Don't create `PHASE3.md` until you're ready for Phase 3.

Start with core files:
1. brainstorm.md
2. specification.md
3. tasks.md
4. PHASE0.md
5. README.md

Add more structure as project complexity demands it.

---

## References

For detailed information, see these reference documents:

- **[references/templates.md](references/templates.md)**: Complete templates for all documentation files
  - brainstorm.md template
  - specification.md template (with required sections)
  - tasks.md template (hierarchical structure)
  - PHASE#.md template (detailed implementation specs)
  - README.md template
  - Feature documentation template

- **[references/workflow-guide.md](references/workflow-guide.md)**: Detailed workflow patterns
  - New project workflow (step-by-step)
  - Existing project workflow (adaptation)
  - Feature addition workflow
  - Phase transition workflow
  - Documentation update workflow

- **[references/phase-management.md](references/phase-management.md)**: Phase file management
  - How to structure phase files
  - When to create new phases
  - Managing phase transitions
  - Phase dependencies
  - Examples of well-structured phases

- **[references/git-hooks-setup.md](references/git-hooks-setup.md)**: Optional automation
  - Pre-commit hook for doc reminders
  - Pre-push hook for checklist
  - Setup instructions for bash/zsh
  - Example hook scripts
  - Bypassing hooks when needed

---

## Troubleshooting

### Documentation Out of Sync

**Problem**: Code has been updated but documentation hasn't been updated.

**Solution**:
1. Review recent commits to identify changes
2. Update specification.md with any new architecture/tech
3. Update relevant PHASE#.md with implementation details
4. Check off completed tasks in tasks.md
5. Update README.md if user-facing changes
6. Consider setting up git hooks to prevent future drift

### Conflicting Requirements

**Problem**: Requirements in specification.md conflict with implementation in PHASE#.md.

**Solution**:
1. Determine which is correct (spec or implementation)
2. Update the incorrect document to match reality
3. Document why the change was made
4. Ensure both documents now align
5. Communicate change to team if applicable

### Missing Architecture Decisions

**Problem**: specification.md is missing critical information (database, LLM, logging, observability).

**Solution**:
1. Identify what's missing from the four critical items
2. Ask user or check codebase for current choices
3. Update specification.md with all four items
4. Document rationale for each choice
5. Ensure future updates maintain this information

### Unclear Which Phase

**Problem**: Unsure which PHASE#.md file to update for a new feature.

**Solution**:
1. Check tasks.md to see which phase the task belongs to
2. If not listed, determine based on dependencies:
   - Phase 0: Foundation (database, auth, core models)
   - Phase 1: Core features (primary user functionality)
   - Phase 2+: Advanced features (enhancements, optimization)
3. Add task to appropriate phase in tasks.md
4. Update corresponding PHASE#.md file

### Lost Context

**Problem**: Coming back to project after time away, can't remember current state.

**Solution**:
1. Read README.md for project overview
2. Check specification.md for architecture decisions
3. Review tasks.md to see what's completed vs remaining
4. Read current PHASE#.md to understand what you were building
5. Check brainstorm.md for original vision and open questions

This is why keeping documentation current is critical.

### Documentation Too Large

**Problem**: A documentation file (especially PHASE#.md) is becoming unwieldy.

**Solution**:
1. For phase files: Consider if features should be split across phases
2. For complex features: Move to individual `features/feature-name.md` files
3. For specification.md: Ensure detailed specs are in phase files, not here
4. Use hierarchical structure and clear sections
5. Link between documents rather than duplicating content

Remember: specification.md should stay general, PHASE#.md files contain details, complex features get their own files.

---

## Tips for AI Assistants

When using this skill, AI assistants should:

1. **Proactively ask about architecture decisions** when starting new projects:
   - "Which database provider would you like to use such as Sqlite, Supabase, or Convex?"
   - "Will this project use LLMs? If so, which provider such as Ollama or OpenRouter?"
   - "What logging solution should we set up? For your current stack, I suggest..."
   - "How should we handle observability and monitoring during development? For your current stack, I suggest..."
   - "What unit test framework should we prepare? For your current stack, I suggest..."

2. **Always update documentation when adding features**:
   - Update tasks.md with new or modified tasks
   - Update relevant PHASE#.md with implementation details
   - Update specification.md if adding a new technology/package or planned feature
   - Update README.md if user-facing instruction changes

3. **Check documentation sync before major work**:
   - Verify specification.md reflects current architecture
   - Ensure tasks.md is up to date
   - Confirm phase files match implementation

4. **Use templates from references/templates.md** when creating new documentation files

5. **Keep feedback loops short** by updating docs incrementally during implementation, not in large batches after

6. **Remind users about the checklist** before committing code changes

This skill works best when documentation updates are treated as part of feature implementation, not as a separate afterthought.
