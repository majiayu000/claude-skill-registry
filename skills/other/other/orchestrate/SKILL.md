---
name: orchestrate
description: Leader → Executor → Tester → Review 전체 워크플로우 실행
user-invocable: true
argument: [--new] 기능 설명 (예: "로그인 기능")
---

# /orchestrate

Leader가 직접 스펙을 작성하고 Executor 세션으로 실행합니다. Tester는 Executor가 필요 시 on-demand로 생성합니다.

## 전체 흐름
```
Leader (직접 스펙 작성 → pending/)
  │
  └──send-keys──→ Executor (exec-ears)
                      │
                      ├── 구현 → done/
                      └── Tester pane 생성 (on-demand)
                            │
                        ┌───┤
                        │   ├── 성공 → Leader (완료 알림)
                        │   │            └── review-quick 실행
                        │   └── 실패 → Executor (수정 요청)
                        └───────────────┘ (E ↔ T 반복)
```

## Arguments
- `기능 설명` — 구현할 기능 (필수)
- `--new` — 기존 dual 세션 무시하고 새로 생성 (선택)

## Instructions

### 0. 레포/Worktree/브랜치 선택
사용자에게 대화형으로 작업 환경을 선택하도록 합니다:

**1) 레포 선택**
- 현재 디렉토리가 git 레포인 경우: "현재 레포 사용" 또는 "다른 레포 선택"
- 현재 디렉토리가 git 레포가 아닌 경우: 사용 가능한 레포 목록 표시
  ```bash
  find ~ -maxdepth 3 -name ".git" -type d 2>/dev/null | xargs dirname | sort
  ```

**2) Worktree 선택** (선택된 레포에서)
- 현재 worktree 또는 사용 가능한 worktree 목록 제시
  ```bash
  git worktree list | awk '{print $1}'
  ```

**3) 브랜치 선택**
- 현재 브랜치 유지 또는 다른 브랜치로 변경
- 새 브랜치 생성 옵션 (MMDD/{type}/{name} 형식)
- 브랜치 목록:
  ```bash
  git branch -a | sed 's/^ *//' | grep -v "^*" | head -10
  ```

선택된 경로를 `TARGET_DIR`에 저장합니다.

### 1. 세션 레지스트리 생성
orchestrate 실행마다 **고유 세션 파일**을 생성하여 Leader-Executor-Tester 간 통신을 안정적으로 합니다:

```bash
# 고유 세션 ID 생성 (타임스탬프 기반)
SESSION_ID="orch-$(date +%s)"

# 세션 레지스트리 디렉토리
SESSION_DIR="$HOME/.claude/orchestrate/sessions"
mkdir -p "$SESSION_DIR"

# 세션 파일 생성 (JSON)
SESSION_FILE="$SESSION_DIR/${SESSION_ID}.json"

cat > "$SESSION_FILE" <<EOF
{
  "session_id": "$SESSION_ID",
  "spec_id": "{SPEC-ID}",
  "target_dir": "$TARGET_DIR",
  "status": "leader_active",
  "created_at": "$(date -Iseconds)",
  "leader": {
    "pane_id": "$(tmux display-message -p '#{pane_id}')",
    "window_id": "$(tmux display-message -p '#{window_id}')",
    "pid": "$$"
  },
  "executor": {
    "pane_id": null,
    "status": "pending"
  },
  "tester": {
    "pane_id": null,
    "status": "pending"
  }
}
EOF

# Executor/Tester가 접근할 수 있도록 환경변수로 전달
export ORCHESTRATE_SESSION_ID="$SESSION_ID"
export ORCHESTRATE_SESSION_FILE="$SESSION_FILE"
```

✅ **파일 기반 통신:**
- Executor는 `$ORCHESTRATE_SESSION_FILE`에서 Leader pane ID 읽음
- Tester도 동일하게 Executor pane ID 읽음
- pane 파싱/윈도우명 검색 불필요 (파일에 명시적으로 저장)

### 2. 스펙 작성 (Leader가 직접 수행하는 유일한 코드 관련 작업)
Leader가 EARS 스펙을 작성하여 `~/.claude/specs/{project}/pending/`에 저장합니다. **스펙 작성까지만 Leader의 역할이며, 구현은 반드시 Executor에게 위임합니다.**

