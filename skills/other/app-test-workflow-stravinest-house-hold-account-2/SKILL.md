---
name: app-test-workflow
description: Flutter 앱 테스트 워크플로우를 시작합니다. 테스트 계획 수립 -> 에뮬레이터 테스트 -> 실패 시 디버그 수정 -> 재테스트 순서로 진행합니다. "앱 테스트 워크플로우", "/app-test-workflow", "앱 테스트" 등의 명령으로 활성화됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite, AskUserQuestion, mcp__supabase__execute_sql, mcp__supabase__list_tables, mcp__mobile-mcp__mobile_list_devices, mcp__mobile-mcp__mobile_list_apps, mcp__mobile-mcp__mobile_launch_app, mcp__mobile-mcp__mobile_terminate_app, mcp__mobile-mcp__mobile_screenshot, mcp__mobile-mcp__mobile_tap, mcp__mobile-mcp__mobile_type_text, mcp__mobile-mcp__mobile_swipe, mcp__mobile-mcp__mobile_get_screen_size, mcp__mobile-mcp__mobile_list_elements, mcp__mobile-mcp__mobile_get_element, mcp__mobile-mcp__mobile_press_button
---

# 앱 테스트 워크플로우 (App Test Workflow)

Flutter 앱의 특정 기능을 에뮬레이터에서 직접 테스트하고, 실패 시 자동으로 수정하는 워크플로우입니다.

## 활성화 방법

다음 명령어로 워크플로우를 시작합니다:

- `앱 테스트 워크플로우` 또는 `앱 테스트 워크플로우로 진행해줘`
- `/app-test-workflow`
- `앱 테스트로 [테스트할 기능]`

### 예시

```
사용자: 앱 테스트 워크플로우로 로그인 기능을 테스트해줘
사용자: /app-test-workflow 거래 추가 기능 테스트
사용자: 앱 테스트로 카테고리 관리 확인해줘
```

---

## 워크플로우 개요

```
[요청 접수]
    |
    v
[Phase 1: 테스트 계획 수립] ────────────────────────
    |  - 테스트할 기능 분석
    |  - 테스트 시나리오 정의
    |  - Todo 리스트 작성
    |  - 사용자 확인
    v
[Phase 2: 환경 준비] ────────────────────────────────
    |  - 에뮬레이터 상태 확인
    |  - 테스트 데이터 준비 (Supabase)
    |  - 앱 빌드 및 실행
    v
[Phase 3: 테스트 실행 Loop] ─────────────────────────
    |  - app-test-agent 호출
    |  - Todo 항목별 테스트 수행
    |  +──[테스트 실패]──> [app-debug-agent 호출]
    |  |                      - 버그 분석
    |  |                      - 코드 수정
    |  |                      - 수정 검증
    |  +<────────────────── [재테스트]
    |
    v (모든 Todo 완료)
[Phase 4: 완료 보고] ────────────────────────────────
    - 테스트 결과 요약
    - 수정된 코드 목록
    - 보고서 생성
```

---

## Phase 1: 테스트 계획 수립

### 1.1 기능 분석

테스트할 기능의 코드와 구조를 파악합니다.

```
Task(
  subagent_type: "Explore",
  prompt: "[기능명] 관련 코드를 분석하고 테스트 포인트를 파악해주세요.
  - 관련 파일 목록
  - 주요 로직 흐름
  - 의존성 (API, DB 등)"
)
```

### 1.2 테스트 시나리오 정의

기능별 테스트 시나리오를 정의합니다.

```markdown
## 테스트 시나리오: [기능명]

### 정상 케이스
1. [시나리오 1 설명]
   - 입력: [테스트 입력]
   - 예상 결과: [예상 출력]

2. [시나리오 2 설명]
   - 입력: [테스트 입력]
   - 예상 결과: [예상 출력]

### 에러 케이스
1. [에러 시나리오 설명]
   - 입력: [잘못된 입력]
   - 예상 결과: [에러 메시지/처리]
```

### 1.3 Todo 리스트 작성

테스트 항목을 Todo로 등록합니다.

```
TodoWrite([
  { content: "[기능명] 테스트 환경 준비", status: "pending", activeForm: "테스트 환경 준비 중" },
  { content: "[시나리오 1] 정상 케이스 테스트", status: "pending", activeForm: "정상 케이스 테스트 중" },
  { content: "[시나리오 2] 에러 케이스 테스트", status: "pending", activeForm: "에러 케이스 테스트 중" },
  ...
])
```

### 1.4 사용자 확인

```
테스트 계획이 수립되었습니다:

테스트 대상: [기능명]
테스트 항목: [N]개
- [ ] 시나리오 1
- [ ] 시나리오 2
...

진행하시겠습니까? (Y/n)
```

---

## Phase 2: 환경 준비

