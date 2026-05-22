---
name: test-coverage-assistant
description: |
  Evaluate test completeness using the 7 dimensions framework.
  Use when: writing tests, reviewing test coverage, ensuring test quality.
  Keywords: test coverage, completeness, dimensions, 7 dimensions, test quality, 測試覆蓋, 測試完整性, 七維度.
---

# Test Coverage Assistant

> **Language**: English | [繁體中文](../../../locales/zh-TW/skills/claude-code/test-coverage-assistant/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-30
**Applicability**: Claude Code Skills

---

## Purpose

This skill helps evaluate and improve test completeness using the 7 dimensions framework, ensuring comprehensive test coverage for each feature.

## Quick Reference

### The 7 Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│              Test Completeness = 7 Dimensions                │
├─────────────────────────────────────────────────────────────┤
│  1. Happy Path        Normal expected behavior              │
│  2. Boundary          Min/max values, limits                │
│  3. Error Handling    Invalid input, exceptions             │
│  4. Authorization     Role-based access control             │
│  5. State Changes     Before/after verification             │
│  6. Validation        Format, business rules                │
│  7. Integration       Real query verification               │
└─────────────────────────────────────────────────────────────┘
```

### Dimension Summary Table

| # | Dimension | What to Test | Key Question |
|---|-----------|--------------|--------------|
| 1 | **Happy Path** | Valid input → expected output | Does the normal flow work? |
| 2 | **Boundary** | Min/max values, limits | What happens at edges? |
| 3 | **Error Handling** | Invalid input, not found | How do errors behave? |
| 4 | **Authorization** | Role permissions | Who can do what? |
| 5 | **State Changes** | Before/after states | Did the state change correctly? |
| 6 | **Validation** | Format, business rules | Is input validated? |
| 7 | **Integration** | Real DB/API calls | Does the query really work? |

### When to Apply Each Dimension

| Feature Type | Required Dimensions |
|--------------|---------------------|
| CRUD API | 1, 2, 3, 4, 6, 7 |
| Query/Search | 1, 2, 3, 4, 7 |
| State Machine | 1, 3, 4, 5, 6 |
| Validation Logic | 1, 2, 3, 6 |
| Background Job | 1, 3, 5 |
| External Integration | 1, 3, 7 |

## Test Design Checklist

Use this checklist for each feature:

```
Feature: ___________________

□ Happy Path
  □ Valid input produces expected success
  □ Correct data is returned/created
  □ Side effects occur as expected

□ Boundary Conditions
  □ Minimum valid value
  □ Maximum valid value
  □ Empty collection
  □ Single item collection
  □ Large collection (if applicable)

□ Error Handling
  □ Invalid input format
  □ Missing required fields
  □ Duplicate/conflict scenarios
  □ Not found scenarios
  □ External service failure (if applicable)

□ Authorization
  □ Each permitted role tested
  □ Each denied role tested
  □ Unauthenticated access tested
  □ Cross-boundary access tested

□ State Changes
  □ Initial state verified
  □ Final state verified
  □ All valid state transitions tested

□ Validation
  □ Format validation (email, phone, etc.)
  □ Business rule validation
  □ Cross-field validation

□ Integration (if UT uses wildcards)
  □ Query predicates verified
  □ Entity relationships verified
  □ Pagination verified
  □ Sorting/filtering verified
```

## Detailed Guidelines

For complete standards, see:
- [Test Completeness Dimensions](../../../core/test-completeness-dimensions.md)
- [Testing Standards](../../../core/testing-standards.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/test-completeness-dimensions.ai.yaml`

## Examples

### 1. Happy Path

```csharp
[Fact]
public async Task CreateUser_WithValidData_ReturnsSuccess()
{
    // Arrange
    var request = new CreateUserRequest
    {
        Username = "newuser",
        Email = "user@example.com"
    };

    // Act
    var result = await _service.CreateUserAsync(request);

    // Assert
    result.Success.Should().BeTrue();
    result.Data.Username.Should().Be("newuser");
}
```

### 2. Boundary

```csharp
[Theory]
[InlineData(0, false)]      // Below minimum
[InlineData(1, true)]       // Minimum valid
[InlineData(100, true)]     // Maximum valid
[InlineData(101, false)]    // Above maximum
public void ValidateQuantity_BoundaryValues_ReturnsExpected(
    int quantity, bool expected)
{
    var result = _validator.IsValidQuantity(quantity);
    result.Should().Be(expected);
}
```

### 4. Authorization

```csharp
[Fact]
public async Task DeleteUser_AsAdmin_Succeeds()
{
    var adminContext = CreateContext(role: "Admin");
    var result = await _service.DeleteUserAsync(userId, adminContext);
    result.Success.Should().BeTrue();
}

[Fact]
public async Task DeleteUser_AsMember_ReturnsForbidden()
{
    var memberContext = CreateContext(role: "Member");
    var result = await _service.DeleteUserAsync(userId, memberContext);
    result.ErrorCode.Should().Be("FORBIDDEN");
}
```

### 5. State Changes

```csharp
[Fact]
public async Task DisableUser_UpdatesStateCorrectly()
{
    // Arrange
    var user = await CreateEnabledUser();
    user.IsEnabled.Should().BeTrue();  // Verify initial state

    // Act
    await _service.DisableUserAsync(user.Id);

    // Assert
    var updatedUser = await _repository.GetByIdAsync(user.Id);
    updatedUser.IsEnabled.Should().BeFalse();  // Verify final state
}
```

## Authorization Matrix Template

Create a matrix for each feature:

| Operation | Admin | Manager | Member | Guest |
|-----------|-------|---------|--------|-------|
| Create | ✅ | ✅ | ❌ | ❌ |
| Read All | ✅ | ⚠️ Scoped | ❌ | ❌ |
| Update | ✅ | ⚠️ Own dept | ❌ | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ |

Each cell should have a corresponding test case.

## Anti-Patterns to Avoid

- ❌ Testing only happy path
- ❌ Missing authorization tests for multi-role systems
- ❌ Not verifying state changes
- ❌ Using wildcards in UT without corresponding IT
- ❌ Same values for ID and business identifier in test data
- ❌ Testing implementation details instead of behavior

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Testing Standards" section
2. Check for existing test patterns in the codebase
3. If not found, **default to all 7 dimensions**

### First-Time Setup

If no configuration found:

1. Suggest: "This project hasn't configured test completeness requirements. Would you like to customize which dimensions are required?"
2. Suggest documenting in `CONTRIBUTING.md`:

```markdown
## Test Completeness

We use the 7 Dimensions framework for test coverage.

### Required Dimensions by Feature Type
- API endpoints: All 7 dimensions
- Utility functions: Dimensions 1, 2, 3, 6
- Background jobs: Dimensions 1, 3, 5
```

---

## Related Standards

- [Test Completeness Dimensions](../../../core/test-completeness-dimensions.md)
- [Testing Standards](../../../core/testing-standards.md)
- [Testing Guide](../testing-guide/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
