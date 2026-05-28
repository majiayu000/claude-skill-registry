---
name: usecase-expert
version: 3.0.0
description: Port-In 인터페이스 설계, UseCase/Service 구현, CQRS Command/Query 분리. CommandService와 QueryService 템플릿 제공. @Transactional은 Facade/Manager 책임.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, application, usecase, cqrs, port-in, service, command, query]
---

# UseCase 전문가 (Application Layer - UseCase & Service)

## 활성화 조건

- `/impl application {feature}` 명령 실행 시
- `/plan` 실행 후 Application Layer UseCase 작업 시
- usecase, port-in, service, cqrs 키워드 언급 시

---

## 🎯 목적

Application Layer의 **UseCase(Port-In)** 인터페이스와 **Service** 구현체를 설계하고 구현한다.

- **UseCase = 단일 비즈니스 트랜잭션** 추상화
- **CQRS 분리** (Command/Query 완전 분리)
- **Port/Adapter 패턴** 준수
- **Transaction 경계** Facade/Manager 위임

---

## ✅ 완료 기준

### Command UseCase

- [ ] `{Action}{Bc}UseCase` Interface 정의
- [ ] `{Action}{Bc}Command` DTO record 정의
- [ ] `{Bc}Response` DTO record 정의
- [ ] `{Action}{Bc}Service` 구현체 작성
- [ ] `execute()` 단일 메서드 패턴 준수
- [ ] CommandFactory, Facade/Manager, Assembler 의존성 구성

### Query UseCase

- [ ] `Get{Bc}UseCase` 또는 `Search{Bc}UseCase` Interface 정의
- [ ] `Get{Bc}Query` 또는 `Search{Bc}Query` DTO record 정의
- [ ] `{Bc}Response` DTO record 정의
- [ ] `{QueryType}{Bc}Service` 구현체 작성
- [ ] QueryFactory, ReadManager/QueryFacade, Assembler 의존성 구성

---

## 📋 산출물 체크리스트

| 산출물 | 패키지 | 네이밍 규칙 |
|--------|--------|-------------|
| Command UseCase | `port.in.command` | `{Action}{Bc}UseCase` |
| Query UseCase | `port.in.query` | `Get{Bc}UseCase`, `Search{Bc}UseCase` |
| Command Service | `service.command` | `{Action}{Bc}Service` |
| Query Service | `service.query` | `Get{Bc}Service`, `Search{Bc}Service` |
| Command DTO | `dto.command` | `{Action}{Bc}Command` |
| Query DTO | `dto.query` | `Get{Bc}Query`, `Search{Bc}Query` |
| Response DTO | `dto.response` | `{Bc}Response`, `{Bc}DetailResponse` |

---

## 📝 코드 템플릿

### 1. Command UseCase Interface

```java
package com.ryuqq.application.{bc}.port.in.command;

import com.ryuqq.application.{bc}.dto.command.{Action}{Bc}Command;
import com.ryuqq.application.{bc}.dto.response.{Bc}Response;

/**
 * {Action} {Bc} UseCase (Command)
 *
 * <p>상태 변경을 담당하는 Inbound Port</p>
 *
 * @author development-team
 * @since 1.0.0
 */
public interface {Action}{Bc}UseCase {

    /**
     * {Action} {Bc}
     *
     * @param command {Action} 명령
     * @return {Action} 결과
     */
    {Bc}Response execute({Action}{Bc}Command command);
}
```

### 2. Query UseCase Interface (단건)

```java
package com.ryuqq.application.{bc}.port.in.query;

import com.ryuqq.application.{bc}.dto.query.Get{Bc}Query;
import com.ryuqq.application.{bc}.dto.response.{Bc}DetailResponse;

/**
 * Get {Bc} UseCase (Query)
 *
 * <p>조회를 담당하는 Inbound Port</p>
 *
 * @author development-team
 * @since 1.0.0
 */
public interface Get{Bc}UseCase {

    /**
     * {Bc} 조회
     *
     * @param query 조회 조건
     * @return 조회 결과
     */
    {Bc}DetailResponse execute(Get{Bc}Query query);
}
```

### 3. Query UseCase Interface (페이지네이션)

