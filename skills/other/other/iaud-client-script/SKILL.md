---
name: iaud-client-script
description: i-AUD 클라이언트 스크립트 개발 가이드. 브라우저에서 실행되는 TypeScript 스크립트 작성법을 안내합니다. "클라이언트 스크립트", "버튼 이벤트", "그리드 조작", "UI 컨트롤", "Matrix API", "화면 개발" 등을 물어볼 때 사용하세요.
---

# i-AUD 클라이언트 스크립트 개발 가이드

## 1. 개요

클라이언트 스크립트는 브라우저에서 실행되며, UI 컨트롤 조작, 이벤트 처리, 데이터 바인딩 등을 담당합니다.

**파일 위치**: `[보고서폴더]/[보고서명].script.ts` 또는 `[보고서폴더]/[보고서명].script.js`

---

## 2. 기본 구조

```typescript
// 필수 import 구문
import { Matrix } from "@AUD_CLIENT/control/Matrix";
import { Button } from "@AUD_CLIENT/control/Button";
import { DataGrid } from "@AUD_CLIENT/control/DataGrid";
import { TextBox } from "@AUD_CLIENT/control/TextBox";
import { ComboBox } from "@AUD_CLIENT/control/ComboBox";
import { DataSet } from "@AUD_CLIENT/data/DataSet";

// Matrix 변수 선언 (필수)
let Matrix: Matrix;

// 컨트롤 변수 선언
let btnSearch: Button;
let grdData: DataGrid;
let txtKeyword: TextBox;

/**
 * 문서 로드 완료 시 초기화 (권장)
 * - 모든 컨트롤이 로드된 후 실행됨
 */
Matrix.OnDocumentLoadComplete = function(sender, args){   
    // 컨트롤 바인딩
    btnSearch = Matrix.getObject("btnSearch") as Button;
    grdData = Matrix.getObject("grdData") as DataGrid;
    txtKeyword = Matrix.getObject("txtKeyword") as TextBox;

    // 이벤트 등록
    btnSearch.OnClick = btnSearchOnClick;
}; 
// 버튼 클릭 이벤트
const btnSearchOnClick = function(sender, args){
    
};
```

> VS Code에서 `AUD: Generate Starter Code` 명령을 사용하면 자동으로 생성됩니다.

### 2.1 초기화 이벤트

| 이벤트 | 설명 | 용도 |
|--------|------|------|
| `OnDocumentLoadComplete` | 문서 로드 완료 후 발생 (권장) | 컨트롤 초기화, 이벤트 등록 |
| `OnLoadComplete` | 모든 데이터 실행 완료 후 발생 | 일반 초기화 |
---

## 3. 핵심 API - Matrix 객체

Matrix는 i-AUD 클라이언트의 핵심 객체로, 모든 컨트롤 접근과 유틸리티 기능을 제공합니다.

### 3.1 컨트롤 접근

```typescript
// 컨트롤 가져오기
let button = Matrix.getObject("Button1") as Button;
let grid = Matrix.getObject("DataGrid1") as DataGrid;
let textbox = Matrix.getObject("TextBox1") as TextBox;
```

### 3.2 메시지 표시

```typescript
// 알림창
Matrix.Alert("저장되었습니다.");

// 확인 대화상자
Matrix.Confirm("삭제하시겠습니까?", "확인", function(ok) {
    if (ok) {
        // 확인 클릭 시 처리
    }
}, 0);  // 0: 예/아니오, 1: 확인/취소
```

### 3.3 서비스 호출 (서버 스크립트 실행)

```typescript
// 파라미터 리스트
let paramList ={"VS_CODE":"codevalue"
   	,"VS_NAME":"name value"
     };
//서비스 호출
Matrix.RunScriptEx(["gridName"], "ServerScriptName"
    , paramList
    ,function (p) {
        //call back
        if (p.Success == false) {
            Matrix.Alert(p.Message);
            return;
        }
        var ds = p.DataSet;
    });     
```

