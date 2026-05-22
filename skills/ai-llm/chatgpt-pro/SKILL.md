---
name: chatgpt-pro
description: Send prompts to ChatGPT Pro via Playwriter browser automation. Use for cross-validation, second opinions, or leveraging GPT-5.2 Pro's research-grade intelligence.
---

# ChatGPT Pro Automation

Send prompts to ChatGPT (including project GPTs) via Playwriter and get responses back. Connects to your existing Chrome session - no need to quit Chrome or manage cookies.

## When to use

- Cross-validate complex reasoning with a second model
- Leverage GPT-5.2 Pro's extended thinking for research tasks
- Query a ChatGPT Project that has custom instructions/files

## Requirements

- Chrome with Playwriter extension installed and activated on at least one tab
- User must be logged into ChatGPT in Chrome
- Dependencies: `playwright-core`, `playwriter`

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

### As a module
```javascript
import { askChatGPT } from './chatgpt-automation.js';

const result = await askChatGPT({
  prompt: 'Your question here',
  model: 'pro'
});

console.log(result.response);
```

### From command line
```bash
node .claude/skills/chatgpt-pro/chatgpt-automation.js "What is 2+2?"
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | `CHATGPT_ORACLE_URL` or `https://chatgpt.com/` | ChatGPT URL |
| `prompt` | string | required | The prompt to send |
| `model` | string | `'pro'` | `'auto'`, `'instant'`, `'thinking'`, or `'pro'` |
| `files` | array | `[]` | Files to attach: `[{path: 'file.py', content: '...'}]` |
| `timeout` | number | `900000` | Max wait time in ms (default 15 min) |
| `onProgress` | function | `null` | Callback called every 30s during long waits |

## Return value

```javascript
{
  success: true,       // Did it work?
  response: "...",     // ChatGPT's response
  url: "https://...",  // Conversation URL
  elapsed: 45,         // Seconds taken
  timedOut: false,     // Hit timeout?
  error: undefined     // Error message if failed
}
```

## Models

- **auto**: ChatGPT decides how long to think
- **instant**: Fast responses
- **thinking**: Extended thinking for complex questions
- **pro**: Research-grade intelligence (can take 10+ minutes)

## Examples

### Simple question
```javascript
const result = await askChatGPT({
  prompt: 'What are the key differences between REST and GraphQL?',
  model: 'instant'
});
```

### With a project GPT
```javascript
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

const result = await askChatGPT({
  prompt: 'Find bugs in this code',
  files: [
    { path: 'src/main.py', content: fs.readFileSync('src/main.py', 'utf-8') }
  ]
});
```

## Long-running requests

GPT-5.2 Pro can take 10+ minutes for complex tasks. For long requests, run as a background task in Claude Code rather than blocking.

## Troubleshooting

- **"Extension not running"**: Click the Playwriter extension icon in Chrome on any tab
- **Model not switching**: ChatGPT may have changed their UI; check data-testid values
- **Empty response**: Increase timeout or check if ChatGPT is rate-limiting
