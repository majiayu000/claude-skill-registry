---
name: react-code-review
description: Master React code review patterns including hooks rules, useEffect dependencies, state management, performance optimization, and component design. Use PROACTIVELY when reviewing React PRs.
---

# React Code Review

Comprehensive code review checklist and patterns for React applications, focusing on hooks, state management, performance, and component design.

## When to Use This Skill

- Reviewing React pull requests
- Establishing React code review standards
- Training reviewers on React-specific issues
- Catching hooks violations and performance issues
- Ensuring proper component architecture

## Quick Checklist

```markdown
## React Review Checklist

- [ ] Hooks at top level (not in conditions/loops)
- [ ] useEffect has correct dependencies
- [ ] useEffect cleanups for subscriptions/timers
- [ ] Keys are stable, not array indices
- [ ] Props not mutated
- [ ] Expensive computations memoized (useMemo/useCallback)
- [ ] Components are small and focused
- [ ] No state updates during render
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Hooks Rules

### Hooks Inside Conditions

```tsx
// ❌ Hook inside condition - violates Rules of Hooks
function UserProfile({ userId }: Props) {
  if (!userId) {
    return null; // Early return before hook!
  }
  const [user, setUser] = useState<User | null>(null); // Conditional hook!

  // ...
}

// ✅ Hooks must be at top level, before any conditions
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);

  if (!userId) {
    return null; // Early return after hooks
  }

  // ...
}
```

### Hooks Inside Loops

```tsx
// ❌ Hook inside loop - violates Rules of Hooks
function UserList({ userIds }: Props) {
  return (
    <div>
      {userIds.map((id) => {
        const user = useUser(id); // WRONG! Hook in loop!
        return <UserCard key={id} user={user} />;
      })}
    </div>
  );
}

// ✅ Move hook to child component
function UserList({ userIds }: Props) {
  return (
    <div>
      {userIds.map((id) => (
        <UserCardLoader key={id} userId={id} />
      ))}
    </div>
  );
}

function UserCardLoader({ userId }: { userId: string }) {
  const user = useUser(userId); // Correct! Top level of component
  return <UserCard user={user} />;
}
```

### Hooks Inside Callbacks

```tsx
// ❌ Hook inside callback
function SearchForm() {
  const handleSubmit = () => {
    const [results, setResults] = useState([]); // WRONG!
  };
}

// ✅ Hooks at component top level
function SearchForm() {
  const [results, setResults] = useState([]);

  const handleSubmit = () => {
    // Use setResults here
  };
}
```

---

## useEffect Dependencies

### Missing Dependencies

```tsx
// ❌ Missing dependency - stale closure bug
function SearchResults({ query }: Props) {
  const [results, setResults] = useState<Item[]>([]);

  useEffect(() => {
    fetchResults(query).then(setResults);
  }, []); // Missing 'query' dependency! Uses stale query value
}

// ✅ Complete dependencies
function SearchResults({ query }: Props) {
  const [results, setResults] = useState<Item[]>([]);

  useEffect(() => {
    let cancelled = false;

    fetchResults(query).then((data) => {
      if (!cancelled) setResults(data);
    });

    return () => {
      cancelled = true;
    };
  }, [query]); // Includes query
}
```

### Object/Function Dependencies

```tsx
// ❌ Object recreated every render - infinite loop!
function UserList({ filter }: Props) {
  const options = { filter, limit: 10 }; // New object every render!

  useEffect(() => {
    fetchUsers(options);
  }, [options]); // Changes every render!
}

// ✅ Use primitive dependencies
function UserList({ filter }: Props) {
  useEffect(() => {
    fetchUsers({ filter, limit: 10 });
  }, [filter]); // Primitive value, stable reference
}

// ✅ Or memoize the object
function UserList({ filter }: Props) {
  const options = useMemo(() => ({ filter, limit: 10 }), [filter]);

  useEffect(() => {
    fetchUsers(options);
  }, [options]);
}
```

### Function Dependencies

```tsx
// ❌ Function changes every render
function DataFetcher({ userId }: Props) {
  const fetchData = () => {
    return api.getUser(userId);
  };

  useEffect(() => {
    fetchData().then(setUser);
  }, [fetchData]); // fetchData changes every render!
}

// ✅ useCallback for stable function reference
function DataFetcher({ userId }: Props) {
  const fetchData = useCallback(() => {
    return api.getUser(userId);
  }, [userId]);

  useEffect(() => {
    fetchData().then(setUser);
  }, [fetchData]);
}

// ✅ Or move function inside useEffect
function DataFetcher({ userId }: Props) {
  useEffect(() => {
    const fetchData = () => api.getUser(userId);
    fetchData().then(setUser);
  }, [userId]);
}
```

---

## useEffect Cleanup

### Missing Cleanup for Timers

```tsx
// ❌ No cleanup - timer runs after unmount, memory leak
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount((c) => c + 1);
    }, 1000);
    // Missing cleanup! Timer continues after unmount
  }, []);
}