**스펙 저장 위치:**
```bash
# TARGET_DIR의 basename을 project 이름으로 사용
PROJECT=$(basename "$TARGET_DIR")
SPEC_DIR="$HOME/.claude/specs/$PROJECT/pending"
mkdir -p "$SPEC_DIR"
# SPEC_FILE="$SPEC_DIR/{SPEC-ID}.md"에 저장
```

**스펙 작성 프로세스:**
- 코드베이스를 탐색 (sub-agent 위임)하여 필요한 컨텍스트 수집 (TARGET_DIR 기준)
- EARS 형식으로 스펙 작성 (Requirements, Scope, Acceptance Criteria)
- `pending/`에 저장

### 3. Executor Pane 생성 및 세션 업데이트
**Leader가 있는 탭(window) 내에서 오른쪽으로 수직 분할하여 Executor pane을 생성합니다:**
```bash
# 세션 파일에서 Leader의 window ID 읽기
LEADER_WINDOW=$(jq -r '.leader.window_id' "$ORCHESTRATE_SESSION_FILE")

# Leader 탭 내에서 오른쪽(50%)으로 수직 분할
# mise run z.ai:claude 실행 (바로 Claude 시작, bypass 옵션 포함)
EXECUTOR_PANE=$(tmux split-window -h -t "$LEADER_WINDOW" -c "$TARGET_DIR" -P -F '#{pane_id}' \
  "cd '$TARGET_DIR' && ORCHESTRATE_SESSION_ID='$ORCHESTRATE_SESSION_ID' ORCHESTRATE_SESSION_FILE='$ORCHESTRATE_SESSION_FILE' mise run z.ai:claude -- --dangerously-skip-permissions")

# 창 크기 조정 (Leader 70%, Executor 30%)
LEADER_PANE=$(jq -r '.leader.pane_id' "$ORCHESTRATE_SESSION_FILE")
tmux resize-pane -t "$LEADER_PANE" -x 140

# 세션 파일 업데이트 (Executor pane ID 저장)
jq ".executor.pane_id = \"$EXECUTOR_PANE\" | .status = \"executor_ready\"" \
  "$ORCHESTRATE_SESSION_FILE" > "${ORCHESTRATE_SESSION_FILE}.tmp" && \
  mv "${ORCHESTRATE_SESSION_FILE}.tmp" "$ORCHESTRATE_SESSION_FILE"
```

**구조:**
```
Leader 탭 (window_id: @4)
├─ Pane 0 (Leader)          │ Pane 1 (Executor)
│ /orchestrate 실행         │ mise run z.ai:claude
│ 70%                       │ 30%
└───────────────────────────┴──────────────────
세션 파일: ~/.claude/orchestrate/sessions/orch-{timestamp}.json
```

**Executor에서 세션 파일 사용:**
```bash
# 세션 파일에서 Leader pane ID 읽기
LEADER_PANE=$(jq -r '.leader.pane_id' "$ORCHESTRATE_SESSION_FILE")

# Leader에게 메시지 전송 (tmux send-keys 올바른 형식)
tmux send-keys -t "$LEADER_PANE" "메시지 내용" C-m
```

⚠️ **주의:**
- `-l` 플래그는 사용하지 않음 (글자별 입력 → 문제 발생)
- `tmux send-keys -t PANE "명령" C-m` 형식 (Enter 대신 C-m 사용)

### 4. Executor에게 명령 전달
생성된 Executor pane에 `/exec-ears` 명령을 전송합니다:
```bash
# Executor pane은 스텝 3에서 반환된 $EXECUTOR_PANE (이미 claude 실행 중)
tmux send-keys -t "$EXECUTOR_PANE" "/exec-ears" C-m
```

**주의:**
- Executor pane은 이미 `mise run z.ai:claude`로 실행 중
- `/exec-ears` 스킬 명령을 실행
- `-l` 플래그 제거 (줄바꿈 문제)
- `tmux send-keys -t PANE "명령" Enter` 형식

