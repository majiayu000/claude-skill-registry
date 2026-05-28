---
name: spawn-test-case
description: 테스트 케이스 생성을 test-case-agent에 위임
allowed-tools: Task, Read
---

# Test Case Agent 활용 가이드

테스트 케이스 생성 작업을 test-case-agent에 위임하는 방법입니다.

## 핵심 원칙

**커밋 성공 후 테스트 케이스를 생성합니다.**

commit-agent가 성공적으로 완료된 후 test-case-agent를 spawn합니다.

## 관련 명령어

- `/create-testcase`: 사용자가 직접 테스트 케이스 생성 요청
  - `--task TASK-ID`: Task 기반 생성
  - `--standalone {설명}`: 독립 테스트 케이스
  - `--files {파일들} {설명}`: 파일 기반 생성

## 언제 사용하나?

- commit-agent 성공 후 (자동 워크플로우)
- 각 Step 완료 시
- 새 기능 구현 완료 시
- `/create-testcase` 명령어 실행 시

## 사전 조건

1. coder-agent: COMPLETED
2. builder-agent: COMPLETED
3. commit-agent: COMPLETED

## Spawn 방법

### 1. 커밋 성공 확인

commit-agent 결과 확인:
```markdown
## commit-agent 결과
- 상태: COMPLETED
- 커밋 해시: abc1234
- 커밋 메시지: [TASK-001] Add user authentication
```

### 2. Spawn 실행

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

```
Task tool 호출:
  subagent_type: "test-case-agent"
  run_in_background: true
  prompt: |
TASK-ID: TASK-001
Step: Step 2
변경 파일:
- src/auth/login.ts
- src/middleware/auth.ts

Step 설명: 사용자 인증 미들웨어 구현

coder-agent 결과:
- JWT 토큰 생성/검증 구현
- bcrypt 비밀번호 해싱
- Express 미들웨어 작성

.claude/agents/test-case-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 결과 대기

test-case-agent 결과 확인:
- COMPLETED: 테스트 케이스 생성 완료
- FAILED: 생성 실패 (드문 경우)

---

## 독립/파일 기반 Spawn

`/create-testcase --standalone` 또는 `--files` 사용 시:

### Spawn 실행

```
Task tool 호출:
  subagent_type: "test-case-agent"
  run_in_background: true
  prompt: |
    모드: standalone (또는 files)
테스트 ID: STANDALONE-001-T01
설명: {사용자 제공 설명}
대상 파일:
- {파일 목록}

코드 분석:
- {분석 결과}

.claude/agents/test-case-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 독립 테스트 ID 규칙

- 형식: `STANDALONE-{NNN}-T{XX}`
- 순번: `./Test/` 폴더의 기존 STANDALONE 번호 확인 후 +1
- 예시: STANDALONE-001-T01, STANDALONE-002-T01

---

## 정보 전달 항목

test-case-agent에 전달해야 할 정보:

| 항목 | 설명 | 필수 |
|------|------|------|
| TASK-ID | Task 식별자 | ✓ |
| Step | 완료된 Step 번호 | ✓ |
| 변경 파일 | 수정된 파일 목록 | ✓ |
| Step 설명 | 작업 내용 요약 | ✓ |
| coder 결과 | 구현 상세 내용 | ✓ |

## 결과 처리

### 성공 시

```markdown
## test-case-agent 결과
- 상태: COMPLETED
- 생성된 테스트 케이스:
  - [TASK-001-T01] 사용자 인증 테스트
  - [TASK-001-T02] 권한 검증 테스트
- 테스트 파일:
  - ./Test/[TASK-001-T01] User Authentication Test.md
  - ./Test/[TASK-001-T02] Permission Validation Test.md
- 총 테스트 항목: 12개
```

→ 사용자에게 테스트 실행 안내

### 실패 시

```markdown
## test-case-agent 결과
- 상태: FAILED
- 에러: 구현 내용 분석 실패
```

→ 추가 정보 제공 후 재시도

## 워크플로우 통합

```
coder-agent (코드 작성)
    ↓
builder-agent (빌드/테스트)
    ↓
commit-agent (커밋 생성)
    ↓
test-case-agent (테스트 케이스 생성) ← 이 시점
    ↓
Task 상태: pending_test
    ↓
사용자: /test-report 실행
```

## 테스트 파일 구조

### 파일 위치
- 활성: `./Test/[TASK-ID-TXX] Description.md`
- 아카이브: `./Test/Archive/[TASK-ID-TXX] Description.md`

### 파일명 규칙
- 형식: `[TASK-ID-TXX] Description.md`
- 예시: `[TASK-001-T01] User Authentication Test.md`

### 테스트 ID 규칙
- 형식: `TASK-{NNN}-T{XX}`
- 순번: Step 순서대로 증가
- 예시: TASK-001-T01, TASK-001-T02, ...

## 주의사항

1. **순서 준수**: commit-agent 성공 후 실행
2. **충분한 정보 제공**: coder-agent 결과 포함 필수
3. **한국어 내용**: 테스트 내용은 한국어로 (파일명은 영어)
4. **Step별 생성**: 각 Step에 대해 별도 테스트 케이스 생성

---

<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
