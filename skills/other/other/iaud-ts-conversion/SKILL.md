---
name: iaud-ts-conversion
description: i-AUD 클라이언트 스크립트 TypeScript 전환 가이드. .script.ts 파일의 var→let/const 변환, 타입 어노테이션, MCP 기반 컨트롤 타입 조회 등을 안내합니다. "TypeScript 전환", "var 변환", "타입 전환", "스크립트 변환", "TS 마이그레이션" 등을 요청할 때 사용하세요.
---

# i-AUD 클라이언트 스크립트 TypeScript 전환 가이드

> `.script.ts` 파일을 JavaScript 스타일에서 TypeScript로 전환할 때 사용하는 작업 가이드입니다.

## 1. 전환 대상 및 범위

### 대상 파일
- `5.reportSources/src/reports/{프로그램명}/{프로그램명}.script.ts`
- 원래 `.js`였으나 `.ts`로 확장자만 변경된 상태
- `tsconfig.json`의 `strict: false` 환경

### 전환 항목
| 항목 | 변환 전 | 변환 후 |
|------|---------|---------|
| 변수 선언 | `var x = ...` | `const x = ...` (재할당 없음) / `let x = ...` (재할당 있음) |
| for 루프 | `for(var i=0; ...)` | `for(let i=0; ...)` |
| for-in 루프 | `for(var k in obj)` | `for(const k in obj)` |
| enum-like 객체 | `var enMode = { A:0, B:1 }` | `const enMode = { A:0, B:1 } as const` |
| 함수 선언 | `var fn = function(){` | `const fn = function(){` |
| 이벤트 핸들러 파라미터 | `function(s, e){` | `function(s: any, e: any){` |
| 콜백 파라미터 | `function(ret){` | `function(ret: any){` |

### 전환하지 않는 항목
- **Constructor 함수 → class 변환 금지**: `var TabManager = function(){ this.xxx = ... }` 같은 생성자 패턴은 `const`로만 변경하고, class로 변환하지 않음 (런타임 동작 변경 위험)
- **주석 안의 var**: 변경하지 않음
- **기존 타입 에러 수정 금지**: 변환 과정에서 기존 코드의 버그나 타입 에러를 수정하지 않음

---

## 2. 컨트롤 변수 타입 어노테이션 규칙

### 2.1 컨트롤 변수는 MTSD 파일 기반으로 정확한 타입 지정

MTSD 파일(같은 폴더의 `.mtsd` 파일)에서 각 컨트롤의 `Type` 프로퍼티를 확인하여 정확한 타입을 지정한다.

**MTSD Type → TypeScript 타입 매핑표:**

