---
name: check-qa
description: Quality code review enforcing Deno standards and project conventions
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash(git diff*), Bash(git show*), Bash(deno lint*), Bash(deno fmt*), Read, Grep, Glob
---

# Quality Assurance Code Review

Review code for quality, consistency with project conventions, and Deno best practices.

## Scope

Review changes from: `!git diff --name-only HEAD~1` or files specified in $ARGUMENTS

## Pre-checks

Run automated checks first:
```bash
cd api && deno lint
cd api && deno fmt --check
```

## Quality Checklist

### 1. Code Style & Formatting
- [ ] **Line width**: Max 120 characters (per deno.jsonc)
- [ ] **Import organization**: Use Deno's organize imports (no `../../../` paths, use `@/`)
- [ ] **Consistent naming**: PascalCase for classes/interfaces, camelCase for functions/variables
- [ ] **No unused imports**: Remove dead imports
- [ ] **No commented code**: Remove or document why it's kept

### 2. TypeScript Standards
- [ ] **Explicit types**: Function parameters and return types should be typed
- [ ] **No `any`**: Avoid `any`, use `unknown` or proper types
- [ ] **Interface naming**: Use `Interface` suffix for interfaces
- [ ] **Type imports**: Use `import type` for type-only imports
- [ ] **Null handling**: Prefer `undefined` over `null` unless interfacing with external APIs

### 3. ILOS Framework Conventions
- [ ] **Action structure**: Actions extend `Action` class with proper `handle` method
- [ ] **Handler decorator**: Correct `@handler()` configuration
- [ ] **Service signatures**: Format `service:method` for RPC calls
- [ ] **Repository pattern**: SQL via `sql` template literal, no string concatenation
- [ ] **Dependency injection**: Use Inversify decorators properly

### 4. Error Handling
- [ ] **Specific exceptions**: Use typed exceptions (NotFoundException, etc.)
- [ ] **Error context**: Include relevant context in error messages
- [ ] **Async/await**: Proper try/catch for async operations
- [ ] **No swallowed errors**: All catch blocks either rethrow or log

### 5. Testing
- [ ] **Test coverage**: New logic has corresponding tests
- [ ] **Test naming**: `.unit.spec.ts` or `.integration.spec.ts` suffix
- [ ] **Edge cases**: Tests cover boundary conditions
- [ ] **Test isolation**: Tests don't depend on each other

### 6. Code Organization
- [ ] **Single responsibility**: Functions/classes do one thing
- [ ] **File length**: Files under 300 lines preferred
- [ ] **Function length**: Functions under 50 lines preferred
- [ ] **Nesting depth**: Max 3-4 levels of nesting

### 7. Project Coherence
- [ ] **Existing patterns**: Follow patterns from similar existing code
- [ ] **Shared types**: Use types from `shared/` or define in service contracts
- [ ] **Configuration**: Use `env_or_*` helpers for environment variables
- [ ] **No over-engineering**: Simple solutions preferred (per CLAUDE.md)

### 8. Deno 2.x Best Practices
- [ ] **Import maps**: Use aliases from deno.jsonc
- [ ] **Standard library**: Prefer `jsr:@std/*` packages
- [ ] **Node compatibility**: Use `node:` prefix for Node.js APIs
- [ ] **Permission-aware**: Consider minimal permission requirements

## Output Format

```markdown
## Quality Review Summary

**Quality Score**: [A | B | C | D | F]
**Files Reviewed**: X files
**Lint Issues**: X errors, Y warnings

### Code Issues

#### [SEVERITY] Issue Title
- **File**: path/to/file.ts:line
- **Issue**: What's wrong
- **Standard**: Which convention is violated
- **Fix**: How to correct it

### Style Issues
- Minor formatting or naming issues

### Suggestions
- Non-blocking improvements for code quality

### Approved Changes
- Changes that meet quality standards

### Required Actions
- [ ] Fix all ERROR level issues
- [ ] Address WARNING level issues
- [ ] Run `deno fmt` before commit
```

## Invocation

```
/check-qa                          # Review uncommitted changes
/check-qa src/pdc/services/auth/   # Review specific directory
/check-qa --strict                 # Enable stricter checks
```