```java
package com.ryuqq.application.{bc}.port.in.query;

import com.ryuqq.application.{bc}.dto.query.Search{Bc}Query;
import com.ryuqq.application.{bc}.dto.response.{Bc}SummaryResponse;
import com.ryuqq.application.common.dto.PageResponse;

/**
 * Search {Bc} UseCase (Pagination)
 *
 * <p>페이징 조회를 담당하는 Inbound Port</p>
 *
 * @author development-team
 * @since 1.0.0
 */
public interface Search{Bc}UseCase {

    /**
     * {Bc} 목록 페이징 조회
     *
     * @param query 검색 조건 (page, size 포함)
     * @return 페이징된 결과
     */
    PageResponse<{Bc}SummaryResponse> execute(Search{Bc}Query query);
}
```

### 4. Command DTO (Record)

```java
package com.ryuqq.application.{bc}.dto.command;

import java.util.List;

/**
 * {Action} {Bc} Command
 *
 * @author development-team
 * @since 1.0.0
 */
public record {Action}{Bc}Command(
    Long customerId,
    List<{Bc}ItemCommand> items,
    String deliveryAddress
) {
    /**
     * Compact Constructor: 불변화만
     */
    public {Action}{Bc}Command {
        items = (items != null) ? List.copyOf(items) : List.of();
    }

    public record {Bc}ItemCommand(
        Long productId,
        Integer quantity,
        Long unitPrice
    ) {}
}
```

### 5. Query DTO (Record)

```java
package com.ryuqq.application.{bc}.dto.query;

import java.time.Instant;

/**
 * Search {Bc} Query (Offset Paging)
 *
 * @author development-team
 * @since 1.0.0
 */
public record Search{Bc}Query(
    Long filterId,
    String status,
    Instant startDate,
    Instant endDate,
    String sortBy,
    String sortDirection,
    Integer page,
    Integer size
) {}
```

### 6. Response DTO (Record)

```java
package com.ryuqq.application.{bc}.dto.response;

import java.time.Instant;

/**
 * {Bc} Response
 *
 * @author development-team
 * @since 1.0.0
 */
public record {Bc}Response(
    Long id,
    String status,
    Long totalAmount,
    Instant createdAt
) {}
```

### 7. Command Service (복잡한 경우 - Facade 사용)

```java
package com.ryuqq.application.{bc}.service.command;

import com.ryuqq.application.{bc}.assembler.{Bc}Assembler;
import com.ryuqq.application.{bc}.dto.bundle.{Bc}PersistBundle;
import com.ryuqq.application.{bc}.dto.command.{Action}{Bc}Command;
import com.ryuqq.application.{bc}.dto.response.{Bc}Response;
import com.ryuqq.application.{bc}.facade.command.{Bc}Facade;
import com.ryuqq.application.{bc}.factory.command.{Bc}CommandFactory;
import com.ryuqq.application.common.config.TransactionEventRegistry;
import com.ryuqq.application.{bc}.port.in.command.{Action}{Bc}UseCase;
import com.ryuqq.domain.{bc}.aggregate.{Bc};
import org.springframework.stereotype.Service;

/**
 * {Action} {Bc} UseCase 구현체
 * - 복잡한 Command: Facade 사용 (Manager 2개 이상 조합)
 *
 * @author development-team
 * @since 1.0.0
 */
@Service
public class {Action}{Bc}Service implements {Action}{Bc}UseCase {

    private final {Bc}CommandFactory commandFactory;
    private final {Bc}Facade {bc}Facade;
    private final TransactionEventRegistry eventRegistry;
    private final {Bc}Assembler assembler;

    public {Action}{Bc}Service(
        {Bc}CommandFactory commandFactory,
        {Bc}Facade {bc}Facade,
        TransactionEventRegistry eventRegistry,
        {Bc}Assembler assembler
    ) {
        this.commandFactory = commandFactory;
        this.{bc}Facade = {bc}Facade;
        this.eventRegistry = eventRegistry;
        this.assembler = assembler;
    }

    @Override
    public {Bc}Response execute({Action}{Bc}Command command) {
        // 1. Command → Bundle (Factory)
        {Bc}PersistBundle bundle = commandFactory.createBundle(command);

        // 2. 영속화 (Facade - 여러 Manager 조합)
        {Bc} saved{Bc} = {bc}Facade.persist{Bc}Bundle(bundle);

        // 3. Event 등록 (커밋 후 발행)
        eventRegistry.registerForPublish(saved{Bc}.pullDomainEvents());

        // 4. Response 변환 (Assembler)
        return assembler.toResponse(saved{Bc});
    }
}
```

### 8. Command Service (단순한 경우 - Manager 직접)

