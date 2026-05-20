---
name: ax-seminar
description: "세미나 Activity 생성 — Activity + AAR 템플릿"
---

# AX Seminar Skill

세미나/컨퍼런스 참석을 Activity → AAR → Signal로 자동 전환합니다.

## 입력
- 세미나 URL/메타 정보
- 관심 테마 키워드

## 출력
- Activity JSON
- AAR(After Action Review) 템플릿
- Signal 2개 (최소)

## Workflow (WF-01)

```
세미나 등록 → Activity 생성 → 캘린더 등록
    ↓
참석 완료 → AAR 작성 (24h 이내)
    ↓
AAR에서 Signal 추출 (최소 2개)
    ↓
Confluence Live doc에 기록
    ↓
Play DB QTD 업데이트
```

## Activity 자동 생성 필드

| 필드 | 소스 | 예시 |
|------|------|------|
| title | 세미나 제목 | "AI Summit 2025" |
| source | 고정값 | "대외" |
| channel | 고정값 | "데스크리서치" |
| play_id | 라우팅 규칙 | "EXT_Desk_D01_Seminar" |
| url | 입력값 | "https://..." |
| date | 파싱/입력 | "2025-01-20" |
| status | 초기값 | "REGISTERED" |

## AAR 템플릿

```markdown
## After Action Review: {세미나명}

**일시**: {날짜}
**주최**: {주최사}
**참석자**: {이름}

### 1. 핵심 인사이트 (3개)
1. 
2. 
3. 

### 2. AX BD 관련성
- 관련 Play: 
- 잠재 기회:

### 3. Follow-up Actions
- [ ] 발표자료 확보
- [ ] 담당자 연락처 확보
- [ ] Signal 등록

### 4. Signal 후보
| 제목 | Pain/Need | 근거 |
|------|----------|------|
| | | |
| | | |

### 5. 종합 평가
- 참석 가치: ⭐⭐⭐⭐☆
- 재참석 의사: Y/N
```

## Signal 자동 추출 규칙

AAR에서 다음 패턴 감지 시 Signal 후보로 추출:
- "~문제가 있다", "~어려움을 겪고 있다"
- "~솔루션을 찾고 있다", "~예산이 있다"
- "~% 개선", "~비용 절감"
- "AI/ML/자동화 도입 고려"

## 출력 예시

```json
{
  "activity": {
    "activity_id": "ACT-2025-001",
    "title": "AI Summit 2025 - 금융AI 트랙",
    "source": "대외",
    "channel": "데스크리서치",
    "play_id": "EXT_Desk_D01_Seminar",
    "date": "2025-01-20",
    "status": "REGISTERED"
  },
  "aar_template_url": "https://confluence.../aar-template",
  "signals": [
    {
      "signal_id": "SIG-2025-010",
      "title": "금융사 AML 자동화 니즈",
      "pain": "수동 AML 심사로 인한 지연",
      "evidence": [{"type": "meeting_note", "url": "..."}]
    }
  ]
}
```

## 사용법

```
/ax:seminar-add https://event.example.com/ai-summit-2025 --theme AI,금융,자동화
```
