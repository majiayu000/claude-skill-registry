---
name: domain-expert
version: 3.0.0
description: Domain Layer 전문가. DDD Aggregate Root 설계, VO 불변 객체, Domain Event, Domain Exception 구현. Law of Demeter 적용, Tell Don't Ask 패턴 강제. Lombok 금지, Setter 금지, 외부 의존성 금지.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, domain, ddd, aggregate, vo, event, exception, pure-java]
---

# Domain Layer 전문가

## 🎯 목적 (Purpose)

Domain Layer의 핵심 객체(Aggregate, Value Object, Domain Event, Domain Exception) 설계 및 구현 가이드를 제공합니다. DDD 원칙에 따라 비즈니스 로직을 순수한 도메인 객체로 캡슐화합니다.

## 활성화 조건

- `/impl domain {feature}` 명령 실행 시
- `/plan` 실행 후 Domain Layer 작업 시
- aggregate, vo, domain event, domain exception 키워드 언급 시

---

## ✅ 완료 기준 (Acceptance Criteria)

### Aggregate Root
- [ ] 생성자 `private` + 정적 팩토리 메서드 3종 (`forNew`, `of`, `reconstitute`)
- [ ] ID 필드 `final` 선언
- [ ] 비즈니스 메서드로 상태 변경 (Setter 금지)
- [ ] `Clock` 주입으로 시간 생성 (`clock.instant()`)
- [ ] Domain Event 등록 (`registerEvent`, `pullDomainEvents`)
- [ ] 불변식(Invariant) 검증 로직 포함

### Value Object
- [ ] `record` 키워드 사용
- [ ] Compact Constructor에서 Self-Validation
- [ ] 정적 팩토리 메서드 (`of`, ID VO는 `forNew` 추가)
- [ ] 외부 의존성 제로

### Domain Exception
- [ ] `DomainException` 상속
- [ ] `ErrorCode` 기반 생성자
- [ ] 컨텍스트 정보 (`Map<String, Object> args`)

### Domain Event
- [ ] `DomainEvent` 인터페이스 구현
- [ ] `record` 타입 사용
- [ ] `from(Aggregate, Instant)` 팩토리 메서드
- [ ] VO 타입 필드만 사용 (원시 타입 금지)

---

## 📋 산출물 체크리스트 (Output Checklist)

| 산출물 | 필수 | 위치 | 네이밍 규칙 |
|--------|------|------|-------------|
| Aggregate Root | ✅ | `domain/{bc}/aggregate/{name}/` | `{Name}.java` |
| Value Object (ID) | ✅ | `domain/{bc}/vo/` | `{Name}Id.java` |
| Value Object (일반) | 선택 | `domain/{bc}/vo/` | `{Name}.java` |
| Domain Exception | ✅ | `domain/{bc}/exception/` | `{Name}Exception.java` |
| ErrorCode Enum | ✅ | `domain/{bc}/exception/` | `{BC}ErrorCode.java` |
| Domain Event | 선택 | `domain/{bc}/event/` | `{Name}Event.java` |

---

## 📝 코드 템플릿 (Code Templates)

### 1. Aggregate Root 템플릿

