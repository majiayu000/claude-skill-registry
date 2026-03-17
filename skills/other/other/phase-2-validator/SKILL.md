---
name: phase-2-validator
description: Validates Design Phase completion before advancing to Implementation Phase. Checks functional specifications, database design, and UI/UX design for completeness and technical feasibility.
---

# Phase 2 (Design) Validation Skill

**Purpose**: Automate validation of Design Phase completion before advancing to Implementation Phase.

**When to Use**: When orchestrator or agents need to verify design documents are ready for implementation.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage with new-work directory path
bash .claude/skills/phase-2-validator/execute.sh <new-work-directory>

# With work type specification
bash .claude/skills/phase-2-validator/execute.sh <new-work-dir> <work-type>

# With custom quality gate threshold
bash .claude/skills/phase-2-validator/execute.sh <new-work-dir> Feature 90

# Examples:
bash .claude/skills/phase-2-validator/execute.sh docs/functional-areas/events/new-work/2025-11-03-feature
bash .claude/skills/phase-2-validator/execute.sh docs/functional-areas/checkin/new-work/2025-11-03-bug Bug 70
```

**Parameters**:
- `new-work-directory`: Path to new-work folder containing design documents
- `work-type`: (optional) Feature|Bug|Hotfix|Docs|Refactor (default: Feature)
- `required-percentage`: (optional) Override quality gate threshold

**Script validates**:
- Functional Specification (12 points): Technical Overview, Architecture, Data Models, API Specs, Components, Security, Testing
- Database Design (8 points): ER diagram, table schemas, migration plan, indexes, PostgreSQL types, relationships
- UI/UX Design (8 points): Wireframes, component breakdown, Mantine v7, mobile considerations, accessibility
- Integration (7 points): API endpoints match needs, database supports API, auth flow, state management, no violations

**Exit codes**:
- 0: Validation passed - ready for Implementation Phase
- 1: Validation failed - design incomplete

## Quality Gate Checklist (90% Required for Features)

### Functional Specification (12 points)
- [ ] Technical Overview section present (1 point)
- [ ] Architecture section with Web+API pattern (2 points)
- [ ] Data Models section with DTOs (2 points)
- [ ] API Specifications table present (2 points)
- [ ] Component Specifications defined (2 points)
- [ ] Security Requirements addressed (2 points)
- [ ] Testing Requirements defined (1 point)

### Database Design (8 points)
- [ ] Entity Relationship Diagram present (2 points)
- [ ] Table schemas with PostgreSQL syntax (2 points)
- [ ] Migration plan defined (1 point)
- [ ] Indexes and constraints specified (1 point)
- [ ] Relationships properly defined (1 point)
- [ ] Data types appropriate for PostgreSQL (1 point)

### UI/UX Design (8 points)
- [ ] Wireframes for key screens (2 points)
- [ ] Component breakdown provided (2 points)
- [ ] Mantine v7 components specified (2 points)
- [ ] Mobile responsive considerations (1 point)
- [ ] Accessibility requirements (1 point)

### Integration & Technical Feasibility (7 points)
- [ ] API endpoints match component needs (2 points)
- [ ] Database schema supports API requirements (2 points)
- [ ] Authentication flow defined (1 point)
- [ ] State management approach specified (1 point)
- [ ] No architectural violations (1 point)

**See**: The validation logic is now in `execute.sh` - this maintains single source of truth for the automation.

## Usage Examples

### From Orchestrator
```
Use the phase-2-validator skill to check if design is ready for implementation
```

### Manual Validation
```bash
# Find new-work directory
NEW_WORK_DIR=$(find docs/functional-areas -type d -path "*/new-work/*-*-*" | sort | tail -1)

# Run validation
bash .claude/skills/phase-2-validator.md "$NEW_WORK_DIR"
```

## Common Issues

### Issue: Missing Web+API Architecture
**Solution**: Functional spec must explicitly document:
- Web Service (React + Vite) at localhost:5173
- API Service (Minimal API) at localhost:5655
- No direct database access from Web Service

### Issue: Using SQL Server Syntax
**Solution**: All database designs must use PostgreSQL syntax:
- ✅ `UUID` not `UNIQUEIDENTIFIER`
- ✅ `VARCHAR` not `NVARCHAR`
- ✅ `TIMESTAMP` not `DATETIME2`

### Issue: Missing Mantine v7 Specification
**Solution**: UI design must specify Mantine components:
- `Button`, `TextInput`, `Select`, `Modal`, etc.
- No Material-UI or Chakra references

### Issue: Architectural Violations
**Critical violations that fail validation:**
- Direct database access from Web Service
- References to Razor Pages or Blazor
- SignalR (should use HTTP polling or webhooks)
- Repository pattern over EF Core

## Output Format

```json
{
  "phase": "design",
  "status": "pass|fail",
  "score": 32,
  "maxScore": 35,
  "percentage": 91,
  "requiredPercentage": 90,
  "documents": {
    "functionalSpec": "present",
    "databaseDesign": "present",
    "uiUxDesign": "present"
  },
  "missingItems": [
    "Accessibility requirements not addressed",
    "Mobile wireframes not provided"
  ],
  "architecturalViolations": [],
  "readyForNextPhase": true
}
```

## Integration with Quality Gates

This skill enforces the quality gate thresholds by work type:

- **Feature**: 90% required (32/35 points)
- **Bug Fix**: 70% required (25/35 points)
- **Hotfix**: 60% required (21/35 points)
- **Documentation**: 80% required (28/35 points)
- **Refactoring**: 85% required (30/35 points)

## Progressive Disclosure

**Initial Context**: Show quick document checklist
**On Request**: Show full validation script with scoring
**On Failure**: Show specific missing items and architectural violations
**On Pass**: Show concise summary with score

---

**Remember**: This skill automates design validation but doesn't replace agent judgment. If validation fails, orchestrator should loop back to functional-spec, database-designer, or ui-designer agents.