### 2.1 디바이스 확인 (Mobile MCP)

```
// Mobile MCP로 연결된 디바이스 확인 (권장)
mcp__mobile-mcp__mobile_list_devices

// Flutter CLI로도 확인 가능
flutter devices
flutter emulators
```

### 2.2 에뮬레이터 실행 (필요시)

```bash
# Android 에뮬레이터 실행
flutter emulators --launch <emulator_id>

# iOS 시뮬레이터 실행
flutter emulators --launch apple_ios_simulator

# 에뮬레이터 실행 후 약 10-20초 대기
```

### 2.3 Mobile MCP 도구 목록

| 도구 | 설명 |
|------|------|
| `mobile_list_devices` | 연결된 디바이스/에뮬레이터 목록 |
| `mobile_list_apps` | 설치된 앱 목록 |
| `mobile_launch_app` | 앱 실행 (패키지명) |
| `mobile_terminate_app` | 앱 종료 |
| `mobile_screenshot` | 스크린샷 캡처 |
| `mobile_tap` | 화면 탭 (x, y 좌표) |
| `mobile_type_text` | 텍스트 입력 |
| `mobile_swipe` | 스와이프/스크롤 |
| `mobile_list_elements` | UI 요소 목록 (Accessibility Tree) |
| `mobile_get_element` | 특정 UI 요소 정보 |
| `mobile_press_button` | 하드웨어 버튼 (back, home) |
| `mobile_get_screen_size` | 화면 크기 |

### 2.4 테스트 데이터 준비

Supabase MCP를 사용하여 테스트 데이터를 준비합니다.

```sql
-- 테스트 사용자 생성 (필요시)
INSERT INTO profiles (id, display_name, email)
VALUES ('test-user-id', 'Test User', 'test@example.com');

-- 테스트용 가계부 생성
INSERT INTO ledgers (id, name, owner_id)
VALUES ('test-ledger-id', 'Test Ledger', 'test-user-id');
```

### 2.5 앱 빌드 및 실행

```bash
# 의존성 설치
flutter pub get

# 앱 빌드 및 실행
flutter run -d <device_id>
```

또는 Mobile MCP로 이미 설치된 앱 실행:

```
// 설치된 앱 목록 확인
mcp__mobile-mcp__mobile_list_apps

// 앱 실행
mcp__mobile-mcp__mobile_launch_app(packageName: "com.example.household_account")
```

---

## Phase 3: 테스트 실행 Loop

### 3.1 테스트 실행

각 Todo 항목에 대해 app-test-agent를 호출합니다.

```
Task(
  subagent_type: "app-test-agent",
  prompt: """
  [테스트 지시서]
  - 테스트 ID: [Todo 번호]
  - 테스트 시나리오: [시나리오 설명]
  - 입력 데이터: [테스트 입력]
  - 예상 결과: [예상 출력]
  - 디바이스: [device_id]
  - 패키지명: com.example.household_account

  Mobile MCP를 사용하여 에뮬레이터에서 직접 테스트를 수행하세요:
  1. mobile_screenshot으로 현재 화면 확인
  2. mobile_list_elements로 UI 요소 파악
  3. mobile_tap, mobile_type_text로 상호작용
  4. 결과 스크린샷 캡처 후 검증
  """
)
```

### 3.1.1 Mobile MCP 테스트 예시

```
// 1. 화면 스크린샷 캡처
mcp__mobile-mcp__mobile_screenshot

// 2. UI 요소 목록 확인 (Accessibility Tree)
mcp__mobile-mcp__mobile_list_elements

// 3. 버튼 탭 (좌표 또는 요소 기반)
mcp__mobile-mcp__mobile_tap(x: 200, y: 400)

// 4. 텍스트 입력
mcp__mobile-mcp__mobile_type_text(text: "test@email.com")

// 5. 스크롤/스와이프
mcp__mobile-mcp__mobile_swipe(startX: 200, startY: 600, endX: 200, endY: 200)

// 6. 뒤로가기 버튼
mcp__mobile-mcp__mobile_press_button(button: "back")

// 7. 결과 확인용 스크린샷
mcp__mobile-mcp__mobile_screenshot
```

### 3.2 테스트 결과 처리

#### 성공 시

```
TodoWrite([
  { content: "[시나리오 1] 정상 케이스 테스트", status: "completed", activeForm: "정상 케이스 테스트 중" },
  ...
])
```

#### 실패 시 -> app-debug-agent 호출

```
Task(
  subagent_type: "app-debug-agent",
  prompt: """
  [디버그 지시서]
  - 실패한 테스트: [테스트 ID]
  - 에러 정보:
    ```
    [테스트 결과 JSON]
    ```
  - 예상 동작: [예상 결과]
  - 실제 동작: [실제 결과]

  원인을 분석하고 코드를 수정해주세요.
  """
)
```

