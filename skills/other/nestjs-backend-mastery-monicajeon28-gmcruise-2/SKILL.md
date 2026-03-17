---
name: nestjs-backend-mastery
description: "**NESTJS BACKEND MASTERY** - 'NestJS', 'Zod', 'shared 패키지', 'DTO', '스키마', '타입 공유', 'controller', 'service', '백엔드' 요청 시 자동 발동. *.controller.ts/*.service.ts/*.dto.ts/*.schema.ts 작업 시 적용. Zod 기반 type-safe 백엔드. 웹/모바일 타입 공유."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# NestJS Backend Mastery v1.0

**Type-Safe Backend Guardian** - NestJS + Zod + Monorepo 환경에서 타입 안전한 백엔드 개발

## 핵심 문제 인식

```yaml
문제점:
  타입_미추출_시:
    - 웹/모바일에서 inline interface 사용
    - 수정 시 유지보수 x3 (Backend + Web + Mobile)
    - build로 문제 캐치 불가 → 런타임 버그 발생

  해결책:
    - Zod 스키마를 Single Source of Truth로
    - packages/shared에서 중앙 관리
    - Controller 데코레이터 type-strict 적용
    - API Client 자동 생성 (Orval)
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  File_Patterns:
    - "*.controller.ts, *.controller.js"
    - "*.service.ts, *.service.js"
    - "*.module.ts, *.module.js"
    - "*.dto.ts, *.schema.ts"
    - "packages/shared/**/*"
    - "apps/backend/**/*"

  Keywords_KO:
    - "NestJS, 네스트, 백엔드"
    - "Zod, 검증, 스키마, DTO"
    - "타입 공유, shared 패키지"
    - "컨트롤러, 서비스, 모듈"
    - "API 타입, 엔드포인트 타입"

  Keywords_EN:
    - "NestJS, backend, controller"
    - "Zod, validation, schema, DTO"
    - "type sharing, shared package"
    - "type-safe, strict typing"
```

## 선택적 문서 로드 전략

```yaml
Document_Loading_Strategy:
  Always_Load:
    - "core/zod-schema-patterns.md"      # Zod 스키마 작성 (항상)
    - "quick-reference/checklist.md"     # 체크리스트 (항상)

  Context_Specific_Load:
    Shared_Package: "core/shared-package-structure.md"
    Controller_Work: "patterns/controller-decorators.md"
    DTO_Design: "patterns/dto-design.md"
    API_Client: "patterns/api-client-generation.md"
    New_Module: "templates/module-template.md"
```

---

## Quick Reference

### 1. 핵심 원칙 - Zod Schema First

```typescript
// packages/shared/src/schemas/user.schema.ts

import { z } from 'zod';

// 1. Zod 스키마 정의 (Single Source of Truth)
export const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(50),
});

// 2. TypeScript 타입 자동 추론
export type CreateUserInput = z.infer<typeof createUserSchema>;
// → { email: string; password: string; name: string; }
```

### 2. NestJS에서 Zod 사용

```typescript
// apps/backend/src/users/dto/create-user.dto.ts

import { createZodDto } from 'nestjs-zod';
import { createUserSchema } from '@myapp/shared';

// Zod 스키마 → NestJS DTO 변환
export class CreateUserDto extends createZodDto(createUserSchema) {}
```

### 3. Controller 필수 데코레이터

```typescript
@Controller('users')
@ApiTags('Users')                    // 필수: Swagger 그룹
@ApiBearerAuth('access-token')       // 조건부: 인증 필요시
export class UsersController {

  @Post()
  @ApiOperation({ summary: '사용자 생성' })           // 필수
  @ApiBody({ type: CreateUserDto })                  // 필수
  @ApiResponse({ status: 201, type: UserResponseDto }) // 필수
  @ApiResponse({ status: 400, description: '검증 실패' }) // 필수
  async create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.usersService.create(dto);
  }
}
```

### 4. 의존성 방향

```
✅ 허용:
   apps/backend → packages/shared
   apps/web     → packages/shared
   apps/mobile  → packages/shared

❌ 금지:
   packages/shared → apps/*
   apps/backend → apps/web
```

---

## 모노레포 구조 (packages/shared)

```
packages/
└── shared/
    ├── package.json
    └── src/
        ├── index.ts              # Barrel export
        ├── schemas/              # Zod 스키마 (진실의 원천)
        │   ├── user.schema.ts
        │   ├── order.schema.ts
        │   └── common.schema.ts
        ├── types/                # Zod에서 추론된 타입
        │   ├── user.types.ts
        │   └── api.types.ts
        └── validators/           # 재사용 검증 로직
            ├── email.validator.ts
            └── password.validator.ts
```

---

