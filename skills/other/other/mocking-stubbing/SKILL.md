---
name: mocking-stubbing
description: Create and manage mocks, stubs, spies, and test doubles for isolating unit tests from external dependencies. Use for mock, stub, spy, test double, Mockito, Jest mocks, and dependency isolation.
---

# Mocking and Stubbing

## Overview

Mocking and stubbing are essential techniques for isolating units of code during testing by replacing dependencies with controlled test doubles. This enables fast, reliable, and focused unit tests that don't depend on external systems like databases, APIs, or file systems.

## When to Use

- Isolating unit tests from external dependencies
- Testing code that depends on slow operations (DB, network)
- Simulating error conditions and edge cases
- Verifying interactions between objects
- Testing code with non-deterministic behavior (time, randomness)
- Avoiding expensive operations in tests
- Testing error handling without triggering real failures

## Test Double Types

- **Stub**: Returns predefined values, no behavior verification
- **Mock**: Verifies interactions (method calls, arguments)
- **Spy**: Wraps real object, allows partial mocking
- **Fake**: Working implementation, but simplified (in-memory DB)
- **Dummy**: Passed but never used (fills parameter lists)

## Instructions

### 1. **Jest Mocking (JavaScript/TypeScript)**

#### Basic Mocking
```typescript
// services/UserService.ts
import { UserRepository } from './UserRepository';
import { EmailService } from './EmailService';

export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(userData: CreateUserDto) {
    const user = await this.userRepository.create(userData);
    await this.emailService.sendWelcomeEmail(user.email, user.name);
    return user;
  }

  async getUserStats(userId: string) {
    const user = await this.userRepository.findById(userId);
    if (!user) throw new Error('User not found');

    const orderCount = await this.userRepository.getOrderCount(userId);
    return { ...user, orderCount };
  }
}

// __tests__/UserService.test.ts
import { UserService } from '../UserService';
import { UserRepository } from '../UserRepository';
import { EmailService } from '../EmailService';

// Mock the dependencies
jest.mock('../UserRepository');
jest.mock('../EmailService');

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();

    // Create mock instances
    mockUserRepository = new UserRepository() as jest.Mocked<UserRepository>;
    mockEmailService = new EmailService() as jest.Mocked<EmailService>;

    userService = new UserService(mockUserRepository, mockEmailService);
  });

  describe('createUser', () => {
    it('should create user and send welcome email', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      };

      const createdUser = {
        id: '123',
        ...userData,
        createdAt: new Date()
      };

      mockUserRepository.create.mockResolvedValue(createdUser);
      mockEmailService.sendWelcomeEmail.mockResolvedValue(undefined);

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toEqual(createdUser);
      expect(mockUserRepository.create).toHaveBeenCalledWith(userData);
      expect(mockUserRepository.create).toHaveBeenCalledTimes(1);
      expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(
        userData.email,
        userData.name
      );
    });

    it('should not send email if user creation fails', async () => {
      // Arrange
      mockUserRepository.create.mockRejectedValue(
        new Error('Database error')
      );

      // Act & Assert
      await expect(
        userService.createUser({ email: 'test@example.com' })
      ).rejects.toThrow('Database error');

      expect(mockEmailService.sendWelcomeEmail).not.toHaveBeenCalled();
    });
  });

  describe('getUserStats', () => {
    it('should return user with order count', async () => {
      // Arrange
      const userId = '123';
      const user = { id: userId, name: 'Test User' };

      mockUserRepository.findById.mockResolvedValue(user);
      mockUserRepository.getOrderCount.mockResolvedValue(5);

      // Act
      const result = await userService.getUserStats(userId);

      // Assert
      expect(result).toEqual({ ...user, orderCount: 5 });
      expect(mockUserRepository.findById).toHaveBeenCalledWith(userId);
      expect(mockUserRepository.getOrderCount).toHaveBeenCalledWith(userId);
    });

    it('should throw error if user not found', async () => {
      // Arrange
      mockUserRepository.findById.mockResolvedValue(null);

      // Act & Assert
      await expect(userService.getUserStats('999')).rejects.toThrow(
        'User not found'
      );

      expect(mockUserRepository.getOrderCount).not.toHaveBeenCalled();
    });
  });
});
```

