---
name: iaud-olap-formula
description: i-OLAP 수식 작성 가이드. OlapGrid 계산 필드, 사용자 정의 항목, 조건부 서식에서 사용하는 수식 함수와 문법을 안내합니다. "OLAP 수식", "계산 필드", "ForAll", "ForEach", "집계 함수", "Rank", "조건부 서식 수식" 등을 물어볼 때 사용하세요.
---

# i-OLAP 함수 작성 가이드

> 이 문서는 i-OLAP 서버의 수식 엔진에서 사용할 수 있는 함수, 상수, 변수 바인딩 규칙을 정리한 가이드입니다.

---

## 1. 개요

### 1.1. 수식 사용 위치

i-OLAP에서 함수는 다음 세 곳에서 사용됩니다.

| 사용 위치 | 설명 |
|-----------|------|
| **계산 필드** | OLAP 그리드의 속성 창에서 필드를 추가한 뒤, 수식 편집창에서 수식을 입력합니다. |
| **계산 항목 (사용자 정의 항목)** | 디멘전 항목의 context menu에서 [사용자 정의 항목]을 클릭하여 생성합니다. 필터 수식(bool 반환)과 집계 수식 두 가지로 구성됩니다. |
| **조건부 서식** | 사전 정의된 스타일의 이름 또는 키 값을 반환하는 수식을 작성합니다. |

### 1.2. Context 이해

수식이 사용되는 위치에 따라 Context가 달라집니다.

| Context | 설명 |
|---------|------|
| **DataCell Context** | 계산 필드를 값 영역에 배치할 때 사용. **다수의 레코드**를 대상으로 계산합니다. |
| **HeaderCell Context** | 계산 필드를 헤더 영역(Row/Column)에 배치할 때 사용. 전체 레코드를 **순차적으로 단일 레코드씩** 계산합니다. 레코드가 많으면 성능 저하 우려. |
| **Filter Context** | 사용자 정의 항목의 필터 수식에서 사용. 모든 레코드를 순회하며 `true`/`false`를 반환하여 항목 포함 여부를 결정합니다. |

### 1.3. 필드 참조 문법

수식에서 필드를 참조할 때는 **대괄호(`[]`)**로 감싸서 사용합니다.

```
[필드명]
[COMPANY]
[판매수량]
```

### 1.4. 연산자

| 연산자 | 설명 |
|--------|------|
| `+` | 덧셈 |
| `-` | 뺄셈 |
| `*` | 곱셈 |
| `/` | 나눗셈 |
| `%` | 나머지 |
| `==` | 같음 비교 |
| `!=` | 같지 않음 비교 |
| `>` | 크다 |
| `<` | 작다 |
| `>=` | 크거나 같다 |
| `<=` | 작거나 같다 |

### 1.5. 주석

```
// 라인 주석
/* 멀티 라인 주석 */
```

---

## 2. 변수 바인딩 및 상수 선언

### 2.1. 변수 바인딩

수식 내부에 동적으로 조건이나 값을 변경할 수 있도록 변수 바인딩을 지원합니다.
변수 바인딩 규칙은 `:변수명` 형식을 사용합니다.

```
SUM([Units]) / :VN_UNIT
```

실행 시 `:VN_UNIT`은 바인딩된 값(예: 10)으로 치환되어 `SUM([Units]) / 10`이 됩니다.

### 2.2. 동적 필드 선언 (define)

`define`은 수식 내에서 **동적으로 필드를 선언**합니다. 다른 수식에서 필드를 파라미터로 받는 경우, 해당 필드를 사전에 등록하는 용도로 사용합니다. `define`으로 선언한 필드는 셀 계산 시마다 수식이 평가되어 동적으로 값이 결정됩니다.

**문법:**
```
define 필드명 = 수식
```

**사용 시 `[]` 필수:** `define`으로 선언한 필드를 참조할 때는 일반 필드와 동일하게 **대괄호(`[]`)로 감싸서** 필드임을 표시해야 합니다.

**제약 사항:** 순차적으로 파싱되므로, 사용하기 전에 선언해야 합니다.

