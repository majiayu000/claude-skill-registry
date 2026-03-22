---
name: component-patterns
description: >
  React component composition patterns including compound components, render props, HOCs,
  and controlled vs uncontrolled components. Use when the user is building React components,
  asking about component architecture, refactoring components, or designing reusable UI APIs.
  Trigger on mentions of compound components, render props, higher-order components, forwardRef,
  composition, or component design patterns.
---

# React Component Patterns

Advanced React component composition patterns for building flexible, reusable UI APIs.

## When to Use
- User is designing a reusable component API
- User asks about compound components, render props, or HOCs
- User needs to choose between controlled and uncontrolled components
- User is refactoring components for better composition
- User mentions forwardRef or ref forwarding

## Core Patterns

### Compound Components

Share implicit state between related components using React context. This gives consumers a declarative API without prop drilling.

```tsx
import { createContext, useContext, useState, ReactNode } from 'react'

interface TabsContextType {
  activeTab: string
  setActiveTab: (id: string) => void
}

const TabsContext = createContext<TabsContextType | null>(null)

function useTabsContext() {
  const context = useContext(TabsContext)
  if (!context) {
    throw new Error('Tabs compound components must be used within <Tabs>')
  }
  return context
}

function Tabs({ defaultTab, children }: { defaultTab: string; children: ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab)
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  )
}

function TabTrigger({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext()
  return (
    <button role="tab" aria-selected={activeTab === id} onClick={() => setActiveTab(id)}>
      {children}
    </button>
  )
}

function TabContent({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab } = useTabsContext()
  if (activeTab !== id) return null
  return <div role="tabpanel">{children}</div>
}

Tabs.Trigger = TabTrigger
Tabs.Content = TabContent
export { Tabs }
```

Usage:
```tsx
<Tabs defaultTab="settings">
  <Tabs.Trigger id="profile">Profile</Tabs.Trigger>
  <Tabs.Trigger id="settings">Settings</Tabs.Trigger>
  <Tabs.Content id="profile"><ProfileForm /></Tabs.Content>
  <Tabs.Content id="settings"><SettingsForm /></Tabs.Content>
</Tabs>
```

### Render Props

Delegate rendering to consumers while encapsulating behavior logic.

```tsx
interface MouseTrackerProps {
  children: (position: { x: number; y: number }) => ReactNode
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  const handleMouseMove = (e: React.MouseEvent) => {
    setPosition({ x: e.clientX, y: e.clientY })
  }

  return <div onMouseMove={handleMouseMove}>{children(position)}</div>
}

// Usage
<MouseTracker>
  {({ x, y }) => <Tooltip style={{ left: x, top: y }}>Cursor here</Tooltip>}
</MouseTracker>
```

### Higher-Order Components (HOC)

Wrap components to inject cross-cutting concerns. Prefer hooks for new code, but HOCs remain useful for class components and third-party integrations.

```tsx
function withAuth<P extends object>(WrappedComponent: React.ComponentType<P>) {
  const displayName = WrappedComponent.displayName || WrappedComponent.name || 'Component'

  function WithAuth(props: P) {
    const { user, isLoading } = useAuth()

    if (isLoading) return <Spinner />
    if (!user) return <Navigate to="/login" />

    return <WrappedComponent {...props} />
  }

  WithAuth.displayName = `withAuth(${displayName})`
  return WithAuth
}

const ProtectedDashboard = withAuth(Dashboard)
```

### Controlled vs Uncontrolled Components

Controlled: parent owns state. Uncontrolled: component owns state internally. Support both with a flexible API.

```tsx
interface InputProps {
  value?: string
  defaultValue?: string
  onChange?: (value: string) => void
}

function Input({ value: controlledValue, defaultValue = '', onChange }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue)
  const isControlled = controlledValue !== undefined
  const currentValue = isControlled ? controlledValue : internalValue

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value
    if (!isControlled) {
      setInternalValue(next)
    }
    onChange?.(next)
  }

  return <input value={currentValue} onChange={handleChange} />
}
```

### forwardRef with useImperativeHandle

Expose a limited imperative API to parent components via refs.

```tsx
import { forwardRef, useImperativeHandle, useRef } from 'react'

interface VideoPlayerHandle {
  play: () => void
  pause: () => void
  seek: (time: number) => void
}

const VideoPlayer = forwardRef<VideoPlayerHandle, { src: string }>(({ src }, ref) => {
  const videoRef = useRef<HTMLVideoElement>(null)

  useImperativeHandle(ref, () => ({
    play: () => videoRef.current?.play(),
    pause: () => videoRef.current?.pause(),
    seek: (time: number) => {
      if (videoRef.current) videoRef.current.currentTime = time
    },
  }))

  return <video ref={videoRef} src={src} />
})

VideoPlayer.displayName = 'VideoPlayer'
```

## Anti-Patterns

- **Prop drilling through 5+ levels** -- Use compound components or context instead of passing props through intermediate components that do not use them.
- **God components** -- A single component handling layout, data fetching, and business logic. Split into container/presentational or use hooks.
- **Overusing HOCs** -- Stacking multiple HOCs creates wrapper hell and makes debugging difficult. Prefer hooks for new code.
- **Mixing controlled and uncontrolled** without a clear API boundary -- Pick one default and document it. If supporting both, use the pattern above.

## Quick Reference

| Pattern | Use When | Complexity |
|---------|----------|------------|
| Compound Components | Declarative multi-part UI (tabs, accordion, menu) | Medium |
| Render Props | Consumer needs full control over rendering | Low |
| HOC | Cross-cutting concerns on class components | Medium |
| Controlled/Uncontrolled | Form inputs, toggles, any stateful element | Low |
| forwardRef | Parent needs imperative access to child DOM/API | Low |

Prefer composition over inheritance. Prefer hooks over HOCs for new code. Prefer compound components for multi-element UI widgets.
