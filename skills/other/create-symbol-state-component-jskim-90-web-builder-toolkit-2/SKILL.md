---
name: create-symbol-state-component
description: 인라인 SVG HTML을 상태 기반 동적 컴포넌트로 변환합니다. CSS 변수로 색상을 제어하고 런타임 API를 제공합니다.
---

# 심볼 상태 컴포넌트 생성

인라인 SVG HTML을 **상태 기반 동적 컴포넌트**로 변환합니다.
`data-status` 속성과 CSS 셀렉터로 색상을 제어합니다.

> 공통 규칙: [SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) 참조
> 기본 원칙: [create-standard-component](/.claude/skills/2-component/create-standard-component/SKILL.md) 참조

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/.claude/skills/SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) - 공통 규칙
2. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
3. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일
4. **기존 심볼 컴포넌트 패턴 확인** - Cube3DSymbol의 register.js, component.html, component.css를 먼저 읽을 것

---

## 핵심 원리

```
SVG <defs>에 N세트 gradient 정의 (paint0-green, paint0-yellow, paint0-red)
  ↓
SVG path에 layer 클래스 부여 (layer-grad0, layer-fill-primary)
  ↓
CSS [data-status="xxx"] 셀렉터로 fill URL 제어
  ↓
JS에서 dataset.status만 변경 → CSS가 색상 전환
```

**장점:** innerHTML 교체 없이 속성만 변경 (DOM 효율적)

---

## Layer 클래스 분류 체계

SVG의 각 `<path>` 요소에 아래 클래스를 부여합니다.

### Gradient 레이어

| 클래스 | 용도 | 수량 |
|--------|------|------|
| `layer-grad0` ~ `layer-grad9` | gradient fill | SVG에 따라 0~10개 |

- 하나의 gradient ID에 하나의 layer 클래스가 매핑됩니다
- `layer-grad0`은 `paint0-green`, `paint0-yellow`, `paint0-red`에 대응

### Solid 레이어

| 클래스 | 용도 | 색상 특성 |
|--------|------|----------|
| `layer-fill-primary` | 주요 solid fill | 가장 진한 색 |
| `layer-fill-secondary` | 보조 solid fill | 중간 색 |
| `layer-fill-tertiary` | 3차 solid fill | 가장 연한 색 |

### Stroke 레이어

| 클래스 | 용도 |
|--------|------|
| `layer-stroke` | 내부 선/획 (opacity 변형 가능) |
| `layer-stroke-border` | 외곽 테두리 선 |

---

## Gradient 수량 계산

**공식:** `gradient 수` × `상태 수` = 총 `<defs>` 항목

```
예: Cube3DSymbol
- gradient 수: 10개 (paint0 ~ paint9)
- 상태 수: 3개 (green, yellow, red)
- 총 defs: 10 × 3 = 30개 linearGradient 정의
```

### Gradient 수 결정 방법

1. `figma-to-inline-svg`의 정적 SVG에서 gradient를 세기
2. Figma 원본에 `<linearGradient>` 또는 `<radialGradient>`가 몇 개인지 확인
3. 그 수만큼 layer-grad 클래스 부여

---

## component.html 구조

```html
<div class="symbol-container" data-status="green">
    <svg class="symbol-svg" viewBox="0 0 73 54" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <!-- GREEN gradients -->
            <linearGradient id="paint0-green" ...>
                <stop stop-color="#3A6B47"/>...
            </linearGradient>
            <!-- ... paint1-green ~ paint9-green -->

            <!-- YELLOW gradients -->
            <linearGradient id="paint0-yellow" ...>
                <stop stop-color="#8B6F20"/>...
            </linearGradient>
            <!-- ... paint1-yellow ~ paint9-yellow -->

            <!-- RED gradients -->
            <linearGradient id="paint0-red" ...>
                <stop stop-color="#8B3A3A"/>...
            </linearGradient>
            <!-- ... paint1-red ~ paint9-red -->
        </defs>

        <!-- SVG 도형에 layer 클래스 부여 -->
        <g>
            <path class="layer-grad0" opacity="0.8" d="..."/>
            <path class="layer-grad1 layer-stroke" opacity="0.5" d="..." stroke-opacity="0.3"/>
            <path class="layer-grad2" opacity="0.7" d="..."/>
            <!-- ... -->
            <path class="layer-fill-primary" d="..."/>
            <path class="layer-fill-secondary" d="..."/>
            <path class="layer-fill-tertiary layer-stroke-border" opacity="0.4" d="..." stroke-width="0.07"/>
        </g>
    </svg>
</div>
```

