---
name: lsp-setup
description: Auto-discovers and configures Language Server Protocol (LSP) servers for your project's languages
type: skill
activationStrategy: lazy-aggressive
activationKeywords:
  - LSP
  - Language Server Protocol
  - LSP setup
  - LSP configuration
  - configure LSP
  - enable LSP
  - lsp-setup
  - language server
  - code intelligence
  - code completion
  - pyright
  - rust-analyzer
  - gopls
activationContextWindow: 3
persistenceThreshold: 20
---

# LSP Auto-Configuration Skill

**Manual control and troubleshooting for Language Server Protocol (LSP) configuration.**

## Important: LSP is Configured Automatically

**You probably don't need this skill!** LSP is configured automatically when you run `amplihack claude`.

**When amplihack launches Claude Code, it automatically:**
- Detects programming languages in your project
- Sets `ENABLE_LSP_TOOL=1` environment variable
- Installs required LSP plugins via Claude Code plugin marketplace
- Configures project-specific settings in `.env`

**You'll see:** `📡 LSP: Detected 3 language(s): python, javascript...` when amplihack starts Claude Code.

## When to Use This Skill

**Use `/lsp-setup` only when you need to:**

- **Check Status**: Verify LSP configuration is working (`/lsp-setup --status-only`)
- **Troubleshoot Issues**: Diagnose why code intelligence isn't working
- **Force Reconfiguration**: Rebuild LSP config after manual changes (`/lsp-setup --force`)
- **Add New Languages**: Configure LSP for newly added languages

**Don't use this skill if:** LSP is already working! The automatic setup handles 99% of cases.

## Overview

The LSP Setup skill provides manual control over the same LSP auto-configuration that happens automatically at launch. It supports 16 popular programming languages out of the box and gives you direct access to configuration, status checking, and troubleshooting.

## What LSP Provides to You

When LSP is properly configured, Claude Code gains powerful code intelligence capabilities that enhance the AI's understanding of your codebase:

### Real-Time Code Intelligence

**Type Information** - Claude can see the exact types of variables, functions, and classes:
```python
# Claude can hover over 'user' and see: Type: User (class from models.py)
user = get_current_user()
```

**Go to Definition** - Claude can jump to where symbols are defined:
```python
# Claude can navigate from 'authenticate()' call to its definition in auth.py
result = authenticate(credentials)
```

**Code Diagnostics** - Claude receives real-time error detection from LSP servers:
```python
# Pyright reports: "Set" is not accessed
from typing import List, Set  # Claude sees this warning
```

### How Claude Uses LSP

**Better Code Understanding** - Instead of guessing types and behavior, Claude gets precise information from LSP servers about:
- Function signatures and return types
- Class hierarchies and inheritance
- Import paths and module structure
- Errors and warnings before runtime

**Smarter Suggestions** - With LSP data, Claude provides:
- Accurate refactoring recommendations
- Type-safe code completions
- Precise error fixes
- Context-aware code generation

**Example Workflow**:
```
You: "Fix the type error in user_service.py"

Without LSP: Claude reads the file, guesses at types, may miss subtle issues

With LSP: Claude receives diagnostic:
  Line 42: Expected type 'User | None', got 'str'
  → Claude provides exact fix based on actual type information
```

### What You'll Notice

After `/lsp-setup` configures your project:

1. **More Accurate Responses** - Claude's code suggestions match your actual types and APIs
2. **Faster Debugging** - Claude sees the same errors your IDE would show
3. **Better Refactoring** - Claude can safely rename variables across files using LSP references
4. **Improved Navigation** - Claude can find definitions, usages, and implementations precisely

### Important Note

LSP enhances Claude's capabilities *behind the scenes*. You don't interact with LSP directly - it makes Claude smarter about your code automatically.

## When to Use This Skill

Use `/lsp-setup` when you:

- Start working on a new project in Claude Code
- Add a new programming language to an existing project
- Experience missing or incorrect code intelligence features
- Want to verify your LSP configuration is correct
- Need to troubleshoot LSP server connection issues

## How It Works

### LSP Architecture - Three Layers

Claude Code's LSP system uses a three-layer architecture that must all be configured for LSP features to work:

