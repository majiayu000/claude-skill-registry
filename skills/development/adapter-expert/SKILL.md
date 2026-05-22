---
name: adapter-expert
version: 3.0.0
description: |
  Adapter Layer 전문가. CommandAdapter(persist만, JpaRepository 1:1), QueryAdapter(4개 메서드, QueryDslRepository 1:1),
  AdminQueryAdapter(Join 허용, DTO Projection), LockQueryAdapter(6개 Lock 메서드).
  필드 2개만(Repository + Mapper). @Component 필수. @Transactional 절대 금지.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, persistence, adapter, port-out, command, query, lock, cqrs]
---

# Adapter Expert (Adapter 전문가)

## 목적 (Purpose)

Persistence Layer에서 **Port-Out 인터페이스를 구현**하는 Adapter를 규칙에 맞게 생성합니다.
CQRS 원칙에 따라 Command/Query를 완전 분리하고, Repository ↔ Adapter 1:1 매핑 원칙을 준수합니다.

## 활성화 조건

- `/impl persistence {feature}` 명령 실행 시
- `/plan` 실행 후 Persistence Layer 작업 시
- adapter, port-out, command adapter, query adapter 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 | Repository |
|----------|-------------|------|------------|
| CommandAdapter | `{Bc}CommandAdapter.java` | `.../adapter/` | JpaRepository |
| QueryAdapter | `{Bc}QueryAdapter.java` | `.../adapter/` | QueryDslRepository |
| AdminQueryAdapter | `{Bc}AdminQueryAdapter.java` | `.../adapter/` | AdminQueryDslRepository |
| LockQueryAdapter | `{Bc}LockQueryAdapter.java` | `.../adapter/` | LockRepository |

## 완료 기준 (Acceptance Criteria)

- [ ] CQRS 분리: Command/Query Adapter 완전 분리
- [ ] 1:1 매핑: 각 Adapter는 하나의 Repository만 의존
- [ ] 필드 2개만: Repository + Mapper (AdminQueryAdapter는 Mapper 선택적)
- [ ] `@Component` 어노테이션 사용 (`@Repository` 아님!)
- [ ] `@Transactional` 절대 금지 (Application Layer 책임)
- [ ] 비즈니스 로직 없음 (단순 위임 + 변환만)
- [ ] Lombok 금지
- [ ] ArchUnit 테스트 통과

---

## Adapter 선택 기준

```
┌─────────────────────────────────────────────────────────────────┐
│                    CQRS 기반 Adapter 분리                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Command Adapter                         │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │  CommandAdapter                                           │ │
│  │  └─ JpaRepository (1:1) + Mapper                         │ │
│  │  └─ persist() 메서드만 (1개)                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                     Query Adapters                         │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐ │ │
│  │  │  QueryAdapter   │ │AdminQueryAdapter│ │LockQueryAdp │ │ │
│  │  │   (일반 조회)   │ │   (관리자)      │ │   (Lock)    │ │ │
│  │  ├─────────────────┤ ├─────────────────┤ ├─────────────┤ │ │
│  │  │• QueryDslRepo   │ │• AdminQueryDsl  │ │• LockRepo   │ │ │
│  │  │• 4개 메서드     │ │• Join 허용      │ │• 6개 메서드 │ │ │
│  │  │• Domain 반환    │ │• DTO Projection │ │• Domain 반환│ │ │
│  │  └─────────────────┘ └─────────────────┘ └─────────────┘ │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 언제 무엇을 사용?

| 상황 | Adapter | Repository | 반환 타입 |
|------|---------|------------|----------|
| 저장/삭제 | CommandAdapter | JpaRepository | *Id |
| 단순 조회 (ID, 목록) | QueryAdapter | QueryDslRepository | Domain |
| 관리자 복잡 조회 (Join) | AdminQueryAdapter | AdminQueryDslRepository | DTO |
| 동시성 제어 (재고, 좌석) | LockQueryAdapter | LockRepository | Domain |

### Adapter 선택 플로우

```
저장/삭제 필요?
├─ Yes → CommandAdapter (persist만)
│
조회 필요?
├─ 단순 조회 (ID, 목록) → QueryAdapter (4개 메서드)
├─ 관리자 복잡 조회 (Join) → AdminQueryAdapter (DTO Projection)
│
동시성 제어 필요?
└─ 재고, 포인트, 좌석 예약 → LockQueryAdapter (6개 Lock 메서드)
```

---

## 코드 템플릿

### 1. CommandAdapter (JpaRepository 1:1)

```java
package com.ryuqq.adapter.out.persistence.order.adapter;

