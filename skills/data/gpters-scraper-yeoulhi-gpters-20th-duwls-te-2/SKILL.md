---
name: gpters-scraper
description: 지피터스(gpters.org) 멤버 프로필에서 게시물을 스크래핑하여 Markdown으로 저장. "지피터스 게시물 수집", "gpters 스크랩", "editor_소연 게시물", "프로필 크롤링" 등을 언급하면 자동 실행. Selenium 기반 동적 페이지 수집.
---

# gpters Scraper

지피터스 멤버 프로필에서 게시물을 자동 수집하여 로컬 Markdown 파일로 저장합니다.

## 사전 요구사항

### 필수 패키지

```bash
pip install selenium webdriver-manager beautifulsoup4 lxml
```

### 설치 확인

```bash
python -c "import selenium; print(f'Selenium {selenium.__version__}')"
python -c "import bs4; print('BeautifulSoup 설치됨')"
```

**Chrome 브라우저**: Windows 11에 기본 탑재되어 있으며, ChromeDriver는 자동으로 설치됩니다 (webdriver-manager).

---

## 사용 방법

### 기본 실행 (최근 10개 게시물)

```bash
python scripts/scrape_posts.py --profile-url "https://www.gpters.org/member/WZlPiwwnpW"
```

### 추가 옵션

```bash
# 최근 20개 게시물 수집
python scripts/scrape_posts.py --profile-url "URL" --max-results 20

# 헤드리스 모드 (백그라운드 실행)
python scripts/scrape_posts.py --profile-url "URL" --headless

# 중복 파일 덮어쓰기
python scripts/scrape_posts.py --profile-url "URL" --no-skip

# 출력 경로 변경
python scripts/scrape_posts.py --profile-url "URL" --output-dir "내_경로/"
```

---

## 옵션 설명

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--profile-url` | 프로필 URL (필수) | - |
| `--max-results` | 최대 수집 개수 | 10 |
| `--output-dir` | 저장 디렉토리 | `docs/notes/gpters_editor_soyeon/` |
| `--headless` | 헤드리스 모드 (브라우저 숨김) | False |
| `--no-skip` | 중복 파일 덮어쓰기 | False (중복 건너뜀) |

---

## 출력 형식

### 저장 경로
```
docs/notes/gpters_editor_soyeon/
├── 20260106_Claude_Code_자동화.md
├── 20250105_GPT_활용_가이드.md
└── ...
```

### Markdown 파일 예시

```markdown
# Claude Code로 업무 자동화 시작하기

