---
name: legacy-code-summarizer
description: Produces comprehensive summaries and insights about legacy codebases to help understand unfamiliar code. Use when onboarding to a new project, planning refactoring efforts, assessing code for acquisition/migration, or generating documentation for undocumented systems. Analyzes architecture, dependencies, code quality issues, and test coverage. Creates high-level overviews with architecture diagrams, key components, entry points, and actionable insights for understanding and improving legacy code.
---

# Legacy Code Summarizer

Analyze and summarize legacy codebases to quickly understand their structure, quality, and improvement opportunities.

## Core Capabilities

This skill helps understand legacy code by:

1. **Mapping architecture** - Identify key components, layers, and relationships
2. **Analyzing dependencies** - Understand module coupling and import patterns
3. **Detecting quality issues** - Find code smells, technical debt, and outdated patterns
4. **Assessing test coverage** - Identify testing gaps and untested code
5. **Generating documentation** - Create actionable summaries for teams

## Code Analysis Workflow

### Step 1: Survey the Codebase

Get an overview of the project structure and size.

**Initial Questions:**
- What programming language(s)?
- What is the project structure?
- How large is the codebase?
- What frameworks/libraries are used?
- Is there existing documentation?

**Commands to Run:**

```bash
# Count lines of code
find . -name "*.py" | xargs wc -l | tail -1  # Python
find . -name "*.java" | xargs wc -l | tail -1  # Java

# Count files
find . -name "*.py" | wc -l
find . -name "*.java" | wc -l

# Directory structure
tree -L 3 -I '__pycache__|node_modules|target|build'

# Or without tree command
find . -type d -not -path '*/\.*' | head -20
```

**Identify Project Type:**
- Web application (frontend/backend)
- CLI tool
- Library/framework
- Microservice
- Monolith
- Desktop application

### Step 2: Identify Entry Points

Find where execution starts and main workflows.

**Common Entry Points:**

**Python:**
```bash
# Find main entry points
grep -r "if __name__ == '__main__':" --include="*.py"

# Find Flask/Django apps
grep -r "app = Flask\|application = " --include="*.py"
grep -r "INSTALLED_APPS\|MIDDLEWARE" --include="*.py"

# Find CLI entry points (setup.py, pyproject.toml)
grep -A 10 "entry_points\|console_scripts" setup.py pyproject.toml
```

**Java:**
```bash
# Find main methods
grep -r "public static void main" --include="*.java"

# Find Spring Boot applications
grep -r "@SpringBootApplication" --include="*.java"

# Find servlets
grep -r "extends HttpServlet\|@WebServlet" --include="*.java"
```

**JavaScript/TypeScript:**
```bash
# Check package.json for entry points
cat package.json | grep -A 5 "main\|scripts"

# Find Express apps
grep -r "app = express()\|express()" --include="*.js" --include="*.ts"

# Find React entry points
find . -name "index.js" -o -name "index.tsx" -o -name "App.js"
```

### Step 3: Map Architecture and Components

Understand the high-level structure and key modules.

**Analyze Directory Structure:**

```bash
# List top-level directories
ls -d */ | head -20

# Common patterns to look for:
# - src/ or lib/ (source code)
# - tests/ or test/ (test files)
# - config/ (configuration)
# - docs/ (documentation)
# - scripts/ (utility scripts)
# - models/ or entities/ (data models)
# - views/ or templates/ (UI)
# - controllers/ or handlers/ (business logic)
# - services/ or api/ (external services)
# - utils/ or helpers/ (utilities)
```

**Identify Architecture Pattern:**

Common patterns in legacy code:
- **MVC** (Model-View-Controller): Django, Rails, Spring MVC
- **Layered**: Presentation → Business → Data layers
- **Microservices**: Multiple small services
- **Monolith**: Single large application
- **Plugin-based**: Core + extensions

See `references/architecture_patterns.md` for detailed pattern identification.

**Create Architecture Diagram:**