import org.springframework.stereotype.Component;

import com.ryuqq.application.common.port.out.OrderPersistencePort;
import com.ryuqq.adapter.out.persistence.order.repository.OrderJpaRepository;
import com.ryuqq.adapter.out.persistence.order.mapper.OrderJpaEntityMapper;
import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.OrderId;

@Component
public class OrderCommandAdapter implements OrderPersistencePort {

    private final OrderJpaRepository orderJpaRepository;
    private final OrderJpaEntityMapper orderJpaEntityMapper;

    public OrderCommandAdapter(
        OrderJpaRepository orderJpaRepository,
        OrderJpaEntityMapper orderJpaEntityMapper
    ) {
        this.orderJpaRepository = orderJpaRepository;
        this.orderJpaEntityMapper = orderJpaEntityMapper;
    }

    /**
     * Order 저장 (신규 생성 또는 수정)
     *
     * <p>신규 생성 (ID 없음) → JPA가 ID 자동 할당 (INSERT)</p>
     * <p>기존 수정 (ID 있음) → 더티체킹으로 자동 UPDATE</p>
     *
     * @param order 저장할 Order (Domain)
     * @return 저장된 Order의 ID
     */
    @Override
    public OrderId persist(Order order) {
        // 1. Domain → Entity 변환
        OrderJpaEntity entity = orderJpaEntityMapper.toEntity(order);

        // 2. JPA 저장 (신규/수정 JPA가 자동 판단)
        OrderJpaEntity savedEntity = orderJpaRepository.save(entity);

        // 3. ID 반환
        return OrderId.of(savedEntity.getId());
    }
}
```

**핵심 규칙**:
- **메서드 1개**: `persist()` 만 제공 (update, delete 메서드 금지)
- **JpaRepository 1:1 매핑**: 정확히 하나의 JpaRepository만 의존
- **필드 2개만**: Repository + Mapper
- **반환 타입**: `*Id` (OrderId, ProductId 등)
- **@Transactional 금지**: Application Layer에서 관리

### 2. QueryAdapter (QueryDslRepository 1:1)

```java
package com.ryuqq.adapter.out.persistence.order.adapter;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Component;

import com.ryuqq.application.common.port.out.OrderQueryPort;
import com.ryuqq.adapter.out.persistence.order.repository.OrderQueryDslRepository;
import com.ryuqq.adapter.out.persistence.order.mapper.OrderJpaEntityMapper;
import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.order.vo.OrderSearchCriteria;

@Component
public class OrderQueryAdapter implements OrderQueryPort {

    private final OrderQueryDslRepository queryDslRepository;
    private final OrderJpaEntityMapper orderJpaEntityMapper;

    public OrderQueryAdapter(
        OrderQueryDslRepository queryDslRepository,
        OrderJpaEntityMapper orderJpaEntityMapper
    ) {
        this.queryDslRepository = queryDslRepository;
        this.orderJpaEntityMapper = orderJpaEntityMapper;
    }

    /**
     * ID로 Order 단건 조회
     *
     * @param id Order ID
     * @return Order Domain (Optional)
     */
    @Override
    public Optional<Order> findById(OrderId id) {
        return queryDslRepository.findById(id.value())
            .map(orderJpaEntityMapper::toDomain);
    }

    /**
     * ID로 Order 존재 여부 확인
     *
     * @param id Order ID
     * @return 존재 여부
     */
    @Override
    public boolean existsById(OrderId id) {
        return queryDslRepository.existsById(id.value());
    }

    /**
     * 검색 조건으로 Order 목록 조회
     *
     * @param criteria 검색 조건
     * @return Order Domain 목록
     */
    @Override
    public List<Order> findByCriteria(OrderSearchCriteria criteria) {
        List<OrderJpaEntity> entities = queryDslRepository.findByCriteria(criteria);
        return entities.stream()
            .map(orderJpaEntityMapper::toDomain)
            .toList();
    }

