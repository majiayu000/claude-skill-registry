---
name: component-development
description: Patterns and best practices for developing React 19 components with Shadcn UI, Radix primitives, and Tailwind CSS 4 in Next.js 16. Covers accessibility, composition, variants, and server/client component patterns. Use when creating, modifying, or debugging UI components.
---

# Component Development Skill

Comprehensive guide for building accessible, composable React 19 components using Shadcn UI, Radix primitives, and Tailwind CSS 4 in The Simpsons API project.

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Create a component"
- "Build a UI element"
- "Add Shadcn component"
- "Make this accessible"
- "Add dark mode support"
- "Create reusable component"

✅ **Secondary Use Cases**

- "Fix component styling"
- "Add component variants"
- "Make responsive component"
- "Compose components together"
- "Debug rendering issues"
- "Add animations/transitions"

❌ **Do NOT use when**

- Server-only data fetching (use repositories)
- Server actions (use server-actions-patterns skill)
- Global styles (use globals.css directly)
- Configuration changes (use project docs)

## Project Context

### Component Structure

```
app/_components/           # App-specific components
├── CharacterImage.tsx
├── CommentSection.tsx
├── CreateCollectionForm.tsx
├── DeleteDiaryEntryButton.tsx
├── DiaryForm.tsx
├── EpisodeTracker.tsx
├── FollowButton.tsx
├── IntroSection.tsx
├── RecentlyViewedList.tsx
├── RecentlyViewedTracker.tsx
├── SimpsonsHeader.tsx
├── SyncButton.tsx
└── TriviaSection.tsx

components/ui/             # Shadcn UI primitives
├── avatar.tsx
├── badge.tsx
├── button.tsx
├── card.tsx
├── input.tsx
├── label.tsx
├── select.tsx
└── textarea.tsx
```

### Tech Stack

- **React**: 19 (with use client, useOptimistic, useActionState)
- **Styling**: Tailwind CSS 4 (`@import "tailwindcss"` syntax)
- **UI Library**: Shadcn UI (installed via `pnpm dlx shadcn@latest add`)
- **Primitives**: Radix UI (via Shadcn)
- **Icons**: Lucide React (recommended)

---

## Core Patterns

### Pattern 1: Server Component (Default)

```tsx
// app/_components/CharacterCard.tsx
// No "use client" = Server Component by default

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { DBCharacter } from "@/app/_lib/db-types";

interface CharacterCardProps {
  character: DBCharacter;
}

export function CharacterCard({ character }: CharacterCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {character.name}
          {character.is_main && (
            <Badge variant="secondary">Main</Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{character.occupation}</p>
        {character.catchphrase && (
          <p className="mt-2 italic">"{character.catchphrase}"</p>
        )}
      </CardContent>
    </Card>
  );
}
```

### Pattern 2: Client Component with Interactivity

```tsx
// app/_components/FollowButton.tsx
"use client";

import { useState, useTransition } from "react";
import { Button } from "@/components/ui/button";
import { Heart, HeartOff, Loader2 } from "lucide-react";
import { toggleFollow } from "@/app/_actions/social";

interface FollowButtonProps {
  characterId: number;
  initialFollowing: boolean;
  className?: string;
}

export function FollowButton({
  characterId,
  initialFollowing,
  className,
}: FollowButtonProps) {
  const [isFollowing, setIsFollowing] = useState(initialFollowing);
  const [isPending, startTransition] = useTransition();

  async function handleClick() {
    startTransition(async () => {
      // Optimistic update
      setIsFollowing(!isFollowing);

      const result = await toggleFollow(characterId);

      if (!result.success) {
        // Revert on error
        setIsFollowing(isFollowing);
        console.error(result.error);
      }
    });
  }

  return (
    <Button
      variant={isFollowing ? "destructive" : "default"}
      size="sm"
      onClick={handleClick}
      disabled={isPending}
      className={className}
      aria-label={isFollowing ? "Unfollow character" : "Follow character"}
    >
      {isPending ? (
        <Loader2 className="h-4 w-4 animate-spin" />
      ) : isFollowing ? (
        <>
          <HeartOff className="h-4 w-4 mr-2" />
          Unfollow
        </>
      ) : (
        <>
          <Heart className="h-4 w-4 mr-2" />
          Follow
        </>
      )}
    </Button>
  );
}
```

