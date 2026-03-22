---
name: create-onboarding-guide
description: Create a developer onboarding guide when the user asks to write onboarding docs, create a getting started guide, document the setup process, or help new developers ramp up
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[project name, team, or specific onboarding focus]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: onboarding, docs, developer-experience
---

# Create Onboarding Guide

## Overview

Generate a structured developer onboarding guide by reading all available `.chalk/docs/` documentation and curating it into a progressive learning path. The guide follows a Day 1 / Week 1 / Month 1 structure, starting with environment setup and a first commit, then expanding to architecture understanding and feature ownership. Every step is concrete and runnable — no "ask around" or tribal knowledge assumptions.

## Workflow

1. **Read all available documentation** — Scan the full `.chalk/docs/` directory tree:
   - `.chalk/docs/product/` for product profile, PRDs, user stories, and roadmap
   - `.chalk/docs/engineering/` for architecture docs, ADRs, runbooks, and incident history
   - `.chalk/docs/ai/` for analysis documents and research
   - Root `.chalk/docs/` for any overview or index documents
   Build a mental map of what documentation exists and what gaps remain.

2. **Inspect the codebase** — Use `Bash` and `Glob` to understand the project structure:
   - Package manager and dependency files (package.json, requirements.txt, go.mod, etc.)
   - Build and run scripts
   - Test framework and test file patterns
   - Environment configuration (.env.example, config files)
   - CI/CD configuration
   - Linting and formatting tools

3. **Parse the onboarding scope** — From `$ARGUMENTS`, identify:
   - Which project or team the guide is for
   - Whether the guide targets a specific role (frontend, backend, full-stack, etc.)
   - Any specific areas the user wants emphasized
   If not specified, create a general full-stack onboarding guide.

4. **Build the Day 1 section** — Environment setup and first commit:
   - Step-by-step setup instructions with copy-pasteable commands
   - How to run the application locally
   - How to run the test suite
   - A "hello world" first task: a small, safe change that exercises the full development workflow (edit, test, commit, PR)
   Verify setup steps against actual project files (package.json scripts, Makefile targets, etc.).

5. **Build the Week 1 section** — Architecture and first real contribution:
   - Curated reading list from existing docs, ordered from foundational to detailed
   - Simplified architecture overview (key services, data flow, external dependencies)
   - A starter task: a real but well-scoped issue that builds understanding
   - Key concepts the developer must understand to be effective
   - Common gotchas that trip up new team members (based on incident reports, ADRs, and codebase patterns)

6. **Build the Month 1 section** — Ownership and cross-cutting concerns:
   - Feature ownership expectations
   - Cross-cutting concerns: authentication, logging, error handling, deployment, monitoring
   - How to navigate the codebase for common tasks
   - Who to ask about what (mapped to teams or roles, not individuals)

7. **Create the reading list** — Order all `.chalk/docs/` files into a recommended reading sequence:
   - Start with product profile and architecture overview
   - Then PRDs and ADRs relevant to the developer's area
   - Then runbooks and operational docs
   - Mark which docs are "required reading" vs. "reference"

8. **Identify gaps** — Flag any onboarding needs that are not covered by existing documentation:
   - Missing setup instructions
   - Undocumented architecture decisions
   - Tribal knowledge that should be written down
   List these as "Documentation TODOs" at the end of the guide.

9. **Determine the next file number** — List files in `.chalk/docs/ai/` to find the highest numbered file. Increment by 1.

10. **Write the file** — Save to `.chalk/docs/ai/<n>_onboarding_guide.md`.

11. **Confirm** — Present the guide with a summary of what is covered, the recommended reading list, and any documentation gaps that need to be filled.

## Onboarding Guide Structure

```markdown
# Developer Onboarding Guide

**Project**: <project name>
**Last Updated**: <YYYY-MM-DD>
**Target Audience**: <role or "all developers">

## Day 1: Setup and First Commit

### Environment Setup

Prerequisites:
- <language runtime> (version <X.Y+>)
- <package manager>
- <database or other local services>
- <any other tools>

Step-by-step:

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <project-name>
   ```

2. **Install dependencies**
   ```bash
   <install command>
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with the following values:
   # <explain each required variable>
   ```

4. **Start local services**
   ```bash
   <command to start database, etc.>
   ```

5. **Run the application**
   ```bash
   <run command>
   ```
   You should see: <expected output or URL>

6. **Run the test suite**
   ```bash
   <test command>
   ```
   Expected: All tests pass. If not, check <common fix>.

