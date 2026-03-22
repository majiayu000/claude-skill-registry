---
name: Agent Sandboxes
description: Operate E2B agent sandboxes using the CLI. Use when user needs to run code in isolation, test packages, execute commands safely, or work with binary files in a sandbox environment. Keywords: sandbox, e2b, isolated environment, run code, test code, safe execution.
---

# Agent Sandboxes

This skill provides access to E2B sandboxes through a streamlined CLI for safe code execution and file operations in isolated environments.

## Variables

- **E2B_API_KEY**: The environment variable containing the E2B API key (stored in the environment file)
- **SANDBOX_CLI_PATH**: `.claude/skills/agent-sandboxes/sandbox_cli/`
- **ENVIRONMENT_FILE_PATH**: `../../../../.env`
- **TIMEOUT_DURATION_IN_SECONDS**: `43200` (12 hours)

## Prerequisites

Before using sandbox operations, **validate the environment**:

1. **Check for E2B_API_KEY**:
   ```bash
   # Verify the API key is set
   grep "E2B_API_KEY" `ENVIRONMENT_FILE_PATH`
   ```

   If missing, instruct the user:
   ```
   Error: E2B_API_KEY not found in .env file

   Please add your E2B API key to the .env file in the project root:
   echo "E2B_API_KEY=your_api_key_here" >> .env

   Get your API key from: https://e2b.dev/docs
   ```

2. **Verify CLI is available**:
   The sandbox CLI is located at `SANDBOX_CLI_PATH`
   The `.env` file is automatically loaded from the project root.

## Instructions

- IMPORTANT: **Don't create files locally**, always use the sandbox. Only do this if the user explicitly asks you to do so.
- **ALWAYS USE --timeout TIMEOUT_DURATION_IN_SECONDS**
- **CAPTURE AND REMEMBER SANDBOX ID** - Store it in your context, don't use shell variables or files
- **Multi-agent safe** - Each agent tracks its own sandbox ID independently
- **Always validate E2B_API_KEY first** - Don't proceed without it
- **Change directory to SANDBOX_CLI_PATH** - All commands must be run from there
- **Use --shell for complex commands** - Enables pipes, redirections, wildcards
- **Use --cwd instead of cd** - More reliable for working directory changes
- **Binary files** - Use `upload`/`download` for images, PDFs, executables
- **Never delete the sandbox unless you're explicitly asked to do so** - Sandboxes auto-timeout after TIMEOUT_DURATION_IN_SECONDS

### Template Tiers

Pre-built templates with different resource levels. Use `--template` flag with `sbx init`:

| Template | vCPU | RAM | Cost | Best For |
|----------|------|-----|------|----------|
| `fullstack-vue-fastapi-node22` | 2 | 2GB | $0.13/hr | Simple apps (default) |
| `fullstack-vue-fastapi-node22-lite` | 2 | 4GB | $0.15/hr | Browser tests |
| `fullstack-vue-fastapi-node22-standard` | 4 | 4GB | $0.27/hr | Parallel builds |
| `fullstack-vue-fastapi-node22-heavy` | 4 | 8GB | $0.33/hr | Multi-browser |
| `fullstack-vue-fastapi-node22-max` | 8 | 8GB | $0.44/hr | Fastest |

Build new templates: `uv run build_template.py --tier <tier>` or `--list-tiers` to see options.

### When to Use Sandboxes

Use agent sandboxes when the user needs to:
- **Run untrusted or experimental code** safely
- **Test packages or dependencies** without affecting the local system
- **Execute system commands** in an isolated environment
- **Work with binary files** (images, PDFs, executables)
- **Clone and test repositories** in isolation
- **Install and test different package versions**
- **Run long-running processes** without blocking

### CLI Overview

The sandbox CLI has **four core command groups**:

1. **`sbx init`** - Quick sandbox initialization
2. **`sbx sandbox`** - Lifecycle management (create, connect, kill, pause, extend-lifetime, info)
3. **`sbx files`** - File operations (ls, read, write, upload, download, rm, mkdir, mv)
4. **`sbx exec`** - Unified command execution (the most powerful command)
5. **`sbx browser`** - Browser automation for UI validation (visual testing)

**Get CLI Help**: Use `sbx --help` to see all available commands and options:
```bash
cd SANDBOX_CLI_PATH
uv run sbx --help           # Main help
uv run sbx init --help      # Help for init command
uv run sbx sandbox --help   # Help for sandbox commands
uv run sbx files --help     # Help for file operations
uv run sbx exec --help      # Help for exec command
```

### Key Command: `sbx exec`

The `exec` command is the primary interface for running commands in sandboxes:

