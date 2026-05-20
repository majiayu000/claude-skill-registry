---
name: readme-for-developers
description: Write developer-oriented README as onboarding documentation. Use when creating/updating README, setting up new projects, or when new developers need to understand the codebase quickly. README = Entry point + Architecture overview + Working agreement.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# README for Developers

**개발자를 위한 README**는 마케팅 문서가 아니라 **'인계인수서'**입니다.
이 문서 하나만 보고도 신규 개발자가 로컬 서버를 띄우고, 코드 흐름을 머릿속에 그릴 수 있어야 합니다.

## Core Principle

> **"README = 지도, 디테일은 docs/로 링크"**
>
> 정보를 한 파일에 다 넣지 말고, README가 전체 지도를 제공하고 세부는 링크로 내려가게 한다.

## README 품질 체크리스트

README만 읽고 새 개발자가 아래 질문에 답할 수 있으면 합격:

- [ ] 이 시스템의 **목표/비목표**는?
- [ ] 데이터는 어디에 저장되고, **핵심 식별자**는?
- [ ] **핵심 플로우 2~3개**는 어떻게 동작하는가?
- [ ] **엔트리포인트 파일 3개**는 어디인가?
- [ ] 자주 터지는 버그의 **관측 지점**은?
- [ ] **CI는 무엇을 어떤 순서로** 강제하는가?
- [ ] **배포/롤백**은 어떻게 하는가?
- [ ] **로컬 실행 3단계**는?

---

## 필수 섹션 구조

### 0) New Engineer Fast Path (30분 코스)

```markdown
## 0) New Engineer Fast Path
- ✅ 1) 시스템 한 장 요약 → '1) System at a glance'
- ✅ 2) 로컬 실행 → '4) Local Dev'
- ✅ 3) 핵심 플로우 2개 → '2) Core Flows'
- ✅ 4) 디버깅 포인트 → '8) Debugging'
- ✅ 5) 첫 작업 가이드 → '10) Working Agreement'
```

### 1) System at a glance

```markdown
## 1) System at a glance

### What / Why
- **목표**:
- **비목표** (안 하는 것):
- **사용자/고객**:
- **성공지표**:

### Architecture
(Mermaid 다이어그램 또는 이미지)

### Design Principles (3~5개)
- SSOT 우선
- 안전 기본값
- 점진적 로드
- 결정 기록 (ADR)
```

### 2) Core Flows (핵심 동작 2~3개)

```markdown
## 2) Core Flows

### Flow A: <예: Preview Render>
- **입력**:
- **처리 단계**:
- **출력**:
- **주요 코드 위치**:
- **자주 터지는 지점**:

### Flow B: <예: Video Export>
(동일 포맷)
```

### 3) Repo Map (폴더 구조)

```markdown
## 3) Repo Map

\`\`\`
/app          # Next.js App Router
/src          # 소스 코드
  /components # 공용 UI 컴포넌트
  /features   # 기능별 모듈
  /lib        # 유틸리티
/scripts      # 빌드/배포 스크립트
/docs         # 상세 문서
\`\`\`

- **엔트리포인트**: `app/page.tsx`
- **상태/도메인 핵심**: `src/features/`
- **파이프라인**: `src/lib/pipeline/`
```

### 4) Local Dev (로컬 개발)

```markdown
## 4) Local Dev

### Prerequisites
- Node.js: v20+
- Package manager: pnpm
- OS 이슈: (있으면 명시)

### Setup
\`\`\`bash
# 1. 의존성 설치
pnpm install

# 2. 환경변수
cp .env.example .env.local
# 필요한 값 채우기

# 3. 실행
pnpm dev
\`\`\`

### Common Commands
| 명령어 | 설명 |
|--------|------|
| `pnpm dev` | 개발 서버 |
| `pnpm test` | 테스트 |
| `pnpm build` | 빌드 |
| `pnpm lint` | 린트 |
```

### 5) Configuration & Secrets

```markdown
## 5) Configuration & Secrets

| 변수명 | 용도 | 예시 | 필수 | 노출금지 |
|--------|------|------|------|----------|
| `DATABASE_URL` | DB 연결 | `postgresql://...` | ✅ | ✅ |
| `NEXT_PUBLIC_API_URL` | API 주소 | `https://api.example.com` | ✅ | ❌ |

