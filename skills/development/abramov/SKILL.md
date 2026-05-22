---
name: abramov-state-composition
description: Write JavaScript code in the style of Dan Abramov, co-creator of Redux and React core team member. Emphasizes predictable state management, composition over inheritance, and developer experience. Use when building React applications or managing complex state.
---

# Dan Abramov Style Guide

## Overview

Dan Abramov is the co-creator of Redux, Create React App, and a member of the React core team. His philosophy emphasizes predictable state, composition, and building tools that make developers more productive.

## Core Philosophy

> "Redux is not the answer to all state management. It's one tool in the toolbox."

> "The best code is the code that doesn't exist."

> "Make impossible states impossible."

Abramov believes in making code predictable and debuggable, using the right level of abstraction, and prioritizing developer experience.

## Design Principles

1. **Predictability**: State changes should be predictable and traceable.

2. **Composition**: Build complex from simple, not through inheritance.

3. **Explicit Over Magic**: Prefer verbose clarity over clever brevity.

4. **Developer Experience**: Tools should help developers, not fight them.

## When Writing Code

### Always

- Keep state as flat as possible
- Make state changes predictable and traceable
- Use composition to build complex components
- Colocate state with components that need it
- Write components that are easy to test
- Think about error boundaries

### Never

- Mutate state directly
- Put everything in global state
- Use inheritance for component reuse
- Create deeply nested state structures
- Ignore render performance in lists
- Swallow errors silently

### Prefer

- Local state over global when possible
- Hooks over class components
- Function composition over inheritance
- Explicit data flow over prop drilling solutions
- Pure functions for state updates
- Custom hooks for reusable logic

## Code Patterns

### Component Composition

```javascript
// BAD: Prop drilling and inheritance thinking
function App() {
    return (
        <Layout 
            header={<Header user={user} onLogout={logout} />}
            sidebar={<Sidebar items={items} selected={selected} onSelect={select} />}
            content={<Content data={data} user={user} />}
        />
    );
}

// GOOD: Composition with children
function App() {
    return (
        <Layout>
            <Header>
                <UserMenu user={user} onLogout={logout} />
            </Header>
            <Sidebar>
                <Navigation items={items} selected={selected} onSelect={select} />
            </Sidebar>
            <Content>
                <Dashboard data={data} />
            </Content>
        </Layout>
    );
}


// Compound Components Pattern
function Tabs({ children, defaultIndex = 0 }) {
    const [activeIndex, setActiveIndex] = useState(defaultIndex);
    
    return (
        <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
            {children}
        </TabsContext.Provider>
    );
}

Tabs.List = function TabList({ children }) {
    return <div role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ index, children }) {
    const { activeIndex, setActiveIndex } = useContext(TabsContext);
    return (
        <button 
            role="tab"
            aria-selected={activeIndex === index}
            onClick={() => setActiveIndex(index)}
        >
            {children}
        </button>
    );
};

Tabs.Panels = function TabPanels({ children }) {
    const { activeIndex } = useContext(TabsContext);
    return Children.toArray(children)[activeIndex];
};

// Usage - composable and flexible
<Tabs defaultIndex={0}>
    <Tabs.List>
        <Tabs.Tab index={0}>First</Tabs.Tab>
        <Tabs.Tab index={1}>Second</Tabs.Tab>
    </Tabs.List>
    <Tabs.Panels>
        <Panel>First content</Panel>
        <Panel>Second content</Panel>
    </Tabs.Panels>
</Tabs>
```

### Custom Hooks for Logic Reuse

```javascript
// Extract reusable logic into custom hooks
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(error);
            return initialValue;
        }
    });

    const setValue = useCallback((value) => {
        try {
            const valueToStore = value instanceof Function 
                ? value(storedValue) 
                : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    }, [key, storedValue]);

    return [storedValue, setValue];
}


// Async data fetching hook
function useAsync(asyncFunction, immediate = true) {
    const [status, setStatus] = useState('idle');
    const [value, setValue] = useState(null);
    const [error, setError] = useState(null);

    const execute = useCallback(async () => {
        setStatus('pending');
        setValue(null);
        setError(null);
        
        try {
            const response = await asyncFunction();
            setValue(response);
            setStatus('success');
        } catch (error) {
            setError(error);
            setStatus('error');
        }
    }, [asyncFunction]);

    useEffect(() => {
        if (immediate) {
            execute();
        }
    }, [execute, immediate]);

    return { execute, status, value, error };
}
```

### State Management Patterns

```javascript
// Pattern 1: Colocate state
// State should live as close to where it's used as possible

// BAD: Lifting state too high
function App() {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState([]);
    // ... passed down through many layers
}

// GOOD: State lives where it's used
function SearchComponent() {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState([]);
    // Only this component cares about search
}


// Pattern 2: Reducer for complex state
function reducer(state, action) {
    switch (action.type) {
        case 'FETCH_START':
            return { ...state, loading: true, error: null };
        case 'FETCH_SUCCESS':
            return { ...state, loading: false, data: action.payload };
        case 'FETCH_ERROR':
            return { ...state, loading: false, error: action.payload };
        default:
            throw new Error(`Unknown action: ${action.type}`);
    }
}

function DataComponent() {
    const [state, dispatch] = useReducer(reducer, {
        data: null,
        loading: false,
        error: null
    });
    
    // Actions are explicit and traceable
    const fetchData = async () => {
        dispatch({ type: 'FETCH_START' });
        try {
            const data = await api.getData();
            dispatch({ type: 'FETCH_SUCCESS', payload: data });
        } catch (error) {
            dispatch({ type: 'FETCH_ERROR', payload: error.message });
        }
    };
}


// Pattern 3: Make impossible states impossible
// BAD: Multiple booleans that can conflict
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
// What if isLoading AND isError are both true?

// GOOD: Single status that can only be one thing
const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'error' | 'success'
```

### Performance Patterns

```javascript
// Memoize expensive computations
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]);

// Memoize callbacks passed to children
const handleClick = useCallback((id) => {
    setSelected(id);
}, []);

// Memoize components that receive stable props
const MemoizedChild = React.memo(function Child({ data, onClick }) {
    return <div onClick={onClick}>{data.name}</div>;
});

// Don't over-optimize! Profile first
// BAD: Premature optimization everywhere
const value = useMemo(() => a + b, [a, b]);  // Simple addition doesn't need memo

// GOOD: Optimize what matters
// - Large lists with React.memo on items
// - Expensive computations with useMemo
// - Context values to prevent cascading rerenders
```

### Error Boundaries

```javascript
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by boundary:', error, errorInfo);
        // Log to error reporting service
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || <h1>Something went wrong.</h1>;
        }
        return this.props.children;
    }
}

// Usage: wrap parts of your app
<ErrorBoundary fallback={<ErrorPage />}>
    <FeatureComponent />
</ErrorBoundary>
```

## Mental Model

Abramov approaches React code by asking:

1. **Where should this state live?** As low as possible, as high as necessary
2. **Is this predictable?** Can I trace how we got here?
3. **Can this be composed?** Small pieces that combine well
4. **Is this testable?** Pure functions, clear inputs/outputs
5. **What can go wrong?** Error boundaries, loading states

## Signature Abramov Moves

- Composition over inheritance, always
- Custom hooks for reusable logic
- useReducer for complex state transitions
- Make impossible states impossible
- Colocate state near usage
- Memoize strategically, not everywhere