```bash
uv run sbx exec $SANDBOX_ID "command" [options]

Options:
  --cwd PATH          Working directory
  --env KEY=VALUE     Environment variables (multiple allowed)
  --root              Run as root user
  --shell             Enable shell features (pipes, redirections, wildcards)
  --timeout SECONDS   Command timeout (default: 60)
  --background        Run command in background
```

**Important**: All commands must be run from `SANDBOX_CLI_PATH` directory.

### Key Command: `sbx browser`

Browser automation for visual validation of sandbox applications using Playwright's isolated Chromium.

**Commands** (all support `--port PORT` for parallel agents):
```bash
sbx browser init                        # First-time setup (once per machine)
sbx browser start [--headed]            # Start browser (--headed shows window)
sbx browser nav <url>                   # Navigate to URL
sbx browser eval <code>                 # Run JavaScript, returns result
sbx browser screenshot [--path P] [--full]  # Screenshot (--full for entire page)
sbx browser click <selector>            # Click element by CSS selector
sbx browser type <selector> <text>      # Type text into input field
sbx browser scroll <direction>          # up | down | top | bottom
sbx browser a11y                        # Get accessibility tree (JSON)
sbx browser dom [--full]                # Get DOM (--full for raw HTML)
sbx browser status                      # Check if browser is running
sbx browser close                       # Close browser and kill process
```

**For parallel agents**: Use `--port` flag with unique ports (9222-9999).

### Multi-Agent Considerations

**CRITICAL**: Multiple agents may be running sandboxes simultaneously. Each agent MUST:

1. **Always use `--timeout TIMEOUT_DURATION_IN_SECONDS`** when initializing (unless the user specifies a different timeout)
2. **Capture the sandbox ID** from `sbx init` output and remember it in your context
3. **DO NOT use shell variables** like `export SANDBOX_ID=...` (conflicts with other agents)
4. **DO NOT rely on `.sandbox_id` file** (gets overwritten by other agents)
5. **Track the sandbox ID yourself** and use it directly in all subsequent commands
6. **Report the sandbox ID** to the user when done

**Example of proper ID handling**:
```bash
# When you run this:
uv run sbx init

# Capture the sandbox ID from output (e.g., "sbx_abc123def456")
# Store it in YOUR context/memory as: sandbox_id = "sbx_abc123def456"

# Then use it directly in all commands:
uv run sbx exec sbx_abc123def456 "python --version"
uv run sbx files write sbx_abc123def456 /home/user/test.py "print('hello')"
```

## Cookbook

Extended documentation for specific features. **Read these when you need to use the feature.**

| Feature            | When to Read                                                           | Documentation                              |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------ |
| Browser Automation | When validating UIs, taking screenshots, or interacting with web pages | [cookbook/browser.md](cookbook/browser.md) |


## Workflow

### Step 1: Validate Environment

Always start by checking for the E2B_API_KEY:

```bash
cd SANDBOX_CLI_PATH
grep "E2B_API_KEY" `ENVIRONMENT_FILE_PATH`
```

If not found, stop and request the user to add their API key.

### Step 2: Initialize Sandbox and Capture ID

Create a new sandbox and **capture the sandbox ID from the output**:

```bash
cd SANDBOX_CLI_PATH
uv run sbx init --timeout TIMEOUT_DURATION_IN_SECONDS
```

**CRITICAL**:
- **Always use `--timeout TIMEOUT_DURATION_IN_SECONDS`**
- The command will output a sandbox ID (e.g., `sbx_abc123def456`)
- **Capture this ID** and remember it in your context
- **DO NOT use environment variables** or files to store it
- **Use this exact ID** in all subsequent commands

Additional options (optional):
- `--template NAME` - Use a specific template (default: base)
- `--env KEY=VALUE` - Set environment variables

Example:
```bash
uv run sbx init --timeout TIMEOUT_DURATION_IN_SECONDS
# Output: Created sandbox: sbx_abc123def456
# YOU remember: sandbox_id = "sbx_abc123def456"
```

### Step 3: Perform Operations

Use the appropriate command based on the task, **using the sandbox ID you captured**:

**Run commands** (replace `<sandbox_id>` with your captured ID):
```bash
uv run sbx exec <sandbox_id> "python --version"
uv run sbx exec <sandbox_id> "pip list" --cwd /home/user/project
```

**File operations**:
```bash
uv run sbx files write <sandbox_id> /home/user/script.py "print('hello')"
uv run sbx files read <sandbox_id> /home/user/output.txt
uv run sbx files upload <sandbox_id> ./local.png /home/user/image.png
uv run sbx files edit <sandbox_id> /home/user/config.ts --old "old text" --new "new text"
uv run sbx files edit <sandbox_id> /home/user/config.ts --old "find" --new "replace" --all
```

