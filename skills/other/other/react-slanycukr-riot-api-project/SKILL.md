---
name: React 19
description: Modern React development with React 19 features, hooks, components, and server-side capabilities
when_to_use: When building React applications, creating components, managing state, or implementing React 19 specific features like server components and form actions
---

# React 19 Development

React 19 introduces powerful new features for building modern web applications with enhanced server capabilities, improved form handling, and better performance.

## Quick Start

### Basic Component with Hooks

```jsx
import { useState, useEffect } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log("Count changed:", count);
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

### Custom Hook for API Data

```jsx
import { useState, useEffect } from "react";

function useApiData(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }) {
  const { data: user, loading, error } = useApiData(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user found</div>;

  return <div>{user.name}</div>;
}
```

## React 19 New Features

### Server Actions and Forms

```jsx
// Server action
"use server";
async function updateUser(formData) {
  const name = formData.get("name");
  const email = formData.get("email");

  // Database update logic here
  await db.users.update({ name, email });

  return { success: true, message: "User updated successfully" };
}

// Client component with form
function UserForm({ user }) {
  const [state, formAction, isPending] = useActionState(updateUser, null);

  return (
    <form action={formAction}>
      <input name="name" defaultValue={user.name} />
      <input name="email" defaultValue={user.email} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Updating..." : "Update"}
      </button>
      {state?.message && <p>{state.message}</p>}
    </form>
  );
}
```

### Form Status Hook

```jsx
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
}

function ContactForm() {
  return (
    <form action={submitContact}>
      <input name="name" placeholder="Your name" />
      <input name="email" placeholder="Your email" />
      <SubmitButton />
    </form>
  );
}
```

### Server Components

```jsx
// Server Component (runs on server)
async function BlogPost({ id }) {
  const post = await db.posts.find(id);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      <CommentSection postId={post.id} />
    </article>
  );
}

// Client Component for interactivity
("use client");
function CommentSection({ postId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  const addComment = async () => {
    // Client-side logic for adding comments
  };

  return (
    <div>
      <h3>Comments</h3>
      {/* Comment rendering and form */}
    </div>
  );
}
```

## Common Patterns

### State Management with Context

```jsx
import { createContext, useContext, useState, useReducer } from "react";

// Create context
const AuthContext = createContext();

// Auth provider component
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (credentials) => {
    // Login logic
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for consuming context
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

// Usage in components
function Header() {
  const { user, logout } = useAuth();

  return (
    <header>
      {user ? (
        <div>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <div>Please log in</div>
      )}
    </header>
  );
}
```

### Data Fetching with Suspense

```jsx
import { Suspense } from "react";

// Async component
async function UserList() {
  const users = await fetchUsers(); // async function

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// Using Suspense boundary
function App() {
  return (
    <div>
      <h1>Users</h1>
      <Suspense fallback={<div>Loading users...</div>}>
        <UserList />
      </Suspense>
    </div>
  );
}
```

### Optimistic Updates

```jsx
import { useState, useTransition } from "react";

function TodoList() {
  const [todos, setTodos] = useState(initialTodos);
  const [isPending, startTransition] = useTransition();

  const addTodo = async (newTodo) => {
    // Optimistic update
    const optimisticId = Date.now();
    startTransition(() => {
      setTodos((prev) => [
        ...prev,
        {
          id: optimisticId,
          text: newTodo,
          status: "optimistic",
        },
      ]);
    });

    try {
      const savedTodo = await saveTodo(newTodo);
      // Replace optimistic todo with saved one
      setTodos((prev) =>
        prev.map((todo) => (todo.id === optimisticId ? savedTodo : todo)),
      );
    } catch (error) {
      // Revert optimistic update on error
      setTodos((prev) => prev.filter((todo) => todo.id !== optimisticId));
    }
  };

  return (
    <div>
      <ul>
        {todos.map((todo) => (
          <li
            key={todo.id}
            style={{ opacity: todo.status === "optimistic" ? 0.5 : 1 }}
          >
            {todo.text}
          </li>
        ))}
      </ul>
      <button onClick={() => addTodo("New task")} disabled={isPending}>
        Add Todo
      </button>
    </div>
  );
}
```

### Error Boundaries

```jsx
import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong</h2>
          <details>{this.state.error?.message}</details>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

## Performance Patterns

### Memoization with useMemo and useCallback

```jsx
import { useState, useMemo, useCallback } from "react";

function ExpensiveComponent({ data, onItemClick }) {
  const [filter, setFilter] = useState("");

  // Memoize expensive computation
  const filteredData = useMemo(() => {
    console.log("Filtering data...");
    return data.filter((item) =>
      item.name.toLowerCase().includes(filter.toLowerCase()),
    );
  }, [data, filter]);

  // Memoize event handler
  const handleItemClick = useCallback(
    (item) => {
      onItemClick(item);
    },
    [onItemClick],
  );

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter items..."
      />
      <ul>
        {filteredData.map((item) => (
          <li key={item.id} onClick={() => handleItemClick(item)}>
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Code Splitting with lazy loading

```jsx
import { lazy, Suspense } from "react";

// Lazy load component
const AdminDashboard = lazy(() => import("./AdminDashboard"));

function App() {
  const [isAdmin, setIsAdmin] = useState(false);

  return (
    <div>
      <h1>My App</h1>
      <button onClick={() => setIsAdmin(true)}>Admin View</button>

      {isAdmin && (
        <Suspense fallback={<div>Loading admin dashboard...</div>}>
          <AdminDashboard />
        </Suspense>
      )}
    </div>
  );
}
```

## Best Practices

### Component Structure

```jsx
// Good: Single responsibility components
function UserAvatar({ user, size = "medium" }) {
  return (
    <img
      src={user.avatar}
      alt={user.name}
      className={`avatar avatar-${size}`}
    />
  );
}

function UserCard({ user }) {
  return (
    <div className="user-card">
      <UserAvatar user={user} size="large" />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

### Prop Types and Default Values

```jsx
import PropTypes from "prop-types";

function Button({
  children,
  variant = "primary",
  size = "medium",
  onClick,
  disabled = false,
}) {
  const className = `btn btn-${variant} btn-${size}`;

  return (
    <button className={className} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(["primary", "secondary", "danger"]),
  size: PropTypes.oneOf(["small", "medium", "large"]),
  onClick: PropTypes.func,
  disabled: PropTypes.bool,
};
```

## Requirements

- React 19.0 or higher
- Node.js 18+ (for development)
- Modern browser with ES6+ support

### Dependencies for Full React 19 Experience

```bash
npm install react@19 react-dom@19
```

### Recommended Development Tools

```bash
npm install --save-dev @types/react @types/react-dom
```

### Common Additional Libraries

- **State Management**: `zustand`, `jotai`, or Context API
- **Routing**: `react-router-dom`
- **Data Fetching**: `@tanstack/react-query`
- **Form Handling**: Built-in React 19 forms or `react-hook-form`
- **Styling**: `tailwindcss`, `styled-components`, or CSS modules
