---
name: api-first-design
description: "**API FIRST DESIGN**: 'API 만들어', 'API 설계', '엔드포인트', 'REST', 'Swagger', 'OpenAPI', 'DTO', 'CRUD' 요청 시 자동 발동. *.controller.ts/*.dto.ts/routes/** 파일 작업 시 자동 적용. Contract-First, 표준 응답 포맷, 타입 자동 생성."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# API First Design Skill

> **Version**: 1.0.0
> **Purpose**: Swagger/OpenAPI 기반 Contract-First API 설계 및 일관된 응답 포맷 보장
> **Target**: NestJS + Next.js + Expo Monorepo

---

## Document Loading Strategy

**전체 문서를 로드하지 않습니다!** 상황에 따라 필요한 문서만 로드:

```yaml
Document_Loading_Strategy:
  Step_1_Detect_Framework:
    - 파일 확장자, import 문, 데코레이터로 프레임워크 감지
    - 불명확하면 package.json/requirements.txt 확인

  Step_2_Load_Required_Docs:
    Universal_Always_Load:
      - "core/contract-first.md"        # Contract-First 원칙 (항상)
      - "core/response-format.md"       # 표준 응답 포맷 (항상)
      - "core/error-codes.md"           # 에러 코드 체계 (항상)

    Framework_Specific_Load:
      NestJS: "frameworks/nestjs-swagger.md"     # NestJS Swagger 데코레이터
      Express: "frameworks/express-openapi.md"   # Express OpenAPI
      FastAPI: "frameworks/fastapi-openapi.md"   # Python FastAPI
      Django: "frameworks/django-rest.md"        # Django REST Framework
      SpringBoot: "frameworks/spring-openapi.md" # Spring OpenAPI
      Go: "frameworks/go-swagger.md"             # Go Swagger
      Rails: "frameworks/rails-openapi.md"       # Rails OpenAPI

    Type_Generation_Load:
      TypeScript: "patterns/type-generation.md"  # swagger-typescript-api
      Python: "patterns/python-types.md"         # pydantic
      Go: "patterns/go-types.md"                 # oapi-codegen

    Context_Specific_Load:
      Controller_Template: "templates/controller-template.md"
      OpenAPI_YAML: "templates/openapi-yaml.md"
      Checklist: "quick-reference/checklist.md"
      Anti_Patterns: "quick-reference/anti-patterns.md"
```

---

## Auto Trigger Conditions

```yaml
Auto_Trigger_Conditions:
  File_Patterns:
    - "*.controller.ts, *.controller.js"
    - "*.dto.ts, *.dto.js"
    - "**/routes/**, **/api/**"
    - "*.router.ts, *.router.js"
    - "openapi.yaml, swagger.yaml"

  Keywords_KO:
    - "API 만들어, API 작성, API 설계"
    - "엔드포인트, 라우트, 라우터"
    - "요청, 응답, 리퀘스트, 리스폰스"
    - "REST, RESTful, GraphQL"
    - "Swagger, OpenAPI, API 문서"
    - "DTO, 데이터 전송, 스키마"
    - "CRUD, 생성, 조회, 수정, 삭제"

  Keywords_EN:
    - "API, endpoint, route, router"
    - "request, response, REST, RESTful"
    - "Swagger, OpenAPI, API docs"
    - "DTO, schema, contract"
    - "CRUD, create, read, update, delete"

  Code_Patterns:
    - "@Controller, @Get, @Post, @Put, @Delete"
    - "@ApiOperation, @ApiResponse, @ApiTags"
    - "router.get, router.post, app.get"
    - "@app.get, @app.post"  # FastAPI
```

---

## Base Knowledge (다른 스킬 참조)

> **에러 처리 기본**: `clean-code-mastery/core/principles.md` 참조
> **인증/보안 패턴**: `security-shield` 참조 (JWT, 세션, CSRF)
> **입력 검증 기본**: `clean-code-mastery/core/security.md` 참조

---

## Core Concepts

### 1. Contract-First Workflow
```
OpenAPI Spec 정의 → 스펙 리뷰 → Type 자동 생성 → Backend/Frontend 구현
```

### 2. Standard Response Format
```typescript
// 성공
{ success: true, data: T, meta?: ApiMeta, timestamp: string }

// 에러
{ success: false, error: ApiError, timestamp: string }
```

### 3. Error Code System
```
패턴: DOMAIN_ACTION_REASON
예시: AUTH_TOKEN_EXPIRED, USER_NOT_FOUND, VALIDATION_FAILED
```

---

## Quick Reference

```yaml
필수_데코레이터:
  Controller:
    - "@ApiTags('Resources')"      # 복수형
    - "@ApiBearerAuth('access-token')"

  Method:
    - "@ApiOperation({ summary, description })"
    - "@ApiResponse({ status, description, type })"
    - "@ApiParam / @ApiQuery / @ApiBody"

  DTO:
    - "@ApiProperty({ description, example, format })"
    - "@ApiPropertyOptional()"

버전_전략:
  형식: "/api/v1/resources"
  지원: "현재 버전 + 이전 버전(12개월)"
```

