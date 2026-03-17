---
name: vibe-coding-orchestrator
description: "**VIBE CODING ORCHESTRATOR v5.0** - 16개 AI 스킬 자동 조율 시스템. 비개발자도 프로급 코딩. 바이브 코딩에서 프로덕션까지. 4단계 성숙도 모델. 2025 현대 도구 통합."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
---

# Vibe Coding Orchestrator v5.0

**16개 AI 스킬을 자동으로 감지, 호출, 조율하는 마스터 오케스트레이터**

## v5.0 업데이트

### 신규 스킬 - Production Scale Launcher
- **production-scale-launcher**: 바이브 코딩 → 프로덕션 전환 가이드
  - 4단계 성숙도 모델 (MVP → Stable → Scalable → Enterprise)
  - Vercel/Supabase → AWS 마이그레이션 경로
  - 유료 서비스 필수 기능 (Stripe, 사용량 관리)
  - 비용 최적화 전략
  - SST (Ion) IaC 가이드

### v4.0 스킬 (유지)
- **project-architect**: 프로젝트 구조 설계 (레이어 분리, 기능 모듈화)
- **tech-stack-advisor**: 2025 현대적 기술 스택 선택 가이드
- **requirements-analyzer**: 요구사항 → 기술 스펙 변환
- **naming-convention-guard**: 네이밍 규칙 자동 적용
- **code-smell-detector**: 22가지 코드 스멜 탐지

### 2025 현대 도구 통합
- **Vitest**: Jest 대체 (30-70% 빠름)
- **Biome/Oxlint**: ESLint 대체 (15-100배 빠름)
- **Zustand/Jotai**: 상태관리 현대화
- **TanStack Query v5**: 서버 상태 필수
- **Orval**: OpenAPI → TypeScript 클라이언트 자동생성
- **React Hook Form + Zod**: 폼 검증 표준
- **Turborepo + pnpm**: 모노레포 표준
- **SST (Ion)**: AWS IaC 권장 (Claude Code 최적화)

## 스킬 레지스트리 (16개)

| Layer | Skills | 설명 |
|-------|--------|------|
| **Planning** | project-architect, tech-stack-advisor, requirements-analyzer | 시작 전 설계 |
| **Foundation** | codebase-graph, smart-context | 코드베이스 분석 |
| **Analysis** | impact-analyzer, arch-visualizer | 변경 영향도 |
| **Quality** | clean-code-mastery, tdd-guardian, security-shield | 코드 품질 |
| **Structure** | monorepo-architect, api-first-design | 구조 설계 |
| **Validation** | naming-convention-guard, code-smell-detector | 검증 |
| **Integration** | code-reviewer | 최종 리뷰 |
| **Production** | production-scale-launcher | 프로덕션 전환 |

## 비개발자 워크플로우

```yaml
새_프로젝트_시작:
  1. requirements-analyzer: "아이디어 → 기술 스펙"
  2. project-architect: "폴더 구조 설계"
  3. tech-stack-advisor: "기술 스택 선택"
  4. 코딩 시작

코드_작성_시:
  자동_적용:
    - clean-code-mastery: "SOLID/DRY/KISS"
    - naming-convention-guard: "네이밍 검증"
    - code-smell-detector: "스멜 탐지"
    - security-shield: "보안 검증"

코드_리뷰_시:
  1. code-reviewer: "통합 리뷰"
  2. tdd-guardian: "테스트 검증"

프로덕션_전환_시:
  1. production-scale-launcher: "성숙도 레벨 평가"
  2. 체크리스트_실행: "단계별 요구사항 확인"
  3. 마이그레이션_가이드: "AWS 전환 경로"
```

## Quick Commands v5.0

| Command | Action |
|---------|--------|
| vibe init | 새 프로젝트 (requirements → architect → stack) |
| vibe code | 코드 작성 (clean + naming + smell + security) |
| vibe review | 코드 리뷰 (전체 스킬 통합) |
| vibe stack | 2025 기술 스택 추천 |
| vibe test | TDD 가이드 (Vitest/Jest 선택) |
| vibe launch | 프로덕션 준비 체크 (production-scale-launcher) |
| vibe scale | AWS 마이그레이션 가이드 |
| vibe paid | 유료 서비스 전환 가이드 (Stripe, 사용량) |

## 4단계 성숙도 기반 스킬 체인

```yaml
Level_1_MVP:
  목표: "빠르게 작동 증명"
  활성_스킬:
    - requirements-analyzer
    - project-architect
    - tech-stack-advisor
  비활성: "품질 스킬 최소화 (속도 우선)"

Level_2_Stable:
  목표: "테스트됨, 안정적"
  추가_활성:
    - clean-code-mastery
    - code-smell-detector
    - tdd-guardian
    - security-shield
    - code-reviewer
  스킬_체인: "코드 작성 → 스멜 탐지 → 클린코드 → 리뷰"

Level_3_Scalable:
  목표: "확장 가능"
  추가_활성:
    - impact-analyzer
    - codebase-graph
    - monorepo-architect
    - production-scale-launcher
  스킬_체인: "영향 분석 → 구조 개선 → AWS 마이그레이션"

Level_4_Enterprise:
  목표: "보안/규정 준수"
  강화_활성:
    - security-shield (FULL)
    - arch-visualizer
  스킬_체인: "보안 감사 → 아키텍처 문서화"
```

## 스킬 실행 순서

```yaml
프로젝트_시작:
  1. requirements-analyzer → 요구사항 분석
  2. project-architect → 구조 설계
  3. tech-stack-advisor → 기술 선택

코드_작성:
  4. clean-code-mastery → 클린 코드
  5. naming-convention-guard → 네이밍
  6. security-shield → 보안

검증:
  7. code-smell-detector → 스멜 탐지
  8. tdd-guardian → 테스트
  9. code-reviewer → 최종 리뷰

프로덕션_전환:
  10. production-scale-launcher → 성숙도 평가
  11. 체크리스트 실행 → 단계별 요구사항
  12. AWS 마이그레이션 → SST 기반 배포
```

---

**Version**: 5.0.0 | **Skills**: 16 | **Updated**: 2025-12-10
**Focus**: 바이브 코딩 → 프로덕션, 4단계 성숙도 모델, 유료 서비스 런칭
