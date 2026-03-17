---
description: "feature branch + worktree에서 작업 후 현재 브랜치로 merge까지 자동 수행"
argument-hint: "\"기능 설명\" | --branch name \"설명\" | --abort [branch]"
---

# Dev Skill — Feature Branch Workflow Automation

feature branch를 생성하고 worktree에서 작업한 뒤, 현재 브랜치로 merge하고 정리까지 자동으로 수행한다.

## 사용법

```
/dev "간단한 기능 설명"
/dev --branch custom-name "기능 설명"
/dev --abort [branch-name]
```

## 인자 처리

`$ARGUMENTS`에서 다음을 추출한다:

1. **기능 설명** (필수, `--abort` 제외): 따옴표로 감싼 문자열. 구현할 내용을 간결하게 기술
2. **--branch** (선택): 브랜치 이름을 직접 지정. prefix 감지를 건너뛰고 지정된 이름을 그대로 사용한다 (예: `--branch hotfix/urgent` → 브랜치명 `hotfix/urgent`)
3. **--abort** (선택): 진행 중인 dev 워크플로우를 중단하고 worktree 정리

### `--abort` 처리

```bash
# 1. branch-name이 지정된 경우: 해당 브랜치의 worktree를 찾는다
# 2. branch-name이 없는 경우: worktree 목록을 출력하고 사용자에게 재실행을 안내한다
git worktree list
```

branch-name이 없을 때의 출력:
```
현재 등록된 worktree 목록:
{git worktree list 결과}

정리할 브랜치를 지정하여 다시 실행하세요:
  /dev --abort feat/my-feature
```

branch-name이 지정된 경우:
```bash
# merge되지 않은 커밋이 있는지 확인
git log "$BASE_BRANCH".."$BRANCH_NAME" --oneline

# 커밋이 있으면 경고
```

merge되지 않은 커밋이 있을 때의 확인 메시지:
```
[WARNING] 이 브랜치에 merge되지 않은 커밋이 {N}개 있습니다:
{커밋 목록}

이 커밋들은 삭제 후 복구할 수 없습니다. 진행하시겠습니까?
```
**→ `AskUserQuestion`으로 확인을 요청하고, 사용자 응답을 기다린다. 응답 전까지 삭제를 진행하지 않는다.**

사용자 확인 후:
```bash
WORKTREE_DIR=$(echo "$BRANCH_NAME" | tr '/' '-')
WORKTREE_PATH="../${PROJECT_NAME}-${WORKTREE_DIR}"

git worktree remove --force "$WORKTREE_PATH"

# 안전 삭제 시도 → 실패 시 사용자 확인 후 강제 삭제
git branch -d "$BRANCH_NAME" || git branch -D "$BRANCH_NAME"  # -D는 위 확인 후에만
```

### 브랜치 이름 자동 생성

기능 설명에서 **변경 유형을 감지**하여 prefix를 결정한다:

| 키워드 감지 | prefix | 예시 |
|-------------|--------|------|
| "수정", "fix", "bug", "버그", "오류", "에러" | `fix/` | `fix/pty-path-bug` |
| "리팩토링", "refactor", "정리", "개선" | `refactor/` | `refactor/mcp-server` |
| "문서", "docs", "README", "주석" | `docs/` | `docs/update-readme` |
| 그 외 (기본값) | `feat/` | `feat/add-dashboard` |

slug 생성 규칙:
- 한글이면 영문으로 의역 (예: "PTY 버그 수정" → `fix/pty-bug`)
- 공백/특수문자는 하이픈으로 치환
- 최대 30자, 소문자

### Worktree 경로 생성

브랜치명의 `/`는 worktree 경로에서 `-`로 치환한다:
```bash
WORKTREE_DIR=$(echo "$BRANCH_NAME" | tr '/' '-')
WORKTREE_PATH="../${PROJECT_NAME}-${WORKTREE_DIR}"
# 예: feat/add-dashboard → ../oh-my-til-feat-add-dashboard
```

## 경로 규칙 (중요)

