---
name: project-architect
description: "**PROJECT ARCHITECT** - '새 프로젝트', '프로젝트 시작', '폴더 구조', '아키텍처 설계', '구조 잡아줘', '프로젝트 세팅' 요청 시 자동 발동. 프로 개발자 수준의 확장 가능한 프로젝트 구조 설계. 레이어 분리, 모듈화, 베스트 프랙티스 적용."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Project Architect Skill v1.0

**프로젝트 설계 마스터** - 시작부터 확장 가능한 구조로 설계

## 핵심 철학

```yaml
Core_Philosophy:
  원칙: "집 짓기 전에 설계도 먼저"
  목표: "비개발자도 프로 개발자 수준의 구조로 시작"
  
  Anti_Patterns_Prevention:
    - ❌ 모든 코드가 한 파일에 (God File)
    - ❌ 폴더 없이 루트에 파일 나열
    - ❌ 비즈니스 로직과 UI 코드 혼재
    - ❌ 설정값 하드코딩
    - ❌ 테스트 없는 구조
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  Keywords_KO:
    - "새 프로젝트", "프로젝트 시작"
    - "폴더 구조", "디렉토리 구조"
    - "아키텍처 설계", "구조 설계"
    - "프로젝트 세팅", "초기 설정"
    - "뼈대 잡아줘", "구조 잡아줘"
    - "보일러플레이트", "스캐폴딩"
    
  Keywords_EN:
    - "new project", "project setup"
    - "folder structure", "directory structure"
    - "architecture design", "scaffolding"
    - "boilerplate", "project skeleton"
    
  File_Events:
    - "package.json 없는 빈 디렉토리 진입"
    - "신규 프로젝트 생성 요청"
```

## 선택적 문서 로드 전략

```yaml
Document_Loading_Strategy:
  Always_Load:
    - "core/universal-principles.md"   # 공통 원칙
    - "core/layer-separation.md"       # 레이어 분리
    
  Project_Type_Load:
    Web_Frontend: "templates/frontend.md"
    Web_Backend: "templates/backend.md"
    Fullstack: "templates/fullstack.md"
    API_Server: "templates/api-server.md"
    CLI_Tool: "templates/cli.md"
    Library: "templates/library.md"
    Monorepo: "templates/monorepo.md"
    
  Framework_Specific_Load:
    Next.js: "frameworks/nextjs.md"
    React: "frameworks/react.md"
    Vue: "frameworks/vue.md"
    NestJS: "frameworks/nestjs.md"
    FastAPI: "frameworks/fastapi.md"
    Express: "frameworks/express.md"
    Django: "frameworks/django.md"
```

## 핵심 원칙

### 1. 레이어 분리 (Layer Separation)

```yaml
Layer_Architecture:
  Presentation_Layer:
    역할: "사용자 인터페이스"
    포함: "pages, components, views, layouts"
    규칙: "비즈니스 로직 금지, UI만"
    
  Business_Layer:
    역할: "비즈니스 로직"
    포함: "services, usecases, domain"
    규칙: "UI/DB 직접 접근 금지"
    
  Data_Layer:
    역할: "데이터 접근"
    포함: "repositories, api, database"
    규칙: "데이터 소스 추상화"
    
  Shared_Layer:
    역할: "공유 유틸리티"
    포함: "utils, helpers, constants, types"
    규칙: "의존성 최소화"
```

### 2. 기능별 모듈화 (Feature-Based Modularity)

```yaml
Module_Structure:
  방식: "기능별로 관련 파일 그룹화"
  
  Before_Bad:
    components/
      Button.tsx
      UserCard.tsx
      ProductCard.tsx
    hooks/
      useUser.ts
      useProduct.ts
    services/
      userService.ts
      productService.ts
      
  After_Good:
    features/
      user/
        components/UserCard.tsx
        hooks/useUser.ts
        services/userService.ts
        types/user.types.ts
        index.ts  # Public exports
      product/
        components/ProductCard.tsx
        hooks/useProduct.ts
        services/productService.ts
        types/product.types.ts
        index.ts
    shared/
      components/Button.tsx
      utils/helpers.ts
```

### 3. 설정 외부화 (Configuration Externalization)

```yaml
Config_Management:
  환경별_분리:
    .env.local: "로컬 개발 (git 무시)"
    .env.development: "개발 환경"
    .env.production: "프로덕션 환경"
    .env.example: "템플릿 (git 포함)"
    
  설정_구조:
    config/
      index.ts      # 설정 진입점
      database.ts   # DB 설정
      auth.ts       # 인증 설정
      api.ts        # API 설정
      constants.ts  # 상수
      
  절대_금지:
    - ❌ 코드에 API 키 직접 입력
    - ❌ 하드코딩된 URL
    - ❌ 매직 넘버 (의미 없는 숫자)
```

### 4. 명확한 진입점 (Clear Entry Points)

