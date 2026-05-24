# 20-build-domain

Status: ACTIVE  
AppliesTo: v10

---

## 0. 목적

- 특정 게임이 아니라 **도메인/프로토콜이 동적으로 바뀌는 빌드**를 표준화한다.
- `DomainKey`와 `ProtocolGroup`이 추가될 때마다 빌드 산출물이 자동으로 늘어나는 구조를 정의한다.
- 빌드 입력/설정/산출물 원칙을 명확히 하여 빌더 구현과의 불일치를 제거한다.

---

## 1. 적용 범위

### 적용 대상

- `framework-ts/tools/builder/build.js` 기반 빌드 전반
- **입력:** `{buildInputJson}` (예: `input/input_common.json`)
- **설정:** `{configJson}` (예: `input/config.json`)

### 비대상

- 런타임 실행 로직
- 에러/로그 표준 (→ `skills/devian-tools/21-build-error-reporting/SKILL.md`)

---

## 2. 용어

| 용어 | 정의 |
|------|------|
| **DomainKey** | 도메인 식별자 (예: `Game`, `Common`) |
| **ProtocolGroup** | 프로토콜 그룹 식별자 (예: `Game`) |
| **buildInputJsonDir** | buildInputJson 파일이 위치한 디렉토리. 상대경로 해석의 기준 |
| **{tempDir}** | 빌드 중간 산출물이 생성되는 staging 디렉토리 |
| **{configJson}** | 빌드 설정 파일 (출력 경로 등 정의) |

---

## 3. 빌드 실행

### 스크립트 실행

```bash
bash input/build.sh <buildInputJson>
```

### 직접 실행

```bash
node framework-ts/tools/builder/build.js <buildInputJson>
```

- `<buildInputJson>`은 빌드 입력 JSON 파일 경로 (예: `input/input_common.json`)
- 빌더는 `buildInputJson`을 읽고, 그 안의 `configPath`로 설정 파일을 로드한다.

---

## 4. 입력 파일 스펙 (build json)

### 최상위 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `version` | string | 빌드 스펙 버전 |
| `configPath` | string | 설정 파일 경로 (buildInputJsonDir 기준 상대경로) |
| `tempDir` | string | staging 디렉토리 경로 |
| `domains` | object | 도메인 정의 (map 형태) |
| `protocols` | array | 프로토콜 정의 (배열 형태) |

### domains (map)

```json
{
  "DomainKey": {
    "contractDir": "Domains/Game/contracts",
    "contractFiles": ["*.json"],
    "tableDir": "Domains/Game/tables",
    "tableFiles": ["*.xlsx"]
  }
}
```

- key는 `DomainKey` (예: `"Game"`, `"Common"`)
- `contractDir`, `tableDir`는 buildInputJsonDir 기준 상대경로

### protocols (array)

```json
[
  {
    "group": "Game",
    "protocolDir": "Protocols/Game",
    "protocolFiles": ["C2Game.json", "Game2C.json"]
  }
]
```

- `group`은 `ProtocolGroup` 식별자

---

## 5. 설정 파일 스펙 (config.json)

### csConfig (C# 출력)

| 필드 | 필수 | 설명 |
|------|------|------|
| `moduleDir` | ✓ | C# 모듈 출력 디렉토리 |
| `generateDir` | 옵션 | C# 생성 코드 디렉토리 (미지정 시 moduleDir 사용) |

### tsConfig (TypeScript 출력)

| 필드 | 필수 | 설명 |
|------|------|------|
| `moduleDir` | ✓ | TS 모듈 출력 디렉토리 |
| `generateDir` | 옵션 | TS 생성 코드 디렉토리 (미지정 시 moduleDir 사용) |

### upmConfig (UPM 패키지)

| 필드 | 필수 | 설명 |
|------|------|------|
| `sourceDir` | ✓ | UPM 소스 디렉토리 |
| `packageDir` | ✓ | UPM 패키지 출력 디렉토리 |

### tableConfig (데이터 출력)

| 필드 | 필수 | 설명 |
|------|------|------|
| `tableDirs` | ✓ | 테이블 출력 디렉토리 배열 |
| `stringDirs` | ✓ | String 테이블 출력 디렉토리 배열 |
| `soundDirs` | ✓ | 사운드 데이터 출력 디렉토리 배열 |

> **CRITICAL:** config.json에 `dataConfig` 키가 존재하면 빌드가 **즉시 FAIL**한다 (deprecated).
> tableConfig의 각 Dir 배열에 대해 해당 데이터 유형이 출력된다.

### samplePackages

| 필드 | 타입 | 설명 |
|------|------|------|
| `samplePackages` | string[] | 샘플 패키지 목록 (com.devian.samples만 허용) |

### Hard Rule: samplePackages cannot contain libraries/domains

- `samplePackages`에는 `com.devian.samples`만 포함할 수 있다.
- `com.devian.foundation` 또는 `com.devian.domain.*` 가 들어가면 FAIL (Generated 덮어쓰기/삭제 위험).
- `staticUpmPackages` 키는 금지이며 존재 시 FAIL.

---

## 6. 산출물 규칙

### 원칙

