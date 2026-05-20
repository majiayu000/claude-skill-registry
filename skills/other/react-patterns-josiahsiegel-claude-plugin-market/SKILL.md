---
name: react-patterns
description: Complete React component patterns system. PROACTIVELY activate for: (1) Compound components with context, (2) Render props pattern, (3) Higher-Order Components (HOC), (4) Custom hooks as patterns, (5) Provider pattern with reducer, (6) Controlled vs uncontrolled components, (7) Prop getter pattern, (8) State reducer pattern. Provides: Pattern implementations, composition strategies, reusable component APIs, flexible state control. Ensures clean, maintainable component architecture.
---

## Quick Reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| Compound Components | Related components sharing state | `<Tabs><Tab /><Panel /></Tabs>` |
| Render Props | Dynamic rendering with shared logic | `<Mouse>{({x,y}) => ...}</Mouse>` |
| HOC | Cross-cutting concerns | `withAuth(Component)` |
| Custom Hooks | Stateful logic reuse | `useToggle()`, `useDebounce()` |
| Provider Pattern | Global/shared state | `<CartProvider>...</CartProvider>` |
| Controlled/Uncontrolled | Form input flexibility | `value` vs `defaultValue` |
| Prop Getters | Accessible component APIs | `getButtonProps()` |
| State Reducer | Customizable state logic | `useReducer(customReducer)` |

## When to Use This Skill

Use for **React component architecture**:
- Building flexible, reusable component APIs
- Implementing compound component patterns
- Creating render props for dynamic content
- Developing custom hooks for logic reuse
- Managing controlled vs uncontrolled inputs
- Designing accessible component interfaces

**For state management**: see `react-state-management`

---

# React Component Patterns

## Compound Components

### Basic Compound Component

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Context for sharing state
interface TabsContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs components must be used within a Tabs provider');
  }
  return context;
}

// Parent component
interface TabsProps {
  defaultTab: string;
  children: ReactNode;
}

function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Tab List
function TabList({ children }: { children: ReactNode }) {
  return <div className="tab-list" role="tablist">{children}</div>;
}

// Tab Button
interface TabProps {
  value: string;
  children: ReactNode;
}

function Tab({ value, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext();

  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
      className={activeTab === value ? 'active' : ''}
    >
      {children}
    </button>
  );
}

// Tab Panel
interface TabPanelProps {
  value: string;
  children: ReactNode;
}

function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabsContext();

  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className="tab-panel">
      {children}
    </div>
  );
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

export { Tabs };

// Usage
function App() {
  return (
    <Tabs defaultTab="overview">
      <Tabs.List>
        <Tabs.Tab value="overview">Overview</Tabs.Tab>
        <Tabs.Tab value="features">Features</Tabs.Tab>
        <Tabs.Tab value="pricing">Pricing</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panel value="overview">Overview content</Tabs.Panel>
      <Tabs.Panel value="features">Features content</Tabs.Panel>
      <Tabs.Panel value="pricing">Pricing content</Tabs.Panel>
    </Tabs>
  );
}
```

### Flexible Compound Component with Slot Pattern

```tsx
import { createContext, useContext, useState, ReactNode, isValidElement, Children, cloneElement } from 'react';

interface AccordionContextType {
  openItems: Set<string>;
  toggleItem: (id: string) => void;
  allowMultiple: boolean;
}

const AccordionContext = createContext<AccordionContextType | null>(null);

interface AccordionProps {
  children: ReactNode;
  allowMultiple?: boolean;
  defaultOpen?: string[];
}

function Accordion({ children, allowMultiple = false, defaultOpen = [] }: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set(defaultOpen));

  const toggleItem = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        if (!allowMultiple) next.clear();
        next.add(id);
      }
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggleItem, allowMultiple }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

interface AccordionItemProps {
  id: string;
  children: ReactNode;
}

