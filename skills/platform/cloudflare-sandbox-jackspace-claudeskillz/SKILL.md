---
name: cloudflare-sandbox
description: |
  This skill provides comprehensive knowledge for building applications with Cloudflare Sandboxes SDK, which enables secure, isolated code execution in full Linux containers at the edge. It should be used when executing untrusted code, running Python/Node.js scripts, performing git operations, building AI code execution systems, creating interactive development environments, or implementing CI/CD workflows that require full OS capabilities.

  Use when: Setting up Cloudflare Sandboxes, executing Python/Node.js code safely, managing stateful development environments, implementing AI code interpreters, running shell commands in isolation, handling git repositories programmatically, building chat-based coding agents, creating temporary build environments, processing files with system tools (ffmpeg, imagemagick, etc.), or when encountering issues with container lifecycle, session management, or state persistence.

  Keywords: cloudflare sandbox, container execution, code execution, isolated environment, durable objects, linux container, python execution, node execution, git operations, code interpreter, AI agents, session management, ephemeral container, workspace, sandbox SDK, @cloudflare/sandbox, exec(), getSandbox(), runCode(), gitCheckout(), ubuntu container
license: MIT
---

# Cloudflare Sandboxes SDK

**Status**: Production Ready (Open Beta)
**Last Updated**: 2025-10-29
**Dependencies**: `cloudflare-worker-base`, `cloudflare-durable-objects` (recommended for understanding)
**Latest Versions**: `@cloudflare/sandbox@0.4.12`, Docker image: `cloudflare/sandbox:0.4.12`

---

## Quick Start (15 Minutes)

### 1. Install SDK and Setup Wrangler

```bash
npm install @cloudflare/sandbox@latest
```

**wrangler.jsonc:**
```jsonc
{
  "name": "my-sandbox-worker",
  "main": "src/index.ts",
  "compatibility_flags": ["nodejs_compat"],
  "containers": [{
    "class_name": "Sandbox",
    "image": "cloudflare/sandbox:0.4.12",
    "instance_type": "lite"
  }],
  "durable_objects": {
    "bindings": [{
      "class_name": "Sandbox",
      "name": "Sandbox"
    }]
  },
  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["Sandbox"]
  }]
}
```

**Why this matters:**
- `nodejs_compat` enables Node.js APIs required by SDK
- `containers` defines the Ubuntu container image
- `durable_objects` binding enables persistent routing
- `migrations` registers the Sandbox class

### 2. Create Your First Sandbox Worker

```typescript
import { getSandbox, type Sandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';

type Env = {
  Sandbox: DurableObjectNamespace<Sandbox>;
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Get sandbox instance (creates if doesn't exist)
    const sandbox = getSandbox(env.Sandbox, 'my-first-sandbox');

    // Execute Python code
    const result = await sandbox.exec('python3 -c "print(2 + 2)"');

    return Response.json({
      output: result.stdout,
      success: result.success,
      exitCode: result.exitCode
    });
  }
};
```

**CRITICAL:**
- **MUST export** `{ Sandbox }` from `@cloudflare/sandbox` in your Worker
- Sandbox ID determines routing (same ID = same container)
- First request creates container (~2-3 min cold start)
- Subsequent requests are fast (<1s)

### 3. Deploy and Test

```bash
npm run deploy
curl https://your-worker.workers.dev
```

Expected output:
```json
{
  "output": "4\n",
  "success": true,
  "exitCode": 0
}
```

---

## Architecture (Understanding the 3-Layer Model)

### How Sandboxes Work

```
┌─────────────────────────────────────────┐
│  Your Worker (Layer 1)                  │
│  - Handles HTTP requests                │
│  - Calls getSandbox()                   │
│  - Uses sandbox.exec(), writeFile(), etc│
└──────────────┬──────────────────────────┘
               │ RPC via Durable Object
┌──────────────▼──────────────────────────┐
│  Durable Object (Layer 2)               │
│  - Routes by sandbox ID                 │
│  - Maintains persistent identity        │
│  - Geographic stickiness                │
└──────────────┬──────────────────────────┘
               │ Container API
┌──────────────▼──────────────────────────┐
│  Ubuntu Container (Layer 3)             │
│  - Full Linux environment               │
│  - Python 3.11, Node 20, Git, etc.      │
│  - Filesystem: /workspace, /tmp, /home  │
│  - Process isolation (VM-based)         │
└─────────────────────────────────────────┘
```

