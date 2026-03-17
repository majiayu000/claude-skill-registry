---
name: frontend-implementation
description: Frontend Implementation Workflow Agent. Frontend만 구현이 필요한 경우 사용합니다. UI 컴포넌트, 페이지, 상태 관리, API 연동 등을 오케스트레이션합니다.
allowed-tools: Read, Write, Edit, Task, AskUserQuestion, TodoWrite, Glob, Grep, Bash, Skill
---

# Frontend Implementation Workflow Agent

## 역할
Frontend만 구현이 필요한 경우 (UI 추가, 페이지 개발, 상태 관리 등)를 총괄하는 오케스트레이터입니다.

## 워크플로우 개요

```
┌─────────────────────────────────────────────────────────────┐
│                  /frontend-implementation                     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 1: 컴포넌트 구현 (병렬)
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐ │
│  │ frontend-       │ │ frontend-       │ │ frontend-     │ │
│  │ component       │ │ state           │ │ hook          │ │
│  │ (UI 컴포넌트)   │ │ (상태 관리)     │ │ (커스텀 훅)   │ │
│  └─────────────────┘ └─────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 2: 통합 (순차)
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐                                        │
│  │ frontend-api    │                                        │
│  │ (API 연동)      │                                        │
│  └────────┬────────┘                                        │
│           ▼                                                 │
│  ┌─────────────────┐                                        │
│  │ frontend-socket │  ← 실시간 기능 필요 시                   │
│  │ (WebSocket)     │                                        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 3: 최적화 & 테스트 (병렬)
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐ │
│  │ frontend-       │ │ frontend-       │ │ frontend-     │ │
│  │ perf            │ │ test            │ │ lint          │ │
│  │ (성능 최적화)   │ │ (테스트)        │ │ (코드 품질)   │ │
│  └─────────────────┘ └─────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 4: 빌드 & 배포 (순차)
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐      ┌─────────────────┐              │
│  │ frontend-build  │  →   │ devops-jenkins  │              │
│  │ (빌드 설정)     │      │ (CI/CD)         │              │
│  └─────────────────┘      └─────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Phase별 상세

### Phase 1: 컴포넌트 구현 (병렬)

| Agent | 역할 | 산출물 |
|-------|------|--------|
| frontend-component | UI 컴포넌트 설계 및 구현 | 컴포넌트 파일 |
| frontend-state | 상태 관리 (Zustand/Redux/Context) | Store 파일 |
| frontend-hook | 커스텀 훅 구현 | Hook 파일 |

### Phase 2: 통합 (순차)

| 순서 | Agent | 역할 | 산출물 |
|------|-------|------|--------|
| 1 | frontend-api | API 클라이언트, 데이터 페칭 | API 연동 코드 |
| 2 | frontend-socket | WebSocket/SSE 연동 (필요시) | 실시간 통신 코드 |

### Phase 3: 최적화 & 테스트 (병렬)

| Agent | 역할 | 산출물 |
|-------|------|--------|
| frontend-perf | 번들 최적화, 렌더링 성능 | 성능 리포트 |
| frontend-test | 단위/통합 테스트 작성 | 테스트 파일 |
| frontend-lint | ESLint, 코드 품질 검사 | Lint 리포트 |

### Phase 4: 빌드 & 배포 (순차)

| 순서 | Agent | 역할 | 산출물 |
|------|-------|------|--------|
| 1 | frontend-build | 빌드 설정, 환경 변수 | 빌드 결과물 |
| 2 | devops-jenkins | CI/CD 파이프라인 실행 | 배포 완료 |

## 산출물 디렉토리 구조

```
docs/implementation/<기능명>/frontend/
├── README.md              # 구현 개요
├── components/            # 컴포넌트 문서
│   ├── component-spec.md
│   └── storybook-notes.md
├── state-management.md    # 상태 관리 설계
├── api-integration.md     # API 연동 문서
├── test-report.md         # 테스트 결과
├── performance-report.md  # 성능 리포트
└── build-config.md        # 빌드 설정
```

## 사용 방법

```bash
/frontend-implementation <기능명>
```

### 예시
```bash
/frontend-implementation 로그인 페이지
/frontend-implementation 대시보드 UI
/frontend-implementation 실시간 채팅
```

## 협업 Agent

| Agent | 용도 |
|-------|------|
| tech-implementation | 전체 구현 (Backend + Frontend) |
| backend-implementation | API가 필요한 경우 |
| ux-ui-component | UI 명세 확인 |
| design-tokens | 디자인 토큰 참조 |

## 컴포넌트 구조 패턴

### Atomic Design
```
src/components/
├── atoms/          # Button, Input, Badge 등
├── molecules/      # SearchBar, Card 등
├── organisms/      # Header, Sidebar 등
└── templates/      # PageLayout 등
```

### 상태 관리 패턴
```
src/
├── stores/         # Zustand stores
├── contexts/       # React Context
└── hooks/          # Custom hooks
    ├── useAuth.ts
    ├── useFetch.ts
    └── useDebounce.ts
```

## 주의사항

- Phase 3 테스트 통과 후 자동 빌드/배포
- Lighthouse 점수 90점 미만 시 경고
- 번들 크기 증가 500KB 초과 시 경고
- 접근성 검사 통과 필수
- 반응형 디자인 검증 필수
