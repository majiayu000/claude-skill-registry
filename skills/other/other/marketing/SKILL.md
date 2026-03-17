---
name: marketing
description: |
  URL 또는 주제를 입력받아 콘텐츠 마케팅 파이프라인 전체를 자동 실행합니다.
  8개 에이전트를 4단계 워크플로우로 오케스트레이션합니다.
  "마케팅 콘텐츠 만들어줘", "콘텐츠 마케팅 시작" 요청 시 사용합니다.
argument-hint: "[URL 또는 주제]"
user-invocable: true
agents:
  planner: marketing/planner
  shorts-scriptwriter: marketing/shorts-scriptwriter
  thread-writer: marketing/thread-writer
  newsletter-writer: marketing/newsletter-writer
  blog-writer: marketing/blog-writer
  youtube-scriptwriter: marketing/youtube-scriptwriter
  linkedin-writer: marketing/linkedin-writer
  reviewer: marketing/reviewer
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - WebFetch
  - AskUserQuestion
---

# 마케팅 팀 오케스트레이터

URL 또는 주제를 입력받아 8개 에이전트를 4단계 워크플로우로 자동 실행하여 콘텐츠 마케팅 파이프라인을 완성합니다.

## 입력 모드

두 가지 방식으로 사용할 수 있다:

| 모드 | 입력 | 예시 |
|------|------|------|
| **URL 모드** | 웹 URL | `/marketing https://example.com/article` |
| **주제 모드** | 주제/키워드 직접 입력 | `/marketing AI 코딩 도구의 미래` |

입력이 `http://` 또는 `https://`로 시작하면 URL 모드, 아니면 주제 모드로 동작한다.

## 워크플로우 개요

```
Phase 1: 입력(URL/주제) → planner → outputs/brief.md             [순차]
Phase 2: brief.md → [6 에이전트 병렬] → 콘텐츠 6종               [병렬]
Phase 3: (선택) shorts-video-maker / nanobanana-visual            [선택]
Phase 4: 전체 outputs → reviewer → outputs/review-report.md      [순차]
```

## Phase 1: 브리프 생성 (순차)

### 1-1. 입력 확인

입력이 없으면 AskUserQuestion으로 요청한다:

```
질문: "마케팅 콘텐츠의 소스를 알려주세요."
선택지:
  1. URL 입력 — 기존 웹 콘텐츠를 분석하여 마케팅 콘텐츠 생성
  2. 주제 직접 입력 — 원하는 주제/아이디어를 설명하여 콘텐츠 생성
```

### 1-2. 출력 디렉토리 생성

```bash
mkdir -p outputs/shorts-scripts outputs/threads outputs/visuals/card-news outputs/shorts-videos
```

### 1-3. planner 에이전트 호출

입력 모드에 따라 프롬프트를 분기한다.

**URL 모드:**
```
subagent_type: planner
prompt: |
  다음 URL의 콘텐츠를 분석하여 마케팅 브리프를 작성하세요.
  URL: {URL}
  outputs/brief.md 파일로 저장하세요.
```

**주제 모드:**
```
subagent_type: planner
prompt: |
  다음 주제에 대한 마케팅 브리프를 작성하세요.
  주제: {TOPIC}
  웹 검색을 통해 관련 정보를 수집하고, 핵심 메시지를 도출하세요.
  outputs/brief.md 파일로 저장하세요.
```

### 1-4. 결과 확인

`outputs/brief.md` 파일이 생성되었는지 확인한다. 실패 시 사용자에게 알린다.

## Phase 2: 콘텐츠 생성 (병렬)

6개 에이전트를 **단일 메시지에서 Task tool 6회 동시 호출**하여 병렬 실행한다.

### 에이전트별 프롬프트

각 에이전트에게 동일한 구조의 프롬프트를 전달한다:

1. `outputs/brief.md`를 읽는다
2. 에이전트 고유 지침을 따른다
3. 지정된 출력 파일에 작성한다

### 에이전트-출력 매핑

| Agent | subagent_type | Output |
|-------|---------------|--------|
| shorts-scriptwriter | `shorts-scriptwriter` | `outputs/shorts-scripts/shorts-01.md` ~ `shorts-03.md` |
| thread-writer | `thread-writer` | `outputs/threads/thread-01.md` ~ `thread-10.md` |
| newsletter-writer | `newsletter-writer` | `outputs/newsletter.md` |
| blog-writer | `blog-writer` | `outputs/blog.md` |
| youtube-scriptwriter | `youtube-scriptwriter` | `outputs/youtube-script.md` |
| linkedin-writer | `linkedin-writer` | `outputs/linkedin.md` |

### 호출 예시

