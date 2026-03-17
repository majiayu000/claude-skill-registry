---
name: issue-feature
description: |
  GitHub 이슈 기반 기능 구현 스킬. 현재 브랜치의 이슈를 확인하고 DDD → Plan → TDD → Test 파이프라인을 실행합니다.
  사용 시기: (1) feature 브랜치에서 작업 시작 시 (2) 이슈 기반 개발 시작 시 (3) /issue-feature 호출 시
---

# Issue-Based Feature Implementation

GitHub 이슈 기반 기능 구현 파이프라인을 실행합니다.

## Quick Start

```bash
# 현재 브랜치에 연결된 이슈로 기능 구현 시작
/issue-feature

# 특정 이슈 번호 지정
/issue-feature 159
```

## Workflow

이 스킬은 `issue-feature-builder` 에이전트를 호출하여 다음 파이프라인을 실행합니다:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Issue Feature Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │  Issue   │ → │   DDD    │ → │  Feature │ → │   TDD    │     │
│  │ Discovery│   │ Analysis │   │   Plan   │   │   Impl   │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│       │              │              │              │             │
│       ▼              ▼              ▼              ▼             │
│  gh issue view   ddd-planning   feature-planner   tdd-orch     │
│                                                                  │
│                            ┌──────────┐                         │
│                          → │   Test   │                         │
│                            │  Auto    │                         │
│                            └──────────┘                         │
│                                 │                               │
│                                 ▼                               │
│                          test-automator                         │
└─────────────────────────────────────────────────────────────────┘
```

## Pipeline Options

### 1. Full Pipeline (Recommended)
```
DDD Analysis → Feature Plan → TDD Implementation → Test Automation
```
- 새로운 도메인 기능 구현 시 사용
- 가장 완전한 워크플로우
- 예상 소요: Opus ~$6.50

### 2. Quick Implementation
```
Feature Plan → TDD Implementation
```
- 도메인 설계가 이미 완료된 경우
- 단순 기능 추가 시
- 예상 소요: ~$3.50

### 3. Domain Focus
```
DDD Analysis → Feature Plan
```
- 설계 검토가 필요한 경우
- 복잡한 비즈니스 로직 분석 시
- 예상 소요: ~$4.50

### 4. Test Focus
```
Test Automation only
```
- 기존 코드에 테스트 추가 시
- 커버리지 향상 목적
- 예상 소요: ~$1.50

## Branch Naming Convention

이슈 번호 자동 추출을 위한 브랜치 명명 규칙:

```bash
feature/{issue-number}-{description}  # ✅ feature/159-crawling-youtube
fix/{issue-number}-{description}      # ✅ fix/42-login-bug
issue-{issue-number}-{description}    # ✅ issue-159-youtube
{issue-number}-{description}          # ✅ 159-crawling-youtube
```

## Agents Orchestrated

| Phase | Agent | Model | 역할 |
|-------|-------|-------|------|
| DDD | `ddd-planning` | Opus | 도메인 분석, Bounded Context, Aggregate 설계 |
| Plan | `feature-planner` (skill) | Opus | TDD 기반 Phase별 계획 수립 |
| TDD | `backend-development:tdd-orchestrator` | Sonnet | Red-Green-Refactor 구현 |
| Test | `full-stack-orchestration:test-automator` | Sonnet | 테스트 자동화, 커버리지 검증 |

## Output Artifacts

파이프라인 완료 시 생성되는 산출물:

```
docs/
├── ddd/
│   └── bounded-contexts/{context}.md  # DDD 분석 결과
└── plans/
    └── PLAN_{feature-name}.md          # 구현 계획서

src/
├── domain/                              # 도메인 코드
├── application/                         # 애플리케이션 서비스
└── infrastructure/                      # 인프라 코드

src/test/
├── unit/                                # 단위 테스트
├── integration/                         # 통합 테스트
└── e2e/                                 # E2E 테스트
```

## Quality Gates

각 Phase 완료 시 검증 항목:

- [ ] 빌드 성공
- [ ] 모든 테스트 통과
- [ ] 린팅 오류 없음
- [ ] 타입 체크 통과
- [ ] 커버리지 80%+ (비즈니스 로직)

## Example Session

```
$ git checkout -b feature/159-crawling-youtube
$ claude

User: /issue-feature

Claude: 🔍 브랜치 분석 중...

📋 **Issue #159: YouTube 크롤링 구현**
- Labels: `platform:backend`, `type:feature`
- Milestone: Sprint 4: Content Integration

**요구사항:**
> YouTube API를 사용하여 K-POP 관련 영상 크롤링 기능 구현
> - 아티스트별 최신 영상 수집
> - 영상 메타데이터 저장
> - 일일 자동 크롤링 스케줄

어떤 워크플로우를 실행할까요?
1. ⭐ Full Pipeline (DDD → Plan → TDD → Test) [권장]
2. 🚀 Quick Implementation (Plan → TDD)
3. 📐 Domain Focus (DDD → Plan)
4. 🧪 Test Focus only

User: 1

Claude: Full Pipeline을 시작합니다...

[Phase A: DDD Analysis]
ddd-planning 에이전트 실행 중...
✅ Content Bounded Context 분석 완료
✅ YouTubeVideo Aggregate 설계 완료
✅ doc/ddd/bounded-contexts/content.md 업데이트

[Phase B: Feature Planning]
feature-planner 스킬 실행 중...
📝 계획서 생성: docs/plans/PLAN_youtube-crawling.md

계획을 검토해주세요. 진행할까요? [Y/n]
...
```

## Tips

1. **이슈 작성 팁**: Acceptance Criteria를 명확히 작성하면 더 정확한 계획 생성
2. **라벨 활용**: `platform:*`, `type:*` 라벨이 있으면 자동 분류
3. **점진적 실행**: 각 Phase 후 검토 가능, 필요시 수정 후 재실행
4. **중단 재개**: TodoWrite로 진행 상황 추적, 중단 후 재개 가능