**Download directories** (clone sandbox code locally):
```bash
# Download directory (excludes .venv, node_modules, .git, __pycache__ by default)
uv run sbx files download-dir <sandbox_id> /home/user/project ./local/project

# Include everything (no exclusions)
uv run sbx files download-dir <sandbox_id> /home/user/project ./local/project --all
```

**IMPORTANT - Writing Files with Special Characters**:
The `sbx files write` command has limitations with special characters like brackets `[]` when passing content as an argument due to shell glob expansion. Use one of these workarounds:

**Option 1: Use --stdin flag (recommended)**:
```bash
# Pipe content through stdin to avoid shell escaping issues
echo 'const arr = [1, 2, 3]; const val = obj["key"];' | uv run sbx files write <sandbox_id> /home/user/file.js --stdin

# Or with heredoc
uv run sbx files write <sandbox_id> /home/user/file.js --stdin << 'EOF'
const arr = [1, 2, 3];
const value = obj["key"];
EOF
```

**Option 2: Write locally, then upload**:
```bash
# Write file locally first (using Write tool)
# Then upload to sandbox - bypasses shell escaping entirely
uv run sbx files upload <sandbox_id> ./local/file.js /home/user/file.js
```

**Option 3: Use sbx exec with heredoc or Python**:
```bash
# Use cat heredoc for complex content
uv run sbx exec <sandbox_id> "cat > /home/user/file.js << 'EOF'
const arr = [1, 2, 3];
const value = obj['key'];
EOF
" --shell

# Or use Python to write files
uv run sbx exec <sandbox_id> "python3 << 'EOF'
with open('/home/user/file.js', 'w') as f:
    f.write('''const arr = [1, 2, 3];
const value = obj[\"key\"];''')
EOF
" --shell
```

**Install packages**:
```bash
# Install uv package manager
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120

# Install Python packages
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system requests"
```

### Step 4: Expose Frontend (If Applicable)

**When building applications with a frontend/UI**, create a lightweight server to host your work and expose it:

#### 4.1: Start the Server

**Always default to port 5173** and ensure your frontend is configured to use this port:

```bash
# For Python/Flask
uv run sbx exec <sandbox_id> "python -m http.server 5173" --background --cwd /home/user/project

# For Node/React (Vite)
uv run sbx exec <sandbox_id> "npm run dev -- --port 5173" --background --cwd /home/user/project

# For static HTML/CSS/JS
uv run sbx exec <sandbox_id> "python -m http.server 5173" --background --cwd /home/user/dist

# For a custom Python server
uv run sbx files write <sandbox_id> /home/user/server.py "from flask import Flask; app = Flask(__name__); app.run(host='0.0.0.0', port=5173)"
uv run sbx exec <sandbox_id> "python /home/user/server.py" --background
```

**Key points**:
- Use `--background` flag to keep server running
- **Port 5173 is the default** - use this unless you have a specific reason not to
- Ensure your frontend code is configured for the same port

#### 4.2: Get the Exposed URL

**CRITICAL**: Always use the `get-host` command to retrieve the actual public URL. **Do NOT try to construct or infer the URL**.

```bash
uv run sbx sandbox get-host <sandbox_id> --port 5173
```

This command returns the authoritative public URL (format: `https://5173-<sandbox_id>.e2b.app`).

**Example**:
```bash
uv run sbx sandbox get-host sbx_abc123def456 --port 5173
# Output: https://5173-sbx_abc123def456.e2b.app
# YOU capture and remember this URL in your context
```

**Important**:
- Always use `--port 5173` to match your server port
- Capture the URL in your context/memory (not shell variables)
- Use the exact URL returned by this command
- Do NOT construct URLs manually (they will fail)

#### 4.3: Verify It's Working

Get the URL using `get-host` and test it:
```bash
# Get the URL (captures output: https://5173-<sandbox_id>.e2b.app)
uv run sbx sandbox get-host <sandbox_id> --port 5173

# YOU remember the URL in your context, then test it
curl https://5173-<sandbox_id>.e2b.app
```

**Note**: Capture the URL from get-host output and remember it in your context. Use the exact URL in subsequent commands.

**Important**:
- The server must listen on `0.0.0.0` (not `localhost` or `127.0.0.1`)
- Port must match between server and frontend configuration
- The sandbox will remain alive until TIMEOUT_DURATION_IN_SECONDS

### Pausing, Resuming, and Extending Sandboxes

**Pause a sandbox** (beta feature):
```bash
uv run sbx sandbox pause <sandbox_id>
```

**Resume a paused sandbox** (use `connect`):
```bash
uv run sbx sandbox connect <sandbox_id>
```

**Extend sandbox lifetime** (adds time to remaining):
```bash
uv run sbx sandbox extend-lifetime <sandbox_id> <seconds_to_add>
```

