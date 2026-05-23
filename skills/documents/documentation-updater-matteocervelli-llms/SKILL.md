---
name: documentation-updater
description: Update all project documentation including implementation docs, user
  guides, API docs, and architecture diagrams. Use when finalizing features to ensure
  comprehensive documentation.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Documentation Updater Skill

## Purpose

This skill provides systematic guidance for updating all types of project documentation when finalizing feature implementations, ensuring comprehensive, accurate, and well-structured documentation.

## When to Use

- After feature implementation and validation are complete
- Need to document implementation details
- Creating or updating user guides
- Updating API documentation
- Adding architecture diagrams
- Documenting configuration changes

## Documentation Update Workflow

### 1. Implementation Documentation

**Objective**: Document how the feature was implemented for developers and maintainers.

**Location**: `docs/implementation/issue-<number>-<feature-name>.md`

**Template**:
```markdown
# Implementation: Issue #<number> - <Feature Name>

## Overview
Brief description of what was implemented and why.

## Solution Approach
Detailed explanation of the implementation approach:
- Architecture pattern used (e.g., repository pattern, service layer)
- Key design decisions and rationale
- Trade-offs considered
- Alternative approaches rejected and why

## Architecture

### Component Structure
```
src/tools/feature/
├── __init__.py           # Public API exports
├── models.py             # Data models (Pydantic)
├── interfaces.py         # Abstract interfaces
├── core.py               # Business logic
├── repository.py         # Data access layer
├── validators.py         # Input validation
└── exceptions.py         # Custom exceptions
```

### Data Flow
[Describe how data flows through the system]

### Key Components

#### ComponentName
- **Purpose**: [What it does]
- **Responsibilities**: [What it's responsible for]
- **Dependencies**: [What it depends on]

## Implementation Details

### Models
[Document Pydantic models and their fields]

### Business Logic
[Document core algorithms and workflows]

### Data Access
[Document repository methods and database interactions]

### Validation
[Document validation rules and error handling]

## Security Measures
- **Authentication**: [How auth is handled]
- **Authorization**: [Permission checks implemented]
- **Input Validation**: [Validation at entry points]
- **Output Sanitization**: [XSS prevention measures]
- **Data Protection**: [Encryption, secure storage]
- **Secrets Management**: [How secrets are handled]

## Performance Optimizations
- **Caching**: [Caching strategy if applicable]
- **Database**: [Query optimization, indexing]
- **Async Operations**: [Use of async/await]
- **Resource Management**: [Memory, connections]
- **Response Times**: [Measured response times]

## Testing
- **Unit Test Coverage**: [percentage]%
- **Integration Tests**: [what's covered]
- **Security Tests**: [auth, validation, etc.]
- **Performance Tests**: [benchmarks met]
- **Edge Cases**: [scenarios tested]

## Configuration
Environment variables required:
```bash
FEATURE_API_KEY=your_api_key
FEATURE_TIMEOUT=30
FEATURE_DEBUG=false
```

## Dependencies
New dependencies added:
- `package-name==version`: [reason for dependency]

## Breaking Changes
[List any breaking changes or "None"]

## Migration Notes
[Steps needed to migrate or "None required"]

## Known Issues
- [Issue 1]: [Description and workaround]

## Future Enhancements
- [Enhancement 1]: [Description]

## References
- Original Issue: #<number>
- Pull Request: #<pr-number>
- Related Issues: #<related-issues>
- Design Document: docs/architecture/<design-doc>.md
```

**Actions**:
1. Create implementation doc using template
2. Fill in all sections thoroughly
3. Add code examples where helpful
4. Include diagrams for complex flows
5. Document all security and performance measures

**Deliverable**: Complete implementation documentation

---

### 2. User-Facing Documentation

**Objective**: Update documentation that end users and developers will read to use the feature.

#### README Updates

**Location**: `README.md`

**Check if updates needed**:
- Does the feature change installation steps?
- Does it add new CLI commands?
- Does it change configuration?
- Does it add new user-facing features?

**Actions**:
1. Read current README
2. Identify sections needing updates
3. Add new sections if needed
4. Update code examples
5. Verify all links work

