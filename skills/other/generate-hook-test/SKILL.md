---
name: generate-hook-test
description: 훅 테스트 템플릿을 자동 생성합니다. 프로젝트의 47개 테스트 파일 패턴을 재활용합니다. 새 훅 작성 후 사용.
argument-hint: "[훅 파일명 (예: 'useNewFeature')]"
---

## Purpose

새로운 커스텀 훅에 대한 테스트 파일을 프로젝트의 기존 패턴에 맞춰 자동 생성합니다:

1. **Firebase mock 설정** - 프로젝트 표준 Firebase mock 패턴 적용
2. **React Query wrapper** - renderHook용 QueryClientProvider 래핑
3. **테스트 구조** - describe/it 블록 구조화
4. **주요 시나리오** - 쿼리/mutation/에러 핸들링 테스트 케이스

## When to Run

- `hooks/` 디렉토리에 새 훅을 추가한 후
- 테스트가 누락된 기존 훅의 테스트를 작성할 때

## Related Files

| File | Purpose |
|------|---------|
| `vitest.config.ts` | Vitest 설정 (globals: true, happy-dom) |
| `tests/hooks/` | 기존 훅 테스트 파일 (47개) |
| `tests/setup.test.ts` | 테스트 설정 파일 |

## Workflow

### Step 1: 대상 훅 분석

인수로 전달된 훅 파일을 읽고 다음을 분석합니다:

1. **import 목록** - Firebase, React Query, 다른 훅 등
2. **export 목록** - 반환하는 함수/상태
3. **useQuery 사용 여부** - queryKey, enabled 등
4. **useMutation 사용 여부** - onSuccess, invalidateQueries 등
5. **onSnapshot 사용 여부** - 실시간 리스너
6. **의존성** - departmentId, userId 등 필수 파라미터

### Step 2: 테스트 파일 생성

**파일 위치:** `tests/hooks/<hookName>.test.ts` (JSX 사용 시 `.test.tsx`)

**템플릿 구조:**

```typescript
// Vitest globals: true - describe/it/expect/vi를 import하지 않음

// Firebase mock
vi.mock('firebase/firestore', () => ({
  collection: vi.fn((...args: any[]) => ({ __type: 'collection', __name: args[1] })),
  doc: vi.fn(() => ({})),
  getDocs: vi.fn(),
  getDoc: vi.fn(),
  setDoc: vi.fn(),
  updateDoc: vi.fn(),
  deleteDoc: vi.fn(),
  writeBatch: vi.fn(() => ({ set: vi.fn(), update: vi.fn(), delete: vi.fn(), commit: vi.fn() })),
  query: vi.fn((...args: any[]) => args[0]),
  where: vi.fn(),
  orderBy: vi.fn(),
  onSnapshot: vi.fn(),
}));

vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(),
}));

vi.mock('../firebaseConfig', () => ({
  db: {},
  auth: {},
}));

// React Query wrapper
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderHook, waitFor, act } from '@testing-library/react';
import React from 'react';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children);
}

// 훅 import
import { use<HookName> } from '../../hooks/use<HookName>';

describe('use<HookName>', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // 쿼리 훅인 경우:
  describe('데이터 조회', () => {
    it('데이터를 정상적으로 조회한다', async () => {
      // getDocs mock 설정
      // renderHook + waitFor
    });

    it('의존성이 없으면 쿼리가 비활성화된다', () => {
      // enabled: false 검증
    });
  });

  // mutation 훅인 경우:
  describe('mutation', () => {
    it('데이터를 생성한다', async () => {
      // setDoc mock + act + mutate 호출
    });

    it('성공 시 캐시를 무효화한다', async () => {
      // invalidateQueries 호출 검증
    });

    it('에러 시 에러를 처리한다', async () => {
      // setDoc.mockRejectedValue + onError 검증
    });
  });
});
```

### Step 3: 테스트 실행 및 검증

```bash
npx vitest run tests/hooks/<hookName>.test.ts --reporter=verbose 2>&1 | head -30
```

**PASS 기준:** 모든 테스트 통과
**FAIL 기준:** 테스트 실패 → mock 설정 또는 assertion 수정

### Step 4: 결과 보고

## Output Format

```markdown
## 테스트 생성 완료

| 항목 | 상태 |
|------|------|
| 파일 | `tests/hooks/<hookName>.test.ts` |
| 테스트 수 | N개 |
| 커버리지 | 쿼리: X개, mutation: Y개, 에러: Z개 |

주요 패턴:
- Firebase mock: ✅
- React Query wrapper: ✅
- Vitest globals: ✅ (import 없음)
```

## Exceptions

다음은 **문제가 아닙니다**:

1. **`.test.tsx` 확장자** - JSX를 사용하는 테스트(renderHook wrapper)는 `.test.tsx` 필수
2. **vi.clearAllMocks() vs vi.restoreAllMocks()** - clearAllMocks를 기본 사용 (restoreAllMocks는 require() 패턴을 깨뜨릴 수 있음)
3. **Firebase mock에서 marker 객체 사용** - `vi.fn((...args) => ({ __type: 'collection', __name: args[1] }))`는 getDocs가 쿼리를 구별할 수 있게 하는 프로젝트 표준 패턴
