---
name: research-cosmetics
description: 연예인 화장품 리서치 프로세스. 연예인명을 입력하면 해당 연예인의 SNS를 분석하여 실제 사용 화장품 정보를 수집합니다.
allowed-tools: WebSearch, WebFetch, Read, Write
user-invocable: true
---

# Research Cosmetics Skill

연예인이 실제 사용하는 화장품 정보를 수집하는 리서치 스킬입니다.

## 사용법

```
/research-cosmetics [연예인명]
```

## 실행 프로세스

### Step 1: SNS 채널 탐색
1. "[연예인명] 공식 유튜브" 검색
2. "[연예인명] 공식 인스타그램" 검색
3. 공식 계정 여부 확인 (인증 마크, 팔로워 수)

### Step 2: 화장품 콘텐츠 탐색
검색 키워드:
- "[연예인명] 화장품"
- "[연예인명] 스킨케어"
- "[연예인명] 겟레디윗미"
- "[연예인명] GRWM"
- "[연예인명] 뷰티 루틴"
- "[연예인명] 파우치 공개"

### Step 3: 정보 수집
각 제품에 대해 수집할 정보:
- 브랜드명
- 제품명
- 카테고리 (스킨케어/메이크업/헤어/바디)
- 출처 URL
- 언급 맥락 (추천/일상 사용/협찬)
- 협찬 여부

### Step 4: 결과 저장
결과물을 다음 경로에 저장:
```
data/research/[연예인명]_[날짜].json
```

## 출력 형식

```json
{
  "celebrity": {
    "name": "연예인명",
    "youtube": "채널 URL",
    "instagram": "계정 URL"
  },
  "research_date": "YYYY-MM-DD",
  "products": [
    {
      "brand": "브랜드명",
      "product_name": "제품명",
      "category": "스킨케어",
      "price_range": "가격대",
      "source": {
        "platform": "youtube/instagram",
        "url": "출처 URL",
        "date": "콘텐츠 날짜"
      },
      "context": "사용 맥락 설명",
      "is_sponsored": false,
      "confidence": "high/medium/low"
    }
  ],
  "summary": {
    "total_products": 10,
    "categories": {
      "skincare": 4,
      "makeup": 5,
      "hair": 1
    },
    "top_brands": ["브랜드1", "브랜드2"]
  }
}
```

## 주의사항

- 최근 1년 이내 콘텐츠 우선
- 협찬/광고 콘텐츠 명확히 구분
- 출처 없는 정보는 수집하지 않음
- 추측 정보는 confidence: low로 표기

## 다음 단계

리서치 완료 후 권장 스킬:
1. `/verify-product` - 제품 정보 검증
2. `/create-script` - 스크립트 작성
