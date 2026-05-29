---
name: _worktree-remove
version: 1.0.0
description: 워크트리 제거 로직 (재사용 스킬)
user-invocable: false
---

# Worktree Remove

기존 Git worktree를 제거하는 내부 로직입니다.

## 입력

- `WORKTREE_PATH`: 제거할 워크트리 경로 (필수)
- `FORCE`: 강제 제거 여부 (기본: false)

## 실행 단계

### 1. 워크트리 목록 조회

```bash
git worktree list
```

### 2. 변경사항 확인

```bash
cd "$WORKTREE_PATH" && git status --porcelain
```

**IF** 변경사항 있을 경우:

**옵션**:
1. `/commit` 스킬로 변경사항 커밋 후 진행 (권장)
2. 강제 제거 (변경사항 삭제)
3. 취소

### 3. 병합 여부 확인

커밋된 변경사항이 있는 경우:

```bash
# 워크트리의 브랜치명 추출
BRANCH_NAME=$(cd "$WORKTREE_PATH" && git branch --show-current)

# 병합 안 된 커밋 확인
git log develop.."$BRANCH_NAME" --oneline
```

**옵션**:
1. `/merge` 스킬로 develop에 병합 후 제거 (권장)
2. 병합 없이 제거 (브랜치만 삭제)
3. 병합 없이 제거 (브랜치 유지)
4. 취소

### 4. 워크트리 제거

```bash
# 일반 제거
git worktree remove "$WORKTREE_PATH"

# 강제 제거 (변경사항 무시)
git worktree remove --force "$WORKTREE_PATH"
```

### 5. 메타데이터 정리

`.worktree/.meta.json`에서 해당 워크트리 정보 제거.

### 6. 디렉토리 정리

```bash
# .worktree 디렉토리가 비었으면 삭제
rmdir .worktree/ 2>/dev/null

# 잘못된 워크트리 참조 정리
git worktree prune
```

### 7. 브랜치 정리

**IF 병합 완료된 경우**:
```bash
git branch -d "$BRANCH_NAME"
```

**IF 병합하지 않은 경우** (강제 삭제 선택 시):
```bash
git branch -D "$BRANCH_NAME"
```

## 출력

| 항목 | 상태 |
|------|------|
| 워크트리 경로 | `{worktree-path}` 제거됨 |
| 변경사항 | 커밋됨 / 삭제됨 / 없음 |
| 병합 | develop에 병합됨 / 병합 안 함 |
| 브랜치 | 삭제됨 / 유지됨 |

## 엣지 케이스

### Case: 현재 워크트리 내에서 제거 시도
→ "먼저 원본 저장소로 이동하세요" 안내

### Case: 중첩 워크트리가 있는 상위 제거
→ 중첩 워크트리 먼저 정리 필요

### Case: 브랜치 삭제 실패
→ 워크트리는 제거됨, 브랜치만 유지
