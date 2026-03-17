---
name: spec-update
description: Use when updating specifications, comparing branches, or ensuring documentation reflects current implementation.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Specification Update Workflow

## When to Use This Skill
- Syncing specs with implementation
- Branch comparison analysis
- Post-implementation documentation update
- Feature spec verification

## Pre-Flight Checklist
- [ ] Identify specification files to update
- [ ] Determine implementation changes
- [ ] Compare current state vs documented state
- [ ] Plan update strategy

## Phase 1: Change Discovery

### Git-Based Discovery
```bash
# Compare branches
git diff main..feature-branch --name-only

# Get detailed diff
git diff main..feature-branch

# List commits with messages
git log main..feature-branch --oneline

# Find files changed since date
git log --since="2024-01-01" --name-only --oneline
```

### Pattern-Based Discovery
```bash
# Find all spec files
find . -name "*.spec.md" -o -name "*-specification.md"

# Find implementation files
grep -r "class.*Command" --include="*.cs" -l

# Cross-reference
grep -r "SaveEmployee" --include="*.md"  # In specs
grep -r "SaveEmployee" --include="*.cs"  # In code
```

## Phase 2: Gap Analysis

### Create Analysis Document
```markdown
# Specification Gap Analysis

## Date: [Date]
## Feature: [Feature Name]

## Implementation Status

| Component | Specified | Implemented | Gap |
|-----------|-----------|-------------|-----|
| Entity: Employee | ✅ | ✅ | None |
| Command: SaveEmployee | ✅ | ✅ | Missing validation doc |
| Query: GetEmployeeList | ✅ | ✅ | Filters not documented |
| Event: OnEmployeeCreated | ❌ | ✅ | Not in spec |

## New Implementations (Not in Spec)
1. `BulkUpdateEmployeeCommand` - Added in PR #123
2. `EmployeeExportQuery` - Added for reporting

## Spec Items Not Implemented
1. `EmployeeArchiveCommand` - Deferred to Phase 2
2. `EmployeeAuditTrail` - Pending requirements

## Documentation Updates Needed
1. Add BulkUpdateEmployeeCommand to spec
2. Document new query filters
3. Add event handler documentation
```

## Phase 3: Specification Update

### Update Checklist
```markdown
## Specification Updates

### Entities
- [ ] Update property list
- [ ] Document new computed properties
- [ ] Add validation rules
- [ ] Update relationships

### Commands
- [ ] Add new commands
- [ ] Update validation rules
- [ ] Document side effects
- [ ] Add error codes

### Queries
- [ ] Document new filters
- [ ] Update response schema
- [ ] Add pagination details

### Events
- [ ] Document entity events
- [ ] List event handlers
- [ ] Describe cross-service effects

### API Endpoints
- [ ] Add new endpoints
- [ ] Update request/response
- [ ] Document auth requirements
```

## Pattern 1: Entity Specification Update

```markdown
# Employee Entity Specification

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| Id | string | Yes | Unique identifier (ULID) |
| FullName | string | Yes | Employee full name (max 200) |
| Email | string | Yes | Email address (unique per company) |
| Status | EmployeeStatus | Yes | Current employment status |
| PhoneNumber | string | No | Contact phone (NEW in v2.1) |

## Computed Properties

| Property | Calculation |
|----------|-------------|
| IsActive | Status == Active && !IsDeleted |
| DisplayName | `{Code} - {FullName}` |

## Validation Rules

1. FullName: Required, max 200 characters
2. Email: Required, valid email format, unique within company
3. PhoneNumber: Optional, valid phone format (NEW in v2.1)

## Static Expressions

| Expression | Purpose |
|------------|---------|
| UniqueExpr(companyId, userId) | Find unique employee |
| ActiveInCompanyExpr(companyId) | Filter active employees |
| SearchExpr(term) | Full-text search |
```

## Pattern 2: Command Specification Update

```markdown
# SaveEmployeeCommand Specification

## Overview
Creates or updates an employee record.

## Request

```json
{
  "id": "string | null",
  "fullName": "string",
  "email": "string",
  "status": "Active | Inactive | Terminated",
  "phoneNumber": "string | null"
}
```

## Validation

| Field | Rule | Error Code |
|-------|------|------------|
| fullName | Required | EMPLOYEE_NAME_REQUIRED |
| fullName | Max 200 chars | EMPLOYEE_NAME_TOO_LONG |
| email | Required | EMPLOYEE_EMAIL_REQUIRED |
| email | Valid format | EMPLOYEE_EMAIL_INVALID |
| email | Unique in company | EMPLOYEE_EMAIL_EXISTS |

## Response

```json
{
  "employee": {
    "id": "string",
    "fullName": "string",
    "email": "string",
    "status": "string"
  }
}
```

## Side Effects

1. **Entity Event**: `PlatformCqrsEntityEvent<Employee>` raised
2. **Cross-Service Sync**: Employee synced to TextSnippet
3. **Notification**: Welcome email sent (create only)

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| EMPLOYEE_NOT_FOUND | 404 | Employee ID not found |
| EMPLOYEE_EMAIL_EXISTS | 400 | Email already in use |
| EMPLOYEE_VALIDATION_FAILED | 400 | Validation error |
```

## Pattern 3: API Endpoint Specification

```markdown
# Employee API Endpoints

## Base URL
`/api/Employee`

## Endpoints

### GET /api/Employee
List employees with filtering and pagination.

**Query Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| searchText | string | Full-text search |
| statuses | array | Filter by status |
| skipCount | int | Pagination offset |
| maxResultCount | int | Page size (max 100) |

**Response**
```json
{
  "items": [...],
  "totalCount": 100
}
```

### POST /api/Employee
Create or update employee.

**Request Body**
See SaveEmployeeCommand specification.

### DELETE /api/Employee/{id}
Soft delete an employee.

**Path Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Employee ID |

**Response**: 204 No Content

## Authentication
All endpoints require authentication.
Use `Authorization: Bearer {token}` header.

## Authorization
| Endpoint | Required Role |
|----------|---------------|
| GET | Employee, Manager, Admin |
| POST | Manager, Admin |
| DELETE | Admin |
```

## Phase 4: Verification

### Cross-Reference Check
```bash
# Verify all commands are documented
for cmd in $(grep -r "class.*Command" --include="*.cs" -l); do
  name=$(grep -o "class [A-Za-z]*Command" "$cmd" | head -1)
  if ! grep -q "$name" docs/specifications/*.md; then
    echo "Missing in spec: $name"
  fi
done
```

### Validation Report
```markdown
# Specification Verification Report

## Date: [Date]
## Verified By: AI

## Summary
- Total Specs: 15
- Up to Date: 12
- Needs Update: 3
- Missing: 0

## Issues Found

### Outdated Specifications
1. **Employee.spec.md**
   - Missing: PhoneNumber property
   - Missing: BulkUpdate command

2. **API-Reference.md**
   - Missing: /export endpoint
   - Outdated: Error codes

## Recommendations
1. Update Employee.spec.md with new properties
2. Add BulkUpdateEmployeeCommand specification
3. Regenerate API reference from OpenAPI
```

## Verification Checklist
- [ ] All implementation changes identified
- [ ] Gap analysis completed
- [ ] Specifications updated
- [ ] Cross-references verified
- [ ] Version numbers updated
- [ ] Change log updated
