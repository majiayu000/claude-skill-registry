---
name: iaud-mxgrid-guide
description: i-AUD MX-GRID 개발 가이드. 엑셀 기반 MX-GRID 보고서의 서버 스크립트(WorkBook/WorkSheet API), 클라이언트 스크립트(iGrid API), 예약어(이름 정의), 전용 함수(AUD_xxx), .ds 파일 구조를 안내합니다. "MX-GRID", "엑셀 그리드", "WorkBook", "WorkSheet", "iGrid", "셀 조작", "데이터 바인딩", "CRUD", "PDF 내보내기", "엑셀 내보내기", "예약어", "이름 정의" 등을 물어볼 때 사용하세요.
---

# i-AUD MX-GRID 개발 가이드

## 1. 개요

MX-GRID는 엑셀 문서를 웹에서 표현하는 i-AUD 컨트롤입니다.

**아키텍처 흐름**:
```
[엑셀 파일(.xlsx)]
     │  (서버 변환)
[템플릿 모델(.json2)] ─── 스타일, 셀, 수식, 차트, 이미지, 조건부서식
     │  (서버 WorkBook)
[서버 WorkBook 객체] ◄── [데이터셋(.ds)] ── SQL → 셀 영역에 바인딩
     │  (수식 계산 후 직렬화)
[클라이언트 JSON 모델] → 브라우저에서 iGrid 컨트롤로 렌더링
```

**보고서 폴더 구조**:
```
보고서명/
├── 보고서명.mtsd              # UI 정의
├── 보고서명.script.ts         # 클라이언트 스크립트
├── MX_GRID/
│   ├── {코드}.xlsx            # 원본 엑셀 (디자이너용)
│   ├── {코드}.json2           # 엑셀 → JSON 변환 템플릿
│   └── {코드}.ds              # 데이터셋 바인딩 정의
├── DataSource/
│   └── *.sql                  # SQL 쿼리
└── ServerScript/
    └── *.ts                   # 서버 스크립트
```

**3파일 셋트**:
- `.xlsx` — 원본 엑셀 파일 (i-AUD Designer 또는 Excel에서 편집)
- `.json2` — 엑셀 구조의 JSON 변환 (서버가 자동 생성, AI 부분 수정 가능)
- `.ds` — 데이터 바인딩 정의 (SQL 결과를 어느 셀 영역에 출력할지 지정)

**AI가 할 수 있는 작업**:
- 서버 스크립트(WorkBook API), 클라이언트 스크립트(iGrid API), SQL, .ds 수정
- .json2 부분 수정(셀 값, 스타일, 조건부서식)

**AI가 할 수 없는 작업**:
- .json2 전체 신규 생성, .xlsx 파일 생성/편집

---

## 2. 서버 스크립트 API — WorkBook

서버 스크립트에서 MX-GRID를 조작하는 핵심 API입니다.

### 2.1 WorkBook 획득 방법

```typescript
// 방법 1: 현재 실행 중인 MX-GRID의 WorkBook (OnExecute 이벤트에서 사용)
var wb = Matrix.getWorkBook();

// 방법 2: 특정 MX-GRID 템플릿을 열기 (내보내기, 별도 처리용)
var wb = Matrix.OpenWorkBook(req.getReportCode(), "MX_GRID_CODE");

// 방법 3: 수식 포함하여 열기
var wb = Matrix.OpenWorkBook(req.getReportCode(), "MX_GRID_CODE", true);

// 방법 4: .json2 파일 경로로 직접 열기
var path = fso.PathCombine(["iGRID_DESIGN", req.getReportCode(), "MX_GRID_CODE"]) + ".json2";
var wb = Matrix.CreateWorkBookByJson(path);
```

### 2.2 ScriptWorkBook 주요 메서드

