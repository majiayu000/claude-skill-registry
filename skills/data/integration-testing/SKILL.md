---
name: integration-testing
description: Design and implement integration tests that verify component interactions, API endpoints, database operations, and external service communication. Use for integration test, API test, end-to-end component testing, and service layer validation.
---

# Integration Testing

## Overview

Integration testing validates that different components, modules, or services work correctly together. Unlike unit tests that isolate single functions, integration tests verify the interactions between multiple parts of your system including databases, APIs, external services, and infrastructure.

## When to Use

- Testing API endpoints with real database connections
- Verifying service-to-service communication
- Validating data flow across multiple layers
- Testing repository/DAO layer with actual databases
- Checking authentication and authorization flows
- Verifying message queue consumers and producers
- Testing third-party service integrations

## Instructions

### 1. **API Integration Testing**

#### Express/Node.js with Jest and Supertest
```javascript
// test/api/users.integration.test.js
const request = require('supertest');
const app = require('../../src/app');
const { setupTestDB, teardownTestDB } = require('../helpers/db');

describe('User API Integration Tests', () => {
  beforeAll(async () => {
    await setupTestDB();
  });

  afterAll(async () => {
    await teardownTestDB();
  });

  beforeEach(async () => {
    await clearUsers();
  });

  describe('POST /api/users', () => {
    it('should create a new user with valid data', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: userData.email,
        name: userData.name
      });
      expect(response.body.password).toBeUndefined();

      // Verify in database
      const user = await User.findById(response.body.id);
      expect(user).toBeTruthy();
      expect(user.email).toBe(userData.email);
    });

    it('should reject duplicate email addresses', async () => {
      const userData = { email: 'test@example.com', name: 'Test', password: 'pass' };

      await request(app).post('/api/users').send(userData).expect(201);

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(409);

      expect(response.body.error).toMatch(/email.*exists/i);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should retrieve user with associated orders', async () => {
      const user = await createTestUser();
      await createTestOrder({ userId: user.id, total: 99.99 });

      const response = await request(app)
        .get(`/api/users/${user.id}`)
        .set('Authorization', `Bearer ${user.token}`)
        .expect(200);

      expect(response.body).toMatchObject({
        id: user.id,
        orders: expect.arrayContaining([
          expect.objectContaining({ total: 99.99 })
        ])
      });
    });
  });
});
```

#### FastAPI/Python with pytest
```python
# tests/integration/test_user_api.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import User
from tests.conftest import test_db

@pytest.mark.asyncio
class TestUserAPI:
    async def test_create_user_integration(
        self,
        client: AsyncClient,
        db: AsyncSession
    ):
        """Test user creation with database persistence."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }

        response = await client.post("/api/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "password" not in data

        # Verify in database
        result = await db.execute(
            select(User).where(User.email == user_data["email"])
        )
        user = result.scalar_one()
        assert user is not None
        assert user.name == user_data["name"]

    async def test_user_with_relationships(
        self,
        client: AsyncClient,
        db: AsyncSession
    ):
        """Test retrieving user with related data."""
        # Setup: Create user with orders
        user = await create_test_user(db)
        await create_test_order(db, user_id=user.id, total=99.99)

        # Test: Fetch user with orders
        response = await client.get(
            f"/api/users/{user.id}",
            headers={"Authorization": f"Bearer {user.token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user.id
        assert len(data["orders"]) == 1
        assert data["orders"][0]["total"] == 99.99
```

### 2. **Database Integration Testing**

#### Spring Boot with JUnit
```java
// src/test/java/com/example/integration/UserRepositoryIntegrationTest.java
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(locations = "classpath:application-test.properties")
class UserRepositoryIntegrationTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private TestEntityManager entityManager;

    @BeforeEach
    void setUp() {
        orderRepository.deleteAll();
        userRepository.deleteAll();
    }

    @Test
    @Transactional
    void testSaveUserWithOrders() {
        // Given
        User user = new User();
        user.setEmail("test@example.com");
        user.setName("Test User");

        Order order1 = new Order();
        order1.setTotal(new BigDecimal("99.99"));
        order1.setUser(user);

        Order order2 = new Order();
        order2.setTotal(new BigDecimal("49.99"));
        order2.setUser(user);

        user.setOrders(Arrays.asList(order1, order2));

        // When
        User savedUser = userRepository.save(user);
        entityManager.flush();
        entityManager.clear();

        // Then
        User foundUser = userRepository.findById(savedUser.getId())
            .orElseThrow();

        assertThat(foundUser.getEmail()).isEqualTo("test@example.com");
        assertThat(foundUser.getOrders()).hasSize(2);
        assertThat(foundUser.getOrders())
            .extracting(Order::getTotal)
            .containsExactlyInAnyOrder(
                new BigDecimal("99.99"),
                new BigDecimal("49.99")
            );
    }

    @Test
    void testCustomQueryWithJoins() {
        // Given
        User user = createTestUser("test@example.com");
        createTestOrder(user, new BigDecimal("150.00"));

        // When
        List<User> highValueUsers = userRepository
            .findUsersWithOrdersAbove(new BigDecimal("100.00"));

        // Then
        assertThat(highValueUsers).hasSize(1);
        assertThat(highValueUsers.get(0).getEmail())
            .isEqualTo("test@example.com");
    }
}
```