#### Spying on Functions
```javascript
// services/PaymentService.js
const stripe = require('stripe');

class PaymentService {
  async processPayment(amount, currency, customerId) {
    const charge = await stripe.charges.create({
      amount: amount * 100,
      currency,
      customer: customerId,
    });

    this.logPayment(charge.id, amount);
    return charge;
  }

  logPayment(chargeId, amount) {
    console.log(`Payment processed: ${chargeId} for $${amount}`);
  }
}

// __tests__/PaymentService.test.js
describe('PaymentService', () => {
  let paymentService;
  let stripeMock;

  beforeEach(() => {
    // Mock Stripe module
    stripeMock = {
      charges: {
        create: jest.fn(),
      },
    };
    jest.mock('stripe', () => jest.fn(() => stripeMock));

    paymentService = new PaymentService();
  });

  it('should process payment and log', async () => {
    // Arrange
    const mockCharge = { id: 'ch_123', amount: 5000 };
    stripeMock.charges.create.mockResolvedValue(mockCharge);

    // Spy on internal method
    const logSpy = jest.spyOn(paymentService, 'logPayment');

    // Act
    await paymentService.processPayment(50, 'usd', 'cus_123');

    // Assert
    expect(stripeMock.charges.create).toHaveBeenCalledWith({
      amount: 5000,
      currency: 'usd',
      customer: 'cus_123',
    });
    expect(logSpy).toHaveBeenCalledWith('ch_123', 50);

    logSpy.mockRestore();
  });
});
```

### 2. **Python Mocking with unittest.mock**

```python
# services/order_service.py
from typing import Optional
from repositories.order_repository import OrderRepository
from services.payment_service import PaymentService
from services.notification_service import NotificationService

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_service: PaymentService,
        notification_service: NotificationService
    ):
        self.order_repository = order_repository
        self.payment_service = payment_service
        self.notification_service = notification_service

    def create_order(self, user_id: str, items: list) -> Order:
        """Create and process a new order."""
        order = self.order_repository.create({
            'user_id': user_id,
            'items': items,
            'status': 'pending'
        })

        try:
            payment = self.payment_service.process_payment(
                order.id,
                order.total
            )
            order.status = 'paid'
            order.payment_id = payment.id
            self.order_repository.update(order)

            self.notification_service.send_order_confirmation(
                order.user_id,
                order.id
            )
        except PaymentError as e:
            order.status = 'failed'
            self.order_repository.update(order)
            raise

        return order

# tests/test_order_service.py
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from services.order_service import OrderService
from exceptions import PaymentError

class TestOrderService:
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies."""
        return {
            'order_repository': Mock(),
            'payment_service': Mock(),
            'notification_service': Mock()
        }

    @pytest.fixture
    def order_service(self, mock_dependencies):
        """Create OrderService with mocked dependencies."""
        return OrderService(**mock_dependencies)

    def test_create_order_success(self, order_service, mock_dependencies):
        """Test successful order creation and payment."""
        # Arrange
        user_id = 'user-123'
        items = [{'product_id': 'p1', 'quantity': 2}]

        mock_order = Mock(
            id='order-123',
            total=99.99,
            status='pending',
            user_id=user_id
        )
        mock_payment = Mock(id='payment-123')

        mock_dependencies['order_repository'].create.return_value = mock_order
        mock_dependencies['payment_service'].process_payment.return_value = mock_payment

        # Act
        result = order_service.create_order(user_id, items)

        # Assert
        assert result.status == 'paid'
        assert result.payment_id == 'payment-123'

        mock_dependencies['order_repository'].create.assert_called_once_with({
            'user_id': user_id,
            'items': items,
            'status': 'pending'
        })

        mock_dependencies['payment_service'].process_payment.assert_called_once_with(
            'order-123',
            99.99
        )

        mock_dependencies['notification_service'].send_order_confirmation.assert_called_once_with(
            user_id,
            'order-123'
        )

        assert mock_dependencies['order_repository'].update.call_count == 1

    def test_create_order_payment_failure(self, order_service, mock_dependencies):
        """Test order creation when payment fails."""
        # Arrange
        mock_order = Mock(id='order-123', total=99.99, status='pending')
        mock_dependencies['order_repository'].create.return_value = mock_order
        mock_dependencies['payment_service'].process_payment.side_effect = PaymentError('Card declined')

        # Act & Assert
        with pytest.raises(PaymentError):
            order_service.create_order('user-123', [])

        # Verify order status was updated to failed
        assert mock_order.status == 'failed'
        mock_dependencies['order_repository'].update.assert_called()

        # Notification should not be sent
        mock_dependencies['notification_service'].send_order_confirmation.assert_not_called()

    @patch('services.order_service.datetime')
    def test_order_timestamp(self, mock_datetime, order_service, mock_dependencies):
        """Test order creation with mocked time."""
        # Arrange
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time

        mock_order = Mock(id='order-123', created_at=fixed_time)
        mock_dependencies['order_repository'].create.return_value = mock_order

        # Act
        result = order_service.create_order('user-123', [])

        # Assert
        assert result.created_at == fixed_time
```

### 3. **Mockito for Java**

