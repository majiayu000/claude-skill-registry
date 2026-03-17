---
name: react-patterns
description: Modern React patterns for React 19. Hooks, state management, component composition, performance optimization. Use when building React components.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# React Patterns - Modern Component Architecture

## Purpose

Expert guidance for React 19 patterns:

- **Component Design** - Composition over inheritance
- **State Management** - Local, context, and server state
- **Performance** - Memoization and optimization
- **Hooks** - Built-in and custom hooks
- **TypeScript** - Proper typing patterns

---

## Component Patterns

### 1. Compound Components

```tsx
// Composable API for complex UIs
interface TabsContextValue {
	activeTab: string;
	setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
	const [activeTab, setActiveTab] = useState(defaultTab);

	return (
		<TabsContext.Provider value={{ activeTab, setActiveTab }}>
			<div className="tabs">{children}</div>
		</TabsContext.Provider>
	);
}

function TabList({ children }: { children: ReactNode }) {
	return (
		<div className="tab-list" role="tablist">
			{children}
		</div>
	);
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
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
}

function TabPanel({ id, children }: { id: string; children: ReactNode }) {
	const context = useContext(TabsContext);
	if (!context) throw new Error('TabPanel must be used within Tabs');

	if (context.activeTab !== id) return null;
	return <div role="tabpanel">{children}</div>;
}

// Usage
<Tabs defaultTab="home">
	<TabList>
		<Tab id="home">Home</Tab>
		<Tab id="settings">Settings</Tab>
	</TabList>
	<TabPanel id="home">Home content</TabPanel>
	<TabPanel id="settings">Settings content</TabPanel>
</Tabs>;
```

### 2. Render Props Pattern

```tsx
interface MousePosition {
	x: number;
	y: number;
}

function MouseTracker({ render }: { render: (pos: MousePosition) => ReactNode }) {
	const [position, setPosition] = useState({ x: 0, y: 0 });

	useEffect(() => {
		const handleMove = (e: MouseEvent) => {
			setPosition({ x: e.clientX, y: e.clientY });
		};
		window.addEventListener('mousemove', handleMove);
		return () => window.removeEventListener('mousemove', handleMove);
	}, []);

	return <>{render(position)}</>;
}

// Usage
<MouseTracker
	render={({ x, y }) => (
		<div>
			Mouse: {x}, {y}
		</div>
	)}
/>;
```

### 3. HOC (Higher-Order Component)

```tsx
function withAuth<P extends object>(Component: ComponentType<P>) {
	return function AuthenticatedComponent(props: P) {
		const { user, isLoading } = useAuth();

		if (isLoading) return <Loading />;
		if (!user) return <Redirect to="/login" />;

		return <Component {...props} />;
	};
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

---

## Hooks Patterns

### Custom Hooks

```tsx
// useLocalStorage - Persist state
function useLocalStorage<T>(key: string, initialValue: T) {
	const [storedValue, setStoredValue] = useState<T>(() => {
		if (typeof window === 'undefined') return initialValue;
		try {
			const item = window.localStorage.getItem(key);
			return item ? JSON.parse(item) : initialValue;
		} catch {
			return initialValue;
		}
	});

	const setValue = useCallback(
		(value: T | ((val: T) => T)) => {
			setStoredValue((prev) => {
				const valueToStore = value instanceof Function ? value(prev) : value;
				window.localStorage.setItem(key, JSON.stringify(valueToStore));
				return valueToStore;
			});
		},
		[key]
	);

	return [storedValue, setValue] as const;
}

// useDebounce - Debounced value
function useDebounce<T>(value: T, delay: number): T {
	const [debouncedValue, setDebouncedValue] = useState(value);

	useEffect(() => {
		const handler = setTimeout(() => setDebouncedValue(value), delay);
		return () => clearTimeout(handler);
	}, [value, delay]);

	return debouncedValue;
}