    /**
     * 검색 조건으로 Order 개수 조회
     *
     * @param criteria 검색 조건
     * @return Order 개수
     */
    @Override
    public long countByCriteria(OrderSearchCriteria criteria) {
        return queryDslRepository.countByCriteria(criteria);
    }
}
```

**핵심 규칙**:
- **메서드 4개 고정**: `findById`, `existsById`, `findByCriteria`, `countByCriteria`
- **QueryDslRepository 1:1 매핑**: 정확히 하나의 QueryDslRepository만 의존
- **필드 2개만**: Repository + Mapper
- **Domain 반환**: Entity → Domain 변환 (DTO 반환 금지)
- **JPAQueryFactory 직접 사용 금지**: QueryDslRepository에 위임

### 3. AdminQueryAdapter (AdminQueryDslRepository 1:1)

```java
package com.ryuqq.adapter.out.persistence.order.adapter;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Component;

import com.ryuqq.application.common.port.out.OrderAdminQueryPort;
import com.ryuqq.adapter.out.persistence.order.repository.OrderAdminQueryDslRepository;
import com.ryuqq.application.order.dto.AdminOrderListResponse;
import com.ryuqq.application.order.dto.AdminOrderDetailResponse;
import com.ryuqq.application.order.dto.AdminOrderSearchCriteria;
import com.ryuqq.domain.order.vo.OrderId;

@Component
public class OrderAdminQueryAdapter implements OrderAdminQueryPort {

    private final OrderAdminQueryDslRepository adminQueryDslRepository;

    public OrderAdminQueryAdapter(OrderAdminQueryDslRepository adminQueryDslRepository) {
        this.adminQueryDslRepository = adminQueryDslRepository;
    }

    /**
     * 관리자 목록 조회 (Join 허용)
     *
     * @param criteria 검색 조건
     * @return 관리자 목록 Response (DTO Projection)
     */
    @Override
    public List<AdminOrderListResponse> findList(AdminOrderSearchCriteria criteria) {
        return adminQueryDslRepository.findList(criteria);
    }

    /**
     * 관리자 상세 조회 (Join 허용)
     *
     * @param id Order ID
     * @return 관리자 상세 Response (DTO Projection)
     */
    @Override
    public Optional<AdminOrderDetailResponse> findDetail(OrderId id) {
        return adminQueryDslRepository.findDetail(id.value());
    }

    /**
     * 관리자 페이징 조회
     *
     * @param criteria 검색 조건
     * @param pageable 페이징 정보
     * @return 페이징된 목록
     */
    @Override
    public Page<AdminOrderListResponse> findPage(
            AdminOrderSearchCriteria criteria,
            Pageable pageable
    ) {
        return adminQueryDslRepository.findPage(criteria, pageable);
    }
}
```

**핵심 규칙**:
- **메서드 자유**: 고정된 메서드 개수 없음
- **필드 1~2개**: AdminQueryDslRepository + (선택적) ResponseMapper
- **DTO Projection 직접 반환**: Domain이 아닌 DTO 반환
- **Join 허용**: AdminQueryDslRepository에서 Long FK 기반 Join

### 4. LockQueryAdapter (LockRepository 1:1)

```java
package com.ryuqq.adapter.out.persistence.order.adapter;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Component;

import com.ryuqq.application.common.port.out.OrderLockQueryPort;
import com.ryuqq.adapter.out.persistence.order.repository.OrderLockRepository;
import com.ryuqq.adapter.out.persistence.order.mapper.OrderJpaEntityMapper;
import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.order.vo.OrderSearchCriteria;

@Component
public class OrderLockQueryAdapter implements OrderLockQueryPort {

    private final OrderLockRepository lockRepository;
    private final OrderJpaEntityMapper orderJpaEntityMapper;

    public OrderLockQueryAdapter(
        OrderLockRepository lockRepository,
        OrderJpaEntityMapper orderJpaEntityMapper
    ) {
        this.lockRepository = lockRepository;
        this.orderJpaEntityMapper = orderJpaEntityMapper;
    }

    // ========================================================================
    // Pessimistic Write Lock (FOR UPDATE)
    // ========================================================================