```typescript
// 시트 접근
var ws = wb.getWorkSheet("V1");           // 이름으로 시트 접근
var ws = wb.getWorkSheet(0);              // 인덱스로 시트 접근
var activeSheet = wb.getActiveSheet();     // 활성 시트
var count = wb.WorkSheetCount();           // 시트 수

// 시트 생성/삭제
var newSheet = wb.CreateWorkSheet("시트명");
wb.AddWorkSheet(ws, "시트명");             // 다른 워크북의 시트를 추가
wb.RemoveWorkSheet("시트명");              // 시트 삭제
wb.MergeSheets();                          // 모든 시트를 첫 번째 시트에 통합

// 데이터 실행 및 수식
wb.ExecuteDataSet();                       // .ds에 정의된 데이터셋 실행
wb.ClearDataSet();                         // 바인딩된 데이터 삭제
wb.Calculate();                            // 수식 계산
wb.Calculate(true);                        // 수식 계산 후 수식 삭제 (값만 유지)
wb.Calculate(true, ["V1", "V2"]);          // 특정 시트만 수식 계산
wb.DisableFormula(false);                  // 수식 활성화 (재계산 전 필요)
wb.UpdateFormulaReference();               // 수식 참조 관계 업데이트

// 이름 정의 (Named Range)
var names = wb.getNameList();              // 이름 정의 목록
var name = wb.getName("_D_DATA");          // 이름 정의 객체
var range = wb.getNameRange("V1!A1");      // 이름 또는 셀주소로 범위 반환
var text = wb.getNameRangeText("V1!A1");   // 셀의 텍스트 반환
var value = wb.getNameRangeValue("_D_DATA"); // 이름 정의 셀의 값
wb.setNameRangeValue("_D_DATA", "새값");   // 이름 정의 셀의 값 변경
wb.addName("이름", "시트명", "A1:B10");     // 이름 정의 추가
wb.removeName("이름");                     // 이름 정의 삭제

// 데이터 바인딩 정보
var bindInfo = wb.getDataBindingRange("데이터셋명"); // 바인딩 영역 정보
var ds = wb.getDataSet();                  // 데이터셋 객체

// 파일 저장
wb.Save("경로.xlsx");                      // 엑셀 저장
wb.Save("경로.xlsx", "V1,V2");             // 특정 시트만 저장
wb.Save("경로.xlsx", ["V1", "V2"]);        // 배열로도 가능
wb.SaveAsPDF("경로.pdf", "V1");            // PDF 저장
wb.SaveAsPDF("경로.pdf", ["V1", "V2"]);    // 여러 시트 PDF
wb.SaveAsMSWord("경로.docx", "V1");        // MS Word 저장
wb.SaveAsHML("경로.hwpx", "V1");           // 한글(HWPX) 저장
wb.SaveRangeToCSV("경로.csv", "V1!B2");    // 특정 영역을 CSV로 저장
wb.WriteTemplate("경로.json2");            // MX-GRID 템플릿으로 저장

// 스타일
var style = wb.CreateCellStyle(
  "font-family:Tahoma;font-size:10;font-weight:bold;font-color:#000000;",  // 폰트
  "border-left:solid,#000000;border-top:solid,#000000;",                   // 테두리
  "#FFFFFF",    // 배경색
  "#,##0.00",   // 포맷
  enHorizontal.Center,   // 가로정렬
  enVertical.Center      // 세로정렬
);

// 데이터 Reader (대용량 읽기)
var reader = wb.getWorkSheetDataReader("V1!B2");
var table = reader.ReadSchema();
while(reader.hasNext()){
  var row = reader.next();
}
```

**API 타입 정의**: `types/com/matrix/script/excel/ScriptWorkBook.ts`

---

## 3. 서버 스크립트 API — WorkSheet

### 3.1 ScriptWorkSheet 주요 메서드