### Pattern 3: Component with Variants (CVA)

```tsx
// components/ui/status-badge.tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const statusBadgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors",
  {
    variants: {
      status: {
        success: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
        warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
        error: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
        info: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
        neutral: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100",
      },
      size: {
        sm: "text-xs px-2 py-0.5",
        md: "text-sm px-2.5 py-0.5",
        lg: "text-base px-3 py-1",
      },
    },
    defaultVariants: {
      status: "neutral",
      size: "md",
    },
  }
);

interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadgeVariants> {
  children: React.ReactNode;
}

export function StatusBadge({
  status,
  size,
  className,
  children,
  ...props
}: StatusBadgeProps) {
  return (
    <span
      className={cn(statusBadgeVariants({ status, size }), className)}
      {...props}
    >
      {children}
    </span>
  );
}

// Usage:
// <StatusBadge status="success">Active</StatusBadge>
// <StatusBadge status="error" size="lg">Failed</StatusBadge>
```

### Pattern 4: Compound Component Pattern

```tsx
// components/ui/character-profile.tsx
"use client";

import { createContext, useContext } from "react";
import { cn } from "@/lib/utils";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

// Context for compound components
const CharacterProfileContext = createContext<{
  name: string;
  imageUrl?: string;
} | null>(null);

function useCharacterProfile() {
  const context = useContext(CharacterProfileContext);
  if (!context) {
    throw new Error("CharacterProfile components must be used within CharacterProfile");
  }
  return context;
}

// Root component
interface CharacterProfileProps {
  name: string;
  imageUrl?: string;
  children: React.ReactNode;
  className?: string;
}

function CharacterProfile({ name, imageUrl, children, className }: CharacterProfileProps) {
  return (
    <CharacterProfileContext.Provider value={{ name, imageUrl }}>
      <div className={cn("flex items-start gap-4", className)}>
        {children}
      </div>
    </CharacterProfileContext.Provider>
  );
}

// Sub-components
function ProfileAvatar({ className }: { className?: string }) {
  const { name, imageUrl } = useCharacterProfile();
  return (
    <Avatar className={cn("h-12 w-12", className)}>
      {imageUrl && <AvatarImage src={imageUrl} alt={name} />}
      <AvatarFallback>{name.slice(0, 2).toUpperCase()}</AvatarFallback>
    </Avatar>
  );
}

function ProfileName({ className }: { className?: string }) {
  const { name } = useCharacterProfile();
  return <h3 className={cn("font-semibold text-lg", className)}>{name}</h3>;
}

function ProfileContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("flex-1", className)}>{children}</div>;
}

// Attach sub-components
CharacterProfile.Avatar = ProfileAvatar;
CharacterProfile.Name = ProfileName;
CharacterProfile.Content = ProfileContent;

export { CharacterProfile };

// Usage:
// <CharacterProfile name="Homer Simpson" imageUrl="/homer.jpg">
//   <CharacterProfile.Avatar />
//   <CharacterProfile.Content>
//     <CharacterProfile.Name />
//     <p>Safety Inspector at Springfield Nuclear Power Plant</p>
//   </CharacterProfile.Content>
// </CharacterProfile>
```

### Pattern 5: Polymorphic Component (as prop)

```tsx
// components/ui/box.tsx
import { cn } from "@/lib/utils";
import { type ElementType, type ComponentPropsWithoutRef } from "react";

type BoxProps<T extends ElementType = "div"> = {
  as?: T;
  className?: string;
  children?: React.ReactNode;
} & Omit<ComponentPropsWithoutRef<T>, "as" | "className" | "children">;

export function Box<T extends ElementType = "div">({
  as,
  className,
  children,
  ...props
}: BoxProps<T>) {
  const Component = as || "div";
  return (
    <Component className={cn(className)} {...props}>
      {children}
    </Component>
  );
}

// Usage:
// <Box>Default div</Box>
// <Box as="section" className="my-section">Section element</Box>
// <Box as="article">Article element</Box>
// <Box as="a" href="/link">Link element</Box>
```

---

## Shadcn UI Integration

### Installing New Components