**예제 1: 뉴욕 판매 비중 계산**
```
// 뉴욕판매수량을 동적 필드로 선언 → 참조 시 [뉴욕판매수량]으로 사용
define 뉴욕판매수량  = IF( [지역] == "뉴욕", [판매수량] , 0)
define 뉴욕_수량     = Sum( ForEach("[지역]", [뉴욕판매수량]) )
IF([판매수량]== 0, 0,  [뉴욕_수량]  /[판매수량])
```

**멀티라인 수식:**
중괄호 `{}`를 사용하여 멀티라인 수식을 작성할 수 있습니다.
```
define V_CALC = {
  IF([지역] == "뉴욕", [판매수량], 0)
}
// 사용 시: [V_CALC]
```

### 2.3. 상수 정의 (const)

`const`는 **상수를 정의**합니다. 한 번 계산된 값을 고정으로 보유하며, 이후 수식에서 해당 값으로 대체되어 계산됩니다. `define`과 달리 셀마다 재평가되지 않습니다.

**문법:**
```
const 상수명 = 값 또는 수식
```

**예제:**
```
const RATE = 1.1
const BASE = 100

[판매수량] * RATE + BASE
```

---

## 3. 내장 상수

수식 내에서 사용할 수 있는 내장 상수입니다.

| 상수명 | 타입 | 설명 |
|--------|------|------|
| `IsRowGrandTotal` | bool | 데이터 셀의 Row 헤더가 총계인지 여부 |
| `IsColGrandTotal` | bool | 데이터 셀의 Column 헤더가 총계인지 여부 |
| `IsRowTotal` | bool | 데이터 셀의 Row 헤더가 소계인지 여부 |
| `IsColTotal` | bool | 데이터 셀의 Column 헤더가 소계인지 여부 |
| `IsTotal` | bool | 데이터 셀의 헤더가 소계인지 여부 |
| `IsGrandTotal` | bool | 데이터 셀의 헤더가 총계인지 여부 |
| `IsTotalOrGrandTotal` | bool | 데이터 셀의 헤더가 총계 또는 소계인지 여부 |
| `CELL_VALUE` | object | 데이터 셀의 값 |
| `FIELD_KEY` | string | 데이터 셀의 데이터 필드의 키값 |
| `FIELD_LABEL` | string | 데이터 셀의 데이터 필드의 표시명 |

**활용 예:**
```
// 소계/총계 행에서는 빈 값을 반환
IF(IsTotalOrGrandTotal, "", [판매수량] / [목표수량] * 100)
```

---

## 4. 함수 레퍼런스

### 4.1. 조건 분기 함수

#### IF / IIF

조건 검사를 수행하여 참이면 trueValue를, 거짓이면 falseValue를 반환합니다.

```
IF(condition, trueValue, falseValue)
IIF(condition, trueValue, falseValue)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| condition | bool | 조건식 |
| trueValue | object | 조건이 참일 때 반환값 |
| falseValue | object | 조건이 거짓일 때 반환값 |

**반환 타입:** object

**예제:**
```
IF( 1 > 2, "1은 2보다 크다", "1은 2보다 작다")
// => "1은 2보다 작다"

IF( [판매수량] > 100, "초과", "미달")
```

#### SWITCH / CASE

조건 n개에 대해 순차적으로 검사하여 가장 처음으로 참인 조건의 값을 반환합니다.

```
SWITCH(condition1, value1, condition2, value2, ..., defaultValue)
CASE(condition1, value1, condition2, value2, ..., defaultValue)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| condition1 | bool | 조건 1 |
| value1 | object | 조건1이 참일 때 반환값 |
| ... | ... | 반복 |
| defaultValue | object | 모든 조건이 거짓일 때 기본값 |

**반환 타입:** object

**예제:**
```
CASE(
  1==2, "1과 2는 같다",
  2==1, "2와 1은 같다",
  1==1, "1과 1은 같다",
  "같은 조건이 없다"
)
// => "1과 1은 같다"
```

---

### 4.2. 논리 함수

#### AND

넘겨진 파라미터 n개의 논리곱(AND)을 반환합니다.

```
AND(bool1, bool2, ..., boolN)
```

**반환 타입:** bool

**예제:**
```
IF( AND(true, 1==1, "Korea" == "Korea"), 1, 0)   // => 1
IF( AND(true, 1==2, "Korea" == "Korea"), 1, 0)   // => 0
```

#### OR

넘겨진 파라미터 n개의 논리합(OR)을 반환합니다.

