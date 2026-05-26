---
name: react-hooks-best-practices
description: Provides React patterns for hooks, effects, refs, and component design. Covers escape hatches, anti-patterns, and correct effect usage. Use when reading or writing React components with hooks or effects.
---

# React Hooks Best Practices

## Pair with TypeScript

When working with React, always load both this skill and `typescript-best-practices` together. TypeScript patterns (type-first development, discriminated unions, Zod validation) apply to React code.

## Core Principle: Effects Are Escape Hatches

Effects let you "step outside" React to synchronize with external systems. **Most component logic should NOT use Effects.** Before writing an Effect, ask: "Is there a way to do this without an Effect?"

## When to Use Effects

Effects are for synchronizing with **external systems**:
- Subscribing to browser APIs (WebSocket, IntersectionObserver, resize)
- Connecting to third-party libraries not written in React
- Setting up/cleaning up event listeners on window/document
- Fetching data on mount (though prefer React Query or framework data fetching)
- Controlling non-React DOM elements (video players, maps, modals)

## When NOT to Use Effects

### Derived State (Calculate During Render)

```tsx
// BAD: Effect for derived state
const [firstName, setFirstName] = useState('Taylor');
const [lastName, setLastName] = useState('Swift');
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(firstName + ' ' + lastName);
}, [firstName, lastName]);

// GOOD: Calculate during render
const [firstName, setFirstName] = useState('Taylor');
const [lastName, setLastName] = useState('Swift');
const fullName = firstName + ' ' + lastName;
```

### Expensive Calculations (Use useMemo)

```tsx
// BAD: Effect for caching
const [visibleTodos, setVisibleTodos] = useState([]);
useEffect(() => {
  setVisibleTodos(getFilteredTodos(todos, filter));
}, [todos, filter]);

// GOOD: useMemo for expensive calculations
const visibleTodos = useMemo(
  () => getFilteredTodos(todos, filter),
  [todos, filter]
);
```

### Resetting State on Prop Change (Use key)

```tsx
// BAD: Effect to reset state
function ProfilePage({ userId }) {
  const [comment, setComment] = useState('');
  useEffect(() => {
    setComment('');
  }, [userId]);
  // ...
}

// GOOD: Use key to reset component state
function ProfilePage({ userId }) {
  return <Profile userId={userId} key={userId} />;
}

function Profile({ userId }) {
  const [comment, setComment] = useState(''); // Resets automatically
  // ...
}
```

### User Event Handling (Use Event Handlers)

```tsx
// BAD: Event-specific logic in Effect
function ProductPage({ product, addToCart }) {
  useEffect(() => {
    if (product.isInCart) {
      showNotification(`Added ${product.name} to cart`);
    }
  }, [product]);
  // ...
}

// GOOD: Logic in event handler
function ProductPage({ product, addToCart }) {
  function buyProduct() {
    addToCart(product);
    showNotification(`Added ${product.name} to cart`);
  }
  // ...
}
```

### Notifying Parent of State Changes

```tsx
// BAD: Effect to notify parent
function Toggle({ onChange }) {
  const [isOn, setIsOn] = useState(false);
  useEffect(() => {
    onChange(isOn);
  }, [isOn, onChange]);
  // ...
}

// GOOD: Update both in event handler
function Toggle({ onChange }) {
  const [isOn, setIsOn] = useState(false);
  function updateToggle(nextIsOn) {
    setIsOn(nextIsOn);
    onChange(nextIsOn);
  }
  // ...
}

// BEST: Fully controlled component
function Toggle({ isOn, onChange }) {
  function handleClick() {
    onChange(!isOn);
  }
  // ...
}
```

### Chains of Effects

```tsx
// BAD: Effect chain
useEffect(() => {
  if (card !== null && card.gold) {
    setGoldCardCount(c => c + 1);
  }
}, [card]);

useEffect(() => {
  if (goldCardCount > 3) {
    setRound(r => r + 1);
    setGoldCardCount(0);
  }
}, [goldCardCount]);

// GOOD: Calculate derived state, update in event handler
const isGameOver = round > 5;

function handlePlaceCard(nextCard) {
  setCard(nextCard);
  if (nextCard.gold) {
    if (goldCardCount < 3) {
      setGoldCardCount(goldCardCount + 1);
    } else {
      setGoldCardCount(0);
      setRound(round + 1);
    }
  }
}
```

## Effect Dependencies

### Never Suppress the Linter

```tsx
// BAD: Suppressing linter hides bugs
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + increment);
  }, 1000);
  return () => clearInterval(id);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);

// GOOD: Fix the code, not the linter
useEffect(() => {
  const id = setInterval(() => {
    setCount(c => c + increment);
  }, 1000);
  return () => clearInterval(id);
}, [increment]);
```

### Use Updater Functions to Remove State Dependencies

