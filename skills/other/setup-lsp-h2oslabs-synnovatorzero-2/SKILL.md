---
name: setup-lsp
description: Help users configure and verify LSP (Language Server Protocol) setup for Python and JavaScript/TypeScript in Claude Code. This skill should be used when users ask about LSP configuration, need to check if LSP servers are properly installed, encounter LSP-related issues, or want to verify LSP functionality before starting development work.
---

# LSP Setup and Verification

Guide for configuring and verifying Language Server Protocol (LSP) servers for Python and JavaScript/TypeScript in Claude Code projects.

## When to Use

Use this skill when:
- User asks about LSP configuration or setup
- User needs to verify LSP servers are installed and working
- LSP features are not working (no autocomplete, no diagnostics, etc.)
- Starting a new development session and want to check LSP environment
- User encounters errors related to language servers

## Quick Check Commands

### Check Python LSP Installation

```bash
# Check if pylsp is installed
which pylsp || which python-lsp-server

# Check Python version
python --version

# Test pylsp directly
pylsp --help 2>&1 | head -5
```

### Check JavaScript/TypeScript LSP Installation

```bash
# Check if typescript-language-server is installed
which typescript-language-server

# Check Node.js version
node --version

# Test typescript-language-server directly
typescript-language-server --version
```

## Installation Steps

### Python LSP Server

**Using pip:**
```bash
pip install python-lsp-server[all]
```

**Using uv (recommended for this project):**
```bash
uv pip install python-lsp-server[all]
```

**Verify installation:**
```bash
pylsp --help
```

### TypeScript Language Server

**Using npm:**
```bash
npm install -g typescript-language-server typescript
```

**Using npx (no global install):**
```bash
npx typescript-language-server --version
```

**Verify installation:**
```bash
typescript-language-server --version
```

## Configuration Verification

### Check LSP Configuration File

The project should have `.claude/lsp.json` with the following structure:

```json
{
  "lspServers": {
    "python": {
      "command": "pylsp",
      ...
    },
    "javascript": {
      "command": "typescript-language-server",
      ...
    }
  }
}
```

**Verify configuration:**
```bash
# Check if lsp.json exists
test -f .claude/lsp.json && echo "✓ lsp.json exists" || echo "✗ lsp.json missing"

# Validate JSON syntax
python3 -m json.tool .claude/lsp.json > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
```

### Check Python Environment

**For this project (Python 3.12):**
```bash
# Check Python version matches .python-version
python --version
cat .python-version

# Check if virtual environment is active
echo $VIRTUAL_ENV

# Check PYTHONPATH
echo $PYTHONPATH
```

### Check JavaScript Environment

```bash
# Check Node.js version
node --version

# Check if package.json exists (for project-specific config)
test -f package.json && echo "✓ package.json exists" || echo "✗ package.json missing"
```

## Common Issues and Solutions

### Issue: "pylsp: command not found"

**Solution:**
1. Install python-lsp-server: `pip install python-lsp-server[all]`
2. Ensure Python environment is in PATH
3. For virtual environments, activate the venv before installing

### Issue: "typescript-language-server: command not found"

**Solution:**
1. Install globally: `npm install -g typescript-language-server typescript`
2. Or ensure npx is available and use npx
3. Check Node.js is installed: `node --version`

### Issue: LSP server starts but no diagnostics appear

**Possible causes:**
1. LSP server not properly configured in `.claude/lsp.json`
2. File extensions not mapped correctly
3. Workspace folder path incorrect
4. LSP server crashed (check logs)

**Solution:**
1. Verify `.claude/lsp.json` syntax is valid
2. Check `extensionToLanguage` mappings match your file types
3. Ensure `workspaceFolder` uses `${CLAUDE_PROJECT_DIR}`
4. Check LSP server logs for errors

### Issue: Python LSP can't find project dependencies

**Solution:**
1. Ensure `PYTHONPATH` includes project root
2. Activate virtual environment if using one
3. Install project dependencies: `uv pip install -e .` or `pip install -r requirements.txt`
4. Check `env.PYTHONPATH` in `.claude/lsp.json` is set correctly

### Issue: TypeScript LSP shows errors for valid code

**Solution:**
1. Ensure `tsconfig.json` exists in project root (if using TypeScript)
2. For JavaScript projects, may need `jsconfig.json`
3. Check TypeScript version compatibility
4. Restart LSP server

## Verification Checklist

Before starting development, verify:

- [ ] Python LSP server (`pylsp`) is installed and accessible
- [ ] TypeScript language server is installed and accessible
- [ ] `.claude/lsp.json` exists and has valid JSON syntax
- [ ] Python version matches project requirements (check `.python-version`)
- [ ] Node.js is installed (for JavaScript/TypeScript support)
- [ ] Project dependencies are installed (if applicable)
- [ ] Virtual environment is activated (if using one)

## Testing LSP Functionality

### Test Python LSP

1. Open a `.py` file
2. Check for:
   - Autocomplete suggestions
   - Syntax highlighting
   - Error diagnostics
   - Go to definition (if supported)

### Test JavaScript/TypeScript LSP

1. Open a `.js`, `.jsx`, `.ts`, or `.tsx` file
2. Check for:
   - Autocomplete suggestions
   - Type checking (for TypeScript)
   - Error diagnostics
   - Import suggestions

## Project-Specific Notes

This project uses:
- **Python 3.12** (see `.python-version`)
- **Django/Wagtail** framework
- **JavaScript/TypeScript** for frontend (see `package.json`)

Ensure LSP servers are configured to work with these technologies.
