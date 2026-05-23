---
name: ink
version: "1.0.0"
description: Ink - React for CLI applications, build interactive command-line interfaces using React components with Flexbox layout, hooks for input/focus, and testing support
---

# Ink

Ink is a framework for building command-line interfaces using React components. It provides the same component-based UI building experience that React offers in the browser, but for command-line apps. The framework leverages Yoga, a Flexbox layout engine, enabling developers to use familiar CSS-like properties in terminal environments.

## When to Use

- Building interactive CLI applications with React
- Creating terminal UIs with complex layouts
- Building progress indicators and spinners for CLI tools
- Creating multi-step wizards in the terminal
- Building dev tools with rich terminal output
- Creating dashboard-style CLI interfaces
- Handling keyboard input in terminal apps
- Building accessible CLI applications with screen reader support
- Testing terminal UI components

## Adoption

Ink is used by major projects including:
- Shopify CLI
- Gatsby
- Prisma
- Google's Gemini CLI
- Cloudflare Wrangler
- Parcel

---

## Installation

```bash
npm install ink react
```

For TypeScript:
```bash
npm install ink react
npm install -D @types/react
```

### Quick Start with Template

```bash
npx create-ink-app my-ink-cli
cd my-ink-cli
npm start
```

---

## Basic Usage

```jsx
import React from 'react';
import {render, Text} from 'ink';

const App = () => <Text color="green">Hello, Ink!</Text>;

render(<App />);
```

### Counter Example

```jsx
import React, {useState, useEffect} from 'react';
import {render, Text} from 'ink';

const Counter = () => {
  const [counter, setCounter] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCounter(c => c + 1);
    }, 100);
    return () => clearInterval(timer);
  }, []);

  return <Text color="green">{counter} tests passed</Text>;
};

render(<Counter />);
```

---

## Core Components

### Text

The `<Text>` component handles all text rendering. Text content must be wrapped in this component.

```jsx
import {Text} from 'ink';

// Basic text
<Text>Hello World</Text>

// With colors
<Text color="green">Success</Text>
<Text color="#ff0000">Error (hex)</Text>
<Text color="rgb(255, 128, 0)">Warning (rgb)</Text>

// With styles
<Text bold>Bold text</Text>
<Text italic>Italic text</Text>
<Text underline>Underlined</Text>
<Text strikethrough>Strikethrough</Text>
<Text inverse>Inverted colors</Text>
<Text dimColor>Dimmed text</Text>

// Combined styles
<Text bold color="cyan" backgroundColor="blue">
  Styled text
</Text>
```

#### Text Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | string | - | Text color (named, hex, rgb) |
| `backgroundColor` | string | - | Background color |
| `dimColor` | boolean | false | Dim the color |
| `bold` | boolean | false | Bold text |
| `italic` | boolean | false | Italic text |
| `underline` | boolean | false | Underlined text |
| `strikethrough` | boolean | false | Strikethrough text |
| `inverse` | boolean | false | Swap foreground/background |
| `wrap` | string | "wrap" | Text wrapping mode |

**Wrap modes:**
- `wrap` - Wrap text (default)
- `truncate` / `truncate-end` - Truncate at end with ellipsis
- `truncate-start` - Truncate at start
- `truncate-middle` - Truncate in middle

---

### Box

`<Box>` is the primary layout component - a flexbox container for organizing UI elements.

```jsx
import {Box, Text} from 'ink';

// Basic layout
<Box>
  <Text>Left</Text>
  <Text>Right</Text>
</Box>

// Column layout
<Box flexDirection="column">
  <Text>Top</Text>
  <Text>Bottom</Text>
</Box>

// With padding and margin
<Box padding={2} margin={1}>
  <Text>Padded content</Text>
</Box>

// With border
<Box borderStyle="round" borderColor="green" padding={1}>
  <Text>Bordered box</Text>
</Box>

// Centered content
<Box justifyContent="center" alignItems="center" height={10}>
  <Text>Centered</Text>
</Box>
```

#### Box Props - Dimensions

| Prop | Type | Description |
|------|------|-------------|
| `width` | number \| string | Width in spaces or percentage |
| `height` | number \| string | Height in lines or percentage |
| `minWidth` | number | Minimum width |
| `minHeight` | number | Minimum height |

#### Box Props - Padding

| Prop | Type | Description |
|------|------|-------------|
| `padding` | number | All sides |
| `paddingX` | number | Left and right |
| `paddingY` | number | Top and bottom |
| `paddingTop` | number | Top only |
| `paddingBottom` | number | Bottom only |
| `paddingLeft` | number | Left only |
| `paddingRight` | number | Right only |

