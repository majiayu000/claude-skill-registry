---
name: create-dashboard
description: RNBT 아키텍처 패턴에 맞는 완전한 대시보드 페이지를 생성합니다. Master/Page 레이어, 여러 컴포넌트, Mock 서버, datasetList.json을 포함한 전체 구조를 생성합니다. Use when creating dashboard pages, implementing Master/Page architecture, or setting up complete page structures with multiple components.
---

# RNBT 대시보드 생성

RNBT 아키텍처 패턴에 맞는 **완전한 대시보드 페이지**를 생성하는 Skill입니다.
Master/Page 레이어, 컴포넌트들, Mock 서버, datasetList.json을 포함합니다.

---

## 출력 구조

```
RNBT_architecture/Examples/[example_name]/
├── mock_server/                    # Express API 서버
│   ├── server.js
│   └── package.json
│
├── master/                         # MASTER 레이어 (앱 전역)
│   └── page/
│       ├── page_scripts/
│       │   ├── before_load.js      # 이벤트 핸들러 등록
│       │   ├── loaded.js           # 데이터 매핑 및 발행
│       │   └── before_unload.js    # 리소스 정리
│       ├── page_styles/
│       │   └── container.css       # #master-container 스타일
│       └── components/
│           ├── Header/
│           └── Sidebar/
│
├── page/                           # PAGE 레이어 (페이지별)
│   ├── page_scripts/
│   │   ├── before_load.js          # 이벤트 핸들러 + currentParams
│   │   ├── loaded.js               # 데이터 매핑 + interval
│   │   └── before_unload.js        # 리소스 정리
│   ├── page_styles/
│   │   └── container.css           # #page-container 스타일
│   └── components/
│       ├── StatsCards/
│       ├── DataTable/
│       └── TrendChart/
│
├── datasetList.json                # API 엔드포인트 정의
├── preview.html                    # 전체 대시보드 프리뷰
└── README.md                       # 프로젝트 문서 (필수)
```

**컴포넌트별 README.md도 필수:**
```
components/[ComponentName]/
├── views/component.html
├── styles/component.css
├── scripts/
│   ├── register.js
│   └── beforeDestroy.js
└── README.md                       # 컴포넌트 문서 (필수)
```

---

## Master vs Page 레이어

| 레이어 | 범위 | 용도 | 예시 컴포넌트 |
|--------|------|------|--------------|
| **Master** | 앱 전역 | 공통 UI, 사용자 정보, 네비게이션 | Header, Sidebar |
| **Page** | 페이지별 | 페이지 고유 컴포넌트, 데이터 | StatsCards, DataTable, TrendChart |

---

## 라이프사이클 흐름

```
앱 시작
  ↓
[MASTER] before_load.js
  - eventBusHandlers 등록 (네비게이션 등)
  ↓
[MASTER] 컴포넌트 register.js
  - Header, Sidebar 초기화
  ↓
[MASTER] loaded.js
  - userInfo, menuList 발행
  ↓
페이지 진입
  ↓
[PAGE] before_load.js
  - eventBusHandlers 등록
  - currentParams 초기화
  ↓
[PAGE] 컴포넌트 register.js
  - StatsCards, DataTable, TrendChart 초기화
  ↓
[PAGE] loaded.js
  - globalDataMappings 등록
  - fetchAndPublish
  - startAllIntervals
  ↓
페이지 이탈
  ↓
[PAGE] before_unload.js
  - stopAllIntervals
  - offEventBusHandlers
  - unregisterMapping
  ↓
[PAGE] 컴포넌트 beforeDestroy.js
  ↓
앱 종료
  ↓
[MASTER] before_unload.js
  ↓
[MASTER] 컴포넌트 beforeDestroy.js
```

---

## 파일 템플릿

### datasetList.json

