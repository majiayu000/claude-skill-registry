---
name: factory-assembler-expert
version: 3.0.0
description: |
  Factory & Assembler 변환 전문가. CommandFactory Command→Domain 변환, QueryFactory Query→Criteria 변환,
  Assembler Domain→Response 변환. PersistBundle 영속화 묶음, QueryBundle 조회 결과 묶음.
  단방향 변환 원칙: Factory는 생성만, Assembler는 조립만. 비즈니스 로직 절대 금지.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, application, factory, assembler, bundle, dto-conversion, cqrs]
---

# Factory & Assembler 전문가

## 목적 (Purpose)

Application Layer에서 **DTO 변환을 담당**하는 컴포넌트(Factory, Assembler)를 규칙에 맞게 생성합니다.
CQRS 원칙에 따라 Command/Query 변환을 분리하고, 단방향 변환 원칙을 준수합니다.

## 활성화 조건

- `/impl application {feature}` 명령 실행 시 (Factory/Assembler 생성)
- `/plan` 실행 후 Application Layer 작업 시
- factory, assembler, bundle, dto 변환 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 |
|----------|-------------|------|
| CommandFactory | `{Bc}CommandFactory.java` | `application/{bc}/factory/command/` |
| QueryFactory | `{Bc}QueryFactory.java` | `application/{bc}/factory/query/` |
| Assembler | `{Bc}Assembler.java` | `application/{bc}/assembler/` |
| PersistBundle | `{Bc}PersistBundle.java` | `application/{bc}/dto/bundle/` |
| QueryBundle | `{Bc}QueryBundle.java` | `application/{bc}/dto/bundle/` |

## 완료 기준 (Acceptance Criteria)

- [ ] Factory: @Component 어노테이션, Port 의존 금지
- [ ] CommandFactory: create*(), createBundle() 메서드 네이밍
- [ ] QueryFactory: createCriteria*() 메서드 네이밍
- [ ] Assembler: toResponse*(), toResponseList() 메서드 네이밍
- [ ] Assembler: toDomain() 메서드 절대 금지
- [ ] Bundle: record 사용, enrichWithId() 메서드
- [ ] 비즈니스 로직 없음 (순수 변환/조립만)
- [ ] Lombok 금지
- [ ] @Transactional 금지
- [ ] ArchUnit 테스트 통과

---

## 컴포넌트 역할 분리

```
┌─────────────────────────────────────────────────────────────────┐
│                    CQRS 변환 컴포넌트                            │
├───────────────────────────────────┬─────────────────────────────┤
│          COMMAND (인바운드)        │       QUERY (아웃바운드)     │
├───────────────────────────────────┼─────────────────────────────┤
│  CommandFactory                   │  QueryFactory               │
│  Command → Domain                 │  Query → Criteria           │
│  create*(), createBundle()        │  createCriteria*()          │
├───────────────────────────────────┼─────────────────────────────┤
│                                   │  Assembler                  │
│                                   │  Domain → Response          │
│                                   │  toResponse*()              │
├───────────────────────────────────┴─────────────────────────────┤
│  ❌ Assembler의 toDomain() 절대 금지!                           │
│  → Command → Domain 변환은 CommandFactory 책임                  │
└─────────────────────────────────────────────────────────────────┘
```

### 컴포넌트별 책임

| 컴포넌트 | 입력 | 출력 | 메서드 | 책임 |
|----------|------|------|--------|------|
| CommandFactory | Command DTO | Domain, PersistBundle | `create*()`, `createBundle()` | Command → Domain 변환 |
| QueryFactory | Query DTO | Criteria | `createCriteria*()` | Query → Criteria 변환 |
| Assembler | Domain | Response DTO | `toResponse*()` | Domain → Response 변환 |
| PersistBundle | - | - | `enrichWithId()` | 영속화 대상 묶음 |
| QueryBundle | - | - | - | 조회 결과 묶음 |