```typescript
var ws = wb.getWorkSheet("V1");

// 셀 접근
var cell = ws.getRange("B5");              // 셀 주소로 접근
var cell = ws.getRange(5, 2);              // 행/열 번호로 접근 (1부터 시작)
var exists = ws.hasRange(5, 2);            // 셀 존재 여부 확인
var usedArea = ws.getUsedRange();          // 사용 중인 전체 영역

// 셀 값 쓰기
ws.setCellText("B5", "텍스트");            // 텍스트 작성
ws.setCellText(5, 2, "텍스트");            // 행/열 번호로 작성
ws.setCellValue("B5", 12345);             // 수치값 작성
ws.setCellValue(5, 2, 12345);
ws.setCellFormula("C5", "=B5*1.1");        // 수식 작성
ws.setCellFormula(5, 3, "=B5*1.1");

// 셀 스타일
ws.setCellStyle("B5", style);              // 스타일 객체 적용
ws.setCellStyle(5, 2, style);
ws.setCellStyle(5, 2,
  "font-family:Tahoma;font-size:10;",     // 폰트
  "border-left:solid,#000000;",            // 테두리
  "#FFFFFF",                               // 배경색
  "#,##0",                                 // 포맷
  enHorizontal.Center,                     // 가로정렬
  enVertical.Center                        // 세로정렬
);
ws.setRangeStyle("B5:G10", style);         // 범위에 스타일 적용

// 행/열 크기 조절
ws.setRowHeight(5, 30);                    // 행 높이 (0 = 숨기기)
ws.setRowHeightByPixel(5, 40);             // 행 높이 (pixel)
ws.setAutoRowHeight(5);                    // 행 높이 자동 맞춤
ws.setColumnWidth(2, 100);                 // 열 너비 (0 = 숨기기)
ws.setColumnWidthByPixel(2, 120);          // 열 너비 (pixel)
ws.setColumnWidthUnit(2, "%");             // 열 너비 단위 (% 또는 빈값)

// 행/열 삽입/삭제
ws.InsertRows(5, 3);                       // 5번 위치에 3행 삽입
ws.InsertColumns(2, 2);                    // 2번 위치에 2열 삽입
ws.DeleteRow(5);                           // 5번 행 삭제
ws.DeleteRows(5, 10);                      // 5~10번 행 삭제
ws.DeleteColumn(2);                        // 2번 열 삭제
ws.DeleteColumns(2, 5);                    // 2~5번 열 삭제
ws.DeleteHiddenRows();                     // 숨겨진 행 삭제
ws.DeleteHiddenColumns();                  // 숨겨진 열 삭제

// 셀 병합
ws.MergeCell(5, 2, 7, 4);                  // 행/열 번호로 병합
ws.MergeCell("B5", "D7");                  // 주소로 병합
ws.MergeCell("B5:D7");                     // 범위로 병합

// 영역 복사/붙이기
var copied = ws.Copy("B5", "G10");         // 영역 복사
var copied = ws.Copy("B5:G10");            // 범위 복사
var copied = ws.Copy(5, 2, 10, 7);         // 행/열 번호로 복사
copied.Paste(ws, 15, 2);                   // 대상 시트의 위치에 붙이기

// DataTable → 시트에 삽입
var area = ws.CopyFromDataTable(table, "B5", true);   // 헤더 포함
var area = ws.CopyFromDataTable(table, "B5", true, "COL1,COL2,COL3");  // 특정 컬럼만
ws.CopyFromJsonTable(jsonText, "B5");      // JSON 데이터 삽입

// 데이터 바인딩 (템플릿 기반)
var binder = ws.getDataTableBinder("B10", false, -1);
// 인자: 시작셀, 헤더표시여부, 스타일복사대상Row(-1이면 미사용)

// 차트/이미지 생성
var chart = ws.CreateChart(enChartType.Column, "B15", "G25");
var chart = ws.CreateChartByJson(jsonText, "B15", "G25");
var img = ws.CreateImage("이미지경로", "B15", "G25");
var img = ws.CreateImageByBase64(base64, "B15", "G25");

// 시트 설정
ws.setName("새시트명");                     // 시트명 변경
ws.IsActive(true);                         // 시트 활성화
ws.IsVisible(false);                       // 시트 숨기기
ws.setFreezePanes(3, 2);                   // 틀 고정
ws.setDisplayGridlines(false);             // 눈금선 숨기기
ws.setDefaultRowHeight(20);                // 기본 행 높이
ws.DisableFormula(true);                   // 수식 비활성화
ws.setColumnHeaderRange("A1:G1");          // 헤더 영역 설정
ws.UpdateProtection(true, true);           // 보호 옵션
var viewRange = ws.getViewRange();         // MX-GRID 표시 영역
```

