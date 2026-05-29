---
name: verify-product
description: 화장품 제품 정보 검증 프로세스. 수집된 제품 정보의 진위여부를 확인하고 공식 출처를 검증합니다.
allowed-tools: WebSearch, WebFetch, Read, Write
user-invocable: true
---

# Verify Product Skill

화장품 제품 정보의 진위를 검증하는 팩트체킹 스킬입니다.

## 사용법

```
/verify-product [제품명]
또는
/verify-product [리서치파일경로]
```

## 실행 프로세스

### Step 1: 공식 정보 확인
1. 브랜드 공식 웹사이트 검색
2. 제품 페이지 존재 여부 확인
3. 공식 가격/용량 정보 수집

### Step 2: 교차 검증
검색 대상:
- 올리브영/세포라 등 공식 판매처
- 네이버 쇼핑/쿠팡 가격 비교
- 화해/글로우픽 등 뷰티 앱 리뷰
- 뷰티 전문 매체 기사

### Step 3: 출처 신뢰도 평가

| 등급 | 기준 | 설명 |
|------|------|------|
| A | 공식 확인 | 브랜드 공식 사이트/공식 판매처 확인 |
| B | 복수 확인 | 2개 이상 신뢰 출처에서 확인 |
| C | 단일 확인 | 1개 출처에서만 확인 |
| D | 미확인 | 공식 확인 불가, 추가 검증 필요 |

### Step 4: 검증 리포트 생성

## 출력 형식

```json
{
  "verification_date": "YYYY-MM-DD",
  "product": {
    "brand": "브랜드명",
    "name": "제품명",
    "claimed_info": {
      "price": "주장된 가격",
      "source": "원본 출처"
    }
  },
  "verification_result": {
    "status": "verified/partial/unverified",
    "confidence_level": "A/B/C/D",
    "checks": {
      "product_exists": true,
      "price_accurate": true,
      "brand_confirmed": true,
      "source_accessible": true
    }
  },
  "official_info": {
    "official_url": "공식 제품 페이지 URL",
    "official_price": "공식 가격",
    "volume": "용량",
    "key_ingredients": ["성분1", "성분2"]
  },
  "additional_sources": [
    {
      "name": "출처명",
      "url": "URL",
      "info": "확인된 정보"
    }
  ],
  "notes": "검증 과정 메모",
  "recommendation": "사용 권장 여부"
}
```

## 검증 체크리스트

- [ ] 브랜드 공식 사이트에서 제품 확인
- [ ] 제품 단종 여부 확인
- [ ] 가격 정보 정확성 확인
- [ ] 공식 판매처 URL 확보
- [ ] 성분 정보 확인 (선택)
- [ ] 출처 URL 접근 가능 여부

## 주의사항

- 병행수입 제품은 별도 표기
- 단종/리뉴얼 제품 주의
- 가격은 정가 기준 (할인가 X)
- 검증 불가 시 정직하게 표기

## 다음 단계

검증 완료 후 권장 스킬:
1. `/create-script` - 검증된 정보로 스크립트 작성
