---
name: integration-test-expert
description: E2E 테스트, Flyway vs @Sql 분리, TestRestTemplate 필수. MockMvc 금지. /kb-integration 명령 시 자동 활성화.
triggers: [/kb-integration, /go, /red, /green, /refactor, /tidy, integration, e2e, testcontainers, flyway]
---

# Integration Testing 전문가

## 핵심 원칙 (Zero-Tolerance)

### ✅ Mandatory
1. **@SpringBootTest(RANDOM_PORT)** - Full Spring context
2. **TestRestTemplate 필수** - MockMvc 금지
3. **Flyway (DDL)** - Schema 관리 (`CREATE TABLE`)
4. **@Sql (DML)** - Test data만 (`INSERT`)
5. **IntegrationTestFixture 필수** - Inline 객체 생성 금지
6. **@Transactional + @Rollback** - Data isolation
7. **@Testcontainers** - Real database (MySQL)

### ❌ Prohibited
1. **DDL in @Sql 금지** - Flyway migration 사용
2. **MockMvc 금지** - TestRestTemplate 사용
3. **@WebMvcTest 금지** - @SpringBootTest 사용
4. **Inline 객체 생성 금지** - IntegrationTestFixture 사용
5. **Flyway 수정 금지** - Test data는 @Sql에
6. **Excessive @MockBean 금지** - Real dependencies 사용
7. **@DirtiesContext 남용 금지** - @Transactional 사용

## 예시

### ✅ CORRECT: E2E Test 패턴
```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@ActiveProfiles("test")
@Testcontainers
@Transactional
@Sql("/sql/orders-test-data.sql")  // Test data (DML)
class OrderIntegrationTest extends IntegrationTestSupport {

    @Test
    void shouldCreateAndGetOrder() {
        // Given - Use Fixture
        PlaceOrderRequest request = PlaceOrderRequestFixture.create();

        // When - 실제 HTTP POST
        ResponseEntity<OrderResponse> response = post(
            "/api/orders",
            request,
            OrderResponse.class
        );

        // Then
        assertCreated(response);
    }
}
```

### ✅ CORRECT: Flyway (DDL) vs @Sql (DML)
```sql
-- ✅ Flyway: V1__create_order_table.sql (DDL)
CREATE TABLE IF NOT EXISTS orders (
    order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ...
);

-- ✅ @Sql: orders-test-data.sql (DML)
INSERT INTO orders (order_id, customer_id, status, ...)
VALUES (100, 1, 'PENDING', ...);

-- ❌ WRONG: No DDL in @Sql
-- CREATE TABLE orders (...);
```

## 참조

- **전체 가이드**: [Integration Testing Overview](../../../docs/coding_convention/05-testing/integration-testing/01_integration-testing-overview.md)
- **상세 규칙 + 템플릿**: [REFERENCE.md](./REFERENCE.md)

## 자동 활성화

`/kb-integration /go|red|green|refactor|tidy` 실행 시 자동 활성화.
