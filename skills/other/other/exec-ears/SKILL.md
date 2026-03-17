---
name: exec-ears
description: pending EARS 스펙을 선택하여 구현 실행
user-invocable: true
argument: (선택) 특정 스펙 파일명
---

# /exec-ears

pending 스펙을 실행합니다.

## Instructions

1. 현재 프로젝트의 pending 스펙을 확인합니다:
   ```bash
   PROJECT=$(basename "$PWD")
   ls ~/.claude/specs/$PROJECT/pending/
   ```
2. 스펙이 여러 개면 목록을 보여주고 AskUserQuestion으로 선택받습니다
3. 인자로 특정 스펙이 지정되면 해당 스펙을 바로 실행합니다
4. 선택된 스펙을 `doing/`으로 이동합니다:
   ```bash
   mv ~/.claude/specs/$PROJECT/pending/{spec} ~/.claude/specs/$PROJECT/doing/
   ```
5. 스펙 파일을 읽고 Requirements, Scope, Acceptance Criteria에 따라 구현합니다
6. 구현 완료 후 스펙 파일 하단에 실행 결과를 추가합니다:
   ```markdown
   ## Execution Result
   - completed: {timestamp}
   - status: success|partial|failed
   - Changes: [list of files changed]
   - Notes: (실행 중 발견된 사항)
   ```
7. 스펙을 `done/`으로 이동합니다:
   ```bash
   mv ~/.claude/specs/$PROJECT/doing/{spec} ~/.claude/specs/$PROJECT/done/
   ```
8. **Tester pane을 on-demand 생성하고 테스트 요청 전송**:
   ```bash
   # Tester pane이 없으면 생성
   TESTER_PANE=$(tmux list-panes -F '#{pane_index}:#{pane_id}' | grep '^1:' | cut -d: -f2)
   if [ -z "$TESTER_PANE" ]; then
     LID="${CLAUDE_LEADER_ID:-1}"
     tmux split-window -h -c "$PWD" "CLAUDE_LEADER_ID=${LID} CLAUDE_ROLE=tester ~/.config/mise/tasks/zai/claude --dangerously-skip-permissions"
     sleep 3
     TESTER_PANE=$(tmux list-panes -F '#{pane_index}:#{pane_id}' | grep '^1:' | cut -d: -f2)
   fi

   if [ -n "$TESTER_PANE" ]; then
     tmux send-keys -t "$TESTER_PANE" -l "테스트 요청: {spec-id}. 구현 완료된 스펙을 테스트해주세요." && tmux send-keys -t "$TESTER_PANE" Enter
   fi
   ```

## 주의사항
- 스펙의 Scope에 명시된 파일만 수정합니다
- Acceptance Criteria를 모두 충족하는지 확인합니다
- Tester pane이 이미 있으면 재사용, 없으면 새로 생성합니다
- Tester가 수정 요청을 보내면 수정 후 다시 테스트 요청합니다
