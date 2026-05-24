---
name: design-synthesizer
description: Auto-activates when synthesizing outputs from multiple parallel sub-agents
  to create cohesive, integrated design with consistency checking and conflict resolution.
allowed-tools: Read, Write, Edit
---

## Purpose

The **design-synthesizer** skill provides structured methods for integrating outputs from multiple parallel sub-agents into a cohesive design. It ensures consistency across architecture, library documentation, and dependencies while identifying and resolving conflicts or gaps.

## When to Use

This skill auto-activates when you:
- Integrate outputs from multiple parallel sub-agents
- Synthesize architecture design with library documentation
- Align dependencies with architectural requirements
- Check consistency across design documents
- Resolve conflicts between sub-agent outputs
- Identify gaps or missing information in design
- Prepare integrated design for PRP generation

## Provided Capabilities

### 1. Output Integration
- **Load Multiple Documents**: Read and parse outputs from all sub-agents
- **Extract Key Information**: Identify critical design elements from each output
- **Cross-Reference**: Link related elements across different outputs
- **Merge Content**: Combine information into unified design

### 2. Consistency Checking
- **Architecture-Library Alignment**: Verify architecture uses documented library features
- **Data Model Validation**: Ensure data models match library APIs
- **API Contract Verification**: Check API designs align with library patterns
- **Version Compatibility**: Validate library versions match dependency analysis
- **Naming Consistency**: Ensure consistent terminology across outputs

### 3. Conflict Resolution
- **Identify Mismatches**: Find inconsistencies between sub-agent outputs
- **Version Conflicts**: Resolve dependency version incompatibilities
- **Architecture Adjustments**: Modify architecture to meet library constraints
- **Trade-off Analysis**: Document compromises and decisions
- **Priority Resolution**: Apply priority rules for conflicting requirements

### 4. Gap Identification
- **Missing Documentation**: Flag undocumented library features
- **Incomplete Dependencies**: Identify missing or unresolved dependencies
- **Architecture Gaps**: Find components without implementation paths
- **Unresolved Issues**: List conflicts or ambiguities requiring attention

### 5. Coherent Design Narrative
- **Unified Story**: Create cohesive narrative across design elements
- **Traceability**: Link design decisions to requirements
- **Rationale Documentation**: Explain why specific approaches were chosen
- **Implementation Path**: Define clear path from design to code

## Usage Guide

### Step 1: Load Sub-Agent Outputs

Read outputs from all 3 parallel sub-agents:

```bash
# Architecture Designer output
/docs/implementation/design/architecture-{issue-number}.md

# Documentation Researcher output
/docs/implementation/design/libraries-{issue-number}.md

# Dependency Manager output
/docs/implementation/design/dependencies-{issue-number}.md
```

**Parse Each Output**:
- **Architecture**: Components, data models, API contracts, data flow, error handling
- **Libraries**: Library versions, API references, code examples, integration patterns
- **Dependencies**: Dependency tree, versions, compatibility, installation order

### Step 2: Extract Key Information

Create structured summary of each output:

**From Architecture Designer**:
```markdown
### Architecture Summary
**Components**:
- Component A: [Purpose and responsibilities]
- Component B: [Purpose and responsibilities]

**Data Models**:
- Model X: [Fields, validations, relationships]
- Model Y: [Fields, validations, relationships]

**API Contracts**:
- Endpoint 1: [Method, path, request/response]
- Endpoint 2: [Method, path, request/response]

**Data Flow**:
- Flow 1: [Source → Transform → Destination]

**Error Handling**:
- Strategy: [Approach and patterns]
```

**From Documentation Researcher**:
```markdown
### Library Documentation Summary
**Library A (v1.2.3)**:
- Purpose: [What it does]
- Key APIs: [Main functions/classes]
- Code Example: [Integration pattern]
- Best Practices: [Recommended usage]

**Library B (v2.0.0)**:
- Purpose: [What it does]
- Key APIs: [Main functions/classes]
- Code Example: [Integration pattern]
- Known Issues: [Caveats and workarounds]
```

**From Dependency Manager**:
```markdown
### Dependency Summary
**Dependency Tree**:
├── library-a==1.2.3
│   ├── dep-x>=2.0
│   └── dep-y<3.0
└── library-b==2.0.0
    └── dep-z~=1.5

**Conflicts**: [List of version conflicts]
**Resolution**: [How conflicts were resolved]
**Installation Order**: [Sequence of installation]
```

### Step 3: Cross-Reference Design Elements

