---
name: checklist-generator
description: Generate context-aware quality checklists for code review and QA using IEEE 1028 base standards plus LLM contextual additions
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep]
best_practices:
  - Start with IEEE 1028 base checklist (80-90% coverage)
  - Add contextual items based on project type (10-20%)
  - Mark AI-generated items with [AI-GENERATED] prefix
  - Tailor checklist to current file types and frameworks
  - Return markdown checklist with checkboxes
error_handling: strict
streaming: supported
---

# Quality Checklist Generator

## Overview

Generate comprehensive, context-aware quality checklists combining IEEE 1028 standards (80-90%) with LLM-generated contextual items (10-20%). Ensures systematic quality validation before completion.

**Core principle:** Universal quality standards enhanced with project-specific context.

## When to Use

**Always:**

- Before completing implementation tasks
- During code review
- QA validation phase
- Pre-commit verification
- Before marking tasks complete

**Exceptions:**

- Throwaway prototypes
- Configuration-only changes

## Purpose

1. **IEEE 1028 Base**: Proven quality review standards (universal)
2. **Contextual Enhancement**: LLM adds project-specific items
3. **Systematic Validation**: Ensures comprehensive quality coverage

## IEEE 1028 Base Categories

The following categories are included in every checklist (80-90% of items):

### Code Quality

- Code follows project style guide
- No code duplication (DRY principle)
- Cyclomatic complexity < 10 per function
- Functions have single responsibility
- Variable names are clear and descriptive
- Magic numbers replaced with named constants
- Dead code removed

### Testing

- Tests written first (TDD followed)
- All new code has corresponding tests
- Tests cover edge cases and error conditions
- Test coverage ≥ 80% for new code
- Integration tests for multi-component interactions
- Tests are isolated and don't depend on order

### Security

- Input validation on all user inputs
- No SQL injection vulnerabilities
- No XSS vulnerabilities
- Sensitive data encrypted at rest and in transit
- Authentication and authorization checks present
- No hardcoded secrets or credentials
- OWASP Top 10 considered

### Performance

- No obvious performance bottlenecks
- Database queries optimized (no N+1 queries)
- Appropriate caching used
- Resource cleanup (close connections, release memory)
- No infinite loops or recursion risks
- Large data operations paginated

### Documentation

- Public APIs documented
- Complex logic has explanatory comments
- README updated if needed
- CHANGELOG updated
- Breaking changes documented
- Architecture diagrams updated if structure changed

### Error Handling

- All error conditions handled
- User-friendly error messages (4xx for user errors)
- Detailed logs for debugging (5xx for system errors)
- No swallowed exceptions
- Graceful degradation implemented
- Rollback procedures for failures

## Contextual Addition Logic

The skill analyzes the current project context to add 10-20% contextual items:

### Detection Strategy

1. **Read project files** to identify:
   - Framework (React, Vue, Angular, Next.js, FastAPI, etc.)
   - Language (TypeScript, Python, Go, Java, etc.)
   - Patterns (REST API, GraphQL, microservices, monolith)
   - Infrastructure (Docker, Kubernetes, serverless)

2. **Generate contextual items** based on findings:

**TypeScript Projects:**

- [ ] [AI-GENERATED] TypeScript types exported properly
- [ ] [AI-GENERATED] No `any` types unless justified with comment
- [ ] [AI-GENERATED] Strict null checks satisfied

**React Projects:**

- [ ] [AI-GENERATED] Components use proper memo/useCallback
- [ ] [AI-GENERATED] No unnecessary re-renders (React DevTools checked)
- [ ] [AI-GENERATED] Hooks follow Rules of Hooks
- [ ] [AI-GENERATED] Accessibility attributes (aria-\*) on interactive elements

**API Projects:**

- [ ] [AI-GENERATED] Rate limiting implemented
- [ ] [AI-GENERATED] API versioning strategy followed
- [ ] [AI-GENERATED] OpenAPI/Swagger docs updated
- [ ] [AI-GENERATED] Request/response validation with schemas

**Database Projects:**

- [ ] [AI-GENERATED] Migration scripts reversible
- [ ] [AI-GENERATED] Indexes added for query performance
- [ ] [AI-GENERATED] Database transactions used appropriately
- [ ] [AI-GENERATED] Connection pooling configured

