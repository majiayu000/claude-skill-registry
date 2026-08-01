---
name: feature-documenter-apettey-battlescope
description: Document new features and their implementations in the BattleScope documentation
  system.
---

# Feature Documenter

Document new features and their implementations in the BattleScope documentation system.

## Purpose

This skill helps you create and maintain comprehensive documentation for new features, ensuring consistency with the established documentation structure and standards.

## When to Use

Invoke this skill when:
- Implementing a new feature
- Completing a major feature enhancement
- Adding a new API endpoint
- Creating a new service or component
- Updating existing feature functionality
- Need to document technical implementation details

## What This Skill Does

1. **Creates Feature Documentation**
   - Generates complete feature specifications
   - Documents API endpoints (OpenAPI)
   - Creates frontend specifications
   - Updates product requirements
   - Maintains architecture documentation

2. **Maintains Documentation Consistency**
   - Follows established templates
   - Cross-references related docs
   - Updates multiple documentation layers
   - Keeps documentation synchronized

3. **Tracks Feature Status**
   - Documents implementation status
   - Updates roadmap progress
   - Maintains feature catalog
   - Tracks technical debt

4. **Generates Implementation Summaries**
   - Creates IMPLEMENTATION_SUMMARY.md files
   - Documents key decisions
   - Records challenges and solutions
   - Provides future maintenance guidance

## BattleScope Documentation Structure

### Product Layer (`docs/product-specifications/`)

**Purpose**: Business requirements and user stories

- **features.md**: Complete feature catalog with status
- **requirements.md**: Functional and non-functional requirements
- **user-stories.md**: User personas and workflows
- **roadmap.md**: Future development plans

### Feature Layer (`docs/features/<feature-name>/`)

**Purpose**: Individual feature specifications

Required files:
- **feature-spec.md**: Feature overview, requirements, acceptance criteria
- **openapi-spec.md**: API endpoint specifications (if applicable)
- **frontend-spec.md**: UI/UX specifications (if applicable)
- **IMPLEMENTATION_SUMMARY.md**: Implementation details and decisions

### Technical Layer (`docs/technical-specifications/`)

**Purpose**: System-level technical requirements

- **sla-slo.md**: Service level objectives
- **observability.md**: Logging, metrics, tracing
- **infrastructure.md**: Resource requirements
- **security.md**: Security architecture

### Architecture Layer (`docs/`)

**Purpose**: System architecture and design

- **architecture.md**: Complete system architecture
- **DOCUMENTATION_SUMMARY.md**: Overall documentation status

## Feature Documentation Templates

### Location
Feature-specific docs go in: `docs/features/<feature-name>/`

### Required Structure

```
docs/features/<feature-name>/
├── feature-spec.md          # Main specification
├── openapi-spec.md          # API endpoints (if backend)
├── frontend-spec.md         # UI specifications (if frontend)
└── IMPLEMENTATION_SUMMARY.md # Implementation details
```

## Creating New Feature Documentation

### Step 1: Create Feature Directory

```bash
mkdir -p docs/features/<feature-name>
```

### Step 2: Create Feature Specification

**File**: `docs/features/<feature-name>/feature-spec.md`

**Template Structure**:
```markdown
# <Feature Name> Feature Specification

## Overview
[Brief description of the feature]

## Business Value
[Why this feature matters]

## User Stories
- As a [persona], I want to [action] so that [benefit]

## Requirements

### Functional Requirements
1. [Requirement 1]
2. [Requirement 2]

### Non-Functional Requirements
- Performance: [targets]
- Security: [requirements]
- Usability: [standards]

## Architecture

### Components Affected
- [Component 1]
- [Component 2]

### Data Model
[Database schema changes]

### Dependencies
- [Internal dependencies]
- [External dependencies]

## API Design
[High-level API overview, link to openapi-spec.md]

## UI/UX Design
[High-level UI overview, link to frontend-spec.md]

## Implementation Plan

### Phase 1: [Phase Name]
- [ ] Task 1
- [ ] Task 2

### Phase 2: [Phase Name]
- [ ] Task 3
- [ ] Task 4

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Testing Strategy
- Unit tests: [scope]
- Integration tests: [scope]
- E2E tests: [scope]

## Rollout Plan
[Deployment strategy]

## Monitoring
- Metrics to track
- Alerts to configure
- Dashboard requirements

## Documentation Updates
- [ ] API documentation
- [ ] User documentation
- [ ] Admin documentation

## Future Enhancements
[Planned improvements]

## References
- Related features
- External documentation
```