```json
{
  "version": "3.2.0",
  "data": [
    {
      "datasource": "",
      "mode": "0",
      "delivery_type": "0",
      "param_info": [],
      "data_type": "1",
      "interval": "",
      "page_id": "MASTER",
      "dataset_id": "user-001",
      "name": "userApi",
      "rest_api": "{\"url\":\"http://localhost:3003/api/user\",\"method\":\"GET\",\"headers\":{},\"body\":\"\"}"
    },
    {
      "datasource": "",
      "mode": "0",
      "delivery_type": "0",
      "param_info": [
        {"param_name": "category", "param_type": "string", "default_value": "all"}
      ],
      "data_type": "1",
      "interval": "30000",
      "page_id": "PAGE",
      "dataset_id": "table-001",
      "name": "tableApi",
      "rest_api": "{\"url\":\"http://localhost:3003/api/data?category=#{category}\",\"method\":\"GET\",\"headers\":{},\"body\":\"\"}"
    }
  ],
  "datasource": []
}
```

**주의사항:**
- `rest_api`는 JSON 문자열로 이스케이프
- `param_info`는 배열 형태
- `interval`은 밀리초 문자열 (예: "30000")
- `page_id`는 "MASTER" 또는 "PAGE"

### page/page_scripts/before_load.js

```javascript
/**
 * PAGE - before_load.js
 *
 * 시점: 컴포넌트 register 이전
 * 책임: 이벤트 핸들러 등록, currentParams 초기화
 */

const { onEventBusHandlers } = Weventbus;

// ==================
// CURRENT PARAMS
// ==================

this.currentParams = {
    tableData: { category: 'all' },
    chartData: { period: '7d' }
};

// ==================
// EVENT BUS HANDLERS
// ==================

this.eventBusHandlers = {
    '@filterChanged': ({ event }) => {
        const category = event.target.value;
        this.currentParams.tableData = { category };
        GlobalDataPublisher.fetchAndPublish('tableData', this, this.currentParams.tableData);
        console.log('[Page] Filter changed:', category);
    },

    '@periodChanged': ({ event }) => {
        const period = event.target.value;
        this.currentParams.chartData = { period };
        GlobalDataPublisher.fetchAndPublish('chartData', this, this.currentParams.chartData);
        console.log('[Page] Period changed:', period);
    },

    '@rowClicked': ({ data }) => {
        console.log('[Page] Row clicked:', data);
    },

    '@cardClicked': ({ event }) => {
        const key = event.currentTarget.dataset.statKey;
        console.log('[Page] Card clicked:', key);
    }
};

onEventBusHandlers(this.eventBusHandlers);

console.log('[Page] before_load completed');
```

### page/page_scripts/loaded.js

```javascript
/**
 * PAGE - loaded.js
 *
 * 시점: 컴포넌트 completed 이후
 * 책임: 데이터 매핑 등록, 초기 발행, interval 시작
 */

const { registerMapping, fetchAndPublish, startAllIntervals } = GlobalDataPublisher;

// ==================
// DATA MAPPINGS
// ==================

this.globalDataMappings = [
    {
        topic: 'stats',
        datasetName: 'statsApi',
        param: {}
    },
    {
        topic: 'tableData',
        datasetName: 'tableApi',
        param: this.currentParams.tableData
    },
    {
        topic: 'chartData',
        datasetName: 'chartApi',
        param: this.currentParams.chartData
    }
];

// 매핑 등록
fx.go(
    this.globalDataMappings,
    fx.each(mapping => registerMapping(this, mapping))
);

// ==================
// REFRESH INTERVALS
// ==================

this.refreshIntervals = {
    stats: 10000,      // 10초
    tableData: 30000,  // 30초
    chartData: 15000   // 15초
};

// ==================
// INITIAL FETCH
// ==================

fx.go(
    this.globalDataMappings,
    fx.each(({ topic }) => {
        const param = this.currentParams[topic] || {};
        fetchAndPublish(topic, this, param);
    })
);

// ==================
// START INTERVALS
// ==================

startAllIntervals(this, this.refreshIntervals, this.currentParams);

console.log('[Page] loaded completed');
```