#### Box Props - Margin

| Prop | Type | Description |
|------|------|-------------|
| `margin` | number | All sides |
| `marginX` | number | Left and right |
| `marginY` | number | Top and bottom |
| `marginTop` | number | Top only |
| `marginBottom` | number | Bottom only |
| `marginLeft` | number | Left only |
| `marginRight` | number | Right only |

#### Box Props - Flexbox

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `flexDirection` | string | "row" | row, row-reverse, column, column-reverse |
| `flexGrow` | number | 0 | Grow factor |
| `flexShrink` | number | 1 | Shrink factor |
| `flexBasis` | number \| string | - | Initial size |
| `flexWrap` | string | "nowrap" | nowrap, wrap, wrap-reverse |
| `alignItems` | string | - | flex-start, center, flex-end |
| `alignSelf` | string | - | auto, flex-start, center, flex-end |
| `justifyContent` | string | - | flex-start, center, flex-end, space-between, space-around, space-evenly |
| `gap` | number | - | Gap between children |
| `columnGap` | number | - | Horizontal gap |
| `rowGap` | number | - | Vertical gap |

#### Box Props - Borders

| Prop | Type | Description |
|------|------|-------------|
| `borderStyle` | string \| object | Border style |
| `borderColor` | string | Border color |
| `borderTop` | boolean | Show top border |
| `borderBottom` | boolean | Show bottom border |
| `borderLeft` | boolean | Show left border |
| `borderRight` | boolean | Show right border |

**Border styles:**
- `single` - Single line (─│)
- `double` - Double line (═║)
- `round` - Rounded corners (╭╮╰╯)
- `bold` - Bold line (━┃)
- `singleDouble` - Single horizontal, double vertical
- `doubleSingle` - Double horizontal, single vertical
- `classic` - ASCII (+, -, |)

#### Box Props - Other

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `display` | string | "flex" | flex or none |
| `overflow` | string | "visible" | visible or hidden |
| `overflowX` | string | - | Horizontal overflow |
| `overflowY` | string | - | Vertical overflow |
| `backgroundColor` | string | - | Background color |

---

### Newline

Insert line breaks within text.

```jsx
import {Text, Newline} from 'ink';

<Text>
  First line
  <Newline />
  Second line
  <Newline count={2} />
  After two newlines
</Text>
```

---

### Spacer

Flexible space that expands along the flex direction.

```jsx
import {Box, Text, Spacer} from 'ink';

// Push items apart
<Box>
  <Text>Left</Text>
  <Spacer />
  <Text>Right</Text>
</Box>

// Equivalent to flexGrow: 1
<Box>
  <Text>Left</Text>
  <Box flexGrow={1} />
  <Text>Right</Text>
</Box>
```

---

### Static

Render output once without updates. Perfect for logs or completed tasks.

```jsx
import {Static, Box, Text} from 'ink';

const App = ({tests}) => (
  <>
    <Static items={tests}>
      {test => (
        <Box key={test.id}>
          <Text color="green">✔ {test.title}</Text>
        </Box>
      )}
    </Static>

    <Box marginTop={1}>
      <Text>Running more tests...</Text>
    </Box>
  </>
);
```

**Props:**
- `items` - Array of items to render
- `children` - Function `(item, index) => ReactNode`

Only new items trigger renders; previously rendered items are not updated.

---

### Transform

Modify text output before rendering.

```jsx
import {Transform, Text} from 'ink';

// Uppercase transform
<Transform transform={output => output.toUpperCase()}>
  <Text>hello world</Text>
</Transform>
// Output: HELLO WORLD

// Per-line transform (hanging indent)
<Transform transform={(line, index) =>
  index === 0 ? line : `  ${line}`
}>
  <Text>First line{'\n'}Second line{'\n'}Third line</Text>
</Transform>
```

---

## Hooks

### useInput

Capture keyboard input.

```jsx
import {useInput, useApp} from 'ink';

const App = () => {
  const {exit} = useApp();

  useInput((input, key) => {
    // Character input
    if (input === 'q') {
      exit();
    }

    // Arrow keys
    if (key.upArrow) {
      // Move up
    }
    if (key.downArrow) {
      // Move down
    }

    // Modifiers
    if (key.ctrl && input === 'c') {
      exit();
    }

    // Special keys
    if (key.return) {
      // Enter pressed
    }
    if (key.escape) {
      // Escape pressed
    }
  });

  return <Text>Press 'q' to quit</Text>;
};
```

**Key object properties:**
| Property | Description |
|----------|-------------|
| `upArrow` | Up arrow pressed |
| `downArrow` | Down arrow pressed |
| `leftArrow` | Left arrow pressed |
| `rightArrow` | Right arrow pressed |
| `return` | Enter key pressed |
| `escape` | Escape key pressed |
| `ctrl` | Ctrl modifier held |
| `shift` | Shift modifier held |
| `meta` | Meta/Cmd modifier held |
| `tab` | Tab key pressed |
| `backspace` | Backspace pressed |
| `delete` | Delete pressed |
| `pageUp` | Page Up pressed |
| `pageDown` | Page Down pressed |

**Options:**
```jsx
// Disable input handling conditionally
useInput(handler, {isActive: false});
```

---

### useApp

Access app-level methods.

```jsx
import {useApp} from 'ink';

const App = () => {
  const {exit} = useApp();

  const handleDone = () => {
    exit(); // Exit successfully
  };

  const handleError = () => {
    exit(new Error('Something went wrong')); // Exit with error
  };

  return <Text>App running...</Text>;
};
```

---

### useStdin

Access stdin stream and raw mode.

```jsx
import {useStdin} from 'ink';

const App = () => {
  const {stdin, isRawModeSupported, setRawMode} = useStdin();

  useEffect(() => {
    if (isRawModeSupported) {
      setRawMode(true);
    }
    return () => setRawMode(false);
  }, []);

  return <Text>Raw mode: {isRawModeSupported ? 'enabled' : 'not supported'}</Text>;
};
```

---

### useStdout / useStderr

Access output streams.

```jsx
import {useStdout, useStderr} from 'ink';

const App = () => {
  const {stdout, write} = useStdout();
  const {stderr, write: writeError} = useStderr();

  const logToStdout = () => {
    write('Direct stdout output\n');
  };

  const logToStderr = () => {
    writeError('Error output\n');
  };

  return <Text>Stream access available</Text>;
};
```

---

### useFocus

Enable focus on components for Tab navigation.

```jsx
import {useFocus, Box, Text} from 'ink';

const FocusableItem = ({label}) => {
  const {isFocused} = useFocus();

  return (
    <Box>
      <Text color={isFocused ? 'green' : 'gray'}>
        {isFocused ? '>' : ' '} {label}
      </Text>
    </Box>
  );
};

const App = () => (
  <Box flexDirection="column">
    <FocusableItem label="Option 1" />
    <FocusableItem label="Option 2" />
    <FocusableItem label="Option 3" />
  </Box>
);
```

**Options:**
```jsx
useFocus({
  autoFocus: true,    // Focus on mount
  isActive: true,     // Enable/disable focus
  id: 'my-component'  // Unique identifier for programmatic focus
});
```

---

### useFocusManager

Control focus programmatically.

```jsx
import {useFocusManager, useInput} from 'ink';

const App = () => {
  const {
    enableFocus,
    disableFocus,
    focusNext,
    focusPrevious,
    focus
  } = useFocusManager();

  useInput((input, key) => {
    if (key.tab) {
      if (key.shift) {
        focusPrevious();
      } else {
        focusNext();
      }
    }
  });

  return (
    <Box flexDirection="column">
      <FocusableItem id="item-1" />
      <FocusableItem id="item-2" />
    </Box>
  );
};
```

---

## render() API

```jsx
import {render} from 'ink';

const {rerender, unmount, waitUntilExit, clear} = render(<App />, options);
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `stdout` | stream | process.stdout | Output stream |
| `stdin` | stream | process.stdin | Input stream |
| `stderr` | stream | process.stderr | Error stream |
| `exitOnCtrlC` | boolean | true | Exit on Ctrl+C |
| `patchConsole` | boolean | true | Intercept console output |
| `debug` | boolean | false | Debug mode (no clear) |
| `maxFps` | number | 30 | Maximum frame rate |
| `incrementalRendering` | boolean | false | Only update changed lines |

### Instance Methods

```jsx
// Re-render with new props
rerender(<App newProp={value} />);

// Unmount and exit
unmount();

// Wait for exit (returns promise)
await waitUntilExit();

// Clear rendered output
clear();
```

---

## Testing

Use `ink-testing-library` for testing Ink components.

```bash
npm install --save-dev ink-testing-library
```

```jsx
import {render} from 'ink-testing-library';
import App from './App';

test('renders greeting', () => {
  const {lastFrame} = render(<App name="World" />);
  expect(lastFrame()).toContain('Hello, World');
});

