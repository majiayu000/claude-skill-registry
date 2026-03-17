---
name: iaud-formula
description: i-AUD 계산수식(Formula) 작성 가이드. 텍스트박스, 라벨, 데이터그리드 등 컨트롤에 수식을 설정하여 값을 자동 연산하는 방법을 안내합니다. "계산수식", "수식 설정", "SUMIF", "컨트롤 참조", "그리드 수식", "JavaScript 수식" 등을 물어볼 때 사용하세요.
---

# i-AUD Formula (계산수식) 작성 가이드

i-AUD 계산수식(FormulaManager)은 텍스트박스, 라벨, 데이터그리드 등의 컨트롤에 수식을 설정하여 값을 자동 연산하는 시스템이다.
수식 내 다른 컨트롤을 참조하면 해당 컨트롤의 값 변경 시 자동으로 재연산된다.

---

## 수식 기본 문법

### 컨트롤 참조
- **`:컨트롤명`** - 다른 컨트롤의 값을 참조
- **`:전역변수명`** - 전역 파라미터(GlobalParam) 또는 Variable 참조
- **`[필드명]`** - 데이터그리드 내 필드(컬럼) 값 참조 (그리드 수식에서만 사용)

```
// 텍스트박스 txtPrice의 값 참조
:txtPrice

// 전역변수 gYear 참조
:gYear

// 그리드 필드 참조 (그리드 수식 내)
[PRICE] * [QTY]
```

### 연산자
| 연산자 | 설명 | 예시 |
|--------|------|------|
| `+` | 덧셈 / 문자열 연결 | `:txtA + :txtB` |
| `-` | 뺄셈 | `[PRICE] - [DISCOUNT]` |
| `*` | 곱셈 | `[PRICE] * [QTY]` |
| `/` | 나눗셈 | `[TOTAL] / [COUNT]` |
| `%` | 나머지 | `[VALUE] % 2` |
| `^` | 거듭제곱 | `[BASE] ^ 2` |
| `=` | 비교(==) | `[STATUS] = "Y"` |
| `!=` | 불일치 | `[STATUS] != "N"` |
| `>` `<` `>=` `<=` | 비교 | `[AMT] > 1000` |
| `!` | 논리 NOT | `![FLAG]` |
| `&&` / `AND` | 논리 AND (연산자) | `[A] > 0 && [B] > 0` |
| `‖` / `OR` | 논리 OR (연산자) | `[A] = 1 ‖ [B] = 1` |

> **참고:** 수식 모드에서 단일 `=`는 비교(`==`)로 처리된다. JavaScript 모드(`return`, `var`, `{}`가 포함된 경우)에서는 대입(`=`)으로 처리된다.

### 주석
```
// 한 줄 주석
/* 여러 줄
   주석 */
```

### JavaScript 모드
수식에 `return`, `var`, `{`, `}` 키워드가 포함되면 JavaScript 모드로 동작한다.
```
var result = [PRICE] * [QTY];
if (result > 10000) {
    return result * 0.9;
} else {
    return result;
}
```

---

## 그리드 전용 키워드

| 키워드 | 설명 |
|--------|------|
| `CELL_VALUE` | 현재 셀의 기존 값 (데이터 셀의 집계 값) |
| `FIELD_LABEL` | 현재 컬럼의 Caption (데이터 필드의 표시명) |
| `FIELD_KEY` | 현재 컬럼의 Name (데이터 필드의 키값) |
| `IS_GRAND_TOTAL` | 현재 행이 총합계 행인지 여부 (boolean) |
| `IS_SUB_TOTAL` | 현재 행이 소계 행인지 여부 (boolean) |

```
// 총합계 행에서만 다른 계산 적용
IIF(IS_GRAND_TOTAL, [TOTAL_AMT], [PRICE] * [QTY])
```

---

## 함수 레퍼런스

### 조건/논리 함수

#### IIF(condition, trueValue, falseValue)
> `bool IF(bool condition, object trueValue, object falseValue)`

조건 검사를 수행하여 참이면 trueValue를 반환하고, 거짓이면 falseValue를 반환한다.
- `IF()`로도 사용 가능 (내부에서 `IIF`로 변환됨)
```
IIF([STATUS] = "Y", "활성", "비활성")
IIF(:txtAge > 20, "성인", "미성년")
```

