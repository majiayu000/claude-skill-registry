---
name: merge
version: 3.2.0
description: feature 브랜치를 main에 squash merge (워크트리 지원)
user-invocable: true
---

# Merge 스킬

현재 feature 브랜치를 main 브랜치에 squash merge합니다.
워크트리 환경에서도 메인 레포를 통해 정상 동작합니다.

> **참고**: develop 브랜치가 존재하면 develop을, 없으면 main을 머지 타겟으로 사용합니다.

## 실행 단계

### 1. 환경 감지

```bash
# 워크트리 여부 확인
WORKTREE_COUNT=$(git worktree list | wc -l)
PROJECT_ROOT=$(git worktree list --porcelain | head -1 | cut -d' ' -f2)
CURRENT_DIR=$(pwd)

# 워크트리인지 판별
if [ "$WORKTREE_COUNT" -gt 1 ] && [ "$PROJECT_ROOT" != "$CURRENT_DIR" ]; then
  IS_WORKTREE=true
else
  IS_WORKTREE=false
fi
```

**워크트리 감지 시**:
→ 메인 레포 경로(`PROJECT_ROOT`)를 사용하여 `git -C "$PROJECT_ROOT"` 형태로 명령 실행

### 2. 사전 확인

```bash
# 현재 브랜치 확인
git branch --show-current

# 변경사항 확인 (커밋되지 않은 변경사항 체크)
git status --short
```

