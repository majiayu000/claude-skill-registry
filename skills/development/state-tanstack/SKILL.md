---
name: state-tanstack
description: State management patterns using Tanstack Query for server state and Zustand for client state. This skill should be used when setting up data fetching, implementing mutations, managing UI state, or organizing stores in React applications.
---

# State Management Skill

Patterns for managing state in React applications using Tanstack Query (server state) and Zustand (client/UI state).

## When to Use This Skill

- Setting up data fetching in a new project
- Implementing mutations with optimistic updates
- Managing UI state (modals, filters, preferences)
- Organizing Zustand stores
- Integrating Tanstack Query with Zustand

## Core Principle: Separation of Concerns

| Library | Purpose | Examples |
|---------|---------|----------|
| **Tanstack Query** | Server state | API data, cached responses, background refetching |
| **Zustand** | Client state | UI state, drafts, local preferences, temporary data |

**Golden Rule**: Don't duplicate server data in Zustand. Let Query be the source of truth for anything from the server.

## Setup

### Installation

```bash
npm install @tanstack/react-query zustand
```

### Query Provider

Create `src/providers/query-provider.tsx`:

```typescript
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            gcTime: 5 * 60 * 1000, // 5 minutes
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

Add to `src/app/layout.tsx`:

```typescript
import { QueryProvider } from '@/providers/query-provider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
```

## Tanstack Query Patterns

### Query Keys Convention

Use consistent, hierarchical keys:

```typescript
// Key factory pattern
export const queryKeys = {
  all: ['projects'] as const,
  lists: () => [...queryKeys.all, 'list'] as const,
  list: (filters: ProjectFilters) => [...queryKeys.lists(), filters] as const,
  details: () => [...queryKeys.all, 'detail'] as const,
  detail: (id: string) => [...queryKeys.details(), id] as const,
};
```

### Basic Query Hook

Create `src/hooks/use-projects.ts`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';

interface Project {
  id: string;
  name: string;
  status: 'active' | 'archived';
}

// Fetch all projects
export function useProjects(filters?: ProjectFilters) {
  return useQuery({
    queryKey: queryKeys.list(filters ?? {}),
    queryFn: async () => {
      const params = new URLSearchParams(filters as Record<string, string>);
      const res = await fetch(`/api/projects?${params}`);
      if (!res.ok) throw new Error('Failed to fetch projects');
      return res.json() as Promise<Project[]>;
    },
  });
}

// Fetch single project
export function useProject(id: string) {
  return useQuery({
    queryKey: queryKeys.detail(id),
    queryFn: async () => {
      const res = await fetch(`/api/projects/${id}`);
      if (!res.ok) throw new Error('Failed to fetch project');
      return res.json() as Promise<Project>;
    },
    enabled: !!id, // Don't fetch if no ID
  });
}
```

### Mutations

```typescript
export function useCreateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateProjectInput) => {
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Failed to create project');
      return res.json() as Promise<Project>;
    },
    onSuccess: () => {
      // Invalidate list queries to refetch
      queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
    },
  });
}

export function useUpdateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, ...data }: UpdateProjectInput) => {
      const res = await fetch(`/api/projects/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Failed to update project');
      return res.json() as Promise<Project>;
    },
    onSuccess: (data) => {
      // Update specific project in cache
      queryClient.setQueryData(queryKeys.detail(data.id), data);
      // Invalidate lists
      queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
    },
  });
}

export function useDeleteProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`/api/projects/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete project');
    },
    onSuccess: (_, id) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: queryKeys.detail(id) });
      // Invalidate lists
      queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
    },
  });
}
```

### Optimistic Updates

```typescript
export function useToggleProjectStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, status }: { id: string; status: 'active' | 'archived' }) => {
      const res = await fetch(`/api/projects/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) throw new Error('Failed to update status');
      return res.json() as Promise<Project>;
    },
    
    // Optimistic update
    onMutate: async ({ id, status }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.detail(id) });

      // Snapshot previous value
      const previousProject = queryClient.getQueryData<Project>(queryKeys.detail(id));

      // Optimistically update
      if (previousProject) {
        queryClient.setQueryData(queryKeys.detail(id), {
          ...previousProject,
          status,
        });
      }

      return { previousProject };
    },
    
    // Rollback on error
    onError: (err, { id }, context) => {
      if (context?.previousProject) {
        queryClient.setQueryData(queryKeys.detail(id), context.previousProject);
      }
    },
    
    // Refetch after success or error
    onSettled: (_, __, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.detail(id) });
    },
  });
}
```

## Zustand Patterns

### Store Structure

Create `src/stores/ui-store.ts`:

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  
  // Modal
  activeModal: string | null;
  modalData: unknown;
  openModal: (modal: string, data?: unknown) => void;
  closeModal: () => void;
}

export const useUIStore = create<UIState>()((set) => ({
  // Sidebar
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  
  // Modal
  activeModal: null,
  modalData: null,
  openModal: (modal, data) => set({ activeModal: modal, modalData: data }),
  closeModal: () => set({ activeModal: null, modalData: null }),
}));
```

