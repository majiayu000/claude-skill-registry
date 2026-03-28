---
name: onboard
description: Use when a new developer needs to understand the project, or the user asks for an onboarding or setup guide.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Generate a complete onboarding guide for this project.

## Analyze

1. **Project basics**
   - Read package.json / pyproject.toml / Cargo.toml / go.mod
   - Identify language, framework, database, key dependencies
   - Read README if it exists

2. **Project structure**
   - Scan top-level directories
   - Identify source, test, config, build, and doc directories
   - Map the architecture

3. **Entry points**
   - Find main/index files
   - Find route definitions
   - Find configuration files

4. **Development workflow**
   - Read scripts in package.json
   - Check for Makefile, docker-compose, CI config
   - Identify how to run, test, build, deploy

5. **Code conventions**
   - Read linter configs (.eslintrc, .prettierrc, ruff.toml, etc.)
   - Check existing CLAUDE.md or .editorconfig
   - Sample 3-4 files to identify patterns

6. **Git workflow**
   - Check branch naming from recent branches
   - Read git log for commit message style
   - Check for PR templates (.github/pull_request_template.md)

## Output

```
# Onboarding Guide: [Project Name]

## Quick Start
1. Clone: `git clone [url]`
2. Install: `[install command]`
3. Setup: `[env setup, db setup]`
4. Run: `[dev command]`
5. Test: `[test command]`

## Architecture
[High-level architecture diagram/description]

## Project Structure
[Directory map with purpose of each]

## Key Files
[Entry points and important files]

## Tech Stack
| Category | Technology |
|----------|-----------|
| Language | [X] |
| Framework | [X] |
| Database | [X] |
| Testing | [X] |

## Development Workflow
[How to create branches, commit, PR]

## Code Conventions
[Naming, structure, patterns used]

## Common Tasks
- Add a new API endpoint: [steps]
- Add a new component: [steps]
- Add a new test: [steps]
- Run specific tests: [command]

## Environment Variables
[Required env vars and what they do]

## Useful Commands
| Command | What It Does |
|---------|-------------|
| [cmd] | [description] |
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