**체크리스트**:
- [ ] 현재 브랜치가 feature/* 또는 fix/* 등 작업 브랜치인가?
- [ ] 커밋되지 않은 변경사항이 없는가?

**분기 처리**:
- **IF** 현재 브랜치가 `main` 또는 `develop`:
  → "feature 브랜치에서 실행해주세요. 현재 브랜치: {브랜치명}" 안내 후 종료

- **IF** 커밋되지 않은 변경사항 존재:
  → "먼저 `/commit` 스킬을 실행하여 변경사항을 커밋해주세요." 안내 후 종료

### 3. 브랜치 정보 분석

**Step 1: 현재 브랜치명 확인**

```bash
BRANCH=$(git branch --show-current)
# 예: feat/grt-42/button-disabled
```

**Step 2: 브랜치명에서 정보 추출**

```bash
# 예: feat/button-disabled
TYPE=$(echo "$BRANCH" | cut -d'/' -f1)
DESCRIPTION=$(echo "$BRANCH" | cut -d'/' -f2-)
```

**추출 정보**:
- 타입: 브랜치 prefix에서 추출 (`feat`, `fix`, `refactor`, `chore`, `docs`, `build`)
- 설명: 브랜치명의 두 번째 세그먼트 (예: `button-disabled`)

**타입 매핑** (병합 커밋용 대문자):
| 브랜치 prefix | 커밋 prefix |
|--------------|-------------|
| `feat/`      | `FEAT`      |
| `fix/`       | `FIX`       |
| `refactor/`  | `REFACTOR`  |
| `chore/`     | `CHORE`     |
| `docs/`      | `DOCS`      |
| `build/`     | `BUILD`     |

### 4. 병합 커밋 메시지 생성

**머지 타겟 결정**:
```bash
# develop 브랜치가 있으면 develop, 없으면 main
if git show-ref --verify --quiet refs/heads/develop; then
  TARGET="develop"
else
  TARGET="main"
fi
```

**커밋 로그 분석**:
```bash
# 타겟 브랜치와의 차이 확인
git log $TARGET..HEAD --oneline
```

**커밋 메시지 형식**:

```
[TYPE] 기능 요약
```

**예시**:
- `[FEAT] Button disabled 상태 추가`
- `[FIX] 로그인 유효성 검증 버그 수정`
- `[REFACTOR] 네트워크 레이어 구조 개선`

**기능 요약 생성 방법**:
1. 커밋 로그에서 주요 변경사항 파악
2. 50자 이내 한글로 요약

### 5. Squash Merge 실행

#### 일반 환경 (워크트리가 아닌 경우)

```bash
# 현재 브랜치명 저장
FEATURE_BRANCH=$(git branch --show-current)

# 타겟 브랜치로 전환
git checkout $TARGET

# 타겟 브랜치를 최신 상태로 동기화
git pull origin $TARGET

# feature 브랜치를 squash merge
git merge --squash $FEATURE_BRANCH

# 병합 커밋 생성
git commit -m "[TYPE] 기능 요약"

# feature 브랜치 삭제
git branch -d $FEATURE_BRANCH
```

#### 워크트리 환경

```bash
# 현재 브랜치명 저장
FEATURE_BRANCH=$(git branch --show-current)

# 메인 레포에서 타겟 브랜치 최신화
git -C "$PROJECT_ROOT" fetch origin
git -C "$PROJECT_ROOT" checkout $TARGET
git -C "$PROJECT_ROOT" pull origin $TARGET

# 메인 레포에서 squash merge 실행
git -C "$PROJECT_ROOT" merge --squash $FEATURE_BRANCH

# 충돌 발생 시: 메인 레포에서 충돌 해결 후 스테이징
# git -C "$PROJECT_ROOT" add <충돌파일>

# 메인 레포에서 병합 커밋 생성
git -C "$PROJECT_ROOT" commit -m "[TYPE] 기능 요약"

# feature 브랜치 삭제는 워크트리 제거 후 수동으로
# (워크트리에서 사용 중인 브랜치는 삭제 불가)
```

**체크리스트**:
- [ ] 타겟 브랜치 최신화 성공
- [ ] Squash merge 성공
- [ ] 병합 커밋 생성 성공
- [ ] Feature 브랜치 삭제 성공 (워크트리 환경에서는 보류)

**IF** 타겟 브랜치 pull 중 충돌:
→ 오류 메시지 출력 후 안내:
```
타겟 브랜치 동기화 중 충돌이 발생했습니다.

해결 방법:
1. git checkout {feature-branch}
2. git rebase {target-branch}
3. 충돌 해결 후 다시 /merge 실행

또는 수동으로 병합을 진행해주세요.
```

### 6. Push 여부 확인

**사용자에게 질문**:
```
병합이 완료되었습니다.

타겟 브랜치를 원격에 push할까요?

1. 예, push합니다
2. 아니오, 나중에 수동으로 push합니다

선택:
```

**IF** "예" 선택:

일반 환경:
```bash
git push origin $TARGET
```

워크트리 환경:
```bash
git -C "$PROJECT_ROOT" push origin $TARGET
```

### 7. 최종 확인 및 요약

**사용자에게 보고**:

```
병합 완료!

병합 정보:
- 브랜치: {feature-branch} → {target-branch}
- 커밋: [TYPE] 기능 요약
- Push: {완료/미완료}
- 환경: {일반/워크트리}

다음 단계:
- 새 작업을 시작하려면 `/start-branch`를 실행하세요
- 워크트리 환경: 워크트리 제거 후 브랜치 삭제 필요
```

## 엣지 케이스 처리

### Case 1: main 또는 develop 브랜치에서 실행
→ "feature 브랜치에서 실행해주세요" 안내 후 종료

### Case 2: 커밋되지 않은 변경사항이 있을 때
→ "/commit 스킬을 먼저 실행하세요" 안내 후 종료

### Case 3: 타겟 브랜치와 충돌 발생
→ 메인 레포에서 충돌 해결 후 스테이징, 커밋 진행

### Case 4: feature 브랜치 삭제 실패 (워크트리)
→ 안내 출력:
```
워크트리에서 사용 중인 브랜치는 삭제할 수 없습니다.
워크트리 제거 후 삭제하세요:
  git worktree remove <worktree-path>
  git branch -d {branch-name}
```

### Case 5: 워크트리에서 메인 레포 작업 디렉토리가 dirty
→ 경고 출력:
```
메인 레포에 커밋되지 않은 변경사항이 있습니다.
메인 레포에서 변경사항을 정리한 후 다시 시도하세요.
경로: {PROJECT_ROOT}
```

## 사용자 상호작용 포인트

### 필수 확인 사항:
1. **Push 여부** - 병합 후 develop을 원격에 push할지

### 자동화 가능:
- 워크트리 환경 감지
- 브랜치명 분석
- 타입 매핑
- Squash merge 실행 (메인 레포 경유)
- 커밋 메시지 생성