---

## 코드 템플릿

### 1. CommandFactory (Command → Domain 변환)

```java
package com.ryuqq.application.order.factory.command;

import org.springframework.stereotype.Component;

import com.ryuqq.application.order.dto.command.PlaceOrderCommand;
import com.ryuqq.application.order.dto.command.OrderItemCommand;
import com.ryuqq.application.order.dto.bundle.OrderPersistBundle;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.aggregate.OrderItem;
import com.ryuqq.domain.order.vo.CustomerId;
import com.ryuqq.domain.order.vo.Money;
import com.ryuqq.domain.order.vo.ProductId;
import com.ryuqq.domain.order.vo.Quantity;
import com.ryuqq.domain.outbox.OutboxEvent;

import java.util.List;

/**
 * Order Command Factory
 * - Command → Domain 변환
 * - PersistBundle 생성
 * - 비즈니스 로직 없음 (순수 변환)
 */
@Component
public class OrderCommandFactory {

    /**
     * PlaceOrderCommand → Order 변환
     */
    public Order create(PlaceOrderCommand command) {
        List<OrderItem> items = command.items().stream()
            .map(this::createOrderItem)
            .toList();

        return Order.forNew(
            new CustomerId(command.customerId()),
            items
        );
    }

    /**
     * OrderItemCommand → OrderItem 변환
     */
    private OrderItem createOrderItem(OrderItemCommand itemCommand) {
        return OrderItem.forNew(
            new ProductId(itemCommand.productId()),
            new Quantity(itemCommand.quantity()),
            new Money(itemCommand.unitPrice())
        );
    }

    /**
     * PersistBundle 생성 (Order + Outbox)
     * - 영속화에 필요한 객체들을 하나로 묶음
     * - Event ID는 null (Facade에서 Enrichment)
     */
    public OrderPersistBundle createBundle(PlaceOrderCommand command) {
        Order order = create(command);

        OutboxEvent outboxEvent = OutboxEvent.forNew(
            "Order",
            null,  // ID는 Facade에서 할당
            "OrderPlaced",
            order.toEventPayload()
        );

        return new OrderPersistBundle(order, outboxEvent);
    }
}
```

**핵심 규칙**:
- `@Component` 어노테이션 (not @Service)
- `*CommandFactory` 접미사 필수
- `create*()`, `createBundle()` 메서드 네이밍
- `Domain.forNew()` 팩토리 메서드 사용
- Port 의존 금지 (조회 없음)
- 비즈니스 로직 금지 (순수 변환)

### 2. QueryFactory (Query → Criteria 변환)

```java
package com.ryuqq.application.order.factory.query;

import org.springframework.stereotype.Component;

import com.ryuqq.application.order.dto.query.OrderDetailQuery;
import com.ryuqq.application.order.dto.query.OrderSearchQuery;
import com.ryuqq.domain.order.criteria.OrderDetailCriteria;
import com.ryuqq.domain.order.criteria.OrderSearchCriteria;
import com.ryuqq.domain.order.vo.CustomerId;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.order.vo.OrderStatus;

/**
 * Order Query Factory
 * - Query DTO → Domain Criteria 변환
 * - 비즈니스 로직 없음 (순수 변환)
 */
@Component
public class OrderQueryFactory {

    /**
     * OrderSearchQuery → OrderSearchCriteria
     */
    public OrderSearchCriteria createSearchCriteria(OrderSearchQuery query) {
        return OrderSearchCriteria.builder()
            .customerId(query.customerId() != null
                ? new CustomerId(query.customerId())
                : null)
            .status(query.status() != null
                ? OrderStatus.valueOf(query.status())
                : null)
            .fromDate(query.fromDate())
            .toDate(query.toDate())
            .page(query.page())
            .size(query.size())
            .build();
    }

    /**
     * OrderDetailQuery → OrderDetailCriteria
     */
    public OrderDetailCriteria createDetailCriteria(OrderDetailQuery query) {
        return new OrderDetailCriteria(
            new OrderId(query.orderId()),
            query.includeItems(),
            query.includeShipping(),
            query.includePayment()
        );
    }

    /**
     * 단순 ID 기반 Criteria
     */
    public OrderDetailCriteria createByIdCriteria(Long orderId) {
        return new OrderDetailCriteria(
            new OrderId(orderId),
            true,   // includeItems
            true,   // includeShipping
            true    // includePayment
        );
    }
}
```

