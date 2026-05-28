---
name: pdca
description: |
  Project-level PDCA skill override for gaegulzip.
  Integrates with project agents (CTO, PO, Tech Lead, etc.) and
  uses platform-specific document paths from bkit.config.json.

  All agent interactions are BIDIRECTIONAL — downstream agents can push back
  to upstream agents when issues are found, with structured feedback loops.

  Agent workflow per phase (↔ = bidirectional):
  - Research: clarify ↔ research-director → CTO 통합 평가 (아키텍처+복잡도, BLOCK → clarify 재호출)
  - Plan: PO ↔ CTO (타당성 스캔, BLOCK → PO 재호출) → 사용자 승인 → CTO 라우팅 ↔ PO (Scope Mismatch → PO 보완 + 재승인)
  - Design: ui-ux-designer ↔ tech-lead (Design Pushback 루프) + API Contract 양방향 검증 (server/frontend tech-lead)
  - Do: CTO (work-plan) → developers ↔ CTO (BLOCKED:QUESTIONS → 라우팅 → 답변 → 재개)
  - Analyze: gap-detector ↔ CTO (integration review)
  - Iterate/Report: bkit agents

  Triggers: pdca, research, plan, design, analyze, report, status, next, iterate
argument-hint: "[action] [feature]"
user-invocable: true
agents:
  research-brainstorm: clarify (Skill)
  research-director: bkit/research-director
  research-feasibility-cto: cto (Feasibility Council)

  plan: product-owner
  plan-review: interactive-review:review (Skill)
  feasibility: cto
  routing: cto
  design-server: server/tech-lead
  design-mobile-ui: mobile/ui-ux-designer
  design-mobile-visual: frontend-design (Skill)
  design-mobile-tech: mobile/tech-lead
  design-web-ui: web/ui-ux-designer
  design-web-visual: frontend-design (Skill)
  design-web-tech: web/tech-lead
  do-distribute: cto
  do-server: server/node-developer
  do-mobile: mobile/flutter-developer
  do-web: web/react-developer
  test-scenario: test-scenario-generator
  design-review: plan-review (Skill, MANDATORY)
  analyze: bkit:gap-detector
  code-review: plan-review (Skill, MANDATORY)
  review: cto
  iterate: bkit:pdca-iterator
  report: bkit:report-generator
  verify: independent-reviewer
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - AskUserQuestion
imports:
  - ${PLUGIN_ROOT}/templates/plan.template.md
  - ${PLUGIN_ROOT}/templates/design.template.md
  - ${PLUGIN_ROOT}/templates/do.template.md
  - ${PLUGIN_ROOT}/templates/analysis.template.md
  - ${PLUGIN_ROOT}/templates/report.template.md
  - ${PLUGIN_ROOT}/templates/iteration-report.template.md
next-skill: null
pdca-phase: null
task-template: "[PDCA] {feature}"
---

# PDCA Skill (gaegulzip Project Override)

> Unified Skill for managing PDCA cycle with **agent-integrated workflow**.
> Each PDCA phase automatically invokes the appropriate project agents from `bkit.config.json`.
> Phase 상세 절차는 `phases/` 디렉토리의 개별 파일 참조.

## Config Reference

Read `bkit.config.json` to determine:
- `context.defaultLanguage` → **모든 출력(문서, 상태 메시지, 에이전트 응답)에 이 언어 사용**
- `pdca.planDocPaths` → document output paths
- `pdca.designDocPaths` → document output paths
- `pdca.analyzeDocPaths` → analysis document output paths
- `pdca.reportDocPaths` → report document output paths
- `platforms.{platform}.agents` → agent mapping per phase
- `pdca.statusFile` → `.pdca-status.json` path
- `pdca.matchRateThreshold` → 90 (default)
- `pdca.maxIterations` → 5 (default)

## Language Rule

**All output MUST be in the language specified by `bkit.config.json` → `context.defaultLanguage`.**
When calling agents via Task tool, always append to the prompt:
`\nIMPORTANT: Respond and write all documents in {defaultLanguage}. Code, paths, and technical terms stay in English.`

## ⚠️ Intent-Only Document Rule (Plan & Design 문서 필수 원칙)

**Plan/Design 문서는 "무엇을(WHAT)"과 "왜(WHY)"만 작성한다. "어떻게(HOW)" 즉 구현은 절대 작성하지 않는다.**