Examples:
```bash
# Add 1 hour to remaining time
uv run sbx sandbox extend-lifetime <sandbox_id> 3600

# Add 3 hours
uv run sbx sandbox extend-lifetime <sandbox_id> 10800

# Add 12 hours
uv run sbx sandbox extend-lifetime <sandbox_id> 43200
```

The `extend-lifetime` command **adds** the specified seconds to the remaining lifetime. If a sandbox has 30m left and you add 1h, it will have 1h 30m remaining.

### Step 5: Report Results

**Report the results to the user** with the sandbox information:

#### 5.1: Get the Sandbox URL (if frontend/web app)

If you built a frontend or web application, use `get-host` to retrieve the public URL:
```bash
uv run sbx sandbox get-host <sandbox_id> --port 5173
```

This returns the actual URL (e.g., `https://5173-<sandbox_id>.e2b.app`).

**Do NOT construct the URL manually** - always use the `get-host` command.

#### 5.2: Report to User

Provide the user with:
1. **The sandbox ID** - So they can reference it if needed
2. **The URL** (if applicable) - So they can access the application
3. **Timeout information** - Let them know the sandbox timeout (TIMEOUT_DURATION_IN_SECONDS)

Example report:
```
✓ Sandbox created successfully!

Sandbox ID: sbx_abc123def456
Application URL: [Use: uv run sbx sandbox get-host sbx_abc123def456 --port 5173]

Your sandbox will automatically terminate after TIMEOUT_DURATION_IN_SECONDS.
```

**Note**: Always get the actual URL using `sbx sandbox get-host <sandbox_id> --port 5173` - never construct it manually.

**IMPORTANT**:
- **Never delete the sandbox unless you're explicitly asked to do so**
- Sandboxes will automatically timeout after TIMEOUT_DURATION_IN_SECONDS

## Examples

**Progressive Disclosure**: Read only the example you need for your specific task.

### Example 1: Run Python Code Safely
**Read when**: User needs to run/test Python code in isolation.
**See**: [examples/01_run_python_code.md](examples/01_run_python_code.md)

Covers: Basic sandbox workflow, writing scripts, executing Python code, capturing sandbox ID.

### Example 2: Test a Package
**Read when**: User needs to install and test Python packages.
**See**: [examples/02_test_package.md](examples/02_test_package.md)

Covers: Installing uv package manager, installing Python packages, testing package functionality.

### Example 3: Clone and Test Repository
**Read when**: User needs to clone a GitHub repo and run tests or commands in it.
**See**: [examples/03_clone_and_test_repo.md](examples/03_clone_and_test_repo.md)

Covers: Git operations, using --cwd flag, running commands in repository context, longer timeouts.

### Example 4: Process Binary Files
**Read when**: User needs to upload, process, or download binary files (images, PDFs).
**See**: [examples/04_process_binary_files.md](examples/04_process_binary_files.md)

Covers: Binary file upload/download, image processing, using appropriate file operations for binary vs text.

### Example 5: Host Frontend Application
**Read when**: User wants to build a web app, UI, dashboard, or any frontend accessible via browser.
**See**: [examples/05_host_frontend.md](examples/05_host_frontend.md)

Covers: Exposing frontends, using port 5173, starting servers in background, getting public URLs, keeping sandboxes alive.

## Reference

**Built-in CLI Help**:
```bash
cd SANDBOX_CLI_PATH
uv run sbx --help       # Overview of all commands
uv run sbx <command> --help  # Detailed help for specific command
```

For complete command reference and advanced usage, see:
- **CLI Help**: Run `uv run sbx --help` for interactive command reference
- **Full documentation**: `SANDBOX_CLI_PATH/README.md`
- **Architecture details**: Command groups, modules, and design principles
- **Advanced examples**: Multi-step workflows, git operations, package management

## Troubleshooting

**"Need help with a command"**:
- Run `uv run sbx --help` for all available commands
- Run `uv run sbx <command> --help` for specific command details
- All commands have built-in help documentation

**"E2B_API_KEY not found"**:
- Check `.env` file exists in project root
- Verify key is set: `grep E2B_API_KEY .env`
- Add key if missing: `echo "E2B_API_KEY=key" >> .env`

**"Command not found: sbx"**:
- Ensure you're in the sandbox_cli directory
- Run with `uv run sbx` instead of just `sbx`

**"Sandbox timeout"**:
- Increase timeout: `sbx init --timeout 900`
- Use `--timeout` flag on long-running exec commands

**"Permission denied"**:
- Use `--root` flag for system operations
- Check file paths are in `/home/user/` directory

**"Forgot command syntax"**:
- Use `uv run sbx --help` to see command structure
- Each command group has detailed help with examples

**Browser issues**: See [cookbook/browser.md](cookbook/browser.md) for troubleshooting.
