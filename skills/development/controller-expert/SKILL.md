---
name: controller-expert
version: 3.0.0
description: |
  REST Controller 전문가. Thin Controller 패턴, CQRS Command/Query Controller 분리,
  ResponseEntity<ApiResponse<T>> 래핑, @Valid 검증 필수. DELETE 금지(PATCH 사용).
  TestRestTemplate 필수 (MockMvc 금지). UseCase 의존. Mapper DI.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, rest-api, controller, dto, validation, restful, cqrs]
---

# Controller Expert (REST API 전문가)

## 목적 (Purpose)

REST API Layer에서 **HTTP 요청/응답을 처리**하는 컴포넌트를 규칙에 맞게 생성합니다.
Thin Controller 패턴과 CQRS 분리 원칙을 준수합니다.

## 활성화 조건

- `/impl rest-api {feature}` 명령 실행 시
- `/plan` 실행 후 REST API Layer 작업 시
- controller, rest, dto, request, response, api 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 |
|----------|-------------|------|
| CommandController | `{Bc}CommandController.java` | `adapter-in/rest-api/{bc}/controller/` |
| QueryController | `{Bc}QueryController.java` | `adapter-in/rest-api/{bc}/controller/` |
| Command DTO | `{Action}{Bc}ApiRequest.java` | `adapter-in/rest-api/{bc}/dto/command/` |
| Query DTO | `{Bc}SearchApiRequest.java` | `adapter-in/rest-api/{bc}/dto/query/` |
| Response DTO | `{Bc}ApiResponse.java` | `adapter-in/rest-api/{bc}/dto/response/` |
| ApiMapper | `{Bc}ApiMapper.java` | `adapter-in/rest-api/{bc}/mapper/` |
| ErrorMapper | `{Bc}ApiErrorMapper.java` | `adapter-in/rest-api/{bc}/error/` |

## 완료 기준 (Acceptance Criteria)

- [ ] CQRS 분리: CommandController (POST, PATCH) / QueryController (GET)
- [ ] `ResponseEntity<ApiResponse<T>>` 래핑 (두 가지 모두 필수)
- [ ] `@Valid` 검증: 모든 Request DTO에 필수
- [ ] UseCase 직접 의존 (Service 금지)
- [ ] Mapper DI: `@Component` Bean (Static 금지)
- [ ] DELETE 금지: 소프트 삭제는 `PATCH /{id}/delete`
- [ ] Lombok 금지
- [ ] DTO는 Java 21 Record
- [ ] ArchUnit 테스트 통과

---

## Thin Controller 패턴

```
HTTP Request
    ↓
@Valid 검증 (Request DTO)
    ↓
Mapper 변환 (API DTO → UseCase DTO)
    ↓
UseCase 실행
    ↓
Mapper 변환 (UseCase DTO → API DTO)
    ↓
ResponseEntity<ApiResponse<T>> 래핑
    ↓
HTTP Response
```

**핵심**: Controller는 **HTTP 요청/응답 처리만**. 비즈니스 로직 절대 금지.

---

## 코드 템플릿

### 1. CommandController (POST, PATCH)

