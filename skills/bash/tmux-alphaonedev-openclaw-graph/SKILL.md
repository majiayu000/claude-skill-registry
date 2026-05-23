---
name: tmux
cluster: community
description: "Terminal multiplexer: sessions, windows, panes, splits, attach/detach. Critical for Linux/System76 headless ops"
tags: ["terminal", "tmux", "linux", "multiplexer"]
dependencies: []
composes: []
similar_to: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "tmux terminal session window pane split attach detach linux"
clawhub_install: "clawhub install tmux"
note: "NOT installed via ClaWHub CLI — registered in Neo4j skill graph only. To activate: clawhub install tmux"
---

# Tmux

## Purpose
Terminal multiplexer: sessions, windows, panes, splits, attach/detach. Critical for Linux/System76 headless ops

## Install When Needed
```
clawhub install tmux
```

## Note
This skill is registered in the Neo4j skill graph for discovery purposes only.
It is **NOT installed** via the traditional ClaWHub methodology.
When a task matches this skill, the agent will inform you to install it if needed.

## When to Use
- When the task requires tmux capabilities