```
Example Web Application Architecture:

┌─────────────────────────────────────────┐
│          Frontend (React)               │
│  - components/                          │
│  - pages/                               │
│  - hooks/                               │
└───────────────┬─────────────────────────┘
                │ API Calls
                ↓
┌─────────────────────────────────────────┐
│       API Layer (Flask/Express)         │
│  - routes/                              │
│  - middleware/                          │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│       Business Logic                    │
│  - services/                            │
│  - controllers/                         │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│       Data Layer                        │
│  - models/                              │
│  - repositories/                        │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│       Database (PostgreSQL/MongoDB)      │
└─────────────────────────────────────────┘
```

### Step 4: Analyze Dependencies

Map module relationships and identify coupling issues.

**Find Direct Dependencies:**

**Python:**
```bash
# Find imports in all Python files
grep -rh "^import \|^from " --include="*.py" | sort | uniq

# Analyze requirements
cat requirements.txt

# Or from setup.py
grep -A 20 "install_requires" setup.py
```

**Java:**
```bash
# Analyze Maven dependencies
cat pom.xml | grep -A 3 "<dependency>"

# Or Gradle
cat build.gradle | grep -A 3 "implementation\|compile"

# Find imports in code
grep -rh "^import " --include="*.java" | sort | uniq | head -50
```

**JavaScript:**
```bash
# Analyze package.json
cat package.json | grep -A 50 "dependencies"

# Find imports
grep -rh "^import \|require(" --include="*.js" --include="*.ts" | head -50
```

**Create Dependency Map:**

```
Key Internal Dependencies:

auth module
  ├─ depends on: user_model, database, config
  └─ used by: api_routes, admin_panel

user_model
  ├─ depends on: database, validators
  └─ used by: auth, profile, admin

payment module
  ├─ depends on: user_model, external_api, logger
  └─ used by: checkout, subscription

Circular dependencies detected:
  ⚠️  module_a → module_b → module_c → module_a
```

See `references/dependency_analysis.md` for tools and techniques.

### Step 5: Identify Code Quality Issues

Detect technical debt, code smells, and improvement opportunities.

**Common Quality Issues to Look For:**

**1. Large Files (God Objects)**
```bash
# Find files over 500 lines
find . -name "*.py" -exec wc -l {} \; | awk '$1 > 500' | sort -rn

# Find files over 1000 lines (serious issue)
find . -name "*.java" -exec wc -l {} \; | awk '$1 > 1000' | sort -rn
```

**2. Dead Code**
```bash
# Find unused imports (Python - requires tools)
# Install: pip install autoflake
find . -name "*.py" -exec autoflake --check {} \;

# Find TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.java"
```

**3. Code Duplication**
```bash
# Find duplicate code (requires tool)
# Install: pip install pylint
pylint --disable=all --enable=duplicate-code src/

# Or use PMD for Java
# pmd cpd --minimum-tokens 100 --files src/
```

**4. Complex Functions**
```bash
# Find long functions (crude check - look for large blocks)
# Python: Look for functions with many lines between def and next def
# Java: Look for methods with many lines between { and }

# Use complexity tools for accurate analysis:
# Python: radon cc src/ -a
# Java: Use PMD or Checkstyle
```

**5. Missing Documentation**
```bash
# Find functions without docstrings (Python)
grep -A 1 "^def " --include="*.py" -r . | grep -v '"""' | grep -v "'''"

# Find classes without documentation (Java)
grep -B 1 "^public class\|^class " --include="*.java" -r . | grep -v "/\*\*" | grep -v "//"
```

**6. Outdated Patterns**

Look for:
- Python 2 syntax (e.g., `print "hello"`, `raw_input()`)
- Java pre-8 patterns (no lambdas, no Optional)
- Deprecated libraries
- Security vulnerabilities (SQL injection, XSS)

See `references/code_quality_checklist.md` for comprehensive quality checks.

### Step 6: Assess Test Coverage

Identify testing gaps and quality of existing tests.

**Find Tests:**

```bash
# Python tests
find . -name "test_*.py" -o -name "*_test.py"
ls tests/ test/

# Java tests
find . -name "*Test.java" -o -name "*Tests.java"
ls src/test/

# JavaScript tests
find . -name "*.test.js" -o -name "*.spec.js" -o -name "*.test.ts"
```