function AccordionItem({ id, children }: AccordionItemProps) {
  const context = useContext(AccordionContext);
  if (!context) throw new Error('AccordionItem must be within Accordion');

  const isOpen = context.openItems.has(id);

  return (
    <div className={`accordion-item ${isOpen ? 'open' : ''}`} data-state={isOpen ? 'open' : 'closed'}>
      {Children.map(children, (child) => {
        if (isValidElement(child)) {
          return cloneElement(child as React.ReactElement<{ itemId?: string; isOpen?: boolean }>, {
            itemId: id,
            isOpen,
          });
        }
        return child;
      })}
    </div>
  );
}

interface AccordionTriggerProps {
  children: ReactNode;
  itemId?: string;
  isOpen?: boolean;
}

function AccordionTrigger({ children, itemId, isOpen }: AccordionTriggerProps) {
  const context = useContext(AccordionContext);
  if (!context || !itemId) return null;

  return (
    <button
      className="accordion-trigger"
      aria-expanded={isOpen}
      onClick={() => context.toggleItem(itemId)}
    >
      {children}
      <span className="icon">{isOpen ? '−' : '+'}</span>
    </button>
  );
}

interface AccordionContentProps {
  children: ReactNode;
  isOpen?: boolean;
}

function AccordionContent({ children, isOpen }: AccordionContentProps) {
  if (!isOpen) return null;

  return <div className="accordion-content">{children}</div>;
}

Accordion.Item = AccordionItem;
Accordion.Trigger = AccordionTrigger;
Accordion.Content = AccordionContent;

export { Accordion };
```

## Render Props Pattern

### Basic Render Props

```tsx
import { useState, ReactNode } from 'react';

interface ToggleRenderProps {
  on: boolean;
  toggle: () => void;
  setOn: (value: boolean) => void;
}

interface ToggleProps {
  defaultOn?: boolean;
  children: (props: ToggleRenderProps) => ReactNode;
}

function Toggle({ defaultOn = false, children }: ToggleProps) {
  const [on, setOn] = useState(defaultOn);

  const toggle = () => setOn((prev) => !prev);

  return <>{children({ on, toggle, setOn })}</>;
}

// Usage
function App() {
  return (
    <Toggle defaultOn={false}>
      {({ on, toggle }) => (
        <div>
          <p>The toggle is {on ? 'ON' : 'OFF'}</p>
          <button onClick={toggle}>Toggle</button>
        </div>
      )}
    </Toggle>
  );
}
```

### Mouse Position Tracker

```tsx
import { useState, useEffect, ReactNode } from 'react';

interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  children: (position: MousePosition) => ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{children(position)}</>;
}

// Usage
function App() {
  return (
    <MouseTracker>
      {({ x, y }) => (
        <div
          style={{
            position: 'absolute',
            left: x + 10,
            top: y + 10,
            background: 'black',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
          }}
        >
          {x}, {y}
        </div>
      )}
    </MouseTracker>
  );
}
```

### Data Fetching Render Props

```tsx
import { useState, useEffect, ReactNode } from 'react';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

interface FetchProps<T> {
  url: string;
  children: (state: FetchState<T>) => ReactNode;
}

function Fetch<T>({ url, children }: FetchProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [url]);

  return <>{children({ data, loading, error, refetch: fetchData })}</>;
}

// Usage
function UserList() {
  return (
    <Fetch<User[]> url="/api/users">
      {({ data, loading, error, refetch }) => {
        if (loading) return <p>Loading...</p>;
        if (error) return <p>Error: {error.message}</p>;

        return (
          <div>
            <button onClick={refetch}>Refresh</button>
            <ul>
              {data?.map((user) => (
                <li key={user.id}>{user.name}</li>
              ))}
            </ul>
          </div>
        );
      }}
    </Fetch>
  );
}
```

## Higher-Order Components (HOC)

### Basic HOC

```tsx
import { ComponentType } from 'react';

interface WithLoadingProps {
  isLoading: boolean;
}

function withLoading<P extends object>(
  WrappedComponent: ComponentType<P>
) {
  return function WithLoadingComponent(props: P & WithLoadingProps) {
    const { isLoading, ...rest } = props;

    if (isLoading) {
      return <div className="loading-spinner">Loading...</div>;
    }

    return <WrappedComponent {...(rest as P)} />;
  };
}

// Usage
interface UserListProps {
  users: User[];
}

