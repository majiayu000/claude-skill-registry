---
name: react-component-patterns
description: React component development patterns for building UI components with hooks, state management, error handling, loading states. Use when creating React components, managing component state, handling user interactions, or working with component lifecycle.
allowed-tools: Read, Grep, Glob
---

# React Component Patterns

## Core Principles

1. **Single Responsibility** - One component does one thing well
2. **Composition Over Inheritance** - Build complex UIs from simple components
3. **Props Down, Events Up** - Data flows down, events bubble up
4. **Always Handle All States** - Loading, error, empty, success

---

## Component Structure Pattern

### CORRECT: Well-Structured Component

```javascript
// client/src/components/ChatInterface.jsx
import { useState, useEffect } from 'react';
import { generatePage } from '../utils/api';
import MessageBubble from './MessageBubble';

export default function ChatInterface({ config, onGenerationComplete }) {
  // 1. State declarations (grouped by purpose)
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 2. Effects
  useEffect(() => {
    // Initialize or cleanup
    return () => {
      // Cleanup if needed
    };
  }, []);

  // 3. Event handlers
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await generatePage(config, input, messages);
      setMessages([...messages, { role: 'user', content: input }, response]);
      setInput('');
      onGenerationComplete(response.html);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 4. Early returns for states
  if (error) {
    return (
      <div className="text-red-500 p-4">
        <p>Error: {error}</p>
        <button onClick={() => setError(null)}>Retry</button>
      </div>
    );
  }

  // 5. Main render
  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-center">
            Start a conversation...
          </div>
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble key={idx} message={msg} />
          ))
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          className="w-full px-4 py-2 border rounded"
          placeholder="Describe changes..."
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
```

### WRONG: Poorly Structured Component

```javascript
// ❌ DON'T DO THIS
export default function ChatInterface(props) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  // ❌ No loading or error state

  // ❌ No error handling
  const handleSubmit = () => {
    generatePage(props.config, input, messages).then(response => {
      // ❌ Directly mutating state
      messages.push({ role: 'user', content: input });
      messages.push(response);
      setMessages(messages);
    });
  };

  // ❌ No empty state handling
  // ❌ No loading feedback
  return (
    <div>
      {messages.map((msg, idx) => <div key={idx}>{msg.content}</div>)}
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleSubmit}>Send</button>
    </div>
  );
}
```

---

## The Four States Pattern

**Every component that fetches data MUST handle these states:**

1. **Loading** - Data is being fetched
2. **Error** - Something went wrong
3. **Empty** - No data to display
4. **Success** - Data is available

### CORRECT: All States Handled

```javascript
export default function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  // Loading state
  if (loading) {
    return <div className="p-4">Loading users...</div>;
  }

  // Error state
  if (error) {
    return (
      <div className="p-4 text-red-500">
        <p>Error: {error.message}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  // Empty state
  if (users.length === 0) {
    return (
      <div className="p-4 text-gray-500">
        No users found.
      </div>
    );
  }

  // Success state
  return (
    <div className="p-4">
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

---

## Custom Hooks Pattern

Extract reusable logic into custom hooks:

### CORRECT: Custom Hook

```javascript
// client/src/hooks/useChat.js
import { useState, useCallback } from 'react';
import { generatePage } from '../utils/api';

export function useChat(config) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (userMessage) => {
    setLoading(true);
    setError(null);

    try {
      const response = await generatePage(config, userMessage, messages);
      setMessages(prev => [
        ...prev,
        { role: 'user', content: userMessage },
        { role: 'assistant', content: response.message, html: response.html }
      ]);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [config, messages]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages
  };
}
```

### Using the Custom Hook

```javascript
export default function ChatInterface({ config }) {
  const { messages, loading, error, sendMessage } = useChat(config);
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      await sendMessage(input);
      setInput('');
    } catch (err) {
      // Error already handled by hook
    }
  };

  // ... render UI
}
```

---

## Props Patterns

### Props Destructuring

```javascript
// ✅ CORRECT: Destructure at function signature
export default function MessageBubble({ message, onDelete, className }) {
  return (
    <div className={className}>
      <p>{message.content}</p>
      {onDelete && <button onClick={onDelete}>Delete</button>}
    </div>
  );
}