### Step 3: Create API Specification (If Applicable)

**File**: `docs/features/<feature-name>/openapi-spec.md`

**Template**:
```markdown
# <Feature Name> API Specification

## Base URL
`/api/v1/<feature-path>`

## Authentication
[Auth requirements]

## Endpoints

### GET /<endpoint>
**Description**: [What this endpoint does]

**Authorization**: [Required permissions]

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1    | string | Yes    | Description |

**Response**: 200 OK
```json
{
  "field1": "value",
  "field2": 123
}
```

**Errors**:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found

[Repeat for each endpoint]

## Data Models

### <Model Name>
```typescript
interface Model {
  field1: string;
  field2: number;
}
```

## Rate Limiting
[Rate limit specifications]

## Versioning
[API versioning strategy]
```

### Step 4: Create Frontend Specification (If Applicable)

**File**: `docs/features/<feature-name>/frontend-spec.md`

**Template**:
```markdown
# <Feature Name> Frontend Specification

## Overview
[UI overview]

## Pages/Views

### <View Name>
**Route**: `/path/to/view`

**Purpose**: [What this view does]

**Components**:
- Component1: [purpose]
- Component2: [purpose]

**State Management**:
- [State description]

**Data Fetching**:
- API endpoints used
- Caching strategy
- Error handling

**User Interactions**:
1. User does [action]
2. System responds with [response]

## Components

### <ComponentName>
**Location**: `frontend/src/components/<ComponentName>.tsx`

**Props**:
```typescript
interface Props {
  prop1: string;
  prop2: number;
}
```

**Behavior**: [Component behavior]

## Styling
- Design system: [guidelines]
- Responsive breakpoints: [specifications]

## Accessibility
- ARIA labels
- Keyboard navigation
- Screen reader support

## Performance
- Loading states
- Optimistic updates
- Code splitting

## Testing
- Unit tests: [coverage]
- Integration tests: [scenarios]
```

### Step 5: Create Implementation Summary

**File**: `docs/features/<feature-name>/IMPLEMENTATION_SUMMARY.md`

**Template**:
```markdown
# <Feature Name> Implementation Summary

**Status**: ✅ Completed | ⚠️ In Progress | ❌ Blocked
**Implemented**: YYYY-MM-DD
**Version**: X.Y.Z

## Overview
[What was built]

## Key Implementation Decisions

### Decision 1: [Topic]
**Context**: [Why this decision was needed]
**Options Considered**:
1. Option A: [pros/cons]
2. Option B: [pros/cons]

**Decision**: [What we chose]
**Rationale**: [Why we chose it]

## Implementation Details

### Backend Changes
**Files Modified**:
- `path/to/file.ts`: [changes]
- `path/to/another.ts`: [changes]

**New Dependencies**:
- package-name@version: [purpose]

**Database Changes**:
- Tables added/modified
- Migrations applied

### Frontend Changes
**Files Modified**:
- `frontend/src/path/file.tsx`: [changes]

**New Components**:
- ComponentName: [purpose]

**State Management**:
- [How state is managed]

### Infrastructure Changes
- Kubernetes manifests updated
- New environment variables
- Resource adjustments

## Challenges Encountered

### Challenge 1
**Problem**: [Description]
**Solution**: [How it was solved]
**Lessons Learned**: [Takeaways]

## Testing

### Unit Tests
- Coverage: X%
- Key test cases

### Integration Tests
- Scenarios covered

### Manual Testing
- Test environments
- Edge cases verified

## Performance

### Benchmarks
- API response time: Xms
- UI render time: Xms
- Database query time: Xms

### Optimizations Applied
- [Optimization 1]
- [Optimization 2]

## Security

### Security Considerations
- Authentication/Authorization
- Input validation
- Data encryption

### Security Testing
- Vulnerabilities checked
- Penetration testing results

## Monitoring

### Metrics Added
- metric_name: [description]

### Alerts Configured
- alert_name: [trigger condition]

### Dashboards
- Dashboard name: [link]

## Deployment

### Deployment Steps
1. Step 1
2. Step 2

### Rollback Plan
[How to rollback if needed]

### Post-Deployment Verification
- [ ] Feature works as expected
- [ ] No errors in logs
- [ ] Metrics showing healthy state

## Future Improvements

### Technical Debt
- [Debt item 1]
- [Debt item 2]

### Enhancement Opportunities
- [Enhancement 1]
- [Enhancement 2]

## References
- PRs: #123, #456
- Issues: #789
- Related features: [links]

---

**Author**: [Name]
**Reviewers**: [Names]
**Last Updated**: YYYY-MM-DD
```

