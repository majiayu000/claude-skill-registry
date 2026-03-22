---
name: sonoscli
cluster: community
description: "Sonos speaker control: play/pause/volume/group/ungrouped, queue management, line-in, TTS inject"
tags: ["sonos", "speakers", "audio", "home"]
dependencies: []
composes: []
similar_to: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "sonos speaker play pause volume group queue tts home audio"
clawhub_install: "clawhub install sonoscli"
note: "NOT installed via ClaWHub CLI — registered in Neo4j skill graph only. To activate: clawhub install sonoscli"
---

# Sonoscli

## Purpose
Sonos speaker control: play/pause/volume/group/ungrouped, queue management, line-in, TTS inject

## Install When Needed
```
clawhub install sonoscli
```

## Note
This skill is registered in the Neo4j skill graph for discovery purposes only.
It is **NOT installed** via the traditional ClaWHub methodology.
When a task matches this skill, the agent will inform you to install it if needed.

## When to Use
- When the task requires sonoscli capabilities