**핵심 규칙**:
- `@Component` 어노테이션
- `*QueryFactory` 접미사 필수
- `createCriteria*()` 메서드 네이밍
- Domain Criteria 반환 (VO 포함)
- null 안전 처리
- Port 의존 금지

### 3. Assembler (Domain → Response 변환)

```java
package com.ryuqq.application.order.assembler;

import org.springframework.stereotype.Component;

import com.ryuqq.application.order.dto.response.OrderResponse;
import com.ryuqq.application.order.dto.response.OrderDetailResponse;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.aggregate.OrderLineItem;

import java.util.List;

/**
 * Order Assembler - Domain → Response 변환 전용
 *
 * <p>Assembler는 Domain 객체를 Response DTO로 변환하는 단일 책임을 가집니다.</p>
 * <p><strong>Command → Domain 변환은 CommandFactory에서 처리합니다.</strong></p>
 *
 * @see <a href="https://github.com/Sairyss/domain-driven-hexagon">domain-driven-hexagon</a>
 */
@Component
public class OrderAssembler {

    /**
     * Domain → Response 변환
     */
    public OrderResponse toResponse(Order order) {
        return new OrderResponse(
            order.id().value(),
            order.customerId().value(),
            order.totalAmount().value(),
            order.status().name(),
            order.createdAt()
        );
    }

    /**
     * Domain → Detail Response 변환
     */
    public OrderDetailResponse toDetailResponse(Order order) {
        return new OrderDetailResponse(
            order.id().value(),
            order.customerId().value(),
            toLineItems(order.lineItems()),
            order.totalAmount().value(),
            order.status().name(),
            order.createdAt()
        );
    }

    /**
     * LineItem 목록 변환 (private helper)
     */
    private List<OrderDetailResponse.LineItem> toLineItems(List<OrderLineItem> items) {
        return items.stream()
            .map(item -> new OrderDetailResponse.LineItem(
                item.id().value(),
                item.productId().value(),
                item.productName(),
                item.quantity().value(),
                item.unitPrice().value()
            ))
            .toList();
    }

    /**
     * List 변환
     */
    public List<OrderResponse> toResponseList(List<Order> orders) {
        if (orders == null || orders.isEmpty()) {
            return List.of();
        }
        return orders.stream()
            .map(this::toResponse)
            .toList();
    }
}
```

**핵심 규칙**:
- `@Component` 어노테이션
- `*Assembler` 접미사 필수
- `toResponse*()`, `toResponseList()` 메서드 네이밍
- **toDomain() 메서드 절대 금지!**
- Port/Repository 의존 금지 (순수 변환)
- PageResponse 반환 금지 (UseCase 책임)
- Static 메서드 금지

### 4. PersistBundle (영속화 대상 묶음)

```java
package com.ryuqq.application.order.dto.bundle;

import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.aggregate.OrderHistory;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.outbox.OutboxEvent;

/**
 * Order 영속화 Bundle
 * - CommandFactory에서 생성
 * - Facade에서 영속화
 * - enrichWithId()로 ID 할당
 */
public record OrderPersistBundle(
    Order order,
    OrderHistory history,
    OutboxEvent outboxEvent
) {
    /**
     * ID 할당 후 새 Bundle 반환
     * - 불변성 유지
     * - Law of Demeter 준수 (Facade에서 내부 객체 직접 접근 안 함)
     */
    public OrderPersistBundle enrichWithId(OrderId orderId) {
        return new OrderPersistBundle(
            order,
            history.withOrderId(orderId),
            outboxEvent.withAggregateId(orderId.value())
        );
    }
}
```

