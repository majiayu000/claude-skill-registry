---
name: worktree
version: 3.0.0
description: Git worktree 생성, 제거, 목록 확인
user-invocable: true
---

# Worktree 스킬

Git worktree를 관리하여 동일 저장소에서 여러 브랜치를 동시에 작업할 수 있는 환경을 구성합니다.

## 워크트리 경로 컨벤션

```
{project-root}/.worktree/{branch-path}/
```

**예시**:
```
greet-design-system/
├── .worktree/
│   ├── feat-grt-63-toast/     # feat/grt-63/toast 브랜치
│   ├── fix-urgent-bug/        # fix/urgent-bug 브랜치
│   └── .meta.json             # 워크트리 메타데이터
├── .gitignore                 # .worktree/ 포함
└── src/
```

---

## 실행 단계

### 0. 작업 선택

스킬 시작 시 AskUserQuestion으로 작업을 선택받습니다:

**옵션**:
1. **생성** - 새 워크트리 생성
2. **제거** - 기존 워크트리 제거
3. **목록** - 현재 워크트리 목록 확인

---

## 생성 (Create)

→ **_worktree-create** 스킬 참조하여 실행

### 입력 수집

AskUserQuestion으로 사용자에게 새 브랜치명을 입력받습니다.

**옵션 예시**:
- feat/GRT-XX/description
- fix/bug-description
- 직접 입력

### 경로 계산

```bash
WORKTREE_PATH=$(~/.claude/scripts/worktree-path.sh "$BRANCH_NAME")
```

### 자동 디렉토리 이동

**IF** 메인 저장소에서 워크트리 생성 시:
→ 생성된 워크트리 디렉토리로 **자동 이동** (`cd` 실행)

```bash
cd "$WORKTREE_PATH"
```

```
📍 워크트리로 이동했습니다: .worktree/{branch-path}/
```

**ELSE** 서브 워크트리(중첩) 생성 시:
→ 이동하지 않고 **경로만 안내**

---

## 제거 (Remove)

→ **_worktree-remove** 스킬 참조하여 실행

### 워크트리 선택

현재 워크트리 목록에서 제거할 항목 선택:

```
1. .worktree/feat-grt-63 (feat/grt-63/toast) - clean
2. .worktree/fix-bug (fix/bug) - modified
```

### 완전 정리 워크플로우

1. 변경사항 확인 → `/commit` 제안
2. 병합 여부 확인 → `/merge` 제안
3. 워크트리 제거
4. 브랜치 정리

---

## 목록 (List)

현재 저장소의 모든 워크트리를 표시합니다:

```bash
git worktree list
```

**출력 형식**:
```
## 워크트리 목록

| 경로 | 브랜치 | 상태 |
|------|--------|------|
| (main) | develop | (main worktree) |
| .worktree/feat-a | feat/a | clean |
| .worktree/fix-b | fix/b | modified |
```

---

## 자동 정리 (Hook)

`git merge` 명령 실행 후 PostToolUse hook이 트리거되어 병합된 브랜치의 워크트리를 자동 정리합니다.

**Hook 설정**: `~/.claude/settings.json`의 PostToolUse 참조

---

## 엣지 케이스 처리

### develop 브랜치 없음
→ main 사용 또는 사용자 입력

### 브랜치 이미 존재
→ 기존 브랜치로 워크트리 생성/다른 이름/취소 선택

### 경로 충돌
→ 기존 워크트리 사용/제거/다른이름 선택

### Git 저장소 아님
→ 오류 메시지 출력 후 종료

### 워크트리 없음 (제거/목록 시)
→ 생성 옵션 제안

### 워크트리 내에서 실행
→ 원본 저장소 루트 기준으로 동작

### 현재 워크트리 제거 시도
→ "먼저 원본 저장소로 이동하세요" 안내

---

## 연계 스킬

| 스킬 | 용도 | 실행 위치 |
|------|------|----------|
| `/commit` | 변경사항 원자적 커밋 | 워크트리 경로 |
| `/merge` | feature → develop 병합 | 워크트리 경로 |
| `/start-branch` | 새 작업 브랜치 생성 | 원본 저장소 |

---

## 유용한 명령어 참조

```bash
# 워크트리 목록 확인
git worktree list

# 메인 저장소 루트 찾기
git worktree list --porcelain | head -1 | cut -d' ' -f2

# 워크트리 제거
git worktree remove <path>

# 강제 제거 (변경사항 무시)
git worktree remove --force <path>

# 잘못된 워크트리 참조 정리
git worktree prune
```
