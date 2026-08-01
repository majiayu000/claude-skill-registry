---
name: 34-ndjson-storage
description: 이 문서는 NDJSON 저장 포맷의 정본이다.
---

# 34-ndjson-storage

Status: ACTIVE
AppliesTo: v10

## SSOT

이 문서는 **NDJSON 저장 포맷**의 정본이다.

---

## 목적/범위

**NDJSON(Line-delimited JSON) 파일의 저장 포맷(내용/확장자)을 정의한다.**

이 스킬은 "저장 포맷"만 정의한다. 구체적인 폴더 경로/라우팅은 각 도메인 스킬에서 정한다:
- String Table: `skills/devian-data/33-string-table/SKILL.md` → `.../string/ndjson/...`
- 일반 Table: `skills/devian-data/32-json-row-io/SKILL.md` → `.../ndjson/...`

---

## NDJSON 포맷 규칙 (Hard Rules)

### 파일 인코딩

**UTF-8 텍스트**

### 내용 형식

**NDJSON (Line-delimited JSON)**

- 한 줄 = JSON object 1개
- 빈 줄 금지
- JSON array (`[]`) 금지

```
{"id":"item1","value":100}
{"id":"item2","value":200}
{"id":"item3","value":300}
```

### 확장자 규칙 (중요)

**파일 확장자는 `.json`이다.**

- 내용이 NDJSON이라도 확장자는 `.json` 사용
- 소비 측(Unity/툴링) 요구로 `.json` 고정
- `.ndjson` 확장자 금지

### 결정성 (Deterministic)

**같은 입력이면 항상 같은 출력이 나와야 한다.**

- 라인 순서: 입력 데이터 순서 유지
- JSON stringify: 컴팩트 포맷 (들여쓰기 없음)
- 필드 순서: 각 도메인 스킬에서 정의

---

## 빌더 API

### 소스 경로

```
framework-ts/tools/builder/generators/ndjson-storage.js
```

### Export 함수

```javascript
/**
 * Object 배열을 NDJSON 문자열로 변환
 * @param {Array<object>} objects - JSON object 배열
 * @returns {string} NDJSON 문자열
 */
export function encodeNdjsonFromObjects(objects);

/**
 * JSON 문자열 배열을 NDJSON 문자열로 변환
 * @param {Array<string>} lines - 이미 JSON.stringify된 라인 배열
 * @returns {string} NDJSON 문자열
 */
export function encodeNdjsonFromLines(lines);
```

### 동작 규칙

- `encodeNdjsonFromObjects`: `objects.map(o => JSON.stringify(o)).join('\n')`
- `encodeNdjsonFromLines`: `lines.join('\n')`
- 빈 배열이면 `''` 반환 (기존 동작과 호환)

---

## 금지 행동

- NDJSON 내용을 JSON array(`[]`)로 바꾸기 금지
- 확장자를 `.ndjson`로 바꾸기 금지 (`.json` 유지)
- 라인 끝에 trailing comma 추가 금지

---

## DoD (검증 가능)

### PASS 조건

- [ ] NDJSON 파일 확장자가 `.json`임
- [ ] 파일 내용이 한 줄당 JSON object 1개
- [ ] JSON array가 아님
- [ ] 빈 줄 없음
- [ ] 같은 입력이면 같은 출력 (결정성)

### FAIL 조건

- 파일 확장자가 `.ndjson`
- 내용이 JSON array
- 빈 줄 포함
- 비결정적 출력

---

## Reference

- Consumer: `skills/devian-data/32-json-row-io/SKILL.md` (일반 Table)
- Consumer: `skills/devian-data/33-string-table/SKILL.md` (String Table)