```java
// service/UserService.java
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final AuditLogger auditLogger;

    public UserService(
        UserRepository userRepository,
        EmailService emailService,
        AuditLogger auditLogger
    ) {
        this.userRepository = userRepository;
        this.emailService = emailService;
        this.auditLogger = auditLogger;
    }

    public User createUser(UserDto userDto) {
        User user = userRepository.save(mapToUser(userDto));
        emailService.sendWelcomeEmail(user.getEmail());
        auditLogger.log("User created: " + user.getId());
        return user;
    }

    public Optional<User> getUserWithOrders(Long userId) {
        return userRepository.findByIdWithOrders(userId);
    }
}

// test/UserServiceTest.java
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @Mock
    private AuditLogger auditLogger;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_shouldSaveAndSendEmail() {
        // Arrange
        UserDto userDto = new UserDto("test@example.com", "Test User");
        User savedUser = new User(1L, "test@example.com", "Test User");

        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(anyString());

        // Act
        User result = userService.createUser(userDto);

        // Assert
        assertNotNull(result);
        assertEquals(1L, result.getId());

        verify(userRepository, times(1)).save(any(User.class));
        verify(emailService, times(1)).sendWelcomeEmail("test@example.com");
        verify(auditLogger, times(1)).log(contains("User created"));
    }

    @Test
    void createUser_shouldThrowExceptionWhenEmailFails() {
        // Arrange
        UserDto userDto = new UserDto("test@example.com", "Test User");
        User savedUser = new User(1L, "test@example.com", "Test User");

        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        doThrow(new EmailException("SMTP error"))
            .when(emailService)
            .sendWelcomeEmail(anyString());

        // Act & Assert
        assertThrows(EmailException.class, () -> {
            userService.createUser(userDto);
        });

        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("test@example.com");
    }

    @Test
    void getUserWithOrders_shouldReturnUserWhenExists() {
        // Arrange
        User user = new User(1L, "test@example.com", "Test User");
        when(userRepository.findByIdWithOrders(1L))
            .thenReturn(Optional.of(user));

        // Act
        Optional<User> result = userService.getUserWithOrders(1L);

        // Assert
        assertTrue(result.isPresent());
        assertEquals(user, result.get());

        verify(userRepository).findByIdWithOrders(1L);
    }

    @Test
    void getUserWithOrders_shouldReturnEmptyWhenNotExists() {
        // Arrange
        when(userRepository.findByIdWithOrders(999L))
            .thenReturn(Optional.empty());

        // Act
        Optional<User> result = userService.getUserWithOrders(999L);

        // Assert
        assertFalse(result.isPresent());
    }

    @Captor
    private ArgumentCaptor<User> userCaptor;

    @Test
    void createUser_shouldSaveUserWithCorrectData() {
        // Arrange
        UserDto userDto = new UserDto("test@example.com", "Test User");
        when(userRepository.save(any(User.class)))
            .thenReturn(new User(1L, "test@example.com", "Test User"));

        // Act
        userService.createUser(userDto);

        // Assert - Capture and verify the saved user
        verify(userRepository).save(userCaptor.capture());
        User capturedUser = userCaptor.getValue();

        assertEquals("test@example.com", capturedUser.getEmail());
        assertEquals("Test User", capturedUser.getName());
    }
}
```

### 4. **Advanced Mocking Patterns**

```typescript
// Mock timers
describe('Scheduled Tasks', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should execute task after delay', () => {
    const callback = jest.fn();
    const scheduler = new TaskScheduler();

    scheduler.scheduleTask(callback, 5000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(5000);

    expect(callback).toHaveBeenCalledTimes(1);
  });
});

// Partial mocking
describe('UserService with partial mocking', () => {
  it('should use real method for validation, mock for DB', async () => {
    const userService = new UserService();

    // Spy on real object
    const saveSpy = jest
      .spyOn(userService.repository, 'save')
      .mockResolvedValue({ id: '123' });

    // Real validation method is used
    await expect(
      userService.createUser({ email: 'invalid' })
    ).rejects.toThrow('Invalid email');

    expect(saveSpy).not.toHaveBeenCalled();

    // Valid data uses mocked save
    await userService.createUser({ email: 'valid@example.com' });
    expect(saveSpy).toHaveBeenCalled();
  });
});
```

## Best Practices

### ✅ DO
- Mock external dependencies (DB, API, file system)
- Use dependency injection for easier mocking
- Verify important interactions with mocks
- Reset mocks between tests
- Mock at the boundary (repositories, services)
- Use spies for partial mocking when needed
- Create reusable mock factories
- Test both success and failure scenarios

### ❌ DON'T
- Mock everything (don't mock what you own)
- Over-specify mock interactions
- Use mocks in integration tests
- Mock simple utility functions
- Create complex mock hierarchies
- Forget to verify mock calls
- Share mocks between tests
- Mock just to make tests pass

## Tools & Libraries

- **JavaScript/TypeScript**: Jest, Sinon.js, ts-mockito
- **Python**: unittest.mock, pytest-mock, responses
- **Java**: Mockito, EasyMock, PowerMock, JMockit
- **C#**: Moq, NSubstitute, FakeItEasy

## Examples

See also: integration-testing, test-data-generation, test-automation-framework for complete testing patterns.
