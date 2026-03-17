---
name: interview-script
description: 면접 스크립트 작성 및 PDF 내보내기가 필요할 때
---

# 면접 스크립트 작성

> **원본 데이터**: `docs/career/my_career_data.md` (SSOT)
> **출력 위치**: `private/by-company/{company}/interview-script.md`
> **PDF 템플릿**: `private/exports/{company}/interview-script.html`

---

## 개요

면접 대비용 스크립트를 작성하고 PDF로 내보냅니다.

---

## 입출력

| 구분 | 파일 |
|------|------|
| **입력** | `docs/career/my_career_data.md` (원본 데이터) |
| | `/jd-match` 결과 (회사 조사, JD 분석) |
| **출력** | `private/by-company/{company}/interview-script.md` |
| | `private/exports/{company}/interview-script.html` |
| | `output/윤원희_{company}_면접스크립트_YYYY-MM.pdf` |

---

## 문서 구조 (4 Parts)

### Part 1: 인성 면접 (8 섹션)

| 섹션 | 주제 | 핵심 포인트 |
|------|------|-------------|
| 1 | 자기소개 | 3문장 (연차+강점+성과+방향) |
| 2 | 이직 사유 | 긍정적 동기, 성장 지향 |
| 3 | 왜 우리 회사? | 회사 조사 기반 구체적 이유 |
| 4 | 장점/단점 | 업무 관련 장점, 개선 중인 단점 |
| 5 | 갈등 해결 | 구체적 사례, 해결 과정 |
| 6 | 압박 대처 | 실제 경험, 대응 방법 |
| 7 | 5년 후 목표 | 회사와 연계된 커리어 계획 |
| 8 | 질문하기 | 팀 문화, 기술 방향 질문 |

### Part 2: 기술 면접 (9 섹션)

| 섹션 | 주제 | 핵심 포인트 |
|------|------|-------------|
| 9 | 최근 프로젝트 | STAR 형식, 정량적 성과 |
| 10 | 기술적 의사결정 | Why 중심, Trade-off |
| 11 | 트러블슈팅 | 문제→분석→해결→결과 |
| 12 | 성능 최적화 | Before/After 수치 |
| 13 | 시스템 설계 | 요구사항→아키텍처→확장성 |
| 14 | 기술 스택 선택 | 비교 분석, 선택 이유 |
| 15 | 코드 품질 | TDD, 리팩토링, 코드 리뷰 |
| 16 | 레거시 전환 | 점진적 마이그레이션 |
| 17 | 운영 경험 | 모니터링, 장애 대응 |

### Part 3: 경험 면접 (7 섹션)

| 섹션 | 주제 | 핵심 포인트 |
|------|------|-------------|
| 18 | 팀 리딩 | 역할, 방법론, 성과 |
| 19 | 주니어 멘토링 | 구체적 멘토링 방법 |
| 20 | 비개발자 협업 | 소통 방식, 성공 사례 |
| 21 | 실패 경험 | 원인 분석, 학습 포인트 |
| 22 | 자기 개발 | 학습 방법, 기술 트렌드 |
| 23 | 리모트 경험 | 협업 도구, 소통 방식 |
| 24 | 연봉 협상 | 시장 가치 기반 논리 |

### Part 4: 심화 대응 (3 섹션)

| 섹션 | 주제 | 핵심 포인트 |
|------|------|-------------|
| 25 | 회사/도메인 특화 | 회사 서비스 이해, 기여 포인트 |
| 26 | Follow-up/압박 질문 | 추가 질문 패턴, 압박 대응 |
| 27 | 시니어 역할 질문 | 리더십, 의사결정, 문화 기여 |

---

## 작성 가이드라인

### 1. STAR 형식

```markdown
**[Situation]**: 당시 상황/배경 (1-2문장)
**[Task]**: 맡은 역할/목표 (1문장)
**[Action]**: 구체적 행동 (2-3문장, 기술적 의사결정 포함)
**[Result]**: 정량적 성과 (숫자 필수)
```

### 2. Q&A 블록 구조

```markdown
### Q. 질문 내용

**[핵심 메시지]**
> 1-2문장으로 답변의 핵심 요약

**[상세 답변]**
- 구체적인 내용
- 예시/사례 포함
- 정량적 수치 강조

**[연결 포인트]**
- 후속 질문 대비
- 회사 연결점
```

### 3. 회사별 커스터마이징

```markdown
**필수 반영 항목:**
1. 회사 비전/미션 연결
2. 도메인 특화 질문 추가
3. JD 키워드 반영
4. 인재상 키워드 활용
```

---

## PDF 템플릿 구조

### HTML 파일 위치

