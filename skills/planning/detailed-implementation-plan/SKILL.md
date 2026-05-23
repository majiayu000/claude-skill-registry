---
name: detailed-implementation-plan
description: Generates detailed implementation plans from a SINGLE plan-based-page output file. Supports parallel execution - run multiple sessions simultaneously for different pages. Input is ONE file (either _shared-components.md or a specific page like landingpage-page.md). Use when you want to generate implementation plans in parallel across multiple sessions.
---

# Detailed Implementation Plan
Transform a single plan-based-page output file into an actionable implementation plan. Designed for parallel session execution.
Fixed Paths
모든 프로젝트에서 아래 고정 경로 사용:
.doc/plan/
plans/ ← plan-based-page 출력 (입력)
implementation/ ← 상세 구현 계획 (출력)
Input Requirements
Single File Input - ONE of the following from .doc/plan/plans/ directory:
파일 유형경로세션공통 컴포넌트.doc/plan/plans/\_shared-components.md세션 0 (먼저 실행)페이지 계획.doc/plan/plans/[page-name]-page.md세션 1+ (병렬 가능)
Required References (세션 1+ 에서):

.doc/plan/implementation/shared-components-impl.md - 공통 컴포넌트 상세 구현 참조

Optional References:

/ui-spec/[page].html - 상세 스타일 확인용

Session-Based Parallel Workflow
[순차 - 먼저 실행]
세션 0: .doc/plan/plans/\_shared-components.md
↓
출력: .doc/plan/implementation/shared-components-impl.md
↓ (완료 후)

[병렬 - 동시 실행 가능]
세션 1: .doc/plan/plans/landingpage-page.md + 참조: shared-components-impl.md → .doc/plan/implementation/landingpage-impl.md
세션 2: .doc/plan/plans/detailPage-page.md + 참조: shared-components-impl.md → .doc/plan/implementation/detailPage-impl.md
세션 3: .doc/plan/plans/listPage-page.md + 참조: shared-components-impl.md → .doc/plan/implementation/listPage-impl.md
How to Use
세션 0: 공통 컴포넌트 (먼저 실행)
입력: .doc/plan/plans/\_shared-components.md
출력: .doc/plan/implementation/shared-components-impl.md
세션 1+: 페이지별 (병렬 실행 가능, 세션 0 완료 후)
입력: .doc/plan/plans/landingpage-page.md
참조: .doc/plan/implementation/shared-components-impl.md (공통 컴포넌트 import 경로, props, 인터페이스 확인)
출력: .doc/plan/implementation/landingpage-impl.md
Output Location
모든 상세 구현 계획은 .doc/plan/implementation/ 디렉토리에 저장:
.doc/plan/implementation/
shared-components-impl.md # 세션 0
landingpage-impl.md # 세션 1
detailPage-impl.md # 세션 2
listPage-impl.md # 세션 3
Important Rules

하나의 세션 = 하나의 파일 입력 = 하나의 출력
공통 컴포넌트 먼저 - 페이지 세션 실행 전에 세션 0 완료 필수
페이지는 병렬 가능 - 서로 의존성 없음 (세션 0 완료 후)
공통 컴포넌트 impl 참조 - 페이지 세션에서 .doc/plan/implementation/shared-components-impl.md 참조하여 정확한 import 경로, props, 인터페이스 확인

Output Structure
Generate implementation plans in this exact format:
For 공통 컴포넌트 (Shared Components)
markdown# 공통 컴포넌트 구현 계획

## 개요

공통으로 사용되는 UI 컴포넌트 구현

- [Component 1]: [pages where used]
- [Component 2]: [pages where used]

---

## 의존성 설치

