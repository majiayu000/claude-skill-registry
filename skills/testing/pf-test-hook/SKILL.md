---
name: pf-test-hook
description: 커스텀 훅 테스트 생성. "훅 테스트", "hook 테스트" 요청 시 사용.
allowed-tools: Read, Write, Glob
---

# PF 커스텀 훅 테스트 생성기

$ARGUMENTS 훅에 대한 테스트 파일을 생성합니다.

---

## 테스트 구조 (Vitest + @testing-library/react)

```tsx
import { renderHook, act, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  // 1. 초기 상태 테스트
  describe("초기화", () => {
    it("기본값 0으로 시작한다", () => {
      const { result } = renderHook(() => useCounter());
      expect(result.current.count).toBe(0);
    });

    it("initialValue로 시작한다", () => {
      const { result } = renderHook(() => useCounter(10));
      expect(result.current.count).toBe(10);
    });
  });

  // 2. 액션 테스트
  describe("액션", () => {
    it("increment가 count를 1 증가시킨다", () => {
      const { result } = renderHook(() => useCounter());

      act(() => {
        result.current.increment();
      });

      expect(result.current.count).toBe(1);
    });

    it("decrement가 count를 1 감소시킨다", () => {
      const { result } = renderHook(() => useCounter(5));

      act(() => {
        result.current.decrement();
      });

      expect(result.current.count).toBe(4);
    });

    it("reset이 initialValue로 되돌린다", () => {
      const { result } = renderHook(() => useCounter(10));

      act(() => {
        result.current.increment();
        result.current.increment();
        result.current.reset();
      });

      expect(result.current.count).toBe(10);
    });
  });

  // 3. props 변경 테스트
  describe("props 변경", () => {
    it("initialValue 변경 시 reset하면 새 값으로", () => {
      const { result, rerender } = renderHook(
        ({ initial }) => useCounter(initial),
        { initialProps: { initial: 0 } }
      );

      rerender({ initial: 100 });

      act(() => {
        result.current.reset();
      });

      expect(result.current.count).toBe(100);
    });
  });
});
```

---

## 비동기 훅 테스트

```tsx
import { renderHook, waitFor } from "@testing-library/react";

describe("useFetch", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("데이터를 성공적으로 가져온다", async () => {
    const mockData = { id: 1, name: "Test" };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    });

    const { result } = renderHook(() => useFetch("/api/test"));

    // 로딩 상태 확인
    expect(result.current.isLoading).toBe(true);

    // 데이터 로드 대기
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual(mockData);
    expect(result.current.error).toBeNull();
  });

  it("에러를 처리한다", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    const { result } = renderHook(() => useFetch("/api/test"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toBeNull();
    expect(result.current.error).toBe("Network error");
  });
});
```

---

## Zustand Store를 사용하는 훅 테스트

```tsx
import { renderHook, act } from "@testing-library/react";
import { useAuthStore } from "@/stores/auth.store";

// Store 초기화
beforeEach(() => {
  useAuthStore.setState({ user: null, isLoading: false });
});

describe("useAuth", () => {
  it("로그인 성공 시 user가 설정된다", async () => {
    const mockUser = { id: 1, name: "Test User" };
    vi.spyOn(authService, "login").mockResolvedValue(mockUser);

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login("test@test.com", "password");
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
  });
});
```

---

## Context Provider가 필요한 훅 테스트

```tsx
import { renderHook } from "@testing-library/react";
import { ReactNode } from "react";

const wrapper = ({ children }: { children: ReactNode }) => (
  <ThemeProvider defaultTheme="light">
    <AuthProvider>
      {children}
    </AuthProvider>
  </ThemeProvider>
);

describe("useTheme", () => {
  it("현재 테마를 반환한다", () => {
    const { result } = renderHook(() => useTheme(), { wrapper });
    expect(result.current.theme).toBe("light");
  });
});
```

---

## 테스트 체크리스트

- [ ] 초기 상태가 올바른가
- [ ] 모든 반환값이 테스트되는가
- [ ] 액션이 상태를 올바르게 변경하는가
- [ ] props/deps 변경에 반응하는가
- [ ] cleanup이 제대로 동작하는가 (useEffect)
- [ ] 에러 케이스가 처리되는가
