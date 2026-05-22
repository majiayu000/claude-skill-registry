---
name: frontend-pattern
description: React 19 및 Next.js 16 패턴을 적용하는 스킬
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Frontend Pattern Skill

이 스킬은 ForkLore 프로젝트의 프론트엔드 개발 패턴을 적용합니다.

## Next.js 16 App Router 패턴

### 1. Server vs Client Components

```typescript
// Server Component (기본값) - 데이터 페칭, SEO
// app/novels/page.tsx
export default async function NovelsPage() {
  const novels = await fetchNovels();  // 서버에서 직접 fetch
  return <NovelList novels={novels} />;
}

// Client Component - 상호작용 필요시만
// components/novel-like-button.tsx
'use client';

import { useState } from 'react';

export function NovelLikeButton({ novelId }: { novelId: number }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>♥</button>;
}
```

**규칙**: 
- 기본은 Server Component
- `useState`, `useEffect`, 이벤트 핸들러 필요시만 `'use client'`

### 2. 데이터 페칭 패턴

```typescript
// Server Action (폼 제출, 데이터 변경)
// app/actions/novel.ts
'use server';

export async function createNovel(formData: FormData) {
  const title = formData.get('title') as string;
  const response = await fetch('/api/novels', {
    method: 'POST',
    body: JSON.stringify({ title }),
  });
  revalidatePath('/novels');
  return response.json();
}

// 사용
<form action={createNovel}>
  <input name="title" />
  <button type="submit">생성</button>
</form>
```

### 3. 비동기 params/searchParams (Next.js 15+)

```typescript
// ✅ Next.js 15+ 방식 (async 필수)
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ page?: string }>;
}) {
  const { id } = await params;
  const { page } = await searchParams;
  // ...
}

// ❌ 이전 방식 (동기) - 더 이상 사용 금지
export default function Page({ params }: { params: { id: string } }) {
  // ...
}
```

## React 19 패턴

### 1. 새로운 훅

```typescript
// use() - Promise/Context 직접 사용
import { use } from 'react';

function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);  // Suspense와 함께 사용
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}

// useOptimistic() - 낙관적 업데이트
function LikeButton({ count, onLike }) {
  const [optimisticCount, addOptimistic] = useOptimistic(count);
  
  async function handleLike() {
    addOptimistic(prev => prev + 1);
    await onLike();
  }
  
  return <button onClick={handleLike}>{optimisticCount}</button>;
}

// useFormStatus() - 폼 제출 상태
function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? '저장 중...' : '저장'}</button>;
}

// useActionState() - 서버 액션 상태
function Form() {
  const [state, formAction, isPending] = useActionState(createNovel, null);
  return <form action={formAction}>...</form>;
}
```

### 2. ref를 prop으로 전달 (forwardRef 불필요)

```typescript
// ✅ React 19 - ref를 직접 prop으로
function Input({ ref, ...props }) {
  return <input ref={ref} {...props} />;
}

// ❌ 이전 방식 - forwardRef 사용
const Input = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});
```

## Shadcn/ui 패턴

### 1. 컴포넌트 사용

```typescript
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

function MyComponent({ className }) {
  return (
    <div className={cn("flex gap-2", className)}>
      <Input placeholder="제목" />
      <Button variant="default">저장</Button>
    </div>
  );
}
```

### 2. 폼 + Zod 검증

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Form, FormField, FormItem, FormLabel, FormControl } from '@/components/ui/form';

const schema = z.object({
  title: z.string().min(1, '제목은 필수입니다'),
  genre: z.enum(['FANTASY', 'ROMANCE', 'SF']),
});

function NovelForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { title: '', genre: 'FANTASY' },
  });
  
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>제목</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
            </FormItem>
          )}
        />
      </form>
    </Form>
  );
}
```

## 타입 안전성 규칙

**절대 금지**:
- `as any`
- `@ts-ignore`
- `@ts-expect-error`

```typescript
// ❌ 금지
const data = response as any;

// ✅ 올바른 방법
interface NovelResponse { id: number; title: string; }
const data: NovelResponse = await response.json();
```

## 체크리스트

- [ ] Server/Client 컴포넌트가 적절히 분리되었는가?
- [ ] async params/searchParams를 사용하는가? (Next.js 15+)
- [ ] 타입 안전성이 유지되는가? (any 금지)
- [ ] React 19 훅을 적절히 활용하는가?
- [ ] Shadcn/ui 컴포넌트를 올바르게 사용하는가?
