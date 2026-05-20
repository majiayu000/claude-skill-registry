---
name: nextjs15-init
description: Use when user wants to create a new Next.js 15 project (Todo/Blog/Dashboard/E-commerce/Custom domain) with App Router, ShadCN, Zustand, Tanstack Query, and modern Next.js stack
---

# NextJS 15 Init Skill

도메인 기반 Next.js 15 프로젝트를 생성하고 현대적인 스택으로 자동 설정합니다.
Todo, Blog, Dashboard, E-commerce 또는 Custom 도메인을 선택하여 App Router 기반의 완전한 CRUD 앱을 즉시 생성할 수 있습니다.

## Quick Start

스킬 실행 시 다음 정보를 입력받습니다:
- 폴더명 (예: my-todo-app)
- 프로젝트명 (예: todo-app)
- 도메인 선택 (Todo/Blog/Dashboard/E-commerce/Custom)
- 스택 프리셋 (Minimal/Essential/Full Stack/Custom)

그 후 자동으로 다음 단계가 실행됩니다:

```bash
# 1. Next.js 15 프로젝트 생성 (App Router, TypeScript, Tailwind)
npx create-next-app@latest [폴더명] --typescript --tailwind --app --use-npm

# 2. 패키지 설치
npm install

# 3. 도메인별 App Router 구조 자동 생성
# - app/[domain]/ (페이지)
# - components/[domain]/ (컴포넌트)
# - lib/stores/[domain].ts (Zustand 스토어)
# - lib/api/[domain].ts (API 로직)
# - lib/validations/[domain].ts (Zod 스키마)

# 4. 코드 품질 검증 (필수)
npm run lint

# 5. 개발 서버 실행
npm run dev
```

## Task Instructions

**IMPORTANT**: 이 스킬은 대화형으로 진행됩니다.

### Step 1: 도메인 및 프로젝트 설정 질문

**먼저 사용자에게 이렇게 물어보세요:**

"Next.js 15 앱을 생성합니다. 다음 정보를 알려주세요:

**1. 도메인(엔티티) 선택**

어떤 도메인의 앱을 만드시겠습니까?

**A) Todo (할 일 관리)**
- 필드: title, description, completed, createdAt, updatedAt
- 기능: CRUD, 필터링(전체/진행중/완료), 체크박스 토글
- API: /api/todos (GET, POST, PATCH, DELETE)

**B) Blog (블로그/CMS)**
- 필드: title, content, excerpt, slug, published, createdAt, updatedAt
- 기능: CRUD, 글 작성/수정, 목록/상세 페이지, 검색
- API: /api/posts (GET, POST, PATCH, DELETE)

**C) Dashboard (대시보드/어드민)**
- 필드: 통계, 차트 데이터, 사용자 관리
- 기능: 데이터 시각화, 테이블, 필터링, 페이지네이션
- API: /api/analytics, /api/users

**D) E-commerce (쇼핑몰)**
- 필드: name, price, description, images, stock, category
- 기능: 상품 목록/상세, 장바구니, 주문
- API: /api/products, /api/cart, /api/orders

**E) Custom (직접 정의)**
- 엔티티명과 필드를 직접 입력

**2. 프로젝트 정보**
- **폴더명**: 프로젝트를 생성할 폴더 이름 (기본값: [도메인]-app, 예: todo-app)
  - 이 폴더에 Next.js 프로젝트가 생성됩니다
- **프로젝트명**: Next.js 프로젝트 이름 (기본값: 폴더명과 동일)
  - package.json의 name 필드에 사용됩니다

**3. 스택 프리셋 선택**

다음 중 하나를 선택해주세요:

**A) Essential (권장)**
- ✅ Next.js 15 (App Router)
- ✅ TypeScript
- ✅ Tailwind CSS
- ✅ ShadCN/ui (UI 컴포넌트)
- ✅ Zustand (클라이언트 상태 관리)
- ✅ React Hook Form + Zod (폼 관리 + 검증)
- ✅ Lucide Icons
- ❌ Tanstack Query 제외
- ❌ Prisma 제외
- ❌ NextAuth 제외

**B) Minimal (가장 단순)**
- ✅ Next.js 15 (App Router)
- ✅ TypeScript
- ✅ Tailwind CSS
- ❌ ShadCN 제외
- ❌ Zustand 제외
- ❌ React Hook Form 제외
- ❌ 기타 라이브러리 제외

**C) Full Stack (모든 기능)**
- ✅ Next.js 15 (App Router)
- ✅ TypeScript
- ✅ Tailwind CSS
- ✅ ShadCN/ui
- ✅ Zustand (클라이언트 상태)
- ✅ Tanstack Query (서버 상태)
- ✅ React Hook Form + Zod
- ✅ Drizzle ORM (TypeScript-first ORM)
- ✅ Better Auth (인증)
- ✅ Framer Motion (애니메이션)
- ✅ Lucide Icons

**D) Custom (직접 선택)**
- 각 기능을 개별적으로 선택

