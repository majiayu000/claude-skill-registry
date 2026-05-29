---
name: epic-hygiene-process
description: Execute systematic code quality tasks following Epic 10 hygiene standards
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for Epic 10 hygiene tasks:
  - Dead code removal and cleanup
  - Architecture compliance fixes
  - Performance optimization projects
  - Technical debt reduction
  - Code quality improvements
  
  Examples:
  "Execute dead code removal using the epic-hygiene-process skill"
  "Perform architecture compliance cleanup using the epic-hygiene-process skill"
  "Run Epic 10 hygiene checklist using the epic-hygiene-process skill"

# Epic Hygiene Process Execution Skill

## Overview

This skill automates systematic code quality tasks following Epic 10 hygiene standards, ensuring consistent, thorough, and well-documented improvements to the Saberloop codebase.

## When to Use This Skill

Use this skill when ALL of these are true:
- [ ] Task is code quality/technical debt related
- [ ] No behavior changes are intended
- [ ] Task follows Epic 10 hygiene standards
- [ ] Existing tests must continue passing
- [ ] Documentation updates are required

### Common Use Cases

- **Dead code removal** - Unused functions, imports, and modules
- **Architecture compliance** - Fixing layer boundary violations
- **Performance optimization** - Cleaning up inefficient patterns
- **Technical debt reduction** - Modernizing legacy code patterns
- **Code standardization** - Updating to current conventions

## Prerequisites

Before starting any hygiene task:

- [ ] Main branch is clean and up to date
- [ ] All tests currently pass
- [ ] Have a worktree directory available for isolation
- [ ] Understand what code will be changed/removed
- [ ] Have rollback plan (git revert capability)

## Setup: Worktree Configuration

### Step 1: Create Hygiene Worktree

```bash
# From main repo directory
git worktree add ../saberloop-hygiene hygiene/[task-name]

cd ../saberloop-hygiene
npm install
```

### Step 2: Verify Environment

```bash
# Confirm you're in hygiene worktree
pwd  # Should show ../saberloop-hygiene

# Confirm branch
git branch  # Should show hygiene/[task-name]

# Install dependencies if needed
npm install

# Run baseline tests
npm test && npm run typecheck && npm run arch:test
```

## Hygiene Task Templates

### Task Type 1: Dead Code Removal

#### Pre-Removal Analysis

```bash
# Find unused exports
npm run lint:dead-code

# Check for orphaned files
git ls-files | xargs grep -l "TODO" | head -10

# Look for console.log/debugging code
grep -r "console.log" src/ --include="*.js" | grep -v node_modules
```

#### Removal Checklist

For each file/module to remove:

- [ ] No imports found in codebase
- [ ] No references in documentation
- [ ] No tests reference the code
- [ ] File is not part of public API
- [ ] Removal doesn't break functionality

#### Removal Process

```bash
# Remove files
git rm path/to/unused-file.js
git rm -r path/to/unused-folder/

# Remove unused exports
# Edit file to remove unused functions/imports

# Remove unused dependencies
npm uninstall package-name
```

### Task Type 2: Architecture Compliance

#### Common Violations

Based on `.dependency-cruiser.cjs` rules:

| Rule | Description | Fix Pattern |
|-------|-------------|--------------|
| `no-view-to-view` | View importing another view | Move logic to service layer |
| `views-should-not-import-db` | Direct database access | Create service method |
| `components-should-not-import-api` | Component calling API | Pass as prop/callback |
| `api-should-not-import-db` | API accessing database | Accept credentials as param |

#### Compliance Fix Template

```javascript
// BEFORE (Violation)
import { saveTopic } from '@/core/db.js'; // View importing DB

export default class QuizView extends BaseView {
  async handleSave() {
    await saveTopic(this.topic); // Direct DB access
  }
}

// AFTER (Compliant)
import { quizService } from '@/services/quiz-service.js'; // Use service layer

export default class QuizView extends BaseView {
  async handleSave() {
    await quizService.saveTopic(this.topic); // Service handles DB
  }
}
```

#### Architecture Validation

```bash
# Check current architecture compliance
npm run arch:test

# Generate dependency graph for visualization
npm run arch:graph

# Convert to image (requires dot)
dot -Tpng dependency-graph.dot -o architecture.png
```