```bash
# Add single component
pnpm dlx shadcn@latest add button

# Add multiple components
pnpm dlx shadcn@latest add card badge avatar

# List available components
pnpm dlx shadcn@latest add
```

### Customizing Shadcn Components

```tsx
// Extend the button with Simpsons theme
// components/ui/simpsons-button.tsx
import { Button, type ButtonProps } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface SimpsonsButtonProps extends ButtonProps {
  character?: "homer" | "bart" | "lisa" | "marge";
}

const characterColors = {
  homer: "bg-amber-500 hover:bg-amber-600 text-white",
  bart: "bg-orange-500 hover:bg-orange-600 text-white",
  lisa: "bg-red-500 hover:bg-red-600 text-white",
  marge: "bg-blue-500 hover:bg-blue-600 text-white",
};

export function SimpsonsButton({
  character,
  className,
  variant,
  ...props
}: SimpsonsButtonProps) {
  return (
    <Button
      className={cn(
        character && characterColors[character],
        className
      )}
      variant={character ? undefined : variant}
      {...props}
    />
  );
}
```

### Using Radix Primitives Directly

```tsx
// When you need more control than Shadcn provides
import * as Dialog from "@radix-ui/react-dialog";
import { cn } from "@/lib/utils";

export function CustomDialog({
  trigger,
  title,
  children,
}: {
  trigger: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-background rounded-lg p-6 shadow-lg w-full max-w-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          <Dialog.Title className="text-lg font-semibold">{title}</Dialog.Title>
          {children}
          <Dialog.Close className="absolute top-4 right-4">
            <span className="sr-only">Close</span>
            ✕
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

## Accessibility Patterns

### Keyboard Navigation

```tsx
// Ensure all interactive elements are keyboard accessible
"use client";

import { useRef, KeyboardEvent } from "react";

export function KeyboardNavigableList({ items }: { items: string[] }) {
  const listRef = useRef<HTMLUListElement>(null);

  function handleKeyDown(e: KeyboardEvent, index: number) {
    const list = listRef.current;
    if (!list) return;

    const items = list.querySelectorAll('[role="listitem"]');
    let nextIndex = index;

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        nextIndex = (index + 1) % items.length;
        break;
      case "ArrowUp":
        e.preventDefault();
        nextIndex = (index - 1 + items.length) % items.length;
        break;
      case "Home":
        e.preventDefault();
        nextIndex = 0;
        break;
      case "End":
        e.preventDefault();
        nextIndex = items.length - 1;
        break;
      default:
        return;
    }

    (items[nextIndex] as HTMLElement).focus();
  }

  return (
    <ul ref={listRef} role="list" className="space-y-2">
      {items.map((item, index) => (
        <li
          key={item}
          role="listitem"
          tabIndex={0}
          className="p-2 rounded hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring"
          onKeyDown={(e) => handleKeyDown(e, index)}
        >
          {item}
        </li>
      ))}
    </ul>
  );
}
```

### ARIA Labels and Live Regions

```tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export function AccessibleCounter() {
  const [count, setCount] = useState(0);

  return (
    <div className="flex items-center gap-4">
      <Button
        onClick={() => setCount((c) => c - 1)}
        aria-label="Decrease count"
      >
        -
      </Button>

      {/* Live region announces changes to screen readers */}
      <span
        aria-live="polite"
        aria-atomic="true"
        className="text-2xl font-bold min-w-[3ch] text-center"
      >
        {count}
      </span>

      <Button
        onClick={() => setCount((c) => c + 1)}
        aria-label="Increase count"
      >
        +
      </Button>
    </div>
  );
}
```

### Focus Management

```tsx
"use client";

import { useEffect, useRef } from "react";

export function AutoFocusInput({ shouldFocus }: { shouldFocus: boolean }) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (shouldFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [shouldFocus]);

  return (
    <input
      ref={inputRef}
      type="text"
      className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
      aria-describedby="input-help"
    />
  );
}
```

---

## Dark Mode Support

### Using CSS Variables (Tailwind CSS 4)

```tsx
// Component automatically adapts to dark mode via CSS variables
export function ThemedCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-background text-foreground border border-border rounded-lg p-4 shadow-sm">
      {children}
    </div>
  );
}