```java
package com.ryuqq.adapter.in.rest.order.controller;

import com.ryuqq.adapter.in.rest.common.dto.ApiResponse;
import com.ryuqq.adapter.in.rest.order.dto.command.CreateOrderApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.command.CancelOrderApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.response.OrderApiResponse;
import com.ryuqq.adapter.in.rest.order.mapper.OrderApiMapper;
import com.ryuqq.application.order.port.in.CreateOrderUseCase;
import com.ryuqq.application.order.port.in.CancelOrderUseCase;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * Order Command Controller
 *
 * <p>Order 도메인의 상태 변경 API를 제공합니다.</p>
 *
 * <p>제공하는 API:</p>
 * <ul>
 *   <li>POST /api/v1/orders - 주문 생성</li>
 *   <li>PATCH /api/v1/orders/{id}/cancel - 주문 취소</li>
 * </ul>
 *
 * @author development-team
 * @since 1.0.0
 */
@RestController
@RequestMapping("${api.endpoints.base-v1}/orders")
@Validated
public class OrderCommandController {

    private final CreateOrderUseCase createOrderUseCase;
    private final CancelOrderUseCase cancelOrderUseCase;
    private final OrderApiMapper orderApiMapper;

    public OrderCommandController(
            CreateOrderUseCase createOrderUseCase,
            CancelOrderUseCase cancelOrderUseCase,
            OrderApiMapper orderApiMapper) {
        this.createOrderUseCase = createOrderUseCase;
        this.cancelOrderUseCase = cancelOrderUseCase;
        this.orderApiMapper = orderApiMapper;
    }

    /**
     * 주문 생성
     *
     * @param request 주문 생성 요청 DTO
     * @return 주문 생성 결과 (201 Created)
     */
    @PostMapping
    public ResponseEntity<ApiResponse<OrderApiResponse>> createOrder(
            @RequestBody @Valid CreateOrderApiRequest request) {

        // 1. API Request → UseCase Command 변환 (Mapper)
        var command = orderApiMapper.toCommand(request);

        // 2. UseCase 실행 (비즈니스 로직)
        var useCaseResponse = createOrderUseCase.execute(command);

        // 3. UseCase Response → API Response 변환 (Mapper)
        var apiResponse = orderApiMapper.toApiResponse(useCaseResponse);

        // 4. ResponseEntity<ApiResponse<T>> 래핑
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(ApiResponse.ofSuccess(apiResponse));
    }

    /**
     * 주문 취소 (소프트 삭제 패턴)
     *
     * @param id 주문 ID
     * @param request 취소 요청 DTO
     * @return 취소 결과 (200 OK)
     */
    @PatchMapping("/{id}/cancel")
    public ResponseEntity<ApiResponse<Void>> cancelOrder(
            @PathVariable Long id,
            @RequestBody @Valid CancelOrderApiRequest request) {

        var command = orderApiMapper.toCancelCommand(id, request);
        cancelOrderUseCase.execute(command);

        return ResponseEntity.ok(ApiResponse.ofSuccess());
    }
}
```

**핵심 규칙**:
- POST: 201 Created 반환
- PATCH: 200 OK 반환
- DELETE 금지 → `PATCH /{id}/delete` 또는 `PATCH /{id}/cancel`
- `@Validated` 클래스 레벨 (PathVariable/RequestParam 검증용)
- `@Valid` 파라미터 레벨 (RequestBody 검증용)

### 2. QueryController (GET)

```java
package com.ryuqq.adapter.in.rest.order.controller;

import com.ryuqq.adapter.in.rest.common.dto.ApiResponse;
import com.ryuqq.adapter.in.rest.common.dto.SliceApiResponse;
import com.ryuqq.adapter.in.rest.order.dto.query.OrderSearchApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.response.OrderApiResponse;
import com.ryuqq.adapter.in.rest.order.dto.response.OrderDetailApiResponse;
import com.ryuqq.adapter.in.rest.order.mapper.OrderApiMapper;
import com.ryuqq.application.order.port.in.GetOrderQueryService;
import com.ryuqq.application.order.port.in.SearchOrderQueryService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Positive;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * Order Query Controller
 *
 * <p>Order 도메인의 조회 API를 제공합니다.</p>
 *
 * <p>제공하는 API:</p>
 * <ul>
 *   <li>GET /api/v1/orders/{id} - 주문 단건 조회</li>
 *   <li>GET /api/v1/orders - 주문 검색</li>
 * </ul>
 *
 * @author development-team
 * @since 1.0.0
 */
@RestController
@RequestMapping("${api.endpoints.base-v1}/orders")
@Validated
public class OrderQueryController {

    private final GetOrderQueryService getOrderQueryService;
    private final SearchOrderQueryService searchOrderQueryService;
    private final OrderApiMapper orderApiMapper;

    public OrderQueryController(
            GetOrderQueryService getOrderQueryService,
            SearchOrderQueryService searchOrderQueryService,
            OrderApiMapper orderApiMapper) {
        this.getOrderQueryService = getOrderQueryService;
        this.searchOrderQueryService = searchOrderQueryService;
        this.orderApiMapper = orderApiMapper;
    }

    /**
     * 주문 단건 조회
     *
     * @param id 주문 ID (양수)
     * @return 주문 상세 정보 (200 OK)
     */
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<OrderDetailApiResponse>> getOrder(
            @PathVariable @Positive Long id) {

        // 1. ID → UseCase Query 변환 (Mapper)
        var query = orderApiMapper.toGetQuery(id);

        // 2. UseCase 실행 (조회 로직)
        var useCaseResponse = getOrderQueryService.getById(query);

        // 3. UseCase Response → API Response 변환 (Mapper)
        var apiResponse = orderApiMapper.toDetailApiResponse(useCaseResponse);

        // 4. ResponseEntity<ApiResponse<T>> 래핑
        return ResponseEntity.ok(ApiResponse.ofSuccess(apiResponse));
    }

    /**
     * 주문 검색 (Cursor 기반)
     *
     * @param request 검색 조건
     * @return 주문 검색 결과 (200 OK)
     */
    @GetMapping
    public ResponseEntity<ApiResponse<SliceApiResponse<OrderApiResponse>>> searchOrders(
            @Valid @ModelAttribute OrderSearchApiRequest request) {

        var query = orderApiMapper.toSearchQuery(request);
        var useCaseResponse = searchOrderQueryService.search(query);
        var apiResponse = SliceApiResponse.from(
            useCaseResponse,
            orderApiMapper::toApiResponse
        );

        return ResponseEntity.ok(ApiResponse.ofSuccess(apiResponse));
    }
}
```

