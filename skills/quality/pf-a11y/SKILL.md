---
name: pf-a11y
description: 접근성 검사. "접근성", "a11y", "ARIA", "키보드" 관련 요청 시 사용.
allowed-tools: Read, Glob, Grep
---

# PF 접근성 검사

$ARGUMENTS 컴포넌트/페이지의 접근성을 검사합니다.

---

## 검사 항목

### 1. 시맨틱 HTML

```tsx
// ❌ 나쁨
<div onClick={handleClick}>버튼</div>
<div className="header">헤더</div>

// ✅ 좋음
<button onClick={handleClick}>버튼</button>
<header>헤더</header>
```

**체크리스트:**
- [ ] 버튼은 `<button>` 사용
- [ ] 링크는 `<a>` 사용
- [ ] 제목은 `<h1>`-`<h6>` 순서대로
- [ ] 목록은 `<ul>`, `<ol>`, `<li>` 사용
- [ ] 랜드마크 (`<header>`, `<main>`, `<footer>`, `<nav>`)

---

### 2. 키보드 접근성

```tsx
// ❌ 키보드 접근 불가
<div onClick={handleClick} className="card">
  클릭하세요
</div>

// ✅ 키보드 접근 가능
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      handleClick();
    }
  }}
  className="card"
>
  클릭하세요
</div>

// ✅ 더 좋음 - 그냥 button 사용
<button onClick={handleClick} className="card">
  클릭하세요
</button>
```

**체크리스트:**
- [ ] 모든 인터랙티브 요소가 Tab으로 접근 가능
- [ ] Enter/Space로 활성화 가능
- [ ] Escape로 모달/드롭다운 닫기
- [ ] 화살표 키로 메뉴/리스트 탐색
- [ ] 포커스 순서가 논리적

---

### 3. 포커스 표시

```tsx
// ❌ 포커스 표시 제거 (절대 금지!)
button:focus {
  outline: none;
}

// ✅ 커스텀 포커스 스타일
button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
```

**Tailwind:**
```tsx
<button className="focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
  버튼
</button>
```

---

### 4. ARIA 속성

```tsx
// 버튼 레이블
<button aria-label="닫기">
  <XIcon />
</button>

// 확장/축소 상태
<button aria-expanded={isOpen} aria-controls="menu-content">
  메뉴
</button>
<div id="menu-content" hidden={!isOpen}>
  메뉴 내용
</div>

// 로딩 상태
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? "로딩 중..." : "저장"}
</button>

// 필수 입력
<input aria-required="true" aria-invalid={hasError} />

// 설명 연결
<input aria-describedby="email-hint email-error" />
<p id="email-hint">회사 이메일을 입력하세요</p>
<p id="email-error" role="alert">유효하지 않은 이메일입니다</p>
```

---

### 5. 이미지 대체 텍스트

```tsx
// ❌ alt 없음
<img src="/logo.png" />

// ❌ 무의미한 alt
<img src="/logo.png" alt="이미지" />

// ✅ 의미 있는 alt
<img src="/logo.png" alt="PLUXITY 로고" />

// ✅ 장식용 이미지
<img src="/decoration.png" alt="" role="presentation" />
```

---

### 6. 색상 대비

**최소 대비율:**
- 일반 텍스트: 4.5:1
- 큰 텍스트 (18px+): 3:1
- UI 컴포넌트: 3:1

```tsx
// ❌ 낮은 대비
<p className="text-gray-400 bg-gray-100">읽기 어려움</p>

// ✅ 충분한 대비
<p className="text-gray-700 bg-white">읽기 쉬움</p>
```

---

### 7. 폼 접근성

```tsx
// ❌ label 없음
<input type="email" placeholder="이메일" />

// ✅ 명시적 label
<label htmlFor="email">이메일</label>
<input id="email" type="email" />

// ✅ 또는 aria-label
<input type="email" aria-label="이메일 주소" />

// 에러 메시지 연결
<input
  id="email"
  type="email"
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : undefined}
/>
{error && (
  <p id="email-error" role="alert" className="text-red-500">
    {error}
  </p>
)}
```

---

### 8. 모달/다이얼로그

```tsx
import { Dialog } from "@radix-ui/react-dialog";

// Radix UI는 접근성 내장
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
  <Dialog.Trigger asChild>
    <button>열기</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/50" />
    <Dialog.Content className="fixed ...">
      <Dialog.Title>제목</Dialog.Title>
      <Dialog.Description>설명</Dialog.Description>
      {/* 내용 */}
      <Dialog.Close asChild>
        <button aria-label="닫기">X</button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**수동 구현 시:**
- [ ] `role="dialog"` 또는 `role="alertdialog"`
- [ ] `aria-modal="true"`
- [ ] `aria-labelledby`로 제목 연결
- [ ] 포커스 트랩 구현
- [ ] Escape로 닫기
- [ ] 닫을 때 이전 포커스로 복귀

---

### 9. 동적 콘텐츠 알림

```tsx
// 실시간 알림
<div role="status" aria-live="polite">
  {message}
</div>

// 긴급 알림
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

---

## 테스트 도구

```bash
# axe-core (자동 검사)
npm install -D @axe-core/react

# 사용
import React from "react";
import ReactDOM from "react-dom";

if (process.env.NODE_ENV !== "production") {
  import("@axe-core/react").then((axe) => {
    axe.default(React, ReactDOM, 1000);
  });
}
```

**수동 테스트:**
1. Tab 키로 전체 페이지 탐색
2. 스크린 리더 테스트 (NVDA, VoiceOver)
3. 200% 확대 시 레이아웃 확인
4. 키보드만으로 모든 기능 사용

---

## @pf-dev/ui 컴포넌트 접근성

UI 패키지는 Radix UI 기반으로 접근성이 내장되어 있습니다.
- Button, Dialog, Select, Tabs 등
- 키보드 탐색 자동 지원
- ARIA 속성 자동 적용

커스텀 컴포넌트 작성 시 위 가이드라인을 따르세요.