```
OR(bool1, bool2, ..., boolN)
```

**반환 타입:** bool

**예제:**
```
IF( OR(1==2, "Korea" == "Korea"), 1, 0)   // => 1
IF( OR(1==2, "Korea" == "Europe"), 1, 0)  // => 0
```

#### IsNull

검사 대상 값이 null인지 여부를 반환합니다.

```
IsNull(value)
```

**반환 타입:** bool

#### IsBool

검사 대상 값이 Boolean인지 여부를 반환합니다.

```
IsBool(value)
```

**반환 타입:** bool

#### IsNumber

검사 대상 값이 숫자형인지 여부를 반환합니다.

```
IsNumber(value)
```

**반환 타입:** bool

**예제:**
```
IsNumber("100")    // => true
IsNumber(100)      // => true
IsNumber("Korea")  // => false
```

#### IsString

검사 대상 값의 타입이 문자열인지 여부를 반환합니다.

```
IsString(value)
```

**반환 타입:** bool

#### IsDateTime

검사 대상 값의 타입이 DateTime인지 여부를 반환합니다.

```
IsDateTime(value)
```

**반환 타입:** bool

**예제:**
```
IsDateTime(DATE(2013, 12, 12))  // => true
IsDateTime("2013-12-12")        // => false
```

---

### 4.3. 변환 함수

#### ToString

넘겨진 값을 문자열로 변환합니다.

```
ToString(value)
ToString(value, format)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| value | object | 변환 대상값 |
| format | string (Optional) | 변환 포맷 (수치형/일자형) |

**반환 타입:** string

**예제:**
```
ToString(DATE(2014,01,01), "yyyyMMdd")    // => "20140101"
ToString(0.12, "P2")                      // => "12.00 %"
ToString(123456.789, "#,###.###")         // => "123,456.789"
```

#### ToNumber

값을 숫자형으로 변환합니다. 실패 시 failValue를 반환합니다.

```
ToNumber(value, failValue)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| value | object | 변환 대상값 |
| failValue | object (Optional) | 변환 실패시 기본값 |

**반환 타입:** double

**예제:**
```
ToNumber("123.12", 0)   // => 123.12
ToNumber("Matrix", 0)   // => 0
```

#### ToDate

넘겨진 값을 일자형으로 변환합니다.

```
ToDate(value)
ToDate(value, format)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| value | object | 변환 대상값 |
| format | string (Optional) | 일자형 포맷 |

**반환 타입:** DateTime

**예제:**
```
ToDate("2014-12-12", "yyyy-MM-dd")   // => 2014-12-12
```

---

### 4.4. 집계 함수 (Aggregate)

#### Sum

전달값에 대한 합계를 반환합니다.

```
Sum([FIELD_NAME])
Sum(value1, value2, ..., valueN)
```

**반환 타입:** double

#### Average

전달값에 대한 평균값을 반환합니다.

```
Average([FIELD_NAME])
Average(value1, value2, ..., valueN)
```

**반환 타입:** double

#### Count

전달값에 대한 개수를 반환합니다.

```
Count([FIELD_NAME])
Count(value1, value2, ..., valueN)
```

**반환 타입:** double

#### DistinctCount

데이터 셀에서 해당 필드의 값 리스트 중 중복값을 제거한 수량을 반환합니다.

```
DistinctCount([FIELD_NAME])
```

**반환 타입:** double

#### Max / Min

전달값에 대해 최대값/최소값을 반환합니다. 문자형과 수치형 모두 지원합니다.

```
Max([FIELD_NAME])
Min([FIELD_NAME])
```

**반환 타입:** object

#### AverageOfChild

현재 셀의 자식 데이터 셀을 기준으로 평균을 계산한 값을 반환합니다.

```
AverageOfChild([FIELD_NAME])
```

**반환 타입:** double

---

### 4.5. OLAP/큐브 함수

#### AreaIsRow / AreaIsColumn / AreaIsData / AreaIsFilter / AreaIsHidden

전달 받은 필드가 배치된 영역을 판별합니다.

```
AreaIsRow([FIELD_NAME])
AreaIsColumn([FIELD_NAME])
AreaIsData([FIELD_NAME])
AreaIsFilter([FIELD_NAME])
AreaIsHidden([FIELD_NAME])
```

**반환 타입:** bool

#### AreaIndex / Area

필드가 해당 영역 내에서 몇 번째 위치인지 인덱스를 반환합니다.

```
AreaIndex([FIELD_NAME])
Area([FIELD_NAME])
```

#### IsHeaderTotal

현재 헤더가 특정 필드의 소계인지 여부를 반환합니다.

```
IsHeaderTotal([FIELD_NAME])
```

**반환 타입:** bool

#### HeaderText

화면에 배치된 상태에서 헤더영역(Row/Column)의 필드 표시 텍스트를 반환합니다.

```
HeaderText([FIELD_NAME])
```

**반환 타입:** string

#### ForAll

배치에 대해 제어하는 함수로, 현재 배치를 기준으로 Dimensions에 정의된 항목을 제거하여 상위 합에 대한 접근이 가능하게 합니다.
**비율 계산 시 주로 사용됩니다.** SQL의 그룹핑 기능과 유사하게 동작합니다.

```
ForAll("Dimensions", [MEASURE])
ForAll("Dimensions", [MEASURE], NoFilter)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| Dimensions | string | 현재 배치에서 제외할 디멘전 목록 (`;`로 구분) |
| Measure | string | 계산할 대상 필드명 |
| NoFilter | bool (Optional) | 필터 정보 미반영 여부 (기본값: false) |

