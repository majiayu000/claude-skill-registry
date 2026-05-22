---
name: tuistory
description: Test and automate TUI applications using tuistory (Playwright for terminals). PREFERRED over tmux-tui for most cases. Use when you need reliable TUI automation with proper wait conditions instead of sleep hacks.
allowed-tools: Bash, Write, Read
---

# tuistory - Terminal UI Testing

Automate and test terminal applications using tuistory, a TypeScript library that works like Playwright but for TUIs.

**Prefer tuistory over tmux-tui** for most TUI automation. It has proper `waitForText` synchronization instead of unreliable `sleep` commands.

## Prerequisites

- Bun must be installed (`brew install oven-sh/bun/bun` on macOS)
- No other setup needed - Bun auto-installs dependencies on first run

## Quick Start

Create a script and run with `bun script.ts`:

```typescript
// No bun add needed - Bun auto-installs on import!
import { launchTerminal } from 'tuistory';

const session = await launchTerminal({
  command: 'my-cli',
  args: ['--interactive'],
  cols: 120,
  rows: 40,
});

// Wait for app to be ready (no more sleep guessing!)
await session.waitForText('Ready', { timeout: 5000 });

// Type input
await session.type('hello world');
await session.press(['enter']);

// Check output
const output = await session.text();
console.log(output);

// Clean up
await session.close();
```

## API Reference

### `launchTerminal(options)`

| Option | Type | Description |
|--------|------|-------------|
| `command` | string | CLI command to run |
| `args` | string[] | Command arguments |
| `cols` | number | Terminal width (default: 80) |
| `rows` | number | Terminal height (default: 24) |
| `cwd` | string? | Working directory |
| `env` | object? | Environment variables |

### `session.type(text)`

Type text character by character:

```typescript
await session.type('search query');
```

### `session.press(keys)`

Press keys or key combinations:

```typescript
// Single keys
await session.press(['enter']);
await session.press(['tab']);
await session.press(['esc']);
await session.press(['up']);
await session.press(['down']);

// Key combinations
await session.press(['ctrl', 'c']);
await session.press(['ctrl', 'shift', 'a']);
await session.press(['alt', 'f']);
```

**Available keys:** enter, esc, tab, space, backspace, delete, up, down, left, right, home, end, pageup, pagedown

**Modifiers:** ctrl, alt, shift, meta

### `session.waitForText(pattern, options?)`

Wait for text to appear (much better than `sleep`!):

```typescript
// Wait for exact text
await session.waitForText('Loading complete');

// Wait for regex pattern
await session.waitForText(/error|success/i);

// With timeout
await session.waitForText('Ready', { timeout: 10000 });
```

### `session.text(options?)`

Get current terminal content:

```typescript
// Get all text
const output = await session.text();

// Filter by style
const boldText = await session.text({ bold: true });
const redText = await session.text({ foreground: 'red' });
```

### `session.click(pattern, options?)`

Click on text matching a pattern:

```typescript
// Click on text
await session.click('Submit');

// Click first match
await session.click(/button/i, { first: true });
```

### `session.close()`

Clean up the terminal session:

```typescript
await session.close();
```

## Complete Example

```typescript
import { launchTerminal } from 'tuistory';

async function testMyCLI() {
  const session = await launchTerminal({
    command: 'my-interactive-cli',
    cols: 100,
    rows: 30,
  });

  try {
    // Wait for startup
    await session.waitForText('Main Menu', { timeout: 5000 });
    console.log('✓ CLI started');

    // Navigate menu
    await session.press(['down']);
    await session.press(['down']);
    await session.press(['enter']);

    // Wait for submenu
    await session.waitForText('Settings', { timeout: 2000 });
    console.log('✓ Entered settings');

    // Type in a field
    await session.type('new-value');
    await session.press(['enter']);

    // Verify result
    await session.waitForText('Saved');
    console.log('✓ Settings saved');

    // Get final state
    const output = await session.text();
    console.log('Final output:', output);

  } finally {
    await session.close();
  }
}

testMyCLI();
```

## Inline Usage

For quick one-off automation, use bun's eval:

```bash
bun -e "
import { launchTerminal } from 'tuistory';
const s = await launchTerminal({ command: 'my-cli' });
await s.waitForText('ready');
await s.type('test');
console.log(await s.text());
await s.close();
"
```

## Version Pinning

Pin versions directly in import statements (no package.json needed):

```typescript
import { launchTerminal } from 'tuistory@1.0.0';    // exact version
import { launchTerminal } from 'tuistory@^1.0.0';   // semver range
import { launchTerminal } from 'tuistory@latest';   // explicit latest
```

Bun caches packages globally and checks for updates every 24h for `latest`.

## When to Use tmux-tui Instead

Fall back to tmux-tui skill when:
- You need to visually attach to the session for debugging (`tmux attach -t name`)
- Bun is not available in the environment
- You're doing very quick one-off interactions where synchronization doesn't matter

## Debugging Tips

- Use `console.log(await session.text())` liberally to see current state
- Increase timeout values if the app is slow to respond
- Check `cols` and `rows` match what the app expects
- For apps that clear the screen, capture output before navigation
