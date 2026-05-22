---
name: react-context-patterns
description: Use when React Context patterns for state management. Use when sharing state across component trees without prop drilling.
allowed-tools:
  - Bash
  - Read
---

# React Context Patterns

Master react context patterns for building high-performance, scalable
React applications with industry best practices.

## Understanding Prop Drilling vs Context

Prop drilling occurs when you pass props through multiple layers of components
that don't need them, just to reach a deeply nested component.

```typescript
// Prop Drilling (AVOID)
function App() {
  const [user, setUser] = useState<User | null>(null);
  return <Layout user={user} setUser={setUser} />;
}

function Layout({ user, setUser }: Props) {
  // Layout doesn't use user, just passes it down
  return <Sidebar user={user} setUser={setUser} />;
}

function Sidebar({ user, setUser }: Props) {
  // Sidebar doesn't use user, just passes it down
  return <UserMenu user={user} setUser={setUser} />;
}

function UserMenu({ user, setUser }: Props) {
  // Finally used here
  return <div>{user?.name}</div>;
}
```

Context solves this by providing a way to share values between components without
explicitly passing props through every level:

```typescript
// Using Context (BETTER)
const UserContext = createContext<UserContextType | undefined>(undefined);

function App() {
  const [user, setUser] = useState<User | null>(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout />
    </UserContext.Provider>
  );
}

function Layout() {
  return <Sidebar />; // No props needed
}

function Sidebar() {
  return <UserMenu />; // No props needed
}

function UserMenu() {
  const { user } = useContext(UserContext);
  return <div>{user?.name}</div>;
}
```

## Creating and Using Context with TypeScript

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const user = await api.login(email, password);
      setUser(user);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    api.clearSession();
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: user !== null,
    isLoading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

## Context with useReducer for Complex State

```typescript
import { createContext, useContext, useReducer, ReactNode } from 'react';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface State {
  items: CartItem[];
  total: number;
}

type Action =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' };

const CartContext = createContext<{
  state: State;
  dispatch: React.Dispatch<Action>;
} | undefined>(undefined);

function cartReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find(i => i.id === action.payload.id);
      if (existingItem) {
        return {
          items: state.items.map(i =>
            i.id === action.payload.id
              ? { ...i, quantity: i.quantity + action.payload.quantity }
              : i
          ),
          total: state.total + action.payload.price * action.payload.quantity
        };
      }
      return {
        items: [...state.items, action.payload],
        total: state.total + action.payload.price * action.payload.quantity
      };
    }
    case 'REMOVE_ITEM': {
      const item = state.items.find(i => i.id === action.payload);
      return {
        items: state.items.filter(i => i.id !== action.payload),
        total: state.total - (item ? item.price * item.quantity : 0)
      };
    }
    case 'UPDATE_QUANTITY': {
      const item = state.items.find(i => i.id === action.payload.id);
      if (!item) return state;
      const priceDiff = item.price * (action.payload.quantity - item.quantity);
      return {
        items: state.items.map(i =>
          i.id === action.payload.id
            ? { ...i, quantity: action.payload.quantity }
            : i
        ),
        total: state.total + priceDiff
      };
    }
    case 'CLEAR_CART':
      return { items: [], total: 0 };
    default:
      return state;
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    total: 0
  });

  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}

// Helper hook with actions
export function useCartActions() {
  const { dispatch } = useCart();

  return {
    addItem: (item: CartItem) => dispatch({ type: 'ADD_ITEM', payload: item }),
    removeItem: (id: string) => dispatch({ type: 'REMOVE_ITEM', payload: id }),
    updateQuantity: (id: string, quantity: number) =>
      dispatch({ type: 'UPDATE_QUANTITY', payload: { id, quantity } }),
    clearCart: () => dispatch({ type: 'CLEAR_CART' })
  };
}
```

## Multiple Context Composition

```typescript
import { ReactNode } from 'react';

// Compose multiple providers
export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        <CartProvider>
          <NotificationProvider>
            {children}
          </NotificationProvider>
        </CartProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

// Usage in main app
function App() {
  return (
    <AppProviders>
      <Router />
    </AppProviders>
  );
}
```

## Performance Optimization: Splitting Context

Split read and write operations to prevent unnecessary re-renders:

```typescript
import { createContext, useContext, useState, ReactNode, useMemo } from 'react';

// Separate read and write contexts
const UserStateContext = createContext<User | null>(null);
const UserDispatchContext = createContext<{
  setUser: (user: User | null) => void;
} | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Memoize dispatch to prevent re-renders
  const dispatch = useMemo(() => ({ setUser }), []);

  return (
    <UserStateContext.Provider value={user}>
      <UserDispatchContext.Provider value={dispatch}>
        {children}
      </UserDispatchContext.Provider>
    </UserStateContext.Provider>
  );
}

// Components only re-render when they use state that changes
export function useUser() {
  const context = useContext(UserStateContext);
  return context; // Can be null
}

export function useUserDispatch() {
  const context = useContext(UserDispatchContext);
  if (!context) {
    throw new Error('useUserDispatch must be used within UserProvider');
  }
  return context;
}
```

## Context with useMemo for Value Stability