Map architecture components to libraries and dependencies:

Use `synthesis-guide.md` for detailed cross-referencing methodology.

**Architecture → Libraries Mapping**:
```markdown
### Component A
- **Uses**: Library A (v1.2.3)
- **APIs**: Library A's `ClassX` and `FunctionY`
- **Pattern**: Documented in libraries-{issue-number}.md, section 2.3
- **Code Example**: [Link to example in library docs]

### Data Model X
- **Validation**: Uses Library A's `ValidationMixin`
- **Serialization**: Uses Library B's `Serializer`
- **Storage**: Requires dependency: `database-driver>=3.0`
```

**Libraries → Dependencies Mapping**:
```markdown
### Library A (v1.2.3)
- **Required Dependencies**: dep-x>=2.0, dep-y<3.0
- **Optional Dependencies**: dep-optional (for feature Z)
- **Compatibility**: Python 3.9+
- **Conflicts**: None identified
```

**Cross-Reference Matrix**:
| Component | Library | Version | Dependencies | Documented |
|-----------|---------|---------|--------------|------------|
| Component A | Library A | 1.2.3 | dep-x, dep-y | ✅ |
| Component B | Library B | 2.0.0 | dep-z | ✅ |
| Data Model X | Library A | 1.2.3 | dep-x | ✅ |

### Step 4: Check Consistency

Validate alignment across all outputs:

**Architecture-Library Consistency**:
- ✅ All architecture components reference documented libraries
- ✅ All library APIs used in architecture are documented
- ✅ All data models align with library expectations
- ✅ All API contracts follow library patterns
- ⚠️  Warning: Component C uses undocumented Library API (flag for review)

**Library-Dependency Consistency**:
- ✅ All libraries have resolved dependencies
- ✅ All dependency versions are compatible
- ✅ No circular dependencies detected
- ⚠️  Conflict: Library A requires dep-x>=2.0, but Library B requires dep-x<2.5 (resolved to 2.4.0)

**Naming and Terminology Consistency**:
- ✅ Component names consistent across documents
- ✅ Data model names match architecture diagrams
- ⚠️  Inconsistency: Architecture calls it "UserProfile", libraries call it "Profile" (standardize to "UserProfile")

**Version Consistency**:
- ✅ Library versions match dependency analysis
- ✅ All version constraints satisfied
- ⚠️  Note: Library C has newer version (3.0.0) available, but using 2.8.5 for stability

### Step 5: Resolve Conflicts

Use `synthesis-guide.md` conflict resolution strategies:

**Conflict Type 1: Version Incompatibility**
```markdown
**Conflict**: Library A requires dep-x>=2.0, Library B requires dep-x<2.5
**Analysis**: Both constraints can be satisfied with dep-x==2.4.0
**Resolution**: Pin dep-x to 2.4.0 in requirements
**Trade-off**: Cannot use dep-x 2.5+ features until Library B updates
**Risk**: Low - 2.4.0 is stable and well-tested
```

**Conflict Type 2: Architecture-Library Mismatch**
```markdown
**Conflict**: Architecture designs async API, but Library C only supports sync
**Analysis**: Need to wrap Library C with async adapter or redesign
**Options**:
  1. Use asyncio.to_thread() to wrap Library C (simpler, slight overhead)
  2. Replace Library C with async alternative (more work, better performance)
**Resolution**: Use asyncio.to_thread() wrapper (priority: speed of implementation)
**Trade-off**: 5-10% performance overhead vs. 2-3 days rewrite
**Mitigation**: Profile performance, optimize if needed
```

**Conflict Type 3: Missing Documentation**
```markdown
**Conflict**: Architecture uses Library D feature, but no documentation found
**Analysis**: Feature exists in Library D source code but undocumented
**Resolution**:
  1. Add note in PRP about undocumented feature
  2. Include code example from Library D source
  3. Flag for testing during implementation
**Risk**: Medium - undocumented features may change without notice
**Mitigation**: Pin Library D version, add comprehensive tests
```

### Step 6: Identify Gaps

Document missing information or unresolved issues:

**Gap Analysis**:
```markdown
### Missing Documentation
- Library E's `advanced_feature()` used in architecture but not documented
- Library F's error handling patterns unclear from documentation

### Incomplete Dependencies
- Component G requires database driver, but version not specified
- Testing framework not included in dependency analysis

### Architecture Gaps
- Component H has no implementation path (needs design detail)
- Error handling for API endpoint 3 not specified

### Unresolved Ambiguities
- Data Model Z validation rules conflict with Library requirements
- Performance target not specified for async operations
```

