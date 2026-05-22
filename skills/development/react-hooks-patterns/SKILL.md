---
name: react-hooks-patterns
description: Use when React Hooks patterns including useState, useEffect, useContext, useMemo, useCallback, and custom hooks. Use for modern React development.
allowed-tools:
  - Bash
  - Read
---

# React Hooks Patterns

Master React Hooks to build modern, functional React components.  
This skill covers built-in hooks, custom hooks, and advanced patterns
for state management and side effects.

## useState Hook

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  const increment = () => setCount(count + 1);
  const decrement = () => setCount(prev => prev - 1);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick=

{decrement}>-</button>
    </div>
  );
}

// Complex state
interface User {
  name: string;
  email: string;
}

function UserForm() {
  const [user, setUser] = useState<User>({
    name: '',
    email: ''
  });
  
  const updateField = (field: keyof User, value: string) => {
    setUser(prev => ({ ...prev, [field]: value }));
  };
  
  return (
    <form>
      <input
        value={user.name}
        onChange={(e) => updateField('name', e.target.value)}
      />
      <input
        value={user.email}
        onChange={(e) => updateField('email', e.target.value)}
      />
    </form>
  );
}
```

## useEffect Hook

```typescript
import { useEffect, useState } from 'react';

function DataFetcher({ userId }: { userId: number }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        const result = await response.json();
        
        if (!cancelled) {
          setData(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }
    
    fetchData();
    
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  return <div>{JSON.stringify(data)}</div>;
}
```

## useContext Hook

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

interface Theme {
  mode: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<Theme | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  
  const toggleTheme = () => {
    setMode(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function ThemedButton() {
  const { mode, toggleTheme } = useTheme();
  return (
    <button onClick={toggleTheme}>
      Current mode: {mode}
    </button>
  );
}
```

## useMemo and useCallback

```typescript
import { useMemo, useCallback, useState } from 'react';

function ExpensiveComponent({ items }: { items: number[] }) {
  const [filter, setFilter] = useState('');
  
  // Memoize expensive computation
  const filteredItems = useMemo(() => {
    console.log('Filtering items...');
    return items.filter(item => 
      item.toString().includes(filter)
    );
  }, [items, filter]);
  
  // Memoize callback function
  const handleFilterChange = useCallback((value: string) => {
    setFilter(value);
  }, []);
  
  return (
    <div>
      <input 
        value={filter}
        onChange={(e) => handleFilterChange(e.target.value)}
      />
      <ItemList items={filteredItems} />
    </div>
  );
}
```

## Custom Hooks

```typescript
// useLocalStorage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });
  
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = 
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };
  
  return [storedValue, setValue] as const;
}

// useDebounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
}

// Usage
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);
  
  useEffect(() => {
    if (debouncedSearchTerm) {
      // Perform search
      console.log('Searching for:', debouncedSearchTerm);
    }
  }, [debouncedSearchTerm]);
  
  return (
    <input
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
    />
  );
}
```

## useReducer for Complex State

```typescript
import { useReducer } from 'react';

interface State {
  count: number;
  history: number[];
}

type Action =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'RESET' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'INCREMENT':
      return {
        count: state.count + 1,
        history: [...state.history, state.count + 1]
      };
    case 'DECREMENT':
      return {
        count: state.count - 1,
        history: [...state.history, state.count - 1]
      };
    case 'RESET':
      return { count: 0, history: [0] };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, {
    count: 0,
    history: [0]
  });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
      <button onClick={() => dispatch({ type: 'RESET' })}>Reset</button>
      <p>History: {state.history.join(', ')}</p>
    </div>
  );
}

// Complex form state with useReducer
interface FormState {
  values: {
    name: string;
    email: string;
    age: number;
  };
  errors: {
    name?: string;
    email?: string;
    age?: string;
  };
  touched: {
    name: boolean;
    email: boolean;
    age: boolean;
  };
  isSubmitting: boolean;
}

type FormAction =
  | { type: 'SET_FIELD'; field: string; value: string | number }
  | { type: 'SET_ERROR'; field: string; error: string }
  | { type: 'SET_TOUCHED'; field: string }
  | { type: 'SUBMIT_START' }
  | { type: 'SUBMIT_SUCCESS' }
  | { type: 'SUBMIT_ERROR' }
  | { type: 'RESET' };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value }
      };
    case 'SET_ERROR':
      return {
        ...state,
        errors: { ...state.errors, [action.field]: action.error }
      };
    case 'SET_TOUCHED':
      return {
        ...state,
        touched: { ...state.touched, [action.field]: true }
      };
    case 'SUBMIT_START':
      return { ...state, isSubmitting: true };
    case 'SUBMIT_SUCCESS':
      return { ...state, isSubmitting: false };
    case 'SUBMIT_ERROR':
      return { ...state, isSubmitting: false };
    case 'RESET':
      return {
        values: { name: '', email: '', age: 0 },
        errors: {},
        touched: { name: false, email: false, age: false },
        isSubmitting: false
      };
    default:
      return state;
  }
}

function ComplexForm() {
  const [state, dispatch] = useReducer(formReducer, {
    values: { name: '', email: '', age: 0 },
    errors: {},
    touched: { name: false, email: false, age: false },
    isSubmitting: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch({ type: 'SUBMIT_START' });
    try {
      await submitForm(state.values);
      dispatch({ type: 'SUBMIT_SUCCESS' });
    } catch (error) {
      dispatch({ type: 'SUBMIT_ERROR' });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={state.values.name}
        onChange={(e) => dispatch({
          type: 'SET_FIELD',
          field: 'name',
          value: e.target.value
        })}
        onBlur={() => dispatch({ type: 'SET_TOUCHED', field: 'name' })}
      />
      {state.touched.name && state.errors.name && (
        <span>{state.errors.name}</span>
      )}
      <button type="submit" disabled={state.isSubmitting}>
        Submit
      </button>
    </form>
  );
}
```

## useRef Hook

```typescript
import { useRef, useEffect, useState } from 'react';

function FocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} />;
}

// Storing mutable values
function Timer() {
  const intervalRef = useRef<number | null>(null);
  const [count, setCount] = useState(0);

  const start = () => {
    if (intervalRef.current !== null) return;
    intervalRef.current = window.setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
  };

  const stop = () => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current !== null) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// Previous value tracking
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

function CounterWithPrevious() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

## useLayoutEffect for DOM Measurements

```typescript
import { useLayoutEffect, useRef, useState } from 'react';

// Measure element dimensions before paint
function TooltipWithMeasurement() {
  const [tooltipHeight, setTooltipHeight] = useState(0);
  const tooltipRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (tooltipRef.current) {
      const { height } = tooltipRef.current.getBoundingClientRect();
      setTooltipHeight(height);
    }
  }, []);

  return (
    <div>
      <div
        ref={tooltipRef}
        style={{
          position: 'absolute',
          top: `calc(100% + ${tooltipHeight}px)`
        }}
      >
        Tooltip content
      </div>
    </div>
  );
}