```tsx
// BAD: messages in dependencies causes reconnection on every message
useEffect(() => {
  connection.on('message', (msg) => {
    setMessages([...messages, msg]);
  });
  // ...
}, [messages]); // Reconnects on every message!

// GOOD: Updater function removes dependency
useEffect(() => {
  connection.on('message', (msg) => {
    setMessages(msgs => [...msgs, msg]);
  });
  // ...
}, []); // No messages dependency needed
```

### Move Objects/Functions Inside Effects

```tsx
// BAD: Object created each render triggers Effect
function ChatRoom({ roomId }) {
  const options = { serverUrl, roomId }; // New object each render
  useEffect(() => {
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [options]); // Reconnects every render!
}

// GOOD: Create object inside Effect
function ChatRoom({ roomId }) {
  useEffect(() => {
    const options = { serverUrl, roomId };
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, serverUrl]); // Only reconnects when values change
}
```

### useEffectEvent for Non-Reactive Logic

```tsx
// BAD: theme change reconnects chat
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      showNotification('Connected!', theme);
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, theme]); // Reconnects on theme change!
}

// GOOD: useEffectEvent for non-reactive logic
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // theme no longer causes reconnection
}
```

### Wrap Callback Props with useEffectEvent

```tsx
// BAD: Callback prop in dependencies
function ChatRoom({ roomId, onReceiveMessage }) {
  useEffect(() => {
    connection.on('message', onReceiveMessage);
    // ...
  }, [roomId, onReceiveMessage]); // Reconnects if parent re-renders
}

// GOOD: Wrap callback in useEffectEvent
function ChatRoom({ roomId, onReceiveMessage }) {
  const onMessage = useEffectEvent(onReceiveMessage);

  useEffect(() => {
    connection.on('message', onMessage);
    // ...
  }, [roomId]); // Stable dependency list
}
```

## Effect Cleanup

### Always Clean Up Subscriptions

```tsx
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect(); // REQUIRED
}, [roomId]);

useEffect(() => {
  function handleScroll(e) {
    console.log(window.scrollY);
  }
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll); // REQUIRED
}, []);
```

### Data Fetching with Ignore Flag

```tsx
useEffect(() => {
  let ignore = false;

  async function fetchData() {
    const result = await fetchTodos(userId);
    if (!ignore) {
      setTodos(result);
    }
  }

  fetchData();

  return () => {
    ignore = true; // Prevents stale data from old requests
  };
}, [userId]);
```

### Development Double-Fire Is Intentional

React remounts components in development to verify cleanup works. If you see effects firing twice, don't try to prevent it with refs:

```tsx
// BAD: Hiding the symptom
const didInit = useRef(false);
useEffect(() => {
  if (didInit.current) return;
  didInit.current = true;
  // ...
}, []);

// GOOD: Fix the cleanup
useEffect(() => {
  const connection = createConnection();
  connection.connect();
  return () => connection.disconnect(); // Proper cleanup
}, []);
```

## Refs

### Use Refs for Values That Don't Affect Rendering

```tsx
// GOOD: Ref for timeout ID (doesn't affect UI)
const timeoutRef = useRef(null);

function handleClick() {
  clearTimeout(timeoutRef.current);
  timeoutRef.current = setTimeout(() => {
    // ...
  }, 1000);
}

// BAD: Using ref for displayed value
const countRef = useRef(0);
countRef.current++; // UI won't update!
```

### Never Read/Write ref.current During Render

```tsx
// BAD: Reading ref during render
function MyComponent() {
  const ref = useRef(0);
  ref.current++; // Mutating during render!
  return <div>{ref.current}</div>; // Reading during render!
}

// GOOD: Read/write refs in event handlers and effects
function MyComponent() {
  const ref = useRef(0);

  function handleClick() {
    ref.current++; // OK in event handler
  }

  useEffect(() => {
    ref.current = someValue; // OK in effect
  }, [someValue]);
}
```

### Ref Callbacks for Dynamic Lists

```tsx
// BAD: Can't call useRef in a loop
{items.map((item) => {
  const ref = useRef(null); // Rule violation!
  return <li ref={ref} />;
})}

// GOOD: Ref callback with Map
const itemsRef = useRef(new Map());

{items.map((item) => (
  <li
    key={item.id}
    ref={(node) => {
      if (node) {
        itemsRef.current.set(item.id, node);
      } else {
        itemsRef.current.delete(item.id);
      }
    }}
  />
))}
```

### useImperativeHandle for Controlled Exposure

```tsx
// Limit what parent can access
function MyInput({ ref }) {
  const realInputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus() {
      realInputRef.current.focus();
    },
    // Parent can ONLY call focus(), not access full DOM node
  }));

  return <input ref={realInputRef} />;
}
```


## Extended Reference

Detailed material starting at `## Custom Hooks` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
