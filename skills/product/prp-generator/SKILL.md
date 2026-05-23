---
name: prp-generator
description: Auto-activates when generating Product Requirements Prompt (PRP) documents
  from synthesized design outputs, providing structured templates and comprehensive
  implementation guidance.
allowed-tools: Write, Edit
---

## Purpose

The **prp-generator** skill provides structured templates and methods for creating comprehensive Product Requirements Prompt (PRP) documents. PRPs serve as the primary input for Phase 3 (Implementation), containing all design information, library documentation, dependencies, implementation plans, testing strategies, and success criteria needed to implement features.

## When to Use

This skill auto-activates when you:
- Generate PRP documents from synthesized design
- Create implementation guidance from architectural design
- Structure design information for implementation phase
- Define implementation plans with step-by-step guidance
- Specify testing strategies and success criteria
- Document architecture, libraries, and dependencies for implementers

## Provided Capabilities

### 1. Structured PRP Generation
- **Standard Template**: Consistent PRP structure across all features
- **Section Templates**: Pre-defined templates for each PRP section
- **Completeness Checking**: Ensure all required sections present
- **Format Validation**: Validate markdown structure and linking

### 2. Implementation Planning
- **Phased Approach**: Break implementation into logical phases
- **Step-by-Step Guidance**: Detailed steps within each phase
- **Dependency Ordering**: Ensure dependencies installed before use
- **Validation Checkpoints**: Define validation at each phase

### 3. Testing Strategy Documentation
- **Test Types**: Unit, integration, end-to-end testing approaches
- **Test Coverage**: Specify coverage targets per component
- **Mock Strategies**: Document how to mock library dependencies
- **Test Data**: Provide test data and fixture guidance

### 4. Success Criteria Definition
- **Acceptance Criteria**: Map from requirements analysis
- **Implementation Criteria**: Code-level success criteria
- **Testing Criteria**: Test coverage and passing requirements
- **Documentation Criteria**: Required documentation artifacts

### 5. Architecture Documentation
- **Component Diagrams**: Visual architecture representations
- **Data Models**: Pydantic schemas with validations
- **API Contracts**: Endpoint specifications with examples
- **Data Flow**: How data moves through system

## Usage Guide

### Step 1: Load Inputs

Load all required inputs for PRP generation:

**Required Inputs**:
1. **Analysis Document**: `/docs/implementation/analysis/feature-{issue-number}-analysis.md`
   - Requirements (functional and non-functional)
   - Security considerations
   - Technical stack requirements
   - Dependencies
   - Scope definition
   - Identified risks

2. **Synthesized Design**: Output from design-synthesizer skill
   - Component architecture with library mappings
   - Data models with library validation patterns
   - API contracts with library integration
   - Library integration strategies
   - Dependency resolution
   - Implementation path
   - Design decisions
   - Identified issues/gaps

**Loading Pattern**:
```python
# Read analysis document
analysis = read_document("/docs/implementation/analysis/feature-{issue-number}-analysis.md")

# Parse synthesized design (from synthesis step)
design = parse_synthesized_design()

# Extract key information
requirements = extract_requirements(analysis)
architecture = extract_architecture(design)
libraries = extract_libraries(design)
dependencies = extract_dependencies(design)
implementation_plan = extract_implementation_plan(design)
```

### Step 2: Create PRP Header

Use `prp-template.md` header section:

```markdown
# Product Requirements Prompt: [Feature Name] (Issue #{issue-number})

**Date**: [YYYY-MM-DD]
**Designer**: Design Orchestrator (Claude Code)
**Issue**: #{issue-number} - [Issue Title]
**Analysis Document**: /docs/implementation/analysis/feature-{issue-number}-analysis.md

---

**Status**: Ready for Implementation (Phase 3)
**Complexity**: [Low / Medium / High]
**Estimated Effort**: [Hours/Days]
**Priority**: [P0 / P1 / P2 / P3]

---
```

**Complexity Guidelines**:
- **Low**: Single component, <3 files, well-documented libraries
- **Medium**: Multiple components, 3-10 files, some custom logic
- **High**: Complex architecture, >10 files, custom integrations