## API Client 자동 생성 (Orval)

```yaml
Workflow:
  1. NestJS에서 Swagger JSON 생성
  2. Orval로 API Client 자동 생성
  3. React Query 훅 + TypeScript 타입 생성
  4. Frontend에서 import 사용

Benefits:
  - OpenAPI 스펙 기반 타입 안전
  - React Query 훅 자동 생성
  - MSW Mock 자동 생성
  - 스펙 변경 시 컴파일 에러로 감지
```

---

## 문서 구조

| 파일 | 설명 |
|------|------|
| `core/zod-schema-patterns.md` | Zod 스키마 작성 패턴 |
| `core/shared-package-structure.md` | packages/shared 구조 |
| `patterns/controller-decorators.md` | Controller 데코레이터 표준 |
| `patterns/api-client-generation.md` | Orval API Client 생성 |
| `patterns/bun-integration.md` | Bun 런타임 통합 가이드 |
| `quick-reference/checklist.md` | 개발 체크리스트 |
| `quick-reference/anti-patterns.md` | 안티패턴 목록 |

---

## Bun 런타임 지원

```yaml
Bun_Integration:
  장점:
    - "TypeScript 네이티브 실행 (트랜스파일 불필요)"
    - "패키지 설치 10-20배 빠름"
    - "HTTP 처리량 Node.js 대비 4배"
    - "All-in-One (런타임 + 번들러 + 테스트 러너)"

  워크스페이스_설정:
    - "package.json의 workspaces 배열 설정"
    - "workspace:* 프로토콜로 내부 의존성"
    - "bun install --filter로 선택적 설치"

  권장_사용:
    - "새 프로젝트, MVP, 빠른 프로토타이핑"
    - "개발 환경에서 적극 활용"
    - "프로덕션은 충분한 테스트 후 결정"

  상세_가이드: "patterns/bun-integration.md"
```

---

## 관련 스킬 통합

### Base Knowledge (다른 스킬 참조)

> **SOLID 원칙**: `clean-code-mastery/core/principles.md` 참조
> **의존성 규칙**: `monorepo-architect/core/dependency-rules.md` 참조
> **보안 기본**: `security-shield` 스킬 참조
> **Swagger 데코레이터**: `api-first-design/patterns/swagger-decorators.md` 참조

이 스킬은 위 내용을 중복하지 않고, **NestJS + Zod 특화 패턴**에 집중합니다.

### 스킬 시너지 매트릭스

```yaml
Integration_Skills:
  api-first-design:
    역할: "Contract-First API 설계, Swagger/OpenAPI, Orval"
    연동: "Swagger 데코레이터 상세 → api-first-design"
    트리거_조율: "nestjs가 Primary, api-first는 문서화 보조"
    참조: "patterns/swagger-decorators.md"

  monorepo-architect:
    역할: "모노레포 구조, 의존성 방향, Turborepo"
    연동: "packages/shared 구조 → monorepo-architect"
    트리거_조율: "shared 패키지 작업 시 monorepo가 Primary"
    참조: "core/dependency-rules.md"

  clean-code-mastery:
    역할: "SOLID, DRY, KISS, TypeScript strict"
    연동: "코드 품질 원칙 → clean-code-mastery"
    트리거_조율: "모든 코드 작성 시 함께 적용"
    참조: "core/principles.md"

  security-shield:
    역할: "인증/인가, OWASP, 보안 검증"
    연동: "JWT Guard, 인증 로직 → security-shield"
    트리거_조율: "인증 관련 코드 시 security가 Primary"

  tdd-guardian:
    역할: "테스트 작성, 커버리지 80%+"
    연동: "Service 테스트 템플릿 참조"
    트리거_조율: "테스트 파일 작업 시 tdd가 Primary"

  code-reviewer:
    역할: "통합 품질 점수, Quality Gate"
    연동: "코드 리뷰 시 모든 스킬 점수 통합"
    트리거_조율: "리뷰 요청 시만 발동"
```

### 개발 워크플로우 순서

```
1. monorepo-architect    → 패키지 위치 결정
2. api-first-design      → OpenAPI 스펙 정의
3. nestjs-backend-mastery → Zod 스키마 + DTO + Controller
4. clean-code-mastery    → 코드 품질 적용
5. tdd-guardian          → 테스트 작성
6. security-shield       → 보안 검토 (인증 관련 시)
7. code-reviewer         → 최종 품질 검증
```

---

**Version**: 1.1.0
**Updated**: 2025-12-10
**Dependencies**: nestjs-zod, zod, @nestjs/swagger, orval, bun (optional)
**Related Skills**: api-first-design, monorepo-architect, clean-code-mastery, security-shield, tdd-guardian, code-reviewer
