---
name: ocr
description: "PDF/이미지를 Claude vision으로 OCR하여 마크다운 변환. MUST use this skill when user: (1) asks to convert PDF/image to markdown, (2) asks to OCR any file, (3) sends PDF/image file and asks to extract/read/변환/추출, (4) mentions 'OCR', 'PDF 변환', '이미지 변환', '텍스트 추출'. This skill uses Task agent to protect main context - NEVER process files directly in main context."
context: fork
agent: general-purpose
---

# OCR (PDF + Image)

PDF 및 이미지 파일을 Claude의 vision 기능으로 읽어 마크다운으로 변환합니다.

## Supported Formats

| 타입 | 확장자 |
|------|--------|
| PDF | `.pdf` |
| 이미지 | `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tiff` |

## Quick Start

```bash
# 단일 파일 (PDF 또는 이미지)
/ocr /path/to/document.pdf
/ocr /path/to/image.png

# 커스텀 지침과 함께
/ocr /path/to/document.pdf "표만 추출해줘"
/ocr /path/to/screenshot.png "코드만 추출해줘"

# 폴더 내 모든 PDF/이미지 (병렬 처리)
/ocr /path/to/folder/
```

## Core Workflow

### Step 1: 경로 및 파일 타입 확인

```bash
# 파일인지 폴더인지 확인
ls -la <path>
```

