---
name: transaction-expert
version: 3.0.0
description: |
  Transaction 경계 전문가. TransactionManager(단일 Port persist), ReadManager(단일 Query Port findBy/get),
  CommandFacade(2+ Manager persist* 조합), QueryFacade(2+ ReadManager fetch* 조합).
  @Transactional 메서드 단위 필수. @Component 사용. @Service 금지.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, application, transaction, manager, facade, persist, cqrs]
---

# Transaction Expert (트랜잭션 전문가)

## 목적 (Purpose)

Application Layer에서 **트랜잭션 경계를 관리**하는 컴포넌트(Manager, Facade)를 규칙에 맞게 생성합니다.
CQRS 원칙에 따라 Command/Query를 완전 분리하고, Service에서 트랜잭션 책임을 위임합니다.

## 활성화 조건

- `/impl application {feature}` 명령 실행 시 (Manager/Facade 생성)
- `/plan` 실행 후 트랜잭션 설계 시
- manager, facade, @Transactional, persist, readmanager 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 |
|----------|-------------|------|
| TransactionManager | `{Bc}TransactionManager.java` | `application/{bc}/manager/` |
| ReadManager | `{Bc}ReadManager.java` | `application/{bc}/manager/` |
| CommandFacade | `{Bc}CommandFacade.java` | `application/{bc}/facade/` |
| QueryFacade | `{Bc}QueryFacade.java` | `application/{bc}/facade/` |

## 완료 기준 (Acceptance Criteria)

- [ ] CQRS 분리: Command(persist) / Query(read) 완전 분리
- [ ] Manager: 단일 Port만 의존
- [ ] Facade: 2개 이상 Manager 의존 (필수 조건)
- [ ] `@Component` 어노테이션 사용 (`@Service` 금지)
- [ ] `@Transactional` 메서드 단위만 (클래스 레벨 금지)
- [ ] 비즈니스 로직 없음 (순수 조율만)
- [ ] Lombok 금지
- [ ] ArchUnit 테스트 통과

---

## 컴포넌트 선택 기준

```
┌─────────────────────────────────────────────────────────┐
│                    CQRS 분리 원칙                        │
├───────────────────────┬─────────────────────────────────┤
│      COMMAND          │           QUERY                 │
│  (상태 변경)          │       (상태 조회)                │
├───────────────────────┼─────────────────────────────────┤
│  TransactionManager   │        ReadManager              │
│  (단일 Port)          │     (단일 QueryPort)            │
├───────────────────────┼─────────────────────────────────┤
│  CommandFacade        │        QueryFacade              │
│  (2+ Manager)         │     (2+ ReadManager)            │
└───────────────────────┴─────────────────────────────────┘
```

### 언제 무엇을 사용?

| 상황 | 컴포넌트 | 이유 |
|------|----------|------|
| 단일 Aggregate 저장 | TransactionManager | 단일 Port, persist() |
| 단일 데이터 조회 | ReadManager | 단일 QueryPort, findBy/get |
| 여러 Aggregate 저장 (Outbox 포함) | CommandFacade | 2+ Manager 조합 |
| 여러 데이터 조회 조합 | QueryFacade | 2+ ReadManager 조합 |

---

## 코드 템플릿

### 1. TransactionManager (Command - 단일 Port)

```java
package com.ryuqq.application.order.manager;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.ryuqq.application.common.port.out.OrderPersistencePort;
import com.ryuqq.domain.order.aggregate.Order;

@Component
public class OrderTransactionManager {

    private final OrderPersistencePort orderPersistencePort;

    public OrderTransactionManager(OrderPersistencePort orderPersistencePort) {
        this.orderPersistencePort = orderPersistencePort;
    }

    @Transactional
    public Order persist(Order order) {
        return orderPersistencePort.save(order);
    }
}
```

**핵심 규칙**:
- 단일 PersistencePort만 의존
- 메서드명: `persist()` 고정 (save, create 금지)
- `@Transactional` 메서드 레벨
- 비즈니스 로직 없음 - 순수 저장만

### 2. ReadManager (Query - 단일 Port)

```java
package com.ryuqq.application.order.manager;

import java.util.Optional;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.ryuqq.application.common.port.out.OrderQueryPort;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.OrderId;

@Component
public class OrderReadManager {

    private final OrderQueryPort orderQueryPort;

    public OrderReadManager(OrderQueryPort orderQueryPort) {
        this.orderQueryPort = orderQueryPort;
    }

    @Transactional(readOnly = true)
    public Optional<Order> findById(OrderId orderId) {
        return orderQueryPort.findById(orderId);
    }

    @Transactional(readOnly = true)
    public Order getById(OrderId orderId) {
        return orderQueryPort.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }
}
```

**핵심 규칙**:
- 단일 QueryPort만 의존
- 메서드명: `findBy*()` (Optional 반환), `get*()` (예외 던짐)
- `@Transactional(readOnly = true)` 필수
- 비즈니스 로직 없음 - 순수 조회만