    /**
     * ID로 Order 단건 조회 (FOR UPDATE)
     *
     * @param id Order ID
     * @return Order Domain (Optional)
     * @throws PessimisticLockException Lock 획득 실패 시
     * @throws LockTimeoutException Lock 타임아웃 시
     */
    @Override
    public Optional<Order> findByIdForUpdate(OrderId id) {
        return lockRepository.findByIdForUpdate(id.value())
            .map(orderJpaEntityMapper::toDomain);
    }

    /**
     * Criteria로 Order 목록 조회 (FOR UPDATE)
     *
     * @param criteria 검색 조건
     * @return Order Domain 목록
     * @throws PessimisticLockException Lock 획득 실패 시
     * @throws LockTimeoutException Lock 타임아웃 시
     */
    @Override
    public List<Order> findByCriteriaForUpdate(OrderSearchCriteria criteria) {
        List<OrderJpaEntity> entities = lockRepository.findByCriteriaForUpdate(criteria);
        return entities.stream()
            .map(orderJpaEntityMapper::toDomain)
            .toList();
    }

    // ========================================================================
    // Pessimistic Read Lock (FOR SHARE)
    // ========================================================================

    /**
     * ID로 Order 단건 조회 (FOR SHARE)
     *
     * @param id Order ID
     * @return Order Domain (Optional)
     * @throws PessimisticLockException Lock 획득 실패 시
     * @throws LockTimeoutException Lock 타임아웃 시
     */
    @Override
    public Optional<Order> findByIdForShare(OrderId id) {
        return lockRepository.findByIdForShare(id.value())
            .map(orderJpaEntityMapper::toDomain);
    }

    /**
     * Criteria로 Order 목록 조회 (FOR SHARE)
     *
     * @param criteria 검색 조건
     * @return Order Domain 목록
     * @throws PessimisticLockException Lock 획득 실패 시
     * @throws LockTimeoutException Lock 타임아웃 시
     */
    @Override
    public List<Order> findByCriteriaForShare(OrderSearchCriteria criteria) {
        List<OrderJpaEntity> entities = lockRepository.findByCriteriaForShare(criteria);
        return entities.stream()
            .map(orderJpaEntityMapper::toDomain)
            .toList();
    }

    // ========================================================================
    // Optimistic Lock (@Version)
    // ========================================================================

    /**
     * ID로 Order 단건 조회 (Optimistic Lock)
     *
     * <p>조회 시 Lock을 걸지 않으며, 업데이트 시 OptimisticLockException 발생 가능</p>
     *
     * @param id Order ID
     * @return Order Domain (Optional)
     */
    @Override
    public Optional<Order> findByIdWithOptimisticLock(OrderId id) {
        return lockRepository.findByIdWithOptimisticLock(id.value())
            .map(orderJpaEntityMapper::toDomain);
    }

    /**
     * Criteria로 Order 목록 조회 (Optimistic Lock)
     *
     * <p>조회 시 Lock을 걸지 않으며, 업데이트 시 OptimisticLockException 발생 가능</p>
     *
     * @param criteria 검색 조건
     * @return Order Domain 목록
     */
    @Override
    public List<Order> findByCriteriaWithOptimisticLock(OrderSearchCriteria criteria) {
        List<OrderJpaEntity> entities = lockRepository.findByCriteriaWithOptimisticLock(criteria);
        return entities.stream()
            .map(orderJpaEntityMapper::toDomain)
            .toList();
    }
}
```

**핵심 규칙**:
- **메서드 6개 고정**: ForUpdate(2), ForShare(2), OptimisticLock(2)
- **LockRepository 1:1 매핑**: 정확히 하나의 LockRepository만 의존
- **필드 2개만**: Repository + Mapper
- **Domain 반환**: Entity → Domain 변환
- **예외 명시**: JavaDoc에 `@throws` 명시 (catch 하지 않음)
- **예외 처리는 Application Layer**: Adapter는 위임만

---

## N+1 해결 전략

### Application Layer에서 해결 (1:1 매핑 원칙 유지)

```
❌ Adapter에서 N+1 해결 (금지)
──────────────────────────────
OrderQueryAdapter
├─ orderQueryDslRepository
├─ customerQueryDslRepository  ← 금지! 1:1 위반
└─ mapper