**API 타입 정의**: `types/com/matrix/script/excel/ScriptWorkSheet.ts`

---

## 4. 서버 스크립트 예제

### 4.1 데이터 바인딩 (템플릿 시트 활용)

```typescript
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
let Matrix: Matrix;

var req = Matrix.getRequest();
var res = Matrix.getResponse();

try {
  var wb = Matrix.getWorkBook();
  var v1 = wb.getWorkSheet("V1");   // 뷰 시트
  var t1 = wb.getWorkSheet("T1");   // 템플릿 시트

  // 템플릿 영역 복사
  var dataTemplate = t1.Copy("B12", "I13");         // 데이터 필드 정의
  var styleTemplate = t1.Copy("B4", "I5");          // 스타일 템플릿
  var altStyleTemplate = t1.Copy("B8", "I9");       // 반복행 스타일
  var firstRowTemplate = t1.Copy("B16", "I17");     // 첫 행 스타일

  // 데이터 바인더 생성
  var binder = v1.getDataTableBinder("B10", false, -1);
  binder.setDataBindingTemplate(dataTemplate);
  binder.setFirstRowStyleTemplate(firstRowTemplate);
  binder.setStyleTemplate(styleTemplate);
  binder.setAlternateStyleTemplate(altStyleTemplate);

  // 데이터소스 실행 (바인더에 자동 바인딩)
  req.ExecuteReportDataSource("데이터", binder);

  // 합계행 복사하여 데이터 아래에 붙이기
  var total = t1.Copy("B21:I22");
  total.Paste(v1, binder.getBindedArea().getBottom() + 1,
                  binder.getBindedArea().getLeft());

} catch(e) {
  Matrix.ThrowException("Error: " + e.message);
}
```

### 4.2 셀 값에 따른 행/열 숨기기

```typescript
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
let Matrix: Matrix;

try {
  var wb = Matrix.getWorkBook();
  var ws = wb.getWorkSheet("V1");

  wb.Calculate();  // 수식 계산 먼저 수행

  // 열 숨기기: 첫 행의 값이 "HIDDEN"인 열
  var idx = 1;
  while (true) {
    var rng = ws.getRange(1, idx);
    if (rng == null || rng.getText() == "") break;
    if (rng.getText() == "HIDDEN") {
      ws.setColumnWidth(idx, 0);
    }
    idx++;
  }

  // 행 숨기기: 첫 열의 값이 "HIDDEN"인 행
  idx = 1;
  while (true) {
    var rng = ws.getRange(idx, 1);
    if (rng == null || rng.getText() == "") break;
    if (rng.getText() == "HIDDEN") {
      ws.setRowHeight(idx, 0);
    }
    idx++;
  }

  // 필요 시 숨겨진 행/열을 완전히 삭제
  // ws.DeleteHiddenRows();
  // ws.DeleteHiddenColumns();

} catch(e) {
  Matrix.ThrowException("Error: " + e.message);
}
```

### 4.3 PDF 내보내기 (파라미터별 반복 생성 + 병합)

```typescript
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
let Matrix: Matrix;

var req = Matrix.getRequest();
var res = Matrix.getResponse();
var util = Matrix.getUtility();
var fso = Matrix.getFileSystemObject();

try {
  var params = req.getParam("VS_CODE").split(",");
  var wb = Matrix.OpenWorkBook(req.getReportCode(), "MX_GRID_CODE");
  var PDF_FILES: string[] = [];

  for (var i = 0; i < params.length; i++) {
    req.setParam("VS_CODE", params[i]);   // 조회 조건 변경
    wb.ClearDataSet();                     // 이전 데이터 삭제
    wb.ExecuteDataSet();                   // 데이터 재실행
    wb.DisableFormula(false);              // 수식 활성화
    wb.Calculate();                        // 수식 계산

    var pdfPath = fso.getTemplatePath(util.getUniqueKey("PDF") + ".pdf");
    wb.SaveAsPDF(pdfPath, "V1");
    PDF_FILES.push(pdfPath);
  }

  // PDF 병합
  var mergedPath = util.getUniqueKey("PDF") + ".pdf";
  var PDFDocument = util.CreatePDFDocument();
  PDFDocument.MergeFiles(PDF_FILES, fso.getTemplatePath(mergedPath));

  res.WriteResponseText(JSON.stringify({ "FILE_NAME": mergedPath }));

} catch(e) {
  Matrix.ThrowException("Error: " + e.message);
}
```

