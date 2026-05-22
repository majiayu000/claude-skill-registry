---
name: repository-expert
version: 3.0.0
description: |
  Repository 전문가. JpaRepository(Command: save/delete), QueryDslRepository(Query: 4개 메서드),
  AdminQueryDslRepository(Join 허용, DTO Projection), LockRepository(Pessimistic Lock).
  Entity 직접 반환 금지, N+1은 Application Layer에서 해결. JPQL 금지, Lazy Loading 의존 금지.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, persistence, repository, jpa, querydsl, projection, lock, cqrs]
---

# Repository Expert (Repository 전문가)

## 목적 (Purpose)

Persistence Layer에서 **데이터 접근 계층**을 규칙에 맞게 생성합니다.
CQRS 원칙에 따라 Command/Query를 분리하고, 각 역할에 맞는 Repository 패턴을 적용합니다.

## 활성화 조건

- `/impl persistence {feature}` 명령 실행 시
- `/plan` 실행 후 Persistence Layer 작업 시
- repository, querydsl, projection, jpa, lock 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 역할 |
|----------|-------------|------|
| JpaRepository | `{Bc}Repository.java` | Command (save, delete) |
| QueryDslRepository | `{Bc}QueryDslRepository.java` | Query (4개 메서드) |
| AdminQueryDslRepository | `{Bc}AdminQueryDslRepository.java` | Admin Query (Join 허용) |
| LockRepository | `{Bc}LockRepository.java` | Lock (동시성 제어) |

## 완료 기준 (Acceptance Criteria)

- [ ] CQRS 분리: Command(JPA) / Query(QueryDSL) 완전 분리
- [ ] JpaRepository: `JpaRepository<Entity, ID>`만 상속, Query Method 금지
- [ ] QueryDslRepository: 4개 메서드만 제공, Join 금지
- [ ] AdminQueryDslRepository: DTO Projection 사용, Join 허용
- [ ] LockRepository: Pessimistic Lock 전용
- [ ] Entity 직접 반환 금지 (Adapter에서 Mapper로 변환)
- [ ] Long FK 전략 (연관관계 어노테이션 금지)
- [ ] ArchUnit 테스트 통과

---

## Repository 선택 기준

```
┌─────────────────────────────────────────────────────────────────┐
│                      Repository Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  JpaRepository  │  │ QueryDslRepo    │  │ AdminQueryDsl   │ │
│  │   (Command)     │  │   (Query)       │  │   (Admin)       │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │ • save()        │  │ • findById()    │  │ • Join 허용     │ │
│  │ • delete()      │  │ • existsById()  │  │ • DTO Projection│ │
│  │ • deleteById()  │  │ • findByCriteria│  │ • 자유 메서드   │ │
│  │                 │  │ • countByCriteria│ │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│  ┌─────────────────┐                                           │
│  │ LockRepository  │                                           │
│  │   (Lock)        │                                           │
│  ├─────────────────┤                                           │
│  │ • ForUpdate     │                                           │
│  │ • ForShare      │                                           │
│  │ • Pessimistic   │                                           │
│  └─────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 언제 무엇을 사용?

| 상황 | Repository | 이유 |
|------|------------|------|
| 저장/삭제 | JpaRepository | save(), delete() |
| 단순 조회 (ID, 목록) | QueryDslRepository | 4개 메서드 |
| 관리자 복잡 조회 | AdminQueryDslRepository | Join 허용, DTO Projection |
| 재고/포인트 동시성 | LockRepository | Pessimistic Lock |

---

## 코드 템플릿

### 1. JpaRepository (Command 전용)

```java
package com.ryuqq.adapter.out.persistence.order.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;

/**
 * OrderRepository - Order JPA Repository
 *
 * <p>Command 전용 (save, delete만 사용)</p>
 * <p>모든 Query 작업은 QueryDslRepository 사용</p>
 */