**Example addition**:
```markdown
## New Feature: <Feature Name>

Description of what the feature does.

### Usage

```bash
# Example command
llm-tool feature-command --option value
```

### Configuration

Add to your config file:
```yaml
feature:
  enabled: true
  option: value
```

### Example

```python
from llms.feature import FeatureService

service = FeatureService()
result = service.do_something()
```
```

#### User Guides

**Location**: `docs/guides/<feature-name>-guide.md`

**Create guide for complex features**:
```markdown
# <Feature Name> User Guide

## Introduction
What is this feature and who is it for?

## Getting Started

### Prerequisites
- Requirement 1
- Requirement 2

### Installation
```bash
pip install required-package
```

### Basic Setup
```bash
llm-tool init feature-name
```

## Usage

### Basic Example
```python
# Simple example
from llms.feature import Feature

feature = Feature()
result = feature.process(data)
```

### Advanced Usage

#### Use Case 1: <Scenario>
[Step-by-step instructions]

#### Use Case 2: <Scenario>
[Step-by-step instructions]

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | str | "default" | What it does |

## Troubleshooting

### Common Issues

**Problem**: Error message or issue
**Solution**: How to fix it

## Best Practices
- Practice 1
- Practice 2

## Examples

### Example 1: <Scenario>
Full working example with explanation

### Example 2: <Scenario>
Another complete example

## FAQ

**Q: Question?**
A: Answer.

## References
- API Documentation: [link]
- Implementation: [link]
```

**Deliverable**: User guides for new features

---

### 3. API Documentation

**Objective**: Document API endpoints and interfaces.

#### REST API Documentation

**Location**: `docs/api/<feature-name>-api.md`

**For REST APIs**:
```markdown
# <Feature Name> API

## Base URL
```
https://api.example.com/v1
```

## Authentication
```bash
Authorization: Bearer <token>
```

## Endpoints

### GET /feature/resource

Get a resource.

**Request**:
```http
GET /feature/resource?param=value
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "example",
  "value": 123
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: Resource not found

### POST /feature/resource

Create a resource.

**Request**:
```http
POST /feature/resource
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "example",
  "value": 123
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "example",
  "value": 123,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting
- Rate limit: 100 requests per minute
- Header: `X-RateLimit-Remaining`

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid auth |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
```

#### Python API Documentation

**Update docstrings** to be comprehensive:
```python
def create_feature(
    name: str,
    value: int,
    options: Optional[Dict[str, Any]] = None
) -> Feature:
    """
    Create a new feature resource.

    This function creates a feature with the given name and value,
    applying optional configuration if provided.

    Args:
        name: The feature name (1-100 characters, alphanumeric)
        value: The feature value (must be non-negative)
        options: Optional configuration dict with keys:
            - timeout (int): Request timeout in seconds (default: 30)
            - retry (bool): Whether to retry on failure (default: True)

    Returns:
        Feature: Created feature instance with:
            - id: Auto-generated unique identifier
            - name: The provided name
            - value: The provided value
            - created_at: Timestamp of creation

    Raises:
        ValueError: If name is empty or value is negative
        ValidationError: If options are invalid
        APIError: If API request fails

    Examples:
        Basic usage:
        >>> feature = create_feature("example", 123)
        >>> print(feature.id)
        1

        With options:
        >>> feature = create_feature(
        ...     "example",
        ...     123,
        ...     options={"timeout": 60, "retry": False}
        ... )

    Note:
        Feature names must be unique within the system.
        The function performs input validation before API calls.

    See Also:
        - get_feature(): Retrieve existing feature
        - update_feature(): Modify existing feature
        - delete_feature(): Remove feature
    """
    pass
```

**Deliverable**: Complete API documentation

---

### 4. Architecture Documentation

**Objective**: Document architectural decisions and system design.

**Location**: `docs/architecture/<feature-name>-architecture.md`

**When needed**:
- Complex features with multiple components
- New architectural patterns introduced
- Significant design decisions made

**Template**:
```markdown
# Architecture: <Feature Name>

## Context
Why was this architecture needed?

## Architecture Overview

### System Diagram
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────┐
│  API Layer      │
└──────┬──────────┘
       │
┌──────▼──────────┐
│ Service Layer   │
└──────┬──────────┘
       │
┌──────▼──────────┐
│ Repository      │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Data Store     │
└─────────────────┘
```