### 3.4 전역 파라미터

```typescript
// 전역 파라미터 설정
Matrix.AddGlobalParams("YEAR", "2025", enQueryParamType.String);

// 전역 파라미터 삭제
Matrix.ClearGlobalParams();
```

---

## 4. 주요 컨트롤 API

### 4.1 Button (버튼)

```typescript
let btn = Matrix.getObject("Button1") as Button;

// 속성
btn.Text = "검색";
btn.IsEnabled = false;  // 비활성화
btn.Visible = false;    // 숨김

// 이벤트
btn.OnClick = function(sender, args) {
    Matrix.Alert("버튼 클릭: " + args.Id);
};
```

### 4.2 TextBox (텍스트박스)

```typescript
let txt = Matrix.getObject("TextBox1") as TextBox;

// 속성
let value = txt.Text;     // 값 읽기
txt.Text = "새 값";       // 값 설정
txt.MaxLength = 100;      // 최대 길이

// 이벤트
txt.OnTextChange = function(sender : TextBox, args : {Id: string, Text: string}) {
    console.log("변경된 값:", args.Text);
};
```

### 4.3 ComboBox (콤보박스)

```typescript
let combo = Matrix.getObject("ComboBox1") as ComboBox;

// 속성
let selectedValue = combo.Value;
let selectedText = combo.Text;
combo.SelectedIndex = 0;  // 첫 번째 항목 선택

// 이벤트
combo.OnValueChanged = function(sender : ComboBox, args : {Id: string,Value: string,SelectedIndex: number}) {
    console.log("선택값:", args.Value);
};
```

### 4.4 DataGrid (데이터 그리드)

```typescript
let dataGrid = Matrix.getObject("DataGrid1") as DataGrid;

// 행 조회
let rowCount = dataGrid.GetRowCount();
let row = dataGrid.GetRow(0);  // 첫 번째 행

// 셀 값 읽기/쓰기
let cellValue = row.GetValue("ColumnName");
row.SetValue("ColumnName", "새 값");

// 행 추가/삭제
let newRow = dataGrid.AppendRow();
dataGrid.RemoveRowAt(0, true);

// 페이징
dataGrid.UsePaging = true;
dataGrid.PageSize = 20;
dataGrid.MovePage(2);  // 2페이지로 이동

// 이벤트
dataGrid.OnCellClick = function(sender : DataGrid, args : { Id: string,Row: DataGridRow,Cell: DataGridCell,Field: DataGridColumn,Handled: boolean}) {
    console.log("클릭한 셀:", args.Row.GetValue("fieldName"), args.Field.Name);
};
```

### 4.5 iGrid (Excel 형식 그리드)

```typescript
let igrid = Matrix.getObject("iGrid1") as iGrid;
//엑셀 저장 하기
igrid.ExportServiceCall(enExportType.Excel,
        function(p){
        //   
        //   p.FolderName = file path
        //   p.FileName = file name
        //   
        var newName = "MXGrid_" + Matrix.GetDateTime().ToString("yyyyMMddHHmmss") + ".xlsx";
        Matrix.DownloadFile(p.FolderName, p.FileName ,newName ,true);
} ); 
```

### 4.6 Chart (차트)

```typescript
let chart = Matrix.getObject("Chart1") as Chart;

// 차트 옵션 접근
let options = chart.ChartOptions;

// 차트 다시 그리기
chart.Update();
```

### 4.7 OlapGrid (OLAP 그리드)

```typescript
let olap = Matrix.getObject("OlapGrid1") as OlapGrid;

// 필터 설정
olap.setDimensionFilterIn("DimensionName", ["Value1", "Value2"]);

// 데이터 새로고침
olap.Refresh();

// 이벤트
olap.OnDataCellDoubleClick = function(sender, args) {
    console.log("더블클릭:", args);
};
```

---

## 5. 공통 컨트롤 속성 (Control)

모든 컨트롤이 상속받는 기본 속성입니다.

