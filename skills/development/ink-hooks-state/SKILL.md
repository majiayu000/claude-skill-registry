---
name: ink-hooks-state
description: Use when managing state and side effects in Ink applications using React hooks for terminal UIs.
allowed-tools: []
---

# Ink Hooks and State Management

You are an expert in managing state and side effects in Ink applications using React hooks.

## Core Hooks

### useState - Local State

```tsx
import { Box, Text } from 'ink';
import React, { useState } from 'react';

const Counter: React.FC = () => {
  const [count, setCount] = useState(0);

  return (
    <Box>
      <Text>Count: {count}</Text>
    </Box>
  );
};
```

### useEffect - Side Effects

```tsx
import { useEffect, useState } from 'react';

const DataLoader: React.FC<{ fetchData: () => Promise<string[]> }> = ({ fetchData }) => {
  const [data, setData] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchData()
      .then((result) => {
        setData(result);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err);
        setLoading(false);
      });
  }, [fetchData]);

  if (loading) return <Text>Loading...</Text>;
  if (error) return <Text color="red">Error: {error.message}</Text>;

  return (
    <Box flexDirection="column">
      {data.map((item, i) => (
        <Text key={i}>{item}</Text>
      ))}
    </Box>
  );
};
```

### useInput - Keyboard Input

```tsx
import { useInput } from 'ink';
import { useState } from 'react';

const InteractiveMenu: React.FC<{ onExit: () => void }> = ({ onExit }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const items = ['Option 1', 'Option 2', 'Option 3'];

  useInput((input, key) => {
    if (key.upArrow) {
      setSelectedIndex((prev) => Math.max(0, prev - 1));
    }

    if (key.downArrow) {
      setSelectedIndex((prev) => Math.min(items.length - 1, prev + 1));
    }

    if (key.return) {
      // Handle selection
    }

    if (input === 'q' || key.escape) {
      onExit();
    }
  });

  return (
    <Box flexDirection="column">
      {items.map((item, i) => (
        <Text key={i} color={i === selectedIndex ? 'cyan' : 'white'}>
          {i === selectedIndex ? '> ' : '  '}
          {item}
        </Text>
      ))}
    </Box>
  );
};
```

### useApp - App Control

```tsx
import { useApp } from 'ink';
import { useEffect } from 'react';

const AutoExit: React.FC<{ delay: number }> = ({ delay }) => {
  const { exit } = useApp();

  useEffect(() => {
    const timer = setTimeout(() => {
      exit();
    }, delay);

    return () => clearTimeout(timer);
  }, [delay, exit]);

  return <Text>Exiting in {delay}ms...</Text>;
};
```

### useStdout - Terminal Dimensions

```tsx
import { useStdout } from 'ink';

const ResponsiveComponent: React.FC = () => {
  const { stdout } = useStdout();
  const width = stdout.columns;
  const height = stdout.rows;

  return (
    <Box>
      <Text>
        Terminal size: {width}x{height}
      </Text>
    </Box>
  );
};
```

### useFocus - Focus Management

```tsx
import { useFocus, useFocusManager } from 'ink';

const FocusableItem: React.FC<{ label: string }> = ({ label }) => {
  const { isFocused } = useFocus();

  return (
    <Text color={isFocused ? 'cyan' : 'white'}>
      {isFocused ? '> ' : '  '}
      {label}
    </Text>
  );
};

const FocusableList: React.FC = () => {
  const { enableFocus } = useFocusManager();

  useEffect(() => {
    enableFocus();
  }, [enableFocus]);

  return (
    <Box flexDirection="column">
      <FocusableItem label="First" />
      <FocusableItem label="Second" />
      <FocusableItem label="Third" />
    </Box>
  );
};
```

## Advanced Patterns

### Custom Hooks

```tsx
// useInterval hook
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

// Usage
const Spinner: React.FC = () => {
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  const [frame, setFrame] = useState(0);

  useInterval(() => {
    setFrame((prev) => (prev + 1) % frames.length);
  }, 80);

  return <Text color="cyan">{frames[frame]}</Text>;
};
```

### Async State Management

```tsx
function useAsync<T>(asyncFunction: () => Promise<T>) {
  const [state, setState] = useState<{
    loading: boolean;
    error: Error | null;
    data: T | null;
  }>({
    loading: true,
    error: null,
    data: null,
  });

  useEffect(() => {
    let mounted = true;

    asyncFunction()
      .then((data) => {
        if (mounted) {
          setState({ loading: false, error: null, data });
        }
      })
      .catch((error: Error) => {
        if (mounted) {
          setState({ loading: false, error, data: null });
        }
      });

    return () => {
      mounted = false;
    };
  }, [asyncFunction]);

  return state;
}
```

### Promise-based Flow Control

```tsx
interface PromiseFlowProps {
  onComplete: (result: string[]) => void;
  onError: (error: Error) => void;
  execute: () => Promise<string[]>;
}

const PromiseFlow: React.FC<PromiseFlowProps> = ({ onComplete, onError, execute }) => {
  const [phase, setPhase] = useState<'pending' | 'success' | 'error'>('pending');

  useEffect(() => {
    execute()
      .then((result) => {
        setPhase('success');
        onComplete(result);
      })
      .catch((err: Error) => {
        setPhase('error');
        onError(err);
      });
  }, [execute, onComplete, onError]);

  return (
    <Box>
      {phase === 'pending' && <Text color="yellow">Processing...</Text>}
      {phase === 'success' && <Text color="green">Complete!</Text>}
      {phase === 'error' && <Text color="red">Failed!</Text>}
    </Box>
  );
};
```

## Best Practices

1. **Cleanup**: Always cleanup in useEffect return functions
2. **Dependencies**: Correctly specify dependency arrays
3. **Refs**: Use useRef for mutable values that don't trigger re-renders
4. **Callbacks**: Use useCallback to memoize event handlers
5. **Unmount Safety**: Check mounted state before setting state in async operations

## Common Pitfalls

- Forgetting to cleanup intervals and timeouts
- Missing dependencies in useEffect
- Setting state on unmounted components
- Not handling keyboard input edge cases
- Infinite re-render loops from incorrect dependencies