### Task Type 3: Performance Optimization

#### Common Performance Issues

| Issue | Detection | Fix Pattern |
|-------|-------------|--------------|
| Inefficient loops | Code review, profiling | Use built-in methods |
| Memory leaks | Long-running sessions | Proper cleanup |
| Bundle size | Bundle analyzer | Tree shaking, lazy loading |
| Redundant API calls | Telemetry, profiling | Caching, deduplication |

#### Optimization Template

```javascript
// BEFORE (Inefficient)
export function processItems(items) {
  let result = [];
  for (let i = 0; i < items.length; i++) {
    result.push(transform(items[i]));
  }
  return result;
}

// AFTER (Optimized)
export function processItems(items) {
  return items.map(transform); // Built-in, faster
}
```

### Task Type 4: Code Standardization

#### Standardization Patterns

| Area | Old Pattern | New Pattern |
|-------|--------------|--------------|
| Error handling | throw new Error() | Use errorHandler |
| Logging | console.log() | Use logger |
| Async/await | Promise chains | Async/await |
| Imports | Relative paths | Absolute with @/ |

#### Standardization Template

```javascript
// BEFORE (Legacy)
function fetchData() {
  return fetch('/api/data')
    .then(response => response.json())
    .catch(error => {
      console.error('Failed:', error);
      throw new Error('API error');
    });
}

// AFTER (Standardized)
import { logger } from '@/utils/logger.js';
import { handleApiError } from '@/utils/errorHandler.js';

export async function fetchData() {
  try {
    const response = await fetch('/api/data');
    return await response.json();
  } catch (error) {
    logger.error('API fetch failed', { endpoint: '/api/data', error });
    throw new Error(handleApiError(error));
  }
}
```

## Execution Process

### Step 1: Task Planning

```bash
# Create task-specific branch
git checkout -b hygiene/[task-description]

# Create learning notes file
touch docs/learning/epic10_hygiene/PHASE*_TASK_DESCRIPTION_NOTES.md
```

### Step 2: Implementation

#### Work in Small, Atomic Changes

```bash
# Make one logical change
# Test it works
git add .
git commit -m "type(scope): description"

# Repeat for each change
```

#### Commit Message Format for Hygiene

```bash
# Prefixes:
refactor(hygiene): Code refactoring without behavior change
test(hygiene): Test updates for hygiene task
docs(hygiene): Documentation updates
chore(hygiene): Build/config changes
perf(hygiene): Performance improvements

# Examples:
refactor(hygiene): remove unused utility functions
test(hygiene): update tests after dead code removal
docs(hygiene): document architecture compliance fixes
perf(hygiene): optimize data processing functions
```

### Step 3: Quality Validation

After each logical change, run:

```bash
# Unit tests
npm test

# Type checking
npm run typecheck

# Architecture validation
npm run arch:test

# Dead code detection
npm run lint:dead-code

# E2E tests (if UI changes)
npm run test:e2e
```

### Step 4: Mutation Testing

For critical code changes:

```bash
# Run mutation testing on affected files
npx stryker run --mutate "src/core/state.js"

# Target: >75% mutation score
```

### Step 5: Documentation Updates

#### Learning Notes Template

**File:** `docs/learning/epic10_hygiene/PHASE*_TASK_NOTES.md`

```markdown
# Task: [Task Description]

**Date:** YYYY-MM-DD
**Type:** [dead-code-removal|architecture-compliance|performance|standardization]
**Effort:** X sessions

## Objective
Brief description of what the task accomplished.

## What Was Changed
- [ ] Files removed: [list]
- [ ] Files modified: [list]
- [ ] Dependencies removed: [list]
- [ ] Tests updated: [list]

## Problems Encountered
1. **Problem**: Description
   **Solution**: How solved
   **Learning**: What to avoid in future

## Results
- Lines of code removed: [number]
- Mutation score improvement: [before] → [after]
- Architecture violations fixed: [number]
- Test coverage impact: [before] → [after]

## Process Improvements
- What worked well
- What could be improved
- Tools or scripts that would help next time

## Before/After Metrics
| Metric | Before | After |
|--------|--------|--------|
| Bundle size | X kb | Y kb |
| Test coverage | X% | Y% |
| Mutation score | X% | Y% |
| Architecture violations | X | Y |
```