### Step 3: Write Executive Summary

Provide 2-3 paragraph overview of the design:

**Executive Summary Template**:
```markdown
## Executive Summary

This document provides comprehensive implementation guidance for [feature name],
which [high-level description of what feature does and why it's valuable].

**Architectural Approach**: [Brief description of architecture - e.g., "Service layer
pattern with FastAPI endpoints, SQLAlchemy ORM, and Redis caching"]

**Key Libraries**: [List 3-5 primary libraries - e.g., "FastAPI 0.95.0 for API
framework, SQLAlchemy 2.0.0 for ORM, PassLib 1.7.4 for password hashing"]

**Implementation Strategy**: [Brief description of implementation phases - e.g.,
"4-phase approach: (1) Data models and repository, (2) Service layer business logic,
(3) API endpoints, (4) Testing and validation"]

**Key Considerations**: [1-2 important considerations - e.g., "Security-first
approach with OWASP compliance, performance target of <200ms API response time"]
```

**Example**:
```markdown
## Executive Summary

This document provides comprehensive implementation guidance for user authentication
system, which enables secure user login, session management, and access control for
the application.

**Architectural Approach**: Service layer pattern with FastAPI RESTful API endpoints,
SQLAlchemy ORM for user persistence, PassLib for secure password hashing, and JWT
tokens for session management.

**Key Libraries**: FastAPI 0.95.0 (API framework), SQLAlchemy 2.0.0 (ORM), PassLib
1.7.4 (password hashing), python-jose 3.3.0 (JWT tokens), pydantic 1.10.7 (validation).

**Implementation Strategy**: 4-phase approach: (1) User data model and repository
with SQLAlchemy, (2) Authentication service with PassLib and JWT, (3) FastAPI
endpoints with pydantic validation, (4) Comprehensive testing with pytest and mocks.

**Key Considerations**: OWASP Top 10 compliance for authentication vulnerabilities,
bcrypt with cost factor 12 for password hashing, rate limiting for brute force
protection, secure session token management with expiration.
```

### Step 4: Document Requirements Reference

Link to analysis document and summarize key requirements:

**Requirements Reference Template**:
```markdown
## Requirements Reference

**Source**: [Link to analysis document]

### Functional Requirements (Summary)
- **[FR-001]**: [Brief description]
- **[FR-002]**: [Brief description]
...

### Non-Functional Requirements (Summary)
- **Performance**: [Key performance requirements]
- **Security**: [Key security requirements]
- **Usability**: [Key usability requirements]
- **Scalability**: [Key scalability requirements]

### Acceptance Criteria (Key Points)
- [ ] [Top acceptance criterion 1]
- [ ] [Top acceptance criterion 2]
- [ ] [Top acceptance criterion 3]

**Full Requirements**: See analysis document for complete requirements, security
assessment, and risk analysis.
```

### Step 5: Document Architecture Design

Use synthesized architecture design:

**Architecture Design Template**:
```markdown
## Architecture Design

### Component Overview

[ASCII diagram or description of component architecture]

### Components

#### Component: [ComponentName]
**Purpose**: [What this component does]
**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

**Library Integration**:
- **Primary Library**: [LibraryName] v[Version]
- **APIs Used**: [Specific library APIs/classes]
- **Pattern**: [Integration pattern from design-patterns.md]
- **Dependencies**: [Required dependencies]

**Implementation Notes**:
- [Important implementation detail 1]
- [Important implementation detail 2]

**Code Example**:
```python
# Example from library documentation (libraries-{issue-number}.md, Example X.Y)
[Code snippet showing library usage pattern]
```

[Repeat for each component]

### Data Models

#### Model: [ModelName]
**Purpose**: [What this model represents]
**Fields**:
```python
from pydantic import BaseModel, Field
from [library] import [ValidationMixin]

class [ModelName](BaseModel):
    field1: type = Field(..., description="...")  # Validation
    field2: type = Field(default=..., ge=..., le=...)  # Range validation
    # ... more fields