- **도메인/프로토콜 추가에 따라 출력이 늘어남 (동적)**
- 개별 도메인 고정표 대신 **템플릿 기반**으로 산출물 경로가 결정됨
- **정확한 디렉토리/파일 배치는 빌더 구현이 SSOT**

### C# Domain 템플릿

```
{csConfig.generateDir}/Devian.Domain.{DomainKey}/
```

### TypeScript Domain 템플릿

```
{tsConfig.generateDir}/devian-domain-{domainKeyLower}/
```

### UPM Domain 템플릿

```
{upmConfig.sourceDir}/com.devian.domain.{domainKeyLower}/
```

### Protocol 템플릿 (동일 원칙)

```
C#:  {csConfig.generateDir}/Devian.Protocol.{ProtocolGroup}/
TS:  {tsConfig.generateDir}/devian-protocol-{protocolGroupLower}/
UPM: {upmConfig.sourceDir}/com.devian.protocol.{protocolGroupLower}/
```

### 데이터 산출물

**일반 테이블 (tableConfig.tableDirs):**
```
{tableDir}/ndjson/{TableName}.json
{tableDir}/pb64/{TableName}.asset
```

**String Table (tableConfig.stringDirs):**
```
{stringDir}/ndjson/{Language}/{TableName}.json
{stringDir}/pb64/{Language}/{TableName}.asset
```

**Sound 데이터 (tableConfig.soundDirs):**
```
{soundDir}/ndjson/{TableName}.json
{soundDir}/pb64/{TableName}.asset
```

- 복수 타겟 가능 (각 Dir 배열의 모든 경로에 복사)
- **도메인 폴더 미사용**: 최종 경로에 `{DomainKey}` 폴더 없음
- **동일 파일명 충돌 시 빌드 FAIL** (조용한 덮어쓰기 금지)

---

## 7. Hard Rules

### Staging 규칙

- `{tempDir}`는 **staging 전용**이며 **커밋 금지**
- 빌드 완료 후 staging에서 최종 위치로 복사됨

### 필수 필드 FAIL

| 조건 | 결과 |
|------|------|
| `tableConfig.tableDirs` 누락 | **즉시 FAIL** |
| `tableConfig.stringDirs` 누락 | **즉시 FAIL** |
| `tableConfig.soundDirs` 누락 | **즉시 FAIL** |

### Forbidden 필드 FAIL

아래 필드가 존재하면 **즉시 FAIL** 처리됨:

| 위치 | Forbidden 필드 |
|------|-----------------|
| `config.json` | `dataConfig` (deprecated) |
| `domains[*]` | `csTargetDir` |
| `domains[*]` | `tsTargetDir` |
| `domains[*]` | `dataTargetDirs` |
| `protocols[*]` | `csTargetDir` |
| `protocols[*]` | `tsTargetDir` |
| `protocols[*]` | `upmName` |
| `protocols[*]` | `upmTargetDir` |

> **총 8개** 금지 필드. 하나라도 발견되면 빌드가 중단된다.

---

## 8. 예시

Game 도메인/프로토콜 예제의 상세 설명은 별도 스킬 문서를 참조한다:

> **예제 정책:** `skills/devian-examples/01-policy/SKILL.md`

예제 입력 위치:
- `devian/input/Domains/Game/contracts/**`
- `devian/input/Domains/Game/tables/**`
- `devian/input/Protocols/Game/**`

---

## Verification Checklist

1) `input/config.json`에 `samplePackages: ["com.devian.samples"]`만 존재한다.
2) `input/config.json`에 `staticUpmPackages` 키가 존재하지 않는다 (금지 필드).
3) 빌드 후 `framework-cs/upm/com.devian.domain.sound/Runtime/Generated/Sound.g.cs` 가 존재한다.
4) 빌드 후 `framework-cs/apps/UnityExample/Packages/com.devian.domain.sound/Runtime/Generated/Sound.g.cs` 가 존재한다.
5) samplePackages 처리 이후에도 (3), (4)가 삭제되지 않는다.
6) Unity 컴파일 에러 `CS0246 (SOUND/VOICE not found)` 가 발생하지 않는다.

## Verification Checklist (Dependencies)

- `framework-cs/upm/**/package.json`에서 `com.devian.core`, `com.devian.unity` dependency가 0개여야 한다.
- `framework-cs/apps/UnityExample/Packages/**/package.json`에서도 위 dependency가 0개여야 한다.

---

## 9. Reference

### 빌더 (SSOT)

- `framework-ts/tools/builder/build.js`

### 입력/설정 예시

- `input/input_common.json` — 빌드 입력 예시
- `input/config.json` — 설정 파일 예시

### 관련 스킬

| 스킬 | 설명 |
|------|------|
| `skills/devian-core/03-ssot/SKILL.md` | 전체 SSOT 정책 |
| `skills/devian-tools/21-build-error-reporting/SKILL.md` | 빌드 에러/로그 표준 |
| `skills/devian-examples/01-policy/SKILL.md` | Game 예제 정책 |
| `skills/devian-unity/02-unity-bundles/SKILL.md` | UPM 번들/복사 흐름 |
