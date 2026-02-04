---
name: project-rule-generator
description: >
  프로젝트의 의존성, PRD, 구조를 분석하여 필수/선택 Rule을 자동 생성합니다.
  package.json, tsconfig.json 등 설정 파일과 문서를 분석하여
  기술 스택에 맞는 Claude Rules 구조를 구성합니다.
  "프로젝트 룰 생성", "규칙 자동 생성", "프로젝트 분석해서 룰 만들어줘" 요청 시 활성화.
argument-hint: "[project-path?]"
---

# Project Rule Generator

프로젝트를 종합 분석하여 `.claude/rules/` 구조를 자동으로 구성합니다.

## 핵심 원칙

1. **카테고리 기반 구조**: 기본적으로 규칙을 카테고리별로 그룹화하고 목차를 제공
2. **계층적 인덱스**: 루트 AGENTS.md에 카테고리별 목차 + 각 카테고리에 하위 인덱스
3. **최신 정보 반영**: 웹 검색으로 기술 스택의 최신 베스트 프랙티스 확인
4. **동적 규칙 생성**: 분석 결과를 기반으로 프로젝트에 맞는 규칙을 동적 생성

---

## 규칙 구조

### 기본 구조 (카테고리 기반)

**기본적으로 규칙을 카테고리별로 그룹화하고 목차를 제공합니다.**

```
.claude/rules/
├── AGENTS.md              # 전체 인덱스 + 카테고리 목차
├── CLAUDE.md              # "AGENTS.md"
│
│   # 카테고리별 그룹화 (기본)
├── core/                  # 핵심 규칙
│   ├── AGENTS.md          # 그룹 인덱스
│   ├── typescript.md
│   └── architecture.md
│
├── frontend/              # 프론트엔드 규칙
│   ├── AGENTS.md
│   ├── react.md
│   ├── state-management.md
│   └── components.md
│
├── testing/               # 테스트 규칙
│   ├── AGENTS.md
│   ├── unit.md
│   └── e2e.md
│
└── docs/                  # 문서 기반 규칙
    ├── AGENTS.md
    └── prd/
        ├── AGENTS.md
        └── overview.md
```

### 카테고리 분류 기준

| 카테고리 | 포함 규칙 | 예시 |
|----------|----------|------|
| `core/` | 전역 적용, 언어/타입 규칙 | typescript.md, architecture.md |
| `frontend/` | UI, 컴포넌트, 상태관리 | react.md, styling.md, state.md |
| `backend/` | API, DB, 서버 로직 | api.md, database.md, auth.md |
| `testing/` | 테스트 관련 | unit.md, integration.md, e2e.md |
| `docs/` | 문서 기반 규칙 | prd/, api-spec/ |
| `infra/` | 인프라, 배포 | docker.md, ci-cd.md |

### 루트 인덱스 목차 구조 (AGENTS.md)

```markdown
# {프로젝트명} Rules

> 프로젝트 규칙 인덱스

## 목차

- [핵심 규칙 (Core)](#핵심-규칙)
- [프론트엔드 (Frontend)](#프론트엔드)
- [백엔드 (Backend)](#백엔드)
- [테스트 (Testing)](#테스트)
- [문서 (Docs)](#문서)

---

## 핵심 규칙

> 모든 코드에 적용되는 기본 규칙

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [typescript](core/typescript.md) | `**/*.ts{,x}` | TypeScript 컨벤션 |
| [architecture](core/architecture.md) | 전역 | 프로젝트 구조 원칙 |

→ 상세: [core/AGENTS.md](core/AGENTS.md)

---

## 프론트엔드

> UI 및 컴포넌트 관련 규칙

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [react](frontend/react.md) | `**/*.tsx` | React 패턴 |
| [components](frontend/components.md) | `**/components/**` | 컴포넌트 구조 |

→ 상세: [frontend/AGENTS.md](frontend/AGENTS.md)

---

## 테스트

> 테스트 작성 관련 규칙

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [unit](testing/unit.md) | `**/*.test.*` | 단위 테스트 |
| [e2e](testing/e2e.md) | `e2e/**` | E2E 테스트 |

→ 상세: [testing/AGENTS.md](testing/AGENTS.md)
```

### 그룹 인덱스 (카테고리별 AGENTS.md)

```markdown
# {카테고리명} Rules

> {카테고리 설명}

## 규칙 목록

| 규칙 | 설명 | 트리거 |
|------|------|--------|
| [rule-a](rule-a.md) | 설명 | `**/*.tsx` |
| [rule-b](rule-b.md) | 설명 | 컴포넌트 작성 시 |

## 빠른 참조

### {주요 개념 1}
- 핵심 포인트 1
- 핵심 포인트 2

### {주요 개념 2}
- 핵심 포인트 1
```

### 플랫 구조 (예외: 규칙 2-3개)

규칙이 매우 적은 경우에만 플랫 구조 허용:

```
.claude/rules/
├── AGENTS.md
├── CLAUDE.md
├── typescript.md
└── architecture.md
```

---

## 실행 단계

### 1단계: 프로젝트 분석

