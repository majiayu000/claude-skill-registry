---
name: setup
description: Install development tools (claude | playwright)
disable-model-invocation: true
allowed-tools: Bash
---

# Setup Development Tools

Install Claude Code CLI with Too Many Cooks extension OR Playwright with Chromium.

**Usage**: `/setup <tool>`
- `claude` — Install Claude Code CLI and Too Many Cooks VSCode extension
- `playwright` — Install Chromium and Playwright for website E2E testing

---

## Claude Setup

Sets up Claude Code CLI and the Too Many Cooks VSCode extension for multi-agent coordination.

### Step 1: Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

### Step 2: Build the Too Many Cooks VSCode Extension

The extension provides visual agent coordination (locks, messages, plans) via the MCP server.

#### 2a. Build the MCP Server first

```bash
cd examples/too_many_cooks && dart pub get && npm install
dart compile js -o examples/too_many_cooks/build/bin/server.js examples/too_many_cooks/bin/server.dart
dart run tools/build/add_preamble.dart \
  examples/too_many_cooks/build/bin/server.js \
  examples/too_many_cooks/build/bin/server_node.js \
  --shebang
```

#### 2b. Build and package the extension

```bash
cd examples/too_many_cooks_vscode_extension
npm install
npm run compile
npx @vscode/vsce package
```

This creates a `.vsix` file in `examples/too_many_cooks_vscode_extension/`.

#### 2c. Install the extension

```bash
code --install-extension examples/too_many_cooks_vscode_extension/*.vsix
```

Or use the full build script that does steps 2a-2b:
```bash
bash examples/too_many_cooks_vscode_extension/build.sh
```

### Step 3: Configure Claude Code for this project

The project's `.claude/settings.local.json` already has the required permissions:
- `Bash(dart pub get:*)` — dependency installation
- `mcp__too-many-cooks__register` — MCP agent registration
- `Bash(docker ps:*)` — Docker status checks

Custom skills are in `.claude/skills/` — run `/help` to see them.

### Multi-Agent Usage

After setup, agents coordinate via the Too Many Cooks MCP server:
- **Lock files** before editing, unlock after
- **Check messages** regularly between agents
- **Update plans** so other agents can see your intent
- Keep your agent key — it's critical for authentication

---

## Playwright Setup

Sets up Playwright with Chromium for running the website's E2E test suite.

### Steps

1. **Install website npm dependencies** (includes `@playwright/test`):
   ```bash
   cd website && npm ci
   ```

2. **Install Chromium browser and OS dependencies**:
   ```bash
   cd website && npx playwright install --with-deps chromium
   ```
   This installs the Chromium binary plus required system libraries (libgbm, libasound, etc.).

3. **Verify installation**:
   ```bash
   cd website && npx playwright --version
   ```

### Notes

- Only Chromium is needed — this project does not test against Firefox or WebKit.
- On the Dev Container (Ubuntu 24.04), `--with-deps` installs the OS packages automatically.
- On macOS, Playwright downloads its own Chromium binary — no Homebrew needed.
- Browser cache lives at `~/.cache/ms-playwright/`. Delete this to force a clean reinstall.
- The website tests are at `website/tests/` and configured in `website/playwright.config.js`.
- Base URL: `http://localhost:8080` (Eleventy dev server).

### After installing

Run the website tests:
```bash
cd website && npm test
```

Or with UI mode:
```bash
cd website && npm run test:ui
```