**Layer 1: System LSP Binaries** (User-installed)
- LSP server executables installed on your system via npm, brew, rustup, etc.
- Example: `npm install -g pyright` installs the Pyright LSP server binary
- These are the actual language analysis engines

**Layer 2: Claude Code LSP Plugins** (Installed via cclsp)
- Claude Code plugins that connect to Layer 1 binaries
- Installed using: `npx cclsp install <server-name>`
- The `cclsp` tool uses the `claude-code-lsps` plugin marketplace
- These act as bridges between Claude Code and LSP servers

**Layer 3: Project Configuration** (.env file)
- Project-specific settings: virtual environments, project roots, etc.
- Must include `ENABLE_LSP_TOOL=1` to activate LSP features
- Stored in `.env` at project root

**Important**: `cclsp` and `claude-code-lsps` work together. `cclsp` is the installation tool, `claude-code-lsps` is the plugin marketplace it uses. They are complementary, not alternatives.

### The Skill's 4-Phase Process

The `/lsp-setup` skill automates the workflow from `npx cclsp@latest setup`:

#### Phase 1: Language Detection

Scans your project directory to identify programming languages based on file extensions and framework markers. Detects 16 languages including Python, TypeScript, JavaScript, Rust, Go, Java, and more.

#### Phase 2: LSP Configuration

Generates the appropriate LSP server configuration for each detected language. Checks if:
1. System LSP binaries are installed (Layer 1)
2. Claude Code plugins are installed (Layer 2)

Provides installation guidance if either is missing. **NEVER auto-installs** - user has full control.

#### Phase 3: Project Configuration

Creates or updates `.env` file with project-specific LSP settings (Layer 3):
- Workspace-specific options (Python virtual environments, Node.js project roots, etc.)
- **ENABLE_LSP_TOOL=1** (required for LSP features to activate)

#### Phase 4: Verification

Tests each LSP server connection and reports status. Provides actionable guidance for any configuration issues.

## Usage

### Basic Usage

```bash
/lsp-setup
```

Detects all languages in your project and configures LSP servers automatically.

### Check Status Only

```bash
/lsp-setup --status-only
```

Reports current LSP configuration and server availability without making changes.

### Force Reconfiguration

```bash
/lsp-setup --force
```

Regenerates LSP configuration even if valid configuration already exists.

### Specific Languages

```bash
/lsp-setup --languages python,typescript
```

Configures LSP servers only for specified languages.

### Manual Plugin Management

If you need to manage Claude Code LSP plugins directly, use the `cclsp` command:

```bash
# Install a plugin (Layer 2)
npx cclsp install pyright

# List installed plugins
npx cclsp list

# Remove a plugin
npx cclsp remove pyright

# Full setup workflow (what /lsp-setup automates)
npx cclsp@latest setup
```

The `/lsp-setup` skill automates the `npx cclsp@latest setup` workflow, adding intelligent language detection and project-specific configuration.

## Supported Languages

| Language   | LSP Server       | System Binary Installation (Layer 1) | Claude Code Plugin (Layer 2) |
|------------|------------------|--------------------------------------|------------------------------|
| Python     | pyright          | `npm install -g pyright`             | `npx cclsp install pyright`  |
| TypeScript | vtsls            | `npm install -g @vtsls/language-server` | `npx cclsp install vtsls` |
| JavaScript | vtsls            | `npm install -g @vtsls/language-server` | `npx cclsp install vtsls` |
| Rust       | rust-analyzer    | `rustup component add rust-analyzer` | `npx cclsp install rust-analyzer` |
| Go         | gopls            | `go install golang.org/x/tools/gopls@latest` | `npx cclsp install gopls` |
| Java       | jdtls            | Download from eclipse.org/jdtls      | `npx cclsp install jdtls`    |
| C/C++      | clangd           | `brew install llvm` (macOS) / `apt install clangd` (Linux) | `npx cclsp install clangd` |
| C#         | omnisharp        | Download from omnisharp.net          | `npx cclsp install omnisharp` |
| Ruby       | ruby-lsp         | `gem install ruby-lsp`               | `npx cclsp install ruby-lsp` |
| PHP        | phpactor         | `composer global require phpactor/phpactor` | `npx cclsp install phpactor` |
| Bash       | bash-language-server | `npm install -g bash-language-server` | `npx cclsp install bash-language-server` |
| YAML       | yaml-language-server | `npm install -g yaml-language-server` | `npx cclsp install yaml-language-server` |
| JSON       | vscode-json-languageserver | `npm install -g vscode-json-languageserver` | `npx cclsp install vscode-json-languageserver` |
| HTML       | vscode-html-languageserver | `npm install -g vscode-html-languageserver` | `npx cclsp install vscode-html-languageserver` |
| CSS        | vscode-css-languageserver | `npm install -g vscode-css-languageserver` | `npx cclsp install vscode-css-languageserver` |
| Markdown   | marksman         | `brew install marksman` (macOS) / Download from GitHub | `npx cclsp install marksman` |