**반환 타입:** object (Measure의 계산 결과)

**예제: 전체 대비 비율 계산**
```
// [COMPANY] 디멘전을 제외한 전체 합계 대비 비율
[판매수량] / ForAll("[COMPANY]", [판매수량]) * 100
```

#### ForEach

배치에 대해 제어하는 함수로, 현재 배치를 기준으로 Dimensions에 정의된 항목을 추가하여 하위 목록의 그룹 데이터를 반환합니다.
**특정 레벨로 그룹하여 평균 등을 계산할 때 주로 사용됩니다.**

```
ForEach("Dimensions", [MEASURE])
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| Dimensions | string | 추가할 디멘전 목록 (`;`로 구분) |
| Measure | string | 계산할 대상 필드명 |

**반환 타입:** Record Array

**예제:**
```
// 지역별 그룹 데이터의 합계
Sum(ForEach("[지역]", [판매수량]))
```

#### InList

대상 필드의 값이 비교 값 목록 내에 존재하는지 여부를 반환합니다.

```
InList([FIELD_NAME], "value1", "value2", ..., "valueN")
```

**반환 타입:** bool

**예제:**
```
InList([지역], "서울", "부산", "대구")
// InList의 역: InList([필드명], "항목1", "항목2") == false
// 배열 형식: InList([Locale], ["a","b","c","d"])
```

#### InDimension

특정 디멘전을 제외하고 값을 계산합니다.

```
InDimension("Dimensions", [MEASURE])
```

**반환 타입:** object

#### Match

대상 필드의 값이 문자열 패턴에 일치하는지 여부를 반환합니다. 대/소문자를 구분합니다.

```
Match([FIELD_NAME], "pattern")
```

**패턴 규칙:**
- `*a` : a로 끝나는 모든 문자열
- `a*` : a로 시작하는 모든 문자열
- `*a*` : a가 포함된 모든 문자열

**반환 타입:** bool

#### GetMembers

현재 배치된 화면에서 특정 항목에 일치하는 데이터 셀을 검색하고 해당 셀의 값들을 반환합니다.

```
GetMembers([FIELD_NAME], "keyword", [MEASURE])
GetMembers([FIELD_NAME], "keyword", [MEASURE], "noCheckField")
```

**반환 타입:** Record Array

**예제: Korea 대비 비중값 구하기**
```
[판매수량] / Sum(GetMembers([지역], "Korea", [판매수량])) * 100
```

#### Rank

특정값을 기준으로 디멘전 항목에 대한 순위를 계산합니다.

```
Rank("DIMENSION_LIST", [MEASURE])
Rank("DIMENSION_LIST", [MEASURE], isTop)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| DIMENSION_LIST | string | 순위를 적용할 Dimension 필드 목록 (`*`=전체 필드) |
| MEASURE | string | 순위 계산에 사용할 필드 (문자열로 전달) |
| isTop | bool (Optional) | 값이 큰 항목부터 순위 지정 여부 |

