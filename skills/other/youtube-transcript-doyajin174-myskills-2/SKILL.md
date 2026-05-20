---
name: youtube-transcript
description: Download and process YouTube video transcripts using yt-dlp. Use this when extracting subtitles, creating summaries from videos, or processing video content.
allowed-tools: Read, Glob, Grep, Bash, Write
license: MIT
metadata:
  author: michalparkola
  version: "1.0"
---

# YouTube Transcript Downloader

유튜브 영상에서 자막을 추출하고 처리하는 스킬입니다.

## Priority Order

```
1. yt-dlp 설치 확인
2. 사용 가능한 자막 목록 확인
3. 수동 자막 우선 시도
4. 자동 생성 자막 폴백
5. 최후 수단: Whisper 변환
```

## Requirements

```bash
# macOS
brew install yt-dlp

# Linux
sudo apt install yt-dlp

# Universal
pip install yt-dlp
```

## Workflow

### Step 1: 자막 목록 확인

```bash
yt-dlp --list-subs "VIDEO_URL"
```

### Step 2: 수동 자막 다운로드 (권장)

```bash
# 한국어 자막
yt-dlp --write-sub --sub-lang ko --skip-download "VIDEO_URL"

# 영어 자막
yt-dlp --write-sub --sub-lang en --skip-download "VIDEO_URL"
```

### Step 3: 자동 생성 자막 (폴백)

```bash
yt-dlp --write-auto-sub --sub-lang ko --skip-download "VIDEO_URL"
```

### Step 4: VTT → 텍스트 변환

```bash
# VTT 파일에서 타임스탬프 제거
sed '/^[0-9]/d; /^$/d; /-->/d' subtitle.ko.vtt > transcript.txt
```

## Output Processing

### 중복 제거
자동 생성 자막은 progressive 캡션으로 인해 중복이 많음:

```python
# 중복 라인 제거
seen = set()
unique_lines = []
for line in lines:
    if line not in seen:
        seen.add(line)
        unique_lines.append(line)
```

### 요약 생성
추출된 자막으로:
- 핵심 내용 요약
- 타임스탬프별 챕터 생성
- 주요 키워드 추출

## Examples

### Example 1: 강의 영상 요약
```
User: 이 유튜브 강의 요약해줘 - https://youtube.com/watch?v=xxx

Claude:
1. yt-dlp로 자막 다운로드
2. VTT → 텍스트 변환
3. 핵심 내용 요약 생성
4. 타임스탬프별 목차 제공
```

### Example 2: 다국어 자막 추출
```
User: 이 영상의 영어/한국어 자막 둘 다 추출해줘

Claude:
1. --list-subs로 가용 언어 확인
2. 각 언어별 자막 다운로드
3. 정리된 텍스트 파일 제공
```

## Error Handling

| 에러 | 원인 | 해결책 |
|------|------|--------|
| `yt-dlp not found` | 미설치 | brew/apt/pip 설치 |
| `No subtitles available` | 자막 없음 | Whisper 사용 제안 |
| `Invalid URL` | URL 오류 | URL 형식 확인 |
| `Video unavailable` | 비공개/삭제 | 사용자에게 알림 |

## Whisper Fallback

자막이 전혀 없는 경우 (사용자 확인 필요):

```bash
# 파일 크기 확인
yt-dlp --print filesize "VIDEO_URL"

# 사용자 승인 후 오디오 다운로드
yt-dlp -x --audio-format mp3 "VIDEO_URL"

# Whisper로 변환
whisper audio.mp3 --language ko --model base
```

**주의**: 대역폭/처리 시간 소요로 사용자 확인 필수