**Note**: Both Layer 1 (system binary) and Layer 2 (Claude Code plugin) must be installed for LSP features to work.

## Example: Python Project Setup

```bash
$ cd my-python-project
$ /lsp-setup

[LSP Setup] Detecting languages...
✓ Found: Python (23 files)
✓ Found: YAML (2 files)
✓ Found: Markdown (1 file)

[LSP Setup] Configuring LSP servers...
✓ pyright: Installed at /usr/local/bin/pyright
✓ yaml-language-server: Installed at /usr/local/bin/yaml-language-server
✓ marksman: Installed at /usr/local/bin/marksman

[LSP Setup] Configuring project...
✓ Created .env with LSP configuration
✓ Detected Python virtual environment: .venv
✓ Configured pyright to use .venv/bin/python

[LSP Setup] Verifying connections...
✓ pyright: Connected (Python 3.11.5)
✓ yaml-language-server: Connected
✓ marksman: Connected

Configuration complete! LSP servers ready.
```

## Example: Polyglot Project Setup

```bash
$ cd my-fullstack-app
$ /lsp-setup

[LSP Setup] Detecting languages...
✓ Found: TypeScript (45 files)
✓ Found: Python (12 files)
✓ Found: Rust (8 files)
✓ Found: JSON (6 files)

[LSP Setup] Configuring LSP servers...
✓ vtsls: Installed
✓ pyright: Installed
✗ rust-analyzer: Not found

[LSP Setup] Installation guidance:
To install rust-analyzer:
  $ rustup component add rust-analyzer

Would you like to continue with available servers? [Y/n] y

[LSP Setup] Configuring project...
✓ Created .env with LSP configuration
✓ Detected Node.js project root: ./frontend
✓ Detected Python project root: ./backend
✓ Detected Rust workspace: ./services

[LSP Setup] Verifying connections...
✓ vtsls: Connected (TypeScript 5.3.3)
✓ pyright: Connected (Python 3.11.5)
⚠ rust-analyzer: Skipped (not installed)

Configuration complete! 2/3 LSP servers ready.
Run `rustup component add rust-analyzer` to enable Rust support.
```

## How to Verify LSP is Working

After running `/lsp-setup`, here's how to confirm LSP is providing code intelligence to Claude:

### Method 1: Check for Diagnostics

**Ask Claude to analyze a file with intentional errors**:
```
You: "What issues do you see in src/main.py?"

If LSP is working: Claude will report specific diagnostics from Pyright
  → "Line 15: 'name' is not accessed"
  → "Line 23: Expected type 'int', got 'str'"

If LSP is NOT working: Claude only sees what's in the file content
  → Generic observations about code style
  → No specific type errors or warnings
```

### Method 2: Request Type Information

**Ask Claude about types in your code**:
```
You: "What's the type of the 'user' variable in auth.py line 42?"

If LSP is working: Claude provides exact type from LSP
  → "Type: User | None (from models.User)"

If LSP is NOT working: Claude guesses based on context
  → "It appears to be a User object based on the code"
```

### Method 3: Test Navigation

**Ask Claude to find definitions**:
```
You: "Where is the authenticate() function defined?"

If LSP is working: Claude uses LSP goToDefinition
  → "Defined in src/auth/service.py:156"

If LSP is NOT working: Claude searches file contents
  → "I found it by searching for 'def authenticate'"
```

### Method 4: Check Status Command

**Run the status check**:
```bash
/lsp-setup --status-only
```

**Expected Output (LSP Working)**:
```
[LSP Setup] Configuration Status:

✓ Python (pyright): Connected
  - System Binary: /usr/local/bin/pyright-langserver
  - Plugin: Installed and active
  - Project Config: .env configured with ENABLE_LSP_TOOL=1

✓ TypeScript (vtsls): Connected
  - System Binary: /usr/local/bin/vtsls
  - Plugin: Installed and active
  - Project Config: .env configured with ENABLE_LSP_TOOL=1

Overall Status: ✓ All LSP servers ready (2/2)
```

**Problem Output (LSP NOT Working)**:
```
[LSP Setup] Configuration Status:

✗ Python (pyright): Not Connected
  - System Binary: Not found
  - Plugin: Not installed
  - Project Config: Missing ENABLE_LSP_TOOL=1

Issue: Run 'npm install -g pyright' and 'npx cclsp install pyright'
```

### What Success Looks Like

When LSP is working properly, you'll notice:

1. **Claude mentions specific line numbers** when discussing errors
2. **Claude provides exact types** instead of guessing
3. **Claude sees warnings/errors before code runs** (like your IDE does)
4. **Claude can navigate code structure** using LSP's understanding

### What Failure Looks Like

When LSP is NOT working, you'll notice:

1. **Claude only sees file contents** - no type information or diagnostics
2. **Claude makes educated guesses** about types and behavior
3. **Claude doesn't mention errors** until you run the code
4. **Claude searches text** instead of using semantic understanding

## Troubleshooting

### Issue: LSP server not found

**Symptom**: "rust-analyzer: Not found" during configuration

**Solution**: Install the LSP server using the provided installation command

```bash
$ rustup component add rust-analyzer
$ /lsp-setup --force  # Reconfigure after installation
```

### Issue: LSP server crashes on startup

**Symptom**: "pyright: Connection failed" during verification

**Solution**: Check LSP server logs and verify installation

```bash
# Check if server is properly installed
$ which pyright
/usr/local/bin/pyright

# Test server manually
$ pyright --version
pyright 1.1.332

# Check Claude Code LSP logs
$ cat ~/.claude-code/lsp-logs/pyright.log
```

### Issue: Wrong Python interpreter used

**Symptom**: Import errors despite packages being installed in virtual environment

**Solution**: Verify `.env` configuration points to correct Python interpreter

```bash
# Check current configuration
$ cat .env | grep PYTHON

# Should show:
LSP_PYTHON_INTERPRETER=/path/to/.venv/bin/python

# If incorrect, update manually or run:
$ /lsp-setup --force
```

### Issue: TypeScript project not detected

**Symptom**: No TypeScript LSP configuration despite `.ts` files present

**Solution**: Ensure `tsconfig.json` exists in project root

```bash
# Create minimal tsconfig.json
$ cat > tsconfig.json << EOF
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true
  }
}
EOF

$ /lsp-setup --force
```

### Issue: Multiple Python versions causing conflicts

**Symptom**: "Module not found" errors when LSP server uses wrong Python version

**Solution**: Explicitly set Python interpreter in `.env`

```bash
# Edit .env manually
LSP_PYTHON_INTERPRETER=/usr/bin/python3.11

# Or activate the correct virtual environment before running
$ source .venv/bin/activate
$ /lsp-setup --force
```

## Configuration Files

### `.env` (Project Root)

The skill creates or updates `.env` with LSP-specific configuration:

```bash
# LSP Configuration - Auto-generated by /lsp-setup
ENABLE_LSP_TOOL=1  # REQUIRED: Activates LSP features in Claude Code

# Project-specific settings (Layer 3)
LSP_PYTHON_INTERPRETER=/path/to/.venv/bin/python
LSP_NODE_PROJECT_ROOT=/path/to/frontend
LSP_RUST_WORKSPACE=/path/to/services
LSP_GO_MODULE=/path/to/go.mod

# Language Server Paths (auto-detected)
LSP_PYRIGHT_PATH=/usr/local/bin/pyright
LSP_VTSLS_PATH=/usr/local/bin/vtsls
LSP_RUST_ANALYZER_PATH=/usr/local/bin/rust-analyzer
```