**핵심 규칙**:
- `record` 사용 (불변성)
- `*PersistBundle` 접미사 필수
- `enrichWithId()` 메서드 제공
- Domain 객체만 포함 (DTO/Response 금지)
- 비즈니스 로직 금지

### 5. QueryBundle (조회 결과 묶음)

```java
package com.ryuqq.application.order.dto.bundle;

import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.member.aggregate.Member;

/**
 * Order 조회 결과 Bundle
 * - QueryFacade에서 생성
 * - Assembler에서 Response 변환
 */
public record OrderDetailQueryBundle(
    Order order,
    Member member
) {
}
```

**핵심 규칙**:
- `record` 사용
- `*QueryBundle` 접미사 필수
- 순수 데이터 객체 (특수 메서드 없음)
- Domain 객체만 포함

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 대상 | 설명 |
|------|------|------|
| `@Component` | Factory, Assembler | Spring Bean 등록 |
| `*CommandFactory` 접미사 | CommandFactory | 네이밍 규칙 |
| `*QueryFactory` 접미사 | QueryFactory | 네이밍 규칙 |
| `*Assembler` 접미사 | Assembler | 네이밍 규칙 |
| `create*()` / `createBundle()` | CommandFactory | 메서드 네이밍 |
| `createCriteria*()` | QueryFactory | 메서드 네이밍 |
| `toResponse*()` / `toResponseList()` | Assembler | 메서드 네이밍 |
| `enrichWithId()` | PersistBundle | ID 할당 메서드 |
| `record` | Bundle | 불변성 보장 |
| `Domain.forNew()` 사용 | CommandFactory | 팩토리 메서드 사용 |

### ❌ PROHIBITED (금지)

| 항목 | 대상 | 이유 |
|------|------|------|
| `@Service` 어노테이션 | Factory, Assembler | @Component 사용 |
| `@Transactional` | 모든 컴포넌트 | Service 책임 |
| `toDomain()` 메서드 | Assembler | **핵심**: CommandFactory 책임 |
| `toCriteria()` 메서드 | Assembler | QueryFactory 책임 |
| Port 의존 | Factory, Assembler | 순수 변환 원칙 |
| Repository 의존 | Factory, Assembler | 순수 변환 원칙 |
| 비즈니스 로직 | 모든 컴포넌트 | Domain 책임 |
| 계산 로직 | Assembler | Domain 책임 |
| PageResponse 반환 | Assembler | UseCase 책임 |
| Static 메서드 | Assembler | 테스트 용이성 |
| Lombok | 모든 컴포넌트 | Plain Java 사용 |
| final 클래스 | Factory, Assembler | Spring Proxy |

---

## 패키지 구조

```
application/
└── {bc}/
    ├── factory/
    │   ├── command/
    │   │   └── {Bc}CommandFactory.java     # Command → Domain
    │   └── query/
    │       └── {Bc}QueryFactory.java       # Query → Criteria
    ├── assembler/
    │   └── {Bc}Assembler.java              # Domain → Response
    └── dto/
        ├── bundle/
        │   ├── {Bc}PersistBundle.java      # 영속화 대상 묶음
        │   └── {Bc}QueryBundle.java        # 조회 결과 묶음
        ├── command/
        │   └── {Action}{Bc}Command.java    # Command DTO
        ├── query/
        │   └── {Bc}{Action}Query.java      # Query DTO
        └── response/
            └── {Bc}Response.java           # Response DTO
```

---

## 체크리스트 (Output Checklist)

