---
name: codebase-improvement-planner
description: Analyze codebase and generate comprehensive improvement plans with prioritized recommendations
auto-load: false
user-invocable: true
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Task
model: opus
---

# Codebase Improvement Planner

Session: ${CLAUDE_SESSION_ID}
Task List: ${CLAUDE_CODE_TASK_LIST_ID}

## Purpose
Comprehensive codebase analysis and improvement planning with actionable recommendations.

---

## Phase 1: Discovery & Analysis

### 1.1 Project Structure Mapping
```bash
# Get project overview
echo "=== PROJECT STRUCTURE ==="
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) | head -100

# Count files by type
echo "=== FILE COUNTS ==="
for ext in ts tsx js jsx py go rs java; do
  count=$(find . -type f -name "*.$ext" 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "$ext: $count files"
done

# Check for configuration files
echo "=== CONFIG FILES ==="
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null || echo "No standard config found"
```

### 1.2 Dependency Analysis
```bash
# Node.js dependencies
[ -f package.json ] && echo "=== NPM DEPENDENCIES ===" && cat package.json | grep -A 100 '"dependencies"' | head -50

# Python dependencies
[ -f requirements.txt ] && echo "=== PIP REQUIREMENTS ===" && cat requirements.txt
[ -f pyproject.toml ] && echo "=== PYPROJECT ===" && cat pyproject.toml

# Outdated checks
[ -f package.json ] && npm outdated 2>/dev/null || true
```

### 1.3 Code Quality Indicators
```bash
# TODO/FIXME/HACK comments
echo "=== TECHNICAL DEBT MARKERS ==="
grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|DEPRECATED" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" . 2>/dev/null | head -50

# Large files (potential refactoring candidates)
echo "=== LARGE FILES (>500 lines) ==="
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \) -exec wc -l {} \; 2>/dev/null | awk '$1 > 500 {print}' | sort -rn | head -20

# Complex functions (high cyclomatic complexity indicators)
echo "=== POTENTIAL COMPLEXITY ISSUES ==="
grep -rn "if.*if.*if\|&&.*&&.*&&\|||.*||.*||" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" . 2>/dev/null | head -20
```

---

## Phase 2: Parallel Deep Analysis

Launch specialized analysis agents:

### Agent 1: Security Scanner
```
Analyze for:
- Hardcoded secrets/credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- Missing input validation
- Exposed sensitive data in logs
```

### Agent 2: Performance Analyzer
```
Identify:
- N+1 query patterns
- Synchronous blocking operations
- Memory leak indicators
- Inefficient algorithms (O(n²) or worse)
- Missing caching opportunities
- Large bundle sizes
```

### Agent 3: Test Coverage Auditor
```
Assess:
- Test file coverage
- Missing test scenarios
- Test quality (assertions per test)
- Integration vs unit test ratio
- Mock usage patterns
```

### Agent 4: Architecture Reviewer
```
Evaluate:
- SOLID principle adherence
- Separation of concerns
- Dependency injection usage
- Module coupling/cohesion
- API design consistency
- Error handling patterns
```

### Agent 5: Documentation Checker
```
Review:
- README completeness
- API documentation
- Code comments quality
- Changelog maintenance
- Architecture decision records
```

---

## Phase 3: Issue Classification

### Priority Matrix

| Priority | Criteria | Example Issues |
|----------|----------|----------------|
| P0 Critical | Security vulnerabilities, data loss risk, production blockers | Exposed credentials, SQL injection |
| P1 High | Major tech debt, significant performance issues | Missing tests for critical paths, O(n²) algorithms |
| P2 Medium | Code quality issues, maintenance burden | Code duplication, inconsistent patterns |
| P3 Low | Minor improvements, nice-to-have | Documentation gaps, minor style issues |

### Issue Template
```yaml
issue:
  id: "IMP-001"
  title: ""
  priority: "P0|P1|P2|P3"
  category: "security|performance|quality|testing|architecture|documentation"
  location:
    file: ""
    line_start: 0
    line_end: 0
  description: ""
  impact: ""
  recommendation: ""
  effort_estimate: "S|M|L|XL"
  dependencies: []
```

---

## Phase 4: Improvement Roadmap Generation

### Roadmap Structure
```yaml
improvement_roadmap:
  sprint_1_critical:
    duration: "1-2 weeks"
    focus: "Security & Stability"
    tasks:
      - id: "IMP-001"
        title: ""
        assignee_type: "senior_developer"
        
  sprint_2_foundation:
    duration: "2-3 weeks"
    focus: "Testing & Architecture"
    tasks: []
    
  sprint_3_optimization:
    duration: "2-3 weeks"
    focus: "Performance & Quality"
    tasks: []
    
  sprint_4_polish:
    duration: "1-2 weeks"
    focus: "Documentation & Cleanup"
    tasks: []
```

---

## Phase 5: Execution Guidelines

### For Each Improvement Task:

1. **Preparation**
   - Create feature branch: `improvement/IMP-XXX-description`
   - Review related code
   - Identify test requirements

2. **Implementation**
   - Follow TDD approach
   - Make atomic commits
   - Document changes

3. **Validation**
   - Run full test suite
   - Performance benchmarks (if applicable)
   - Security scan (if applicable)

4. **Review**
   - Self-review with code-reviewer agent
   - Update documentation
   - Create PR with detailed description

5. **Merge**
   - Squash commits if needed
   - Update CHANGELOG
   - Close related issues

---

## Output Format

Generate report as:
```
.claude/reports/
├── improvement-analysis-${CLAUDE_SESSION_ID}.md
├── security-findings-${CLAUDE_SESSION_ID}.json
├── performance-recommendations-${CLAUDE_SESSION_ID}.json
└── roadmap-${CLAUDE_SESSION_ID}.yaml
```

---

## Invocation

To use this skill:
1. Navigate to project root
2. Run: `Analyze this codebase and create an improvement plan`
3. Review generated reports in `.claude/reports/`
4. Execute improvements using task list: `CLAUDE_CODE_TASK_LIST_ID=improvement-${PROJECT_NAME}`
