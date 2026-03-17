---
name: frontend
description: 프론트엔드 개발 스킬. React 컴포넌트, 커스텀 훅, Tailwind 스타일링. UI 작업 시 사용.
---

# Frontend Skill

## Chrome Extension UI 구조

### Popup (주요 UI)

```
src/popup/
├── Popup.tsx           # 메인 엔트리
├── components/
│   ├── LinkCard.tsx    # 링크 카드 컴포넌트
│   ├── TagFilter.tsx   # 태그 필터 UI
│   ├── SearchBar.tsx   # 검색 바
│   └── LinkList.tsx    # 링크 목록
└── hooks/
    ├── useLinks.ts     # 링크 CRUD 훅
    ├── useTags.ts      # 태그 관리 훅
    └── useSearch.ts    # 검색 훅
```

### Options Page (설정)

```
src/options/
├── Options.tsx         # 설정 페이지 엔트리
└── components/
    ├── ExportImport.tsx
    └── ThemeSelector.tsx
```

## 컴포넌트 규칙

### 함수형 컴포넌트만 사용

```tsx
// Good
export function LinkCard({ link, onDelete }: LinkCardProps) {
  return (
    <div className="p-4 border rounded-lg">
      {/* ... */}
    </div>
  );
}

// Bad - 클래스 컴포넌트
class LinkCard extends React.Component { }
```

### Props 타입 정의

```tsx
interface LinkCardProps {
  link: Link;
  onDelete: (id: string) => void;
  onTagClick?: (tag: string) => void;
}
```

### 커스텀 훅 패턴

```tsx
// useLinks.ts
export function useLinks() {
  const [links, setLinks] = useState<Link[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLinks();
  }, []);

  async function loadLinks() {
    setLoading(true);
    const data = await getLinks();
    setLinks(data);
    setLoading(false);
  }

  async function addLink(input: CreateLinkInput) {
    const newLink = createLink(input);
    await saveLink(newLink);
    setLinks(prev => [...prev, newLink]);
  }

  return { links, loading, addLink, /* ... */ };
}
```

## Tailwind CSS 규칙

### 유틸리티 클래스 우선

```tsx
// Good - Tailwind 유틸리티
<div className="flex items-center gap-2 p-4 bg-white rounded-lg shadow">

// Avoid - 커스텀 CSS
<div className="link-card">
```

### 반응형 디자인

```tsx
// Popup 크기 고려 (400px width 기준)
<div className="w-full max-w-[400px]">
```

### 다크 모드 지원

```tsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
```

## 에러 핸들링

### 로딩/에러 상태 표시

```tsx
function LinkList() {
  const { links, loading, error } = useLinks();

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;
  if (links.length === 0) return <EmptyState />;

  return (
    <div className="space-y-2">
      {links.map(link => (
        <LinkCard key={link.id} link={link} />
      ))}
    </div>
  );
}
```

## 접근성 (A11y)

### 기본 규칙

- 버튼에 `aria-label` 제공 (아이콘만 있는 경우)
- 포커스 상태 표시 (`focus:ring-2`)
- 시맨틱 HTML 사용 (`<button>`, `<nav>`, `<main>`)

```tsx
<button
  aria-label="Delete link"
  onClick={handleDelete}
  className="p-2 hover:bg-gray-100 focus:ring-2 focus:ring-blue-500 rounded"
>
  <TrashIcon className="w-4 h-4" />
</button>
```

## 체크리스트

- [ ] 함수형 컴포넌트 사용
- [ ] Props 타입 정의
- [ ] 로딩/에러 상태 처리
- [ ] Tailwind 유틸리티 사용
- [ ] 접근성 고려
- [ ] 다크 모드 지원

> 상세 패턴은 코드베이스의 기존 구현 참조
