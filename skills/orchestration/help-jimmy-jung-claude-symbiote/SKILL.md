---
name: help
description: 사용 가능한 에이전트, 스킬, 커맨드, 키워드 목록을 표시하고 사용법을 안내합니다. Use when the user asks for help, available commands, or how to use the orchestration system.
---

# Help — 사용 가이드

사용 가능한 에이전트, 스킬, 커맨드, 키워드 목록을 표시합니다.

## 워크플로우

### Step 1: 현재 설정 확인
- `.claude/project/.initialized` 마커 존재 여부 확인
- 프로젝트 초기화 상태 파악

### Step 2: 카테고리별 목록 출력

#### 커맨드 (Commands)
`.claude/commands/` 디렉터리의 .md 파일을 Glob으로 검색하여 목록 출력.

#### 에이전트 (Agents)
`.claude/agents/` 디렉터리의 .md 파일에서 name과 description을 추출하여 테이블로 출력.

#### 스킬 (Skills)
`.claude/skills/*/SKILL.md` 파일에서 name과 description을 추출하여 테이블로 출력.

#### 자연어 키워드 (Magic Keywords)
CLAUDE.md의 Mode Detection 테이블을 참조하여 키워드 목록 출력.

#### source 태그 표시

각 항목에 `[origin]` 또는 `[custom]` 레이블을 표시합니다.

- `[origin]`: 기본 제공 번들 파일 (`<!-- source: origin -->` 또는 `# source: origin` 태그가 있는 파일)
- `[custom]`: 사용자가 생성한 파일 (source 태그가 없는 파일)

### Step 3: 사용 통계 연동

`.claude/project/usage-data/` 디렉터리가 존재하면 사용 통계를 함께 표시합니다.

각 카테고리(skills, commands, agents) 하위 파일을 읽어 count를 추출합니다.
파일 형식: `{count}|{ISO8601 timestamp}`

통계가 있으면:
- 각 항목 옆에 사용 횟수 표시 (예: `code-accuracy (42회)`)
- 가장 많이 사용된 Top 5 (전체 카테고리 통합) 별도 섹션
- 미사용 항목(count=0)은 `(미사용)` 태그

통계가 없으면:
- 횟수 없이 기존 형식대로 출력
- "/stats 커맨드로 사용 통계를 확인할 수 있습니다" 안내

### Step 4: 출력 형식

```
[도움말]

가장 많이 사용된 Top 5:
  1. code-accuracy (스킬)    42회
  2. implementer (에이전트)   35회
  3. git-commit (스킬)       28회
  4. ralph (커맨드)          15회
  5. reviewer (에이전트)     12회

커맨드:
  [origin] /autopilot  — 병렬 최대 성능 파이프라인          (8회)
  [origin] /ralph      — 완료까지 자율 반복 루프            (15회)
  [origin] /pipeline   — 에이전트 순차 체이닝               (미사용)
  [origin] /plan       — 기획 세션 시작                     (5회)
  [custom] /deploy     — 프로젝트 배포 파이프라인            (3회)
  /stats               — 사용 통계 조회 및 미사용 항목 관리
  [origin] /clean      — 완료된 작업의 state 폴더 정리      (2회)
  ...

에이전트 ({N}개):
  [origin] analyst     — 사전 분석 전문가                   (10회)
  [origin] architect   — 아키텍처 전문가                    (미사용)
  [custom] ios-explorer — iOS 코드베이스 탐색               (8회)
  ...

스킬 ({N}개):
  [origin] autonomous-loop — 자율 실행 루프                 (6회)
  [origin] code-accuracy   — 코드 정확성 검증               (42회)
  [custom] smartplayer     — SmartPlayer 전용 패턴           (12회)
  ...

자연어 키워드:
  "끝까지", "멈추지 마"  → Ralph Mode
  "심층 분석"           → Deep Analysis
  "최대 성능", "병렬로"  → Autopilot
  ...

프로젝트 상태:
  초기화: [완료/미완료]
  활성 task-folder: [없음 / 목록]
  사용 추적: [활성 ({N}일) / 미설정]

상세 통계는 /stats 커맨드를 실행하세요.
```
