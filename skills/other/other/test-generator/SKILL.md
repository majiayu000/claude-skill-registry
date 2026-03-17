---
name: test-generator
description: 自动生成全面的测试套件，包括单元测试、集成测试和E2E测试，支持Jest、Vitest、pytest、xUnit等。
metadata:
  short-description: 自动生成测试套件
---

# Test Generator Skill

## Description
Generate comprehensive test suites with unit tests, integration tests, mocks, and edge case coverage.

## Trigger
- `/test` command
- User requests test generation
- User needs test coverage

## Prompt

You are a testing expert that creates comprehensive test suites.

### Jest/Vitest Unit Tests (TypeScript)

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './UserService';
import { UserRepository } from './UserRepository';

// Mock the repository
vi.mock('./UserRepository');

describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = new UserRepository() as jest.Mocked<UserRepository>;
    userService = new UserService(mockRepository);
    vi.clearAllMocks();
  });

  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test User' };
      const expectedUser = { id: '123', ...userData, createdAt: new Date() };
      mockRepository.create.mockResolvedValue(expectedUser);

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockRepository.create).toHaveBeenCalledWith(userData);
      expect(mockRepository.create).toHaveBeenCalledTimes(1);
    });

    it('should throw error for duplicate email', async () => {
      // Arrange
      const userData = { email: 'existing@example.com', name: 'Test' };
      mockRepository.create.mockRejectedValue(new Error('DUPLICATE_EMAIL'));

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('DUPLICATE_EMAIL');
    });

    it('should validate email format', async () => {
      // Arrange
      const invalidData = { email: 'invalid-email', name: 'Test' };

      // Act & Assert
      await expect(userService.createUser(invalidData))
        .rejects.toThrow('INVALID_EMAIL');
    });
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const user = { id: '123', email: 'test@example.com', name: 'Test' };
      mockRepository.findById.mockResolvedValue(user);

      const result = await userService.getUserById('123');

      expect(result).toEqual(user);
    });

    it('should return null when user not found', async () => {
      mockRepository.findById.mockResolvedValue(null);

      const result = await userService.getUserById('nonexistent');

      expect(result).toBeNull();
    });
  });
});
```

### pytest (Python)

```python
import pytest
from unittest.mock import Mock, patch
from user_service import UserService

class TestUserService:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def user_service(self, mock_repository):
        return UserService(mock_repository)

    def test_create_user_success(self, user_service, mock_repository):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}
        expected = {"id": "123", **user_data}
        mock_repository.create.return_value = expected

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert result == expected
        mock_repository.create.assert_called_once_with(user_data)

    def test_create_user_duplicate_email(self, user_service, mock_repository):
        mock_repository.create.side_effect = ValueError("DUPLICATE_EMAIL")

        with pytest.raises(ValueError, match="DUPLICATE_EMAIL"):
            user_service.create_user({"email": "existing@example.com"})

    @pytest.mark.parametrize("invalid_email", [
        "invalid",
        "@example.com",
        "test@",
        "",
    ])
    def test_validate_email_invalid(self, user_service, invalid_email):
        with pytest.raises(ValueError, match="INVALID_EMAIL"):
            user_service.create_user({"email": invalid_email, "name": "Test"})
```

### xUnit (C#)

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepository;
    private readonly UserService _userService;

    public UserServiceTests()
    {
        _mockRepository = new Mock<IUserRepository>();
        _userService = new UserService(_mockRepository.Object);
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsUser()
    {
        // Arrange
        var userData = new CreateUserDto { Email = "test@example.com", Name = "Test" };
        var expectedUser = new User { Id = Guid.NewGuid(), Email = userData.Email };
        _mockRepository.Setup(r => r.CreateAsync(It.IsAny<User>()))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _userService.CreateUserAsync(userData);

        // Assert
        Assert.Equal(expectedUser.Email, result.Email);
        _mockRepository.Verify(r => r.CreateAsync(It.IsAny<User>()), Times.Once);
    }

    [Theory]
    [InlineData("")]
    [InlineData("invalid")]
    [InlineData("@example.com")]
    public async Task CreateUser_WithInvalidEmail_ThrowsValidationException(string email)
    {
        var userData = new CreateUserDto { Email = email, Name = "Test" };

        await Assert.ThrowsAsync<ValidationException>(
            () => _userService.CreateUserAsync(userData));
    }
}
```

## Tags
`testing`, `unit-tests`, `integration-tests`, `tdd`, `quality-assurance`

## Compatibility
- Codex: ✅
- Claude Code: ✅
