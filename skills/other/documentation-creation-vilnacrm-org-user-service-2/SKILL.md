---
name: documentation-creation
description: Create comprehensive project documentation from scratch. Use when setting up INITIAL documentation for a new project or building a complete documentation suite. NOT for updating existing docs (use documentation-sync instead). Covers project analysis, documentation structure, templates, and verification.
---

# Documentation Creation Skill

## Overview

This skill guides the creation of comprehensive project documentation from scratch by analyzing the project codebase and applying established VilnaCRM documentation patterns. It ensures documentation accurately reflects the actual project implementation.

**Use this skill for**: Initial documentation creation from scratch
**Use documentation-sync for**: Updating existing documentation when code changes

## Context (Input)

- Need to create documentation for a project from scratch
- Want consistent style following VilnaCRM patterns
- Need to ensure documentation accuracy against actual codebase
- Project has no existing comprehensive documentation

## Task (Function)

Create comprehensive, accurate project documentation by:

1. Analyzing the project codebase thoroughly
2. Creating documentation using established templates
3. Verifying all references against actual codebase
4. Ensuring consistent style and cross-linking

**Success Criteria**:

- All documentation files created with consistent structure
- All code references verified against actual project structure
- All directory paths and file mentions exist in codebase
- All links between documentation files work correctly
- Technology stack accurately reflected (no false claims)

---

## Quick Start: Documentation Creation Workflow

### Step 1: Analyze Project Structure

Before creating any documentation, thoroughly understand the project:

```bash
# Check project structure
ls -la src/

# Identify technology stack
cat composer.json | grep -A5 "require"
cat Dockerfile
cat docker-compose.yml

# Identify bounded contexts
ls -la src/Core/ 2>/dev/null
ls -la src/User/ 2>/dev/null
ls -la src/Shared/ 2>/dev/null
ls -la src/Internal/ 2>/dev/null

# Check for entities
find src -path "*/Entity/*.php"

# Check for commands and handlers
find src -name "*Command.php" | head -20
find src -name "*Handler.php" | head -20
```

**Key items to document**:

- [ ] Technology stack (PHP version, framework, database, runtime)
- [ ] Architecture style (DDD, hexagonal, CQRS)
- [ ] Bounded contexts and their purposes
- [ ] Main entities and their relationships
- [ ] Available commands and testing tools

### Step 2: Create Technology Stack Summary

Document the verified technology stack:

```bash
# PHP version
grep -i "php:" Dockerfile

# Framework
grep -i "symfony" composer.json

# Database
grep -i "mysql\|postgres\|mongo" docker-compose.yml

# Available make commands
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile | head -30
```

Create a technology summary table:

| Component  | Technology | Version |
| ---------- | ---------- | ------- |
| Language   | PHP        | X.Y     |
| Runtime    | {Runtime}  | -       |
| Framework  | Symfony    | X.Y     |
| Database   | {Database} | X.Y     |
| Web Server | {Server}   | -       |

### Step 3: Create Documentation Files

Create each documentation file following this order:

1. **main.md** - Project overview and design principles
2. **getting-started.md** - Installation and quick start
3. **design-and-architecture.md** - Architectural decisions and patterns
4. **developer-guide.md** - Code structure and development workflow
5. **api-endpoints.md** - REST and GraphQL API documentation
6. **testing.md** - Testing strategy and commands
7. **glossary.md** - Domain terminology and naming conventions
8. **user-guide.md** - API usage examples
9. **advanced-configuration.md** - Environment and configuration
10. **performance.md** - Benchmarks and optimization
11. **security.md** - Security measures and practices
12. **operational.md** - Operational considerations
13. **onboarding.md** - New contributor guide
14. **community-and-support.md** - Support channels
15. **legal-and-licensing.md** - License and dependencies
16. **release-notes.md** - Release process
17. **versioning.md** - Versioning policy

> Add project-specific docs as needed (e.g., `performance-frankenphp.md` for FrankenPHP projects)

### Step 4: Write Each Documentation File

For each documentation file:

1. **Use the appropriate template** from [reference/doc-templates.md](reference/doc-templates.md)

2. **Fill in project-specific content**:

   - Project name and description
   - Entity names from codebase
   - Bounded context names
   - URLs and repository links

3. **Verify all references**:

   - Directory paths exist
   - Commands exist in Makefile
   - Entity names match codebase

4. **Add cross-links** to related documentation

### Step 5: Verify Accuracy

Run comprehensive verification using [reference/verification-checklist.md](reference/verification-checklist.md):

1. **Technology Stack Verification**:

   ```bash
   grep -i "php" Dockerfile
   grep -i "symfony" composer.json
   grep -i "mysql\|mongo\|postgres" docker-compose.yml
   ```

2. **Directory Structure Verification**:

   ```bash
   # Verify all mentioned src directories exist
   for dir in $(ls src/); do
     ls -la src/$dir/ 2>/dev/null || echo "Check: src/$dir"
   done
   ```

3. **Command Verification**:

   ```bash
   # Verify mentioned make commands exist
   for cmd in "unit-tests" "integration-tests" "behat" "ci"; do
     grep -q "^$cmd:" Makefile && echo "Found: $cmd" || echo "Missing: $cmd"
   done
   ```