✅ Application Layer에서 해결 (권장)
──────────────────────────────
OrderQueryUseCase (Application Layer)
├─ orderQueryPort.findByCriteria()     → 주문 목록
├─ customerQueryPort.findByIds()       → 고객 목록 (IN 절)
└─ 조합 및 Response 생성               → Application에서 처리
```

**N+1 해결 패턴**:
```java
// Application Layer (UseCase)
@Component
public class OrderQueryUseCase {
    private final OrderQueryPort orderQueryPort;
    private final CustomerQueryPort customerQueryPort;

    @Transactional(readOnly = true)
    public List<OrderWithCustomerResponse> findOrdersWithCustomer(
            OrderSearchCriteria criteria) {
        // 1. 주문 조회
        List<Order> orders = orderQueryPort.findByCriteria(criteria);

        // 2. 고객 ID 수집
        Set<Long> customerIds = orders.stream()
            .map(Order::getCustomerId)
            .collect(Collectors.toSet());

        // 3. 고객 일괄 조회 (IN 절로 N+1 해결)
        Map<Long, Customer> customerMap = customerQueryPort.findByIds(customerIds)
            .stream()
            .collect(Collectors.toMap(c -> c.getId().getValue(), c -> c));

        // 4. 조합
        return orders.stream()
            .map(order -> new OrderWithCustomerResponse(
                order,
                customerMap.get(order.getCustomerId())
            ))
            .toList();
    }
}
```

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 설명 |
|------|------|
| `@Component` | 모든 Adapter에 적용 |
| 1:1 매핑 | 각 Adapter는 정확히 하나의 Repository만 의존 |
| 필드 2개만 | Repository + Mapper (AdminQueryAdapter는 Mapper 선택적) |
| Domain 반환 | QueryAdapter, LockQueryAdapter는 Domain 반환 |
| DTO 반환 | AdminQueryAdapter만 DTO Projection 반환 |
| persist() | CommandAdapter 유일한 메서드 |
| 4개 메서드 | QueryAdapter: findById, existsById, findByCriteria, countByCriteria |
| 6개 메서드 | LockQueryAdapter: ForUpdate(2), ForShare(2), OptimisticLock(2) |

### ❌ PROHIBITED (금지)

| 항목 | 이유 |
|------|------|
| `@Repository` | `@Component` 사용 |
| `@Transactional` | Application Layer에서 관리 |
| 비즈니스 로직 | Domain Layer 책임 |
| 다른 Repository 주입 | 1:1 매핑 위반 |
| JPAQueryFactory 직접 사용 | QueryDslRepository에 위임 |
| update(), delete() 메서드 | persist()로 통합 (더티체킹 활용) |
| Query 메서드 in CommandAdapter | CQRS 분리 |
| Command 메서드 in QueryAdapter | CQRS 분리 |
| Lombok | Plain Java 사용 |

---

## Adapter 유형별 비교

| 항목 | CommandAdapter | QueryAdapter | AdminQueryAdapter | LockQueryAdapter |
|------|---------------|--------------|-------------------|------------------|
| **Repository** | JpaRepository | QueryDslRepo | AdminQueryDslRepo | LockRepository |
| **메서드 수** | 1개 (persist) | 4개 고정 | 자유 | 6개 고정 |
| **필드 수** | 2개 | 2개 | 1~2개 | 2개 |
| **Mapper** | 필수 | 필수 | 선택적 | 필수 |
| **반환 타입** | *Id | Domain | DTO | Domain |
| **Join** | N/A | ❌ 금지 | ✅ 허용 | N/A |

---

## 패키지 구조

```
adapter-out/persistence-mysql/
└─ src/main/java/
   └─ com/company/adapter/out/persistence/
       └─ order/
           ├─ entity/
           │  └─ OrderJpaEntity.java
           │
           ├─ repository/
           │  ├─ OrderJpaRepository.java              (JPA - Command)
           │  ├─ OrderQueryDslRepository.java         (QueryDSL - 일반)
           │  ├─ OrderAdminQueryDslRepository.java    (QueryDSL - 관리자)
           │  └─ OrderLockRepository.java             (Lock)
           │
           ├─ mapper/
           │  └─ OrderJpaEntityMapper.java
           │
           └─ adapter/
              ├─ OrderCommandAdapter.java          (JpaRepository 1:1)
              ├─ OrderQueryAdapter.java            (QueryDslRepository 1:1)
              ├─ OrderAdminQueryAdapter.java       (AdminQueryDslRepository 1:1)
              └─ OrderLockQueryAdapter.java        (LockRepository 1:1)
