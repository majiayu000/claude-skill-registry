---
name: rest-api-expert
description: RESTful API 설계, Request/Response DTO, @Valid 검증. MockMvc 금지, TestRestTemplate 필수. /kb-rest-api 명령 시 자동 활성화.
triggers: [/kb-rest-api, /go, /red, /green, /refactor, /tidy, controller, api, endpoint, dto, mapper]
---

# REST API Layer 전문가

## 핵심 원칙 (Zero-Tolerance)

### ✅ Mandatory
1. **TestRestTemplate 필수** - 통합 테스트
2. **Request/Response DTO 분리** - API 전용 DTO
3. **@Valid 필수** - Request DTO 검증
4. **GlobalExceptionHandler 필수** - 통합 에러 처리
5. **@RestController** - REST API 명시
6. **ResponseEntity 반환** - HTTP 상태 코드 명시
7. **Mapper 분리** - API DTO ↔ UseCase Command/Response

### ❌ Prohibited
1. **Domain/Entity 직접 반환 금지** - DTO 변환 필수
2. **Business 로직 금지** - UseCase 위임
3. **Transaction 금지** - Controller는 트랜잭션 경계 밖
4. **MockMvc 금지** - TestRestTemplate 사용
5. **@RequestParam 남용 금지** - Request DTO 사용
6. **Raw String 금지** - ErrorCode Enum 사용
7. **Validation 로직 금지** - @Valid + Bean Validation

## 예시

### ✅ CORRECT: Controller 패턴
```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final PlaceOrderUseCase placeOrderUseCase;

    @PostMapping
    public ResponseEntity<OrderApiResponse> create(
        @Valid @RequestBody PlaceOrderApiRequest request
    ) {
        PlaceOrderCommand command = OrderApiMapper.toCommand(request);
        OrderResponse response = placeOrderUseCase.execute(command);
        OrderApiResponse apiResponse = OrderApiMapper.toApiResponse(response);

        return ResponseEntity.created(URI.create("/api/orders/" + apiResponse.orderId()))
            .body(apiResponse);
    }
}
```

## 참조

- **전체 가이드**: [REST API Guide](../../../docs/coding_convention/01-adapter-in-layer/rest-api/rest-api-guide.md)
- **상세 규칙 + 템플릿**: [REFERENCE.md](./REFERENCE.md)

## 자동 활성화

`/kb-rest-api /go|red|green|refactor|tidy` 실행 시 자동 활성화.