**Key Insight**: Workers handle API logic (fast), Durable Objects route requests (persistent identity), Containers execute code (full capabilities).

---

## Critical Container Lifecycle (Most Important Section!)

### Container States

```
┌─────────┐  First request  ┌────────┐  ~10 min idle  ┌──────┐
│ Not     │ ───────────────>│ Active │ ─────────────> │ Idle │
│ Created │                 │        │                │      │
└─────────┘                 └───┬────┘                └──┬───┘
                                │ ^                      │
                                │ │ New request          │
                                │ └──────────────────────┘
                                │                         │
                                ▼                         ▼
                            Files persist          ALL FILES DELETED
                            Processes run          ALL PROCESSES KILLED
                            State maintained       ALL STATE RESET
```

### The #1 Gotcha: Ephemeral by Default

**While Container is Active** (~10 min after last request):
- ✅ Files in `/workspace`, `/tmp`, `/home` persist
- ✅ Background processes keep running
- ✅ Shell environment variables remain
- ✅ Session working directories preserved

**When Container Goes Idle** (after inactivity):
- ❌ **ALL files deleted** (entire filesystem reset)
- ❌ **ALL processes terminated**
- ❌ **ALL shell state lost**
- ⚠️  Next request creates **fresh container from scratch**

**This is NOT like a traditional server**. Sandboxes are ephemeral by design.

### Handling Persistence

**For Important Data**: Use external storage
```typescript
// Save to R2 before container goes idle
await sandbox.writeFile('/workspace/data.txt', content);
const fileData = await sandbox.readFile('/workspace/data.txt');
await env.R2.put('backup/data.txt', fileData);

// Restore on next request
const restored = await env.R2.get('backup/data.txt');
if (restored) {
  await sandbox.writeFile('/workspace/data.txt', await restored.text());
}
```

**For Build Artifacts**: Accept ephemerality or use caching
```typescript
// Check if setup needed (handles cold starts)
const exists = await sandbox.readdir('/workspace/project').catch(() => null);
if (!exists) {
  await sandbox.gitCheckout(repoUrl, '/workspace/project');
  await sandbox.exec('npm install', { cwd: '/workspace/project' });
}
// Now safe to run build
await sandbox.exec('npm run build', { cwd: '/workspace/project' });
```

---

## Session Management (Game-Changer for Chat Agents)

### What Are Sessions?

Sessions are **bash shell contexts** within one sandbox. Think terminal tabs.

**Key Properties**:
- Each session has separate working directory
- Sessions share same filesystem
- Working directory persists across commands in same session
- Perfect for multi-step workflows

### Pattern: Chat-Based Coding Agent

```typescript
type ConversationState = {
  sandboxId: string;
  sessionId: string;
};

// First message: Create sandbox and session
const sandboxId = `user-${userId}`;
const sandbox = getSandbox(env.Sandbox, sandboxId);
const sessionId = await sandbox.createSession();

// Store in conversation state (database, KV, etc.)
await env.KV.put(`conversation:${conversationId}`, JSON.stringify({
  sandboxId,
  sessionId
}));

// Later messages: Reuse same session
const state = await env.KV.get(`conversation:${conversationId}`);
const { sandboxId, sessionId } = JSON.parse(state);
const sandbox = getSandbox(env.Sandbox, sandboxId);

// Commands run in same context
await sandbox.exec('cd /workspace/project', { session: sessionId });
await sandbox.exec('ls -la', { session: sessionId }); // Still in /workspace/project
await sandbox.exec('git status', { session: sessionId }); // Still in /workspace/project
```

### Without Sessions (Common Mistake)

