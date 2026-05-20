---
name: dispatching-parallel-agents
description: Use when facing 3+ independent failures that can be investigated without shared state or dependencies. Dispatches multiple Claude agents to investigate and fix independent problems concurrently.
allowed-tools: Read, Glob, Grep, Task, Bash
license: MIT
metadata:
  author: obra/superpowers
  version: "1.0"
---

# Dispatching Parallel Agents

여러 독립적인 문제를 병렬 에이전트로 동시에 해결하는 스킬입니다.

## Core Principle

> **"Dispatch one agent per independent problem domain. Let them work concurrently."**

## When to Use

### ✅ 적합한 상황

```
- 3개 이상의 독립적 실패
- 각 문제가 서로 관련 없음
- 공유 상태 없이 조사 가능
- 서로 다른 파일/서브시스템에서 발생
```

### ❌ 피해야 할 상황

```
- 실패들이 연결되어 있음 (하나 해결 시 다른 것도 해결)
- 전체 시스템 컨텍스트가 필요
- 에이전트들이 공유 리소스에 간섭
```

## Execution Pattern

### 1. 독립적 문제 도메인 식별

```markdown
## 실패 분석

| 파일/영역 | 문제 | 독립성 |
|-----------|------|--------|
| auth.test.js | JWT 검증 실패 | ✅ 독립 |
| api.test.js | 라우팅 오류 | ✅ 독립 |
| db.test.js | 연결 타임아웃 | ✅ 독립 |
```

### 2. 에이전트 태스크 생성

```markdown
## Agent 1: Auth Module
Scope: src/auth/, tests/auth/
Goal: JWT 검증 실패 원인 찾기
Constraint: auth 관련 파일만 수정

## Agent 2: API Routes
Scope: src/api/, tests/api/
Goal: 라우팅 오류 해결
Constraint: api 관련 파일만 수정

## Agent 3: Database
Scope: src/db/, tests/db/
Goal: 연결 타임아웃 해결
Constraint: db 관련 파일만 수정
```

### 3. 동시 디스패치

```
Task(Agent 1) || Task(Agent 2) || Task(Agent 3)
```

### 4. 결과 통합

```markdown
## Results

### Agent 1 (Auth)
- 문제: 만료 시간 계산 오류
- 수정: auth/jwt.js:45
- 테스트: ✅ 통과

### Agent 2 (API)
- 문제: 미들웨어 순서
- 수정: api/routes.js:12
- 테스트: ✅ 통과

### Agent 3 (DB)
- 문제: 커넥션 풀 설정
- 수정: db/config.js:8
- 테스트: ✅ 통과
```

## Agent Prompt Template

```markdown
## Task
[구체적인 문제 설명]

## Scope
- 파일: [제한된 파일 목록]
- 관련 테스트: [테스트 파일]

## Goal
[명확한 목표]

## Constraints
- 다른 영역 코드 수정 금지
- 프로덕션 코드 최소 변경
- 테스트 통과 필수

## Expected Output
1. 근본 원인 분석
2. 수정 내용 요약
3. 테스트 결과
```

## Common Pitfalls

| 문제 | 해결책 |
|------|--------|
| 범위가 너무 넓음 | 구체적인 파일/디렉토리 지정 |
| 컨텍스트 누락 | 필요한 배경 정보 포함 |
| 제약 미정의 | "~하지 마세요" 명시 |
| 출력 불명확 | 정확한 deliverable 지정 |

## Demonstrated Results

```
6개 실패, 3개 파일
→ 3개 병렬 에이전트
→ 동시 완료
→ 충돌 0건
→ 순차 대비 ~3배 속도
```
