---
name: ax-scorecard
description: "Signal 정량 평가 — Scorecard JSON (100점 만점, 5개 차원)"
---

# AX Scorecard Skill

Signal을 정량 평가하여 Go/Pivot/Hold/No-Go를 판정합니다.

## 입력
- Signal JSON (`signal.schema.json` 준수)

## 출력
- Scorecard JSON (`scorecard.schema.json` 준수)

## 평가 기준 (100점 만점)

| 차원 | 배점 | 평가 항목 |
|------|------|----------|
| **Problem Severity** | 20점 | 고객 Pain 심각도, 빈도, 비용 |
| **Willingness to Pay** | 20점 | 예산 존재 여부, Buyer 명확성 |
| **Data Availability** | 20점 | 데이터 접근성, 품질, 보안 허들 |
| **Feasibility** | 20점 | 기술 난이도, PoC 기간, 리소스 |
| **Strategic Fit** | 20점 | AX BD 전략 정합성, 확장성 |

## Red Flags (자동 감점/경고)

다음 조건 중 하나라도 해당 시 Red Flag 표시:
- 데이터 접근 불가 (내부 정책/보안)
- Buyer/예산 오너 부재
- 규제/법무 이슈 확인됨
- 경쟁사 선점 (6개월 이상 앞섬)
- KT DS 역량 외 영역

## Recommendation 로직

```
IF total_score >= 70 AND red_flags == 0:
    decision = "GO"
    next_step = "BRIEF"
ELIF total_score >= 50 AND red_flags <= 1:
    decision = "PIVOT"
    next_step = "NEED_MORE_EVIDENCE"
ELIF total_score >= 30:
    decision = "HOLD"
    next_step = "NEED_MORE_EVIDENCE"
ELSE:
    decision = "NO_GO"
    next_step = "DROP"
```

## 출력 예시

```json
{
  "signal_id": "SIG-2025-001",
  "total_score": 75,
  "dimension_scores": {
    "problem_severity": 18,
    "willingness_to_pay": 15,
    "data_availability": 14,
    "feasibility": 16,
    "strategic_fit": 12
  },
  "red_flags": [],
  "recommendation": {
    "decision": "GO",
    "next_step": "BRIEF",
    "rationale": "고객 Pain이 명확하고 예산 확보 가능성 높음"
  },
  "scored_by": "ScorecardEvaluator",
  "scored_at": "2025-01-14T10:00:00Z"
}
```

## 사용법

```
/ax:triage --signal-id SIG-2025-001
```