public interface OrderRepository extends JpaRepository<OrderJpaEntity, Long> {
    // ❌ Query Method 추가 금지
    // ❌ @Query 추가 금지
    // ❌ QuerydslPredicateExecutor 상속 금지
}
```

**핵심 규칙**:
- `JpaRepository<Entity, ID>`만 상속
- Query Method 추가 금지 (`findBy*`, `existsBy*` 등)
- `@Query` JPQL 금지
- Custom Repository 구현 금지 (`*RepositoryImpl`)

### 2. QueryDslRepository (Query 전용 - 4개 메서드)

```java
package com.ryuqq.adapter.out.persistence.order.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Repository;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;

import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.adapter.out.persistence.order.entity.QOrderJpaEntity;
import com.ryuqq.application.order.dto.query.SearchOrderQuery;

/**
 * OrderQueryDslRepository - Order QueryDSL Repository
 *
 * <p>4개 메서드만 제공 (findById, existsById, findByCriteria, countByCriteria)</p>
 * <p>Join 절대 금지, N+1 해결은 Application Layer에서</p>
 */
@Repository
public class OrderQueryDslRepository {

    private final JPAQueryFactory queryFactory;
    private static final QOrderJpaEntity qOrder = QOrderJpaEntity.orderJpaEntity;

    public OrderQueryDslRepository(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    // 1. 단건 조회
    public Optional<OrderJpaEntity> findById(Long id) {
        return Optional.ofNullable(
            queryFactory.selectFrom(qOrder)
                .where(qOrder.id.eq(id))
                .fetchOne()
        );
    }

    // 2. 존재 여부 확인
    public boolean existsById(Long id) {
        Integer count = queryFactory
            .selectOne()
            .from(qOrder)
            .where(qOrder.id.eq(id))
            .fetchFirst();
        return count != null;
    }

    // 3. 목록 조회 (동적 쿼리)
    public List<OrderJpaEntity> findByCriteria(SearchOrderQuery criteria) {
        var query = queryFactory
            .selectFrom(qOrder)
            .where(buildSearchConditions(criteria));

        // Cursor 페이징
        if (criteria.lastId() != null) {
            query = query.where(qOrder.id.gt(criteria.lastId()));
        }

        // Offset 페이징
        if (criteria.page() != null && criteria.size() != null) {
            query = query
                .offset((long) criteria.page() * criteria.size())
                .limit(criteria.size());
        } else if (criteria.size() != null) {
            query = query.limit(criteria.size() + 1);
        }

        if (criteria.sortBy() != null) {
            query = query.orderBy(buildOrderSpecifier(criteria));
        }

        return query.fetch();
    }

    // 4. 개수 조회
    public long countByCriteria(SearchOrderQuery criteria) {
        Long count = queryFactory
            .select(qOrder.count())
            .from(qOrder)
            .where(buildSearchConditions(criteria))
            .fetchOne();
        return count != null ? count : 0L;
    }

    // Private 헬퍼 메서드
    private BooleanExpression buildSearchConditions(SearchOrderQuery criteria) {
        BooleanExpression expression = null;

        if (criteria.orderNumber() != null && !criteria.orderNumber().isBlank()) {
            expression = qOrder.orderNumber.containsIgnoreCase(criteria.orderNumber());
        }

        if (criteria.status() != null) {
            BooleanExpression statusCondition = qOrder.status.eq(criteria.status());
            expression = expression != null ? expression.and(statusCondition) : statusCondition;
        }

        if (criteria.startDate() != null) {
            BooleanExpression dateCondition = qOrder.createdAt.goe(criteria.startDate());
            expression = expression != null ? expression.and(dateCondition) : dateCondition;
        }

        return expression;
    }

    private OrderSpecifier<?> buildOrderSpecifier(SearchOrderQuery criteria) {
        String sortBy = criteria.sortBy();
        boolean isAsc = "ASC".equalsIgnoreCase(criteria.sortDirection());

        return switch (sortBy.toLowerCase()) {
            case "id" -> isAsc ? qOrder.id.asc() : qOrder.id.desc();
            case "ordernumber" -> isAsc ? qOrder.orderNumber.asc() : qOrder.orderNumber.desc();
            default -> isAsc ? qOrder.createdAt.asc() : qOrder.createdAt.desc();
        };
    }
}
```

**핵심 규칙**:
- **4개 메서드만**: `findById`, `existsById`, `findByCriteria`, `countByCriteria`
- **Join 절대 금지** (fetch join, left join, inner join 모두)
- BooleanExpression으로 동적 쿼리
- Offset/Cursor 페이징 지원

### 3. AdminQueryDslRepository (관리자 전용 - Join 허용)

```java
package com.ryuqq.adapter.out.persistence.order.repository;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;

import com.ryuqq.adapter.out.persistence.order.entity.QOrderJpaEntity;
import com.ryuqq.adapter.out.persistence.member.entity.QMemberJpaEntity;
import com.ryuqq.application.order.dto.query.AdminOrderListQuery;
import com.ryuqq.application.order.dto.response.AdminOrderResponse;

/**
 * OrderAdminQueryDslRepository - 관리자 전용 QueryDSL Repository
 *
 * <p>Join 허용 (Long FK 기반), DTO Projection 권장</p>
 */
@Repository
public class OrderAdminQueryDslRepository {

