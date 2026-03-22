---
name: autonomous-loop
description: 자율 실행 루프. Plan→Execute→Verify를 반복하여 복잡한 작업을 자율적으로 완성합니다. Ralph(완료 보장) 모드와 Autopilot(병렬 최대 성능) 모드를 지원합니다. Use when the user wants autonomous task completion without manual intervention.
disable-model-invocation: true
---

# Autonomous Loop

Plan→Execute→Verify를 반복하여 복잡한 작업을 자율적으로 완성합니다.
사용자 개입 없이 계획 수립부터 구현, 검증, 수정까지 수행합니다.

## Task-Folder 구조

모든 상태 파일은 작업별 폴더에 격리됩니다:

```
.claude/project/state/{ISO8601-basic}_{task-name}/
├── ralph-state.md     # 루프 제어 메타데이터
├── notepad.md         # 작업 메모 (note 스킬)
└── prd.json           # PRD (선택)
```

폴더 네이밍 예시: `2026-02-13T1430_login-feature`

## 모드

| 모드 | 설명 | 최대 반복 | 병렬 실행 |
|------|------|-----------|----------|
| Ralph | 완료 보장. 상태 파일 추적, PRD 연동, 완료까지 반복 | 10 (설정 가능) | 선택적 |
| Autopilot | 최대 성능. 병렬 에이전트, 빠른 반복 | 3 | 적극적 |

Ralph: 사용자가 "끝까지", "완료할 때까지" 등을 요청할 때
Autopilot: 사용자가 "최대 성능", "병렬로" 등을 요청할 때

## 참조 스킬

Read tool로 다음 스킬을 읽어 적용하세요:
- `.claude/skills/verify-loop/SKILL.md` — 자기 수정 루프, 4-Level 완료 기준
- `.claude/skills/planning/SKILL.md` — 개발 계획 수립
- `.claude/skills/code-accuracy/SKILL.md` — 코드 정확성 검증
- `.claude/skills/notify-user/SKILL.md` — 에스컬레이션 시 Slack-First 모드로 사용자 응답 수신
- `project CLAUDE.md or .claude/rules/` — 프로젝트별 패턴 및 컨벤션

## 진입 조건

다음 조건 중 하나 이상에 해당할 때 사용합니다:
- 사용자가 자율 완료를 요청할 때
- 3개 이상의 파일 수정이 필요한 Feature 구현
- 신규 Feature 전체 생성
- 대규모 리팩토링 (5개 이상 파일 영향)
- PRD가 있고 acceptance criteria가 명확할 때

## 상태 파일 (Ralph 모드)

경로: `.claude/project/state/{task-folder}/ralph-state.md`

```markdown
# Ralph State

- active: true
- iteration: 0
- maxIterations: 10
- phase: analyze
- taskDescription: ...
- completionLevel: 2
- startedAt: 2026-02-13T14:30:00Z
- prdPath: none

## 실행 이력

- [1] phase: execute | result: ... | action: fix
- [2] phase: verify | result: ... | action: retry
```

## 6-Step 워크플로우

### Step 1: 초기화
- task-folder 생성: `mkdir -p .claude/project/state/{ISO8601-basic}_{task-name}`
  - 시각은 현재 시각 (예: `2026-02-13T1430`)
  - task-name은 작업 설명에서 kebab-case로 추출
- Ralph 모드: task-folder 내에 `ralph-state.md` 생성 (active: true, iteration: 0)
- Autopilot 모드: task-folder 내에 `notepad.md`로 상태 추적

### Step 2: ANALYZE
Analyst 에이전트로 요구사항 정제, 코드베이스/제약사항 분석. PRD가 있으면 acceptance criteria 로드.

### Step 3: PLAN
planning 스킬에 따라 계획 수립. Grep+SemanticSearch+Glob 병렬 실행하여 코드베이스 분석. Critic으로 계획 검증: 완전성, 의존성, 파괴적 변경, 실현 가능성.

### Step 4: EXECUTE
project context의 프로젝트 패턴을 따르며 구현. 독립 작업은 병렬 실행(최대 4개). 단계 완료 시마다 TODO 기록.

### Step 5: VERIFY
코드 품질, 패턴 준수, ReadLints, 완료 기준 검증. verify-loop 4-Level 기준 대조.
- Level ≥ 3: QA-tester 에이전트로 기능 검증
- Level ≥ 4: security-reviewer, doc-writer 추가 검증

### Step 6: LOOP
- 모든 기준 충족 → 완료
- 이슈 발견 + 반복 잔여 → 실패 원인 분석 → Fix → Step 4로 복귀
- 반복 한도 도달 → 에스컬레이션

## 완료 기준 (4-Level)

| Level | 기준 |
|-------|------|
| 1 | 코드 완료 + ReadLints 0 에러 |
| 2 | Level 1 + 기능 동작 + Reviewer 승인 |
| 3 | Level 2 + 테스트 통과 + QA-tester 검증 |
| 4 | Level 3 + 보안 검토 + 문서화 |

## PRD 연동

- task-folder 내 `prd.json`이 존재하면 사용
- prd.json의 userStories.acceptanceCriteria를 completion 검증 항목으로 활용

## 에스컬레이션 규칙

다음 상황에서 루프를 중단하고 사용자에게 질문합니다:
- maxIterations 도달 (Ralph) 또는 3회 반복 (Autopilot)
- 동일 오류 연속 발생 (Ralph: 3회, Autopilot: 2회)
- 아키텍처/파괴적 변경이 사용자 승인 필요
- 요구사항 모호/추가 정보 필요
- 보안 관련 결정 필요

에스컬레이션 시 notify-user 스킬을 호출합니다.
자율 루프 중이므로 Slack-First 모드가 자동 활성화됩니다:
- 직접 Slack DM으로 질문
- 30초 간격 폴링으로 응답 대기 (최대 10분)
- 응답 수신 시 자율 루프 계속 진행
- 타임아웃 시 ralph-state.md phase를 waiting-user로 변경 후 일시정지

## 병렬 실행 (Autopilot)

Step 3: Grep+SemanticSearch+Glob 동시 실행
Step 4: 독립 파일 생성 병렬
Step 5: 여러 파일 ReadLints 병렬, Reviewer+QA-tester 병렬

## 진행 보고 형식

```
[Autonomous Loop 진행] iteration N/M (모드)
- Task: {task-folder}
- Phase: [현재 단계]
- 최근 결과: [요약]
- 남은 이슈: [목록]
- 다음 조치: [fix|retry|escalate]
```

## 완료 시 정리

- Ralph: ralph-state.md의 active를 false, phase를 complete로 변경. 로그 작성.
- Autopilot: 완료 보고 형식으로 결과 출력.
- 완료된 task-folder는 `/clean` 커맨드로 정리 가능.
