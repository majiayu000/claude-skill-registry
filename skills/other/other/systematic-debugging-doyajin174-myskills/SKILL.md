---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Four-phase framework ensuring understanding before attempting solutions.
allowed-tools: Read, Glob, Grep, Bash, Edit
license: MIT
metadata:
  author: obra/superpowers
  version: "1.0"
---

# Systematic Debugging

버그, 테스트 실패, 예상치 못한 동작에 대한 체계적 디버깅 방법론입니다.

## Core Principle

> **"ALWAYS find root cause before attempting fixes. Symptom fixes are failure."**

## Mandatory Phases

### Phase 1: Root Cause Investigation

```
1. 에러 메시지 정확히 읽기
2. 문제를 일관되게 재현
3. 최근 변경사항 확인
4. 멀티 컴포넌트 시스템에서 진단 증거 수집
5. 데이터 흐름을 역방향으로 추적
```

### Phase 2: Pattern Analysis

```
1. 작동하는 예시 찾기
2. 레퍼런스와 비교
3. 차이점 식별
4. 의존성 이해
```

### Phase 3: Hypothesis Testing

```
1. 구체적인 가설 수립
   - "X가 Y 때문에 발생한다고 생각됨"

2. 최소한의 테스트로 검증
   - 한 번에 하나의 변수만 변경

3. 과학적으로 결과 검증
   - 가설이 틀렸다면 다음 가설로
```

### Phase 4: Implementation

```
1. 실패하는 테스트 케이스 작성
2. 단일 수정 구현
3. 결과 검증
4. 3번 실패 시 중단
   → 아키텍처 문제 가능성 검토
```

## Critical Rules

| 규칙 | 설명 |
|------|------|
| 순차 진행 | 단계를 건너뛰지 않음 |
| 단일 수정 | 동시에 여러 수정 금지 |
| 3회 실패 시 중단 | 아키텍처 검토 필요 |

## Red Flags - 프로세스 포기 징후

```
❌ "일단 빠르게 고치고..."
❌ "아마 여기가 문제인 것 같아서..."
❌ "시간이 없어서 그냥..."
❌ "재현은 안되지만 고쳐봤어요"
```

## Debugging Template

```markdown
## 문제
[증상 설명]

## 재현 단계
1. [단계 1]
2. [단계 2]
→ [예상 결과] vs [실제 결과]

## Phase 1: 조사
- 에러 메시지: [정확한 메시지]
- 최근 변경: [관련 커밋/변경]
- 데이터 흐름: [추적 결과]

## Phase 2: 패턴 분석
- 작동 케이스: [예시]
- 차이점: [식별된 차이]

## Phase 3: 가설
1. 가설: [내용]
   테스트: [방법]
   결과: [결과]

## Phase 4: 수정
- 수정 내용: [변경사항]
- 테스트: [검증 방법]
- 결과: ✅/❌
```

## Evidence-Based Results

```
체계적 디버깅 적용 시:
- 문제 해결 시간: 2-3시간 → 15-30분
- 재발 방지: 근본 원인 해결로 재발 감소
- 학습 효과: 시스템 이해도 향상
```

## Best Practices

1. **증거 수집**: 로그, 스택 트레이스, 재현 단계 문서화
2. **최소 변경**: 한 번에 하나만 변경하고 테스트
3. **원복 준비**: 변경 전 상태로 돌릴 수 있게 준비
4. **기록 유지**: 시도한 것과 결과 문서화
