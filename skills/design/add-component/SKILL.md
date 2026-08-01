---
name: add-component
description: Add a new component following Next.js 15 and shadcn/ui best practices
---

---
name: add-component
description: 새 React 컴포넌트를 생성합니다. shadcn/ui 스타일과 프로젝트 컨벤션을 준수합니다. 사용법: /add-component ComponentName [directory]
---

# Add Component

새 React 컴포넌트를 프로젝트 컨벤션에 맞게 생성합니다.

## Instructions

1. 사용자로부터 컴포넌트 이름(PascalCase)과 선택적으로 디렉토리를 받습니다
2. 기본 디렉토리는 `src/components/common/`입니다
3. 다음 파일을 생성합니다:
   - `src/components/{directory}/{ComponentName}.tsx`
4. 해당 디렉토리에 `index.ts`가 있으면 export를 추가합니다

## Template

```tsx
import { cn } from "@/lib/utils";

interface ${ComponentName}Props {
  className?: string;
  children?: React.ReactNode;
}

export function ${ComponentName}({ className, children }: ${ComponentName}Props) {
  return (
    <div className={cn("", className)}>
      {children}
    </div>
  );
}
```

## Checklist

- Props 인터페이스 정의
- `cn()` 유틸리티 사용
- className prop 지원
- named export 사용

## Examples

```
/add-component UserAvatar common
```

→ `src/components/common/UserAvatar.tsx` 생성
