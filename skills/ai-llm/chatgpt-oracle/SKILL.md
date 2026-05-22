---
name: chatgpt-oracle
description: Send prompts to ChatGPT Pro via Playwriter browser automation. Use for cross-validation, second opinions, or leveraging GPT-5.2 Pro's research-grade intelligence.
---

# ChatGPT Pro Oracle

Send prompts to ChatGPT (including project GPTs) via Playwriter and get responses back. Connects to your existing Chrome session - no need to quit Chrome or manage cookies.

## When to use

- Cross-validate complex reasoning with a second model
- Leverage GPT-5.2 Pro's extended thinking for research tasks
- Query a ChatGPT Project that has custom instructions/files

## Requirements

- Chrome with Playwriter extension installed and activated on at least one tab
- User must be logged into ChatGPT in Chrome
- Package: `npm install -g @erwinkn/chatgpt-oracle`

## Configuration

Set `CHATGPT_ORACLE_URL` to use a custom default URL (e.g., a ChatGPT Project).

**Option 1: `.env` file in repo root**
```bash
# .env
CHATGPT_ORACLE_URL="https://chatgpt.com/g/g-p-.../project"
```

**Option 2: Environment variable**
```bash
export CHATGPT_ORACLE_URL="https://chatgpt.com/g/g-p-.../project"
```

If not set, defaults to `https://chatgpt.com/`.

## Usage

### CLI Reference

```
COMMANDS
  chatgpt-oracle <prompt>                 Send prompt and wait for response
  chatgpt-oracle send <prompt>            Send prompt, return session ID (async)
  chatgpt-oracle poll <session-id>        Check if response is ready
  chatgpt-oracle continue <id> <prompt>   Send follow-up in existing conversation
  chatgpt-oracle sessions                 List active sessions
  chatgpt-oracle close <session-id>       Close an active session

OPTIONS
  -m, --model <model>       Model: auto, instant, thinking, pro (default: pro)
  -u, --url <url>           ChatGPT URL (or set CHATGPT_ORACLE_URL env var)
  -f, --file <path>         Attach file contents (can be repeated)
  -t, --timeout <ms>        Max wait time in ms (default: 900000 = 15min)
  -w, --wait                Wait for completion (poll command)
  --no-wait                 Return immediately (continue command)
  -h, --help                Show full help
```

### CLI Examples
```bash
# Simple question
chatgpt-oracle "What is 2+2?"

# Use a specific model
chatgpt-oracle -m instant "Quick question"

# Attach files for code review
chatgpt-oracle -f src/main.ts -f src/utils.ts "Review this code for bugs"

# Use a ChatGPT Project
chatgpt-oracle -u "https://chatgpt.com/g/g-p-.../project" "Analyze this"

# Async mode: send and poll later
chatgpt-oracle send "Complex analysis task"
# Returns: Session ID: abc123...
chatgpt-oracle poll abc123
chatgpt-oracle poll -w abc123  # Wait for completion

# Multi-turn conversation
chatgpt-oracle "Explain SOLID principles"
# Returns: Session ID: xyz789...
chatgpt-oracle continue xyz789 "Give TypeScript examples"

# Long timeout for pro model research
chatgpt-oracle -m pro -t 1800000 "Deep research task"
```

### As a module
```javascript
import { askChatGPT, sendChatGPT, pollChatGPT, continueChatGPT } from '@erwinkn/chatgpt-oracle';

// Standard usage - wait for response
const result = await askChatGPT({
  prompt: 'Your question here',
  model: 'pro'
});
console.log(result.response);
console.log(result.sessionId); // Use for follow-ups

// Async mode - send and poll later
const { sessionId } = await sendChatGPT({ prompt: 'Complex question' });
// ... do other work ...
const pollResult = await pollChatGPT({ sessionId, wait: true });

// Follow-up in same conversation
const followUp = await continueChatGPT({
  sessionId: result.sessionId,
  prompt: 'Follow-up question'
});
```

## Functions

### `askChatGPT(options)` - Standard usage
Sends a prompt and waits for the complete response.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | `CHATGPT_ORACLE_URL` or `https://chatgpt.com/` | ChatGPT URL |
| `prompt` | string | required | The prompt to send |
| `model` | string | `'pro'` | `'auto'`, `'instant'`, `'thinking'`, or `'pro'` |
| `files` | array | `[]` | Files to attach: `[{path: 'file.py', content: '...'}]` |
| `timeout` | number | `900000` | Max wait time in ms (default 15 min) |
| `onProgress` | function | `null` | Callback called every 30s during long waits |

