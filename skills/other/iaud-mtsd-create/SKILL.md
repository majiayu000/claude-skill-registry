---
name: iaud-mtsd-create
description: i-AUD MTSD 문서 생성 가이드. 새 보고서의 .mtsd 파일을 처음부터 만들 때 사용합니다. MCP 생성 도구(generate_element, generate_grid_column, generate_datasource)의 활용법과 MTSD 루트 구조 템플릿, Element 타입별 패턴, Docking 레이아웃, DataGrid 컬럼 패턴을 포함합니다. "MTSD 만들기", "보고서 생성", "화면 만들기", "새 프로그램", "Element 추가" 등을 요청할 때 사용하세요.
---

# i-AUD MTSD 문서 생성 가이드

## 1. 개요

MTSD (.mtsd) 파일은 i-AUD 보고서의 화면 UI 배치, 데이터소스, 서비스를 정의하는 JSON 문서입니다.

### MCP 생성 도구 활용

`aud_mcp_server` MCP 서버의 생성 도구를 사용하면 복잡한 JSON 구조를 간소화된 입력으로 빠르게 만들 수 있습니다.

| MCP 도구 | 용도 |
|----------|------|
| `generate_element` | Element 1개 생성 (Label, Button, DataGrid, Group 등) |
| `generate_grid_column` | DataGrid의 GridColumn 배열 생성 |
| `generate_datasource` | DataSource 1개 생성 (SQL 파라미터 자동 추출) |
| `validate_mtsd` | 완성된 MTSD 문서 전체 검증 |
| `validate_part` | 부분 검증 (Element, DataSource 등 개별 검증) |
| `fix_mtsd` | MTSD 파일 자동 보정 (파일 경로 입력 → 읽고 수정 후 덮어쓰기) |

### ID 생성 규칙 (UUID 형식)

MTSD 문서에서 사용하는 모든 **Id** 값은 **접두사 + 32자리 대문자 HEX** (UUID without dashes) 형식을 따릅니다.

| 항목 | 접두사 | 예시 |
|------|--------|------|
| ReportCode | `REP` | `REP2EDC58234142492D8829411E8C0FD90B` |
| DataSource Id | `DS` | `DS902D12727EFC4373A2BCA30935FC6109` |
| Form Id | `Form` | `FormD64B8652095A4B9798E93B38EDBCCCD4` |
| Element Id | `{타입명}` | `Group2B4BD0E69A92CDBCD029B105CA49D457` |
|  |  | `DataGridF080EDCACB22D1D56A21D1B1E3AE9017` |
|  |  | `LabelA9693D8ACAE63C7AEDBE7AA0D37A9CEB` |
|  |  | `Button31C6D3784F6E49F90EE81B75752BC500` |
|  |  | `TextBoxDA3777D9E0B17780BCB31B58D859EA40` |
|  |  | `ComboBox974223E5E3F8F649965F6D538A2B02D5` |

> **Id vs Name 구분**:
> - **Id**: 시스템 내부 식별자 → 반드시 `접두사 + UUID(32 HEX)` 형식
> - **Name**: 사람이 읽는 이름 → `GRP_HEADER`, `GRD_SALES`, `BTN_SEARCH` 등 의미 있는 이름 사용

> **중요**: `REPSALESPERF0001...`, `REPMYREPORT...` 같은 의미 있는 문자열을 Id에 사용하지 마세요. 반드시 랜덤 UUID를 생성합니다.

**UUID HEX 생성 방법** (32자리 랜덤 대문자 HEX):
```javascript
crypto.randomUUID().replace(/-/g, '').toUpperCase()
// 결과: "2EDC58234142492D8829411E8C0FD90B"
```

---

## 2. MTSD 루트 구조 템플릿

새 MTSD 문서를 만들 때 이 구조에서 시작합니다:

```json
{
  "ReportInfo": {
    "ReportCode": "{보고서코드}",
    "FolderCode": "{폴더코드}",
    "SavePath": "{폴더코드}/{보고서코드}.mtsd",
    "ReportName": "{보고서명}",
    "Writer": "",
    "WriteDate": "",
    "Editor": "",
    "EditDate": "",
    "TabPosition": 0,
    "UsePersonalConditions": false,
    "DocumentVersion": "3.0.0.0",
    "RefreshType": 0
  },
  "DataSources": {
    "Datas": []
  },
  "ScriptText": "",
  "ServerScriptText": [],
  "Forms": [
    {
      "Id": "Form{32자HEX}",
      "Name": "Form1",
      "Activated": true,
      "Visible": true,
      "LanguageCode": "",
      "Style": {
        "Type": 0,
        "BoxStyle": "",
        "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" },
        "Background": {}
      },
      "Elements": []
    }
  ],
  "MetaDataSources": {
    "TemplateMeta": { "TemplateName": "" },
    "MetaDataSources": []
  }, 
  "EXECUTION_PLANS": [],
  "Variables": [],
  "Modules": [],
  "ResponsiveLayout": [],
  "Langs": [],
  "WorkFlowModules": [],
  "WorkFlowInfo": ""
}
```

---

## 3. MCP 생성 도구 사용법

### 3.1 generate_element — Element 생성

간소화된 입력으로 스키마 준수 Element JSON을 생성합니다.

**단축 표기:**

| 입력 | 설명 | 예시 |
|------|------|------|
| `type` | Element 타입 (필수) | `"Label"`, `"Button"`, `"DataGrid"` |
| `id` | Element ID (생략 시 자동) | `"LBL_TTL"` |
| `text` | 텍스트 (Label→Text, Button→Value) | `"판매실적 조회"` |
| `position` | 위치/크기 | `{ "left": 15, "top": 12, "width": 200, "height": 30 }` |
| `docking` | 도킹 단축 | `"left"`, `"left+right"`, `"fill"` |
| `font` | 폰트 단축 | `{ "size": 16, "bold": true, "color": "#333" }` |
| `background` | 배경색 | `"#F5F5F5"` |
| `border` | 테두리 | `"solid 1px #DDD"`, `"none"` |
| `color` | 텍스트 색상 | `"#333333"` |

**사용 예시:**

```
generate_element({
  type: "Label",
  id: "LBL_TTL",
  text: "판매실적 조회",
  position: { left: 15, top: 12, width: 200, height: 30 },
  font: { size: 16, bold: true, color: "#333333" },
  docking: "left"
})
```

### 3.2 generate_grid_column — GridColumn 배열 생성

```
generate_grid_column({
  columns: [
    { name: "CHK", header: "선택", type: "checkbox", width: 50 },
    { name: "SALES_ID", header: "판매ID", width: 100, align: "center" },
    { name: "CUST_NAME", header: "고객명", width: 150 },
    { name: "UNIT_PRICE", header: "단가", width: 100, format: "#,##0", align: "right" }
  ]
})
```

**컬럼 타입 매핑:**

| type | ColumnType | 자동 설정 |
|------|-----------|----------|
| `"text"` | 0 | 기본값 |
| `"checkbox"` | 1 | Editable: true |
| `"combo"` | 2 | DefinedItems 설정 가능 |
| (format 지정) | — | DataType: 1(Number), TextPosition: "right" |

### 3.3 generate_datasource — DataSource 생성

```
generate_datasource({
  name: "GRD_SALES",
  connection: "AUD_SAMPLE_DB",
  sql: "SELECT SP.SALES_ID FROM SM_SALES_PERFORMANCE SP WHERE SP.SALES_DATE >= @:VS_YMD_FROM",
  columns: [
    { name: "SALES_ID", type: "string" },
    { name: "SALES_DATE", type: "string" }
  ]
})
```

- `params` 생략 시 SQL에서 `@:PARAM`, `:PARAM`, `%:PARAM` 패턴 자동 추출
- Id는 `DS` + 32자리 HEX로 자동 생성
- 기본값: `UseMeta:  false`, `UseCache: false`, `Encrypted: false`, `DSType: 0`

---

## 4. Docking 레이아웃 패턴

### 4.1 Docking 동작 원리

Docking은 컨트롤의 가장자리를 **부모 컨트롤 영역의 가장자리에 맞추는** 자동 맞춤 기능입니다.

- `Left: true` → 컨트롤의 왼쪽 가장자리를 부모의 왼쪽에 맞춤
- `Right: true` → 컨트롤의 오른쪽 가장자리를 부모의 오른쪽에 맞춤
- `Top: true` → 컨트롤의 **상단을 부모의 상단(0)**에 맞춤
- `Bottom: true` → 컨트롤의 **하단을 부모의 하단**에 맞춤