```typescript
// 위치/크기 
control.Left = 100;
control.Top = 50;
control.Width = 200;
control.Height = 30;

// 표시 여부
control.Visible = true;
control.IsEnabled = true;

// 스타일
control.Tooltip = "도움말 텍스트";
control.ZIndex = 10;

// 메서드
control.Focus();      // 포커스 설정
control.Update();     // 화면 갱신
control.Resize();     // 크기 재계산

// 위치/크기 일괄 설정
control.setRect({Left: 100, Top: 50, Width: 200, Height: 30} as Rect);
control.Resize();
```

---

## 6. 데이터 관련 API

### 6.1 DataSet

```typescript
let ds: DataSet = Matrix.CreateDataSet("DataSetName");

// 테이블 접근
let table = ds.GetTable(0);  // 인덱스로
let table = ds.GetTable("TableName");  // 이름으로

// 테이블 생성
let newTable = ds.CreateTable("NewTable");
```

### 6.2 DataTable

```typescript
let table = ds.GetTable("Table1");
let rowCount = table.GetRowCount();

// 행 접근
let row = table.GetRow(0);

// 행 추가
let nIdx = table.AppendRow();
table.setRowValue(nIdx, "FIELD_NAME", "value")

// 컬럼 정보
let columnNames = table.GetColumnNames();
for(let i=0,i2=columnNames.length;i<i2; i++){
    table.setRowValue(nIdx, columnNames[i], "value...");
}
```

### 6.3 DataRow

```typescript
let row = table.GetRow(0);

// 값 읽기/쓰기
let value = row.GetValue("ColumnName");
row.SetValue("ColumnName", "새 값");

// 인덱스로 접근
let value = row.GetValue(0);
```

---

## 7. 유틸리티

### 7.1 날짜 유틸리티

```typescript

//날자로 변환
let date = Matrix.getDate("2025-12-12", "yyyy-MM-dd");
let addDay = date.AddDays(10).Day;
//현재일자
let nowdate = Matrix.getDate(); 
let text = nowdate.AddDays(-7).ToString("yyyy-MM-dd");

```

### 7.2 문자열 유틸리티

```typescript
let strUtil = Matrix.getStringUtility();
let formatted = strUtil.Format("{0}년 {1}월", "2025", "01");
```

### 7.3 사용자/보고서 정보

```typescript
// 사용자 정보
let userInfo = Matrix.getUserInfo();
let userId = userInfo.UserCode;
let userName = userInfo.UserName;

// 보고서 정보
let reportInfo = Matrix.getReportInfo();
let reportCode = reportInfo.ReportCode;
```

---

## 8. 이벤트 핸들러 패턴

```typescript
// 버튼 클릭 이벤트
let btnSearch = Matrix.getObject("btnSearch") as Button;
btnSearch.OnClick = function(sender, args) {
    // 검색 로직
    Matrix.ExecuteService("SearchService", function(result) {
        if (result.Success) {
            Matrix.Alert("조회 완료");
        }
    });
};

// 그리드 셀 변경 이벤트
let grid = Matrix.getObject("DataGrid1") as DataGrid;
grid.OnEndEdit = function(sender, args) {
    console.log("변경됨:", args.Row.GetValue("필드명"), args.AfterValue, args.BeforeValue, args.Field.Name);
    
};
```

---

## 9. 샘플 코드 위치

실제 구현 예제는 다음 폴더를 참조하세요:

- `src/reports/samples/MX_GRID/` - MX-GRID 관련 샘플
- `src/reports/samples/OLAP/` - OLAP 그리드 샘플
- `src/reports/samples/ETC/` - 기타 기능 샘플

---

## 10. API 인터페이스 위치

상세 API 정의는 `types/aud/` 폴더를 참조하세요:

- `types/aud/control/` - UI 컨트롤 인터페이스
- `types/aud/data/` - 데이터 관련 인터페이스
- `types/aud/common/` - 공통 유틸리티
- `types/aud/enums/` - 열거형 타입
