---
name: entity-mapper-expert
version: 3.0.0
description: |
  JPA Entity Long FK 전략, BaseAuditEntity/SoftDeletableEntity 상속, EntityMapper Domain⇄Entity 변환.
  JPA 관계 어노테이션(@ManyToOne, @OneToMany) 금지. Lombok 금지, Setter 금지.
  Entity는 of() static factory method만 public, 생성자는 protected/private.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, persistence, entity, mapper, jpa, long-fk, baseauditentity]
---

# Entity & Mapper 전문가 (Entity-Mapper Expert)

## 목적 (Purpose)

Persistence Layer에서 **JPA Entity**와 **EntityMapper**를 규칙에 맞게 생성합니다.
Domain Layer와 Infrastructure(JPA)를 깔끔하게 분리하여 헥사고날 아키텍처를 준수합니다.

## 활성화 조건

- `/impl persistence {feature}` 명령 실행 시
- `/plan` 실행 후 Persistence Layer 작업 시
- entity, mapper, jpa, BaseAuditEntity 키워드 언급 시
- `/kb-entity` 명령 시 자동 활성화

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 |
|----------|-------------|------|
| JPA Entity | `{Domain}JpaEntity.java` | `adapter-out/persistence-mysql/{bc}/entity/` |
| EntityMapper | `{Domain}JpaEntityMapper.java` | `adapter-out/persistence-mysql/{bc}/mapper/` |

## 완료 기준 (Acceptance Criteria)

- [ ] Long FK 전략 적용 (JPA 관계 어노테이션 금지)
- [ ] BaseAuditEntity 또는 SoftDeletableEntity 상속 검토
- [ ] protected 기본 생성자 + private 전체 필드 생성자
- [ ] public static of() 팩토리 메서드만 노출
- [ ] Getter만 제공 (Setter 금지)
- [ ] `*JpaEntity` 네이밍 규칙
- [ ] EntityMapper는 `@Component` Bean
- [ ] EntityMapper는 toEntity() + toDomain() 필수
- [ ] Lombok 금지
- [ ] ArchUnit 테스트 통과

---

## JPA Entity 코드 템플릿

### 1. BaseAuditEntity 상속 (시간 정보만)

```java
package com.ryuqq.adapter.out.persistence.order.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import com.ryuqq.adapter.out.persistence.common.entity.BaseAuditEntity;
import com.ryuqq.domain.order.vo.OrderStatus;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * OrderJpaEntity - 주문 JPA Entity
 *
 * <p><strong>BaseAuditEntity 상속:</strong></p>
 * <ul>
 *   <li>공통 감사 필드 상속: createdAt, updatedAt</li>
 * </ul>
 *
 * <p><strong>Long FK 전략:</strong></p>
 * <ul>
 *   <li>JPA 관계 어노테이션 사용 금지 (@ManyToOne, @OneToMany 등)</li>
 *   <li>모든 외래키는 Long 타입으로 직접 관리</li>
 * </ul>
 */
@Entity
@Table(name = "orders")
public class OrderJpaEntity extends BaseAuditEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "order_number", nullable = false, length = 50)
    private String orderNumber;

    @Column(name = "customer_id", nullable = false)
    private Long customerId;  // ✅ Long FK (관계 어노테이션 금지)

    @Column(name = "total_amount", nullable = false, precision = 15, scale = 2)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    private OrderStatus status;

    /**
     * JPA 기본 생성자 (protected)
     *
     * <p>JPA 스펙 요구사항으로 반드시 필요합니다.</p>
     */
    protected OrderJpaEntity() {
    }

    /**
     * 전체 필드 생성자 (private)
     *
     * <p>직접 호출 금지, of() 스태틱 메서드로만 생성하세요.</p>
     */
    private OrderJpaEntity(
        Long id,
        String orderNumber,
        Long customerId,
        BigDecimal totalAmount,
        OrderStatus status,
        LocalDateTime createdAt,
        LocalDateTime updatedAt
    ) {
        super(createdAt, updatedAt);  // ✅ 부모 필드 초기화 필수
        this.id = id;
        this.orderNumber = orderNumber;
        this.customerId = customerId;
        this.totalAmount = totalAmount;
        this.status = status;
    }

    /**
     * of() 스태틱 팩토리 메서드 (Mapper 전용)
     *
     * <p>Entity 생성은 반드시 이 메서드를 통해서만 가능합니다.</p>
     */
    public static OrderJpaEntity of(
        Long id,
        String orderNumber,
        Long customerId,
        BigDecimal totalAmount,
        OrderStatus status,
        LocalDateTime createdAt,
        LocalDateTime updatedAt
    ) {
        return new OrderJpaEntity(
            id, orderNumber, customerId, totalAmount, status, createdAt, updatedAt
        );
    }

    // ===== Getters (Setter 제공 금지) =====

    public Long getId() { return id; }
    public String getOrderNumber() { return orderNumber; }
    public Long getCustomerId() { return customerId; }
    public BigDecimal getTotalAmount() { return totalAmount; }
    public OrderStatus getStatus() { return status; }
    // createdAt, updatedAt은 BaseAuditEntity에서 제공
}
```