> **주의**: `Top: true`는 컨트롤의 Top 위치를 유지하는 것이 아니라, **부모 영역의 Top(0)에 맞추는 것**입니다. 마찬가지로 `Bottom: true`는 부모의 Bottom에 맞춥니다. 따라서 `fill`(모두 true)을 사용하면 부모 영역 전체를 덮게 됩니다.

### 4.2 기본 패턴

| 도킹 | Left | Right | Top | Bottom | 용도 |
|------|------|-------|-----|--------|------|
| `"none"` | F | F | F | F | 고정 위치/크기 |
| `"left"` | T | F | F | F | 왼쪽 고정 |
| `"right"` | F | T | F | F | 오른쪽 고정 |
| `"left+right"` | T | T | F | F | 좌우 확장 (헤더, 검색바, 고정 높이 그룹) |
| `"left+right+bottom"` | T | T | F | T | 좌우 확장 + 하단 채움 (**그리드, 본문 영역**) |
| `"fill"` | T | T | T | T | 부모 영역 전체 채움 (단독 배치 시만 사용) |
| `"bottom"` | F | F | F | T | 하단 고정 |

### 4.3 일반적인 화면 레이아웃

```
┌─────────────────────────────────────────┐
│  GRP_HEADER (docking: "left+right")     │  고정 높이 55
│  ├─ LBL_TTL (제목)                       │  Top: false
│  └─ BTN_SEARCH, BTN_SAVE (버튼)          │  Bottom: false
├─────────────────────────────────────────┤
│  GRP_SEARCH (docking: "left+right")     │  고정 높이 60~80
│  ├─ LBL_FROM, CAL_FROM (조건 1)          │  Top: false
│  └─ LBL_TO, CAL_TO (조건 2)              │  Bottom: false
├─────────────────────────────────────────┤
│  GRD_MAIN (docking: "left+right+bottom")│  나머지 영역
│  DataGrid                               │  Top: false ← 상단 위치 유지
│                                         │  Bottom: true ← 하단으로 확장
└─────────────────────────────────────────┘
```

### 4.4 Docking 선택 가이드

| 배치 유형 | 올바른 Docking | 설명 |
|-----------|---------------|------|
| 상단 고정 높이 그룹 (헤더, 검색바) | Left+Right | 좌우만 확장, 높이/위치 고정 |
| 하단 고정 높이 그룹 (푸터, 버튼바) | Left+Right+Bottom | 좌우 확장 + 하단 고정, 높이 고정 |
| 그리드/본문 (위에 헤더 있음) | **Left+Right+Bottom** | 좌우 확장 + 하단까지 채움, Top은 false로 상단 위치 유지 |
| 그리드/본문 (단독 배치) | fill | 부모 전체 채움 (위에 다른 요소가 없을 때만) |
| 그룹 내 고정 위치 컨트롤 | none | Label, Button 등 고정 크기 컨트롤 |

> **흔한 실수**: 헤더/검색바 아래에 그리드를 배치할 때 `fill`(모두 true)을 사용하면 그리드가 부모 전체를 덮어 헤더를 가립니다. 반드시 `Top: false`로 설정하여 그리드의 상단 위치를 유지해야 합니다.

### 4.5 Docking 부속 속성

Docking 객체에는 방향(Left/Right/Top/Bottom) 외에 추가 속성이 있습니다.

#### Margin — 부모 영역 안쪽 여백

도킹이 활성화된 방향에 대해 부모 가장자리와 컨트롤 사이의 **안쪽 여백(padding)**을 설정합니다.

- **형식**: `"Left,Top,Right,Bottom"` (픽셀 단위, 쉼표 구분 문자열)
- **기본값**: `"0,0,0,0"` (여백 없음)

```
부모 영역
┌──────────────────────────────────┐
│  ← Left margin                  │
│  ┌────────────────────────────┐  │
│  │  컨트롤 (도킹 적용)        │  │ ↑ Top margin
│  │                            │  │
│  │                            │  │
│  └────────────────────────────┘  │ ↓ Bottom margin
│                   Right margin → │
└──────────────────────────────────┘
```

**사용 예시:**

