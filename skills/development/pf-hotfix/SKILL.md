---
name: pf-hotfix
description: 긴급 버그 수정 플로우. "핫픽스", "긴급", "버그 수정" 요청 시 사용.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# PF 핫픽스 플로우

$ARGUMENTS 긴급 버그를 빠르게 수정합니다.

---

## 핫픽스 플로우

```
1. 버그 재현 & 원인 파악 (10분 이내)
   ↓
2. 브랜치 생성
   ↓
3. 최소한의 수정
   ↓
4. 테스트
   ↓
5. PR 생성 & 머지
   ↓
6. 배포 확인
```

---

## 1단계: 버그 재현 & 원인 파악

### 정보 수집
```
- 어떤 페이지/기능에서 발생?
- 재현 단계?
- 에러 메시지?
- 콘솔/네트워크 에러?
- 언제부터 발생? (최근 배포 이후?)
```

### 빠른 디버깅

```bash
# 최근 커밋 확인
git log --oneline -10

# 최근 변경 파일 확인
git diff HEAD~5 --name-only

# 에러 관련 파일 검색
/search "에러메시지"
```

---

## 2단계: 브랜치 생성

```bash
# 핫픽스 브랜치
git checkout main
git pull
git checkout -b fix/이슈번호-간단설명

# 예시
git checkout -b fix/456-login-crash
```

---

## 3단계: 최소한의 수정

### 원칙
- **오직 버그만 수정** - 리팩토링 금지
- **영향 범위 최소화** - 관련 파일만 수정
- **테스트 가능한 수정** - 수정 후 바로 확인 가능

### 수정 예시

```tsx
// ❌ 핫픽스에서 하면 안 되는 것
// - 코드 정리
// - 변수명 변경
// - 구조 개선

// ✅ 핫픽스에서 해야 하는 것
// - 버그의 직접적인 원인만 수정

// Before (버그)
const user = users[0];
console.log(user.name);  // users가 빈 배열이면 에러

// After (수정)
const user = users[0];
if (user) {
  console.log(user.name);
}
```

---

## 4단계: 테스트

### 필수 확인

```bash
# 1. 타입 체크
pnpm tsc --noEmit

# 2. 린트
pnpm lint

# 3. 빌드
pnpm build

# 4. 로컬에서 버그 재현 테스트
pnpm --filter 앱이름 dev
```

### 체크리스트
- [ ] 버그가 수정되었는가?
- [ ] 다른 기능이 깨지지 않았는가?
- [ ] 빌드가 성공하는가?

---

## 5단계: PR 생성 & 머지

### 커밋

```bash
git add .
git commit -m "fix: 로그인 페이지 크래시 수정

- users 배열이 빈 경우 null 체크 추가
- Fixes #456"
```

### PR 생성

```bash
git push -u origin fix/456-login-crash

gh pr create --title "fix: 로그인 페이지 크래시 수정" --body "
## 버그
로그인 페이지에서 users 배열이 빈 경우 크래시 발생

## 원인
users[0] 접근 시 null 체크 누락

## 수정
null 체크 추가

## 테스트
- [x] 로컬 빌드 성공
- [x] 버그 재현 후 수정 확인

Fixes #456
"
```

### 빠른 머지 요청

- 리뷰어에게 긴급 리뷰 요청
- 또는 권한이 있다면 셀프 머지 (긴급 시)

---

## 6단계: 배포 확인

### 자동 배포 (main 머지 시)

```bash
# GitHub Actions 상태 확인
gh run list --limit 5

# 또는 GitHub에서 확인
# Actions 탭 > deploy-staging 워크플로우
```

### 수동 확인

```bash
# 스테이징 서버에서 버그 수정 확인
# 프로덕션 배포 후 최종 확인
```

---

## 핫픽스 체크리스트

```
[ ] 버그 원인 파악됨
[ ] 최소한의 변경만 수행
[ ] 타입 체크 통과
[ ] 린트 통과
[ ] 빌드 성공
[ ] 버그 수정 확인
[ ] 사이드 이펙트 없음
[ ] PR 생성
[ ] 배포 확인
```

---

## 긴급 연락

- 배포 실패 시: DevOps 담당자
- 서버 에러 시: 백엔드 담당자
- DB 문제 시: DBA

---

## 롤백 (최후의 수단)

```bash
# 이전 커밋으로 롤백
git revert HEAD
git push

# 또는 이전 배포 버전으로 롤백 (서버에서)
```
