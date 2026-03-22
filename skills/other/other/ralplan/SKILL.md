---
name: ralplan
description: 반복적 기획 합의 워크플로우. Planner가 계획을 수립하고, Architect가 구조를 검토하고, Critic이 비판적으로 평가하는 과정을 합의에 도달할 때까지 반복합니다. Use when planning complex features that need multiple perspectives and iterative refinement.
disable-model-invocation: true
---

# Ralplan — 반복적 기획 합의

Planner → Architect → Critic 순환을 통해 계획을 반복적으로 정제합니다.

## 참조

- `.claude/skills/planning/SKILL.md` — 개발 계획 수립
- `.claude/skills/verify-loop/SKILL.md` — 루프 탈출 조건

## 진입 조건

- 복잡한 Feature 구현 계획이 필요할 때
- 아키텍처 결정이 포함된 기획일 때
- 여러 팀/모듈에 걸친 변경일 때

## 워크플로우

### Round 1: 초기 계획

#### Step 1: Planner (Prometheus)
- 요구사항 인터뷰 (What/Why/How/Success Criteria)
- 코드베이스 분석 (Grep+SemanticSearch+Glob 병렬)
- 영향도 평가
- 초기 구현 계획서 작성

#### Step 2: Architect (Oracle)
- 계획의 아키텍처 적합성 검토
- 모듈 경계와 인터페이스 설계 확인
- 기술적 실현 가능성 평가
- 구조적 개선안 제시

#### Step 3: Critic (Momus)
- 완전성 검증 (누락된 단계?)
- 숨겨진 의존성 식별
- 리스크 평가
- 판정: Approve / Conditional Approve / Requires Re-planning

### Round 2+: 정제 (필요 시)

Critic이 "Requires Re-planning"인 경우:
1. Critic의 피드백을 Planner에 전달
2. Planner가 계획을 수정
3. Architect가 구조 변경 검토
4. Critic이 재평가

### 합의 조건

- Critic이 "Approve" 또는 "Conditional Approve" 판정
- 최대 3회 반복 후 합의 미달 시 사용자에게 에스컬레이션

## 출력 형식

```
[Ralplan 완료] Round N

계획 상태: [Approved / Conditional]

구현 계획서:
  [계획 내용]

Architect 의견:
  [구조적 검토 요약]

Critic 의견:
  [평가 요약]

조건부 항목 (있는 경우):
  - [조건과 해결 방안]
```