// useAsync - Async operation state
function useAsync<T>(asyncFunction: () => Promise<T>, deps: unknown[] = []) {
	const [state, setState] = useState<{
		data: T | null;
		loading: boolean;
		error: Error | null;
	}>({
		data: null,
		loading: true,
		error: null,
	});

	useEffect(() => {
		let mounted = true;
		setState((s) => ({ ...s, loading: true }));

		asyncFunction()
			.then((data) => mounted && setState({ data, loading: false, error: null }))
			.catch((error) => mounted && setState({ data: null, loading: false, error }));

		return () => {
			mounted = false;
		};
	}, deps);

	return state;
}
```

---

## State Management

### 1. useReducer for Complex State

```tsx
type State = {
	items: Item[];
	loading: boolean;
	error: string | null;
};

type Action =
	| { type: 'FETCH_START' }
	| { type: 'FETCH_SUCCESS'; payload: Item[] }
	| { type: 'FETCH_ERROR'; payload: string }
	| { type: 'ADD_ITEM'; payload: Item }
	| { type: 'REMOVE_ITEM'; payload: string };

function reducer(state: State, action: Action): State {
	switch (action.type) {
		case 'FETCH_START':
			return { ...state, loading: true, error: null };
		case 'FETCH_SUCCESS':
			return { ...state, loading: false, items: action.payload };
		case 'FETCH_ERROR':
			return { ...state, loading: false, error: action.payload };
		case 'ADD_ITEM':
			return { ...state, items: [...state.items, action.payload] };
		case 'REMOVE_ITEM':
			return { ...state, items: state.items.filter((i) => i.id !== action.payload) };
		default:
			return state;
	}
}
```

### 2. Context for Global State

```tsx
interface AppContextValue {
	user: User | null;
	theme: 'light' | 'dark';
	setTheme: (theme: 'light' | 'dark') => void;
}

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
	const [theme, setTheme] = useState<'light' | 'dark'>('light');
	const { data: user } = useUser();

	const value = useMemo(() => ({ user, theme, setTheme }), [user, theme]);

	return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
	const context = useContext(AppContext);
	if (!context) throw new Error('useApp must be used within AppProvider');
	return context;
}
```

---

## Performance Optimization

### 1. Memoization

```tsx
// memo - Prevent re-renders
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
	return (
		<ul>
			{items.map((item) => (
				<li key={item.id}>{item.name}</li>
			))}
		</ul>
	);
});

// useMemo - Expensive calculations
function Dashboard({ data }: { data: DataPoint[] }) {
	const processedData = useMemo(() => {
		return data.map((d) => ({ ...d, computed: expensiveCalculation(d) }));
	}, [data]);

	return <Chart data={processedData} />;
}

// useCallback - Stable function references
function Parent() {
	const [count, setCount] = useState(0);

	const handleClick = useCallback(() => {
		setCount((c) => c + 1);
	}, []);

	return <Child onClick={handleClick} />;
}
```

### 2. Code Splitting

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
	return (
		<Suspense fallback={<Loading />}>
			<HeavyComponent />
		</Suspense>
	);
}
```

---

## TypeScript Patterns

### Props Types

```tsx
// Discriminated unions for variants
type ButtonProps = { variant: 'primary'; onClick: () => void } | { variant: 'link'; href: string };

function Button(props: ButtonProps) {
	if (props.variant === 'link') {
		return <a href={props.href}>Link</a>;
	}
	return <button onClick={props.onClick}>Button</button>;
}

// Generic components
interface ListProps<T> {
	items: T[];
	renderItem: (item: T) => ReactNode;
	keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
	return (
		<ul>
			{items.map((item) => (
				<li key={keyExtractor(item)}>{renderItem(item)}</li>
			))}
		</ul>
	);
}
```

---

## Agent Integration

This skill is used by:

- **react-expert** subagent
- **render-optimizer** for performance issues
- **ui-mobile/tablet/desktop** for component patterns

---

## FORBIDDEN

1. **Class components** - Use function components
2. **Prop drilling** - Use context or composition
3. **Inline objects/functions in JSX** - Causes re-renders
4. **useEffect for derived state** - Use useMemo
5. **Mutating state directly** - Always use setState/dispatch

---

## Version

- **v1.0.0** - Initial implementation based on React 19 patterns
