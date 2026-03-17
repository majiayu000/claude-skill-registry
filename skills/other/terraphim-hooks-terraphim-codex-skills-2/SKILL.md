---
name: terraphim-hooks
description: |
  Knowledge graph-based text replacement using Terraphim hooks.
  Intercepts commands and text to apply transformations defined in the knowledge graph.
  Works with Claude Code PreToolUse hooks and Git prepare-commit-msg hooks.
license: Apache-2.0
---

# Terraphim Hooks

Use this skill when setting up or using Terraphim's knowledge graph-based text replacement capabilities through hooks.

## Overview

Terraphim hooks intercept text at key points (CLI commands, commit messages) and apply transformations using Aho-Corasick automata built from knowledge graph definitions.

**Key Components:**
- `terraphim-agent replace` - CLI command for text replacement
- PreToolUse hooks - Intercept Claude Code tool calls before execution
- Git hooks - Transform commit messages using prepare-commit-msg

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Knowledge Graph (docs/src/kg/)              │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ bun.md       │  │ bun install.md   │  │ terraphim ai.md  │  │
│  │ synonyms::   │  │ synonyms::       │  │ synonyms::       │  │
│  │ npm, yarn,   │  │ npm install,     │  │ Claude Code,     │  │
│  │ pnpm, npx    │  │ yarn install...  │  │ Claude Opus...   │  │
│  └──────────────┘  └──────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Aho-Corasick Automata       │
              │   (LeftmostLongest matching)  │
              └───────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
   ┌──────────────────────┐       ┌──────────────────────┐
   │  PreToolUse Hook     │       │  Git Hook            │
   │  (npm → bun)         │       │  (Claude → Terraphim)│
   │                      │       │                      │
   │  Input: Bash command │       │  Input: Commit msg   │
   │  Output: Modified    │       │  Output: Modified    │
   └──────────────────────┘       └──────────────────────┘
```

## For Humans

### Quick Start (Using Released Binary)

```bash
# Download and install terraphim-agent from GitHub releases (latest version)
# macOS ARM64 (Apple Silicon)
gh release download --repo terraphim/terraphim-ai \
  --pattern "terraphim-agent-aarch64-apple-darwin" --dir /tmp
chmod +x /tmp/terraphim-agent-aarch64-apple-darwin
mv /tmp/terraphim-agent-aarch64-apple-darwin ~/.cargo/bin/terraphim-agent

# macOS x86_64 (Intel)
# gh release download --repo terraphim/terraphim-ai \
#   --pattern "terraphim-agent-x86_64-apple-darwin" --dir /tmp

# Linux x86_64
# gh release download --repo terraphim/terraphim-ai \
#   --pattern "terraphim-agent-x86_64-unknown-linux-gnu" --dir /tmp

# Note: crates.io version (cargo install terraphim_agent) is outdated (v1.0.0)
# and missing hook/guard commands. Use GitHub releases for latest features.

# Create knowledge graph directory
mkdir -p ~/.config/terraphim/docs/src/kg

# Create replacement rules (example: npm -> bun)
cat > ~/.config/terraphim/docs/src/kg/"bun install.md" << 'EOF'
# bun install

Install dependencies using Bun package manager.

synonyms:: npm install, yarn install, pnpm install, npm i
EOF

# Create hooks directory and script
mkdir -p ~/.claude/hooks
cat > ~/.claude/hooks/pre_tool_use.sh << 'EOF'
#!/bin/bash
INPUT=$(cat)
cd ~/.config/terraphim 2>/dev/null || exit 0
terraphim-agent hook --hook-type pre-tool-use --json <<< "$INPUT" 2>/dev/null
EOF
chmod +x ~/.claude/hooks/pre_tool_use.sh

# Test replacement
echo "npm install react" | ~/.claude/hooks/pre_tool_use.sh
# Output: {"tool_input":{"command":"bun install react"},"tool_name":"Bash"}
```

### Configure Claude Code Hook

Add to `~/.claude/settings.local.json`:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/pre_tool_use.sh"
      }]
    }]
  }
}
```

### Alternative: Build from Source

```bash
# Clone terraphim-ai repository
git clone https://github.com/terraphim/terraphim-ai
cd terraphim-ai

# Build the agent
cargo build -p terraphim_agent --release

# Install to cargo bin
cp target/release/terraphim-agent ~/.cargo/bin/
```

### CLI Usage

```bash
# Basic replacement
echo "npm install package" | terraphim-agent replace
# Output: bun install package

# With JSON output (for programmatic use)
echo "npm install" | terraphim-agent replace --json
# Output: {"result":"bun install","original":"npm install","replacements":1,"changed":true}

# Fail-open mode (returns original on error)
echo "npm install" | terraphim-agent replace --fail-open
```