```typescript
// ❌ WRONG: Each command runs in separate session
await sandbox.exec('cd /workspace/project');
await sandbox.exec('ls'); // NOT in /workspace/project (different session)
```

### Pattern: Parallel Execution

```typescript
const session1 = await sandbox.createSession();
const session2 = await sandbox.createSession();

// Run different tasks simultaneously
await Promise.all([
  sandbox.exec('python train_model.py', { session: session1 }),
  sandbox.exec('node generate_reports.js', { session: session2 })
]);
```

---

## Sandbox Naming Strategies

### Per-User Sandboxes (Persistent Workspace)

```typescript
const sandbox = getSandbox(env.Sandbox, `user-${userId}`);
```

**Pros**: User's work persists while actively using (10 min idle time)
**Cons**: Geographic lock-in (first request determines location)
**Use Cases**: Interactive notebooks, IDEs, persistent workspaces

### Per-Session Sandboxes (Fresh Each Time)

```typescript
const sandboxId = `session-${Date.now()}-${crypto.randomUUID()}`;
const sandbox = getSandbox(env.Sandbox, sandboxId);
// Always destroy after use
await sandbox.destroy();
```

**Pros**: Clean environment, no state pollution
**Cons**: No persistence between requests
**Use Cases**: One-shot code execution, CI/CD, testing

### Per-Task Sandboxes (Idempotent & Traceable)

```typescript
const sandbox = getSandbox(env.Sandbox, `build-${repoName}-${commitSha}`);
```

**Pros**: Reproducible, debuggable, cacheable
**Cons**: Need explicit cleanup strategy
**Use Cases**: Build systems, data pipelines, automated workflows

---

## Core API Reference

### Getting a Sandbox

```typescript
import { getSandbox } from '@cloudflare/sandbox';

const sandbox = getSandbox(env.Sandbox, 'unique-sandbox-id');
// Creates new sandbox if doesn't exist, or gets existing one
```

### Executing Commands

```typescript
// Basic execution
const result = await sandbox.exec('python3 script.py');
console.log(result.stdout);   // Standard output
console.log(result.stderr);   // Standard error
console.log(result.exitCode); // Exit code (0 = success)
console.log(result.success);  // Boolean (exitCode === 0)

// With options
const result = await sandbox.exec('npm install', {
  cwd: '/workspace/project',        // Working directory
  timeout: 120000,                   // Timeout in ms (default: 30s)
  session: sessionId,                // Session ID
  env: { NODE_ENV: 'production' }   // Environment variables
});

// Always check exit codes!
if (!result.success) {
  throw new Error(`Command failed: ${result.stderr}`);
}
```

### File Operations

```typescript
// Write file
await sandbox.writeFile('/workspace/data.txt', 'content');

// Read file
const content = await sandbox.readFile('/workspace/data.txt');

// Create directory
await sandbox.mkdir('/workspace/project', { recursive: true });

// List directory
const files = await sandbox.readdir('/workspace');
console.log(files); // ['data.txt', 'project']

// Delete file/directory
await sandbox.rm('/workspace/data.txt');
await sandbox.rm('/workspace/project', { recursive: true });
```

### Git Operations

```typescript
// Clone repository (optimized, faster than exec('git clone'))
await sandbox.gitCheckout(
  'https://github.com/user/repo',
  '/workspace/repo'
);

// Now use standard git commands
await sandbox.exec('git status', { cwd: '/workspace/repo' });
await sandbox.exec('git diff', { cwd: '/workspace/repo' });
```

### Code Interpreter (Jupyter-like)

```typescript
// Create Python context
const ctx = await sandbox.createCodeContext({ language: 'python' });

// Execute code - last expression auto-returned
const result = await sandbox.runCode(`
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df['a'].sum()  # This value is automatically returned
`, { context: ctx });

console.log(result.results[0].text); // "6"
console.log(result.logs); // Output from print() statements
console.log(result.error); // Any errors
```

### Background Processes

```typescript
// Start long-running process
const proc = await sandbox.spawn('python server.py');
console.log(proc.pid);

// Check if still running
const running = await sandbox.isProcessRunning(proc.pid);

// Kill process
await sandbox.killProcess(proc.pid);
```

