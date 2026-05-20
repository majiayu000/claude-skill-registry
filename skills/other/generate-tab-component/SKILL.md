---
name: generate-tab-component
description: 새 탭 추가 시 필요한 보일러플레이트(컴포넌트, lazy import, 권한, 메타데이터)를 자동 생성합니다. 새 탭 추가 시 사용.
argument-hint: "[탭 이름 (예: 'notice-board')]"
---

## Purpose

새로운 네비게이션 탭을 추가할 때 필요한 모든 파일과 설정을 자동으로 생성합니다:

1. **탭 컴포넌트 생성** - 탭의 메인 컴포넌트 파일 생성
2. **TabContent lazy import 추가** - React.lazy import + Suspense 래핑 추가
3. **types/system.ts 업데이트** - AppTab 타입, TAB_META, TAB_GROUPS, DEFAULT_TAB_PERMISSIONS 업데이트
4. **권한 설정** - 역할별 접근 권한 기본값 설정

## When to Run

- 새로운 네비게이션 탭을 추가해야 할 때
- 기존 탭을 새로운 구조로 분리할 때

## Related Files

| File | Purpose |
|------|---------|
| `types/system.ts` | AppTab 타입, TAB_META, TAB_GROUPS, DEFAULT_TAB_PERMISSIONS |
| `components/Layout/TabContent.tsx` | 탭 라우팅 (React.lazy import) |
| `components/Navigation/Sidebar.tsx` | 사이드바 네비게이션 |

## Workflow

### Step 1: 사용자 입력 수집

`AskUserQuestion`을 사용하여 다음을 확인합니다:

1. **탭 ID** (kebab-case, 예: `notice-board`)
2. **탭 한국어 라벨** (예: `공지사항`)
3. **탭 아이콘** (예: `📢`)
4. **소속 탭 그룹** (HOME, SCHEDULE, CLASS, STUDENT, ADMIN, SYSTEM, SUPPORT 중 선택)
5. **접근 가능 역할** (기본값: 전체 역할)

### Step 2: 탭 컴포넌트 디렉토리 및 파일 생성

**생성할 파일:**

```
components/<PascalCase>/
├── <PascalCase>Tab.tsx    # 메인 탭 컴포넌트
└── index.ts               # barrel export
```

**탭 컴포넌트 템플릿:**

```tsx
import React from 'react';

interface <PascalCase>TabProps {
  departmentId: string;
  // 필요한 props 추가
}

export default function <PascalCase>Tab({ departmentId }: <PascalCase>TabProps) {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4"><한국어 라벨></h1>
      {/* TODO: 구현 */}
    </div>
  );
}
```

### Step 3: types/system.ts 업데이트

1. **AppTab 유니온 타입에 추가:**

```typescript
type AppTab = '...' | '<tab-id>';
```

2. **TAB_META에 메타데이터 추가:**

```typescript
'<tab-id>': { label: '<한국어 라벨>', icon: '<아이콘>' },
```

3. **TAB_GROUPS의 해당 그룹에 추가:**

```typescript
{ id: '<GROUP>', tabs: [...existingTabs, '<tab-id>'], ... }
```

4. **DEFAULT_TAB_PERMISSIONS에 추가** (선택된 역할에 탭 추가)

### Step 4: TabContent.tsx에 lazy import 추가

```typescript
const <PascalCase>Tab = React.lazy(() => import('../<PascalCase>/<PascalCase>Tab'));
```

렌더링 분기에 case 추가:

```typescript
case '<tab-id>':
  return <Suspense fallback={<VideoLoading />}><ErrorBoundary><PascalCase>Tab {...props} /></ErrorBoundary></Suspense>;
```

### Step 5: 검증

생성된 파일들이 올바른지 확인합니다:

1. 탭 컴포넌트 파일 존재 확인
2. AppTab 타입에 새 탭 포함 확인
3. TabContent lazy import 존재 확인
4. TAB_META에 메타데이터 존재 확인

## Output Format

```markdown
## 탭 생성 완료

| 항목 | 상태 | 파일 |
|------|------|------|
| 컴포넌트 | 생성됨 | `components/<Name>/<Name>Tab.tsx` |
| barrel export | 생성됨 | `components/<Name>/index.ts` |
| AppTab 타입 | 업데이트 | `types/system.ts` |
| TAB_META | 업데이트 | `types/system.ts` |
| TAB_GROUPS | 업데이트 | `types/system.ts` |
| DEFAULT_TAB_PERMISSIONS | 업데이트 | `types/system.ts` |
| lazy import | 추가됨 | `components/Layout/TabContent.tsx` |

다음 단계:
1. 탭 컴포넌트에 실제 기능을 구현하세요
2. 필요한 훅을 `hooks/` 디렉토리에 추가하세요
3. `/verify-lazy-loading`으로 lazy import 패턴을 검증하세요
```

## Exceptions

다음은 **문제가 아닙니다**:

1. **TODO 주석이 남아있는 컴포넌트** - 보일러플레이트이므로 실제 구현은 별도 작업
2. **props 타입이 기본값인 것** - departmentId만 기본 제공하며, 추가 props는 구현 시 정의
