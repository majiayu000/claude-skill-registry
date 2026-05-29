---
name: srt
description: Sandbox Runtime (srt) patterns for CLI/autonomous Claude runs. For interactive sandboxing, use Claude Code's built-in `/sandbox` command instead.
---

# Sandboxing Claude

## Interactive vs Autonomous

Claude Code now has **built-in sandboxing**. Choose the right approach:

| Mode | Tool | When to Use |
|------|------|-------------|
| **Interactive** | `/sandbox` | Human-in-the-loop sessions with sandbox protection |
| **CLI/Autonomous** | srt | `claude -p` with `--dangerously-skip-permissions` |

### For Interactive Sessions: Use `/sandbox`

Run `/sandbox` in Claude Code to enable native sandboxing. It uses the same OS primitives as srt (macOS seatbelt, Linux bubblewrap) but is simpler:

- No installation required
- Integrated with permission system (auto-allow mode reduces prompts by 84%)
- Configure via `settings.json`

**What `/sandbox` protects:**
- Filesystem: Write access limited to CWD by default
- Network: Domain allowlist with prompts for new domains
- Subprocesses: Same restrictions apply to scripts Claude runs

**What `/sandbox` does NOT protect:**
- No CLI flag equivalent (Docker required for CLI sandbox)
- Has escape hatch (`dangerouslyDisableSandbox`) - commands can break out
- Config is global (`settings.json`), not per-project

### For CLI/Autonomous: Use srt

When running Claude with `-p` and `--dangerously-skip-permissions`, srt provides stricter control:

- **No escape hatch** - commands cannot break out
- **Per-project config** - `.srt.json` in each repo
- **Explicit allowlists** - you specify exactly what's permitted

---

# Sandbox Runtime (srt)