    private final JPAQueryFactory queryFactory;

    private static final QOrderJpaEntity qOrder = QOrderJpaEntity.orderJpaEntity;
    private static final QMemberJpaEntity qMember = QMemberJpaEntity.memberJpaEntity;

    public OrderAdminQueryDslRepository(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    // Join + DTO Projection
    public List<AdminOrderResponse> findOrderListWithMember(AdminOrderListQuery criteria) {
        return queryFactory
            .select(Projections.constructor(
                AdminOrderResponse.class,
                qOrder.id,
                qOrder.orderNumber,
                qOrder.status,
                qOrder.totalAmount,
                qOrder.createdAt,
                qMember.id,
                qMember.name,
                qMember.email
            ))
            .from(qOrder)
            .leftJoin(qMember).on(qOrder.memberId.eq(qMember.id))  // ✅ Long FK 기반 조인
            .where(buildConditions(criteria))
            .orderBy(qOrder.createdAt.desc())
            .offset(criteria.offset())
            .limit(criteria.limit())
            .fetch();
    }

    public long countOrderListWithMember(AdminOrderListQuery criteria) {
        Long count = queryFactory
            .select(qOrder.count())
            .from(qOrder)
            .leftJoin(qMember).on(qOrder.memberId.eq(qMember.id))
            .where(buildConditions(criteria))
            .fetchOne();
        return count != null ? count : 0L;
    }

    private BooleanExpression buildConditions(AdminOrderListQuery criteria) {
        BooleanExpression expression = null;

        if (criteria.status() != null) {
            expression = qOrder.status.eq(criteria.status());
        }

        if (criteria.memberName() != null && !criteria.memberName().isBlank()) {
            BooleanExpression nameCondition = qMember.name.containsIgnoreCase(criteria.memberName());
            expression = expression != null ? expression.and(nameCondition) : nameCondition;
        }

        return expression;
    }
}
```

**핵심 규칙**:
- **Join 허용** (Long FK 기반 명시적 조인)
- **DTO Projection 권장** (`Projections.constructor()`)
- 메서드 제한 없음 (자유로운 메서드 정의)
- Entity 연관관계 어노테이션은 여전히 금지

### 4. LockRepository (동시성 제어 전용)

```java
package com.ryuqq.adapter.out.persistence.order.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Repository;

import com.querydsl.jpa.impl.JPAQueryFactory;
import jakarta.persistence.LockModeType;

import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.adapter.out.persistence.order.entity.QOrderJpaEntity;

/**
 * OrderLockRepository - Order Lock 전용 Repository
 *
 * <p>비관적 락 (Pessimistic Lock) 처리</p>
 * <p>재고 차감, 포인트 처리, 좌석 예약 등</p>
 */
@Repository
public class OrderLockRepository {

