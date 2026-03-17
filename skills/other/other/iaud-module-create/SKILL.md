---
name: iaud-module-create
description: i-AUD 모듈(Module) 생성 가이드. 프로세스 봇에서 재활용 가능한 모듈의 JavaScript 스크립트와 .module.json 파일을 작성합니다. "모듈 만들기", "모듈 생성", "프로세스 봇 모듈", "워크플로우 모듈" 등을 요청할 때 사용하세요.
---

# i-AUD 모듈(Module) 생성 가이드

## 1. 모듈이란?

i-AUD **모듈**은 프로세스 봇(WorkFlow)에서 재활용할 수 있는 **클라이언트 스크립트 단위**입니다.
모듈은 **익명 함수** 형태로 호출되며, 파라미터는 `arguments[n]`으로 전달받습니다.

```
실행 구조:
(function() {
    // ← SCRIPT_TEXT 내용이 여기에 들어감
    // arguments[0], arguments[1], ... 로 파라미터 수신
})(파라미터1값, 파라미터2값, ...)
```

---

## 2. 출력 파일 형식

모듈 생성 결과물은 **`.module.json`** 파일입니다.
파일명은 모듈 제목과 동일하게 합니다: `[모듈제목].module.json`

### 2.1 전체 JSON 구조

```json
{
    "TYPE": "Single",
    "MTX_MODULE_INFO": [
        {
            "MODULE_CODE": "",
            "MODULE_SUBJECT": "모듈 제목",
            "USE_AUTHORITY": "0",
            "EDIT_AUTHORITY": "-1",
            "MODULE_DESCRIPTION": "모듈 설명",
            "SCRIPT_TEXT": "... JavaScript 소스코드 ...",
            "MODULE_TYPE": "",
            "RESULT_TYPE": "",
            "ORIGINAL_MODULE_CODE": "",
            "CREATE_USER": "",
            "MODIFY_USER": "",
            "MODULE_SEQ": "3",
            "WF_YN": "",
            "EVENT_YN": "N",
            "ATTR1": "",
            "ATTR2": "",
            "ATTR3": "",
            "MTX_MODULE_PARAMS": [
                {
                    "MODULE_CODE": "",
                    "PARAM_SEQ": "1",
                    "PARAM_TYPE": "INP001",
                    "NULLABLE": "N",
                    "PARAM_DESCRIPTION": "파라미터 설명",
                    "DEFAULT_VALUE": "",
                    "ATTR1": "",
                    "ATTR2": "",
                    "ATTR3": ""
                }
            ]
        }
    ]
}
```

### 2.2 주요 필드 설명

| 필드 | 설명 | 비고 |
|------|------|------|
| `MODULE_CODE` | 모듈 고유코드 | 빈 문자열 (서버에서 자동 생성) |
| `MODULE_SUBJECT` | 모듈 제목 | 사용자에게 표시되는 이름 |
| `MODULE_DESCRIPTION` | 모듈 설명 | 줄바꿈은 `\n` 사용 |
| `SCRIPT_TEXT` | JavaScript 소스코드 | 익명 함수 본문 (아래 작성 규칙 참조) |
| `EVENT_YN` | 이벤트 등록 모듈 여부 | `"Y"` 또는 `"N"` |
| `WF_YN` | WorkFlow 전용 여부 | `"Y"` 또는 빈 문자열 |
| `MTX_MODULE_PARAMS` | 파라미터 정의 배열 | 아래 파라미터 타입 참조 |

### 2.3 EVENT_YN 판단 기준

- **`"N"`** (기본): 모듈 실행 시 **즉시 동작**하고 완료 (예: 값 설정, 데이터 변환, Alert 표시)
- **`"Y"`**: 모듈이 **이벤트 핸들러를 등록**하여 이후 사용자 동작에 반응 (예: 버튼 클릭 시 동작, 그리드 데이터 바인딩 시 동작)

---

## 3. 파라미터 타입 (PARAM_TYPE)

| 코드 | 설명 | UI 동작 | arguments 값 |
|------|------|---------|-------------|
| `INP001` | 텍스트 입력 | 텍스트 입력창 | string |
| `INP002` | 정수 입력 | 숫자 입력창 | string (정수) |
| `INP021` | 실수 입력 | 숫자 입력창 (소수점) | string (실수) |
| `INP003` | 데이터 그리드 선택 | 그리드 목록에서 선택 | string (컨트롤명) |
| `INP004` | 단일 컨트롤 선택 | 컨트롤 목록에서 하나 선택 | string (컨트롤명) |
| `INP005` | 다중 컨트롤 선택 | 컨트롤 목록에서 여러 개 선택 | string (콤마 구분) |
| `INP006` | Form 선택 | Form 목록에서 선택 | string (Form명) |
| `INP007` | 데이터 소스 선택 | 데이터소스 목록에서 선택 | string (데이터소스명) |
| `INP008` | Y/N 선택 | 체크박스 | string ("Y" 또는 "N") |
| `INP009` | BoxStyle 선택 | BoxStyle 목록에서 선택 | string (스타일코드) |
| `INP010` | ServerScript 선택 | 서버스크립트 목록에서 선택 | string (스크립트명) |
| `INP011` | 실행계획 선택 | 실행계획 목록에서 선택 | string (실행계획명) |
| `INP020` | 보고서 선택 | 보고서 선택 다이얼로그 | string (보고서코드) |
| `INP999` | 사용자 정의 목록 | 드롭다운 선택 | string (선택값) |

