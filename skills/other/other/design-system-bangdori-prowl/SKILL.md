---
name: design-system
description: Prowl 앱의 디자인 시스템 (Liquid Glass + 골드 액센트)
---

# Prowl Design System

UI 작업 시 아래 디자인 시스템을 반드시 참조하여 일관된 스타일을 유지합니다.

## 1. Base Colors (Liquid Glass 기반 반투명)

macOS vibrancy를 통해 데스크톱이 블러되어 비치는 투명 배경을 사용합니다.

| 용도 | Tailwind Token | 값 |
|------|---------------|----|
| Deep Background | `prowl-bg` | `transparent` |
| Surface | `prowl-surface` | `rgba(255, 255, 255, 0.06)` |
| Card | `prowl-card` | `rgba(255, 255, 255, 0.04)` |
| Border | `prowl-border` | `rgba(255, 255, 255, 0.08)` |
| Border Hover | `prowl-border-hover` | `rgba(255, 255, 255, 0.15)` |

## 2. Accent (골드 / 고양이 눈)

| 용도 | Tailwind Token | 색상 코드 |
|------|---------------|-----------|
| Primary Accent | `accent` | `#f59e0b` |
| Accent Hover | `accent-hover` | `#fbbf24` |
| Accent Muted | `accent-muted` | `#b45309` |

## 3. 라이트 테마 (폴백)

| 용도 | Tailwind Token | 색상 코드 |
|------|---------------|-----------|
| Surface Light | `surface-light` | `#fafafa` |
| Card Light | `card-light` | `#ffffff` |

## 4. 효과

| 용도 | Tailwind Token | 값 |
|------|---------------|----|
| Glow Accent | `shadow-glow-accent` | `0 0 20px rgba(245, 158, 11, 0.15)` |
| Glow Success | `shadow-glow-success` | `0 0 10px rgba(34, 197, 94, 0.2)` |
| Glow Error | `shadow-glow-error` | `0 0 10px rgba(239, 68, 68, 0.2)` |

## 5. Liquid Glass (macOS Vibrancy)

Apple Liquid Glass 트렌드에 맞춘 투명 배경 시스템입니다.

### Electron 윈도우 설정

| 속성 | 값 | 설명 |
|------|-----|------|
| `vibrancy` | `"under-window"` | macOS 네이티브 블러로 데스크톱이 비침 |
| `visualEffectState` | `"active"` | 비활성 윈도우에서도 투명 효과 유지 |
| `backgroundColor` | `"#00000000"` | 투명 배경 |

### 레이아웃 투명도

| 요소 | 클래스 | 설명 |
|------|--------|------|
| `html, body` | `background: transparent !important` | 전체 배경 투명 |
| 루트 컨테이너 | `bg-transparent` | vibrancy가 보이도록 |
| 사이드바 | `bg-white/[0.02]` | 극미세 반투명 레이어 |
| 헤더/보더 | `border-white/[0.06]` | 반투명 화이트 보더 |

### 주의사항

- 레이아웃 요소에 `backdrop-blur` 추가 시 vibrancy 위에 이중 blur가 걸려 어두워짐
- CSS `backdrop-blur`는 **팝업/플로팅 요소**에만 사용 (macOS vibrancy와 분리된 레이어)
- 솔리드 배경(`#0d0d0d` 등)은 vibrancy를 완전히 차단하므로 사용 금지

## 6. 3D 글래스 카드

카드 컴포넌트에 입체감을 부여하는 CSS 3D 효과입니다.

### 클래스: `.glass-card-3d`

```css
/* 기본 상태 */
transform: perspective(800px) rotateX(1deg);
box-shadow: 0 4px 16px rgba(0,0,0,0.25), 0 1px 0 rgba(255,255,255,0.06) inset;

/* hover 상태 */
transform: perspective(800px) rotateX(0deg) translateY(-2px);
box-shadow: 0 8px 30px rgba(0,0,0,0.35), 0 1px 0 rgba(255,255,255,0.1) inset;
border-color: rgba(255,255,255,0.12);
```

### 적용 패턴

```html
<div class="glass-card-3d rounded-lg bg-prowl-card backdrop-blur-xl border border-white/[0.06]">
  카드 내용
</div>
```

### 적용 대상

- Settings 섹션: Night Watch, Notifications, Links 카드
- Version History 섹션: 현재 버전 헤더, 각 릴리스 카드

## 7. 컴포넌트 클래스 (globals.css)

| 클래스 | 용도 |
|--------|------|
| `.glass-card-3d` | 3D 입체 글래스 카드 (perspective + hover tilt) |
| `.job-card` | 작업 카드 (hover 시 `bg-white/[0.02]`) |
| `.btn-icon` | 아이콘 버튼 (hover 시 `text-gray-200`) |
| `.btn-primary` | 프라이머리 버튼 (`bg-blue-500 text-white`) |
| `.btn-ghost` | 고스트 버튼 (`text-gray-400` → hover `text-gray-200`) |
| `.input-field` | 인풋/셀렉트 (`bg-white/[0.04] backdrop-blur-sm`) |
| `.log-viewer` | 터미널 로그 뷰어 (`bg-black/40 backdrop-blur-md`) |
| `.toggle-switch` | 토글 스위치 (on: `bg-green-500`) |
| `.app-header` | 헤더 (`bg-white/[0.03] backdrop-blur-xl`) |
| `.skeleton` | 로딩 스켈레톤 |
| `.section-title` | 섹션 제목 (`tracking-wider text-gray-500`) |
| `.empty-state` | 빈 상태 안내 |

## 8. 적용 규칙

1. **Liquid Glass 우선**: 배경은 반투명, macOS vibrancy로 데스크톱이 비침
2. **커스텀 토큰 사용**: prowl 계열 토큰으로 반투명 색상 통일
3. **하드코딩 금지**: 색상 값을 직접 입력하지 않고 반드시 Tailwind 토큰 사용
4. **반투명 보더**: `border-white/[0.06]` ~ `border-white/[0.08]` 범위 사용
5. **accent 활용**: 강조 요소에 `accent` 계열 사용
6. **3D 카드**: Settings, Version History 등 카드형 UI에 `.glass-card-3d` 적용
7. **backdrop-blur 주의**: 팝업/플로팅 요소에만 `backdrop-blur-xl` 사용, 레이아웃 요소에는 지양
