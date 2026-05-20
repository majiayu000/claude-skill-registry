---
name: code-changelog
description: AI가 만든 모든 코드 변경사항을 reviews 폴더에 기록하고 간단한 HTML 뷰어로 웹 브라우저에서 실시간 확인할 수 있습니다. 매 수정마다 문서가 생성되고 Python 서버로 즉시 확인 가능합니다.
---

# Code Changelog with Simple HTML Viewer

AI가 생성한 모든 코드 변경사항을 reviews 폴더에 기록하고, 간단한 HTML 뷰어로 브라우저에서 실시간으로 확인할 수 있는 솔루션입니다.

## 🎯 핵심 기능

- ✅ **자동 문서 생성**: 매 수정마다 reviews 폴더에 MD 파일 생성
- ✅ **간단한 HTML 뷰어**: 설치 불필요, Python만으로 작동
- ✅ **자동 index.html 업데이트**: 새 문서 추가 시 자동으로 파일 목록 갱신
- ✅ **실시간 서버**: http://localhost:4000에서 즉시 확인
- ✅ **다크 모드 UI**: GitHub 스타일의 아름다운 문서 사이트
- ✅ **네비게이션**: 자동 파일 목록 생성으로 쉬운 탐색
- ✅ **Markdown 렌더링**: 코드 하이라이팅 및 diff 표시
- ✅ **최신 문서 우선**: 가장 최근 작성한 문서가 기본으로 표시됨

## 🚀 빠른 시작

### 1. 초기 설정 (최초 1회)

```bash
# 설치 불필요! Python만 있으면 OK
python3 create_changelog.py
```

### 2. 개발하면서 사용

```python
from code_changelog_tracker import CodeChangeLogger

# 로거 생성
logger = CodeChangeLogger("프로젝트명", user_request="요구사항")

# 변경사항 기록
logger.log_file_creation("main.py", "코드", "이유")
logger.save_and_build()  # 저장!
```

### 3. 문서 서버 실행

```bash
# reviews 폴더에서 Python 서버 실행
cd reviews
python3 -m http.server 4000

# 브라우저에서 확인
# http://localhost:4000
```

**또는 백그라운드 실행:**
```bash
cd reviews && python3 -m http.server 4000 &
```

## 📁 프로젝트 구조

```
your-project/
├── reviews/                    # 문서 루트
│   ├── index.html             # HTML 뷰어 (자동 생성)
│   ├── README.md              # 홈페이지
│   ├── SUMMARY.md             # 네비게이션 (자동 생성)
│   │
│   ├── 20251020_140000.md    # 변경 이력 1
│   ├── 20251020_140530.md    # 변경 이력 2
│   ├── 20251020_141200.md    # 변경 이력 3
│   └── ...
│
├── code_changelog_tracker.py  # 로거 스크립트
└── create_changelog.py         # 변경사항 기록 스크립트
```

## 💡 사용 시나리오

### 시나리오 1: 연속 개발하면서 문서화

```python
logger = CodeChangeLogger("로그인 기능")

# 첫 번째 작업
logger.log_file_creation("auth.py", "def login(): pass", "로그인 함수")
logger.save_and_build()
# → reviews/20251020_140000.md 생성
# → index.html 자동 업데이트 (파일 목록에 추가)
# → 기본 페이지가 20251020_140000.md로 변경

# 두 번째 작업
logger.log_file_modification("auth.py", "old", "new", "암호화 추가")
logger.save_and_build()
# → reviews/20251020_140530.md 생성
# → index.html 자동 업데이트 (파일 목록 갱신)
# → 기본 페이지가 20251020_140530.md로 변경

# 세 번째 작업
logger.log_file_creation("test_auth.py", "test code", "테스트")
logger.save_and_build()
# → reviews/20251020_141200.md 생성
# → index.html 자동 업데이트 (파일 목록 갱신)
# → 기본 페이지가 20251020_141200.md로 변경

# 브라우저에서 http://localhost:4000 방문
# → 최신 문서가 자동으로 표시됨!
# → 좌측 네비게이션에서 이전 버전들도 확인 가능
```

