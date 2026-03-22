---
name: showboat
tier: skill
type: tool
protocol: SHOWBOAT
aliases: [showboat, demo-builder, agent-demo]
audience: ["devs", "agents"]
platforms: ["macos", "linux", "windows"]
author: Simon Willison
license: Apache-2.0
related: [datasette, cursor-mirror, sister-script, play-learn-lift]
tools:
  required: [terminal]
  optional: [read_file, web_search]
invoke_when:
  - "Agent needs to demonstrate a feature it built"
  - "Need shareable proof that code works"
  - "Building a tutorial from real execution"
  - "Want real-time progress view of agent work"
---

# Showboat: Agents Demonstrate Their Work

> *"I never trust any feature until I've seen it running with my own eye."*
> -- Simon Willison

Showboat is a CLI tool that helps coding agents construct Markdown documents
demonstrating exactly what their code can do. Each section is built from real
command execution -- not hallucinated output.

## Quick Start

```bash
# No install needed -- uvx runs it directly
uvx showboat --help

# Build a demo document
uvx showboat init demo.md "My Feature Demo"
uvx showboat note demo.md "Here's what the feature does:"
uvx showboat exec demo.md python "python my_script.py --example"
uvx showboat image demo.md "python make_chart.py && echo chart.png"
```

The `--help` text teaches an agent everything it needs. Tell your agent:

> Run "uvx showboat --help" and then use showboat to create a demo.md
> document describing the feature you just built.

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `init` | Start a new document with title | `showboat init demo.md "Title"` |
| `note` | Add prose text | `showboat note demo.md "Explanation..."` |
| `exec` | Run command, capture output | `showboat exec demo.md bash "ls -la"` |
| `image` | Run command, embed resulting image | `showboat image demo.md "cmd && echo file.png"` |
| `pop` | Remove last section | `showboat pop demo.md` |
| `verify` | Re-run and check outputs match | `showboat verify demo.md` |
| `extract` | Reverse-engineer build commands | `showboat extract demo.md` |

## Real-Time Streaming (datasette-showboat)

Set an environment variable to stream doc fragments to a Datasette instance:

```bash
export SHOWBOAT_REMOTE_URL="https://your-server/-/showboat/receive?token=secret"
```

Every `init`, `note`, `exec`, `image` command will POST updates to that endpoint.
The document updates in the browser in real-time.

## Ecosystem

Showboat works with companion CLI tools through loose conventions:

- **Rodney** (`uvx rodney`): Browser automation -- open pages, click, inject JS,
  take screenshots. Designed for `showboat image`.
- **Chartroom** (`uvx chartroom`): Generate charts from CSV/SQL data.
  Designed for `showboat image`.
- **datasette-showboat**: Datasette plugin that receives streaming updates
  and displays documents in a web UI.

## The "--help as Skill" Pattern

Simon designed `showboat --help` to be a complete instruction set for agents.
This is the same insight as MOOLLM's semantic image pyramid: a single file
(or help text) that tells the LLM everything it needs to operate the tool.

The difference: MOOLLM skills use YAML frontmatter + Markdown body.
Showboat uses CLI help text. Same function, different format.

## cursor-mirror Integration

Showboat can demo cursor-mirror features with real output:

```bash
uvx showboat init demo.md "cursor-mirror Status Report"
uvx showboat exec demo.md python "scripts/cursor_mirror.py status"
uvx showboat exec demo.md python "scripts/cursor_mirror.py list-workspaces -n 5"
uvx showboat exec demo.md python "scripts/cursor_mirror.py tail @1 -n 3"
uvx showboat note demo.md "Feature flag drift detected:"
uvx showboat exec demo.md python "scripts/cursor_mirror.py status-features"
```

This produces a shareable Markdown document proving cursor-mirror works
against your actual Cursor installation, with real data.

## Key Design Decisions

- **CLI, not library**: agents run shell commands; showboat is a shell command
- **Markdown output**: renderable anywhere (VS Code, GitHub, Datasette)
- **exec captures real output**: can't fake it (though agents try -- Simon filed a bug)
- **172 lines of Go**: small, fast, single binary
- **uvx for zero-install**: `uvx showboat` works immediately

## About

Created by Simon Willison (Feb 2026). Go binary with Python wrapper.
Part of his "How I use LLMs" series.

- Source: https://github.com/simonw/showboat
- Blog: https://simonwillison.net/2026/Feb/10/showboat-and-rodney/
- Ecosystem: https://simonwillison.net/2026/Feb/17/chartroom-and-datasette-showboat/

## Part of MOOLLM

This is a MOOLLM skill. See the [MOOLLM README](../../README.md) and
[skills index](../README.md) for context.