```
# 단일 메시지에서 6개 Task tool 동시 호출

Task(subagent_type="shorts-scriptwriter", prompt="outputs/brief.md를 읽고 쇼츠 대본 3개를 작성하세요. outputs/shorts-scripts/shorts-01.md ~ shorts-03.md로 저장하세요.")
Task(subagent_type="thread-writer", prompt="outputs/brief.md를 읽고 X 스레드 10개를 작성하세요. outputs/threads/thread-01.md ~ thread-10.md로 저장하세요.")
Task(subagent_type="newsletter-writer", prompt="outputs/brief.md를 읽고 뉴스레터를 작성하세요. outputs/newsletter.md로 저장하세요.")
Task(subagent_type="blog-writer", prompt="outputs/brief.md를 읽고 블로그 글을 작성하세요. outputs/blog.md로 저장하세요.")
Task(subagent_type="youtube-scriptwriter", prompt="outputs/brief.md를 읽고 유튜브 대본을 작성하세요. outputs/youtube-script.md로 저장하세요.")
Task(subagent_type="linkedin-writer", prompt="outputs/brief.md를 읽고 링크드인 포스트를 작성하세요. outputs/linkedin.md로 저장하세요.")
```

## Phase 3: 미디어 생성 (선택)

Phase 2 완료 후 AskUserQuestion으로 사용자에게 선택지를 제시한다:

```
질문: "미디어 콘텐츠를 추가로 생성하시겠습니까?"
선택지:
  1. 쇼츠 영상 제작 (shorts-video-maker) — YouTube URL 필요, 외부 도구(yt-dlp, whisper, ffmpeg) 필요
  2. 비주얼 생성 (nanobanana-visual) — 카드뉴스 + 썸네일
  3. 둘 다
  4. 건너뛰기
```

### 선택에 따른 실행

- **쇼츠 영상 제작**: Skill tool로 `shorts-video-maker` 호출
- **비주얼 생성**: Skill tool로 `nanobanana-visual` 호출
- **둘 다**: 두 스킬을 순차 호출
- **건너뛰기**: Phase 4로 진행

## Phase 4: 검수 (순차)

### 4-1. reviewer 에이전트 호출

Task tool로 reviewer 에이전트를 호출한다.

```
subagent_type: reviewer
prompt: |
  outputs/ 디렉토리의 모든 콘텐츠를 outputs/brief.md와 대조하여 검수하세요.
  브랜드 톤 일관성, 팩트 체크, 플랫폼별 스펙을 검증하세요.
  검수 결과를 outputs/review-report.md로 저장하세요.
```

### 4-2. 결과 요약

`outputs/review-report.md`를 읽고 검수 결과를 사용자에게 요약 출력한다:
- 전체 통과/실패 상태
- 에이전트별 품질 점수
- 수정 필요 항목 목록

## 에러 처리

| 상황 | 처리 |
|------|------|
| 입력 없음 | AskUserQuestion으로 URL 또는 주제 요청 |
| 에이전트 실패 | 실패한 에이전트만 재실행 가능하도록 안내 |
| 부분 완료 | 리뷰어가 존재하는 출력만 검수 |
| brief.md 미생성 | Phase 2 진행 불가, 사용자에게 알림 |

## 사용 예시

```
# URL 모드
/marketing https://youtube.com/watch?v=xxxxx
/marketing https://example.com/article

# 주제 모드
/marketing AI 코딩 도구의 미래와 개발자 생산성
/marketing 2026년 SaaS 트렌드 분석
마케팅 콘텐츠 만들어줘 클라우드 네이티브 앱 개발 방법론
```

## 출력 디렉토리 구조

```
outputs/
├── brief.md                          # Phase 1: 브리프
├── newsletter.md                     # Phase 2: 뉴스레터
├── blog.md                           # Phase 2: 블로그
├── linkedin.md                       # Phase 2: 링크드인 포스트
├── youtube-script.md                 # Phase 2: 유튜브 대본
├── shorts-scripts/                   # Phase 2: 쇼츠 대본
│   ├── shorts-01.md
│   ├── shorts-02.md
│   └── shorts-03.md
├── threads/                          # Phase 2: X 스레드
│   ├── thread-01.md
│   ├── ...
│   └── thread-10.md
├── shorts-videos/                    # Phase 3 (선택): 쇼츠 영상
│   ├── shorts-01.mp4
│   ├── shorts-02.mp4
│   └── shorts-03.mp4
├── visuals/                          # Phase 3 (선택): 비주얼
│   ├── card-news/
│   │   ├── slide-01.png
│   │   └── ...
│   └── thumbnail.png
└── review-report.md                  # Phase 4: 검수 보고서
```

## 에이전트 참조 테이블

| Agent | 파일 경로 | 모델 | 주요 출력 |
|-------|----------|------|----------|
| planner | `.claude/agents/marketing/planner.md` | sonnet | `outputs/brief.md` |
| shorts-scriptwriter | `.claude/agents/marketing/shorts-scriptwriter.md` | haiku | `outputs/shorts-scripts/shorts-01~03.md` |
| thread-writer | `.claude/agents/marketing/thread-writer.md` | haiku | `outputs/threads/thread-01~10.md` |
| newsletter-writer | `.claude/agents/marketing/newsletter-writer.md` | sonnet | `outputs/newsletter.md` |
| blog-writer | `.claude/agents/marketing/blog-writer.md` | sonnet | `outputs/blog.md` |
| youtube-scriptwriter | `.claude/agents/marketing/youtube-scriptwriter.md` | sonnet | `outputs/youtube-script.md` |
| linkedin-writer | `.claude/agents/marketing/linkedin-writer.md` | haiku | `outputs/linkedin.md` |
| reviewer | `.claude/agents/marketing/reviewer.md` | sonnet | `outputs/review-report.md` |