### 시나리오 2: 백그라운드 서버 실행

```bash
# 터미널 1: 문서 서버 실행 (계속 켜둠)
cd reviews && python3 -m http.server 4000

# 터미널 2: 개발 작업
python3 your_dev_script.py  # logger.save_and_build() 호출

# 브라우저 새로고침하여 최신 문서 확인!
```

### 시나리오 3: 팀 공유

```bash
# reviews 폴더를 팀원들과 공유
# GitHub Pages, Netlify 등에 배포
# 또는 내부 웹서버에 호스팅
```

## 🛠️ 구현 코드

### code_changelog_tracker.py (메인 로거)

이미 생성된 파일 사용. 주요 메서드:
- `log_file_creation()` - 파일 생성 기록
- `log_file_modification()` - 파일 수정 기록
- `log_file_deletion()` - 파일 삭제 기록
- `update_index_html()` - index.html 파일 목록 자동 업데이트 ⭐ NEW!
- `save_and_build()` - 저장 + SUMMARY 업데이트 + index.html 업데이트

### reviews/index.html (HTML 뷰어)

**자동으로 생성 및 업데이트됩니다!** `save_and_build()` 호출 시 매번 최신 파일 목록으로 갱신됩니다.

제공 기능:
- Markdown 자동 렌더링 (marked.js)
- 다크 모드 UI (GitHub 스타일)
- 파일 목록 네비게이션 (자동 업데이트)
- 코드 하이라이팅
- 최신 문서가 기본으로 표시됨
- 활성 링크 하이라이트

## 📋 간단한 사용법

### 1단계: 변경사항 기록

```python
# create_changelog.py 예시
from code_changelog_tracker import CodeChangeLogger

logger = CodeChangeLogger(
    "Daily Signal App - 회원 가입 기능",
    user_request="이메일/비밀번호 기반 회원 가입 구현"
)

# 파일 생성 기록
logger.log_file_creation(
    "lib/screens/signup_screen.dart",
    "SignUpScreen 코드...",
    "회원 가입 화면 구현"
)

# 파일 수정 기록
logger.log_file_modification(
    "lib/providers/auth_provider.dart",
    "old code",
    "new code",
    "signUp 메서드 추가"
)

# 저장
logger.save_and_build()
```

### 2단계: 서버 실행

```bash
cd reviews
python3 -m http.server 4000
```

### 3단계: 브라우저에서 확인

```
http://localhost:4000
```

## 🎨 HTML 뷰어 특징

### 다크 모드 UI
- GitHub 스타일의 마크다운 렌더링
- 코드 블록 하이라이팅
- 반응형 레이아웃

### 네비게이션
- 좌측에 파일 목록 자동 표시
- 날짜/시간별 정렬
- 클릭으로 쉬운 이동

### Markdown 렌더링
- 제목, 목록, 코드 블록 지원
- Diff 표시
- 이모지 지원

## 💻 명령어 가이드

### 서버 시작
```bash
cd reviews
python3 -m http.server 4000
```

### 포트 변경
```bash
python3 -m http.server 3000
python3 -m http.server 8080
```

### 백그라운드 실행
```bash
cd reviews && python3 -m http.server 4000 &
```

### 서버 종료
```bash
# 포그라운드: Ctrl+C
# 백그라운드: 프로세스 ID 찾아서 종료
lsof -ti:4000 | xargs kill -9
```

## 🔧 포트 설정

### 기본 포트: 4000
```bash
python3 -m http.server 4000
# → http://localhost:4000
```

### 다른 포트 사용
```bash
python3 -m http.server 3000
# → http://localhost:3000
```

### 포트 충돌 해결
```bash
# 다른 포트 사용
python3 -m http.server 4001

# 또는 기존 프로세스 종료
lsof -ti:4000 | xargs kill -9
```

