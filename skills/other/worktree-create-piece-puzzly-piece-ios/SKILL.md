---
name: _worktree-create
version: 1.0.0
description: 워크트리 생성 로직 (재사용 스킬)
user-invocable: false
---

# Worktree Create

새 Git worktree를 생성하는 내부 로직입니다.

## 입력

- `BRANCH_NAME`: 생성할 브랜치명 (필수)
- `BASE_BRANCH`: 베이스 브랜치 (기본: develop)
- `PROJECT_ROOT`: 메인 저장소 루트 (선택)

## 실행 단계

### 1. 사전 확인

```bash
# Git 저장소 여부
git rev-parse --is-inside-work-tree

# 프로젝트 루트 찾기 (워크트리 내부에서도 동작)
PROJECT_ROOT=$(git worktree list --porcelain | head -1 | cut -d' ' -f2)

# 베이스 브랜치 확인 (develop 우선, 없으면 main)
if git ls-remote --heads origin develop | grep -q develop; then
  BASE_BRANCH="develop"
elif git ls-remote --heads origin main | grep -q main; then
  BASE_BRANCH="main"
else
  # 사용자에게 베이스 브랜치 입력받기
fi
```

### 2. .gitignore 확인

```bash
# 프로젝트 루트의 .gitignore 확인
cd "$PROJECT_ROOT"
if ! grep -q "^\.worktree/$" .gitignore 2>/dev/null; then
  echo "" >> .gitignore
  echo "# Git worktrees" >> .gitignore
  echo ".worktree/" >> .gitignore
fi
```

### 3. 브랜치 존재 여부 확인

```bash
# 기존 브랜치 존재 여부
if git show-ref --verify "refs/heads/$BRANCH_NAME" 2>/dev/null; then
  # 기존 브랜치로 워크트리 생성할지 확인
  IS_EXISTING_BRANCH=true
else
  IS_EXISTING_BRANCH=false
fi
```

### 4. 워크트리 경로 계산

```bash
WORKTREE_PATH=$(~/.claude/scripts/worktree-path.sh "$BRANCH_NAME")
# 예: .worktree/feat-grt-60-header-component
```

### 5. 워크트리 생성

```bash
# 디렉토리 생성
mkdir -p "$PROJECT_ROOT/.worktree"

# 최신 베이스 브랜치 fetch
git fetch origin "$BASE_BRANCH"

# 워크트리 생성
if [ "$IS_EXISTING_BRANCH" = true ]; then
  # 기존 브랜치
  git worktree add "$PROJECT_ROOT/$WORKTREE_PATH" "$BRANCH_NAME"
else
  # 새 브랜치
  git worktree add -b "$BRANCH_NAME" "$PROJECT_ROOT/$WORKTREE_PATH" "origin/$BASE_BRANCH"
fi
```

### 6. 메타데이터 기록

`.worktree/.meta.json`에 워크트리 정보 기록:

```json
{
  "worktrees": {
    "{branch-path}": {
      "branch": "{branch-name}",
      "baseBranch": "{base-branch}",
      "createdAt": "{ISO timestamp}",
      "parentWorktree": null
    }
  }
}
```

### 7. 프로젝트별 훅 실행

```bash
HOOK_SCRIPT="$PROJECT_ROOT/.claude/scripts/worktree-setup.sh"

if [ -f "$HOOK_SCRIPT" ]; then
  bash "$HOOK_SCRIPT" "$WORKTREE_PATH"
fi
```

## 출력

| 항목 | 값 |
|------|-----|
| 브랜치 | `{branch-name}` |
| 베이스 | `{base-branch}` |
| 경로 | `.worktree/{branch-path}/` |
| 훅 실행 | ✅ 실행됨 / ⚠️ 훅 없음 |

## 엣지 케이스

### Case: 브랜치 이미 존재
→ 기존 브랜치로 워크트리 생성할지 확인

### Case: 경로 충돌
→ 기존 워크트리 사용/제거/다른이름 선택

### Case: develop 브랜치 없음
→ main 사용 또는 사용자 입력
