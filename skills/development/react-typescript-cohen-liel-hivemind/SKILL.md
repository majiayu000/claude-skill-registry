---
name: react-typescript
description: React + TypeScript patterns for production frontends. Use when building React components, hooks, state management, forms, routing, or any React/TSX UI.
---

# React + TypeScript Patterns

## Project Structure
```
src/
  components/     # Reusable UI components
  pages/          # Route-level components
  hooks/          # Custom hooks (useAuth, useApi, etc.)
  store/          # Zustand/Redux state
  api/            # API client functions (axios/fetch wrappers)
  types/          # Shared TypeScript types/interfaces
  utils/          # Pure utility functions
```

## Component Pattern
```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
  isLoading?: boolean
}

export const Button: React.FC<ButtonProps> = ({
  label, onClick, variant = 'primary', disabled, isLoading
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`btn btn-${variant}`}
    >
      {isLoading ? <Spinner /> : label}
    </button>
  )
}
```

## Custom Hook Pattern
```tsx
function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    fetch(url, { signal: controller.signal })
      .then(r => r.json())
      .then(setData)
      .catch(e => { if (e.name !== 'AbortError') setError(e.message) })
      .finally(() => setLoading(false))
    return () => controller.abort()
  }, [url])

  return { data, loading, error }
}
```

## State Management (Zustand)
```tsx
interface AuthStore {
  user: User | null
  token: string | null
  login: (user: User, token: string) => void
  logout: () => void
}

const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  login: (user, token) => set({ user, token }),
  logout: () => set({ user: null, token: null }),
}))
```

## Form Pattern (React Hook Form)
```tsx
const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema)
})
```

## Rules
- Always type props explicitly — no `any`
- Use `React.FC<Props>` for components
- Cleanup effects: return cleanup function from useEffect
- Memoize expensive computations with useMemo
- Memoize callbacks passed to children with useCallback
- Split large components: <300 lines per file
- Error boundaries around page-level components
- Lazy load routes: `const Page = React.lazy(() => import('./Page'))`