    private final JPAQueryFactory queryFactory;
    private static final QOrderJpaEntity qOrder = QOrderJpaEntity.orderJpaEntity;

    public OrderLockRepository(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    // Pessimistic Write Lock (FOR UPDATE)
    public Optional<OrderJpaEntity> findByIdForUpdate(Long id) {
        return Optional.ofNullable(
            queryFactory.selectFrom(qOrder)
                .where(qOrder.id.eq(id))
                .setLockMode(LockModeType.PESSIMISTIC_WRITE)
                .fetchOne()
        );
    }

    // 여러 건 Lock (데드락 방지: ID 오름차순 정렬)
    public List<OrderJpaEntity> findByIdsForUpdate(List<Long> ids) {
        return queryFactory.selectFrom(qOrder)
            .where(qOrder.id.in(ids))
            .orderBy(qOrder.id.asc())  // 데드락 방지
            .setLockMode(LockModeType.PESSIMISTIC_WRITE)
            .fetch();
    }

    // Pessimistic Read Lock (FOR SHARE)
    public Optional<OrderJpaEntity> findByIdForShare(Long id) {
        return Optional.ofNullable(
            queryFactory.selectFrom(qOrder)
                .where(qOrder.id.eq(id))
                .setLockMode(LockModeType.PESSIMISTIC_READ)
                .fetchOne()
        );
    }
}
```

**핵심 규칙**:
- Lock 관련 메서드만 제공
- 데드락 방지: 여러 건 Lock 시 ID 오름차순 정렬
- Lock 범위 최소화 (트랜잭션 내 빠른 처리)

---

## Adapter ↔ Repository 1:1 매핑

```
┌─────────────────┐       ┌─────────────────┐
│  QueryAdapter   │  1:1  │ QueryDslRepo    │
│  ───────────────│◄─────►│                 │
│  • repository   │       │ • findById()    │
│  • mapper       │       │ • existsById()  │
│  (필드 2개만)   │       │ • findByCriteria│
└─────────────────┘       └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│ CommandAdapter  │  1:1  │  JpaRepository  │
│  ───────────────│◄─────►│                 │
│  • repository   │       │ • save()        │
│  • mapper       │       │ • delete()      │
│  (필드 2개만)   │       │                 │
└─────────────────┘       └─────────────────┘
```

**N+1 해결은 Application Layer에서**:
```java
// ✅ Application Layer (UseCase)에서 N+1 해결
@Component
public class OrderQueryUseCase {
    private final OrderQueryPort orderQueryPort;
    private final CustomerQueryPort customerQueryPort;