### INP999 사용 시 ATTR1 설정

`INP999`는 `ATTR1`에 파이프(`|`)로 구분한 선택 목록을 정의합니다. 항목의 실제 값과 사용자에게 표현값을 달리하려면 값;표시문자 형태로 합니다.

```json
{
    "PARAM_TYPE": "INP999",
    "PARAM_DESCRIPTION": "집계 함수를 선택해 주세요.",
    "DEFAULT_VALUE": "SUM",
    "ATTR1": "SUM;합계|COUNT;개수|AVG;평균|MIN;최소값|MAX;최대값"
}
```

---

## 4. 스크립트 작성 규칙

### 4.1 핵심 규칙

1. **순수 JavaScript로 작성** - TypeScript 문법 사용 불가 (var 사용, 타입 어노테이션 없음)
2. **익명 함수 본문** - function 선언 없이 바로 실행 코드 작성
3. **파라미터는 `arguments[n]`** - 0부터 시작, 모두 string 타입
4. **`Matrix` 객체 사용 가능** - 전역으로 접근 가능
5. **`EXECUTE_NEXT()` 호출** - WorkFlow에서 다음 단계로 진행 시 호출 (비동기 작업 완료 후)
6. **SCRIPT_TEXT는 한 줄 문자열** - JSON 내에서 줄바꿈은 `\n`, 따옴표는 `\"`, 탭은 `\t`로 이스케이프

### 4.2 스크립트 구조 패턴

```javascript
// 1. 파라미터 수신
var gridName = (arguments[0] || "").trim();
var chartName = (arguments[1] || "").trim();

// 2. 입력 검증 (validate)
var errors = [];
if (!gridName) errors.push("그리드 이름은 필수입니다.");
if (errors.length > 0) {
    Matrix.Alert("파라미터 오류\n\n" + errors.join("\n"));
    return;
}

// 3. 비즈니스 로직 (함수 정의 → 실행)
function doSomething() {
    var grid = Matrix.getObject(gridName);
    // ... 로직 ...
}

// 4. 실행 또는 이벤트 등록
doSomething();                          // EVENT_YN = "N" 일 때
// 또는
grid.OnDataBindEnd = function() { ... }; // EVENT_YN = "Y" 일 때
```

### 4.3 이벤트 등록 모듈 패턴 (EVENT_YN = "Y")

이벤트를 등록하는 모듈은 실행 즉시 이벤트 핸들러를 바인딩하고, 이후 사용자 동작 시 실제 로직이 동작합니다.

```javascript
var controlName = arguments[0];
var grid = Matrix.getObject(controlName);
if (grid) {
    grid.OnDataBindEnd = function(_sender, _args) {
        // 데이터 바인딩 완료 시 실행할 로직
    };
}
```

### 4.4 사용 가능한 API

모듈 스크립트에서는 **클라이언트 스크립트 API**를 사용합니다:

- `Matrix.getObject(name)` - 컨트롤 참조
- `Matrix.Alert(msg)` / `Matrix.Confirm(msg, title, callback, type)` - 메시지
- `Matrix.CreateDataSet()` - DataSet 생성
- `Matrix.doRefresh(controlNames)` - 컨트롤 새로고침
- `Matrix.ExecutePlan(planName, params, callback)` - 실행계획 호출
- `Matrix.RunScriptEx(targets, serviceName, params, callback)` - 서버 스크립트 호출
- Grid: `GetDataSet()`, `GetFields()`, `GetRowCount()`, `SetDataSet()`, `Calculate()`, `Draw()`
- DataTable: `GetRowCount()`, `getData(rowIdx, fieldName)`, `setData(rowIdx, fieldName, value)`, `AppendRow()`, `AddColumn(name, isNumber)`
- Chart: `SetDataSet(ds)`, `Draw()`

> 자세한 API는 `/iaud-client-script` 스킬 또는 `types/aud/` 폴더의 TypeScript 인터페이스를 참조하세요.

---

## 5. 모듈 생성 절차

사용자가 모듈 생성을 요청하면 아래 순서로 진행합니다:

### Step 1: 요구사항 파악