### page/page_scripts/before_unload.js

```javascript
/**
 * PAGE - before_unload.js
 *
 * 시점: 컴포넌트 beforeDestroy 이전
 * 책임: interval 정지, 이벤트 해제, 매핑 해제
 */

const { offEventBusHandlers } = Weventbus;
const { stopAllIntervals, unregisterMapping } = GlobalDataPublisher;

// ==================
// STOP INTERVALS
// ==================

if (this.refreshIntervals) {
    stopAllIntervals(this);
    this.refreshIntervals = null;
}

// ==================
// OFF EVENT HANDLERS
// ==================

if (this.eventBusHandlers) {
    offEventBusHandlers(this.eventBusHandlers);
    this.eventBusHandlers = null;
}

// ==================
// UNREGISTER MAPPINGS
// ==================

if (this.globalDataMappings) {
    fx.go(
        this.globalDataMappings,
        fx.each(mapping => unregisterMapping(this, mapping))
    );
    this.globalDataMappings = null;
}

// ==================
// CLEAR PARAMS
// ==================

this.currentParams = null;

console.log('[Page] before_unload completed');
```

---

## 컴포넌트 유형별 구현

### StatsCards (Summary Config 패턴)

```javascript
// register.js
const summaryConfig = [
    { key: 'revenue', label: 'Revenue', icon: '💰', format: (v, unit) => `${unit}${v.toLocaleString()}` },
    { key: 'orders', label: 'Orders', icon: '📦', format: v => v.toLocaleString() },
    { key: 'customers', label: 'Customers', icon: '👥', format: v => v.toLocaleString() },
    { key: 'conversion', label: 'Conversion', icon: '📈', format: (v, unit) => `${v}${unit}` }
];

this.subscriptions = { stats: ['renderStats'] };
this.customEvents = { click: { '.stat-card': '@cardClicked' } };
```

### DataTable (Table Config + Tabulator)

```javascript
// register.js
const tableConfig = {
    columns: [
        { title: 'ID', field: 'id', width: 60, hozAlign: 'center' },
        { title: 'Product', field: 'product', widthGrow: 2 },
        { title: 'Category', field: 'category', width: 120 },
        { title: 'Price', field: 'price', width: 100, hozAlign: 'right',
          formatter: cell => `$${cell.getValue().toLocaleString()}` }
    ]
};

this.tableInstance = new Tabulator(`#${uniqueId}`, {
    layout: 'fitColumns',
    height: '100%',
    placeholder: 'No data available',
    columns: tableConfig.columns
});

this.tableInstance.on('tableBuilt', () => {
    // 데이터 로드
});

this.subscriptions = { tableData: ['renderTable'] };
this.customEvents = { change: { '.filter-select': '@filterChanged' } };
```

### TrendChart (Chart Config + ECharts)

```javascript
// register.js
const chartConfig = {
    xKey: 'labels',
    seriesKey: 'series',
    optionBuilder: getChartOptions
};

this.chartInstance = echarts.init(chartContainer);

this.resizeObserver = new ResizeObserver(() => {
    this.chartInstance && this.chartInstance.resize();
});
this.resizeObserver.observe(chartContainer);

