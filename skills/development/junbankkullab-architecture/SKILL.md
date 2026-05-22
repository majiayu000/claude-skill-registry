---
name: junbankkullab-architecture
description: 전반꿀 연구소 프로젝트 아키텍처 규칙. 새 기능 추가, 파일 생성, 코드 구조 변경 시 반드시 참조. Feature-based + Layer separation 패턴 적용.
---

# 전반꿀 연구소 아키텍처 규칙

이 문서는 프로젝트의 아키텍처 규칙을 정의한다. 모든 코드 변경은 이 규칙을 따른다.

## 핵심 원칙

1. **Feature-based 구조**: 기능별로 코드를 응집
2. **Layer Separation**: app(라우팅) / features(기능) / shared(공용) 분리
3. **Colocation**: 관련 파일은 가까이 배치
4. **Public API**: 각 모듈은 `index.ts`로 외부에 노출할 것만 export

---

## 디렉토리 구조 규칙

```
src/
├── app/                    # 라우팅 레이어 (Next.js App Router)
├── features/               # 기능 모듈
├── shared/                 # 공용 모듈
├── config/                 # 설정 (상수, 환경변수)
└── styles/                 # 글로벌 스타일
```

### `app/` - 라우팅 레이어

**책임**: 라우팅, 레이아웃, 페이지 구성만
**금지**: 비즈니스 로직, 상태 관리, 데이터 fetching 직접 구현

```
app/
├── (public)/               # 공개 페이지 그룹
│   ├── page.tsx
│   └── [dynamic]/page.tsx
├── (auth)/                 # 인증 필요 페이지
├── (admin)/                # 관리자 전용
├── api/
│   └── v1/                 # 버전된 API
└── layout.tsx
```

**Route Group 규칙**:
- `(public)` - 누구나 접근 가능
- `(auth)` - 로그인 필요
- `(admin)` - 관리자 권한 필요

### `features/` - 기능 모듈

**책임**: 특정 기능에 필요한 모든 것 (컴포넌트, 훅, API, 타입, 로직)

```
features/
└── {feature-name}/
    ├── components/         # UI 컴포넌트
    │   ├── FeatureComponent.tsx
    │   └── index.ts
    ├── hooks/              # 커스텀 훅
    │   └── useFeature.ts
    ├── api/                # API 함수
    │   └── feature.ts
    ├── lib/                # 비즈니스 로직
    │   └── calculator.ts
    ├── types.ts            # Feature 전용 타입
    └── index.ts            # Public API (barrel export)
```

**Feature 추가 규칙**:
1. 새 기능 = 새 폴더 (`features/{name}/`)
2. 반드시 `index.ts`로 public API 정의
3. Feature 간 직접 import 금지 → `shared/`로 승격

### `shared/` - 공용 모듈

**책임**: 2개 이상 feature에서 사용하는 코드

```
shared/
├── components/
│   ├── ui/                 # 기본 UI (Button, Card, Badge, Modal)
│   ├── layout/             # 레이아웃 (Header, Footer, Sidebar)
│   └── charts/             # 차트 컴포넌트
├── hooks/                  # 공용 훅 (useLocalStorage, useMediaQuery)
├── lib/
│   ├── api/                # API 클라이언트
│   ├── utils/              # 순수 유틸 (date, format, validation)
│   └── analytics/          # 데이터 분석 (youtube, market, sentiment)
└── types/                  # 공용 타입
```

**승격 규칙**:
- Feature 전용 코드 → 2개 이상 feature에서 사용 시 `shared/`로 이동
- `shared/` 내 코드는 feature에 의존 금지

### `config/` - 설정

```
config/
├── constants.ts            # 앱 상수
├── env.ts                  # 환경변수 타입 및 검증
└── {domain}.ts             # 도메인별 설정 (analysts.ts 등)
```

### `styles/` - 스타일

```
styles/
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   └── spacing.css
└── globals.css
```

---

## Import 규칙

### 허용되는 Import 패턴

