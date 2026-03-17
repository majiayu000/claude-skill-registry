---
name: create-component-with-popup
description: Shadow DOM 팝업을 가진 컴포넌트를 생성합니다. 컴포넌트가 직접 데이터를 fetch하고 팝업으로 표시합니다. 3D 씬, 독립 위젯 등에 사용합니다.
---

# 팝업 컴포넌트 생성

컴포넌트가 직접 데이터를 fetch하고 Shadow DOM 팝업으로 표시합니다.

> 공통 규칙: [SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) 참조
> 기본 원칙: [create-standard-component](/.claude/skills/2-component/create-standard-component/SKILL.md) 참조

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/.claude/skills/SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) - 공통 규칙
2. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
3. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일
4. [/RNBT_architecture/Utils/PopupMixin.js](/RNBT_architecture/Utils/PopupMixin.js) - PopupMixin API
5. **기존 팝업 컴포넌트 패턴 확인** - UPS, PDU, CRAC 중 하나를 먼저 읽을 것

---

## 일반 vs 팝업 컴포넌트

| 구분 | 일반 컴포넌트 | 팝업 컴포넌트 |
|------|--------------|--------------|
| 데이터 | GlobalDataPublisher | fetchData (Wkit에서 import) |
| 구독 | `subscriptions` | `datasetInfo` |
| 팝업 | 선택적 | **필수** |
| fetch 주체 | 페이지 | 컴포넌트 자신 |
| 이벤트 바인딩 | `bindEvents` | `bind3DEvents` (3D) 또는 `bindEvents` (2D) |

---

## 핵심 원칙

### 데이터 흐름

```
페이지 → @assetClicked 이벤트 수신 → targetInstance.showDetail() 호출
  ↓
컴포넌트.showDetail()
  ├─ showPopup()
  ├─ fx.go(datasetInfo, fx.each(d => fetchDatasetAndRender(d)))
  └─ fx.go(datasetInfo, fx.filter(refreshInterval > 0), fx.each(setInterval))
```

- `assetKey`는 컴포넌트 초기화 시 `this._defaultAssetKey`에 이미 설정됨
- `showDetail()`은 **인자 없이** 호출됨

- **팝업이 있을 때만** 컴포넌트의 직접 fetch 허용

---

## register.js 구조

### 1. config 객체 (핵심)

config 객체가 컴포넌트의 모든 동작을 제어합니다. **UI 영역별로 분리**합니다.

```javascript
this.config = {
    // 데이터셋 이름 (datasetList.json의 키)
    datasetNames: {
        assetDetail: 'assetDetailUnified',
        metricLatest: 'metricLatest',
        metricHistory: 'metricHistoryStats',
    },

    // API 엔드포인트 및 파라미터
    api: {
        trendHistory: '/api/v1/mhs/l',
        trendParams: {
            interval: '1h',
            timeRange: 24 * 60 * 60 * 1000,
            metricCodes: ['INPUT_A', 'OUTPUT_A'],
            statsKeys: [],
            timeField: 'time',
        },
        // metricCode → statsKey 매핑 (필수 쌍)
        statsKeyMap: {
            'INPUT_A': 'sum',
            'OUTPUT_A': 'sum',
        },
    },

    // 상태 코드별 레이블/속성 매핑
    statusMap: {
        ACTIVE: { label: '정상운영', dataAttr: 'normal' },
        WARNING: { label: '주의', dataAttr: 'warning' },
        CRITICAL: { label: '위험', dataAttr: 'critical' },
        DEFAULT: { label: '알 수 없음', dataAttr: 'normal' },
    },

    // ========================
    // UI 영역별 설정
    // ========================

    // 팝업 헤더 영역
    header: {
        fields: [
            { key: 'name', selector: '.popup-name' },
            { key: 'statusType', selector: '.popup-status', transform: this.statusTypeToLabel },
            { key: 'statusType', selector: '.popup-status', dataAttr: 'status', transform: this.statusTypeToDataAttr },
        ],
    },

    // 정보 테이블 영역
    infoTable: {
        fields: [
            { key: 'name', selector: '.info-name' },
            { key: 'assetType', selector: '.info-type' },
            { key: 'installDate', selector: '.info-date', transform: this.formatDate },
        ],
        // 연쇄 fetch (모델 → 벤더 등)
        chain: {
            vendor: '.info-vendor',
        },
    },

    // 메트릭 카드 영역
    powerStatus: {
        metrics: {
            load: { label: '부하율', unit: '%', metricCode: 'LOAD_PCT', scale: 1.0 },
            temp: { label: '온도',   unit: '°C', metricCode: 'TEMP',     scale: 0.1 },
        },
        selectors: {
            card: '.metric-card',
            label: '.metric-label',
            value: '.metric-value',
            unit: '.metric-unit',
        },
    },

    // 차트 영역 (탭 구성)
    chart: {
        tabs: {
            current: { label: '전류', unit: 'A', inputCode: 'INPUT_A', outputCode: 'OUTPUT_A' },
            voltage: { label: '전압', unit: 'V', inputCode: 'INPUT_V', outputCode: 'OUTPUT_V' },
        },
        series: {
            input:  { label: '입력', color: '#f59e0b' },
            output: { label: '출력', color: '#22c55e' },
        },
        selectors: {
            container: '.chart-container',
            tabBtn: '.tab-btn',
        },
    },
};
```

