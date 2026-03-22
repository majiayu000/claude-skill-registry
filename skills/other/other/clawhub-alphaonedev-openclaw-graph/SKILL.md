---
name: clawhub
cluster: community
description: "ClaWHub skills marketplace: browse, search, install, rate, review skills. https://clawhub.com"
tags: ["clawhub", "skills", "marketplace"]
dependencies: []
composes: []
similar_to: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "clawhub skills marketplace browse search install discover"
clawhub_install: "clawhub install clawhub"
note: "NOT installed via ClaWHub CLI — registered in Neo4j skill graph only. To activate: clawhub install clawhub"
---

# Clawhub

## Purpose
ClaWHub skills marketplace: browse, search, install, rate, review skills. https://clawhub.com

## Install When Needed
```
clawhub install clawhub
```

## Note
This skill is registered in the Neo4j skill graph for discovery purposes only.
It is **NOT installed** via the traditional ClaWHub methodology.
When a task matches this skill, the agent will inform you to install it if needed.

## When to Use
- When the task requires clawhub capabilities
