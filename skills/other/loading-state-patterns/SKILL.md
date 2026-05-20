---
name: loading-state-patterns
model: fast
description: Patterns for skeleton loaders, shimmer effects, and loading states that match design system aesthetics. Covers skeleton components, shimmer animations, and progressive loading. Use when building polished loading experiences. Triggers on skeleton, loading state, shimmer, placeholder, loading animation.
---

# Loading State Patterns

Build loading states that feel intentional and match your design system aesthetic.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install loading-state-patterns
```


---

## When to Use

- Building skeleton loaders for content areas
- Need shimmer effects for streaming content
- Want progressive loading experiences
- Building premium loading UX

---

## Pattern 1: Skeleton Base

```tsx
import { cn } from '@/lib/utils';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  shimmer?: boolean;
}

export function Skeleton({ className, shimmer = true, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-muted',
        shimmer && 'animate-shimmer bg-gradient-to-r from-muted via-muted-foreground/10 to-muted bg-[length:200%_100%]',
        className
      )}
      {...props}
    />
  );
}
```

### CSS Animation

```css
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.animate-shimmer {
  animation: shimmer 1.5s ease-in-out infinite;
}
```

---

## Pattern 2: Content Skeleton Layouts

### Card Skeleton

```tsx
export function CardSkeleton() {
  return (
    <div className="rounded-lg border bg-card p-4 space-y-3">
      <div className="flex items-center gap-3">
        <Skeleton className="size-10 rounded-full" />
        <div className="space-y-1.5 flex-1">
          <Skeleton className="h-4 w-1/3" />
          <Skeleton className="h-3 w-1/4" />
        </div>
      </div>
      <Skeleton className="h-20 w-full" />
      <div className="flex gap-2">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  );
}
```

### Table Row Skeleton

```tsx
export function TableRowSkeleton({ columns = 4 }: { columns?: number }) {
  return (
    <tr>
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="p-3">
          <Skeleton className="h-4 w-full" />
        </td>
      ))}
    </tr>
  );
}
```

### Metric Skeleton

```tsx
export function MetricSkeleton() {
  return (
    <div className="space-y-2">
      <Skeleton className="h-3 w-16" />
      <Skeleton className="h-8 w-24" />
    </div>
  );
}
```

---

## Pattern 3: Design System Skeleton

Match skeleton to your aesthetic:

```tsx
// For retro-futuristic theme
export function CyberSkeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-tone-cadet/30',
        'animate-pulse-glow',
        'border border-tone-cyan/10',
        className
      )}
      {...props}
    />
  );
}

// CSS
@keyframes pulse-glow {
  0%, 100% { opacity: 0.4; box-shadow: 0 0 0 0 rgba(var(--tone-cyan), 0); }
  50% { opacity: 0.6; box-shadow: 0 0 8px 0 rgba(var(--tone-cyan), 0.1); }
}
```

---

## Pattern 4: Progressive Loading

Show content as it loads:

```tsx
interface ProgressiveLoadProps {
  isLoading: boolean;
  skeleton: React.ReactNode;
  children: React.ReactNode;
}

export function ProgressiveLoad({
  isLoading,
  skeleton,
  children,
}: ProgressiveLoadProps) {
  return (
    <div className="relative">
      {isLoading ? (
        skeleton
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          {children}
        </motion.div>
      )}
    </div>
  );
}
```

---

## Pattern 5: Streaming Content Indicator

For AI/LLM content that streams:

```tsx
export function StreamingIndicator() {
  return (
    <div className="flex items-center gap-1">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="size-1.5 rounded-full bg-primary"
          animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            delay: i * 0.15,
          }}
        />
      ))}
    </div>
  );
}
```

---

## Pattern 6: Loading Progress Bar

```tsx
interface LoadingProgressProps {
  progress?: number; // 0-100, undefined = indeterminate
}

export function LoadingProgress({ progress }: LoadingProgressProps) {
  const isIndeterminate = progress === undefined;

  return (
    <div className="h-1 w-full bg-muted overflow-hidden rounded-full">
      <div
        className={cn(
          'h-full bg-primary transition-all duration-300',
          isIndeterminate && 'animate-indeterminate'
        )}
        style={!isIndeterminate ? { width: `${progress}%` } : undefined}
      />
    </div>
  );
}

// CSS
@keyframes indeterminate {
  0% { transform: translateX(-100%); width: 50%; }
  100% { transform: translateX(200%); width: 50%; }
}

.animate-indeterminate {
  animation: indeterminate 1.5s ease-in-out infinite;
}
```

---

## Pattern 7: Skeleton Grid

```tsx
export function GridSkeleton({ 
  count = 6, 
  columns = 3 
}: { 
  count?: number; 
  columns?: number;
}) {
  return (
    <div 
      className="grid gap-4" 
      style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
    >
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — Complete design system workflow
- [distinctive-design-systems](../distinctive-design-systems/) — Aesthetic matching for themed skeletons
---

## NEVER Do

- **Use gray skeletons on dark themes** — Match your surface colors
- **Skip shimmer animation** — Static blocks look broken
- **Make skeletons exact size** — Slight size variation is natural
- **Forget aspect ratios** — Images need consistent skeleton ratios
- **Show skeleton forever** — Add timeout fallbacks for errors

---

## Quick Reference

```tsx
// Basic skeleton
<Skeleton className="h-4 w-full" />

// Avatar skeleton
<Skeleton className="size-10 rounded-full" />

// Text lines
<div className="space-y-2">
  <Skeleton className="h-4 w-3/4" />
  <Skeleton className="h-4 w-1/2" />
</div>

// Card skeleton
<div className="p-4 space-y-3">
  <Skeleton className="h-6 w-1/3" />
  <Skeleton className="h-20 w-full" />
</div>
```