// ✅ Proper cleanup
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount((c) => c + 1);
    }, 1000);

    return () => clearInterval(id); // Cleanup on unmount
  }, []);
}
```

### Missing Cleanup for Subscriptions

```tsx
// ❌ Subscription without cleanup - memory leak
function useWebSocket(url: string) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (e) => setData(JSON.parse(e.data));
    // WebSocket stays open after unmount!
  }, [url]);
}

// ✅ Close on cleanup
function useWebSocket(url: string) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (e) => setData(JSON.parse(e.data));

    return () => ws.close(); // Close connection on unmount
  }, [url]);
}
```

### Missing Cleanup for Fetch

```tsx
// ❌ State update after unmount - memory leak warning
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
    // If unmounted before fetch completes, tries to update unmounted component!
  }, [userId]);
}

// ✅ Cancel pending operations
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    fetchUser(userId, { signal: controller.signal })
      .then(setUser)
      .catch((e) => {
        if (e.name !== "AbortError") throw e;
      });

    return () => controller.abort();
  }, [userId]);
}
```

---

## Keys

### Using Array Index as Key

```tsx
// ❌ Using array index as key - bugs when list changes
function TodoList({ todos }: Props) {
  return (
    <ul>
      {todos.map((todo, index) => (
        <TodoItem key={index} todo={todo} /> // Wrong!
      ))}
    </ul>
  );
}
// If items reorder, React reuses wrong components!

// ✅ Use stable unique identifier
function TodoList({ todos }: Props) {
  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </ul>
  );
}
```

### Missing Keys

```tsx
// ❌ No key at all - React will warn
function ItemList({ items }: Props) {
  return (
    <>
      {items.map((item) => (
        <ItemCard item={item} /> // Missing key!
      ))}
    </>
  );
}

// ✅ Always provide keys for lists
function ItemList({ items }: Props) {
  return (
    <>
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </>
  );
}
```

### Keys Must Be Stable

```tsx
// ❌ Random key - defeats purpose of keys
function ItemList({ items }: Props) {
  return (
    <>
      {items.map((item) => (
        <ItemCard key={Math.random()} item={item} /> // Wrong!
      ))}
    </>
  );
}

// ❌ Unstable compound key
function ItemList({ items }: Props) {
  return (
    <>
      {items.map((item) => (
        <ItemCard key={`${item.name}-${Date.now()}`} item={item} />
      ))}
    </>
  );
}

// ✅ Stable unique identifier
function ItemList({ items }: Props) {
  return (
    <>
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </>
  );
}
```

---

## State Management

### State Updates During Render

```tsx
// ❌ Setting state during render - infinite loop!
function Counter({ value }: Props) {
  const [displayValue, setDisplayValue] = useState(value);

  if (value !== displayValue) {
    setDisplayValue(value); // Setting state during render!
  }

  return <div>{displayValue}</div>;
}

// ✅ Use the prop directly or compute during render
function Counter({ value }: Props) {
  // If transformation needed, compute it
  const displayValue = formatNumber(value);

  return <div>{displayValue}</div>;
}

// ✅ Or use useEffect for derived state that needs syncing
function Counter({ value }: Props) {
  const [displayValue, setDisplayValue] = useState(value);

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  return <div>{displayValue}</div>;
}
```

### Prop Mutation

```tsx
// ❌ Mutating props - breaks React's data flow
function UserProfile({ user }: Props) {
  const handleUpdate = () => {
    user.lastViewed = new Date(); // Mutating prop!
  };

  return <div onClick={handleUpdate}>{user.name}</div>;
}

// ✅ Lift state up or use callback
function UserProfile({ user, onView }: Props) {
  const handleUpdate = () => {
    onView(user.id); // Parent handles the update
  };

  return <div onClick={handleUpdate}>{user.name}</div>;
}
```

### Unnecessary State

```tsx
// ❌ Derived state stored in useState
function UserList({ users }: Props) {
  const [filteredUsers, setFilteredUsers] = useState(
    users.filter((u) => u.active),
  );

  useEffect(() => {
    setFilteredUsers(users.filter((u) => u.active));
  }, [users]);

  return <List users={filteredUsers} />;
}

// ✅ Compute during render (or useMemo if expensive)
function UserList({ users }: Props) {
  const filteredUsers = users.filter((u) => u.active);
  // Or with memoization:
  // const filteredUsers = useMemo(
  //     () => users.filter(u => u.active),
  //     [users]
  // );

  return <List users={filteredUsers} />;
}
```

---

## Performance

### Expensive Computations

```tsx
// ❌ Expensive computation every render
function ProductList({ products }: Props) {
  const sortedProducts = products
    .filter((p) => p.inStock)
    .sort((a, b) => b.rating - a.rating); // Every render!

  return <List items={sortedProducts} />;
}

