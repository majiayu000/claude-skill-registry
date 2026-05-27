---
name: create-symbol-state-component
description: 인라인 SVG HTML을 상태 기반 동적 컴포넌트로 변환합니다. CSS 변수로 색상을 제어하고 런타임 API를 제공합니다.
---

# 심볼 상태 컴포넌트 생성

인라인 SVG HTML을 **상태 기반 동적 컴포넌트**로 변환합니다.
`data-status` 속성과 CSS 셀렉터로 색상을 제어합니다.

> 기본 원칙은 [create-standard-component](/.claude/skills/2-component/create-standard-component/SKILL.md) 참조

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
2. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일

---

## 핵심 원리

```
SVG <defs>에 3세트 gradient 정의 (paint0-green, paint0-yellow, paint0-red)
  ↓
SVG path에 layer 클래스 부여 (layer-grad0, layer-fill-primary)
  ↓
CSS [data-status="xxx"] 셀렉터로 fill URL 제어
  ↓
JS에서 dataset.status만 변경 → CSS가 색상 전환
```

**장점:** innerHTML 교체 없이 속성만 변경 (DOM 효율적)

---

## 입출력

**입력:** `Figma_Conversion/Static_Components/[프로젝트명]/[컴포넌트명]/`

**출력:**
```
components/[ComponentName]/
├── views/component.html       # SVG + 3세트 gradient + layer 클래스
├── styles/component.css       # [data-status] 셀렉터
├── scripts/
│   ├── register.js            # setStatus, getStatus API
│   └── beforeDestroy.js
├── preview.html
└── README.md
```

---

## Layer 클래스 명명 규칙

| 클래스 | 용도 |
|--------|------|
| `layer-grad0` ~ `layer-grad9` | gradient fill |
| `layer-fill-primary` | 주요 solid color |
| `layer-fill-secondary` | 보조 solid color |
| `layer-stroke` | 외곽선 |

---

## 핵심 API

```javascript
// 상태 변경 - data-status 속성만 변경
function setStatus(config, status) {
    container.dataset.status = status;  // CSS가 색상 제어
    this._currentStatus = status;
}

// 현재 상태 반환
function getStatus() {
    return this._currentStatus;
}
```

---

## 금지 사항

- ❌ innerHTML 교체로 색상 변경
- ❌ 생성/정리 불일치
- ❌ `function(response)` 사용 → `function({ response })` 필수

---

## 관련 자료

| 참조 | 위치 |
|------|------|
| 예제 | [/RNBT_architecture/Projects/Symbol_Test/page/components/Cube3DSymbol/](/RNBT_architecture/Projects/Symbol_Test/page/components/Cube3DSymbol/) |