**핵심 규칙**:
- GET: 200 OK 반환
- `@ModelAttribute`로 Query Parameter 바인딩
- `@Positive`로 PathVariable 검증
- SliceApiResponse (Cursor) vs PageApiResponse (Offset) 선택

### 3. Command DTO (Request)

```java
package com.ryuqq.adapter.in.rest.order.dto.command;

import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.util.List;

/**
 * 주문 생성 요청
 *
 * @param customerId 고객 ID
 * @param items 주문 항목 목록
 * @param shippingAddress 배송 주소
 * @author development-team
 * @since 1.0.0
 */
public record CreateOrderApiRequest(
    @NotNull(message = "고객 ID는 필수입니다")
    Long customerId,

    @NotEmpty(message = "주문 항목은 필수입니다")
    @Valid
    List<OrderItemRequest> items,

    @NotNull(message = "배송 주소는 필수입니다")
    @Valid
    AddressRequest shippingAddress
) {
    // Compact Constructor (불변 리스트, 추가 검증)
    public CreateOrderApiRequest {
        if (customerId != null && customerId <= 0) {
            throw new IllegalArgumentException("유효하지 않은 고객 ID: " + customerId);
        }
        items = items == null ? List.of() : List.copyOf(items);
    }

    /**
     * 주문 항목 요청
     */
    public record OrderItemRequest(
        @NotNull(message = "상품 ID는 필수입니다")
        Long productId,

        @NotNull(message = "수량은 필수입니다")
        @Min(value = 1, message = "수량은 1 이상이어야 합니다")
        Integer quantity,

        @NotNull(message = "가격은 필수입니다")
        @Min(value = 0, message = "가격은 0 이상이어야 합니다")
        Long price
    ) {}

    /**
     * 배송 주소 요청
     */
    public record AddressRequest(
        @NotBlank(message = "우편번호는 필수입니다")
        String zipCode,

        @NotBlank(message = "주소는 필수입니다")
        String address,

        String addressDetail
    ) {}
}
```

**Command DTO 네이밍 규칙**:

| HTTP 메서드 | 접두사 | 예시 |
|-------------|--------|------|
| POST | Create, Register, Place | `CreateOrderApiRequest` |
| PATCH | Update, Modify, Cancel | `CancelOrderApiRequest` |

### 4. Query DTO (Request)

```java
package com.ryuqq.adapter.in.rest.order.dto.query;

import jakarta.validation.constraints.*;
import java.time.LocalDate;

/**
 * 주문 검색 요청
 *
 * @param customerId 고객 ID (Optional)
 * @param status 주문 상태 (Optional)
 * @param startDate 시작 날짜 (Optional)
 * @param endDate 종료 날짜 (Optional)
 * @param cursor 다음 페이지 커서 (Optional)
 * @param size 페이지 크기
 * @author development-team
 * @since 1.0.0
 */
public record OrderSearchApiRequest(
    // Optional 필드 (null 허용)
    Long customerId,

    @Pattern(regexp = "PLACED|CONFIRMED|SHIPPED|DELIVERED|CANCELLED",
             message = "유효하지 않은 상태입니다")
    String status,

    LocalDate startDate,
    LocalDate endDate,

    // Cursor 기반 페이징
    String cursor,

    // 페이징 필수
    @Min(value = 1, message = "페이지 크기는 1 이상")
    @Max(value = 100, message = "페이지 크기는 100 이하")
    Integer size
) {
    // Compact Constructor (기본값 설정)
    public OrderSearchApiRequest {
        size = size == null ? 20 : size;

        // 날짜 범위 검증
        if (startDate != null && endDate != null && startDate.isAfter(endDate)) {
            throw new IllegalArgumentException("시작 날짜는 종료 날짜보다 이전이어야 합니다");
        }
    }
}
```