function UserList({ users }: UserListProps) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

const UserListWithLoading = withLoading(UserList);

// In parent component
<UserListWithLoading isLoading={loading} users={users} />
```

### HOC with Injected Props

```tsx
import { ComponentType, useEffect, useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface WithUserProps {
  user: User | null;
  userLoading: boolean;
}

function withUser<P extends WithUserProps>(
  WrappedComponent: ComponentType<P>
) {
  return function WithUserComponent(
    props: Omit<P, keyof WithUserProps>
  ) {
    const [user, setUser] = useState<User | null>(null);
    const [userLoading, setUserLoading] = useState(true);

    useEffect(() => {
      fetch('/api/me')
        .then((res) => res.json())
        .then((data) => {
          setUser(data);
          setUserLoading(false);
        })
        .catch(() => setUserLoading(false));
    }, []);

    return (
      <WrappedComponent
        {...(props as P)}
        user={user}
        userLoading={userLoading}
      />
    );
  };
}

// Usage
interface ProfileProps extends WithUserProps {
  showAvatar?: boolean;
}

function Profile({ user, userLoading, showAvatar = true }: ProfileProps) {
  if (userLoading) return <div>Loading user...</div>;
  if (!user) return <div>Not logged in</div>;

  return (
    <div>
      {showAvatar && <img src={`/avatars/${user.id}`} alt="" />}
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

const ProfileWithUser = withUser(Profile);
```

### Composing Multiple HOCs

```tsx
import { ComponentType } from 'react';

// Utility for composing HOCs
function compose<P>(...hocs: Array<(c: ComponentType<any>) => ComponentType<any>>) {
  return (Component: ComponentType<P>) =>
    hocs.reduceRight((acc, hoc) => hoc(acc), Component);
}

// Usage
const EnhancedComponent = compose(
  withLoading,
  withUser,
  withTheme
)(BaseComponent);
```

## Custom Hooks as Patterns

### useToggle

```tsx
import { useState, useCallback } from 'react';

function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((v) => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse, setValue };
}

// Usage
function Modal() {
  const { value: isOpen, toggle, setFalse: close } = useToggle();

  return (
    <>
      <button onClick={toggle}>Open Modal</button>
      {isOpen && (
        <div className="modal">
          <button onClick={close}>Close</button>
        </div>
      )}
    </>
  );
}
```

### useDisclosure

```tsx
import { useState, useCallback } from 'react';

interface UseDisclosureReturn {
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
  onToggle: () => void;
  getDisclosureProps: () => { 'aria-expanded': boolean; 'aria-controls': string };
  getContentProps: () => { id: string; hidden: boolean };
}

function useDisclosure(
  id: string,
  { defaultOpen = false }: { defaultOpen?: boolean } = {}
): UseDisclosureReturn {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const onOpen = useCallback(() => setIsOpen(true), []);
  const onClose = useCallback(() => setIsOpen(false), []);
  const onToggle = useCallback(() => setIsOpen((prev) => !prev), []);

  const getDisclosureProps = useCallback(
    () => ({
      'aria-expanded': isOpen,
      'aria-controls': `${id}-content`,
    }),
    [isOpen, id]
  );

  const getContentProps = useCallback(
    () => ({
      id: `${id}-content`,
      hidden: !isOpen,
    }),
    [isOpen, id]
  );

  return {
    isOpen,
    onOpen,
    onClose,
    onToggle,
    getDisclosureProps,
    getContentProps,
  };
}
```

### useClickOutside

```tsx
import { useEffect, useRef, RefObject } from 'react';

function useClickOutside<T extends HTMLElement>(
  handler: () => void,
  events: Array<'mousedown' | 'mouseup' | 'touchstart' | 'touchend'> = ['mousedown', 'touchstart']
): RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const listener = (event: Event) => {
      const target = event.target as Node;
      if (!ref.current || ref.current.contains(target)) {
        return;
      }
      handler();
    };

    events.forEach((event) => document.addEventListener(event, listener));

    return () => {
      events.forEach((event) => document.removeEventListener(event, listener));
    };
  }, [handler, events]);

  return ref;
}