어떤 도메인과 프리셋을 선택하시겠습니까? (도메인: A/B/C/D/E, 프리셋: A/B/C/D)"

### Step 2: Custom 선택 시 추가 질문

#### 2-1. Custom 도메인 (E) 선택 시:

1. **엔티티명**: 엔티티 이름을 입력하세요 (예: Product, Post, User)
2. **필드 정의**: 각 필드를 입력하세요 (형식: 필드명:타입, 예: title:string, price:number, isActive:boolean)
   - 지원 타입: string, number, boolean, Date
   - createdAt, updatedAt은 자동 추가됨
3. **주요 기능**: 필터링/정렬 기준이 될 필드를 선택하세요

#### 2-2. Custom 스택 프리셋 (D) 선택 시:

다음 질문들을 순차적으로 하세요:

1. **UI 컴포넌트**: ShadCN/ui를 사용하시겠습니까? (예/아니오)
2. **상태 관리**: Zustand를 사용하시겠습니까? (예/아니오)
3. **서버 상태**: Tanstack Query를 사용하시겠습니까? (예/아니오)
4. **폼 관리**: React Hook Form + Zod를 사용하시겠습니까? (예/아니오)
5. **데이터베이스**: Drizzle ORM을 사용하시겠습니까? (예/아니오)
6. **인증**: Better Auth를 사용하시겠습니까? (예/아니오)
7. **애니메이션**: Framer Motion을 사용하시겠습니까? (예/아니오)

### Step 3: 선택된 도메인과 스택에 따라 프로젝트 생성

1. **Next.js 15 프로젝트 생성**:
   - 사용자가 지정한 **폴더명**으로 프로젝트 생성
   - 명령어: `npx create-next-app@latest [폴더명] --typescript --tailwind --app --use-npm`
   - 폴더명과 프로젝트명이 다른 경우, 생성 후 package.json의 `name` 필드를 수정

2. **선택된 패키지 설치**: `npm install [패키지들]`

3. **폴더 구조 생성**: App Router 기반 구조
   ```
   app/
   ├── (auth)/
   ├── [domain]/
   ├── api/[domain]/
   ├── layout.tsx
   └── page.tsx
   components/
   ├── ui/ (ShadCN)
   ├── [domain]/
   └── layouts/
   lib/
   ├── db/ (Prisma)
   ├── stores/ (Zustand)
   ├── api/
   ├── utils/
   └── validations/ (Zod)
   ```

4. **도메인별 보일러플레이트 생성**:

   **A) Todo**: title, description, completed, createdAt, updatedAt
   - API Routes: /api/todos (CRUD)
   - Pages: /todos (리스트), /todos/[id] (상세)
   - Components: TodoList, TodoItem, TodoForm
   - Store: useTodoStore (Zustand)
   - Validation: todoSchema (Zod)

   **B) Blog**: title, content, excerpt, slug, published, createdAt, updatedAt
   - API Routes: /api/posts (CRUD)
   - Pages: /blog (목록), /blog/[slug] (상세), /blog/write (작성)
   - Components: PostList, PostCard, PostEditor
   - Store: usePostStore (Zustand)
   - Validation: postSchema (Zod)

   **C) Dashboard**: 통계, 차트, 사용자 관리
   - API Routes: /api/analytics, /api/users
   - Pages: /dashboard (메인), /dashboard/users (사용자)
   - Components: Chart, StatsCard, DataTable
   - Store: useDashboardStore (Zustand)
   - Validation: userSchema (Zod)

   **D) E-commerce**: name, price, description, images, stock, category
   - API Routes: /api/products, /api/cart, /api/orders
   - Pages: /products (목록), /products/[id] (상세), /cart (장바구니)
   - Components: ProductCard, ProductGrid, Cart
   - Store: useCartStore, useProductStore (Zustand)
   - Validation: productSchema, cartSchema (Zod)

   **E) Custom**: 사용자 정의 필드
   - API Routes: 기본 CRUD
   - Pages: 기본 List/Detail
   - Components: 기본 CRUD 컴포넌트
   - Store: 기본 store
   - Validation: 기본 schema

5. **ShadCN 설치 및 구성** (Essential 이상):
   ```bash
   npx shadcn@latest init
   npx shadcn@latest add button card input form table
   ```

6. **코드 검증 및 오류 수정**:

   a. `npm run lint` 실행

   b. 발견된 오류 수정:
   - **Import 경로**: @/ alias 사용 (tsconfig.json 설정)
   - **TypeScript 타입**: 모든 타입 명시
   - **ESLint 규칙**: 사용하지 않는 변수, import 제거
   - **Next.js 규칙**: metadata, generateStaticParams 등
   - **'use client' 지시어**: useState, useEffect 등 React Hooks 사용 시 파일 최상단에 추가

   c. `npm run build` 또는 `pnpm build` 실행

   d. 빌드 오류 수정:
   - **TypeScript 타입 오류**: 타입 불일치, nullable 체크 누락 등
   - **모듈 import 오류**: 경로 확인, 패키지 설치 확인
   - **Server/Client Component 오류**: 적절한 'use client' 지시어 추가
   - **Dynamic import 오류**: server-only 코드가 클라이언트에서 사용되지 않도록 확인

   e. 재검증: lint와 build 모두 성공할 때까지 반복

   f. 목표:
      - `npm run lint` 결과가 "0 errors"
      - `npm run build` 또는 `pnpm build` 성공

   **✅ CRITICAL**: 이 단계는 필수입니다. lint와 build 모두 성공해야 다음 단계로 진행할 수 있습니다.