### CommandFactory
- [ ] `@Component` 어노테이션
- [ ] `*CommandFactory` 접미사
- [ ] 패키지: `application.{bc}.factory.command`
- [ ] `create*()` 메서드 네이밍
- [ ] `createBundle()` 메서드 (Bundle 필요 시)
- [ ] `Domain.forNew()` 팩토리 메서드 사용
- [ ] 생성자 주입 (Lombok 없음)
- [ ] Port 의존 없음
- [ ] `@Transactional` 없음
- [ ] 비즈니스 로직 없음

### QueryFactory
- [ ] `@Component` 어노테이션
- [ ] `*QueryFactory` 접미사
- [ ] 패키지: `application.{bc}.factory.query`
- [ ] `createCriteria*()` 메서드 네이밍
- [ ] Domain Criteria 반환
- [ ] null 안전 처리
- [ ] 생성자 주입 (Lombok 없음)
- [ ] Port 의존 없음
- [ ] `@Transactional` 없음
- [ ] 비즈니스 로직 없음

### Assembler
- [ ] `@Component` 어노테이션
- [ ] `*Assembler` 접미사
- [ ] 패키지: `application.{bc}.assembler`
- [ ] `toResponse*()` 메서드 네이밍
- [ ] `toResponseList()` 메서드
- [ ] **toDomain() 메서드 없음** (핵심!)
- [ ] **toCriteria() 메서드 없음**
- [ ] Port/Repository 의존 없음
- [ ] PageResponse 반환 없음
- [ ] Static 메서드 없음
- [ ] 비즈니스 로직/계산 로직 없음
- [ ] Lombok 없음
- [ ] `@Transactional` 없음

### PersistBundle
- [ ] `record` 사용
- [ ] `*PersistBundle` 접미사
- [ ] 패키지: `application.{bc}.dto.bundle`
- [ ] `enrichWithId()` 메서드 제공
- [ ] Domain 객체만 포함
- [ ] DTO/Response 포함 금지
- [ ] 비즈니스 로직 없음

### QueryBundle
- [ ] `record` 사용
- [ ] `*QueryBundle` 접미사
- [ ] 패키지: `application.{bc}.dto.bundle`
- [ ] Domain 객체만 포함

---

## ArchUnit 테스트 체크리스트

### CommandFactory ArchUnit (10개 규칙)

| # | 규칙 | 유형 |
|---|------|------|
| 1 | `@Component` 어노테이션 필수 | 필수 |
| 2 | `*CommandFactory` 접미사 필수 | 필수 |
| 3 | `factory.command` 패키지 위치 | 필수 |
| 4 | `final` 클래스 금지 | 필수 |
| 5 | `create*` 메서드 네이밍 | 권장 |
| 6 | `@Transactional` 금지 | 필수 |
| 7 | Port 의존 금지 | 필수 |
| 8 | Repository 의존 금지 | 필수 |
| 9 | Lombok 금지 | 필수 |
| 10 | `@Service` 금지 | 필수 |

### QueryFactory ArchUnit (10개 규칙)

| # | 규칙 | 유형 |
|---|------|------|
| 1 | `@Component` 어노테이션 필수 | 필수 |
| 2 | `*QueryFactory` 접미사 필수 | 필수 |
| 3 | `factory.query` 패키지 위치 | 필수 |
| 4 | `final` 클래스 금지 | 필수 |
| 5 | `createCriteria*` 메서드 네이밍 | 권장 |
| 6 | `@Transactional` 금지 | 필수 |
| 7 | Port 의존 금지 | 필수 |
| 8 | Repository 의존 금지 | 필수 |
| 9 | Lombok 금지 | 필수 |
| 10 | `@Service` 금지 | 필수 |

### Assembler ArchUnit (19개 규칙)