// Usage
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useClickOutside<HTMLDivElement>(() => setIsOpen(false));

  return (
    <div ref={ref}>
      <button onClick={() => setIsOpen(true)}>Open</button>
      {isOpen && <div className="dropdown-menu">Menu content</div>}
    </div>
  );
}
```

## Provider Pattern

### Context with Reducer

```tsx
import { createContext, useContext, useReducer, ReactNode, Dispatch } from 'react';

// Types
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' };

// Reducer
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find((item) => item.id === action.payload.id);

      if (existingItem) {
        const items = state.items.map((item) =>
          item.id === action.payload.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
        return { items, total: calculateTotal(items) };
      }

      const items = [...state.items, { ...action.payload, quantity: 1 }];
      return { items, total: calculateTotal(items) };
    }
    case 'REMOVE_ITEM': {
      const items = state.items.filter((item) => item.id !== action.payload);
      return { items, total: calculateTotal(items) };
    }
    case 'UPDATE_QUANTITY': {
      const items = state.items.map((item) =>
        item.id === action.payload.id
          ? { ...item, quantity: action.payload.quantity }
          : item
      );
      return { items, total: calculateTotal(items) };
    }
    case 'CLEAR_CART':
      return { items: [], total: 0 };
    default:
      return state;
  }
}

function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Context
interface CartContextType {
  state: CartState;
  dispatch: Dispatch<CartAction>;
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
}

const CartContext = createContext<CartContextType | null>(null);

// Provider
function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 });

  const addItem = (item: Omit<CartItem, 'quantity'>) => {
    dispatch({ type: 'ADD_ITEM', payload: item });
  };

  const removeItem = (id: string) => {
    dispatch({ type: 'REMOVE_ITEM', payload: id });
  };

  const updateQuantity = (id: string, quantity: number) => {
    dispatch({ type: 'UPDATE_QUANTITY', payload: { id, quantity } });
  };

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' });
  };

  return (
    <CartContext.Provider
      value={{ state, dispatch, addItem, removeItem, updateQuantity, clearCart }}
    >
      {children}
    </CartContext.Provider>
  );
}

// Hook
function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
}

export { CartProvider, useCart };
```

## Controlled vs Uncontrolled Components

### Controlled Input

```tsx
import { useState, ChangeEvent } from 'react';

function ControlledInput() {
  const [value, setValue] = useState('');

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  };

  return (
    <input
      type="text"
      value={value}
      onChange={handleChange}
      placeholder="Controlled input"
    />
  );
}
```

### Uncontrolled Input

```tsx
import { useRef, FormEvent } from 'react';

function UncontrolledInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    console.log('Value:', inputRef.current?.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} type="text" defaultValue="" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Hybrid Controlled/Uncontrolled Component

```tsx
import { useState, useCallback, ChangeEvent } from 'react';

interface InputProps {
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
}

function Input({ value: controlledValue, defaultValue = '', onChange }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue);

  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;

      if (!isControlled) {
        setInternalValue(newValue);
      }

      onChange?.(newValue);
    },
    [isControlled, onChange]
  );

  return <input type="text" value={value} onChange={handleChange} />;
}

// Usage - Controlled
function ControlledUsage() {
  const [value, setValue] = useState('');
  return <Input value={value} onChange={setValue} />;
}

// Usage - Uncontrolled
function UncontrolledUsage() {
  return <Input defaultValue="initial" onChange={console.log} />;
}
```

## Prop Getter Pattern