### 3.3 수정 후 재테스트

app-debug-agent 수정 완료 후:

1. 앱 재빌드 (Hot Reload 또는 재시작)
2. 동일 테스트 시나리오 재실행
3. 성공 시 다음 Todo로 진행
4. 실패 시 다시 app-debug-agent 호출 (최대 3회)

### 3.4 반복 제한

- 동일 테스트 최대 3회 재시도
- 초과 시 사용자에게 확인 요청

```
테스트 [시나리오명]이 3회 실패했습니다.

실패 원인:
- 1차: [원인]
- 2차: [원인]
- 3차: [원인]

계속 진행하시겠습니까?
1. 건너뛰고 다음 테스트 진행
2. 수동으로 문제 해결 후 재시도
3. 워크플로우 중단
```

---

## Phase 4: 완료 보고

### 4.1 테스트 결과 요약

```markdown
# 앱 테스트 완료 보고서

## 테스트 개요
- 테스트 대상: [기능명]
- 테스트 일시: YYYY-MM-DD HH:MM
- 테스트 디바이스: [디바이스명]

## 테스트 결과

| 시나리오 | 결과 | 재시도 | 비고 |
|----------|------|--------|------|
| 시나리오 1 | PASS | 0 | - |
| 시나리오 2 | PASS | 2 | 버그 수정 후 통과 |
| 시나리오 3 | SKIP | 3 | 수동 확인 필요 |

## 수정된 코드

| 파일 | 수정 내용 |
|------|----------|
| lib/features/auth/data/repositories/auth_repository.dart | null 처리 추가 |
| lib/features/auth/presentation/pages/login_page.dart | 에러 메시지 개선 |

## 남은 이슈
- [ ] 시나리오 3 수동 확인 필요
```

### 4.2 보고서 저장

```
.app-test-reports/
├── test-report-YYYY-MM-DD-[기능명].md
└── ...
```

---

## Agent 역할 분담

### app-test-agent

| 역할 | 설명 |
|------|------|
| 에뮬레이터 관리 | 에뮬레이터 실행, 앱 실행 |
| 테스트 수행 | 시나리오별 테스트 실행 |
| 데이터 입력 | Supabase를 통한 테스트 데이터 관리 |
| 결과 수집 | 테스트 결과 JSON 형식 반환 |

### app-debug-agent

| 역할 | 설명 |
|------|------|
| 에러 분석 | 테스트 실패 원인 분석 |
| 코드 수정 | 버그 픽스, 로직 수정 |
| 검증 | 수정 후 flutter analyze 실행 |
| 보고 | 수정 내역 JSON 형식 반환 |

---

## 테스트 데이터 관리

### Supabase 테스트 계정

테스트용 계정 정보는 `.env` 파일에서 관리합니다.

```env
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=TestPassword123!
```

### 테스트 데이터 정리

테스트 완료 후 테스트 데이터를 정리합니다.

```sql
-- 테스트 데이터 정리
DELETE FROM transactions WHERE ledger_id = 'test-ledger-id';
DELETE FROM categories WHERE ledger_id = 'test-ledger-id';
DELETE FROM ledgers WHERE id = 'test-ledger-id';
```

---

## 자동 승인 설정

워크플로우가 끊김 없이 실행되려면 다음 도구들을 자동 승인해야 합니다.

### settings.local.json 추가 필요

```json
{
  "permissions": {
    "allow": [
      "Bash(flutter devices:*)",
      "Bash(flutter emulators:*)",
      "Bash(flutter emulators --launch:*)",
      "Bash(flutter pub get:*)",
      "Bash(flutter run:*)",
      "Bash(flutter test:*)",
      "Bash(flutter analyze:*)",
      "mcp__supabase__execute_sql",
      "mcp__supabase__list_tables"
    ]
  }
}
```

---

## 주의사항

1. **에뮬레이터 필수**: 실제 디바이스 또는 에뮬레이터가 실행 중이어야 함
2. **Supabase 연결**: `.env` 파일에 Supabase 설정 필요
3. **테스트 격리**: 테스트 데이터는 운영 데이터와 분리
4. **재시도 제한**: 동일 테스트 최대 3회 재시도
5. **수동 개입**: 복잡한 버그는 사용자에게 알림

---

## 트러블슈팅

### 에뮬레이터가 없는 경우

```bash
# Android 에뮬레이터 생성
flutter emulators --create --name test_device

# iOS는 Xcode에서 시뮬레이터 추가 필요
```

### 앱 빌드 실패

```bash
# 캐시 정리
flutter clean
flutter pub get

# 재빌드
flutter run -d <device_id>
```

### Supabase 연결 실패

1. `.env` 파일 확인
2. Supabase 대시보드에서 서비스 상태 확인
3. 네트워크 연결 확인
