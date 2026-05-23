---
name: plan-ears
description: EARS 기반 구현 스펙을 생성하여 pending에 저장
user-invocable: true
argument: 기능 설명 (예: "로그인 기능")
---

# /plan-ears

EARS 스펙을 생성합니다.

## Instructions

1. 인자로 받은 기능 설명을 분석합니다
2. 현재 프로젝트의 코드베이스를 탐색합니다 (관련 파일, 패턴, 의존성)
3. EARS 형식의 요구사항 스펙을 작성합니다
4. 프로젝트 specs 디렉토리를 준비합니다:
   ```bash
   PROJECT=$(basename "$PWD")
   mkdir -p ~/.claude/specs/$PROJECT/{pending,doing,done}
   ```
5. SPEC-ID는 `YYYYMMDD-HHMMSS` 타임스탬프를 사용합니다
6. 스펙 파일을 `~/.claude/specs/$PROJECT/pending/{SPEC-ID}.ears.md`에 저장합니다

## EARS 스펙 템플릿

```markdown
# {SPEC-ID}: {제목}
- created: {timestamp}
- project: {project-name}
- priority: high|medium|low

## Requirements (EARS)
- When {trigger}, the system shall {action}
- While {condition}, the system shall {behavior}
- If {condition}, then the system shall {response}

## Scope
- Files to create: [list]
- Files to modify: [list]
- Dependencies: [list]

## Acceptance Criteria
- [ ] criterion 1
- [ ] criterion 2

## Notes
(추가 컨텍스트)
```

## Executor 자동 전달

스펙 저장 완료 후, 같은 윈도우의 executor pane에 자동 전달합니다:

```bash
# 현재 윈도우의 pane 목록 조회
MY_PANE=$(tmux display-message -p '#{pane_id}')
EXECUTOR_PANE=$(tmux list-panes -F '#{pane_id}' | grep -v "$MY_PANE" | head -1)

# executor에게 exec-ears 명령 전송
if [ -n "$EXECUTOR_PANE" ]; then
  tmux send-keys -t "$EXECUTOR_PANE" -l '/exec-ears {spec-filename}' && tmux send-keys -t "$EXECUTOR_PANE" Enter
fi
```

- 자신의 pane ID를 제외한 나머지 pane이 executor입니다
- 전달 후 사용자에게 "스펙을 executor에 전달했습니다" 메시지를 출력합니다
- 전달 실패 시에도 스펙은 `pending/`에 저장되어 있으므로 수동 실행 가능합니다

## 주의사항
- 코드를 직접 작성하지 않고 스펙만 작성합니다
- 코드베이스를 충분히 탐색하여 정확한 Scope를 기술합니다
- Acceptance Criteria는 검증 가능한 형태로 작성합니다