test('updates on input', () => {
  const {lastFrame, stdin} = render(<Counter />);

  expect(lastFrame()).toContain('Count: 0');

  stdin.write('i'); // Increment
  expect(lastFrame()).toContain('Count: 1');
});
```

### Testing API

| Method | Description |
|--------|-------------|
| `lastFrame()` | Get last rendered output as string |
| `frames` | Array of all rendered frames |
| `stdin` | Writable stream for simulating input |
| `rerender(element)` | Re-render with new element |
| `unmount()` | Unmount the component |

---

## Accessibility

Ink supports ARIA attributes for screen reader compatibility.

```jsx
<Box
  aria-role="list"
  aria-label="Menu options"
>
  <Box aria-role="listitem">
    <Text>Option 1</Text>
  </Box>
  <Box aria-role="listitem">
    <Text>Option 2</Text>
  </Box>
</Box>
```

### ARIA Props

| Prop | Type | Description |
|------|------|-------------|
| `aria-label` | string | Accessible label |
| `aria-hidden` | boolean | Hide from screen readers |
| `aria-role` | string | ARIA role |
| `aria-state` | object | State properties |

**Supported roles:**
- `button`, `checkbox`, `radio`, `radiogroup`
- `list`, `listitem`
- `menu`, `menuitem`
- `progressbar`
- `tab`, `tablist`
- `timer`, `toolbar`, `table`

### Screen Reader Detection

```jsx
import {useIsScreenReaderEnabled} from 'ink';

const App = () => {
  const isScreenReaderEnabled = useIsScreenReaderEnabled();

  return (
    <Box aria-label="Main content">
      {isScreenReaderEnabled ? (
        <Text>Screen reader friendly content</Text>
      ) : (
        <Text>Visual content with colors</Text>
      )}
    </Box>
  );
};
```

---

## Common Patterns

### Loading Spinner

```jsx
import React, {useState, useEffect} from 'react';
import {Text} from 'ink';

const Spinner = () => {
  const [frame, setFrame] = useState(0);
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

  useEffect(() => {
    const timer = setInterval(() => {
      setFrame(f => (f + 1) % frames.length);
    }, 80);
    return () => clearInterval(timer);
  }, []);

  return <Text color="cyan">{frames[frame]} Loading...</Text>;
};
```

### Progress Bar

```jsx
import {Box, Text} from 'ink';

const ProgressBar = ({percent}) => {
  const width = 20;
  const filled = Math.round(width * percent / 100);
  const empty = width - filled;

  return (
    <Box>
      <Text color="green">{'█'.repeat(filled)}</Text>
      <Text color="gray">{'░'.repeat(empty)}</Text>
      <Text> {percent}%</Text>
    </Box>
  );
};
```

### Menu Selection

```jsx
import React, {useState} from 'react';
import {Box, Text, useInput} from 'ink';

const Menu = ({items, onSelect}) => {
  const [selected, setSelected] = useState(0);

  useInput((input, key) => {
    if (key.upArrow) {
      setSelected(s => Math.max(0, s - 1));
    }
    if (key.downArrow) {
      setSelected(s => Math.min(items.length - 1, s + 1));
    }
    if (key.return) {
      onSelect(items[selected]);
    }
  });

  return (
    <Box flexDirection="column">
      {items.map((item, i) => (
        <Text key={item} color={i === selected ? 'green' : 'white'}>
          {i === selected ? '> ' : '  '}{item}
        </Text>
      ))}
    </Box>
  );
};
```

### Two-Column Layout

```jsx
import {Box, Text} from 'ink';

const TwoColumn = () => (
  <Box>
    <Box width="50%" borderStyle="single" padding={1}>
      <Text>Left Column</Text>
    </Box>
    <Box width="50%" borderStyle="single" padding={1}>
      <Text>Right Column</Text>
    </Box>
  </Box>
);
```

---

## Resources

- **Repository**: https://github.com/vadimdemedes/ink
- **NPM**: https://www.npmjs.com/package/ink
- **Testing Library**: https://github.com/vadimdemedes/ink-testing-library
- **Awesome Ink**: https://github.com/vadimdemedes/awesome-ink
- **License**: MIT

---

## Related Packages

| Package | Description |
|---------|-------------|
| `ink-spinner` | Spinner component |
| `ink-text-input` | Text input component |
| `ink-select-input` | Select/menu component |
| `ink-table` | Table component |
| `ink-link` | Clickable links |
| `ink-gradient` | Gradient text |
| `ink-big-text` | Large ASCII text |
| `ink-testing-library` | Testing utilities |
