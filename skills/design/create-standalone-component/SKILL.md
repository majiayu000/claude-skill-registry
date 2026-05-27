---
name: create-standalone-component
description: API나 Figma 없이 독립 컴포넌트를 새로 제작합니다. Components/ 폴더에 재사용 가능한 컴포넌트를 만들 때 사용합니다. Use when creating reusable components from scratch, building UI components without Figma designs, or developing components independently of API definitions.
---

# 독립 컴포넌트 제작

API나 Figma 없이 **재사용 가능한 독립 컴포넌트**를 제작하는 Skill입니다.

---

## 출력 위치

```
RNBT_architecture/Components/[ComponentName]/
├── views/component.html       # HTML 구조
├── styles/component.css       # 스타일
├── scripts/
│   ├── register.js            # 초기화 + 메서드 정의
│   └── beforeDestroy.js       # 정리
├── preview.html               # 독립 테스트 (Mock 데이터 포함)
└── README.md                  # 컴포넌트 문서 (필수)
```

---

## 핵심 원칙

### 이벤트 처리의 두 가지 방식

컴포넌트 이벤트는 **내부 동작**과 **외부 알림** 두 가지로 구분됩니다. 두 방식은 공존 가능합니다.

#### 1. 외부 알림 (customEvents) - 페이지에 이벤트 발생

```javascript
// 페이지가 구독하여 처리할 이벤트
this.customEvents = {
    click: {
        '.node-content': '@TBD_nodeClicked',  // 페이지에서 상세 패널 열기 등
        '.btn-export': '@TBD_exportClicked'   // 페이지에서 export 로직 처리
    }
};
bindEvents(this, this.customEvents);
```

**언제 사용?** 페이지가 알아야 하거나, 페이지가 처리 방식을 결정해야 할 때

#### 2. 내부 동작 (setupInternalHandlers) - 컴포넌트 자체 처리

```javascript
// STATE에 핸들러 참조 저장용 객체 추가
this._internalHandlers = {};

// 컴포넌트 자체 UI 동작
function setupInternalHandlers() {
    const root = this.appendElement;

    // 핸들러 참조 저장 (beforeDestroy에서 제거용)
    this._internalHandlers.clearClick = () => this.clearLogs();
    this._internalHandlers.scrollClick = () => this.toggleAutoScroll();

    // 핸들러 바인딩
    root.querySelector('.btn-clear')?.addEventListener('click', this._internalHandlers.clearClick);
    root.querySelector('.btn-scroll')?.addEventListener('click', this._internalHandlers.scrollClick);
}
setupInternalHandlers.call(this);
```

**언제 사용?** 순수 UI 동작으로, 페이지가 알 필요 없을 때 (Clear, Toggle, 내부 탭 전환 등)

**중요:** 핸들러 참조를 `this._internalHandlers`에 저장하여 beforeDestroy에서 명시적으로 제거해야 합니다.

#### 3. 공존 패턴 (내부 동작 + 외부 알림)

동일 이벤트가 내부 동작과 외부 알림을 모두 수행할 수 있습니다:

```javascript
// customEvents로 페이지에 알림
this.customEvents = {
    click: {
        '.node-toggle': '@TBD_nodeToggled'  // 페이지에 알림 (선택적)
    }
};
bindEvents(this, this.customEvents);

// setupInternalHandlers로 내부 동작 수행
function setupInternalHandlers() {
    const root = this.appendElement;

    // 핸들러 참조 저장
    this._internalHandlers.toggleClick = (e) => {
        const toggle = e.target.closest('.node-toggle');
        if (toggle) {
            this.toggleNode(nodeId);  // 내부 동작 (필수)
        }
    };

    // 핸들러 바인딩
    root.addEventListener('click', this._internalHandlers.toggleClick);
}
```

**중요:** 내부 동작이 먼저 수행되고, 이벤트 발생은 그 후입니다.
페이지가 이벤트를 구독하지 않아도 컴포넌트는 독립적으로 동작해야 합니다.

### 외부 인터페이스만 TBD

미리 정할 수 없는 것 (외부 인터페이스):
- `subscriptions`의 topic명 - 데이터 입력
- `config`의 key - API 필드명
- `customEvents`의 이벤트명 - 이벤트 출력

미리 완성 가능한 것:
- HTML/CSS 구조
- 이벤트 바인딩 로직
- 렌더 함수 로직
- beforeDestroy 정리 로직

---

## 워크플로우

```
1. 요구사항 확인
   └─ 컴포넌트 용도, 데이터 구조, 필요한 이벤트

2. HTML 구조 설계
   └─ views/component.html 작성

3. CSS 스타일 작성
   └─ styles/component.css 작성

4. register.js 작성
   └─ TBD 패턴으로 외부 인터페이스 정의

5. beforeDestroy.js 작성
   └─ 모든 리소스 정리

6. preview.html 작성
   └─ Mock 데이터로 독립 테스트
```

---