### 2. datasetInfo 배열

각 데이터셋의 fetch 방법과 렌더링 대상을 정의합니다.

```javascript
const { datasetNames, api } = this.config;
const baseParam = { baseUrl: this._baseUrl, assetKey: this._defaultAssetKey };

this.datasetInfo = [
    {
        datasetName: datasetNames.assetDetail,
        param: { ...baseParam },
        render: ['renderBasicInfo'],      // 이 데이터로 호출할 메서드 이름 배열
        refreshInterval: 0                // 0 = 1회만 fetch, > 0 = 주기적 fetch (ms)
    },
    {
        datasetName: datasetNames.metricLatest,
        param: { ...baseParam },
        render: ['renderPowerStatus'],
        refreshInterval: 5000             // 5초마다 갱신
    },
    {
        datasetName: datasetNames.metricHistory,
        param: { ...baseParam, ...api.trendParams, apiEndpoint: api.trendHistory },
        render: ['renderTrendChart'],
        refreshInterval: 5000
    },
];
```

**render 배열**: 하나의 dataset 응답으로 여러 렌더 함수를 호출할 수 있습니다.

### 3. 팝업 라이프사이클

```javascript
// 팝업 HTML/CSS는 properties.publishCode에서 추출
const { htmlCode, cssCode } = this.properties.publishCode || {};

this.getPopupHTML = () => extractTemplate(htmlCode || '', this._popupTemplateId);
this.getPopupStyles = () => cssCode || '';
this.onPopupCreated = onPopupCreated.bind(this, popupCreatedConfig);

// Mixin 적용
applyShadowPopupMixin(this, {
    getHTML: this.getPopupHTML,
    getStyles: this.getPopupStyles,
    onCreated: this.onPopupCreated,
});

// 차트가 필요하면 추가
applyEChartsMixin(this);
```

### 4. onPopupCreated (팝업 생성 직후 초기화)

```javascript
const popupCreatedConfig = {
    chartSelector: this.config.chart.selectors.container,
    events: {
        click: {
            '.close-btn': () => this.hideDetail(),
            '.tab-btn': (e) => this._switchTab(e.target.dataset.tab),
        },
    },
};

function onPopupCreated({ chartSelector, events }) {
    // 1. 차트 초기화
    chartSelector && this.createChart(chartSelector);

    // 2. 팝업 내부 이벤트 바인딩
    events && this.bindPopupEvents(events);

    // 3. 초기 라벨 렌더링 (config의 label/unit 값 적용)
    this.renderInitialLabels();
}
```

### 5. showDetail / hideDetail (외부 API)