[srt](https://github.com/anthropic-experimental/sandbox-runtime) is a lightweight OS-level sandbox for restricting filesystem and network access without containers.

**Use cases:**
- Running Claude with `--dangerously-skip-permissions` safely
- DX testing (stress-testing skills, toolchain validation)
- CI/CD autonomous Claude runs
- Isolating subagent work to specific directories

## Installation

```bash
npm install -g @anthropic-ai/sandbox-runtime
```

## How It Works

| Platform | Mechanism |
|----------|-----------|
| macOS | `sandbox-exec` with dynamic profiles |
| Linux | `bubblewrap` with network namespaces |

**Access model:**
- **Network**: Default deny, explicit allowlist
- **FS Read**: Default allow, explicit denylist
- **FS Write**: Default deny, explicit allowlist

---

## Configuration

srt uses JSON config files (default: `~/.srt-settings.json` or `-s <path>`).

### Config Structure

```json
{
  "allowPty": false,
  "network": {
    "allowedDomains": ["api.anthropic.com", "github.com"],
    "deniedDomains": []
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg", "~/.aws/credentials"],
    "allowWrite": [".", "/tmp"],
    "denyWrite": []
  }
}
```

| Option | Default | Purpose |
|--------|---------|---------|
| `allowPty` | `false` | Enable pseudo-terminal access for interactive tools |
| `network.allowedDomains` | `[]` | Domains to allow network access |
| `filesystem.allowWrite` | `[]` | Paths to allow write access |
| `filesystem.denyRead` | `[]` | Paths to block read access |

### Network Allowlist Strategy

**The GitHub question:** Many examples include `github.com` by default. Understand why before blindly copying:

| Reason to allow GitHub | When needed |
|------------------------|-------------|
| Git-based dependencies | Cargo git deps, Go modules, npm git refs |
| Beads sync | `bd sync` pushes work state to remote |
| Code search | Looking up OSS implementations |

| Reason to block GitHub | Consideration |
|------------------------|---------------|
| Exfiltration surface | Domain fronting allows data to reach any GitHub-hosted endpoint |
| Not always needed | Pure registry deps (crates.io, npm) don't need GitHub |
| Context7 alternative | For docs/code lookup, Context7 is more focused |

**Recommendation:** Start with minimal allowlist, add GitHub only if builds fail on git-based deps or you need beads sync.

### Minimal vs Full Allowlists

**Minimal (no GitHub) — prefer when possible:**

```json
"allowedDomains": [
  "api.anthropic.com",
  "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
  "static.rust-lang.org"
]
```

**With GitHub (when git deps or beads needed):**

```json
"allowedDomains": [
  "api.anthropic.com",
  "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
  "github.com", "*.github.com",
  "static.rust-lang.org",
  "*.cloudfront.net"
]
```

### Ecosystem-Specific Allowlists

**Rust (minimal):**
```json
"allowedDomains": [
  "api.anthropic.com",
  "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
  "static.rust-lang.org"
]
```

**Go (minimal):**
```json
"allowedDomains": [
  "api.anthropic.com",
  "proxy.golang.org", "sum.golang.org", "storage.googleapis.com",
  "gopkg.in"
]
```

**Node/TypeScript (minimal):**
```json
"allowedDomains": [
  "api.anthropic.com",
  "registry.npmjs.org", "*.npmjs.org"
]
```

**Add GitHub to any of the above if:**
- Build fails fetching git-based dependencies
- You need `bd sync` for beads state persistence

### MCP in Sandbox (Context7, Brightdata)

The official context7 plugin is an MCP wrapper (`npx @upstash/context7-mcp`), so it has the same requirements as any MCP:

**To enable MCP in sandbox:**
```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "context7.com", "*.context7.com",
      "api.upstash.com"
    ]
  },
  "filesystem": {
    "allowWrite": [
      ".",
      "~/Library/Caches/claude-cli-nodejs"
    ]
  }
}
```

Then run **without** `--strict-mcp-config`:
```bash
srt -s .srt.json -c 'claude --dangerously-skip-permissions \
  --no-session-persistence \
  -p "prompt"'
```

**Tradeoff:** Context7 gives better docs lookup than GitHub search, but requires MCP cache writes. For pure build/test tasks, skip MCP entirely.

---

## Interactive Mode (allowPty)

**Key discovery:** Interactive CLI tools require pseudo-terminal access.

### The Problem

Running interactive tools (like Claude Code in interactive mode) fails with:
```
setRawMode failed with errno: 1
```

### Why It Happens

On macOS, `sandbox-exec` blocks `/dev/ptmx` and `/dev/ttys*` by default. Interactive CLI tools need these for:
- Raw terminal mode (keyboard input handling)
- Terminal UI rendering
- Signal handling (Ctrl+C, etc.)

### The Solution

Add `"allowPty": true` to your srt config:

```json
{
  "allowPty": true,
  "network": {
    "allowedDomains": ["api.anthropic.com"]
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg", "~/.aws/credentials"],
    "allowWrite": [".", "/tmp"]
  }
}
```

### When to Use

| Mode | `allowPty` | Use Case |
|------|------------|----------|
| Interactive | `true` | Human-in-the-loop Claude sessions |
| Batch/Autonomous | `false` (default) | CI/CD, one-shot prompts |

**Security note:** PTY access is lower risk than network/filesystem—it only affects terminal I/O, not data exfiltration.

### Documentation Gap

The `allowPty` option is:
- Not documented in the srt README
- Not shown in `srt --help`
- Only visible in source code (`sandbox-manager.ts`, `macos-sandbox-utils.ts`)

This is a common gotcha when setting up interactive sessions.

---

## Claude Stateless Flags

For sandboxed Claude runs, disable state writes:

```bash
claude --dangerously-skip-permissions \
       --no-session-persistence \
       --strict-mcp-config --mcp-config '{"mcpServers":{}}'
```

| Flag | Purpose |
|------|---------|
| `--dangerously-skip-permissions` | No permission prompts (srt handles safety) |
| `--no-session-persistence` | Don't write to `~/.claude.json` |
| `--strict-mcp-config --mcp-config '{...}'` | No MCP servers (avoids log writes to `~/Library/Caches/`) |

**Why disable MCP?** Claude writes MCP logs to `~/Library/Caches/claude-cli-nodejs/`. Sandboxing this requires broad write access. Simpler to disable for autonomous runs.

---

## Example Configs

### Project-Specific `.srt.json`

For a Rust project (minimal — no GitHub):

```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
      "static.rust-lang.org"
    ]
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg", "~/.aws/credentials"],
    "allowWrite": [
      ".",
      "~/.cargo/registry",
      "~/.cargo/git",
      "/tmp"
    ]
  }
}
```

If builds fail on git-based deps, add: `"github.com", "*.github.com", "*.cloudfront.net"`

### With Beads Sync

If you need `bd sync` to push work state:

```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
      "static.rust-lang.org",
      "github.com", "*.github.com"
    ]
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg", "~/.aws/credentials"],
    "allowWrite": [
      ".",
      "~/.cargo/registry", "~/.cargo/git",
      "/tmp"
    ]
  }
}
```

**Alternative:** Skip `bd sync` in autonomous runs and sync manually after review. This keeps GitHub out of the allowlist.

### DX Testing Config

For stress-testing skills in `/tmp` (multi-ecosystem):

```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
      "static.rust-lang.org",
      "registry.npmjs.org", "*.npmjs.org",
      "proxy.golang.org", "sum.golang.org", "storage.googleapis.com",
      "pypi.org", "*.pypi.org", "files.pythonhosted.org"
    ],
    "deniedDomains": []
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg"],
    "allowWrite": [
      "/tmp",
      "~/.cargo/registry", "~/.cargo/git",
      "~/.npm", "~/.cache/go-build",
      "~/.cache/uv",
      "~/.claude/session-env"
    ],
    "denyWrite": []
  }
}
```

**Note:** `~/.claude/session-env` is required for Claude to execute bash commands even with `--no-session-persistence`. Without it, subagent bash commands fail with EPERM.

No GitHub in DX testing config. Add only if tests specifically need git-based deps.

### With Context7 (MCP enabled)

For tasks needing documentation lookup:

```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "context7.com", "*.context7.com", "api.upstash.com",
      "crates.io", "*.crates.io", "static.crates.io", "index.crates.io",
      "static.rust-lang.org"
    ]
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.gnupg", "~/.aws/credentials"],
    "allowWrite": [
      ".",
      "~/.cargo/registry", "~/.cargo/git",
      "~/Library/Caches/claude-cli-nodejs",
      "/tmp"
    ]
  }
}
```

Run without `--strict-mcp-config` to enable Context7.

---

## Usage Patterns

### One-Shot Task

```bash
srt -s .srt.json -c 'claude --dangerously-skip-permissions \
  --no-session-persistence \
  --strict-mcp-config --mcp-config "{\"mcpServers\":{}}" \
  -p "Build and test the project, report any issues"'
```

### DX Stress Test

```bash
srt -s /tmp/dx-test.srt.json -c 'claude --dangerously-skip-permissions \
  --no-session-persistence \
  --strict-mcp-config --mcp-config "{\"mcpServers\":{}}" \
  -p "Create a Rust CLI in /tmp/test-project following rust-pro patterns.
      Report any toolchain friction or missing patterns."'
```

---

## Optional: Justfile Integration

Add this recipe to a project's justfile for autonomous runs:

```just
# Autonomous Claude (sandboxed, no prompts, batch mode)
ai-auto prompt:
    srt -s .srt.json -c 'claude --dangerously-skip-permissions \
        --no-session-persistence \
        --strict-mcp-config --mcp-config "{\"mcpServers\":{}}" \
        -p "{{prompt}}"'
```

**Note:** For interactive sandboxed sessions, use `/sandbox` in Claude Code instead of srt. The `ai-auto` recipe is for CLI/autonomous runs only.

---

## Limitations & Tradeoffs

| Limitation | Impact |
|------------|--------|
| Domain fronting | Broad allowlists (github.com) have exfiltration surface |
| Linux monitoring | No violation alerts (macOS has real-time notifications) |
| Proxy bypass | Apps ignoring env vars can bypass network filtering |

### Decision Matrix

| Need | Allowlist | Notes |
|------|-----------|-------|
| Pure build/test | Minimal (no GitHub) | Prefer this when possible |
| Git-based deps | Add GitHub | Only if builds fail without it |
| Beads sync | Add GitHub | Or skip sync, review manually |
| Docs lookup | Context7 + MCP cache | Better than GitHub search |
| Web research | Brightdata + MCP cache | Or skip for autonomous builds |

### The GitHub vs Context7 Question

For **information gathering** (docs, code patterns):
- Context7 is more focused and doesn't have exfiltration surface
- Requires MCP cache writes (`~/Library/Caches/claude-cli-nodejs`)
- Worth the tradeoff for research-heavy tasks

For **pure execution** (build, test, lint):
- Skip both GitHub and MCP
- Minimal attack surface
- Claude works from training data + local context

For **beads integration**:
- GitHub required for `bd sync`
- Alternative: Skip sync during autonomous run, sync manually after
- Consider: Is persisting work state during autonomous run worth the exfiltration risk?

---

## Troubleshooting

### "setRawMode failed with errno: 1"

Interactive CLI tools need PTY access. Add to your config:
```json
{
  "allowPty": true
}
```

See [Interactive Mode (allowPty)](#interactive-mode-allowpty) for details.

### "EPERM: operation not permitted"

Check what path is being blocked:
- `~/.claude.json` → Add `--no-session-persistence`
- `~/.claude/session-env/` → Add to `allowWrite` (required for bash execution)
- `~/Library/Caches/claude-cli-nodejs/` → Disable MCP or allow writes
- Project files → Add project dir to `allowWrite`

### Debug Mode

```bash
srt -d -s .srt.json -c 'your-command'
```

Shows sandbox profile and violations.

### Test Write Access

```bash
srt -s .srt.json -c 'touch /path/to/test && echo "write ok"'
```

---

## Quick Reference

```bash
# Install
npm install -g @anthropic-ai/sandbox-runtime

# Run sandboxed command
srt -s config.json -c 'command'

# Run sandboxed Claude (stateless)
srt -s .srt.json -c 'claude --dangerously-skip-permissions \
  --no-session-persistence \
  --strict-mcp-config --mcp-config "{\"mcpServers\":{}}" \
  -p "prompt"'

# Debug mode
srt -d -s config.json -c 'command'
```
