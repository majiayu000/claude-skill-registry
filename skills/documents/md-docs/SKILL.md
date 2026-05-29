---
name: md-docs
description: This skill should be used when the user asks to "update README", "update context files", "init context", "create CLAUDE.md", "update CLAUDE.md", "update AGENTS.md", "update DOCS.md", "generate documentation", "API documentation", or mentions project documentation, context files, or markdown documentation workflows.
version: 0.1.0
---

# Markdown Documentation Management

## Overview

Manage project documentation for Claude Code workflows including context files, READMEs, and agent instructions. This skill provides structured automation for maintaining accurate, up-to-date documentation that aligns with actual codebase structure and functionality. Use this skill when initializing new projects, updating existing documentation, or ensuring context files accurately reflect current code.

The skill emphasizes verification and validation over blind generation—analyze the actual codebase structure, file contents, and patterns before creating or updating documentation. All generated content should be terse, imperative, and expert-to-expert rather than verbose or tutorial-style.

## Prerequisites

Before using any documentation workflow, verify basic project structure:

```bash
git rev-parse --git-dir
```

Ensure the output confirms you are in a git repository. If not initialized, documentation workflows may still proceed but git-specific features will be skipped.

For update workflows, verify target files exist:

```bash
ls -la CLAUDE.md AGENTS.md DOCS.md README.md
```

Check which files are present before attempting updates. Missing files will show errors, which helps identify what needs initialization. Note that DOCS.md is optional and only relevant for projects with APIs or public interfaces.

## Update Context Files

Verify and fix CLAUDE.md, AGENTS.md, and optionally DOCS.md against the actual codebase. This workflow reads existing context files, analyzes the codebase structure, identifies discrepancies, and updates documentation to match reality. DOCS.md is only processed if it exists (it contains API/code documentation).

### Workflow Steps

**Parse Arguments**

Support the following arguments:

- `--dry-run`: Show what would change without writing files
- `--preserve`: Keep existing content structure, only fix inaccuracies
- `--thorough`: Perform deep analysis of all files (slower but comprehensive)
- `--minimal`: Quick verification focusing on high-level structure only

**Verify Git Repository**

Confirm working directory is a git repository. If not, warn the user but proceed with limitations (cannot analyze git history or branches).

**Read Existing Context Files**

Read current CLAUDE.md, AGENTS.md, and DOCS.md (if present) contents:

```bash
cat CLAUDE.md
cat AGENTS.md
cat DOCS.md  # if exists
```

Parse the structure and extract documented information including:

- Project description and purpose
- File structure and organization
- Build and test commands
- Custom tooling or scripts
- Agent configurations and triggers
- API endpoints and methods (from DOCS.md)
- Function signatures and parameters (from DOCS.md)
- Type definitions and interfaces (from DOCS.md)

**Analyze Codebase**

Scan the project to gather accurate information:

- Directory structure (`ls -la`, `tree` if available)
- Package configuration (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.)
- Build scripts and commands
- Test frameworks and configurations
- README badges and metadata

For `--thorough` mode, also analyze:

- File content patterns (imports, exports, interfaces)
- Code organization conventions
- Dependency relationships

**Identify Discrepancies**

Compare documented information against actual codebase:

- Outdated file paths or structure
- Incorrect build commands
- Missing or removed features
- Deprecated dependencies
- Stale agent configurations
- Outdated API endpoints or routes (DOCS.md)
- Changed function signatures (DOCS.md)
- Modified type definitions (DOCS.md)

**Create Backups**

Before overwriting, create backup files:

```bash
cp CLAUDE.md CLAUDE.md.backup
cp AGENTS.md AGENTS.md.backup
test -f DOCS.md && cp DOCS.md DOCS.md.backup
```

**Update Context Files**

Write corrected versions maintaining the existing structure when `--preserve` is used, or reorganizing for clarity when not. For `--dry-run`, display the diff without writing:

```bash
diff -u CLAUDE.md.backup CLAUDE.md
```

**Generate Report**

Display a summary of changes.

When DOCS.md exists:

```
✓ Updated CLAUDE.md
  - Fixed outdated build command
  - Added new /api directory to structure

✓ Updated AGENTS.md
  - Updated test-runner trigger pattern

✓ Updated DOCS.md
  - Fixed outdated endpoint path /api/v1/users
  - Updated function signature for createUser()
```

When DOCS.md is absent:

```
✓ Updated CLAUDE.md
  - Fixed outdated build command

✓ Updated AGENTS.md
  - Updated test-runner trigger pattern

⊘ DOCS.md not found (skipped)
```

For the complete update context files workflow with verification strategies, diff examples, and edge cases, refer to `./references/update-agents.md`.

## Update README

Generate or update README.md based on project structure, package metadata, and codebase analysis. This workflow creates comprehensive, accurate READMEs that reflect the actual state of the project.

### Workflow Steps

**Parse Arguments**

Support the following arguments:

- `--dry-run`: Preview README content without writing
- `--preserve`: Keep existing sections, only update outdated information
- `--minimal`: Generate minimal README (title, description, installation, usage)
- `--full`: Generate comprehensive README with all optional sections

**Analyze Project Structure**

Gather information from multiple sources:

```bash
# Package metadata
cat package.json
cat pyproject.toml
cat Cargo.toml

# Git information
git remote get-url origin
git describe --tags

# Directory structure
ls -la
```

Extract:

- Project name and description
- Version number
- Repository URL
- License
- Dependencies
- Scripts/commands

**Read Existing README**

If README.md exists and `--preserve` is used:

```bash
cat README.md
```

Parse existing sections to preserve custom content while updating technical details.

**Create Backup**

Before overwriting existing README:

```bash
cp README.md README.md.backup
```

**Generate README Content**

Create structured content with appropriate sections:

- **Title and badges** (version, license, build status)
- **Description** (concise project summary)
- **Installation** (package manager commands)
- **Usage** (basic examples)
- **Development** (build, test, lint commands)
- **Contributing** (if applicable)
- **License** (based on package metadata)

For `--minimal` mode, include only title, description, installation, and usage.

For `--full` mode, also include:

- API documentation
- Examples directory listing
- Deployment instructions
- Troubleshooting section
- Credits and acknowledgments

**Write README**

Save the generated content. For `--dry-run`, display without writing.

**Generate Report**

Display summary:

```
✓ Updated README.md
  - Added installation section
  - Updated build commands to match package.json
  - Added badges for license and version
```

For the complete update README workflow with section templates, metadata extraction strategies, and formatting examples, refer to `./references/update-readme.md`.

## Initialize Context

Create project-specific CLAUDE.md from scratch based on codebase analysis. This workflow is ideal for new projects or repositories lacking context documentation.

### Workflow Steps

**Parse Arguments**

Support the following arguments:

- `--dry-run`: Preview generated content without writing
- `--minimal`: Create minimal context file (project description, structure)
- `--full`: Create comprehensive context file with all relevant sections

**Verify No Existing CLAUDE.md**

Check if CLAUDE.md already exists:

```bash
test -f CLAUDE.md && echo "exists" || echo "missing"
```

If exists, warn the user and suggest using the update workflow instead. Allow override with `--force` flag.

**Analyze Project**

Gather comprehensive information:

- Language and framework (detect from files and package configs)
- Directory structure and organization patterns
- Build system (npm, cargo, poetry, gradle, etc.)
- Test framework (jest, pytest, cargo test, etc.)
- Linting and formatting tools
- Environment variables or configuration files

**Generate CLAUDE.md Content**

Create structured sections:

```markdown
# Context

Brief project description and purpose.

## Structure

Directory organization and key files.

## Build

Commands for building the project.

## Test

Commands for running tests.

## Development

Conventions, patterns, and workflows.
```

Adapt sections based on project type. For `--minimal`, include only Context and Structure. For `--full`, add all applicable sections including deployment, troubleshooting, and custom tooling.

**Write CLAUDE.md**

Save generated content. For `--dry-run`, display without writing.

**Generate Report**

Display summary:

```
✓ Created CLAUDE.md
  - Detected Next.js project
  - Added npm scripts from package.json
  - Documented project structure
  - Added testing section for Jest
```

For the complete initialize context workflow with language-specific templates, detection strategies, and customization options, refer to `./references/init-agents.md`.

### DOCS.md Initialization

DOCS.md is optional and not created by default. Create DOCS.md manually when the project has:

- Public API endpoints requiring documentation
- Exported functions or classes intended for external use
- Complex type definitions users need to understand

The update context workflow will suggest creating DOCS.md if it detects significant APIs without corresponding documentation.

## Common Patterns

Shared conventions and patterns used across all documentation workflows.

### Argument Parsing

Standard arguments supported across workflows:

- `--dry-run`: Preview changes without writing files
- `--preserve`: Maintain existing structure, only fix inaccuracies
- `--minimal`: Generate minimal documentation
- `--thorough`/`--full`: Generate comprehensive documentation
- `--force`: Override safety checks

Parse arguments from user input and set appropriate flags for workflow execution.

### Backup File Handling

Always create backups before overwriting existing files:

```bash
cp CLAUDE.md CLAUDE.md.backup
cp AGENTS.md AGENTS.md.backup
test -f DOCS.md && cp DOCS.md DOCS.md.backup  # only if exists
```

Inform the user when backups are created:

```
Created backup: CLAUDE.md.backup
Created backup: AGENTS.md.backup
Created backup: DOCS.md.backup (optional file)
```

Never delete backups automatically. Let users manage backup cleanup manually. Note that DOCS.md is optional—skip backup and update operations if it doesn't exist.

### Writing Style

Documentation should follow these conventions:

- **Terse**: Omit needless words, lead with the answer
- **Imperative**: Use command form ("Build the project") not descriptive ("The project is built")
- **Expert-to-expert**: Skip basic explanations, assume competence
- **Scannable**: Use headings, lists, and code blocks for easy navigation
- **Accurate**: Verify all commands and paths against actual codebase

**Good:**

```markdown
## Build

Build the project:

\`\`\`bash
npm run build
\`\`\`

Run tests:

\`\`\`bash
npm test
\`\`\`
```

**Bad:**

```markdown
## Building the Project

In order to build the project, you will need to use the npm build command. This command will compile all of the TypeScript files and generate the output in the dist directory. First, make sure you have installed all dependencies by running npm install.
```

### Report Formatting

After completing operations, display a clear summary:

```
✓ Updated CLAUDE.md
  - Fixed build command
  - Added new directory structure

✓ Updated README.md
  - Added installation section
  - Updated badges

✓ Updated DOCS.md
  - Updated API endpoint documentation
  - Fixed function signature

✗ AGENTS.md not found
  - Skipped update

⊘ DOCS.md not found
  - Skipped (optional file)
```

Use checkmarks (✓) for successful operations, crosses (✗) for failed operations, and ⊘ for skipped optional files. Include indented details showing specific changes made.

### File Detection

Detect project type and structure by checking for characteristic files:

```bash
# Node.js/JavaScript
test -f package.json

# Python
test -f pyproject.toml || test -f setup.py

# Rust
test -f Cargo.toml

# Go
test -f go.mod
```

Use detection results to customize documentation templates and commands.

### Metadata Extraction

Read package configuration files to extract accurate metadata:

```bash
# Node.js
cat package.json | grep -E '"name"|"version"|"description"'

# Python
cat pyproject.toml | grep -E 'name|version|description'
```

Parse JSON or TOML appropriately to extract values. Never hardcode or guess metadata when it can be read directly from configuration files.

## Additional Resources

For detailed workflows, examples, and implementation guidance, refer to these reference documents:

- **`./references/update-agents.md`** - Complete context file update workflow including verification strategies, diff generation, and discrepancy detection
- **`./references/update-readme.md`** - Complete README update workflow including section templates, metadata extraction, and formatting conventions
- **`./references/init-agents.md`** - Complete context initialization workflow including language-specific templates, detection strategies, and customization options

These references provide implementation details, code examples, and troubleshooting guidance for each workflow type.
