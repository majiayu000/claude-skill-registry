---
name: iaud-server-script
description: i-AUD 서버 스크립트 개발 가이드. Rhino 엔진에서 실행되는 TypeScript 서버 스크립트 작성법을 안내합니다. "서버 스크립트", "데이터베이스 조회", "SQL 실행", "파일 처리", "FTP", "서비스 개발" 등을 물어볼 때 사용하세요.
---

# i-AUD 서버 스크립트 개발 가이드

## 1. 개요

서버 스크립트는 Rhino JavaScript 엔진에서 실행되며, 데이터베이스 조회, 파일 처리, 외부 API 호출 등 백엔드 로직을 담당합니다.

**파일 위치**: `[보고서폴더]/ServerScript/*.ts`

**특징**:
- 각 파일이 하나의 서비스로 동작
- `@`로 시작하는 파일은 공통 모듈로 사용 가능 (예: `@DATA_MASTER.ts`)

---

## 2. 기본 구조

```typescript
// 필수 import 구문
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
import { ScriptRecordSet } from "@AUD_SERVER/matrix/script/ScriptRecordSet";
import { ScriptPreparedStatement } from "@AUD_SERVER/matrix/script/ScriptPreparedStatement";
import { ScriptDataRow } from "@AUD_SERVER/matrix/script/ScriptDataRow";
import { ScriptTextFileWriter } from "@AUD_SERVER/matrix/script/io/ScriptTextFileWriter";
import { ScriptRequestPacket } from "@AUD_SERVER/matrix/script/ScriptRequestPacket";
import { ScriptResponsePacket } from "@AUD_SERVER/matrix/script/ScriptResponsePacket";
import { ScriptUtility } from "@AUD_SERVER/matrix/script/ScriptUtility";
import { ScriptFileSystemObject } from "@AUD_SERVER/matrix/script/ScriptFileSystemObject";
import { ScriptConnection } from "@AUD_SERVER/matrix/script/ScriptConnection";
import { ScriptSession } from "@AUD_SERVER/matrix/script/ScriptSession";
import { ScriptQueryGenerator } from "@AUD_SERVER/matrix/script/ScriptQueryGenerator";

// 필수 변수 선언 (삭제/수정 금지)
let Matrix: Matrix;

// 핵심 객체 초기화
const req = Matrix.getRequest();      // 클라이언트 요청
const res = Matrix.getResponse();     // 클라이언트 응답
const session = Matrix.getSession();  // 세션 정보
const util = Matrix.getUtility();     // 유틸리티
const fso = Matrix.getFileSystemObject();  // 파일 시스템
let con = Matrix.getConnection();     // DB 연결

// 비즈니스 로직
try {
    // 구현 내용
} catch(e) {
    Matrix.ThrowException(e.message);
} finally {
    // 리소스 정리
    if (con != null) {
        con.DisConnect();
        con = null;
    }
}
```

---

## 3. 핵심 API

### 3.1 ScriptRequestPacket (req) - 클라이언트 요청

```typescript
const req = Matrix.getRequest();

// 파라미터 읽기
let keyword = req.getParam("VS_KEYWORD");
let userId = req.getUserCode();
let reportCode = req.getReportCode();

// 파라미터 설정
req.setParam("NEW_PARAM", "value");

// 테이블 데이터 읽기 (클라이언트에서 전송한 그리드 데이터)
let table = req.getTable("GridName");
let tableCount = req.getTableCount();

// 데이터셋
let dataSet = req.getDataSet();

// 보고서 데이터소스 실행
let resultTable = req.ExecuteReportDataSource("DataSourceName");

// 권한 확인
let hasRole = req.HasRole("ADMIN");
```

### 3.2 ScriptResponsePacket (res) - 클라이언트 응답

```typescript
const res = Matrix.getResponse();

// 테이블 추가 (클라이언트로 데이터 전송)
res.getDataSet().AddTable(table, "ResultTable");

// 쿼리 결과 테이블 생성
let resultTable = res.CreateTable("T1", "DBMS_CODE", "SELECT * FROM TABLE");

// 비동기 쿼리 실행 (대용량 데이터)
res.addAsyncTable("T1", "DBMS_CODE", sql1);
res.addAsyncTable("T2", "DBMS_CODE", sql2);
res.ExecuteAsyncTables();

// PreparedStatement 결과 직접 전달 (메모리 절약)
let stmt = con.PreparedStatement(sql);
res.addTable("TABLE_NAME", stmt);  // stmt는 닫지 말 것!

// 텍스트/JSON 응답
res.WriteResponseText("Success");
let jsonWriter = res.getJsonResponseWriter();
```