### 3. CommandFacade (2+ Manager 조합)

```java
package com.ryuqq.application.order.facade;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.ryuqq.application.order.manager.OrderTransactionManager;
import com.ryuqq.application.order.manager.OrderHistoryTransactionManager;
import com.ryuqq.application.outbox.manager.OutboxTransactionManager;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.aggregate.OrderHistory;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.outbox.aggregate.OutboxEvent;

@Component
public class OrderCommandFacade {

    private final OrderTransactionManager orderTransactionManager;
    private final OrderHistoryTransactionManager orderHistoryTransactionManager;
    private final OutboxTransactionManager outboxTransactionManager;

    public OrderCommandFacade(
        OrderTransactionManager orderTransactionManager,
        OrderHistoryTransactionManager orderHistoryTransactionManager,
        OutboxTransactionManager outboxTransactionManager
    ) {
        this.orderTransactionManager = orderTransactionManager;
        this.orderHistoryTransactionManager = orderHistoryTransactionManager;
        this.outboxTransactionManager = outboxTransactionManager;
    }

    @Transactional
    public Order persistOrderWithHistoryAndOutbox(
        Order order,
        OrderHistory history,
        OutboxEvent outboxEvent
    ) {
        Order saved = orderTransactionManager.persist(order);
        OrderId assignedId = saved.id();

        orderHistoryTransactionManager.persist(history.withOrderId(assignedId));
        outboxTransactionManager.persist(outboxEvent.withAggregateId(assignedId.value()));

        return saved;
    }
}
```

**핵심 규칙**:
- **2개 이상 TransactionManager 의존 필수**
- 메서드명: `persist*()` (persist + 대상 설명)
- `@Transactional` 메서드 레벨
- 순수 조율만 - 객체 생성 없음 (Factory 책임)

### 4. QueryFacade (2+ ReadManager 조합)

```java
package com.ryuqq.application.order.facade;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.ryuqq.application.order.manager.OrderReadManager;
import com.ryuqq.application.product.manager.ProductReadManager;
import com.ryuqq.application.order.dto.OrderDetailBundle;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.product.aggregate.Product;

@Component
public class OrderQueryFacade {

    private final OrderReadManager orderReadManager;
    private final ProductReadManager productReadManager;

    public OrderQueryFacade(
        OrderReadManager orderReadManager,
        ProductReadManager productReadManager
    ) {
        this.orderReadManager = orderReadManager;
        this.productReadManager = productReadManager;
    }

    @Transactional(readOnly = true)
    public OrderDetailBundle fetchOrderDetail(OrderId orderId) {
        Order order = orderReadManager.getById(orderId);
        Product product = productReadManager.getById(order.productId());

        return new OrderDetailBundle(order, product);
    }
}
```

**핵심 규칙**:
- **2개 이상 ReadManager 의존 필수**
- 메서드명: `fetch*()` (여러 데이터 조합 의미)
- `@Transactional(readOnly = true)` 메서드 레벨
- 반환 타입: `*Bundle` Record (여러 도메인 객체 조합)

### 5. QueryBundle (조합 결과 DTO)

```java
package com.ryuqq.application.order.dto;

import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.product.aggregate.Product;

public record OrderDetailBundle(
    Order order,
    Product product
) {
}
```

---

## Service에서 호출 패턴

### CommandService → Facade/Manager 호출

```java
@Component
public class PlaceOrderService implements PlaceOrderUseCase {

    private final OrderCommandFactory orderCommandFactory;
    private final OrderCommandFacade orderCommandFacade;  // 복잡한 경우
    // 또는
    private final OrderTransactionManager orderTransactionManager;  // 단순한 경우

    // ... 생성자

    @Override
    public OrderResponse execute(PlaceOrderCommand command) {
        // 1. Domain 객체 생성 (Factory)
        OrderBundle bundle = orderCommandFactory.create(command);

        // 2. 저장 (Facade 또는 Manager)
        // 복잡한 경우 (여러 Aggregate)
        Order saved = orderCommandFacade.persistOrderWithHistoryAndOutbox(
            bundle.order(),
            bundle.history(),
            bundle.outboxEvent()
        );
        // 단순한 경우 (단일 Aggregate)
        // Order saved = orderTransactionManager.persist(bundle.order());

        // 3. 응답 조립 (Assembler)
        return orderAssembler.toResponse(saved);
    }
}
```

### QueryService → Facade/Manager 호출