### 시크릿 관리
- **로컬**: `.env.local` (gitignore)
- **CI**: GitHub Secrets
- **프로덕션**: Vercel/AWS Secrets Manager
```

### 6) Data Model / Storage

```markdown
## 6) Data Model

### 핵심 테이블
| 테이블 | 설명 | 핵심 필드 |
|--------|------|----------|
| users | 사용자 | id, email, created_at |
| projects | 프로젝트 | id, user_id, name |

### Storage
- S3: `s3://bucket/projects/{project_id}/`
- 업로드 규칙: ...

### Migration
\`\`\`bash
pnpm db:migrate
\`\`\`
```

### 7) CI/CD & Release

```markdown
## 7) CI/CD

### Pipeline
1. `validate` - 린트, 타입체크
2. `test` - 유닛/통합 테스트
3. `build` - 프로덕션 빌드
4. `deploy` - 배포

### 배포 트리거
- `main` → Production
- `develop` → Staging
- PR → Preview

### 롤백
\`\`\`bash
vercel rollback
\`\`\`
```

### 8) Debugging & Observability

```markdown
## 8) Debugging

### 로그 보는 법
- **로컬**: 콘솔 + React DevTools
- **서버**: Vercel Logs / CloudWatch

### 자주 보는 대시보드
- [Vercel Analytics](링크)
- [Sentry](링크)

### 트러블슈팅 TOP 5
| 증상 | 원인 | 해결 |
|------|------|------|
| DB 연결 실패 | Docker 미실행 | `docker-compose up -d` |
| 빌드 실패 | 타입 에러 | `pnpm tsc --noEmit` |
```

### 9) Security

```markdown
## 9) Security

### 권한 모델
- 인증: NextAuth.js
- 권한: Role-based (admin, user)

### allowed-tools (스킬 시스템)
- 스킬별 도구 제한 정책

### 취약점 신고
→ [SECURITY.md](./SECURITY.md)
```

### 10) Working Agreement

```markdown
## 10) Working Agreement

### 브랜치 전략
- `main` - 프로덕션
- `develop` - 개발 통합
- `feature/*` - 기능 개발
- `hotfix/*` - 긴급 수정

### PR 규칙
- 최소 1명 리뷰어 승인
- CI 통과 필수
- PR 템플릿 사용

### 코드 스타일
- ESLint + Prettier
- 파일당 200줄 권장, 300줄 제한

### ADR (결정 기록)
→ `/docs/adr/`
```

### 11) Docs Index

```markdown
## 11) Docs Index

- [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- [RUNBOOK.md](./docs/RUNBOOK.md)
- [ADRs](./docs/adr/)
- [API 문서](./docs/api/)
- [Skills](./docs/skills/)
```

---

## Mermaid 아키텍처 예시

```markdown
\`\`\`mermaid
graph LR
    Browser[Browser] --> NextJS[Next.js App]
    NextJS --> API[API Routes]
    API --> DB[(PostgreSQL)]
    API --> S3[(S3 Storage)]
    API --> External[External APIs]

    Worker[Background Worker] --> DB
    Worker --> S3
\`\`\`
```

---

## Anti-patterns

```
❌ 마케팅 문구만 있음
   "혁신적인 AI 기반 솔루션..."
   → 개발자에게 무의미

❌ 실행 방법 없음
   "설치 후 실행하세요"
   → 복사-붙여넣기 가능해야 함

❌ 구조 설명 없음
   폴더만 나열
   → 각 폴더 역할 설명 필수

❌ 환경변수 설명 없음
   .env.example만 존재
   → 각 변수 의미/예시 필수

❌ 한 파일에 모든 것
   README가 1000줄+
   → docs/로 분리하고 링크
```

## Workflow

### 1. 프로젝트 분석

```bash
# 폴더 구조 확인
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git

# package.json 확인
cat package.json | head -30

# 환경변수 확인
cat .env.example
```

### 2. README 초안 작성

위 11개 섹션 구조에 맞춰 작성

### 3. 체크리스트 검증

신규 개발자 관점에서 8개 질문에 답할 수 있는지 확인

---

## References

- [Diátaxis Documentation Framework](https://diataxis.fr)
- [The Good Docs Project](https://thegooddocsproject.dev)
- [GitHub Developer Onboarding](https://github.com/readme/guides/developer-onboarding)