**파일 타입 분류:**
- `.pdf` → PDF 모드
- `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tiff` → 이미지 모드
- 폴더 → [Batch Mode](#batch-mode-폴더-처리)로 진행

### Step 2: 저장 방식 선택 (PDF만 해당)

**PDF 파일인 경우에만** 사용자에게 저장 방식을 질문:

```
AskUserQuestion:
  question: "PDF 변환 결과를 어떻게 저장할까요?"
  header: "저장 방식"
  options:
    - label: "통합 저장 (Recommended)"
      description: "모든 페이지를 하나의 마크다운 파일로 저장"
    - label: "페이지별 저장"
      description: "각 페이지를 개별 마크다운 파일로 저장 (document_p1.md, document_p2.md, ...)"
```

**저장 방식 변수:**
- `unified`: 통합 저장 → `document.pdf` → `document.md`
- `per_page`: 페이지별 저장 → `document.pdf` → `document_p1.md`, `document_p2.md`, ...

**이미지 파일**: 저장 방식 질문 없이 바로 `image.png` → `image.md`로 변환

---

## Single File Mode - Image

단일 이미지 파일 처리 워크플로우.

**IMPORTANT**: 단일 파일도 Task 에이전트를 사용하여 메인 컨텍스트를 보호합니다.

```
Task(subagent_type="general-purpose"):
  프롬프트: |
    이미지 파일을 OCR하여 마크다운으로 변환하고 저장해주세요.

    파일: [이미지 절대경로]
    커스텀 지침: [사용자 지침 있으면 포함]

    **수행 작업:**
    1. Read 도구로 이미지 읽기
    2. 이미지 내용을 마크다운으로 변환
    3. Write 도구로 [파일명].md 파일 저장
    4. 저장 완료 확인

    **에러 핸들링:**
    - 413 에러: "⚠️ 파일 크기 초과 (413 에러)"
    - 기타 에러: "⚠️ [에러 메시지]"

    **반환 형식 (내용 제외, 상태만):**
    ✅ 성공: [파일명] → [출력파일명].md
    또는
    ⚠️ 실패: [파일명] - [사유]
```

---

## Single File Mode - PDF

단일 PDF 파일 처리 워크플로우.

**IMPORTANT**: 단일 파일도 Task 에이전트를 사용하여 메인 컨텍스트를 보호합니다.

### 통합 저장 모드 (unified)

```
Task(subagent_type="general-purpose"):
  프롬프트: |
    PDF 파일을 OCR하여 마크다운으로 변환하고 저장해주세요.

    파일: [PDF 절대경로]
    저장 방식: 통합 (모든 페이지를 하나의 파일로)
    커스텀 지침: [사용자 지침 있으면 포함]

    **수행 작업:**
    1. Read 도구로 PDF 읽기
    2. 모든 페이지를 하나의 마크다운으로 변환
    3. Write 도구로 [파일명].md 파일 저장
    4. 저장 완료 확인

    **에러 핸들링:**
    - 413 에러: "⚠️ 파일 크기 초과 (413 에러)"
    - 기타 에러: "⚠️ [에러 메시지]"

    **반환 형식 (내용 제외, 상태만):**
    ✅ 성공: [파일명] → [출력파일명].md
    또는
    ⚠️ 실패: [파일명] - [사유]
```

### 페이지별 저장 모드 (per_page)

```
Task(subagent_type="general-purpose"):
  프롬프트: |
    PDF 파일을 OCR하여 페이지별로 마크다운 파일을 생성해주세요.

    파일: [PDF 절대경로]
    저장 방식: 페이지별 (각 페이지를 개별 파일로)
    커스텀 지침: [사용자 지침 있으면 포함]

    **수행 작업:**
    1. Read 도구로 PDF 읽기
    2. 각 페이지별로 마크다운 변환
    3. 각 페이지를 개별 파일로 저장:
       - [파일명]_p1.md (1페이지)
       - [파일명]_p2.md (2페이지)
       - ...
    4. 모든 파일 저장 완료 확인

    **출력 파일 명명 규칙:**
    - document.pdf → document_p1.md, document_p2.md, document_p3.md, ...

    **에러 핸들링:**
    - 413 에러: "⚠️ 파일 크기 초과 (413 에러)"
    - 기타 에러: "⚠️ [에러 메시지]"

    **반환 형식 (내용 제외, 상태만):**
    ✅ 성공: [파일명] → [N]개 페이지 파일 생성
       - [파일명]_p1.md
       - [파일명]_p2.md
       - ...
    또는
    ⚠️ 실패: [파일명] - [사유]
```

---

## Batch Mode (폴더 처리)

폴더 내 여러 PDF/이미지를 병렬로 처리.

### 1. 파일 목록 수집 및 분류

```bash
# 폴더 내 지원 파일 목록
ls <folder_path>/*.{pdf,png,jpg,jpeg,webp,gif,bmp,tiff} 2>/dev/null
```

**파일 분류:**
- PDF 파일 목록: `*.pdf`
- 이미지 파일 목록: `*.png`, `*.jpg`, `*.jpeg`, `*.webp`, `*.gif`, `*.bmp`, `*.tiff`

### 2. 저장 방식 선택 (PDF가 있는 경우만)

PDF 파일이 포함된 경우에만 저장 방식 질문:

```
AskUserQuestion:
  question: "PDF 변환 결과를 어떻게 저장할까요? (이미지는 항상 통합 저장)"
  header: "저장 방식"
  options:
    - label: "통합 저장 (Recommended)"
      description: "각 PDF의 모든 페이지를 하나의 마크다운 파일로 저장"
    - label: "페이지별 저장"
      description: "각 PDF의 페이지를 개별 마크다운 파일로 저장"
```

### 3. 배치 분할 (3개 단위)

파일들을 **3개씩 그룹**으로 나눕니다 (PDF와 이미지 혼합 가능):
- 그룹 1: file1.pdf, image1.png, file2.pdf
- 그룹 2: image2.jpg, file3.pdf, image3.webp
- ...

### 4. 병렬 에이전트 실행

각 그룹에 대해 **Task 도구**로 병렬 에이전트 실행:

```
Task(subagent_type="general-purpose"):
  프롬프트: |
    다음 파일들을 OCR하여 마크다운으로 변환해주세요.

    파일 목록:
    - [file1 절대경로]
    - [file2 절대경로]
    - [file3 절대경로]

    PDF 저장 방식: [unified 또는 per_page]
    커스텀 지침: [사용자 지침 있으면 포함]
    출력 폴더: [원본과 동일 폴더]

    **파일 타입별 처리:**
    - PDF (.pdf): 지정된 저장 방식 적용
    - 이미지 (.png, .jpg 등): 항상 통합 저장 (image.png → image.md)

    **CRITICAL - 각 파일에 대해 에이전트 내에서 완료:**
    1. Read 도구로 파일 읽기
    2. 에러 발생 시 skip하고 다음 파일로 (413 에러 등)
    3. 마크다운으로 변환
    4. **Write 도구로 파일 저장** (반드시 에이전트 내에서!)
    5. 저장 완료 확인

    **IMPORTANT**:
    - 변환된 마크다운 내용을 메인으로 반환하지 마세요
    - 파일 저장까지 에이전트 내에서 완료해야 합니다
    - 메인에는 처리 결과 상태만 반환합니다

    처리 결과를 다음 형식으로만 보고 (내용 제외):
    ✅ 성공: [파일명] → [출력파일명].md
    ⚠️ SKIP: [파일명] - [사유]
```

**IMPORTANT**:
- 모든 그룹의 Task를 **동시에** 호출하여 병렬 실행
- 에이전트는 **Read + Write 모두 완료** 후 상태만 반환
- 메인 컨텍스트에 파일 내용이 로드되지 않도록 함

### 5. 결과 집계

모든 에이전트 완료 후 결과 집계:

```markdown
## 📊 OCR 처리 결과

### ✅ 성공 ([N]개)
**PDF:**
- document1.pdf → document1.md
- document2.pdf → document2_p1.md, document2_p2.md (페이지별)

**이미지:**
- screenshot.png → screenshot.md
- photo.jpg → photo.md

### ⚠️ Skip ([M]개)
- large_file.pdf - 파일 크기 초과 (413 에러)
- corrupted.png - 읽기 실패

### 📁 출력 위치
[folder_path]/
```

---

## 마크다운 변환 가이드라인

파일 내용을 분석하여 다음 형식으로 마크다운 변환:

```markdown
# 문서 제목

## 섹션 1
본문 내용...

### 표
| 열1 | 열2 |
|-----|-----|
| 값  | 값  |

### 이미지/다이어그램 설명
[이미지 설명: ...]
```

### 커스텀 지침 적용

사용자가 추가 지침을 제공한 경우:
- "표만 추출" → 표 형식 데이터만 마크다운 테이블로
- "요약해줘" → 핵심 내용만 요약
- "영어로 번역" → 번역된 결과물
- "코드만 추출" → 코드 블록만 추출

---

## Supported Content Types

| 콘텐츠 | 변환 방식 |
|--------|-----------|
| 일반 텍스트 | 그대로 마크다운 |
| 제목/섹션 | # 헤딩으로 구조화 |
| 표 | 마크다운 테이블 |
| 목록 | - 또는 1. 형식 |
| 이미지/다이어그램 | [이미지 설명] 형태로 기술 |
| 코드 | ```언어``` 코드 블록 |
| 수식 | LaTeX ($...$) 형식 |
| 스크린샷 UI | UI 요소 및 텍스트 추출 |

## Important Rules

### Context 보호 (핵심)
- **ALWAYS** Task 에이전트 내에서 Read + Write 모두 완료
- **ALWAYS** 에이전트는 처리 상태만 반환 (변환된 내용 반환 금지)
- **NEVER** 메인 컨텍스트에 파일 내용을 로드하지 않음

### 처리 방식
- **ALWAYS** Read 도구를 사용하여 파일 읽기 (라이브러리 사용 금지)
- **ALWAYS** 원본 문서의 구조를 최대한 보존
- **ALWAYS** 사용자 커스텀 지침이 있으면 우선 적용
- **ALWAYS** 에러 발생 시 해당 파일 skip하고 나머지 계속 처리
- **ALWAYS** 폴더 처리 시 3개 단위로 병렬 에이전트 실행
- **NEVER** 외부 라이브러리 사용하지 않음 (PyPDF, Pillow 등)
- **NEVER** 읽을 수 없는 부분을 추측으로 채우지 않음 (불명확시 [불명확] 표시)
- **NEVER** 하나의 context에서 모든 파일을 처리하지 않음 (메모리 초과 방지)