```

**Validation Rules**:
- [Field1]: [Validation description]
- [Field2]: [Validation description]

**Relationships**:
- [Related Model]: [Relationship type and description]

**Library Integration**:
- **Validation**: [Library providing validation - e.g., Pydantic validators]
- **Serialization**: [How model is serialized - e.g., Pydantic .dict()]
- **Storage**: [ORM pattern - e.g., SQLAlchemy declarative base]

[Repeat for each model]

### API Contracts

#### Endpoint: [METHOD] [/path]
**Purpose**: [What this endpoint does]

**Request**:
```python
class [RequestModel](BaseModel):
    field1: type
    field2: type
```

**Response**:
```python
class [ResponseModel](BaseModel):
    field1: type
    field2: type
```

**Status Codes**:
- `200`: Success - [Description]
- `400`: Bad Request - [Description]
- `401`: Unauthorized - [Description]
- `404`: Not Found - [Description]
- `500`: Internal Server Error - [Description]

**Implementation**:
```python
# FastAPI endpoint pattern from library docs
@app.[method]("/path", response_model=[ResponseModel])
def endpoint([params: RequestModel]):
    # Implementation using service layer
    ...
```

[Repeat for each endpoint]

### Data Flow

[Describe how data flows through system]

**Example Flow**: User Authentication
```
1. Client sends POST /auth/login with email/password
2. FastAPI endpoint validates request (Pydantic)
3. AuthenticationService.authenticate() called
4. UserRepository.get_by_email() queries database (SQLAlchemy)
5. PassLib.verify() checks password hash
6. JWT token generated (python-jose)
7. Token returned to client
```

### Error Handling Strategy

**Library Exception Mapping**:
| Library Exception | Architectural Exception | HTTP Status | User Message |
|-------------------|------------------------|-------------|--------------|
| [LibraryException] | [AppException] | [Code] | [Message] |

**Error Handling Pattern**:
```python
try:
    # Library operation
except LibraryException as e:
    # Map to architectural exception
    raise AppException(...) from e
```
```

### Step 6: Document Library Documentation

Use library information from Documentation Researcher:

**Library Documentation Template**:
```markdown
## Library Documentation

### Library: [LibraryName] v[Version]

**Purpose**: [What library does]
**Documentation**: [Link to official docs]
**Repository**: [Link to GitHub/source]

**Installation**:
```bash
pip install [library-name]==[version]
```

**Key APIs Used**:
- `[API1]`: [Description and purpose]
- `[API2]`: [Description and purpose]

**Integration Pattern**:
```python
# Example from library documentation
[Code example showing how to use library in this project]
```

**Configuration**:
```python
# Configuration required for this library
[Configuration code or settings]
```

**Best Practices** (from library docs):
- [Best practice 1]
- [Best practice 2]

**Known Issues**:
- [Issue 1 and workaround]
- [Issue 2 and workaround]

**Testing Notes**:
- **Mocking**: [How to mock this library in tests]
- **Test Containers**: [If integration tests need real library instance]

[Repeat for each library]

### Library Comparison (if alternatives considered)

| Library | Version | Pros | Cons | Decision |
|---------|---------|------|------|----------|
| [Lib A] | [Ver] | [Pros] | [Cons] | ✅ Chosen |
| [Lib B] | [Ver] | [Pros] | [Cons] | ❌ Not chosen |

**Selection Rationale**: [Why chosen library was selected]
```

### Step 7: Document Dependencies

Use dependency information from Dependency Manager:

**Dependencies Template**:
```markdown
## Dependencies

### Dependency Tree

```
[Full dependency tree with versions]
[library-a]==[version]
├── [dep-1]==[version]
│   └── [sub-dep]==[version]
├── [dep-2]==[version]
└── [optional-dep] (optional)
```

### Installation Commands

**Install all dependencies**:
```bash
# Install using pip
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

**Install in order (if order matters)**:
```bash
# Step 1: Install base dependencies
pip install [base-deps]

# Step 2: Install main libraries
pip install [main-libs]

# Step 3: Install optional dependencies
pip install [optional-deps]
```

### Dependency Details