**Critical**: `ENABLE_LSP_TOOL=1` must be present for LSP features to work. Without it, LSP servers won't be activated.

### Claude Code LSP Configuration

The skill automatically updates Claude Code's LSP configuration. No manual editing required.

## Integration with Claude Code

Once configured, Claude Code automatically:

- Provides code completion based on project context
- Shows real-time diagnostics (errors, warnings)
- Enables "Go to Definition" navigation
- Offers inline documentation on hover
- Suggests intelligent refactorings

## Best Practices

1. **Run at project start**: Configure LSP servers when you first open a project
2. **Update after adding languages**: Rerun `/lsp-setup` when adding new language files
3. **Commit `.env`**: Include LSP configuration in version control for team consistency
4. **Verify after installation**: Use `--status-only` to check server availability
5. **Keep servers updated**: Regularly update LSP servers to latest versions

## Technical Details

**Skill Type**: Interactive command-driven workflow

**Dependencies**: None (pure skill, no external packages)

**Execution Time**: 2-10 seconds depending on project size

**Persistence**: Configuration stored in `.env` and Claude Code settings

**Supported Platforms**: macOS, Linux, WSL

## Related Skills

- `environment-setup` - General development environment configuration
- `dependency-manager` - Package and dependency management
- `project-init` - New project initialization

## Maintenance

The LSP Setup skill requires no manual maintenance. It automatically adapts to your project structure and detects language changes on each run.

To update LSP server definitions or add new languages, see the developer documentation in `README.md`.

---

## Execution Instructions (For Claude Code)

When this skill is activated via `/lsp-setup` or activation keywords, execute the following workflow:

### Phase 1: Language Detection

```python
from pathlib import Path
from lsp_setup import LanguageDetector

# Detect languages in current project
detector = LanguageDetector()
project_root = Path.cwd()
languages = detector.detect_languages(project_root)

# Report findings
print(f"Detected {len(languages)} language(s):")
for lang in languages:
    print(f"  - {lang.language}: {lang.file_count} files")
```

### Phase 2: Check Current Status

```python
from lsp_setup import StatusTracker

# Get current LSP setup status
language_names = [lang.language for lang in languages]
tracker = StatusTracker(project_root, language_names)
status = tracker.get_full_status()

# Show status
print(tracker.generate_user_guidance())
```

### Phase 3: Configure LSP (If Needed)

```python
from lsp_setup import LSPConfigurator

# Configure .env file
configurator = LSPConfigurator(project_root)

# Enable LSP
if not configurator.is_lsp_enabled():
    configurator.enable_lsp()
    print("✓ Enabled LSP in .env")
```

### Phase 4: Install Plugins (If Needed)

```python
from lsp_setup import PluginManager

# Install Claude Code plugins for detected languages
manager = PluginManager()

# Check prerequisites
if not manager.check_npx_available():
    print("⚠ npx not found. Install Node.js first:")
    print("  macOS: brew install node")
    print("  Linux: sudo apt install nodejs")
    exit(1)

# Install plugins for languages with missing Layer 2
for lang_name in language_names:
    layer_2_status = status["layer_2"][lang_name]
    if not layer_2_status["installed"]:
        print(f"Installing {lang_name} plugin...")
        success = manager.install_plugin(lang_name)
        if success:
            print(f"✓ {lang_name} plugin installed")
        else:
            print(f"✗ Failed to install {lang_name} plugin")
            print(f"  {layer_2_status.get('install_guide', 'See docs')}")
```

### Phase 5: Final Status Report

```python
# Recheck status after installation
final_status = tracker.get_full_status()

if final_status["overall_ready"]:
    print("\n✅ LSP setup complete! All layers configured.")
else:
    print("\n⚠ LSP partially configured. Next steps:")
    print(tracker.generate_user_guidance())
```

### Command-Line Arguments (Optional)

Support these arguments if provided by user:

- `--status-only`: Skip installation, just report current status
- `--force`: Reinstall all plugins even if already installed
- `--languages <lang1,lang2>`: Configure only specific languages
- `--dry-run`: Show what would be done without making changes
