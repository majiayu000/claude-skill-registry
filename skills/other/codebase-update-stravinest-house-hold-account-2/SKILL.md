---
name: codebase-update
description: 코드베이스 변경 후 .codebase 문서를 업데이트합니다. 새 기능 추가, 구조 변경, 리팩토링 후 문서 동기화가 필요할 때 사용하세요.
---

# Codebase Update Skill

프로젝트에 변경사항이 있을 때 `.codebase/` 디렉토리의 문서를 업데이트하여 코드와 문서의 동기화를 유지합니다.

## 지침

### 1단계: 변경사항 파악
최근 변경된 내용을 확인하세요:

```bash
# 최근 변경된 파일 확인
git status
git diff --name-only HEAD~5

# 또는 특정 커밋 이후 변경사항
git diff --name-only <commit-hash>
```

### 2단계: 영향 받는 문서 식별
변경 유형에 따라 업데이트할 문서를 결정하세요:

| 변경 유형 | 업데이트할 문서 |
|----------|----------------|
| 새 API 엔드포인트 추가 | `API.md` |
| 디렉토리/파일 구조 변경 | `DIRECTORY.md` |
| 새 모듈/서비스 추가 | `MODULES.md` |
| 데이터베이스 스키마 변경 | `DATABASE.md` |
| 아키텍처 변경 | `ARCHITECTURE.md` |
| 코드 패턴/컨벤션 변경 | `PATTERNS.md` |

### 3단계: 문서 업데이트
해당 문서를 읽고 변경사항을 반영하세요:

1. 기존 문서 내용 확인
2. 변경된 코드 분석
3. 문서에 변경사항 반영
4. 일관된 형식 유지

### 4단계: 검증
업데이트된 문서가 실제 코드와 일치하는지 확인하세요.

## 문서 템플릿

### ARCHITECTURE.md
```markdown
# 아키텍처 개요

## 레이어 구조
- Presentation Layer (Controllers/Routes)
- Business Layer (Services)
- Data Layer (Repositories/Models)

## 의존성 흐름
[다이어그램 또는 설명]

## 주요 컴포넌트
[컴포넌트 목록 및 역할]
```

### DIRECTORY.md
```markdown
# 디렉토리 구조

\`\`\`
src/
├── controllers/    # API 컨트롤러
├── services/       # 비즈니스 로직
├── models/         # 데이터 모델
├── routes/         # 라우팅 정의
├── middlewares/    # 미들웨어
├── utils/          # 유틸리티 함수
└── config/         # 설정 파일
\`\`\`
```

### API.md
```markdown
# API 엔드포인트

## 인증 (Auth)
- POST /api/auth/login - 로그인
- POST /api/auth/register - 회원가입

## 사용자 (Users)
- GET /api/users - 사용자 목록
- GET /api/users/:id - 사용자 상세
```

### DATABASE.md
```markdown
# 데이터베이스 스키마

## 엔티티
- User: 사용자 정보
- Post: 게시글

## 관계
- User 1:N Post
```

### MODULES.md
```markdown
# 주요 모듈

## AuthModule
- 역할: 인증/인가 처리
- 위치: src/modules/auth/
- 주요 파일: auth.service.ts, auth.controller.ts
```

### PATTERNS.md
```markdown
# 코드 패턴 및 컨벤션

## 네이밍 규칙
- 파일: kebab-case (user-service.ts)
- 클래스: PascalCase (UserService)
- 함수: camelCase (getUserById)

## 에러 처리
[에러 처리 패턴 설명]
```

## 자동 업데이트 트리거

다음 상황에서 이 스킬을 사용하세요:

1. **기능 구현 완료 후**: 새로운 기능이 추가되면 관련 문서 업데이트
2. **리팩토링 후**: 구조 변경이 있으면 DIRECTORY.md, ARCHITECTURE.md 업데이트
3. **PR 생성 전**: 변경사항이 문서에 반영되었는지 확인
4. **코드 리뷰 시**: 문서 업데이트 누락 여부 확인

## 주의사항

- 문서는 간결하게 유지하세요 (핵심 정보만)
- 자동 생성 가능한 정보는 문서화하지 마세요 (예: 타입 정의)
- 문서 형식과 스타일을 일관되게 유지하세요
- `.codebase/` 디렉토리가 없으면 먼저 생성하세요