**Query DTO 특징**:
- 대부분 필드 Optional (null 허용)
- 페이징 조건 필수 (무한 조회 방지)
- Compact Constructor로 기본값 설정

### 5. Response DTO

```java
package com.ryuqq.adapter.in.rest.order.dto.response;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 주문 응답
 *
 * @param orderId 주문 ID
 * @param customerId 고객 ID
 * @param status 주문 상태
 * @param totalAmount 총 금액
 * @param items 주문 항목 목록
 * @param createdAt 생성 일시
 * @author development-team
 * @since 1.0.0
 */
public record OrderApiResponse(
    Long orderId,
    Long customerId,
    String status,
    Long totalAmount,
    List<OrderItemResponse> items,
    LocalDateTime createdAt
) {
    // Compact Constructor (불변 컬렉션)
    public OrderApiResponse {
        items = items == null ? List.of() : List.copyOf(items);
    }

    /**
     * Application Layer Response → REST API Response
     */
    public static OrderApiResponse from(OrderResponse appResponse) {
        return new OrderApiResponse(
            appResponse.orderId(),
            appResponse.customerId(),
            appResponse.status(),
            appResponse.totalAmount(),
            appResponse.items().stream()
                .map(OrderItemResponse::from)
                .toList(),
            appResponse.createdAt()
        );
    }

    /**
     * 주문 항목 응답
     */
    public record OrderItemResponse(
        Long productId,
        String productName,
        Integer quantity,
        Long price
    ) {
        public static OrderItemResponse from(OrderItemDto dto) {
            return new OrderItemResponse(
                dto.productId(),
                dto.productName(),
                dto.quantity(),
                dto.price()
            );
        }
    }
}
```

**Response DTO 특징**:
- `from()` 정적 팩토리 메서드로 변환
- 불변 컬렉션 (List.copyOf)
- Nested Record로 복잡한 구조 표현

### 6. ApiMapper (@Component)

```java
package com.ryuqq.adapter.in.rest.order.mapper;

import com.ryuqq.adapter.in.rest.order.dto.command.CreateOrderApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.command.CancelOrderApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.query.OrderSearchApiRequest;
import com.ryuqq.adapter.in.rest.order.dto.response.OrderApiResponse;
import com.ryuqq.adapter.in.rest.order.dto.response.OrderDetailApiResponse;
import com.ryuqq.application.order.dto.command.CreateOrderCommand;
import com.ryuqq.application.order.dto.command.CancelOrderCommand;
import com.ryuqq.application.order.dto.query.GetOrderQuery;
import com.ryuqq.application.order.dto.query.SearchOrdersQuery;
import com.ryuqq.application.order.dto.response.OrderResponse;
import com.ryuqq.application.order.dto.response.OrderDetailResponse;
import org.springframework.stereotype.Component;
import java.util.List;

/**
 * OrderApiMapper - Order REST API ↔ Application Layer 변환
 *
 * <p>REST API Layer와 Application Layer 간의 DTO 변환을 담당합니다.</p>
 *
 * @author development-team
 * @since 1.0.0
 */
@Component
public class OrderApiMapper {

    /**
     * CreateOrderApiRequest → CreateOrderCommand 변환
     */
    public CreateOrderCommand toCommand(CreateOrderApiRequest request) {
        List<CreateOrderCommand.OrderItem> items = request.items().stream()
            .map(item -> CreateOrderCommand.OrderItem.of(
                item.productId(),
                item.quantity(),
                item.price()
            ))
            .toList();

        return CreateOrderCommand.of(
            request.customerId(),
            items,
            toAddressCommand(request.shippingAddress())
        );
    }

    /**
     * CancelOrderApiRequest → CancelOrderCommand 변환
     */
    public CancelOrderCommand toCancelCommand(Long id, CancelOrderApiRequest request) {
        return CancelOrderCommand.of(id, request.reason());
    }

    /**
     * ID → GetOrderQuery 변환
     */
    public GetOrderQuery toGetQuery(Long id) {
        return GetOrderQuery.of(id);
    }

    /**
     * OrderSearchApiRequest → SearchOrdersQuery 변환
     */
    public SearchOrdersQuery toSearchQuery(OrderSearchApiRequest request) {
        boolean isCursor = request.cursor() != null && !request.cursor().isBlank();

        if (isCursor) {
            return SearchOrdersQuery.ofCursor(
                request.customerId(),
                request.status(),
                request.startDate(),
                request.endDate(),
                request.cursor(),
                request.size()
            );
        } else {
            return SearchOrdersQuery.ofOffset(
                request.customerId(),
                request.status(),
                request.startDate(),
                request.endDate(),
                0,  // page default
                request.size()
            );
        }
    }

    /**
     * OrderResponse → OrderApiResponse 변환
     */
    public OrderApiResponse toApiResponse(OrderResponse appResponse) {
        return OrderApiResponse.from(appResponse);
    }

    /**
     * OrderDetailResponse → OrderDetailApiResponse 변환
     */
    public OrderDetailApiResponse toDetailApiResponse(OrderDetailResponse appResponse) {
        return OrderDetailApiResponse.from(appResponse);
    }

    // ========== Private Helper ==========

    private CreateOrderCommand.Address toAddressCommand(
            CreateOrderApiRequest.AddressRequest address) {
        return CreateOrderCommand.Address.of(
            address.zipCode(),
            address.address(),
            address.addressDetail()
        );
    }
}
```

**ApiMapper 규칙**:
- `@Component` Bean 등록 (Static 금지)
- 필드 매핑만 수행 (비즈니스 로직 금지)
- 기본값 설정/검증 금지 (Controller/Bean Validation 책임)

---

## HTTP 상태 코드 규칙

| 메서드 | HTTP 상태 | 용도 |
|--------|-----------|------|
| **POST** | 201 Created | 리소스 생성 성공 |
| **GET** | 200 OK | 조회 성공 |
| **PATCH** | 200 OK | 부분 수정 성공 |
| **PUT** | 200 OK | 전체 수정 성공 |
| **DELETE** | ❌ 지원 안 함 | 소프트 삭제는 PATCH로 |

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 설명 |
|------|------|
| `ResponseEntity<ApiResponse<T>>` | 두 가지 래핑 모두 필수 |
| `@Valid` | 모든 Request DTO에 필수 |
| `@Validated` | Controller 클래스 레벨 |
| UseCase 의존 | Service 직접 의존 금지 |
| Mapper DI | `@Component` Bean (Static 금지) |
| Record DTO | Java 21 Record 사용 |
| RESTful URI | 명사 복수형, 동사 금지 |

### ❌ PROHIBITED (금지)

| 항목 | 이유 |
|------|------|
| DELETE 메서드 | 소프트 삭제는 PATCH 사용 |
| 비즈니스 로직 | UseCase/Domain 책임 |
| `@Transactional` | UseCase 책임 |
| try-catch | GlobalExceptionHandler 위임 |
| Domain 직접 노출 | Response DTO 사용 |
| Lombok | Plain Java 사용 |
| Jackson 어노테이션 | `@JsonFormat`, `@JsonProperty` 금지 |
| MockMvc 테스트 | TestRestTemplate 사용 |

---

## 페이징 패턴

### Slice vs Page 선택

| 구분 | SliceApiResponse | PageApiResponse |
|------|------------------|-----------------|
| **사용 사례** | 무한 스크롤 (일반 사용자) | 페이지 번호 (관리자) |
| **성능** | 빠름 (COUNT 불필요) | 느림 (COUNT 필수) |
| **제공 정보** | hasNext, nextCursor | totalElements, totalPages |
| **적합한 UI** | 모바일, SNS 피드 | 관리자 테이블 |

```java
// Slice (일반 사용자)
@GetMapping
public ResponseEntity<ApiResponse<SliceApiResponse<OrderApiResponse>>> searchOrders(...) {
    // hasNext, nextCursor 반환
}

// Page (관리자)
@GetMapping("/admin")
public ResponseEntity<ApiResponse<PageApiResponse<OrderApiResponse>>> searchOrdersForAdmin(...) {
    // totalElements, totalPages 반환
}
```

---

## 에러 처리 (RFC 7807)

### GlobalExceptionHandler

- `@RestControllerAdvice`로 전역 예외 처리
- `application/problem+json` Content-Type
- `x-error-code` 응답 헤더 추가
- 로깅 레벨: 5xx → ERROR, 404 → DEBUG, 4xx → WARN