| MTSD Type | TypeScript Import | 비고 |
|-----------|-------------------|------|
| `Button` | `Button` | `@AUD_CLIENT/control/Button` |
| `Label` | `Label` | `@AUD_CLIENT/control/Label` |
| `TextBox` | `TextBox` | `@AUD_CLIENT/control/TextBox` |
| `NumberBox` | `NumberBox` | `@AUD_CLIENT/control/NumberBox` |
| `CheckBox` | `CheckBox` | `@AUD_CLIENT/control/CheckBox` |
| `RadioButton` | `RadioButton` | `@AUD_CLIENT/control/RadioButton` |
| `ComboBox` | `ComboBox` | `@AUD_CLIENT/control/ComboBox` |
| `MultiComboBox` | `MultiComboBox` | `@AUD_CLIENT/control/MultiComboBox` |
| `RichTextBox` | `RichTextBox` | `@AUD_CLIENT/control/RichTextBox` |
| `MaskTextBox` | `MaskTextBox` | `@AUD_CLIENT/control/MaskTextBox` |
| `Image` | `Image` | `@AUD_CLIENT/control/Image` |
| `Group` | `Group` | `@AUD_CLIENT/control/Group` |
| `DataGrid` | `DataGrid` | `@AUD_CLIENT/control/DataGrid` |
| `TreeGrid` | `TreeGrid` | `@AUD_CLIENT/control/TreeGrid` |
| `Chart` | `Chart` | `@AUD_CLIENT/control/Chart` |
| `PieChart` | `PieChart` | `@AUD_CLIENT/control/PieChart` |
| `ScatterChart` | `ScatterChart` | `@AUD_CLIENT/control/ScatterChart` |
| `PolygonChart` | `PolygonChart` | `@AUD_CLIENT/control/PolygonChart` |
| `OlapGrid` | `OlapGrid` | `@AUD_CLIENT/control/OlapGrid` |
| `MXGrid` | `iGrid` | `@AUD_CLIENT/control/iGrid` (예외: 타입명 다름) |
| `Calendar` | `Calendar` | `@AUD_CLIENT/control/Calendar` |
| `CalendarFromTo` | `CalendarFromTo` | `@AUD_CLIENT/control/CalendarFromTo` |
| `CalendarYM` | `CalendarYM` | `@AUD_CLIENT/control/CalendarYM` |
| `CalendarYMFromTo` | `CalendarYMFromTo` | `@AUD_CLIENT/control/CalendarYMFromTo` |
| `CalendarWeekly` | `CalendarWeekly` | `@AUD_CLIENT/control/CalendarWeekly` |
| `CalendarWeeklyFromTo` | `CalendarWeeklyFromTo` | `@AUD_CLIENT/control/CalendarWeeklyFromTo` |
| `CalendarYear` | `CalendarYear` | `@AUD_CLIENT/control/CalendarYear` |
| `CalendarYearFromTo` | `CalendarYearFromTo` | `@AUD_CLIENT/control/CalendarYearFromTo` |
| `ColorPicker` | `ColorPicker` | `@AUD_CLIENT/control/ColorPicker` |
| `Slider` | `Slider` | `@AUD_CLIENT/control/Slider` |
| `PickList` | `PickList` | `@AUD_CLIENT/control/PickList` |
| `Tree` | `Tree` | `@AUD_CLIENT/control/Tree` |
| `Slicer` | `Slicer` | `@AUD_CLIENT/control/Slicer` |
| `FileUploadButton` | `FileUploadButton` | `@AUD_CLIENT/control/FileUploadButton` |
| `Browser` | `Browser` | `@AUD_CLIENT/control/Browser` |
| `UserComponent` | `UserComponent` | `@AUD_CLIENT/control/UserComponent` |
| `AddIn` | `AddIn` | `@AUD_CLIENT/control/AddIn` |

**타입 확인 방법:**

1. **MCP 도구 사용 (권장)**: `get_control_info` 도구로 MTSD 파일에서 컨트롤 목록과 타입을 조회
2. **직접 확인**: 같은 폴더의 `.mtsd` 파일을 읽어 Elements 트리에서 `Name`과 `Type` 확인

**적용 예시:**
```typescript
// MTSD에서 확인: BTN_SAVE → Type: "Button", LBL_LOADING → Type: "Label"
let BTN_SAVE: Button | null = null;
let LBL_LOADING: Label | null = null;
let GRP_LIST: Group | null = null;
let GRID_MODULE_LIST: DataGrid | null = null;

// import도 함께 추가
import { Button } from "@AUD_CLIENT/control/Button";
import { Label } from "@AUD_CLIENT/control/Label";
```

**주의: 타입 에러가 발생하는 경우**
- 특정 컨트롤 타입에서 프로퍼티 접근 에러가 나면 해당 변수만 `any`로 fallback
- 예: `Matrix.getObject()` 반환 후 타입별 메서드 호출에서 에러 시 `as any` 유지

### 2.2 Matrix.getObject() 호출의 캐스트

컨트롤 변수에 정확한 타입이 지정된 경우, `Matrix.getObject()`의 캐스트도 해당 타입으로 맞춘다:
```typescript
// 타입이 지정된 경우
BTN_SAVE = Matrix.getObject("BTN_SAVE") as Button;
GRID_MODULE_LIST = Matrix.getObject("GRID_MODULE_LIST") as DataGrid;

// 타입 정의가 불완전하여 에러 발생 시 any로 fallback
SOME_CONTROL = Matrix.getObject("SOME_CONTROL") as any;
```