### 3.3 ScriptConnection (con) - 데이터베이스 연결

```typescript
let con = Matrix.getConnection();

// 연결
con.Connect("DBMS_CODE");

// 트랜잭션
con.BeginTransaction();
con.CommitTransaction();
con.RollBackTransaction();

// 쿼리 실행
let table = con.ExecuteDataTable("SELECT * FROM TABLE");
let count = con.ExecuteScalar("SELECT COUNT(*) FROM TABLE");
let affected = con.ExecuteUpdate("UPDATE TABLE SET COL = 'value'");

// RecordSet 순회
let rs = con.ExecuteRecordSet("SELECT * FROM TABLE");
while (rs.next()) {
    let value = rs.getString("COLUMN_NAME");
    let num = rs.getInt("NUM_COLUMN");
}

// PreparedStatement (파라미터 바인딩)
let stmt = con.PreparedStatement("SELECT * FROM TABLE WHERE ID = ?");
stmt.setString(1, "value");
let result = stmt.ExecuteQuery();
stmt.Close();

// 연결 해제
con.DisConnect();
```

### 3.4 ScriptRecordSet (rs) - 결과셋 순회

```typescript
let rs = con.ExecuteRecordSet("SELECT * FROM TABLE");

while (rs.next()) {
    let strValue = rs.getString("COL1");      // 문자열
    let intValue = rs.getInt("COL2");         // 정수
    let dblValue = rs.getDouble("COL3");      // 실수
    let anyValue = rs.getData("COL4");        // any 타입

    // 인덱스로도 접근 가능
    let val = rs.getString(0);
}
```

---

## 4. 파일 시스템 API

```typescript
const fso = Matrix.getFileSystemObject();

// 파일 존재 확인
let exists = fso.Exists("/path/to/file.txt");

// 파일 읽기
let content = fso.ReadTextFile("/path/to/file.txt");

// 파일 쓰기
fso.WriteTextFile("/path/to/file.txt", "content");

// 임시 파일 경로
let tempPath = fso.getTemplatePath("filename.txt");

// 파일 삭제
fso.Delete("/path/to/file.txt");

// 디렉토리 생성
fso.CreateDirectory("/path/to/dir");
```

---

## 5. FTP/SFTP 연결

```typescript
// FTP 연결
let ftp = Matrix.getFTPConnector();
// 또는 SFTP 연결
let sftp = Matrix.getSFTPConnector();

try {
    // 연결
    ftp.Connect("server.com", 21, "username", "password", false);

    // 작업 경로 설정
    ftp.setFolderPath("/remote/path");

    // 파일 목록 조회
    let fileList = ftp.getListFiles();

    // 파일 업로드
    ftp.Upload("/local/path/file.txt", "remote_file.txt");

    // 파일 다운로드
    ftp.Download("remote_file.txt", "/local/path/file.txt");

} finally {
    ftp.DisConnect();
    ftp = null;
}
```

---

## 6. HTTP 요청

```typescript
let web = Matrix.getHttpConnector();

// GET 요청
let result = web.SendRequest("https://api.example.com/data", "GET", "", []);

// POST 요청 (JSON)
let postData = JSON.stringify({ key: "value" });
let headers = [
    "Content-Type:application/json",
    "Accept:application/json"
];
let result = web.SendRequest("https://api.example.com/data", "POST", postData, headers);

// 인증 쿠키 포함
let cookies = req.getCookieString("UTF-8");
headers.push("Cookie:" + cookies);
```

---

## 7. Excel 처리

```typescript
// 새 워크북 생성
let workbook = Matrix.CreateWorkBook();
let sheet = workbook.GetActiveSheet();

// 셀 값 설정
sheet.GetCell(0, 0).Value = "Header";
sheet.GetCell(1, 0).Value = "Data";

// 기존 엑셀 파일 열기
let wb = Matrix.OpenWorkBook("REPORT_CODE", "MX_GRID_CODE");

// 엑셀 → PDF 변환
Matrix.ExcelToPDF("/path/to/excel.xlsx", "/path/to/output.pdf");

// 엑셀 → HTML 변환
Matrix.ExcelToHtmlTable("/path/to/excel.xlsx", "/path/to/output.html", 1000);

// 엑셀 → 이미지 변환
let images = Matrix.ExcelToImage("/path/to/excel.xlsx", "Sheet1", true);
```