#### CASE(condition1, value1, condition2, value2, ..., defaultValue)
> `object Switch(bool condition1, object value1, bool condition2, object value2, ..., object elseValue)`

조건 n개에 대해 순차적으로 검사하여 가장 처음으로 참인 조건의 값을 반환한다.
모든 조건이 거짓일 경우 마지막 default 값이 반환된다.
인자가 홀수 개이면 마지막 값이 기본값이다.
- `SWITCH()`와 동일하게 동작한다.
```
CASE(
    [GRADE] = "A", 100,
    [GRADE] = "B", 80,
    [GRADE] = "C", 60,
    0
)
```

#### AND(condition1, condition2, ...)
> `bool AND(bool condition1, bool condition2, ...)`

넘겨진 파라미터 n개의 논리곱을 반환한다. 모든 조건이 참이면 `true`를 반환한다.
```
AND([AMT] > 0, [QTY] > 0)
```

#### OR(condition1, condition2, ...)
> `bool OR(bool condition1, bool condition2, ...)`

넘겨진 파라미터 n개의 논리합을 반환한다. 하나라도 참이면 `true`를 반환한다.
```
OR([STATUS] = "A", [STATUS] = "B")
```

---

### 타입 변환 함수

#### TOSTRING(value, format?)
> `string ToString(object value, [string format])`

넘겨진 값을 문자열로 변환한다. format은 수치형 포맷 및 일자형 포맷을 사용할 수 있으며, 생략 가능하다.
```
TOSTRING(123456789, "#,##0")          // "123,456,789"
TOSTRING(12345, "{0:N2}")             // "12,345.00"
TOSTRING(0.15, "{0:P1}")              // "15.0%"
TOSTRING(NOW(), "{0:yyyy-MM-dd}")     // "2025-01-15"
```

**format 종류:**
| 포맷 | 설명 | 예시 |
|-------|------|------|
| `{0:N숫자}` | 숫자(천 단위 콤마, 소수점) | `{0:N2}` -> `1,234.56` |
| `{0:P숫자}` | 백분율 | `{0:P1}` -> `15.0%` |
| `{0:E숫자}` | 지수표현 | `{0:E2}` -> `1.23E45` |
| `{0:C숫자}` | 화폐 | `{0:C0}` -> `1,235` |
| `{0:#,###}` | 사용자 정의 숫자 | `{0:#,###.00}` |
| `#,##0` | 사용자 정의 숫자 (중괄호 없이) | `#,##0` -> `123,456,789` |
| `{0:yyyy-MM-dd}` | 날짜 | `{0:yyyy-MM-dd}` -> `2025-01-15` |

#### TONUMBER(value, defaultValue)
> `double ToNumber(object value, double defaultValue)`

value를 숫자형으로 변환한 값을 반환한다. 수치 형변환 실패 시 defaultValue를 반환한다.
```
TONUMBER("123", 0)        // 123
TONUMBER("abc", -1)       // -1
TONUMBER([QTY], 0)        // 필드값을 숫자로 변환
```

#### TODATE(value, format?)
> `DateTime ToDate(object value, [string format])`

넘겨진 값을 일자형으로 변환한다. format은 일자형 포맷으로 생략 가능하다. format 미지정 시 `yyyy-MM-dd` 형식이다.
```
TODATE("20250115", "{0:yyyy-MM-dd}")   // "2025-01-15"
TODATE("20250115", "{0:yyyy/MM/dd}")   // "2025/01/15"
TODATE(TODAY(), "yyyy-MM-dd")          // "2025-01-15"
```

---

### 타입 체크 함수

| 함수 | 설명 | 반환 |
|------|------|------|
| `ISNULL(value)` | 검사 대상 값이 null 값인지 여부를 반환 | boolean |
| `ISBOOL(value)` | 검사 대상 값이 Boolean인지 여부를 반환 | boolean |
| `ISNUMBER(value)` | 검사 대상 값이 숫자로 치환 가능한지 여부를 반환 | boolean |
| `ISSTRING(value)` | 검사 대상 값의 타입이 문자열인지 여부를 반환 | boolean |
| `ISDATETIME(value)` | 검사 대상 값의 타입이 일자형(DateTime)인지 여부를 반환 | boolean |

```
IIF(ISNULL([PRICE]), 0, [PRICE] * [QTY])
```

---

