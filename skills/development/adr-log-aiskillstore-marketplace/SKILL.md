---
name: adr-log
description: Document architecture decisions with ADR (Architecture Decision Records). Use when making significant technical decisions, choosing between alternatives, or when onboarding needs context on past decisions.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# ADR (Architecture Decision Records)

아키텍처 결정을 문서화하여 "왜 그렇게 했는지"를 기록하는 스킬입니다.

## Core Principle

> **"결정의 '무엇'보다 '왜'가 중요하다."**
> **"6개월 후의 나도 알아볼 수 있게 기록한다."**

## ADR이 필요한 경우

| 상황 | 예시 |
|------|------|
| 기술 선택 | React vs Vue, PostgreSQL vs MongoDB |
| 아키텍처 패턴 | Monolith vs Microservices |
| 의존성 추가 | 새 라이브러리 도입 |
| 보안 결정 | 인증 방식 선택 |
| 성능 트레이드오프 | 캐싱 전략 결정 |
| 표준 변경 | 코딩 컨벤션 변경 |

## ADR 폴더 구조

```
docs/
└── adr/
    ├── 0000-adr-template.md
    ├── 0001-use-nextjs-app-router.md
    ├── 0002-choose-postgresql-over-mongodb.md
    ├── 0003-implement-jwt-authentication.md
    └── README.md
```

## ADR 템플릿

### `docs/adr/0000-adr-template.md`

```markdown
# [번호]. [결정 제목]

날짜: YYYY-MM-DD

## 상태

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## 컨텍스트

이 결정이 필요한 배경/문제 상황을 설명합니다.

- 현재 상황은 무엇인가?
- 어떤 문제를 해결하려 하는가?
- 어떤 제약 조건이 있는가?

## 결정

우리는 [X]를 선택했다.

### 고려한 대안들

1. **대안 A**: [설명]
   - 장점: ...
   - 단점: ...

2. **대안 B**: [설명]
   - 장점: ...
   - 단점: ...

3. **선택: 대안 C**: [설명]
   - 장점: ...
   - 단점: ...

## 결과

### 긍정적 영향
- ...

### 부정적 영향
- ...

### 리스크
- ...

## 참고 자료

- [링크1]
- [링크2]
```

## 실제 ADR 예시

### `docs/adr/0001-use-nextjs-app-router.md`

```markdown
# 1. Next.js App Router 사용

날짜: 2024-01-15

## 상태

Accepted

## 컨텍스트

새 프로젝트의 프론트엔드 프레임워크를 선택해야 한다.

요구사항:
- SEO 최적화 필요 (마케팅 페이지)
- 빠른 초기 로딩
- 팀의 React 경험 활용
- 서버 사이드 데이터 페칭

## 결정

**Next.js 14 App Router**를 선택한다.

### 고려한 대안들

1. **Next.js Pages Router**
   - 장점: 안정적, 레퍼런스 많음
   - 단점: 레거시화 진행 중, 새 기능 제한적

2. **Remix**
   - 장점: 뛰어난 데이터 로딩, 프로그레시브 향상
   - 단점: 팀 학습 비용, 상대적으로 작은 생태계

3. **선택: Next.js App Router**
   - 장점: React Server Components, 향상된 캐싱, Vercel 최적화
   - 단점: 일부 라이브러리 호환성 이슈, 학습 곡선

## 결과

### 긍정적 영향
- React Server Components로 번들 크기 감소
- 레이아웃 중첩으로 코드 재사용성 향상
- Vercel 배포 최적화

### 부정적 영향
- 일부 클라이언트 전용 라이브러리 사용 시 'use client' 필요
- Pages Router 경험자의 학습 필요

### 리스크
- App Router의 상대적인 신규성 (안정성 확인 필요)
- 일부 third-party 라이브러리 호환성

## 참고 자료

- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [Server Components RFC](https://github.com/reactjs/rfcs/pull/188)
```

### `docs/adr/0002-choose-postgresql-over-mongodb.md`