Claude Code의 Bash 도구는 호출 간에 셸 상태(cd 포함)가 유지되지 않는다. 따라서:

- **모든 bash 명령에 절대 경로를 사용한다**
- worktree 작업 시: `$WORKTREE_PATH`의 절대 경로를 매 명령에 prefix로 붙인다
- 파일 편집(Read/Edit 도구) 시: `$WORKTREE_PATH` 기준의 절대 경로로 파일을 참조한다
- Phase 5 이후: `$PROJECT_ROOT`의 절대 경로를 사용한다
- 변수 참조 대신 실제 절대 경로 문자열을 사용한다 (예: `/Users/.../oh-my-til-feat-xxx/src/main.ts`)

## 사전 검증

아래 조건을 모두 확인한다. 하나라도 실패하면 중단하고 사용자에게 안내한다.

1. **working tree가 clean한지 확인**
   ```bash
   git status --porcelain
   ```
   uncommitted changes가 있으면 중단

2. **현재 브랜치 확인**
   ```bash
   git branch --show-current
   ```
   - 빈 문자열(detached HEAD)이면 중단: "detached HEAD 상태에서는 실행할 수 없습니다"
   - `main` 브랜치이면 중단: "main에서는 직접 작업하지 않습니다. release 또는 다른 브랜치에서 실행하세요"
   - `release/*` 브랜치이면 정보 출력: "[INFO] release 브랜치({이름})에서 실행합니다. merge 대상: {이름}"
   - 현재 브랜치를 `BASE_BRANCH`로 저장 (merge 대상)

3. **프로젝트 루트 저장**
   ```bash
   PROJECT_ROOT=$(git rev-parse --show-toplevel)  # 절대 경로
   PROJECT_NAME=$(basename "$PROJECT_ROOT")
   ```

4. **기능 설명이 비어있으면 중단**

## 확인 요청 원칙

**사용자 확인이 필요한 단계에서는 반드시 사용자 응답을 기다린 후 다음 단계로 진행한다.** 확인 메시지를 출력한 뒤 자동으로 다음 Phase로 넘어가지 않는다. `AskUserQuestion` 도구를 사용하여 선택지를 제시하고, 사용자가 응답한 후에만 진행한다.

## 절차

### Phase 1: 브랜치 생성 안내

자동 생성된 브랜치 이름을 출력하고 바로 진행한다:

```
[Phase 1/8] 브랜치 생성
생성할 브랜치: {BRANCH_NAME}
worktree 경로: {WORKTREE_PATH}
base 브랜치: {BASE_BRANCH}
```

별도 확인 없이 Phase 2로 진행한다. 브랜치 이름을 직접 지정하려면 `--branch` 옵션을 사용한다.

### Phase 2: Worktree 생성

```
[Phase 2/8] worktree 생성 중...
```

```bash
# 경로 충돌 확인
```

**경로가 이미 존재하는 경우 — 세 가지 분기:**

(a) `git worktree list`에 해당 경로가 등록되어 있으면:
```
기존 worktree가 발견되었습니다: {경로}
재사용하시겠습니까? (재사용 / 삭제 후 재생성)
```
**→ `AskUserQuestion`으로 선택지를 제시하고, 사용자 응답을 기다린다.**

(b) `git worktree list`에 없지만 디렉토리가 존재하면 (stale worktree):
```bash
git worktree prune  # stale 항목 정리
rm -rf "$WORKTREE_PATH"  # 사용자 확인 후
```

(c) 동일 브랜치가 다른 worktree에 이미 checkout되어 있으면:
```
[ERROR] 브랜치 {BRANCH_NAME}이 이미 다른 worktree에서 사용 중입니다: {경로}
다른 브랜치 이름을 지정하세요: /dev --branch other-name "설명"
```

**정상 생성:**
```bash
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
```

```
worktree 생성 완료: {WORKTREE_PATH}
```

### Phase 3: 환경 설정 + 구현

```
[Phase 3/8] 의존성 설치 + 구현 작업...
```

1. **의존성 설치**
   ```bash
   cd "$WORKTREE_PATH" && npm install
   ```

