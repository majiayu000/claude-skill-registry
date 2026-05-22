---
name: bellog-hooks
description: Provides custom React hooks patterns and best practices specific to Bellog. Triggers when creating custom hooks or implementing interactive features.
---

# Bellog Hook Patterns

This skill defines the patterns and best practices for creating custom React hooks in the Bellog blog project.

## Hook Location

**All custom hooks:** `/src/hooks/`

**Naming convention:** `use[Feature].ts` (camelCase)

## Core Hook Patterns

Bellog uses three main patterns:

1. **Scroll-based hooks** - Track scroll position and direction
2. **Observer-based hooks** - Use IntersectionObserver for viewport detection
3. **Content processing hooks** - Parse and transform data

## Pattern 1: Scroll-Based Hooks

**Example:** `useScrollSpy.ts`

### Structure

```typescript
import { useState, useEffect, useRef, useCallback } from 'react';

export function useScrollSpy() {
  // 1. State with useRef for position tracking
  const [activeId, setActiveId] = useState<string>("");
  const positionsRef = useRef<Map<string, number>>(new Map());

  // 2. Handler with useCallback for optimization
  const handleScroll = useCallback(() => {
    const scrollPosition = window.scrollY + OFFSET;

    // Find active section logic
    let active = "";
    positionsRef.current.forEach((position, id) => {
      if (scrollPosition >= position) {
        active = id;
      }
    });

    setActiveId(active);
  }, []);

  // 3. Effect with cleanup
  useEffect(() => {
    // Passive listener for better performance
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Initial call
    handleScroll();

    // Cleanup
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [handleScroll]);

  return { activeId, setPositions: (positions) => {
    positionsRef.current = positions;
  }};
}
```

### Key Features

- **useRef for positions** - Avoids re-renders on position updates
- **useCallback** - Prevents handler recreation
- **Passive listener** - Better scroll performance
- **Cleanup** - Remove listeners to prevent memory leaks

### Constants Import

```typescript
import { HEADER_OFFSET, SCROLL_SPY_OFFSET } from '@/constants/ui';
```

Use these constants instead of magic numbers.

## Pattern 2: Observer-Based Hooks

**Example:** `useTocObserver.ts`

### Structure

```typescript
import { useEffect, useState, useRef } from 'react';

export function useTocObserver() {
  const [activeId, setActiveId] = useState<string>("");
  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    // 1. Create observer
    observerRef.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      {
        rootMargin: '-80px 0px -80% 0px', // Adjust for header
        threshold: 0
      }
    );

    // 2. Observe elements
    const headings = document.querySelectorAll('h2, h3');
    headings.forEach(heading => {
      observerRef.current?.observe(heading);
    });

    // 3. Cleanup: unobserve and disconnect
    return () => {
      headings.forEach(heading => {
        observerRef.current?.unobserve(heading);
      });
      observerRef.current?.disconnect();
    };
  }, []); // Dependencies

  return activeId;
}
```

### Key Features

- **IntersectionObserver** - Efficient viewport detection
- **useRef for observer** - Stable reference across renders
- **Proper cleanup** - unobserve + disconnect
- **rootMargin** - Account for fixed headers

## Pattern 3: Content Processing Hooks

**Example:** `useHeadings.ts`

### Structure

```typescript
import { useEffect, useState } from 'react';

interface Heading {
  id: string;
  text: string;
  level: number;
}

export function useHeadings() {
  const [headings, setHeadings] = useState<Heading[]>([]);

  useEffect(() => {
    // 1. Extract headings from DOM
    const elements = document.querySelectorAll('h2, h3');

    // 2. Process into structured data
    const processedHeadings = Array.from(elements).map(el => ({
      id: el.id,
      text: el.textContent || '',
      level: parseInt(el.tagName[1])
    }));

    // 3. Update state
    setHeadings(processedHeadings);

    // 4. Handle empty state
    if (processedHeadings.length === 0) {
      console.warn('No headings found');
    }
  }, []); // Re-run only on mount

  return headings;
}
```

### Key Features

- **DOM querying** - Extract content from rendered HTML
- **Data transformation** - Convert to usable structure
- **Empty state handling** - Graceful degradation
- **Type safety** - Explicit return type

## Custom Hook Template

Use this template for new hooks:

```typescript
import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Hook description: What it does and when to use it
 *
 * @example
 * const value = useCustomHook();
 */
export function useCustomHook() {
  // 1. State declarations
  const [state, setState] = useState<Type>(initialValue);

  // 2. Refs (for values that don't cause re-renders)
  const refValue = useRef<Type>(initialValue);

  // 3. Callbacks (for stable function references)
  const handleEvent = useCallback(() => {
    // Event handling logic
  }, [/* dependencies */]);

  // 4. Effects (side effects, subscriptions)
  useEffect(() => {
    // Setup
    // ...

    // Cleanup
    return () => {
      // Cleanup logic
    };
  }, [/* dependencies */]);

  // 5. Return value (keep API minimal)
  return state;
  // or
  return { state, setState, handleEvent };
}
```

## Hook Best Practices

### 1. Naming

```typescript
// ✅ Correct
useScrollSpy
useTocObserver
useScrollPosition
useMediaQuery

// ❌ Wrong
scrollSpy
ObserverHook
scrollPositionHook
```

### 2. Return Values

