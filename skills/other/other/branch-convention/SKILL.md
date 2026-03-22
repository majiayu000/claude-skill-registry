---
name: branch-convention
description: Git 브랜치 생성 시 네이밍 컨벤션과 브랜치 전략을 따르도록 적용. Use when creating git branches to follow naming conventions and branching strategy.
---

# Git 브랜치 컨벤션

## 브랜치 네이밍 형식

`type/description` 또는 `type/TICKET-XXX-description`

티켓 번호가 있으면 포함 권장.

---

## 브랜치 타입 표

| 타입 | 설명 |
|-----|------|
| feature | 새 기능 개발 |
| fix (또는 bugfix) | 버그 수정 |
| hotfix | 긴급 프로덕션 수정 |
| refactor | 코드 리팩토링 |
| docs | 문서 변경 |
| test | 테스트 추가/수정 |
| chore | 유지보수, 빌드, 설정 |
| release | 릴리스 준비 |

---

## 네이밍 규칙

- 소문자만 사용
- 단어 구분은 하이픈(-) (언더스코어, 공백 금지)
- 티켓 번호가 있으면 포함 (예: feature/TASK-123-add-login)
- 짧되 설명적으로

---

## Git Flow 전략

| 브랜치 | 역할 |
|-------|------|
| main / master | 프로덕션 배포 가능 코드 |
| develop | 통합 브랜치, feature들 모임 |
| feature/* | develop에서 분기, develop으로 머지 |
| release/* | develop에서 분기, 릴리스 준비 |
| hotfix/* | main에서 분기, 긴급 수정 |

---

## 브랜치 보호 규칙

| 브랜치 | 권장 설정 |
|-------|----------|
| main / master | PR 필수, 리뷰 필수, 직접 푸시 금지 |
| develop | PR 필수, CI 통과 필수 |
| feature/* | 보호 없음 (개발자 브랜치) |

---

## 브랜치 라이프사이클

1. 올바른 base 브랜치에서 생성
2. base 브랜치와 정기적으로 rebase/merge
3. 머지 후 삭제

---

## 릴리스 브랜치 네이밍

`release/vX.Y.Z` 또는 `release/{버전}+{날짜}`

예: release/v1.2.0, release/1.2.1+250430

---

## Hotfix 브랜치 네이밍

`hotfix/vX.Y.Z` 또는 `hotfix/description`

예: hotfix/v1.2.1, hotfix/critical-auth-fix

---

## 예시

### 기능 개발

- feature/user-authentication
- feature/TASK-123-add-login

### 버그 수정

- fix/api-timeout-handling
- fix/TASK-456-null-pointer-crash

### 긴급 수정

- hotfix/critical-security-patch
- hotfix/v1.2.1

### 리팩토링

- refactor/extract-validation-logic
- refactor/TASK-789-api-layer

---

## 워크플로우 예시

### Feature 개발 흐름

1. develop에서 feature/xxx 분기
2. 작업 후 develop으로 PR
3. 리뷰 및 머지
4. feature 브랜치 삭제

### Hotfix 흐름

1. main에서 hotfix/xxx 분기
2. 수정 후 main과 develop 양쪽으로 PR
3. 머지 후 hotfix 브랜치 삭제

### Release 흐름

1. develop에서 release/vX.Y.Z 분기
2. 버그 수정만 release 브랜치에서 진행
3. main과 develop에 머지
4. 릴리스 브랜치 삭제

---

## 브랜치 정리 명령어

```bash
# 원격에서 삭제된 브랜치 참조 제거
git fetch --prune

# 머지된 로컬 브랜치 삭제
git branch -d branch-name

# 강제 삭제
git branch -D branch-name
```

---

## 좋은 예시

- feature/user-authentication
- fix/api-timeout-handling
- refactor/extract-validation-logic
- feature/PROJ-123-add-login

---

## 나쁜 예시

- Feature/UserAuth (대문자)
- feature_user_auth (언더스코어)
- my-branch (타입 누락)
- branch (설명 누락)