### Gradient ID 네이밍 규칙

```
원본 Figma SVG:  id="paint0_linear_..."
                         ↓
Green:           id="paint0-green"
Yellow:          id="paint0-yellow"
Red:             id="paint0-red"
```

### Layer 클래스 부여 기준

```
원본 SVG path:   fill="url(#paint0_linear_...)"
                         ↓ class 부여
변환 후:         class="layer-grad0"   (paint0 → grad0)

원본 SVG path:   fill="#4ADE80"  (solid color, 진한)
                         ↓
변환 후:         class="layer-fill-primary"

원본 SVG path:   stroke="#16A34A"
                         ↓
변환 후:         class="layer-stroke"
```

---

## component.css 구조 (핵심)

**각 상태별 CSS 블록이 필수입니다.**

```css
#symbol-container {
    width: 73px;    /* Figma 치수 */
    height: 54px;
    position: relative;
    overflow: hidden;
}

.symbol-container { width: 100%; height: 100%; }
.symbol-svg { display: block; width: 100%; height: 100%; }

/* ======== GREEN 상태 (정상) ======== */
.symbol-container[data-status="green"] {
    .layer-grad0 { fill: url(#paint0-green); }
    .layer-grad1 { fill: url(#paint1-green); }
    /* ... grad2 ~ grad9 */
    .layer-fill-primary { fill: #4ADE80; }
    .layer-fill-secondary { fill: #86EFAC; }
    .layer-fill-tertiary { fill: #D1FAE5; }
    .layer-stroke { stroke: #16A34A; }
    .layer-stroke-border { stroke: #16A34A; }
}

/* ======== YELLOW 상태 (경고) ======== */
.symbol-container[data-status="yellow"] {
    .layer-grad0 { fill: url(#paint0-yellow); }
    .layer-grad1 { fill: url(#paint1-yellow); }
    /* ... grad2 ~ grad9 */
    .layer-fill-primary { fill: #FACC15; }
    .layer-fill-secondary { fill: #FEF08A; }
    .layer-fill-tertiary { fill: #FEF9C3; }
    .layer-stroke { stroke: #CA8A04; }
    .layer-stroke-border { stroke: #CA8A04; }
}

/* ======== RED 상태 (위험) ======== */
.symbol-container[data-status="red"] {
    .layer-grad0 { fill: url(#paint0-red); }
    .layer-grad1 { fill: url(#paint1-red); }
    /* ... grad2 ~ grad9 */
    .layer-fill-primary { fill: #EF4444; }
    .layer-fill-secondary { fill: #FECACA; }
    .layer-fill-tertiary { fill: #FEE2E2; }
    .layer-stroke { stroke: #DC2626; }
    .layer-stroke-border { stroke: #DC2626; }
}
```

### 색상 팔레트 패턴

각 상태의 색상은 **primary(진) → secondary(중) → tertiary(연)** 구조입니다.

| 상태 | primary | secondary | tertiary | stroke |
|------|---------|-----------|----------|--------|
| green | #4ADE80 | #86EFAC | #D1FAE5 | #16A34A |
| yellow | #FACC15 | #FEF08A | #FEF9C3 | #CA8A04 |
| red | #EF4444 | #FECACA | #FEE2E2 | #DC2626 |

**이 색상은 예시입니다.** 실제 색상은 `figma-to-inline-svg`에서 추출한 값을 사용합니다.

---

## register.js 구조

```javascript
const { subscribe } = GlobalDataPublisher;
const { bindEvents } = Wkit;

// ======================
// CONFIG
// ======================

const config = {
    validStatuses: ['green', 'yellow', 'red'],
    defaultStatus: 'green',
    statusKey: 'TBD_status'   // API 응답의 상태 필드명
};

// ======================
// STATE
// ======================

this._currentStatus = config.defaultStatus;

// ======================
// BINDINGS
// ======================

this.setStatus = setStatus.bind(this, config);
this.updateFromData = updateFromData.bind(this, config);
this.getStatus = getStatus.bind(this);
this.renderData = renderData.bind(this, config);

// ======================
// SUBSCRIPTIONS
// ======================

this.subscriptions = {
    TBD_topicName: ['renderData']
};

fx.go(
    Object.entries(this.subscriptions),
    fx.each(([topic, fnList]) =>
        fx.each(fn => this[fn] && subscribe(topic, this, this[fn]), fnList)
    )
);

// ======================
// CUSTOM EVENTS
// ======================

this.customEvents = {
    click: { '.symbol-container': '@TBD_symbolClicked' }
};
bindEvents(this, this.customEvents);
```