2. **네이티브 모듈 재빌드** (선택적)
   ```bash
   cd "$WORKTREE_PATH" && npm run rebuild-pty
   ```
   **참고**: `rebuild-pty`는 `ELECTRON_VERSION` 환경변수가 필요하다. 미설정 시 실패하지만 이는 **예상된 실패**이다. 단위 테스트(`npm test`)와 빌드(`npm run build`)는 네이티브 모듈 없이도 동작하므로, 실패 시 아래 경고만 출력하고 구현을 계속 진행한다:
   ```
   [WARN] rebuild-pty 실패 (ELECTRON_VERSION 미설정). 단위 테스트/빌드에는 영향 없음.
   ```

3. **기능 설명을 기반으로 구현 작업 수행**
   - `$WORKTREE_PATH` 내의 파일을 **절대 경로**로 참조하여 탐색/수정
   - **CLAUDE.md의 프로젝트 규칙을 준수하며 구현한다** (코어/플랫폼 레이어 분리, 코드 스타일 등)
   - 구현 완료 후 관련 테스트도 작성/수정
   - 구조적 변경(새 파일 추가, 설정 변경, 스킬 추가/삭제)이 있으면 **문서 동기화** 체크:
     - `CLAUDE.md` 구조 섹션
     - `README.md`, `README.ko.md` (해당 시)

### Phase 4: 검증

```
[Phase 4/8] 테스트 + 빌드 검증 중... (시도 {N}/3)
```

worktree 디렉토리에서 실행:

```bash
cd "$WORKTREE_PATH" && npm test && npm run build
```

**실패 시 재시도 규칙:**
- 재시도 카운터는 Phase 4 진입 시 0에서 시작하여, `npm test && npm run build` 실행이 실패할 때마다 1 증가한다
- **1~3회**: 에러를 분석하고 코드를 수정한 뒤 재검증. 매 시도마다 출력:
  ```
  [Phase 4/8] 검증 실패. 수정 후 재시도... (시도 {N}/3)
  ```
- **3회 초과**: 작업을 중단하고 worktree는 유지한 채 사용자에게 보고:
  ```
  [FAIL] 검증 실패 (3회 시도 초과)
  경로: {WORKTREE_PATH}
  브랜치: {BRANCH_NAME}
  마지막 에러: {에러 요약}

  수동으로 수정 후 worktree에서 직접 작업을 이어가거나,
  /dev --abort {BRANCH_NAME} 으로 정리할 수 있습니다.
  ```
  **이 경우 Phase 5 이후로 진행하지 않는다.**

**자동 검증 통과 후 — 실제 플러그인 테스트 필요 여부 판단:**

`git diff --name-only` 결과에서 변경된 파일 경로를 확인하여, 아래 패턴에 해당하는 파일이 하나라도 포함되면 사용자에게 실제 플러그인 테스트를 요청한다:

| 패턴 | 이유 |
|------|------|
| `src/obsidian/main.ts` | 플러그인 라이프사이클 |
| `src/obsidian/settings.ts` | 설정 탭 UI |
| `src/obsidian/terminal/**` | 터미널 렌더링/PTY |
| `src/mcp/server.ts`, `src/mcp/tools.ts` | MCP 서버 런타임 |
| `src/obsidian/dashboard/**` | 대시보드 UI |
| `vault-assets/skills/**` | 스킬 프롬프트 (Claude Code 동작) |
| `vault-assets/rules/**` | 규칙 프롬프트 |
| `styles.css` | UI 스타일 |

해당 파일이 있으면:

1. **vault 배포를 먼저 실행한다** (사용자가 Obsidian에서 테스트할 수 있도록):
   - 사용자에게 vault 경로를 확인한 뒤 `npm run deploy -- --refresh-skills <vault-path>` 실행
   - 또는 `/update-plugin <vault-path>` 스킬 사용
