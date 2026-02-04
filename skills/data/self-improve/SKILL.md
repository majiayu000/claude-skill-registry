---
name: self-improve
description: Automatically improve and fix bugs in the oh-my-gemini project itself
triggers:
  - "self-improve"
  - "자기개선"
  - "자가발전"
  - "auto-fix"
  - "자동수정"
  - "self-heal"
---

# Self-Improve Skill

Automatically detect, analyze, and fix issues in the oh-my-gemini project itself using multi-agent orchestration.

## Purpose

Enable oh-my-gemini to improve itself through:
- Automated bug detection and fixing
- Code quality improvements
- Test coverage enhancement
- Performance optimization
- Documentation updates

## Workflow

### Phase 1: Detection

1. **Run Diagnostics**
   - Execute `npm test` to find failing tests
   - Run `npm run lint` to find linting errors
   - Run `npm run build` to find compilation errors
   - Check TypeScript errors with `lsp_diagnostics`

2. **Code Analysis**
   - Use `lsp_diagnostics` to find type errors
   - Use `ast_grep` to find code patterns that need improvement
   - Use `grep` to find TODO/FIXME comments
   - Check for deprecated patterns

3. **Dependency Check**
   - Run `npm outdated` to find outdated dependencies
   - Check for security vulnerabilities with `npm audit`

### Phase 2: Prioritization

Create a prioritized list of issues:
1. **Critical**: Build failures, test failures, type errors
2. **High**: Linting errors, security vulnerabilities
3. **Medium**: Code quality issues, deprecated patterns
4. **Low**: Documentation, minor improvements

### Phase 3: Fixing

For each issue:

1. **Analyze the Problem**
   - Use `Read` to examine relevant files
   - Use `lsp_definition` to understand code structure
   - Use `lsp_references` to find all usages

2. **Create Fix Plan**
   - Break down into atomic tasks
   - Use `TodoWrite` to track progress

3. **Implement Fix**
   - Use `Edit` to make changes
   - Follow existing code patterns
   - Ensure type safety

4. **Verify Fix**
   - Run `lsp_diagnostics` on changed files
   - Run `npm run build` to verify compilation
   - Run `npm test` to verify tests pass
   - Check for regressions

### Phase 4: Continuous Improvement

1. **Code Quality**
   - Refactor complex functions
   - Improve type safety
   - Add missing error handling
   - Improve documentation

2. **Test Coverage**
   - Identify untested code paths
   - Add missing test cases
   - Improve test quality

3. **Performance**
   - Identify performance bottlenecks
   - Optimize slow operations
   - Reduce bundle size

4. **Documentation**
   - Update outdated docs
   - Add missing examples
   - Improve clarity

## Agent Delegation

Delegate tasks to specialized agents:

- **architect**: For architectural decisions and complex refactoring
- **executor**: For implementation tasks
- **code-reviewer**: For code quality review
- **tester**: For test-related tasks
- **writer**: For documentation updates

## Example Usage

```
> self-improve: Find and fix all TypeScript errors
> 자가발전: 모든 버그를 찾아서 수정해줘
> auto-fix: 린트 에러와 타입 에러를 모두 수정해줘
```

## Safety Measures

1. **Backup Before Changes**
   - Create git commit before major changes
   - Use git stash for experimental changes

2. **Incremental Changes**
   - Fix one issue at a time
   - Verify each fix before proceeding

3. **No Breaking Changes**
   - Maintain backward compatibility
   - Update tests for any API changes

4. **Review Before Commit**
   - Show changes before committing
   - Get user approval for major changes

## Configuration

Can be configured via `.gemini-cli/GEMINI.md`:

```markdown
## Self-Improve Settings

- Auto-fix: true
- Auto-commit: false (requires approval)
- Test-before-commit: true
- Max-changes-per-run: 10
```