```typescript
// ✅ Single value when simple
return activeId;

// ✅ Object when multiple values
return { activeId, setActiveId, isScrolling };

// ❌ Too many values
return { value1, value2, value3, value4, value5 }; // Too complex
```

### 3. Dependencies

```typescript
// ✅ Correct dependencies
useEffect(() => {
  doSomething(value);
}, [value]); // value is used

// ❌ Missing dependencies
useEffect(() => {
  doSomething(value);
}, []); // value not in deps!

// ✅ ESLint exhaustive-deps will catch this
```

### 4. Cleanup

```typescript
// ✅ Always cleanup event listeners
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, [handleScroll]);

// ✅ Always cleanup observers
useEffect(() => {
  const observer = new IntersectionObserver(...);
  // observe elements
  return () => observer.disconnect();
}, []);

// ✅ Always cleanup timers
useEffect(() => {
  const timer = setTimeout(...);
  return () => clearTimeout(timer);
}, []);
```

### 5. Performance

```typescript
// ✅ Use passive listeners for scroll/touch
{ passive: true }

// ✅ Use useCallback for stable references
const handler = useCallback(() => {...}, [deps]);

// ✅ Use useRef to avoid re-renders
const ref = useRef(value);

// ✅ Debounce/throttle expensive operations
const debouncedHandler = useMemo(
  () => debounce(handler, 100),
  [handler]
);
```

## Common Hook Patterns

### Scroll Position Hook

```typescript
export function useScrollPosition() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Initial value

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollY;
}
```

### Scroll Direction Hook

```typescript
export function useScrollDirection() {
  const [scrollDirection, setScrollDirection] = useState<'up' | 'down'>('up');
  const lastScrollY = useRef(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      if (currentScrollY > lastScrollY.current) {
        setScrollDirection('down');
      } else if (currentScrollY < lastScrollY.current) {
        setScrollDirection('up');
      }

      lastScrollY.current = currentScrollY;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollDirection;
}
```

### Media Query Hook

```typescript
export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => {
      setMatches(e.matches);
    };

    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}

// Usage
const isMobile = useMediaQuery('(max-width: 768px)');
```

### Debounce Hook

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### Previous Value Hook

```typescript
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

## Integration with Components

### Usage Pattern

```typescript
"use client";

import { useScrollSpy } from '@/hooks/useScrollSpy';
import { HEADER_OFFSET } from '@/constants/ui';

export function TableOfContents({ headings }: Props) {
  // 1. Use the hook
  const { activeId, setPositions } = useScrollSpy();

  // 2. Update positions when headings change
  useEffect(() => {
    const positions = new Map();
    headings.forEach(heading => {
      const element = document.getElementById(heading.id);
      if (element) {
        positions.set(heading.id, element.offsetTop - HEADER_OFFSET);
      }
    });
    setPositions(positions);
  }, [headings, setPositions]);

  // 3. Use the returned value
  return (
    <nav>
      {headings.map(heading => (
        <a
          key={heading.id}
          className={activeId === heading.id ? 'active' : ''}
        >
          {heading.text}
        </a>
      ))}
    </nav>
  );
}
```

## TypeScript Patterns

### Generic Hooks

```typescript
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    setStoredValue(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  };

  return [storedValue, setValue];
}
```

### Return Type Inference

```typescript
// ✅ Let TypeScript infer when possible
export function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);
  const toggle = () => setValue(v => !v);
  return [value, toggle] as const; // as const for tuple
}

// Result: [boolean, () => void]
```

## Hook Testing Checklist

- [ ] Hook is pure (same inputs → same outputs)
- [ ] All dependencies in useEffect arrays
- [ ] Cleanup functions defined where needed
- [ ] Event listeners use { passive: true } for performance
- [ ] useCallback used for stable function references
- [ ] useRef used for values that don't need re-renders
- [ ] Type safety: explicit return type or inferred correctly
- [ ] JSDoc comments for complex hooks
- [ ] Constants imported from @/constants/ui
- [ ] File named use[Feature].ts in /src/hooks/

## Common Mistakes

### Mistake 1: Missing Cleanup

```typescript
// ❌ Wrong
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
}, []); // Missing cleanup!

// ✅ Correct
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

### Mistake 2: Incorrect Dependencies

```typescript
// ❌ Wrong
useEffect(() => {
  fetchData(id);
}, []); // id should be in deps!

// ✅ Correct
useEffect(() => {
  fetchData(id);
}, [id]);
```

### Mistake 3: Using State Instead of Ref

```typescript
// ❌ Wrong (causes unnecessary re-renders)
const [lastScrollY, setLastScrollY] = useState(0);

// ✅ Correct (no re-renders)
const lastScrollY = useRef(0);
```

## Quick Reference

```typescript
// Scroll-based pattern
const [value, setValue] = useState(initial);
const handleScroll = useCallback(() => {...}, []);
useEffect(() => {
  window.addEventListener('scroll', handleScroll, { passive: true });
  return () => window.removeEventListener('scroll', handleScroll);
}, [handleScroll]);

// Observer-based pattern
const observerRef = useRef<IntersectionObserver | null>(null);
useEffect(() => {
  observerRef.current = new IntersectionObserver(...);
  // observe elements
  return () => observerRef.current?.disconnect();
}, []);

// Processing pattern
const [data, setData] = useState<Type[]>([]);
useEffect(() => {
  const processed = processData();
  setData(processed);
}, [dependency]);
```

Remember: Hooks are for reusable logic. If it's only used once, consider keeping it in the component.
