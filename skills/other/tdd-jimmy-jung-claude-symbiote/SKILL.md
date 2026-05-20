---
name: tdd
description: 테스트 주도 개발(TDD) 강제 워크플로우. Red-Green-Refactor 사이클을 따르며, 테스트를 먼저 작성한 후 구현합니다. Use when the user wants test-first development or when implementing features that require test coverage.
disable-model-invocation: true
---

# TDD — 테스트 주도 개발 워크플로우

Red-Green-Refactor 사이클을 따르는 TDD 강제 워크플로우입니다.

## 참조

- `project CLAUDE.md or .claude/rules/` — 테스트 프레임워크, 컨벤션
- `.claude/skills/code-accuracy/SKILL.md` — 코드 정확성 검증

## 워크플로우

### Step 1: 요구사항 분석
- 구현할 기능의 동작을 명확히 정의
- 테스트 시나리오 도출 (정상/경계/예외)

### Step 2: Red — 실패하는 테스트 작성
- 하나의 동작을 검증하는 테스트를 작성
- 테스트가 올바른 이유로 실패하는지 확인
- 테스트 이름은 시나리오를 명확히 설명

### Step 3: Green — 최소 구현
- 테스트를 통과시키는 최소한의 코드 작성
- 테스트가 요구하지 않는 기능은 추가하지 않음
- 모든 기존 테스트도 통과하는지 확인

### Step 4: Refactor — 정리
- 코드 구조를 개선 (중복 제거, 네이밍, 패턴 적용)
- 모든 테스트가 여전히 통과하는지 확인
- 프로젝트 컨벤션에 맞게 정리

### Step 5: 반복
- 다음 시나리오로 Step 2부터 반복
- 모든 시나리오가 완료될 때까지 반복

## 테스트 품질 기준

- 각 테스트는 하나의 동작만 검증
- 테스트 간 독립성 보장 (순서 무관)
- 외부 의존성은 테스트 더블로 대체
- 경계 조건과 에러 케이스 포함
- 테스트 이름만으로 동작을 이해할 수 있음

## 에이전트 연동

- tdd-guide 에이전트가 TDD 사이클을 가이드
- qa-tester 에이전트가 테스트 품질을 검증
- implementer 에이전트가 Green 단계 구현

## 완료 보고 형식

```
[TDD 완료]
- 테스트 수: N개 (통과: N, 실패: 0)
- 커버리지: [해당 시]
- 구현 파일: [목록]
- 테스트 파일: [목록]
```