| # | 규칙 | 유형 |
|---|------|------|
| 1 | `@Component` 필수 | 필수 |
| 2 | Lombok 절대 금지 | 금지 |
| 3 | Static 메서드 금지 | 금지 |
| 4 | Port 의존성 금지 | 금지 |
| 5 | Repository 의존성 금지 | 금지 |
| 6 | Spring Data 의존성 금지 | 금지 |
| 7 | `*Assembler` 접미사 | 필수 |
| 8 | `..assembler..` 패키지 | 필수 |
| 9 | `toResponse*` 메서드 네이밍 | 필수 |
| 10 | **toDomain 메서드 금지** (핵심) | 금지 |
| 11 | 비즈니스 메서드 금지 | 금지 |
| 12 | `@Transactional` 금지 | 금지 |
| 13 | PageResponse 반환 금지 | 금지 |
| 14 | public 클래스 | 필수 |
| 15 | final 클래스 금지 | 필수 |
| 16 | 필드 final | 권장 |
| 17 | Layer 의존성 제한 | 필수 |
| 18 | 필드명 소문자 시작 | 권장 |
| 19 | 계산 로직 금지 | 금지 |

---

## Service에서 호출 패턴

### Command Service → Factory + Assembler

```java
@Component
public class PlaceOrderService implements PlaceOrderUseCase {

    private final OrderCommandFactory orderCommandFactory;
    private final OrderFacade orderFacade;
    private final OrderAssembler orderAssembler;

    public PlaceOrderService(
        OrderCommandFactory orderCommandFactory,
        OrderFacade orderFacade,
        OrderAssembler orderAssembler
    ) {
        this.orderCommandFactory = orderCommandFactory;
        this.orderFacade = orderFacade;
        this.orderAssembler = orderAssembler;
    }

    @Override
    public OrderResponse execute(PlaceOrderCommand command) {
        // 1. Command → Domain (Factory)
        OrderPersistBundle bundle = orderCommandFactory.createBundle(command);

        // 2. 영속화 (Facade)
        Order saved = orderFacade.persistOrderBundle(bundle);

        // 3. Domain → Response (Assembler)
        return orderAssembler.toResponse(saved);
    }
}
```

### Query Service → Factory + Assembler

```java
@Component
public class GetOrderDetailService implements GetOrderDetailUseCase {

    private final OrderQueryFactory orderQueryFactory;
    private final OrderReadManager orderReadManager;
    private final OrderAssembler orderAssembler;

    public GetOrderDetailService(
        OrderQueryFactory orderQueryFactory,
        OrderReadManager orderReadManager,
        OrderAssembler orderAssembler
    ) {
        this.orderQueryFactory = orderQueryFactory;
        this.orderReadManager = orderReadManager;
        this.orderAssembler = orderAssembler;
    }

    @Override
    @Transactional(readOnly = true)
    public OrderDetailResponse execute(OrderDetailQuery query) {
        // 1. Query → Criteria (Factory)
        OrderDetailCriteria criteria = orderQueryFactory.createDetailCriteria(query);

        // 2. 조회 (Manager)
        Order order = orderReadManager.getByCriteria(criteria);

        // 3. Domain → Response (Assembler)
        return orderAssembler.toDetailResponse(order);
    }
}
```

---

## 참조 문서

- **CommandFactory Guide**: `docs/coding_convention/03-application-layer/factory/command/command-factory-guide.md`
- **QueryFactory Guide**: `docs/coding_convention/03-application-layer/factory/query/query-factory-guide.md`
- **Assembler Guide**: `docs/coding_convention/03-application-layer/assembler/assembler-guide.md`
- **PersistBundle Guide**: `docs/coding_convention/03-application-layer/dto/bundle/persist-bundle-guide.md`
- **QueryBundle Guide**: `docs/coding_convention/03-application-layer/dto/bundle/query-bundle-guide.md`
- **CommandFactory ArchUnit**: `docs/coding_convention/03-application-layer/factory/command/command-factory-archunit.md`
- **QueryFactory ArchUnit**: `docs/coding_convention/03-application-layer/factory/query/query-factory-archunit.md`
- **Assembler ArchUnit**: `docs/coding_convention/03-application-layer/assembler/assembler-archunit.md`