### Cleanup

```typescript
// Destroy sandbox permanently
await sandbox.destroy();
// All files deleted, container removed, cannot be recovered
```

---

## Critical Rules

### Always Do

✅ **Check exit codes** - `if (!result.success) { handle error }`
✅ **Use sessions for multi-step workflows** - Preserve working directory
✅ **Handle cold starts** - Check if files exist before assuming they're there
✅ **Set timeouts** - Prevent hanging on long operations
✅ **Destroy ephemeral sandboxes** - Cleanup temp/session-based sandboxes
✅ **Use external storage for persistence** - R2/KV/D1 for important data
✅ **Validate user input** - Sanitize before exec() to prevent command injection
✅ **Export Sandbox class** - `export { Sandbox } from '@cloudflare/sandbox'`

### Never Do

❌ **Assume files persist after idle** - Container resets after ~10 min
❌ **Ignore exit codes** - Always check `result.success` or `result.exitCode`
❌ **Chain commands without sessions** - `cd /dir` then `ls` won't work
❌ **Execute unsanitized user input** - Use code interpreter or validate thoroughly
❌ **Forget nodejs_compat flag** - Required in wrangler.jsonc
❌ **Skip migrations** - Durable Objects need migration entries
❌ **Use .workers.dev for preview URLs** - Need custom domain
❌ **Create unlimited sandboxes** - Destroy ephemeral ones to avoid leaks

---

## Known Issues Prevention

This skill prevents **10** documented issues:

### Issue #1: Missing nodejs_compat Flag
**Error**: `ReferenceError: fetch is not defined` or `Buffer is not defined`
**Source**: https://developers.cloudflare.com/sandbox/get-started/
**Why It Happens**: SDK requires Node.js APIs not available in standard Workers
**Prevention**: Add `"compatibility_flags": ["nodejs_compat"]` to wrangler.jsonc

### Issue #2: Missing Migrations
**Error**: `Error: Class 'Sandbox' not found`
**Source**: https://developers.cloudflare.com/durable-objects/
**Why It Happens**: Durable Objects must be registered via migrations
**Prevention**: Include migrations array in wrangler.jsonc

### Issue #3: Assuming File Persistence
**Error**: Files disappear after inactivity
**Source**: https://developers.cloudflare.com/sandbox/concepts/sandboxes/
**Why It Happens**: Containers go idle after ~10 min, all state reset
**Prevention**: Use external storage (R2/KV) or check existence on each request

### Issue #4: Session Directory Confusion
**Error**: Commands execute in wrong directory
**Source**: https://developers.cloudflare.com/sandbox/concepts/sessions/
**Why It Happens**: Each exec() uses new session unless explicitly specified
**Prevention**: Create session with `createSession()`, pass to all related commands

### Issue #5: Ignoring Exit Codes
**Error**: Assuming command succeeded when it failed
**Source**: Shell best practices
**Why It Happens**: Not checking `result.success` or `result.exitCode`
**Prevention**: Always check: `if (!result.success) throw new Error(result.stderr)`

### Issue #6: Not Handling Cold Starts
**Error**: Commands fail because dependencies aren't installed
**Source**: https://developers.cloudflare.com/sandbox/concepts/sandboxes/
**Why It Happens**: Container resets after idle period
**Prevention**: Check if setup needed before running commands

### Issue #7: Docker Not Running (Local Dev)
**Error**: `Failed to build container` during local development
**Source**: https://developers.cloudflare.com/sandbox/get-started/
**Why It Happens**: Local dev requires Docker daemon
**Prevention**: Ensure Docker Desktop is running before `npm run dev`

### Issue #8: Version Mismatch (Package vs Docker Image)
**Error**: API methods not available or behaving unexpectedly
**Source**: GitHub issues
**Why It Happens**: npm package version doesn't match Docker image version
**Prevention**: Keep `@cloudflare/sandbox` package and `cloudflare/sandbox` image in sync

