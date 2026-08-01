---
name: definition-of-done
description: Skill from jarosser06/da-vinci
---

# Definition of Done

**Description**: Validate completed work against issue requirements and acceptance criteria. Use when finishing work on an issue to ensure all requirements are met.

## When to Use This Skill

- After implementing a feature or fix
- Before creating a pull request
- When validating work against issue acceptance criteria
- To ensure nothing was missed from the original requirements

## Quick Reference

### Validation Checklist
- All issue requirements implemented
- Acceptance criteria met
- Tests cover new functionality (≥90% coverage)
- Linting passes with zero errors
- Documentation updated if needed
- CHANGELOG.md updated
- No hardcoded values or credentials

## Resource Guides

### 📖 [Issue Validation Guide](resources/validation-guide.md)
Comprehensive guide for validating work against issue requirements and acceptance criteria.

**Use when**: Checking if all issue requirements have been met.

### 📖 [Common Gaps](resources/common-gaps.md)
Common things developers forget when completing issues.

**Use when**: Performing final validation before marking work complete.

## Key Principles

1. **Requirement Traceability**: Every requirement in the issue should be addressed
2. **Acceptance Criteria**: All acceptance criteria must be met
3. **Test Coverage**: New code must be tested (≥90% coverage)
4. **Quality Gates**: All automated checks must pass
5. **Documentation**: User-facing changes documented appropriately

## Validation Process

1. **Fetch Issue Details**: Get full issue description and requirements
2. **Map Requirements**: Identify each requirement and acceptance criterion
3. **Verify Implementation**: Check that each requirement has been implemented
4. **Check Test Coverage**: Ensure tests exist for new functionality
5. **Validate Quality**: Confirm linting and tests pass
6. **Review Documentation**: Ensure docs/CHANGELOG updated if needed
7. **Report Status**: Provide clear summary of what's complete and any gaps

## Output Format

Provide validation results in this format:

```markdown
## Definition of Done Validation

### Issue: #{number} - {title}

#### Requirements Status
- ✅ Requirement 1: Description
- ✅ Requirement 2: Description
- ❌ Requirement 3: Description (Not implemented)

#### Acceptance Criteria
- ✅ Criterion 1
- ✅ Criterion 2

#### Quality Gates
- ✅ Tests pass (90%+ coverage)
- ✅ Linting passes
- ✅ CHANGELOG.md updated
- ⚠️ Documentation needs update

#### Summary
{brief summary of validation results}

#### Action Items (if any)
- Item 1
- Item 2
```
