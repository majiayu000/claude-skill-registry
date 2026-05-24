---
name: generate-video
description: Python moviepy를 활용한 숏폼 영상 자동 생성. 스크립트를 기반으로 자막, 이미지, BGM이 포함된 영상을 생성합니다.
allowed-tools: Read, Write, Bash
user-invocable: true
---

# Generate Video Skill

스크립트 기반 숏폼 영상을 자동 생성하는 스킬입니다.

## 사용법

```
/generate-video [프로젝트명]
```

## 필수 요구사항

### Python 패키지
```bash
pip install moviepy pillow numpy
```

### 폴더 구조
```
project/
├── scripts/
│   └── [프로젝트명].md      # 스크립트 파일
├── assets/
│   ├── images/              # 연예인/제품 이미지
│   │   ├── celebrity.jpg
│   │   └── product_1.jpg
│   ├── audio/               # BGM 파일
│   │   └── bgm.mp3
│   └── fonts/               # 폰트 파일
│       └── Pretendard-Bold.ttf
└── output/                  # 출력 폴더
```

## 실행 프로세스

### Step 1: 스크립트 파싱
1. `scripts/[프로젝트명].md` 파일 읽기
2. 섹션별 타임코드 추출
3. 자막 텍스트 추출

### Step 2: 에셋 준비 확인
- 이미지 파일 존재 확인
- BGM 파일 확인
- 폰트 파일 확인

### Step 3: 영상 생성
```bash
python .claude/skills/generate-video/scripts/video_generator.py \
  --script "scripts/[프로젝트명].md" \
  --assets "assets/" \
  --output "output/[프로젝트명].mp4" \
  --resolution 1080x1920 \
  --fps 30
```

### Step 4: 검수
- 영상 길이 확인 (60초 이내)
- 자막 가독성 확인
- 오디오 싱크 확인

## Python 스크립트 사용법

```bash
# 기본 실행
python video_generator.py --script script.md --output output.mp4

# 옵션
--script      스크립트 파일 경로 (필수)
--assets      에셋 폴더 경로 (기본: assets/)
--output      출력 파일 경로 (기본: output/video.mp4)
--resolution  해상도 (기본: 1080x1920)
--fps         프레임레이트 (기본: 30)
--preview     미리보기 모드 (저해상도)
```

## 영상 스펙

| 항목 | 값 |
|------|-----|
| 해상도 | 1080 x 1920 (9:16) |
| 프레임레이트 | 30 fps |
| 코덱 | H.264 |
| 최대 길이 | 60초 |
| 파일 형식 | MP4 |

## 자막 스타일 설정

```python
subtitle_style = {
    "font": "Pretendard-Bold",
    "fontsize": 48,
    "color": "white",
    "stroke_color": "black",
    "stroke_width": 2,
    "position": ("center", 0.85)  # 하단 15% 위치
}
```

## 트러블슈팅

### 일반적인 오류
1. **ImageMagick 필요**: `brew install imagemagick`
2. **폰트 오류**: 폰트 경로 확인 또는 시스템 폰트 사용
3. **메모리 부족**: `--preview` 모드로 먼저 테스트

### 대체 방법
moviepy가 어려운 경우:
1. FFmpeg 직접 사용
2. 편집 지시서만 생성 후 수동 편집

## 출력 파일

```
output/
├── [프로젝트명].mp4           # 최종 영상
├── [프로젝트명]_preview.mp4   # 미리보기 (저해상도)
└── [프로젝트명]_log.txt       # 생성 로그
```

## 다음 단계

영상 생성 완료 후:
1. `/optimize-posting` - 포스팅 최적화
2. 수동 검수 및 최종 수정
