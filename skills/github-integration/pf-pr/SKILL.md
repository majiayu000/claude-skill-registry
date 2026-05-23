---
name: pf-pr
description: pf-frontend GitHub PR/커밋 워크플로우. 사용자가 "PR 올려줘", "커밋해줘", "풀리퀘 생성해줘" 등 명시적으로 요청할 때만 사용. 코드 작성 완료 후 자동 실행 금지.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# PF GitHub PR 워크플로우

$ARGUMENTS PR을 pluxity/pf-frontend 프로젝트에 생성합니다.

---

## 프로젝트 정보

- **저장소**: `pluxity/pf-frontend`
- **PR URL**: https://github.com/pluxity/pf-frontend/pulls
- **기본 브랜치**: `main`

---

## PR 워크플로우

```
1. 변경사항 확인
   ↓
2. 커밋 메시지 작성
   ↓
3. 푸시
   ↓
4. PR 생성
   ↓
5. 리뷰 요청
```

---

## 1단계: 변경사항 확인

```bash
# 변경된 파일 확인
git status

# 변경 내용 확인
git diff

# 스테이징된 변경 확인
git diff --staged
```

---

## 2단계: 커밋 메시지 컨벤션

### 형식

```
타입(스코프): 제목

본문 (선택)

Footer (선택)
```

### 타입

| 타입       | 설명      | 예시                                |
| ---------- | --------- | ----------------------------------- |
| `feat`     | 새 기능   | feat(ui): Button 컴포넌트 추가      |
| `fix`      | 버그 수정 | fix(map): 마커 클릭 이벤트 수정     |
| `docs`     | 문서      | docs: README 업데이트               |
| `style`    | 포맷팅    | style: 코드 포맷 정리               |
| `refactor` | 리팩토링  | refactor(core): API 클라이언트 개선 |
| `perf`     | 성능 개선 | perf(ui): Table 가상화 적용         |
| `test`     | 테스트    | test(ui): Button 테스트 추가        |
| `chore`    | 빌드/설정 | chore: 의존성 업데이트              |

### 스코프 (선택)

```
- ui: @pf-dev/ui 패키지
- map: @pf-dev/map 패키지
- core: @pf-dev/core 패키지
- app명: 특정 앱
- (생략): 전체 또는 여러 패키지
```

### 예시

```bash
# 단일 커밋
git commit -m "feat(ui): DatePicker 컴포넌트 추가

- 날짜 선택 기능
- 범위 선택 기능
- 한국어 로케일 지원

Closes #123"

# 버그 수정
git commit -m "fix(map): 3D 모델 로딩 실패 수정

nullish 체크 누락으로 인한 크래시 수정

Fixes #456"
```

---

## 3단계: 브랜치 & 푸시

### 브랜치 네이밍

```bash
# 기능 개발
feature/이슈번호-간단설명
feature/123-user-profile

# 버그 수정
fix/이슈번호-간단설명
fix/456-login-crash

# 문서
docs/간단설명
docs/readme-update

# 리팩토링
refactor/간단설명
refactor/api-client
```

### 푸시

```bash
# 첫 푸시 (업스트림 설정)
git push -u origin feature/123-user-profile

# 이후 푸시
git push
```

---

## 4단계: PR 생성

### 기본 템플릿

```bash
gh pr create \
  --repo pluxity/pf-frontend \
  --base main \
  --title "feat(ui): DatePicker 컴포넌트 추가" \
  --body "$(cat <<'EOF'
## 개요
DatePicker 컴포넌트를 @pf-dev/ui 패키지에 추가합니다.

## 변경사항
- DatePicker 컴포넌트 구현
- 날짜 범위 선택 기능
- 한국어 로케일 지원
- Storybook 문서 추가

## 스크린샷
[스크린샷 첨부]

## 테스트
- [ ] 단일 날짜 선택
- [ ] 범위 선택
- [ ] 키보드 네비게이션
- [ ] 모바일 반응형

## 체크리스트
- [ ] 타입 체크 통과 (`pnpm tsc --noEmit`)
- [ ] 린트 통과 (`pnpm lint`)
- [ ] 빌드 성공 (`pnpm build`)
- [ ] Storybook 확인

## 관련 이슈
Closes #123
EOF
)"
```

### PR 타입별 템플릿

#### 기능 추가 (Feature)

```bash
gh pr create \
  --repo pluxity/pf-frontend \
  --title "feat(스코프): 제목" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## 개요
[기능 설명]

## 변경사항
- 변경1
- 변경2

## 스크린샷
[해당시 첨부]

## 테스트
- [ ] 테스트1
- [ ] 테스트2

## 체크리스트
- [ ] 타입 체크 통과
- [ ] 린트 통과
- [ ] 빌드 성공

## 관련 이슈
Closes #이슈번호
EOF
)"
```