## Updating Existing Documentation

### Step 1: Update Feature Catalog

**File**: `docs/product-specifications/features.md`

Add or update the feature entry:
```markdown
### <Feature Name>
**Status**: ✅ Implemented | ⚠️ In Progress | 📋 Planned
**Version**: X.Y.Z
**Documentation**: [feature-spec.md](../features/<feature-name>/feature-spec.md)

[Brief description]

**Key Capabilities**:
- Capability 1
- Capability 2
```

### Step 2: Update Requirements

**File**: `docs/product-specifications/requirements.md`

Add functional requirements under appropriate category (F1-F9):
```markdown
#### F-NEW-01: <Requirement Title>
[Detailed requirement description]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Priority**: High/Medium/Low
**Status**: Implemented/In Progress/Planned
```

### Step 3: Update Architecture Docs

**File**: `docs/architecture.md`

If the feature adds new components:
1. Update component list
2. Add to architecture diagram (Mermaid)
3. Document dependencies
4. Update data flow diagrams if needed

### Step 4: Update Roadmap

**File**: `docs/product-specifications/roadmap.md`

- Move feature from "Planned" to "In Progress" to "Completed"
- Update quarter/milestone information
- Add actual completion date

## Documentation Quality Checklist

Before considering documentation complete:

### Feature Documentation
- [ ] feature-spec.md exists and is complete
- [ ] All requirements documented
- [ ] Acceptance criteria defined
- [ ] Architecture impact documented

### API Documentation (if applicable)
- [ ] openapi-spec.md created
- [ ] All endpoints documented
- [ ] Request/response examples provided
- [ ] Error codes documented
- [ ] Authentication requirements specified

### Frontend Documentation (if applicable)
- [ ] frontend-spec.md created
- [ ] All views/pages documented
- [ ] Component specifications complete
- [ ] User flows documented
- [ ] Accessibility considered

### Implementation
- [ ] IMPLEMENTATION_SUMMARY.md created
- [ ] Key decisions documented
- [ ] Challenges and solutions recorded
- [ ] Testing approach documented
- [ ] Performance metrics included

### Cross-References
- [ ] Feature added to features.md catalog
- [ ] Requirements added/updated in requirements.md
- [ ] Architecture docs updated if needed
- [ ] Roadmap updated with status
- [ ] Related features cross-referenced

### Technical Specifications
- [ ] SLO targets defined (if applicable)
- [ ] Monitoring requirements specified
- [ ] Security considerations documented
- [ ] Resource requirements estimated

## Documentation Maintenance Workflow