### Your First Commit

Complete this task to verify your setup and learn the workflow:

**Task**: <small, safe change — e.g., "Add your name to CONTRIBUTORS.md" or "Update a log message">

1. Create a branch: `git checkout -b onboarding/<your-name>`
2. Make the change: <specific instructions>
3. Run tests: `<test command>`
4. Commit: `git add <files>` && `git commit -m "<message>"`
5. Push: `git push -u origin onboarding/<your-name>`
6. Open a PR following the team's PR template

This exercises: branching, local development, testing, and the PR process.

## Week 1: Architecture and First Contribution

### Recommended Reading (Ordered)

| Order | Document | Type | Required |
|-------|----------|------|----------|
| 1 | <product profile> | Product Context | Yes |
| 2 | <architecture doc> | Technical | Yes |
| 3 | <key ADR> | Decision Record | Yes |
| 4 | <relevant PRD> | Product Requirements | Recommended |
| 5 | <runbook> | Operations | Reference |

### Architecture Overview

<Simplified description of the system architecture: key services, how they communicate, data flow, external dependencies. Use a text diagram if helpful.>

```
<simple ASCII architecture diagram>
```

### Key Concepts

To be effective in this codebase, understand these concepts:

1. **<Concept>** — <what it is and why it matters in this project>
2. **<Concept>** — <explanation>
3. **<Concept>** — <explanation>

### Common Gotchas

Issues that trip up every new team member:

- **<Gotcha>** — <what happens and how to fix it>
- **<Gotcha>** — <explanation>
- **<Gotcha>** — <explanation>

### Starter Task

**Task**: <a real, well-scoped issue that a new developer can complete in 2-3 days>

Why this task: <what the developer will learn by completing it>

Resources:
- Relevant code: `<file paths>`
- Related doc: `<doc reference>`

## Month 1: Ownership and Cross-Cutting Concerns

### Cross-Cutting Concerns

| Concern | How It Works | Key Files | Documentation |
|---------|-------------|-----------|---------------|
| Authentication | <brief description> | <paths> | <doc link> |
| Error Handling | <brief description> | <paths> | <doc link> |
| Logging | <brief description> | <paths> | <doc link> |
| Deployment | <brief description> | <paths> | <doc link> |
| Monitoring | <brief description> | <paths> | <doc link> |

### Navigating the Codebase

Common tasks and where to find them:

| Task | Where to Look | Example |
|------|---------------|---------|
| Add a new API endpoint | `<path>` | `<example file>` |
| Add a database migration | `<path>` | `<example file>` |
| Add a new UI component | `<path>` | `<example file>` |
| Add a test | `<path>` | `<example file>` |

### Who to Ask About What

| Area | Team/Role | Channel |
|------|-----------|---------|
| <area> | <team or role> | <how to reach them> |
| <area> | <team or role> | <how to reach them> |

## Documentation Gaps

The following onboarding needs are not covered by existing documentation and should be written:

- [ ] <missing doc or knowledge area>
- [ ] <missing doc or knowledge area>
```

## Output

- **File**: `.chalk/docs/ai/<n>_onboarding_guide.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Developer Onboarding Guide`

## Anti-patterns

- **Information dump without ordering** — Dropping 20 documents on a new developer and saying "read these" is not onboarding. Documents must be ordered from foundational to detailed, with required vs. reference clearly marked.
- **No runnable first task** — A developer who cannot run the app and make a change on Day 1 will lose confidence and momentum. The "hello world" task must be completable in under 2 hours with the setup instructions provided.
- **Assuming tribal knowledge** — "Ask Sarah about the auth system" is not documentation. If knowledge exists only in someone's head, the onboarding guide should flag it as a documentation gap, not encode the dependency on a specific person.
- **Outdated setup steps** — Setup instructions that fail on the first command destroy trust in the entire guide. Verify all commands against actual project files. Include version requirements and common failure modes.
- **No architecture context** — Jumping into code without understanding the system architecture leads to local optimizations and broken mental models. The Week 1 architecture overview provides the map before the developer starts navigating the territory.
- **Missing "who to ask"** — New developers need to know which team owns what. Map areas of responsibility to teams and roles, not individuals (people change roles; team responsibilities are more stable).
- **No documentation gap tracking** — If the onboarding guide cannot cover a topic because no documentation exists, that gap must be explicitly listed. Otherwise the gap persists invisibly and every new developer hits the same wall.
