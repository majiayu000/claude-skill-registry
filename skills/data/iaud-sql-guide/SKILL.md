---
name: iaud-sql-guide
description: i-AUD DataSource SQL 작성 가이드. SQL 파라미터 바인딩, 변수 접두사(VS_/VN_), 특수 지시자(@/%/$), IN절 처리, Dynamic SQL, 프로시저 호출 등을 안내합니다. "SQL 작성", "파라미터 바인딩", "데이터소스 SQL", "Dynamic SQL", "변수 치환" 등을 물어볼 때 사용하세요.
---

# AUD Platform SQL 작성 규칙

## 1. 변수(파라미터) 명명 규칙

SQL 내에서 변수는 **콜론(`:`)** 접두사로 선언하며, 접두사에 따라 타입과 동작이 결정된다.

### 1.1 변수 접두사

| 접두사 | 타입 | 설명 | 바인딩 결과 |
|--------|------|------|-------------|
| `:VS_` | String | 문자열 세션/파라미터 변수 | 값이 `'따옴표'`로 감싸짐 |
| `:VN_` | Numeric | 숫자형 세션/파라미터 변수 | 따옴표 없이 값 그대로 치환 |
| `:` (기타) | String | 일반 문자열 파라미터 | 값이 `'따옴표'`로 감싸짐 |

### 1.2 변수명 허용 문자

변수명에는 다음 문자를 사용할 수 있다:
- 영문자 (A-Z, a-z)
- 숫자 (0-9)
- 밑줄 (`_`)
- 달러 기호 (`$`)
- 점 (`.`)

> 숫자로만 구성된 변수명(예: `:123`)은 시간 구문으로 판단하여 파라미터로 인식하지 않는다.

### 1.3 예시

```sql
-- 문자열 변수: 자동으로 '따옴표' 감싸짐
SELECT * FROM EMP WHERE DEPT_CODE = :VS_DEPT_CODE

-- 숫자형 변수: 따옴표 없이 치환
SELECT * FROM EMP WHERE AMOUNT > :VN_MIN_AMOUNT

-- 일반 파라미터
SELECT * FROM EMP WHERE USER_NAME = :USER_NAME
```

바인딩 결과:
```sql
SELECT * FROM EMP WHERE DEPT_CODE = 'A001'
SELECT * FROM EMP WHERE AMOUNT > 10000
SELECT * FROM EMP WHERE USER_NAME = '홍길동'
```

---

## 2. 특수 지시자

### 2.1 `@` - 빈 값 시 라인 삭제

파라미터 앞에 `@`를 붙이면 값이 비어있을 때 해당 라인 전체가 삭제된다.
조건절을 선택적으로 적용할 때 유용하다.

```sql
SELECT * FROM EMP
WHERE 1=1
  AND DEPT_CODE = @:VS_DEPT_CODE
  AND USER_NAME = @:VS_USER_NAME
```

- `:VS_DEPT_CODE`가 빈 값이면 `AND DEPT_CODE = @:VS_DEPT_CODE` 라인 전체 삭제
- `:VS_USER_NAME`에 값이 있으면 정상 바인딩

### 2.2 `%` - LIKE 검색 와일드카드

파라미터 앞뒤에 `%`를 붙이면 LIKE 패턴에 자동 포함된다.

```sql
-- 앞뒤 모두 LIKE
SELECT * FROM EMP WHERE USER_NAME LIKE %:VS_SEARCH_NAME%

-- 뒤쪽만 LIKE
SELECT * FROM EMP WHERE USER_CODE LIKE :VS_SEARCH_CODE%
```

바인딩 결과:
```sql
SELECT * FROM EMP WHERE USER_NAME LIKE '%홍길동%'
SELECT * FROM EMP WHERE USER_CODE LIKE '홍길동%'
```

### 2.3 `$` - 세션 변수 강제 사용

파라미터명 뒤에 `$`를 붙이면 클라이언트 전달값 대신 서버 세션(인증) 값을 사용한다.
보안이 필요한 항목(사용자 코드, 조직 코드 등)에 사용한다.

```sql
-- 세션의 USER_CODE 값을 사용 (클라이언트 조작 불가)
SELECT * FROM EMP WHERE USER_CODE = :VS_USER_CODE$
```

