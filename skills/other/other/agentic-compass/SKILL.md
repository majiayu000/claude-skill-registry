---
name: agentic-compass
version: 1.0.0
description: Navigation and decision-making framework for autonomous agents.
metadata:
  openclaw:
    emoji: 🧭
    category: productivity
---

# Agentic Compass

Navigation and decision-making framework for autonomous agents.

## Purpose

Helps agents make decisions about:
- Which skill to use
- When to ask for clarification
- How to prioritize tasks
- When to escalate to user

## Decision Matrix

| Situation | Action |
|-----------|--------|
| High confidence + Low risk | Execute autonomously |
| Low confidence + Low risk | Try, report outcome |
| High confidence + High risk | Ask for confirmation |
| Low confidence + High risk | Ask before acting |

## Usage

Use this skill when facing ambiguous situations requiring judgment calls.
