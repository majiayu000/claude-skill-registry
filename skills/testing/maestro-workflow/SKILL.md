---
name: maestro-workflow
description: Maestro 기반 모바일 테스트 자동화 워크플로우를 시작합니다. planner -> grouper -> generator -> executor -> healer 순서로 Agent 기반 테스트를 자동 실행합니다. "/maestro-workflow", "마에스트로 워크플로우", "Maestro 테스트" 등의 명령으로 활성화됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite, AskUserQuestion
---

# Maestro 테스트 워크플로우

Claude + Maestro로 Agent 기반 모바일 테스트 자동화를 수행하는 워크플로우입니다.

## 활성화 방법

- `/maestro-workflow`
- `마에스트로 워크플로우`
- `Maestro 테스트`
- `마에스트로로 [기능] 테스트`

### 예시

```
사용자: /maestro-workflow 로그인 기능 테스트
사용자: 마에스트로로 거래 추가 기능 테스트해줘
사용자: Maestro 테스트 전체 앱
```

---

## 워크플로우 개요

```
[요청 접수]
    |
    v
[Phase 1: 시나리오 계획] ── maestro-planner-agent
    |  - 앱 기능 분석
    |  - 테스트 시나리오 YAML 출력
    |
    v
[Phase 2: 그룹화] ── maestro-grouper-agent
    |  - 병렬/순차 실행 그룹 분류
    |  - 실행 순서 결정
    |
    v
[Phase 3: Flow 생성] ── maestro-generator-agent
    |  - Maestro YAML 파일 생성
    |  - flows/ 디렉토리에 저장
    |
    v
[Phase 4: 실행] ── scripts/run-maestro.sh
    |  - 그룹별 병렬/순차 실행
    |  - 결과 수집
    |
    v
[Phase 5: 복구 Loop] ── maestro-healer-agent
    |  +──[테스트 실패]──> healer 호출
    |  |                    - 실패 분석
    |  |                    - flow 수정
    |  +<─────────────────[재실행]
    |
    v (모든 테스트 통과)
[Phase 6: 완료 보고]
    - 결과 요약
    - 보고서 생성
```

---

## Phase 1: 시나리오 계획

### 1.1 maestro-planner-agent 호출

```
Task(
  subagent_type: "maestro-planner-agent",
  prompt: """
  다음 기능에 대한 Maestro 테스트 시나리오를 계획해주세요:

  기능: [테스트 대상 기능]
  앱 정보:
  - 패키지: com.household.shared.shared_household_account
  - 아키텍처: Clean Architecture + Feature-first

  lib/features/ 디렉토리를 분석하여 시나리오를 도출하세요.
  반드시 YAML 형식으로만 출력하세요.
  """
)
```

### 1.2 출력 예시

```yaml
scenarios:
  - id: login_success
    description: 정상 로그인
    entry_state: logged_out
    screen: Login
    mutation: true
    shared_state: true
    priority: critical
    steps:
      - 로그인 화면 진입
      - 이메일 입력
      - 비밀번호 입력
      - 로그인 버튼 탭
      - 홈 화면 확인
```

---

## Phase 2: 그룹화

### 2.1 maestro-grouper-agent 호출

```
Task(
  subagent_type: "maestro-grouper-agent",
  prompt: """
  다음 테스트 시나리오를 병렬 실행 그룹으로 분류해주세요:

  [Phase 1 출력 YAML]

  반드시 YAML 형식으로만 출력하세요.
  """
)
```

### 2.2 출력 예시

```yaml
groups:
  - group_id: auth
    execution: sequential
    test_ids: [login_success, logout]
    reason: 인증 상태 공유로 순차 실행
    order: 1

  - group_id: read_only
    execution: parallel
    test_ids: [category_list, statistics_view]
    reason: 읽기 전용으로 병렬 실행 가능
    order: 2
```

---

## Phase 3: Flow 생성

### 3.1 maestro-generator-agent 호출

```
Task(
  subagent_type: "maestro-generator-agent",
  prompt: """
  다음 시나리오를 Maestro YAML flow 파일로 생성해주세요:

  시나리오:
  [Phase 1 출력 YAML]

  그룹 정보:
  [Phase 2 출력 YAML]

  앱 패키지: com.household.shared.shared_household_account

  flows/ 디렉토리에 파일을 생성하세요.
  """
)
```

### 3.2 생성되는 파일 구조

```
flows/
├── auth/
│   ├── login_success.yaml
│   └── logout.yaml
├── transaction/
│   └── add_expense.yaml
└── common/
    └── setup.yaml
```

---

## Phase 4: 실행

### 4.1 Maestro CLI 실행

