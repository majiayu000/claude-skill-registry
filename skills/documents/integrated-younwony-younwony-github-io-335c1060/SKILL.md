---
name: write-integrated
description: JD 기반 통합 지원서 HTML 작성이 필요할 때
---

# 통합 지원서 작성 (경력기술서 + 지원동기)

> **용도**: JD(채용공고) 분석 후 맞춤형 통합 지원서 HTML 작성
> **참조 템플릿**: `templates/export/pdf/integrated-application.html`

---

## 개요

JD 분석 결과를 바탕으로 경력기술서와 지원동기를 하나의 HTML 문서로 통합 작성합니다.

### 문서 구성

```
Page 1: Summary, Core Competencies, Skills, Work Experience
Page 2-3: 주요 프로젝트 상세 (STAR 형식)
Page 4: 추가 프로젝트 + 이전 회사 경력
Page 5: 지원 동기 + Education
```

### 사전 요구사항

1. `/jd-match` 실행 완료 (회사 조사, JD 분석, 경험 매칭)
2. 원본 데이터 확인 (`docs/career/my_career_data.md`)

---

## HTML 템플릿 스타일 가이드

### 페이지 설정

```css
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important; }
body {
    font-family: 'Malgun Gothic', -apple-system, sans-serif;
    font-size: 9pt; line-height: 1.5; color: #222;
}
.page {
    width: 210mm; height: 297mm; padding: 14mm 18mm;
    page-break-after: always;
}
.page:last-child { page-break-after: avoid; }
```

### 헤더 스타일

```css
.header {
    text-align: center;
    border-bottom: 2px solid #000;
    padding-bottom: 14px;
    margin-bottom: 16px;
}
.header h1 {
    font-size: 20pt;
    font-weight: 700;
    letter-spacing: 4px;
}
.header-info { font-size: 10pt; color: #333; }
.header-contact { font-size: 9pt; color: #666; }
.header-contact span { margin: 0 10px; }
```

### 섹션 타이틀

```css
.section-title {
    font-size: 9.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #000;
    background: linear-gradient(90deg, #f8f8f8 0%, #fff 50%);
    padding: 8px 10px 6px 10px;
    margin: 0 -10px 12px -10px;
}
```

### Company Header (검정 배경)

```css
.company-header {
    display: flex;
    justify-content: space-between;
    padding: 8px 12px;
    background: #000;
    color: #fff;
    margin-bottom: 12px;
}
.company-name { font-size: 10pt; font-weight: 600; }
.company-period { font-size: 9pt; }
```

### Values Header (지원동기 페이지)

```css
.values-header {
    display: flex;
    justify-content: space-between;
    padding: 10px 14px;
    background: linear-gradient(90deg, #f5f5f5 0%, #fff 100%);
    border: 2px solid #000;
    margin-bottom: 16px;
}
.values-header .company-name {
    color: #000; font-size: 11pt; font-weight: 700; letter-spacing: 1px;
}
```

### Metrics Row (성과 지표)

```css
.metrics-row { display: flex; gap: 6px; margin-bottom: 10px; }
.metric-box {
    flex: 1;
    text-align: center;
    padding: 6px 4px;
    background: #f8f8f8;
    border-left: 2px solid #000;
}
.metric-value { font-size: 11pt; font-weight: 700; color: #000; }
.metric-label { font-size: 7pt; color: #666; text-transform: uppercase; }
.metric-detail { font-size: 6.5pt; color: #888; }
```

### Context Grid (배경/문제)

```css
.context-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}
.context-box {
    padding: 8px 10px;
    background: #fafafa;
    border-left: 2px solid #888;
    font-size: 7.5pt;
}
.context-label {
    font-size: 6.5pt; font-weight: 600; color: #666;
    text-transform: uppercase; letter-spacing: 0.5px;
}
```

### Tech Decision Box

```css
.tech-decision {
    padding: 8px 10px;
    background: #f5f5f5;
    border-left: 2px solid #000;
    margin-bottom: 8px;
}
.tech-decision-title {
    font-size: 7pt; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px;
    border-bottom: 1px solid #ddd;
    margin-bottom: 5px; padding-bottom: 3px;
}
.tech-decision-item { font-size: 7pt; color: #444; line-height: 1.5; }
```

### JD Tag (키워드 강조)

```css
.jd-tag {
    display: inline-block;
    font-size: 6.5pt;
    background: #000;
    color: #fff !important;
    padding: 2px 5px;
    margin-left: 4px;
    font-weight: 600;
}
```

### Tech Stack Tags

```css
.tech-stack {
    margin-top: auto;
    padding-top: 8px;
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}
.tech-tag {
    font-size: 6.5pt;
    padding: 3px 6px;
    border: 1px solid #ccc;
    color: #555;
}
```

---

## 프로젝트 레이아웃

### 2분할 레이아웃 (한 페이지에 2개 프로젝트)

```css
.projects-container {
    display: flex;
    flex-direction: column;
    height: calc(100% - 40px);
}
.project-half {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding-bottom: 8px;
}
.project-half:first-child {
    border-bottom: 1px dashed #ccc;
    margin-bottom: 8px;
}
.project-box {
    flex: 1;
    border: 1px solid #ddd;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
}
```