#### Dependency: [dep-name] v[version]
**Purpose**: [What this dependency provides]
**Required By**: [Libraries that need this dependency]
**Version Constraint**: [Why this specific version]
**Alternatives**: [Alternative versions/libraries considered]

[Repeat for key dependencies]

### Compatibility Notes

**Python Version**: [Required Python version]
**Operating System**: [OS compatibility notes]
**Database**: [Database version requirements]
**Other System Dependencies**: [System-level requirements]

### Dependency Conflicts and Resolutions

[If any conflicts were found and resolved]

**Conflict**: [Description]
- **Library A needs**: [Constraint A]
- **Library B needs**: [Constraint B]
- **Resolution**: [How conflict was resolved]
- **Pinned Version**: [Final version chosen]
```

### Step 8: Create Implementation Plan

Use `prp-template.md` implementation plan section:

**Implementation Plan Template**:
```markdown
## Implementation Plan

### Overview

This implementation follows a [N]-phase approach, progressing from foundation
(data models) to core functionality to integration to testing. Each phase builds
on the previous phase and has validation checkpoints.

### Phase 1: Foundation ([Estimated Time])

**Goal**: Create data models, repositories, and core utilities

**Tasks**:
1. **Data Models** ([Time])
   - [ ] Create [Model1] Pydantic schema with validations
   - [ ] Create [Model2] Pydantic schema with validations
   - [ ] Add [Library]-specific validators
   - [ ] Write unit tests for model validation

2. **Repository Layer** ([Time])
   - [ ] Create [Repository1] with CRUD operations
   - [ ] Implement [Library] ORM mappings
   - [ ] Add query methods for common operations
   - [ ] Write repository unit tests with mocks

3. **Configuration** ([Time])
   - [ ] Create configuration classes (Pydantic BaseSettings)
   - [ ] Add environment variable loading
   - [ ] Configure [Library1], [Library2]
   - [ ] Write configuration validation tests

**Validation Checkpoint**:
- [ ] All data models validate correctly
- [ ] All repository operations work with test database
- [ ] Configuration loads from environment
- [ ] Phase 1 tests pass (pytest)

### Phase 2: Core Implementation ([Estimated Time])

**Goal**: Implement business logic services using libraries

**Tasks**:
1. **Service Layer** ([Time])
   - [ ] Create [Service1] with business logic
   - [ ] Integrate [Library1] for [functionality]
   - [ ] Implement error handling and exception mapping
   - [ ] Add logging and monitoring
   - [ ] Write service unit tests with mocked dependencies

2. **Library Integration** ([Time])
   - [ ] Set up [Library2] client/connection
   - [ ] Implement [Library2] operations
   - [ ] Add retry logic for transient failures
   - [ ] Write integration tests with test containers

**Validation Checkpoint**:
- [ ] All service methods work correctly
- [ ] Library integrations functioning
- [ ] Error handling covers all cases
- [ ] Phase 2 tests pass (pytest)

### Phase 3: Integration ([Estimated Time])

**Goal**: Connect components and create API endpoints

**Tasks**:
1. **API Endpoints** ([Time])
   - [ ] Create [Endpoint1] with [Method] [/path]
   - [ ] Add request/response validation (Pydantic)
   - [ ] Integrate with service layer
   - [ ] Add authentication/authorization
   - [ ] Write endpoint integration tests

2. **Component Integration** ([Time])
   - [ ] Connect [Component A] to [Component B]
   - [ ] Implement data flow [Flow description]
   - [ ] Add transaction handling
   - [ ] Write integration tests for full flows

3. **Error Handling** ([Time])
   - [ ] Add global exception handlers
   - [ ] Map library exceptions to HTTP status codes
   - [ ] Implement error response formatting
   - [ ] Test error scenarios

**Validation Checkpoint**:
- [ ] All API endpoints respond correctly
- [ ] End-to-end flows work
- [ ] Error handling covers all endpoints
- [ ] Phase 3 tests pass (pytest)

### Phase 4: Testing & Validation ([Estimated Time])

**Goal**: Comprehensive testing and final validation

