---
name: pf-component
description: pf-frontend 프로젝트 컨벤션에 맞는 React 컴포넌트 생성. "컴포넌트 만들어줘", "새 컴포넌트", "UI 컴포넌트 생성" 요청 시 사용.
allowed-tools: Write, Read, Bash
---

# PF 컴포넌트 생성기

$ARGUMENTS 이름으로 컴포넌트를 생성합니다.

## 컴포넌트 유형 판단

1. **packages/ui 컴포넌트** - 재사용 가능한 공통 UI
   - atoms: 기본 컴포넌트 (Button, Input, Select 등)
   - molecules: 복합 컴포넌트 (Carousel, Widget 등)
   - organisms: 복잡한 컴포넌트 (Sidebar, DataTable 등)

2. **앱 전용 컴포넌트** - 특정 앱에서만 사용
   - `apps/앱이름/src/components/`

---

## packages/ui 컴포넌트 구조

```
packages/ui/src/atoms/ComponentName/
├── ComponentName.tsx        # 메인 컴포넌트
├── index.ts                 # export
├── types.ts                 # Props 타입
├── variants.ts              # CVA 스타일 (필요시)
└── ComponentName.stories.tsx # Storybook (선택)
```

### types.ts 템플릿

```tsx
import type { VariantProps } from "class-variance-authority";
import { componentVariants } from "./variants";

export interface ComponentNameProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {
  /** 컴포넌트 설명 */
  children?: React.ReactNode;
  /** ref 전달 (React 19) */
  ref?: React.Ref<HTMLDivElement>;
}
```

### variants.ts 템플릿 (CVA)

```tsx
import { cva } from "class-variance-authority";

export const componentVariants = cva(
  // Base styles
  "inline-flex items-center justify-center",
  {
    variants: {
      variant: {
        default: "bg-white text-gray-900",
        primary: "bg-brand text-white",
        secondary: "bg-neutral-100 text-gray-700",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-base",
        lg: "h-12 px-6 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);
```

### ComponentName.tsx 템플릿

```tsx
import { cn } from "../../utils";
import { componentVariants } from "./variants";
import type { ComponentNameProps } from "./types";

/**
 * ComponentName 컴포넌트
 *
 * @example
 * <ComponentName variant="primary" size="md">
 *   Content
 * </ComponentName>
 */
function ComponentName({
  className,
  variant,
  size,
  children,
  ref,
  ...props
}: ComponentNameProps) {
  return (
    <div
      ref={ref}
      className={cn(componentVariants({ variant, size, className }))}
      {...props}
    >
      {children}
    </div>
  );
}

export { ComponentName };
```

### index.ts 템플릿

```tsx
export { ComponentName } from "./ComponentName";
export type { ComponentNameProps } from "./types";
```

---

## Composition Pattern (Organism 컴포넌트)

복잡한 컴포넌트는 Context + 서브 컴포넌트 패턴 사용:

```tsx
// Context 생성
import { createContext, useContext, useState } from "react";

interface ComponentContextValue {
  expanded: boolean;
  setExpanded: (value: boolean) => void;
}

const ComponentContext = createContext<ComponentContextValue | null>(null);

function useComponentContext() {
  const context = useContext(ComponentContext);
  if (!context) {
    throw new Error("Component 컨텍스트 내에서 사용해야 합니다");
  }
  return context;
}

// 메인 컴포넌트
interface ComponentNameProps {
  children: React.ReactNode;
  defaultExpanded?: boolean;
}

function ComponentName({ children, defaultExpanded = false }: ComponentNameProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <ComponentContext.Provider value={{ expanded, setExpanded }}>
      <div className="component-wrapper">{children}</div>
    </ComponentContext.Provider>
  );
}

// 서브 컴포넌트
function ComponentHeader({ children }: { children: React.ReactNode }) {
  const { expanded, setExpanded } = useComponentContext();
  return (
    <div className="component-header" onClick={() => setExpanded(!expanded)}>
      {children}
    </div>
  );
}

function ComponentContent({ children }: { children: React.ReactNode }) {
  const { expanded } = useComponentContext();
  if (!expanded) return null;
  return <div className="component-content">{children}</div>;
}

// 서브 컴포넌트 연결
ComponentName.Header = ComponentHeader;
ComponentName.Content = ComponentContent;

export { ComponentName, useComponentContext };
```

**사용:**

```tsx
<ComponentName defaultExpanded>
  <ComponentName.Header>제목</ComponentName.Header>
  <ComponentName.Content>내용</ComponentName.Content>
</ComponentName>
```

---

## 앱 전용 컴포넌트

앱 전용 컴포넌트는 더 간단하게:

```tsx
// apps/앱이름/src/components/FeatureCard.tsx

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  onClick?: () => void;
}

export function FeatureCard({ title, description, icon, onClick }: FeatureCardProps) {
  return (
    <div
      className="rounded-lg border p-4 hover:shadow-md transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-center gap-3">
        {icon}
        <h3 className="font-semibold">{title}</h3>
      </div>
      <p className="mt-2 text-sm text-gray-600">{description}</p>
    </div>
  );
}
```

---

## 중요 규칙

1. **React 19 패턴**
   - `forwardRef` 사용하지 않음
   - ref를 props로 직접 받음
   - 불필요한 memo/useMemo/useCallback 피함

2. **TypeScript**
   - Props 인터페이스 필수
   - `any` 사용 금지

3. **스타일링**
   - Tailwind CSS 사용
   - cn() 유틸리티로 클래스 병합
   - CVA로 variant 관리

4. **Export**
   - named export만 사용 (default export 금지)
   - 타입도 함께 export

5. **문서화**
   - JSDoc 주석 추가
   - @example 포함