```markdown
# 2. PostgreSQL 선택 (MongoDB 대신)

날짜: 2024-01-20

## 상태

Accepted

## 컨텍스트

프로젝트의 주 데이터베이스를 선택해야 한다.

데이터 특성:
- 사용자, 프로젝트, 미디어 간 관계 존재
- 트랜잭션 무결성 필요 (결제 연동 예정)
- 복잡한 쿼리 (필터링, 정렬, 집계)

## 결정

**PostgreSQL**을 선택한다.

### 고려한 대안들

1. **MongoDB**
   - 장점: 스키마 유연성, 수평 확장 용이
   - 단점: 복잡한 JOIN 어려움, 트랜잭션 제한

2. **선택: PostgreSQL**
   - 장점: ACID 보장, 강력한 JOIN, JSON 지원
   - 단점: 수평 확장 복잡, 스키마 변경 마이그레이션 필요

## 결과

### 긍정적 영향
- Prisma와 완벽한 호환
- 복잡한 관계 쿼리 최적화
- 결제 데이터 무결성 보장

### 부정적 영향
- 스키마 변경 시 마이그레이션 필요
- 초기 스키마 설계 중요

### 관련 결정
- Prisma ORM 사용 (ADR-003 예정)
- 마이그레이션 전략 수립 필요
```

## ADR 작성 가이드

### 번호 체계

```
0001 ~ 0099: 기초 아키텍처 결정
0100 ~ 0199: 프론트엔드 관련
0200 ~ 0299: 백엔드 관련
0300 ~ 0399: 인프라/DevOps 관련
0400 ~ 0499: 보안 관련
```

### 상태 흐름

```
Proposed → Accepted → [Deprecated | Superseded]
```

- **Proposed**: 검토 중
- **Accepted**: 승인되어 적용 중
- **Deprecated**: 더 이상 유효하지 않음
- **Superseded by ADR-XXXX**: 새 결정으로 대체됨

### 작성 팁

```markdown
## 컨텍스트 작성 팁
- 배경 설명은 신규 팀원도 이해할 수 있게
- 제약 조건(시간, 예산, 기술 스택) 명시
- 문제의 긴급성/중요도 언급

## 결정 작성 팁
- 결정 내용을 한 문장으로 요약
- 대안들을 공정하게 비교
- 선택 이유를 명확히

## 결과 작성 팁
- 트레이드오프를 솔직하게
- 예상 리스크와 대응 방안
- 관련된 후속 결정 언급
```

## ADR 도구

### adr-tools (CLI)

```bash
# macOS
brew install adr-tools

# 초기화
adr init docs/adr

# 새 ADR 생성
adr new "Use Next.js App Router"

# ADR 목록
adr list

# ADR 생성 (대체)
adr new -s 1 "Switch to Remix"
```

### README.md (ADR 인덱스)

```markdown
# Architecture Decision Records

| 번호 | 제목 | 상태 | 날짜 |
|------|------|------|------|
| [0001](0001-use-nextjs-app-router.md) | Next.js App Router 사용 | Accepted | 2024-01-15 |
| [0002](0002-choose-postgresql-over-mongodb.md) | PostgreSQL 선택 | Accepted | 2024-01-20 |
| [0003](0003-jwt-authentication.md) | JWT 인증 구현 | Accepted | 2024-01-25 |
```

## Workflow

### ADR 작성 시점

```
1. 기술 선택/변경 논의 시작
2. 대안 검토 및 비교
3. 팀 논의 (PR 또는 미팅)
4. 결정 후 ADR 작성
5. PR로 ADR 추가
6. 리뷰 후 머지
```

### 코드 리뷰에서

```
PR 리뷰어:
"이 라이브러리 선택에 대한 ADR이 있나요?"

작성자:
"ADR-0015에 근거 정리되어 있습니다."
또는
"ADR 추가하겠습니다."
```

## Checklist

### 프로젝트 설정

- [ ] `docs/adr/` 폴더 생성
- [ ] ADR 템플릿 파일 추가
- [ ] README.md (인덱스) 생성
- [ ] 번호 체계 정의

### ADR 작성 시

- [ ] 컨텍스트가 충분히 설명되었는가?
- [ ] 대안들이 공정하게 비교되었는가?
- [ ] 결정 이유가 명확한가?
- [ ] 트레이드오프가 솔직하게 기록되었는가?
- [ ] 관련 ADR/이슈가 링크되었는가?

## References

- [ADR GitHub](https://adr.github.io/)
- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [adr-tools](https://github.com/npryce/adr-tools)