```tsx
// ✅ Feature에서 shared 사용
import { Button } from '@/shared/components/ui'
import { formatDate } from '@/shared/lib/utils'

// ✅ Feature 외부에서 public API 사용
import { HoneyIndex } from '@/features/honey-index'

// ✅ Feature 내부에서 상대 경로
// (features/honey-index/components/Chart.tsx에서)
import { useHoneyIndex } from '../hooks/useHoneyIndex'
import type { HoneyData } from '../types'

// ✅ app에서 features 사용
import { HoneyIndexChart } from '@/features/honey-index'
```

### 금지되는 Import 패턴

```tsx
// ❌ Feature 내부 직접 참조 (barrel 우회)
import { Chart } from '@/features/honey-index/components/Chart'

// ❌ Feature 간 직접 의존
// (features/voting/에서)
import { something } from '@/features/predictions'

// ❌ shared에서 feature 의존
// (shared/lib/에서)
import { something } from '@/features/honey-index'

// ❌ 상대 경로로 레이어 탈출
import { something } from '../../../shared/lib'
```

---

## 파일 생성 체크리스트

### 새 Feature 추가 시

1. [ ] `features/{name}/` 폴더 생성
2. [ ] `features/{name}/index.ts` 생성 (barrel export)
3. [ ] 필요한 하위 폴더 생성 (`components/`, `hooks/`, `api/`, `lib/`)
4. [ ] `features/{name}/types.ts` 생성 (필요시)
5. [ ] ARCHITECTURE.md의 feature 목록 업데이트

### 새 컴포넌트 추가 시

1. [ ] Feature 전용 → `features/{name}/components/`
2. [ ] 공용 UI → `shared/components/ui/`
3. [ ] 레이아웃 → `shared/components/layout/`
4. [ ] 차트 → `shared/components/charts/`
5. [ ] 해당 `index.ts`에 export 추가

### 새 API 엔드포인트 추가 시

1. [ ] `app/api/v1/{resource}/route.ts` 생성
2. [ ] Request/Response 타입 정의
3. [ ] Feature의 `api/` 폴더에 클라이언트 함수 추가

---

## 네이밍 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| Feature 폴더 | kebab-case | `honey-index`, `user-profile` |
| 컴포넌트 파일 | PascalCase | `HoneyIndexChart.tsx` |
| 훅 파일 | camelCase, use 접두사 | `useHoneyIndex.ts` |
| 유틸 파일 | camelCase | `formatDate.ts` |
| 타입 파일 | camelCase | `types.ts` |
| 상수 | SCREAMING_SNAKE_CASE | `API_BASE_URL` |
| Route Group | (purpose) | `(public)`, `(auth)`, `(admin)` |

---

## 현재 Feature 목록

| Feature | 설명 | 상태 |
|---------|------|------|
| `predictions` | 예측 분석, 히스토리 | ✅ 구현됨 |
| `honey-index` | 꿀지수 통계, 차트 | ✅ 구현됨 |
| `assets` | 종목별 통계 | ✅ 구현됨 |
| `voting` | 사용자 투표 | 🚧 확장 예정 |
| `auth` | 인증/인가 | 📋 계획됨 |
| `notifications` | 알림 | 📋 계획됨 |
| `analysts` | 다중 분석가 관리 | 📋 계획됨 |
| `admin` | 관리자 기능 | 📋 계획됨 |

---

## 예시: 새 Feature 추가

`analysts` feature 추가 예시:

```
features/analysts/
├── components/
│   ├── AnalystCard.tsx
│   ├── AnalystList.tsx
│   ├── AnalystProfile.tsx
│   └── index.ts
├── hooks/
│   └── useAnalyst.ts
├── api/
│   └── analysts.ts
├── types.ts
└── index.ts
```

**index.ts (barrel export)**:
```tsx
// Public API만 노출
export { AnalystCard } from './components'
export { AnalystList } from './components'
export { AnalystProfile } from './components'
export { useAnalyst } from './hooks/useAnalyst'
export type { Analyst, AnalystStats } from './types'
```

**사용**:
```tsx
// app/analysts/page.tsx
import { AnalystList } from '@/features/analysts'

export default function AnalystsPage() {
  return <AnalystList />
}
```