\`\`\`bash

# shadcn/ui

npx shadcn@latest add button input card form label

# npm packages

npm install react-hook-form zod @hookform/resolvers lucide-react
\`\`\`

---

## Task List

### 1. Header

**상태:** - [ ] 미완료  
**파일:** `components/layout/Header.tsx`
**사용처:** Home, Create, Study (3/3 pages)

**요구사항:**

- [ ] 로고 (왼쪽)
- [ ] 네비게이션 링크
- [ ] 반응형 모바일 메뉴

**스타일 (plan-based-page에서):**

- Background: #FFFFFF
- Height: 64px
- Shadow: soft

**기본 구조:**
\`\`\`typescript
import Link from "next/link"

export function Header() {
return (
<header className="h-16 border-b bg-white">
<nav className="container flex items-center justify-between">
{/_ Logo _/}
{/_ Nav Links _/}
</nav>
</header>
)
}
\`\`\`

**완료 조건:**

- [ ] 모든 페이지에서 동일하게 렌더링
- [ ] 반응형 동작 확인

---

### 2. Button

...
For 페이지별 (Page-specific)
markdown# [PageName] Page 구현 계획

## 개요

[Page description from plan-based-page]

- User Flow Step: [step number and description]
- 주요 기능: [key features]

---

## 페이지 구조 (plan-based-page에서)

\`\`\`

- Header (공통)
- Main
  - [Section 1]
  - [Section 2]
- Footer (공통)
  \`\`\`

---

## Task List

### 0. 페이지 라우트 생성

- [ ] `app/[route]/page.tsx` 생성
- [ ] 메타데이터 설정
- [ ] 레이아웃 연결

### 1. [PageSpecificComponent]

**상태:** - [ ] 미완료  
**파일:** `app/[route]/components/ComponentName.tsx`

**요구사항:**

- [ ] [Requirement from plan-based-page]
- [ ] [UI requirement]

**비즈니스 로직 (PRD에서):**

- [ ] [Logic 1]
- [ ] [Logic 2]

**스타일:**

- Primary: #4A90E2
- Spacing: 16px
- Border radius: 8px

**기본 구조:**
\`\`\`typescript
"use client"

export function ComponentName() {
return (
<section>
{/_ Implementation _/}
</section>
)
}
\`\`\`

**완료 조건:**

- [ ] 기능 동작 확인
- [ ] 스타일 일치 확인

---

## 구현 순서

1. 페이지 라우트 생성
2. 공통 컴포넌트 import (Header, Footer)
3. 페이지 전용 컴포넌트 구현
4. 비즈니스 로직 연결
5. 스타일 조정

---

## 검증 체크리스트

- [ ] 페이지 렌더링 정상
- [ ] User Flow 단계 완료 가능
- [ ] 공통 컴포넌트 정상 표시
- [ ] 반응형 동작
- [ ] 에러 상태 처리
      Analysis Process

Parse Page Plan: Extract selected section (공통 or specific page)
Gather Info: Components, styles, business logic from plan-based-page
Check HTML (Optional): If complex styling needed, reference original HTML
Determine Dependencies: shadcn/ui components, npm packages
Define File Paths: Next.js App Router conventions
Create Task Structure: Actionable tasks with checkboxes
Add Code Skeletons: TypeScript templates for each component
Add Verification Steps: Testing and validation checkpoints
Update Page Plan File: Mark processed items as - [x]

Component Organization Patterns
File Path Conventions
app/
components/
auth/ - Authentication components
admin/ - Admin-specific components
learning/ - Learning-related components
ui/ - shadcn/ui components
layout/ - Layout components
actions/ - Server actions
contexts/ - React contexts/providers
lib/ - Utilities and helpers
(routes)/ - Page routes
Component Types
Client Components ("use client"):

Forms with user interaction
Components using hooks (useState, useEffect)
Event handlers (onClick, onChange)
Contexts that manage client state

Server Components (default):

Data fetching components
Static layouts
Components without interactivity

Implementation Details Template
For each component, provide:

1. File Path
   app/components/[category]/ComponentName.tsx
2. Requirements Checklist

Specific feature 1
Specific feature 2
UI/UX requirement (from image)

3. Dependencies
   List required packages:

shadcn/ui components
npm packages
Custom hooks

4. Code Structure
   Provide skeleton/template:
   typescript"use client" // if needed

import statements
type definitions
component function
return JSX 5. Implementation Details

State management approach
Form handling strategy
API/Server action integration
Styling approach
Error handling

HTML Reference (Optional)
When detailed styling verification is needed:
When to Reference HTML

Complex layouts not fully captured in plan-based-page
Exact pixel values for spacing
Specific CSS classes or patterns
Animation or transition details

How to Use
markdown**HTML 참조:** `/ui-spec/home.html`

스타일 확인 필요:

- [ ] Hero section 정확한 padding 값
- [ ] Button hover 상태
- [ ] Grid gap 값
      Extract from HTML

Exact spacing (padding: 24px 16px)
Color values (#4A90E2, rgba(0,0,0,0.1))
Border radius (rounded-lg = 8px)
Shadow values
Responsive breakpoints

Dependency Management
shadcn/ui Components
List required components to install:
bashnpx shadcn@latest add button input card form
npm Packages
List with installation commands:
bashnpm install react-hook-form zod @hookform/resolvers
Custom Dependencies

Custom hooks to create
Utility functions needed
Type definitions required

Implementation Order Strategy

Infrastructure First

Providers/Contexts
Utility functions
Type definitions

Base Components

UI components (shadcn/ui)
Layout components

Feature Components

Forms
Data display components
Interactive features

Integration

Server actions
API routes
Page routes

Task Breakdown Pattern
For Forms

- [ ] Install dependencies (react-hook-form, zod)
- [ ] Create Zod validation schema
- [ ] Implement form with react-hook-form
- [ ] Add error handling and display
- [ ] Add loading states
- [ ] Connect to server action/API
- [ ] Test validation
- [ ] Test submission
      For Display Components
- [ ] Define TypeScript interface
- [ ] Implement static UI
- [ ] Add conditional rendering
- [ ] Add loading skeleton
- [ ] Add empty state
- [ ] Add error state
- [ ] Test with mock data
- [ ] Test responsive design
      For Contexts/Providers
- [ ] Define context interface
- [ ] Implement context provider
- [ ] Add state management logic
- [ ] Add mutation functions
- [ ] Export custom hook
- [ ] Wrap app with provider
- [ ] Test context consumption
      Verification Checklist Categories
      Functionality

Component renders without errors
All features work as expected
Forms validate correctly
Data fetching works

UI/UX

Matches design mockup
Responsive on mobile/tablet/desktop
Loading states display properly
Error messages are clear

Code Quality

TypeScript types are correct
No console errors
Follows Next.js 15 conventions
Proper use of server/client components

Integration

Server actions work
API calls succeed
Navigation functions properly
State persists correctly

Best Practices

Use Next.js 15 App Router conventions
Prefer Server Components when possible
Use Server Actions for mutations
Implement proper error boundaries
Add loading states for async operations
Use TypeScript strictly
Follow shadcn/ui patterns
Keep components focused and small
Extract reusable logic to hooks
Add proper accessibility (ARIA labels)

Example Output Format
markdown# Home Page 구현 계획

## 개요

FlashLearn 앱의 랜딩 페이지 구현

- User Flow Step 1: User lands on app
- 주요 기능: 앱 소개, 새 덱 생성 CTA

---

## 페이지 구조 (plan-based-page에서)

\`\`\`

- Header (공통)
- Main
  - HeroSection
    - Logo (80px)
    - Tagline
  - CTAButton (공통 Button)
- Footer (공통)
  \`\`\`

---

## 의존성

이미 설치됨 (공통 컴포넌트에서):

- shadcn/ui: button, card
- lucide-react

---

## Task List

### 0. 페이지 라우트 생성

- [ ] `app/page.tsx` 생성
- [ ] metadata 설정 (title, description)

### 1. HeroSection 컴포넌트

**상태:** - [ ] 미완료  
**파일:** `app/(home)/components/HeroSection.tsx`

**요구사항:**

- [ ] 로고 이미지 (80px, 중앙 정렬)
- [ ] 태그라인 텍스트
- [ ] 반응형 레이아웃

**스타일 (plan-based-page에서):**

- Text: #1F2937
- Background: #FFFFFF
- Spacing: 48px (상하)

**기본 구조:**
\`\`\`typescript
import Image from "next/image"

export function HeroSection() {
return (
<section className="py-12 text-center">
<Image 
        src="/logo.png" 
        alt="FlashLearn" 
        width={80} 
        height={80}
        className="mx-auto"
      />
<h1 className="mt-6 text-3xl font-bold text-gray-800">
Learn Smarter with Spaced Repetition
</h1>
</section>
)
}
\`\`\`

**완료 조건:**

- [ ] 로고 정상 표시
- [ ] 반응형 텍스트 크기

---

### 2. Home Page 조립

**상태:** - [ ] 미완료  
**파일:** `app/page.tsx`

**요구사항:**

- [ ] Header 공통 컴포넌트 import
- [ ] HeroSection 배치
- [ ] CTA Button ("Create New Deck")
- [ ] Footer 공통 컴포넌트 import

**비즈니스 로직:**

- [ ] CTA 클릭 → /create 페이지 이동
- [ ] 기존 덱 있으면 덱 카드 표시 (localStorage 확인)

**기본 구조:**
\`\`\`typescript
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { Button } from "@/components/ui/button"
import { HeroSection } from "./(home)/components/HeroSection"
import Link from "next/link"

export default function HomePage() {
return (
<>
<Header />
<main className="container py-8">
<HeroSection />
<div className="mt-8 text-center">
<Button asChild size="lg">
<Link href="/create">Create New Deck</Link>
</Button>
</div>
</main>
<Footer />
</>
)
}
\`\`\`

**완료 조건:**

- [ ] 페이지 정상 렌더링
- [ ] CTA 버튼 동작
- [ ] 공통 컴포넌트 정상 표시

---

## 구현 순서

1. `app/page.tsx` 파일 생성
2. HeroSection 컴포넌트 구현
3. 공통 컴포넌트 import (Header, Footer, Button)
4. 페이지 조립 및 레이아웃 조정
5. CTA 링크 연결
6. 반응형 테스트

---

## 검증 체크리스트

### HeroSection

- [ ] 로고 이미지 표시
- [ ] 태그라인 텍스트 표시
- [ ] 모바일에서 정상 표시

### Home Page

- [ ] 전체 페이지 렌더링 정상
- [ ] Header/Footer 공통 컴포넌트 표시
- [ ] CTA 버튼 클릭 → /create 이동
- [ ] 스타일이 plan-based-page와 일치

---

## HTML 참조 (필요시)

**파일:** `/ui-spec/home.html`

확인 필요 시:

- [ ] HeroSection 정확한 padding 값
- [ ] Button 정확한 스타일
      Progressive Implementation
      세션별 병렬 실행을 통한 빠른 개발:

세션 0: 공통 컴포넌트 먼저 구현 (의존성 기반)
세션 1~N: 페이지별 병렬 실행 (독립적)
통합: 모든 세션 완료 후 통합 테스트

Parallel Execution Flow
[Sequential - 먼저]
세션 0: .doc/plan/plans/\_shared-components.md → .doc/plan/implementation/shared-components-impl.md
↓ (완료 대기)

[Parallel - 동시 실행, shared-components-impl.md 참조]
세션 1: .doc/plan/plans/landingpage-page.md + impl 참조 ──→ .doc/plan/implementation/landingpage-impl.md
세션 2: .doc/plan/plans/detailPage-page.md + impl 참조 ───→ .doc/plan/implementation/detailPage-impl.md
세션 3: .doc/plan/plans/listPage-page.md + impl 참조 ────→ .doc/plan/implementation/listPage-impl.md
↓

[After All Complete]
통합 테스트 및 .doc/plan/plans/\_overview.md 체크박스 업데이트
Source File Update (Optional)
세션 완료 후 원본 plan 파일의 체크박스 업데이트:
markdown# Before

- [ ] Header 구현
- [ ] Button 구현

# After

- [x] Header 구현
- [x] Button 구현
      Session Examples
      세션 0: 공통 컴포넌트
      bash# 입력
      .doc/plan/plans/\_shared-components.md

# 출력

.doc/plan/implementation/shared-components-impl.md
세션 1: Landing Page (병렬, 세션 0 완료 후)
bash# 입력
.doc/plan/plans/landingpage-page.md

# 참조 (import 경로, props, 인터페이스 확인용)

.doc/plan/implementation/shared-components-impl.md

# 출력

.doc/plan/implementation/landingpage-impl.md
세션 2: Detail Page (병렬, 세션 0 완료 후)
bash# 입력
.doc/plan/plans/detailPage-page.md

# 참조

.doc/plan/implementation/shared-components-impl.md

# 출력

.doc/plan/implementation/detailPage-impl.md
Workflow Summary

세션 0 실행: .doc/plan/plans/\_shared-components.md → 공통 컴포넌트 상세 구현
세션 0 완료 대기: .doc/plan/implementation/shared-components-impl.md 생성 완료 필수
세션 1~N 병렬 실행: 각 페이지별 상세 구현 + shared-components-impl.md 참조
모든 세션 완료: .doc/plan/plans/\_overview.md 체크박스 업데이트
구현 시작: .doc/plan/implementation/ 의 impl 파일들 기반으로 코딩