### Components

#### API Layer
- **Responsibility**: Handle HTTP requests/responses
- **Technology**: FastAPI/Flask
- **Key Files**: `api/endpoints.py`

#### Service Layer
- **Responsibility**: Business logic
- **Technology**: Pure Python
- **Key Files**: `core.py`

#### Repository Layer
- **Responsibility**: Data access
- **Technology**: SQLAlchemy/File System
- **Key Files**: `repository.py`

## Design Decisions

### Decision 1: <Decision>
**Context**: [Why this decision was needed]
**Options Considered**:
1. Option A: [Description] - Rejected because [reason]
2. Option B: [Description] - **Selected** because [reason]

**Consequences**:
- Positive: [benefit]
- Negative: [trade-off]

### Decision 2: <Decision>
[Same format]

## Data Flow

### Create Flow
```
1. Client sends POST request with data
2. API layer validates request format
3. Service layer validates business rules
4. Repository persists data
5. Response returned to client
```

### Read Flow
[Describe]

## Security Architecture
- Authentication: [mechanism]
- Authorization: [RBAC, ABAC, etc.]
- Data Protection: [encryption, etc.]

## Performance Considerations
- Caching: [strategy]
- Scaling: [horizontal/vertical]
- Bottlenecks: [identified and mitigated]

## Integration Points
- System A: [how it integrates]
- System B: [how it integrates]

## Future Considerations
- Scalability: [how to scale]
- Evolution: [how to extend]
```

**Deliverable**: Architecture documentation with diagrams

---

### 5. Configuration Documentation

**Objective**: Document all configuration options and environment variables.

**Update these files**:
- `README.md`: Configuration section
- `docs/guides/configuration.md`: Detailed config guide
- `.env.example`: Example environment file

**Example `.env.example` update**:
```bash
# Feature Name Configuration
FEATURE_API_KEY=your_api_key_here
FEATURE_TIMEOUT=30  # Request timeout in seconds
FEATURE_CACHE_TTL=3600  # Cache time-to-live in seconds
FEATURE_DEBUG=false  # Enable debug logging
FEATURE_MAX_RETRIES=3  # Maximum retry attempts
```

**Configuration guide**:
```markdown
## Configuration Options

### Required Settings

#### FEATURE_API_KEY
- **Type**: string
- **Required**: Yes
- **Description**: API key for authentication
- **Example**: `sk_live_xxxxxxxxxxxx`
- **Where to get**: [URL to get API key]

### Optional Settings

#### FEATURE_TIMEOUT
- **Type**: integer
- **Required**: No
- **Default**: 30
- **Description**: Request timeout in seconds
- **Valid range**: 1-300

## Configuration Methods

### Environment Variables
```bash
export FEATURE_API_KEY=your_key
```

### Config File
```yaml
# config.yaml
feature:
  api_key: your_key
  timeout: 30
```

### Programmatic
```python
from llms.feature import configure

configure(api_key="your_key", timeout=30)
```
```

**Deliverable**: Complete configuration documentation

---

### 6. TECH-STACK Updates

**Objective**: Document new dependencies added.

**Location**: `TECH-STACK.md`

**Add entries for new dependencies**:
```markdown
### <Feature Name> (Added: YYYY-MM-DD)

