---
name: code-review
description: 독립 코드 리뷰 워크플로우. 코드 품질, 패턴 준수, 보안, 성능을 검토하고 구조화된 피드백을 제공합니다. Use when reviewing code changes, pull requests, or verifying refactoring correctness.
---

# Code Review — 독립 코드 리뷰

코드 품질, 패턴 준수, 보안, 성능을 종합적으로 검토합니다.

## 참조

- `project CLAUDE.md or .claude/rules/` — 프로젝트 컨벤션, 아키텍처
- `.claude/skills/code-accuracy/SKILL.md` — 코드 정확성

## 리뷰 체크리스트

### 구조 및 설계
- 단일 책임 원칙 준수
- 적절한 추상화 수준
- 기존 아키텍처 패턴 일관성
- 모듈 간 의존성 방향

### 코드 품질
- 함수/메서드 크기와 복잡도
- 네이밍 명확성
- 중복 코드
- 매직 넘버/하드코딩

### 안전성
- 에러 처리 완전성
- 메모리 안전성 (해당 시)
- 널/옵셔널 처리
- 리소스 해제

### 테스트
- 테스트 커버리지 적절성
- 엣지 케이스 포함 여부
- 테스트 가독성

## 워크플로우

### Step 1: 변경 범위 파악
- 변경된 파일 목록 확인
- 각 파일의 변경 내용 읽기
- 영향 받는 모듈 파악

### Step 2: 체크리스트 기반 검토
- 위 체크리스트 항목별로 검토
- 프로젝트 project context의 추가 규칙 적용

### Step 3: 피드백 작성

```
[Code Review 결과]

Critical (즉시 수정):
- [파일:라인] [설명] → [권장 수정]

Warning (수정 권장):
- [파일:라인] [설명] → [권장 수정]

Suggestion (개선 제안):
- [파일:라인] [설명] → [권장 수정]

종합: [Approve / Changes Requested / Needs Discussion]
```

## 에이전트 연동

- reviewer 에이전트가 이 스킬의 주 실행자
- security-reviewer 에이전트와 병렬 실행 가능