**Tasks**:
1. **Unit Test Coverage** ([Time])
   - [ ] Achieve [X]% unit test coverage
   - [ ] All components have isolated unit tests
   - [ ] All edge cases covered
   - [ ] Mock all external dependencies

2. **Integration Testing** ([Time])
   - [ ] Test all API endpoints (end-to-end)
   - [ ] Test library integrations with real instances
   - [ ] Test error scenarios and recovery
   - [ ] Performance testing ([targets])

3. **Security Validation** ([Time])
   - [ ] OWASP Top 10 verification
   - [ ] Input validation testing
   - [ ] Authentication/authorization testing
   - [ ] Secrets management verification

4. **Documentation** ([Time])
   - [ ] Update API documentation
   - [ ] Add code comments for complex logic
   - [ ] Create user guide (if needed)
   - [ ] Update README with new feature

**Final Validation**:
- [ ] All acceptance criteria met
- [ ] All tests pass (pytest)
- [ ] Coverage targets achieved
- [ ] Security validation complete
- [ ] Documentation complete
- [ ] Code review passed

### Phase 5: Deployment ([Estimated Time])

**Goal**: Deploy to production environment

**Tasks**:
1. **Pre-Deployment** ([Time])
   - [ ] Review deployment checklist
   - [ ] Verify environment configuration
   - [ ] Database migrations tested
   - [ ] Rollback plan documented

2. **Deployment** ([Time])
   - [ ] Deploy to staging environment
   - [ ] Run smoke tests in staging
   - [ ] Deploy to production
   - [ ] Monitor for errors

3. **Post-Deployment** ([Time])
   - [ ] Verify production functionality
   - [ ] Monitor performance metrics
   - [ ] Check logs for errors
   - [ ] Update documentation

**Deployment Validation**:
- [ ] Feature working in production
- [ ] No critical errors in logs
- [ ] Performance meets targets
- [ ] Monitoring dashboards updated
```

### Step 9: Define Testing Strategy

Use `prp-template.md` testing section:

**Testing Strategy Template**:
```markdown
## Testing Strategy

### Overview

Comprehensive testing approach with [X]% code coverage target, including unit tests
(with mocks), integration tests (with test containers), and end-to-end tests (full
API flow).

### Unit Testing

**Scope**: Individual functions, classes, methods in isolation

**Framework**: pytest

**Coverage Target**: [X]% for all modules

**Mocking Strategy**:
- Mock [Library1] using unittest.mock
- Mock [Library2] using [library-specific test fixtures]
- Mock database using SQLAlchemy in-memory database

**Test Structure**:
```
tests/
├── unit/
│   ├── test_models.py          # Data model validation tests
│   ├── test_repositories.py    # Repository logic tests (mocked DB)
│   ├── test_services.py        # Service logic tests (mocked deps)
│   └── test_validators.py      # Custom validator tests
```

**Example Unit Test**:
```python
# Test with mocked library
from unittest.mock import Mock
import pytest

def test_service_method():
    # Mock library dependency
    mock_lib = Mock()
    mock_lib.method.return_value = "expected"

    # Test service with mock
    service = MyService(mock_lib)
    result = service.do_something()

    assert result == "processed_expected"
    mock_lib.method.assert_called_once()
```

**Key Test Cases**:
- [ ] [Component1]: Test [key functionality]
- [ ] [Component2]: Test [error handling]
- [ ] [Model1]: Test [validation rules]

### Integration Testing

**Scope**: Components working together with real library instances

**Framework**: pytest with testcontainers

**Test Containers Used**:
- PostgreSQL: `testcontainers.postgres.PostgresContainer`
- Redis: `testcontainers.redis.RedisContainer`

**Test Structure**:
```
tests/
├── integration/
│   ├── test_database_operations.py   # Real DB tests
│   ├── test_cache_operations.py      # Real Redis tests
│   └── test_library_integrations.py  # Real library usage
```

**Example Integration Test**:
```python
from testcontainers.postgres import PostgresContainer

def test_repository_integration():
    with PostgresContainer("postgres:15") as postgres:
        # Create real database engine
        engine = create_engine(postgres.get_connection_url())
        # Test with real database
        ...
```

