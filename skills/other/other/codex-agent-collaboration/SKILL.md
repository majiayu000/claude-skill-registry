---
name: codex-agent-collaboration
description: Delegate coding tasks to Codex AI for implementation, analysis, and alternative solutions. Use when you need a second AI perspective, want to explore different approaches, or need specialized Codex capabilities for complex coding tasks.
---

# Codex CLI Skill

This skill enables Claude Code to execute tasks using OpenAI's Codex AI agent.

## Overview

The `codex-kkp-cli` is a Codex Agent CLI tool, allowing you to:

- Execute coding tasks and get implementations
- Perform code analysis and reviews
- Get alternative solutions and suggestions
- Collaborate with Codex for cross-checking implementations

## Usage

### Basic Syntax

```bash
# Direct call with platform-specific executable
executables/codex-kkp-cli-{platform} --cd=/absolute/path/to/project [options] "<task_description>"
```

Where `{platform}` is one of:
- `macosx64` - macOS Intel (x86_64)
- `macosarm64` - macOS Apple Silicon (ARM64)
- `linuxx64` - Linux x86_64
- `linuxarm64` - Linux ARM64
- `mingwx64` - Windows x86_64

**Platform Auto-Detection Helper**: A platform detection script is provided to help identify your current platform:

> On Windows, Just use mingwx64 platform directly, no need to use script detection.

```bash
# Unix/Linux/macOS
codex-kkp-cli-platform
# Outputs: macosx64, macosarm64, linuxx64, or linuxarm64
```

### communication

This is AI-to-AI communication between You and Codex. PRIORITIZE ACCURACY AND PRECISION over human readability.
Use structured data, exact technical terms, full paths, and precise details. NO conversational formatting needed.

### Required Parameters

| Parameter    | Description                                                |
|--------------|------------------------------------------------------------|
| Task         | The task description (positional argument, must be quoted) |
| `--cd=<dir>` | Working directory (ABSOLUTE PATH REQUIRED)                 |

### Optional Parameters

| Parameter                      | Description                                                                    |
|--------------------------------|--------------------------------------------------------------------------------|
| `--session=<id>`               | Session ID (STRONGLY RECOMMENDED for follow-up chats to maintain context)      |
| `--sandbox=<mode>`             | Sandbox mode. Default is `read-only`. See [sandbox-modes.md](sandbox-modes.md) |
| `--full-auto`                  | Allow Codex to edit files automatically                                        |
| `--image=<path>`               | Include an image file (ABSOLUTE PATH, can repeat)                              |
| `--skip-git-repo-check[=BOOL]` | Skip Git repository check. Default is `true`. Use `=false` to enable Git check |

For output options (`--full`, `--output-last-message`, `--output-schema`), see [outputs.md](outputs.md).

NOTE that parameters and values are connected by an EQUAL SIGN `=`, not a space.

## Response Format

Returns JSON with `"type": "SUCCESS"` or `"type": "ERROR"`.

```JSON
{
  "type": "SUCCESS",
  "session": "xxxxxxx",
  "content": {
    "agentMessages": "I've analyzed the code and found...",
    "fileChanges": [...],   // Optional
    "nonFatalErrors": [...] // Optional
  }
}
```

- `fileChanges` and `nonFatalErrors` is nullable.
- Error responses do NOT include a `session` field.

## Quick Example

New Session:

```bash
executables/codex-kkp-cli-{platform} --cd=/path/to/project "Explain the main function in Main.kt"
```

Continue Previous Session:

```bash
executables/codex-kkp-cli-{platform} --cd=/path/to/project --session=xxxxxxx "Explain the main function in Main.kt"
```

More examples: [examples.md](examples.md)