### 2.3 parent 접근은 `(parent as any)` 캐스트
```typescript
// parent의 커스텀 프로퍼티 접근 시
new (parent as any).NamedDictionary();
```

### 2.4 프레임워크 전역 변수 선언
파일 상단(import 직후)에 프레임워크가 런타임에 주입하는 전역 변수를 선언해야 함:
```typescript
let Matrix: Matrix;
let _AUD_ = parent["_AUD_"];
let _$: any = parent["_$"];
let _viewer_: any;
let myViewerId: any;
```

### 2.5 동적 프로퍼티 추가되는 객체는 `: any` 타입
```typescript
// 프로퍼티가 나중에 동적으로 추가되는 경우
const enRequestAction: any = { ... };
```

---

## 3. 주의사항 및 함정

### 3.1 Temporal Dead Zone (TDZ)
`var`는 호이스팅되지만 `let`/`const`는 안 됨. 선언 전에 참조하는 코드가 있으면 선언 위치를 위로 이동해야 함.
```typescript
// 에러: gvWindowSize가 OnEndDrag 안에서 참조되는데, 아래에 선언됨
const OnEndDrag = function() { gvWindowSize.Width; };
let gvWindowSize: any = {};  // ← 이 선언을 OnEndDrag 위로 이동

// 수정 후:
let gvWindowSize: any = {};
const OnEndDrag = function() { gvWindowSize.Width; };  // OK
```

### 3.2 `var` 재선언 → `let` 중복 선언 에러
`var`는 같은 스코프에서 재선언 가능하지만, `let`은 불가:
```typescript
// 원본 (동작함):
var x = 1;
var x = 2;

// let으로 변환 시 에러:
let x = 1;
let x = 2;  // TS2451: Cannot redeclare block-scoped variable

// 해결: 두 번째 선언을 할당으로 변경
let x = 1;
x = 2;
```

### 3.3 파라미터를 `var`로 재선언하는 패턴
```typescript
// 원본:
function handler(e) {
    if (e == null) var e = window.event;  // var로 재선언
}

// let으로 변환하면 에러 (파라미터 재선언 불가):
function handler(e: any) {
    if (e == null) e = window.event;  // var 제거, 단순 할당으로 변경
}
```

### 3.4 암시적 전역 변수 (Implicit Globals)
원본 JS에서 선언 없이 사용된 변수는 `let` 선언을 추가해야 함:
```typescript
// 원본 JS (암시적 전역):
for (param in list) { ... }  // param 미선언

// TypeScript:
let param: any;
for (param in list) { ... }
```

### 3.5 `const`로 변경 후 재할당 발견
`const`로 변경했는데 아래에서 재할당하는 코드가 있으면 `let`으로 변경:
```typescript
// 파일 전체를 확인하고 재할당 여부를 판단해야 함
let reportNameLabel: any = controls[0];  // 아래에서 재할당됨
```

### 3.6 파라미터명과 본문 변수명 불일치
원본 JS에서 파라미터명과 함수 본문에서 사용하는 변수명이 다른 경우 주의:
```typescript
// 원본: 파라미터는 control이지만 본문은 ctrl 사용 (기존 버그)
var fn = function(control) { ctrl.Width = 100; }

// TypeScript: 그대로 유지 (기존 동작 보존)
const fn = function(control: any) { ctrl.Width = 100; }
```

---

## 4. 작업 순서 (권장)

### Phase 0: 컨트롤 타입 확인
1. 같은 폴더의 `.mtsd` 파일을 읽거나 MCP `get_control_info` 도구를 호출
2. 컨트롤 Name → Type 매핑 목록 확보
3. 필요한 import 목록 정리

### Phase 1: 파일 구조 파악
1. 파일을 읽고 전체 구조를 파악 (함수 경계, 중첩 깊이)
2. `grep`으로 `var ` 선언 총 개수 확인
3. 큰 함수 블록 단위로 작업 구간 나누기