```java
package com.ryuqq.application.{bc}.service.command;

import com.ryuqq.application.{bc}.assembler.{Bc}Assembler;
import com.ryuqq.application.{bc}.dto.command.Update{Bc}Command;
import com.ryuqq.application.{bc}.dto.response.{Bc}Response;
import com.ryuqq.application.{bc}.factory.command.{Bc}CommandFactory;
import com.ryuqq.application.{bc}.manager.command.{Bc}TransactionManager;
import com.ryuqq.application.{bc}.port.in.command.Update{Bc}UseCase;
import com.ryuqq.domain.{bc}.aggregate.{Bc};
import org.springframework.stereotype.Service;

/**
 * Update {Bc} UseCase 구현체
 * - 단순 Command: Manager 직접 호출 (1개)
 *
 * @author development-team
 * @since 1.0.0
 */
@Service
public class Update{Bc}Service implements Update{Bc}UseCase {

    private final {Bc}CommandFactory commandFactory;
    private final {Bc}TransactionManager {bc}Manager;
    private final {Bc}Assembler assembler;

    public Update{Bc}Service(
        {Bc}CommandFactory commandFactory,
        {Bc}TransactionManager {bc}Manager,
        {Bc}Assembler assembler
    ) {
        this.commandFactory = commandFactory;
        this.{bc}Manager = {bc}Manager;
        this.assembler = assembler;
    }

    @Override
    public {Bc}Response execute(Update{Bc}Command command) {
        // 1. Command → Domain (Factory)
        {Bc} {bc} = commandFactory.create(command);

        // 2. 영속화 (Manager 직접 - 단일)
        {Bc} saved{Bc} = {bc}Manager.persist({bc});

        // 3. Response 변환 (Assembler)
        return assembler.toResponse(saved{Bc});
    }
}
```

### 9. Command Service (void 반환)

```java
package com.ryuqq.application.{bc}.service.command;

import com.ryuqq.application.{bc}.dto.command.Delete{Bc}Command;
import com.ryuqq.application.{bc}.manager.command.{Bc}TransactionManager;
import com.ryuqq.application.{bc}.port.in.command.Delete{Bc}UseCase;
import com.ryuqq.domain.{bc}.aggregate.{Bc};
import com.ryuqq.domain.{bc}.vo.{Bc}Id;
import org.springframework.stereotype.Service;

/**
 * Delete {Bc} UseCase 구현체
 * - void 반환: Response 불필요
 *
 * @author development-team
 * @since 1.0.0
 */
@Service
public class Delete{Bc}Service implements Delete{Bc}UseCase {

    private final {Bc}TransactionManager {bc}Manager;

    public Delete{Bc}Service({Bc}TransactionManager {bc}Manager) {
        this.{bc}Manager = {bc}Manager;
    }

    @Override
    public void execute(Delete{Bc}Command command) {
        // 1. 조회 (Manager)
        {Bc} {bc} = {bc}Manager.getById(new {Bc}Id(command.{bc}Id()));

        // 2. 도메인 로직 실행 (Domain)
        {bc}.delete(command.reason());

        // 3. 영속화 (Manager)
        {bc}Manager.persist({bc});
    }
}
```

### 10. Query Service (복잡한 경우 - QueryFacade 사용)

```java
package com.ryuqq.application.{bc}.service.query;

import com.ryuqq.application.{bc}.assembler.{Bc}Assembler;
import com.ryuqq.application.{bc}.dto.bundle.{Bc}DetailQueryBundle;
import com.ryuqq.application.{bc}.dto.query.{Bc}DetailQuery;
import com.ryuqq.application.{bc}.dto.response.{Bc}DetailResponse;
import com.ryuqq.application.{bc}.facade.query.{Bc}QueryFacade;
import com.ryuqq.application.{bc}.factory.query.{Bc}QueryFactory;
import com.ryuqq.application.{bc}.port.in.query.Get{Bc}DetailUseCase;
import com.ryuqq.domain.{bc}.criteria.{Bc}DetailCriteria;
import org.springframework.stereotype.Service;

/**
 * Get {Bc} Detail UseCase 구현체
 * - 복잡한 Query: QueryFacade 사용 (ReadManager 2개 이상 조합)
 *
 * @author development-team
 * @since 1.0.0
 */
@Service
public class Get{Bc}DetailService implements Get{Bc}DetailUseCase {

    private final {Bc}QueryFactory queryFactory;
    private final {Bc}QueryFacade queryFacade;
    private final {Bc}Assembler assembler;

    public Get{Bc}DetailService(
        {Bc}QueryFactory queryFactory,
        {Bc}QueryFacade queryFacade,
        {Bc}Assembler assembler
    ) {
        this.queryFactory = queryFactory;
        this.queryFacade = queryFacade;
        this.assembler = assembler;
    }

    @Override
    public {Bc}DetailResponse execute({Bc}DetailQuery query) {
        // 1. Query → Criteria (Factory)
        {Bc}DetailCriteria criteria = queryFactory.createDetailCriteria(query);

        // 2. 조회 (QueryFacade - 여러 ReadManager 조합)
        {Bc}DetailQueryBundle bundle = queryFacade.fetch{Bc}Detail(criteria);

        // 3. Response 변환 (Assembler)
        return assembler.toDetailResponse(bundle);
    }
}
```

