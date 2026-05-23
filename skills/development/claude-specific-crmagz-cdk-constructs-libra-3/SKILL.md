---
name: claude-specific
description: Claude Code specific instructions for working with this CDK monorepo. General guidance on code generation, refactoring, and feature additions.
---

# Claude-Specific Instructions

## Overview

This document provides Claude-specific instructions for working with this CDK constructs library monorepo.

## Project Context

When working with Claude, be aware of:

1. **Monorepo Structure**: This is a workspace with multiple packages
2. **Build Order**: Packages must be built in dependency order
3. **Workspace Dependencies**: Use `"*"` for internal package references
4. **No Circular Dependencies**: Always check dependency structure

## Key Guidelines

### Code Generation

When generating code:

- Always follow import conventions (explicit named imports)
- Include JSDoc comments for all public APIs
- Use proper naming conventions
- Follow construct patterns from existing code
- Ensure environment-aware configurations

### Refactoring

When refactoring:

1. Check dependency order in `tsconfig.build.json`
2. Verify no circular dependencies are created
3. Update all affected packages
4. Run `npm run build:workspaces` to verify
5. Run `npm run lint` to check for issues

### Adding Features

When adding new features:

1. Determine if it belongs in root or a subpackage
2. Follow the subpackage structure if creating new package
3. Add proper tests and documentation
4. Update relevant documentation files
5. Ensure proper exports from index.ts

## Available Skills

Claude Code has access to specialized skills for this project:

- `repository-structure` - Project structure and architecture
- `import-conventions` - Import rules and ordering
- `naming-conventions` - Naming standards
- `construct-development` - Construct patterns and best practices
- `package-management` - Package configuration and dependencies
- `build-and-deployment` - Build process and commands
- `testing` - Testing requirements and examples
- `common-tasks` - Step-by-step guides for common tasks
- `formatting-standards` - Code formatting rules

## Important Reminders

1. **New constructs go in subpackages**, not the root package
2. **Always use explicit imports**, never wildcards
3. **Match CDK versions** across all packages
4. **Include environment in resource names** to prevent collisions
5. **Gate expensive features** to production environments
6. **Export everything** from `src/index.ts`
7. **Create test files** for all constructs
8. **Add JSDoc comments** to all public APIs
9. **Run lint and format** before committing
10. **Follow dependency order** when adding packages
