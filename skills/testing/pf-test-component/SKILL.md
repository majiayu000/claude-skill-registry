---
name: pf-test-component
description: UI 컴포넌트 테스트 생성. "테스트 만들어줘", "컴포넌트 테스트" 요청 시 사용.
allowed-tools: Read, Write, Glob
---

# PF 컴포넌트 테스트 생성기

$ARGUMENTS 컴포넌트에 대한 테스트 파일을 생성합니다.

---

## 테스트 파일 위치

```
packages/ui/src/atoms/Button/
├── Button.tsx
├── Button.test.tsx  ← 생성
└── ...
```

---

## 테스트 구조 (Vitest + React Testing Library)

```tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { Button } from "./Button";

describe("Button", () => {
  // 1. 렌더링 테스트
  describe("렌더링", () => {
    it("children을 렌더링한다", () => {
      render(<Button>클릭</Button>);
      expect(screen.getByRole("button")).toHaveTextContent("클릭");
    });

    it("variant에 따라 스타일이 적용된다", () => {
      render(<Button variant="secondary">버튼</Button>);
      expect(screen.getByRole("button")).toHaveClass("bg-neutral-50");
    });

    it("size에 따라 크기가 변경된다", () => {
      render(<Button size="lg">버튼</Button>);
      expect(screen.getByRole("button")).toHaveClass("h-12");
    });
  });

  // 2. 상호작용 테스트
  describe("상호작용", () => {
    it("클릭 시 onClick이 호출된다", () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>클릭</Button>);

      fireEvent.click(screen.getByRole("button"));

      expect(handleClick).toHaveBeenCalledOnce();
    });

    it("disabled일 때 클릭이 무시된다", () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick} disabled>클릭</Button>);

      fireEvent.click(screen.getByRole("button"));

      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  // 3. 접근성 테스트
  describe("접근성", () => {
    it("키보드로 활성화할 수 있다", () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>클릭</Button>);

      const button = screen.getByRole("button");
      button.focus();
      fireEvent.keyDown(button, { key: "Enter" });

      expect(handleClick).toHaveBeenCalled();
    });

    it("aria-label이 적용된다", () => {
      render(<Button aria-label="닫기">X</Button>);
      expect(screen.getByRole("button")).toHaveAccessibleName("닫기");
    });
  });

  // 4. 엣지 케이스
  describe("엣지 케이스", () => {
    it("asChild로 다른 요소로 렌더링된다", () => {
      render(
        <Button asChild>
          <a href="/link">링크</a>
        </Button>
      );
      expect(screen.getByRole("link")).toBeInTheDocument();
    });

    it("ref가 전달된다", () => {
      const ref = { current: null };
      render(<Button ref={ref}>버튼</Button>);
      expect(ref.current).toBeInstanceOf(HTMLButtonElement);
    });
  });
});
```

---

## CVA 컴포넌트 테스트 패턴

variants.ts가 있는 경우:

```tsx
import { buttonVariants } from "./variants";

describe("buttonVariants", () => {
  it("기본 variant와 size가 적용된다", () => {
    const classes = buttonVariants();
    expect(classes).toContain("bg-brand");
    expect(classes).toContain("h-10");
  });

  it("모든 variant 조합이 유효하다", () => {
    const variants = ["default", "secondary", "outline", "ghost"] as const;
    const sizes = ["sm", "md", "lg"] as const;

    variants.forEach(variant => {
      sizes.forEach(size => {
        expect(() => buttonVariants({ variant, size })).not.toThrow();
      });
    });
  });
});
```

---

## Composition Pattern 테스트

Sidebar 같은 복합 컴포넌트:

```tsx
describe("Sidebar", () => {
  it("서브 컴포넌트가 함께 렌더링된다", () => {
    render(
      <Sidebar>
        <Sidebar.Header title="대시보드" />
        <Sidebar.Item>메뉴1</Sidebar.Item>
        <Sidebar.Footer />
      </Sidebar>
    );

    expect(screen.getByText("대시보드")).toBeInTheDocument();
    expect(screen.getByText("메뉴1")).toBeInTheDocument();
  });

  it("collapsed 상태가 Context로 전달된다", () => {
    render(
      <Sidebar defaultCollapsed>
        <Sidebar.Header title="대시보드" />
      </Sidebar>
    );

    // collapsed 상태에서 title이 숨겨지는지 확인
    expect(screen.queryByText("대시보드")).not.toBeVisible();
  });
});
```

---

## 테스트 체크리스트

- [ ] 모든 props가 테스트되는가
- [ ] 기본값이 올바른가
- [ ] 사용자 상호작용이 동작하는가
- [ ] 접근성 요구사항이 충족되는가
- [ ] 엣지 케이스가 처리되는가
- [ ] ref 전달이 동작하는가

---

## Context7 참고

최신 Vitest, React Testing Library 문법이 필요하면 Context7로 조회하세요.