this.subscriptions = { chartData: ['renderChart'] };
this.customEvents = { change: { '.period-select': '@periodChanged' } };
```

---

## 컴포넌트 이벤트 처리 원칙

컴포넌트 이벤트는 **내부 동작**과 **외부 알림** 두 가지로 구분됩니다. 두 방식은 공존 가능합니다.

**질문: "이 동작의 결과를 페이지가 알아야 하는가?"**

| 답변 | 처리 방식 | 예시 |
|------|----------|------|
| **아니오** (컴포넌트 내부 완결) | `setupInternalHandlers`만 | Clear, Toggle, 내부 탭 전환 |
| **예** (페이지가 후속 처리) | `customEvents`만 | 행 선택 → 상세 패널, 필터 변경 → 데이터 재조회 |
| **둘 다** (내부 완결 + 알림) | 둘 다 | 노드 클릭 → 선택 표시(내부) + 상세 요청(외부) |

**더 구체적인 기준:**
1. **UI 상태 변경만** → 내부 (setupInternalHandlers)
2. **데이터 요청/페이지 변화 필요** → 외부 (customEvents)
3. **확신 없으면** → 둘 다 (내부 동작 필수, 외부 알림 선택적)

```javascript
// 내부 동작 (setupInternalHandlers)
function setupInternalHandlers() {
    const root = this.appendElement;
    root.querySelector('.btn-clear')?.addEventListener('click', () => this.clearLogs());
}
setupInternalHandlers.call(this);
```

**중요:** 페이지가 이벤트를 구독하지 않아도 컴포넌트는 독립적으로 동작해야 합니다.

---

## Mock Server 템플릿

### mock_server/package.json

```json
{
  "name": "mock-server",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2"
  }
}
```

### mock_server/server.js

```javascript
const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3003;

app.use(cors());
app.use(express.json());

// ==================
// MASTER ENDPOINTS
// ==================

app.get('/api/user', (req, res) => {
    res.json({
        success: true,
        data: {
            name: 'John Doe',
            role: 'Administrator',
            avatar: 'https://via.placeholder.com/32'
        }
    });
});

app.get('/api/menu', (req, res) => {
    res.json({
        success: true,
        items: [
            { id: 'dashboard', label: 'Dashboard', icon: 'home', active: true },
            { id: 'analytics', label: 'Analytics', icon: 'chart' },
            { id: 'settings', label: 'Settings', icon: 'gear' }
        ]
    });
});

// ==================
// PAGE ENDPOINTS
// ==================

app.get('/api/stats', (req, res) => {
    res.json({
        success: true,
        data: {
            revenue: { value: 125000, unit: '$', change: 12.5 },
            orders: { value: 1234, unit: '', change: 8.2 },
            customers: { value: 567, unit: '', change: -2.1 },
            conversion: { value: 3.2, unit: '%', change: 0.5 }
        }
    });
});

app.get('/api/data', (req, res) => {
    const { category } = req.query;
    let data = [
        { id: 1, product: 'Product A', category: 'electronics', price: 299 },
        { id: 2, product: 'Product B', category: 'clothing', price: 59 },
        { id: 3, product: 'Product C', category: 'electronics', price: 199 }
    ];

    if (category && category !== 'all') {
        data = data.filter(item => item.category === category);
    }

    res.json({
        success: true,
        data,
        meta: { total: data.length, category }
    });
});

app.get('/api/trend', (req, res) => {
    const { period } = req.query;
    const labels = period === '24h'
        ? ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
        : period === '7d'
        ? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        : ['Week 1', 'Week 2', 'Week 3', 'Week 4'];

    res.json({
        success: true,
        data: {
            labels,
            series: [
                { name: 'Revenue', data: labels.map(() => Math.floor(Math.random() * 10000)), color: '#3b82f6' },
                { name: 'Orders', data: labels.map(() => Math.floor(Math.random() * 100)), color: '#22c55e' }
            ]
        },
        meta: { period }
    });
});

// ==================
// START SERVER
// ==================

app.listen(PORT, () => {
    console.log(`Mock server running at http://localhost:${PORT}`);
});
```

---

## 응답 구조 규칙

```javascript
// 런타임이 전달하는 응답 구조
// { response: { data, meta, ... } }