```

---

## 체크리스트 (Output Checklist)

### CommandAdapter
- [ ] `@Component` 어노테이션
- [ ] `*PersistencePort` 구현
- [ ] JpaRepository 의존성 주입
- [ ] Mapper 의존성 주입
- [ ] **필드 2개만**
- [ ] `persist()` 메서드만 (1개)
- [ ] **반환 타입 `*Id`**
- [ ] `@Transactional` 금지
- [ ] Query 메서드 없음
- [ ] 비즈니스 로직 없음

### QueryAdapter
- [ ] `@Component` 어노테이션
- [ ] `*QueryPort` 구현
- [ ] QueryDslRepository 의존성 주입
- [ ] Mapper 의존성 주입
- [ ] **필드 2개만**
- [ ] `findById()` 메서드 - Optional<Domain>
- [ ] `existsById()` 메서드 - boolean
- [ ] `findByCriteria()` 메서드 - List<Domain>
- [ ] `countByCriteria()` 메서드 - long
- [ ] **메서드 4개만**
- [ ] `@Transactional` 금지
- [ ] Command 메서드 없음
- [ ] JPAQueryFactory 직접 사용 금지

### AdminQueryAdapter
- [ ] `@Component` 어노테이션
- [ ] `*AdminQueryPort` 구현
- [ ] AdminQueryDslRepository 의존성 주입
- [ ] **필드 1~2개** (Mapper 선택적)
- [ ] **DTO Projection 직접 반환**
- [ ] `@Transactional` 금지
- [ ] 비즈니스 로직 없음

### LockQueryAdapter
- [ ] `@Component` 어노테이션
- [ ] `*LockQueryPort` 구현
- [ ] LockRepository 의존성 주입
- [ ] Mapper 의존성 주입
- [ ] **필드 2개만**
- [ ] `findByIdForUpdate()` - FOR UPDATE 단건
- [ ] `findByCriteriaForUpdate()` - FOR UPDATE 목록
- [ ] `findByIdForShare()` - FOR SHARE 단건
- [ ] `findByCriteriaForShare()` - FOR SHARE 목록
- [ ] `findByIdWithOptimisticLock()` - Optimistic 단건
- [ ] `findByCriteriaWithOptimisticLock()` - Optimistic 목록
- [ ] **메서드 6개만**
- [ ] JavaDoc `@throws` 명시 (예외 catch 금지)
- [ ] `@Transactional` 금지
- [ ] Domain 반환

---

## 테스트 체크리스트

### Adapter 단위 테스트
- [ ] Repository 위임 검증
- [ ] Mapper 변환 검증
- [ ] 반환 타입 검증

### ArchUnit 테스트
- [ ] `@Component` 어노테이션 검증
- [ ] `@Transactional` 금지 검증
- [ ] 필드 개수 검증 (2개)
- [ ] 메서드 개수/이름 검증
- [ ] 1:1 매핑 검증

---

## 참조 문서

- **Adapter Guide**: `docs/coding_convention/04-persistence-layer/mysql/adapter/adapter-guide.md`
- **Command Adapter Guide**: `docs/coding_convention/04-persistence-layer/mysql/adapter/command/command-adapter-guide.md`
- **Query Adapter Guide**: `docs/coding_convention/04-persistence-layer/mysql/adapter/query/general/query-adapter-guide.md`
- **Admin Query Adapter Guide**: `docs/coding_convention/04-persistence-layer/mysql/adapter/query/admin/admin-query-adapter-guide.md`
- **Lock Query Adapter Guide**: `docs/coding_convention/04-persistence-layer/mysql/adapter/query/lock/lock-query-adapter-guide.md`
- **Command Adapter ArchUnit**: `docs/coding_convention/04-persistence-layer/mysql/adapter/command/command-adapter-archunit.md`
- **Query Adapter ArchUnit**: `docs/coding_convention/04-persistence-layer/mysql/adapter/query/general/query-adapter-archunit.md`