```typescript
import { createContext, useContext, useState, ReactNode, useMemo } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  primaryColor: string;
  secondaryColor: string;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  // Memoize value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    theme,
    toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light'),
    primaryColor: theme === 'light' ? '#000000' : '#ffffff',
    secondaryColor: theme === 'light' ? '#666666' : '#cccccc'
  }), [theme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

## Context with Local Storage Persistence

```typescript
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface Settings {
  notifications: boolean;
  language: string;
  timezone: string;
}

const SettingsContext = createContext<{
  settings: Settings;
  updateSettings: (updates: Partial<Settings>) => void;
} | undefined>(undefined);

const defaultSettings: Settings = {
  notifications: true,
  language: 'en',
  timezone: 'UTC'
};

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<Settings>(() => {
    // Initialize from localStorage
    const stored = localStorage.getItem('settings');
    return stored ? JSON.parse(stored) : defaultSettings;
  });

  // Persist to localStorage on change
  useEffect(() => {
    localStorage.setItem('settings', JSON.stringify(settings));
  }, [settings]);

  const updateSettings = (updates: Partial<Settings>) => {
    setSettings(prev => ({ ...prev, ...updates }));
  };

  const value = { settings, updateSettings };

  return (
    <SettingsContext.Provider value={value}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
}
```

## Context for Feature Flags

```typescript
import { createContext, useContext, ReactNode } from 'react';

interface FeatureFlags {
  newDashboard: boolean;
  betaFeatures: boolean;
  experimentalUI: boolean;
}

const FeatureFlagsContext = createContext<FeatureFlags | undefined>(undefined);

export function FeatureFlagsProvider({
  children,
  flags
}: {
  children: ReactNode;
  flags: FeatureFlags;
}) {
  return (
    <FeatureFlagsContext.Provider value={flags}>
      {children}
    </FeatureFlagsContext.Provider>
  );
}

export function useFeatureFlags() {
  const context = useContext(FeatureFlagsContext);
  if (!context) {
    throw new Error('useFeatureFlags must be used within FeatureFlagsProvider');
  }
  return context;
}

export function useFeatureFlag(flag: keyof FeatureFlags): boolean {
  const flags = useFeatureFlags();
  return flags[flag];
}

// Usage
function App() {
  const flags = fetchFeatureFlags(); // From API or config
  return (
    <FeatureFlagsProvider flags={flags}>
      <Router />
    </FeatureFlagsProvider>
  );
}

function Dashboard() {
  const newDashboard = useFeatureFlag('newDashboard');
  return newDashboard ? <NewDashboard /> : <OldDashboard />;
}
```

## Context for Notifications/Toast System

```typescript
import { createContext, useContext, useState, ReactNode, useCallback } from 'react';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(
  undefined
);

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback(
    (notification: Omit<Notification, 'id'>) => {
      const id = Math.random().toString(36).substr(2, 9);
      const newNotification = { ...notification, id };

      setNotifications(prev => [...prev, newNotification]);

      // Auto-remove after duration
      if (notification.duration !== 0) {
        setTimeout(() => {
          removeNotification(id);
        }, notification.duration || 5000);
      }
    },
    []
  );

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const value = { notifications, addNotification, removeNotification };

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <NotificationContainer />
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider');
  }
  return context;
}

function NotificationContainer() {
  const { notifications, removeNotification } = useNotifications();

  return (
    <div className="notification-container">
      {notifications.map(notification => (
        <div
          key={notification.id}
          className={`notification notification-${notification.type}`}
          onClick={() => removeNotification(notification.id)}
        >
          {notification.message}
        </div>
      ))}
    </div>
  );
}
```

## Context for Modal Management

```typescript
import { createContext, useContext, useState, ReactNode, useCallback } from 'react';

interface ModalContextType {
  isOpen: boolean;
  modalContent: ReactNode | null;
  openModal: (content: ReactNode) => void;
  closeModal: () => void;
}

const ModalContext = createContext<ModalContextType | undefined>(undefined);

export function ModalProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [modalContent, setModalContent] = useState<ReactNode | null>(null);

  const openModal = useCallback((content: ReactNode) => {
    setModalContent(content);
    setIsOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setIsOpen(false);
    // Delay clearing content for animation
    setTimeout(() => setModalContent(null), 300);
  }, []);

  const value = { isOpen, modalContent, openModal, closeModal };

  return (
    <ModalContext.Provider value={value}>
      {children}
      {isOpen && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            {modalContent}
            <button onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </ModalContext.Provider>
  );
}

export function useModal() {
  const context = useContext(ModalContext);
  if (!context) {
    throw new Error('useModal must be used within ModalProvider');
  }
  return context;
}