// ❌ WRONG: Accessing props.property everywhere
export default function MessageBubble(props) {
  return (
    <div className={props.className}>
      <p>{props.message.content}</p>
      {props.onDelete && <button onClick={props.onDelete}>Delete</button>}
    </div>
  );
}
```

### Optional Props with Defaults

```javascript
export default function Button({
  children,
  onClick,
  variant = 'primary', // Default value
  disabled = false,
  className = ''
}) {
  const baseClasses = 'px-4 py-2 rounded';
  const variantClasses = {
    primary: 'bg-blue-500 text-white',
    secondary: 'bg-gray-200 text-gray-800'
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
```

---

## Event Handler Patterns

### CORRECT: Proper Event Handling

```javascript
export default function Form({ onSubmit }) {
  const [value, setValue] = useState('');

  // Named handler functions
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent page reload
    onSubmit(value);
    setValue(''); // Clear after submit
  };

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### WRONG: Inline Functions and Missing preventDefault

```javascript
// ❌ DON'T DO THIS
export default function Form({ onSubmit }) {
  const [value, setValue] = useState('');

  return (
    <form onSubmit={() => onSubmit(value)}> {/* ❌ Missing e.preventDefault() */}
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)} {/* ⚠️ OK for simple cases */}
      />
      <button onClick={() => { /* ❌ Use type="submit" instead */
        onSubmit(value);
        setValue('');
      }}>
        Submit
      </button>
    </form>
  );
}
```

---

## Conditional Rendering Patterns

### CORRECT: Clear Conditional Rendering

```javascript
export default function StatusMessage({ status, message }) {
  // Early return for no status
  if (!status) return null;

  // Conditional rendering with ternary (simple)
  return (
    <div className={status === 'error' ? 'text-red-500' : 'text-green-500'}>
      {message}
    </div>
  );
}

// For complex conditions, use early returns
export default function ComplexComponent({ user, loading, error }) {
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  if (!user) return <Login />;

  return <Dashboard user={user} />;
}
```

### WRONG: Nested Ternaries

```javascript
// ❌ DON'T DO THIS: Unreadable nested ternaries
return (
  <div>
    {loading ? (
      <Loading />
    ) : error ? (
      <Error />
    ) : user ? (
      user.isPremium ? (
        <PremiumDashboard />
      ) : (
        <FreeDashboard />
      )
    ) : (
      <Login />
    )}
  </div>
);
```

---

## List Rendering Patterns

### CORRECT: Proper Keys and Mapping

```javascript
export default function MessageList({ messages }) {
  // ✅ Use unique IDs as keys
  return (
    <div>
      {messages.map((message) => (
        <MessageBubble
          key={message.id} // ✅ Unique ID
          message={message}
        />
      ))}
    </div>
  );
}

// If no ID available, use index only as last resort
export default function StaticList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item}</li> // ⚠️ OK only if list never changes
      ))}
    </ul>
  );
}
```

### WRONG: Index as Key (when list changes)

```javascript
// ❌ DON'T DO THIS: Index as key with dynamic list
export default function DynamicList({ items, onDelete }) {
  return (
    <div>
      {items.map((item, index) => (
        <div key={index}> {/* ❌ Index will cause issues when deleting */}
          {item.name}
          <button onClick={() => onDelete(index)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

---

## Checklist

### Before Writing a Component
- [ ] What is the single responsibility of this component?
- [ ] What props does it need?
- [ ] What state does it need?
- [ ] Does it fetch data? (Handle all 4 states)
- [ ] Can logic be extracted into a custom hook?

### After Writing a Component
- [ ] All states handled (loading, error, empty, success)
- [ ] Props are destructured
- [ ] Event handlers prevent default when needed
- [ ] List items have proper keys
- [ ] Early returns for special states
- [ ] No inline function definitions in render (unless very simple)
- [ ] Component is focused and not doing too much

---

## Integration with Other Skills

- **api-client-patterns**: How to call APIs from components
- **express-api-patterns**: Understanding backend endpoints
- **testing-patterns**: How to test React components
- **systematic-debugging**: Debugging component issues

---

## Common Mistakes to Avoid

1. ❌ Not handling loading/error states
2. ❌ Using index as key in dynamic lists
3. ❌ Mutating state directly
4. ❌ Missing preventDefault in form submissions
5. ❌ Accessing undefined properties without checks
6. ❌ Not cleaning up effects
7. ❌ Too many responsibilities in one component
8. ❌ Prop drilling instead of composition or context