### Issue #9: Not Cleaning Up Ephemeral Sandboxes
**Error**: Resource exhaustion, unexpected costs
**Source**: Resource management best practices
**Why It Happens**: Creating sandboxes without destroying them
**Prevention**: `await sandbox.destroy()` in finally block for temp sandboxes

### Issue #10: Command Injection Vulnerability
**Error**: Security breach from unsanitized user input
**Source**: Security best practices
**Why It Happens**: Passing user input directly to `exec()`
**Prevention**: Use code interpreter API or validate/sanitize input thoroughly

---

## Configuration Files Reference

### wrangler.jsonc (Full Example)

```jsonc
{
  "name": "my-sandbox-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-29",
  "compatibility_flags": ["nodejs_compat"],

  "containers": [{
    "class_name": "Sandbox",
    "image": "cloudflare/sandbox:0.4.12",
    "instance_type": "lite"
  }],

  "durable_objects": {
    "bindings": [{
      "class_name": "Sandbox",
      "name": "Sandbox"
    }]
  },

  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["Sandbox"]
  }],

  "env": {
    "ANTHROPIC_API_KEY": {
      "description": "Optional: For AI features"
    }
  },

  "observability": {
    "enabled": true
  }
}
```

**Why these settings:**
- `nodejs_compat`: Required for SDK to work
- `containers.image`: Specific version ensures consistency
- `instance_type: "lite"`: Smallest instance, upgrade to "large" for more resources
- `migrations`: Registers Sandbox Durable Object class
- `observability`: Enable logging for debugging

### Dockerfile (Optional - For Local Dev)

Only needed if extending base image:

```dockerfile
FROM cloudflare/sandbox:0.4.12

# Install additional tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Expose port for preview URLs (local dev only)
EXPOSE 8080
```

---

## Common Patterns

### Pattern 1: One-Shot Code Execution

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const { code, language } = await request.json();

    // Create ephemeral sandbox
    const sandboxId = `exec-${Date.now()}-${crypto.randomUUID()}`;
    const sandbox = getSandbox(env.Sandbox, sandboxId);

    try {
      // Create code context
      const ctx = await sandbox.createCodeContext({ language });

      // Execute code safely
      const result = await sandbox.runCode(code, {
        context: ctx,
        timeout: 10000
      });

      return Response.json({
        result: result.results?.[0]?.text,
        logs: result.logs,
        error: result.error
      });
    } finally {
      // Always cleanup
      await sandbox.destroy();
    }
  }
};
```

**When to use**: API endpoints for code execution, code playgrounds, learning platforms

### Pattern 2: Persistent User Workspace

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const userId = request.headers.get('X-User-ID');
    const { command, sessionId: existingSession } = await request.json();

    // User-specific sandbox (persists while active)
    const sandbox = getSandbox(env.Sandbox, `user-${userId}`);

    // Get or create session
    let sessionId = existingSession;
    if (!sessionId) {
      sessionId = await sandbox.createSession();
    }

    // Execute command in persistent context
    const result = await sandbox.exec(command, {
      session: sessionId,
      timeout: 30000
    });

    return Response.json({
      sessionId, // Return for next request
      output: result.stdout,
      error: result.stderr,
      success: result.success
    });
  }
};
```

**When to use**: Interactive coding environments, notebooks, IDEs, development workspaces

### Pattern 3: CI/CD Build Pipeline