**Calculate Test Coverage:**

**Python:**
```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Java:**
```bash
# Maven with JaCoCo
mvn clean test jacoco:report

# View report
open target/site/jacoco/index.html
```

**JavaScript:**
```bash
# Jest with coverage
npm test -- --coverage

# View report
open coverage/lcov-report/index.html
```

**Assess Test Quality:**

```
Quality Checklist:
- [ ] Unit tests exist for core business logic
- [ ] Integration tests cover key workflows
- [ ] Tests are readable and maintainable
- [ ] Tests run quickly (< 10 seconds for unit tests)
- [ ] Mocking is used appropriately
- [ ] Edge cases are tested
- [ ] Tests don't depend on external services (or are mocked)
- [ ] Coverage > 70% for critical modules
```

### Step 7: Generate Summary Report

Create actionable documentation for the team.

**Summary Template:**

```markdown
# Legacy Codebase Summary: [Project Name]

## Executive Summary

[2-3 sentence overview of what the codebase does]

**Key Metrics:**
- Lines of Code: [X]
- Number of Files: [Y]
- Primary Language: [Language]
- Test Coverage: [Z%]
- Last Major Update: [Date]

## Architecture Overview

### High-Level Structure

[Include architecture diagram from Step 3]

### Key Components

1. **[Component Name]** (`path/to/component/`)
   - **Purpose:** [What it does]
   - **Entry Point:** [Main file/class]
   - **Dependencies:** [Key dependencies]
   - **Lines of Code:** [X]

2. **[Component Name]** (`path/to/component/`)
   - **Purpose:** [What it does]
   - **Entry Point:** [Main file/class]
   - **Dependencies:** [Key dependencies]
   - **Lines of Code:** [X]

[Repeat for 5-10 key components]

### Technology Stack

**Core Technologies:**
- [Language] [Version]
- [Framework] [Version]
- [Database] [Version]

**Key Dependencies:**
- [Library 1] - [Purpose]
- [Library 2] - [Purpose]
- [Library 3] - [Purpose]

## Entry Points and Workflows

### Main Entry Points

1. **[Entry Point Name]** - `path/to/file.py:function()`
   - **Purpose:** [What it does]
   - **Triggered by:** [User action, cron, API call, etc.]