2. 배포 완료 후 사용자에게 안내:
```
[Phase 4/8] 자동 테스트 통과. 런타임 테스트가 필요한 변경이 감지되었습니다.

변경 파일:
- {런타임 관련 파일 목록}

vault에 배포 완료. Obsidian에서 플러그인을 리로드한 뒤 해당 기능을 직접 확인해주세요.
확인이 완료되면 계속 진행합니다.
```

**→ `AskUserQuestion`으로 "테스트 완료 / 문제 발견" 선택지를 제시하고, 사용자 응답을 기다린다.**

- "테스트 완료": Phase 5로 진행
- "문제 발견": 사용자가 설명한 문제를 수정하고 Phase 4를 다시 실행 (재시도 카운터는 리셋)

해당 파일이 없으면 (순수 로직/테스트/문서 변경만): 자동으로 Phase 5로 진행한다.

### Phase 5: 커밋

```
[Phase 5/8] 변경사항 커밋 중...
```

검증 통과 후:

1. 변경된 파일을 확인하고 적절한 커밋 메시지를 작성
2. 커밋 메시지는 conventional commit 스타일 + 이모지 prefix:
   - `✨ feat:` 새 기능
   - `🐛 fix:` 버그 수정
   - `♻️ refactor:` 리팩토링
   - `✅ test:` 테스트
   - `📝 docs:` 문서
3. worktree 디렉토리에서 커밋 실행
4. pre-commit hook 실패 시: hook 에러를 분석하고 수정 후 새 커밋 시도 (amend 아님)

### Phase 6: Pre-Merge 검증

```
[Phase 6/8] merge 전 검증 중...
```

merge 전에 BASE_BRANCH의 상태를 확인한다:

```bash
# 1. BASE_BRANCH가 여전히 현재 브랜치인지 확인
CURRENT=$(git -C "$PROJECT_ROOT" branch --show-current)
# CURRENT != BASE_BRANCH이면 중단 (worktree 유지)
```

```bash
# 2. BASE_BRANCH가 clean한지 확인
git -C "$PROJECT_ROOT" status --porcelain
# uncommitted changes가 있으면 중단 (worktree 유지)
```

```bash
# 3. remote 동기화 상태 확인
git -C "$PROJECT_ROOT" fetch origin "$BASE_BRANCH" 2>/dev/null
git -C "$PROJECT_ROOT" status -sb
```

remote에서 새 커밋이 있으면 (`behind N`):
```
[WARN] {BASE_BRANCH}가 원격보다 {N}개 커밋 뒤처져 있습니다.
먼저 pull하시겠습니까? (pull 후 merge / 그대로 merge / 중단)
```
**→ `AskUserQuestion`으로 선택지를 제시하고, 사용자 응답을 기다린다. 응답 전까지 merge로 진행하지 않는다.**

모든 검증 통과:
```
[OK] Pre-merge 검증 통과. BASE_BRANCH: {BASE_BRANCH} (clean, up-to-date)
```

### Phase 7: Merge

```
[Phase 7/8] {BRANCH_NAME} → {BASE_BRANCH} merge 중...
```

```bash
# merge (fast-forward 우선, 불가 시 merge commit)
git -C "$PROJECT_ROOT" merge "$BRANCH_NAME"
```

**merge conflict 발생 시 — 자동 해결 범위:**
- **자동 해결 시도**: 소스 코드(.ts, .js 등)의 명확한 conflict (한쪽만 변경한 경우)
- **즉시 사용자 위임**: `package-lock.json`, `*.lock`, 바이너리 파일, 또는 양쪽이 같은 라인을 다르게 수정한 경우
- 자동 해결 실패 시:
  ```
  [FAIL] merge conflict를 자동으로 해결할 수 없습니다.
  conflict 파일: {목록}

  worktree({WORKTREE_PATH})는 유지됩니다.
  수동으로 conflict를 해결한 뒤 merge를 완료하세요.
  ```

**merge 성공 후 post-merge 검증:**

```bash
cd "$PROJECT_ROOT" && npm test && npm run build
```

- **성공**: Phase 8(정리)로 진행
- **실패**: BASE_BRANCH에서 추가 수정 → 커밋 → 재검증 (최대 3회)
  ```
  [WARN] Post-merge 검증 실패. 수정 후 재시도... (시도 {N}/3)
  ```