- **작성일**: 2025-01-06
- **URL**: [https://www.gpters.org/post/abc123](https://www.gpters.org/post/abc123)

## 요약
Claude Code를 활용하여 반복적인 업무를 자동화하는 방법에 대해 설명합니다.

---

**수집 일시**: 2025-01-06 14:30:15
```

---

## 실행 결과

### 성공 시 JSON 출력

```json
{
  "status": "success",
  "profile_url": "https://www.gpters.org/member/WZlPiwwnpW",
  "collected_at": "2025-01-06T14:30:15",
  "collected": 10,
  "saved": 8,
  "skipped": 2,
  "saved_files": [
    "20260106_Claude_Code_자동화.md",
    "20250105_GPT_활용_가이드.md"
  ],
  "errors": []
}
```

### 실패 시 JSON 출력

```json
{
  "status": "error",
  "collected": 0,
  "saved": 0,
  "skipped": 0,
  "saved_files": [],
  "errors": [
    {
      "type": "critical",
      "message": "Page load failed: no such element"
    }
  ]
}
```

---

## 에러 처리

### 일반적인 문제

#### 1. ChromeDriver 설치 실패
```
✗ ChromeDriver installation failed
```
**해결책**: Chrome 브라우저가 설치되어 있는지 확인하세요.

#### 2. 페이지 로딩 타임아웃
```
✗ Page load failed: Timeout waiting for element
```
**해결책**: 네트워크 연결을 확인하거나 잠시 후 다시 시도하세요.

#### 3. 게시물 요소를 찾을 수 없음
```
✗ no such element: Unable to locate element
```
**해결책**: 지피터스 페이지 구조가 변경되었을 수 있습니다. `references/selector-guide.md`를 참조하세요.

#### 4. 한글 파일명 저장 오류 (Windows)
**해결책**: UTF-8 인코딩이 자동으로 적용되므로 추가 설정 불필요합니다.

---

## 워크플로우

### 1단계: 페이지 접속
- Chrome 브라우저 시작
- 프로필 URL로 이동
- JavaScript 렌더링 완료 대기 (5초)

### 2단계: 게시물 파싱
- 동적으로 로드된 게시물 목록 대기 (최대 15초)
- BeautifulSoup으로 HTML 파싱
- 제목, URL, 작성일, 요약 추출

### 3단계: Markdown 저장
- `docs/notes/gpters_editor_soyeon/` 디렉토리 생성
- 파일명: `YYYYMMDD_title.md` 형식
- 중복 파일 자동 건너뜀 (--no-skip으로 덮어쓰기 가능)
- UTF-8 인코딩으로 한글 정상 저장

### 4단계: 결과 출력
- JSON 형식으로 결과 출력
- 저장 파일 목록 출력

---

## Claude Code와 통합

### 자동 트리거

사용자가 다음 중 하나를 언급하면 자동으로 이 Skill을 실행합니다:

- "지피터스 게시물 수집"
- "gpters 스크랩"
- "editor_소연님 게시물"
- "프로필 크롤링"
- "지피터스에서 글 가져오기"

### 사용 예시

**사용자**:
```
editor_소연님의 지피터스 게시물 최근 15개 수집해줘
```

**Claude Code 응답**:
```
15개 게시물을 수집하여 12개 파일을 저장했습니다.

저장 위치: docs/notes/gpters_editor_soyeon/

신규 저장: 12개
- 20260106_Claude_Code_자동화.md
- 20250105_GPT_활용_가이드.md
...

건너뜬 중복: 3개
```

---

## 데이터 구조

상세 문서: [references/selector-guide.md](references/selector-guide.md)

### 수집 데이터

각 게시물에서 추출되는 정보:

- **title** (string): 게시물 제목
- **url** (string): 게시물 링크 (절대 URL)
- **published_date** (string): 작성일 (YYYY-MM-DD 형식)
- **summary** (string): 게시물 요약 또는 본문 일부 (최대 200자)

---

## 고급 사용법

### 여러 프로필 수집

```bash
# editor_소연
python scripts/scrape_posts.py --profile-url "https://www.gpters.org/member/WZlPiwwnpW" --max-results 20

# 다른 멤버
python scripts/scrape_posts.py --profile-url "https://www.gpters.org/member/OTHER_ID" --output-dir "docs/notes/gpters_other/"
```

### 배치 처리 (여러 프로필 순회)

Python 스크립트 작성:
```python
import subprocess
import json

profiles = [
    ("https://www.gpters.org/member/ID1", "profile1"),
    ("https://www.gpters.org/member/ID2", "profile2"),
]

for url, name in profiles:
    result = subprocess.run(
        ["python", "scripts/scrape_posts.py",
         "--profile-url", url,
         "--output-dir", f"docs/notes/gpters_{name}"],
        capture_output=True,
        text=True
    )
    output = json.loads(result.stdout)
    print(f"{name}: {output['saved']}개 저장, {output['skipped']}개 건너뜀")
```

---

## 유지보수

### 페이지 구조 변경 시

지피터스 페이지가 변경되면 `references/selector-guide.md`를 참조하여 CSS Selector를 업데이트하세요.

**수정 단계**:
1. Chrome DevTools (F12)에서 게시물 요소 구조 확인
2. `scrape_posts.py`의 Selector 값 업데이트
3. 작은 규모로 테스트 (`--max-results 3`)
4. 성공 시 full run 실행

### 로깅 활성화 (개발용)

Python 스크립트에 다음 추가:
```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

---

## 문제 해결 팁

### 브라우저 창이 제대로 로드되지 않는 경우

```bash
# GUI 모드에서 실행해서 상태 확인
python scripts/scrape_posts.py --profile-url "URL" --max-results 5

# (헤드리스 모드는 나중에)
```

### Selector 찾기

1. Chrome에서 https://www.gpters.org/member/WZlPiwwnpW 방문
2. F12 → Elements 탭
3. 게시물 요소 우클릭 → "Inspect" 또는 Ctrl+Shift+C로 선택
4. HTML 구조 확인

---

## FAQ

**Q**: 스케줄링은 지원하나요?

**A**: MVP에는 수동 실행만 포함되어 있습니다. 자동 스케줄링이 필요하면 `APScheduler` 또는 Windows 작업 스케줄러를 별도로 설정하세요.

**Q**: 게시물 본문 전체를 수집할 수 있나요?

**A**: 현재는 제목, URL, 작성일, 요약만 수집합니다. 본문 전체 수집은 향후 업데이트 예정입니다.

**Q**: 이미지도 다운로드되나요?

**A**: 현재는 Markdown 텍스트만 저장합니다. 이미지 다운로드는 향후 기능 추가 예정입니다.

**Q**: 프록시 설정이 필요한가요?

**A**: 기본 설정은 프록시 없이 작동합니다. 필요시 `scrape_posts.py`의 `setup_driver()` 함수를 수정하세요.

---

## 관련 리소스

- [references/selector-guide.md](references/selector-guide.md) - CSS Selector 유지보수 가이드
- [Selenium 공식 문서](https://www.selenium.dev/documentation/)
- [BeautifulSoup 공식 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**버전**: 1.0.0 MVP
**최종 업데이트**: 2025-01-06
**상태**: Ready for Use ✅