### 4.4 여러 조건의 엑셀을 하나의 파일에 합치기

```typescript
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
let Matrix: Matrix;

var req = Matrix.getRequest();
var res = Matrix.getResponse();
var util = Matrix.getUtility();
var fso = Matrix.getFileSystemObject();

try {
  var FILE_PATH = util.getUniqueKey("XLS") + ".xlsx";

  // 기본 워크북 열기 (빈 껍데기용)
  var wb = Matrix.OpenWorkBook(req.getReportCode(), "EXPORT");
  wb.RemoveWorkSheet("V1");  // 불필요 시트 제거
  wb.RemoveWorkSheet("P1");

  // 데이터소스에서 조건 목록 조회
  var table = req.ExecuteReportDataSource("Data1");
  for (var r = 0; r < table.getRowCount(); r++) {
    var product = table.getRow(r).getString("D1");
    req.setParam("VS_PRODUCT", product);

    // 조건별로 워크북 생성 후 시트를 합치기
    var wb2 = Matrix.OpenWorkBook(req.getReportCode(), "EXPORT");
    wb.AddWorkSheet(wb2.getWorkSheet("V1"), product);
  }

  wb.Save(fso.PathCombine("_TEMP_", FILE_PATH), null);

  var json = res.getJsonResponseWriter();
  json.beginObject()
      .addProperty("FILE_NAME", FILE_PATH)
      .endObject();

} catch(e) {
  Matrix.ThrowException("Error: " + e.message);
}
```

---

## 5. 클라이언트 스크립트 API — iGrid

### 5.1 iGrid 컨트롤 접근

```typescript
// iGrid 컨트롤 획득
let MXGrid = Matrix.getObject("MXGrid컨트롤명") as iGrid;
```

### 5.2 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `ActiveSheet` | string | 활성화된 시트 이름 |
| `WorkBook` | IWorkBook | 클라이언트 WorkBook 모델 |
| `TemplateCode` | string | 원본 엑셀 템플릿 코드 |
| `UseMultiSheet` | boolean | 다중 시트 사용 여부 |
| `EnableZoom` | boolean | 확대/축소 기능 |
| `EnableSheetProtection` | boolean | 시트 보호 적용 여부 |
| `IgnoreExportHiddenCells` | boolean | 내보내기 시 숨김셀 제거 |
| `ScrollLeft` / `ScrollTop` | number | 스크롤 위치 |
| `BeforeScript` | string | 서버 쿼리 실행 전 스크립트 |
| `AfterScript` | string | 서버 쿼리 실행 후 스크립트 |
| `MenuOption` | MenuOption | 메뉴 옵션 |

### 5.3 주요 메서드