- **3회 초과 실패**:
  ```
  [FAIL] Post-merge 검증 실패 (3회 시도 초과)
  {BASE_BRANCH}에 merge는 완료되었으나 테스트/빌드가 실패합니다.

  복구 옵션:
  1. 수동으로 수정 후 커밋
  2. merge 되돌리기: git revert -m 1 HEAD
  3. merge 취소 (주의: 이후 커밋도 제거됨): git reset --hard HEAD~1

  worktree({WORKTREE_PATH})는 유지됩니다.
  ```
  **이 경우 Phase 8로 진행하지 않는다.**

### Phase 8: 정리

```
[Phase 8/8] worktree + 브랜치 정리 중...
```

모든 검증 통과 후 자동 정리:

```bash
# worktree 제거 (node_modules 등 untracked 파일 때문에 --force 필요)
git worktree remove --force "$WORKTREE_PATH"

# 안전 삭제 시도
git branch -d "$BRANCH_NAME"
```

`git branch -d` 실패 시 (not fully merged):
```
[WARN] 브랜치 {BRANCH_NAME}이 완전히 merge되지 않았다는 경고가 발생했습니다.
강제 삭제하시겠습니까? (삭제 / 유지)
```
**→ `AskUserQuestion`으로 선택지를 제시하고, 사용자 응답을 기다린다.**

사용자 확인 후 `-D`로 강제 삭제하거나 브랜치를 유지.

완료 메시지:
```
[DONE] 작업 완료!
{BRANCH_NAME} → {BASE_BRANCH} merge 완료
커밋: {커밋 해시} {커밋 메시지}
변경 파일: {N}개
테스트: 통과
빌드: 통과
worktree + 브랜치 정리 완료
```

## 오류 처리 요약

| 상황 | 대응 | worktree |
|------|------|----------|
| worktree 경로에 기존 worktree 존재 | 재사용/삭제 선택 요청 | 유지 |
| worktree 경로에 stale 디렉토리 존재 | `git worktree prune` 후 정리 | 정리 후 재생성 |
| 동일 브랜치가 다른 worktree에 checkout | 다른 이름 안내 후 중단 | - |
| npm install 실패 | 에러 로그 출력 후 중단 | 유지 |
| rebuild-pty 실패 | 예상된 실패. 경고 출력, 계속 진행 | 유지 |
| 테스트/빌드 실패 (3회 초과) | 상태 보고 후 중단 | 유지 |
| pre-commit hook 실패 | hook 에러 수정 후 새 커밋 시도 | 유지 |
| pre-merge: 브랜치 변경 감지 | 상황 설명 후 중단 | 유지 |
| pre-merge: remote에 새 커밋 | pull/계속/중단 선택 요청 | 유지 |
| merge conflict (자동 해결 실패) | 사용자 안내 후 중단 | 유지 |
| post-merge 테스트 실패 (3회 초과) | 복구 옵션 3가지 안내 후 중단 | 유지 |
| branch -d 실패 | 사용자 확인 후 -D 또는 유지 | 제거됨 |

**원칙**: 실패 시 worktree를 삭제하지 않는다. 사용자가 수동으로 이어서 작업하거나 `--abort`로 정리할 수 있도록 한다.

## 주의사항

- 이 스킬은 프로젝트 루트 디렉토리에서 실행해야 한다 (`package.json`이 있는 위치)
- `main` 브랜치에서는 실행할 수 없다 (프로젝트의 "main 직접 수정 금지" 규칙)
- detached HEAD 상태에서는 실행할 수 없다 (merge 대상 브랜치 불명확)
- worktree 내부에서는 별도의 `node_modules`가 필요하므로 `npm install`을 실행한다
- merge는 현재 브랜치(실행 시점의 브랜치)로 수행된다
- `--abort`는 merge되지 않은 커밋이 있으면 경고하고 확인을 요청한다
- 모든 bash 명령은 절대 경로를 사용한다 (Claude Code의 셸 상태 비유지 특성)
