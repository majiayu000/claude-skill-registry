---
name: 03-ssot
description: 'ParentSSOT: skills/devian-core/03-ssot/SKILL.md'
---

# 03-ssot — Data

Status: ACTIVE
AppliesTo: v10
ParentSSOT: skills/devian-core/03-ssot/SKILL.md

---

## Scope

이 문서는 **DATA 도메인(테이블, Contract, 스토리지)** 관련 SSOT를 정의한다.

**중복 금지:** 공통 용어/플레이스홀더/입력 분리/머지 규칙은 [Root SSOT](../../devian-core/03-ssot/SKILL.md)가 정본이며, 이 문서는 재정의하지 않는다.

---

## tableConfig 설정

DATA 도메인의 데이터 출력 타겟은 전역 `tableConfig`로 설정한다.

```json
"tableConfig": {
  "tableDirs": ["../framework-cs/apps/UnityExample/Assets/Bundles/Tables"],
  "stringDirs": ["../framework-cs/apps/UnityExample/Assets/Bundles/Strings"],
  "soundDirs": ["../framework-cs/apps/UnityExample/Assets/Bundles/Sounds"]
}
```

| 필드 | 역할 | 예시 |
|------|------|------|
| `tableDirs` | 테이블 출력 디렉토리 목록 | `["...Assets/Bundles/Tables"]` |
| `stringDirs` | String 테이블 출력 디렉토리 목록 | `["...Assets/Bundles/Strings"]` |
| `soundDirs` | Sound 데이터 출력 디렉토리 목록 | `["...Assets/Bundles/Sounds"]` |

**필수 규칙:**
- `tableConfig`의 각 Dir 배열은 필수 (빈 배열 허용)
- 빌더가 각 Dir에 대해 `ndjson/` 및 `pb64/` 하위 디렉토리를 생성
- `dataConfig`는 금지 (deprecated, 존재 시 빌드 FAIL)
- `domains[*].dataTargetDirs`는 금지 (존재 시 빌드 실패)

---

## DomainType = DATA

DATA 입력은 `{buildInputJson}`의 `domains` 섹션이 정의한다.

### Common 필수 (Hard Rule)

**Devian v10 프로젝트는 DATA DomainKey로 `Common`을 반드시 포함한다.**

