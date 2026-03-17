---
name: "frontend-fsd-architect"
description: "Feature-Sliced Design architecture specialist"
---

# Frontend FSD Architect

Feature-Sliced Design v2.1 기반 프론트엔드 아키텍처 자동 생성/마이그레이션/검증

## Overview

**FSD 핵심 가치**: "코드를 어디에 둘지 모호함" 해결
- 7계층 구조 + 엄격한 의존성 규칙
- 의존성 혼란, 팀 협업 충돌 방지

**성과**:
- 구조 설계 시간: 80% 단축
- 코드 변경 영향: 70% 감소
- Git 충돌: 60% 감소

## When to Use

### ✅ 적합
- 20k+ LOC 예상 프로젝트
- 3명+ 팀 규모
- 6개월+ 장기 운영
- 복잡한 비즈니스 로직

### ❌ 부적합
- MVP/POC (1-3개월)
- 10k LOC 미만
- 1-2명 개발자
- 정적 콘텐츠 위주

## FSD 7계층

```
src/
├── app/           # 애플리케이션 초기화
├── pages/         # 페이지 단위 조합
├── widgets/       # 독립 UI 블록
├── features/      # 비즈니스 기능
├── entities/      # 도메인 객체
└── shared/        # 공통 라이브러리
```

**의존성 규칙**: 상위 → 하위만 허용

## Core Capabilities

### 1. 구조 자동 생성
프레임워크별 보일러플레이트: React, Vue, Angular, Svelte

### 2. 마이그레이션
기존 MVC/Classical → FSD 5단계 전환

### 3. 린터 통합
Steiger로 의존성 위반 실시간 검증

### 4. 한국 환경
KRW 포맷, 휴대폰 번호 등 로컬라이제이션

## Usage

### 신규 프로젝트
```
"React + TypeScript로 전자상거래 FSD 구조 생성해줘"
→ 전체 폴더 구조 + 보일러플레이트 생성
```

### 마이그레이션
```
"기존 components/ 폴더를 FSD 구조로 전환해줘"
→ 5단계 마이그레이션 계획 제시
```

### 검증
```
"FSD 의존성 규칙 위반 검사해줘"
→ Steiger 실행 + 위반 항목 리포트
```

## References

- `references/layer-guide.md` - 7계층 상세 가이드
- `references/migration-steps.md` - 마이그레이션 단계
- `references/framework-templates.md` - 프레임워크별 템플릿
- `references/steiger-config.md` - 린터 설정