    public List<OrderWithCustomerResponse> findOrdersWithCustomer(Criteria criteria) {
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

        // 4. 조합 (Application Layer에서 처리)
        return orders.stream()
            .map(order -> new OrderWithCustomerResponse(
                order, customerMap.get(order.getCustomerId())
            ))
            .toList();
    }
}
```

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 적용 대상 |
|------|----------|
| `JpaRepository<Entity, ID>`만 상속 | JpaRepository |
| 4개 메서드만 | QueryDslRepository |
| DTO Projection | AdminQueryDslRepository |
| Long FK 기반 조인 | Admin Join |
| 데드락 방지 정렬 | LockRepository 복수 Lock |

### ❌ PROHIBITED (금지)

| 항목 | 이유 |
|------|------|
| Query Method (`findBy*`) | QueryDslRepository 사용 |
| `@Query` JPQL | QueryDSL 사용 |
| `QuerydslPredicateExecutor` | 순수 JPA 유지 |
| Custom Repository (`*RepositoryImpl`) | QueryDslRepository로 대체 |
| Join (일반 QueryDsl) | N+1은 Application Layer에서 해결 |
| Entity 연관관계 (`@OneToMany`) | Long FK 전략 |
| Mapper 호출 (Repository) | Adapter에서 처리 |
| `@Transactional` (Repository) | Service/Manager Layer에서 관리 |
| Fetch Join | Entity 그래프 로딩 불필요 |
| Lazy Loading 의존 | 명시적 Join 사용 |

---

## 패키지 구조

```
adapter-out/persistence-mysql/
└── src/main/java/
    └── com/ryuqq/adapter/out/persistence/
        └── order/
            ├── entity/
            │   └── OrderJpaEntity.java
            │
            ├── repository/
            │   ├── OrderRepository.java              (JPA - Command)
            │   ├── OrderQueryDslRepository.java      (QueryDSL - 4개 메서드)
            │   ├── OrderAdminQueryDslRepository.java (Admin - Join 허용)
            │   └── OrderLockRepository.java          (Lock - 동시성)
            │
            ├── mapper/
            │   └── OrderJpaEntityMapper.java
            │
            └── adapter/
                ├── OrderCommandAdapter.java
                ├── OrderQueryAdapter.java
                └── OrderAdminQueryAdapter.java
```

---

## 체크리스트 (Output Checklist)

### JpaRepository
- [ ] 인터페이스로 정의
- [ ] `JpaRepository<Entity, Long>` 상속
- [ ] Query Method 없음
- [ ] `@Query` 없음
- [ ] `QuerydslPredicateExecutor` 상속 없음

### QueryDslRepository
- [ ] `@Repository` 어노테이션
- [ ] `JPAQueryFactory` 생성자 주입
- [ ] QType `static final` 상수
- [ ] **4개 메서드만**: findById, existsById, findByCriteria, countByCriteria
- [ ] Join 절대 없음
- [ ] Private 헬퍼 메서드 (BooleanExpression, OrderSpecifier)
- [ ] Mapper 호출 없음
- [ ] `@Transactional` 없음

### AdminQueryDslRepository
- [ ] `*AdminQueryDslRepository` 네이밍
- [ ] `@Repository` 어노테이션
- [ ] DTO Projection (`Projections.constructor()`)
- [ ] Long FK 기반 조인
- [ ] 메서드 자유 정의

### LockRepository
- [ ] `*LockRepository` 네이밍
- [ ] `@Repository` 어노테이션
- [ ] `LockModeType.PESSIMISTIC_WRITE`
- [ ] 복수 Lock 시 ID 오름차순 정렬
- [ ] Lock 범위 최소화

---

## 테스트 체크리스트

### JpaRepository
- [ ] **테스트 불필요** (Spring Data JPA 검증 완료)
- [ ] ArchUnit으로 구조 검증

### QueryDslRepository
- [ ] `@DataJpaTest` 통합 테스트
- [ ] 동적 쿼리 조건 검증
- [ ] 페이징 (Offset/Cursor) 검증
- [ ] 정렬 조건 검증

### ArchUnit 테스트 (7개 규칙)
- [ ] JPA: 인터페이스 타입
- [ ] JPA: JpaRepository 상속
- [ ] JPA: QuerydslPredicateExecutor 금지
- [ ] JPA: Query Method 금지
- [ ] JPA: @Query 금지
- [ ] JPA: Custom Repository 금지
- [ ] JPA: 네이밍 규칙

---

## 참조 문서

- **Repository Guide**: `docs/coding_convention/04-persistence-layer/mysql/repository/repository-guide.md`
- **JPA Repository**: `docs/coding_convention/04-persistence-layer/mysql/repository/jpa/jpa-repository-guide.md`
- **QueryDSL Repository**: `docs/coding_convention/04-persistence-layer/mysql/repository/querydsl/querydsl-repository-guide.md`
- **Admin QueryDSL**: `docs/coding_convention/04-persistence-layer/mysql/repository/admin/admin-querydsl-repository-archunit.md`
- **Lock Repository**: `docs/coding_convention/04-persistence-layer/mysql/repository/lock/lock-repository-guide.md`
- **JPA ArchUnit**: `docs/coding_convention/04-persistence-layer/mysql/repository/jpa/jpa-repository-archunit.md`
