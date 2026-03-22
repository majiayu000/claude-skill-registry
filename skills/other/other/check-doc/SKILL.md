---
name: check-doc
description: Verify documentation and CLAUDE instructions are updated alongside code changes
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash(git diff*), Bash(git show*), Read, Grep, Glob
---

# Documentation Review

Ensure documentation stays synchronized with code changes.

## Scope

Review changes from: `!git diff --name-only HEAD~1` or files specified in $ARGUMENTS

## Documentation Files

| File | Purpose | Update When |
| ---- | ------- | ----------- |
| `CLAUDE.md` | Main project guide | Architecture changes |
| `.claude/CLAUDE-API.md` | API instructions | Backend changes |
| `.claude/CLAUDE-APP-PARTNERS.md` | Partners app guide | Frontend changes |
| `.claude/CLAUDE-OBSERVATORY.md` | Observatory guide | Observatory changes |
| `.claude/CLAUDE-DATALAKE.md` | SQLMesh guide | Data pipeline changes |
| `README.md` | Project overview | Major changes |
| `api/justfile` | Command reference | New commands |

## Documentation Checklist

### 1. CLAUDE Instructions

- [ ] **New patterns**: Document new architectural patterns or conventions
- [ ] **New commands**: Add new Just/CLI commands to relevant docs
- [ ] **New services**: Document new API services in CLAUDE-API.md
- [ ] **New hooks**: Document new React hooks in frontend docs
- [ ] **Breaking changes**: Highlight changes to existing patterns

### 2. Code Comments

- [ ] **Complex logic**: Non-obvious algorithms have explanatory comments
- [ ] **TODOs**: New TODOs have issue references or context
- [ ] **Deprecations**: Deprecated code is marked with `@deprecated`
- [ ] **No stale comments**: Comments match current implementation

### 3. Type Documentation

- [ ] **Interface docs**: Public interfaces have JSDoc comments
- [ ] **Action docs**: Handler decorators describe the action purpose
- [ ] **Complex types**: Non-trivial types are documented

### 4. API Documentation

- [ ] **New endpoints**: Document path, method, params, response
- [ ] **Changed endpoints**: Update docs for modified behavior
- [ ] **Error responses**: Document possible error codes

### 5. Configuration

- [ ] **New env vars**: Document in relevant CLAUDE-*.md files
- [ ] **Default values**: Document default values and valid ranges
- [ ] **Required vs optional**: Clearly indicate which are required

### 6. Database

- [ ] **Schema changes**: Document migration purpose
- [ ] **New tables/columns**: Update database section in docs
- [ ] **Index changes**: Note performance implications

### 7. SQLMesh/Datalake

- [ ] **New models**: Document in CLAUDE-DATALAKE.md
- [ ] **New macros**: Add macro documentation
- [ ] **Schema changes**: Update column conventions if needed

## Analysis Steps

1. **Identify changed components**:

   ```bash
   git diff --name-only HEAD~1 | grep -E '\.(ts|tsx|sql|py)$'
   ```

2. **Check for documentation changes**:

   ```bash
   git diff --name-only HEAD~1 | grep -E '(\.md|CLAUDE)'
   ```

3. **Cross-reference**: Ensure code changes have corresponding doc updates

## Output Format

```markdown
## Documentation Review Summary

**Status**: [UP TO DATE | NEEDS UPDATE | OUTDATED]
**Code Files Changed**: X
**Doc Files Changed**: Y

### Missing Documentation

#### [PRIORITY] Missing Doc for Feature/Change

- **Code change**: path/to/file.ts - description of change
- **Documentation needed**: Which file(s) need updates
- **Suggested content**: Brief outline of what to document

### Stale Documentation

- Documentation that no longer matches the code

### Documentation Updates Included

- Doc changes that correctly reflect code changes

### Required Actions

- [ ] Update specific documentation files
- [ ] Add inline comments for complex logic
- [ ] Update CLAUDE instructions for new patterns
```

## Suggested Documentation Updates

When suggesting updates, provide specific text that can be added:

```markdown
### Suggested Addition to .claude/CLAUDE-API.md

Add to "Service Modules" section:

| `new-service` | Description of what it does |

Add to "Action Pattern" section:

New decorator option `newOption` controls...
```

## Invocation

```
/check-doc                         # Review uncommitted changes
/check-doc src/pdc/services/       # Check docs for specific directory
/check-doc --suggest               # Generate documentation suggestions
```