4. **Link Verification**:
   - Check all internal markdown links resolve
   - Verify external links are accurate

---

## Documentation Templates

### Overview Document (main.md)

```markdown
# {Project Name}

Welcome to the **{Project Name}** documentation...

## Design Principles

{List project's core design principles}

## Technology Stack

| Component | Technology | Version |
| --------- | ---------- | ------- |
| Language  | PHP        | X.Y     |
| Framework | Symfony    | X.Y     |
| Database  | {Database} | X.Y     |
```

### Getting Started (getting-started.md)

```markdown
# Getting Started

## Prerequisites

{List required software with versions}

## Installation

{Step-by-step installation commands}

## Verification

{Commands to verify installation}
```

See [reference/doc-templates.md](reference/doc-templates.md) for complete templates.

---

## Constraints

### NEVER

- Include references to non-existent directories or files
- Claim features or technologies the project doesn't use
- Leave placeholder text unreplaced
- Skip verification step after creating documentation
- Document commands that don't exist in Makefile

### ALWAYS

- Verify every directory path mentioned exists
- Confirm technology stack matches project reality
- Test command examples work in the project
- Update all cross-references to point to correct files
- Maintain consistent terminology throughout
- Add Table of Contents to longer documents (100+ lines)

---

## Verification Checklist

After creating documentation:

### Technology Accuracy

- [ ] PHP version matches Dockerfile
- [ ] Framework version matches composer.json
- [ ] Database type matches docker-compose.yml
- [ ] Runtime environment correctly described
- [ ] No false claims about unused technologies

### Structure Accuracy

- [ ] All mentioned `src/` directories exist
- [ ] All bounded context names are correct
- [ ] Entity names match actual codebase
- [ ] Command and handler names are accurate

### Command Accuracy

- [ ] All `make` commands exist in Makefile
- [ ] Docker commands work as documented
- [ ] Test commands produce expected output

### Link Accuracy

- [ ] All internal markdown links resolve
- [ ] External repository links are correct
- [ ] No broken navigation links

### Content Consistency

- [ ] Project name consistent throughout
- [ ] Terminology consistent across documents
- [ ] No placeholder text remaining

---

## Common Pitfalls

### Technology Mismatch

**Problem**: Documenting technologies the project doesn't use

**Solution**:

```bash
# Verify before documenting
grep -i "fpm\|franken" Dockerfile
cat docker-compose.yml
# Only document what actually exists
```

### Missing Directories

**Problem**: Documenting directories that don't exist in `src/`

**Solution**:

```bash
# Verify before documenting
ls -la src/
# Update to match actual structure
```

### Outdated Commands

**Problem**: Documenting non-existent `make` targets

**Solution**:

```bash
# Check actual Makefile
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile
```

### Missing Table of Contents

**Problem**: Long documents hard to navigate

**Solution**: Add TOC to documents over 100 lines:

```markdown
## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

---
```

---

## Format (Output)

### Expected Documentation Structure

```text
docs/
├── main.md                    # Project overview
├── getting-started.md         # Installation guide
├── design-and-architecture.md # Architecture patterns
├── developer-guide.md         # Development workflow
├── api-endpoints.md           # REST/GraphQL docs
├── testing.md                 # Testing strategy
├── glossary.md                # Domain terminology
├── user-guide.md              # API usage examples
├── advanced-configuration.md  # Environment config
├── performance.md             # Benchmarks
├── security.md                # Security measures
├── operational.md             # Operations guide
├── onboarding.md              # Contributor guide
├── community-and-support.md   # Support channels
├── legal-and-licensing.md     # License info
├── release-notes.md           # Release process
└── versioning.md              # Versioning policy
```

### Expected Verification Result

All verification checks pass:

- Technology stack matches reality
- All directory paths exist
- All commands work
- All links resolve

---

## Related Skills

- [documentation-sync](../documentation-sync/SKILL.md) - Keep docs in sync with code changes (use AFTER initial creation)
- [api-platform-crud](../api-platform-crud/SKILL.md) - API documentation patterns
- [testing-workflow](../testing-workflow/SKILL.md) - Testing documentation
- [load-testing](../load-testing/SKILL.md) - Performance documentation

**Skill Relationship**:

- **documentation-creation** (this skill): Create initial documentation from scratch
- **documentation-sync**: Keep existing documentation updated when code changes

---

## Reference Documentation

- **[Doc Templates](reference/doc-templates.md)** - Complete templates for each doc type
- **[Verification Checklist](reference/verification-checklist.md)** - Detailed verification steps
- **[Examples](examples/)** - Real-world documentation examples

---

## Quick Commands

```bash
# Check project structure
ls -laR src/ | head -50

# Find entities
find src -path "*/Entity/*.php"

# Find commands
find src -name "*Command.php"

# Check make commands
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile

# Verify runtime
grep -i "fpm\|franken" Dockerfile

# Check database
grep -i "mysql\|mongo\|postgres" docker-compose.yml

# Verify technology stack
grep -i "php:" Dockerfile
grep -i "symfony" composer.json
```
