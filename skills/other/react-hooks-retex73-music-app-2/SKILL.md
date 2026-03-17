# React Hooks Skill

## Purpose
Master React hooks patterns including useState, useEffect, useContext, useMemo, useCallback, and custom hooks for the music-app project.

## Core Hooks

### useState
```javascript
function Counter() {
  const [count, setCount] = useState(0);

  // Functional update
  setCount(prev => prev + 1);

  // Object state
  const [user, setUser] = useState({ name: '', email: '' });
  setUser(prev => ({ ...prev, email: 'new@email.com' }));

  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### useEffect
```javascript
// Run once on mount
useEffect(() => {
  fetchData();
}, []);

// Run when dependency changes
useEffect(() => {
  console.log('Count changed:', count);
}, [count]);

// Cleanup
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe();
}, []);

// Async in useEffect
useEffect(() => {
  let isMounted = true;

  async function loadData() {
    const data = await fetchData();
    if (isMounted) setState(data);
  }

  loadData();
  return () => { isMounted = false; };
}, []);
```

### useContext Pattern
```javascript
// Define context and hook together
import { createContext, useContext } from 'react';

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// Usage in components
function Component() {
  const { user, login, logout } = useAuth();
  // ...
}
```

### useMemo
```javascript
// Expensive computation
const filteredTunes = useMemo(() => {
  return tunes.filter(tune =>
    tune.genre === selectedGenre &&
    tune.rhythm === selectedRhythm
  );
}, [tunes, selectedGenre, selectedRhythm]);

// Derived state
const tuneCount = useMemo(() => filteredTunes.length, [filteredTunes]);
```

### useCallback
```javascript
// Stable function reference
const handleAddFavorite = useCallback((tuneId) => {
  setFavorites(prev => [...prev, tuneId]);
}, []);

// Pass to child components
<TuneCard
  tune={tune}
  onFavorite={handleAddFavorite} // Stable reference
/>

// With dependencies
const handleSearch = useCallback((query) => {
  performSearch(query, filters);
}, [filters]);
```

## Custom Hooks

### useLocalStorage
```javascript
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  }, [key, value]);

  return [value, setValue];
}

// Usage
const [favorites, setFavorites] = useLocalStorage('favorites', []);
```

### useDebounce
```javascript
function useDebounce(value, delay) {
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
const [query, setQuery] = useState('');
const debouncedQuery = useDebounce(query, 300);

useEffect(() => {
  if (debouncedQuery) {
    performSearch(debouncedQuery);
  }
}, [debouncedQuery]);
```

## Best Practices

✅ **Do:**
- Always include dependencies in dependency arrays
- Clean up side effects in return function
- Use functional updates when new state depends on old state
- Extract reusable logic into custom hooks
- Memoize expensive computations and callbacks

❌ **Don't:**
- Mutate state directly
- Call hooks conditionally
- Skip dependency arrays (eslint-disable is a code smell)
- Forget to clean up listeners/timers
- Overuse useMemo/useCallback (only when needed)

## Common Patterns

### Data Fetching
```javascript
function useTunes() {
  const [tunes, setTunes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTunes() {
      try {
        const data = await getTunes();
        setTunes(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTunes();
  }, []);

  return { tunes, loading, error };
}
```

### Form Handling
```javascript
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialValues);
  }, [initialValues]);

  return { values, handleChange, reset };
}
```

## Project Patterns

### Context Usage
```javascript
// Always use provided hooks, never direct context access
const { user } = useAuth();           // ✓
const { favorites } = useFavorites(); // ✓

// Not this
const context = useContext(AuthContext); // ✗
```

### Effect Dependencies
```javascript
// Include all dependencies
useEffect(() => {
  if (user) {
    loadFavorites(user.uid);
  }
}, [user]); // Include user

// Use exhaustive-deps lint rule
// eslint-plugin-react-hooks
```

## Common Issues

**Issue:** Infinite loop in useEffect
**Solution:** Check dependencies, ensure not setting state that's in dependency array

**Issue:** Stale closure
**Solution:** Include all dependencies or use functional state updates

**Issue:** "Can't perform state update on unmounted component"
**Solution:** Track mounted state and check before setState