// Synchronize scroll positions
function SyncedScrollPanels() {
  const leftRef = useRef<HTMLDivElement>(null);
  const rightRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const left = leftRef.current;
    const right = rightRef.current;
    if (!left || !right) return;

    const syncScroll = (source: HTMLDivElement, target: HTMLDivElement) => {
      return () => {
        target.scrollTop = source.scrollTop;
      };
    };

    const leftHandler = syncScroll(left, right);
    const rightHandler = syncScroll(right, left);

    left.addEventListener('scroll', leftHandler);
    right.addEventListener('scroll', rightHandler);

    return () => {
      left.removeEventListener('scroll', leftHandler);
      right.removeEventListener('scroll', rightHandler);
    };
  }, []);

  return (
    <div style={{ display: 'flex' }}>
      <div ref={leftRef} style={{ overflow: 'auto', height: 300 }}>
        Left panel content
      </div>
      <div ref={rightRef} style={{ overflow: 'auto', height: 300 }}>
        Right panel content
      </div>
    </div>
  );
}
```

## useImperativeHandle with forwardRef

```typescript
import {
  useRef,
  useImperativeHandle,
  forwardRef,
  useState
} from 'react';

// Define exposed methods interface
interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

interface VideoPlayerProps {
  src: string;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  (props, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    useImperativeHandle(ref, () => ({
      play: () => {
        videoRef.current?.play();
        setIsPlaying(true);
      },
      pause: () => {
        videoRef.current?.pause();
        setIsPlaying(false);
      },
      seek: (time: number) => {
        if (videoRef.current) {
          videoRef.current.currentTime = time;
        }
      }
    }), []);

    return (
      <div>
        <video ref={videoRef} src={props.src} />
        <p>Status: {isPlaying ? 'Playing' : 'Paused'}</p>
      </div>
    );
  }
);

