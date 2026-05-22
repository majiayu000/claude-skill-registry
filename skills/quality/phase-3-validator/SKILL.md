---
name: phase-3-validator
description: Validates Implementation Phase completion before advancing to Testing Phase. Checks code compilation, test coverage, implementation completeness, and code quality standards.
---

# Phase 3 (Implementation) Validation Skill

**Purpose**: Automate validation of Implementation Phase before advancing to Testing Phase.

**When to Use**: When orchestrator needs to verify implementation is ready for comprehensive testing.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage
bash .claude/skills/phase-3-validator/execute.sh <feature-name> [work-type] [required-percentage]

# Examples:
bash .claude/skills/phase-3-validator/execute.sh events
bash .claude/skills/phase-3-validator/execute.sh vetting Bug 75
bash .claude/skills/phase-3-validator/execute.sh payment-processing Hotfix 70
```

**Parameters**:
- `feature-name`: Name of feature being validated (required)
- `work-type`: Feature|Bug|Hotfix|Docs|Refactor (optional, default: Feature)
- `required-percentage`: Override quality gate threshold (optional)

**Script validates**:
- API and Web build successfully
- Implementation completeness (endpoints, components, migrations, services)
- Code quality (TypeScript, C#, ESLint, error handling)
- Testing infrastructure (unit, integration, E2E tests, fixtures)
- Documentation (implementation notes, API docs, examples, limitations)

**Exit codes**:
- 0: Implementation Phase complete, ready for Testing Phase
- 1: Implementation incomplete or quality gates not met

## Quality Gate Checklist (85% Required for Features)

### Code Compilation (10 points)
- [ ] API builds without errors (5 points)
- [ ] Web builds without errors (5 points)

### Implementation Completeness (15 points)
- [ ] All API endpoints implemented (4 points)
- [ ] All React components created (4 points)
- [ ] Database migrations created (3 points)
- [ ] Service layer implemented (2 points)
- [ ] Type definitions match API (2 points)

### Code Quality (10 points)
- [ ] No TypeScript errors (2 points)
- [ ] No C# warnings (2 points)
- [ ] ESLint passes (2 points)
- [ ] Proper error handling (2 points)
- [ ] Code follows project patterns (2 points)

### Testing Infrastructure (10 points)
- [ ] Unit tests created (3 points)
- [ ] Integration test stubs created (3 points)
- [ ] E2E test files created (2 points)
- [ ] Test data/fixtures prepared (2 points)

### Documentation (5 points)
- [ ] Implementation notes documented (2 points)
- [ ] API endpoints documented (1 point)
- [ ] Component usage examples (1 point)
- [ ] Known limitations noted (1 point)

## Usage Examples

### From Orchestrator
```
Use the phase-3-validator skill to check if implementation is ready for testing
```

### Manual Validation
```bash
# Run validation for specific feature
bash .claude/skills/phase-3-validator.md "event-management"
```

## Common Issues

### Issue: Build Failures
**Critical - Must fix before testing:**
- Compilation errors in API
- TypeScript errors in Web
- Missing dependencies

**Solution**: Loop back to react-developer or backend-developer agents.

### Issue: Missing Test Files
**Solution**: Test files should exist even if not fully implemented:
- Unit tests for services and components
- Integration test stubs for API endpoints
- E2E test files for user workflows

### Issue: Architectural Violations
**Critical violations:**
- Direct database access from Web service
- Using Blazor patterns in React code
- Missing error handling in API endpoints

### Issue: No Type Definitions
**Solution**: After creating API endpoints:
```bash
cd packages/shared-types
npm run generate
```

## First Vertical Slice Checkpoint

**MANDATORY**: After implementing the first vertical slice (one complete feature from UI → API → Database):

1. Run phase-3-validator
2. If score ≥ 85%, **PAUSE for human review**
3. Wait for explicit approval before continuing with remaining features

**Why**: This catches architectural issues early before they propagate to all features.

## Output Format

```json
{
  "phase": "implementation",
  "status": "pass|fail",
  "score": 43,
  "maxScore": 50,
  "percentage": 86,
  "requiredPercentage": 85,
  "compilation": {
    "api": "success",
    "web": "success"
  },
  "codeQuality": {
    "typescriptErrors": 0,
    "csharpWarnings": 2,
    "eslintErrors": 0,
    "architecturalViolations": 0
  },
  "testing": {
    "unitTests": 12,
    "integrationTests": 3,
    "e2eTests": 2
  },
  "missingItems": [
    "Component usage examples",
    "Known limitations not documented"
  ],
  "criticalIssues": [],
  "readyForNextPhase": true,
  "requiresHumanReview": false
}
```

## Integration with Quality Gates

This skill enforces the quality gate thresholds by work type:

- **Feature**: 85% required (43/50 points)
- **Bug Fix**: 75% required (38/50 points)
- **Hotfix**: 70% required (35/50 points)
- **Refactoring**: 90% required (45/50 points)

## Progressive Disclosure

**Initial Context**: Show compilation and critical checks only
**On Request**: Show full validation with all scoring
**On Failure**: Show specific failing items with fix suggestions
**On First Vertical Slice**: Show full report + human review prompt

---

**Remember**: This skill validates implementation quality but doesn't test functionality. That's Phase 4's job. This ensures code is test-ready.