### 2. SoftDeletableEntity 상속 (소프트 딜리트)

```java
package com.ryuqq.adapter.out.persistence.product.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import com.ryuqq.adapter.out.persistence.common.entity.SoftDeletableEntity;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * ProductJpaEntity - 상품 JPA Entity (Soft Delete 지원)
 *
 * <p><strong>SoftDeletableEntity 상속:</strong></p>
 * <ul>
 *   <li>공통 감사 필드 상속: createdAt, updatedAt, deletedAt</li>
 *   <li>isDeleted(), isActive() 메서드 제공</li>
 * </ul>
 */
@Entity
@Table(name = "products")
public class ProductJpaEntity extends SoftDeletableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "name", nullable = false, length = 200)
    private String name;

    @Column(name = "price", nullable = false, precision = 15, scale = 2)
    private BigDecimal price;

    @Column(name = "stock", nullable = false)
    private Integer stock;

    @Column(name = "category_id", nullable = false)
    private Long categoryId;  // ✅ Long FK

    protected ProductJpaEntity() {
    }

    private ProductJpaEntity(
        Long id,
        String name,
        BigDecimal price,
        Integer stock,
        Long categoryId,
        LocalDateTime createdAt,
        LocalDateTime updatedAt,
        LocalDateTime deletedAt  // ✅ Soft Delete
    ) {
        super(createdAt, updatedAt, deletedAt);
        this.id = id;
        this.name = name;
        this.price = price;
        this.stock = stock;
        this.categoryId = categoryId;
    }

    public static ProductJpaEntity of(
        Long id,
        String name,
        BigDecimal price,
        Integer stock,
        Long categoryId,
        LocalDateTime createdAt,
        LocalDateTime updatedAt,
        LocalDateTime deletedAt
    ) {
        return new ProductJpaEntity(
            id, name, price, stock, categoryId, createdAt, updatedAt, deletedAt
        );
    }

    // ===== Getters (Setter 제공 금지) =====

    public Long getId() { return id; }
    public String getName() { return name; }
    public BigDecimal getPrice() { return price; }
    public Integer getStock() { return stock; }
    public Long getCategoryId() { return categoryId; }
    // deletedAt, isDeleted(), isActive()는 SoftDeletableEntity에서 제공
}
```

### 3. 상속 없음 (시간/삭제 불필요)

```java
package com.ryuqq.adapter.out.persistence.session.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;

/**
 * SessionTokenJpaEntity - 세션 토큰 JPA Entity (감사 정보 없음)
 *
 * <p>임시 데이터로 시간 정보 불필요</p>
 */
@Entity
@Table(name = "session_tokens")
public class SessionTokenJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "token", nullable = false, length = 255)
    private String token;

    @Column(name = "user_id", nullable = false)
    private Long userId;

    @Column(name = "expires_at", nullable = false)
    private LocalDateTime expiresAt;

    protected SessionTokenJpaEntity() {
    }

    private SessionTokenJpaEntity(Long id, String token, Long userId, LocalDateTime expiresAt) {
        this.id = id;
        this.token = token;
        this.userId = userId;
        this.expiresAt = expiresAt;
    }

    public static SessionTokenJpaEntity of(Long id, String token, Long userId, LocalDateTime expiresAt) {
        return new SessionTokenJpaEntity(id, token, userId, expiresAt);
    }

    public Long getId() { return id; }
    public String getToken() { return token; }
    public Long getUserId() { return userId; }
    public LocalDateTime getExpiresAt() { return expiresAt; }
}
```

