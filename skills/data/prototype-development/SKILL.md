---
name: prototype-development
description: UI/UX 설계서를 기반으로 기본 HTML과 JavaScript를 사용하여 동작하는 프로토타입을 개발합니다. 개발 경험이 없는
  사용자도 쉽게 사용할 수 있도록 설계되었습니다.
---

# 프로토타입 개발 가이드

## 목적

UI/UX 설계서를 기반으로 기본 HTML/JavaScript로 동작하는 프로토타입을 개발합니다.

## 사용 시점

- UI/UX 디자인 완료 후
- 사용자 테스트를 위한 프로토타입 필요 시

## 필수 입력
| 파일 | 경로 | 설명 |
|------|------|------|
| UI/UX 명세 | `design/uiux/uiux.md` | 화면 설계, 와이어프레임 |
| 스타일 가이드 | `design/uiux/style-guide.md` | 디자인 시스템 |
| 유저스토리 | `design/userstory.md` | 기능 요구사항 |

---

## 개발 프로세스

### 1단계: 준비

```
1. design/uiux/prototype 디렉토리의 기존 파일 확인
2. 공통 JS/CSS 존재 여부 파악
3. 개발 범위 결정 (전체/특정 화면/MVP)
```

### 2단계: 실행

**개발 순서:**
1. 공통 파일 개발 (`common.js`, `common.css`)
2. 사용자 플로우 순서대로 화면 개발. SPA 방식으로 한 파일에 구현하지 말고 화면별로 파일 분리
3. 화면 간 전환 구현
4. 샘플 데이터 일관성 유지

### 3단계: 검토
- 작성원칙 준수 여부 확인
- 체크리스트 검토 및 수정

### 4단계: 테스트

- Playwright MCP로 브라우저 테스트
- 콘솔 에러 확인 및 수정
- 반응형 레이아웃 검증

---

## 작성원칙

### 1. UI/UX 설계서 매칭 (필수)
- 설계서에 정의된 화면과 기능만 개발
- **불필요한 추가 개발 금지**

### 2. 스타일가이드 준수
- 색상, 타이포그래피, 간격 일관성 유지

### 3. Mobile First
| 원칙 | 설명 |
|------|------|
| 우선순위 중심 | 작은 화면에서 핵심 콘텐츠에 집중 |
| 점진적 향상 | 모바일 → 태블릿 → 데스크톱 순으로 확장 |
| 성능 최적화 | 느린 네트워크 환경 고려 |

---

## 파일 구조

### 공통 파일

**common.js**
```javascript
// 샘플 데이터
const sampleData = {
  user: { name: "홍길동", email: "hong@example.com" },
  items: [{ id: 1, name: "상품 A", price: 10000 }]
};

// 화면 전환
function navigateTo(screen, data) {
  const num = screen.toString().padStart(2, '0');
  window.location.href = `${num}-화면명.html`;
}
```

**common.css**
```css
:root {
  --primary-color: #007bff;
  --font-family: 'Pretendard', sans-serif;
  --spacing-md: 16px;
}

/* Mobile First */
.container { padding: var(--spacing-md); }

@media (min-width: 768px) {
  .container { max-width: 768px; margin: 0 auto; }
}

@media (min-width: 1024px) {
  .container { max-width: 1200px; }
}
```

### 화면 파일 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{화면명}</title>
  <link rel="stylesheet" href="common.css">
</head>
<body>
  <div class="container">
    <header><!-- 헤더 --></header>
    <main><!-- 콘텐츠 --></main>
    <footer><!-- 푸터 --></footer>
  </div>
  <script src="common.js"></script>
  <script>
    // 화면별 스크립트
  </script>
</body>
</html>
```

---

## 체크리스트

### 1. 화면별 기능 동작

| 기능 | 예상 결과 | 실제 결과 | 상태 |
|------|-----------|-----------|------|
| 버튼 클릭 | 다음 화면 이동 | - | ✅/❌ |
| 폼 입력 | 데이터 표시 | - | ✅/❌ |

### 2. 화면간 데이터 일관성

| 데이터 | 사용 화면 | 일관성 |
|--------|-----------|--------|
| 사용자명 | 홈, 프로필 | ✅/❌ |
| 가격정보 | 목록, 상세, 결제 | ✅/❌ |

### 3. 화면간 연결성

| 출발 | 연결방법 | 도착 | 상태 |
|------|----------|------|------|
| 홈 | 검색버튼 | 검색화면 | ✅/❌ |
| 목록 | 카드클릭 | 상세화면 | ✅/❌ |

### 4. 스타일시트 누락
html에 사용된 CSS 스타일이 누락되었는지 체크

---

## Playwright MCP 테스트

### 기본 명령

```
# 단일 화면 열기
design/uiux/prototype/05-홈.html을 브라우저로 열어주세요.

# 콘솔 에러 확인
모든 HTML 파일의 콘솔 에러를 확인해 주세요.

# 반응형 테스트
모바일(375x667), 태블릿(768x1024), 데스크톱(1920x1080)으로 테스트해 주세요.

# 플로우 테스트
01-스플래시 → 05-홈 → 06-검색 순서로 화면 전환을 테스트해 주세요.
```

### 검증 항목

- [ ] 모든 HTML 파일 정상 로드
- [ ] 콘솔 에러 없음
- [ ] 모든 링크/버튼 정상 작동
- [ ] 반응형 레이아웃 정상
- [ ] 화면 전환 정상
- [ ] 이미지/리소스 정상 로드

---

## 결과 파일

| 유형 | 경로 | 명명규칙 |
|------|------|----------|
| 화면 | `design/uiux/prototype/` | `{2자리번호}-{한글화면명}.html` |
| 공통JS | `design/uiux/prototype/` | `common.js` |
| 공통CSS | `design/uiux/prototype/` | `common.css` |

**예시:**
- `01-스플래시.html`
- `05-홈.html`
- `12-프롬프트-상세.html`

---

## 주의사항

| 영역 | 규칙 |
|------|------|
| 개발 | HTML/JS만 사용 (프레임워크 금지), 서버 없이 동작, SPA 방식으로 개발 않함 |
| 데이터 | 실제와 유사한 가상 데이터, 화면 간 일관성 |
| 스타일 | 스타일가이드 준수, Mobile First |
| 테스트 | 브라우저 테스트 필수, 에러 즉시 수정 |

---

## 다음 단계

1. 사용자 테스트 수행
2. 피드백 수집 및 반영
3. 실제 개발 진행 (백엔드 연동)