// 렌더 함수에서 destructuring
function renderData(config, { response }) {
    const { data, meta } = response;
    if (!data) return;
    // ...
}
```

---

## 생성/정리 매칭 테이블

### 페이지

| 생성 (before_load / loaded) | 정리 (before_unload) |
|-----------------------------|----------------------|
| `this.eventBusHandlers = {...}` | `this.eventBusHandlers = null` |
| `onEventBusHandlers(...)` | `offEventBusHandlers(...)` |
| `this.globalDataMappings = [...]` | `this.globalDataMappings = null` |
| `this.currentParams = {...}` | `this.currentParams = null` |
| `this.refreshIntervals = {...}` | `this.refreshIntervals = null` |
| `registerMapping(...)` | `unregisterMapping(...)` |
| `startAllIntervals(...)` | `stopAllIntervals(...)` |

### 컴포넌트

| 생성 (register) | 정리 (beforeDestroy) |
|-----------------|----------------------|
| `this.subscriptions = {...}` | `this.subscriptions = null` |
| `subscribe(topic, this, handler)` | `unsubscribe(topic, this)` |
| `this.customEvents = {...}` | `this.customEvents = null` |
| `bindEvents(this, customEvents)` | `removeCustomEvents(this, customEvents)` |
| `this._internalHandlers = {}` | `this._internalHandlers = null` |
| `addEventListener(event, this._internalHandlers.xxx)` | `removeEventListener(event, this._internalHandlers.xxx)` |
| `echarts.init(...)` | `.dispose()` |
| `new Tabulator(...)` | `.destroy()` |
| `new ResizeObserver(...)` | `.disconnect()` |

---

## 금지 사항

```
❌ datasetList.json 형식 임의 변경
- rest_api는 JSON 문자열로 이스케이프
- param_info는 배열 형태
- 기존 예제 형식 준수

❌ 생성/정리 불일치
- 모든 생성 리소스는 정리되어야 함
- interval, subscription, event 모두 해제

❌ 라이프사이클 순서 위반
- before_load: 이벤트 등록만
- loaded: 데이터 발행, interval 시작
- before_unload: 정리만

❌ 응답 구조 잘못 사용
- function(response) ❌
- function({ response }) ✅
```

---

## 완료 체크리스트

```
Master 레이어:
- [ ] master/page/page_scripts/before_load.js
- [ ] master/page/page_scripts/loaded.js
- [ ] master/page/page_scripts/before_unload.js
- [ ] master/page/components/Header/ (전체 구조)
- [ ] master/page/components/Sidebar/ (전체 구조)

Page 레이어:
- [ ] page/page_scripts/before_load.js
- [ ] page/page_scripts/loaded.js
- [ ] page/page_scripts/before_unload.js
- [ ] page/components/[각 컴포넌트]/ (전체 구조)

데이터:
- [ ] datasetList.json (기존 형식 준수)
- [ ] mock_server/server.js
- [ ] mock_server/package.json

문서:
- [ ] README.md (프로젝트 전체)
- [ ] 각 컴포넌트별 README.md

검증:
- [ ] mock_server 실행 (npm start)
- [ ] API 테스트 (curl)
- [ ] 각 컴포넌트 preview.html 확인
```

---

## preview.html 구조

전체 대시보드를 미리 확인할 수 있는 프리뷰 페이지입니다.

### HTML 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Dashboard Name] - Preview</title>

    <!-- External Libraries -->
    <link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet">
    <script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>

    <!-- Page Styles -->
    <link rel="stylesheet" href="master/page/page_styles/container.css">
    <link rel="stylesheet" href="page/page_styles/container.css">

    <!-- Component Styles -->
    <link rel="stylesheet" href="master/page/components/Header/styles/component.css">
    <link rel="stylesheet" href="master/page/components/Sidebar/styles/component.css">
    <link rel="stylesheet" href="page/components/StatsCards/styles/component.css">
    <link rel="stylesheet" href="page/components/DataTable/styles/component.css">
    <link rel="stylesheet" href="page/components/TrendChart/styles/component.css">

    <style>
        /* Reset & Base - 최소한의 인라인 스타일만 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f1f5f9;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <!-- Master Container -->
    <div id="master-container">
        <div id="header-container">
            <div class="header">...</div>
        </div>
        <div id="sidebar-container">
            <div class="sidebar">...</div>
        </div>
    </div>

    <!-- Page Container -->
    <div id="page-container">
        <div id="stats-cards-container">
            <div class="stats-panel">...</div>
        </div>
        <div id="data-table-container">
            <div class="data-table">...</div>
        </div>
        <div id="trend-chart-container">
            <div class="trend-chart">...</div>
        </div>
    </div>

    <script>
        // API 호출 및 렌더링 로직
    </script>
</body>
</html>
```

