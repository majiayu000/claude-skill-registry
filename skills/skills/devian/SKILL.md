# Devian v10 — Index

Status: ACTIVE
AppliesTo: v10

## Start Here

| 문서 | 설명 |
|------|------|
| **SSOT** | [skills/devian-core/03-ssot](../devian-core/03-ssot/SKILL.md) — 모든 정책/경로/규칙의 정본 |
| **Overview** | [skills/devian/00-overview](./00-overview/SKILL.md) — Devian이 무엇인지 |
| **Common Policy** | [skills/devian/01-policy](./01-policy/SKILL.md) — 프레임워크 공통 정책 |
| **Glossary** | [skills/devian/10-glossary](./10-glossary/SKILL.md) — 용어/플레이스홀더 정의 |
| **Workspace** | [skills/devian/20-workspace](./20-workspace/SKILL.md) — npm workspace 구조 |

---

## Inputs (Quick Reference)

| 플레이스홀더 | 설명 | 예시 |
|-------------|------|------|
| `{buildInputJson}` | 빌드 입력 JSON | `input/input_common.json` |
| `{projectConfigJson}` | 프로젝트 설정 JSON | `input/config.json` |

정확한 키/머지 규칙: [skills/devian-core/03-ssot](../devian-core/03-ssot/SKILL.md)

---

## SSOT Hub

| Category | SSOT | 범위 |
|----------|------|------|
| **Root** | [devian-core/03-ssot](../devian-core/03-ssot/SKILL.md) | 공통 용어, 플레이스홀더, 입력 분리, 머지 규칙 |
| **Tools** | [devian-tools/03-ssot](../devian-tools/03-ssot/SKILL.md) | 빌드 파이프라인, Phase, Validate, tempDir |
| **Data** | [devian-data/03-ssot](../devian-data/03-ssot/SKILL.md) | tableConfig, Tables, NDJSON, pb64 |
| **Protocol** | [devian-protocol/03-ssot](../devian-protocol/03-ssot/SKILL.md) | Protocol Spec, Opcode/Tag, Protocol UPM |
| **Unity** | [devian-unity/03-ssot](../devian-unity/03-ssot/SKILL.md) | upmConfig, UPM Sync, Foundation |

---

## I want to…

| 목적 | 문서 |
|------|------|
| 빌드 실행하기 | [skills/devian-tools/20-build-domain](../devian-tools/20-build-domain/SKILL.md) |
| 빌드 에러 이해하기 | [skills/devian-tools/21-build-error-reporting](../devian-tools/21-build-error-reporting/SKILL.md) |
| 아카이브/배포하기 | [skills/devian-tools/90-project-archive](../devian-tools/90-project-archive/SKILL.md) |
| 테이블 작성하기 | [skills/devian-data/30-table-authoring-rules](../devian-data/30-table-authoring-rules/SKILL.md) |
| NDJSON/Row IO 이해하기 | [skills/devian-data/32-json-row-io](../devian-data/32-json-row-io/SKILL.md) |
| ContractGen 구현 보기 | [skills/devian-data/43-contractgen-implementation](../devian-data/43-contractgen-implementation/SKILL.md) |
| 프로토콜 코드젠 보기 | [skills/devian-protocol/40-codegen-protocol](../devian-protocol/40-codegen-protocol/SKILL.md) |
| Unity 정책 확인하기 | [skills/devian-unity/01-policy](../devian-unity/01-policy/SKILL.md) |
| 샘플 작성하기 | [skills/devian-unity-samples/02-samples-authoring-guide](../devian-unity-samples/02-samples-authoring-guide/SKILL.md) |

---

## Skill Groups

| Group | Overview | Policy | SSOT | 설명 |
|-------|----------|--------|------|------|
| **devian** | [00-overview](./00-overview/SKILL.md) | [01-policy](./01-policy/SKILL.md) | — | 공통 인덱스, 용어, workspace |
| **devian-core** | [00-overview](../devian-core/00-overview/SKILL.md) | [01-policy](../devian-core/01-policy/SKILL.md) | [03-ssot](../devian-core/03-ssot/SKILL.md) | Root SSOT, 스킬 규격, 런타임 |
| **devian-tools** | [00-overview](../devian-tools/00-overview/SKILL.md) | [01-policy](../devian-tools/01-policy/SKILL.md) | [03-ssot](../devian-tools/03-ssot/SKILL.md) | 빌더, 아카이브, CLI 도구 |
| **devian-data** | [00-overview](../devian-data/00-overview/SKILL.md) | [01-policy](../devian-data/01-policy/SKILL.md) | [03-ssot](../devian-data/03-ssot/SKILL.md) | 테이블, 계약, NDJSON, PB64 |
| **devian-protocol** | [00-overview](../devian-protocol/00-overview/SKILL.md) | [01-policy](../devian-protocol/01-policy/SKILL.md) | [03-ssot](../devian-protocol/03-ssot/SKILL.md) | 프로토콜 코드젠, Opcode |
| **devian-common** | [00-overview](../devian-common/00-overview/SKILL.md) | [01-policy](../devian-common/01-policy/SKILL.md) | — | Common 도메인, Feature 모듈 |
| **devian-unity** | [00-overview](../devian-unity/00-overview/SKILL.md) | [01-policy](../devian-unity/01-policy/SKILL.md) | [03-ssot](../devian-unity/03-ssot/SKILL.md) | Unity UPM, 컴포넌트 |
| **devian-examples** | [00-overview](../devian-examples/00-overview/SKILL.md) | [01-policy](../devian-examples/01-policy/SKILL.md) | — | 예제 도메인/프로토콜 |
| **devian-unity-samples** | [00-overview](../devian-unity-samples/00-overview/SKILL.md) | [01-policy](../devian-unity-samples/01-policy/SKILL.md) | — | Unity 샘플 템플릿 |

---

## Reference

- Root Index: [skills/SKILL.md](../SKILL.md)
- SSOT: [skills/devian-core/03-ssot](../devian-core/03-ssot/SKILL.md)
