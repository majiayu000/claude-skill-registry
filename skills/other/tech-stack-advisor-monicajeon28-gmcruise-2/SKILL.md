---
name: tech-stack-advisor
description: "**TECH STACK ADVISOR** - '기술 스택', '프레임워크 추천', 'DB 뭐 쓸까', '어떤 기술', '스택 선택', '뭘로 만들까' 요청 시 자동 발동. 비개발자 친화적 기술 선택 가이드. 유지보수성, 확장성, 학습 곡선 고려한 추천."
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
---

# Tech Stack Advisor Skill v1.0

**기술 스택 선택 가이드** - 비개발자도 올바른 기술 선택 가능

## 핵심 철학

```yaml
Core_Philosophy:
  원칙: "못으로 나사 박지 마라"
  목표: "프로젝트에 맞는 최적의 기술 조합 추천"
  
  고려_요소:
    1순위: "팀 역량과 학습 곡선"
    2순위: "장기 유지보수 가능성"
    3순위: "커뮤니티와 생태계"
    4순위: "성능과 확장성"
    5순위: "비용"
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  Keywords_KO:
    - "기술 스택", "스택 추천"
    - "프레임워크 추천", "뭘로 만들까"
    - "DB 뭐 쓸까", "데이터베이스 선택"
    - "어떤 기술 써야", "기술 선택"
    - "호스팅 어디", "배포 어디서"
    
  Keywords_EN:
    - "tech stack", "stack recommendation"
    - "which framework", "what to use"
    - "database choice", "hosting options"
```

## 선택적 문서 로드 전략

```yaml
Document_Loading_Strategy:
  Always_Load:
    - "core/decision-matrix.md"
    - "core/non-dev-friendly.md"
    
  Category_Specific_Load:
    Frontend: "stacks/frontend.md"
    Backend: "stacks/backend.md"
    Database: "stacks/database.md"
    Hosting: "stacks/hosting.md"
```

## 프로젝트 규모별 권장 스택

### Small Project (MVP, 사이드 프로젝트)

```yaml
규모: "1-5 페이지, 1-2명"
예산: "무료~월 $20"

권장_스택:
  프론트엔드: "Next.js (App Router)"
  백엔드: "Next.js API Routes 또는 Supabase"
  데이터베이스: "Supabase (PostgreSQL)"
  인증: "Supabase Auth 또는 NextAuth"
  호스팅: "Vercel (무료)"
  CSS: "Tailwind CSS"
```

### Medium Project (스타트업, 소규모 서비스)

```yaml
규모: "10-50 페이지, 3-10명"
예산: "월 $50-500"

권장_스택:
  프론트엔드: "Next.js 또는 React + Vite"
  백엔드: "NestJS 또는 FastAPI"
  데이터베이스: "PostgreSQL (Supabase/Neon)"
  캐시: "Redis (Upstash)"
  인증: "Auth0 또는 Clerk"
  호스팅: "Vercel + Railway/Render"
```

## 비개발자 친화도 등급

```yaml
Beginner_Friendly:
  설명: "코딩 경험 거의 없어도 가능"
  추천:
    - "Supabase (백엔드 + DB + 인증)"
    - "Vercel (배포)"
    - "Next.js (문서 최고)"
    - "Tailwind CSS (직관적)"

Advanced_Required:
  설명: "상당한 개발 경험 필요"
  주의:
    - "Kubernetes (운영 복잡)"
    - "GraphQL (설계 복잡)"
    - "마이크로서비스 (오버엔지니어링 위험)"
```

## 카테고리별 추천

### 프론트엔드

| 순위 | 기술 | 장점 | 적합 |
|-----|------|------|------|
| 1 | Next.js | 풀스택, SEO, 문서 풍부 | 대부분 |
| 2 | React+Vite | 빠름, 유연함 | SPA |
| 3 | Vue | 학습 쉬움 | 프로토타입 |

### 백엔드

| 순위 | 기술 | 장점 | 적합 |
|-----|------|------|------|
| 1 | Supabase | 코드 불필요, 인증 내장 | MVP |
| 2 | Next.js API | 프론트와 통합 | 소규모 |
| 3 | NestJS | 구조적, 타입 안전 | 중대규모 |

### 데이터베이스

| 순위 | 기술 | 장점 | 적합 |
|-----|------|------|------|
| 1 | Supabase PostgreSQL | 무료, GUI 있음 | 대부분 |
| 2 | PlanetScale | 브랜칭, 확장성 | 대규모 |
| 3 | Neon | 서버리스 | 서버리스 |

피해야 할 것:
- MongoDB (스키마 없음 - 장기적 혼란)
- Firebase Firestore (비용 예측 어려움)

### 호스팅