### 2.4 조합 사용

지시자를 조합할 수 있다:

```sql
-- 빈 값이면 라인 삭제 + LIKE 검색
SELECT * FROM EMP WHERE USER_NAME LIKE %@:VS_SEARCH%
```

### 2.5 `::` (이중 콜론)

`::` 구문은 Oracle의 네임스페이스 연산자이므로 파라미터로 인식하지 않는다.
바인딩 전에 자동으로 제거된다.

---

## 3. IN 절 처리

쉼표로 구분된 값이 `IN(` 절 안에서 사용되면 자동으로 개별 항목에 따옴표를 적용한다.

```sql
SELECT * FROM EMP WHERE DEPT_CODE IN( :VS_DEPT_LIST )
```

`:VS_DEPT_LIST`의 값이 `A001,A002,A003`이면:
```sql
SELECT * FROM EMP WHERE DEPT_CODE IN( 'A001','A002','A003' )
```

> 이미 따옴표가 감싸진 값(`'A001','A002'`)이나 함수 형태의 값은 추가 처리하지 않는다.

---

## 4. NVarchar 지원 (SQL Server)

SQL Server의 NVarchar 타입 사용 시, 문자열 파라미터 앞에 자동으로 `N` 접두사가 추가된다.

```sql
-- 일반 DB
WHERE NAME = '홍길동'

-- NVarchar DB
WHERE NAME = N'홍길동'
```

---

## 5. 함수 지시자 (VS_FUNC / VN_FUNC)

SQL 내에서 날짜 계산 함수를 사용할 수 있다.

### 5.1 DateText 함수

```
:VS_FUNC(DateText(연도증감, 월증감, 일증감, "날짜형식" [, "기준일자"]))
:VN_FUNC(DateText(연도증감, 월증감, 일증감, "날짜형식" [, "기준일자"]))
```

| 파라미터 | 설명 | 특수값 |
|----------|------|--------|
| 연도증감 | 연도 가감 정수 | `First`=1900, `Last`=2999 |
| 월증감 | 월 가감 정수 | `First`=1월, `Last`=12월 |
| 일증감 | 일 가감 정수 | `First`=해당월 첫날, `Last`=해당월 마지막날 |
| 날짜형식 | Java SimpleDateFormat 패턴 | - |
| 기준일자 | (선택) 기준이 되는 날짜 | 미지정 시 오늘 |

### 5.2 예시

```sql
-- 오늘 날짜 (yyyy-MM-dd 형식)
SELECT :VS_FUNC(DateText(0,0,0,"yyyy-MM-dd")) AS TODAY FROM DUAL

-- 이번달 첫날
SELECT :VS_FUNC(DateText(0,0,First,"yyyy-MM-dd")) AS FIRST_DAY FROM DUAL

-- 이번달 마지막날
SELECT :VS_FUNC(DateText(0,0,Last,"yyyy-MM-dd")) AS LAST_DAY FROM DUAL

-- 3개월 전
SELECT :VS_FUNC(DateText(0,-3,0,"yyyy-MM-dd")) AS THREE_MONTH_AGO FROM DUAL

-- 100일 전 (숫자형으로 반환)
SELECT :VN_FUNC(DateText(0,0,-100,"yyyyMMdd")) AS DAYS_AGO FROM DUAL
```

`VS_FUNC`는 결과를 문자열(`'2026-02-02'`)로, `VN_FUNC`는 숫자(`20260202`)로 바인딩한다.

---

## 6. Dynamic SQL (서버 스크립트)

SQL 안에 `<% %>` 태그를 사용하여 JavaScript 기반 동적 SQL을 생성할 수 있다.

### 6.1 기본 구문

| 구문 | 설명 |
|------|------|
| `<% ... %>` | JavaScript 코드 실행 |
| `<%= ... %>` | JavaScript 표현식의 결과를 SQL에 삽입 |

### 6.2 예시