## TBD 패턴 (API 없이 미리 개발)

```javascript
// API 필드명이 미정일 때
const config = {
    titleKey: 'TBD_title',
    itemsKey: 'TBD_items',
    fields: {
        id: 'TBD_id',
        name: 'TBD_name'
    }
};

this.subscriptions = {
    TBD_topicName: ['renderData']
};

this.customEvents = {
    click: {
        '.btn-action': '@TBD_actionClicked'
    }
};
```

---

## register.js 템플릿

```javascript
/*
 * [ComponentName] Component - register
 * [컴포넌트 설명]
 *
 * Subscribes to: TBD_topicName
 * Events: @TBD_eventName
 *
 * Expected Data Structure:
 * {
 *   field1: "value",
 *   items: [{ id: 1, name: "Item" }]
 * }
 */

const { subscribe } = GlobalDataPublisher;
const { bindEvents } = Wkit;

// ======================
// CONFIG (정적 선언)
// ======================

const config = {
    field1Key: 'TBD_field1',
    itemsKey: 'TBD_items'
};

// ======================
// STATE (필요시)
// ======================

// this._internalState = initialValue;
this._internalHandlers = {};

// ======================
// BINDINGS (바인딩)
// ======================

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
// EVENT BINDING
// ======================

this.customEvents = {
    click: {
        '.btn-action': '@TBD_actionClicked'
    }
};

bindEvents(this, this.customEvents);

// 내부 이벤트 핸들러 (컴포넌트 자체 동작)
setupInternalHandlers.call(this);

// ======================
// RENDER FUNCTIONS (호이스팅)
// ======================

function renderData(config, { response }) {
    const { data } = response;
    if (!data) return;

    // 렌더링 로직
}

// ======================
// INTERNAL HANDLERS (필요시)
// ======================

function setupInternalHandlers() {
    const root = this.appendElement;

    // 핸들러 참조 저장 (beforeDestroy에서 제거용)
    // this._internalHandlers.actionClick = () => this.doAction();

    // 핸들러 바인딩
    // root.querySelector('.btn-action')?.addEventListener('click', this._internalHandlers.actionClick);
}
```

---

## beforeDestroy.js 템플릿

```javascript
/*
 * [ComponentName] Component - beforeDestroy
 * [컴포넌트 설명]
 */

const { unsubscribe } = GlobalDataPublisher;
const { removeCustomEvents } = Wkit;
const { each } = fx;

// ======================
// SUBSCRIPTION CLEANUP
// ======================

fx.go(
    Object.entries(this.subscriptions),
    each(([topic, _]) => unsubscribe(topic, this))
);
this.subscriptions = null;

// ======================
// EVENT CLEANUP
// ======================

removeCustomEvents(this, this.customEvents);
this.customEvents = null;

// ======================
// INTERNAL HANDLER CLEANUP
// ======================

const root = this.appendElement;
if (this._internalHandlers) {
    // root.querySelector('.btn-action')?.removeEventListener('click', this._internalHandlers.actionClick);
}
this._internalHandlers = null;

// ======================
// STATE CLEANUP (필요시)
// ======================

// this._internalState = null;

// ======================
// HANDLER CLEANUP
// ======================

this.renderData = null;
```

---