```yaml
Entry_Points:
  규칙: "각 모듈은 index.ts로 public API 노출"
  
  예시:
    features/user/index.ts: |
      // Public exports only
      export { UserCard } from './components/UserCard';
      export { useUser } from './hooks/useUser';
      export type { User } from './types/user.types';
      // Internal implementations are NOT exported
      
  Import_규칙:
    Good: "import { UserCard } from '@/features/user';"
    Bad: "import { UserCard } from '@/features/user/components/UserCard';"
```

## 프로젝트 타입별 구조 템플릿

### Next.js Fullstack (권장)

```
my-project/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # 인증 필요 페이지 그룹
│   │   ├── (public)/          # 공개 페이지 그룹
│   │   ├── api/               # API Routes
│   │   ├── layout.tsx         # Root Layout
│   │   └── page.tsx           # Home Page
│   │
│   ├── features/              # 기능별 모듈
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   ├── types/
│   │   │   └── index.ts
│   │   └── [feature-name]/
│   │
│   ├── shared/                # 공유 모듈
│   │   ├── components/        # 공통 UI 컴포넌트
│   │   │   ├── ui/           # 기본 UI (Button, Input)
│   │   │   └── layout/       # 레이아웃 컴포넌트
│   │   ├── hooks/            # 공통 훅
│   │   ├── utils/            # 유틸리티 함수
│   │   ├── types/            # 공통 타입
│   │   └── constants/        # 상수
│   │
│   ├── services/              # 외부 서비스 연동
│   │   ├── api/              # API 클라이언트
│   │   ├── database/         # DB 연결
│   │   └── external/         # 외부 API (결제, 이메일 등)
│   │
│   └── config/               # 설정
│       ├── index.ts
│       └── env.ts
│
├── public/                    # 정적 파일
├── tests/                     # 테스트
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                      # 문서
├── scripts/                   # 빌드/배포 스크립트
│
├── .env.example              # 환경변수 템플릿
├── .env.local                # 로컬 환경변수 (gitignore)
├── .gitignore
├── package.json
├── tsconfig.json
├── next.config.js
└── README.md
```

### Backend API Server (NestJS/Express)

```
my-api/
├── src/
│   ├── modules/               # 기능별 모듈
│   │   ├── auth/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── dto/
│   │   │   ├── entities/
│   │   │   └── auth.module.ts
│   │   └── [module-name]/
│   │
│   ├── common/                # 공통 모듈
│   │   ├── decorators/
│   │   ├── filters/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── pipes/
│   │   └── middleware/
│   │
│   ├── database/              # DB 관련
│   │   ├── migrations/
│   │   ├── seeds/
│   │   └── config/
│   │
│   ├── config/                # 설정
│   │   ├── app.config.ts
│   │   ├── database.config.ts
│   │   └── index.ts
│   │
│   ├── app.module.ts
│   └── main.ts
│
├── test/
│   ├── unit/
│   └── e2e/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example
├── package.json
└── README.md
```

## 체크리스트

### 프로젝트 시작 시 필수 확인

```markdown
## 구조 체크리스트

### 레이어 분리
□ UI 코드와 비즈니스 로직이 분리되어 있는가?
□ 데이터 접근 로직이 추상화되어 있는가?
□ 공유 코드가 별도 폴더에 있는가?

### 모듈화
□ 기능별로 폴더가 분리되어 있는가?
□ 각 모듈에 index.ts가 있는가?
□ 순환 참조가 없는가?

### 설정 관리
□ .env.example이 있는가?
□ 하드코딩된 설정값이 없는가?
□ 환경별 설정이 분리되어 있는가?

### 확장성
□ 새 기능 추가 시 기존 코드 수정이 최소화되는가?
□ 폴더 구조가 일관성 있는가?
□ 네이밍 컨벤션이 통일되어 있는가?

### 문서화
□ README.md가 있는가?
□ 프로젝트 구조 설명이 있는가?
□ 실행 방법이 문서화되어 있는가?
```

## Quick Commands

| 명령 | 동작 |
|-----|------|
| `architect init` | 대화형으로 프로젝트 구조 생성 |
| `architect analyze` | 현재 구조 분석 및 개선점 제안 |
| `architect template <type>` | 특정 타입 템플릿 적용 |
| `architect validate` | 구조 규칙 검증 |

## 출력 형식

### 구조 제안 시

```markdown
## 📁 프로젝트 구조 제안

### 프로젝트 정보
- **타입**: Next.js Fullstack
- **규모**: 중형 (10-50 페이지 예상)
- **팀 규모**: 1-3명

### 권장 구조
[폴더 트리 출력]

### 핵심 규칙
1. **features/** - 기능별 모듈화
2. **shared/** - 공통 컴포넌트만
3. **services/** - 외부 연동 추상화

### 시작 명령
\`\`\`bash
npx create-next-app@latest my-project --typescript --tailwind --app
\`\`\`

### 다음 단계
1. 폴더 구조 생성
2. 기본 설정 파일 추가
3. 첫 번째 기능 모듈 생성
```

---

**Version**: 1.0.0
**Dependencies**: tech-stack-advisor, requirements-analyzer
**Quality Target**: 프로 개발자 수준 구조