```javascript
// 페이지가 호출하는 공개 메서드 (인자 없음)
function showDetail() {
    // assetKey는 초기화 시 this._defaultAssetKey에 이미 설정됨

    // 팝업 표시
    this.showPopup();

    // 모든 datasetInfo를 fetchData로 호출 (인라인)
    fx.go(
        this.datasetInfo,
        fx.each(d => fetchDatasetAndRender.call(this, d))
    );

    // refreshInterval > 0인 데이터셋에 대해 주기적 갱신 시작
    this.stopRefresh();
    fx.go(
        this.datasetInfo,
        fx.filter(d => d.refreshInterval > 0),
        fx.each(d => {
            d._intervalId = setInterval(
                () => fetchDatasetAndRender.call(this, d),
                d.refreshInterval
            );
        })
    );
}

function hideDetail() {
    this.stopRefresh();
    this.hidePopup();
}
```

**주의:** `fetchAllDatasets`라는 별도 함수는 존재하지 않습니다. fetch + interval 로직은 `showDetail` 안에 인라인으로 작성합니다.

### 6. 헬퍼 함수 (모든 팝업 컴포넌트 공통)

```javascript
// HTML 템플릿에서 특정 template 추출
function extractTemplate(htmlCode, templateId) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlCode, 'text/html');
    const template = doc.querySelector(`template#${templateId}`);
    return template?.innerHTML || '';
}

// 응답에서 데이터 안전 추출
function extractData(response, path = 'data') {
    if (!response?.response) return null;
    const data = response.response[path];
    return data !== null && data !== undefined ? data : null;
}
```

이 두 함수는 **모든 팝업 컴포넌트의 register.js 상단에 정의**합니다.

### 7. fetch + render 패턴

```javascript
function fetchDatasetAndRender(d) {
    const { datasetName, param, render } = d;

    fetchData(this.page, datasetName, param)
        .then(response => {
            const data = extractData(response);
            if (!data) return;
            fx.each(fn => this[fn](response), render);
        })
        .catch(e => console.warn(`[Component] ${datasetName} fetch failed:`, e));
}

function stopRefresh() {
    fx.go(
        this.datasetInfo,
        fx.filter(d => d._intervalId),
        fx.each(d => {
            clearInterval(d._intervalId);
            d._intervalId = null;
        })
    );
}
```

**주의사항:**
- `fetchDatasetAndRender`는 `async/await`가 아닌 `.then()/.catch()` 체인 사용
- `fetchData`는 `Wkit`에서 import: `const { fetchData } = Wkit;`
- `extractData`는 `response.response.data`를 안전하게 추출하는 헬퍼
- render 배열 순회에 `fx.each` 사용 (Array.forEach 아님)
- `stopRefresh`는 `fx.go` 파이프라인 사용

### 8. Transform 함수 패턴

config의 `transform`에 사용되는 변환 함수입니다.

```javascript
// config에서 참조 (bind 방식)
this.statusTypeToLabel = statusTypeToLabel.bind(this);
this.statusTypeToDataAttr = statusTypeToDataAttr.bind(this);
this.formatDate = formatDate.bind(this);

// 변환 함수 정의
function statusTypeToLabel(statusType) {
    const { statusMap } = this.config;
    const entry = statusMap[statusType] || statusMap.DEFAULT;
    return entry.label;
}

