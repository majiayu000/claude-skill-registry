---
name: style-guide
description: HTML/CSS 스타일 수정이 필요할 때
---

# 스타일 가이드

## 개요

이력서/경력기술서 HTML 템플릿과 CSS 스타일 수정 시 준수해야 할 가이드입니다.

## CSS 구조

### 파일 위치
```
assets/css/style.css
```

### 구조
```css
/* 1. CSS Variables (Light & Dark) */
/* 2. Reset & Base */
/* 3. Typography */
/* 4. Layout */
/* 5. Components */
/* 6. Dark Mode Overrides (if needed) */
```

## CSS 변수 시스템

### Light Mode (기본)
```css
:root {
    --primary-dark: #1a1a2e;
    --primary-blue: #4a6cf7;
    --text-primary: #333;
    --bg-body: #f8f9fa;
    --bg-white: white;
}
```

### Dark Mode
```css
[data-theme="dark"] {
    --primary-dark: #e0e0e0;
    --primary-blue: #60a5fa;
    --text-primary: #e0e0e0;
    --bg-body: #0f0f23;
    --bg-white: #1a1a2e;
}
```

### 변수 사용법
```css
.section {
    background: var(--bg-white);
    color: var(--text-primary);
}

.section h3 {
    color: var(--primary-dark);
}

.section h3 i {
    color: var(--primary-blue);
}
```

## 핵심 원칙

### 1. 인라인 스타일 금지

**Bad:**
```html
<h3 style="color: #1a1a2e; font-size: 1.2rem;">제목</h3>
```

**Good:**
```html
<h3 class="section-title">제목</h3>
```
```css
.section-title {
    color: var(--primary-dark);
    font-size: 1.2rem;
}
```

### 2. CSS 변수 우선 사용

**Bad:**
```css
.title { color: #1a1a2e; }
```

**Good:**
```css
.title { color: var(--primary-dark); }
```

### 3. 다크모드 자동 적용

CSS 변수를 사용하면 다크모드가 자동 적용됩니다.
별도의 `[data-theme="dark"]` 선택자가 필요 없습니다.

## HTML 템플릿 구조

### 공통 구조
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>문서 제목</title>
    <link rel="stylesheet" href="../../assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- 콘텐츠 -->
    <script src="../../assets/js/common.js"></script>
</body>
</html>
```

### 템플릿 종류

| 템플릿 | 특징 | 용도 |
|--------|------|------|
| **default** | 균형 잡힌 레이아웃 | 일반 이력서 |
| **minimal** | 심플한 디자인 | 간결함 선호 |
| **modern** | 모던한 UI | 디자인 중시 |
| **corporate** | 격식 있는 스타일 | 대기업 지원 |

## 스타일 수정 시 체크리스트

### 색상 변경 시
- [ ] CSS 변수로 정의했는가?
- [ ] Light/Dark 모드 둘 다 정의했는가?
- [ ] 인라인 스타일 사용하지 않았는가?

### 레이아웃 변경 시
- [ ] 4개 템플릿 모두 적용했는가? (resume/career 각 4개)
- [ ] 반응형 고려했는가?
- [ ] 인쇄 시 레이아웃 확인했는가?

### 새 클래스 추가 시
- [ ] 기존 클래스와 충돌 없는가?
- [ ] 다크모드 자동 적용되는가?
- [ ] 의미 있는 클래스명인가?

## 주의사항

### 템플릿 일관성 유지
- 8개 HTML 템플릿 모두 동일한 구조 유지
- 공통 스타일은 `style.css`에서 관리
- 템플릿별 차이는 클래스로 구분

### 파일 수정 범위
```
스타일 수정 시 영향받는 파일:
├── assets/css/style.css
├── templates/resume/*.html (4개)
└── templates/career/*.html (4개)
```
