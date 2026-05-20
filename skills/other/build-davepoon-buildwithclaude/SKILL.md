---
name: build
description: Autonomous app-building skill — transforms plain-English descriptions into fully built, tested, and deployed applications via a 9-phase pipeline
---

# Shipwright Build Skill

Provides autonomous application building capabilities:

- **9-Phase Pipeline**: Requirements, scaffold, implement, test, lint, security, docs, verify, deploy
- **4 Stacks**: Next.js + TypeScript + Tailwind, FastAPI + Python, Express + TypeScript, Static HTML/CSS/JS
- **Enterprise Safety**: Pre-commit validation, test coverage enforcement, security audit gates, lint-clean guarantees

## When Loaded

This skill is automatically injected when working with:

- `/shipwright:build` — Build a new app from description
- `/shipwright:enhance` — Add features to existing project
- `/shipwright:stacks` — List available stacks
- `/shipwright:projects` — Manage Shipwright projects
