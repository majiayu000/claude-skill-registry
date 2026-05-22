---
name: autonomous-coding-agent
description: Build autonomous coding agents with CLI integration. Use when creating automated coding workflows, managing multi-session development, or building CI/CD code generation pipelines.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Autonomous Coding Agent

**Version**: 1.0.0
**Purpose**: Build autonomous coding agents and workflows

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Autonomous | "autonomous coding", "自律コーディング" |
| Agent | "coding agent", "コーディングエージェント" |
| Automation | "automate coding tasks", "コーディング自動化" |

---

## Overview

Create MCP servers that can:
- Execute Claude Code commands programmatically
- Manage multi-session coding workflows
- Integrate with CI/CD pipelines
- Build autonomous coding agents

---

## Claude Code CLI Commands

### Basic Commands

```bash
# Start interactive session
claude

# One-shot prompt
claude -p "explain this code"

# With specific model
claude --model claude-sonnet-4-20250514

# Print mode (no streaming)
claude --print "generate a function"
```

### Session Management

```bash
# Resume last session
claude --resume

# Continue specific session
claude --continue abc123

# Non-interactive mode
claude --no-interactive
```

### Output Formats

```bash
# JSON output for parsing
claude --output-format json -p "list files"

# Stream JSON for real-time processing
claude --output-format stream-json -p "explain"
```

---

## MCP Tool Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

const server = new McpServer({ name: 'codex-connector' });

// Define tool
server.tool(
  'codex_execute',
  'Execute a Claude Code command',
  {
    prompt: { type: 'string', description: 'The prompt to execute' },
    workdir: { type: 'string', description: 'Working directory' },
    timeout: { type: 'number', description: 'Timeout in ms', default: 300000 }
  },
  async ({ prompt, workdir, timeout }) => {
    const result = await executeCodex(prompt, workdir, timeout);
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  }
);
```

---

## Execution Pattern

### Safe Execution

```typescript
import { spawn } from 'child_process';

async function executeCodex(
  prompt: string,
  workdir: string,
  timeout: number = 300000
): Promise<CodexResult> {
  return new Promise((resolve, reject) => {
    const proc = spawn('claude', [
      '--print',
      '--output-format', 'json',
      '-p', prompt
    ], {
      cwd: workdir,
      timeout,
      env: { ...process.env, FORCE_COLOR: '0' }
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data; });
    proc.stderr.on('data', (data) => { stderr += data; });

    proc.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true, output: JSON.parse(stdout) });
      } else {
        reject(new Error(`Exit code ${code}: ${stderr}`));
      }
    });

    proc.on('error', reject);
  });
}
```

### With Abort Controller

```typescript
async function executeWithAbort(
  prompt: string,
  signal: AbortSignal
): Promise<CodexResult> {
  const proc = spawn('claude', ['--print', '-p', prompt], {
    signal // Node.js 16+ supports this
  });

  // ... handle output
}
```

---

## Multi-Session Workflow

```typescript
class CodingSession {
  private sessionId?: string;

  async start(initialPrompt: string): Promise<void> {
    const result = await executeCodex(initialPrompt);
    this.sessionId = result.sessionId;
  }

  async continue(prompt: string): Promise<string> {
    if (!this.sessionId) throw new Error('No session');
    return executeCodex(prompt, { continue: this.sessionId });
  }

  async end(): Promise<void> {
    // Session cleanup
    this.sessionId = undefined;
  }
}
```

---

## GitHub Actions Integration

```yaml
- name: Run Claude Code
  run: |
    claude --print --output-format json \
      -p "Fix the failing test in ${{ github.event.issue.body }}" \
      > result.json

- name: Parse Result
  run: |
    jq '.result' result.json
```

---

## Security Considerations

```typescript
// Sanitize user input
function sanitizePrompt(prompt: string): string {
  return prompt
    .replace(/[`$]/g, '') // Remove shell metacharacters
    .slice(0, 10000);      // Limit length
}

// Validate working directory
function validateWorkdir(dir: string): boolean {
  const resolved = path.resolve(dir);
  const allowed = ['/home/user/projects', '/tmp/sandbox'];
  return allowed.some(a => resolved.startsWith(a));
}
```

---

## Error Handling

```typescript
try {
  const result = await executeCodex(prompt, workdir);
  return { success: true, ...result };
} catch (error) {
  if (error.message.includes('timeout')) {
    return { success: false, error: 'TIMEOUT', message: 'Execution timed out' };
  }
  if (error.message.includes('ENOENT')) {
    return { success: false, error: 'NOT_FOUND', message: 'Claude CLI not installed' };
  }
  return { success: false, error: 'UNKNOWN', message: error.message };
}
```

---

## Checklist

- [ ] MCP server properly configured
- [ ] Tool definitions have clear descriptions
- [ ] Input sanitization implemented
- [ ] Timeout handling in place
- [ ] Error handling covers common cases
- [ ] Working directory validation
- [ ] Session management if needed