### Adding Custom Replacements

Create markdown files in `~/.config/terraphim/docs/src/kg/`:

```markdown
# replacement term

Description of the replacement term.

synonyms:: term_to_replace, another_term, third_term
```

**Important:** The heading (after `#`) becomes the replacement text. Use spaces, not underscores.

**Example - Replace pytest with cargo test:**

Create `~/.config/terraphim/docs/src/kg/cargo test.md`:
```markdown
# cargo test

Rust's built-in test runner using Cargo.

synonyms:: pytest, py.test, python -m pytest
```

## For AI Agents

### Detecting Terraphim Capabilities

Check for terraphim-agent availability:

```bash
# Check if agent is available
if command -v terraphim-agent >/dev/null 2>&1; then
    echo "Terraphim agent available"
elif [ -x "./target/release/terraphim-agent" ]; then
    AGENT="./target/release/terraphim-agent"
elif [ -x "$HOME/.cargo/bin/terraphim-agent" ]; then
    AGENT="$HOME/.cargo/bin/terraphim-agent"
fi
```

### Using Replacement in Hooks

**PreToolUse Hook Pattern:**

```bash
#!/bin/bash
# Read JSON input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Only process Bash commands
[ "$TOOL_NAME" != "Bash" ] && exit 0

# Perform replacement with fail-open
REPLACED=$(terraphim-agent replace --fail-open <<< "$COMMAND")

# Output modified tool_input if changed
if [ "$REPLACED" != "$COMMAND" ]; then
    echo "$INPUT" | jq --arg cmd "$REPLACED" '.tool_input.command = $cmd'
fi
```

**Git Hook Pattern:**

```bash
#!/bin/bash
COMMIT_MSG_FILE=$1

# Read original message
ORIGINAL=$(cat "$COMMIT_MSG_FILE")

# Replace using knowledge graph
REPLACED=$(terraphim-agent replace --fail-open <<< "$ORIGINAL")

# Write back if changed
if [ "$REPLACED" != "$ORIGINAL" ]; then
    echo "$REPLACED" > "$COMMIT_MSG_FILE"
fi
```

### Programmatic Usage (Rust)

```rust
use terraphim_hooks::{ReplacementService, HookResult};
use terraphim_types::Thesaurus;

// Load thesaurus from knowledge graph
let thesaurus = load_thesaurus_from_kg("docs/src/kg/");

// Create replacement service
let service = ReplacementService::new(thesaurus);

// Perform replacement
let result: HookResult = service.replace_fail_open("npm install react");
// result.result == "bun install react"
// result.changed == true
// result.replacements == 1
```

### MCP Tool Integration

The `replace_matches` MCP tool provides the same functionality:

```json
{
  "tool": "replace_matches",
  "arguments": {
    "text": "npm install react",
    "role": "Default"
  }
}
```

## Hook Types and Use Cases

| Hook Type | Trigger Point | Use Case |
|-----------|---------------|----------|
| PreToolUse | Before tool execution | Transform commands (npm→bun) |
| PostToolUse | After tool execution | Validate outputs |
| prepare-commit-msg | Before commit | Transform attribution |
| pre-commit | Before commit | Block unwanted patterns |

## Error Handling

Hooks use **fail-open** semantics:
- If terraphim-agent is not found: pass through unchanged
- If replacement fails: return original text
- Errors logged to stderr only in verbose mode

Enable verbose mode:
```bash
export TERRAPHIM_VERBOSE=1
```

## Knowledge Graph Format

Knowledge graph files use markdown with frontmatter:

```markdown
# term_name

Optional description.

synonyms:: synonym1, synonym2, synonym3
```

**Matching behavior:**
- Aho-Corasick with LeftmostLongest matching
- Longer patterns match before shorter ones
- Case-sensitive by default

## Validation

Test your hooks:

```bash
# Run test script
./scripts/test-terraphim-hooks.sh

# Manual test - PreToolUse
echo '{"tool_name":"Bash","tool_input":{"command":"npm install"}}' | .claude/hooks/npm_to_bun_guard.sh

# Manual test - Git hook
echo "Claude Code generated this" | terraphim-agent replace
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not triggering | Check `.claude/settings.local.json` configuration |
| No replacement happening | Verify knowledge graph files exist in `docs/src/kg/` |
| Agent not found | Build with `cargo build -p terraphim_agent --release` |
| Permission denied | Run `chmod +x` on hook scripts |
| jq not found | Install jq: `brew install jq` or `apt install jq` |

## Related Skills

- `implementation` - For building custom hooks
- `testing` - For validating hook behavior
- `devops` - For CI/CD integration with hooks