### 집계 함수 (Aggregate)

집계 함수는 데이터그리드의 데이터를 기반으로 연산한다. `:그리드컨트롤명`으로 그리드를 참조한다.

#### SUMIF(grid, fieldName, condition?)
> `double SUMIF(:Gridname, "Fieldname", "criteria")`

지정한 Grid에서 조건에 맞는 Field 데이터의 합을 구한다.
```
SUMIF(:DataGrid1, "AMT")                                    // AMT 필드 전체 합계
SUMIF(:DataGrid1, "AMT", "[DEPT] = '영업부'")                // 영업부만 합계
SUMIF(:DataGrid1, "AMT", "AND([AREA] == 'Seoul' , [Product] == 'NotBook')")
```

#### AVERAGEIF(grid, fieldName, condition?)
> `double AVERAGEIF(:Gridname, "Fieldname", "criteria")`

지정한 Grid에서 조건을 만족하는 Field 데이터의 평균을 구한다.
```
AVERAGEIF(:DataGrid1, "SCORE")
AVERAGEIF(:DataGrid1, "SCORE", "[CLASS] = 'A'")
AVERAGEIF(:Grid, "AMT", "OR([AREA] == 'Seoul', [AREA] == 'Busan')")
```

#### COUNTIF(grid, fieldName, condition?)
> `int COUNTIF(:Gridname, "Fieldname", "criteria")`

지정한 Grid에서 조건에 맞는 Field 데이터의 개수를 구한다.
```
COUNTIF(:DataGrid1, "ID")                          // 전체 행 수
COUNTIF(:DataGrid1, "ID", "[STATUS] = 'Y'")        // STATUS가 Y인 행 수
COUNTIF(:Grid, "CODE", "AND([AGE] > 20, [AGE] < 30)")
```

#### MAXIF(grid, fieldName, condition?)
> `double MAXIF(:Gridname, "Fieldname", "criteria")`

지정한 Grid에서 조건에 맞는 Field 데이터 중 최대 값을 구한다.
```
MAXIF(:DataGrid1, "AMT")
MAXIF(:DataGrid1, "AMT", "[YEAR] = '2025'")
MAXIF(:Grid, "Score", "AND([Level] == 3 , [SEX] == 'F')")
```

#### MINIF(grid, fieldName, condition?)
> `double MINIF(:Gridname, "Fieldname", "criteria")`

지정한 Grid에서 조건에 맞는 Field 데이터 중 최소 값을 구한다.
```
MINIF(:DataGrid1, "AMT")
MINIF(:Grid, "Score", "AND([Level] == 3 , [SEX] == 'F')")
```

#### DISTINCTCOUNT(grid, fieldName)
> `int DistinctCount(:Gridname, "Fieldname")`

지정한 Grid에서 Field 데이터의 고유(distinct) 값의 개수를 구한다.
```
DISTINCTCOUNT(:DataGrid1, "DEPT")
DISTINCTCOUNT(:Grid, "AREA")
```

#### GETPIVOTDATA(grid, fieldName, criteria)
> `string GETPIVOTDATA(:Gridname, "Fieldname", "criteria")`

OlapGrid에 저장된 데이터를 반환한다. criteria에 `[차원][값]` 형식으로 조건을 지정한다.
```
GETPIVOTDATA(:Grid, "AMT", "[YEAR][2017],[AREA][Seoul],[COMPANY][BIMATRIX]")
```

#### SELECTEDFIELDVALUE(grid, fieldName, defaultValue?)
> `string SelectedFieldValue(:Gridname, "Fieldname", defaultValue)`

지정한 Grid에서 선택된 셀을 구성하고 있는 레코드 중 특정 필드의 값을 반환한다.
OLAP 그리드의 경우 여러 개의 레코드를 포함하는 경우 모든 레코드의 필드값이 동일하지 않으면 NULL을 반환한다.
```
SELECTEDFIELDVALUE(:DataGrid1, "EMP_NAME", "")
SELECTEDFIELDVALUE(:DataGrid1, "DEPT_CD", "ALL")
```

#### SUMCELLS(grid, fieldName?)
> `double SUMCELLS(:Gridname, "Fieldname")`