```java
package com.ryuqq.domain.{bc}.aggregate.{name};

import com.ryuqq.domain.common.event.DomainEvent;
import com.ryuqq.domain.{bc}.vo.{Name}Id;
import com.ryuqq.domain.{bc}.vo.{Name}Status;
import com.ryuqq.domain.{bc}.event.{Name}CreatedEvent;
import com.ryuqq.domain.{bc}.exception.{Name}InvalidStateException;

import java.time.Clock;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

/**
 * {Name} Aggregate Root
 *
 * <p><strong>불변식(Invariant)</strong>:</p>
 * <ul>
 *   <li>TODO: 비즈니스 불변식 정의</li>
 * </ul>
 *
 * @author development-team
 * @since 1.0.0
 */
public class {Name} {

    // ==================== 필드 ====================

    private final {Name}Id id;
    private {Name}Status status;
    private final Instant createdAt;
    private Instant updatedAt;
    private final Clock clock;
    private final List<DomainEvent> domainEvents = new ArrayList<>();

    // ==================== 생성자 (private) ====================

    private {Name}({Name}Id id, {Name}Status status,
                   Instant createdAt, Instant updatedAt, Clock clock) {
        if (status == null) {
            throw new IllegalArgumentException("Status must not be null - this is a bug");
        }
        if (clock == null) {
            throw new IllegalArgumentException("Clock must not be null - this is a bug");
        }
        this.id = id;
        this.status = status;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.clock = clock;
    }

    // ==================== 정적 팩토리 메서드 ====================

    /**
     * 신규 생성 (Auto Increment - ID null)
     */
    public static {Name} forNew(Clock clock) {
        Instant now = clock.instant();
        {Name} entity = new {Name}(null, {Name}Status.CREATED, now, now, clock);
        entity.registerEvent({Name}CreatedEvent.from(entity, now));
        return entity;
    }

    /**
     * ID 기반 생성 (ID 필수)
     */
    public static {Name} of({Name}Id id, {Name}Status status,
                            Instant createdAt, Instant updatedAt, Clock clock) {
        if (id == null) {
            throw new IllegalArgumentException("ID는 null일 수 없습니다.");
        }
        return new {Name}(id, status, createdAt, updatedAt, clock);
    }

    /**
     * 영속성 복원 (Mapper 전용, Event 없음)
     */
    public static {Name} reconstitute({Name}Id id, {Name}Status status,
                                       Instant createdAt, Instant updatedAt, Clock clock) {
        if (id == null) {
            throw new IllegalArgumentException("ID는 null일 수 없습니다.");
        }
        return new {Name}(id, status, createdAt, updatedAt, clock);
    }

    // ==================== 비즈니스 메서드 ====================

    /**
     * 상태 변경 예시 메서드
     *
     * @throws {Name}InvalidStateException 변경 불가능한 상태인 경우
     */
    public void activate() {
        if (!canActivate()) {
            throw {Name}InvalidStateException.cannotActivate(
                this.id != null ? this.id.value() : null,
                this.status.name()
            );
        }
        {Name}Status previousStatus = this.status;
        this.status = {Name}Status.ACTIVE;
        this.updatedAt = clock.instant();
        // registerEvent(...);
    }

    // ==================== 판단 메서드 (도메인 객체가 스스로 판단) ====================

    private boolean canActivate() {
        return this.status == {Name}Status.CREATED;
    }

    public boolean isActive() {
        return this.status == {Name}Status.ACTIVE;
    }

    // ==================== Event 관리 ====================

    protected void registerEvent(DomainEvent event) {
        this.domainEvents.add(event);
    }

    public List<DomainEvent> pullDomainEvents() {
        List<DomainEvent> events = List.copyOf(this.domainEvents);
        this.domainEvents.clear();
        return events;
    }

    // ==================== Getter (Setter 금지) ====================

    public {Name}Id id() { return id; }
    public {Name}Status status() { return status; }
    public Instant createdAt() { return createdAt; }
    public Instant updatedAt() { return updatedAt; }
}
```

### 2. ID Value Object 템플릿 (Long - Auto Increment)

```java
package com.ryuqq.domain.{bc}.vo;

/**
 * {Name} ID Value Object (Auto Increment)
 *
 * <p><strong>DB 전략</strong>: MySQL AUTO_INCREMENT - DB가 ID 할당</p>
 *
 * @param value ID 값 (null 허용: 신규 생성 시)
 * @author development-team
 * @since 1.0.0
 */
public record {Name}Id(Long value) {

    /**
     * Compact Constructor (검증 로직)
     */
    public {Name}Id {
        if (value != null && value <= 0) {
            throw new IllegalArgumentException("{Name}Id는 양수여야 합니다: " + value);
        }
    }

    /**
     * 신규 생성 - DB AUTO_INCREMENT가 ID 할당 예정
     */
    public static {Name}Id forNew() {
        return new {Name}Id(null);
    }

    /**
     * 기존 ID 참조 - null 금지
     */
    public static {Name}Id of(Long value) {
        if (value == null) {
            throw new IllegalArgumentException("기존 {Name}Id는 null일 수 없습니다");
        }
        return new {Name}Id(value);
    }

    /**
     * 신규 엔티티 여부 확인
     */
    public boolean isNew() {
        return value == null;
    }
}
```