### When Starting a Feature

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/<feature-name>
   ```

2. **Create Feature Specification**
   ```bash
   mkdir -p docs/features/<feature-name>
   # Create feature-spec.md with requirements
   ```

3. **Update Product Documentation**
   - Add to features.md (status: "In Progress")
   - Add requirements to requirements.md
   - Update roadmap.md

### During Development

1. **Update Implementation Details**
   - Keep feature-spec.md current with any changes
   - Document decisions in notes

2. **Create API/Frontend Specs**
   - As you build, document the actual implementation
   - Keep specs synchronized with code

### When Completing a Feature

1. **Create Implementation Summary**
   - Document what was actually built
   - Record decisions and challenges
   - Add performance metrics

2. **Update Status**
   - features.md: Change to "✅ Implemented"
   - requirements.md: Mark acceptance criteria complete
   - roadmap.md: Move to completed section

3. **Update Architecture**
   - Add new components to architecture.md
   - Update diagrams if needed

4. **Commit Documentation**
   ```bash
   git add docs/
   git commit -m "docs: complete documentation for <feature-name>"
   ```

## Common Documentation Patterns

### New API Endpoint
Required docs:
1. `docs/features/<feature>/openapi-spec.md` - endpoint specification
2. `docs/product-specifications/requirements.md` - functional requirement
3. Update `docs/architecture.md` if new service

### New Frontend View
Required docs:
1. `docs/features/<feature>/frontend-spec.md` - UI specification
2. `docs/product-specifications/user-stories.md` - user workflows
3. Screenshots/mockups in feature directory

### New Service/Component
Required docs:
1. `docs/features/<service>/feature-spec.md` - service purpose
2. `docs/docker-images/<service>.md` - Docker documentation
3. `docs/architecture.md` - add to component list and diagram
4. `docs/technical-specifications/infrastructure.md` - resource requirements

### Database Schema Change
Required docs:
1. Migration documentation in feature spec
2. Update architecture.md data model section
3. Document in IMPLEMENTATION_SUMMARY.md

## Integration with Other Skills

### Works With `docker-docs-maintainer`
When adding a new service:
1. Use this skill to create feature documentation
2. Use `docker-docs-maintainer` to create Docker image docs

### Works With Code Review
Before PR approval:
1. Check documentation quality checklist
2. Ensure all required docs are created
3. Verify cross-references are correct

## Documentation Style Guidelines

### Language
- Use present tense
- Be concise and specific
- Avoid jargon unless defined
- Use active voice

### Formatting
- Use markdown consistently
- Include code examples in code blocks
- Use tables for structured data
- Use bullet points for lists

### Code Examples
```typescript
// ✅ Good: Complete, runnable example
interface User {
  id: string;
  name: string;
}

function getUser(id: string): User {
  // Implementation
}

// ❌ Bad: Incomplete or pseudo-code
// Get user somehow
user = getUser(id)
```

### Cross-References
```markdown
# ✅ Good: Descriptive link
See the [Authentication specification](../auth/feature-spec.md) for details.

# ❌ Bad: Generic link
See [here](../auth/feature-spec.md).
```

## Troubleshooting

### Documentation Out of Sync
**Problem**: Docs don't match implementation

**Solution**:
1. Review actual code implementation
2. Update specs to match reality
3. Add IMPLEMENTATION_SUMMARY.md to explain discrepancies
4. Mark with TODO if future alignment needed

### Missing Documentation
**Problem**: Feature exists but no documentation

**Solution**:
1. Reverse-engineer documentation from code
2. Interview original developer if possible
3. Create feature-spec.md from actual behavior
4. Create IMPLEMENTATION_SUMMARY.md with known information
5. Mark sections with [Needs Documentation] where unclear

### Unclear Requirements
**Problem**: Feature spec is vague

**Solution**:
1. Look at actual implementation
2. Check user stories and acceptance criteria
3. Test the feature to understand behavior
4. Document actual behavior, not assumptions
5. Flag ambiguities for clarification

## Success Metrics

Documentation is considered high quality when:
- ✅ All required files exist
- ✅ Cross-references are correct
- ✅ Examples are runnable
- ✅ Status indicators are accurate
- ✅ Implementation matches specifications
- ✅ Future developers can understand the feature
- ✅ No orphaned or outdated documentation

## Quick Commands

```bash
# Create new feature documentation
mkdir -p docs/features/<feature-name>
cp docs/features/TEMPLATE_feature-spec.md docs/features/<feature-name>/feature-spec.md

# Find all feature documentation
ls -la docs/features/*/feature-spec.md

# Search for feature status
grep -r "Status:" docs/product-specifications/features.md

# Find incomplete documentation
grep -r "TODO\|FIXME\|TBD" docs/

# Validate documentation structure
find docs/features -type d -mindepth 1 -maxdepth 1 | while read dir; do
  [ ! -f "$dir/feature-spec.md" ] && echo "Missing: $dir/feature-spec.md"
done
```

## Related Documentation

- **Product Specs**: [docs/product-specifications/](../../docs/product-specifications/)
- **Technical Specs**: [docs/technical-specifications/](../../docs/technical-specifications/)
- **Architecture**: [docs/architecture.md](../../docs/architecture.md)
- **Features**: [docs/features/](../../docs/features/)
- **Docker Images**: [docs/docker-images/](../../docs/docker-images/)

## Related Skills

- `docker-docs-maintainer`: For Docker image documentation
- `code-reviewer`: Verify docs match implementation
- `feature-planner`: Plan documentation structure upfront

---

**Last Updated**: 2025-11-12
**Maintained By**: BattleScope Team
**Version**: 1.0