이 원칙을 위반하는 예시:
- ❌ 파일명/경로 지정: `src/services/authService.ts에 구현`
- ❌ 코드 구조 지시: `useEffect로 상태를 관리하고 Redux store에 저장`
- ❌ 함수 시그니처: `async function validateToken(token: string): Promise<boolean>`
- ❌ DB 쿼리 작성: `SELECT * FROM users WHERE email = ?`
- ❌ 특정 라이브러리 사용법: `zod.object({ email: z.string().email() })로 검증`

이 원칙을 지키는 예시:
- ✅ 사용자 행동 정의: `사용자는 이메일과 비밀번호로 로그인할 수 있다`
- ✅ 비즈니스 규칙: `비밀번호는 최소 8자, 영문+숫자+특수문자 포함`
- ✅ 데이터 요구사항: `사용자 프로필에는 닉네임, 프로필 이미지, 가입일이 포함된다`
- ✅ API 계약 (Design): `POST /auth/login → 요청: { email, password }, 응답: { token, user }`
- ✅ 제약조건: `토큰 만료 시간은 24시간`

**이유**: 구현은 Do 단계의 개발자 에이전트가 결정한다. 설계 문서에 구현을 쓰면 에이전트 자율성을 제한하고, 코드 변경 시 문서 부패를 유발한다.

> **모든 Plan/Design phase 에이전트 프롬프트에 이 원칙을 포함시킬 것.**

## Product Naming Convention

`{product}`는 앱 이름을 그대로 사용합니다:
- `wowa` — 메인 앱
- `admin` — 어드민 대시보드
- `talmosang` — 탈모상 AI 두피 분석

경로 예: `docs/wowa/auth/user-story.md`, `docs/admin/dashboard/web-brief.md`

## Fullstack frontendType 제약

`frontendType`은 **단일 값**만 허용합니다 (`"mobile"` 또는 `"web"`).
Mobile + Web 동시 개발이 필요한 경우, **별도 PDCA 사이클**로 분리합니다:
- 예: `wowa` feature = fullstack (frontendType: mobile), `admin` feature = fullstack (frontendType: web)

## Status Tracking

`.pdca-status.json` stores platform and phase per feature:

```json
{
  "features": {
    "{feature}": {
      "phase": "research | plan | design | do | analyze | iterate | completed | archived",
      "platform": "server | mobile | web | fullstack",
      "frontendType": "mobile | web",
      "startedAt": "ISO timestamp",
      "documents": {}
    }
  }
}
```

**IMPORTANT**:
- `platform` is determined during Plan phase by CTO and reused in all subsequent phases.
- `frontendType` is set when platform is `fullstack` to distinguish Mobile vs Web frontend agents.

---

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `research [feature]` | clarify → research-director | `/pdca research user-auth` |
| `plan [feature]` | PO → interactive-review → CTO routing | `/pdca plan user-auth` |
| `design [feature]` | Design docs (per platform) | `/pdca design user-auth` |
| `do [feature]` | CTO distribution → dev agents | `/pdca do user-auth` |
| `analyze [feature]` | Gap analysis + CTO review | `/pdca analyze user-auth` |
| `iterate [feature]` | Auto improvement | `/pdca iterate user-auth` |
| `report [feature]` | Completion report | `/pdca report user-auth` |
| `archive [feature]` | Archive documents | `/pdca archive user-auth` |
| `cleanup [feature]` | Cleanup archived | `/pdca cleanup` |
| `status` | Current status | `/pdca status` |
| `next` | Next phase guide | `/pdca next` |

---

## Phase Details

각 phase 실행 시 해당 파일을 Read하여 상세 절차를 따릅니다.

| Phase | File | Summary |
|-------|------|---------|
| **research** | `phases/research.md` | clarify → research-director (Decision Points) → CTO 통합 평가 (아키텍처+복잡도, BLOCK↔clarify 재호출) |
| **plan** | `phases/plan.md` | clarify → PO (Research Gate) ↔ CTO 타당성 스캔 (BLOCK→PO 재호출) → 사용자 승인 → CTO 라우팅 ↔ PO (Scope Mismatch→보완+재승인) |
| **design** | `phases/design.md` | 플랫폼별 디스패치 + tech-lead ↔ designer Pushback 루프 + API Contract 양방향 검증 (Fullstack) |
| **do** | `phases/do.md` | 선행조건 검증 → 설계 리뷰 → CTO work-plan → 사용자 승인 → 실행 모드 → 에이전트 구현 ↔ BLOCKED:QUESTIONS 프로토콜 |
| **analyze** | `phases/analyze.md` | gap-detector → FINDINGS 구조화 → 코드 리뷰 → CTO 통합 리뷰 |
| **iterate** | `phases/iterate.md` | FINDINGS severity 순 에이전트 디스패치 또는 Ralph Loop 자율 수정 |
| **report** | `phases/report.md` | report-generator → 배포/유지보수/v2 가이드 → CHANGELOG |
| **archive** | `phases/archive.md` | 문서 아카이브 → status 업데이트 |