| 순위 | 기술 | 장점 | 비용 |
|-----|------|------|------|
| 1 | Vercel | 배포 최고 쉬움 | 무료~ |
| 2 | Railway | 백엔드 쉬움 | $5/월~ |
| 3 | Cloudflare | 무료 넉넉함 | 무료 |

## 검증된 스택 조합

### Indie Hacker Stack (비개발자 최적)

```yaml
대상: "1인 개발, MVP, 사이드 프로젝트"

구성:
  - Next.js 15 (App Router)
  - Supabase (백엔드 + DB + 인증)
  - Tailwind CSS + shadcn/ui
  - Vercel (배포)
  - Vitest (테스트 - Jest보다 4배 빠름)
  - Biome (린팅 - ESLint보다 15배 빠름)
  - Zustand (상태관리 - Redux보다 간단)

장점:
  - 코드량 최소화
  - 월 비용 $0-25
  - 배포 자동화
  - 2025 최신 도구 스택

시작:
  npx create-next-app@latest my-app --typescript --tailwind --app
  npx supabase init
```

### Startup Scale Stack

```yaml
대상: "빠른 성장이 예상되는 서비스"

구성:
  - Next.js 15 + TanStack Query v5
  - NestJS + Prisma
  - PostgreSQL (Supabase/Neon)
  - Redis (Upstash)
  - Clerk (인증)
  - Vercel + Railway
  - Orval (OpenAPI → TypeScript 클라이언트 자동생성)
  - React Hook Form + Zod (폼 검증)
  - Turborepo + pnpm (모노레포)

비용: "$50-200/월"
```

### 2025 Modern Tool Stack

```yaml
Testing:
  Vitest:
    장점: "Jest보다 30-70% 빠름, Vite 통합, ESM 네이티브"
    다운로드: "2M+/week"
    권장: "새 프로젝트는 Vitest 사용"

  Jest:
    장점: "안정적, 레퍼런스 많음"
    권장: "기존 프로젝트, React Native"

Linting:
  Biome:
    장점: "ESLint+Prettier 대체, 15-20배 빠름, 설정 간단"
    기능: "린팅 + 포맷팅 통합"
    타입_지원: "85% typescript-eslint 커버리지"
    권장: "새 프로젝트"

  ESLint_Enterprise:
    권장: "AIRUDA Enterprise Grade ESLint config (우수사례)"
    경로: "C:\\Users\\lpian\\OneDrive\\문서\\tsconfig\\eslint.config.mjs"
    특징: "type-aware rules, Brain 커스텀 룰, 모든 프로젝트 적용 가능"

  Oxlint:
    장점: "ESLint보다 50-100배 빠름, 520+ 룰"
    주의: "포맷팅 없음, 아직 타입 인식 룰 미지원"
    권장: "대규모 프로젝트 초기 린팅"

State_Management:
  Zustand:
    장점: "3KB, 보일러플레이트 없음, Redux 대체"
    적합: "중대규모 앱, 전역 상태"

  Jotai:
    장점: "아토믹 모델, 세밀한 리렌더링 제어"
    적합: "폼, 에디터, 복잡한 UI 상태"

  TanStack_Query:
    장점: "서버 상태 전용, 캐싱 자동화"
    필수: "API 데이터는 반드시 TanStack Query로"

Form_Validation:
  React_Hook_Form_Zod:
    장점: "타입 안전, 스키마 재사용, 성능 최적화"
    조합: "react-hook-form + @hookform/resolvers + zod"
    권장: "모든 폼에 기본 적용"

API_Client:
  Orval:
    장점: "OpenAPI → TypeScript + TanStack Query 훅 자동생성"
    기능: "MSW mock, Zod 스키마 통합"
    다운로드: "500K+/week"
    권장: "API-First 개발 필수"

Monorepo:
  Turborepo_pnpm:
    장점: "캐싱으로 CI 시간 90% 단축"
    구성: "pnpm workspace + turbo.json"
    권장: "3개 이상 패키지면 도입"
```

## 기술 선택 체크리스트

```markdown
### 팀 역량
[ ] 팀원들이 이 기술을 사용해본 적 있는가?
[ ] 학습 시간을 투자할 여유가 있는가?

### 프로젝트 적합성
[ ] 프로젝트 규모에 맞는 복잡도인가?
[ ] 오버엔지니어링은 아닌가?

### 장기 유지보수
[ ] 5년 후에도 지원될 기술인가?
[ ] 커뮤니티가 활발한가?

### 비용
[ ] 예상 비용을 계산했는가?
[ ] 무료 티어로 시작 가능한가?
```

## Quick Commands

| 명령 | 동작 |
|-----|------|
| stack recommend | 대화형 스택 추천 |
| stack compare A B | 두 기술 비교 |
| stack cost | 예상 비용 계산 |

---

**Version**: 1.0.0
**Dependencies**: project-architect, requirements-analyzer