| 분석 대상 | 추출 정보 | 우선순위 |
|----------|----------|---------|
| 의존성 파일 | 기술 스택, 프레임워크, 도구, **버전** | 필수 |
| PRD/기획 문서 | 도메인 컨텍스트, 비즈니스 규칙 | 선택 |
| 프로젝트 구조 | 아키텍처 패턴, 디렉토리 컨벤션 | 필수 |
| 설정 파일 | 코딩 컨벤션, 린터 규칙 | 선택 |

#### 1.1 의존성 파일 분석

```
package.json → JavaScript/TypeScript 기술 스택
requirements.txt / pyproject.toml → Python 기술 스택
Cargo.toml → Rust 기술 스택
go.mod → Go 기술 스택
```

**추출 항목:**
- 런타임 및 **버전**: Node.js 20.x, Python 3.12 등
- 프레임워크 및 **버전**: React 19, Next.js 15, NestJS 10 등
- 빌드/테스트/린터 도구
- **신규 도구 감지**: React Compiler, Turbopack 등

#### 1.2 PRD/문서 분석

```
docs/PRD*.md, README.md, ARCHITECTURE.md, docs/*.md
```

#### 1.3 프로젝트 구조 분석

```
src/ 또는 app/ 구조 → 아키텍처 패턴 파악
```

---

### 2단계: 최신 베스트 프랙티스 검색 (WebSearch)

> 분석된 기술 스택과 버전을 기반으로 **웹 검색을 수행**하여 최신 정보를 확인합니다.

| 기술 스택 | 검색 쿼리 예시 |
|----------|---------------|
| React 19 | `"React 19 best practices 2025"`, `"React Compiler migration"` |
| Next.js 15 | `"Next.js 15 App Router best practices"` |

**확인 사항:**
- deprecated된 패턴 (예: React Compiler 사용 시 useMemo 불필요)
- 새로운 권장 패턴
- 보안 관련 업데이트

---

### 3단계: 규칙 분류 및 구조 결정

#### 3.1 필수 vs 선택 분류

```
[분석 결과]
    │
    ├─── 필수 규칙 (Essential)
    │    ├── 기술 스택 규칙 (typescript.md, react.md)
    │    ├── 프로젝트 구조 규칙 (architecture.md)
    │    └── 코딩 컨벤션 (coding-style.md)
    │
    └─── 선택 규칙 (Conditional)
         ├── 도메인 규칙 - paths 또는 트리거 키워드
         ├── 테스트 규칙 - paths: ["**/*.test.*"]
         └── 특정 모듈 규칙
```

#### 3.2 카테고리 분류

**기본적으로 모든 규칙을 카테고리별로 그룹화합니다.**

```
[분석된 규칙들]
    │
    ├─── 언어/타입/전역 규칙
    │    → core/ 카테고리
    │
    ├─── UI/컴포넌트/상태관리
    │    → frontend/ 카테고리
    │
    ├─── API/DB/서버 로직
    │    → backend/ 카테고리
    │
    ├─── 테스트 관련
    │    → testing/ 카테고리
    │
    ├─── 문서 기반 (PRD, 스펙)
    │    → docs/ 카테고리
    │
    └─── 인프라/배포
         → infra/ 카테고리
```

**카테고리별 규칙 예시:**

| 카테고리 | 포함 규칙 | paths 예시 |
|----------|----------|-----------|
| `core/` | typescript.md, architecture.md, coding-style.md | `**/*.ts{,x}` |
| `frontend/` | react.md, state.md, components.md, styling.md | `**/*.tsx`, `**/components/**` |
| `backend/` | api.md, database.md, auth.md, validation.md | `**/api/**`, `**/services/**` |
| `testing/` | unit.md, integration.md, e2e.md | `**/*.test.*`, `e2e/**` |
| `docs/` | prd/, api-spec/, onboarding.md | 문서 참조 시 |
| `infra/` | docker.md, ci-cd.md, deployment.md | `Dockerfile`, `.github/**` |

**예외: 규칙이 2-3개인 경우 플랫 구조 허용**

---

### 4단계: 긴 문서 구조화 (rule-structurizer 연계)

PRD나 긴 가이드 문서는 `rule-structurizer` 스킬을 활용합니다.

#### 사전 확인

```
rule-structurizer 스킬 확인:
├── 존재함 → /rule-structurizer 호출
└── 없음 → 사용자에게 안내
```

#### 스킬 없을 경우 안내 메시지

```
⚠️ rule-structurizer 스킬이 필요합니다.

긴 문서(PRD, 가이드 등)를 규칙 구조로 변환하려면 
rule-structurizer 스킬을 설치하세요:

설치 방법:
1. ai-library 저장소에서 skills/rule-structurizer/ 복사
2. 프로젝트의 .claude/skills/ 또는 ~/.claude/skills/에 배치

또는 수동으로 그룹화 디렉토리를 생성하세요:
- AGENTS.md: 그룹 인덱스
- 섹션별 개별 .md 파일
```

---

### 5단계: 구조 생성 및 검증

#### 생성 구조 예시 (카테고리 기반)

