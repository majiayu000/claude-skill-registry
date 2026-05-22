---
name: pf-test-store
description: Zustand 스토어 테스트 생성. "스토어 테스트", "store 테스트" 요청 시 사용.
allowed-tools: Read, Write, Glob
---

# PF Zustand 스토어 테스트 생성기

$ARGUMENTS 스토어에 대한 테스트 파일을 생성합니다.

---

## 기본 테스트 구조

```tsx
import { describe, it, expect, beforeEach } from "vitest";
import { useAuthStore } from "./auth.store";

describe("useAuthStore", () => {
  // 각 테스트 전 스토어 초기화
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      isLoading: true,
    });
  });

  // 1. 초기 상태 테스트
  describe("초기 상태", () => {
    it("user가 null이다", () => {
      const { user } = useAuthStore.getState();
      expect(user).toBeNull();
    });

    it("isLoading이 true다", () => {
      const { isLoading } = useAuthStore.getState();
      expect(isLoading).toBe(true);
    });
  });

  // 2. 액션 테스트
  describe("액션", () => {
    it("setUser가 user를 설정한다", () => {
      const mockUser = { id: 1, name: "Test", email: "test@test.com" };

      useAuthStore.getState().setUser(mockUser);

      const { user, isLoading } = useAuthStore.getState();
      expect(user).toEqual(mockUser);
      expect(isLoading).toBe(false);
    });

    it("clearUser가 user를 초기화한다", () => {
      // 먼저 user 설정
      useAuthStore.getState().setUser({ id: 1, name: "Test" });

      // clearUser 호출
      useAuthStore.getState().clearUser();

      const { user } = useAuthStore.getState();
      expect(user).toBeNull();
    });
  });

  // 3. Selector 테스트
  describe("Selector", () => {
    it("selectUser가 user를 반환한다", () => {
      const mockUser = { id: 1, name: "Test" };
      useAuthStore.setState({ user: mockUser });

      const user = selectUser(useAuthStore.getState());
      expect(user).toEqual(mockUser);
    });

    it("selectIsAuthenticated가 인증 상태를 반환한다", () => {
      expect(selectIsAuthenticated(useAuthStore.getState())).toBe(false);

      useAuthStore.setState({ user: { id: 1 } });

      expect(selectIsAuthenticated(useAuthStore.getState())).toBe(true);
    });
  });
});
```

---

## Persist 미들웨어 테스트

```tsx
import { describe, it, expect, beforeEach, vi } from "vitest";

// localStorage 모킹
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value;
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();

Object.defineProperty(window, "localStorage", { value: localStorageMock });

describe("useAuthStore (persist)", () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  it("상태가 localStorage에 저장된다", () => {
    const mockUser = { id: 1, name: "Test" };
    useAuthStore.getState().setUser(mockUser);

    expect(localStorageMock.setItem).toHaveBeenCalled();

    const savedData = JSON.parse(
      localStorageMock.setItem.mock.calls[0][1]
    );
    expect(savedData.state.user).toEqual(mockUser);
  });

  it("partialize로 지정한 필드만 저장된다", () => {
    useAuthStore.setState({
      user: { id: 1 },
      isLoading: false,
      tempData: "should not persist",
    });

    const savedData = JSON.parse(
      localStorageMock.setItem.mock.calls[0][1]
    );

    expect(savedData.state.user).toBeDefined();
    expect(savedData.state.tempData).toBeUndefined();
  });
});
```

---

## 비동기 액션 테스트

```tsx
import { vi } from "vitest";
import { userService } from "@/services/user.service";

vi.mock("@/services/user.service");

describe("useUserStore 비동기 액션", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    useUserStore.setState({ users: [], isLoading: false, error: null });
  });

  it("fetchUsers가 성공하면 users를 설정한다", async () => {
    const mockUsers = [{ id: 1 }, { id: 2 }];
    vi.mocked(userService.getUsers).mockResolvedValue({
      data: { content: mockUsers },
    });

    await useUserStore.getState().fetchUsers();

    const { users, isLoading, error } = useUserStore.getState();
    expect(users).toEqual(mockUsers);
    expect(isLoading).toBe(false);
    expect(error).toBeNull();
  });

  it("fetchUsers가 실패하면 error를 설정한다", async () => {
    vi.mocked(userService.getUsers).mockRejectedValue(
      new Error("Network error")
    );

    await useUserStore.getState().fetchUsers();

    const { users, error } = useUserStore.getState();
    expect(users).toEqual([]);
    expect(error).toBe("Network error");
  });

  it("fetchUsers 중 isLoading이 true다", async () => {
    vi.mocked(userService.getUsers).mockImplementation(
      () => new Promise(() => {}) // never resolves
    );

    const fetchPromise = useUserStore.getState().fetchUsers();

    expect(useUserStore.getState().isLoading).toBe(true);
  });
});
```

---

## 스토어 구독 테스트

```tsx
describe("스토어 구독", () => {
  it("상태 변경 시 구독자가 호출된다", () => {
    const listener = vi.fn();

    const unsubscribe = useAuthStore.subscribe(listener);

    useAuthStore.getState().setUser({ id: 1 });

    expect(listener).toHaveBeenCalled();

    unsubscribe();
  });

  it("selector로 특정 값만 구독한다", () => {
    const listener = vi.fn();

    const unsubscribe = useAuthStore.subscribe(
      (state) => state.user,
      listener
    );

    // user 변경 → 호출됨
    useAuthStore.getState().setUser({ id: 1 });
    expect(listener).toHaveBeenCalledTimes(1);

    // isLoading만 변경 → 호출 안됨
    useAuthStore.setState({ isLoading: false });
    expect(listener).toHaveBeenCalledTimes(1);

    unsubscribe();
  });
});
```

---

## 테스트 체크리스트

- [ ] 초기 상태가 올바른가
- [ ] 모든 액션이 상태를 올바르게 변경하는가
- [ ] Selector가 올바른 값을 반환하는가
- [ ] persist 설정이 동작하는가
- [ ] 비동기 액션의 로딩/에러 상태가 올바른가
- [ ] 구독이 올바르게 동작하는가
