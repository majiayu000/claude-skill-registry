---
name: software-architecture
description: Clean Architecture and SOLID principles guide. Use this when designing systems, reviewing architecture, or making structural decisions.
allowed-tools: Read, Glob, Grep, Edit, Write
license: MIT
metadata:
  author: NeoLabHQ
  version: "1.0"
---

# Software Architecture

Clean Architecture와 DDD 원칙 기반 소프트웨어 설계 가이드입니다.

## Core Principles

### SOLID

| 원칙 | 설명 | 예시 |
|------|------|------|
| **S**ingle Responsibility | 하나의 클래스는 하나의 책임 | `UserRepository` vs `UserService` |
| **O**pen/Closed | 확장에 열림, 수정에 닫힘 | 인터페이스 사용 |
| **L**iskov Substitution | 하위 타입은 상위 타입 대체 가능 | 상속 계약 준수 |
| **I**nterface Segregation | 클라이언트별 인터페이스 분리 | `IReader` vs `IWriter` |
| **D**ependency Inversion | 추상화에 의존 | DI 컨테이너 사용 |

### Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│           Frameworks & Drivers          │  ← DB, Web, UI
├─────────────────────────────────────────┤
│         Interface Adapters              │  ← Controllers, Gateways
├─────────────────────────────────────────┤
│         Application Business Rules      │  ← Use Cases
├─────────────────────────────────────────┤
│         Enterprise Business Rules       │  ← Entities
└─────────────────────────────────────────┘
```

**의존성 규칙**: 바깥 → 안쪽 방향으로만 의존

## Code Style Rules

### Early Return Pattern

```typescript
// ❌ 중첩된 조건문
function process(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // do something
      }
    }
  }
}

// ✅ Early Return
function process(user) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) return;
  // do something
}
```

### Function/File Size Limits

| 대상 | 권장 | 최대 | 조치 |
|------|------|------|------|
| 함수 | 30줄 | 50줄 | 분리 |
| 컴포넌트 | 80줄 | 150줄 | 분리 |
| 파일 | 200줄 | 300줄 | 모듈화 |

### Domain-Specific Naming

```typescript
// ❌ 제네릭 네이밍
utils/helpers.ts
common/index.ts

// ✅ 도메인 네이밍
services/OrderCalculator.ts
auth/UserAuthenticator.ts
```

## Library-First Approach

> "모든 커스텀 코드는 유지보수, 테스트, 문서화가 필요한 부채다"

**코드 작성 전 확인:**
1. npm/yarn 패키지 검색
2. 기존 서비스/API 확인
3. 오픈소스 솔루션 검토

## Anti-Patterns to Avoid

| Anti-Pattern | 문제점 | 해결책 |
|--------------|--------|--------|
| NIH Syndrome | 바퀴 재발명 | 라이브러리 우선 |
| God Class | 너무 많은 책임 | SRP 적용 |
| Spaghetti Code | 얽힌 의존성 | 레이어 분리 |
| Magic Numbers | 의미 불명확 | 상수 추출 |
| Deep Nesting | 가독성 저하 | Early Return |

## Separation of Concerns

```
✅ 올바른 분리
├── domain/          # 비즈니스 로직
├── application/     # Use Cases
├── infrastructure/  # DB, API
└── presentation/    # UI, Controllers

❌ 잘못된 분리
├── components/
│   └── UserCard.tsx  # UI + API 호출 + 비즈니스 로직 혼합
```

## Decision Checklist

새로운 코드 작성 시:

- [ ] 기존 라이브러리/서비스로 해결 가능?
- [ ] 단일 책임 원칙 준수?
- [ ] 의존성 방향 올바름?
- [ ] 테스트 가능한 구조?
- [ ] 도메인 네이밍 사용?
