---
name: standards-creator
description: Create phase-appropriate standards files using latest documentation from context7 and web sources. Invoked by prepare-standards command to generate missing standards files based on task requirements.
---

# Standards Creator Skill

## Purpose

Generate comprehensive, phase-appropriate standards files by fetching the latest documentation from context7 and web sources. This skill creates standards files that guide implementation work, ensuring consistency and best practices across all development tasks.

## When to Use

This skill is invoked by the `/prepare-standards` command when:
- A standard file is referenced in tasks.yaml but doesn't exist
- Creating standards for backend, frontend, testing, Python, database, or other technical domains
- Need to ensure standards reflect latest library versions and best practices

## Input Parameters

The skill expects to be invoked with:
- `standard_name`: Name of the standard (e.g., "backend-standard", "python-standard")
- `phase`: Current development phase (prototype/mvp/growth/scale)
- `tasks_context`: List of task IDs that require this standard
- `task_details`: Relevant information from tasks (what/goal/check fields)

## Process

### 1. Analyze Requirements

Review the input parameters to understand:
- What type of standard is needed (backend, frontend, testing, etc.)
- Which technologies are involved (extract from task_details)
- What phase-appropriate quality level is required

Example technologies to identify:
- Backend: FastAPI, Flask, Django, Express, NestJS
- Frontend: React, Vue, Angular, Svelte
- Testing: pytest, Jest, Mocha, Cypress
- Database: PostgreSQL, MongoDB, Redis
- Python: venv, pip, poetry, type hints

### 2. Fetch Latest Documentation

**Use context7 MCP first:**

For each identified technology, use the context7 tools:

```
1. Call mcp__context7__resolve-library-id with library name
2. Call mcp__context7__get-library-docs with the resolved ID
3. Focus on topics relevant to the standard type
```

Example for backend-standard needing FastAPI:
```
resolve-library-id: "fastapi"
get-library-docs: context7ID, topic="application setup, routing, dependency injection, error handling"
```

Example for testing-standard needing pytest:
```
resolve-library-id: "pytest"
get-library-docs: context7ID, topic="test organization, fixtures, parametrization, test discovery"
```

**Fallback to web search if needed:**

If context7 doesn't have sufficient information or library is not available:
- Use WebSearch tool for latest best practices
- Limit to maximum 10 search queries
- Focus on official documentation sites and authoritative sources
- Prioritize recent content (2024-2025)

Search query patterns:
- "{library} {version} best practices 2025"
- "{library} production setup guide"
- "{library} error handling patterns"
- "{library} testing strategies"

### 3. Apply Phase Requirements

Load phase requirements from `references/phase-requirements.md` and adapt content:

**Prototype Phase:**
- Minimal setup, speed over perfection
- Basic error handling
- 2 tests per feature (smoke + happy path)
- Focus on "good enough to ship in 30 minutes"

**MVP Phase:**
- More robust error handling
- 4 tests per feature (smoke, happy, error, auth)
- Input validation
- Basic logging

**Growth Phase:**
- Comprehensive error handling
- 5 tests per feature (+ edge cases)
- Performance considerations
- Monitoring and observability

**Scale Phase:**
- Production-grade reliability
- 6-8 tests per feature
- Security hardening
- Full observability stack

### 4. Generate Standard File

Create the standard file using the appropriate template from `assets/` directory.

**Standard Structure:**

```markdown
# {Standard Name} - {Phase} Phase

Generated: {timestamp}
Phase: {phase}
Quality Target: {quality score}/10

## Overview

{Brief description of what this standard covers}

## Phase Requirements

{Phase-specific requirements from phase-requirements.md}

## Technology Stack

{List of technologies covered with versions}

## Setup and Configuration

{Environment setup, dependencies, configuration}

## Project Structure

{Recommended file/folder organization}

## Coding Standards

{Code style, naming conventions, patterns to follow}

## Error Handling

{How to handle errors appropriately for this phase}

## Testing Standards

{How to test this type of code for this phase}

## Examples

{Code examples demonstrating the standards}

## Common Pitfalls

{Things to avoid, known issues}

## Resources

{Links to documentation used}
- Context7: {libraries fetched}
- Web sources: {URLs consulted}
```

### 5. Save and Validate

- Save standard to `ai-state/standards/{standard-name}.md`
- Verify file was created successfully
- Log the creation to `ai-state/operations.log`:

```
[{timestamp}] [standards-creator] Created {standard-name}.md for {phase} phase
[{timestamp}] [standards-creator] Used context7: {library list}
[{timestamp}] [standards-creator] Web searches: {count}
```

## Bundled Resources

### References

- `references/phase-requirements.md` - Detailed requirements for each phase
- `references/standard-types.md` - Common patterns for each standard type

### Assets

- `assets/backend-standard-template.md` - Template for backend standards
- `assets/python-standard-template.md` - Template for Python standards
- `assets/testing-standard-template.md` - Template for testing standards
- `assets/frontend-standard-template.md` - Template for frontend standards
- `assets/database-standard-template.md` - Template for database standards

## Output

**Success:** Standard file created at `ai-state/standards/{standard-name}.md`

**Contents include:**
- Phase-appropriate guidance
- Latest documentation references
- Practical code examples
- Technology-specific best practices
- Testing requirements for the phase

## Example Usage

Invoked by `/prepare-standards` command:

```
Input:
  standard_name: "backend-standard"
  phase: "prototype"
  tasks_context: ["task-001-fastapi-setup", "task-002-task-model", "task-003-storage-layer"]
  task_details: "FastAPI, Pydantic models, in-memory storage, REST endpoints"

Process:
  1. Identify technologies: FastAPI, Pydantic v2
  2. Fetch docs via context7 for FastAPI and Pydantic
  3. Load prototype phase requirements
  4. Use assets/backend-standard-template.md
  5. Generate file with FastAPI setup, Pydantic models, error handling
  6. Save to ai-state/standards/backend-standard.md

Output:
  ✓ Created backend-standard.md (prototype phase)
  ✓ Includes: FastAPI setup, Pydantic validation, error handling, 2-test strategy
  ✓ Based on latest FastAPI and Pydantic v2 documentation
```

## Critical Rules

- **Always use context7 first** before web search
- **Limit web searches to 10 maximum** to avoid token bloat
- **Adapt content to phase** - don't include scale-phase complexity in prototype standards
- **Include specific examples** from the fetched documentation
- **Log all operations** to operations.log for transparency
- **Validate before saving** - ensure all template sections are filled

## Success Criteria

✓ Standard file exists at correct path
✓ Content is phase-appropriate
✓ Uses latest documentation from context7
✓ Includes practical examples
✓ References documented in Resources section
✓ Operations logged successfully
