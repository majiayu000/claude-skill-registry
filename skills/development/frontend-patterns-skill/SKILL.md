---
document_name: "frontend-patterns.skill.md"
location: ".claude/skills/frontend-patterns.skill.md"
codebook_id: "CB-SKILL-FRONTPAT-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for frontend architecture patterns"
skill_metadata:
  category: "development"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Frontend framework knowledge"
    - "State management"
category: "skills"
status: "active"
tags:
  - "skill"
  - "frontend"
  - "architecture"
  - "patterns"
ai_parser_instructions: |
  This skill defines frontend architectural patterns.
  Used by Frontend Engineer agent.
---

# Frontend Patterns Skill

=== PURPOSE ===

Procedures for implementing frontend architectural patterns.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(frontend-engineer) @ref(CB-AGENT-FRONTEND-001) | Primary skill for architecture |

=== PATTERN: Feature-Based Structure ===

**Directory Organization:**
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/
│   │   └── index.ts
│   ├── users/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── index.ts
│   └── ...
├── shared/
│   ├── components/    # Reusable UI components
│   ├── hooks/         # Shared hooks
│   ├── utils/         # Utility functions
│   └── types/         # Shared types
├── pages/             # Route components
└── App.tsx
```

**Export Pattern:**
```typescript
// features/users/index.ts
export { UserList } from './components/UserList';
export { UserProfile } from './components/UserProfile';
export { useUser, useUsers } from './hooks';
export type { User, UserFilters } from './types';
```

=== PATTERN: State Management ===

**State Categories:**
```
┌─────────────────────────────────────────┐
│            State Types                  │
├─────────────────────────────────────────┤
│ UI State      │ Local useState/useReducer│
│ Server State  │ React Query/SWR         │
│ Form State    │ React Hook Form         │
│ Global State  │ Context/Zustand/Redux   │
│ URL State     │ Router params/search    │
└─────────────────────────────────────────┘
```

**When to Use What:**
| State Type | Tool | Example |
|------------|------|---------|
| Modal open/closed | useState | `const [isOpen, setIsOpen] = useState(false)` |
| API data | React Query | `const { data } = useQuery(['users'], getUsers)` |
| Form values | React Hook Form | `const { register } = useForm()` |
| Auth/Theme | Context | `const user = useContext(AuthContext)` |
| Filter params | URL | `/users?status=active&page=2` |

=== PATTERN: Custom Hooks ===

**Data Fetching Hook:**
```typescript
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => userService.getById(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Usage
const { data: user, isLoading, error } = useUser(userId);
```

**Local Storage Hook:**
```typescript
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

**Toggle Hook:**
```typescript
export function useToggle(initial = false) {
  const [value, setValue] = useState(initial);

  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
}
```

=== PATTERN: Compound Components ===

**Implementation:**
```typescript
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

export function Tabs({ children, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.Tab = function Tab({ id, children }: TabProps) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  return (
    <button
      role="tab"
      aria-selected={context.activeTab === id}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function Panel({ id, children }: PanelProps) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Panel must be used within Tabs');
  if (context.activeTab !== id) return null;

  return <div role="tabpanel">{children}</div>;
};

// Usage
<Tabs defaultTab="profile">
  <Tabs.Tab id="profile">Profile</Tabs.Tab>
  <Tabs.Tab id="settings">Settings</Tabs.Tab>

  <Tabs.Panel id="profile"><ProfileContent /></Tabs.Panel>
  <Tabs.Panel id="settings"><SettingsContent /></Tabs.Panel>
</Tabs>
```

=== PATTERN: Error Boundaries ===

**Implementation:**
```typescript
interface ErrorBoundaryProps {
  fallback: ReactNode | ((error: Error) => ReactNode);
  children: ReactNode;
}

export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  { error: Error | null }
> {
  state = { error: null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Error caught:', error, info);
    // Report to monitoring service
  }

  render() {
    if (this.state.error) {
      return typeof this.props.fallback === 'function'
        ? this.props.fallback(this.state.error)
        : this.props.fallback;
    }
    return this.props.children;
  }
}
```

**Usage:**
```typescript
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

=== PATTERN: Loading States ===

**Skeleton Pattern:**
```typescript
export function UserCard({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) {
    return <UserCardSkeleton />;
  }

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

function UserCardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-6 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

=== PATTERN: API Integration ===

**Service Layer:**
```typescript
// services/users.ts
const API_BASE = '/api/v1';

export const userService = {
  async getAll(filters?: UserFilters): Promise<User[]> {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE}/users?${params}`);
    if (!response.ok) throw new ApiError(response);
    return response.json();
  },

  async getById(id: string): Promise<User> {
    const response = await fetch(`${API_BASE}/users/${id}`);
    if (!response.ok) throw new ApiError(response);
    return response.json();
  },

  async create(data: CreateUserDto): Promise<User> {
    const response = await fetch(`${API_BASE}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new ApiError(response);
    return response.json();
  },
};
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(component-development) | Component implementation |
| @skill(api-development) | API contract alignment |
