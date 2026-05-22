---
name: quick-pr-review
description: "Universal pre-PR checklist that works in ANY project, with or without MCP tools"
---

# Quick PR Review - Universal Pre-PR Checklist

## 🎯 When to Use This Skill

Use BEFORE creating a pull request in ANY project when:
- Preparing code for review
- Self-reviewing your changes
- Ensuring quality standards
- Reducing review iterations

## ⚡ Quick Start (30 seconds)

### With MCP Tools:
```
"Run quick PR review on my staged changes"
```

### Without MCP Tools:
```bash
# Quick self-review checklist
git diff --staged            # Review changes
npm test                      # Run tests
npm run lint                  # Check linting
git grep "TODO\|FIXME\|XXX"  # Find unfinished work
```

## 📋 Universal PR Checklist

### 1. Code Changes Review

#### WITH MCP (Smart Reviewer):
```
"Review my staged files for quality issues"
```

#### WITHOUT MCP:
```bash
# Self-review questions:
# □ Do variable names clearly express intent?
# □ Are functions focused on a single responsibility?
# □ Is error handling comprehensive?
# □ Are there magic numbers that should be constants?
# □ Is the code DRY (Don't Repeat Yourself)?

# Find code smells:
git diff --staged | grep -E "console\.|debugger|TODO|FIXME"
```

### 2. Test Coverage Check

#### WITH MCP (Test Generator):
```
"Check test coverage and generate missing tests"
```

#### WITHOUT MCP:
```bash
# Check coverage (adjust for your test runner)
npm test -- --coverage        # Jest/Vitest
pytest --cov                  # Python
go test -cover                 # Go
mvn test jacoco:report         # Java

# Quick test checklist:
# □ All new functions have tests?
# □ Edge cases covered?
# □ Error scenarios tested?
# □ Integration points verified?
```

### 3. Security Scan

#### WITH MCP (Security Scanner):
```
"Scan my changes for security vulnerabilities"
```

#### WITHOUT MCP:
```bash
# Security checklist:
# □ No hardcoded secrets/keys?
# □ Input validation present?
# □ SQL queries parameterized?
# □ File paths sanitized?
# □ Dependencies up to date?

# Quick scans:
git diff --staged | grep -iE "password|secret|token|api[_-]key"
grep -r "eval\|exec\|innerHTML" --include="*.js" --include="*.ts"
npm audit  # or: pip check, go mod tidy, etc.
```

### 4. Documentation Check

#### WITH MCP (Doc Generator):
```
"Check if my changes need documentation updates"
```

#### WITHOUT MCP:
```bash
# Documentation checklist:
# □ README updated if needed?
# □ API changes documented?
# □ Breaking changes noted?
# □ Examples still accurate?
# □ Changelog entry added?

# Find undocumented functions:
grep -B2 "function\|class\|def" --include="*.js" | grep -v "//"
```

### 5. Performance Check

#### WITH MCP (Architecture Analyzer):
```
"Check for performance issues in my changes"
```

#### WITHOUT MCP:
```bash
# Performance checklist:
# □ No N+1 queries?
# □ Appropriate caching used?
# □ Large loops optimized?
# □ Unnecessary re-renders avoided?
# □ Database queries indexed?

# Find potential issues:
git diff --staged | grep -E "forEach.*forEach|for.*for"  # Nested loops
git diff --staged | grep -E "await.*map|Promise\.all"    # Async patterns
```

## 🚀 Complete Workflow

### Optimal Flow (2-3 minutes):

1. **Stage your changes:**
   ```bash
   git add -p  # Stage selectively
   ```

2. **Run the appropriate checklist:**
   - WITH MCP: `"Run complete PR review checklist"`
   - WITHOUT: Use the manual checklist above

3. **Fix issues found:**
   ```bash
   # Fix issues
   git add -p  # Stage fixes
   ```

4. **Final verification:**
   ```bash
   git diff --staged --stat  # Review scope
   git log --oneline -5      # Check commit context
   ```

5. **Create PR with confidence!**

## 💡 Pro Tips

### Universal Commit Message Check:
```bash
# Ensure good commit messages
git log --oneline -10  # Are they clear and consistent?

# Conventional commits pattern:
# type(scope): description
# Example: feat(auth): add password reset
```

### Quick Scope Check:
```bash
# Is this PR doing too much?
git diff --staged --stat
# If > 500 lines or > 20 files, consider splitting
```

### Dependency Impact:
```bash
# Check what you're affecting
git diff --staged package.json Gemfile go.mod requirements.txt pom.xml
```

## 🎯 Success Metrics

Your PR is ready when:
- ✅ All tests pass
- ✅ No linting errors
- ✅ Security checklist complete
- ✅ Documentation updated
- ✅ Changes focused and clear
- ✅ Commit messages descriptive

## 🔄 Quick Recovery

If you find issues:
```bash
# Unstage everything
git reset HEAD

# Fix issues
# ...

# Restage carefully
git add -p
```

## 📝 Notes

- This workflow is **language-agnostic**
- Adapt commands to your tech stack
- MCP tools speed up the process 10x
- Manual approach ensures you can work anywhere

Remember: A good PR review saves everyone time!