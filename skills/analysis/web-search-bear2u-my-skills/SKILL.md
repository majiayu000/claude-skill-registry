---
name: web-search
description: DuckDuckGo를 사용한 웹 검색. 텍스트, 뉴스, 이미지 검색을 지원. 빌트인 WebSearch가 제한적이거나, 뉴스/이미지 검색, 지역/기간 필터가 필요할 때 사용. "검색해줘", "찾아줘", "search", "뉴스 검색", "이미지 검색" 등의 요청 시 활성화.
---

# DuckDuckGo Web Search

DuckDuckGo 검색 엔진을 활용한 텍스트, 뉴스, 이미지 검색 스킬.

## When to Use

다음 상황에서 사용:
- 빌트인 WebSearch를 사용할 수 없을 때 (US 외 지역)
- 뉴스 전용 검색이 필요할 때
- 이미지 URL을 검색해야 할 때
- 검색 결과를 JSON으로 저장하거나 프로그래밍적으로 처리해야 할 때
- 시간 범위(일/주/월/년)를 세밀하게 지정해야 할 때
- 특정 지역(한국, 일본 등) 기준 검색 결과가 필요할 때

빌트인 WebSearch를 우선 사용하는 경우:
- US 지역의 단순 텍스트 검색
- 빠른 사실 확인

## Core Workflow

### Step 1: 검색 유형 판별

사용자 요청에서 검색 유형 파악:
- **텍스트 검색** (기본): 일반적인 웹 검색
- **뉴스 검색**: "뉴스", "최근 소식", "news" 키워드 포함
- **이미지 검색**: "이미지", "사진", "image", "picture" 키워드 포함

### Step 2: 스크립트 실행

```bash
python3 ~/.claude/skills/web-search/scripts/search.py -q "검색어" -t text -n 5
```

### Step 3: 결과 정리

JSON 출력을 사용자에게 읽기 좋은 형태로 정리하여 전달.

## Parameters

| 파라미터 | 필수 | 기본값 | 설명 |
|----------|------|--------|------|
| `-q` | Yes | - | 검색 키워드 |
| `-t` | No | text | text, news, images |
| `-n` | No | 5 | 최대 결과 수 |
| `-r` | No | wt-wt | 지역 코드 |
| `-s` | No | moderate | SafeSearch: on, moderate, off |
| `-p` | No | None | 기간: d(일), w(주), m(월), y(년) |

### 주요 지역 코드
- 전세계: `wt-wt` | 한국: `kr-kr` | 미국: `us-en` | 일본: `jp-jp` | 영국: `uk-en`

## Examples

### 텍스트 검색
```bash
python3 ~/.claude/skills/web-search/scripts/search.py -q "Claude Code Anthropic" -t text -n 5
```

### 한국 뉴스 검색 (최근 1주)
```bash
python3 ~/.claude/skills/web-search/scripts/search.py -q "AI 인공지능" -t news -n 10 -r kr-kr -p w
```

### 이미지 검색
```bash
python3 ~/.claude/skills/web-search/scripts/search.py -q "modern web design" -t images -n 5
```

### 결과를 파일로 저장
```bash
python3 ~/.claude/skills/web-search/scripts/search.py -q "React 19" -t text -n 20 > results.json
```

## 검색 연산자

query에 포함하여 사용:
- `site:example.com` - 특정 사이트 내 검색
- `filetype:pdf` - 특정 파일 유형
- `"exact phrase"` - 정확한 구문
- `-exclude` - 특정 단어 제외

## Error Handling

- **Rate Limit**: 잠시 후 재시도하거나 결과 수를 줄임
- **Timeout**: 네트워크 확인 후 재시도
- **패키지 미설치**: 스크립트가 자동 설치 시도. 실패 시 `pip install -U ddgs` 수동 실행
