---
name: learner
description: 세션에서 반복되는 작업 패턴을 감지하고 재사용 가능한 스킬이나 룰로 추출합니다. evolve 스킬과 연동하여 .claude 설정을 자동 진화시킵니다. Use when you notice repeated patterns in a session or when the user asks to extract reusable workflows.
---

# Learner — 패턴 학습 및 추출

세션에서 반복되는 작업 패턴을 감지하고, 재사용 가능한 스킬이나 룰로 자동 추출합니다.

## 참조

- `.claude/skills/evolve/SKILL.md` — 설정 진화 워크플로우
- `.claude/rules/claude-code-reference.md` — 스킬/룰 생성 스펙

## 감지 대상 패턴

### 1. 반복 워크플로우
- 동일한 순서의 도구 호출이 3회 이상 반복
- 비슷한 파일 수정 패턴 (예: 항상 Model → ViewModel → View 순서)
- 반복되는 검증 단계

### 2. 프로젝트 컨벤션
- 파일 생성 시 항상 적용하는 헤더/주석 패턴
- import 순서, 코드 구조 규칙
- 네이밍 패턴 (접두사, 접미사)

### 3. 문제 해결 패턴
- 특정 오류에 대한 반복적 수정 방법
- 디버깅 시 항상 확인하는 체크포인트
- 리팩토링 시 적용하는 변환 규칙

## 추출 워크플로우

### Step 1: 패턴 식별
- 세션 중 반복된 작업을 분석
- 패턴의 빈도와 일관성 확인
- 자동화 가치 평가 (시간 절감, 오류 방지)

### Step 2: 패턴 분류
| 유형 | 추출 대상 |
|-----|----------|
| 워크플로우 | Skill (`.claude/skills/{name}/SKILL.md`) |
| 코딩 규칙 | Rule (`.claude/rules/{name}.md`) |
| 커맨드 체인 | Command (`.claude/commands/{name}.md`) |

### Step 3: 사용자 확인
- 감지된 패턴을 사용자에게 제시
- 스킬/룰 초안을 보여주고 승인 요청
- 승인 시 파일 생성

### Step 4: 등록
- claude-code-reference.md 체크리스트에 맞춰 파일 생성
- 프로젝트 히스토리에 기록 (evolve 스킬 연동)

## 안전 장치

- 사용자 확인 없이 자동 생성하지 않음
- 기존 스킬/룰과 중복되는지 검사
- 생성된 파일이 공식 스펙을 준수하는지 검증