### 핵심 API

```javascript
/**
 * 상태 변경 - data-status 속성만 변경 → CSS가 색상 제어
 */
function setStatus(config, status) {
    if (!config.validStatuses.includes(status)) {
        console.warn(`[Symbol] Invalid status: ${status}`);
        return;
    }

    const container = this.appendElement.querySelector('.symbol-container');
    if (!container) return;

    container.dataset.status = status;
    this._currentStatus = status;
}

/**
 * 데이터 객체로 간접 상태 변경
 */
function updateFromData(config, data) {
    if (data && data[config.statusKey]) {
        this.setStatus(data[config.statusKey]);
    }
}

/**
 * 현재 상태 반환
 */
function getStatus() {
    return this._currentStatus;
}

/**
 * 구독 데이터 렌더링
 */
function renderData(config, { response }) {
    const { data } = response;
    if (!data) return;
    this.updateFromData(data);
}
```

---

## beforeDestroy 패턴

```javascript
const { unsubscribe } = GlobalDataPublisher;
const { removeCustomEvents } = Wkit;

// 1. 구독 해제
if (this.subscriptions) {
    fx.go(
        Object.entries(this.subscriptions),
        fx.each(([topic, _]) => unsubscribe(topic, this))
    );
    this.subscriptions = null;
}

// 2. 이벤트 제거
if (this.customEvents) {
    removeCustomEvents(this, this.customEvents);
    this.customEvents = null;
}

// 3. 참조 정리
this.setStatus = null;
this.updateFromData = null;
this.getStatus = null;
this.renderData = null;
this._currentStatus = null;
```

---

## 입출력

**입력:** `Figma_Conversion/Static_Components/[프로젝트명]/[컴포넌트명]/`

**출력:**
```
components/[ComponentName]/
├── views/component.html       # SVG + N세트 gradient + layer 클래스
├── styles/component.css       # [data-status] 셀렉터
├── scripts/
│   ├── register.js            # setStatus, getStatus, updateFromData API
│   └── beforeDestroy.js
├── preview.html
└── README.md
```

---

## 변환 워크플로우

```
1. figma-to-inline-svg 출력물 읽기
   ├─ 인라인 SVG HTML
   └─ 색상 정보 (주석 또는 README)

2. SVG 분석
   ├─ gradient 수 세기 (linearGradient, radialGradient)
   ├─ solid fill path 분류 (primary, secondary, tertiary)
   └─ stroke path 분류 (stroke, stroke-border)

3. Layer 클래스 부여
   ├─ gradient path → layer-grad0 ~ layer-gradN
   ├─ solid fill → layer-fill-primary/secondary/tertiary
   └─ stroke → layer-stroke / layer-stroke-border

4. Gradient defs 복제
   ├─ 원본 gradient의 stop-color를 상태별 색상으로 교체
   ├─ ID를 paintN-green, paintN-yellow, paintN-red로 변경
   └─ 모든 상태 × 모든 gradient = 총 defs 수

5. CSS 작성
   ├─ [data-status="green"] { .layer-grad0 { fill: url(#paint0-green); } ... }
   ├─ [data-status="yellow"] { ... }
   └─ [data-status="red"] { ... }

6. register.js 작성
   └─ setStatus, getStatus, updateFromData, renderData

7. beforeDestroy.js 작성
   └─ 구독해제 → 이벤트제거 → null 처리
```

---

## 금지 사항

- ❌ innerHTML 교체로 색상 변경 (data-status 속성만 사용)
- ❌ gradient defs를 상태별로 누락
- ❌ layer 클래스 없이 직접 fill 값 변경
- ❌ 생성/정리 불일치
- ❌ datasetName 기반 데이터 응답을 받는 함수에서 `function(response)` 사용 → `function({ response })` 필수

---

## 관련 자료

| 참조 | 위치 | 특징 |
|------|------|------|
| Cube3DSymbol | [/RNBT_architecture/Projects/Symbol_Test/page/components/Cube3DSymbol/](/RNBT_architecture/Projects/Symbol_Test/page/components/Cube3DSymbol/) | 10 gradient × 3 상태, 완전한 패턴 |