```
private/exports/{company}/interview-script.html
```

### 기본 CSS 설정

```css
@page {
    size: A4;
    margin: 15mm 15mm 12mm 15mm;
}

body {
    font-family: 'Malgun Gothic', sans-serif;
    font-size: 10pt;
    line-height: 1.5;
}
```

### 주요 CSS 클래스

| 클래스 | 용도 |
|--------|------|
| `.part-header` | Part 제목 (Part 1, Part 2...) |
| `.part-header-new-page` | 새 페이지 시작 Part |
| `.section` | 개별 섹션 컨테이너 |
| `.section-new-page` | 새 페이지 시작 섹션 |
| `.question` | 질문 블록 |
| `.answer-card` | 답변 카드 |
| `.key-message` | 핵심 메시지 박스 |
| `.star-detail` | STAR 형식 상세 내용 |

### 페이지 나누기 제어

```css
/* 새 페이지 시작 */
.section-new-page {
    page-break-before: always;
}

.part-header-new-page {
    page-break-before: always;
}

/* 섹션 내 끊김 방지 */
.answer-card {
    page-break-inside: avoid;
}

.question {
    page-break-inside: avoid;
}
```

---

## PDF 내보내기

### Edge Headless 명령어

```bash
# 면접 스크립트 PDF 생성
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="C:\workspace\younwony.github.io\output\윤원희_{company}_면접스크립트_YYYY-MM.pdf" --no-pdf-header-footer "file:///C:/workspace/younwony.github.io/private/exports/{company}/interview-script.html"
```

### 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--headless` | GUI 없이 실행 |
| `--disable-gpu` | GPU 비활성화 (안정성) |
| `--print-to-pdf` | PDF 출력 경로 |
| `--no-pdf-header-footer` | 머리글/바닥글 제거 (**@page margin과 함께 사용**) |

### 파일명 규칙

```
윤원희_{회사명}_면접스크립트_YYYY-MM.pdf
```

---

## 작성 프로세스

### Step 1: 회사 조사

```markdown
1. 회사 비전/미션 확인
2. 주요 서비스/기술 스택 조사
3. 최근 동향 (뉴스, 기술 블로그)
4. 인재상 키워드 추출
```

### Step 2: Markdown 작성

```markdown
**출력 파일:**
private/by-company/{company}/interview-script.md

**구조:**
1. 표지 (회사명, 버전, 작성일)
2. 목차 (4 Parts, 27 Sections)
3. Part 1-4 내용
4. 체크리스트
```

### Step 3: HTML 템플릿 작성

```markdown
**파일:** private/exports/{company}/interview-script.html

**작업:**
1. Markdown → HTML 변환
2. 회사별 스타일 적용
3. 페이지 나누기 조정
4. 목차 업데이트
```

### Step 4: PDF 생성

```bash
# PDF 생성 및 확인
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="output/윤원희_{company}_면접스크립트_YYYY-MM.pdf" --no-pdf-header-footer "file:///C:/workspace/younwony.github.io/private/exports/{company}/interview-script.html"
```

---

## 체크리스트

### 내용 점검

- [ ] Part 1: 인성 면접 (8섹션) 완료
- [ ] Part 2: 기술 면접 (9섹션) 완료
- [ ] Part 3: 경험 면접 (7섹션) 완료
- [ ] Part 4: 심화 대응 (3섹션) 완료
- [ ] 모든 답변에 STAR 형식 적용
- [ ] 정량적 성과 수치 포함
- [ ] 회사 비전/인재상 반영

### PDF 점검

- [ ] 페이지 상단 여백 적정 (15mm)
- [ ] 섹션 중간 끊김 없음
- [ ] 목차와 본문 페이지 일치
- [ ] 머리글/바닥글 없음
- [ ] 폰트 렌더링 정상

---

## 문제 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| 머리글/바닥글 표시됨 | `--no-margins` 사용 | `--no-pdf-header-footer` 로 변경 |
| 상단 여백 없음 | body padding만 적용 | `@page { margin: 15mm }` 추가 |
| 섹션 중간 끊김 | page-break 미적용 | `.answer-card { page-break-inside: avoid }` |
| 빈 페이지 많음 | 과도한 page-break | 불필요한 `.section-new-page` 제거 |

---

## 관련 스킬

- `/jd-match`: 회사 조사 및 JD 분석
- `/writing-guide`: STAR+I 작성 원칙
- `/export`: PDF 내보내기 가이드
- `/style-guide`: CSS 스타일 수정

---

## 참고: 기존 스크립트

> 실제 예시는 기존 파일 참조

```
private/by-company/{company}/interview-script.md
private/exports/{company}/interview-script.html
```
