# 21-build-error-reporting

Status: ACTIVE  
AppliesTo: v10

---

## 0. 목적

- 빌드/생성 파이프라인에서 실패 시 **원인 파악 시간을 최소화**한다.
- 사람이 읽는 **1줄 요약** + 기계가 읽는 **NDJSON 1줄**을 항상 동일 규격으로 출력한다.
- 동일 규격의 로그 파일을 `{tempDir}/log`에 남겨 CI/로컬에서 재현 및 분석이 가능하게 한다.

---

## 1. 적용 범위

### 적용 대상

- `framework-ts/tools/builder` (및 CLI 엔트리)
- 입력 JSON 로딩/검증
- proto-json 파싱
- 테이블 변환
- 코드 생성 단계

### 비대상 (명시)

- 런타임(게임 실행 중) 로깅 정책은 별도 스킬에서 다룸

---

## 2. 용어 정의

| 용어 | 정의 |
|------|------|
| **Build Error** | 빌드 중단을 유발하는 오류 (ExitCode != 0) |
| **Report Line** | 콘솔에 출력되는 2줄 (요약 1줄 + NDJSON 1줄) |
| **Log Record** | 로그 파일에 쓰이는 NDJSON 한 줄 레코드 |
| **KIND** | 오류가 발생한 입력/단계를 나타내는 분류값 |
| **jsonPath** | 입력 JSON 내부 위치를 나타내는 JSONPath (`$` 기준) |

---

## 3. 출력 규격

### 3.1 콘솔 출력 (표준) — 항상 2줄

#### 사람용 1줄 요약

```
[ERROR] <CODE> <KIND> <LOC> - <MESSAGE>
```

- `<LOC>`는 기본적으로 `<file><jsonPath>` 형태
  - 예: `devian/{buildInputJson}$.domains[1].name` (예: `devian/input/input_common.json$.domains[1].name`)
- `<MESSAGE>`는 1줄, **줄바꿈 금지**

#### 기계용 NDJSON 1줄

- JSON stringify 결과 1줄 (개행 금지)
- 레코드 스펙은 4장 참조

### 3.2 표준 출력 순서 규칙

1. **요약 1줄 → NDJSON 1줄** 순서 고정
2. 동일 에러에 대해 **중복 출력 금지** (최상위 catch에서 1회만)

### 3.3 경고(warn) 출력 규격 (선택)

- `[WARN]` + 동일 포맷
- warn은 ExitCode를 바꾸지 않음 (기본)

---

## 4. NDJSON 레코드 스펙

### 4.1 필수 필드

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `ts` | string | ISO8601 timestamp | `"2026-01-25T12:34:56.789+09:00"` |
| `level` | string | `"error"` \| `"warn"` \| `"info"` | `"error"` |
| `code` | string | 에러 코드 문자열 | `"E_JSON_PARSE"` |
| `kind` | string | 분류 문자열 | `"CONFIG_JSON"` |
| `message` | string | 한 줄 메시지 (개행 금지) | `"Invalid JSON syntax"` |
| `file` | string | 입력 파일 경로 (레포 기준 상대경로) | `"devian/{buildInputJson}"` (예: `"devian/input/input_common.json"`) |
| `jsonPath` | string | JSONPath 문자열 (없으면 `"$"`) | `"$.domains[1].name"` |

### 4.2 권장 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `hint` | string | 해결 힌트 1줄 |
| `link` | string | 관련 SSOT 문서 경로 |
| `context` | object | 추가 컨텍스트 (가능한 값만 포함) |
| `cause` | object | 하위 예외 요약 (`name`, `message` — 둘 다 1줄) |

#### context 객체 예시 필드

- `domainKey`
- `domainType` (`"DATA"` | `"PROTOCOL"`)
- `linkName`
- `protocolName`
- `sheetKey`
- `tableName`
- `target`

### 4.3 금지

- NDJSON 레코드 내에 **멀티라인 문자열 금지**
- 스택 트레이스는 레코드 필드로 넣지 말고 5장의 "로그 파일 분리 규칙"에 따라 별도 기록

---

## 5. 로그 파일 규칙

### 5.1 로그 디렉토리 (고정)

```
{tempDir}/log/
```

### 5.2 파일명 규칙

빌드 실행 1회당 "런(run)" 단위로 파일 분리:

```
build-{yyyyMMdd-HHmmss}-{pid}.ndjson
```

예: `build-20260125-103355-18432.ndjson`

### 5.3 기록 규칙

1. 콘솔에 출력한 NDJSON 레코드는 **동일하게 파일에도 append**
2. `level=info`로 **"build start / build end / summary"** 레코드도 남기는 것을 권장
   - 최소: start/end 2개