지정한 Grid에서 선택된 영역의 합계를 구한다. fieldName을 지정하면 해당 필드만 대상으로 한다.
```
SUMCELLS(:DataGrid1)
SUMCELLS(:DataGrid1, "AMT")
"합계 : " + TOSTRING(SUMCELLS(:Grid, "FieldName"), "#,##0.0")
// -> "합계 : 12,777,856.0"
```

#### COUNTCELLS(grid, fieldName?)
> `int COUNTCELLS(:Gridname, "Fieldname")`

지정한 Grid에서 선택된 영역의 개수를 구한다.
```
COUNTCELLS(:DataGrid1)
"개수 : " + TOSTRING(COUNTCELLS(:Grid, "FieldName"), "#,##0")
// -> "개수 : 3"
```

#### AVGCELLS(grid, fieldName?)
> `double AVGCELLS(:Gridname, "Fieldname")`

지정한 Grid에서 선택된 영역의 평균값을 구한다.
```
AVGCELLS(:DataGrid1, "SCORE")
"평균 : " + TOSTRING(AVGCELLS(:Grid, "FieldName"), "#,##0.##")
// -> "평균 : 4,259,285.33"
```

> **참고:** SUMCELLS, COUNTCELLS, AVGCELLS는 숫자(Numeric) 타입이고 Visible한 컬럼의 셀만 대상으로 한다.

---

### 문자열 함수

#### LEFT(text, size)
> `string Left(string target, int nCount)`

원본 문자열에서 좌측으로부터 nCount개만큼의 길이를 가지는 새로운 문자열을 반환한다.
```
LEFT("123456789", 3)    // "123"
LEFT([CODE], 2)          // CODE 필드의 앞 2자리
```

#### RIGHT(text, size)
> `string Right(string target, int nCount)`

원본 문자열에서 우측으로부터 nCount개만큼의 길이를 가지는 새로운 문자열을 반환한다.
```
RIGHT("123456789", 3)   // "789"
```

#### MID(text, startIndex, count)
> `string SubString(string, int nFirst, int nCount)`

원본 문자열의 특정 위치(nFirst, 0-based)로부터 nCount만큼의 문자열을 반환한다.
`Mid`와 `Substring`은 동일한 함수이다.
```
MID("abcde", 1, 3)      // "bcd"
```

#### LEN(text)
> `int Len(string target)`

전달받은 문자열의 길이를 반환한다.
필드가 파라미터로 전달될 경우 해당 필드의 모든 레코드에 대한 문자열 길이의 배열을 반환한다.
```
LEN("123456789")         // 9
LEN([NAME])              // NAME 필드의 문자열 길이
```

#### LOWER(text) / UPPER(text)
> `string Lower(string target)` / `string Upper(string text)`

전달받은 문자열을 소문자/대문자로 변환한 문자열을 반환한다.
필드가 파라미터로 전달될 경우 해당 필드의 모든 레코드에 대해 처리한다.
```
LOWER("ABC")             // "abc"
UPPER("abcde")           // "ABCDE"
```

#### FIND(textToFind, textToSearch, startIndex?)
> `int Find(string textToFind, string textToSearch, int startIndex)`

원본 문자열(textToSearch)의 특정 위치(startIndex, 0-based)로부터 대상 문자열(textToFind)을 검색하여 해당 인덱스를 반환한다. 검색 대상이 없을 경우 `-1`을 반환한다.

**주의:** 첫 번째 인자가 찾을 문자열(textToFind), 두 번째 인자가 검색 대상 문자열(textToSearch)이다.
```
FIND("bc", "abcde")              // 1
FIND("World", "Hello World")     // 6
FIND("xyz", "Hello World")       // -1
```

#### REPLACE(text, oldText, newText)
> `string Replace(string text, string oldText, string newText)`

원본 문자열의 oldText를 newText로 치환한 문자열을 반환한다 (정규식 지원).
- `SUBSTITUTE()`로도 사용 가능하다 (동일한 함수).
```
REPLACE("abcde", "bc", "BC")            // "aBCde"
REPLACE("Hello World", "World", "AUD")   // "Hello AUD"
REPLACE([CODE], "-", "")                  // CODE에서 하이픈 제거
```

#### TRIM(text)
> `string Trim(string text)`

원본 문자열의 시작과 종료 부분에 공백을 모두 제거한 문자열을 반환한다.
```
TRIM("   abcde   ")     // "abcde"
```

---

### 수학 함수