// bg-background = var(--background) 
// text-foreground = var(--foreground)
// These switch automatically with .dark class on html
```

### Manual Dark Mode Variants

```tsx
export function DarkModeExample() {
  return (
    <div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-lg p-6 transition-colors">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white">
        Title
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mt-2">
        This adapts to dark mode automatically.
      </p>
      <div className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
        Divider also adapts
      </div>
    </div>
  );
}
```

---

## Animation Patterns

### Tailwind Animations

```tsx
// Entrance animation
<div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
  Content appears with animation
</div>

// Exit animation
<div className="animate-out fade-out slide-out-to-top-4 duration-300">
  Content exits with animation
</div>

// Spin animation
<Loader2 className="h-4 w-4 animate-spin" />

// Pulse animation
<div className="animate-pulse bg-gray-200 rounded h-4 w-full" />

// Bounce animation
<span className="animate-bounce inline-block">👋</span>
```

### CSS Transitions

```tsx
export function HoverCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="group relative p-4 rounded-lg border transition-all duration-200 hover:shadow-lg hover:border-primary hover:-translate-y-1">
      {children}
      {/* Hidden content that appears on hover */}
      <div className="absolute inset-x-0 -bottom-2 opacity-0 group-hover:opacity-100 group-hover:bottom-0 transition-all duration-200">
        <span className="text-xs text-muted-foreground">Click for more</span>
      </div>
    </div>
  );
}
```

### Framer Motion Integration

```tsx
"use client";

import { motion, AnimatePresence } from "framer-motion";

export function AnimatedList({ items }: { items: string[] }) {
  return (
    <ul className="space-y-2">
      <AnimatePresence>
        {items.map((item, index) => (
          <motion.li
            key={item}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ delay: index * 0.1 }}
            className="p-3 bg-card rounded border"
          >
            {item}
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
}
```

---

## Responsive Design

### Mobile-First Approach

```tsx
export function ResponsiveGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {children}
    </div>
  );
}
```

### Container Queries (Tailwind CSS 4)

```tsx
export function ContainerQueryCard() {
  return (
    <div className="@container">
      <div className="flex flex-col @md:flex-row gap-4 p-4">
        <img
          src="/image.jpg"
          alt=""
          className="w-full @md:w-1/3 rounded"
        />
        <div className="@md:flex-1">
          <h2 className="text-lg @lg:text-xl font-bold">Title</h2>
          <p className="text-sm @lg:text-base">Content adapts to container</p>
        </div>
      </div>
    </div>
  );
}
```

### Breakpoint Reference

| Prefix | Min Width | Typical Use |
|--------|-----------|-------------|
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

---

## Common Mistakes

### ❌ Wrong: Using hooks in Server Component

```tsx
// This will error
import { useState } from "react";

export function ServerComponent() {
  const [state, setState] = useState(false); // ERROR
  return <div>{state}</div>;
}
```

### ✅ Correct: Add "use client" or move to client component

```tsx
"use client";

import { useState } from "react";

export function ClientComponent() {
  const [state, setState] = useState(false);
  return <div>{state}</div>;
}
```

### ❌ Wrong: Passing functions to client components

```tsx
// page.tsx (Server Component)
export default function Page() {
  function handleClick() { // Server function
    console.log("clicked");
  }
  return <ClientButton onClick={handleClick} />; // ERROR
}
```

### ✅ Correct: Use server actions or client-side handlers

```tsx
// Option 1: Server Action
"use server";
export async function handleClick() {
  console.log("clicked on server");
}

// Option 2: Define handler in client component
"use client";
export function ClientButton() {
  function handleClick() {
    console.log("clicked on client");
  }
  return <button onClick={handleClick}>Click</button>;
}
```

---

## Related Skills

- [server-actions-patterns](../server-actions-patterns/SKILL.md) - Form handling with actions
- [webapp-testing](../webapp-testing/SKILL.md) - Testing components
- [performance-optimization](../performance-optimization/SKILL.md) - Component performance

---

## References

- [Shadcn UI Documentation](https://ui.shadcn.com/)
- [Radix UI Primitives](https://www.radix-ui.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React 19 Documentation](https://react.dev/)
- [Next.js App Router](https://nextjs.org/docs/app)

---

**Last Updated:** January 14, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready
