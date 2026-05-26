---
name: agent-ops-dependencies
description: "Dependency management, updates, and security advisory handling. Use when adding, updating, or auditing project dependencies."
category: utility
invokes: [agent-ops-state, agent-ops-validation, agent-ops-interview]
invoked_by: [agent-ops-implementation, agent-ops-improvement-discovery]
state_files:
  read: [constitution.md, baseline.md, focus.md]
  write: [focus.md, issues/*.md]
---

# Dependencies Workflow

## Purpose

Safely manage project dependencies including adding new packages, updating existing ones, and handling security advisories.

## When to Use

- Adding a new dependency to the project
- Updating dependencies (routine or security)
- Auditing dependencies for vulnerabilities
- Investigating dependency conflicts
- Removing unused dependencies

## Preconditions

- `.agent/constitution.md` exists with package manager info
- Understand the project's dependency management approach

## Dependency Operations

### Adding a New Dependency

**Procedure**:

1. **Justify the addition**:
   - What problem does it solve?
   - Is there an existing alternative in the project?
   - What is the package's maintenance status?
   - What is the license? (compatible with project?)

2. **Evaluate the package**:
   - Check download stats / popularity
   - Check last update date
   - Check open issues / security history
   - Check transitive dependencies (avoid bloat)

3. **Add with pinned version**:
   ```bash
   # npm
   npm install package-name@version --save-exact
   
   # pip
   pip install package-name==version
   
   # cargo
   cargo add package-name@version
   ```

4. **Update lock file**: Ensure lock file is committed

5. **Run validation**: Full test suite after adding

6. **Document**: Note in CHANGELOG if user-facing

### Updating Dependencies

**Routine Updates**:

1. Check for available updates
2. Review changelogs for breaking changes
3. Update one package at a time (easier to debug)
4. Run full test suite after each update
5. Commit with clear message

**Security Updates** (Priority):

1. Identify severity (critical/high/medium/low)
2. For critical/high: update immediately
3. For medium/low: batch with routine updates
4. Test thoroughly (security patches can break things)
5. Document in CHANGELOG

### Removing Dependencies

1. Identify why it's being removed
2. Find all usages in codebase
3. Remove usages first
4. Remove from package manifest
5. Update lock file
6. Run full test suite
7. Document removal reason

## Security Audit

### Running an Audit

```bash
# npm
npm audit

# pip (with safety)
safety check

# cargo
cargo audit

# yarn
yarn audit
```

### Audit Report Format

```markdown
## Dependency Audit - [date]

### Summary
- Total dependencies: X
- Direct: Y
- Transitive: Z
- Vulnerabilities found: N

### Vulnerabilities

| Package | Severity | CVE | Fix Available | Action |
|---------|----------|-----|---------------|--------|
| pkg-a | CRITICAL | CVE-XXXX | Yes (v2.0.1) | Update |
| pkg-b | HIGH | CVE-YYYY | No | Evaluate alternatives |
| pkg-c | MEDIUM | CVE-ZZZZ | Yes (v1.2.3) | Schedule update |

### Recommendations
1. Immediate: Update pkg-a to v2.0.1
2. Short-term: Replace pkg-b with alternative
3. Routine: Update pkg-c in next batch
```

## Package Manager Reference

### Node.js (npm/yarn/pnpm)

| Operation | npm | yarn | pnpm |
|-----------|-----|------|------|
| Add | `npm install pkg` | `yarn add pkg` | `pnpm add pkg` |
| Add dev | `npm install -D pkg` | `yarn add -D pkg` | `pnpm add -D pkg` |
| Remove | `npm uninstall pkg` | `yarn remove pkg` | `pnpm remove pkg` |
| Update | `npm update pkg` | `yarn upgrade pkg` | `pnpm update pkg` |
| Audit | `npm audit` | `yarn audit` | `pnpm audit` |
| Lock file | `package-lock.json` | `yarn.lock` | `pnpm-lock.yaml` |

### Python (pip/poetry/pipenv)

| Operation | pip | poetry | pipenv |
|-----------|-----|--------|--------|
| Add | `pip install pkg` | `poetry add pkg` | `pipenv install pkg` |
| Add dev | `pip install pkg` (manual) | `poetry add -D pkg` | `pipenv install -d pkg` |
| Remove | `pip uninstall pkg` | `poetry remove pkg` | `pipenv uninstall pkg` |
| Update | `pip install -U pkg` | `poetry update pkg` | `pipenv update pkg` |
| Lock file | `requirements.txt` | `poetry.lock` | `Pipfile.lock` |

### Rust (cargo)

| Operation | Command |
|-----------|---------|
| Add | `cargo add pkg` |
| Add dev | `cargo add --dev pkg` |
| Remove | `cargo remove pkg` |
| Update | `cargo update -p pkg` |
| Audit | `cargo audit` |
| Lock file | `Cargo.lock` |

## Constraints

### Must Check with Constitution

- Allowed package sources (registries)
- Version pinning policy
- Lock file policy (commit or not)
- Audit requirements
- License restrictions

### Safety Rules

- ❌ Never add dependencies without justification
- ❌ Never update major versions without review
- ❌ Never ignore critical security vulnerabilities
- ❌ Never remove lock files
- ✅ Always run tests after dependency changes
- ✅ Always commit lock file changes
- ✅ Always document significant dependency changes

## Integration with AgentOps

### During Planning

If task requires new dependency:
1. Add dependency evaluation to plan
2. Note license and security considerations
3. Plan for testing after addition

### During Implementation

When adding dependency:
1. Follow the addition procedure above
2. Update focus.md with dependency added
3. Note in task's `files_actually_changed`

### During Review

Check for:
- Unnecessary new dependencies
- Outdated dependencies with known vulnerabilities
- Unused dependencies that can be removed

## Output

Update `.agent/focus.md`:
```markdown
## Just did
- Added dependency: package-name@1.2.3
  - Reason: needed for feature X
  - License: MIT (compatible)
  - Tests: PASS
```

Create task for security issues:
```markdown
## T-XXXX — Update vulnerable dependency
- Type: security
- Priority: P0
- Description: pkg-a has CRITICAL vulnerability CVE-XXXX
- Action: Update to v2.0.1
```

```