### 11. Query Service (단순한 경우 - ReadManager 직접)

```java
package com.ryuqq.application.{bc}.service.query;

import com.ryuqq.application.{bc}.assembler.{Bc}Assembler;
import com.ryuqq.application.{bc}.dto.query.Search{Bc}Query;
import com.ryuqq.application.{bc}.dto.response.{Bc}ListResponse;
import com.ryuqq.application.{bc}.factory.query.{Bc}QueryFactory;
import com.ryuqq.application.{bc}.manager.query.{Bc}ReadManager;
import com.ryuqq.application.{bc}.port.in.query.Search{Bc}UseCase;
import com.ryuqq.domain.{bc}.aggregate.{Bc};
import com.ryuqq.domain.{bc}.criteria.{Bc}SearchCriteria;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Search {Bc} UseCase 구현체
 * - 단순 Query: ReadManager 직접 호출 (1개)
 *
 * @author development-team
 * @since 1.0.0
 */
@Service
public class Search{Bc}Service implements Search{Bc}UseCase {

    private final {Bc}QueryFactory queryFactory;
    private final {Bc}ReadManager {bc}ReadManager;
    private final {Bc}Assembler assembler;

    public Search{Bc}Service(
        {Bc}QueryFactory queryFactory,
        {Bc}ReadManager {bc}ReadManager,
        {Bc}Assembler assembler
    ) {
        this.queryFactory = queryFactory;
        this.{bc}ReadManager = {bc}ReadManager;
        this.assembler = assembler;
    }

    @Override
    public {Bc}ListResponse execute(Search{Bc}Query query) {
        // 1. Query → Criteria (Factory)
        {Bc}SearchCriteria criteria = queryFactory.createSearchCriteria(query);

        // 2. 조회 (ReadManager 직접 - 단일)
        List<{Bc}> {bc}s = {bc}ReadManager.findBy(criteria);

        // 3. Response 변환 (Assembler)
        return assembler.toListResponse({bc}s);
    }
}
```

---

## ⚠️ Zero-Tolerance Rules

| 규칙 | 설명 | 위반 결과 |
|------|------|----------|
| **UseCase Interface 필수** | Port-In은 Interface로 선언 | 빌드 실패 |
| **execute() 메서드 필수** | 모든 UseCase는 execute() 메서드 | 빌드 실패 |
| **DTO 패키지 분리** | Command/Query/Response 별도 패키지 | 빌드 실패 |
| **@Transactional 금지** | Service에서 직접 사용 금지, Facade/Manager 책임 | 빌드 실패 |
| **Port 직접 호출 금지** | Manager/Facade 통해서만 접근 | 빌드 실패 |
| **Domain 반환 금지** | Response DTO로만 반환 | 빌드 실패 |
| **Lombok 금지** | Plain Java 사용 | 빌드 실패 |
| **비즈니스 로직 금지** | Domain 책임 | 코드 리뷰 |
| **객체 직접 생성 금지** | Factory 책임 | 코드 리뷰 |

---

## 🔗 참조 문서 (Convention References)

| 문서 | 경로 |
|------|------|
| Application Guide | `docs/coding_convention/03-application-layer/application-guide.md` |
| Port-In Command | `docs/coding_convention/03-application-layer/port/in/command/port-in-command-guide.md` |
| Port-In Query | `docs/coding_convention/03-application-layer/port/in/query/port-in-query-guide.md` |
| UseCase ArchUnit | `docs/coding_convention/03-application-layer/port/in/usecase-archunit.md` |
| Command Service | `docs/coding_convention/03-application-layer/service/command/command-service-guide.md` |
| Query Service | `docs/coding_convention/03-application-layer/service/query/query-service-guide.md` |
| Command DTO | `docs/coding_convention/03-application-layer/dto/command/command-dto-guide.md` |
| Query DTO | `docs/coding_convention/03-application-layer/dto/query/query-dto-guide.md` |
| Response DTO | `docs/coding_convention/03-application-layer/dto/response/response-dto-guide.md` |
| DTO Record ArchUnit | `docs/coding_convention/03-application-layer/dto/dto-record-archunit.md` |
| Assembler Guide | `docs/coding_convention/03-application-layer/assembler/assembler-guide.md` |