- `{buildInputJson}`에서 `domains.Common`은 필수 항목이다.
- 결과로 Common 모듈(C#/TS)은 항상 생성/유지된다:
  - C#: `Devian.Domain.Common` (프로젝트명)
  - TS: `@devian/module-common` (폴더명: `devian-domain-common`)

> Common 모듈의 상세 정책은 [skills/devian-common/02-module-policy](../../devian-common/02-module-policy/SKILL.md)를 참조한다.

### 필수 개념

- **Contracts**: JSON 기반 타입/enum 정의
- **Tables**: XLSX 기반 테이블 정의 + 데이터

입력 경로는 `{buildInputJson}`이 정본이다:
- `domains[Common].contractDir = Domains/Common/contracts`
- `domains[Common].tableDir = Domains/Common/tables`

**키 변경 (레거시 호환):**
- `contractDir` (새 키), `contractsDir` (레거시/금지)
- `tableDir` (새 키), `tablesDir` (레거시/금지)

---

## Tables (XLSX) 헤더/데이터 규약

- 최소 **4행 헤더**를 가진다.
  - Row 1: 컬럼명
  - Row 2: 타입
  - Row 3: 옵션
  - Row 4: 코멘트(해석하지 않음)
- Row 5부터 데이터
- **Header Stop Rule**: Row1에서 빈 셀을 만나면 그 뒤 컬럼은 무시
- **Data Stop Rule**: PrimaryKey 컬럼이 비면 즉시 중단

### 옵션 해석 정책

- **PrimaryKey:** `pk` 옵션만 PrimaryKey로 해석한다.
- **gen:\<EnumName\>:** `gen:` 옵션이 선언된 컬럼은 **반드시 `pk`여야 한다**.
- **group:true (Hard):** 테이블당 최대 1개 컬럼만 허용.
- `optional:true`는 "nullable/optional column" 힌트로만 사용
- 그 외 `parser:*` 등은 **Reserved** (있어도 무시 / 의미 부여 금지)

상세 규칙: [skills/devian-data/30-table-authoring-rules](../30-table-authoring-rules/SKILL.md)

---

## DATA 산출물 경로 (정책)

**staging:**
- `{tempDir}/{DomainKey}/cs/Generated/{DomainKey}.g.cs`
- `{tempDir}/{DomainKey}/ts/Generated/{DomainKey}.g.ts`, `index.ts`
- `{tempDir}/{DomainKey}/data/ndjson/{TableName}.json` (내용은 NDJSON)
- `{tempDir}/{DomainKey}/data/pb64/{TableName}.asset` (pk 옵션 있는 테이블만)

**final (csConfig/tsConfig/tableConfig 기반):**
- `{csConfig.generateDir}/Devian.Domain.{DomainKey}/Generated/{DomainKey}.g.cs`
- `{tsConfig.generateDir}/devian-domain-{domainkey}/Generated/{DomainKey}.g.ts`, `index.ts`
- `{tableDir}/ndjson/{TableName}.json` (내용은 NDJSON)
- `{tableDir}/pb64/{TableName}.asset` (pk 옵션 있는 테이블만)

**도메인 폴더 미사용 (Hard Rule):**
- 최종 경로에 `{DomainKey}` 폴더를 생성하지 않는다.
- 모든 도메인의 테이블 파일이 동일 디렉토리에 병합된다.
- **동일 파일명 충돌 시 빌드 FAIL** (조용한 덮어쓰기 금지).

**금지 필드 (Hard Fail):**
- `domains[*].csTargetDir` — 금지, `csConfig.generateDir` 사용
- `domains[*].tsTargetDir` — 금지, `tsConfig.generateDir` 사용
- `domains[*].dataTargetDirs` — 금지, `tableConfig.*Dirs` 사용

---

## C# Namespace (Hard Rule)

DATA Domain 생성물의 C# 네임스페이스:

- `namespace Devian.Domain.{DomainKey}`

예: DomainKey `Common` → `namespace Devian.Domain.Common`

---

## TS index.ts Marker 관리 (Hard Rule)

**TS `devian-domain-*/index.ts`는 빌더가 관리하되, 통째 덮어쓰기를 금지한다.**

- marker 구간:
  - `// <devian:domain-exports>` ~ `// </devian:domain-exports>` — Domain 생성물 export
  - `// <devian:feature-exports>` ~ `// </devian:feature-exports>` — features 폴더 export

---

## NDJSON 스토리지 규약

**파일 확장자는 `.json`이지만, `ndjson/` 폴더의 파일 내용은 NDJSON(라인 단위 JSON)이다.**

상세 규칙: [skills/devian-data/34-ndjson-storage](../34-ndjson-storage/SKILL.md)

---

## pb64 export 규약 (Hard Rule)

**pk 옵션이 있는 테이블만 Unity TextAsset `.asset` 파일로 export한다.**

- 파일명: `{TableName}.asset` (테이블 단위 1개 파일)
- 저장 형식: Unity TextAsset YAML
- pk 옵션이 없는 테이블은 export 안함

상세 규칙: [skills/devian-data/35-pb64-storage](../35-pb64-storage/SKILL.md)

---

## DATA export PK 규칙 (Hard Rule)

**DATA export는 PK 유효 row만 포함하며, 유효 row가 없으면 산출물을 생성하지 않는다.**

- `primaryKey`(pk 옵션)가 정의되지 않은 테이블은 ndjson/pb64 파일을 생성하지 않는다.
- `primaryKey` 값이 비어있는 row는 export 대상에서 제외된다.
- 결과적으로 유효 row가 0개인 경우 파일을 생성하지 않고 `[Skip]` 로그를 남긴다.

---

## See Also

- [Root SSOT](../../devian-core/03-ssot/SKILL.md) — 공통 용어/플레이스홀더/머지 규칙
- [Data Policy](../01-policy/SKILL.md)
- [Table Authoring Rules](../30-table-authoring-rules/SKILL.md)
- [NDJSON Storage](../34-ndjson-storage/SKILL.md)
- [PB64 Storage](../35-pb64-storage/SKILL.md)
