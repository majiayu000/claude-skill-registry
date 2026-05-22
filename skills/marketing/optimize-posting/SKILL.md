---
name: optimize-posting
description: TikTok/인스타그램 포스팅 최적화. 트렌드 해시태그 분석, 최적 업로드 시간 추천, 캡션 생성을 수행합니다.
allowed-tools: WebSearch, WebFetch, Read, Write
user-invocable: true
---

# Optimize Posting Skill

숏폼 콘텐츠 포스팅을 최적화하는 스킬입니다.

## 사용법

```
/optimize-posting [플랫폼]
```

플랫폼 옵션:
- `tiktok` - TikTok 최적화
- `instagram` - Instagram Reels 최적화
- `youtube` - YouTube Shorts 최적화
- `all` - 모든 플랫폼 (기본값)

## 실행 프로세스

### Step 1: 트렌드 해시태그 분석
현재 인기 해시태그 검색:
- 뷰티/화장품 카테고리
- 연예인 관련
- 플랫폼별 추천 태그

### Step 2: 해시태그 조합 생성
구성 비율:
```
대형 태그 (100만+ 게시물): 3-5개
중형 태그 (10만-100만): 5-7개
소형 태그 (1만-10만): 5-7개
니치 태그 (1만 이하): 2-3개
```

### Step 3: 최적 업로드 시간 추천
한국 기준 (KST):
| 요일 | 최적 시간 | 차선 시간 |
|------|----------|----------|
| 평일 | 12:00-13:00 | 18:00-21:00 |
| 주말 | 10:00-12:00 | 20:00-22:00 |

### Step 4: 캡션/설명 생성
플랫폼별 최적화된 캡션 작성

## 출력 형식

```json
{
  "platform": "tiktok",
  "analysis_date": "YYYY-MM-DD",

  "hashtags": {
    "primary": [
      "#연예인화장품",
      "#셀럽뷰티",
      "#뷰티틱톡"
    ],
    "secondary": [
      "#화장품추천",
      "#스킨케어루틴",
      "#겟레디윗미"
    ],
    "niche": [
      "#[연예인이름]화장품",
      "#[브랜드]추천"
    ],
    "total_count": 15
  },

  "posting_schedule": {
    "recommended_time": "12:30 KST",
    "day_of_week": "화요일",
    "reason": "점심시간 최대 활성 사용자"
  },

  "caption": {
    "main_text": "[연예인]이 실제로 쓰는 화장품 TOP 3 공개! 출처도 다 있어요",
    "call_to_action": "저장해두고 쇼핑할 때 참고하세요",
    "character_count": 85
  },

  "description": {
    "full_text": "상세 설명 텍스트...",
    "source_credits": "출처: [URL1], [URL2]",
    "disclaimer": "* 협찬 아님, 직접 리서치한 정보입니다"
  }
}
```

## 플랫폼별 가이드

### TikTok
```yaml
caption_limit: 2200자
hashtag_limit: 제한 없음 (권장 15-20개)
link_in_bio: 지원
sound_credit: 필수
```

### Instagram Reels
```yaml
caption_limit: 2200자
hashtag_limit: 30개 (권장 15-20개)
link_in_bio: 지원
collaborator_tag: 지원
```

### YouTube Shorts
```yaml
title_limit: 100자
description_limit: 5000자
hashtag_limit: 3개 (제목에 표시)
cards_endscreen: 미지원
```

## 해시태그 카테고리

### 연예인 관련
```
#연예인화장품 #셀럽뷰티 #스타뷰티템
#아이돌스킨케어 #연예인추천템 #연예인파우치
```

### 화장품 카테고리
```
#화장품추천 #스킨케어루틴 #데일리메이크업
#뷰티템추천 #화장품리뷰 #겟레디윗미
```

### 플랫폼 최적화
```
#틱톡뷰티 #뷰티틱톡 #릴스추천
#쇼츠추천 #뷰티쇼츠 #추천떠라
```

### 행동 유도
```
#저장해요 #팔로우 #좋아요
#댓글 #공유해줘
```

## 체크리스트

- [ ] 해시태그 15-20개 선정
- [ ] 캡션 작성 완료
- [ ] 업로드 시간 확정
- [ ] 출처 표기 확인
- [ ] 썸네일 준비
- [ ] 음원 저작권 확인

## 다음 단계

포스팅 최적화 완료 후:
1. 영상 업로드
2. 댓글 모니터링
3. 성과 분석 (24시간/48시간/7일)
