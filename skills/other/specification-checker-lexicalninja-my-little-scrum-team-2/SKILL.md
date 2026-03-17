---
name: specification-checker
description: Compares code implementation against specifications and requirements. Verifies functional requirements, non-functional requirements, acceptance criteria, and technical specifications are met. Returns structured reports of specification gaps and misalignments.
---

# Specification Checker Skill

## Instructions

1. Review code against provided specifications
2. Check functional requirements coverage
3. Verify non-functional requirements are met
4. Check acceptance criteria
5. Compare technical specifications (architecture, data models, APIs)
6. Identify missing features
7. Identify incorrect implementations
8. Return structured specification alignment reports with:
   - File path and line numbers (if applicable)
   - Requirement ID and description
   - Status (Missing, Incorrect, Partial, Complete)
   - Current implementation (if applicable)
   - Expected implementation
   - Priority (Must-Fix for missing required features)

## Examples

**Input:** Specification requires error handling, code doesn't have it
**Output:**
```markdown
### SPEC-001
- **File**: `api/endpoints.js`
- **Lines**: 45-50
- **Priority**: Must-Fix
- **Requirement**: FR5 - Error handling for all endpoints
- **Status**: Missing
- **Issue**: Endpoint lacks error handling as required by specification
- **Current Code**:
  ```javascript
  app.post('/api/tasks', (req, res) => {
      const task = createTask(req.body);
      res.json(task);
  });
  ```
- **Expected Implementation**:
  ```javascript
  app.post('/api/tasks', async (req, res) => {
      try {
          const task = await createTask(req.body);
          res.json(task);
      } catch (error) {
          res.status(400).json({ error: error.message });
      }
  });
  ```
- **Reason**: Specification FR5 requires all endpoints to have proper error handling
- **Specification Reference**: FR5 - Error handling requirements
```

## Specification Areas to Check

- **Functional Requirements**: All required features implemented
- **Non-Functional Requirements**: Performance, security, accessibility requirements
- **Acceptance Criteria**: Each requirement's acceptance criteria met
- **Technical Specifications**: Architecture matches spec, data models correct, APIs match contracts
- **Edge Cases**: Edge cases from spec are handled
- **Success Criteria**: All success criteria from spec are met
- **Missing Features**: Features required by spec but not implemented
- **Incorrect Implementation**: Features implemented incorrectly
- **Partial Implementation**: Features partially implemented

## Priority Guidelines

- **Must-Fix**: Missing required features, incorrect implementation of required features
- **Should-Fix**: Missing nice-to-have features, partial implementations
- **Nice-to-Have**: Specification improvements, enhancements beyond spec