```typescript
async function runBuild(repoUrl: string, commit: string, env: Env) {
  const sandboxId = `build-${repoUrl.split('/').pop()}-${commit}`;
  const sandbox = getSandbox(env.Sandbox, sandboxId);

  try {
    // Clone repository
    await sandbox.gitCheckout(repoUrl, '/workspace/repo');

    // Checkout specific commit
    await sandbox.exec(`git checkout ${commit}`, {
      cwd: '/workspace/repo'
    });

    // Install dependencies
    const install = await sandbox.exec('npm install', {
      cwd: '/workspace/repo',
      timeout: 180000 // 3 minutes
    });

    if (!install.success) {
      throw new Error(`Install failed: ${install.stderr}`);
    }

    // Run build
    const build = await sandbox.exec('npm run build', {
      cwd: '/workspace/repo',
      timeout: 300000 // 5 minutes
    });

    if (!build.success) {
      throw new Error(`Build failed: ${build.stderr}`);
    }

    // Save artifacts to R2
    const dist = await sandbox.exec('tar -czf dist.tar.gz dist', {
      cwd: '/workspace/repo'
    });
    const artifact = await sandbox.readFile('/workspace/repo/dist.tar.gz');
    await env.R2.put(`builds/${commit}.tar.gz`, artifact);

    return { success: true, artifactKey: `builds/${commit}.tar.gz` };
  } finally {
    // Optional: Keep sandbox for debugging or destroy
    // await sandbox.destroy();
  }
}
```

**When to use**: Build systems, testing pipelines, deployment automation

### Pattern 4: AI Agent with Claude Code

```typescript
async function runClaudeCodeOnRepo(
  repoUrl: string,
  task: string,
  env: Env
): Promise<{ diff: string; logs: string }> {
  const sandboxId = `claude-${Date.now()}`;
  const sandbox = getSandbox(env.Sandbox, sandboxId);

  try {
    // Clone repository
    await sandbox.gitCheckout(repoUrl, '/workspace/repo');

    // Run Claude Code CLI with secure environment injection
    // ⚠️ SECURITY: Use env option instead of shell export to prevent key exposure in logs
    const result = await sandbox.exec(
      `claude -p "${task}" --permission-mode acceptEdits`,
      {
        cwd: '/workspace/repo',
        timeout: 300000, // 5 minutes
        env: {
          ANTHROPIC_API_KEY: env.ANTHROPIC_API_KEY
        }
      }
    );

    // Get diff of changes
    const diff = await sandbox.exec('git diff', {
      cwd: '/workspace/repo'
    });

    return {
      diff: diff.stdout,
      logs: result.stdout
    };
  } finally {
    await sandbox.destroy();
  }
}
```

**When to use**: Automated code refactoring, code generation, AI-powered development

---

## Using Bundled Resources

### Scripts (scripts/)

- `setup-sandbox-binding.sh` - Interactive wrangler.jsonc configuration
- `test-sandbox.ts` - Validation script to test sandbox setup

**Example Usage:**
```bash
# Setup wrangler config
./scripts/setup-sandbox-binding.sh

# Test sandbox
npx tsx scripts/test-sandbox.ts
```

### References (references/)

- `references/persistence-guide.md` - Deep dive on container lifecycle and persistence
- `references/session-management.md` - Advanced session patterns and best practices
- `references/common-errors.md` - Complete list of errors with solutions
- `references/naming-strategies.md` - Choosing sandbox IDs for different use cases

**When Claude should load these**:
- Load `persistence-guide.md` when debugging state issues or cold starts
- Load `session-management.md` when building multi-step workflows or chat agents
- Load `common-errors.md` when encountering specific errors
- Load `naming-strategies.md` when designing sandbox architecture

---

## Advanced Topics

### Geographic Distribution

First request to a sandbox ID determines its geographic location (via Durable Objects).

**For Global Apps**:
```typescript
// Option 1: Multiple sandboxes per user (better latency)
const region = request.cf?.colo || 'default';
const sandbox = getSandbox(env.Sandbox, `user-${userId}-${region}`);

// Option 2: Single sandbox (simpler, higher latency for distant users)
const sandbox = getSandbox(env.Sandbox, `user-${userId}`);
```

### Error Handling Strategy

```typescript
async function safeSandboxExec(
  sandbox: Sandbox,
  cmd: string,
  options?: any
) {
  try {
    const result = await sandbox.exec(cmd, {
      ...options,
      timeout: options?.timeout || 30000
    });

    if (!result.success) {
      console.error(`Command failed: ${cmd}`, {
        exitCode: result.exitCode,
        stderr: result.stderr
      });

      return {
        success: false,
        error: result.stderr,
        exitCode: result.exitCode
      };
    }

    return {
      success: true,
      output: result.stdout,
      exitCode: 0
    };
  } catch (error) {
    console.error(`Sandbox error:`, error);
    return {
      success: false,
      error: error.message,
      exitCode: -1
    };
  }
}
```

