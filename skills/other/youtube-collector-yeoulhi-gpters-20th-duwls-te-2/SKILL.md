---
name: youtube-collector
description: 유튜브 채널을 등록하고 새 컨텐츠를 수집하여 자막 기반 요약을 생성하는 skill. 사용자가 (1) 유튜브 채널 등록/관리를 요청하거나, (2) 등록된 채널의 새 영상 수집을 요청하거나, (3) 유튜브 영상 요약을 요청할 때 사용. 데이터는 .reference/ 폴더에 YAML 형식으로 저장됨.
---

# YouTube Collector

등록된 유튜브 채널의 새 컨텐츠를 수집하고 자막 기반 요약을 생성.

## 사전 요구사항

**필수 패키지:**
```bash
pip install google-api-python-client youtube-transcript-api pyyaml
```

**API 키 설정:** 보안을 위해 API 키는 사용자 홈 디렉토리에 저장됨.

```bash
# API 키 설정 (대화형)
python3 scripts/setup_api_key.py

# 또는 직접 지정
python3 scripts/setup_api_key.py --api-key YOUR_API_KEY

# 현재 설정 확인
python3 scripts/setup_api_key.py --show
```

**설정 파일 경로:**
- macOS/Linux: `~/.config/youtube-collector/config.yaml`
- Windows: `%APPDATA%\youtube-collector\config.yaml`

## 워크플로우

### 1. 채널 등록

채널 URL 또는 핸들로 등록:

```bash
# 핸들로 등록
python3 scripts/register_channel.py --channel-handle @channelname --output-dir .reference/

# URL로 등록
python3 scripts/register_channel.py --channel-url "https://youtube.com/@channelname" --output-dir .reference/
```

**결과:** `.reference/channels.yaml`에 채널 정보가 추가됨.

### 2. 컨텐츠 수집

스크립트가 영상 목록 조회 + 자막 수집 + YAML 파일 저장을 자동으로 처리:

```bash
# 특정 채널 수집
python3 scripts/collect_videos.py --channel-handle @channelname --output-dir .reference/ --max-results 10

# 등록된 모든 채널 수집
python3 scripts/collect_videos.py --all --output-dir .reference/
```

**결과:** `.reference/contents/{channel_handle}/{video_id}.yaml` 파일들이 생성됨.

### 3. 요약 생성

수집 결과 JSON에서 새로 추가된 영상 확인 후, 각 영상의 YAML 파일에 summary 필드 추가:

```yaml
summary:
  source: "transcript"  # 또는 "description" (자막 없을 때)
  content: |
    ## 서론
    - 문제 제기 또는 주제 소개
    - 영상의 목적/배경

    ## 본론
    - 핵심 내용 상세 설명
    - 해결책, 방법론, 예시 등
    - 주요 포인트별 정리

    ## 결론
    - 핵심 요약
    - 시사점 또는 다음 단계
```

**요약 생성 기준:**
- `transcript.available: true` → 자막 기반 요약, `summary.source: "transcript"`
- `transcript.available: false` → 설명 기반 요약, `summary.source: "description"`

### 4. 데이터 조회

수집된 컨텐츠 확인:
- `.reference/contents/` 폴더 구조 확인
- 특정 채널/영상의 YAML 파일 읽어서 정보 제공

## 스크립트 옵션

### register_channel.py

| 옵션 | 설명 |
|------|------|
| `--channel-handle` | 채널 핸들 (@username) |
| `--channel-url` | 채널 URL |
| `--channel-id` | 채널 ID (UC...) |
| `--output-dir` | 저장 디렉토리 (기본: .reference) |

### collect_videos.py

| 옵션 | 설명 |
|------|------|
| `--channel-handle` | 특정 채널 핸들 |
| `--channel-id` | 특정 채널 ID |
| `--all` | channels.yaml의 모든 채널 처리 |
| `--output-dir` | 저장 디렉토리 (기본: .reference) |
| `--max-results` | 채널당 최대 수집 개수 (기본: 10) |
| `--language` | 자막 우선 언어 (기본: ko) |
| `--no-skip-existing` | 기존 파일 덮어쓰기 |

## 데이터 구조

상세 스키마: [references/data-schema.md](references/data-schema.md)

### 영상 데이터 예시
```yaml
video_id: "abc123"
title: "영상 제목"
published_at: "2025-12-10T10:00:00Z"
url: "https://youtube.com/watch?v=abc123"
thumbnail: "https://..."
description: "영상 설명..."
duration: "PT10M30S"
collected_at: "2025-12-13T15:00:00Z"
transcript:
  available: true
  language: "ko"
  text: "자막 전체..."
summary:
  source: "transcript"
  content: |
    ## 서론
    - 영상의 배경 및 목적

    ## 본론
    - 핵심 내용 1
    - 핵심 내용 2

    ## 결론
    - 핵심 요약
```

## 에러 처리

| 상황 | 안내 메시지 |
|------|------------|
| API 키 미설정 | "YouTube Data API 키가 필요합니다. `python3 scripts/setup_api_key.py`로 설정해주세요." |
| 채널 미등록 | "등록된 채널이 없습니다. 먼저 채널을 등록해주세요." |
| 패키지 미설치 | "필요한 패키지를 설치해주세요: `pip install google-api-python-client youtube-transcript-api pyyaml`" |
| API 할당량 초과 | "YouTube API 할당량이 초과되었습니다. 내일 다시 시도해주세요." |