function ParentComponent() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  return (
    <div>
      <VideoPlayer ref={playerRef} src="video.mp4" />
      <button onClick={() => playerRef.current?.play()}>
        Play
      </button>
      <button onClick={() => playerRef.current?.pause()}>
        Pause
      </button>
      <button onClick={() => playerRef.current?.seek(30)}>
        Skip to 30s
      </button>
    </div>
  );
}

// Input with custom imperative methods
interface InputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

const CustomInput = forwardRef<InputHandle, { placeholder?: string }>(
  (props, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => {
        inputRef.current?.focus();
      },
      clear: () => {
        if (inputRef.current) {
          inputRef.current.value = '';
        }
      },
      getValue: () => {
        return inputRef.current?.value || '';
      }
    }), []);

    return <input ref={inputRef} placeholder={props.placeholder} />;
  }
);
```

## Custom Hooks Composition Patterns

```typescript
import { useState, useEffect, useCallback } from 'react';

// Composing multiple hooks together
function useAsync<T>(asyncFunction: () => Promise<T>) {
  const [status, setStatus] = useState<'idle' | 'pending' | 'success' | 'error'>('idle');
  const [value, setValue] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(() => {
    setStatus('pending');
    setValue(null);
    setError(null);

    return asyncFunction()
      .then((response) => {
        setValue(response);
        setStatus('success');
      })
      .catch((error) => {
        setError(error);
        setStatus('error');
      });
  }, [asyncFunction]);

  return { execute, status, value, error };
}

// Composing useAsync with other hooks
function useFetch<T>(url: string) {
  const fetchData = useCallback(
    () => fetch(url).then((res) => res.json() as Promise<T>),
    [url]
  );

  const { execute, status, value, error } = useAsync<T>(fetchData);

  useEffect(() => {
    execute();
  }, [execute]);

  return { data: value, loading: status === 'pending', error };
}

// Hook that composes multiple custom hooks
function useForm<T extends Record<string, any>>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback((field: keyof T, value: any) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  }, []);

  const handleBlur = useCallback((field: keyof T) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
  }, []);

  const handleSubmit = useCallback(
    async (
      onSubmit: (values: T) => Promise<void>,
      validate?: (values: T) => Partial<Record<keyof T, string>>
    ) => {
      if (validate) {
        const validationErrors = validate(values);
        setErrors(validationErrors);
        if (Object.keys(validationErrors).length > 0) return;
      }

      setIsSubmitting(true);
      try {
        await onSubmit(values);
      } finally {
        setIsSubmitting(false);
      }
    },
    [values]
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset
  };
}

// Using composed hooks
function UserProfileForm() {
  const {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset
  } = useForm({
    name: '',
    email: '',
    bio: ''
  });

  const validate = (vals: typeof values) => {
    const errs: Partial<Record<keyof typeof values, string>> = {};
    if (!vals.name) errs.name = 'Name is required';
    if (!vals.email) errs.email = 'Email is required';
    return errs;
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit(
          async (vals) => {
            await saveProfile(vals);
          },
          validate
        );
      }}
    >
      <input
        value={values.name}
        onChange={(e) => handleChange('name', e.target.value)}
        onBlur={() => handleBlur('name')}
      />
      {touched.name && errors.name && <span>{errors.name}</span>}
      <button type="submit" disabled={isSubmitting}>
        Save
      </button>
      <button type="button" onClick={reset}>
        Reset
      </button>
    </form>
  );
}
```

## Advanced useCallback and useMemo Optimization

```typescript
import { useState, useCallback, useMemo, memo } from 'react';

// Complex memoization scenario
interface Item {
  id: number;
  name: string;
  category: string;
  price: number;
}

interface Props {
  items: Item[];
}