// ✅ Memoize expensive computations
function ProductList({ products }: Props) {
  const sortedProducts = useMemo(() => {
    return products
      .filter((p) => p.inStock)
      .sort((a, b) => b.rating - a.rating);
  }, [products]);

  return <List items={sortedProducts} />;
}
```

### Inline Functions Causing Re-renders

```tsx
// ❌ Inline function causes child re-renders
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <span>{count}</span>
      <Child onClick={() => console.log("click")} />
      {/* New function every render, Child re-renders! */}
    </div>
  );
}

// ✅ useCallback for stable function reference
function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log("click");
  }, []);

  return (
    <div>
      <span>{count}</span>
      <Child onClick={handleClick} />
    </div>
  );
}
```

### Missing React.memo

```tsx
// ❌ Child re-renders even when its props don't change
function ExpensiveList({ items }: Props) {
  return (
    <ul>
      {items.map((item) => (
        <ExpensiveListItem key={item.id} item={item} />
      ))}
    </ul>
  );
}

// Parent re-renders = all ExpensiveListItems re-render

// ✅ Memoize components that are expensive to render
const ExpensiveListItem = React.memo(function ExpensiveListItem({
  item,
}: Props) {
  return <li>{/* expensive rendering */}</li>;
});

// Now only re-renders if item prop changes
```

### Over-Memoization

```tsx
// ❌ Unnecessary memoization - simple computation
function Greeting({ name }: Props) {
  const greeting = useMemo(() => `Hello, ${name}!`, [name]); // Overkill!

  return <div>{greeting}</div>;
}

// ✅ Just compute it
function Greeting({ name }: Props) {
  const greeting = `Hello, ${name}!`;

  return <div>{greeting}</div>;
}

// Only memoize when:
// 1. Computation is expensive (sorting, filtering large arrays)
// 2. Reference equality matters (passing to memoized children)
```

---

## Component Design

### Giant Components

```tsx
// ❌ Component does too much
function UserDashboard({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [followers, setFollowers] = useState<User[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  // 200 lines of hooks, handlers, and rendering...

  return (
    <div>
      {/* Header */}
      {/* Profile */}
      {/* Edit Form */}
      {/* Posts List */}
      {/* Followers Grid */}
      {/* Settings */}
    </div>
  );
}

// ✅ Split into focused components
function UserDashboard({ userId }: Props) {
  return (
    <div>
      <UserHeader userId={userId} />
      <UserProfile userId={userId} />
      <UserPosts userId={userId} />
      <UserFollowers userId={userId} />
    </div>
  );
}
```

### Prop Drilling

```tsx
// ❌ Props passed through many levels
function App() {
  const [user, setUser] = useState<User | null>(null);

  return (
    <Layout user={user} setUser={setUser}>
      <Sidebar user={user} setUser={setUser}>
        <Navigation user={user} setUser={setUser}>
          <UserMenu user={user} setUser={setUser} />
        </Navigation>
      </Sidebar>
    </Layout>
  );
}

// ✅ Use Context for deeply-nested state
const UserContext = createContext<UserContextType | null>(null);

function App() {
  const [user, setUser] = useState<User | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout>
        <Sidebar>
          <Navigation>
            <UserMenu />
          </Navigation>
        </Sidebar>
      </Layout>
    </UserContext.Provider>
  );
}

function UserMenu() {
  const { user, setUser } = useContext(UserContext)!;
  // ...
}
```

---

## Common Pitfalls

| Pitfall             | Problem                  | Solution                |
| ------------------- | ------------------------ | ----------------------- |
| Conditional hooks   | Violates Rules of Hooks  | Hooks at top level only |
| Missing deps        | Stale closures           | Include all deps        |
| No cleanup          | Memory leaks             | Return cleanup function |
| Index as key        | Wrong updates on reorder | Use stable unique id    |
| Prop mutation       | Breaks data flow         | Lift state up           |
| State during render | Infinite loop            | Use useEffect           |

## Best Practices Summary

1. **Hooks at top level** - Never in conditions, loops, callbacks
2. **Complete dependencies** - ESLint exhaustive-deps rule
3. **Always cleanup** - Timers, subscriptions, fetch
4. **Stable keys** - Unique IDs, not indices
5. **Don't mutate props** - Lift state up instead
6. **Memoize wisely** - Only expensive computations
7. **Small components** - Single responsibility
8. **Context for deep props** - Avoid prop drilling


## Parent Hub
- [_frontend-mastery](../_frontend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