### Persisted Store (Preferences)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface PreferencesState {
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  
  density: 'compact' | 'normal' | 'comfortable';
  setDensity: (density: 'compact' | 'normal' | 'comfortable') => void;
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'system',
      setTheme: (theme) => set({ theme }),
      
      density: 'normal',
      setDensity: (density) => set({ density }),
    }),
    {
      name: 'preferences',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
```

### Draft/Edit State Pattern

For editing forms without polluting server state:

```typescript
interface ProjectDraftState {
  // Only store the changed fields
  draftFields: Partial<Project>;
  
  // Actions
  setField: <K extends keyof Project>(key: K, value: Project[K]) => void;
  clearDraft: () => void;
  hasDraft: () => boolean;
}

export const useProjectDraftStore = create<ProjectDraftState>()((set, get) => ({
  draftFields: {},
  
  setField: (key, value) =>
    set((state) => ({
      draftFields: { ...state.draftFields, [key]: value },
    })),
    
  clearDraft: () => set({ draftFields: {} }),
  
  hasDraft: () => Object.keys(get().draftFields).length > 0,
}));
```

Usage with Query:

```typescript
function ProjectEditor({ projectId }: { projectId: string }) {
  const { data: project, isLoading } = useProject(projectId);
  const draftFields = useProjectDraftStore((s) => s.draftFields);
  const setField = useProjectDraftStore((s) => s.setField);
  const clearDraft = useProjectDraftStore((s) => s.clearDraft);
  const updateProject = useUpdateProject();
  
  if (isLoading || !project) return <Skeleton />;
  
  // Merge server state with draft
  const merged = { ...project, ...draftFields };
  
  const handleSave = async () => {
    await updateProject.mutateAsync({
      id: projectId,
      ...draftFields,
    });
    clearDraft();
  };
  
  return (
    <form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
      <input
        value={merged.name}
        onChange={(e) => setField('name', e.target.value)}
      />
      <button type="submit" disabled={updateProject.isPending}>
        Save
      </button>
    </form>
  );
}
```

### Selector Pattern (Prevent Re-renders)

```typescript
// Bad - subscribes to entire store
const { sidebarOpen, toggleSidebar } = useUIStore();

// Good - subscribes only to what you need
const sidebarOpen = useUIStore((s) => s.sidebarOpen);
const toggleSidebar = useUIStore((s) => s.toggleSidebar);

// Or use shallow comparison for objects
import { shallow } from 'zustand/shallow';

const { theme, density } = usePreferencesStore(
  (s) => ({ theme: s.theme, density: s.density }),
  shallow
);
```

### Sliced Stores

For larger apps, split stores by domain:

```
src/stores/
├── ui-store.ts        # UI state (modals, sidebar)
├── preferences.ts     # User preferences (persisted)
├── project-draft.ts   # Project editing draft
└── index.ts           # Re-exports
```

## Integration Patterns

### Filter State in URL + Zustand

```typescript
'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import { useCallback } from 'react';

// Use URL for shareable filter state
export function useFilters() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const filters = {
    status: searchParams.get('status') || 'all',
    search: searchParams.get('search') || '',
  };
  
  const setFilter = useCallback((key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    router.push(`?${params.toString()}`);
  }, [searchParams, router]);
  
  return { filters, setFilter };
}
```

Then pass to Query:

```typescript
function ProjectList() {
  const { filters } = useFilters();
  const { data: projects, isLoading } = useProjects(filters);
  
  // ...
}
```

### Loading States

```typescript
function ProjectCard({ projectId }: { projectId: string }) {
  const { data: project, isLoading, isError, error } = useProject(projectId);
  
  if (isLoading) {
    return <ProjectCardSkeleton />;
  }
  
  if (isError) {
    return <ErrorCard message={error.message} />;
  }
  
  return (
    <Card>
      <h3>{project.name}</h3>
      {/* ... */}
    </Card>
  );
}
```

## Best Practices

### Do

- Keep server data in Tanstack Query only
- Use Zustand for UI state and drafts
- Use selectors to prevent re-renders
- Invalidate queries after mutations
- Use query key factories for consistency

### Don't

- Don't store fetched API data in Zustand
- Don't create one giant store
- Don't destructure entire store (use selectors)
- Don't skip invalidation after mutations
- Don't use strings for query keys

## Directory Structure

```
src/
├── hooks/
│   ├── use-projects.ts      # Query hooks for projects
│   ├── use-users.ts         # Query hooks for users
│   └── use-filters.ts       # Filter state hooks
├── stores/
│   ├── ui-store.ts          # UI state
│   ├── preferences.ts       # Persisted preferences
│   └── index.ts             # Re-exports
├── lib/
│   └── query-keys.ts        # Query key factories
└── providers/
    └── query-provider.tsx   # Query client provider
```