```java
@Component
public class GetOrderDetailService implements GetOrderDetailUseCase {

    private final OrderQueryFacade orderQueryFacade;  // 복잡한 경우
    // 또는
    private final OrderReadManager orderReadManager;  // 단순한 경우
    private final OrderQueryAssembler orderQueryAssembler;

    // ... 생성자

    @Override
    public OrderDetailResponse execute(GetOrderDetailQuery query) {
        // 복잡한 경우 (여러 데이터 조합)
        OrderDetailBundle bundle = orderQueryFacade.fetchOrderDetail(
            new OrderId(query.orderId())
        );
        return orderQueryAssembler.toDetailResponse(bundle);

        // 단순한 경우 (단일 데이터)
        // Order order = orderReadManager.getById(new OrderId(query.orderId()));
        // return orderQueryAssembler.toResponse(order);
    }
}
```

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 설명 |
|------|------|
| `@Component` | `@Service` 아닌 `@Component` 사용 |
| `@Transactional` 메서드 레벨 | 클래스 레벨 금지 |
| Manager: 단일 Port | 1개 Port만 의존 |
| Facade: 2+ Manager | 2개 이상 Manager 필수 |
| persist() | TransactionManager 메서드명 고정 |
| persist*() | CommandFacade 메서드명 prefix |
| findBy*/get*() | ReadManager 메서드명 |
| fetch*() | QueryFacade 메서드명 prefix |
| readOnly=true | Query 계열 Transactional 속성 |

### ❌ PROHIBITED (금지)

| 항목 | 이유 |
|------|------|
| `@Service` 어노테이션 | Manager/Facade는 `@Component` |
| `@Transactional` 클래스 레벨 | 메서드별 제어 불가 |
| 단일 Manager Facade | Facade는 2+ Manager 필수 |
| 비즈니스 로직 | Domain Layer 책임 |
| 객체 생성 | Factory 책임 |
| Lombok | Plain Java 사용 |
| save()/create() | persist() 사용 |
| @Transactional 내 외부 API 호출 | 트랜잭션 오염 방지 |

---

## 패키지 구조

```
application/
└── {bc}/
    ├── manager/
    │   ├── {Bc}TransactionManager.java    # Command
    │   └── {Bc}ReadManager.java           # Query
    ├── facade/
    │   ├── {Bc}CommandFacade.java         # 2+ TransactionManager
    │   └── {Bc}QueryFacade.java           # 2+ ReadManager
    └── dto/
        └── {Bc}Bundle.java                # Facade 반환용
```

---

## 체크리스트 (Output Checklist)

### TransactionManager
- [ ] `@Component` 어노테이션
- [ ] 단일 `*PersistencePort` 의존
- [ ] 생성자 주입 (Lombok 없음)
- [ ] `persist()` 메서드명
- [ ] `@Transactional` 메서드 레벨
- [ ] 비즈니스 로직 없음

### ReadManager
- [ ] `@Component` 어노테이션
- [ ] 단일 `*QueryPort` 의존
- [ ] 생성자 주입 (Lombok 없음)
- [ ] `findBy*()` 또는 `get*()` 메서드명
- [ ] `@Transactional(readOnly = true)` 메서드 레벨
- [ ] 비즈니스 로직 없음

### CommandFacade
- [ ] `@Component` 어노테이션
- [ ] **2개 이상** TransactionManager 의존
- [ ] 생성자 주입 (Lombok 없음)
- [ ] `persist*()` 메서드명
- [ ] `@Transactional` 메서드 레벨
- [ ] 순수 조율만 (객체 생성 없음)

### QueryFacade
- [ ] `@Component` 어노테이션
- [ ] **2개 이상** ReadManager 의존
- [ ] 생성자 주입 (Lombok 없음)
- [ ] `fetch*()` 메서드명
- [ ] `@Transactional(readOnly = true)` 메서드 레벨
- [ ] `*Bundle` Record 반환

---

## 테스트 체크리스트

### Manager/Facade 단위 테스트
- [ ] persist/read 호출 검증
- [ ] Port/Manager 위임 확인
- [ ] 예외 전파 확인

### ArchUnit 테스트
- [ ] `@Component` 어노테이션 검증
- [ ] `@Service` 금지 검증
- [ ] `@Transactional` 메서드 레벨 검증
- [ ] 메서드명 패턴 검증 (persist, findBy, get, fetch)
- [ ] 의존성 규칙 검증 (단일 Port / 2+ Manager)

---

## 참조 문서

- **Transaction Manager Guide**: `docs/coding_convention/03-application-layer/manager/command/transaction-manager-guide.md`
- **Read Manager Guide**: `docs/coding_convention/03-application-layer/manager/query/read-manager-guide.md`
- **Command Facade Guide**: `docs/coding_convention/03-application-layer/facade/command/facade-guide.md`
- **Query Facade Guide**: `docs/coding_convention/03-application-layer/facade/query/query-facade-guide.md`
- **Transaction ArchUnit**: `docs/coding_convention/03-application-layer/manager/transaction-manager-archunit.md`
- **Facade ArchUnit**: `docs/coding_convention/03-application-layer/facade/facade-archunit.md`
