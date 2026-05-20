---
name: nanobanana-visual
description: |
  나노바나나 3.0 프로를 사용해 인스타그램 카드뉴스와 유튜브 썸네일을 생성합니다.
  "카드뉴스 만들어줘", "썸네일 생성해줘" 요청 시 사용합니다.
---

# 나노바나나 비주얼 스킬

브리프를 기반으로 인스타그램 카드뉴스와 유튜브 썸네일을 생성합니다.

## 워크플로우

### 1단계: 브리프 분석
1. `outputs/brief.md` 읽기
2. 핵심 메시지 추출
3. 비주얼 가이드 확인 (카드뉴스 슬라이드, 썸네일 텍스트, 색상 톤)

### 2단계: 카드뉴스 생성
1. `.claude/skills/nanobanana-visual/references/card-news-guide.md` 참조
2. `.claude/skills/nanobanana-visual/templates/card-news-prompt.md` 템플릿 로드
3. 핵심 메시지를 5-7장 슬라이드로 구성
4. 나노바나나 API 호출
5. `outputs/visuals/card-news/` 폴더에 저장

### 3단계: 썸네일 생성
1. `.claude/skills/nanobanana-visual/references/thumbnail-guide.md` 참조
2. `.claude/skills/nanobanana-visual/templates/thumbnail-prompt.md` 템플릿 로드
3. 클릭 유도 썸네일 디자인
4. 나노바나나 API 호출
5. `outputs/visuals/thumbnail.png`로 저장

## 카드뉴스 스펙

### 구성
- **슬라이드 수**: 5-7장
- **크기**: 1080x1350px (인스타 세로형)
- **비율**: 4:5

### 슬라이드 구조
1. **슬라이드 1 (표지)**: 제목 + 후킹 문구
2. **슬라이드 2-6 (본문)**: 핵심 포인트 (1슬라이드 = 1포인트)
3. **마지막 슬라이드 (CTA)**: 저장/팔로우 유도

### 디자인 원칙
- 큰 텍스트 (모바일에서 가독성)
- 단순한 배경
- 일관된 색상 팔레트
- 아이콘/일러스트 활용

## 썸네일 스펙

### 크기
- **해상도**: 1280x720px
- **비율**: 16:9

### 구성 요소
- 제목 텍스트 (3-5단어)
- 강조 요소 (화살표, 동그라미 등)
- 인물/제품 이미지 (해당시)
- 브랜드 로고 (선택)

### 디자인 원칙
- 높은 대비 (눈에 띄게)
- 큰 텍스트 (모바일에서도 보이게)
- 감정 유발 색상
- 깔끔한 구도

## API 사용 (플레이스홀더)

```python
# 나노바나나 API 호출 예시
import requests

def generate_image(prompt: str, size: str = "1080x1350"):
    """
    나노바나나 3.0 Pro API를 통해 이미지 생성

    Args:
        prompt: 이미지 생성 프롬프트
        size: 이미지 크기 (1080x1350 카드뉴스, 1280x720 썸네일)

    Returns:
        생성된 이미지 URL
    """
    # TODO: 실제 API 키 설정
    API_KEY = "YOUR_NANOBANANA_API_KEY"
    API_URL = "https://api.nanobanana.com/v3/generate"

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "prompt": prompt,
            "size": size,
            "style": "professional",
            "quality": "high"
        }
    )

    return response.json()["image_url"]
```

## 출력

### 카드뉴스
- `outputs/visuals/card-news/slide-01.png`
- `outputs/visuals/card-news/slide-02.png`
- ...
- `outputs/visuals/card-news/slide-07.png`

### 썸네일
- `outputs/visuals/thumbnail.png`

## 참조 파일
- `.claude/skills/nanobanana-visual/references/card-news-guide.md`: 카드뉴스 디자인 가이드
- `.claude/skills/nanobanana-visual/references/thumbnail-guide.md`: 썸네일 디자인 가이드
- `.claude/skills/nanobanana-visual/templates/card-news-prompt.md`: 카드뉴스 프롬프트 템플릿
- `.claude/skills/nanobanana-visual/templates/thumbnail-prompt.md`: 썸네일 프롬프트 템플릿