2. **[Entry Point Name]** - `path/to/file.java:main()`
   - **Purpose:** [What it does]
   - **Triggered by:** [How it's invoked]

### Critical Workflows

**Workflow 1: [Name]** (e.g., User Registration)
```
1. User submits form → routes/auth.py:register()
2. Validates input → validators/user_validator.py
3. Creates user → models/user.py:create()
4. Sends email → services/email_service.py
5. Returns response
```

**Workflow 2: [Name]** (e.g., Payment Processing)
```
[Step-by-step flow]
```

## Dependency Analysis

### External Dependencies

**Total Dependencies:** [X]

**Outdated Dependencies (require updates):**
- [Library Name] [Current Version] → [Latest Version]
- [Library Name] [Current Version] → [Latest Version]

**Deprecated Dependencies (require replacement):**
- [Library Name] - Deprecated since [Date]
  - **Suggested Replacement:** [New Library]

### Internal Dependencies

**Highly Coupled Modules (>5 dependencies):**
- `module_a` - depends on [X] modules
- `module_b` - depends on [Y] modules

**Circular Dependencies:**
- ⚠️ `auth` → `user` → `auth`
- ⚠️ `order` → `payment` → `order`

## Code Quality Assessment

### Metrics Summary

- **Average File Size:** [X] lines
- **Largest File:** `path/to/file.py` ([X] lines) ⚠️
- **TODO/FIXME Comments:** [X] occurrences
- **Code Duplication:** [Low/Medium/High]

### Quality Issues

**Critical Issues (Fix Immediately):**
1. **Security Vulnerability:** SQL injection in `path/to/file.py:45`
2. **Large File:** `god_class.java` (2,500 lines) - violates SRP
3. **Circular Dependency:** [Details]

**High Priority (Address Soon):**
1. **No Error Handling:** Missing try/catch in payment module
2. **Hardcoded Credentials:** Found in `config/settings.py`
3. **Deprecated API:** Using old authentication library

**Medium Priority (Technical Debt):**
1. **Code Duplication:** Copy-pasted validation logic in 5 files
2. **Missing Documentation:** 60% of functions lack docstrings
3. **Long Methods:** 15 methods exceed 100 lines

**Low Priority (Improvements):**
1. **Outdated Naming:** Inconsistent variable names
2. **Missing Type Hints:** (Python) or generics (Java)
3. **Verbose Code:** Could be simplified with modern patterns

### Code Smells Detected

- **God Objects:** [List large classes/modules]
- **Feature Envy:** [Methods accessing other objects' data frequently]
- **Dead Code:** [Unused functions/classes]
- **Magic Numbers:** [Hardcoded values without constants]

## Test Coverage Analysis

### Coverage Summary

- **Overall Coverage:** [X%]
- **Critical Modules Coverage:**
  - auth module: [Y%]
  - payment module: [Z%]
  - user management: [W%]

### Testing Gaps

**Untested Critical Code:**
1. `payment/processor.py` - 0% coverage ⚠️
2. `auth/security.py` - 30% coverage
3. `api/routes.py` - 45% coverage

**Missing Test Types:**
- [ ] No integration tests for payment flow
- [ ] No end-to-end tests for user journey
- [ ] No performance/load tests

### Test Quality Issues

- **Slow Tests:** 20 tests take >5 seconds each
- **Flaky Tests:** `test_async_operation` fails intermittently
- **Coupled Tests:** Tests depend on database state

## Recommendations

### Immediate Actions (This Sprint)

1. **Fix Security Issues**
   - Patch SQL injection vulnerability in `auth/login.py`
   - Remove hardcoded credentials, use environment variables

2. **Add Critical Tests**
   - Write integration tests for payment processor
   - Add unit tests for authentication logic

3. **Break Circular Dependencies**
   - Refactor `auth` ↔ `user` circular dependency
   - Extract shared code to new `common` module

### Short-Term Improvements (This Quarter)

1. **Reduce Technical Debt**
   - Refactor `god_class.java` into 3-4 focused classes
   - Eliminate code duplication in validation logic
   - Update deprecated dependencies

2. **Improve Documentation**
   - Add docstrings to all public functions
   - Create architecture diagram
   - Document deployment process

3. **Enhance Test Coverage**
   - Achieve 70% coverage for core modules
   - Add integration tests for critical workflows
   - Set up CI/CD with automated testing

### Long-Term Improvements (This Year)

1. **Architectural Refactoring**
   - Extract microservices for payment and notification
   - Implement proper layering (separate business logic from data access)
   - Introduce dependency injection for better testability

2. **Modernization**
   - Upgrade to [Language] [Latest Version]
   - Adopt modern patterns (async/await, type hints, etc.)
   - Migrate from [Old Framework] to [New Framework]

3. **Quality Infrastructure**
   - Set up automated code quality checks (linting, complexity analysis)
   - Implement pre-commit hooks
   - Add performance monitoring

## Quick Reference

### Key Files to Understand First

1. `path/to/main.py` - Application entry point
2. `path/to/config.py` - Configuration
3. `path/to/models/user.py` - Core data model
4. `path/to/api/routes.py` - API endpoints
5. `path/to/services/auth_service.py` - Authentication logic

### Common Commands

```bash
# Start application
[command]

# Run tests
[command]

# Build for production
[command]

# Deploy
[command]
```

### Key Contacts

- **Original Authors:** [Names/emails if available]
- **Current Maintainers:** [Names/emails]
- **Documentation:** [Links]
- **Issue Tracker:** [URL]

## Appendix

### Glossary

- **[Term]:** [Definition]
- **[Term]:** [Definition]

### External Resources

- [Link to original documentation]
- [Link to related projects]
- [Link to framework docs]
```

## Summary Output Examples

### Example 1: Small Python Flask App

```markdown
# Legacy Codebase Summary: Internal Dashboard

## Executive Summary

Internal dashboard for monitoring application metrics, built with Flask.
Provides real-time data visualization and alerting for operations team.

**Key Metrics:**
- Lines of Code: 3,500
- Number of Files: 42
- Primary Language: Python 3.7
- Test Coverage: 45%
- Last Major Update: 18 months ago

## Architecture Overview

Simple Flask application with SQLAlchemy ORM and PostgreSQL database.

```
┌─────────────────┐
│  Flask Routes   │
│  (app/routes/)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Services       │
│  (app/services/)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Models         │
│  (app/models/)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  PostgreSQL DB  │
└─────────────────┘
```

### Key Components

1. **Metrics Dashboard** (`app/routes/dashboard.py`)
   - Purpose: Display real-time metrics
   - Entry Point: `dashboard_view()`
   - Dependencies: metrics_service, chart_generator
   - Lines of Code: 250

2. **Data Collection** (`app/services/collector.py`)
   - Purpose: Fetch metrics from external APIs
   - Entry Point: `collect_metrics()` (cron job)
   - Dependencies: requests, database models
   - Lines of Code: 180

3. **Alert System** (`app/services/alerts.py`)
   - Purpose: Send notifications when thresholds exceeded
   - Entry Point: `check_alerts()` (background task)
   - Dependencies: email_service, metrics_service
   - Lines of Code: 150

## Recommendations

### Immediate Actions
1. Update Flask to latest version (security patches)
2. Add tests for alert system (currently 0% coverage)
3. Fix hardcoded database credentials

### Short-Term
1. Increase test coverage to 70%
2. Add API documentation
3. Refactor large dashboard route (300+ lines)
```

### Example 2: Large Java Spring Application

```markdown
# Legacy Codebase Summary: E-Commerce Platform

## Executive Summary

Full-featured e-commerce platform handling product catalog, orders, payments,
and customer management. Serves 100K+ daily active users.

**Key Metrics:**
- Lines of Code: 185,000
- Number of Files: 1,240
- Primary Language: Java 8
- Test Coverage: 62%
- Last Major Update: 6 months ago

## Architecture Overview

Layered Spring Boot application with microservice patterns emerging.

[Detailed architecture diagram showing layers]

### Critical Issues Identified

**High Priority:**
1. **Memory Leak:** Order processing service shows increasing heap usage
2. **N+1 Query Problem:** Product listing generates 500+ DB queries
3. **No Monitoring:** Missing APM tools for production

**Modernization Opportunities:**
1. Migrate to Java 17 (LTS)
2. Extract payment service as microservice
3. Implement caching layer (Redis)

## Recommendations

[Detailed phased approach to refactoring]
```

## Best Practices

1. **Start broad, then narrow** - Overview first, details second
2. **Focus on actionable insights** - Prioritize what can be improved
3. **Use visual aids** - Diagrams clarify complex relationships
4. **Prioritize by risk** - Security and stability issues first
5. **Be specific** - Point to exact files and line numbers
6. **Estimate effort** - Help teams plan refactoring work
7. **Document assumptions** - Note what analysis couldn't determine
8. **Update regularly** - Re-analyze as code evolves

## Resources

- **`references/architecture_patterns.md`** - Common architectural patterns in legacy systems and how to identify them
- **`references/dependency_analysis.md`** - Tools and techniques for analyzing module dependencies and coupling
- **`references/code_quality_checklist.md`** - Comprehensive checklist for assessing code quality and technical debt

## Quick Reference

| Task | Command/Approach |
|------|-----------------|
| Count LOC | `find . -name "*.py" \| xargs wc -l` |
| Find entry points | `grep -r "if __name__ == '__main__'"` |
| Analyze imports | `grep -rh "^import \|^from " \| sort \| uniq` |
| Find large files | `find . -name "*.py" -exec wc -l {} \\; \| sort -rn` |
| Test coverage | `pytest --cov=src --cov-report=term` |
| Find TODOs | `grep -rn "TODO\|FIXME"` |