**Python Projects:**

- [ ] [AI-GENERATED] Type hints on all public functions
- [ ] [AI-GENERATED] Docstrings follow Google/NumPy style
- [ ] [AI-GENERATED] Virtual environment requirements.txt updated

**Mobile Projects:**

- [ ] [AI-GENERATED] Offline mode handled gracefully
- [ ] [AI-GENERATED] Battery usage optimized (no constant polling)
- [ ] [AI-GENERATED] Data usage minimized (compression, caching)
- [ ] [AI-GENERATED] Platform-specific features tested

**DevOps/Infrastructure:**

- [ ] [AI-GENERATED] Infrastructure as code (Terraform, CloudFormation)
- [ ] [AI-GENERATED] Monitoring and alerting configured
- [ ] [AI-GENERATED] Backup and disaster recovery tested
- [ ] [AI-GENERATED] Security groups/firewall rules minimal access

## Output Format

Checklists are returned as markdown with checkboxes:

```markdown
# Quality Checklist

Generated: {timestamp}
Context: {detected frameworks/languages}

## Code Quality (IEEE 1028)

- [ ] Code follows project style guide
- [ ] No code duplication
- [ ] Cyclomatic complexity < 10

## Testing (IEEE 1028)

- [ ] Tests written first (TDD followed)
- [ ] Test coverage ≥ 80%
- [ ] Tests cover edge cases

## Security (IEEE 1028)

- [ ] Input validation on all user inputs
- [ ] No hardcoded secrets
- [ ] OWASP Top 10 considered

## Performance (IEEE 1028)

- [ ] No obvious performance bottlenecks
- [ ] Database queries optimized
- [ ] Appropriate caching used

## Documentation (IEEE 1028)

- [ ] Public APIs documented
- [ ] README updated if needed
- [ ] CHANGELOG updated

## Error Handling (IEEE 1028)

- [ ] All error conditions handled
- [ ] User-friendly error messages
- [ ] Detailed logs for debugging

## Context-Specific Items (AI-Generated)

{Detected: TypeScript + React + REST API}

- [ ] [AI-GENERATED] TypeScript types exported properly
- [ ] [AI-GENERATED] React components use proper memo
- [ ] [AI-GENERATED] API rate limiting implemented
- [ ] [AI-GENERATED] OpenAPI docs updated

---

**Total Items**: {count}
**IEEE Base**: {ieee_count} ({percentage}%)
**Contextual**: {contextual_count} ({percentage}%)
```

## Usage

### Basic Invocation

```javascript
Skill({ skill: 'checklist-generator' });
```

This will:

1. Analyze current project context
2. Load IEEE 1028 base checklist
3. Generate contextual items (10-20%)
4. Return combined markdown checklist

### With Specific Context

```javascript
// Provide explicit context
Skill({
  skill: 'checklist-generator',
  args: 'typescript react api',
});
```

### Integration with QA Workflow

```javascript
// Part of QA validation
Skill({ skill: 'checklist-generator' });
// Use checklist for systematic validation
Skill({ skill: 'qa-workflow' });
```

## Integration Points

### QA Agent

The `qa` agent uses this skill for validation:

1. Generate checklist at task start
2. Validate each item systematically
3. Report checklist completion status

### Verification-Before-Completion

Used as pre-completion gate:

1. Generate checklist before marking task complete
2. Ensure all items verified
3. Block completion if critical items fail

### Code-Reviewer Agent

Used during code review:

1. Generate checklist for PR
2. Check each item against changes
3. Comment on missing items

## Context Detection Algorithm

```
1. Read package.json or requirements.txt or go.mod
   → Extract dependencies

2. Glob for framework-specific files:
   - React: **/*.jsx, **/*.tsx, package.json with "react"
   - Vue: **/*.vue, package.json with "vue"
   - Next.js: next.config.js, app/**, pages/**
   - FastAPI: **/main.py with "from fastapi"
   - Django: **/settings.py, **/models.py

3. Analyze imports/dependencies:
   - TypeScript: tsconfig.json
   - GraphQL: **/*.graphql, **/*.gql
   - Docker: Dockerfile, docker-compose.yml
   - Kubernetes: **/*.yaml in k8s/ or manifests/

4. Generate contextual items based on detected stack
5. Mark all generated items with [AI-GENERATED]
```