사용자 요청에서 다음을 파악합니다:
- 모듈이 **무엇을 하는지** (기능)
- 어떤 **컨트롤**을 대상으로 하는지
- 사용자에게 **어떤 입력**을 받아야 하는지
- **즉시 실행**인지 **이벤트 등록**인지

### Step 2: 파라미터 설계

- 각 입력 항목에 적합한 `PARAM_TYPE` 선택
- 필수/선택 여부(`NULLABLE`) 결정
- 사용자 친화적인 설명(`PARAM_DESCRIPTION`) 작성
- 기본값(`DEFAULT_VALUE`) 설정

### Step 3: JavaScript 스크립트 작성

- 파라미터 수신 및 검증 코드
- 비즈니스 로직 함수
- 실행 코드 또는 이벤트 등록 코드

### Step 4: .module.json 파일 출력

- 모듈 제목으로 파일명 결정
- JSON 구조에 맞게 조립
- SCRIPT_TEXT를 JSON 문자열로 이스케이프
- `src/reports/[보고서폴더]/` 하위에 저장

---

## 6. 샘플 모듈

### 6.1 간단한 모듈: 컨트롤 값 초기화

```json
{
    "TYPE": "Single",
    "MTX_MODULE_INFO": [
        {
            "MODULE_CODE": "",
            "MODULE_SUBJECT": "컨트롤 값 초기화 하기",
            "MODULE_DESCRIPTION": "선택된 컨트롤들의 값을 초기화 합니다.\n값은 빈 값으로 설정합니다.",
            "SCRIPT_TEXT": "var controls = arguments[0].split(\",\");\nvar ctl;\nfor(var i=0;i<controls.length; i++){\n\tctl = Matrix.getObject(controls[i]);\n\tif(ctl){\n\t\ttry{\n\t\t\tif(typeof ctl.SetValue == \"function\"){\n\t\t\t\tctl.SetValue(\"\");\n\t\t\t}else{\n\t\t\t\tif(ctl.Checked=== true){\n\t\t\t\t\tctl.Checked = false;\n\t\t\t\t}\n\t\t\t}\n\t\t}catch(e){}\n\t}\n}",
            "USE_AUTHORITY": "0",
            "EDIT_AUTHORITY": "-1",
            "MODULE_TYPE": "",
            "RESULT_TYPE": "",
            "ORIGINAL_MODULE_CODE": "",
            "CREATE_USER": "",
            "MODIFY_USER": "",
            "MODULE_SEQ": "3",
            "WF_YN": "Y",
            "EVENT_YN": "Y",
            "ATTR1": "",
            "ATTR2": "",
            "ATTR3": "",
            "MTX_MODULE_PARAMS": [
                {
                    "MODULE_CODE": "",
                    "PARAM_SEQ": "1",
                    "PARAM_TYPE": "INP005",
                    "NULLABLE": "N",
                    "PARAM_DESCRIPTION": "대상 컨트롤 목록",
                    "DEFAULT_VALUE": "",
                    "ATTR1": "",
                    "ATTR2": "",
                    "ATTR3": ""
                }
            ]
        }
    ]
}
```

### 6.2 이벤트 등록 모듈: 체크박스 변경 시 조회

```json
{
    "TYPE": "Single",
    "MTX_MODULE_INFO": [
        {
            "MODULE_CODE": "",
            "MODULE_SUBJECT": "체크박스 상태 변경 시 특정 컨트롤 조회 하기",
            "MODULE_DESCRIPTION": "체크 박스 클릭 시 특정 컨트롤을 조회 합니다.",
            "SCRIPT_TEXT": "var controlNames = arguments[0];\nvar refreshCtls = arguments[1];\nvar controls = controlNames.split(\",\");\nvar chkBox, name;\nfor(var i=0; i<controls.length; i++){\n\tname = controls[i].trim();\n\tchkBox = Matrix.getObject(name);\n\tif(chkBox){\n\t\tchkBox.OnValueChange = function(s, e){\n\t\t\tMatrix.doRefresh(refreshCtls);\n\t\t};\n\t}\n}",
            "USE_AUTHORITY": "0",
            "EDIT_AUTHORITY": "-1",
            "MODULE_TYPE": "",
            "RESULT_TYPE": "",
            "ORIGINAL_MODULE_CODE": "",
            "CREATE_USER": "",
            "MODIFY_USER": "",
            "MODULE_SEQ": "3",
            "WF_YN": "",
            "EVENT_YN": "N",
            "ATTR1": "",
            "ATTR2": "",
            "ATTR3": "",
            "MTX_MODULE_PARAMS": [
                {
                    "MODULE_CODE": "",
                    "PARAM_SEQ": "1",
                    "PARAM_TYPE": "INP005",
                    "NULLABLE": "N",
                    "PARAM_DESCRIPTION": "체크 박스 컨트롤 목록",
                    "DEFAULT_VALUE": "",
                    "ATTR1": "",
                    "ATTR2": "",
                    "ATTR3": ""
                },
                {
                    "MODULE_CODE": "",
                    "PARAM_SEQ": "2",
                    "PARAM_TYPE": "INP005",
                    "NULLABLE": "N",
                    "PARAM_DESCRIPTION": "조회 대상 컨트롤",
                    "DEFAULT_VALUE": "",
                    "ATTR1": "",
                    "ATTR2": "",
                    "ATTR3": ""
                }
            ]
        }
    ]
}
```