**Executor pane 내부에서:**
- 세션 파일 `$ORCHESTRATE_SESSION_FILE`로 Leader pane 참조
- Tester 필요 시 같은 창 내에서 아래쪽으로 분할 (`tmux split-window -v -t "$LEADER_WINDOW"`)
- Tester → Leader 메시지 전송: `tmux send-keys -t $(jq -r '.leader.pane_id' "$ORCHESTRATE_SESSION_FILE")`

### 5. 진행 모니터링
사용자에게 안내합니다:
```
┌─────────────────────────────────────────────────────────┐
│ 📍 Orchestrate 시작                                      │
├─────────────────────────────────────────────────────────┤
│ 레포: {TARGET_DIR}                                      │
│ 브랜치: {BRANCH}                                        │
│ 세션: {SESSION_ID}                                      │
│                                                         │
│ 구조: [Leader Pane (70%) | Executor Pane (30%)]        │
│       [                 Tester (필요시)                 ]
├─────────────────────────────────────────────────────────┤
│ ✅ 스펙 저장: {SPEC_FILE}                              │
│ ✅ Executor pane 생성: {EXECUTOR_PANE}                 │
│ ✅ 세션 파일: {ORCHESTRATE_SESSION_FILE}               │
│ ⏳ /exec-ears 실행 중...                               │
│                                                         │
│ 진행 과정:                                              │
│  1. Executor가 스펙 구현 중 (우측)                      │
│  2. 테스트 필요 시 Tester pane 자동 생성 (아래)        │
│  3. Tester → Executor (E ↔ T 반복)                     │
│  4. 완료 시 Leader pane에 메시지 도착                  │
│  5. /review-quick으로 최종 검증                         │
└─────────────────────────────────────────────────────────┘
```

**조작:**
- `Ctrl+B, {` / `Ctrl+B, }` — Pane 크기 조정
- `Ctrl+B, →` / `Ctrl+B, ↓` — Pane 이동
- Executor pane 클릭 → Executor와 상호작용
- Leader pane 클릭 → 메시지 대기

### 6. 완료 후 검증
Tester가 테스트 성공하면 이 세션에 메시지가 도착합니다.
메시지를 수신하면 다음을 순차 실행합니다:
1. `specs-status`로 완료 확인
2. `git diff`로 변경사항 확인
3. 변경사항이 있으면 `/review-quick`으로 코드 리뷰 실행
4. 리뷰 결과와 함께 사용자에게 최종 보고

## 주의사항

### 구조
```
현재 윈도우  ┌─ Leader (Pane 0, 70%)
  │         │ /orchestrate 실행
  │         │ 스펙 작성
  │         │ (메시지 수신 대기)
  │         │
  └─────────┼─ Executor (Pane 1, 30%)
            │ /exec-ears 실행
            │ 구현 진행
            │
            └─ Tester (Pane 2, 필요시)
              /exec-ears → Tester pane 분할

환경변수 연결:
  Leader → $CLAUDE_LEADER_PANE_ID
         → $CLAUDE_LEADER_WINDOW
         ↑ Executor/Tester가 이용
```

### 규칙
- **CRITICAL: Leader는 절대 스펙을 직접 구현하지 않습니다. 반드시 Executor에게 전달합니다.**
- **같은 탭(윈도우) 내 pane 분할** — Leader (Pane 0, 70%) | Executor (Pane 1, 30%)
- **환경변수로 명시적 전달** — `$CLAUDE_LEADER_PANE_ID`로 Leader pane을 환경변수로 참조 (윈도우명 파싱 불필요)
- **Executor 세션 위치** — 선택된 TARGET_DIR에서 열림
- **Tester 생성** — Executor가 구현 완료 후 현재 윈도우 내에서 아래쪽 분할로 생성
- **메시지 전달** — tmux send-keys로 Executor/Tester → Leader로 직접 송수신
- Executor → Tester 테스트 요청은 executor-mode 규칙에 의해 자동 수행
- Tester ↔ Executor 반복은 tester-mode 규칙에 의해 자동 수행
- Tester → Leader 완료 알림은 tester-mode 규칙에 의해 자동 수행
- Leader는 알림 수신 후 review-quick을 수동 또는 자동으로 실행