**Key Test Cases**:
- [ ] [Integration1]: Test [data flow]
- [ ] [Integration2]: Test [library interaction]

### End-to-End Testing

**Scope**: Complete API flows from request to response

**Framework**: pytest with TestClient (FastAPI) or requests

**Test Structure**:
```
tests/
├── e2e/
│   ├── test_api_flows.py         # Complete API workflows
│   ├── test_authentication.py    # Auth flows
│   └── test_error_scenarios.py   # Error handling
```

**Example E2E Test**:
```python
from fastapi.testclient import TestClient

def test_user_creation_flow():
    client = TestClient(app)

    # Full flow test
    response = client.post("/users", json={"email": "test@example.com"})
    assert response.status_code == 201

    user_id = response.json()["id"]
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
```

**Key Test Cases**:
- [ ] [Flow1]: Test [complete user journey]
- [ ] [Flow2]: Test [error recovery]

### Performance Testing

**Scope**: Verify performance meets non-functional requirements

**Tools**: pytest-benchmark, locust

**Target Metrics**:
- API response time: [target] (95th percentile)
- Database query time: [target]
- Cache hit rate: [target]

**Test Cases**:
- [ ] Benchmark [operation] performance
- [ ] Load test [endpoint] with [N] concurrent requests

### Security Testing

**Scope**: Verify security controls and OWASP compliance

**Test Cases**:
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output sanitization)
- [ ] CSRF protection (tokens)
- [ ] Authentication bypass attempts
- [ ] Authorization boundary testing
- [ ] Secrets not in logs or responses

### Test Data Management

**Test Fixtures**:
```python
# Shared test fixtures
@pytest.fixture
def sample_user():
    return User(id=1, email="test@example.com", name="Test User")

@pytest.fixture
def mock_database():
    # Create in-memory database for testing
    ...
```

**Test Data Location**: `tests/fixtures/`

### Running Tests

**All Tests**:
```bash
pytest
```

**Unit Tests Only**:
```bash
pytest tests/unit/
```

**Integration Tests Only**:
```bash
pytest tests/integration/
```

**With Coverage**:
```bash
pytest --cov=src --cov-report=html
```

**Coverage Report**: `htmlcov/index.html`

### Continuous Integration

**CI Pipeline** (GitHub Actions / GitLab CI):
1. Run linting (black, mypy)
2. Run unit tests
3. Run integration tests (with test containers)
4. Generate coverage report
5. Fail if coverage < [X]%
```

### Step 10: Document Success Criteria

Use acceptance criteria from analysis and implementation-specific criteria:

**Success Criteria Template**:
```markdown
## Success Criteria

### Acceptance Criteria (from Requirements)

From analysis document (feature-{issue-number}-analysis.md):

- [ ] **AC-001**: [Acceptance criterion from analysis]
- [ ] **AC-002**: [Acceptance criterion from analysis]
- [ ] **AC-003**: [Acceptance criterion from analysis]

### Implementation Criteria

- [ ] **IC-001**: All data models defined with Pydantic validation
- [ ] **IC-002**: All repository CRUD operations implemented with [ORM]
- [ ] **IC-003**: All service methods implemented with error handling
- [ ] **IC-004**: All API endpoints implemented with [Framework]
- [ ] **IC-005**: All library integrations working ([Library1], [Library2])

### Testing Criteria

- [ ] **TC-001**: Unit test coverage ≥ [X]%
- [ ] **TC-002**: All integration tests passing
- [ ] **TC-003**: All end-to-end API tests passing
- [ ] **TC-004**: Performance tests meet targets ([metric] < [target])
- [ ] **TC-005**: Security tests passing (OWASP compliance)

### Code Quality Criteria

- [ ] **QC-001**: Linting passes (black, mypy)
- [ ] **QC-002**: No critical security vulnerabilities (bandit/safety)
- [ ] **QC-003**: Code review approved
- [ ] **QC-004**: All functions have docstrings
- [ ] **QC-005**: Complex logic has explanatory comments

### Documentation Criteria