### 핵심 원칙

1. **Master와 Page는 형제 관계**: 둘 다 `position: absolute`로 겹쳐짐
2. **컨테이너 ID는 고유해야 함**: `#header-container`, `#sidebar-container` 등
3. **내부 클래스는 중첩 구조**: `<div id="xxx-container"><div class="xxx">...</div></div>`
4. **인라인 스타일 최소화**: reset/body 스타일만 인라인, 나머지는 CSS 파일로 분리

---

## page_styles 템플릿

페이지 크기는 **1920 x 1080 고정**입니다. Master와 Page는 둘 다 `position: absolute`로 겹쳐지며, Page가 Master 아래에 위치합니다.

### 레이아웃 계산

```
전체 페이지: 1920 x 1080
├── Header: 1920 x 60 (상단)
├── Sidebar: 240 x 1020 (좌측)
└── Content Area: 1656 x 996 (우측 하단)
    - 계산: 1920 - 240(sidebar) - 24(padding) = 1656
    - 계산: 1080 - 60(header) - 24(padding) = 996
```

### master/page/page_styles/container.css

```css
/* Master Container Styles */
/* 페이지 크기: 1920 x 1080 */
/* Flexbox 레이아웃 사용 (Grid 지양) */
#master-container {
    position: absolute;
    inset: 0;
    width: 1920px;
    height: 1080px;
    display: flex;
    flex-direction: column;
}
```

### page/page_styles/container.css

```css
/* Page Container Styles */
/* 페이지 크기: 1920 x 1080 (Master 아래에 겹쳐짐) */
/* Flexbox 레이아웃 사용 (Grid 지양) */
#page-container {
    position: absolute;
    inset: 0;
    width: 1920px;
    height: 1080px;
    padding-top: 60px;
    padding-left: 240px;
    padding-right: 24px;
    padding-bottom: 24px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
}
/* 실제 콘텐츠 영역: 1656 x 996 (Header 60px, Sidebar 240px, padding 24px 제외) */
```

### 컴포넌트 크기 참조

| 컴포넌트 | 크기 | 비고 |
|----------|------|------|
| Header | 1920 x 60 | 상단 고정 |
| Sidebar | 240 x 1020 | 좌측 고정 |
| StatsCards | 1632 x 180 | 전체 너비 |
| DataTable | 804 x 768 | content-row 내 flex: 1 |
| TrendChart | 804 x 768 | content-row 내 flex: 1 |

---

## CSS 원칙

**[CODING_STYLE.md](../CODING_STYLE.md)의 CSS 원칙 섹션 참조**

핵심 요약:
- **px 단위 사용** (rem/em 금지) - 1920x1080 고정 레이아웃에서 정확한 픽셀 배치 필수
- **Flexbox 우선** (Grid/absolute 지양)

**대시보드 레이아웃 패턴:**
```css
#page-container {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.content-row {
    display: flex;
    gap: 24px;
}

.panel {
    flex: 1;
}
```

---

## CSS 스코핑 패턴

### 컨테이너 ID 명명 규칙

```
#[component-name]-container
```

예시:
- `#header-container`
- `#sidebar-container`
- `#stats-cards-container`
- `#data-table-container`
- `#trend-chart-container`

### 컴포넌트 CSS 구조 (CSS Nesting)