### Phase 2: 최상위 변수 영역
- 파일 상단의 컨트롤 변수 선언: `var X = null` → `let X: ControlType | null = null`
- MTSD에서 확인한 타입으로 정확히 지정
- 필요한 import 추가
- 프레임워크 전역 변수 선언 추가
- enum-like 객체에 `as const` 적용

### Phase 3: 함수 선언 영역
- `var fn = function(...)` → `const fn = function(...)`
- 이벤트 핸들러 파라미터에 `: any` 추가

### Phase 4: 함수 내부 변수
- 구간별로 나누어 `var` → `let`/`const` 변환
- `for(var` → `for(let` 변환
- 암시적 전역 변수 발견 시 `let` 선언 추가
- `Matrix.getObject()` 호출에 MTSD 기반 타입 캐스트 적용

### Phase 5: 검증
1. `grep "^\s*var "` 으로 남은 var 확인 (주석 제외)
2. `grep "for\s*(\s*var "` 으로 남은 for-var 확인
3. `tsc --noEmit` 으로 새로운 에러가 없는지 확인
4. 기존 에러(pre-existing)와 새로 발생한 에러를 구분
5. 컨트롤 타입 에러 발생 시 해당 변수만 `any`로 fallback

---

## 5. 검증 명령어

```bash
# 남은 var 확인 (주석 제외)
grep -n "^\s*var " {파일경로} | grep -v "^\s*//"

# for-var 확인 (주석 제외)
grep -n "for\s*(\s*var " {파일경로} | grep -v "^\s*//"

# TypeScript 빌드 검증
cd 5.reportSources && npx tsc --noEmit --project tsconfig.json 2>&1 | grep "{파일명}"

# 변환으로 인한 에러만 필터링 (재선언, TDZ 관련)
npx tsc --noEmit 2>&1 | grep "{파일명}" | grep -E "2451|2448|2304|Cannot redeclare"
```

---

## 6. 실전 예시 (AUD_MODULE.script.ts 전환 결과)

### 변환 통계
- 파일 크기: 3648줄
- 변환된 `var` 선언: 약 300개+
- 작업 시간: 7개 Phase로 분할 작업
- 새로 발생한 TS 에러: 0개

### 주요 패턴별 처리 사례

| 패턴 | 처리 방법 |
|------|----------|
| `var LBL_LOADING = null` | `let LBL_LOADING: Label \| null = null` (MTSD 타입 기반) |
| `var BTN_SAVE = null` | `let BTN_SAVE: Button \| null = null` (MTSD 타입 기반) |
| `var doRefresh = function(){` | `const doRefresh = function(){` |
| `var OnClick = function(s, e){` | `const OnClick = function(s: any, e: any){` |
| `var enMode = { New:0 }` | `const enMode = { New:0 } as const` |
| `var TabManager = function(){` | `const TabManager = function(){` (class 변환 X) |
| `for(var i=0; ...)` | `for(let i=0; ...)` |
| `for(var k in obj)` | `for(const k in obj)` |
| `Matrix.getObject("BTN_SAVE")` | `Matrix.getObject("BTN_SAVE") as Button` |
| `parent.CustomClass()` | `(parent as any).CustomClass()` |
| `if(e==null) var e = window.event` | `if(e==null) e = window.event` |

---

## 7. Claude에게 작업 요청 시 프롬프트 템플릿

```
{파일경로}는 원래 JS 소스였어. TypeScript 전환을 처리해줘.

전환 범위:
1. 모든 var → let/const 변환
2. MTSD 파일에서 컨트롤 타입을 확인하여 정확한 타입 어노테이션 적용
3. Matrix.getObject() 호출에 MTSD 기반 타입 캐스트
4. enum-like 객체에 as const
5. 이벤트 핸들러/콜백 파라미터에 any 타입
6. Constructor 함수는 class 변환 하지 않기
7. 타입 에러 발생 시 해당 변수만 any로 fallback

검증: 변환 완료 후 tsc --noEmit 으로 새로운 에러가 없는지 확인
```