---

### status (Status Check)

1. Read `.pdca-status.json`
2. Display: feature, phase, platform, matchRate, documents
3. Visualize progress

```
📊 PDCA Status
─────────────────────────────
Feature: {feature}
Platform: {platform}
Phase: {phase}
Match Rate: {matchRate}%
─────────────────────────────
[Research] ✅ → [Plan] ✅ → [Design] ✅ → [Do] 🔄 → [Check] ⏳ → [Act] ⏳
```

---

### next (Next Phase)

| Current | Next | Action |
|---------|------|--------|
| None | research (권장) 또는 plan | research는 선택적. 복잡한 기능은 research 권장, 단순 기능은 plan 직행 가능 |
| research | plan | PO → interactive-review → CTO routing |
| plan | design | Platform-based design agents |
| design | do | CTO distribution → dev agents |
| do | check | Gap analysis + CTO review |
| check (<90%) | act | Auto-iterate |
| check (>=90%) | report | Completion report |
| report | archive | Archive documents |

---

## Agent Integration Summary (All Bidirectional)

> `↔` = 양방향 (피드백 경로 있음), `──→` = 단방향 (최종 출력)
> 참조: `.claude/guide/agent-communication-protocol.md` — 전 phase 양방향 통신 프로토콜

```
Research: clarify (user) ──→ research-director (research.md + Decision Points)
                                       │
                                       ↓ CTO 통합 평가 (아키텍처 + 복잡도)
                                       │
                              BLOCK ↔ clarify 재호출 (max 2회)
                              CONCERN → AskUserQuestion
                                       │
                                       ↓ Decision Points → PO에게 전달
Plan:    PO (user-story.md) ↔ CTO (⓪-pre 타당성 스캔)
              │                        │ BLOCK → PO 재호출 (max 2회)
              │                        ↓ PASS/WARN
         interactive-review (사용자 승인) ──→ CTO (⓪ 플랫폼 라우팅)
                                                   │
                                       Scope Mismatch ↔ PO 보완 + 사용자 재승인
                                                   ↓ platform & frontendType stored
Design:  ┌── Server: tech-lead (server-brief)
         ├── Mobile: ui-ux-designer ↔ tech-lead (Design Pushback 루프, max 2회)
         │           └── frontend-design (Skill) 포함
         └── Web:    ui-ux-designer ↔ tech-lead (Design Pushback 루프, max 2회)
                     └── frontend-design (Skill) 포함
              │      Fullstack = Server + frontend (by frontendType)
              │      + API Contract 양방향 검증 (server tech-lead ↔ CTO ↔ frontend tech-lead)
              │
Do:      CTO (work-plan) ──→ developers (node/flutter/react)
              │                    ↔ BLOCKED:QUESTIONS → CTO 라우팅 → 답변자 → 재개
              │              OR: Ralph Loop (단일 에이전트 자율 반복)
              │
Analyze: gap-detector ↔ CTO (review)
              │
Iterate: pdca-iterator (if < 90%)  OR: Ralph Loop (FINDINGS 자율 수정)
              │
Report:  report-generator ──→ CHANGELOG
              │
Verify:  independent-reviewer (optional)
```

## Bidirectional Communication Reference

전 phase의 양방향 통신 프로토콜 상세는 아래 문서를 참조합니다:
- **통신 프로토콜**: `.claude/guide/agent-communication-protocol.md`
- **phase별 상세**: `phases/{phase}.md`

## CTO Involvement (5 Points)

| Phase | CTO Role | Output | 양방향 |
|-------|---------|--------|--------|
| **Research** (after research-director) | 아키텍처+복잡도 통합 평가 | PASS/CONCERN/BLOCK + complexity 판정 | BLOCK → clarify 재호출 |
| **Plan** (after PO, before user review) | ⓪-pre 타당성 스캔 | PASS/WARN/BLOCK 판정 | BLOCK → PO 재호출 |
| **Plan** (after user review) | ⓪ 플랫폼 라우팅 + Scope Mismatch 감지 | `platform` in status | Mismatch → PO 보완 + 재승인 |
| **Do** (before devs) | ② 작업 분배 + BLOCKED:QUESTIONS 라우팅 | work-plan.md (플랫폼별) | BLOCKED → 적절한 에이전트 라우팅 |
| **Analyze** (after gap) | ③ 통합 리뷰 | cto-review.md (플랫폼별) | — |
