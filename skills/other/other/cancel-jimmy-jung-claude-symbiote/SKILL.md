---
name: cancel
description: 실행 중인 자율 루프(Ralph Loop, Autopilot)를 안전하게 중단합니다. 상태 파일을 정리하고 진행 상황을 보고합니다. Use when the user wants to stop an autonomous execution loop or cancel ongoing multi-agent work.
disable-model-invocation: true
---

# Cancel — 통합 취소

실행 중인 자율 루프(Ralph Loop, Autopilot)를 안전하게 중단합니다.

## 취소 워크플로우

### Step 1: 활성 루프 확인
- `.claude/project/state/*/ralph-state.md`를 스캔
- `active: true`인 task-folder를 모두 찾아 목록 표시
- 여러 활성 루프가 있으면 사용자에게 취소 대상 선택 요청

### Step 2: 상태 정리
- 대상 task-folder의 `ralph-state.md`에서 `active`를 `false`로 변경
- `phase`를 `cancelled`로 변경
- 실행 이력 섹션에 취소 사유 기록

### Step 3: 진행 보고
현재까지의 진행 상황을 보고:
```
[루프 취소 완료]
- 취소된 루프: [Ralph Loop / Autopilot]
- Task-folder: {task-folder}
- 완료된 iteration: N/M
- 마지막 단계: [phase]
- 완료된 작업: [목록]
- 미완료 작업: [목록]
- 상태 파일: 정리 완료
```

### Step 4: 롤백 확인
- 마지막 iteration에서 불완전한 변경이 있는지 확인
- 불완전한 변경이 있으면 사용자에게 롤백 여부 문의
- 취소 후 `/clean` 커맨드로 task-folder 삭제 가능

## 안전 장치

- 파일 시스템 변경은 취소하지 않음 (git으로 관리)
- 상태 파일만 정리
- 취소 로그를 `.claude/project/logs/`에 기록
