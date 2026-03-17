---
name: nextjs-frontend-skill
description: Build Next.js App Router pages, components with TypeScript and Tailwind
when-to-use: Creating new pages, UI components, responsive design
---
# Next.js Frontend Skill

## Instructions

This skill provides guidance for building the Next.js frontend with App Router, TypeScript, and Tailwind CSS.

### Project Structure
```
src/
├── app/
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Home page (dashboard)
│   ├── globals.css         # Global styles
│   ├── tasks/
│   │   ├── page.tsx        # Tasks list page
│   │   ├── [id]/           # Task detail dynamic route
│   │   │   └── page.tsx
│   │   └── new/
│   │       └── page.tsx    # New task page
│   └── auth/
│       ├── login/
│       │   └── page.tsx
│       └── register/
│           └── page.tsx
├── components/
│   ├── ui/                 # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── Badge.tsx
│   ├── tasks/              # Task-specific components
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskCard.tsx
│   └── chat/               # Chat components
│       ├── ChatWindow.tsx
│       ├── ChatMessage.tsx
│       └── ChatInput.tsx
├── lib/
│   ├── api.ts              # API client functions
│   ├── auth.ts             # Auth utilities
│   └── utils.ts            # Helper functions
├── hooks/
│   ├── useTasks.ts         # Task data hooks
│   ├── useAuth.ts          # Auth state hooks
│   └── useChat.ts          # Chat hooks
└── types/
    └── index.ts            # TypeScript type definitions
```

### Creating a New Page

1. **Create Page Component** in `src/app/[route]/page.tsx`:
   ```tsx
   import { Metadata } from 'next'

   export const metadata: Metadata = {
     title: 'Tasks | Todo App',
     description: 'Manage your tasks efficiently',
   }

   export default function TasksPage() {
     return (
       <main className="container mx-auto py-8">
         <h1 className="text-3xl font-bold mb-6">My Tasks</h1>
         {/* Page content */}
       </main>
     )
   }
   ```

2. **Use Client Components for Interactivity**:
   ```tsx
   'use client'

   import { useState } from 'react'

   export default function TaskForm() {
     const [isLoading, setIsLoading] = useState(false)

     async function handleSubmit(e: React.FormEvent) {
       e.preventDefault()
       setIsLoading(true)
       // Submit logic
       setIsLoading(false)
     }

     return (
       <form onSubmit={handleSubmit} className="space-y-4">
         {/* Form fields */}
       </form>
     )
   }
   ```

### Creating Reusable Components

```tsx
// src/components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  isLoading,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-colors'

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="mr-2">Loading...</span>
      ) : null}
      {children}
    </button>
  )
}
```

### Using Tailwind CSS

```tsx
// Responsive design examples
export function ResponsiveCard() {
  return (
    <div className="
      grid
      grid-cols-1
      sm:grid-cols-2
      lg:grid-cols-3
      xl:grid-cols-4
      gap-4
      p-4
      bg-white
      rounded-xl
      shadow-sm
      hover:shadow-md
      transition-shadow
    ">
      {/* Card content */}
    </div>
  )
}

// Dark mode support
export function ThemedComponent() {
  return (
    <div className="
      bg-white
      dark:bg-gray-900
      text-gray-900
      dark:text-gray-100
      border
      border-gray-200
      dark:border-gray-800
    ">
      {/* Content */}
    </div>
  )
}
```

### API Client Integration

```tsx
// src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  created_at: string
}

export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch(`${API_BASE}/api/v1/tasks`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    cache: 'no-store',
  })
  if (!res.ok) throw new Error('Failed to fetch tasks')
  return res.json()
}

export async function createTask(data: Partial<Task>): Promise<Task> {
  const res = await fetch(`${API_BASE}/api/v1/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to create task')
  return res.json()
}
```

### Using Hooks

```tsx
// src/hooks/useTasks.ts
'use client'

import { useState, useEffect, useCallback } from 'react'
import { fetchTasks, createTask as apiCreateTask } from '@/lib/api'

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadTasks = useCallback(async () => {
    try {
      setIsLoading(true)
 await fetchTasks()
      setTasks(data)
    } catch      const data = (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadTasks()
  }, [loadTasks])

  const addTask = async (task: Partial<Task>) => {
    const newTask = await apiCreateTask(task)
    setTasks(prev => [...prev, newTask])
  }

  return { tasks, isLoading, error, loadTasks, addTask }
}
```

## Examples

### Task List Component

```tsx
// src/components/tasks/TaskList.tsx
'use client'

import { TaskItem } from './TaskItem'
import { useTasks } from '@/hooks/useTasks'

export function TaskList() {
  const { tasks, isLoading, error } = useTasks()

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        Error loading tasks: {error}
      </div>
    )
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Create your first task!
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  )
}
```

### Task Item with Actions

```tsx
// src/components/tasks/TaskItem.tsx
'use client'

import { useState } from 'react'
import { Task } from '@/types'
import { Button } from '@/components/ui/Button'

interface TaskItemProps {
  task: Task
  onToggle?: (id: number) => void
  onDelete?: (id: number) => void
}

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    setIsDeleting(true)
    await onDelete?.(task.id)
    setIsDeleting(false)
  }

  return (
    <div className={`
      flex items-center gap-4 p-4 rounded-lg border
      ${task.completed ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-300'}
    `}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle?.(task.id)}
        className="h-5 w-5 rounded border-gray-300"
      />
      <div className="flex-1 min-w-0">
        <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-600 truncate">{task.description}</p>
        )}
      </div>
      <div className="flex items-center gap-2">
        <Button variant="secondary" size="sm">
          Edit
        </Button>
        <Button
          variant="danger"
          size="sm"
          isLoading={isDeleting}
          onClick={handleDelete}
        >
          Delete
        </Button>
      </div>
    </div>
  )
}
```

### Layout with Providers

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/components/providers/AuthProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo AI App',
  description: 'AI-powered task management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-gray-100">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}
```