### 3. 일반 Value Object 템플릿 (Money)

```java
package com.ryuqq.domain.{bc}.vo;

import com.ryuqq.domain.{bc}.exception.MoneyValidationException;

/**
 * Money Value Object
 *
 * <p><strong>도메인 규칙</strong>: 금액은 0 이상이어야 한다.</p>
 *
 * @param amount 금액 (0 이상)
 * @author development-team
 * @since 1.0.0
 */
public record Money(Long amount) {

    public static final Money ZERO = Money.of(0L);

    /**
     * Compact Constructor (검증 로직)
     *
     * @throws MoneyValidationException 금액이 음수인 경우 (400)
     */
    public Money {
        if (amount == null) {
            throw new IllegalArgumentException("금액은 null일 수 없습니다.");
        }
        if (amount < 0) {
            throw new MoneyValidationException(amount);
        }
    }

    public static Money of(Long amount) {
        return new Money(amount);
    }

    public Money add(Money other) {
        return new Money(this.amount + other.amount);
    }

    public Money subtract(Money other) {
        return new Money(this.amount - other.amount);
    }

    public Money multiply(int multiplier) {
        return new Money(this.amount * multiplier);
    }

    public boolean isGreaterThan(Money other) {
        return this.amount > other.amount;
    }
}
```

### 4. ErrorCode Enum 템플릿

```java
package com.ryuqq.domain.{bc}.exception;

import com.ryuqq.domain.common.exception.ErrorCode;

/**
 * {BC} Bounded Context 에러 코드
 *
 * <p><strong>에러 코드 규칙</strong>: {BC}-{3자리 숫자}</p>
 * <ul>
 *   <li>0XX: 404 Not Found</li>
 *   <li>01X: 400 Bad Request (입력 검증)</li>
 *   <li>02X: 409 Conflict</li>
 *   <li>03X: 400 Bad Request (비즈니스 룰)</li>
 *   <li>05X: 500 Internal Server Error</li>
 * </ul>
 *
 * @author development-team
 * @since 1.0.0
 */
public enum {BC}ErrorCode implements ErrorCode {

    // === 404 Not Found ===
    {NAME}_NOT_FOUND("{BC}-001", 404, "{Name} not found"),

    // === 400 Bad Request (Validation) ===
    INVALID_{NAME}_STATUS("{BC}-010", 400, "Invalid {name} status"),
    INVALID_MONEY_AMOUNT("{BC}-011", 400, "Invalid money amount"),

    // === 409 Conflict ===
    {NAME}_ALREADY_EXISTS("{BC}-020", 409, "{Name} already exists"),

    // === 400 Bad Request (Business Rule) ===
    INVALID_{NAME}_STATE("{BC}-030", 400, "Invalid {name} state for this operation");

    private final String code;
    private final int httpStatus;
    private final String message;

    {BC}ErrorCode(String code, int httpStatus, String message) {
        this.code = code;
        this.httpStatus = httpStatus;
        this.message = message;
    }

    @Override
    public String getCode() { return code; }

    @Override
    public int getHttpStatus() { return httpStatus; }

    @Override
    public String getMessage() { return message; }
}
```

### 5. Domain Exception 템플릿 (Not Found)

```java
package com.ryuqq.domain.{bc}.exception;

import com.ryuqq.domain.common.exception.DomainException;
import java.util.Map;

/**
 * {Name}NotFoundException - {Name}를 찾을 수 없을 때 발생
 *
 * <p>HTTP 응답: 404 NOT FOUND</p>
 *
 * @author development-team
 * @since 1.0.0
 */
public class {Name}NotFoundException extends DomainException {

    public {Name}NotFoundException(Long id) {
        super(
            {BC}ErrorCode.{NAME}_NOT_FOUND,
            String.format("{Name} not found: %d", id),
            Map.of("{name}Id", id)
        );
    }
}
```

