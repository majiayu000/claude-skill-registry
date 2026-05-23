---
name: evolve
description: 프로젝트 변화를 감지하고 .claude 설정을 진화시킵니다. 새로운 의존성, 아키텍처 패턴 변경, 코드베이스 성장에 맞춰 rules와 context를 업데이트합니다. Use when project has changed significantly since last setup/evolve.
disable-model-invocation: true
---

# Evolve Skill

프로젝트 변화를 감지하고 .claude 설정을 진화시킵니다. 새로운 의존성, 아키텍처 패턴 변경, 코드베이스 성장에 맞춰 rules와 context를 업데이트합니다.

## 진입 조건 (Entry Condition)

`.claude/project/.initialized` 마커 파일이 존재해야 합니다. setup이 먼저 실행되어야 하며, 없다면 /setup을 먼저 실행하도록 안내합니다.

## 워크플로우

### Step 1: 현재 상태 스냅샷 (Current State Snapshot)

- `.claude/rules/project-context.md` 읽기 (프로젝트 컨텍스트)
- `.claude/project/VERSION` 읽기
- 현재 스택 설정 메모

### Step 2: 변경 감지 (Change Detection)

setup과 동일한 감지 로직을 재실행하여 현재 컨텍스트와 비교:

- 새 의존성 추가? (패키지 매니저 파일 diff)
- 새 프레임워크 import? (grep import 구문)
- 아키텍처 패턴 변경? (새 폴더, 새 패턴)
- 새 언어 도입?
- CI/CD 변경?
- 빌드 도구 변경?

### Step 3: 드리프트 분석 (Drift Analysis)

감지된 현재 상태 vs 기존 컨텍스트 비교:

- 추가 항목 (새 의존성, 새 패턴)
- 제거 항목 (deprecated 라이브러리, 사용 중단 패턴)
- 변경 항목 (버전 업그레이드, 아키텍처 전환)

### Step 4: 진화 계획 (Evolution Plan)

사용자에게 다음을 제시:

- 무엇이 변경되었는지
- `.claude/rules/` 내 규칙에 대한 제안 업데이트
- 추가할 새 규칙
- 제거할 규칙
- 에이전트 커스터마이즈 업데이트

### Step 5: 사용자 승인 (User Approval)

변경 적용 전 사용자 승인 요청. 승인 시 Step 6으로 진행.

### Step 6: 변경 적용 (Apply Changes)

- `project-context.md` 업데이트 (스택 정보 갱신)
- VERSION 버전 증가 (semver patch 또는 minor)
- `.claude/project/.initialized` 내 진화 횟수(moltCount) 증가
- 프로젝트 규칙 생성/수정/삭제
- codebase-index.md가 있으면 deep-index 재실행

moltCount 관리:
- `.initialized` 파일 내 `moltCount: N` 줄을 업데이트
- evolve 실행마다 1씩 증가
- /stats에서 진화 이력 추적에 활용

### Step 7: 히스토리 (History)

`.claude/project/history/vN.M-evolution-YYYYMMDD.md` 작성:

- 변경 사항
- 업데이트된 항목
- Before/After 비교

## 트리거 권장 사항

다음 상황에서 /evolve 실행을 권장합니다:

- 새 의존성 추가 후
- 대규모 리팩토링 후
- 새 모듈/Feature 추가 후
- 주기적 (월 1회 등)

## evolve vs setup

| 항목 | setup | evolve |
|------|-------|--------|
| 전제 조건 | .initialized 없음 | .initialized 있음 |
| 목적 | 최초 부트스트랩 | 기존 설정 진화 |
| 대상 | 전체 설정 생성 | 변경분만 업데이트 |
| 히스토리 | initial-setup | evolution-YYYYMMDD |

## 에스컬레이션

다음 상황에서 사용자 확인 요청:

- 구조적 변경이 커서 규칙 대폭 수정이 필요한 경우
- 기존 규칙과 충돌하는 새 패턴 감지
- 여러 아키텍처 패턴이 혼재된 경우