## Example: TypeScript + React + API Project

**Input Context:**

- `package.json` contains: "react": "^18.0.0", "typescript": "^5.0.0"
- Files include: `src/components/*.tsx`, `src/api/*.ts`

**Generated Checklist:**

```markdown
# Quality Checklist

Generated: 2026-01-28 10:30:00
Context: TypeScript, React, REST API

## Code Quality (IEEE 1028)

- [ ] Code follows project style guide
- [ ] No code duplication
- [ ] Cyclomatic complexity < 10
- [ ] Functions have single responsibility
- [ ] Variable names clear and descriptive
- [ ] Magic numbers replaced with constants
- [ ] Dead code removed

## Testing (IEEE 1028)

- [ ] Tests written first (TDD)
- [ ] All new code has tests
- [ ] Tests cover edge cases
- [ ] Test coverage ≥ 80%
- [ ] Integration tests present
- [ ] Tests isolated (no order dependency)

## Security (IEEE 1028)

- [ ] Input validation on all inputs
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities
- [ ] Sensitive data encrypted
- [ ] Auth/authz checks present
- [ ] No hardcoded secrets
- [ ] OWASP Top 10 reviewed

## Performance (IEEE 1028)

- [ ] No performance bottlenecks
- [ ] Database queries optimized
- [ ] Caching used appropriately
- [ ] Resource cleanup (connections)
- [ ] No infinite loop risks
- [ ] Large data paginated

## Documentation (IEEE 1028)

- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Breaking changes documented

## Error Handling (IEEE 1028)

- [ ] All errors handled
- [ ] User-friendly error messages
- [ ] Detailed logs for debugging
- [ ] No swallowed exceptions
- [ ] Graceful degradation
- [ ] Rollback procedures

## TypeScript (AI-Generated)

- [ ] [AI-GENERATED] Types exported from modules
- [ ] [AI-GENERATED] No `any` types (justified if used)
- [ ] [AI-GENERATED] Strict null checks satisfied
- [ ] [AI-GENERATED] Interfaces prefer over types

## React (AI-GENERATED)

- [ ] [AI-GENERATED] Components use React.memo appropriately
- [ ] [AI-GENERATED] Hooks follow Rules of Hooks
- [ ] [AI-GENERATED] No unnecessary re-renders
- [ ] [AI-GENERATED] Keys on list items

## REST API (AI-GENERATED)

- [ ] [AI-GENERATED] Rate limiting implemented
- [ ] [AI-GENERATED] API versioning in URLs
- [ ] [AI-GENERATED] Request/response validation
- [ ] [AI-GENERATED] OpenAPI/Swagger updated

---

**Total Items**: 38
**IEEE Base**: 30 (79%)
**Contextual**: 8 (21%)
```

## Best Practices

### DO

- Start with IEEE 1028 base (universal quality)
- Analyze project context before generating
- Mark all LLM items with [AI-GENERATED]
- Keep contextual items focused (10-20%)
- Return actionable checklist (not generic advice)

### DON'T

- Generate checklist without context analysis
- Exceed 20% contextual items (dilutes IEEE base)
- Forget [AI-GENERATED] prefix
- Include items that can't be verified
- Make checklist too long (>50 items)

## Iron Law

```
NO TASK COMPLETION WITHOUT CHECKLIST VALIDATION
```

Use `verification-before-completion` skill to enforce this.

## Related Skills

- `qa-workflow` - Systematic QA validation with fix loops
- `verification-before-completion` - Pre-completion gate
- `tdd` - Test-driven development (testing checklist items)
- `security-architect` - Security-specific validation

## Assigned Agents

This skill is used by:

- `qa` - Quality assurance validation
- `developer` - Pre-completion checks
- `code-reviewer` - Code review criteria

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

Check for:

- Previously generated checklists
- Project-specific quality patterns
- Common quality issues in this codebase

**After completing:**

- New checklist pattern → `.claude/context/memory/learnings.md`
- Quality issue found → `.claude/context/memory/issues.md`
- Context detection improvement → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
