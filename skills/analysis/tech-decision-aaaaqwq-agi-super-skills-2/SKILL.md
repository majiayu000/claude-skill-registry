---
name: tech-decision
description: This skill should be used when the user asks to "기술 의사결정", "뭐 쓸지 고민", "A vs B", "비교 분석", "라이브러리 선택", "아키텍처 결정", "어떤 걸 써야 할지", "트레이드오프", "기술 선택", "구현 방식 고민", or needs deep analysis for technical decisions. Provides systematic multi-source research and synthesized recommendations.
version: 0.1.0
---

# Tech Decision - 기술 의사결정 깊이 탐색

기술적 의사결정을 체계적으로 분석하고 종합적인 결론을 도출하는 스킬.

## 핵심 원칙

**두괄식 결과물**: 모든 보고서는 결론을 먼저 제시하고, 그 다음에 근거를 제공한다.

## 사용 시나리오

- 라이브러리/프레임워크 선택 (React vs Vue, Prisma vs TypeORM)
- 아키텍처 패턴 결정 (Monolith vs Microservices, REST vs GraphQL)
- 구현 방식 선택 (Server-side vs Client-side, Polling vs WebSocket)
- 기술 스택 결정 (언어, 데이터베이스, 인프라 등)

## 의사결정 워크플로우

### Phase 1: 문제 정의

의사결정 주제와 맥락을 명확히 한다:

1. **주제 파악**: 무엇을 결정해야 하는가?
2. **옵션 식별**: 비교할 선택지들은 무엇인가?
3. **평가 기준 수립**: 어떤 기준으로 평가할 것인가?
   - 성능, 학습 곡선, 생태계, 유지보수성, 비용 등
   - 프로젝트 특성에 맞는 기준 우선순위 설정
   - 상세 기준은 **`references/evaluation-criteria.md`** 참조

### Phase 2: 병렬 정보 수집

여러 소스에서 동시에 정보를 수집한다. **반드시 병렬로 실행**:

```
┌─────────────────────────────────────────────────────────────┐
│  동시 실행 (Task tool로 병렬 실행)                            │
├─────────────────────────────────────────────────────────────┤
│  1. codebase-explorer agent                                 │
│     → 기존 코드베이스 분석, 현재 패턴/제약사항 파악              │
│                                                             │
│  2. docs-researcher agent                                   │
│     → 공식 문서, 가이드, best practices 리서치                │
│                                                             │
│  3. Skill: dev-scan                                         │
│     → 커뮤니티 의견 수집 (Reddit, HN, Dev.to, Lobsters)       │
│                                                             │
│  4. Skill: agent-council                                    │
│     → 다양한 AI 전문가 관점 수집                              │
│                                                             │
│  5. [선택] Context7 MCP                                     │
│     → 라이브러리별 최신 문서 조회                              │
└─────────────────────────────────────────────────────────────┘
```

**실행 방법**:

```markdown
# Agents는 Task tool로 병렬 실행
Task codebase-explorer: "분석할 주제와 컨텍스트"
Task docs-researcher: "리서치할 기술/라이브러리"

# 기존 스킬은 Skill tool로 호출
Skill: dev-scan (커뮤니티 의견)
Skill: agent-council (전문가 관점)
```

### Phase 3: 종합 분석

수집된 정보를 바탕으로 tradeoff-analyzer agent를 실행:

- 각 옵션별 pros/cons 정리
- 평가 기준별 점수화
- 충돌하는 의견 정리
- 신뢰도 평가 (출처 기반)

### Phase 4: 최종 보고서 생성

decision-synthesizer agent로 두괄식 종합 보고서 작성 (상세 템플릿: **`references/report-template.md`**):

```markdown
# 기술 의사결정 보고서: [주제]

## 결론 (Executive Summary)
**추천: [Option X]**
[1-2문장 핵심 이유]

## 평가 기준 및 가중치
| 기준 | 가중치 | 설명 |
|------|--------|------|
| 성능 | 30% | ... |
| 학습곡선 | 20% | ... |

## 옵션별 분석

### Option A: [이름]
**장점:**
- [장점 1] (출처: 공식 문서)
- [장점 2] (출처: Reddit r/webdev)

**단점:**
- [단점 1] (출처: HN 토론)

**적합한 경우:** [시나리오]

### Option B: [이름]
...

## 종합 비교
| 기준 | Option A | Option B | Option C |
|------|----------|----------|----------|
| 성능 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 학습곡선 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **총점** | **X점** | **Y점** | **Z점** |

## 추천 근거
1. [핵심 근거 1 with 출처]
2. [핵심 근거 2 with 출처]
3. [핵심 근거 3 with 출처]

## 리스크 및 주의사항
- [주의점 1]
- [주의점 2]

## 참고 출처
- [출처 목록]
```

## 활용하는 리소스

### Agents (이 플러그인)

| Agent | 역할 |
|-------|------|
| `codebase-explorer` | 기존 코드베이스 분석, 패턴/제약사항 파악 |
| `docs-researcher` | 공식 문서, 가이드, best practices 리서치 |
| `tradeoff-analyzer` | 옵션별 pros/cons 정리, 비교 분석 |
| `decision-synthesizer` | 두괄식 최종 보고서 생성 |

### 기존 스킬 (Skill tool로 호출)

| Skill | 용도 | 호출 방법 |
|-------|------|-----------|
| `dev-scan` | Reddit, HN, Dev.to 등 커뮤니티 의견 | `Skill: dev-scan` |
| `agent-council` | 다양한 AI 전문가 관점 수집 | `Skill: agent-council` |

### MCP (선택적)

- **Context7**: 라이브러리별 최신 공식 문서 조회

## 빠른 실행 가이드

### 1. 간단한 비교 (A vs B)

```
사용자: "React vs Vue 뭐가 나을까?"

실행:
1. Task docs-researcher + Task codebase-explorer (병렬)
2. Skill: dev-scan
3. Task tradeoff-analyzer
4. Task decision-synthesizer
```

### 2. 깊은 분석 (복잡한 의사결정)

```
사용자: "우리 프로젝트에 상태관리 라이브러리 뭘 쓸지 고민이야"

실행:
1. Task codebase-explorer (현재 상태 분석)
2. 병렬 실행:
   - Task docs-researcher (Redux, Zustand, Jotai, Recoil 등)
   - Skill: dev-scan
   - Skill: agent-council
3. Task tradeoff-analyzer
4. Task decision-synthesizer
```

### 3. 아키텍처 결정

```
사용자: "모놀리스 vs 마이크로서비스 어떻게 해야 할까?"

실행:
1. Task codebase-explorer (현재 규모/복잡도 분석)
2. 병렬 실행:
   - Task docs-researcher (각 아키텍처 best practices)
   - Skill: agent-council (아키텍트 관점)
3. Task tradeoff-analyzer (팀 규모, 배포 복잡도 등 고려)
4. Task decision-synthesizer
```

## 주의사항

1. **컨텍스트 제공**: 프로젝트 특성, 팀 규모, 기존 기술 스택 등 맥락 정보가 많을수록 정확한 분석 가능
2. **평가 기준 확인**: 사용자에게 중요한 기준이 무엇인지 먼저 확인
3. **신뢰도 표시**: 출처가 불분명하거나 오래된 정보는 명시
4. **결론 먼저**: 항상 두괄식으로 결론부터 제시

## 추가 리소스

### 참고 파일
- **`references/report-template.md`** - 상세 보고서 템플릿
- **`references/evaluation-criteria.md`** - 평가 기준 가이드