**Dependencies**:
- **package-name** (version): [Description of why needed]
  - Purpose: [What it's used for]
  - License: [MIT, Apache, etc.]
  - Alternatives considered: [Other options]

**Security Considerations**:
- Vulnerability scan: [Clean/Issues found]
- Maintenance status: [Active/Inactive]
```

**Deliverable**: Updated TECH-STACK.md

---

## Documentation Checklist

Use this checklist to ensure comprehensive documentation:

### Implementation Documentation
- [ ] Implementation doc created in `docs/implementation/`
- [ ] Solution approach documented
- [ ] Architecture and components described
- [ ] Security measures documented
- [ ] Performance optimizations noted
- [ ] Testing coverage detailed
- [ ] Configuration requirements listed
- [ ] Dependencies documented
- [ ] Breaking changes noted
- [ ] Migration notes provided (if applicable)

### User Documentation
- [ ] README.md updated (if applicable)
- [ ] User guide created (for complex features)
- [ ] Usage examples provided
- [ ] Configuration options documented
- [ ] Troubleshooting section added
- [ ] All code examples tested and working

### API Documentation
- [ ] API endpoints documented (if REST API)
- [ ] Request/response formats shown
- [ ] Error codes documented
- [ ] Authentication documented
- [ ] Rate limiting noted
- [ ] Python API docstrings complete

### Architecture Documentation
- [ ] Architecture doc created (if complex feature)
- [ ] System diagrams included
- [ ] Design decisions documented
- [ ] Data flows described
- [ ] Integration points noted

### Configuration Documentation
- [ ] .env.example updated
- [ ] Configuration guide updated
- [ ] All options documented with types/defaults
- [ ] Configuration methods shown

### Technical Documentation
- [ ] TECH-STACK.md updated (if dependencies added)
- [ ] Dependencies documented with rationale
- [ ] Security considerations noted

### Quality Checks
- [ ] All links tested and working
- [ ] Code examples tested
- [ ] Markdown properly formatted
- [ ] No spelling/grammar errors
- [ ] Version numbers consistent
- [ ] Screenshots current (if applicable)

---

## Best Practices

### Writing Style
- Use clear, concise language
- Write in present tense
- Use active voice
- Avoid jargon where possible
- Define technical terms on first use

### Code Examples
- Test all code examples
- Use realistic, meaningful examples
- Include imports and setup
- Show expected output
- Handle errors in examples

### Organization
- Follow logical structure
- Use consistent heading levels
- Group related content
- Cross-reference related docs
- Maintain table of contents for long docs

### Maintenance
- Date all documentation
- Note version numbers
- Link to issues/PRs
- Mark deprecated features
- Update on changes

---

## Common Documentation Patterns

### Feature Introduction
```markdown
## <Feature Name>

<One-line description>

### Overview
<Paragraph explaining what it does and why it's useful>

### Quick Start
<Minimal example to get started>

### Learn More
- [User Guide](link)
- [API Documentation](link)
- [Examples](link)
```

### Code Example Pattern
```markdown
### Example: <Scenario>

<Brief description of what this example demonstrates>

```python
# Import required modules
from llms.feature import Feature

# Initialize
feature = Feature(option="value")

# Use the feature
result = feature.process(data)

# Handle result
print(result)
```

**Output**:
```
Expected output here
```

**Explanation**: <Walk through key parts of the code>
```

### Troubleshooting Pattern
```markdown
### Common Issues

#### Issue: <Error message or problem>

**Symptoms**:
- What the user sees
- Error messages

**Cause**:
Why this happens

**Solution**:
1. Step to fix
2. Another step
3. Verify it's fixed

**Prevention**:
How to avoid this issue
```

---

## Supporting Resources

Reference materials for documentation:
- Markdown Guide: https://www.markdownguide.org/
- Google Developer Documentation Style Guide
- Write the Docs: https://www.writethedocs.org/

---

## Integration with Deployment Flow

**Input**: Completed, validated feature implementation
**Process**: Systematic documentation of all aspects
**Output**: Comprehensive documentation across all types
**Next Step**: Changelog generation

---

## Example Workflow

```bash
# 1. Create implementation documentation
Write docs/implementation/issue-123-user-auth.md

# 2. Update README if needed
Edit README.md to add authentication section

# 3. Create user guide for complex feature
Write docs/guides/authentication-guide.md

# 4. Update API documentation
Edit docs/api/authentication-api.md

# 5. Document architecture if complex
Write docs/architecture/auth-architecture.md

# 6. Update configuration docs
Edit .env.example to add AUTH_* variables
Edit docs/guides/configuration.md

# 7. Update TECH-STACK.md if dependencies added
Edit TECH-STACK.md to add new auth libraries

# 8. Verify all links work
Check all cross-references and external links

# 9. Test all code examples
Run each code example to ensure they work

# 10. Review checklist
Ensure all items checked off
```

---

## Quality Standards

Documentation is complete when:
- All checklist items verified
- Code examples tested and working
- Links verified
- Markdown properly formatted
- Spelling/grammar checked
- Version numbers consistent
- Cross-references complete
- User perspective considered