### Step 4: 최종 검증 및 안내

**✅ CRITICAL**: 이 단계는 프로젝트 완료의 필수 조건입니다. lint와 build 모두 성공해야 합니다.

1. **ESLint 검증**:
   ```bash
   npm run lint
   ```

   - ✅ **성공 예시**:
     ```
     ✔ No ESLint warnings or errors
     ```

   - ❌ **실패 예시** (error가 있으면 반드시 수정):
     ```
     Error: 'useState' is defined but never used
     Error: Missing return type on function
     ```

2. **프로덕션 빌드 검증**:
   ```bash
   npm run build
   ```

   **또는 pnpm 사용 시**:
   ```bash
   pnpm build
   ```

   - ✅ **성공 예시**:
     ```
     ✓ Compiled successfully
     ✓ Linting and checking validity of types
     ✓ Collecting page data
     ✓ Generating static pages
     ```

   - ❌ **실패 예시** (빌드 에러 발생 시 반드시 수정):
     ```
     Type error: Property 'xyz' does not exist on type 'ABC'
     Error: Module not found: Can't resolve '@/...'
     ```

   **중요**: 빌드가 실패하면 TypeScript 타입 오류나 import 경로 문제를 수정하고 다시 빌드해야 합니다.

3. **검증 결과 요약** (lint와 build 모두 성공 시):
   ```
   ✅ Next.js 15 프로젝트 생성 완료!
   ✅ 패키지 설치 완료 (ShadCN, Zustand, Tanstack Query 등)
   ✅ ESLint 검증 통과 (0 errors)
   ✅ TypeScript 빌드 성공
   ✅ 프로덕션 빌드 완료
   ```

4. **프로젝트 정보 제공**:
   - **폴더명**: [사용자 입력값] (예: my-todo-app)
   - **프로젝트명**: [사용자 입력값] (예: todo-app)
   - **도메인**: [선택된 도메인] (Todo/Blog/Dashboard/E-commerce/Custom)
   - **선택된 스택**: [프리셋명] (ShadCN, Zustand, Tanstack Query 등)
   - **주요 기능**: [도메인] CRUD, API Routes, 타입 안전성
   - **생성된 파일**: XX개 TypeScript 파일 (app, components, lib)

5. **실행 방법 안내**:
   ```bash
   cd [폴더명]
   npm run dev
   # http://localhost:3000 에서 확인
   ```

6. **다음 단계 제안** (선택사항, 도메인별):
   - **Todo**: 항목 추가/수정/삭제, 필터링(전체/진행중/완료), 완료 토글
   - **Blog**: 글 작성/수정, 목록/상세 페이지, 검색, 태그
   - **Dashboard**: 데이터 시각화, 차트, 사용자 관리, 필터링
   - **E-commerce**: 상품 목록/상세, 장바구니, 주문, 카테고리
   - **공통**: TypeScript 타입 안전성, API 테스트, 배포 (Vercel)

## Core Principles

- **App Router**: Next.js 15 App Router 기반 구조
- **타입 안전성**: TypeScript Strict Mode
- **컴포넌트 재사용**: ShadCN/ui 활용
- **상태 관리**: Zustand (클라이언트), Tanstack Query (서버)
- **코드 품질**: ESLint + Prettier
- **폼 검증**: React Hook Form + Zod

## Reference Files

[references/setup-guide.md](references/setup-guide.md) - 완전한 가이드
- 기본 셋업 (도메인별 CRUD, API Routes, 컴포넌트)
- 선택 옵션: ShadCN, Zustand, Tanstack Query, Drizzle ORM, Better Auth, Framer Motion

## Notes

- **대화형 스킬**: 사용자에게 도메인과 프리셋 선택을 통해 맞춤형 앱 구성
- **도메인 지원**: Todo, Blog, Dashboard, E-commerce, Custom (사용자 정의)
- **프리셋 제공**: Full Stack, Essential, Minimal, Custom
- **선택 가능 기능**: ShadCN, Zustand, Tanstack Query, Drizzle ORM, Better Auth, Framer Motion
- **기본 포함**: Next.js 15 (App Router), TypeScript, Tailwind CSS, ESLint
- **플랫폼**: Web (Vercel 최적화)
- **품질 보증**:
  - 모든 프로젝트는 `npm run lint` 통과 필수
  - TypeScript Strict Mode
  - 타입 안전성 보장
  - App Router 패턴 준수
  - 도메인별 최적화된 UI/UX

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->