---

## 8. 유틸리티

```typescript
const util = Matrix.getUtility();

// 고유 키 생성
let uniqueKey = util.getUniqueKey("PREFIX");

// 문자열 → 정수 변환
let intVal = util.ToInteger("123", 0);

// 날짜 포맷
let formatted = util.FormatDate(new Date(), "yyyyMMdd");

// 로그 기록
Matrix.WriteLog("Log message");
```

---

## 9. 세션

```typescript
const session = Matrix.getSession();

// 세션 값 읽기
let value = session.getAttribute("KEY");

// 세션 값 설정
session.setAttribute("KEY", "value");
```

---

## 10. 공통 모듈 패턴

`@`로 시작하는 파일을 공통 모듈로 만들 수 있습니다.

**파일: ServerScript/@DATA_MASTER.ts**
```typescript
import { Matrix } from "@AUD_SERVER/matrix/script/Matrix";
let Matrix: Matrix;

export class QueryRepository {
    private static Request = Matrix.getRequest();
    private static QueryHelper = Matrix.getQueryGenerator();

    public static CONNECTION_CODE = "MTXRPTY";

    public static getSalesList(keyword: string): string {
        let sqls: Array<string> = [];
        sqls.push("SELECT * FROM SALES");
        sqls.push("WHERE KEYWORD LIKE '%" + keyword + "%'");

        return QueryRepository.QueryHelper.getParameterBindedSQL(
            sqls.join("\n"),
            this.CONNECTION_CODE
        );
    }
}
```

**다른 스크립트에서 사용:**
```typescript
import { QueryRepository } from "../ServerScript/@DATA_MASTER";
//<%@include file="/REPORT_CODE/DATA_MASTER.jsx"%>

let sql = QueryRepository.getSalesList("검색어");
```

---

## 11. 에러 처리 패턴

```typescript
let con = null;
let stmt = null;

try {
    con = Matrix.getConnection();
    con.Connect("DBMS_CODE");

    // 비즈니스 로직

} catch(e) {
    Matrix.ThrowException("Error: " + e.message);
} finally {
    // 리소스 정리 (순서 중요!)
    if (stmt != null) {
        stmt.Close();
        stmt = null;
    }
    if (con != null) {
        con.DisConnect();
        con = null;
    }
}
```

---

## 12. 대용량 데이터 처리

### 콜백 패턴 (메모리 효율적)

```typescript
// 행 단위 처리 (메모리 절약)
con.ExecuteDataTable(sql, function(row) {
    let table = row.getDataTable();
    let value = row.getString("COLUMN");

    // 처리 로직...

    return null;  // null: 다음 행, true: 테이블에 추가, false: 종료
});
```

### 비동기 테이블

```typescript
// 여러 쿼리 병렬 실행
res.addAsyncTable("T1", "DBMS_CODE", sql1);
res.addAsyncTable("T2", "DBMS_CODE", sql2);
res.addAsyncTable("T3", "DBMS_CODE", sql3);
res.ExecuteAsyncTables();  // 병렬 실행
```

---

## 13. API 인터페이스 위치

상세 API 정의는 `types/com/` 폴더를 참조하세요:

- `types/com/matrix/script/` - 핵심 스크립트 API
  - `Matrix.ts` - 메인 Matrix API
  - `ScriptConnection.ts` - DB 연결
  - `ScriptRecordSet.ts` - 결과셋
  - `ScriptRequestPacket.ts` - 요청
  - `ScriptResponsePacket.ts` - 응답
- `types/com/matrix/script/io/` - 파일 I/O
- `types/com/matrix/script/excel/` - Excel 처리
- `types/com/matrix/olap/` - OLAP 관련

---

## 14. 샘플 코드 위치

실제 구현 예제는 다음 폴더를 참조하세요:

- `src/reports/samples/ETC/FTP Client/ServerScript/` - FTP 샘플
- `src/reports/samples/ETC/AUD_Dynamic-SQL/ServerScript/` - 동적 SQL 샘플
- `src/reports/samples/ETC/서버 스크립트로 다중 쿼리 실행/ServerScript/` - 다중 쿼리 샘플