### 3. **External Service Integration**

#### Testing with Test Containers
```javascript
// test/integration/payment-service.test.js
const { GenericContainer } = require('testcontainers');
const PaymentService = require('../../src/services/payment');

describe('Payment Service Integration', () => {
  let container;
  let paymentService;

  beforeAll(async () => {
    // Start PostgreSQL container
    container = await new GenericContainer('postgres:14')
      .withEnvironment({
        POSTGRES_DB: 'test',
        POSTGRES_USER: 'test',
        POSTGRES_PASSWORD: 'test'
      })
      .withExposedPorts(5432)
      .start();

    const connectionString = `postgresql://test:test@${container.getHost()}:${container.getMappedPort(5432)}/test`;
    paymentService = new PaymentService(connectionString);
    await paymentService.initialize();
  }, 60000);

  afterAll(async () => {
    await paymentService.close();
    await container.stop();
  });

  test('should process payment and update database', async () => {
    const payment = {
      orderId: 'order-123',
      amount: 99.99,
      currency: 'USD',
      paymentMethod: 'credit_card'
    };

    const result = await paymentService.processPayment(payment);

    expect(result.status).toBe('completed');
    expect(result.transactionId).toBeDefined();

    // Verify in database
    const stored = await paymentService.getPayment(result.id);
    expect(stored.orderId).toBe('order-123');
    expect(stored.status).toBe('completed');
  });
});
```

### 4. **Message Queue Integration**

```python
# tests/integration/test_message_queue.py
import pytest
from unittest.mock import patch
import json

from app.queue import MessageQueue
from app.workers import OrderProcessor

@pytest.mark.integration
class TestMessageQueueIntegration:
    @pytest.fixture
    async def queue(self):
        """Create test message queue."""
        queue = MessageQueue(url=TEST_RABBITMQ_URL)
        await queue.connect()
        yield queue
        await queue.close()

    async def test_publish_and_consume_message(self, queue):
        """Test full message lifecycle."""
        received_messages = []

        async def message_handler(message):
            received_messages.append(message)

        # Subscribe to queue
        await queue.subscribe('orders', message_handler)

        # Publish message
        order_data = {
            'order_id': '123',
            'customer': 'test@example.com',
            'total': 99.99
        }
        await queue.publish('orders', order_data)

        # Wait for message processing
        await asyncio.sleep(0.5)

        assert len(received_messages) == 1
        assert received_messages[0]['order_id'] == '123'

    async def test_order_processing_workflow(self, queue, db):
        """Test complete order processing through queue."""
        processor = OrderProcessor(queue, db)
        await processor.start()

        # Publish order
        order = await create_test_order(db, status='pending')
        await queue.publish('orders.new', {'order_id': order.id})

        # Wait for processing
        await asyncio.sleep(1)

        # Verify order was processed
        await db.refresh(order)
        assert order.status == 'processing'
        assert order.processed_at is not None
```

## Testing Patterns

### Test Data Management

```python
# conftest.py - Shared fixtures
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture(scope="session")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db(engine):
    """Create database session for each test."""
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db):
    """Create test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

## Best Practices

### ✅ DO
- Use real databases in integration tests (in-memory or containers)
- Test actual HTTP requests, not mocked responses
- Verify database state after operations
- Test transaction boundaries and rollbacks
- Include authentication/authorization in tests
- Test error scenarios and edge cases
- Use test containers for isolated environments
- Clean up data between tests

### ❌ DON'T
- Mock database connections in integration tests
- Skip testing error paths
- Leave test data in databases
- Use production databases for testing
- Ignore transaction management
- Test only happy paths
- Share state between tests
- Hardcode URLs or credentials

## Tools

- **Node.js**: Supertest, Jest, Testcontainers
- **Python**: pytest, httpx, pytest-asyncio, Testcontainers
- **Java**: Spring Test, TestContainers, RestAssured
- **Database**: Testcontainers, in-memory DBs (H2, SQLite)
- **Mocking Services**: WireMock, MockServer, Localstack

## Common Patterns

```javascript
// Test helper for database setup
class TestDatabase {
  static async setup() {
    await db.migrate.latest();
  }

  static async teardown() {
    await db.destroy();
  }

  static async clear() {
    const tables = ['orders', 'users', 'products'];
    for (const table of tables) {
      await db(table).truncate();
    }
  }
}

// Factory pattern for test data
class TestDataFactory {
  static async createUser(overrides = {}) {
    const defaults = {
      email: `user-${Date.now()}@test.com`,
      name: 'Test User',
      role: 'customer'
    };
    return await User.create({ ...defaults, ...overrides });
  }

  static async createOrder(userId, overrides = {}) {
    const defaults = {
      userId,
      status: 'pending',
      total: 99.99
    };
    return await Order.create({ ...defaults, ...overrides });
  }
}
```

## Examples

See also: test-data-generation, mocking-stubbing, continuous-testing skills for related testing patterns.
