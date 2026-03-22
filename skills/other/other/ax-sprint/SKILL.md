---
name: ax-sprint
description: "5-day Sprint 플랜 수립 — Sprint 체크리스트"
---

# AX Sprint Skill

Brief 승인 후 5-Day Validation Sprint를 설계하고 운영합니다.

## 입력
- Brief JSON (승인됨)

## 출력
- Validation JSON (`validation.schema.json` 준수)
- Sprint 체크리스트
- Confluence 스프린트 페이지

## 5-Day Sprint 프레임워크

### Day 1: 문제 정의 & 매핑
- [ ] Brief 기반 문제 상세화
- [ ] 이해관계자 맵 작성
- [ ] 검증 질문 우선순위화
- [ ] 검증 방법론 확정

### Day 2: 솔루션 스케치
- [ ] How Might We (HMW) 질문 도출
- [ ] 아이디어 브레인스토밍 (4-up)
- [ ] 팀 투표 & 수렴
- [ ] 프로토타입 범위 결정

### Day 3: 결정 & 프로토타입 설계
- [ ] 최종 솔루션 방향 결정
- [ ] 스토리보드 작성
- [ ] 역할 분담
- [ ] 인터뷰 가이드 준비

### Day 4: 프로토타입 제작
- [ ] MVP 프로토타입 개발
- [ ] 테스트 시나리오 작성
- [ ] 인터뷰 참여자 확정
- [ ] 리허설

### Day 5: 검증 & 결론
- [ ] 고객 인터뷰/테스트 수행
- [ ] 결과 종합 & 인사이트 도출
- [ ] Go/Pivot/No-Go 결정
- [ ] 후속 액션 정의

## Validation 방법론

| 방법 | 적합 상황 | 기간 |
|------|----------|------|
| **5DAY_SPRINT** | 솔루션 컨셉 검증 | 5일 |
| **INTERVIEW** | 고객 Pain 검증 | 1-2주 |
| **DATA_ANALYSIS** | 가설 정량 검증 | 1주 |
| **BUYER_REVIEW** | 예산/구매의사 확인 | 3-5일 |
| **POC** | 기술 실현가능성 | 2-4주 |

## Decision Criteria

```
IF 성공 기준 70%+ 달성:
    decision = "GO"
    → Pilot-ready (S3) 진입
    
ELIF 성공 기준 40-70% 달성:
    decision = "PIVOT"
    → Brief 수정 후 재검증
    
ELSE:
    decision = "NO_GO"
    → Archive
```

## 출력 예시

```json
{
  "validation_id": "VAL-2025-001",
  "brief_id": "BRF-2025-001",
  "method": "5DAY_SPRINT",
  "decision": "GO",
  "findings": [
    "상담사 10명 중 8명이 실시간 제안 유용하다고 응답",
    "AHT 예상 감소율 12-18%",
    "CTI 연동 기술적 가능 확인"
  ],
  "evidence_links": [
    "https://confluence.../sprint-result",
    "https://figma.../prototype"
  ],
  "next_actions": [
    "Pilot 범위 확정 미팅 (1/20)",
    "데이터 접근 권한 요청",
    "PM 연결"
  ],
  "validated_at": "2025-01-24T18:00:00Z"
}
```

## 사용법

```
/ax:sprint --brief-id BRF-2025-001 --method 5DAY_SPRINT
```