| Margin 값 | 의미 | 용도 |
|-----------|------|------|
| `"0,0,0,0"` | 여백 없음 | 기본값, 부모 가장자리에 딱 맞춤 |
| `"20,0,20,20"` | 좌·우·하 20px 여백 | 그리드에 좌우·하단 간격 부여 |
| `"20,75,20,20"` | 좌 20, 상 75, 우 20, 하 20 | 상단 헤더 영역(75px)을 피해 배치 |
| `"5,5,5,5"` | 전체 5px 여백 | 그룹 내부 컨트롤 균일 간격 |

#### HoldSize — 도킹 시 크기 유지 (위치만 이동)

- **타입**: `boolean` (기본값: `false`)
- `false`: 도킹 방향으로 컨트롤이 **늘어남** (기본 동작)
- `true`: 컨트롤의 원래 Width/Height를 **유지**하고, 도킹 방향의 가장자리에 **위치만 이동**

> **핵심**: `HoldSize: true`는 크기를 늘리지 않고 **위치만 조정**하는 것입니다. 예를 들어 버튼을 항상 화면 우측에 배치하고 싶을 때 `Right: true` + `HoldSize: true`를 사용하면, 화면 크기가 변해도 버튼이 오른쪽 가장자리에 맞춰 이동만 합니다.

**사용 예시:**

```
화면 너비 변경 시 HoldSize 동작 비교:

HoldSize: false (기본) — 크기가 늘어남
┌─────────────────────────────┐
│ [=========버튼=========]  ← │  Right: true → 우측에 맞추며 너비 확장
└─────────────────────────────┘

HoldSize: true — 위치만 이동
┌─────────────────────────────┐
│                    [버튼]  ← │  Right: true → 우측에 맞추되 원래 크기 유지
└─────────────────────────────┘
```

```json
// 버튼을 항상 우측에서 20px 떨어진 위치에 고정 (크기 변경 없이 이동만)
"Docking": { "Right": true, "HoldSize": true, "Margin": "0,0,20,0" }

// 패널을 우측에 도킹하되 원래 너비(460px) 유지
"Docking": { "Right": true, "Top": true, "Bottom": true, "HoldSize": true, "Margin": "20,75,20,20" }
```

**주요 활용 패턴:**

| 패턴 | 설정 | 용도 |
|------|------|------|
| 우측 고정 버튼 | `Right: true, HoldSize: true` | 조회/저장 버튼을 항상 화면 우측에 배치 |
| 우측 고정 패널 | `Right: true, Top: true, Bottom: true, HoldSize: true` | 상세 패널을 우측에 고정 너비로 배치 |
| 하단 고정 버튼 | `Bottom: true, HoldSize: true` | 버튼을 항상 하단에 배치 (높이 유지) |

#### MinWidth / MinHeight — 최소 크기

- **타입**: `number` (기본값: `0`)
- 도킹으로 크기가 줄어들 때 이 값 이하로는 줄어들지 않음
- 화면 축소 시 컨트롤이 너무 작아지는 것을 방지

---

## 5. Element 타입별 최소 패턴

### 5.1 Label

```json
{
  "Type": "Label", "Id": "LBL_TTL", "Name": "LBL_TTL",
  "Position": { "Left": 15, "Top": 12, "Width": 200, "Height": 30, "ZIndex": 1, "TabIndex": 0,
    "Docking": { "Left": false, "Right": false, "Top": false, "Bottom": false, "Margin": "0,0,0,0", "HoldSize": false, "MinWidth": 0, "MinHeight": 0 }
  },
  "Style": { "Type": 0, "BoxStyle": "", "Background": {}, "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" } },
  "LanguageCode": "", "Text": "제목", "Cursor": "default", "Formula": "",
  "UseTextOverflow": false, "UseAutoLineBreak": false, "LineSpacing": 0, "HasLineSpacing": false,
  "MxBinding": "", "MxBindingUseStyle": false
}
```

### 5.2 Button

```json
{
  "Type": "Button", "Id": "BTN_SEARCH", "Name": "BTN_SEARCH",
  "Position": { "Left": 10, "Top": 10, "Width": 80, "Height": 30, "ZIndex": 1, "TabIndex": 0,
    "Docking": { "Left": false, "Right": false, "Top": false, "Bottom": false, "Margin": "0,0,0,0", "HoldSize": false, "MinWidth": 0, "MinHeight": 0 }
  },
  "Style": { "Type": 0, "BoxStyle": "", "Background": {}, "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" } },
  "LanguageCode": "", "Value": "조회", "Cursor": "pointer", "HasNewRadius": false
}
```