const ItemList = memo(({ items }: Props) => {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

function OptimizedShop() {
  const [items] = useState<Item[]>([
    { id: 1, name: 'Apple', category: 'fruit', price: 1.5 },
    { id: 2, name: 'Banana', category: 'fruit', price: 0.8 },
    { id: 3, name: 'Carrot', category: 'vegetable', price: 1.2 }
  ]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'price'>('name');

  // Memoize filtered items
  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      const matchesSearch = item.name
        .toLowerCase()
        .includes(searchTerm.toLowerCase());
      const matchesCategory =
        selectedCategory === 'all' || item.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [items, searchTerm, selectedCategory]);

  // Memoize sorted items
  const sortedItems = useMemo(() => {
    return [...filteredItems].sort((a, b) => {
      if (sortBy === 'name') {
        return a.name.localeCompare(b.name);
      }
      return a.price - b.price;
    });
  }, [filteredItems, sortBy]);

  // Memoize categories list
  const categories = useMemo(() => {
    const uniqueCategories = new Set(items.map((item) => item.category));
    return ['all', ...Array.from(uniqueCategories)];
  }, [items]);

  // Memoize callbacks
  const handleSearch = useCallback((value: string) => {
    setSearchTerm(value);
  }, []);

  const handleCategoryChange = useCallback((category: string) => {
    setSelectedCategory(category);
  }, []);

  const handleSortChange = useCallback((sort: 'name' | 'price') => {
    setSortBy(sort);
  }, []);

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search items..."
      />
      <select
        value={selectedCategory}
        onChange={(e) => handleCategoryChange(e.target.value)}
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>
            {cat}
          </option>
        ))}
      </select>
      <select
        value={sortBy}
        onChange={(e) => handleSortChange(e.target.value as 'name' | 'price')}
      >
        <option value="name">Sort by Name</option>
        <option value="price">Sort by Price</option>
      </select>
      <ItemList items={sortedItems} />
    </div>
  );
}

// Factory pattern with useCallback
function useEventCallback<T extends (...args: any[]) => any>(fn: T): T {
  const ref = useRef<T>(fn);

  useLayoutEffect(() => {
    ref.current = fn;
  });

  return useCallback(
    ((...args) => ref.current(...args)) as T,
    []
  );
}

// Usage of useEventCallback
function FormWithEventCallback() {
  const [count, setCount] = useState(0);

  // This callback always has access to latest count
  // but maintains stable reference
  const handleSubmit = useEventCallback(() => {
    console.log('Current count:', count);
  });

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <ExpensiveChild onSubmit={handleSubmit} />
    </div>
  );
}
```

## Advanced Hook Patterns

```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

// useInterval - Declarative interval hook
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}

function Clock() {
  const [time, setTime] = useState(new Date());

  useInterval(() => {
    setTime(new Date());
  }, 1000);

  return <div>{time.toLocaleTimeString()}</div>;
}

// useOnScreen - Detect if element is visible
function useOnScreen(ref: React.RefObject<HTMLElement>) {
  const [isIntersecting, setIntersecting] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(([entry]) =>
      setIntersecting(entry.isIntersecting)
    );

    observer.observe(ref.current);
    return () => {
      observer.disconnect();
    };
  }, [ref]);

  return isIntersecting;
}

function LazyImage({ src, alt }: { src: string; alt: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const isVisible = useOnScreen(ref);

  return (
    <div ref={ref}>
      {isVisible ? (
        <img src={src} alt={alt} />
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}

// useMediaQuery - Responsive design hook
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);

    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

function ResponsiveComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)');
  const isDesktop = useMediaQuery('(min-width: 1025px)');

  return (
    <div>
      {isMobile && <div>Mobile View</div>}
      {isTablet && <div>Tablet View</div>}
      {isDesktop && <div>Desktop View</div>}
    </div>
  );
}

// useClickOutside - Detect clicks outside element
function useClickOutside(
  ref: React.RefObject<HTMLElement>,
  handler: (event: MouseEvent | TouchEvent) => void
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}

function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useClickOutside(ref, () => setIsOpen(false));

  return (
    <div ref={ref}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && <div>Dropdown Content</div>}
    </div>
  );
}

// useToggle - Boolean state management
function useToggle(initialValue = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue);
  const toggle = useCallback(() => setValue((v) => !v), []);
  return [value, toggle];
}

function ToggleExample() {
  const [isOn, toggle] = useToggle(false);

  return (
    <div>
      <p>The switch is {isOn ? 'ON' : 'OFF'}</p>
      <button onClick={toggle}>Toggle</button>
    </div>
  );
}

// useArray - Array manipulation hook
function useArray<T>(initialValue: T[]) {
  const [array, setArray] = useState(initialValue);

  const push = useCallback((element: T) => {
    setArray((a) => [...a, element]);
  }, []);

  const filter = useCallback((callback: (item: T) => boolean) => {
    setArray((a) => a.filter(callback));
  }, []);

  const update = useCallback((index: number, newElement: T) => {
    setArray((a) => [
      ...a.slice(0, index),
      newElement,
      ...a.slice(index + 1)
    ]);
  }, []);

  const remove = useCallback((index: number) => {
    setArray((a) => [...a.slice(0, index), ...a.slice(index + 1)]);
  }, []);

  const clear = useCallback(() => {
    setArray([]);
  }, []);

  return { array, set: setArray, push, filter, update, remove, clear };
}