### 프로젝트 박스 구조

```html
<div class="project-box">
    <div class="project-header">
        <span class="project-title">프로젝트명 <span class="jd-tag">JD키워드</span></span>
        <span class="project-period">2024.01 - 현재</span>
    </div>
    <div class="project-role">역할: 백엔드 아키텍처 설계 주도 | 팀 협업</div>

    <div class="metrics-row">
        <div class="metric-box">
            <div class="metric-value">10x</div>
            <div class="metric-label">성과 지표</div>
            <div class="metric-detail">상세 설명</div>
        </div>
        <!-- 3-4개 metric-box -->
    </div>

    <div class="context-grid">
        <div class="context-box">
            <div class="context-label">배경</div>
            <div class="context-text">상황 설명</div>
        </div>
        <div class="context-box">
            <div class="context-label">문제</div>
            <div class="context-text">해결해야 할 문제</div>
        </div>
    </div>

    <div class="achievements-label">[주요 성과]</div>
    <ul class="achievements">
        <li><strong>성과1:</strong> 설명</li>
        <li><strong>성과2:</strong> 설명</li>
    </ul>

    <div class="tech-decision">
        <div class="tech-decision-title">Tech Decision (Why)</div>
        <div class="tech-decision-item"><strong>기술:</strong> 선택 이유</div>
    </div>

    <div class="tech-stack">
        <span class="tech-tag">Spring Boot</span>
        <span class="tech-tag">Elasticsearch</span>
    </div>
</div>
```

---

## 지원동기 페이지 구조

### 지원동기 박스

```css
.motivation-box {
    border: 1px solid #ddd;
    padding: 12px 14px;
    margin-bottom: 12px;
}
.motivation-title {
    font-size: 9pt; font-weight: 700;
    margin-bottom: 8px; padding-bottom: 6px;
    border-bottom: 1px solid #eee;
}
.motivation-text {
    font-size: 8pt; color: #333; line-height: 1.65;
}
```

### 비전-기여 테이블

```css
.vision-table {
    width: 100%; border-collapse: collapse; font-size: 8pt;
}
.vision-table th {
    background: #000; color: #fff;
    padding: 8px 10px; text-align: left;
}
.vision-table td {
    padding: 8px 10px; border-bottom: 1px solid #ddd;
}
.vision-table tr:nth-child(even) { background: #fafafa; }
```

---

## PDF 생성

### Edge Headless 명령

```bash
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" \
  --headless \
  --disable-gpu \
  --print-to-pdf="output.pdf" \
  --print-to-pdf-no-header \
  "file:///path/to/combined_resume.html"
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `--print-to-pdf-no-header` | 브라우저 머리글/바닥글 제거 |
| `--disable-gpu` | GPU 가속 비활성화 (헤드리스 안정성) |

---

## 실행 순서

### Step 1: JD 분석 (필수)

```bash
/jd-match
```

- 회사 조사 (비전, 성장, 인재상)
- JD 분석 (필수/우대 요건)
- 경험 매칭

### Step 2: HTML 작성

1. 참조 템플릿 복사: `templates/export/pdf/integrated-application.html`
2. 회사별 내용 커스터마이징
3. 위 CSS 스타일 적용
4. 프로젝트 배치 (JD 매칭 우선순위)
5. 지원동기 작성 (회사 조사 기반)

### Step 3: PDF 생성

```bash
/export  # 또는 Edge headless 직접 실행
```

### Step 4: 검토

- [ ] 5페이지 A4 구성 확인
- [ ] JD 키워드 태그 표시 확인
- [ ] 머리글/바닥글 없음 확인
- [ ] 페이지 끊김 없음 확인

---

## JD 키워드 태그 사용

JD 필수/우대 요건과 매칭되는 프로젝트에 `jd-tag` 추가:

```html
<!-- JD 필수 요건: 대용량 트래픽 처리 -->
<span class="project-title">
    인플루언서 데이터 플랫폼
    <span class="jd-tag">대용량 처리</span>
</span>

<!-- JD 우대 요건: 성능 최적화 -->
<span class="project-title">
    성능 최적화 (TPS 1,500%)
    <span class="jd-tag">성능 최적화</span>
</span>
```

---

## 체크리스트

### HTML 작성

- [ ] 표준 템플릿 스타일 적용
- [ ] 5페이지 구성 (Summary → 프로젝트 → 지원동기)
- [ ] JD 키워드 태그 표시
- [ ] 회사 조사 기반 지원동기 작성
- [ ] 비전-기여 테이블 포함

### PDF 출력

- [ ] Edge headless로 PDF 생성
- [ ] `--print-to-pdf-no-header` 옵션 사용
- [ ] 머리글/바닥글 없음 확인
- [ ] 페이지 끊김 없음 확인

---

## 관련 스킬

- `/jd-match`: JD 분석 및 회사 조사 (사전 필수)
- `/write-career`: 경력기술서 작성 (5페이지+)
- `/export`: PDF 내보내기
- `/style-guide`: CSS 스타일 가이드

---

## 참조 파일

| 파일 | 설명 |
|------|------|
| `templates/export/pdf/integrated-application.html` | 표준 템플릿 (복사하여 사용) |
