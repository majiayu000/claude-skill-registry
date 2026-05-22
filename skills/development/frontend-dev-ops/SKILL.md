---
name: frontend-dev-ops
description: Frontend development and UI implementation for web and mobile applications. Use for React, Next.js, React Native, TypeScript, Tailwind CSS, component libraries, responsive design, state management, API integration, and UI/UX implementation. Triggers on queries like "build the frontend", "create UI components", "implement this screen", "style this page", "add responsive design", or any frontend development task.
---

# Frontend Development Operations

Build production-quality frontend interfaces for web and mobile applications.

## Tech Stack Defaults

| Platform | Framework | Styling | State |
|----------|-----------|---------|-------|
| Web | Next.js 14+ (App Router) | Tailwind CSS | React Query + Zustand |
| Mobile | React Native + Expo | NativeWind | React Query + Zustand |
| Components | shadcn/ui (web), custom (mobile) | - | - |

## Project Setup

### Next.js Web App
```bash
npx create-next-app@latest project-name --typescript --tailwind --eslint --app --src-dir
cd project-name
npx shadcn@latest init
```

### React Native Mobile App
```bash
npx create-expo-app project-name --template blank-typescript
cd project-name
npm install nativewind tailwindcss react-native-reanimated
npx tailwindcss init
```

## Standard Structure

```
src/
├── app/                    # Routes (Next.js) or screens (RN)
│   ├── (auth)/            # Auth-gated routes
│   ├── (public)/          # Public routes
│   └── api/               # API routes (Next.js)
├── components/
│   ├── ui/                # Base components (buttons, inputs)
│   ├── features/          # Feature-specific components
│   └── layouts/           # Layout wrappers
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities and helpers
│   ├── api.ts            # API client
│   ├── utils.ts          # General utilities
│   └── constants.ts      # App constants
├── stores/               # State management
├── types/                # TypeScript definitions
└── styles/               # Global styles (if needed)
```

## Component Patterns

### Functional Component Template
```typescript
interface ComponentProps {
  title: string;
  onAction?: () => void;
  children?: React.ReactNode;
}

export function Component({ title, onAction, children }: ComponentProps) {
  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold">{title}</h2>
      {children}
      {onAction && (
        <button onClick={onAction} className="mt-2 btn-primary">
          Action
        </button>
      )}
    </div>
  );
}
```

### Custom Hook Template
```typescript
export function useFeature(id: string) {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchData(id)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [id]);

  return { data, loading, error };
}
```

## API Integration

### API Client Setup
```typescript
// lib/api.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`);
  }
  
  return res.json();
}
```

### React Query Pattern
```typescript
// hooks/useItems.ts
export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: () => apiClient<Item[]>('/api/items'),
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateItemInput) => 
      apiClient<Item>('/api/items', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
```

## State Management

### Zustand Store Pattern
```typescript
// stores/appStore.ts
interface AppState {
  user: User | null;
  setUser: (user: User | null) => void;
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  theme: 'light',
  toggleTheme: () => set((state) => ({ 
    theme: state.theme === 'light' ? 'dark' : 'light' 
  })),
}));
```

## Auth UI Patterns

### Protected Route (Next.js)
```typescript
// app/(auth)/layout.tsx
export default async function AuthLayout({ children }: { children: React.ReactNode }) {
  const session = await getSession();
  
  if (!session) {
    redirect('/login');
  }
  
  return <>{children}</>;
}
```

### Login Form
```typescript
export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await signIn(email, password);
    } catch (error) {
      toast.error('Login failed');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input 
        type="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <Input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <Button type="submit" disabled={loading}>
        {loading ? 'Signing in...' : 'Sign In'}
      </Button>
    </form>
  );
}
```

## Responsive Design

### Breakpoint Strategy
```
sm: 640px   - Mobile landscape
md: 768px   - Tablets
lg: 1024px  - Desktop
xl: 1280px  - Large desktop
```

### Responsive Pattern
```typescript
<div className="
  grid grid-cols-1 
  sm:grid-cols-2 
  lg:grid-cols-3 
  gap-4 p-4
">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

## Loading & Error States

### Loading Skeleton
```typescript
export function CardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

### Error Boundary
```typescript
export function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div className="p-4 text-center">
      <p className="text-red-600">Something went wrong</p>
      <button onClick={resetErrorBoundary} className="mt-2 btn-secondary">
        Try again
      </button>
    </div>
  );
}
```

## Quality Checklist

Before marking frontend task complete:
- [ ] TypeScript: No `any` types, proper interfaces
- [ ] Responsive: Works on mobile, tablet, desktop
- [ ] Loading states: Skeletons or spinners
- [ ] Error states: User-friendly error handling
- [ ] Accessibility: Semantic HTML, ARIA labels, keyboard nav
- [ ] Performance: No unnecessary re-renders, lazy loading
- [ ] Build: `npm run build` passes without errors