---

## EntityMapper 코드 템플릿

### 1. BaseAuditEntity 상속 경우

```java
package com.ryuqq.adapter.out.persistence.order.mapper;

import org.springframework.stereotype.Component;

import com.ryuqq.adapter.out.persistence.order.entity.OrderJpaEntity;
import com.ryuqq.domain.order.aggregate.Order;
import com.ryuqq.domain.order.vo.CustomerId;
import com.ryuqq.domain.order.vo.Money;
import com.ryuqq.domain.order.vo.OrderAudit;
import com.ryuqq.domain.order.vo.OrderId;
import com.ryuqq.domain.order.vo.OrderNumber;

/**
 * OrderJpaEntityMapper - Entity ↔ Domain 변환 Mapper
 *
 * <p><strong>변환 책임:</strong></p>
 * <ul>
 *   <li>Order → OrderJpaEntity (저장용)</li>
 *   <li>OrderJpaEntity → Order (조회용)</li>
 * </ul>
 *
 * <p><strong>핵심 규칙:</strong></p>
 * <ul>
 *   <li>비즈니스 로직 금지 (단순 변환만)</li>
 *   <li>시간 생성 금지 (Domain의 시간 전달)</li>
 *   <li>Entity.of() 메서드 사용</li>
 *   <li>Domain.reconstitute() 메서드 사용</li>
 * </ul>
 */
@Component
public class OrderJpaEntityMapper {

    /**
     * Domain → Entity 변환 (저장 시 사용)
     *
     * @param domain Order 도메인
     * @return OrderJpaEntity
     */
    public OrderJpaEntity toEntity(Order domain) {
        return OrderJpaEntity.of(
            domain.id() != null ? domain.id().value() : null,
            domain.orderNumber().value(),
            domain.customerId().value(),
            domain.totalAmount().value(),
            domain.status(),
            domain.audit().createdAt(),
            domain.audit().updatedAt()
        );
    }

    /**
     * Entity → Domain 변환 (조회 시 사용)
     *
     * @param entity OrderJpaEntity
     * @return Order 도메인
     */
    public Order toDomain(OrderJpaEntity entity) {
        return Order.reconstitute(
            OrderId.of(entity.getId()),
            OrderNumber.of(entity.getOrderNumber()),
            CustomerId.of(entity.getCustomerId()),
            Money.of(entity.getTotalAmount()),
            entity.getStatus(),
            OrderAudit.of(entity.getCreatedAt(), entity.getUpdatedAt())
        );
    }
}
```

### 2. SoftDeletableEntity 상속 경우

```java
package com.ryuqq.adapter.out.persistence.product.mapper;

import org.springframework.stereotype.Component;

import com.ryuqq.adapter.out.persistence.product.entity.ProductJpaEntity;
import com.ryuqq.domain.product.aggregate.Product;
import com.ryuqq.domain.product.vo.CategoryId;
import com.ryuqq.domain.product.vo.Money;
import com.ryuqq.domain.product.vo.ProductAudit;
import com.ryuqq.domain.product.vo.ProductId;
import com.ryuqq.domain.product.vo.ProductName;
import com.ryuqq.domain.product.vo.Stock;

/**
 * ProductJpaEntityMapper - Entity ↔ Domain 변환 Mapper (Soft Delete 지원)
 */
@Component
public class ProductJpaEntityMapper {

    public ProductJpaEntity toEntity(Product domain) {
        return ProductJpaEntity.of(
            domain.id() != null ? domain.id().value() : null,
            domain.name().value(),
            domain.price().value(),
            domain.stock().value(),
            domain.categoryId().value(),
            domain.audit().createdAt(),
            domain.audit().updatedAt(),
            domain.audit().deletedAt()  // ✅ deletedAt 전달
        );
    }

    public Product toDomain(ProductJpaEntity entity) {
        return Product.reconstitute(
            ProductId.of(entity.getId()),
            ProductName.of(entity.getName()),
            Money.of(entity.getPrice()),
            Stock.of(entity.getStock()),
            CategoryId.of(entity.getCategoryId()),
            ProductAudit.of(
                entity.getCreatedAt(),
                entity.getUpdatedAt(),
                entity.getDeletedAt()  // ✅ deletedAt 전달
            )
        );
    }
}
```