## preview.html 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[ComponentName] Preview</title>
    <link rel="stylesheet" href="styles/component.css">
    <style>
        body {
            margin: 0;
            padding: 40px;
            background: #0d1117;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        h1 { color: #e0e6ed; margin-bottom: 24px; }
        .preview-container { width: 400px; height: 300px; }
        .controls { margin-top: 24px; }
        .controls button {
            padding: 8px 16px;
            margin-right: 8px;
            background: #4ade80;
            color: #1a1f2e;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .controls button.destroy { background: #f87171; }
    </style>
</head>
<body>
    <h1>[ComponentName] Component Preview</h1>
    <div id="component-root" class="preview-container"></div>
    <div class="controls">
        <button onclick="sendMockData()">Send Data</button>
        <button onclick="destroy()" class="destroy">Destroy</button>
    </div>

    <script>
        // ======================
        // MOCK CONTEXT
        // ======================

        const mockThis = {
            appendElement: document.getElementById('component-root')
        };

        // HTML 삽입 (views/component.html 내용)
        mockThis.appendElement.innerHTML = `
            <!-- component.html 내용 복사 -->
        `;

        // ======================
        // MOCK DEPENDENCIES
        // ======================

        const GlobalDataPublisher = {
            subscribe: (topic, context, fn) => {
                console.log(`[Mock] subscribe: ${topic}`);
            },
            unsubscribe: (topic, context) => {
                console.log(`[Mock] unsubscribe: ${topic}`);
            }
        };

        const Wkit = {
            bindEvents: (context, events) => {
                console.log('[Mock] bindEvents:', events);
            },
            removeCustomEvents: (context, events) => {
                console.log('[Mock] removeCustomEvents:', events);
            }
        };

        const fx = {
            go: (arr, ...fns) => fns.reduce((acc, fn) => fn(acc), arr),
            each: fn => arr => { arr.forEach(fn); return arr; }
        };

        // ======================
        // REGISTER (scripts/register.js 내용)
        // ======================

        (function register() {
            // register.js 내용 복사 (TBD를 실제 값으로 변경)
        }).call(mockThis);

        // ======================
        // BEFORE DESTROY
        // ======================

        function destroy() {
            (function beforeDestroy() {
                // beforeDestroy.js 내용 복사
            }).call(mockThis);
        }

        // ======================
        // TEST HELPERS
        // ======================

        function sendMockData() {
            mockThis.renderData({
                response: {
                    data: {
                        // Mock 데이터
                    }
                }
            });
        }

        // 초기 렌더링
        sendMockData();
    </script>
</body>
</html>
```

---

## CSS 원칙

**[CODING_STYLE.md](../CODING_STYLE.md)의 CSS 원칙 섹션 참조**

핵심 요약:
- **px 단위 사용** (rem/em 금지)
- **Flexbox 우선** (Grid/absolute 지양)

### 스코프: .component-name

```css
/* 최상위 컨테이너 클래스로 스코프 */
.component-name {
    display: flex;
    flex-direction: column;
    background: #1a1f2e;
    border-radius: 8px;
    overflow: hidden;
}

/* 모든 하위 셀렉터는 부모 포함 */
.component-name .header { ... }
.component-name .content { ... }
```

---

## 생성/정리 매칭 테이블

| 생성 (register) | 정리 (beforeDestroy) |
|-----------------|----------------------|
| `this.subscriptions = {...}` | `this.subscriptions = null` |
| `subscribe(topic, this, handler)` | `unsubscribe(topic, this)` |
| `this.customEvents = {...}` | `this.customEvents = null` |
| `bindEvents(this, customEvents)` | `removeCustomEvents(this, customEvents)` |
| `this._internalHandlers = {}` | `this._internalHandlers = null` |
| `addEventListener(event, this._internalHandlers.xxx)` | `removeEventListener(event, this._internalHandlers.xxx)` |
| `this.renderData = fn.bind(this)` | `this.renderData = null` |
| `this._state = value` | `this._state = null` |

---

## 완료 체크리스트

```
- [ ] 요구사항 확인 (용도, 데이터 구조, 이벤트)
- [ ] views/component.html 생성
- [ ] styles/component.css 생성
- [ ] register.js 작성
    - [ ] TBD 패턴으로 외부 인터페이스 정의
    - [ ] subscriptions, customEvents, config 정의
    - [ ] 렌더 함수 구현
- [ ] beforeDestroy.js 작성
    - [ ] 모든 리소스 정리
- [ ] preview.html 작성
    - [ ] Mock 데이터 정의
    - [ ] TBD를 실제 값으로 변경
- [ ] README.md 작성 (필수)
- [ ] 브라우저에서 preview.html 테스트
- [ ] Components/README.md 목록 업데이트
```

---

## README.md 템플릿 (필수)

각 컴포넌트에 README.md를 작성하여 컴포넌트의 동작과 사용법을 문서화합니다.

```markdown
# [ComponentName]

[컴포넌트 한 줄 설명]

## 데이터 구조

\`\`\`javascript
{
    field1: "value",        // 필드 설명
    items: [                // 배열 필드 설명
        { id: 1, name: "Item" }
    ]
}
\`\`\`

## 구독 (Subscriptions)

| Topic | 함수 | 설명 |
|-------|------|------|
| `TBD_topicName` | `renderData` | 데이터 수신 시 렌더링 |

## 발행 이벤트 (Events)

| 이벤트 | 발생 시점 | payload |
|--------|----------|---------|
| `@TBD_eventName` | 버튼 클릭 시 | `{ event, targetInstance }` |

## 내부 동작

### [기능 1]
- 동작 설명

### [기능 2]
- 동작 설명

## TBD 항목

실제 사용 시 변경 필요:

\`\`\`javascript
// config
field1Key: 'TBD_field1' → 'actualFieldName'

// subscriptions
TBD_topicName → 'actualTopic'

// events
@TBD_eventName → '@actualEventName'
\`\`\`

## 파일 구조

\`\`\`
[ComponentName]/
├── views/component.html
├── styles/component.css
├── scripts/
│   ├── register.js
│   └── beforeDestroy.js
├── preview.html
└── README.md
\`\`\`
```

---

## 참고

| 문서 | 내용 |
|------|------|
| `discussions/2025-12-30_component_standalone.md` | 단독 개발 가능 범위 논의 (필수 참고) |
| `RNBT_architecture/Components/README.md` | 컴포넌트 원칙, 구조 |
| `RNBT_architecture/Components/LogViewer/` | 참고 예제 |
| `.claude/skills/CODING_STYLE.md` | 함수형 코딩 지침 |
