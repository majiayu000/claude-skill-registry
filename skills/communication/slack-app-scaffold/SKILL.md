---
name: slack-app-scaffold
description: "Scaffold Slack apps from existing functionality using Bolt for JavaScript and the Slack CLI. Use when turning a service, script, or workflow into a Slack app with events, commands, modals, or automations."
---

# Slack App Scaffold

Bolt for JavaScript + Slack CLI is the 2026 default. Optimize for fast local runs, clear handlers, and safe deploys.

## Stack (Default)

- Runtime: Node.js (LTS)
- Framework: `@slack/bolt`
- Tooling: Slack CLI (`slack`)
- Config: Slack manifest via CLI-generated project

## Core CLI Commands

```bash
# Create new Slack app project
slack create my-slack-app

# Run locally (socket mode / dev env)
cd my-slack-app
slack run

# Deploy to Slack-hosted runtime / target env
slack deploy
```

## Workflow (CLI-First)

1. Identify integration points in existing functionality.
2. Scaffold app with `slack create`.
3. Model capabilities in the manifest (scopes, events, commands, interactivity).
4. Implement handlers in Bolt (events, commands, actions, views/modals).
5. Run locally with `slack run` and validate in a dev workspace.
6. Deploy with `slack deploy`.

## Project Structure (Typical)

```text
my-slack-app/
├── app/
│   ├── app.js              # Bolt app bootstrap
│   ├── listeners/          # Events, commands, actions, views
│   ├── services/           # Integration layer to existing functionality
│   └── middleware/         # Auth, validation, shared guards
├── manifest.json           # Slack app manifest (CLI-managed)
├── package.json
└── README.md
```

Design rule: keep Slack handlers thin; push real work into `services/`.

## Common Use Cases

- Notifications: post messages from existing jobs or webhooks.
- Slash commands: wrap existing scripts or APIs behind `/commands`.
- Workflows: compose multi-step flows with Slack-native triggers.
- Modals: collect structured input, then call existing systems.

## Implementation Notes

- Map each Slack surface to one listener module.
- Normalize inputs at the edge; pass clean DTOs inward.
- Acknowledge fast (`ack()`), then do work.
- Centralize Slack Web API calls behind a small service.

See `references/bolt-patterns.md` for concrete patterns.

## Verification Steps

```bash
# 1) Install deps
npm install

# 2) Run locally
slack run

# 3) Lint/test if present
npm test

# 4) Deploy
slack deploy
```

Manual checks in Slack workspace:
- Trigger each command or event once.
- Validate permissions/scopes match what handlers need.
- Confirm errors surface as user-visible messages, not silent failures.