---

## 상속 클래스 선택 기준

### BaseAuditEntity vs SoftDeletableEntity

| 상황 | 상속 클래스 | 제공 필드 |
|------|------------|----------|
| 시간 정보만 필요 | `BaseAuditEntity` | createdAt, updatedAt |
| 소프트 딜리트 필요 | `SoftDeletableEntity` | createdAt, updatedAt, deletedAt |
| 시간/삭제 불필요 | 상속 안 함 | 없음 |

### 적용 케이스

```
┌─────────────────────────────────────────────────────────┐
│            상속 클래스 선택 Decision Tree               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  소프트 딜리트 필요? ─── YES ─→ SoftDeletableEntity    │
│          │                                              │
│          NO                                             │
│          ↓                                              │
│  시간 정보 필요? ───── YES ─→ BaseAuditEntity          │
│          │                                              │
│          NO                                             │
│          ↓                                              │
│      상속 안 함                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 설명 | 적용 대상 |
|------|------|----------|
| Long FK 전략 | 모든 외래키는 `Long` 타입 | Entity |
| `*JpaEntity` 네이밍 | Entity 클래스명 접미사 | Entity |
| protected 기본 생성자 | JPA 스펙 요구사항 | Entity |
| private 전체 필드 생성자 | 무분별한 생성 방지 | Entity |
| public static of() | 팩토리 메서드만 노출 | Entity |
| Getter만 제공 | Setter 금지 | Entity |
| `@Component` | Spring Bean 등록 | Mapper |
| `*Mapper` 네이밍 | Mapper 클래스명 접미사 | Mapper |
| toEntity() | Domain → Entity 변환 | Mapper |
| toDomain() | Entity → Domain 변환 | Mapper |
| Entity.of() 호출 | new 생성자 직접 호출 금지 | Mapper |
| Domain.reconstitute() 호출 | DB 재구성용 메서드 사용 | Mapper |

### ❌ PROHIBITED (금지)

| 항목 | 이유 | 대안 |
|------|------|------|
| `@ManyToOne` | N+1 문제, 복잡도 | Long FK |
| `@OneToMany` | N+1 문제, 복잡도 | Long FK |
| `@OneToOne` | N+1 문제, 복잡도 | Long FK |
| `@ManyToMany` | N+1 문제, 복잡도 | 중간 테이블 Entity |
| Lombok | 명시적 코드 원칙 | Plain Java |
| Setter | 불변성 보장 | of() 메서드 |
| new Entity() | 생성자 숨김 | Entity.of() |
| LocalDateTime.now() (Mapper) | 시간 생성은 Domain 책임 | Domain 시간 전달 |
| Static 메서드 (Mapper) | Spring Bean 필요 | Instance 메서드 |
| 비즈니스 로직 (Entity) | Domain Layer 책임 | Domain으로 이동 |
| 비즈니스 로직 (Mapper) | 단순 변환만 | Domain으로 이동 |

---

## 패키지 구조

```
adapter-out/persistence-mysql/
└── src/main/java/com/ryuqq/adapter/out/persistence/
    ├── common/
    │   └── entity/
    │       ├── BaseAuditEntity.java
    │       └── SoftDeletableEntity.java
    └── {bc}/
        ├── entity/
        │   └── {Domain}JpaEntity.java
        └── mapper/
            └── {Domain}JpaEntityMapper.java