Claude가 직접 실행합니다:

```bash
# 순차 그룹 실행
maestro test flows/auth/login_success.yaml
maestro test flows/auth/logout.yaml

# 병렬 그룹 실행
maestro test flows/transaction/ &
maestro test flows/category/ &
wait
```

### 4.2 실행 스크립트

```bash
# scripts/run-maestro.sh 실행
./scripts/run-maestro.sh
```

---

## Phase 5: 복구 Loop

### 5.1 실패 감지

실행 결과에서 실패한 테스트 확인:

```bash
# 로그에서 실패 추출
grep -l "FAILED" .maestro/logs/*.log
```

### 5.2 maestro-healer-agent 호출

```
Task(
  subagent_type: "maestro-healer-agent",
  prompt: """
  다음 실패한 Maestro 테스트를 수정해주세요:

  실패한 flow: flows/auth/login_success.yaml

  실패 로그:
  ```
  [실패 로그 내용]
  ```

  테스트 목적은 변경하지 마세요.
  selector 변경이나 대기 시간 추가로 해결하세요.
  """
)
```

### 5.3 재시도 제한

- 동일 테스트 최대 3회 재시도
- 초과 시 수동 검토 요청

---

## Phase 6: 완료 보고

### 6.1 결과 요약

```yaml
# .maestro/reports/summary.yaml
execution:
  date: 2026-01-05
  total_tests: 10
  passed: 8
  failed: 1
  healed: 1

groups:
  - group_id: auth
    tests: 2
    passed: 2

  - group_id: transaction
    tests: 3
    passed: 2
    healed: 1

failures:
  - test_id: share_invite
    attempts: 3
    status: manual_review
```

### 6.2 보고서 저장

```
.maestro/
├── flows/          # 생성된 flow 파일
├── logs/           # 실행 로그
├── screenshots/    # 스크린샷
└── reports/        # 결과 보고서
    └── summary.yaml
```

---

## Agent 역할 정리

| Agent | 역할 | 출력 |
|-------|------|------|
| maestro-planner-agent | 테스트 시나리오 계획 | scenarios YAML |
| maestro-grouper-agent | 병렬/순차 그룹화 | groups YAML |
| maestro-generator-agent | Maestro flow 생성 | .yaml 파일들 |
| maestro-healer-agent | 실패 테스트 복구 | 수정된 flow |

---

## 디렉토리 구조

```
project/
├── .claude/
│   ├── agents/
│   │   ├── maestro-planner-agent.md
│   │   ├── maestro-grouper-agent.md
│   │   ├── maestro-generator-agent.md
│   │   └── maestro-healer-agent.md
│   └── skills/
│       └── maestro-workflow/
│           └── SKILL.md
├── flows/                    # Maestro flow 파일
│   ├── auth/
│   ├── transaction/
│   └── common/
├── scripts/
│   ├── run-maestro.sh       # 실행 스크립트
│   └── heal-maestro.sh      # 복구 스크립트
└── .maestro/
    ├── logs/
    ├── screenshots/
    └── reports/
```

---

## 환경 설정

### Maestro 설치

```bash
# macOS
brew install maestro

# 또는 curl
curl -Ls "https://get.maestro.mobile.dev" | bash
```

### 환경변수 (.env)

```env
TEST_EMAIL=test@example.com
TEST_PASSWORD=TestPassword123!
MAESTRO_DRIVER_STARTUP_TIMEOUT=120000
```

---

## 자동 승인 설정

워크플로우 원활한 실행을 위한 settings.local.json 권한:

```json
{
  "permissions": {
    "allow": [
      "Bash(maestro:*)",
      "Bash(./scripts/run-maestro.sh:*)",
      "Bash(./scripts/heal-maestro.sh:*)"
    ]
  }
}
```

---

## 사용 예시

### 전체 앱 테스트

```
사용자: /maestro-workflow 전체 앱 테스트
```

### 특정 기능 테스트

```
사용자: /maestro-workflow 로그인 기능만 테스트
```

### 특정 그룹만 재실행

```
사용자: auth 그룹 테스트만 다시 실행해줘
```

---

## 주의사항

1. **Maestro 설치 필수**: `maestro` CLI가 PATH에 있어야 함
2. **에뮬레이터 실행 필요**: Android/iOS 에뮬레이터가 실행 중이어야 함
3. **YOLO 모드 권장**: `--dangerously-skip-permissions`로 실행 시 끊김 없이 진행
4. **테스트 격리**: 각 테스트는 `clearState`로 시작하여 격리
5. **병렬 실행 주의**: shared_state 테스트는 반드시 순차 실행