function TodoList() {
  const { array: todos, push, remove, update } = useArray<{
    id: number;
    text: string;
    completed: boolean;
  }>([]);

  const addTodo = (text: string) => {
    push({ id: Date.now(), text, completed: false });
  };

  const toggleTodo = (index: number) => {
    const todo = todos[index];
    update(index, { ...todo, completed: !todo.completed });
  };

  return (
    <div>
      {todos.map((todo, index) => (
        <div key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(index)}
          />
          <span>{todo.text}</span>
          <button onClick={() => remove(index)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

## When to Use This Skill

Use react-hooks-patterns when you need to:

- Build modern React applications with functional components
- Manage component state with useState and useReducer
- Handle side effects with useEffect
- Share state across components with useContext
- Optimize performance with useMemo and useCallback
- Create reusable logic with custom hooks
- Access DOM elements with useRef
- Build maintainable React applications
- Follow React best practices and patterns

## Best Practices

- Use functional updates when new state depends on previous state
- Always clean up side effects in useEffect return function
- Include all dependencies in useEffect dependency array
- Use useCallback to memoize functions passed to child components
- Use useMemo only for expensive computations, not simple values
- Create custom hooks to encapsulate and reuse stateful logic
- Use useReducer for complex state logic with multiple sub-values
- Keep hooks at the top level of components, never in conditions
- Name custom hooks with "use" prefix for linting and conventions
- Use TypeScript for type safety and better developer experience
- Separate concerns by creating focused custom hooks
- Use useRef for values that don't trigger re-renders
- Prefer useLayoutEffect only when measuring DOM or preventing flicker
- Use memo() with components that receive callback props
- Compose hooks to build more complex behaviors from simple ones
- Use useImperativeHandle sparingly, prefer declarative patterns
- Avoid premature optimization with useMemo and useCallback
- Keep dependency arrays honest, use ESLint exhaustive-deps rule
- Extract complex logic into custom hooks for testability
- Use useContext for global state, not prop drilling

## Common Pitfalls

- Forgetting to include dependencies in useEffect array
- Not cleaning up side effects leading to memory leaks
- Overusing useCallback and useMemo causing premature optimization
- Calling hooks conditionally or inside loops (violates Rules of Hooks)
- Not handling async operations properly in useEffect
- Creating infinite loops by updating state in useEffect incorrectly
- Mutating ref.current during render instead of in effects
- Using stale closures in callbacks without proper dependencies
- Not using functional updates with useState when needed
- Setting state on unmounted components
- Using object or array literals in dependency arrays
- Not memoizing expensive calculations that run on every render
- Confusing useEffect with useLayoutEffect use cases
- Creating unnecessary re-renders by not memoizing callbacks
- Using useState for values that should be refs
- Not using cleanup functions for event listeners and subscriptions
- Forgetting that useEffect runs after paint, not before
- Creating tightly coupled custom hooks that are hard to reuse
- Over-abstracting with custom hooks too early
- Ignoring ESLint warnings about dependency arrays

## Resources

### Official React Documentation

- [React Hooks API Reference](https://react.dev/reference/react)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [useState Hook](https://react.dev/reference/react/useState)
- [useEffect Hook](https://react.dev/reference/react/useEffect)
- [useContext Hook](https://react.dev/reference/react/useContext)
- [useReducer Hook](https://react.dev/reference/react/useReducer)
- [useCallback Hook](https://react.dev/reference/react/useCallback)
- [useMemo Hook](https://react.dev/reference/react/useMemo)
- [useRef Hook](https://react.dev/reference/react/useRef)
- [useLayoutEffect Hook](https://react.dev/reference/react/useLayoutEffect)
- [useImperativeHandle Hook](https://react.dev/reference/react/useImperativeHandle)

### Guides and Best Practices

- [Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects)
- [Removing Effect Dependencies](https://react.dev/learn/removing-effect-dependencies)
- [Lifecycle of Reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects)

### TypeScript Resources

- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [React TypeScript Hooks](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/hooks)
- [Advanced React TypeScript](https://react-typescript-cheatsheet.netlify.app/docs/advanced/intro)

### Additional Resources

- [usehooks.com - Custom Hooks Collection](https://usehooks.com/)
- [usehooks-ts - TypeScript Hooks](https://usehooks-ts.com/)
- [React Hooks FAQ](https://react.dev/learn#using-hooks)
- [ESLint Plugin React Hooks](https://www.npmjs.com/package/eslint-plugin-react-hooks)