```
.claude/rules/
├── AGENTS.md                 # 전체 인덱스 + 목차
├── CLAUDE.md
│
├── core/                     # 핵심 규칙 카테고리
│   ├── AGENTS.md             # 카테고리 인덱스
│   ├── typescript.md
│   ├── architecture.md
│   └── coding-style.md
│
├── frontend/                 # 프론트엔드 카테고리
│   ├── AGENTS.md
│   ├── react.md
│   ├── state-management.md
│   ├── components.md
│   └── styling.md
│
├── backend/                  # 백엔드 카테고리 (있는 경우)
│   ├── AGENTS.md
│   ├── api.md
│   └── database.md
│
├── testing/                  # 테스트 카테고리
│   ├── AGENTS.md
│   ├── unit.md
│   └── e2e.md
│
└── docs/                     # 문서 기반 카테고리
    ├── AGENTS.md
    └── prd/
        ├── AGENTS.md
        ├── overview.md
        ├── user-stories.md
        └── functional-specs.md
```

#### 루트 인덱스 (AGENTS.md) 작성 - 목차 포함

```markdown
# {프로젝트명} Rules

> 프로젝트 규칙 인덱스

## 목차

- [핵심 규칙 (Core)](#핵심-규칙-core)
- [프론트엔드 (Frontend)](#프론트엔드-frontend)
- [백엔드 (Backend)](#백엔드-backend)
- [테스트 (Testing)](#테스트-testing)
- [문서 (Docs)](#문서-docs)

---

## 핵심 규칙 (Core)

> 모든 코드에 적용되는 기본 규칙

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [typescript](core/typescript.md) | `**/*.ts{,x}` | TypeScript 컨벤션 |
| [architecture](core/architecture.md) | 전역 | 아키텍처 원칙 |
| [coding-style](core/coding-style.md) | 전역 | 코딩 스타일 |

→ 상세: [core/AGENTS.md](core/AGENTS.md)

---

## 프론트엔드 (Frontend)

> UI, 컴포넌트, 상태관리 규칙

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [react](frontend/react.md) | `**/*.tsx` | React 패턴 |
| [components](frontend/components.md) | `**/components/**` | 컴포넌트 구조 |
| [styling](frontend/styling.md) | `**/*.css` | 스타일링 규칙 |

→ 상세: [frontend/AGENTS.md](frontend/AGENTS.md)

---

## 테스트 (Testing)

> 테스트 작성 규칙 (조건부 활성화)

| 규칙 | 적용 대상 | 설명 |
|------|----------|------|
| [unit](testing/unit.md) | `**/*.test.*` | 단위 테스트 |
| [e2e](testing/e2e.md) | `e2e/**` | E2E 테스트 |

→ 상세: [testing/AGENTS.md](testing/AGENTS.md)

---

## 문서 (Docs)

> PRD, API 스펙 등 문서 기반 규칙

| 문서 | 설명 | 참조 |
|------|------|------|
| [PRD](docs/prd/) | 제품 요구사항 | 기획 참조 시 |

→ 상세: [docs/AGENTS.md](docs/AGENTS.md)
```

#### 검증 체크리스트

```
구조 검증:
□ 루트 AGENTS.md에 목차가 있는가?
□ 규칙이 적절한 카테고리에 분류되었는가?
□ 각 카테고리에 AGENTS.md 인덱스가 있는가?
□ 각 규칙 파일에 frontmatter(description)가 있는가?

목차 검증:
□ 목차의 링크가 해당 섹션으로 연결되는가?
□ 각 카테고리 섹션에 "→ 상세" 링크가 있는가?
□ 카테고리별 대표 규칙이 테이블에 표시되는가?

내용 검증:
□ 규칙이 최신 베스트 프랙티스를 반영하는가?
□ 기존 린터/설정과 충돌하지 않는가?
□ deprecated 패턴이 권장되고 있지 않은가?

카테고리 검증:
□ 규칙이 적절한 카테고리에 배치되었는가?
□ 카테고리 인덱스가 하위 규칙을 명확히 안내하는가?
□ 빈 카테고리가 없는가? (최소 1개 규칙)
```

---

## 규칙 생성 원칙

### 1. 프로젝트 특성 우선

```
# 좋은 예
"이 프로젝트는 Feature 기반 구조를 사용합니다."
"React Compiler가 활성화되어 있어 수동 메모이제이션이 불필요합니다."

# 피해야 할 예
"React에서는 useMemo를 사용하세요." (← 버전/설정에 따라 다름)
```

### 2. 기존 설정 존중

```
# 린터 설정이 있는 경우
"상세 규칙은 eslint.config.js 참조"
"Biome 설정(biome.json)이 포맷팅을 담당"
```

### 3. 버전 명시

```yaml
---
description: >
  Next.js 15 App Router 규칙. 
  주의: Next.js 14 이하와 캐싱 전략이 다름.
---
```

---

## 상세 참조

- [분석 가이드](references/analysis-guide.md) - 프로젝트 분석 상세 방법론
- [인덱싱 가이드](references/indexing-guide.md) - 필수/선택 규칙 인덱싱 전략
- [규칙 생성 가이드](references/rule-generation-guide.md) - 동적 규칙 생성 상세
