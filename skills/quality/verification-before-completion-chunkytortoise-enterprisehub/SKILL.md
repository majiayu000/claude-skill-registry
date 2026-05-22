---
name: Verification Before Completion
description: This skill should be used when the user asks to "verify the implementation", "check before finishing", "quality gates", "pre-completion validation", "verify before deploy", or needs comprehensive quality validation before marking work as complete.
version: 1.0.0
---

# Verification Before Completion: Quality Gates

## Overview

Verification Before Completion implements comprehensive quality gates to ensure work meets standards before being marked as complete. This systematic approach prevents issues from reaching production and maintains high code quality standards.

## The 5-Gate Verification Process

### Gate 1: FUNCTIONAL - Feature Works as Specified

Verify that the implementation meets all functional requirements.

**Validation Criteria:**
- All acceptance criteria are met
- Core functionality works in happy path scenarios
- Edge cases are handled appropriately
- Error conditions are managed gracefully

**Verification Steps:**
```bash
# Manual testing
./scripts/test-functionality.sh

# Automated testing
npm test
python -m pytest

# Integration testing
./scripts/integration-tests.sh
```

### Gate 2: TECHNICAL - Code Quality and Architecture

Ensure code adheres to quality standards and architectural principles.

**Code Quality Checklist:**
- [ ] SOLID principles applied
- [ ] DRY (Don't Repeat Yourself) violations addressed
- [ ] Clear and descriptive naming
- [ ] Proper error handling
- [ ] No hardcoded values
- [ ] Security best practices followed

**Architecture Validation:**
- [ ] Follows established patterns
- [ ] Proper separation of concerns
- [ ] Maintainable and extensible design
- [ ] Performance considerations addressed

### Gate 3: TESTING - Comprehensive Test Coverage

Validate that all code paths are tested and tests are meaningful.

**Coverage Requirements:**
- **Lines:** ≥80%
- **Branches:** ≥80%
- **Functions:** ≥90%
- **New code:** 100%

**Test Quality:**
- [ ] Unit tests for business logic
- [ ] Integration tests for component interactions
- [ ] Edge case testing
- [ ] Error condition testing
- [ ] Performance tests where applicable

### Gate 4: SECURITY - Vulnerability Assessment

Ensure implementation is secure and follows security best practices.

**Security Checklist:**
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS protection applied
- [ ] Authentication/authorization checked
- [ ] Secrets management verified
- [ ] Dependencies scanned for vulnerabilities

### Gate 5: DEPLOYMENT - Production Readiness

Verify the code is ready for production deployment.

**Deployment Readiness:**
- [ ] Environment configuration validated
- [ ] Database migrations tested
- [ ] Rollback procedures defined
- [ ] Monitoring and logging implemented
- [ ] Documentation updated
- [ ] Change management followed

## Automated Quality Gates

### Pre-Commit Gates

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit quality gates..."

# Gate 1: Code formatting
echo "🔍 Checking code formatting..."
if ! npx prettier --check .; then
    echo "❌ Code formatting failed"
    exit 1
fi

# Gate 2: Linting
echo "🔍 Running linter..."
if ! npx eslint src/ --max-warnings 0; then
    echo "❌ Linting failed"
    exit 1
fi

# Gate 3: Type checking
echo "🔍 Type checking..."
if ! npx tsc --noEmit; then
    echo "❌ Type checking failed"
    exit 1
fi

# Gate 4: Unit tests
echo "🔍 Running unit tests..."
if ! npm test; then
    echo "❌ Unit tests failed"
    exit 1
fi

echo "✅ All pre-commit gates passed!"
```

### CI/CD Pipeline Gates

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality-gates:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    # Gate 1: Dependencies
    - name: Install dependencies
      run: npm ci

    # Gate 2: Code quality
    - name: Run ESLint
      run: npx eslint src/ --max-warnings 0

    - name: Check formatting
      run: npx prettier --check .

    # Gate 3: Type safety
    - name: Type check
      run: npx tsc --noEmit

    # Gate 4: Testing
    - name: Run tests with coverage
      run: npm run test:coverage

    # Gate 5: Security scan
    - name: Run security audit
      run: npm audit --audit-level high

    # Gate 6: Build verification
    - name: Build application
      run: npm run build
```

## Language-Specific Verification

### Python Quality Gates

```python
# scripts/python-quality-gates.py
import subprocess
import sys
from typing import List, Dict, Any

class PythonQualityGates:
    def __init__(self, src_dir: str = "src", test_dir: str = "tests"):
        self.src_dir = src_dir
        self.test_dir = test_dir
        self.results: Dict[str, Any] = {}

    def run_gate(self, name: str, command: List[str]) -> bool:
        """Run a quality gate command and record results"""
        print(f"🔍 Running {name}...")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            self.results[name] = {"status": "passed", "output": result.stdout}
            print(f"✅ {name} passed")
            return True
        except subprocess.CalledProcessError as e:
            self.results[name] = {
                "status": "failed",
                "output": e.stdout,
                "error": e.stderr
            }
            print(f"❌ {name} failed")
            print(e.stderr)
            return False

    def check_formatting(self) -> bool:
        """Verify code formatting with black"""
        return self.run_gate("Code Formatting", [
            "black", "--check", "--diff", self.src_dir, self.test_dir
        ])

    def check_imports(self) -> bool:
        """Verify import sorting with isort"""
        return self.run_gate("Import Sorting", [
            "isort", "--check-only", "--diff", self.src_dir, self.test_dir
        ])

    def check_linting(self) -> bool:
        """Run flake8 linting"""
        return self.run_gate("Linting", [
            "flake8", self.src_dir, self.test_dir
        ])

    def check_type_hints(self) -> bool:
        """Run mypy type checking"""
        return self.run_gate("Type Checking", [
            "mypy", self.src_dir
        ])

    def check_tests(self) -> bool:
        """Run tests with coverage"""
        return self.run_gate("Tests with Coverage", [
            "pytest", "--cov=" + self.src_dir, "--cov-report=term-missing",
            "--cov-fail-under=80", self.test_dir
        ])

    def check_security(self) -> bool:
        """Run security checks with bandit"""
        return self.run_gate("Security Scan", [
            "bandit", "-r", self.src_dir
        ])

    def run_all_gates(self) -> bool:
        """Run all quality gates"""
        gates = [
            self.check_formatting,
            self.check_imports,
            self.check_linting,
            self.check_type_hints,
            self.check_tests,
            self.check_security
        ]

        all_passed = True
        for gate in gates:
            if not gate():
                all_passed = False

        return all_passed

if __name__ == "__main__":
    gates = PythonQualityGates()

    if gates.run_all_gates():
        print("\n🎉 All quality gates passed!")
        sys.exit(0)
    else:
        print("\n💥 Some quality gates failed!")
        sys.exit(1)
```

### TypeScript/JavaScript Quality Gates

```typescript
// scripts/quality-gates.ts
import { execSync } from 'child_process';
import { existsSync } from 'fs';

interface GateResult {
  name: string;
  passed: boolean;
  output?: string;
  error?: string;
}

class TypeScriptQualityGates {
  private results: GateResult[] = [];

  private runCommand(name: string, command: string): boolean {
    console.log(`🔍 Running ${name}...`);

    try {
      const output = execSync(command, { encoding: 'utf-8' });
      this.results.push({
        name,
        passed: true,
        output
      });
      console.log(`✅ ${name} passed`);
      return true;
    } catch (error: any) {
      this.results.push({
        name,
        passed: false,
        error: error.message
      });
      console.log(`❌ ${name} failed`);
      console.log(error.message);
      return false;
    }
  }

  checkFormatting(): boolean {
    return this.runCommand(
      'Code Formatting',
      'npx prettier --check .'
    );
  }

  checkLinting(): boolean {
    return this.runCommand(
      'ESLint',
      'npx eslint src/ tests/ --max-warnings 0'
    );
  }

  checkTypeScript(): boolean {
    return this.runCommand(
      'TypeScript Compilation',
      'npx tsc --noEmit'
    );
  }

  checkTests(): boolean {
    return this.runCommand(
      'Jest Tests with Coverage',
      'npm test -- --coverage --watchAll=false'
    );
  }

  checkBuild(): boolean {
    return this.runCommand(
      'Production Build',
      'npm run build'
    );
  }

  checkSecurity(): boolean {
    return this.runCommand(
      'Security Audit',
      'npm audit --audit-level high'
    );
  }

  runAllGates(): boolean {
    const gates = [
      () => this.checkFormatting(),
      () => this.checkLinting(),
      () => this.checkTypeScript(),
      () => this.checkTests(),
      () => this.checkBuild(),
      () => this.checkSecurity()
    ];

    let allPassed = true;
    for (const gate of gates) {
      if (!gate()) {
        allPassed = false;
      }
    }

    return allPassed;
  }

  getResults(): GateResult[] {
    return this.results;
  }
}

// CLI execution
if (require.main === module) {
  const gates = new TypeScriptQualityGates();

  if (gates.runAllGates()) {
    console.log('\n🎉 All quality gates passed!');
    process.exit(0);
  } else {
    console.log('\n💥 Some quality gates failed!');
    process.exit(1);
  }
}
```

## Quality Gate Checklists

### Pre-Implementation Checklist

**Requirements Validation:**
- [ ] Acceptance criteria are clear and testable
- [ ] Edge cases identified
- [ ] Performance requirements defined
- [ ] Security considerations documented
- [ ] Error handling strategy planned

### During Implementation Checklist

**Code Quality (Continuous):**
- [ ] Follow established coding standards
- [ ] Write tests alongside implementation
- [ ] Keep functions/methods small and focused
- [ ] Use descriptive variable and function names
- [ ] Handle errors appropriately

### Pre-Commit Checklist

**Local Validation:**
- [ ] Code compiles/runs without errors
- [ ] All tests pass locally
- [ ] Code formatting applied
- [ ] No debugging code left in
- [ ] Documentation updated

### Pre-Review Checklist

**Review Preparation:**
- [ ] Self-review completed
- [ ] Meaningful commit messages
- [ ] PR description explains changes
- [ ] Screenshots/demos included if applicable
- [ ] Breaking changes documented

### Pre-Deployment Checklist

**Production Readiness:**
- [ ] Feature flags configured
- [ ] Database migrations tested
- [ ] Environment variables updated
- [ ] Monitoring alerts configured
- [ ] Rollback plan defined

## Verification Scripts

### Comprehensive Quality Gate Script

```bash
#!/bin/bash
# scripts/verify-completion.sh

# Comprehensive verification script
set -e

PROJECT_TYPE=""
COVERAGE_THRESHOLD=80
SKIP_SECURITY=false
VERBOSE=false

# Detect project type
detect_project_type() {
    if [[ -f "package.json" ]]; then
        PROJECT_TYPE="javascript"
    elif [[ -f "pyproject.toml" || -f "requirements.txt" ]]; then
        PROJECT_TYPE="python"
    else
        echo "❌ Unknown project type"
        exit 1
    fi
}

# Run verification for JavaScript/TypeScript
verify_javascript() {
    echo "🔍 Verifying JavaScript/TypeScript project..."

    # Gate 1: Dependencies
    echo "Gate 1: Checking dependencies..."
    npm ci

    # Gate 2: Code quality
    echo "Gate 2: Code quality checks..."
    npx prettier --check .
    npx eslint src/ --max-warnings 0

    # Gate 3: Type checking
    echo "Gate 3: Type checking..."
    if [[ -f "tsconfig.json" ]]; then
        npx tsc --noEmit
    fi

    # Gate 4: Tests
    echo "Gate 4: Running tests..."
    npm test -- --coverage --watchAll=false

    # Gate 5: Build
    echo "Gate 5: Building..."
    npm run build

    # Gate 6: Security (optional)
    if [[ $SKIP_SECURITY == false ]]; then
        echo "Gate 6: Security audit..."
        npm audit --audit-level moderate
    fi
}

# Run verification for Python
verify_python() {
    echo "🔍 Verifying Python project..."

    # Gate 1: Dependencies
    echo "Gate 1: Installing dependencies..."
    pip install -r requirements.txt

    # Gate 2: Code quality
    echo "Gate 2: Code quality checks..."
    black --check src/ tests/
    isort --check-only src/ tests/
    flake8 src/ tests/

    # Gate 3: Type checking
    echo "Gate 3: Type checking..."
    mypy src/

    # Gate 4: Tests
    echo "Gate 4: Running tests..."
    pytest --cov=src --cov-report=term-missing --cov-fail-under=$COVERAGE_THRESHOLD

    # Gate 5: Security (optional)
    if [[ $SKIP_SECURITY == false ]]; then
        echo "Gate 5: Security scan..."
        bandit -r src/
    fi
}

# Main verification
main() {
    echo "🚀 Starting verification before completion..."
    echo "============================================"

    detect_project_type
    echo "Detected project type: $PROJECT_TYPE"

    case $PROJECT_TYPE in
        "javascript")
            verify_javascript
            ;;
        "python")
            verify_python
            ;;
        *)
            echo "❌ Unsupported project type: $PROJECT_TYPE"
            exit 1
            ;;
    esac

    echo ""
    echo "🎉 All verification gates passed!"
    echo "✅ Code is ready for review/deployment"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-security)
            SKIP_SECURITY=true
            shift
            ;;
        --coverage-threshold)
            COVERAGE_THRESHOLD="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
```

## Integration with Development Workflow

### Git Hooks Integration

```bash
# Setup verification as pre-push hook
ln -s ../../scripts/verify-completion.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### IDE Integration

**VS Code Settings:**
```json
{
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true,
        "source.organizeImports": true
    },
    "editor.formatOnSave": true,
    "typescript.preferences.includePackageJsonAutoImports": "off",
    "eslint.run": "onSave",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### Continuous Integration

```yaml
# Quality gates in CI
- name: Quality Gates
  run: |
    ./scripts/verify-completion.sh

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

## Common Quality Issues

### Code Smells to Check

**Long Methods:**
```python
# ❌ Too long and complex
def process_user_data(user_data):
    # 50+ lines of complex logic
    pass

# ✅ Broken down into smaller functions
def process_user_data(user_data):
    validated_data = validate_user_data(user_data)
    normalized_data = normalize_user_data(validated_data)
    return save_user_data(normalized_data)
```

**Magic Numbers:**
```javascript
// ❌ Magic numbers
if (user.age > 18 && user.score > 85) {
    return true;
}

// ✅ Named constants
const MINIMUM_AGE = 18;
const PASSING_SCORE = 85;

if (user.age > MINIMUM_AGE && user.score > PASSING_SCORE) {
    return true;
}
```

### Performance Red Flags

**N+1 Queries:**
```python
# ❌ N+1 query problem
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # Separate query for each user

# ✅ Optimized with select_related
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # Single query
```

## Additional Resources

### Reference Files
For detailed verification patterns and checklists, consult:
- **`references/quality-standards.md`** - Detailed quality standards and metrics
- **`references/security-checklist.md`** - Comprehensive security validation checklist
- **`references/performance-benchmarks.md`** - Performance testing and validation

### Example Files
Working verification examples in `examples/`:
- **`examples/python-verification.py`** - Complete Python verification workflow
- **`examples/javascript-verification.js`** - JavaScript/TypeScript verification
- **`examples/ci-cd-pipeline.yml`** - CI/CD verification pipeline

### Scripts
Verification utility scripts in `scripts/`:
- **`scripts/verify-completion.sh`** - Comprehensive verification script
- **`scripts/quality-report.py`** - Quality metrics reporting
- **`scripts/security-scan.sh`** - Security validation automation

## Success Metrics

### Quality Metrics
- Code coverage percentage
- Linting violations count
- Security vulnerabilities found
- Test pass/fail ratio
- Build success rate

### Process Metrics
- Time to complete verification
- Number of verification failures
- Issues caught before production
- Developer satisfaction with process

Use this systematic verification approach to ensure all work meets quality standards before completion, reducing production issues and maintaining high code quality.