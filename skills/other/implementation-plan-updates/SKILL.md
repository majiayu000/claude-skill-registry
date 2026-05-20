---
name: implementation-plan-updates
description: Defines the pattern for updating project documentation when completing features. Use when marking features as complete to ensure consistent documentation of implementation status, test coverage, and deliverables.
license: MIT
metadata:
  version: "1.0.0"
  documentation: "project documentation files"
---

# Documentation Updates Pattern

This skill defines how to update project documentation when completing features or milestones.

## Update Locations

### Feature Header

Add completion marker:

```markdown
**Feature: Health Endpoint** ✅ **COMPLETE**
```

### Implementation Notes Section

Add immediately after phase header:

```markdown
**Implementation Notes:**
- Implemented server state tracking with `_server_start_time` and `_server_shutting_down` globals
- Uptime calculated from server start time, rounded to 2 decimal places
- Shutdown state tracked in lifespan context manager
- Timestamp in ISO 8601 format with 'Z' suffix for UTC
```

### Subsection Tests Section

Mark each test as complete:

```markdown
**Subsection Tests** ✅:
- ✅ GET /health returns 200 with status="healthy" when server is running
- ✅ GET /health response includes timestamp in ISO 8601 format
- ✅ GET /health response includes uptime_seconds with 2 decimal precision
- ✅ GET /health response completes within 100ms
- ✅ GET /health returns 503 with status="unhealthy" when shutting down
```

### Test Coverage Section

Update with actual counts:

```markdown
**Test Coverage** ✅:
- **Subsection Tests**: 5 tests implemented and passing
- **Acceptance Criteria**: AC-5.1.1, AC-5.1.2, AC-5.1.3 verified (AC-5.1.4 is for failure case, tested via shutdown)
- **Test File**: `tests/integration/api/test_api_health.py`
```

## Update Pattern by Feature Type

### Core Business Logic

```markdown
**Feature: Data Validation** ✅ **COMPLETE**

**Implementation Notes:**
- Implemented validation layer with input validation
- Added bounds checking with error codes
- Tests cover all validation cases

**Test Coverage**: ✅
- **Tests**: 10 tests implemented
- **Acceptance Criteria**: All requirements verified
- **Test File**: `tests/unit/core/test_validation.py`
```

### Service Layer

```markdown
**Feature: Processing Service** ✅ **COMPLETE**

**Implementation Notes:**
- Implemented processing logic with error handling
- Returns result wrapper with success/error states
- Handles edge cases correctly

**Test Coverage**: ✅
- **Tests**: 10 tests implemented
- **Acceptance Criteria**: All requirements verified
- **Test File**: `tests/unit/services/test_processing.py`
```

### API Endpoints

```markdown
**Feature: Health Endpoint** ✅ **COMPLETE**

**Implementation Notes:**
- Implemented server state tracking
- Uptime calculated from server start time
- Shutdown state tracked in lifespan context manager

**Tests** ✅:
- ✅ Returns 200 with status="healthy" when server is running
- ✅ Response includes timestamp in ISO 8601 format
- ✅ Response includes uptime_seconds with 2 decimal precision
- ✅ Response completes within 100ms
- ✅ Returns 503 with status="unhealthy" when shutting down

**Test Coverage** ✅:
- **Tests**: 5 tests implemented and passing
- **Acceptance Criteria**: All requirements verified
- **Test File**: `tests/integration/api/test_health.py`
```

## Deliverables Section

Update the deliverables section for the milestone:

```markdown
**Milestone Deliverables:**
- ✅ Health endpoint implemented and tested
- ✅ Ready endpoint implemented (if complete)
- ✅ 5 API integration tests passing
- ✅ Error handling with proper HTTP status codes
- ⚠️ Create endpoint (in progress)
- ⚠️ Update endpoint (not started)
```

**Note**: Only mark deliverables as ✅ when fully complete. Use ⚠️ for in-progress items.

## Specification References

Ensure specification references are correct:

```markdown
**Spec References:**
- API Design Specification
- Health and Readiness Endpoints
- HTTP Status Code Mapping
```

## Common Update Patterns

### Adding Implementation Notes

Include:
- Key implementation decisions
- Notable patterns or approaches
- Any deviations from the plan
- Important technical details

### Updating Test Counts

- Count actual tests implemented
- Match test file names
- Note which acceptance criteria are verified
- Mention if some AC are tested indirectly

### Marking Files Complete

```markdown
**Files:**
- `src/api/main.py` ✅ (extended with /health endpoint)
- `tests/integration/api/test_api_health.py` ✅ (created with 5 tests)
```

## Best Practices

1. **Update immediately**: Mark complete right after implementation
2. **Be specific**: Include concrete details in implementation notes
3. **Accurate counts**: Ensure test counts match reality
4. **Check deliverables**: Update deliverables section carefully
5. **Verify AC**: Note which acceptance criteria are covered
6. **File paths**: Use correct relative paths from project root
7. **Consistent format**: Follow established format for consistency

## Common Mistakes to Avoid

### ❌ Don't Mark Unfinished Work

```markdown
**Feature: Create Endpoint** ✅ **COMPLETE**  # WRONG - not implemented yet
```

### ❌ Don't Overcount Tests

```markdown
**Tests**: 10 tests  # WRONG - only 5 were implemented
```

### ❌ Don't Forget Deliverables

```markdown
**Milestone Deliverables:**
- ✅ Health endpoint  # Missing other endpoints status
```

### ✅ Correct Format

```markdown
**Feature: Health Endpoint** ✅ **COMPLETE**

**Implementation Notes:**
- [Specific implementation details]

**Tests** ✅:
- ✅ [List of tests with checkmarks]

**Test Coverage** ✅:
- **Tests**: 5 tests implemented and passing
- **Acceptance Criteria**: All requirements verified
- **Test File**: `tests/integration/api/test_health.py`
```

## Checklist for Updates

When marking a feature complete, ensure:

- [ ] Feature header marked with ✅ **COMPLETE**
- [ ] Implementation Notes section added
- [ ] All tests marked with ✅
- [ ] Test Coverage section updated with actual counts
- [ ] Acceptance Criteria status noted
- [ ] Test file path is correct
- [ ] Deliverables section updated
- [ ] Specification References are accurate
- [ ] File paths in "Files:" section are correct