### Step 7: Create Cohesive Design Narrative

Synthesize all information into unified design:

Use `design-patterns.md` for common patterns and structures.

**Synthesized Design Structure**:
```markdown
## Synthesized Design

### Overview
[High-level description of integrated design]

### Component Architecture
[Unified component diagram with library annotations]

**Component A** (uses Library A v1.2.3)
- **Responsibilities**: [What it does]
- **Implementation**: Uses `Library A.ClassX` for [purpose]
- **Dependencies**: dep-x>=2.0, dep-y<3.0
- **Integration**: [How it connects to other components]

**Component B** (uses Library B v2.0.0)
- **Responsibilities**: [What it does]
- **Implementation**: Uses `Library B.ServiceY` for [purpose]
- **Dependencies**: dep-z~=1.5
- **Integration**: [How it connects to other components]

### Data Models (Pydantic Schemas)

**UserProfile Model**
```python
from library_a import ValidationMixin
from pydantic import BaseModel

class UserProfile(BaseModel, ValidationMixin):
    id: int
    name: str
    email: EmailStr  # From library_a
    # ... fields with library-specific validations
```

### API Contracts

**Endpoint 1**: `POST /api/users`
- **Implementation**: Uses Library A's `create_user()` method
- **Request**: UserProfile schema
- **Response**: UserProfile with generated ID
- **Error Handling**: Library A's exceptions mapped to HTTP status codes

### Library Integration Strategy

**Library A (v1.2.3)**: User management and validation
- **Integration Point**: Component A, Data Model UserProfile
- **Code Pattern**: [Example from documentation]
- **Error Handling**: Catch `LibraryAException`, return 400/500

**Library B (v2.0.0)**: Background task processing
- **Integration Point**: Component B
- **Code Pattern**: [Example from documentation]
- **Configuration**: [Settings required]

### Dependency Resolution

**Final Dependency Tree**:
```
library-a==1.2.3
├── dep-x==2.4.0  # Pinned to resolve conflict
├── dep-y==2.8.0
library-b==2.0.0
├── dep-z==1.5.3
└── dep-x==2.4.0  # Shared with library-a
```

**Installation Commands**:
```bash
pip install library-a==1.2.3
pip install library-b==2.0.0
pip install -r requirements.txt
```

### Implementation Path

**Phase 1**: Foundation
1. Install dependencies (in order above)
2. Create data models with Library A validations
3. Set up Library B configuration

**Phase 2**: Core Components
1. Implement Component A using Library A patterns
2. Implement Component B using Library B patterns
3. Test components independently

**Phase 3**: Integration
1. Connect Component A → Component B
2. Implement error handling across components
3. Integration testing

**Phase 4**: Validation
1. Unit tests for each component
2. Integration tests for component interactions
3. Performance testing

### Design Decisions

**Decision 1**: Async Wrapper for Library C
- **Rationale**: Library C only supports sync, but architecture requires async
- **Approach**: Use asyncio.to_thread() wrapper
- **Trade-off**: 5-10% performance overhead vs. 2-3 days to rewrite with async library
- **Risk**: Low - overhead is acceptable for current scale

**Decision 2**: Pin dep-x to 2.4.0
- **Rationale**: Resolve version conflict between Library A and Library B
- **Approach**: Pin to highest compatible version (2.4.0)
- **Trade-off**: Cannot use dep-x 2.5+ features until Library B updates
- **Risk**: Low - 2.4.0 is stable

### Identified Issues

**Issue 1**: Undocumented Library D Feature
- **Description**: Architecture uses Library D's `advanced_feature()`, but not in docs
- **Impact**: Medium - feature may change without notice
- **Mitigation**: Pin Library D version, add comprehensive tests, monitor for updates

**Issue 2**: Component H Implementation Gap
- **Description**: Component H responsibilities defined, but implementation approach unclear
- **Impact**: High - blocks implementation
- **Action Required**: Architecture Designer needs to provide implementation details

### Gaps Requiring Attention

- [ ] Resolve Component H implementation approach
- [ ] Verify Library D's `advanced_feature()` API stability
- [ ] Specify database driver version for Component G
- [ ] Clarify performance targets for async operations
- [ ] Add testing framework to dependency analysis
```

### Step 8: Validate Synthesis Quality

Quality checklist:

**Completeness**:
- ✅ All architecture components mapped to libraries
- ✅ All libraries mapped to dependencies
- ✅ All data models have implementation details
- ✅ All API contracts have library integration notes
- ⚠️  Component H needs more detail