### 5.3 DataGrid (최소)

```json
{
  "Type": "DataGrid", "Id": "GRD_MAIN", "Name": "GRD_MAIN",
  "Position": { "Left": 0, "Top": 100, "Width": 800, "Height": 400, "ZIndex": 1, "TabIndex": 0,
    "Docking": { "Left": true, "Right": true, "Top": false, "Bottom": true, "Margin": "0,0,0,0", "HoldSize": false, "MinWidth": 0, "MinHeight": 0 }
  },
  "Style": { "Type": 0, "BoxStyle": "", "Background": {}, "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" } },
  "CellMargin": "2", "Columns": [], "UsePPTExport": false
}
```

### 5.4 Group (컨테이너)

```json
{
  "Type": "Group", "Id": "GRP_HEADER", "Name": "GRP_HEADER",
  "Position": { "Left": 0, "Top": 0, "Width": 800, "Height": 55, "ZIndex": 1, "TabIndex": 0,
    "Docking": { "Left": true, "Right": true, "Top": false, "Bottom": false, "Margin": "0,0,0,0", "HoldSize": false, "MinWidth": 0, "MinHeight": 0 }
  },
  "Style": { "Type": 0, "BoxStyle": "", "Background": {}, "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" } },
  "ChildElements": []
}
```

### 5.5 ComboBox

```json
{
  "Type": "ComboBox", "Id": "CMB_STATUS", "Name": "CMB_STATUS",
  "Position": { "Left": 100, "Top": 10, "Width": 150, "Height": 25, "ZIndex": 1, "TabIndex": 0,
    "Docking": { "Left": false, "Right": false, "Top": false, "Bottom": false, "Margin": "0,0,0,0", "HoldSize": false, "MinWidth": 0, "MinHeight": 0 }
  },
  "Style": { "Type": 0, "BoxStyle": "", "Background": {}, "Border": { "CornerRadius": "0,0,0,0", "LineType": "none", "Thickness": "0,0,0,0" } },
  "DataSource": "", "Value": "", "Text": "", "InitType": 0, "RefreshType": 0,
  "IsReadOnly": false, "SortType": 0, "AutoRefresh": false, "AfterRefresh": "",
  "UseAllItems": false, "UseAllItemsText": "", "DisplayType": 0,
  "DataSourceInfo": { "LabelField": "", "ValueField": "" }, "InitValue": ""
}
```

---

## 6. 전체 생성 워크플로우

> **필수 규칙**: MTSD 파일을 생성하거나 수정할 때마다 반드시 `validate_mtsd`로 전체 검증을 수행합니다. 속성 타입 오류(예: array를 string으로 기입)나 필수 속성 누락은 MCP 검증으로만 확인할 수 있습니다.

### Step 1: MTSD 루트 구조 생성
위 섹션 2의 템플릿을 복사하고 ReportInfo를 채웁니다.

### Step 2: DataSource 생성
```
generate_datasource({ name: "DS이름", connection: "연결코드", sql: "SELECT ..." })
```
결과를 `DataSources.Datas[]`에 추가합니다.

### Step 3: Element 생성
```
// 헤더 그룹
generate_element({ type: "Group", id: "GRP_HEADER", docking: "left+right", position: { left: 0, top: 0, width: 800, height: 55 } })

// 제목 라벨
generate_element({ type: "Label", id: "LBL_TTL", text: "보고서 제목", font: { size: 16, bold: true } })

// 조회 버튼
generate_element({ type: "Button", id: "BTN_SEARCH", text: "조회" })

// 데이터 그리드 (헤더 아래 배치 시 fill 대신 left+right+bottom 사용)
generate_element({ type: "DataGrid", id: "GRD_MAIN", docking: "left+right+bottom", position: { left: 0, top: 100, width: 800, height: 400 } })
```

### Step 4: GridColumn 생성
```
generate_grid_column({ columns: [...] })
```
결과를 DataGrid의 `Columns`에 설정합니다.

### Step 5: 조합 및 검증
모든 Element를 `Forms[0].Elements[]`에 배치하고 `validate_mtsd`로 전체 검증합니다.

### Step 6: 자동 보정 (fix_mtsd)
MTSD 파일을 **Write/Edit로 저장한 후** `fix_mtsd`를 실행하여 자동 보정합니다.

