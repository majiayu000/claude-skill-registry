---
name: accessibility-wcag
description: Enforce WCAG 2.2 accessibility standards. Use when creating UI components, reviewing frontend code, or when accessibility issues are detected. Covers semantic HTML, ARIA, keyboard navigation, and color contrast.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Accessibility (WCAG 2.2)

웹 접근성 표준 WCAG 2.2를 준수하도록 강제하는 스킬입니다.

## 2025 Context

> **WCAG 2.2는 2023년 10월 ISO 표준(ISO/IEC 40500)으로 채택되었습니다.**
> **유럽 접근성법(EAA)은 2025년 6월부터 시행됩니다.**

## Core Principles (POUR)

| 원칙 | 설명 | 예시 |
|------|------|------|
| **P**erceivable | 인지 가능 | 대체 텍스트, 자막, 색상 대비 |
| **O**perable | 조작 가능 | 키보드 접근, 충분한 시간 |
| **U**nderstandable | 이해 가능 | 명확한 언어, 예측 가능한 동작 |
| **R**obust | 견고함 | 보조 기술 호환성 |

## Rules

### 1. Semantic HTML (필수)

```tsx
// ❌ BAD: div 남용
<div onClick={handleClick}>버튼</div>
<div class="header">제목</div>

// ✅ GOOD: 시맨틱 태그 사용
<button onClick={handleClick}>버튼</button>
<h1>제목</h1>
```

### 2. 이미지 대체 텍스트 (필수)

```tsx
// ❌ BAD: alt 누락 또는 의미 없음
<img src="logo.png" />
<img src="chart.png" alt="이미지" />

// ✅ GOOD: 의미 있는 alt
<img src="logo.png" alt="회사명 로고" />
<img src="chart.png" alt="2024년 매출 증가 추이 그래프" />

// ✅ 장식용 이미지는 빈 alt
<img src="decoration.png" alt="" role="presentation" />
```

### 3. 키보드 접근성 (필수)

```tsx
// ❌ BAD: 키보드 접근 불가
<div onClick={handleClick} style={{ cursor: 'pointer' }}>
  클릭
</div>

// ✅ GOOD: 키보드 접근 가능
<button onClick={handleClick}>클릭</button>

// 또는 커스텀 요소 사용 시
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  클릭
</div>
```

### 4. 포커스 관리

```tsx
// ❌ BAD: 포커스 스타일 제거
button:focus {
  outline: none;
}

// ✅ GOOD: 명확한 포커스 표시
button:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

button:focus-visible {
  outline: 2px solid #005fcc;
}
```

### 5. 색상 대비 (WCAG AA 기준)

| 텍스트 크기 | 최소 대비율 |
|------------|------------|
| 일반 텍스트 | 4.5:1 |
| 큰 텍스트 (18pt+, 14pt bold+) | 3:1 |
| UI 컴포넌트/그래픽 | 3:1 |

```css
/* ❌ BAD: 낮은 대비 */
.text {
  color: #999;  /* 회색 on 흰색 = 2.85:1 */
  background: #fff;
}

/* ✅ GOOD: 충분한 대비 */
.text {
  color: #595959;  /* 4.54:1 */
  background: #fff;
}
```

### 6. 폼 레이블 (필수)

```tsx
// ❌ BAD: 레이블 없음
<input type="email" placeholder="이메일" />

// ✅ GOOD: 명시적 레이블
<label htmlFor="email">이메일</label>
<input id="email" type="email" />

// 또는 aria-label 사용
<input type="email" aria-label="이메일 주소" placeholder="이메일" />
```

### 7. ARIA 역할 및 속성

```tsx
// 모달 다이얼로그
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">확인</h2>
  ...
</div>

// 알림 메시지
<div role="alert" aria-live="polite">
  저장되었습니다.
</div>

// 로딩 상태
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? '처리 중...' : '제출'}
</button>
```

### 8. 건너뛰기 링크

```tsx
// 페이지 상단에 추가
<a href="#main-content" className="skip-link">
  본문으로 건너뛰기
</a>

// CSS
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

## WCAG 2.2 신규 기준

### 2.4.11 Focus Not Obscured (AA)

```tsx
// ❌ BAD: 고정 헤더가 포커스 요소를 가림
.header { position: fixed; top: 0; }

// ✅ GOOD: scroll-margin으로 여유 공간 확보
:target {
  scroll-margin-top: 80px;
}

*:focus {
  scroll-margin-top: 80px;
}
```

### 2.5.7 Dragging Movements (AA)

```tsx
// ❌ BAD: 드래그만 지원
<DraggableList onDrag={handleReorder} />

// ✅ GOOD: 드래그 + 버튼 대안 제공
<DraggableList onDrag={handleReorder}>
  <button onClick={moveUp}>위로 이동</button>
  <button onClick={moveDown}>아래로 이동</button>
</DraggableList>
```

### 2.5.8 Target Size (AA)

```css
/* 최소 터치 타겟: 24x24px (AA), 44x44px 권장 */
button, a, input[type="checkbox"] {
  min-width: 44px;
  min-height: 44px;
}
```

## 테스트 도구

### 자동화 도구

```bash
# axe-core (React)
npm install @axe-core/react

# eslint-plugin-jsx-a11y
npm install eslint-plugin-jsx-a11y --save-dev

# Lighthouse CI
npm install -g @lhci/cli
lhci autorun
```

### eslint 설정

```json
{
  "extends": ["plugin:jsx-a11y/recommended"],
  "rules": {
    "jsx-a11y/alt-text": "error",
    "jsx-a11y/anchor-is-valid": "error",
    "jsx-a11y/click-events-have-key-events": "error",
    "jsx-a11y/no-static-element-interactions": "error"
  }
}
```

### 수동 테스트 체크리스트

- [ ] 키보드만으로 모든 기능 사용 가능
- [ ] Tab 순서가 논리적
- [ ] 포커스 표시가 명확함
- [ ] 스크린 리더로 내용 이해 가능
- [ ] 200% 확대해도 콘텐츠 손실 없음
- [ ] 색상만으로 정보 전달하지 않음

## Workflow

### 1. 컴포넌트 작성 시

```
체크포인트:
1. 시맨틱 HTML 사용했는가?
2. 키보드 접근 가능한가?
3. 적절한 ARIA 속성이 있는가?
4. 포커스 스타일이 있는가?
```

### 2. 코드 리뷰 시

```
접근성 체크:
1. img에 alt 있는가?
2. form에 label 있는가?
3. 색상 대비 충분한가?
4. 터치 타겟 크기 충분한가?
```

## Checklist

- [ ] 시맨틱 HTML 태그 사용
- [ ] 모든 이미지에 의미 있는 alt
- [ ] 폼 요소에 label 연결
- [ ] 키보드만으로 조작 가능
- [ ] 포커스 표시 명확
- [ ] 색상 대비 4.5:1 이상
- [ ] 터치 타겟 44x44px 이상
- [ ] 건너뛰기 링크 제공
- [ ] axe/Lighthouse 테스트 통과

## References

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/)
- [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
