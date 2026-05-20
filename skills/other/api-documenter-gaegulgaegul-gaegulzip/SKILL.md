---
name: api-documenter
description: |
  OpenAPI 3.0 문서를 자동 생성/업데이트합니다.
  handlers.ts, validators.ts, schema.ts를 분석하여 API 명세를 작성합니다.
  "API 문서 만들어줘", "OpenAPI 문서 생성해줘" 요청 시 사용합니다.
---

# API Documenter Skill

OpenAPI 3.0 명세를 자동 생성하는 스킬입니다.

## 사용 방법

```bash
# 스킬 실행
/api-documenter [feature-name]

# 예시
/api-documenter users
```

## 기능

1. **handlers.ts 분석**: API 엔드포인트, JSDoc 주석에서 정보 추출
2. **index.ts 분석**: Router 경로, HTTP 메서드, 미들웨어 추출
3. **validators.ts 분석**: Zod 스키마에서 request/response 타입 추출
4. **schema.ts 분석**: Drizzle ORM 테이블에서 데이터 타입 정의 추출
5. **OpenAPI 3.0 업데이트**: `apps/server/docs/openapi.yaml` 갱신
6. **최신 표준 준수**: context7 MCP로 OpenAPI 베스트 프랙티스 확인
7. **과거 패턴 참조**: claude-mem MCP로 과거 API 문서 작성 패턴 참조

> **참고**: 기존 OpenAPI 문서(`apps/server/docs/openapi.yaml`)가 이미 존재하며,
> Swagger UI가 `/api-docs` 경로에서 서빙 중입니다. 새로 생성이 아닌 **업데이트** 방식으로 동작합니다.

## 워크플로우

### 0. 기존 OpenAPI 문서 읽기 (필수)
```typescript
Read("apps/server/docs/openapi.yaml")
// 기존 문서가 이미 존재하며 Swagger UI(/api-docs)에서 서빙 중
// 새 모듈 추가 시 기존 문서에 병합하는 방식으로 작업
```

### 1. handlers.ts 읽기
```typescript
Read("apps/server/src/modules/[feature]/handlers.ts")
// JSDoc 주석에서 API 정보 추출
// - summary: 첫 줄 설명
// - @param: 파라미터 정보
// - @returns: HTTP 상태 코드 + 응답 형태
// - @throws: 에러 타입 (NotFoundException, ValidationException 등)
```

### 2. index.ts (Router) 읽기
```typescript
Read("apps/server/src/modules/[feature]/index.ts")
// Router 정의에서 경로 추출
// - HTTP Method (GET, POST, PUT, PATCH, DELETE)
// - Path (/auth/oauth, /push/devices 등)
// - @route 태그에서 메서드+경로 추출
// - 미들웨어 확인 (authenticate → securitySchemes: BearerAuth)
```

### 3. validators.ts 읽기 (핵심)
```typescript
Read("apps/server/src/modules/[feature]/validators.ts")
// Zod 스키마에서 request/response 계약 추출
// - 필드명, 타입, 필수 여부
// - 문자열 제약 (min, max, email, url 등)
// - z.infer<> 로 추출된 TypeScript 타입
// ★ 이 파일이 실제 API 계약의 핵심 (handlers.ts JSDoc보다 정확)
```

### 4. schema.ts 읽기
```typescript
Read("apps/server/src/modules/[feature]/schema.ts")
// Drizzle 스키마에서 DB 타입 정의 추출
// - 테이블명, 필드명, 데이터 타입
// - JSDoc 주석에서 설명 추출
// - 인덱스, 유니크 제약 확인
```

### 5. context7 MCP로 베스트 프랙티스 확인
```typescript
"OpenAPI 3.0 specification best practices"
"OpenAPI schema definition patterns"
```

### 6. claude-mem MCP로 과거 패턴 참조
```typescript
"search for past API documentation patterns"
"search for past OpenAPI definitions"
```

### 7. OpenAPI 3.0 문서 업데이트
기존 `apps/server/docs/openapi.yaml`에 새 모듈의 paths/schemas를 병합

## 출력 파일

### apps/server/docs/openapi.yaml (기존 파일 업데이트)

