---
name: feature-build
description: End-to-end feature development - plan, implement, test, review. Use when building new features.
allowed-tools: Bash(git:*), Bash(npm:*), Read, Write, Edit, Glob, Grep, Task, EnterPlanMode
model: opus
---

# Feature Build Pipeline

Complete feature development workflow from planning to PR-ready code.

## Pipeline Stages

### 1. Planning Phase
Use EnterPlanMode to:
- Understand requirements
- Research existing codebase patterns
- Identify affected files
- Design implementation approach
- Get user approval before coding

### 2. Branch Setup
Create a feature branch:

```bash
git checkout -b feature/[feature-name]
```

### 3. Implementation
Follow project conventions:
- React functional components with hooks
- Tailwind CSS for styling
- Async/await for async operations
- Try/catch error handling
- Proper import ordering

### 4. Testing
Write and run tests:

```bash
# Add test files alongside implementation
# Run tests to verify
npm test
```

Ensure:
- Unit tests for new functions
- Integration tests for API endpoints
- Component tests for React components

### 5. Security Check
Before committing, verify:
- No hardcoded secrets
- Input validation on user data
- Proper authentication checks
- No SQL injection vulnerabilities

### 6. Code Quality
Run linting and fix issues:

```bash
npm run lint
```

### 7. Commit & Push
Create atomic commits with clear messages:

```bash
git add -A
git commit -m "feat: [description]"
git push -u origin feature/[feature-name]
```

### 8. PR Preparation
Generate PR description including:
- Summary of changes
- Test plan
- Screenshots (if UI changes)
- Breaking changes (if any)

## Deliverables
- Working feature code
- Test coverage
- Updated documentation (if needed)
- PR-ready branch