### 6. Domain Exception 템플릿 (Invalid State)

```java
package com.ryuqq.domain.{bc}.exception;

import com.ryuqq.domain.common.exception.DomainException;
import java.util.Map;

/**
 * {Name}InvalidStateException - 상태 전환 불가 시 발생
 *
 * <p>HTTP 응답: 400 BAD REQUEST</p>
 *
 * @author development-team
 * @since 1.0.0
 */
public class {Name}InvalidStateException extends DomainException {

    private {Name}InvalidStateException(String message, Map<String, Object> args) {
        super({BC}ErrorCode.INVALID_{NAME}_STATE, message, args);
    }

    public static {Name}InvalidStateException cannotActivate(Long id, String currentStatus) {
        return new {Name}InvalidStateException(
            String.format("Cannot activate {name} %d. Current status: %s", id, currentStatus),
            Map.of("{name}Id", id, "currentStatus", currentStatus, "action", "activate")
        );
    }

    public static {Name}InvalidStateException cannotDeactivate(Long id, String currentStatus) {
        return new {Name}InvalidStateException(
            String.format("Cannot deactivate {name} %d. Current status: %s", id, currentStatus),
            Map.of("{name}Id", id, "currentStatus", currentStatus, "action", "deactivate")
        );
    }
}
```

### 7. Domain Event 템플릿

```java
package com.ryuqq.domain.{bc}.event;

import com.ryuqq.domain.common.event.DomainEvent;
import com.ryuqq.domain.{bc}.aggregate.{name}.{Name};
import com.ryuqq.domain.{bc}.vo.{Name}Id;
import com.ryuqq.domain.{bc}.vo.{Name}Status;

import java.time.Instant;

/**
 * {Name} 생성 이벤트
 *
 * <p>{Name}가 성공적으로 생성되었을 때 발행됩니다.</p>
 *
 * @param {name}Id {Name} ID (VO)
 * @param status 상태 (VO)
 * @param occurredAt 이벤트 발생 시각
 * @author development-team
 * @since 1.0.0
 */
public record {Name}CreatedEvent(
    {Name}Id {name}Id,
    {Name}Status status,
    Instant occurredAt
) implements DomainEvent {

    /**
     * Aggregate로부터 Event 생성
     *
     * @param entity {Name} Aggregate
     * @param occurredAt 이벤트 발생 시각
     * @return {Name} 생성 이벤트
     */
    public static {Name}CreatedEvent from({Name} entity, Instant occurredAt) {
        return new {Name}CreatedEvent(
            entity.id(),
            entity.status(),
            occurredAt
        );
    }
}
```

---

## ⚠️ Zero-Tolerance Rules

### 🚫 절대 금지

| 규칙 | 잘못된 예 | 올바른 예 |
|------|-----------|-----------|
| **Lombok 금지** | `@Data`, `@Getter` | Plain Java 수동 작성 |
| **Setter 금지** | `setStatus()` | `activate()`, `cancel()` 비즈니스 메서드 |
| **Getter 체이닝 금지** | `order.getCustomer().getAddress()` | `order.shippingCity()` |
| **LocalDateTime 금지** | `LocalDateTime createdAt` | `Instant createdAt` |
| **Instant.now() 직접 호출** | `Instant.now()` | `clock.instant()` |
| **Long FK 금지 (VO 필수)** | `Long paymentId` | `PaymentId paymentId` |
| **외부 의존성 금지** | `@Entity`, `@Component` | 순수 Java |

### ✅ 필수 규칙