### ErrorMapper 패턴

```java
@Component
public class OrderApiErrorMapper implements ErrorMapper {

    @Override
    public boolean supports(DomainException ex) {
        return ex instanceof OrderException;
    }

    @Override
    public MappedError map(DomainException ex, Locale locale) {
        return switch (ex.code()) {
            case "ORDER_NOT_FOUND" -> new MappedError(
                HttpStatus.NOT_FOUND,
                "Not Found",
                "주문을 찾을 수 없습니다",
                URI.create("/errors/order/not-found")
            );
            // ...
        };
    }
}
```

---

## 패키지 구조

```
adapter-in/rest-api/
├── common/
│   ├── controller/
│   │   └── GlobalExceptionHandler.java
│   ├── dto/
│   │   ├── ApiResponse.java
│   │   ├── SliceApiResponse.java
│   │   └── PageApiResponse.java
│   ├── error/
│   │   └── ErrorMapperRegistry.java
│   └── mapper/
│       └── ErrorMapper.java
│
└── {bc}/
    ├── controller/
    │   ├── {Bc}CommandController.java
    │   └── {Bc}QueryController.java
    ├── dto/
    │   ├── command/
    │   │   └── {Action}{Bc}ApiRequest.java
    │   ├── query/
    │   │   └── {Bc}SearchApiRequest.java
    │   └── response/
    │       └── {Bc}ApiResponse.java
    ├── mapper/
    │   └── {Bc}ApiMapper.java
    └── error/
        └── {Bc}ApiErrorMapper.java
```

---

## 체크리스트 (Output Checklist)

### Controller
- [ ] `@RestController`, `@RequestMapping` 어노테이션
- [ ] `@Validated` 클래스 레벨
- [ ] UseCase, Mapper 생성자 주입 (Lombok 없음)
- [ ] `ResponseEntity<ApiResponse<T>>` 반환
- [ ] HTTP 상태 코드 올바르게 설정 (POST → 201)
- [ ] `@Valid` 모든 Request DTO에 적용
- [ ] DELETE 미사용 (PATCH로 대체)
- [ ] 비즈니스 로직 없음
- [ ] Javadoc 작성

### Command DTO
- [ ] `public record` 키워드
- [ ] `{Action}{Bc}ApiRequest` 네이밍
- [ ] Bean Validation 어노테이션
- [ ] Compact Constructor (불변 리스트, 추가 검증)
- [ ] Nested Record (복잡한 구조)

### Query DTO
- [ ] `public record` 키워드
- [ ] `{Bc}SearchApiRequest` 네이밍
- [ ] Optional 필드 (대부분 null 허용)
- [ ] 페이징 조건 필수 (size)
- [ ] 기본값 설정 (Compact Constructor)

### Response DTO
- [ ] `public record` 키워드
- [ ] `{Bc}ApiResponse` 네이밍
- [ ] `from()` 정적 팩토리 메서드
- [ ] 불변 컬렉션 (List.copyOf)

### ApiMapper
- [ ] `@Component` 어노테이션
- [ ] 생성자 주입 (필요 시)
- [ ] 필드 매핑만 수행
- [ ] 비즈니스 로직 없음
- [ ] Static 메서드 없음

---

## 테스트 체크리스트

### Controller 통합 테스트
- [ ] `@SpringBootTest(webEnvironment = RANDOM_PORT)`
- [ ] `TestRestTemplate` 사용 (MockMvc 금지)
- [ ] `@Tag("integration")`, `@Tag("adapter-rest")`
- [ ] 성공/실패 시나리오 테스트
- [ ] Validation 실패 테스트

### REST Docs 테스트
- [ ] `RestDocsTestSupport` 상속
- [ ] `document()` 메서드로 Snippet 생성
- [ ] `requestFields()`, `responseFields()` 문서화
- [ ] `pathParameters()`, `queryParameters()` 문서화

---

## 참조 문서

- **Controller Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/controller/controller-guide.md`
- **Command DTO Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/dto/command/command-dto-guide.md`
- **Query DTO Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/dto/query/query-dto-guide.md`
- **Response DTO Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/dto/response/response-dto-guide.md`
- **Mapper Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/mapper/mapper-guide.md`
- **Error Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/error/error-guide.md`
- **REST Docs Guide**: `docs/coding_convention/01-adapter-in-layer/rest-api/controller/controller-test-restdocs-guide.md`