| 함수 | 시그니처 | 설명 | 예시 |
|------|---------|------|------|
| `ABS(value)` | `double ABS(double value)` | 절댓값 | `ABS(-100)` -> `100` |
| `CEIL(value)` | `double CEIL(value)` | 지정한 수 이상의 가장 작은 정수(올림) | `CEIL(0.95)` -> `1` |
| `FLOOR(value, significance?)` | `double FLOOR(double value, double significance)` | 수를 significance의 배수가 되도록 내림. significance 생략 시 주어진 수와 같거나 작은 가장 큰 정수를 반환 | `FLOOR(45.95)` -> `45`, `FLOOR(3910, 50)` -> `3900` |
| `ROUND(value, decimals?)` | `double ROUND(double value, int decimals)` | 지정한 소수점 자릿수로 반올림 | `ROUND(1.256, 2)` -> `1.26` |
| `LOG(value, base?)` | `double LOG(double value, double base)` | 지정한 밑의 로그 | `LOG(2, 8)` -> `3` |
| `LOG10(value)` | `double LOG10(double value)` | 상용로그 (밑 10) | `LOG10(100)` -> `2` |
| `EXP(value)` | `double EXP(double value)` | 자연 상수 e의 거듭제곱 | `EXP(1)` -> `2.71828...` |
| `RAND(max?)` | `double RAND([double max])` | 0~max 사이 난수. max 미지정 시 0~1 사이 난수 반환 | `RAND(100)` -> `97.1234` |
| `SIN(value)` | `double SIN(double value)` | 사인 (라디안) | `SIN(Math.PI / 2)` -> `1` |
| `COS(value)` | `double COS(double value)` | 코사인 (라디안) | `COS(1)` -> `0.5403...` |
| `TAN(value)` | `double TAN(double value)` | 탄젠트 | `TAN(1)` -> `1.557...` |
| `ASIN(value)` | `double ASIN(double value)` | 아크사인 | `ASIN(-1)` -> `-1.5707...` |
| `ACOS(value)` | `double ACOS(double value)` | 아크코사인 | `ACOS(-1)` -> `3.1415...` |
| `ATAN(value)` | `double ATAN(double value)` | 아크탄젠트 | `ATAN(1)` -> `0.7853...` |

---

### 날짜/시간 함수

#### NOW()
> `DateTime NOW()`

현재 시스템의 날짜와 시간을 `yyyyMMddHHmmssSSS` 형식 문자열로 반환한다.
```
NOW()       // "20250115170409448"
```

#### TODAY()
> `DateTime TODAY()`

현재 시스템의 날짜를 `yyyyMMdd` 형식 문자열로 반환한다. 시간은 00:00:00으로 설정된다.
```
TODAY()     // "20250115"
```

#### YEAR(date), MONTH(date), DAY(date)
> `int YEAR(DateTime date)` / `int MONTH(DateTime date)` / `int DAY(DateTime date)`

대상 날짜에서 연/월/일을 추출한다. date는 Date 객체 또는 `yyyyMMdd` 이상의 문자열이다.
- **YEAR**: 년도를 반환
- **MONTH**: 월의 값을 반환 (1~12)
- **DAY**: 일의 값을 반환 (1~31)
```
YEAR("20250115")    // 2025
MONTH("20250115")   // 1
DAY("20250115")     // 15
YEAR(TODAY())       // 현재 연도
```

#### WEEKDAY(date)
> `int WEEKDAY(DateTime date)`

대상 날짜의 요일값을 반환한다 (0=일요일, 1=월요일, ..., 6=토요일).
```
WEEKDAY("20250115")   // 3 (수요일)
```

#### HOUR(date), MINUTE(date), SECOND(date)
> `int HOUR(DateTime date)` / `int MINUTE(DateTime date)` / `int SECOND(DateTime date)`

대상 시간의 시/분/초를 추출한다.
- **HOUR**: 시간 값 반환 (0~23)
- **MINUTE**: 분 값 반환 (0~59)
- **SECOND**: 초 값 반환 (0~59)
```
HOUR("20250115143025")      // 14
MINUTE("20250115143025")    // 30
SECOND("20250115143025")    // 25
```

#### DATEADD(interval, number, date)
> `DateTime DATEADD(interval, double number, DateTime date)`

대상 일자에 일자의 각 단위(년, 분기, 월, 일 등)를 가감한 일자를 반환한다.