```

---

## 체크리스트 (Output Checklist)

### JPA Entity 체크리스트

- [ ] `@Entity`, `@Table(name = "...")` 어노테이션
- [ ] `*JpaEntity` 네이밍 규칙
- [ ] BaseAuditEntity 또는 SoftDeletableEntity 상속 검토
- [ ] Long FK 전략 (JPA 관계 어노테이션 없음)
- [ ] `@Id @GeneratedValue(strategy = GenerationType.IDENTITY)` PK 설정
- [ ] `@Column` 어노테이션으로 컬럼 매핑
- [ ] `@Enumerated(EnumType.STRING)` Enum 매핑
- [ ] **protected 기본 생성자** (JPA 스펙)
- [ ] **private 전체 필드 생성자** (무분별한 생성 방지)
- [ ] **public static of() 메서드** (Mapper 전용)
- [ ] 전체 필드 생성자에서 `super(createdAt, updatedAt)` 호출 (상속 시)
- [ ] Getter만 제공 (Setter 없음)
- [ ] Lombok 사용 없음
- [ ] 비즈니스 로직 없음
- [ ] Javadoc 작성

### EntityMapper 체크리스트

- [ ] `@Component` 어노테이션
- [ ] `*Mapper` 네이밍 규칙 (`*JpaEntityMapper` 권장)
- [ ] **public toEntity(Domain)** 메서드 존재
  - [ ] Entity.of() 메서드 사용
  - [ ] Domain의 시간 필드 직접 전달
- [ ] **public toDomain(Entity)** 메서드 존재
  - [ ] Domain.reconstitute() 메서드 사용
  - [ ] Value Object 재구성
- [ ] Static 메서드 없음 (Instance 메서드만)
- [ ] 비즈니스 로직 없음 (단순 변환만)
- [ ] 검증 로직 없음 (Domain에서 검증)
- [ ] LocalDateTime.now() 사용 없음
- [ ] Lombok 사용 없음
- [ ] Javadoc 작성

---

## 테스트 체크리스트

### Entity ArchUnit 테스트 (16개 규칙)

- [ ] Lombok 금지 (6개: @Data, @Getter, @Setter, @Builder, @AllArgsConstructor, @NoArgsConstructor)
- [ ] JPA 관계 금지 (4개: @ManyToOne, @OneToMany, @OneToOne, @ManyToMany)
- [ ] Setter 메서드 금지
- [ ] 비즈니스 로직 메서드 금지
- [ ] protected/public 기본 생성자 필수
- [ ] private 전체 필드 생성자 필수
- [ ] public static of() 메서드 필수
- [ ] `*JpaEntity` 네이밍 필수

### Mapper ArchUnit 테스트 (15개 규칙)

- [ ] `@Component` 필수
- [ ] Lombok 금지 (9개)
- [ ] Static 변환 메서드 금지
- [ ] 비즈니스 로직 메서드 금지
- [ ] toEntity() 메서드 필수
- [ ] toDomain() 메서드 필수
- [ ] `*Mapper` 네이밍 필수

### 단위 테스트

- [ ] toEntity(): Domain → Entity 정확히 변환
- [ ] toDomain(): Entity → Domain 정확히 변환
- [ ] Null 처리 확인 (신규 생성 시 id = null)
- [ ] Value Object 재구성 확인

---

## 참조 문서

- **Entity Guide**: `docs/coding_convention/04-persistence-layer/mysql/entity/entity-guide.md`
- **Entity ArchUnit**: `docs/coding_convention/04-persistence-layer/mysql/entity/entity-archunit.md`
- **Entity Test Guide**: `docs/coding_convention/04-persistence-layer/mysql/entity/entity-test-guide.md`
- **Mapper Guide**: `docs/coding_convention/04-persistence-layer/mysql/mapper/mapper-guide.md`
- **Mapper ArchUnit**: `docs/coding_convention/04-persistence-layer/mysql/mapper/mapper-archunit.md`
- **Mapper Test Guide**: `docs/coding_convention/04-persistence-layer/mysql/mapper/mapper-test-guide.md`