#### 버그 수정 (Bug Fix)

```bash
gh pr create \
  --repo pluxity/pf-frontend \
  --title "fix(스코프): 제목" \
  --label "bug" \
  --body "$(cat <<'EOF'
## 버그 설명
[수정한 버그 설명]

## 원인
[버그 원인]

## 해결 방법
[어떻게 수정했는지]

## 테스트
- [ ] 버그 재현 후 수정 확인
- [ ] 사이드 이펙트 확인

## 체크리스트
- [ ] 타입 체크 통과
- [ ] 린트 통과
- [ ] 빌드 성공

## 관련 이슈
Fixes #이슈번호
EOF
)"
```

#### 리팩토링 (Refactor)

```bash
gh pr create \
  --repo pluxity/pf-frontend \
  --title "refactor(스코프): 제목" \
  --label "refactor" \
  --body "$(cat <<'EOF'
## 개요
[리팩토링 목적]

## 변경사항
- Before: [이전 구조/방식]
- After: [새로운 구조/방식]

## 영향 범위
[영향받는 파일/컴포넌트]

## 테스트
- [ ] 기존 기능 동작 확인
- [ ] 성능 저하 없음

## 체크리스트
- [ ] 타입 체크 통과
- [ ] 린트 통과
- [ ] 빌드 성공
EOF
)"
```

---

## 5단계: 리뷰 & 머지

### 리뷰어 지정

```bash
# PR 생성 시 리뷰어 지정
gh pr create --reviewer username1,username2

# 이미 생성된 PR에 리뷰어 추가
gh pr edit 123 --add-reviewer username
```

### PR 상태 확인

```bash
# PR 목록 확인
gh pr list --repo pluxity/pf-frontend

# PR 상세 보기
gh pr view 123 --repo pluxity/pf-frontend

# PR 체크 상태 확인
gh pr checks 123 --repo pluxity/pf-frontend
```

### 머지

```bash
# Squash 머지 (권장)
gh pr merge 123 --repo pluxity/pf-frontend --squash

# 일반 머지
gh pr merge 123 --repo pluxity/pf-frontend --merge

# 리베이스 머지
gh pr merge 123 --repo pluxity/pf-frontend --rebase
```

---

## 관련 스킬 연동

### 코드 리뷰 후 PR

```bash
# 1. 코드 리뷰
/pf-code-review src/components/Button

# 2. 수정 후 PR 생성
/pf-pr feat(ui): Button 접근성 개선
```

### 기능 개발 후 PR

```bash
# 1. 기능 개발
/pf-feature #123 사용자 프로필

# 2. PR 생성
/pf-pr feat: 사용자 프로필 페이지 추가
```

### 핫픽스 후 PR

```bash
# 1. 핫픽스
/pf-hotfix #456 로그인 크래시

# 2. PR 생성
/pf-pr fix: 로그인 페이지 크래시 수정
```

---

## PR 전 체크리스트

```bash
# 1. 타입 체크
pnpm tsc --noEmit

# 2. 린트
pnpm lint

# 3. 빌드
pnpm build

# 4. 테스트 (있는 경우)
pnpm test
```

---

## 유용한 명령어

```bash
# 내 PR 목록
gh pr list --repo pluxity/pf-frontend --author @me

# PR 댓글 추가
gh pr comment 123 --repo pluxity/pf-frontend --body "리뷰 반영 완료했습니다"

# PR 닫기
gh pr close 123 --repo pluxity/pf-frontend

# Draft PR 생성
gh pr create --draft

# Draft -> Ready
gh pr ready 123

# PR diff 보기
gh pr diff 123 --repo pluxity/pf-frontend
```

---

## CI/CD 연동

PR 생성 시 자동으로 실행되는 체크:

- TypeScript 타입 체크
- ESLint
- Build 테스트

main 브랜치 머지 시:

- Staging 서버 자동 배포 (deploy-staging 워크플로우)

---

## 주의사항

- **[필수] PR은 항상 Draft로 생성** (`--draft` 플래그 사용)
- 리뷰 준비 완료 시 `gh pr ready` 로 변경
- PR 제목은 커밋 컨벤션을 따름
- 큰 변경은 여러 PR로 나누기
- 리뷰어 피드백은 적극적으로 반영
- 머지 전 최신 main과 rebase/merge 권장
- **[필수] 커밋 메시지에 `Co-Authored-By` 절대 포함 금지 - 반드시 확인할 것**