```tsx
import { useState, useCallback, HTMLAttributes, InputHTMLAttributes } from 'react';

interface UseSelectReturn<T> {
  selectedItem: T | null;
  isOpen: boolean;
  highlightedIndex: number;
  getToggleButtonProps: () => HTMLAttributes<HTMLButtonElement>;
  getMenuProps: () => HTMLAttributes<HTMLUListElement>;
  getItemProps: (options: { item: T; index: number }) => HTMLAttributes<HTMLLIElement>;
  getInputProps: () => InputHTMLAttributes<HTMLInputElement>;
}

function useSelect<T extends { id: string; label: string }>(
  items: T[]
): UseSelectReturn<T> {
  const [selectedItem, setSelectedItem] = useState<T | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);

  const getToggleButtonProps = useCallback(
    () => ({
      onClick: () => setIsOpen((prev) => !prev),
      'aria-haspopup': 'listbox' as const,
      'aria-expanded': isOpen,
    }),
    [isOpen]
  );

  const getMenuProps = useCallback(
    () => ({
      role: 'listbox' as const,
      'aria-activedescendant': highlightedIndex >= 0 ? items[highlightedIndex]?.id : undefined,
      hidden: !isOpen,
    }),
    [isOpen, highlightedIndex, items]
  );

  const getItemProps = useCallback(
    ({ item, index }: { item: T; index: number }) => ({
      role: 'option' as const,
      id: item.id,
      'aria-selected': selectedItem?.id === item.id,
      onClick: () => {
        setSelectedItem(item);
        setIsOpen(false);
      },
      onMouseEnter: () => setHighlightedIndex(index),
    }),
    [selectedItem]
  );

  const getInputProps = useCallback(
    () => ({
      value: selectedItem?.label || '',
      readOnly: true,
      onClick: () => setIsOpen(true),
    }),
    [selectedItem]
  );

  return {
    selectedItem,
    isOpen,
    highlightedIndex,
    getToggleButtonProps,
    getMenuProps,
    getItemProps,
    getInputProps,
  };
}

// Usage
function Select({ items }: { items: Array<{ id: string; label: string }> }) {
  const {
    selectedItem,
    isOpen,
    highlightedIndex,
    getToggleButtonProps,
    getMenuProps,
    getItemProps,
    getInputProps,
  } = useSelect(items);

  return (
    <div className="select">
      <input {...getInputProps()} placeholder="Select an item" />
      <button {...getToggleButtonProps()}>▼</button>
      <ul {...getMenuProps()}>
        {isOpen &&
          items.map((item, index) => (
            <li
              key={item.id}
              {...getItemProps({ item, index })}
              className={highlightedIndex === index ? 'highlighted' : ''}
            >
              {item.label}
            </li>
          ))}
      </ul>
    </div>
  );
}
```

## State Reducer Pattern

```tsx
import { useReducer, Reducer } from 'react';

// Types
type ToggleState = { on: boolean };
type ToggleAction = { type: 'toggle' } | { type: 'reset'; initialState: ToggleState };

// Default reducer
function toggleReducer(state: ToggleState, action: ToggleAction): ToggleState {
  switch (action.type) {
    case 'toggle':
      return { on: !state.on };
    case 'reset':
      return action.initialState;
    default:
      return state;
  }
}

interface UseToggleOptions {
  initialOn?: boolean;
  reducer?: Reducer<ToggleState, ToggleAction>;
}

function useToggleWithReducer({
  initialOn = false,
  reducer = toggleReducer,
}: UseToggleOptions = {}) {
  const initialState = { on: initialOn };
  const [state, dispatch] = useReducer(reducer, initialState);

  const toggle = () => dispatch({ type: 'toggle' });
  const reset = () => dispatch({ type: 'reset', initialState });

  return { ...state, toggle, reset, dispatch };
}

// Usage with custom reducer
function App() {
  const customReducer: Reducer<ToggleState, ToggleAction> = (state, action) => {
    // Custom logic: can only toggle if some condition
    if (action.type === 'toggle' && state.on) {
      // Prevent turning off
      return state;
    }
    return toggleReducer(state, action);
  };

  const { on, toggle } = useToggleWithReducer({ reducer: customReducer });

  return (
    <button onClick={toggle}>
      {on ? 'ON (cannot turn off)' : 'OFF'}
    </button>
  );
}
```

## Best Practices Summary

| Pattern | Use Case |
|---------|----------|
| Compound Components | Related components sharing implicit state |
| Render Props | Dynamic rendering with shared logic |
| HOC | Cross-cutting concerns, code reuse |
| Custom Hooks | Stateful logic reuse |
| Provider Pattern | Global/shared state management |
| Controlled/Uncontrolled | Form input flexibility |
| Prop Getters | Accessible component APIs |
| State Reducer | Customizable state logic |