```typescript
// 데이터 조작
MXGrid.Refresh();                          // 데이터 새로고침 (서버 요청)
MXGrid.Calculate();                        // 수식 재계산
MXGrid.Calculate(true);                    // 서버에 계산 요청

// 시트 조작
MXGrid.ChangeSheet("V2");                 // 시트 전환
var sheets = MXGrid.getWorkSheetNames();   // 전체 시트 목록

// 셀 접근
var cell = MXGrid.getCell(5, 2);           // 행/열 번호로 셀 접근
var cell = MXGrid.getRange("B5");          // 주소로 셀 접근

// 행/열 표시
MXGrid.ShowHideRows([3, 4, 5], false);     // 행 숨기기
MXGrid.ShowHideColumns([1, 2], true);      // 열 표시

// 확장/축소 (AUD_EXPAND_ROW/COLUMN 사용 시)
MXGrid.ExpandAll();                        // 모두 펼치기
MXGrid.CollapsedAll();                     // 모두 접기

// 내보내기
MXGrid.ExportServiceCall("Excel", function(p) {
  // p.FolderName, p.FileName
  Matrix.DownloadFile(p.FolderName, p.FileName, p.FileName, true);
});

// 편집 모드
MXGrid.setEditable(true);                 // 편집 활성화
MXGrid.IsModified();                       // 수정 여부 확인
MXGrid.Validate();                         // 유효성 검사

// DataTable 접근 (_D_ 이름 정의 영역)
var dt = MXGrid.getDataTable("DATA");      // _D_DATA 이름 정의의 DataTable

// 스크롤
MXGrid.ScrollTo(10, 5);                    // 특정 셀로 스크롤
MXGrid.ScrollMove(0, 100, 300);            // 특정 위치로 스크롤

// WorkBook/유틸리티
var wb = MXGrid.getWorkBook();             // 클라이언트 WorkBook 모델
var sel = MXGrid.getSelection();           // 선택기 객체
var xlsUtil = MXGrid.getUtility();         // MX-Grid 유틸리티

// 내보내기 방식
MXGrid.setExcelExportType("AllSheets");    // Default, AllSheets, AllSheetsWithoutAUDFunction

// 화면 갱신
MXGrid.Update();                           // 다시 그리기
```

### 5.4 이벤트

| 이벤트 | 설명 | 주요 인자 |
|--------|------|----------|
| `OnClick` | 컨트롤 클릭 | `Id` |
| `OnCellClick` | 셀 클릭 | `Cell`, `X`, `Y` |
| `OnCellDoubleClick` | 셀 더블클릭 | `Cell`, `X`, `Y` |
| `OnCellBeginEdit` | 편집 시작 | `Cell`, `Cancel`, `MergeColumn`, `LOVList` |
| `OnCellEndEdit` | 편집 완료 | `getCells()`, `Cancel` |
| `OnSelectionChange` | 셀 선택 변경 | `Cells` |
| `OnDataBindEnd` | 데이터 바인딩 완료 | `RecordCount` |
| `OnActivateSheetChanged` | 시트 변경 | `Sheet` |
| `OnSheetChanged` | 시트 전환 완료 | `SheetName` |
| `OnCalculateStart` | CRUD 서버 요청 시작 | `Cancel` |
| `OnCalculateEnd` | CRUD 서버 결과 처리 완료 | `Id` |
| `OnExecuteStart` | 서버 데이터 요청 전 | `Cancel` |
| `OnContextMenuOpening` | 컨텍스트 메뉴 열림 | `Cell`, `Menu`, `Cancel` |
| `OnCellValidatorMessage` | 유효성 메시지 표시 | `Cell`, `Validator`, `Title`, `Message`, `Cancel` |
| `OnScroll` | 스크롤 변경 | `ScrollLeft`, `ScrollTop` |
| `OnMessage` | 메시지 출력 | `Code`, `Message`, `Type`, `Handled` |

**이벤트 사용 예시**:
```typescript
MXGrid.OnCellClick = function(sender, args) {
  let cell = args.Cell;
  Matrix.Alert("클릭한 셀: " + cell.getText());
};

MXGrid.OnCellBeginEdit = function(sender, args) {
  // 특정 열만 편집 허용
  if (args.Cell.Column < 3) {
    args.Cancel = true;  // 편집 취소
  }
  // 콤보박스 목록 설정
  args.LOVList = ["옵션1", "옵션2", "옵션3"];
};

MXGrid.OnCellEndEdit = function(sender, args) {
  var cells = args.getCells();
  // 수정된 셀 처리
  args.Cancel = true;  // 서버 계산 요청 취소
};
```

**API 타입 정의**: `types/aud/control/iGrid.ts`

---

## 6. 예약어 (이름 정의) 레퍼런스

엑셀의 **이름 정의(Named Range)** 에 특정 예약어를 설정하면 MX-GRID가 자동으로 인식합니다.

### 6.1 화면 표시 영역

