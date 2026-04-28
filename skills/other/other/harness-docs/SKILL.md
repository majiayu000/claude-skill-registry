---
name: harness-docs
description: Harness Kit documentation — installation, plugin catalog, creating plugins, cross-harness setup, architecture, and FAQ. Use when working with or configuring harness-kit plugins, understanding the plugin/skill system, installing slash commands, setting up AI coding tool configuration, answering questions about the plugin marketplace, writing SKILL.md files, using harness.yaml, or integrating with Copilot, Cursor, or Codex. Do NOT use for general Claude Code questions unrelated to harness-kit.
user-invocable: false
---

# Harness Kit Documentation

harness-kit is a harness-agnostic framework for AI coding tools. Plugins, skills, MCP servers, hooks, and conventions live in one portable config. It works with Claude Code today and is designed to travel across tools.

**Repo:** https://github.com/harnessprotocol/harness-kit  
**Docs:** https://harnesskit.ai/docs

## How to Use This Skill

This is a background knowledge skill. When the user asks about harness-kit, load the relevant reference file from `${CLAUDE_SKILL_DIR}/references/` and answer from it.

| Topic | Reference file |
|-------|---------------|
| Installation, architecture, quick start | `getting-started.md` |
| Plugin list, what each plugin does | `plugin-catalog.md` |
| Creating plugins, writing SKILL.md, frontmatter | `creating-plugins.md` |
| Using with Copilot, Cursor, Codex | `cross-harness.md` |
| Core concepts, FAQ, harness.yaml, comparison with MCP/A2A | `concepts-and-faq.md` |

Load with: `Read ${CLAUDE_SKILL_DIR}/references/<filename>.md`

## Quick Reference: 16 Plugins

| Plugin | Slash command | What it does |
|--------|---------------|-------------|
| research | `/research` | Process any source (URL, GitHub, YouTube, PDF) into a structured knowledge base |
| orient | `/orient` | Topic-focused session orientation across knowledge graph and research |
| capture | `/capture` | Capture session info into a staging file for later reflection |
| review | `/review` | Structured code review for branches, PRs, or file paths with severity labels |
| explain | `/explain` | Layered explanations of files, functions, directories, or concepts |
| lineage | `/lineage` | Column-level lineage tracing through SQL, Kafka, Spark, JDBC |
| docgen | `/docgen` | Generate or update README, API docs, architecture overview, or changelog |
| open-pr | `/open-pr` | Pre-flight checks and PR creation: tests, review, CI |
| merge-pr | `/merge-pr` | Merge a ready PR: verify CI, sync base, squash merge, clean up |
| pr-sweep | `/pr-sweep` | Cross-repo PR sweep: triage, review, merge, fix CI |
| harness-share | `/harness-export`, `/harness-import` | Compile, export, import, and sync harness configs across AI tools |
| stats | `/stats` | Interactive HTML dashboard for Claude Code token and session usage |
| iterm-notify | — | macOS desktop notifications and iTerm2 badge management for Claude Code events |
| board | `/board` | Kanban project board with real-time Claude-to-web sync via MCP |
| frontend-design | `/frontend-design` | Production-grade frontend design rules: OKLCH color, typography, motion, accessibility |
| membrain | `/membrain` | Graph-based agent memory — search, trace, and manage a persistent knowledge graph |

## Key Concepts

**Skill** — A `SKILL.md` file: the workflow Claude reads when you type a slash command.  
**Plugin** — The package wrapping a skill: a directory with `plugin.json`, the skill, optional scripts, hooks, and agents.  
**harness** — Your complete AI tool setup: CLAUDE.md, plugins, MCP servers, hooks, permissions.  
**harness.yaml** — A portable snapshot of your complete harness. Export with `/harness-export`, restore with `/harness-import`.

## Install

```
/plugin marketplace add harnessprotocol/harness-kit
/plugin install <plugin-name>@harness-kit
```