```sql
SELECT *
FROM EMP
WHERE 1=1
<% if(VS_DEPT_CODE) { %>
  AND DEPT_CODE = :VS_DEPT_CODE
<% } %>
<% if(VS_USE_YN) { %>
  AND USE_YN = :VS_USE_YN
<% } %>
<% for(var i=0; i<3; i++) { %>
  UNION ALL SELECT * FROM EMP_<%= i %>
<% } %>
```

### 6.3 JS_SQL 모드

SQL 전체를 JavaScript로 작성하려면 첫 줄에 `///@@JS_SQL`을 선언한다.

```
///@@JS_SQL
RESULT_SQL.push("SELECT * FROM EMP WHERE 1=1");
if(VS_DEPT_CODE) {
    RESULT_SQL.push(" AND DEPT_CODE = '" + VS_DEPT_CODE + "'");
}
```

### 6.4 사용 가능한 변수

Dynamic SQL 내에서 `VS_`, `VN_` 접두사가 붙은 파라미터는 자동으로 JavaScript 변수로 등록된다.

```javascript
// 자동 생성되는 변수
var VS_DEPT_CODE = Matrix.getRequest().getParam("VS_DEPT_CODE");
var VN_AMOUNT = Matrix.getRequest().getParam("VN_AMOUNT");

// 세션 변수 ($ 접미사)
var USER_CODE$ = Matrix.getSession().getAttribute("USER_CODE");
var ORG_CODE$ = Matrix.getSession().getAttribute("ORG_CODE");
```

---

## 7. 주석 처리

### 7.1 SQL 주석

| 주석 형태 | 처리 |
|-----------|------|
| `-- 라인주석` | 바인딩 전 제거됨 |
| `/* 블록주석 */` | 바인딩 전 제거됨 |
| `/*+ 힌트 */` | Oracle Hint - 제거하지 않음 |
| `/*! 힌트 */` | MySQL/MariaDB Hint - 제거하지 않음 |

> 주석 내의 변수(`:PARAM`)는 파라미터로 인식하지 않는다.
> 문자열 리터럴(`'...'`, `"..."`) 내의 `:PARAM`도 파라미터로 인식하지 않는다.

---

## 8. 프로시저 호출

다음 형태의 SQL은 프로시저로 판별된다:

```sql
-- EXEC 방식
EXEC PROC_NAME :PARAM1, :PARAM2

-- CALL 방식
CALL PROC_NAME(:PARAM1, :PARAM2)

-- {CALL} 방식 (JDBC 표준)
{CALL PROC_NAME(:PARAM1, :PARAM2)}

-- BEGIN...END 방식 (Sybase)
BEGIN
  EXEC PROC_NAME :PARAM1
END
```

> `SELECT`, `WITH`로 시작하는 SQL은 일반 쿼리로 판별된다.

---

## 9. 파일 데이터 소스

SQL 대신 파일 경로를 지정하여 데이터를 로드할 수 있다.

| 접두사 | 설명 |
|--------|------|
| `@@CSV` | CSV 파일 데이터 소스 |
| `@@TXT` | 텍스트 파일 데이터 소스 |
| `@@TAB` | 탭 구분 파일 데이터 소스 |
| `@@URL` | URL 데이터 소스 |
| `@@FILE` | 일반 파일 데이터 소스 |

파일 데이터 소스에서도 `:PARAM` 변수 치환은 동작하지만, 따옴표 자동 감싸기 등의 SQL 전용 처리는 적용되지 않는다.

---

## 10. 주의사항

1. **SQL Injection 방지**: 문자열 값의 작은따옴표는 자동으로 이스케이프(`'` → `''`)된다.
2. **역슬래시 쉼표**: 값에 `\,`가 포함되면 쉼표가 아닌 일반 문자로 처리된다(`\,` → `,`).
3. **바인딩 값 검증**: 변수명과 동일한 값(예: `:PARAM`에 `:PARAM`을 바인딩)은 무한루프 방지를 위해 거부된다.
4. **주석 내 값 주입**: 바인딩된 값에 `/*`, `*/`, `--`가 포함되면 바인딩 후 주석 제거를 다시 수행한다.
5. **PreparedStatement**: `getStatementSQLParsing` 메서드 사용 시 `:PARAM`이 `?`로 치환되어 PreparedStatement 바인딩이 가능하다.