### Security Hardening

```typescript
// Input validation
function sanitizeCommand(input: string): string {
  const dangerous = ['rm -rf', '$(', '`', '&&', '||', ';', '|'];
  for (const pattern of dangerous) {
    if (input.includes(pattern)) {
      throw new Error(`Dangerous pattern detected: ${pattern}`);
    }
  }
  return input;
}

// Use code interpreter instead of direct exec for untrusted code
async function executeUntrustedCode(code: string, sandbox: Sandbox) {
  const ctx = await sandbox.createCodeContext({ language: 'python' });
  return await sandbox.runCode(code, { context: ctx, timeout: 10000 });
}
```

---

## Dependencies

**Required**:
- `@cloudflare/sandbox@0.4.12` - Sandbox SDK
- `wrangler@latest` - Deployment CLI
- Docker Desktop - Local development only

**Optional**:
- `@anthropic-ai/sdk` - For AI features
- `@cloudflare/workers-types` - TypeScript types

---

## Official Documentation

- **Cloudflare Sandboxes**: https://developers.cloudflare.com/sandbox/
- **Architecture Guide**: https://developers.cloudflare.com/sandbox/concepts/architecture/
- **API Reference**: https://developers.cloudflare.com/sandbox/api-reference/
- **Durable Objects**: https://developers.cloudflare.com/durable-objects/
- **GitHub SDK**: https://github.com/cloudflare/sandbox-sdk

---

## Package Versions (Verified 2025-10-29)

```json
{
  "dependencies": {
    "@cloudflare/sandbox": "^0.4.12"
  },
  "devDependencies": {
    "wrangler": "^3.80.0",
    "@cloudflare/workers-types": "^4.20241106.0"
  }
}
```

**Docker Image**: `cloudflare/sandbox:0.4.12`

---

## Production Example

This skill is based on official Cloudflare tutorials:
- **Claude Code Integration**: https://developers.cloudflare.com/sandbox/tutorials/claude-code/
- **AI Code Executor**: https://developers.cloudflare.com/sandbox/tutorials/ai-code-executor/
- **Build Time**: ~15 min (setup) + ~5 min (first deploy)
- **Errors**: 0 (all 10 known issues prevented)
- **Validation**: ✅ Tested with Python, Node.js, Git, background processes, sessions

---

## Troubleshooting

### Problem: "Class 'Sandbox' not found"
**Solution**: Add migrations to wrangler.jsonc and ensure `export { Sandbox }` in Worker

### Problem: Files disappear after some time
**Solution**: Container goes idle after ~10 min. Use R2/KV for persistence or rebuild environment

### Problem: Commands execute in wrong directory
**Solution**: Create session with `createSession()`, pass sessionId to all related commands

### Problem: Docker error during local dev
**Solution**: Ensure Docker Desktop is running before `npm run dev`

### Problem: "fetch is not defined"
**Solution**: Add `"compatibility_flags": ["nodejs_compat"]` to wrangler.jsonc

---

## Complete Setup Checklist

- [ ] `npm install @cloudflare/sandbox@latest`
- [ ] Add `nodejs_compat` to compatibility_flags
- [ ] Add containers configuration with correct image version
- [ ] Add Durable Objects binding
- [ ] Add migrations for Sandbox class
- [ ] Export Sandbox class in Worker: `export { Sandbox } from '@cloudflare/sandbox'`
- [ ] Docker Desktop running (local dev only)
- [ ] Test with simple exec command
- [ ] Verify exit codes are being checked
- [ ] Implement cleanup for ephemeral sandboxes
- [ ] Test cold start behavior

---

**Questions? Issues?**

1. Check `references/common-errors.md` for specific error solutions
2. Verify all steps in wrangler.jsonc configuration
3. Check official docs: https://developers.cloudflare.com/sandbox/
4. Ensure Docker is running for local development
5. Confirm package version matches Docker image version
