---
name: export
description: PDF/PPTX 내보내기가 필요할 때
---

# 이력서/경력기술서/포트폴리오 내보내기

## 개요

이력서/경력기술서를 **PDF**로, 포트폴리오를 **PPTX**로 내보냅니다.

| 포맷 | 대상 | 용도 | 특징 |
|------|------|------|------|
| **PDF** | 이력서, 경력기술서 | 채용 제출, 이메일 첨부 | 페이지 끊김 방지 최적화 |
| **PPTX** | 포트폴리오 | Tech Lead/CTO 면접, 화면 발표 | AWS 스타일 아키텍처 다이어그램 |

---

## 파일명 규칙

> **파일명 형식**: `윤원희_[문서타입]_YYYY-MM.pdf`
> - **YYYY-MM**: 현재 날짜 기준 (예: 2026-01)

---

## 템플릿 종류

### 1. 기본 (Colorful)
- 컬러풀한 디자인, 아이콘 사용
- Font Awesome 아이콘 포함
- 그라데이션, 배경색 활용

### 2. 모던 (Modern) - Black & White
- 미니멀한 흑백 디자인
- 아이콘 최소화, 타이포그래피 중심
- 프로젝트별 페이지 이분할 레이아웃
- 컨텍스트 그리드 (배경/문제 영역 분리)

---

## PDF 내보내기

### 핵심 원칙

> **PDF 출력 요청 시 기본 + 모던 두 가지 형식을 모두 생성합니다.**

### PDF 생성 명령어 (Edge Headless)

```bash
# Windows - 기본 형식 (YYYY-MM을 현재 날짜로 교체)
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="C:\workspace\younwony.github.io\output\윤원희_이력서_YYYY-MM.pdf" --no-margins "file:///C:/workspace/younwony.github.io/templates/export/pdf/resume-2page.html"

"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="C:\workspace\younwony.github.io\output\윤원희_경력기술서_YYYY-MM.pdf" --no-margins "file:///C:/workspace/younwony.github.io/templates/export/pdf/career-portfolio.html"

# Windows - 모던 형식
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="C:\workspace\younwony.github.io\output\윤원희_이력서_Modern_YYYY-MM.pdf" --no-margins "file:///C:/workspace/younwony.github.io/templates/export/pdf/resume-modern.html"

"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="C:\workspace\younwony.github.io\output\윤원희_경력기술서_Modern_YYYY-MM.pdf" --no-margins "file:///C:/workspace/younwony.github.io/templates/export/pdf/career-portfolio-modern.html"
```

> **중요**: 위 명령어의 `YYYY-MM`을 현재 날짜로 교체하세요!

### 출력 파일 목록 (총 4개)

```
output/
├── 윤원희_이력서_YYYY-MM.pdf           # 기본 (컬러풀)
├── 윤원희_이력서_Modern_YYYY-MM.pdf    # 모던 (흑백)
├── 윤원희_경력기술서_YYYY-MM.pdf       # 기본 (컬러풀)
└── 윤원희_경력기술서_Modern_YYYY-MM.pdf # 모던 (흑백)
```

---

## 템플릿 파일 구조

```
templates/export/pdf/
├── resume-2page.html           # 이력서 - 기본 (3페이지)
├── resume-modern.html          # 이력서 - 모던 (3페이지)
├── career-portfolio.html       # 경력기술서 - 기본 (5페이지+)
└── career-portfolio-modern.html # 경력기술서 - 모던 (5페이지)
```

---

## 모던 템플릿 특징

### 디자인 원칙

