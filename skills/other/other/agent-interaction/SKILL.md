---
name: agent-interaction
description: 에이전트 간 상호작용 구조와 워크플로우 정의
---

# Agent Interaction Guide

에이전트 간 상호작용 구조와 워크플로우를 정의합니다.

## 팀 구성

```
┌─────────────────────────────────────────────────────────┐
│                    Strategic Layer                       │
│  ┌─────────┐    ┌──────────────────┐                    │
│  │   CTO   │───▶│ Planning Advisor │                    │
│  └────┬────┘    └────────┬─────────┘                    │
│       │                  │ (Codex 호출)                  │
│       ▼                  ▼                              │
│  ┌─────────────────────────────────────┐                │
│  │          .context/plan.md           │                │
│  └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Execution Layer                        │
│                                                         │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  FE Lead  │  │ Electron Lead │  │ Platform Lead │     │
│  └─────┬─────┘  └──────┬───────┘  └──────┬───────┘     │
│        │               │                  │             │
│        └───────────────┼──────────────────┘             │
│                        │                                │
│                        ▼                                │
│              ┌─────────────────┐                        │
│              │    UX Lead      │ (UI 검토)              │
│              └─────────────────┘                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Support Layer                         │
│                                                         │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │ DevOps Lead  │  │  Test Lead  │  │ Tech Writer  │   │
│  └──────────────┘  └─────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 워크플로우

### Phase 1: 계획 수립

```
요청 접수
    │
    ▼
┌─────────┐
│   CTO   │ ─── .context/plan.md 작성
└────┬────┘
     │
     ▼
┌──────────────────┐
│ Planning Advisor │ ─── 계획 검토
└────────┬─────────┘
         │
    ┌────┴────┐
    │ 위험도? │
    └────┬────┘
         │
   ┌─────┼─────┐
   ▼     ▼     ▼
 저/중  고위험
   │     │
   │     ▼
   │  Codex 검증
   │     │
   └──┬──┘
      ▼
  피드백 반영
      │
      ▼
  계획 확정
```

### Phase 2: 구현

계획에 명시된 담당 Lead가 작업 수행:

| 변경 영역 | 담당 Lead | 협업 대상 |
|-----------|-----------|-----------|
| React 컴포넌트 | FE Lead | UX Lead |
| Main process | Electron Lead | Platform Lead |
| IPC 채널 | Electron Lead | FE Lead |
| launchd 연동 | Platform Lead | Electron Lead |
| 스타일/디자인 | UX Lead | FE Lead |
| 빌드/패키징 | DevOps Lead | - |
| 테스트 | Test Lead | 해당 Lead |
| 문서 | Tech Writer | 해당 Lead |

### Phase 3: 검증

```
구현 완료
    │
    ▼
┌──────────────┐
│  Test Lead   │ ─── 테스트 커버리지 및 품질 검토
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ DevOps Lead  │ ─── bun run test && bun run build
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   UX Lead    │ ─── UI 변경 시 시각적 검토
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Tech Writer  │ ─── 문서 업데이트 필요 시
└──────────────┘
```

## 공유 아티팩트

| 파일 | 용도 | 작성자 | 소비자 |
|------|------|--------|--------|
| `.context/plan.md` | 구현 계획 | CTO | 모든 Lead |
| `.context/review.md` | Planning Advisor 피드백 | Planning Advisor | CTO |
| `CLAUDE.md` | 프로젝트 가이드 | Tech Writer | 모든 에이전트 |

## 핸드오프 프로토콜

### CTO → Planning Advisor

```markdown
## 계획 검토 요청

plan.md 경로: .context/plan.md
주요 변경: [IPC 추가 / 시스템 연동 / UI 변경 / ...]
예상 위험도: [저 / 중 / 고]
```

### Planning Advisor → CTO

```markdown
## 계획 검토 결과

위험도: [저 / 중 / 고]
Codex 검증: [수행 / 생략]

### 이슈
1. ...

### 권고
1. ...

결론: [수정 필요 / 진행 가능]
```

### CTO → Lead

```markdown
## 작업 할당

담당: [FE Lead / Electron Lead / Platform Lead]
plan.md 섹션: [해당 섹션 참조]
성공 기준: [구체적 기준]
협업 필요: [다른 Lead와 협업 필요 시]
```

### Lead → Lead (협업)

```markdown
## 협업 요청

요청자: [FE Lead]
대상: [Electron Lead]
내용: IPC 채널 `jobs:newChannel` 추가 필요
스펙:
  - 입력: { ... }
  - 출력: { ... }
```

### Lead → UX Lead (UI 검토)

```markdown
## UI 검토 요청

변경 컴포넌트: [JobCard, LogViewer, ...]
스크린샷: [첨부 또는 dev server URL]
체크 포인트:
  - 디자인 시스템 준수
  - 레이아웃 깨짐
```

### Lead → Tech Writer

```markdown
## 문서 업데이트 요청

변경 내용: [새 IPC 채널 / 새 타입 / ...]
업데이트 대상: [CLAUDE.md / README.md]
```

## IPC 변경 시 필수 협업

IPC 채널 추가/수정은 반드시 세 곳을 동시에 변경해야 함:

```
Electron Lead: src/main/ipc.ts (핸들러)
       │
       ├──▶ src/preload/index.ts (contextBridge)
       │
       └──▶ FE Lead: src/renderer/global.d.ts (타입)
```

**협업 순서:**
1. Electron Lead가 ipc.ts + preload/index.ts 수정
2. FE Lead에게 global.d.ts 타입 정의 요청
3. FE Lead가 렌더러에서 사용

## 에스컬레이션

### Lead → CTO

다음 상황에서 CTO에게 에스컬레이션:
- 계획에 명시되지 않은 추가 변경 필요
- 다른 Lead와 의견 충돌
- 기술적 결정이 필요한 상황

### Planning Advisor → CTO

다음 상황에서 계획 수정 요청:
- Codex가 심각한 이슈 발견
- 누락된 파일/변경사항 발견
- 실행 불가능한 계획

## 완료 조건

모든 작업은 다음을 만족해야 완료:

```bash
bun run test    # 전체 통과
bun run build   # 타입 에러 없음
```

추가로 plan.md에 명시된 성공 기준 충족.
