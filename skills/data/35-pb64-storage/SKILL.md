---
name: 35-pb64-storage
description: 이 문서는 pb64 저장(포장) 규약의 정본이다.
---

# 35-pb64-storage

Status: ACTIVE
AppliesTo: v10

## SSOT

이 문서는 **pb64 저장(포장) 규약**의 정본이다.

---

## 목적/범위

**pb64는 Unity/UPM 소비를 전제로 하며, Addressables에서 TextAsset으로 로드 가능한 `.asset` 형태로 저장한다.**

이 스킬은 "저장(포장) 규약"만 정의한다. pb64 payload 자체 규약은 각 생성 스킬이 정의/참조한다:
- 일반 Table pb64 payload: DVGB 컨테이너 (이 문서에서 정의)
- String Table pb64 payload: `skills/devian-data/33-string-table/SKILL.md`의 StringChunk 규약

---

## 저장 규칙 (Hard Rules)

### 파일 확장자

**`.asset`**

### 저장 형태

**Unity TextAsset YAML**

### YAML 구조

```yaml
%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!49 &4900000
TextAsset:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_Name: <TABLE_NAME>
  m_Script: <PAYLOAD>
```

### m_Script 페이로드 규칙

**두 가지 케이스를 지원한다:**

| 케이스 | 사용처 | m_Script 형식 |
|--------|--------|---------------|
| Single-line base64 | 일반 Table (DVGB 컨테이너) | 인라인 문자열 |
| Multi-line text | String Table (청크 base64) | Block scalar (`|`) |

### Multi-line Block Scalar (필수)

**Multi-line일 경우 YAML이 깨지지 않도록 block scalar(`|`) 사용을 강제한다.**

```yaml
  m_Script: |
    base64Line1
    base64Line2
    base64Line3
```

> **절대 금지**: `m_Script: ${multilineText}`처럼 단일 라인에 멀티라인 문자열을 끼워 넣기 (YAML 깨짐)

### Decoding Note (Runtime) — Hard Rule

`.asset`는 Unity TextAsset YAML이므로 `TextAsset.text`가 **YAML 전체를 반환할 수 있다**.

**StringTable pb64 디코더 규칙:**

| 규칙 | 설명 |
|------|------|
| base64 라인만 추출 | YAML 헤더/필드 라인은 무시 |
| 구분자 지원 | `\n` + `|` 둘 다 지원 (파이프 연결형 입력 방어) |
| 실패 로깅 | `Devian.Log`로 기록 (단, base64 후보 라인에 대해서만) |
| 로그 스팸 방지 | YAML 라인은 base64 후보 필터로 사전 제외 |

**base64 후보 판별:**
- 문자: `A-Za-z0-9+/=` 만 허용
- 길이 4 미만이면 base64가 아님

> **Reference:** `skills/devian-data/33-string-table/SKILL.md`의 "pb64 Encoding/Decoding 규칙" 섹션

---

## DVGB Gzip Block Container Format (일반 Table용)

일반 Table pb64의 `m_Script` 페이로드는 DVGB gzip 블록 컨테이너를 base64 인코딩한 것이다.

### 컨테이너 헤더

| Offset | Size | Field | Value |
|--------|------|-------|-------|
| 0 | 4 | Magic | `DVGB` (ASCII) |
| 4 | 1 | Version | `1` |
| 5 | 4 | BlockSize | `1048576` (1024K, little-endian) |
| 9 | 4 | BlockCount | 블록 개수 (little-endian) |

### 블록 구조 (BlockCount 만큼 반복)

| Size | Field | Description |
|------|-------|-------------|
| 4 | UncompressedLen | 압축 전 바이트 수 (little-endian) |
| 4 | CompressedLen | gzip 압축 후 바이트 수 (little-endian) |
| CompressedLen | GzipBytes | gzip 압축된 데이터 |

### 블록 크기

- 블록 크기: **1024K (1,048,576 bytes)** 고정
- 마지막 블록은 1024K보다 작을 수 있음

### 압축 대상

- rawBinary (varint length-delimited JSON rows)를 1024K 블록으로 분할
- 각 블록을 개별 gzip 압축
- **rawBinary 포맷은 변경하지 않음** (압축만 추가)

### 하위 호환

- C# 로더는 앞 4바이트가 `DVGB`가 아니면 **기존 포맷(압축 없음)**으로 처리
- 기존 .asset 파일도 계속 읽을 수 있음

---

## rawBinary 포맷 (DVGB 압축 전)

압축 전/후 동일한 포맷. 테이블의 모든 row를 concat:

```
[row1][row2][row3]...
```

각 row 구조:
```
[varint jsonLength][jsonUtf8]
```

- `jsonLength`: JSON 문자열의 UTF-8 바이트 길이 (protobuf varint 인코딩)
- `jsonUtf8`: JSON 문자열의 UTF-8 바이트

### Varint 인코딩

protobuf 표준 varint 인코딩을 사용한다:
- unsigned 32-bit 길이 기준
- 각 바이트의 MSB가 1이면 다음 바이트가 이어짐
- 7비트씩 little-endian 순서로 저장

---

## 결정성 (Deterministic)

**같은 입력이면 항상 같은 .asset 출력이 나와야 한다.**

- gzip 압축 레벨: 9 (최대)
- JSON stringify: 컴팩트 포맷 (들여쓰기 없음)

---

## 소스 경로

| 역할 | 경로 |
|------|------|
| 일반 Table pb64 생성기 | `framework-ts/tools/builder/generators/table.js` |
| String Table pb64 생성기 | `framework-ts/tools/builder/generators/string-table.js` |

---

## 금지 행동

- `.pb64` 확장자 사용 금지 (`.asset` 사용)
- Multi-line 페이로드에 인라인 문자열 사용 금지 (block scalar `|` 사용)
- rawBinary 포맷 변경 금지 (압축만 추가)
- DVGB 블록 크기(1024K) 변경 금지

---

## DoD (검증 가능)

### PASS 조건

- [ ] pb64 파일 확장자가 `.asset`임
- [ ] 파일 내용이 Unity TextAsset YAML 형식
- [ ] Multi-line 페이로드에 block scalar(`|`) 사용됨
- [ ] 같은 입력이면 같은 출력 (결정성)

### FAIL 조건

- 파일 확장자가 `.pb64`
- Multi-line 페이로드를 인라인 문자열로 저장
- YAML 파싱 실패

---

## C# 로더 API (참고)

```csharp
// DVGB 컨테이너 로드 (하위 호환 지원)
byte[] rawBinary = Pb64Loader.LoadFromBase64(base64String);

// row 파싱
Pb64Loader.ParseRows(rawBinary, json => {
    var entity = JsonConvert.DeserializeObject<MyEntity>(json);
    // ...
});
```

---

## Reference

- Policy SSOT: `skills/devian-core/03-ssot/SKILL.md`
- 일반 Table: `skills/devian-data/32-json-row-io/SKILL.md`
- String Table: `skills/devian-data/33-string-table/SKILL.md`