| 항목 | 기본 | 모던 |
|------|------|------|
| 색상 | 컬러풀 (그라데이션) | 흑백 (#000, #333, #666) |
| 아이콘 | Font Awesome | 최소화 (텍스트 중심) |
| 레이아웃 | 자유 배치 | 페이지 이분할 (50%/50%) |
| 컨텍스트 | 한 줄 텍스트 | 그리드 분리 (배경/문제) |

### 모던 레이아웃 구조

```
┌─────────────────────────────────────────────┐
│ 프로젝트 제목                    2024.01-현재 │
│ 역할: 백엔드 아키텍처 설계 주도                │
├─────────────────────────────────────────────┤
│ [Metrics: 100x | 20x | 100% | Zero]         │
├──────────────────────┬──────────────────────┤
│ 배경 (Situation)     │ 문제 (Problem)        │
│ - 상황 설명          │ - 해결해야 할 문제    │
├──────────────────────┴──────────────────────┤
│ [주요 성과 및 해결 방법]                      │
│ - 성과 1: 설명                               │
│ - 성과 2: 설명                               │
├─────────────────────────────────────────────┤
│ Tech Decision (Why)                          │
│ - 기술 선택 이유 1                            │
│ - 기술 선택 이유 2                            │
├─────────────────────────────────────────────┤
│ [Spring Boot] [Elasticsearch] [Redis]        │
└─────────────────────────────────────────────┘
```

---

## PDF 생성 체크리스트

### 필수 생성 항목

- [ ] 이력서 - 기본 형식 (resume-2page.html)
- [ ] 이력서 - 모던 형식 (resume-modern.html)
- [ ] 경력기술서 - 기본 형식 (career-portfolio.html)
- [ ] 경력기술서 - 모던 형식 (career-portfolio-modern.html)

### 확인 사항

- [ ] 각 페이지가 자연스럽게 구성됨
- [ ] 섹션/프로젝트가 중간에 잘리지 않음
- [ ] 모던 형식: 프로젝트가 페이지 50%씩 균등 분할
- [ ] 여백이 균일함
- [ ] output 폴더에 4개 PDF 생성됨

---

## 수동 내보내기 (브라우저)

### Step 1: HTML 파일 열기

```bash
# Windows - 기본 형식
start templates/export/pdf/resume-2page.html
start templates/export/pdf/career-portfolio.html

# Windows - 모던 형식
start templates/export/pdf/resume-modern.html
start templates/export/pdf/career-portfolio-modern.html
```

### Step 2: 인쇄 미리보기 (Ctrl+P)

**필수 설정:**
- 대상: "PDF로 저장"
- 용지 크기: A4
- 여백: **없음** 또는 **최소**
- 배경 그래픽: **체크**

### Step 3: PDF 저장

---

## 용도별 권장 포맷

| 상황 | 권장 포맷 |
|------|----------|
| **채용 사이트 제출** | PDF (기본 or 모던) |
| **이메일 첨부** | PDF (모던 권장) |
| **면접 자료** | PDF |
| **보수적인 기업** | PDF (모던 권장) |
| **스타트업/IT기업** | PDF (기본 or 모던) |

---

## 문제 해결

### PDF

| 문제 | 해결 |
|------|------|
| 배경색이 인쇄 안 됨 | 인쇄 설정에서 "배경 그래픽" 체크 |
| 섹션이 잘림 | `page-break-inside: avoid` 적용 |
| 페이지 여백이 너무 큼 | 인쇄 설정에서 여백 "없음" |
| 아이콘이 안 보임 | Font Awesome CDN 연결 확인 (기본만) |
| 한글 깨짐 | 폰트 지정: 'Malgun Gothic' |
| 모던 하단 여백 많음 | `justify-content: space-between` 확인 |

---

## PPTX 내보내기 (포트폴리오)

### 생성 명령어

```bash
# 포트폴리오 PPTX 생성
node scripts/pptx/generate-portfolio.js
```

### 출력 파일

```
output/
└── 윤원희_포트폴리오_YYYY-MM.pptx    # 11 슬라이드
```

### 슬라이드 구성

| 슬라이드 | 내용 |
|----------|------|
| 1 | Title (이름, 직책, 연락처) |
| 2 | Executive Summary (역량, 핵심 메트릭) |
| 3-8 | Key Projects × 3 (아키텍처 + 결과) |
| 9 | Technical Decisions (설계 원칙) |
| 10 | Technical Skills (숙련도 바) |
| 11 | Contact & Q&A |

### 디자인 스타일

- **배경**: #232F3E (AWS 다크 네이비)
- **악센트**: #FF9900 (AWS 오렌지)
- **아이콘**: AWS 공식 아이콘 (aws-svg-icons)

### 상세 가이드

> PPTX 상세 가이드는 `/export-pptx` 스킬 참조

---

## 관련 스킬

- `/write-resume`: 이력서 작성 (2-3페이지)
- `/write-career`: 경력기술서 작성 (5페이지+)
- `/write-portfolio`: 포트폴리오 작성 (Markdown)
- `/export-pptx`: 포트폴리오 PPTX 상세 가이드
- `/style-guide`: CSS 스타일 수정 가이드
