---
name: create-standard-component
description: 표준 RNBT 컴포넌트를 생성합니다. 페이지가 GlobalDataPublisher로 데이터를 제어합니다.
---

# 표준 컴포넌트 생성

페이지가 GlobalDataPublisher로 데이터를 제어하고, 컴포넌트는 구독만 합니다.

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
2. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일

---

## 핵심 원칙

### 1. 역할 분리

```
페이지 = 오케스트레이터
- 데이터 정의 (globalDataMappings)
- Interval 관리 (refreshIntervals)
- 이벤트 핸들러 등록 (eventBusHandlers)

컴포넌트 = 독립적 구독자
- topic 구독 (subscriptions)
- 이벤트 발행 (@eventName)
- 렌더링만 집중
```

### 2. 메서드 분리 (재사용성)

**핵심: 컴포넌트 재사용을 위해 메서드를 철저히 분리한다.**

```javascript
// 고정 (재사용)
function renderChart(config, { response }) {
    const { optionBuilder, ...chartCfg } = config;
    const option = optionBuilder(chartCfg, data);
    this.chartInstance.setOption(option, true);
}

// 가변 (컴포넌트별)
const chartConfig = { optionBuilder: getChartOption };
this.renderChart = renderChart.bind(this, chartConfig);
```

| 구분 | 역할 | 재사용 |
|------|------|--------|
| renderChart / renderTable | 규격화된 렌더링 함수 | O (고정) |
| chartConfig / tableConfig | 데이터 매핑 + 옵션 | X (컴포넌트별) |
| optionBuilder | ECharts/Tabulator 옵션 생성 | X (컴포넌트별) |

### 3. 이벤트 처리 기준

| 페이지가 알아야 하는가? | 처리 | 예시 |
|----------------------|------|------|
| 아니오 | `_internalHandlers` | Clear, Toggle |
| 예 | `customEvents` + `bindEvents` | 행 선택, 필터 변경 |

### 4. 응답 구조

```javascript
// response 키가 한 번 더 감싸져 있음
function renderData(config, { response }) {
    const { data, meta } = response;
}
```

---

## 출력 구조

```
[ComponentName]/
├── views/component.html
├── styles/component.css
├── scripts/
│   ├── register.js
│   └── beforeDestroy.js
├── preview.html
└── README.md
```

---

## 핵심 패턴

### PUB-SUB (GlobalDataPublisher)

```javascript
this.subscriptions = {
    topicA: ['renderData'],
    topicB: ['renderList', 'updateCount']
};
```

### Event-Driven (Weventbus)

```javascript
this.customEvents = {
    click: { '.btn-refresh': '@refreshClicked' },
    change: { '.filter-select': '@filterChanged' }
};
```

---

## 금지 사항

- ❌ 컴포넌트가 직접 fetch (팝업 없이)
- ❌ 생성 후 정리 누락
- ❌ `function(response)` 사용 → `function({ response })` 필수

---

## 관련 자료

| 문서 | 위치 |
|------|------|
| 예제 | [/RNBT_architecture/Examples/SimpleDashboard/](/RNBT_architecture/Examples/SimpleDashboard/) |