**interval 상수:**
| 상수 | 의미 |
|------|------|
| `1` | YEAR (년) |
| `2` | MONTH (월) |
| `5` | DAY (일) |
| `11` | HOUR (시) |
| `12` | MINUTE (분) |
| `13` | SECOND (초) |

```
DATEADD(5, 1, "20201231")           // 1일 후 -> "202101010000000"
DATEADD(5, 7, "20250115")           // 7일 후 -> "20250122..."
DATEADD(2, -1, "20250115")          // 1개월 전 -> "20241215..."
DATEADD(1, 1, TODAY())              // 1년 후
```

#### DATEDIFF(interval, date1, date2)
> `int DATEDIFF(interval, DateTime date1, DateTime date2)`

두 일자 간 차이의 값을 반환한다 (date2 - date1). interval 상수는 DATEADD와 동일하다.
```
DATEDIFF(5, "20201215", "20201231")    // 16 (일)
DATEDIFF(5, "20250101", "20250115")    // 14 (일)
DATEDIFF(2, "20240115", "20250115")    // 12 (개월)
DATEDIFF(1, "20200101", "20250101")    // 5 (년)
```

#### DATEPART(interval, date)
> `double DATEPART(interval, DateTime date)`

일자의 각 파트에 해당하는 값을 반환한다. interval 상수는 DATEADD와 동일하다.
YEAR(), MONTH() 등과 유사하나 interval로 지정한다.
```
DATEPART(1, "20250115")     // 2025 (년)
DATEPART(2, "20250115")     // 1 (월)
DATEPART(5, "20250115")     // 15 (일)
```

#### DATE(year, month, day, hour?, minute?, second?)
> `DateTime DATE(int year, int month, int day [, int hour, int minute, int second])`

넘겨진 파라미터 값을 가지고 새로운 일자(Date 객체)를 반환한다. 시/분/초는 옵션이다.
```
DATE(2025, 1, 15)
DATE(2025, 1, 15, 14, 30, 0)
DATE("2020", "12", "31")           // Thu Dec 31 2020 ...
```

#### DATE2(year_diff, month_diff, day_diff)
> `DateTime DATE2(int year_diff, int month_diff, int day_diff)`

현재 날짜를 기준으로 상대적인 차이(년, 월, 일)를 적용한 새로운 일자를 반환한다.
```
DATE2(0, 0, 1)      // 오늘 + 1일
DATE2(0, -1, 0)     // 오늘 - 1개월
DATE2(1, 0, 0)      // 오늘 + 1년
```

---

## MTSD 문서에서의 수식 적용 위치

MTSD(.mtsd) 파일에서 수식은 각 Element의 `Formula` 속성에 설정한다.

### Formula 속성을 지원하는 Element 타입

| Element 타입 | Formula 속성 | 필수/선택 | MTSD JSON 경로 |
|-------------|-------------|----------|---------------|
| **Label** | `Formula` | 필수 | `Forms[].Elements[].Formula` |
| **NumberBox** | `Formula` | 필수 | `Forms[].Elements[].Formula` |
| **TextBox** | `Formula` | 선택 | `Forms[].Elements[].Formula` |

> **참고:** CheckBox, ComboBox, Button, DataGrid(GridColumn) 등에는 `Formula` 속성이 없다.

### MTSD 적용 예시

#### 라벨에 수식 설정
`:VS_COMPANY` 값이 변경될 때 `lblText`에 `:VS_COMPANY + 1` 값을 표시하려면,
해당 Label Element의 `Formula` 속성에 수식을 작성한다.
```json
{
  "Type": "Label",
  "Name": "lblText",
  "Formula": ":VS_COMPANY + 1",
  "Text": "",
  "Cursor": "default",
  "UseTextOverflow": false,
  "UseAutoLineBreak": false,
  "LineSpacing": 0,
  "HasLineSpacing": false,
  "LanguageCode": "",
  "MxBinding": "",
  "MxBindingUseStyle": false
}
```
수식에서 `:VS_COMPANY`를 참조하면, 해당 컨트롤의 값이 변경될 때 수식이 자동 재연산된다.