| 예약어 | 설명 |
|--------|------|
| `_VIEW_RANGE_xx` | MX-GRID로 표시할 영역을 지정. `xx`는 순번. 예: `_VIEW_RANGE_01` = `A1:Z100` |
| `_AUTO_SIZE_xx` | 자동 크기 조절 영역. 지정된 영역이 화면에 맞도록 자동 확대/축소 |
| `_RESIZE_AREA_xx` | 마우스로 크기 조절 가능한 영역 |

### 6.2 컨트롤 및 데이터 배치

| 예약어 | 설명 |
|--------|------|
| `_C_xx` | 셀에 i-AUD 컨트롤(TextBox, ComboBox 등)을 배치. `xx`는 컨트롤명. 예: `_C_TextBox1` = `C5` |
| `_D_xx` | 데이터셋 영역을 정의. `xx`는 데이터 이름. 예: `_D_DATA` = `A10:G100`. 클라이언트에서 `getDataTable("DATA")`로 접근 가능 |
| `_DS_xx` | i-AUD DataSource의 결과를 자동으로 출력. `xx`는 데이터소스명. 예: `_DS_조회` = `B5:H5` (헤더 시작 셀) |

### 6.3 CRUD 관련

| 예약어 | 설명 |
|--------|------|
| `_PROTECT_` | CRUD가 적용되는 시트를 지정. 해당 시트에서 편집 가능. 예: `_PROTECT_` = `V1!A1` |
| `CRUD_xx` | CRUD 데이터 테이블의 시작 위치를 지정. `xx`는 테이블명. 예: `CRUD_TABLE1` = `B5` |

### 6.4 내보내기 관련

| 예약어 | 설명 |
|--------|------|
| `_EXPORT_SHEETS_` | 내보내기 대상 시트 목록. 쉼표로 구분. 예: `_EXPORT_SHEETS_` = `V1,V2` |
| `_IGNORE_SHEET_` | 템플릿으로 전환에서 제외할 시트 |

---

## 7. 전용 함수 (AUD_xxx) 레퍼런스

엑셀 셀에 `AUD_xxx(...)` 형태의 수식을 입력하면 MX-GRID가 특수 기능을 수행합니다.
이 함수들은 **엑셀 셀의 수식**으로 작성합니다.

### 7.1 행/열 숨기기

```
=AUD_HIDE_ROWS(조건, [범위])
=AUD_HIDE_COLUMNS(조건, [범위])
```
- `조건`: 셀 참조 또는 수식. 결과가 0이거나 빈값이면 해당 행/열 숨김
- `범위`: 생략 시 현재 행/열. 지정 시 해당 범위의 행/열 숨김

### 7.2 이미지

```
=AUD_IMAGE(이미지명)
```
- 셀에 이미지를 표시. 서버의 이미지 파일명 또는 URL

### 7.3 셀 속성 추가

```
=AUD_PROPERTY(텍스트, 속성명1, 속성값1, [속성명2, 속성값2, ...])
```
- 셀에 사용자 정의 속성을 추가. 클라이언트 스크립트에서 접근 가능

### 7.4 템플릿 바인딩

```
=AUD_TEMPLATE_BINDING(수식범위, 스타일범위, [반복스타일])
```
- 데이터 행 수에 맞게 동적으로 행을 확장하며 바인딩
- `수식범위`: 데이터 필드가 정의된 셀 범위
- `스타일범위`: 적용할 스타일이 정의된 셀 범위
- `반복스타일`: 짝수/홀수 행에 교대로 적용할 스타일 범위

### 7.5 셀 내 컨트롤

```
=AUD_CHECK_BOX(텍스트, 값, [링크셀], [상태])
```
- 셀에 체크박스를 생성
- `텍스트`: 표시 텍스트, `값`: 체크 시 값, `링크셀`: 값 연동 셀, `상태`: 초기 체크 여부

```
=AUD_RADIO_BUTTON(텍스트, 값, [링크셀])
```
- 셀에 라디오 버튼을 생성

### 7.6 셀 잠금

```
=AUD_PROTECT(범위1, [범위2], ...)
```
- 지정한 범위를 잠금 처리 (CRUD 시 편집 불가)

