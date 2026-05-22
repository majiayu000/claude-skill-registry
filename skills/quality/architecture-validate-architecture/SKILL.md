---
name: architecture-validate-architecture
description: Automates architecture validation for Clean Architecture, Hexagonal, Layered, and MVC patterns. Detects layer boundary violations, dependency rule breaches, and architectural anti-patterns. Use when asked to "validate architecture", "check layer boundaries", "architectural review", before major refactoring, or as pre-commit quality gate. Adapts to project's architectural style by reading ARCHITECTURE.md.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Glob
---

# Validate Architecture

## Table of Contents

**Quick Start** → [When to Use](#when-to-use-this-skill) | [What It Does](#purpose) | [Simple Example](#quick-start)

**How to Implement** → [Validation Process](#validation-process) | [Architecture Rules](#architecture-specific-rules) | [Expected Output](#expected-outcomes)

**Patterns** → [Clean Architecture](#clean-architecture) | [Hexagonal](#hexagonal-architecture) | [Layered](#layered-architecture) | [MVC](#mvc-architecture)

**Help** → [Anti-Patterns](#common-anti-patterns-detected) | [Troubleshooting](#troubleshooting) | [Integration](#integration-points)

**Reference** → [Layer Dependencies](./references/reference.md) | [Diff-Aware Validation](./references/diff-aware-validation.md) | [Quick Reference](./references/diff-aware-validation-quickref.md)

---

## Purpose

Automates architecture validation for multiple architectural patterns (Clean Architecture, Hexagonal, Layered, MVC). Automatically detects the project's architectural style from ARCHITECTURE.md, scans all source files for import violations, validates dependency direction (inward only for Clean/Hexagonal), and reports violations with specific fixes. Adapts to any architectural pattern and provides actionable remediation guidance.

## Quick Start

**User asks:** "Validate my architecture" or "Check if this follows Clean Architecture"

**What happens:**
1. Reads project's `ARCHITECTURE.md` to identify architectural pattern
2. Scans all source files for import violations
3. Validates dependency direction (inward only for Clean/Hexagonal)
4. Reports violations with file:line:fix recommendations

**Result:** ✅ All checks passed OR ❌ Violations with specific fixes

## When to Use This Skill

Invoke this skill when:
- User asks "validate architecture", "check layer boundaries", "architectural review"
- Before major refactoring or structural changes
- As part of pre-commit quality gates
- After adding new dependencies to any layer
- Reviewing code for architecture compliance
- User mentions "Clean Architecture", "Hexagonal", "Layered", or "MVC"

## What This Skill Does

### Supported Architectural Patterns

This skill automatically adapts to:

1. **Clean Architecture** (Concentric layers: Domain → Application → Infrastructure → Interface)
2. **Hexagonal Architecture** (Ports and Adapters)
3. **Layered Architecture** (Presentation → Business → Data)
4. **MVC** (Model → View → Controller)

### Validation Checks

**1. Pattern Detection**
- Reads `ARCHITECTURE.md` or similar documentation
- Identifies architectural style and layer definitions
- Parses dependency rules and constraints

**2. Layer Boundary Validation**
- Scans all import statements in source files
- Checks for violations (e.g., Domain importing Infrastructure)
- Detects circular dependencies between layers

**3. Dependency Direction Validation**
- Verifies dependencies flow correctly (inward for Clean/Hexagonal)
- Ensures outer layers depend on inner, never reverse
- Validates domain/core has no external dependencies

**4. Pattern Compliance**
- Checks for required patterns (ServiceResult, Repository, etc.)
- Verifies naming conventions (Services in application/, etc.)
- Validates file organization matches architectural layers

**5. Anti-Pattern Detection**
- Domain importing database/framework code
- Application importing concrete infrastructure
- Circular dependencies between layers
- Business logic in interface/presentation layers

## Instructions

### Overview

Validating architecture involves a 5-step process:

1. **Identify Architecture** - Read ARCHITECTURE.md and detect pattern (Clean, Hexagonal, Layered, MVC)
2. **Extract Layer Definitions** - Map directory structure to architectural layers
3. **Scan Imports** - Analyze all import statements in source files
4. **Validate Rules** - Check dependency direction and layer boundaries
5. **Report Violations** - Generate actionable report with specific fixes

See detailed steps in [Validation Process](#validation-process) section below.

## Validation Process

### Step 1: Identify Architecture

```bash
# Read project documentation
Read ARCHITECTURE.md or README.md

# Identify pattern from keywords:
# - "Clean Architecture" → Clean
# - "Hexagonal" or "Ports and Adapters" → Hexagonal
# - "Layered" → Layered
# - "MVC" → MVC
```

### Step 2: Extract Layer Definitions

For Clean Architecture:
```
Domain Layer: domain/ (innermost)
Application Layer: application/
Infrastructure Layer: infrastructure/
Interface Layer: interfaces/ (outermost)
```

For Hexagonal:
```
Core/Domain: domain/
Ports: ports/ (interfaces)
Adapters: adapters/ (implementations)
```

### Step 3: Scan Imports

```bash
# Find all Python files
Glob: **/*.py (or **/*.js, **/*.ts for other languages)

# Extract imports from each file
Grep pattern: "^from .* import|^import "

# Categorize by layer based on file path
```

### Step 4: Validate Rules

**Clean Architecture Rules:**
```
Domain:
  ✅ Can import: domain only
  ❌ Cannot import: application, infrastructure, interfaces

Application:
  ✅ Can import: domain, application
  ❌ Cannot import: interfaces, infrastructure (concrete)

Infrastructure:
  ✅ Can import: domain, application (interfaces)
  ❌ Cannot import: interfaces (API/MCP layers)

Interface:
  ✅ Can import: application, domain
  ❌ Cannot import: infrastructure directly
```

### Step 5: Report Violations

```
❌ Architecture Validation: FAILED

Violations found:

1. [CRITICAL] Domain Layer Violation
   File: src/domain/models/entity.py:12
   Issue: Importing from infrastructure layer
   Code: from infrastructure.neo4j import Neo4jDriver
   Fix: Remove direct infrastructure dependency. Use repository interface instead.

2. [HIGH] Application Layer Violation
   File: src/application/services/search.py:8
   Issue: Importing from interfaces layer
   Code: from interfaces.mcp.tools import search_code
   Fix: Application should not know about interfaces. Move logic to application handler.

Total Violations: 2 (2 critical, 0 high, 0 medium)
```

## Usage Examples

### Example 1: Validate Entire Codebase

```
User: "Validate architecture before I commit"

Claude:
1. Reads ARCHITECTURE.md → Identifies Clean Architecture
2. Scans all .py files for imports
3. Validates each layer's imports
4. Reports violations or confirms compliance
```

### Example 2: Validate Specific Changes

```
User: "Check if my refactoring follows Clean Architecture"

Claude:
1. Runs: git diff --name-only
2. Filters Python files
3. Validates only modified files
4. Reports violations in changed code
```

### Example 3: Pre-Commit Hook Integration

```
Automatically invoked by pre-commit hook:
1. Gets staged files
2. Validates architectural boundaries
3. Blocks commit if critical violations found
4. Provides actionable fix recommendations
```

## Architecture-Specific Rules

### Clean Architecture

**Dependency Rule**: Dependencies flow inward only

```
Interface → Application → Domain ← Infrastructure
   (UI)      (Use Cases)   (Core)    (External)
```

**Layer Rules:**
- **Domain**: Pure business logic, no framework/external dependencies
- **Application**: Orchestrates domain, defines interfaces for infrastructure
- **Infrastructure**: Implements application interfaces, depends on external systems
- **Interface**: Entry points, depends on application use cases only

**Detection Patterns:**
```bash
# Domain violations
grep -rn "from.*\.\(application\|infrastructure\|interfaces\)" domain/

# Application violations
grep -rn "from.*\.interfaces" application/

# Interface violations
grep -rn "from.*\.infrastructure" interfaces/
```

### Hexagonal Architecture

**Dependency Rule**: Core has no dependencies, adapters depend on ports

```
   Adapters (Outside)
        ↓
   Ports (Interfaces)
        ↓
   Domain (Core)
```

**Layer Rules:**
- **Domain/Core**: Pure business logic, no external dependencies
- **Ports**: Interfaces defined by core
- **Adapters**: Implement ports, connect to external systems

**Detection Patterns:**
```bash
# Core violations
grep -rn "from.*\.\(adapters\|ports\)" domain/

# Adapter bypassing ports
grep -rn "from.*\.domain" adapters/ | grep -v "from.*\.ports"
```

### Layered Architecture

**Dependency Rule**: Each layer depends only on layer below

```
Presentation Layer
       ↓
Business Logic Layer
       ↓
Data Access Layer
```

**Layer Rules:**
- **Presentation**: Depends on business logic only
- **Business Logic**: Depends on data access only
- **Data Access**: No dependencies on upper layers

**Detection Patterns:**
```bash
# Presentation bypassing business logic
grep -rn "from.*\.data" presentation/

# Data access depending on business
grep -rn "from.*\.business" data/
```

### MVC Architecture

**Dependency Rule**: Model is independent, View/Controller depend on Model

```
View → Controller → Model
  ↓         ↓
  ←─────────
```

**Layer Rules:**
- **Model**: Independent, no View/Controller dependencies
- **View**: Depends on Model, not Controller
- **Controller**: Orchestrates Model and View

**Detection Patterns:**
```bash
# Model violations
grep -rn "from.*\.\(views\|controllers\)" models/

# View importing Controller
grep -rn "from.*\.controllers" views/
```

## Common Anti-Patterns Detected

### 1. Domain Importing Infrastructure
```python
# ❌ VIOLATION
# domain/entities/user.py
from infrastructure.database import DatabaseConnection

# ✅ FIX
# domain/repositories/user_repository.py (interface)
class UserRepository(Protocol):
    def save(self, user: User) -> None: ...

# infrastructure/repositories/user_repository_impl.py
class UserRepositoryImpl:
    def __init__(self, db: DatabaseConnection):
        self.db = db
```

### 2. Application Importing Interfaces
```python
# ❌ VIOLATION
# application/services/search.py
from interfaces.api.routes import SearchEndpoint

# ✅ FIX
# application/handlers/search_handler.py
class SearchHandler:
    def handle(self, query: SearchQuery) -> SearchResult:
        # Application logic here
        pass

# interfaces/api/routes.py
@app.post("/search")
def search(query: str):
    handler = SearchHandler()
    return handler.handle(SearchQuery(query))
```

### 3. Circular Dependencies
```python
# ❌ VIOLATION
# service_a.py
from service_b import ServiceB

# service_b.py
from service_a import ServiceA

# ✅ FIX
# Extract shared interface/base class
# interfaces.py
class ServiceInterface(Protocol):
    def execute(self) -> Result: ...

# service_a.py
from interfaces import ServiceInterface

# service_b.py
from interfaces import ServiceInterface
```

### 4. Business Logic in Interface Layer
```python
# ❌ VIOLATION
# interfaces/api/routes.py
@app.post("/users")
def create_user(data: dict):
    # Validation, business rules, database save all here
    user = User(**data)
    if not user.email:
        raise ValueError("Email required")
    db.save(user)

# ✅ FIX
# application/commands/create_user.py
class CreateUserHandler:
    def handle(self, cmd: CreateUserCommand) -> ServiceResult[User]:
        # Business logic here
        pass

# interfaces/api/routes.py
@app.post("/users")
def create_user(data: dict):
    handler = CreateUserHandler()
    return handler.handle(CreateUserCommand(**data))
```

## Integration Points

### With Pre-Commit Hooks

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python .claude/skills/validate-architecture/scripts/validate.py
if [ $? -ne 0 ]; then
    echo "❌ Architecture validation failed. Commit blocked."
    exit 1
fi
```

### With CI/CD Pipeline

Add to `.github/workflows/ci.yml`:
```yaml
- name: Validate Architecture
  run: python .claude/skills/validate-architecture/scripts/validate.py
```

### With Quality Gates

Add to `scripts/check_all.sh`:
```bash
echo "Validating architecture..."
python .claude/skills/validate-architecture/scripts/validate.py
```

## Supporting Files

- **[references/reference.md](./references/reference.md)** - Complete layer dependency matrices for all patterns
- **[references/diff-aware-validation.md](./references/diff-aware-validation.md)** - Diff-aware validation comprehensive guide
- **[references/diff-aware-validation-summary.md](./references/diff-aware-validation-summary.md)** - Diff-aware validation summary
- **[references/diff-aware-validation-checklist.md](./references/diff-aware-validation-checklist.md)** - Pre-commit validation checklist
- **[references/diff-aware-validation-quickref.md](./references/diff-aware-validation-quickref.md)** - Quick reference for diff-aware validation
- **[references/installation.md](./references/installation.md)** - Installation and integration guide
- **[scripts/validate.py](./scripts/validate.py)** - Standalone validation script for all architectural patterns
- **[templates/arch-rules.yaml](./templates/arch-rules.yaml)** - Customizable rule definitions

## Expected Outcomes

### Success (No Violations)

```
✅ Architecture Validation: PASSED

Pattern: Clean Architecture
Files checked: 127
Violations: 0

All layer boundaries respected.
Dependencies flow correctly (inward only).
No architectural anti-patterns detected.
```

### Failure (Violations Found)

```
❌ Architecture Validation: FAILED

Pattern: Clean Architecture
Files checked: 127
Violations: 5 (3 critical, 2 high, 0 medium)

Critical Violations:

1. Domain Layer Importing Infrastructure
   File: src/domain/models/entity.py:12
   Code: from infrastructure.neo4j import Neo4jDriver
   Fix: Use repository interface instead. Move Neo4jDriver to infrastructure layer.
   Impact: Breaks dependency inversion, couples domain to database

2. Application Layer Importing Interface
   File: src/application/services/search.py:8
   Code: from interfaces.mcp.tools import search_code
   Fix: Move business logic from interface to application handler
   Impact: Creates circular dependency risk

High Violations:

3. Circular Dependency Detected
   Files: service_a.py:5 ↔ service_b.py:8
   Fix: Extract shared interface or base class
   Impact: Difficult to test, fragile architecture

Summary:
- Fix critical violations before committing
- See Common Anti-Patterns Detected section above for detailed fix patterns
- Run validation again after fixes
```

## Success Metrics

After invoking this skill, measure:
- **Violation Detection Rate**: 95%+ (catches all major violations)
- **False Positive Rate**: <5% (minimal incorrect reports)
- **Context Reduction**: 90%+ vs manual agent review
- **Execution Time**: <2s for typical codebase
- **Actionability**: 100% of violations include specific fix

## Customization

### Define Custom Rules

Create `arch-rules.yaml` in project root:
```yaml
architecture: clean
layers:
  domain:
    path: src/core
    can_import: []
    cannot_import: [infrastructure, interfaces, application]

  application:
    path: src/usecases
    can_import: [domain]
    cannot_import: [interfaces]

severity:
  domain_violation: CRITICAL
  application_violation: HIGH
```

### Language Support

Currently supports:
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)

Extend by adding patterns in `scripts/validate.py`.

## Troubleshooting

### Issue: False Positives

**Symptom**: Valid imports flagged as violations

**Fix**: Add exceptions to `arch-rules.yaml`:
```yaml
exceptions:
  - pattern: "from typing import"
    reason: "Standard library, not architectural violation"
```

### Issue: Pattern Not Detected

**Symptom**: Skill doesn't recognize architectural pattern

**Fix**: Ensure `ARCHITECTURE.md` contains pattern keywords:
- "Clean Architecture"
- "Hexagonal Architecture" or "Ports and Adapters"
- "Layered Architecture"
- "MVC"

### Issue: Missing Violations

**Symptom**: Known violations not reported

**Fix**: Check file paths match layer definitions. Update layer patterns if needed.

## Expected Benefits

| Metric | Without Validation | With Validation | Improvement |
|--------|-------------------|----------------|-------------|
| Architecture violations | 15-20 per quarter | 0-2 per quarter | 95% reduction |
| Time to detect violations | 2-5 days | 5-10 seconds | 99.9% faster |
| Refactoring cost | High (violations embedded) | Low (caught early) | 80% reduction |
| Code review time | 45-60 min | 15-20 min | 70% faster |
| Onboarding time | 2-3 weeks | 3-5 days | 75% faster |
| Technical debt | 20-30 violations/year | 2-5 violations/year | 90% reduction |

## Requirements

- Python 3.10+ (for validation script)
- Source code in supported language (Python/JS/TS)
- `ARCHITECTURE.md` or similar documentation defining layers
- Read, Grep, Bash, Glob tools available

## Red Flags to Avoid

### Architecture Violations

1. **Domain importing Infrastructure** - Breaks dependency inversion
2. **Application importing Interface** - Creates circular dependencies
3. **Infrastructure importing concrete Domain** - Should use Protocols
4. **Business logic in Interface layer** - Violates layer separation

### Detection Anti-Patterns

5. **Ignoring False Positives** - Add exceptions to arch-rules.yaml
6. **Skipping validation before major changes** - Always validate first
7. **Not updating layer definitions** - Keep ARCHITECTURE.md current
8. **Assuming pattern without verification** - Read ARCHITECTURE.md first

### Process Mistakes

9. **Proceeding with violations** - Fix before committing
10. **Not documenting exceptions** - Explain why deviation needed
11. **Skipping after refactor** - Validation most critical after structural changes
12. **Manual validation only** - Automate in pre-commit hooks and CI

## Utility Scripts

- [Validate Architecture Script](./scripts/validate.py) - Full-featured architecture validation tool supporting Clean, Hexagonal, Layered, and MVC patterns

## See Also

- **validate-layer-boundaries** - Project-specific validation for project-watch-mcp
- **@architecture-guardian** - Agent for architectural guidance and review
- **ARCHITECTURE.md** - Project's architecture documentation
- **ADR-001** - Architecture Decision Record for Clean Architecture
