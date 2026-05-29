---
name: ecomode
description: 토큰 효율적 실행 모드. 비용을 최소화하면서 작업을 수행합니다. 간단한 작업에 fast 모델을 자동 선택하고, 병렬 에이전트 수를 제한하며, 불필요한 컨텍스트 로딩을 줄입니다. Use when budget-conscious execution is needed or when the user requests token-efficient processing.
disable-model-invocation: true
---

# Ecomode — 토큰 효율적 실행

비용을 최소화하면서 품질을 유지하는 실행 모드입니다.

## 진입 조건

- 사용자가 "eco", "절약", "budget", "효율적으로" 등 키워드를 사용할 때
- 단순 수정이 반복될 때 자동 전환 권장

## 최적화 전략

### 1. 모델 라우팅

| 작업 유형 | 모델 선택 |
|----------|----------|
| 파일 탐색, 패턴 검색 | fast (explore subagent) |
| 단순 코드 수정, 리팩토링 | fast |
| 문서 작성, 주석 | fast |
| 복잡한 아키텍처 결정 | inherit (기본 모델) |
| 디버깅, 근본 원인 분석 | inherit (기본 모델) |

### 2. 에이전트 사용 제한

- 병렬 에이전트: 최대 2개 (기본 4개 대비 절반)
- 분석 단계 축소: analyst 생략, planner가 직접 분석
- 검증 단계 축소: reviewer만 실행 (qa-tester 생략)

### 3. 컨텍스트 절약

- 필요한 파일만 Read (전체 파일 대신 라인 범위 지정)
- SemanticSearch 대신 Grep 우선 사용 (토큰 절약)
- 불필요한 룰/스킬 로딩 생략

### 4. 출력 최소화

- 중간 보고 생략, 최종 결과만 출력
- 코드 블록 위주, 설명 최소화
- Mermaid 다이어그램 생략

## 워크플로우

1. 작업 복잡도 평가 (Simple/Medium/Complex)
2. Simple: 직접 처리 (에이전트 위임 없음)
3. Medium: fast 모델 에이전트 1개 위임
4. Complex: inherit 모델 에이전트 최대 2개 병렬

## Autopilot과의 차이

| 항목 | Autopilot | Ecomode |
|-----|----------|---------|
| 병렬 에이전트 | 최대 4개 | 최대 2개 |
| 모델 | inherit | fast 우선 |
| 분석 단계 | 전체 (analyst+planner) | 축소 (planner only) |
| 검증 단계 | reviewer+qa-tester | reviewer only |
| 보고 | 상세 | 최소 |

## 완료 보고 형식

```
[Ecomode 완료]
- 수정 파일: [목록]
- 검증: ReadLints 통과
```