---

## Module Files

| File | Description |
|------|-------------|
| `core/contract-first.md` | Contract-First 워크플로우, 디렉토리 구조 |
| `core/response-format.md` | 표준 응답 포맷, ApiResponse/ApiError |
| `core/error-codes.md` | 에러 코드 체계, HTTP 상태 매핑 |
| `patterns/swagger-decorators.md` | NestJS Swagger 데코레이터 가이드 |
| `patterns/type-generation.md` | 타입 자동 생성, React Query 통합 |
| `templates/controller-template.md` | 완전한 Controller 템플릿 |
| `templates/openapi-yaml.md` | OpenAPI YAML 템플릿 |
| `quick-reference/checklist.md` | API 개발/배포 체크리스트 |
| `quick-reference/anti-patterns.md` | API 안티패턴 목록 |

---

**Document Version**: 1.0.0
**Last Updated**: 2025-12-09

---

## Code Generation Tools (2025 권장)

### 🏆 1위: Orval (강력 추천)

```yaml
Orval:
  설명: "OpenAPI → TypeScript 클라이언트 + React Query 훅 자동 생성"
  주간_다운로드: "513K+"
  GitHub_Stars: "4,700+"
  
  핵심_장점:
    - React Query/TanStack Query 훅 자동 생성
    - MSW(Mock Service Worker) 핸들러 자동 생성
    - Zod 스키마 검증 통합 가능
    - TypeScript 특화, 타입 안전
    - 설정 간단 (orval.config.ts)
    
  지원_클라이언트:
    - Axios (기본)
    - Fetch API
    - React Query (TanStack Query)
    - SWR
    - Vue Query
    - Svelte Query
    - Angular HttpClient

설치_및_설정:
  install: |
    npm install orval -D
    
  config_file: |
    // orval.config.ts
    import { defineConfig } from 'orval';
    
    export default defineConfig({
      api: {
        input: './openapi.yaml',  // OpenAPI 스펙 경로
        output: {
          target: './src/api/generated.ts',
          client: 'react-query',  // React Query 훅 생성
          mode: 'tags-split',     // 태그별 파일 분리
          mock: true,             // MSW mock 자동 생성
        },
      },
    });
    
  실행: |
    npx orval
    # 또는 package.json scripts에 추가
    "scripts": {
      "api:generate": "orval"
    }

생성_결과_예시:
  input_openapi: |
    paths:
      /users/{id}:
        get:
          operationId: getUser
          parameters:
            - name: id
              in: path
          responses:
            200:
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/User'
                    
  output_react_query: |
    // 자동 생성된 코드
    export const useGetUser = (id: string) => {
      return useQuery({
        queryKey: ['getUser', id],
        queryFn: () => axios.get<User>(`/users/${id}`),
      });
    };
    
  output_msw_mock: |
    // 자동 생성된 MSW 핸들러
    export const getGetUserMock = () => 
      http.get('/users/:id', () => {
        return HttpResponse.json(getUserResponseMock());
      });
```

### 2위: openapi-typescript

```yaml
openapi-typescript:
  설명: "OpenAPI → TypeScript 타입만 생성 (가벼움)"
  주간_다운로드: "1.7M+"
  
  적합한_경우:
    - 타입만 필요하고 클라이언트는 직접 작성할 때
    - 번들 크기 최소화가 중요할 때
    
  사용: |
    npx openapi-typescript ./openapi.yaml -o ./src/api/types.ts
```

### ❌ 피해야 할 도구

```yaml
Legacy_Tools:
  swagger-codegen:
    문제: "레거시, 업데이트 느림, 현대 프레임워크 미지원"
    대안: "Orval 사용"
    
  OpenAPI_Generator_CLI:
    문제: "설정 복잡, Java 의존성, 느림"
    대안: "Orval 또는 openapi-typescript"
    
  swagger-typescript-api:
    문제: "React Query 지원 약함, mock 생성 없음"
    대안: "Orval"
```

### Contract-First + Orval 워크플로우

```yaml
Recommended_Workflow:
  1_API_설계:
    - OpenAPI YAML/JSON 작성
    - API 스펙 리뷰 (팀)
    
  2_코드_생성:
    - "npx orval" 실행
    - TypeScript 타입 생성
    - React Query 훅 생성
    - MSW mock 생성
    
  3_개발:
    - 프론트엔드: 생성된 훅 사용
    - 백엔드: 스펙에 맞춰 구현
    - 테스트: MSW mock으로 독립 테스트
    
  4_API_변경_시:
    - OpenAPI 스펙 수정
    - "npx orval" 재실행
    - TypeScript 컴파일 에러로 변경점 파악
```

### package.json 권장 스크립트

```json
{
  "scripts": {
    "api:generate": "orval",
    "api:watch": "orval --watch",
    "api:validate": "swagger-cli validate ./openapi.yaml"
  }
}
```

---

**Updated**: 2025-12-10
**Added**: Orval 코드 생성 도구 권장 (우수사례 피드백)
