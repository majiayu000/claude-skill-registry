---
name: shorts-video-maker
description: |
  YouTube 영상에서 쇼츠 클립 3개를 자동 제작합니다.
  yt-dlp, whisper, ffmpeg 파이프라인을 사용합니다.
  "쇼츠 만들어줘", "영상 클립 추출해줘" 요청 시 사용합니다.
---

# 쇼츠 비디오 메이커 스킬

YouTube 원본 영상에서 하이라이트 구간을 추출하여 9:16 세로형 쇼츠 클립을 제작합니다.

## 필수 요구사항

### 시스템 의존성
- Python 3.8+
- yt-dlp (YouTube 다운로드)
- ffmpeg (영상 편집)
- OpenAI Whisper (음성 인식) 또는 Whisper API

### 설치
```bash
pip install yt-dlp openai-whisper
brew install ffmpeg  # macOS
# 또는 apt-get install ffmpeg  # Ubuntu
```

## 워크플로우

### 1단계: 영상 다운로드
```bash
python .claude/skills/shorts-video-maker/scripts/download_video.py \
  --url "YOUTUBE_URL" \
  --output ".claude/skills/shorts-video-maker/temp/"
```
- yt-dlp로 최고 화질 영상 다운로드
- 출력: `.claude/skills/shorts-video-maker/temp/video.mp4`

### 2단계: 자막 추출
```bash
python .claude/skills/shorts-video-maker/scripts/transcribe.py \
  --input ".claude/skills/shorts-video-maker/temp/video.mp4" \
  --output ".claude/skills/shorts-video-maker/temp/transcript.json"
```
- Whisper로 음성 → 텍스트 변환
- 타임스탬프 포함 JSON 출력
- 출력: `.claude/skills/shorts-video-maker/temp/transcript.json`

### 3단계: 쇼츠 대본 참조
- `outputs/shorts-scripts/shorts-01.md` ~ `shorts-03.md` 읽기
- 대본의 "원본 영상 참조" 섹션에서 구간 정보 확인
- 또는 transcript.json에서 매칭되는 구간 자동 탐색

### 4단계: 클립 추출 및 편집
```bash
python .claude/skills/shorts-video-maker/scripts/cut_shorts.py \
  --input ".claude/skills/shorts-video-maker/temp/video.mp4" \
  --transcript ".claude/skills/shorts-video-maker/temp/transcript.json" \
  --scripts "outputs/shorts-scripts/" \
  --output "outputs/shorts-videos/"
```
- ffmpeg로 구간 클리핑
- 9:16 비율 크롭
- 자막 하드코딩 (선택)
- 출력: `outputs/shorts-videos/shorts-01.mp4` ~ `shorts-03.mp4`

## 쇼츠 스펙

### 영상 규격
- **해상도**: 1080x1920px (세로)
- **비율**: 9:16
- **길이**: 15-60초
- **포맷**: MP4 (H.264)

### 자막 스타일
- 위치: 하단 중앙 또는 상단
- 폰트: 굵은 산세리프
- 색상: 흰색 + 검정 테두리
- 크기: 화면 너비의 80%

## 스크립트 상세

### download_video.py
- YouTube URL 입력
- 최고 화질 다운로드
- 진행률 표시
- 에러 처리

### transcribe.py
- 오디오 추출
- Whisper 모델 로드
- 세그먼트별 타임스탬프 생성
- JSON 형식 출력

### cut_shorts.py
- 시작/종료 시간 기반 클리핑
- 16:9 → 9:16 변환 (center crop)
- 자막 오버레이 (선택)
- 3개 클립 배치 처리

## 출력

### 최종 결과물
- `outputs/shorts-videos/shorts-01.mp4`
- `outputs/shorts-videos/shorts-02.mp4`
- `outputs/shorts-videos/shorts-03.mp4`

### 중간 파일
- `.claude/skills/shorts-video-maker/temp/video.mp4`: 원본 다운로드
- `.claude/skills/shorts-video-maker/temp/transcript.json`: 자막 데이터
- `.claude/skills/shorts-video-maker/temp/audio.wav`: 추출된 오디오

## 참조 파일
- `.claude/skills/shorts-video-maker/references/shorts-spec.md`: 쇼츠 플랫폼별 스펙
- `.claude/agents/marketing/shorts-scriptwriter.md`: 대본 에이전트 (연동)

## 사용 예시

```bash
# 전체 파이프라인 실행 (프로젝트 루트에서)

# 1. 다운로드
python .claude/skills/shorts-video-maker/scripts/download_video.py \
  --url "https://youtube.com/watch?v=xxxxx" \
  --output ".claude/skills/shorts-video-maker/temp/"

# 2. 자막 추출
python .claude/skills/shorts-video-maker/scripts/transcribe.py \
  --input ".claude/skills/shorts-video-maker/temp/video.mp4" \
  --output ".claude/skills/shorts-video-maker/temp/transcript.json"

# 3. 쇼츠 생성
python .claude/skills/shorts-video-maker/scripts/cut_shorts.py \
  --input ".claude/skills/shorts-video-maker/temp/video.mp4" \
  --transcript ".claude/skills/shorts-video-maker/temp/transcript.json" \
  --scripts "outputs/shorts-scripts/" \
  --output "outputs/shorts-videos/"
```

## 주의사항

1. YouTube 영상 저작권 확인 필요
2. 원본 영상이 16:9가 아닌 경우 크롭 조정 필요
3. Whisper 모델 크기에 따라 정확도/속도 트레이드오프
4. GPU 사용 시 처리 속도 향상