#### NumberBox에 수식 설정
두 텍스트박스의 곱셈 결과를 NumberBox에 자동 계산하려면:
```json
{
  "Type": "NumberBox",
  "Name": "nbxTotal",
  "Formula": ":txtPrice * :txtQty",
  "Format": "{0:N0}",
  "Value": 0,
  "Text": "",
  "IsReadOnly": true,
  "Maximum": 999999999,
  "Minimum": 0,
  "MxBinding": "",
  "MxBindingUseStyle": false
}
```

### DataGrid 컬럼 수식에 대한 참고

DataGrid의 GridColumn에는 MTSD 스키마상 `Formula` 속성이 존재하지 않는다.
그리드 컬럼 수식(`[PRICE] * [QTY]` 등)은 i-AUD Designer에서 컬럼의 **계산수식** 설정을 통해 구성한다.
따라서 MTSD 파일을 직접 편집하여 그리드 컬럼에 수식을 추가할 수 없으며,
i-AUD Designer에서 해당 컬럼을 선택한 뒤 속성 창의 '계산수식' 항목에서 설정해야 한다.

> **대안:** 클라이언트 스크립트에서 `DataGrid`의 `OnCellFormatting` 이벤트 등을 활용하여
> 런타임에 셀 값을 동적으로 계산하는 방법도 있다.

---

## 수식 사용 예시

### 라벨/텍스트박스 수식
```
// 다른 컨트롤 참조하여 계산
:txtPrice * :txtQty

// 그리드 합계를 라벨에 표시
SUMIF(:DataGrid1, "AMT")

// 조건부 텍스트 표시
IIF(:txtScore >= 60, "합격", "불합격")

// 포맷 적용
TOSTRING(SUMIF(:DataGrid1, "AMT"), "{0:N0}")

// 문자열 연결 + 날짜 함수 조합
LEFT(TODAY(), 4) + "년 " + MID(TODAY(), 4, 2) + "월"
```

### 데이터그리드 컬럼 수식
```
// 단가 x 수량
[PRICE] * [QTY]

// 할인율 적용 금액
[PRICE] * [QTY] * (1 - [DISCOUNT_RATE] / 100)

// 조건에 따른 등급
IIF([SCORE] >= 90, "A", IIF([SCORE] >= 80, "B", IIF([SCORE] >= 70, "C", "D")))

// CASE 사용
CASE(
    [DEPT] = "10", "영업부",
    [DEPT] = "20", "개발부",
    [DEPT] = "30", "관리부",
    "기타"
)

// 날짜 차이 계산
DATEDIFF(5, [START_DATE], [END_DATE])

// 총합계 행에서 다른 계산 적용 (GroupGrid)
IIF(IS_GRAND_TOTAL, CELL_VALUE, [PRICE] * [QTY])
```

### 복합 수식 (JavaScript 모드)
```
var price = TONUMBER([PRICE], 0);
var qty = TONUMBER([QTY], 0);
var total = price * qty;

if (total > 100000) {
    return TOSTRING(total * 0.9, "{0:N0}");
} else {
    return TOSTRING(total, "{0:N0}");
}
```

---

## 주의사항

1. **순환 참조 금지**: 수식에서 자기 자신을 참조하거나 순환 참조하면 오류가 발생한다.
2. **필드명/캡션**: 그리드 집계 함수의 fieldName 인자에는 필드명(Name) 또는 캡션(Caption) 모두 사용 가능하다.
3. **대소문자**: 함수명은 대소문자를 구분하지 않는다 (`SUMIF`, `SumIf`, `sumif` 모두 동일).
4. **문자열 리터럴**: 문자열은 큰따옴표(`"`) 또는 작은따옴표(`'`)로 감싼다.
5. **반환값**: 수식 모드에서는 `return`을 생략하면 자동으로 추가된다. JavaScript 모드에서는 명시적으로 `return`을 사용해야 한다.
6. **숫자 필드**: Numeric 타입 필드의 값이 null/undefined이면 `0`으로 처리된다.
7. **집계 함수의 condition**: condition 내에서 `[필드명]`으로 그리드의 각 행의 필드를 참조할 수 있다.
8. **FIND 파라미터 순서**: `FIND(찾을문자열, 검색대상문자열, 시작인덱스)` 순서이다. 첫 번째가 찾을 문자열임에 주의한다.
9. **FLOOR의 significance**: `FLOOR(3910, 50)` -> `3900`과 같이 significance 인자를 지정하면 해당 배수로 내림한다.