| 규칙 | 설명 |
|------|------|
| **private 생성자** | 정적 팩토리 메서드로만 생성 |
| **정적 팩토리 3종** | `forNew()`, `of()`, `reconstitute()` |
| **Clock 주입** | 테스트 가능성 보장 |
| **Compact Constructor** | VO에서 Self-Validation |
| **record 사용** | VO, Event는 record 필수 |

---

## 🔗 참조 문서 (Convention References)

### 필수 참조
| 문서 | 경로 | 용도 |
|------|------|------|
| Domain Guide | `docs/coding_convention/02-domain-layer/domain-guide.md` | 전체 개요 |
| Aggregate Guide | `docs/coding_convention/02-domain-layer/aggregate/aggregate-guide.md` | Aggregate 설계 |
| Aggregate Test | `docs/coding_convention/02-domain-layer/aggregate/aggregate-test-guide.md` | Aggregate 테스트 |
| Aggregate ArchUnit | `docs/coding_convention/02-domain-layer/aggregate/aggregate-archunit.md` | ArchUnit 규칙 |
| VO Guide | `docs/coding_convention/02-domain-layer/vo/vo-guide.md` | Value Object 설계 |
| VO Test | `docs/coding_convention/02-domain-layer/vo/vo-test-guide.md` | VO 테스트 |
| VO ArchUnit | `docs/coding_convention/02-domain-layer/vo/vo-archunit.md` | VO ArchUnit 규칙 |
| Exception Guide | `docs/coding_convention/02-domain-layer/exception/exception-guide.md` | 예외 설계 |
| Exception Test | `docs/coding_convention/02-domain-layer/exception/exception-test-guide.md` | 예외 테스트 |
| Event Guide | `docs/coding_convention/02-domain-layer/event/event-guide.md` | Event 설계 |
| Event ArchUnit | `docs/coding_convention/02-domain-layer/event/event-archunit.md` | Event ArchUnit |

---

## 📦 패키지 구조

```
domain/
├─ common/                        # 공통 인터페이스
│  ├─ event/
│  │  └─ DomainEvent.java         # 도메인 이벤트 인터페이스
│  ├─ exception/
│  │  ├─ DomainException.java     # 기본 도메인 예외
│  │  └─ ErrorCode.java           # 에러 코드 인터페이스
│  └─ util/
│     └─ ClockHolder.java         # Clock 인터페이스
│
└─ {boundedContext}/              # 예: order
   ├─ aggregate/
   │  └─ {aggregateName}/         # 예: order
   │     ├─ Order.java            # Aggregate Root
   │     └─ OrderLineItem.java    # 종속 Entity
   │
   ├─ vo/
   │  ├─ OrderId.java             # ID VO
   │  ├─ Money.java               # 일반 VO
   │  └─ OrderStatus.java         # Enum VO
   │
   ├─ event/
   │  └─ OrderCreatedEvent.java   # Domain Event
   │
   └─ exception/
      ├─ OrderErrorCode.java      # ErrorCode Enum
      ├─ OrderNotFoundException.java
      └─ OrderInvalidStateException.java
```

---

## 🧪 테스트 체크리스트

### Aggregate 테스트
- [ ] `forNew()` - 신규 생성 및 Event 등록 확인
- [ ] `of()` - ID null 시 예외 발생 확인
- [ ] `reconstitute()` - Event 미등록 확인
- [ ] 비즈니스 메서드 - 상태 전환 성공/실패 케이스
- [ ] 불변식 위반 시 예외 발생 확인

### Value Object 테스트
- [ ] `of()` - 유효한 값으로 생성 성공
- [ ] Compact Constructor - 유효하지 않은 값 시 예외
- [ ] `equals()/hashCode()` - 값 동등성 확인
- [ ] ID VO - `forNew()`, `isNew()` 테스트

### Exception 테스트
- [ ] ErrorCode 매핑 확인
- [ ] HTTP 상태 코드 확인
- [ ] 컨텍스트 정보(args) 확인

### Event 테스트
- [ ] `from()` - Aggregate에서 Event 생성
- [ ] 필드 값 정확성 확인
- [ ] `occurredAt` 시간 확인