### 7.7 펼침/접기

```
=AUD_EXPAND_ROW(확장여부, 범위1, [범위2], ...)
=AUD_EXPAND_COLUMN(확장여부, 범위1, [범위2], ...)
```
- 행 또는 열의 펼침/접기 기능
- `확장여부`: true=펼침, false=접기 (초기 상태)
- 클라이언트에서 `ExpandAll()` / `CollapsedAll()` 로 제어

### 7.8 수정 여부 확인

```
=AUD_ISMODIFIED(범위1, [범위2], ...)
```
- 지정된 범위의 데이터가 수정되었는지 확인

---

## 8. .ds 파일 구조

`.ds` 파일은 MX-GRID에 바인딩할 데이터소스를 정의하는 JSON 파일입니다.

```json
{
  "DataSources": {
    "Datas": [
      {
        "Id": "데이터소스코드",
        "Name": "데이터소스명",
        "OutputAddress": "'V1'!$C$9:$K$9",
        "WriterColumnHeader": true,
        "ConnectionCode": "AUD_SAMPLE_DB", 
         "SQL": "select * from table",
         "MetaLayout":"",
               
      }
    ]
  }
}
```

| 필드 | 설명 |
|------|------|
| `Id` | 데이터 소스의 고유 ID |
| `Name` | 데이터소스 표시명 |
| `OutputAddress` | 데이터가 출력되어 있는 영역의 주소 |
| `WriterColumnHeader` | 컬럼 헤더 출력 여부 |
| `ConnectionCode` | 데이터베이스 연결코드 |
| `SQL` | 데이터베이스 연결코드 |
| `MetaLayout` | i-META를 사용하는 경우 META 배치 정보 |

**수정 시 주의사항**: 
- `MetaLayout`의 값이 있는 경우 수정 하면 안된다.

---

## 9. .json2 부분 수정 가이드

`.json2`는 대용량 구조이므로 전체 생성은 불가하지만, 특정 부분은 수정 가능합니다.

**수정 가능 영역**:

| 영역 | 키 | 설명 |
|------|-----|------|
| 셀 값 | `WorkSheets[].Ranges[].Value` | 특정 셀의 텍스트/수식 변경 |
| 스타일 | `WorkSheets[].Styles[]` | 색상, 폰트, 테두리 등 변경 |
| 행/열 크기 | `WorkSheets[].Rows[].Height`, `Columns[].Width` | 크기 변경 |
| 조건부서식 | `WorkSheets[].FormatConditions[]` | 조건부 서식 규칙 |
| 이름 정의 | `Names[]` | 예약어(이름 정의) 추가/수정 |

**수정 방법**:
1. .json2 파일을 읽고 특정 키를 검색
2. `Ranges` 배열에서 `Row`/`Col` 로 대상 셀을 찾음
3. `Value` 또는 `Formula` 필드를 수정

---

 
---

## 11. API 인터페이스 위치

상세 API 정의는 다음 파일을 참조하세요:

- **서버 WorkBook**: `types/com/matrix/script/excel/ScriptWorkBook.ts`
- **서버 WorkSheet**: `types/com/matrix/script/excel/ScriptWorkSheet.ts`
- **서버 CellRange**: `types/com/matrix/script/excel/ScriptCellRange.ts`
- **서버 CellStyle**: `types/com/matrix/script/excel/ScriptCellStyle.ts`
- **서버 TableBinder**: `types/com/matrix/script/data/ScriptWorkSheetTableBinder.ts`
- **서버 Chart**: `types/com/matrix/script/excel/ScriptChart.ts`
- **서버 Image**: `types/com/matrix/script/excel/ScriptImage.ts`
- **클라이언트 iGrid**: `types/aud/control/iGrid.ts`
- **클라이언트 IWorkBook**: `types/aud/control/igrids/IWorkBook.ts`
- **클라이언트 IWorkSheet**: `types/aud/control/igrids/IWorkSheet.ts`
- **클라이언트 Cell**: `types/aud/control/igrids/Cell.ts`
