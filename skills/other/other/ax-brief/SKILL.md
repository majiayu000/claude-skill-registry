---
name: ax-brief
description: "1-Page Brief 자동 생성 — Brief JSON + Confluence 페이지"
---

# AX Brief Skill

Scorecard 통과(GO) Signal을 1-Page Opportunity Brief로 변환합니다.

## 입력
- Signal JSON (Scorecard 통과)
- Scorecard JSON

## 출력
- Brief JSON (`brief.schema.json` 준수)
- Confluence 페이지 (선택)

## Brief 템플릿 구조

### 1. Executive Summary
- 한 문장 기회 정의
- 예상 임팩트 (KPI 가설)

### 2. Customer
- **Segment**: 타겟 고객군
- **Buyer Role**: 의사결정자
- **Users**: 실사용자
- **Account**: 특정 고객사 (있을 경우)

### 3. Problem
- **Pain**: 핵심 문제 상세
- **Why Now**: 지금 해결해야 하는 이유
- **Current Process**: 현재 해결 방식과 한계

### 4. Solution Hypothesis
- **Approach**: 제안 솔루션 방향
- **Integration Points**: 연동 포인트
- **Data Needed**: 필요 데이터

### 5. KPIs (측정 지표)
- 정량 목표 (예: AHT 15%↓, 처리시간 30%↓)

### 6. Evidence
- 근거 자료 링크 (최소 2개)

### 7. Validation Plan
- **Questions**: 검증할 질문들
- **Method**: 5DAY_SPRINT / INTERVIEW / DATA_ANALYSIS / BUYER_REVIEW
- **Success Criteria**: 성공 기준
- **Timebox**: 검증 기간 (일)

### 8. MVP Scope
- In-scope / Out-of-scope

### 9. Risks
- 주요 리스크 목록

## 자동 처리

1. Signal의 evidence 자동 링크
2. Scorecard 점수/rationale 참조
3. Confluence 페이지 자동 생성 (승인 후)
4. Play DB에 Brief 상태 업데이트

## 출력 예시

```json
{
  "brief_id": "BRF-2025-001",
  "signal_id": "SIG-2025-001",
  "title": "콜센터 AHT 최적화 AI 솔루션",
  "customer": {
    "segment": "대기업 콜센터",
    "buyer_role": "CS운영팀장",
    "users": "상담사 200명",
    "account": "ABC금융"
  },
  "problem": {
    "pain": "평균 통화 시간 8분으로 고객 불만 및 인건비 증가",
    "why_now": "AI 도입 예산 확보, 경쟁사 도입 사례 증가",
    "current_process": "수동 스크립트 참조, 신입 교육 3개월 소요"
  },
  "solution_hypothesis": {
    "approach": "실시간 상담 어시스턴트",
    "integration_points": ["CTI 시스템", "CRM"],
    "data_needed": ["통화 로그", "FAQ DB"]
  },
  "kpis": ["AHT 15% 감소", "FCR 10% 향상"],
  "validation_plan": {
    "questions": ["실시간 제안이 상담사에게 도움이 되는가?"],
    "method": "5DAY_SPRINT",
    "success_criteria": ["상담사 만족도 4.0/5.0 이상"],
    "timebox_days": 5
  }
}
```

## 사용법

```
/ax:brief --signal-id SIG-2025-001
```
