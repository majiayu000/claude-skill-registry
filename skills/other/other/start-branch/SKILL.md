---
name: start-branch
version: 4.0.0
description: 새 작업 브랜치 생성
user-invocable: true
---

# Start-Branch 스킬

새로운 작업 브랜치를 시작합니다.

**지원하는 작업 타입**: feat, fix, refactor, chore

---

## 실행 단계

### 1. 사전 확인

```bash
git branch --show-current
git status --short
```

**IF** 커밋되지 않은 변경사항 존재:
→ "/commit 먼저 실행하세요" 안내 후 종료

### 2. 현재 브랜치 확인 및 분기 처리

**IF** feature 브랜치:
→ 서브 브랜치 vs 새 작업 선택

**IF** main:
→ develop으로 checkout

**IF** develop:
→ 바로 브랜치 정보 입력으로

### 3. 작업 타입 선택

**AskUserQuestion 도구로 타입 선택**:

| 옵션 | 설명 |
|------|------|
| feat | 새 기능 |
| fix | 버그 수정 |
| refactor | 리팩토링 |
| chore | 설정/도구 |

→ 선택된 타입을 `$TYPE` 변수로 사용

### 4. 브랜치 설명 입력

**대화로 직접 질문**:

"브랜치 설명을 입력해주세요. (kebab-case, 예: header-component, fix-login-bug)"

→ 사용자 입력을 `$TITLE` 변수로 사용

### 5. 워크트리 사용 여부 확인

**AskUserQuestion 도구로 확인**:

| 옵션 | 설명 |
|------|------|
| 일반 브랜치 | `git checkout -b`로 생성, 현재 디렉토리에서 작업 |
| 워크트리로 분리 | `/worktree` 스킬 호출, 병렬 작업 가능 |

**워크트리 선택 시**:
→ `/worktree` 스킬 참조하여 실행
→ 워크트리 생성 후 **자동으로 해당 디렉토리로 이동** (`cd` 실행)
→ 이후 단계는 워크트리 내에서 진행

**일반 브랜치 선택 시**:
→ 아래 6단계로 진행

### 6. 새 작업 브랜치 생성

**브랜치명 생성** (스크립트 사용):

```bash
# 브랜치명 생성
BRANCH_NAME=$(~/.claude/scripts/branch-name.sh "$TYPE" "$TITLE")
# 예: feat/header-component

# 브랜치 생성
git checkout -b "$BRANCH_NAME"
```

**생성 예시**:
- `feat` + `header component` → `feat/header-component`
- `fix` + `button hover` → `fix/button-hover`
- `refactor` + `auth module` → `refactor/auth-module`

### 7. 워크트리 자동 이동 (워크트리 선택 시)

**IF** 워크트리로 분리 선택:

```bash
cd {워크트리 경로}
```

예시:
```bash
cd .worktrees/header-component
```

→ 이후 모든 작업은 워크트리 디렉토리에서 수행됨

### 8. 최종 확인 및 요약

**일반 브랜치 선택 시**:
```
✅ 새 작업 시작 완료!

새 작업:
- 브랜치: feat/header-component

다음 단계:
1. 코드 작성
2. `/commit`으로 변경사항 커밋
3. `/merge`로 병합 또는 `/start-branch`로 다음 작업
```

**워크트리 선택 시**:
```
✅ 새 작업 시작 완료!

새 작업:
- 브랜치: feat/header-component
- 워크트리: .worktrees/header-component/

📂 워크트리로 이동 완료 (현재 위치: .worktrees/header-component/)

다음 단계:
1. 코드 작성
2. `/commit`으로 변경사항 커밋
3. `/merge`로 병합 또는 `/start-branch`로 다음 작업
```

---

## 엣지 케이스 처리

### Case 1: 커밋되지 않은 변경사항
→ "/commit 먼저 실행하세요"

### Case 2: 작업 브랜치에서 실행
→ 서브 브랜치 vs 새 작업 선택

### Case 3: 동일한 브랜치명 존재
→ 전환/삭제/다른이름 선택