```css
/* 컴포넌트명/styles/component.css */
#stats-cards-container {
    /* 컨테이너 레이아웃 스타일 */
    flex: 1;

    .stats-panel {
        background: white;
        border-radius: 12px;
        padding: 24px;
    }

    .stats-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
    }

    .stat-card {
        flex: 1 1 calc(25% - 12px);
        min-width: 200px;
        padding: 16px;
        border-radius: 8px;

        &:hover {
            transform: translateY(-2px);
        }
    }
}

/* Responsive */
@media (max-width: 768px) {
    #stats-cards-container {
        .stat-card {
            flex: 1 1 calc(50% - 8px);
        }
    }
}
```

### 컨테이너 vs 컴포넌트 역할 분리

| 위치 | 역할 | 예시 |
|------|------|------|
| `page_styles/container.css` | 페이지 레이아웃 | `#page-container { display: flex; }` |
| `component.css` 상단 | 컨테이너 배치 | `#stats-cards-container { flex: 1; }` |
| `component.css` 내부 | 컴포넌트 스타일 | `.stats-panel { background: white; }` |

---

## README.md 템플릿 (필수)

### 프로젝트 루트 README.md

프로젝트 전체 기능과 데이터 정보를 문서화합니다.

```markdown
# [Project Name]

[프로젝트 한 줄 설명]

## 기능 개요

| 기능 | 설명 |
|------|------|
| 실시간 모니터링 | 자산 상태 실시간 표시 |
| 데이터 조회 | 테이블 형태로 상세 정보 조회 |
| 트렌드 분석 | 시계열 차트로 추이 확인 |

## 데이터 흐름

\`\`\`
Mock Server (port 3000)
    │
    ├─ /api/userInfo    → Master: Header (userInfo)
    ├─ /api/menuList    → Master: Sidebar (menuList)
    │
    ├─ /api/stats       → Page: StatsCards (dashboardStats)
    ├─ /api/tableData   → Page: DataTable (tableData)
    └─ /api/trendData   → Page: TrendChart (trendData)
\`\`\`

## API 엔드포인트

| Endpoint | Topic | 컴포넌트 | 설명 |
|----------|-------|----------|------|
| `/api/userInfo` | `userInfo` | Header | 사용자 정보 |
| `/api/menuList` | `menuList` | Sidebar | 네비게이션 메뉴 |
| `/api/stats` | `dashboardStats` | StatsCards | 통계 카드 데이터 |

## 레이어 구조

| 레이어 | 컴포넌트 | 역할 |
|--------|----------|------|
| Master | Header, Sidebar | 앱 공통 UI |
| Page | StatsCards, DataTable, TrendChart | 페이지별 콘텐츠 |

## 컴포넌트 목록

| 컴포넌트 | 설명 | README |
|----------|------|--------|
| Header | 상단 헤더, 사용자 정보 | [README](master/page/components/Header/README.md) |
| Sidebar | 좌측 네비게이션 | [README](master/page/components/Sidebar/README.md) |
| StatsCards | 통계 카드 4개 | [README](page/components/StatsCards/README.md) |

## 실행 방법

\`\`\`bash
# Mock Server
cd mock_server && npm install && npm start

# 브라우저
open preview.html
\`\`\`

## 파일 구조

\`\`\`
[project]/
├── mock_server/
├── master/page/
│   ├── page_scripts/
│   └── components/
├── page/
│   ├── page_scripts/
│   └── components/
├── datasetList.json
├── preview.html
└── README.md
\`\`\`
```

### 컴포넌트별 README.md

각 컴포넌트에 README.md를 작성하여 동작과 사용법을 문서화합니다.
(create-component 스킬의 README.md 템플릿 참고)

---

## 참고 문서

| 문서 | 내용 |
|------|------|
| [CODING_STYLE.md](../CODING_STYLE.md) | 함수형 코딩 지침 (필수 참고) |
| [create-component/SKILL.md](./create-component/SKILL.md) | 컴포넌트 생성 지침 (컴포넌트 작성 시 참고) |

---

## 참고 예제

- `RNBT_architecture/Examples/SimpleDashboard/` - 표준 대시보드 예제 (CODING_STYLE 적용)
- `RNBT_architecture/Projects/ECO/` - 실전 데이터센터 관리