### 5.4 선택: 상세 로그 (스택/원문) 분리 파일

스택 트레이스/원문 예외를 남기고 싶으면:

```
{tempDir}/log/build-{...}.detail.log
```

- detail 파일은 **텍스트 자유 포맷 허용** (멀티라인 OK)

---

## 6. 에러 코드 체계

### 6.1 네이밍 규칙

- `E_` 접두어 고정, **대문자 스네이크**
- 가능한 "원인 기반"으로 분리 (단계 기반 분리 과도 금지)

### 6.2 최소 필수 코드 (초기 세트)

| 코드 | 설명 |
|------|------|
| `E_JSON_READ` | JSON 파일 읽기 실패 |
| `E_JSON_PARSE` | JSON 파싱 실패 |
| `E_JSON_SCHEMA` | JSON 스키마 검증 실패 |
| `E_DUPLICATE_KEY` | 중복 키 |
| `E_INVALID_VALUE` | 잘못된 값 |
| `E_PATH_NOT_FOUND` | 경로/파일 없음 |
| `E_NAMESPACE_MISMATCH` | 네임스페이스 불일치 |
| `E_PRIMARYKEY_EMPTY` | primaryKey 필수인데 없음 |

### 6.3 KIND enum (초기 세트)

| KIND | 설명 |
|------|------|
| `CONFIG_JSON` | 설정 JSON (`{buildInputJson}` 등) |
| `PROTO_JSON` | 프로토콜 JSON |
| `TABLE_JSON` | 테이블 JSON |
| `XLSX` | 엑셀 파일 |
| `CODEGEN_CS` | C# 코드 생성 |
| `CODEGEN_TS` | TypeScript 코드 생성 |
| `UPM_PACK` | UPM 패키지 처리 |
| `COPY_STAGE` | 파일 복사/스테이징 |

---

## 7. 실패 처리 규칙 (Exit / FAIL 조건)

### 7.1 ExitCode 정책

- `level=error` 발생 시 기본 **ExitCode = 1**
- `warn`은 기본 ExitCode에 영향 없음 (단, 옵션으로 `--warn-as-error` 가능)

### 7.2 FAIL 조건 (강제)

빌드 중단이 발생한 경우, 아래 중 하나라도 위반하면 FAIL:

| 조건 | 설명 |
|------|------|
| 콘솔 표준 2줄 | 출력되지 않으면 FAIL |
| 로그 파일 | `{tempDir}/log/*.ndjson` 생성되지 않으면 FAIL |
| 필수 필드 | `code`, `kind`, `file`, `jsonPath`, `message` 중 하나라도 누락이면 FAIL |

---

## 8. DoD (Definition of Done)

- [ ] 입력 JSON 파싱/검증 실패 시 **표준 2줄 출력** + `{tempDir}/log`에 NDJSON 로그 생성
- [ ] 최소 3가지 케이스에서 `jsonPath`가 의미 있게 기록됨:
  - JSON parse error (가능하면 line/col은 context로)
  - required field missing
  - duplicate key
- [ ] CI/스크립트가 NDJSON 한 줄을 파싱해 `code`, `file`, `jsonPath`를 안정적으로 읽을 수 있음
- [ ] 동일 에러가 **중복 출력되지 않음** (최상위 1회)

---

## 9. 구현 지침 (비정책 섹션)

> **Note:** 이 섹션은 구현 가이드이며, 정책 강제 사항이 아님

- **최상위 CLI에서만** 출력/파일 기록을 담당 (중간 레이어는 throw만)
- 에러 객체에 구조화 정보 (`devianError` 같은 payload)를 붙이는 방식 권장
- `jsonPath`는 가능하면 생성 (없으면 `$`)
- `link`는 가능한 한 "정본 스킬"로 연결

### 예시: 로그 요약 레코드 (선택)

마지막에 `level=info`로 1줄 요약도 남기면 CI 통계에 유용:

```json
{"level":"info","code":"I_BUILD_SUMMARY","errors":1,"warnings":0,"durationMs":1234}
```

---

## 10. Reference

### 이 스킬

- `skills/devian-tools/21-build-error-reporting/SKILL.md`

### 빌드 관련

- `skills/devian-tools/20-build-domain/SKILL.md`
- `skills/devian-core/03-ssot/SKILL.md`

### 입력 규약 (연결 후보)

- `skills/devian-unity/20-packages/com.devian.domain.template/SKILL.md` — 도메인 패키지 생성 규칙
- `skills/devian-unity-samples/01-policy/SKILL.md`
- `skills/devian-examples/01-policy/SKILL.md`