**Consistency**:
- ✅ Terminology consistent across documents
- ✅ Version numbers match everywhere
- ✅ Component names standardized
- ✅ Dependencies resolved without conflicts

**Actionability**:
- ✅ Implementation path is clear and specific
- ✅ Installation commands provided
- ✅ Code patterns documented
- ⚠️  Some gaps flagged for resolution

**Traceability**:
- ✅ Design elements link to requirements
- ✅ Library choices justified
- ✅ Design decisions documented with rationale

## Best Practices

### 1. Start with Overview
- Read all outputs completely before synthesis
- Create summary of each output
- Identify major themes and patterns

### 2. Map Systematically
- Use structured templates for mapping
- Create traceability matrices
- Document every cross-reference

### 3. Validate Early
- Check consistency as you integrate
- Flag issues immediately
- Don't ignore small discrepancies

### 4. Resolve Conflicts Transparently
- Document all conflicts found
- Explain resolution reasoning
- Note trade-offs and risks

### 5. Identify All Gaps
- Missing documentation
- Incomplete specifications
- Unresolved ambiguities
- Assumptions that need validation

### 6. Create Unified Narrative
- Tell coherent story from architecture → libraries → dependencies → implementation
- Link every design element to requirements
- Provide clear implementation path

## Resources

### synthesis-guide.md
Comprehensive guide for synthesizing sub-agent outputs including:
- Cross-referencing methodology
- Consistency checking procedures
- Conflict resolution strategies
- Gap identification techniques
- Quality validation criteria

### design-patterns.md
Common design patterns and structures including:
- Component integration patterns
- Library usage patterns
- Dependency management patterns
- Error handling patterns
- Testing patterns

## Example Usage

### Input (Sub-Agent Outputs)

**Architecture Designer Output**:
```markdown
## Components
- **UserService**: Handles user CRUD operations
- **TaskQueue**: Manages background tasks

## Data Models
- **User**: id, name, email, created_at
- **Task**: id, task_type, status, payload

## APIs
- POST /api/users: Create user
- POST /api/tasks: Queue background task
```

**Documentation Researcher Output**:
```markdown
## Libraries
**SQLAlchemy (v2.0.0)**: ORM for database
- User model: Use `declarative_base()` pattern
- Example: [Code snippet]

**Celery (v5.3.0)**: Background task queue
- Task definition: Use `@app.task` decorator
- Example: [Code snippet]
```

**Dependency Manager Output**:
```markdown
## Dependencies
sqlalchemy==2.0.0
├── greenlet>=2.0
celery==5.3.0
├── kombu>=5.3
└── billiard>=4.0

Conflict: greenlet version (resolved to 2.0.2)
```

### Output (Synthesized Design)

```markdown
## Synthesized Design

### Component Architecture

**UserService** (uses SQLAlchemy v2.0.0)
- **Implementation**: SQLAlchemy `declarative_base()` pattern
- **Dependencies**: sqlalchemy==2.0.0, greenlet==2.0.2
- **Data Model**: User class inherits from SQLAlchemy Base

**TaskQueue** (uses Celery v5.3.0)
- **Implementation**: Celery `@app.task` decorator
- **Dependencies**: celery==5.3.0, kombu>=5.3, billiard>=4.0
- **Integration**: Tasks defined in tasks.py, queued via TaskQueue service

### Data Models (SQLAlchemy + Pydantic)

```python
from sqlalchemy import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id: int
    name: str
    email: str  # With SQLAlchemy validation
    created_at: datetime
```

### Library Integration

**SQLAlchemy**: Use declarative_base() for User model (documented pattern)
**Celery**: Define tasks with @app.task, configure broker in settings

### Dependencies (Resolved)

```
sqlalchemy==2.0.0
├── greenlet==2.0.2  # Pinned to resolve conflict
celery==5.3.0
├── kombu>=5.3
└── billiard>=4.0
```

Installation:
```bash
pip install sqlalchemy==2.0.0 celery==5.3.0
```

### Design Decisions

**Decision**: Pin greenlet to 2.0.2
- **Rationale**: Resolve version conflict between SQLAlchemy and system
- **Risk**: Low
```

## Integration

This skill is used by:
- **design-orchestrator** agent during Phase 2: Design & Planning
- Activates automatically when orchestrator synthesizes sub-agent outputs
- Provides unified design for PRP generation (prp-generator skill)

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when synthesizing sub-agent outputs)
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29