#### Update Epic Documentation

Update `docs/learning/epic10_hygiene/EPIC10_HYGIENE_PLAN.md`:

```markdown
### Completed Tasks

| Task | Completed | Document |
|------|-----------|----------|
| [Task Description] | YYYY-MM-DD | [PHASE*_TASK_NOTES.md](./PHASE*_TASK_NOTES.md) |
```

### Step 6: Final Validation

```bash
# Complete test suite
npm test -- --run

# Full architecture check
npm run arch:test

# Type checking
npm run typecheck

# Dead code check (should find none new)
npm run lint:dead-code

# Build verification
npm run build
```

## Common Hygiene Tasks

### Task: Remove Unused Dependencies

```bash
# Find unused dependencies
npm ls | grep "unused"

# Remove unused dependency
npm uninstall package-name

# Update package-lock.json
npm install
```

### Task: Clean Up Imports

```javascript
// BEFORE (Mixed imports)
import { func1 } from './utils.js';
import something from 'external-lib';
import { func2 } from './utils.js';

// AFTER (Grouped imports)
import { func1, func2 } from './utils.js';
import something from 'external-lib';
```

### Task: Standardize Error Handling

```javascript
// BEFORE (Inconsistent)
if (error) {
  console.log('Error:', error.message);
  return null;
}

// AFTER (Standardized)
if (error) {
  logger.error('Operation failed', { error: error.message });
  return null;
}
```

### Task: Remove Debugging Code

```bash
# Find debugging statements
grep -r "console.log\|debugger\|alert" src/ --include="*.js"

# Remove them (be careful!)
# Verify no functionality is lost
```

## Quality Gates

Before any hygiene task can be considered complete:

### Functional Requirements
- [ ] All existing tests pass without modification
- [ ] No behavior changes (verify manually)
- [ ] Application builds successfully
- [ ] No new console errors or warnings

### Quality Requirements
- [ ] Code follows project style guidelines
- [ ] Architecture rules pass (`npm run arch:test`)
- [ ] Type checking passes (`npm run typecheck`)
- [ ] No new dead code introduced
- [ ] Mutation score maintained or improved

### Documentation Requirements
- [ ] Learning notes created with metrics
- [ ] Epic documentation updated
- [ ] Commit history is clean and descriptive
- [ ] Before/after metrics documented

### Process Requirements
- [ ] Worktree was used for isolation
- [ ] Changes were made in atomic commits
- [ ] Branch follows naming convention
- [ ] Proper commit message prefixes used

## Rollback Procedures

If something goes wrong:

```bash
# Emergency rollback (if worktree still exists)
cd ../saberloop-hygiene
git reset --hard HEAD~1  # Undo last commit

# Full rollback (if merged to main)
cd ../demo-pwa-app  # Main repo
git revert main  # Creates revert commit
git push origin main  # Push revert
```

## Integration with Other Skills

This skill integrates with:
- **feature-flag-management** - When removing flags during hygiene
- **testing-suite-management** - For test validation
- **architecture-compliance** - For validation and fixes

## Performance Considerations

### Task Time Estimates

| Task Type | Complexity | Estimated Time |
|------------|-------------|----------------|
| Dead code removal | Low | 1-2 hours |
| Architecture compliance | Medium | 2-4 hours |
| Performance optimization | High | 4-8 hours |
| Code standardization | Medium | 2-6 hours |

### Batch Processing

For multiple hygiene tasks:

```bash
# Process in logical order
1. Dead code removal (cleanest slate)
2. Architecture compliance (structural)
3. Performance optimization (last)
4. Code standardization (final polish)
```

## Troubleshooting

### Tests Fail After Changes

1. **Check what functionality was affected**
2. **Review git diff for unintended changes**
3. **Run specific failing test with --run**
4. **Check if test implementation was wrong**

### Architecture Rules Still Failing

1. **Review dependency-cruiser output**
2. **Check import paths (use @/ alias)**
3. **Verify layer boundaries**
4. **Look for circular dependencies**

### Worktree Issues

1. **Ensure worktree is properly created**
2. **Check you're in correct directory**
3. **Verify branch name matches expectation**
4. **Clean up worktrees if corrupted**

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+