// Usage
function UserProfile() {
  const { openModal } = useModal();

  const handleEditProfile = () => {
    openModal(<EditProfileForm />);
  };

  return <button onClick={handleEditProfile}>Edit Profile</button>;
}
```

## Context for Form State Management

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

interface FormData {
  [key: string]: any;
}

interface FormContextType {
  formData: FormData;
  errors: Record<string, string>;
  setFieldValue: (field: string, value: any) => void;
  setFieldError: (field: string, error: string) => void;
  clearErrors: () => void;
  resetForm: () => void;
}

const FormContext = createContext<FormContextType | undefined>(undefined);

export function FormProvider({
  children,
  initialValues = {}
}: {
  children: ReactNode;
  initialValues?: FormData;
}) {
  const [formData, setFormData] = useState<FormData>(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const setFieldValue = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when field is modified
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const setFieldError = (field: string, error: string) => {
    setErrors(prev => ({ ...prev, [field]: error }));
  };

  const clearErrors = () => setErrors({});

  const resetForm = () => {
    setFormData(initialValues);
    setErrors({});
  };

  const value = {
    formData,
    errors,
    setFieldValue,
    setFieldError,
    clearErrors,
    resetForm
  };

  return <FormContext.Provider value={value}>{children}</FormContext.Provider>;
}

export function useForm() {
  const context = useContext(FormContext);
  if (!context) {
    throw new Error('useForm must be used within FormProvider');
  }
  return context;
}

// Usage
function LoginForm() {
  return (
    <FormProvider initialValues={{ email: '', password: '' }}>
      <Form />
    </FormProvider>
  );
}

function Form() {
  const { formData, errors, setFieldValue } = useForm();

  return (
    <form>
      <input
        type="email"
        value={formData.email}
        onChange={e => setFieldValue('email', e.target.value)}
      />
      {errors.email && <span>{errors.email}</span>}

      <input
        type="password"
        value={formData.password}
        onChange={e => setFieldValue('password', e.target.value)}
      />
      {errors.password && <span>{errors.password}</span>}
    </form>
  );
}
```

## Testing Context Providers

```typescript
import { render, screen } from '@testing-library/react';
import { AuthProvider, useAuth } from './AuthContext';

function TestComponent() {
  const { user, isAuthenticated } = useAuth();
  return (
    <div>
      <div data-testid="authenticated">{isAuthenticated.toString()}</div>
      <div data-testid="user">{user?.name || 'None'}</div>
    </div>
  );
}

describe('AuthProvider', () => {
  it('provides authentication state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('authenticated')).toHaveTextContent('false');
    expect(screen.getByTestId('user')).toHaveTextContent('None');
  });

  it('throws error when used outside provider', () => {
    // Suppress console.error for this test
    const spy = jest.spyOn(console, 'error').mockImplementation();

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useAuth must be used within AuthProvider');

    spy.mockRestore();
  });
});
```

## When to Use This Skill

Use react-context-patterns when you need to:

- Share state across many components without prop drilling
- Implement global application state (auth, theme, etc.)
- Build provider patterns for complex features
- Create compound components with shared state
- Manage deeply nested component communication
- Implement feature-specific state management
- Build scalable React applications
- Avoid excessive prop passing
- Create reusable context patterns
- Manage cross-cutting concerns (notifications, modals, etc.)

## Best Practices

1. **Split contexts by concern** - Create separate contexts for auth, theme,
   cart, etc. Don't combine unrelated state.

2. **Memoize context values** - Use `useMemo` to prevent unnecessary re-renders
   when the provider re-renders.

3. **Provide custom hooks** - Always create a custom hook like `useAuth()`
   instead of exposing `useContext()` directly.

4. **Throw errors outside provider** - Ensure context is used within the correct
   provider boundary.

5. **Use TypeScript** - Define proper types for context values to catch errors
   at compile time.

6. **Keep values stable** - Avoid creating new objects/functions on every render.
   Use `useMemo` and `useCallback`.

7. **Split read and write contexts** - For performance-critical applications,
   separate state and dispatch contexts.

8. **Document context usage** - Clearly document what each context provides and
   when to use it.

9. **Test thoroughly** - Write tests for providers, custom hooks, and error cases.

10. **Consider alternatives** - Don't use Context for everything. Local state,
    prop passing, or state management libraries might be better for some cases.

## Common Pitfalls

1. **Creating too many contexts** - Context hell is as bad as prop drilling.
   Group related state together.

2. **Not memoizing values** - Every provider re-render causes all consumers to
   re-render if values aren't memoized.

3. **Using context for all state** - Local state is simpler and more performant
   for component-specific state.

4. **Forgetting error boundaries** - Always check if context exists in custom
   hooks to provide helpful error messages.

5. **Not providing defaults** - Always handle the undefined case when context
   might not be available.

6. **Overusing for performance** - Context causes all consumers to re-render.
   For frequently changing values, consider alternatives.

7. **Not splitting operations** - Separating read and write can significantly
   improve performance.

8. **Creating unstable values** - Defining objects or functions inline in the
   provider causes unnecessary re-renders.

9. **Using for high-frequency updates** - Context isn't optimized for values
   that change many times per second.

10. **Not considering composition** - Sometimes lifting state up or using
    composition patterns is simpler than context.

## Resources

- [React Documentation - Context](https://react.dev/learn/passing-data-deeply-with-context)
- [React Performance Guide](https://react.dev/learn/render-and-commit)
- [React Patterns](https://reactpatterns.com/)
- [Kent C. Dodds - Application State Management](https://kentcdodds.com/blog/application-state-management-with-react)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