Returns:
```javascript
{ success, response, url, sessionId, elapsed, timedOut, error }
```

### `sendChatGPT(options)` - Async mode
Sends a prompt and returns immediately with a session ID for polling.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | `CHATGPT_ORACLE_URL` or `https://chatgpt.com/` | ChatGPT URL |
| `prompt` | string | required | The prompt to send |
| `model` | string | `'pro'` | Model to use |
| `files` | array | `[]` | Files to attach |

Returns:
```javascript
{ success, sessionId, url, error }
```

### `pollChatGPT(options)` - Check/wait for response
Checks if a response is ready or waits for completion.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sessionId` | string | required | Session ID from `sendChatGPT` |
| `wait` | boolean | `false` | If true, wait for completion |
| `timeout` | number | `900000` | Max wait time if `wait=true` |

Returns:
```javascript
{ success, complete, response, url, sessionId, elapsed, timedOut, error }
```

### `continueChatGPT(options)` - Follow-up messages
Sends a follow-up message in an existing conversation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sessionId` | string | required | Session ID from previous conversation |
| `prompt` | string | required | The follow-up prompt |
| `files` | array | `[]` | Files to attach |
| `wait` | boolean | `true` | If true, wait for response |
| `timeout` | number | `900000` | Max wait time if `wait=true` |

Returns:
```javascript
{ success, response, url, sessionId, elapsed, timedOut, error }
```

### Utility functions
- `closeSession(sessionId)` - Close an active session and clean up resources
- `listSessions()` - List all active sessions with their elapsed time

## Models

- **auto**: ChatGPT decides how long to think
- **instant**: Fast responses
- **thinking**: Extended thinking for complex questions
- **pro**: Research-grade intelligence (can take 10+ minutes)

## Examples

### Simple question
```javascript
import { askChatGPT } from '@erwinkn/chatgpt-oracle';

const result = await askChatGPT({
  prompt: 'What are the key differences between REST and GraphQL?',
  model: 'instant'
});
```

### With a project GPT
```javascript
import { askChatGPT } from '@erwinkn/chatgpt-oracle';

const result = await askChatGPT({
  url: 'https://chatgpt.com/g/g-p-69590661701c8191958b62e91c543dfb/project',
  prompt: 'Review this architecture decision',
  model: 'pro',
  timeout: 1800000  // 30 min for complex analysis
});
```

### With file attachments
```javascript
import fs from 'node:fs';
import { askChatGPT } from '@erwinkn/chatgpt-oracle';

const result = await askChatGPT({
  prompt: 'Find bugs in this code',
  files: [
    { path: 'src/main.py', content: fs.readFileSync('src/main.py', 'utf-8') }
  ]
});
```

### Async mode with polling
```javascript
import { sendChatGPT, pollChatGPT } from '@erwinkn/chatgpt-oracle';

// Start a long-running request without blocking
const { sessionId, url } = await sendChatGPT({
  prompt: 'Analyze this complex codebase architecture',
  model: 'pro'
});
console.log(`Started session: ${sessionId}`);

// Do other work while waiting...

// Check if ready (non-blocking)
let result = await pollChatGPT({ sessionId });
if (!result.complete) {
  console.log(`Still working... ${result.elapsed}s elapsed`);
  // Wait for completion
  result = await pollChatGPT({ sessionId, wait: true });
}
console.log(result.response);
```

### Multi-turn conversation
```javascript
import { askChatGPT, continueChatGPT } from '@erwinkn/chatgpt-oracle';

// Initial question
const first = await askChatGPT({
  prompt: 'Explain the SOLID principles',
  model: 'pro'
});

// Follow-up using the same session
const second = await continueChatGPT({
  sessionId: first.sessionId,
  prompt: 'Can you give examples in TypeScript?'
});

// Another follow-up
const third = await continueChatGPT({
  sessionId: first.sessionId,
  prompt: 'How does this apply to React components?'
});
```

## Long-running requests

GPT-5.2 Pro can take 10+ minutes for complex tasks. Use `sendChatGPT` + `pollChatGPT` for async operation, or run as a background task in Claude Code.

## Troubleshooting

- **"Extension not running"**: Click the Playwriter extension icon in Chrome on any tab (icon should turn green)
- **"Failed to connect"**: The CLI auto-retries and kills stale processes. If persistent:
  - Ensure Chrome is running with Playwriter extension active
  - Run `lsof -ti:19988 | xargs kill -9` to clear stuck processes
- **Model not switching**: ChatGPT may have changed their UI; check data-testid values
- **Empty response**: Increase timeout (`-t` flag) or check if ChatGPT is rate-limiting