---

## 📦 패키지 구조

```
application/{bc}/
│
├─ port/
│  ├─ in/
│  │   ├─ command/
│  │   │   ├─ Place{Bc}UseCase.java
│  │   │   ├─ Update{Bc}UseCase.java
│  │   │   └─ Delete{Bc}UseCase.java
│  │   └─ query/
│  │       ├─ Get{Bc}UseCase.java
│  │       └─ Search{Bc}UseCase.java
│  └─ out/
│      ├─ command/
│      │   └─ {Bc}PersistencePort.java
│      └─ query/
│          └─ {Bc}QueryPort.java
│
├─ service/
│  ├─ command/
│  │   ├─ Place{Bc}Service.java
│  │   ├─ Update{Bc}Service.java
│  │   └─ Delete{Bc}Service.java
│  └─ query/
│      ├─ Get{Bc}Service.java
│      └─ Search{Bc}Service.java
│
├─ dto/
│  ├─ command/
│  │   ├─ Place{Bc}Command.java
│  │   └─ Update{Bc}Command.java
│  ├─ query/
│  │   ├─ Get{Bc}Query.java
│  │   └─ Search{Bc}Query.java
│  ├─ response/
│  │   ├─ {Bc}Response.java
│  │   └─ {Bc}DetailResponse.java
│  └─ bundle/
│      ├─ {Bc}PersistBundle.java
│      └─ {Bc}QueryBundle.java
│
├─ factory/
│  ├─ command/
│  │   └─ {Bc}CommandFactory.java
│  └─ query/
│      └─ {Bc}QueryFactory.java
│
├─ facade/
│  ├─ command/
│  │   └─ {Bc}Facade.java
│  └─ query/
│      └─ {Bc}QueryFacade.java
│
├─ manager/
│  ├─ command/
│  │   └─ {Bc}TransactionManager.java
│  └─ query/
│      └─ {Bc}ReadManager.java
│
├─ assembler/
│  └─ {Bc}Assembler.java
│
└─ listener/
   └─ {Bc}EventListener.java
```

---

## 🧪 테스트 체크리스트

### UseCase Interface 테스트

- [ ] `*UseCase` 접미사 검증
- [ ] Interface 타입 검증
- [ ] `execute()` 메서드 존재 검증
- [ ] `@Transactional` 어노테이션 금지 검증
- [ ] Domain 반환 타입 금지 검증

### Service 구현체 테스트

- [ ] `@Service` 어노테이션 검증
- [ ] Port-In 구현 검증
- [ ] 올바른 패키지 위치 검증
- [ ] Lombok 미사용 검증
- [ ] Port 직접 호출 금지 검증

### DTO 테스트

- [ ] Record 타입 검증
- [ ] `jakarta.validation` 의존성 금지 검증
- [ ] 불변성 검증 (List.copyOf 사용)

---

## 컴포넌트 사용 기준

### Command 흐름

| 조건 | 사용 |
|------|------|
| Manager 2개 이상 조합 | Facade 사용 |
| Manager 1개 | Manager 직접 호출 |
| Command → Domain 변환 필요 | CommandFactory 사용 |
| Bundle 생성 필요 | CommandFactory.createBundle() |

### Query 흐름

| 조건 | 사용 |
|------|------|
| ReadManager 2개 이상 조합 | QueryFacade 사용 |
| ReadManager 1개 | ReadManager 직접 호출 |
| Query → Criteria 변환 필요 | QueryFactory 사용 |
| 단순 ID 조회 | Factory 불필요 |

---

## Pagination 패턴

| 패턴 | UseCase 반환 타입 | 사용 시기 |
|------|------------------|----------|
| PageResponse | `PageResponse<T>` | 관리자 페이지 (총 개수 필요) |
| SliceResponse | `SliceResponse<T>` | 무한 스크롤 (COUNT 생략) |
| CursorResponse | `CursorResponse<T>` | 실시간/대용량 (중복 방지) |