function statusTypeToDataAttr(statusType) {
    const { statusMap } = this.config;
    const entry = statusMap[statusType] || statusMap.DEFAULT;
    return entry.dataAttr;
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    try {
        const date = new Date(dateStr);
        return date.toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch { return dateStr; }
}

// 범용 필드 렌더링
function renderField(ctx, data, field) {
    const el = ctx.popupQuery(field.selector);
    if (!el) return;
    let value = data[field.key] ?? field.fallback ?? '-';
    if (field.transform) value = field.transform(value);
    if (field.dataAttr) {
        el.dataset[field.dataAttr] = value;
    } else {
        el.textContent = value;
    }
}
```

### 9. Runtime Parameter Update API

페이지가 런타임에 컴포넌트 설정을 변경할 수 있는 메서드입니다.

```javascript
// 전역 파라미터 변경 (assetKey, baseUrl 등)
function updateGlobalParams(options) {
    const { assetKey, baseUrl, locale } = options;
    if (assetKey !== undefined) this._defaultAssetKey = assetKey;

    this.datasetInfo.forEach(d => {
        if (assetKey !== undefined) d.param.assetKey = assetKey;
        if (baseUrl !== undefined)  d.param.baseUrl = baseUrl;
        if (locale !== undefined)   d.param.locale = locale;
    });
}

// 특정 dataset의 refreshInterval 변경
function updateRefreshInterval(datasetName, interval) {
    const target = this.datasetInfo.find(d => d.datasetName === datasetName);
    if (!target) return;
    target.refreshInterval = interval;
}

// 차트 탭/시리즈 메트릭 변경
// 네이밍 규칙: update + 컴포넌트명 + TabMetric (또는 SeriesMetric)
//   예: updateUpsTabMetric, updatePduTabMetric,
//       updateCracSeriesMetric, updateSensorSeriesMetric
function updateUpsTabMetric(tabName, options) {
    const { inputCode, outputCode, statsKey, label, unit } = options;

    // metricCode 변경 시 statsKey가 없으면 거부
    if ((inputCode !== undefined || outputCode !== undefined) && statsKey === undefined) {
        console.warn(`[updateUpsTabMetric] metricCode 변경 시 statsKey 필수`);
        return;
    }
    // ... 탭 업데이트 + statsKeyMap 업데이트 + metricCodes 재구축
}
```

---

## beforeDestroy 패턴

```javascript
// 1. interval 정리
this.stopRefresh();

// 2. 팝업 파괴 (Shadow DOM + 차트 + 이벤트 리스너)
this.destroyPopup();

// 3. 캐시 데이터 정리 (컴포넌트별로 다름)
this._trendData = null;
// PDU의 경우: this._trendDataComparison = null;
```

**주의:**
- `destroyPopup()`이 팝업 내부의 차트/테이블/이벤트를 **모두** 정리합니다
- 일반 컴포넌트와 달리 **메서드 null 할당은 하지 않습니다** (실제 UPS/PDU/CRAC 모두 미사용)
- `stopRefresh()` → `destroyPopup()` → 캐시 null 순서만 지키면 됩니다

---

## 3D 이벤트 바인딩

3D 씬에서 사용할 때는 `bindEvents` 대신 `bind3DEvents`를 사용합니다.

```javascript
// 3D 컴포넌트의 이벤트
this.customEvents = { click: '@assetClicked' };
bind3DEvents(this, this.customEvents);

// 2D 컴포넌트는 기존 방식
this.customEvents = { click: { '.item': '@itemClicked' } };
bindEvents(this, this.customEvents);
```

---

## 출력 구조

```
components/[ComponentName]/
├── views/component.html       # 팝업 템플릿 (<template id="popup-xxx">)
├── styles/component.css
├── scripts/
│   ├── register.js
│   └── beforeDestroy.js       # stopRefresh() + destroyPopup() 호출
├── preview.html
└── README.md
```

---

## 금지 사항

- ❌ 팝업 없이 컴포넌트가 직접 fetch
- ❌ datasetInfo의 render 배열 누락
- ❌ refreshInterval > 0인데 stopRefresh 미구현
- ❌ metricCode 변경 시 statsKey 없이 변경
- ❌ destroyPopup() 호출 누락
- ❌ datasetName 기반 데이터 응답을 받는 함수에서 `function(response)` 사용 → `function({ response })` 필수

---

## 관련 자료

| 참조 | 위치 | 특징 |
|------|------|------|
| UPS (기본) | [/RNBT_architecture/Projects/ECO/page/components/UPS/](/RNBT_architecture/Projects/ECO/page/components/UPS/) | config 패턴, 4카드 + 3탭 차트 |
| PDU (탭 UI + 비교 차트) | [/RNBT_architecture/Projects/ECO/page/components/PDU/](/RNBT_architecture/Projects/ECO/page/components/PDU/) | 4탭 차트 + 금일/전일 비교 |
| CRAC (듀얼 Y축 차트) | [/RNBT_architecture/Projects/ECO/page/components/CRAC/](/RNBT_architecture/Projects/ECO/page/components/CRAC/) | 듀얼 Y축 ECharts + 6개 BOOL 인디케이터 |
| TempHumiditySensor (센서) | [/RNBT_architecture/Projects/ECO/page/components/TempHumiditySensor/](/RNBT_architecture/Projects/ECO/page/components/TempHumiditySensor/) | 2카드 + 바/라인 복합 차트 |
