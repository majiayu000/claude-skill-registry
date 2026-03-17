---
name: api-contract-design
description: Design APIs using schema-first approach with OpenAPI/Swagger. Use when creating new APIs, documenting existing ones, or when frontend/backend teams need to work in parallel. Covers OpenAPI spec, validation, and code generation.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# API Contract Design

OpenAPI(Swagger) 기반 스키마 우선 API 설계 스킬입니다.

## Core Principle

> **"코드보다 계약(Contract)이 먼저다."**
> **"프론트엔드와 백엔드가 동시에 개발할 수 있게 API를 먼저 정의한다."**

## Schema-First vs Code-First

| 접근법 | 장점 | 단점 |
|--------|------|------|
| **Schema-First** (권장) | 병렬 개발 가능, 명확한 계약 | 초기 설계 시간 필요 |
| Code-First | 빠른 시작 | 문서와 코드 불일치 위험 |

## OpenAPI 기본 구조

### `openapi.yaml`

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: API for My Application

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/api
    description: Development

paths:
  /users:
    get:
      summary: Get all users
      operationId: getUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a new user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUserById
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - createdAt
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        avatarUrl:
          type: string
          format: uri
          nullable: true
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8

    UserListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
        - totalPages
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

## 폴더 구조

```
api/
├── openapi.yaml          # 메인 스펙
├── paths/                # 엔드포인트별 분리
│   ├── users.yaml
│   ├── posts.yaml
│   └── auth.yaml
├── schemas/              # 스키마 분리
│   ├── user.yaml
│   ├── post.yaml
│   └── common.yaml
└── generated/            # 자동 생성 코드
    ├── types.ts
    └── client.ts
```

### 분리된 스펙 (paths/users.yaml)

```yaml
# api/paths/users.yaml
/users:
  get:
    $ref: '../operations/users/getUsers.yaml'
  post:
    $ref: '../operations/users/createUser.yaml'
```

### 메인 스펙에서 참조

```yaml
# api/openapi.yaml
paths:
  /users:
    $ref: './paths/users.yaml#/~1users'
```

## TypeScript 타입 생성

### openapi-typescript

```bash
npm install -D openapi-typescript
```

```bash
# 타입 생성
npx openapi-typescript ./api/openapi.yaml -o ./src/types/api.ts
```

### 생성된 타입 사용

```typescript
import type { paths, components } from './types/api';

type User = components['schemas']['User'];
type CreateUserRequest = components['schemas']['CreateUserRequest'];

// API 응답 타입
type GetUsersResponse = paths['/users']['get']['responses']['200']['content']['application/json'];
```

## API 클라이언트 생성

### openapi-fetch (권장)

```bash
npm install openapi-fetch
```

```typescript
// lib/api-client.ts
import createClient from 'openapi-fetch';
import type { paths } from './types/api';

export const api = createClient<paths>({
  baseUrl: process.env.NEXT_PUBLIC_API_URL,
});

// 사용
const { data, error } = await api.GET('/users', {
  params: {
    query: { page: 1, limit: 20 },
  },
});

const { data: user } = await api.POST('/users', {
  body: {
    email: 'user@example.com',
    name: 'John',
    password: 'password123',
  },
});
```

### Orval (코드 생성)

```bash
npm install -D orval
```

```typescript
// orval.config.ts
export default {
  api: {
    input: './api/openapi.yaml',
    output: {
      mode: 'tags-split',
      target: './src/api',
      schemas: './src/api/schemas',
      client: 'react-query',
    },
  },
};
```

## 요청 검증

### Zod + OpenAPI

```typescript
// 스키마에서 Zod 스키마 생성
import { z } from 'zod';

// OpenAPI 스펙 기반 Zod 스키마
export const CreateUserRequestSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  password: z.string().min(8),
});

// API 라우트에서 검증
export async function POST(request: Request) {
  const body = await request.json();

  const result = CreateUserRequestSchema.safeParse(body);
  if (!result.success) {
    return Response.json(
      { code: 'VALIDATION_ERROR', message: result.error.message },
      { status: 400 }
    );
  }

  // result.data는 타입 안전
  const user = await createUser(result.data);
  return Response.json(user, { status: 201 });
}
```

## API 문서 UI

### Swagger UI

```bash
npm install swagger-ui-react
```

```tsx
// app/api-docs/page.tsx
'use client';

import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

export default function ApiDocs() {
  return <SwaggerUI url="/api/openapi.yaml" />;
}
```

### Scalar (모던 대안)

```bash
npm install @scalar/nextjs-api-reference
```

```tsx
// app/api-docs/page.tsx
import { ApiReference } from '@scalar/nextjs-api-reference';

export default function ApiDocs() {
  return (
    <ApiReference
      configuration={{
        spec: {
          url: '/api/openapi.yaml',
        },
      }}
    />
  );
}
```

## 버전 관리

### URL 버전 관리

```yaml
servers:
  - url: https://api.example.com/v1
  - url: https://api.example.com/v2
```

### 헤더 버전 관리

```yaml
parameters:
  - name: API-Version
    in: header
    schema:
      type: string
      enum: ['2024-01-01', '2024-06-01']
```

## Workflow

### Schema-First 개발 흐름

```
1. API 스펙 작성 (openapi.yaml)
   ↓
2. 팀 리뷰 (PR)
   ↓
3. 타입 생성 (openapi-typescript)
   ↓
4. 병렬 개발
   - Frontend: Mock 서버로 개발
   - Backend: 스펙 기반 구현
   ↓
5. 통합 테스트
```

### Mock 서버

```bash
# Prism (Stoplight)
npm install -D @stoplight/prism-cli

# Mock 서버 실행
npx prism mock ./api/openapi.yaml
```

## Checklist

### 스펙 작성

- [ ] 모든 엔드포인트 정의
- [ ] Request/Response 스키마 정의
- [ ] 에러 응답 정의
- [ ] 인증 방식 정의
- [ ] 예제 데이터 포함

### 타입 안전성

- [ ] TypeScript 타입 생성
- [ ] 요청 검증 (Zod)
- [ ] 응답 타입 체크

### 문서화

- [ ] API 문서 UI 제공
- [ ] 변경 이력 관리
- [ ] 버전 관리 전략

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [openapi-typescript](https://github.com/drwpow/openapi-typescript)
- [openapi-fetch](https://github.com/drwpow/openapi-typescript/tree/main/packages/openapi-fetch)
- [Prism Mock Server](https://stoplight.io/open-source/prism)