```
fix_mtsd({ path: "D:/reports/sample/REPXXXXXXXX.mtsd" })
```

- **입력**: MTSD 파일의 **전체 경로** (디스크에 저장된 파일 대상)
- **동작**: 파일을 읽어 보정 규칙을 적용한 뒤 **파일을 덮어씁니다**
- **현재 보정 규칙**:
  - DataSource Name→Id 참조 보정 (Element의 `DataSource`가 Name으로 참조된 경우 Id로 자동 변환)
- **반환값**: `{ fixed: boolean, fixCount: number, fixes: string[], errors: string[] }`

> **중요**: `fix_mtsd`는 파일을 직접 수정하므로 반드시 Write/Edit 이후에 실행하세요. 새 MTSD 생성 시, 수정 시 모두 사용합니다.

### Step 7: 수정 시 재검증 + 재보정
MTSD 파일을 수정(Edit/Write)할 때마다 아래 순서를 따릅니다:
1. `validate_mtsd`로 오류 확인 → 오류 발견 시 수정
2. `fix_mtsd`로 자동 보정 실행 → 보정 결과 확인

---

## 7. DataSource SQL 패턴

> SQL 파라미터 바인딩의 상세 규칙(변수 접두사, 특수 지시자, IN절, Dynamic SQL 등)은 **`/iaud-sql-guide`** 스킬을 참조하세요.

### 주요 바인딩 요약

```sql
SELECT * FROM TABLE
WHERE STATUS = :VS_STATUS              -- 문자열 바인딩 (자동 따옴표 처리)
  AND AMOUNT > :VN_MIN_AMT             -- 숫자 바인딩 (따옴표 없이 값 그대로)
  AND YMD >= @:VS_YMD_FROM             -- @: 빈 값이면 해당 라인 삭제
  AND NAME LIKE %:VS_KEYWORD%          -- %: LIKE 와일드카드 자동 포함
  AND USER_CODE = :VS_USER_CODE$       -- $: 서버 세션(인증) 값 사용
```

| 접두사/지시자 | 설명 |
|-------------|------|
| `:VS_` | 문자열 변수 (자동 따옴표 `'` 감싸짐) |
| `:VN_` | 숫자 변수 (따옴표 없이 값 그대로 치환) |
| `@:` | 빈 값이면 해당 **라인 전체를 삭제** (선택적 조건) |
| `%:` | LIKE 검색 와일드카드 자동 포함 |
| `$` (접미사) | 클라이언트 값 대신 **서버 세션 값** 사용 |

---

## 8. 주의사항

1. **ID/Name 규칙**: Id는 `{타입접두사}` + 32자리 UUID HEX (예: `LabelA9693D8ACAE63C7AEDBE7AA0D37A9CEB`). Name은 `{타입약어}_{용도}` 형식의 의미 있는 이름 (예: `LBL_TTL`, `BTN_SEARCH`, `GRD_MAIN`). ReportCode는 `REP` + UUID, DataSource Id는 `DS` + UUID, Form Id는 `Form` + UUID. 상세 규칙은 섹션 1의 "ID 생성 규칙" 참조
2. **Group 내 Element**: Group의 `ChildElements[]`에 넣고, 자식 Element에 `"InGroup": "그룹ID"` 설정
3. **DataGrid.DataSource**: DataSource의 `Id` 값이 아닌 `Name` 값을 사용
4. **MCP 검증 + 자동 보정 필수**: MTSD 파일을 **생성 또는 수정할 때마다** `validate_mtsd`로 전체 검증 후 `fix_mtsd`로 자동 보정을 수행합니다. `fix_mtsd`는 파일 경로를 받아 직접 파일을 수정하므로 반드시 Write/Edit 이후에 실행합니다.
5. **속성 타입 확인**: 속성 타입이 불확실할 때는 `get_schema_info`로 정확한 타입을 확인한 후 값을 설정합니다. (예: `MetaDataSources.MetaDataSources`는 `array` 타입이므로 `""` 가 아닌 `[]`로 설정)
6. **generate_element 미지원 타입**: 기본 Element 속성만 생성되므로, 반환된 warnings를 확인하고 타입별 필수 속성을 수동 추가
7. **WriteDate/EditDate 패턴**: `YYYY-MM-DD HH:MM:SS` 형식이어야 하며, 빈 문자열은 허용되지 않음