```yaml
openapi: 3.0.0
info:
  title: gaegulzip-server API
  version: 1.0.0
  description: gaegulzip-server RESTful API Documentation

servers:
  - url: http://localhost:3001/api/v1
    description: Development server

paths:
  /users:
    get:
      summary: 모든 사용자 조회
      description: 시스템의 모든 사용자 목록을 반환합니다
      tags:
        - Users
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
        '500':
          description: 서버 에러
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    post:
      summary: 새 사용자 생성
      description: 이메일과 이름으로 새 사용자를 생성합니다
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  format: email
                  example: user@example.com
                name:
                  type: string
                  minLength: 1
                  maxLength: 100
                  example: John Doe
      responses:
        '201':
          description: 생성 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/User'
        '400':
          description: 유효성 에러
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          description: 서버 에러
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{id}:
    get:
      summary: 특정 사용자 조회
      description: ID로 사용자를 조회합니다
      tags:
        - Users
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: 사용자 ID
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/User'
        '404':
          description: 사용자 없음
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          description: 서버 에러
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    put:
      summary: 사용자 정보 수정
      description: ID로 사용자 정보를 수정합니다
      tags:
        - Users
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: 사용자 ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                name:
                  type: string
                  minLength: 1
                  maxLength: 100
      responses:
        '200':
          description: 수정 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/User'
        '400':
          description: 유효성 에러
        '404':
          description: 사용자 없음
        '500':
          description: 서버 에러

    delete:
      summary: 사용자 삭제
      description: ID로 사용자를 삭제합니다
      tags:
        - Users
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: 사용자 ID
      responses:
        '200':
          description: 삭제 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: User deleted successfully
        '404':
          description: 사용자 없음
        '500':
          description: 서버 에러

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          description: 사용자 ID
          example: 1
        email:
          type: string
          format: email
          description: 이메일 주소
          example: user@example.com
        name:
          type: string
          description: 사용자 이름
          example: John Doe
        createdAt:
          type: string
          format: date-time
          description: 생성 일시
          example: 2024-01-15T10:30:00Z
        updatedAt:
          type: string
          format: date-time
          description: 수정 일시
          example: 2024-01-15T10:30:00Z
      required:
        - id
        - email
        - name
        - createdAt
        - updatedAt

    Error:
      type: object
      properties:
        error:
          type: string
          description: 에러 메시지
          example: Invalid request
      required:
        - error

tags:
  - name: Users
    description: 사용자 관리 API
```

## 타입 매핑

### Drizzle → OpenAPI

| Drizzle Type | OpenAPI Type | Format |
|--------------|--------------|--------|
| `serial()` | `integer` | - |
| `integer()` | `integer` | - |
| `varchar()` | `string` | - |
| `text()` | `string` | - |
| `boolean()` | `boolean` | - |
| `timestamp()` | `string` | `date-time` |
| `uuid()` | `string` | `uuid` |
| `jsonb()` | `object` | - |

### Zod → OpenAPI

| Zod Type | OpenAPI Type | Format / 비고 |
|----------|--------------|---------------|
| `z.string()` | `string` | - |
| `z.string().email()` | `string` | `format: email` |
| `z.string().url()` | `string` | `format: uri` |
| `z.string().uuid()` | `string` | `format: uuid` |
| `z.string().min(n).max(m)` | `string` | `minLength: n, maxLength: m` |
| `z.number()` | `number` | - |
| `z.number().int()` | `integer` | - |
| `z.boolean()` | `boolean` | - |
| `z.array(z.T)` | `array` | `items: T` |
| `z.object({...})` | `object` | `properties: {...}` |
| `z.enum([...])` | `string` | `enum: [...]` |
| `z.optional()` | - | required에서 제외 |
| `z.nullable()` | - | `nullable: true` |

## JSDoc에서 정보 추출

### handlers.ts 예시
```typescript
/**
 * 사용자를 생성합니다
 * @param req - 요청 객체 (body: { email, name })
 * @param res - 응답 객체
 * @returns 201: 생성된 사용자, 400: 유효성 에러, 500: 서버 에러
 */
export const createUser: RequestHandler = async (req, res) => {
  // ...
};
```

**추출 정보**:
- **summary**: "사용자를 생성합니다"
- **request**: `{ email, name }`
- **responses**: `201`, `400`, `500`

## 사용 도구

- **Read**: 파일 읽기
- **Write**: OpenAPI 문서 작성
- **Glob**: handlers/schema 파일 찾기
- **Grep**: 특정 패턴 검색
- **context7 MCP**: OpenAPI 3.0 베스트 프랙티스
- **claude-mem MCP**: 과거 API 문서 패턴

## 체크리스트

작업 완료 전 확인:
- [ ] 기존 OpenAPI 문서 읽기 (`apps/server/docs/openapi.yaml`)
- [ ] handlers.ts 읽고 엔드포인트 추출
- [ ] index.ts 읽고 경로/메서드 추출
- [ ] validators.ts 읽고 request/response Zod 스키마 추출 (★ 핵심)
- [ ] schema.ts 읽고 타입 정의 추출
- [ ] context7 MCP로 OpenAPI 베스트 프랙티스 확인
- [ ] claude-mem MCP로 과거 패턴 참조
- [ ] 기존 OpenAPI 문서에 새 모듈 병합 (`apps/server/docs/openapi.yaml`)
- [ ] 모든 엔드포인트 포함
- [ ] 모든 스키마 정의 포함
- [ ] 예시 값 포함
- [ ] 한국어 설명 포함

## 다음 단계

OpenAPI 문서 업데이트 완료 후:
1. **사용자 검토**: 문서 정확성 확인
2. **Swagger UI 확인**: `/api-docs`에서 업데이트된 문서 시각적 확인 (이미 통합됨)
3. **최종 승인**: 전체 워크플로우 완료