**반환 타입:** int

**예제:**
```
Rank("[Company]", "[Units]", true)
Rank(GetRowFields(""), "[Units]", true)
```

#### RankIn

화면 배치에 따라 자동으로 마지막 단계에 해당하는 항목의 순위를 반환합니다.

```
RankIn([MEASURE], direction, isTop)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| MEASURE | field | 순위 계산에 사용할 필드 |
| direction | int | Rank 계산 방향 (1=Row, 2=Column) |
| isTop | bool | 값이 큰 항목부터 순위 지정 여부 |

**반환 타입:** int

#### CellValueByOffset

현재 셀의 위치를 기준으로 특정 위치의 셀의 값을 반환합니다.

```
CellValueByOffset(offsetRow, offsetColumn)
CellValueByOffset(offsetRow, offsetColumn, visibleCellOnly)
CellValueByOffset(offsetRow, offsetColumn, visibleCellOnly, targetField)
```

**예제: 전년 대비 증감률**
```
CELL_VALUE - CellValueByOffset(0, -1)
```

#### ColumnIndex / RowIndex / DisplayColumn / DisplayRow

셀의 위치 인덱스를 반환합니다.

```
ColumnIndex()    // Column 내부 인덱스 (0부터)
RowIndex()       // Row 내부 인덱스 (0부터)
DisplayColumn()  // Column 화면 표시 순서 (0부터)
DisplayRow()     // Row 화면 표시 순서 (0부터)
```

> **RowIndex vs DisplayRow:** RowIndex는 내부 인덱스이고, DisplayRow는 노드 축소 등의 상태가 반영된 화면 표시 순서입니다.

#### GetRowFields / GetColumnFields / GetFields

현재 OLAP 배치를 기준으로 영역의 필드 목록을 반환합니다.

```
GetRowFields("제외할_필드목록")
GetColumnFields("제외할_필드목록")
GetFields("제외할_필드목록")
```

**반환 타입:** string

#### GetVariationValue

해당 셀의 특정 Measure 값으로 2차 계산의 값을 반환합니다.

```
GetVariationValue([FIELD_NAME])
GetVariationValue([FIELD_NAME], isVisible)
```

#### GetRecordValue / GetRecordCount

데이터 셀의 레코드 값 또는 레코드 수를 반환합니다.

```
GetRecordValue([FIELD_NAME])
GetRecordValue([FIELD_NAME], recordIndex)
GetRecordCount()
```

#### IsNullCell

해당 셀이 레코드가 없거나 모든 레코드의 값이 null인지 여부를 반환합니다.

```
IsNullCell()
```

**반환 타입:** bool

#### HasUpdateRow

현재 셀의 레코드 중 수정된 레코드가 존재하는지 여부를 반환합니다. (Write-Back시 사용)

```
HasUpdateRow()
```

**반환 타입:** bool

#### IMG

셀에 이미지를 표현합니다.

```
IMG("imagePath", width, height)
```

**예제:**
```
IF([Units] < 100000, IMG("red_circle.png", 16, 16), IMG("green_circle.png", 16, 16))
```

#### Array / DrawChart

셀 차트(SparkLine)를 그리기 위한 함수입니다.

```
Array(value1, value2, ..., valueN)
DrawChart(array, itemNames, lineWidth, pointSize, lineColor, pointColor, maxPointColor, minPointColor, pointType)
```

| pointType | 설명 |
|-----------|------|
| 0 | None |
| 1 | MinMax |
| 2 | All |
| 3 | BigSizeMinMax |

---

### 4.6. 문자열 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| `Left` | `Left(source, nCount)` | 좌측으로부터 n개 문자열 |
| `Right` | `Right(source, nCount)` | 우측으로부터 n개 문자열 |
| `Len` | `Len(source)` | 문자열 길이 |
| `Lower` | `Lower(source)` | 소문자 변환 |
| `Upper` | `Upper(source)` | 대문자 변환 |
| `Find` | `Find(source, findText, startIndex)` | 문자열 검색 (없으면 -1) |
| `Mid` / `Substring` | `Mid(source, startIndex, nCount)` | 부분 문자열 |
| `Replace` / `Substitute` | `Replace(source, oldText, newText)` | 문자열 치환 |
| `Trim` | `Trim(source)` | 양쪽 공백 제거 |

---

### 4.7. 수학 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| `ABS` | `ABS(value)` | 절대값 |
| `ACOS` | `ACOS(value)` | 아크코사인 |
| `ASIN` | `ASIN(value)` | 아크사인 |
| `ATAN` | `ATAN(value)` | 아크탄젠트 |
| `CEIL` | `CEIL(value)` | 올림 |
| `COS` | `COS(value)` | 코사인 |
| `EXP` | `EXP(value)` | e의 거듭제곱 |
| `FLOOR` | `FLOOR(value)` | 내림 |
| `LOG` | `LOG(value)` | 자연 로그 |
| `LOG10` | `LOG10(value)` | 상용 로그 |
| `RAND` | `RAND(max)` | 난수 (max 미지정 시 0~1) |
| `ROUND` | `ROUND(value, decimals)` | 반올림 |
| `SIN` | `SIN(value)` | 사인 |
| `TAN` | `TAN(value)` | 탄젠트 |

---

### 4.8. 날짜/시간 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| `NOW` | `NOW()` | 현재 날짜와 시간 |
| `TODAY` | `TODAY()` | 현재 날짜 (시간 00:00:00) |
| `YEAR` | `YEAR(dateTime)` | 년도 |
| `MONTH` | `MONTH(dateTime)` | 월 (1~12) |
| `DAY` | `DAY(dateTime)` | 일 (1~31) |
| `WEEKDAY` | `WEEKDAY(dateTime)` | 요일 (0=일~6=토) |
| `HOUR` | `HOUR(dateTime)` | 시 (0~23) |
| `MINUTE` | `MINUTE(dateTime)` | 분 (0~59) |
| `SECOND` | `SECOND(dateTime)` | 초 (0~59) |
| `DATE` | `DATE(year, month, day [, hour, minute, second])` | 날짜 생성 |
| `DATEADD` | `DATEADD(interval, addValue, dateTime)` | 일자 가감 |
| `DATEDIFF` | `DATEDIFF(interval, date1, date2)` | 두 일자 차이 |
| `DATEPART` | `DATEPART(interval, dateTime)` | 일자 파트 값 |

**날짜 상수 (Interval):** `dtYear`, `dtMonth`, `dtDay`, `dtHour`, `dtMinute`, `dtSecond`

**예제:**
```
DATEADD(dtYear, 1, DATE(2015, 04, 01))    // => 2016-04-01
DATEDIFF(dtMonth, DATE(2000, 04, 01), DATE(2015, 04, 01))  // => 180
```

---

## 5. 실전 수식 예제

### 5.1. 전체 대비 비율 계산
```
[판매수량] / ForAll("[COMPANY]", [판매수량]) * 100
```

### 5.2. 소계/총계 행 분기 처리
```
IF(IsTotalOrGrandTotal, "",
   [판매수량] / [목표수량] * 100
)
```

### 5.3. define을 활용한 복합 계산
```
define V_뉴욕판매수량 = IF([지역] == "뉴욕", [판매수량], 0)
define V_뉴욕_수량 = Sum(ForEach("[지역]", [V_뉴욕판매수량]))
IF([판매수량] == 0, 0, [V_뉴욕_수량] / [판매수량])
```

### 5.4. 전년 대비 증감률
```
IF(CellValueByOffset(0, -1) == 0, 0,
   (CELL_VALUE - CellValueByOffset(0, -1)) / CellValueByOffset(0, -1) * 100
)
```

### 5.5. 조건별 이미지 표시
```
IF([Units] < 100000,
   IMG("red_circle.png", 16, 16),
   IMG("green_circle.png", 16, 16)
)
```

### 5.6. 다중 조건 분기
```
CASE(
  FIELD_KEY == "revenue", [매출액] * 1.1,
  FIELD_KEY == "cost",    [원가] * 0.9,
  CELL_VALUE
)
```

### 5.7. 순위 계산
```
Rank("[Company]", "[Units]", true)
```

### 5.8. 셀 차트 (SparkLine)
```
DrawChart(
  Array([Q1_Units], [Q2_Units], [Q3_Units], [Q4_Units]),
  "Q1,Q2,Q3,Q4",
  1, 3,
  "#3366CC", "#3366CC", "#DC3912", "#109618",
  1
)
```