### 6.3 복합 모듈: 데이터 그리드 필터·그룹핑 → 차트 바인딩

파라미터 6개, 입력 검증, 이벤트 등록을 포함하는 복합 모듈입니다.
실제 샘플은 `src/reports/DataTable 필터_그룹핑/차트 데이터 구성하기 (데이터 그리드 필터 및 그룹).module.json`을 참조하세요.

주요 특징:
- `INP003`(그리드 선택), `INP004`(차트 선택), `INP001`(텍스트), `INP999`(목록 선택) 활용
- arguments 수신 → validate → 이벤트 등록 → 비즈니스 함수 호출 패턴
- `grid.GetFields()`로 Caption → Name 변환 처리

---

## 7. SCRIPT_TEXT JSON 이스케이프 규칙

SCRIPT_TEXT는 JSON 문자열이므로 다음을 이스케이프해야 합니다:

| 원본 | 이스케이프 |
|------|-----------|
| 줄바꿈 | `\n` |
| 탭 | `\t` |
| 쌍따옴표 `"` | `\"` |
| 역슬래시 `\` | `\\` |

> **중요**: JavaScript 코드를 먼저 작성한 뒤, JSON 문자열로 변환하여 SCRIPT_TEXT에 넣습니다.

---

## 8. MCP 검증 도구 (validate_module)

모듈 JSON 파일을 작성한 후, MCP `validate_module` 도구를 호출하여 스키마 검증을 수행합니다.

### 사용 방법

```
MCP 도구: validate_module
파라미터:
  - path: 모듈 JSON 파일의 전체 경로
  또는
  - document: 모듈 JSON 문자열/객체
```

### 검증 항목

**스키마 검증 (에러)**:
- `TYPE`이 `"Single"`인지
- 필수 필드 존재 여부 (`MODULE_SUBJECT`, `SCRIPT_TEXT`, `USE_AUTHORITY`, `EDIT_AUTHORITY`, `MODULE_DESCRIPTION`, `MODULE_SEQ`, `EVENT_YN`)
- `MODULE_SUBJECT`, `SCRIPT_TEXT`가 빈 문자열이 아닌지
- `EVENT_YN`이 `"Y"` 또는 `"N"`인지
- `WF_YN`이 `"Y"`, `"N"`, 또는 빈 문자열인지
- `PARAM_TYPE`이 유효한 코드(INP001~INP999)인지
- `NULLABLE`이 `"Y"` 또는 `"N"`인지
- 알 수 없는 속성이 포함되지 않았는지

**비즈니스 로직 검증 (경고)**:
- `ATTR3="MTX"`인 경우 MATRIX 내장 모듈로 서버에서 가져오기 거부 경고
- `PARAM_TYPE="INP999"`인데 `ATTR1`(선택 목록)이 비어있는 경우 경고
- `PARAM_SEQ` 순번이 배열 순서와 일치하지 않는 경우 경고

### 모듈 생성 절차에 통합

Step 4(.module.json 파일 출력) 이후 반드시 `validate_module` 도구를 호출하여 검증합니다.
오류가 발견되면 수정 후 재검증합니다.

---

## 9. 체크리스트

모듈 생성 시 아래 항목을 확인합니다:

- [ ] 모듈 제목(`MODULE_SUBJECT`)이 기능을 명확히 설명하는가?
- [ ] `MODULE_DESCRIPTION`에 사용 방법과 주의사항이 있는가?
- [ ] 파라미터 타입(`PARAM_TYPE`)이 적절한가? (그리드→INP003, 컨트롤→INP004/005 등)
- [ ] 필수 파라미터의 `NULLABLE`이 `"N"`인가?
- [ ] 스크립트에서 파라미터 검증(validate)을 하는가?
- [ ] 컨트롤을 찾지 못했을 때 `Matrix.Alert`로 안내하는가?
- [ ] `EVENT_YN`이 올바르게 설정되었는가?
- [ ] SCRIPT_TEXT가 순수 JavaScript인가? (var 사용, 타입 어노테이션 없음)
- [ ] SCRIPT_TEXT 내의 따옴표, 줄바꿈이 올바르게 이스케이프되었는가?
- [ ] MCP `validate_module` 도구로 검증을 통과했는가?