- [ ] **DC-001**: API endpoints documented (OpenAPI/Swagger)
- [ ] **DC-002**: README updated with new feature
- [ ] **DC-003**: User guide created (if user-facing)
- [ ] **DC-004**: Code comments for complex logic
- [ ] **DC-005**: CHANGELOG updated

### Deployment Criteria

- [ ] **DEP-001**: Feature deployed to staging
- [ ] **DEP-002**: Smoke tests passing in staging
- [ ] **DEP-003**: Feature deployed to production
- [ ] **DEP-004**: Production monitoring dashboards updated
- [ ] **DEP-005**: No critical errors in first 24 hours

### Definition of Done

All of the following must be true:
- ✅ All acceptance criteria met
- ✅ All implementation criteria met
- ✅ All testing criteria met
- ✅ All code quality criteria met
- ✅ All documentation criteria met
- ✅ All deployment criteria met
- ✅ Feature reviewed and approved
- ✅ Feature in production and stable
```

### Step 11: Validate PRP Completeness

Use prp-template.md validation checklist:

**PRP Completeness Checklist**:
- [ ] Header with metadata (date, designer, issue, analysis link)
- [ ] Executive summary (2-3 paragraphs)
- [ ] Requirements reference with key points
- [ ] Architecture design (components, data models, APIs, data flow, error handling)
- [ ] Library documentation (all libraries with examples and best practices)
- [ ] Dependencies (tree, installation, compatibility)
- [ ] Implementation plan (phased with tasks and validation checkpoints)
- [ ] Testing strategy (unit, integration, e2e, performance, security)
- [ ] Documentation requirements (what docs to create)
- [ ] Success criteria (acceptance, implementation, testing, quality, docs, deployment)
- [ ] Risks & mitigations (from synthesis)

### Step 12: Write PRP to File

Save PRP to designated location:

**File Path**: `/docs/implementation/prp/feature-{issue-number}-prp.md`

**Final PRP Structure**:
```markdown
# Product Requirements Prompt: [Feature Name] (Issue #{issue-number})
[Header with metadata]
## Executive Summary
[2-3 paragraphs]
## Requirements Reference
[Key requirements from analysis]
## Architecture Design
[Components, models, APIs, data flow, error handling]
## Library Documentation
[All libraries with examples]
## Dependencies
[Tree, installation, compatibility]
## Implementation Plan
[Phases with tasks and validation]
## Testing Strategy
[Unit, integration, e2e, performance, security]
## Documentation Requirements
[What to document]
## Success Criteria
[Acceptance, implementation, testing, quality, docs, deployment]
## Risks & Mitigations
[From synthesis and analysis]
---
**PRP Complete**: [Date/Time]
**Ready for Phase 3**: Implementation
```

## Best Practices

### 1. Be Comprehensive But Concise
- Include all necessary information
- Avoid redundancy
- Link to other documents for details
- Use examples liberally

### 2. Make It Actionable
- Every section should guide implementer
- Provide code examples
- Specify exact commands
- Define clear validation checkpoints

### 3. Ensure Traceability
- Link requirements to design elements
- Link design to implementation tasks
- Link tasks to test cases
- Link tests to acceptance criteria

### 4. Validate Completeness
- Use prp-template.md checklist
- Verify all required sections present
- Check all links work
- Ensure all code examples valid

### 5. Consider the Implementer
- Write for someone unfamiliar with design discussions
- Provide context and rationale
- Explain trade-offs and decisions
- Anticipate questions

## Resources

### prp-template.md
Complete PRP template with:
- Standard structure
- Section templates
- Markdown formatting
- Validation checklist

### prp-examples.md
Example PRPs showing:
- Simple feature PRP
- Complex feature PRP
- Multi-component PRP
- API-focused PRP
- Data-focused PRP

## Example Usage

See `prp-examples.md` for complete PRP examples.

## Integration

This skill is used by:
- **design-orchestrator** agent during Phase 2: Design & Planning
- Activates automatically when generating PRP from synthesized design
- Output feeds into Phase 3: Implementation (Implementation Specialist)

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when generating PRP documents)
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29