## 🌐 배포 옵션

### GitHub Pages
```bash
# reviews 폴더를 gh-pages 브랜치에 푸시
git subtree push --prefix reviews origin gh-pages
```

### Netlify
```bash
# Netlify에 reviews 폴더 배포
# Build command: (없음)
# Publish directory: reviews
```

### Vercel
```bash
# Vercel에 reviews 폴더 배포
vercel reviews
```

## 📝 Best Practices

1. **서버 항상 실행**: 개발 중에는 서버를 계속 켜두기
2. **작은 단위**: 각 작업을 작은 단위로 나누어 문서화
3. **명확한 제목**: 프로젝트명을 명확하게 작성
4. **정기적 백업**: reviews 폴더를 Git으로 관리
5. **브라우저 북마크**: http://localhost:4000 북마크 추가

## 🎓 활용 예시

### 회원 가입 기능 구현
```python
logger = CodeChangeLogger(
    "Daily Signal App - 회원 가입",
    user_request="이메일/비밀번호 회원 가입 기능"
)

# CustomTextField 생성
logger.log_file_creation(
    "lib/widgets/custom_text_field.dart",
    "CustomTextField 코드...",
    "재사용 가능한 입력 필드 위젯"
)

# SignUpScreen 생성
logger.log_file_creation(
    "lib/screens/signup_screen.dart",
    "SignUpScreen 코드...",
    "회원 가입 화면 구현"
)

# AuthProvider 수정
logger.log_file_modification(
    "lib/providers/auth_provider.dart",
    "old code",
    "new code with signUp",
    "signUp 메서드 추가"
)

# 저장
logger.save_and_build()

# 서버에서 확인: http://localhost:4000
```

## 🚨 문제 해결

### 포트가 이미 사용 중
```bash
# 다른 포트 사용
python3 -m http.server 4001

# 또는 프로세스 종료
lsof -ti:4000 | xargs kill -9
```

### 파일이 표시되지 않음
```bash
# index.html이 있는지 확인
ls reviews/index.html

# 없으면 logger.save_and_build() 호출 시 자동 생성됨
```

**중요**: `logger.save_and_build()`를 호출하면 index.html이 자동으로 업데이트됩니다!
- 새 마크다운 파일 추가 시 파일 목록 자동 갱신
- 최신 파일이 기본 페이지로 자동 설정
- 브라우저 새로고침만으로 최신 문서 확인 가능

### Markdown이 렌더링되지 않음
- 브라우저 캐시 삭제 (Cmd+Shift+R / Ctrl+Shift+R)
- 서버 재시작
- index.html이 최신인지 확인 (save_and_build() 재실행)

## 🎯 장점

### 설치 불필요
- Node.js, npm, HonKit 설치 불필요
- Python만 있으면 즉시 사용 가능
- 의존성 없음

### 빠른 실행
- 1초 안에 서버 시작
- 즉시 문서 확인 가능

### 간단한 배포
- reviews 폴더만 배포하면 끝
- 정적 사이트로 어디든 호스팅 가능

### 자동 업데이트 ⭐ NEW!
- `save_and_build()` 호출 시 index.html 자동 갱신
- 수동 편집 불필요
- 항상 최신 파일 목록 유지
- 최신 문서가 기본 페이지로 자동 설정

## 📊 비교: HonKit vs Simple HTML

| 기능 | HonKit | Simple HTML |
|------|--------|-------------|
| 설치 | npm, Node.js 필요 | Python만 필요 |
| 빌드 시간 | 5-10초 | 즉시 |
| 의존성 | 많음 | 없음 |
| 커스터마이징 | 높음 | 중간 |
| 검색 기능 | 있음 | 브라우저 검색 |
| 배포 | _book 폴더 | reviews 폴더 |

## 라이선스

MIT License

---

**설치 불필요! Python으로 바로 실행하고 웹 브라우저에서 확인하세요!** 🎉
