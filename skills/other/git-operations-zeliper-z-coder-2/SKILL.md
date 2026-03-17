---
name: git-operations
description: git 명령어 사용 및 커밋 생성 가이드
allowed-tools: Bash
---

# Git Operations 가이드

git 명령어를 사용하여 변경사항을 관리하고 커밋하는 방법입니다.

## 핵심 원칙

**커밋 메시지 형식**: `[TASK-ID] Description`

예시:
- `[TASK-001] Add user authentication middleware`
- `[TASK-002] Fix login validation bug`
- `[TASK-003] Refactor database connection handling`

## 커밋 워크플로우

### 1. 변경사항 확인

```bash
# 변경된 파일 목록
git status

# 변경 내용 확인
git diff

# 스테이징된 변경 확인
git diff --staged
```

### 2. 파일 스테이징

```bash
# 특정 파일 스테이징
git add src/auth/login.ts

# 여러 파일 스테이징
git add src/auth/*.ts

# 모든 변경 스테이징 (주의해서 사용)
git add .
```

### 3. 커밋 생성

```bash
# 커밋 메시지와 함께 커밋
git commit -m "[TASK-001] Add user authentication"

# 여러 줄 커밋 메시지
git commit -m "[TASK-001] Add user authentication

- Implement JWT token generation
- Add password hashing
- Create auth middleware"
```

## 커밋하지 않을 파일

### 민감 정보
- `.env`, `.env.local`, `.env.production`
- `credentials.json`, `secrets.json`
- `*.pem`, `*.key`

### 빌드 아티팩트
- `node_modules/`
- `dist/`, `build/`, `out/`
- `__pycache__/`, `*.pyc`
- `.next/`, `.nuxt/`

### 설정 파일 (선택적)
- `.claude/` - 오케스트레이션 설정 (별도 관리)
- `tasks/` - 태스크 파일 (별도 관리)

## 커밋 메시지 작성 규칙

### 형식
```
[TASK-ID] <type>: <subject>

<body> (선택)

<footer> (선택)
```

### Type 종류
| Type | 설명 |
|------|------|
| Add | 새 기능 추가 |
| Fix | 버그 수정 |
| Update | 기존 기능 수정 |
| Refactor | 코드 리팩토링 |
| Remove | 코드/파일 삭제 |
| Docs | 문서 수정 |
| Test | 테스트 추가/수정 |

### 좋은 커밋 메시지 예시

```
[TASK-001] Add user authentication middleware

- Implement JWT token generation and validation
- Add bcrypt password hashing
- Create express middleware for protected routes
```

### 나쁜 커밋 메시지 예시

```
# 너무 모호함
[TASK-001] Fix bug

# TASK-ID 누락
Add login feature

# 너무 김
[TASK-001] Add user authentication middleware and also fix some bugs and refactor the code
```

## 에러 처리

### 커밋 실패 시

```bash
# pre-commit hook 실패
# → 코드 스타일, 린트 에러 수정 후 재시도

# merge conflict
git status  # 충돌 파일 확인
# 충돌 해결 후
git add <resolved-files>
git commit -m "[TASK-ID] Resolve merge conflict"
```

### 커밋 취소

```bash
# 마지막 커밋 취소 (변경사항 유지)
git reset --soft HEAD~1

# 마지막 커밋 수정
git commit --amend -m "[TASK-ID] Updated message"
```

## 브랜치 관리 (선택적)

```bash
# 새 브랜치 생성
git checkout -b feature/TASK-001-auth

# 브랜치 전환
git checkout main

# 브랜치 병합
git merge feature/TASK-001-auth
```

---

<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
